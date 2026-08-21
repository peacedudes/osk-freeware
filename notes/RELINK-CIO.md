# Relinking the trap-free builds against cio

Written 2026-08-19.

## Why

199 programs on this disk were rebuilt `-qm` — trap-free, stdio linked into
each binary — because at the time it was not known that Microware would permit
`cio`, `csl`, `csl020`, `math` and `math881`. Permission came on 2026-08-16 and
those five are now in `disk/CMDS`, so the reason for `-qm` has expired. The
cost has not: a trap-free `wc` is 14,978 bytes and the cio-linked one is 1,430.

## What was measured

`tools/rebuild/relink_cio.sh` rebuilds each one with `-qixm` in place of
`-qm`, mirroring `tools/rebuild/rebuild.sh` in every other respect.

    198 programs attempted
    174 rebuilt
     21 failed to build
      3 have no source tree at all

    174 rebuilt: 4,083,098 -> 1,905,744 bytes, a saving of 2,177,354 (53.3%)

The saving is not even. Small utilities shrink dramatically — stdio is most of
their bulk — while a large program like `vi` drops only 5%. Extrapolating from
the biggest programs would have badly underestimated the total; extrapolating
from `wc` would have badly overestimated it.

## Smaller is not better if it is broken

Every rebuild was run against the binary it would replace, same input, and the
two captures compared (`tools/rebuild/compare_relink.sh`).

    SAME         104   byte-identical output
    DIFFERENT     42   re-checked on a shorter prefix, see below
    BOTH-QUIET    17   neither printed anything -- NOT installed
    NEW-SPEAKS    10   old printed nothing, new works -- an improvement
    NEW-BROKEN     1   installed nowhere

**`calen` is the NEW-BROKEN one.** The binary on the disk prompts
`Enter calendar specs (month year length):`; its relinked build prints nothing
at all, at 7,146 bytes against 21,486. It is exactly the shape of `wc.cio`,
which is 10× smaller than the trap-free `wc` and silently does nothing for a
file argument. Two out of roughly 180 is a low rate and a completely
sufficient reason to test every one individually rather than trusting the
size.

**NEW-SPEAKS was a bad rule, and it cost six programs.** It treated ANY
output from the new binary as an improvement. `No more memory !!!` is output,
and it is os9exec refusing to give the process its static storage — strictly
worse than the silence it replaced. Six of the ten so scored regressed this
way: `m4`, `ifdef`, `pageline`, `sepwords`, `casefix`, `input`. All six were
reverted from git.

**Root cause, traced 2026-08-19.** The cio-linked build calls `F$SRqMem` for
`$4FB68` — 326,504 bytes — and os9exec returns `E_NORAM`, whereupon the
program retries the identical request forever, printing the message each time.
The trap-free build never makes that request: cio's allocator asks for one
large arena where the statically linked stdio does not. It is not the module
header — `m4`'s new `M$Mem` is 14,992 against the old 16,974, i.e. it asks for
*less*.

Raising `-qixm` from 16k to 32k to 64k changed neither the binary size nor the
behaviour, so that flag is not the lever.

**os9exec's memory options DO parse — the earlier claim was wrong, and it was
mine.** `notes/HANDOFF.md` records `-m`/`-M` as failing with `Error in decimal
number` naming the program, and I reproduced that and repeated it. It is a
QUOTING mistake, not a defect. `os9main.c` takes the number as the **next argv
element** (`getlnum:` does `k++; p = argv[k]`), so the value must be a separate
argument:

    os9exec -r -m 64k m4        works -- parses, runs
    os9exec -r -m=64k m4        fails -- `=64k' is not a number
    os9exec -r "-m 64k" m4      fails -- one argument, not two

`-m`, `-mm` and `-M` were all confirmed working this way. **`notes/HANDOFF.md`
is wrong on this point and should be corrected.**

None of them helps here, though: `-m 512k`, `-mm 512k`, `-M 64M` and `-M 128M`
all still give `No more memory !!!`. The failing call is `F$SRqMem` for 326,504
bytes, which os9exec answers from `os9malloc()` rather than from the static
storage `-m` adjusts or the arena `-M` sizes. So the cause is understood, the
lever is not `-m`/`-M`, and the six keep their trap-free builds -- which work. The other two NEW-SPEAKS, `pagefraz` and `pagekwic`, print
`word too long in line 0`, which is the program working on empty input, and
`valspeak` and `ape` print nothing at all now — their "speaks" was transient.

**Every installed binary was then audited by running it**, looking for the
failure modes a size comparison cannot see: `No more memory`, `E_BMID`,
`E_NEMOD`, `User Trap`, `Illegal instruction`, `BUSERR`. Of 117 installed,
**111 ok and 6 NO-MEMORY** — the same six, and no faults anywhere else. That
audit is the check that should have run before installing rather than after.

**BOTH-QUIET is not a pass.** Seventeen programs printed nothing either way.
That is no evidence the rebuild works, so none of them was installed. An
earlier verifier in this collection reported 20/20 OK having run nothing at
all, and the lesson stuck.

**DIFFERENT is mostly an artefact of the capture**, not of the programs. The
comparison takes the first 2,000 bytes, and a full-screen program that draws
continuously gets cut at a different point on each run. `sedt` is the type
case: old and new emit the same escape sequences, the same `File:` banner and
the same ruler, and differ only past the cut. Those are re-checked on the
first 400 bytes and installed only if that prefix matches exactly.

## What was installed

    118  passed the comparison in the dry run
    111  installed and verified by running (117 installed, 6 reverted)
         (one DIFFERENT re-check flipped between runs -- full-screen
         programs do not draw byte-identically every time, and the installer
         is deliberately the stricter of the two)
     57  skipped
      1,455,706  bytes reclaimed

Disk tree 99M -> 96M; the built image 194M -> 190M.

**The `.nocio` copies were NOT kept.** Keeping a trap-free copy of each
replaced binary made the tree *larger* — 117 copies is 2.5 MB against
1.46 MB reclaimed — which defeats the point. Git holds every one of them, so
`git show <commit>:disk/CMDS/<prog>` recovers any single binary exactly. The
four from the earlier hand-checked swap (`cat`, `basename`, `dirname`,
`strings`) are kept, because `DOC/INDEX` documents them as an alternative for
somebody who removes the Microware modules.

## One regression, caused and caught

**`tar` must never be relinked, and I relinked it.** `mkimage.sh` populates
the image using the collection's *own* `tar`, which is why the header says the
build needs no Microware software at all. The relinked `tar` requires `cio`.
Nothing detected this by inspection — the next image build simply failed with
`tar extracted 0 files, expected 5596`, because the test image deliberately had
the five modules removed.

`tar` was reverted from git. `sh`, the only other program `mkimage.sh`
depends on, was not relinked and needs nothing.

**The rule this leaves:** anything the image build itself runs is off limits
to this exercise, and the way to prove it is to build an image with the five
Microware modules absent. That is now a two-minute check and it should be run
after any future relinking.

## The 21 that would not build, by cause

  - **`/dd/LIB/strings.r` missing — 4** (`digclk`, `hang`, `screen`,
    `sokoban`). Not in the SDK and not anywhere in the pool.
    **RESOLVED 2026-08-20: they do not need it.** The recipes name it because
    the trap-free build did; the cio-linked build gets those symbols from cio.
    Dropping `-l=/dd/LIB/strings.r` builds all four, and each behaves
    identically to the binary it replaces when run in a login session — the
    differences seen bare were only two different ways of saying `no TERM`.
    Installed, **40,656 bytes** reclaimed.
  - **Missing headers, and the source trees are incomplete — 7**
    (`convert`, `sonnet`, `gen`, `if`, `run`, `patch`, `pdraw`). `convert`
    wants `parame.inc`, `sonnet` wants `lex.i`, `gen` wants `../defs/misc.h`.
    **`parame.inc` and `lex.i` do not exist in the pool at all**, so those
    trees were captured incompletely and cannot be built by anybody.
  - **Unresolved symbols — 7.** `bcopy` (`bmgtest`, `bmgtest2`), `getpwuid`
    (`lp`, `lpq`), `xmalloc` (`diff`), `standby` (`pep`), `_gs_sopt`
    (`devprc` — that one is `getsys.a`, which the recipe omits; `devprc` was
    rebuilt separately and correctly earlier the same day).
  - **Duplicate symbols — 2** (`rain`, `worms`), from linking `math.l`
    alongside their own definitions.
  - **`chess` — 1**, compilation errors in its own source.

Several of the unresolved-symbol cases are probably fixable by adding a source
file from `SRC/unixlib`, the way `devprc` took `perror.c` from there. That is
the obvious next increment and it was not attempted.

## Two bugs in the driver, both found by making it fail

- **os9exec inside a `while read` loop eats the loop's own stdin.** The first
  run processed 2 of 198 rows and then began treating fragments of recipe
  lines as program names. `< /dev/null` on the emulator call fixes it. This
  collection's own notes already warn about the same trap in a different
  script; it was rediscovered anyway.
- **The include path.** Without `-V=/h7` for the COMPAT shims, `yacc` stops at
  `can't open /dd/defs/assert.h`; without `math.l` linked, `wanderer` fails on
  `_T$LtoD`. `rebuild.sh` had both right and the first draft of the new driver
  did not copy it closely enough.

## What is kept

Only the four hand-checked ones from the earlier swap keep a `.nocio` copy on
the disk. For the other 117, git is the record: `git show 326dbd7^:disk/CMDS/<prog>`
returns the trap-free binary byte for byte. See "What was installed" above for
why keeping all of them on the disk was the wrong call.
