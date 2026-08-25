# For rdoggett, on your return

One file, one place to look. Branch **`release-pass-2026-08-21`**, off `main`,
nothing pushed. Every commit made with the `check_disk.py` checks green.

Newest first. The 2026-08-21 pass is below the 2026-08-22 one and still
stands — nothing in it was undone.

---

# 2026-08-24, later — ls rebuilt and adopted; gtar creates; C++ runs

**Two things need you. Both are one-liners.**

**1. ~~Do you still have the h0 workshop disk?~~ Withdrawn — I was asking the
wrong question.** Three of those four were never our builds. `cat`, `basename`
and `dirname` are **byte-for-byte identical** to the binaries in Martin
Gregorie's `sh75` package, which is already in your pool at
`Scraped/os9/PUBCMDS/microware/sh75/CMDS`. The star grid had been saying so all
along: all three need `cio`, which a rebuild against os9lib would have removed.
`DOC/INDEX` is corrected.

That leaves **`wc` alone** — 14978 bytes. Its source is not in this repo, not
in the pool, and there is no second `wc` in the pool either. The binary gives
nothing away: no banner, no version, no author, no build path; its only
printable strings are `%7ld` and ` %s`. Running it with a bad option just says
`wc: unknown option`.

And its provenance is now doubtful too. It is **starred** — it needs `cio` —
and a gcc2 build made here links `clibn` and needs none, which is why `ls` is
not starred. So "REBUILT HERE with gcc2" is probably as wrong as the claim
about the other three was. `DOC/INDEX` now says the provenance is unsettled
rather than asserting either way.

**If you have a copy, the bytes matter less than where it sits.** Point me at
the path and I will compare it with ours and read whatever is around it — a
README, the archive name, the directory it came from. That is where provenance
lives, and it is the only thread left.

**2. Five files in `/dd/CMDS`, or a script, or documentation?** My earlier
"two byte copies and C++ works" was WRONG -- I proved it in the build overlay,
which has a flat `CMDS` and the SDK headers, and the disk has neither. You
caught it by asking whether a rename would do.

What is actually true, now measured on the disk: `gcc2` and `gpp` find their
passes by a hardcoded prefix, and it is a DIFFERENT prefix for each --
`/dd/CMDS/gcc_<pass>` and `/dd/CMDS/gpp_<pass>`. The passes ship in
`/dd/CMDS/GCC2`, which is neither, so `gcc2` cannot fork `cccp2` and **plain
C fails exactly like C++ did**. And `r68`, `l68`, `clibn.l` and `cstart.r` are
Microware's, so an SDK is needed regardless -- that part cannot be fixed here.

With those in place both compilers work: C and C++ each compiled, linked and
RAN on the disk, 2026-08-24.

Already landed: `DOC/README-GCC` with the whole procedure, the `DOC/INDEX`
rationale corrected (its own reasoning is what caused this), and
`DEFS/GCC2/stdio.h` fixed -- it forwarded to `/dd/DEFS/stdio.h`, which is
Microware's and not on the disk, so nothing including `<stdio.h>` could
compile at all.

**The open question is only packaging**: ship the five files (`gcc_cccp2`,
`gcc_cc2`, `gpp_cccp`, `gpp_cc1plus`, `gpp_collect`, about 1 MB, `cccp2`
twice), or one `gccsetup` script that makes them, or leave README-GCC to it.
I would ship the five. Nothing done -- `disk/CMDS` is yours.

**`ls` now builds from `SRC/ls` and is installed.** You said same-or-better or
not at all. Measured against your binary over 40 option cases — `-l -lt -lS
-lR -C -x -m -1 -a -F -d -p -s -k -Q -b -o -g -n -w -T --full-time --help`,
two directories at once, a missing file, and the whole of `/dd/CMDS`:

    39 of 40 byte-identical
     1 better:  ls -i printed 0 for every inode.  It prints real ones now.

Three things were wrong and all three are in the source, marked and dated:

  - `os9stubs.c` fabricated `stat`/`fstat` — one mode for every file, no date.
    os9lib has real ones. Deleted ours; the recipe links `os9lib.l`.
  - os9lib's `stat()` **sign-extends the attribute byte**, so a directory
    (`0xbf`) arrives as `0xffbf`. `system.h` tested it through an `S_IFMT` of
    `0x0380`, matched the sign fill, and `S_ISDIR` was false for every
    directory on the disk — `ls -l /dd/DOC` printed the directory instead of
    listing it.
  - `filemode.c` never included `system.h`, so it rendered OS-9's attribute
    bits with Unix's `0777` layout and printed `d--S--S--T` for every one.

**gtar creates archives correctly now** — the thing that was broken yesterday.
`gtar -cf` over `/dd/SYS`, extracted host-side: **809 files, all byte-identical**,
binaries included. `cc2` no longer dies on `port.c`: os9lib defines `bcopy`,
`bcmp` and `bzero` as macros, and port.c's `USG` block was defining functions
of the same names straight into them.

**I did NOT replace `CMDS/REBUILT/gtar`.** That one is an archive binary and it
already worked — I only thought it did not because yesterday's note said so.
Ours is 130868 bytes against its 113562 and behaves the same, so there is
nothing to gain by swapping it. What is new is that the recipe reproduces it.

**The disk can build C++ now, and that is new.** A class, a constructor, a
method call — compiled, linked and ran. It needed four things nobody had
found: `gcc2` cannot start the C++ front end at all (no `.cc` in its suffix
table), only `gpp` can; `gpp` wants `cccp`; `collect` lives in `CMDS/GCC2`
rather than `CMDS` and nothing links without it once there is a global
constructor; and it opens `gpp.l`. `make_overlay.sh` supplies all of that now
and `rebuild.sh` has a `GPP` flag.

**No recipe uses it yet.** The only C++ in the tree is `homelibr` — six
programs, all six already on the disk as working binaries — and it needs a
port, not a recipe: pre-standard class constants GCC 2.5.6 rejects, and an
`ofstream` that cannot exist here because `LIB/libgpp.l` is libg++ 1.x and has
no stream file classes at all. Written up in `notes/COMPILE-AUDIT.md`. I fixed
one real bug there and stopped: `Include/common.h` had `#include <sgstat.h>`
commented out, which made `Terminal.h` unparseable.

**`aterm` now builds from its assembly source, and the module that comes out
is byte-for-byte the one that ships.** Not "works the same" -- identical, all
13422 bytes. That is the strongest check this machinery has ever produced.
What it needed was two libraries: `os9.l` and `sys.l` resolve all 53 of the
`F$Fork`/`I$GetStt`/`SS_Opt` names, because Microware's assembler definitions
file is not in our SDK copy and `oskdefs.d` here has only the module-type
equates. The other two assembly trees cannot be built at all -- `serload`
wants a `rt_comm` directory that exists nowhere, and `graph`'s six programs
want `graphmakros` and `mathmakros`, likewise nowhere. Both written up.

**The whole tree builds from a clean clone: 289 of 291, one command.**
`tools/build.sh --from-scratch`. The two that fail are `pdraw` (wants X11
headers) and `pep` (wants an EPROM board's assembly); neither is a linkage
problem and both have always failed.

**I stopped quoting the source-coverage number and wrote the tool instead.**
`tools/src_census.py disk` -- 410 of 937, 43%, of which 279 are built by a
recipe. The old 42% was taken by hand in a shell on 2026-08-21 and could not
be re-derived. CLAUDE.md now points at the tool rather than carrying a figure
that goes stale every time a recipe lands.

**Thirty-five more programs build from source now** — 290 recipes to 325, and
279 programs built by one to 313. Eighteen mtools commands, six macutils, the
four elvis helpers, and five singles. Every one compared against your binary
first; the ones that did not match were left out with the reason written down.

**One of those comparisons is worth your time.** `SRC/bix` has a `chown.c`, a
`dir.c` and a `mkdir.c`, each a real program with a `main()`. None of them is
the `CMDS` program of that name — I built all three and compared, and they are
completely different programs. So a source file matching a program's NAME is
evidence and not proof, and any count built on it is soft. `src_census.py`
says that out loud now.

Everything committed on the same branch, all eleven checks green.

---

# 2026-08-24 — gtar builds; and I think I found what ls needs

**gtar reads and extracts real tar archives, byte for byte.** Given a `.tar`
made elsewhere it lists it with correct modes, owners, sizes and dates and
extracts everything identically, including a binary. Someone who downloads a
tarball now has something that opens it.

**Creating archives is wrong and it says so loudly** — `file X shrunk by
720880 bytes, padding with zeros`, on every file. So there is a recipe, but
**do not install it over anything yet**. Cause below.

**Your three K&R edits objection was right and they are gone.** The gtar
source is the archive's own again; gcc2 never needed them.

## The thing worth reading

`LIB/os9lib.l` already has a `stat()` that WORKS — I measured it:

    f1   ino=3108864  size=4   mtime=1787549940
    f2   ino=2079232  size=8   mtime=1787549940     (different inode)
    d1   ino=2318336  size=64  mode=0177677         (directory)

Distinct inodes, real sizes, a real date. It only works when compiled against
**os9lib's own `<stat.h>`** — the library fills os9lib's `struct stat`, and
what everything here has in scope is `DEFS/UNIX`'s. Both are 36 bytes, so
nothing is overrun; the fields just land in the wrong members. That is exactly
why gtar's creation writes nonsense sizes.

**And it is exactly what `SRC/ls/os9stubs.c` fabricates.** So before hunting
the lost ls source in the pool, try the cheap experiment: delete os9stubs.c's
`stat`/`fstat` and let os9lib's be linked instead. If that works, the
collection can rebuild `ls` from what it already ships. I have written the
method into `notes/PLAN-next.md` at the top.

I could not do it for gtar today because gcc2's `cc2` dies on `port.c` once
the os9lib headers are in scope — a compiler bug on one file, and the whole
distance between gtar-as-reader and gtar complete.

---

# 2026-08-23 — ls: it compiles, and you should NOT take it

You said same-or-better or not at all. **It is not better, so I have not
adopted it and there is no recipe.** Here is the comparison, same directory,
one file `chmod 400`, one `chmod 755`, one dated 1993:

    ls -l   YOUR BINARY                       BUILT FROM SRC/ls
            -r--------  a.txt                 bus error, TRAP 2
            -rw-r--r--  b_longer_name.dat
            -rwxr-xr-x  big.bin
            drwxrwxrwx  sub
            real modes, real dates            (bare `ls` also loses columns)

**The old note was right and I can now prove it.** `SRC/ls/os9stubs.c` gives
every regular file one hard-coded mode —

    buf->st_mode = S_IFREG | S_IRUSR | S_IXUSR | S_IROTH;

— and never assigns `st_mtime` at all. Your binary prints per-file modes and
real timestamps, so it was built from a **later source that is on no disk
here**. `disk/SRC/ls` and `play/oskBoot/SRC/ls` are byte-identical and both
pre-fix; there is no other `os9stubs.c` anywhere under `~/Developer/os9`. The
binary is the only surviving artefact of the fixed source.

**So the answer to "people trying this with os9exec need ls" is: they have
it, and it must not be rebuilt from what ships.** If you ever want it from
source, the only broken part is `os9stubs.c`'s `stat()` — it needs `_gs_gfd`
to read the real file descriptor for the attribute byte and the date. The rest
compiles today; the exact recipe is in `notes/SESSION-2026-08-23.md`.

Worth having from the attempt, and all three are committed:

  - **An include cycle in `SRC/COMPAT`** that made cccp2 die with
    `**** Stack Overflow ****` — `COMPAT/stat.h` and a tree's own
    `sys/stat.h` calling each other. Reads like a broken source file; is not.
  - `shims/os9isgraph.c` — `isgraph` is in `csl.l` and nowhere else.
  - **`DEFS/os9lib` is usable from the GCC path** (it is ANSI-era, which is
    why it was a dead end for `c68`). It is the only place on this disk with
    `uid_t` and `S_IRUSR` — **and gtar's missing `TRUE`, `FALSE`, `ERROR` and
    `S_ISUID` are all in it too.** It needs the overlay mounted as `/h0` as
    well; that is one line and it is written down, not in the tree, because no
    recipe needs it yet. First thing to try for gtar.

---

# 2026-08-23 — the GCC flag is built, and mtools builds with it

You told me to do it and I stopped short the first time. Done now.

**`mtools` builds and runs** — 45 sources, the whole DOS-disk toolkit. `mdir -?`
prints the real mtools 3.6 usage; `mdir` reaches for `/pc1@`, the PC floppy
descriptor, which is right when none is configured. The audit had it filed
under "a gcc2 build, same category as `ls`", and that was the end of the
thought.

**The reason nobody got further: the gcc2 on your disk could not compile a
two-line program.** Four headers in `DEFS/GCC2` were inconsistent with the SDK
set underneath them — the worst being `stdio.h`, which was GNU's own, written
against a GNU libio that is not here, and whose own comment said `/* TODO */`.
Any program that so much as named `stderr` failed at the link; printf-only
programs worked, which is why it survived. All four are repaired.

**That very likely explains `ls` being "repaired" rather than rebuilt**, and
why `mtools` and `lua` were written off.

Three things about the flag that cost time and are worth knowing:

  - gcc2 **predefines `_OSK`**, and `-U_OSK` cannot beat it (user options go
    ahead of its own `-D`s, and `-Wp,` is dropped). Anything behind
    `#ifdef _OSK` is unavoidable.
  - The link **cannot be gcc2** — the module would name itself after the
    output file, i.e. `R_mtools`. It runs `l68` underneath anyway, so the path
    calls l68 itself with `-n=`.
  - **`l68` makes one pass per distinct library FILE.** Repeating `-l=x.l`
    buys nothing — I measured five repetitions changing nothing. The failure
    table said otherwise and is corrected; the fix is copies under different
    names.

`lua` and `luac` are much closer but still blocked, and now on absent material
rather than the compiler: 16 of 17 and 17 of 17 sources compile. lua wants an
`ldblib.h` that is in no copy of the tree; luac wants Ultra C's syscall
library. Neither is a recipe.

**Two more marked source fixes, and I claim these are not compiler
workarounds:** mtools' `config.h` claimed `HAVE_STRERROR` (it is `configure`
output from the porter's machine — correcting it is what a config header is
for), and its `sysincludes.h` declared `void atexit()` while its own
`missing_functions.c` defines `int atexit()`. The package contradicts itself.

---

# 2026-08-23 — you asked how these ever compiled. Answer: a different compiler

**They were built with GCC, not Microware's `cc`.** Their own makefiles say so
— `gtar: CC = gcc`, `rayshade: CC = gcc -mlong-calls`, `mtools` and `jpeglib`:
`gcc2`. GCC is ANSI, has no 512-character line limit, and `-mlong-calls` is
exactly the answer to rayshade's huge stack frame. **So most of my source
edits work around the wrong compiler, not broken source.** You were right to
push on it.

Which of the six survive that:

  - **gtar's three K&R conversions** — compiler workaround. Confirmed: under
    gcc2 those files sail past.
  - **rayshade's `MAXMODELDEPTH` and `lex.c free()`** — compiler workaround.
  - **rayshade's `CPPSTDIN`** — stands. A real runtime bug, nothing to do with
    the compiler.
  - **ed's `_SIZE_T` guard** — stands, but it is MY fault: I created that
    conflict by adding `size_t` to `SRC/COMPAT/types.h`. ed really is a `cc`
    build.
  - **macutils** — no source edits, only a driver fix.

**And the thing worth having: the gcc2 on your disk could not compile this.**

    #include <ctype.h>
    #include <stdlib.h>
    main(){return 0;}

Two faults, both in `DEFS/GCC2/stdlib.h`, both now fixed and committed: it
pulled in `<direct.h>` which needs `WORD` from a `stdio.h` that GCC's own
shadows, and it declared `isalnum(char c)` and fifteen more as functions when
`<ctype.h>` defines them as macros. **That is very likely why `ls` was
"repaired" rather than rebuilt, and why `mtools` and `lua` were written off.**
Nobody had tried the disk's gcc2 on something small enough to see why.

It does not rescue gtar — under gcc2 it stops on the same names it stopped on
under `cc` (`TRUE`, `FALSE`, `ERROR`, `S_ISUID`). Two independent routes, same
wall, so "what is left is a port decision" holds either way.

I did **not** build the `GCC` recipe flag. The DEFS repair under it was the
real blocker and that is done; the flag itself needs a way to link long object
lists through `gcc2` (it cannot be `l68` — gcc objects carry their own magic),
and I would rather you saw the finding than a half-built flag.

**If you want the compiler-workaround edits reverted, say so** — with the
gcc2 repair in place they may simply be unnecessary, and I would rather have a
`GCC` recipe than six edits to other people's source.

---

# 2026-08-23 (overnight) — three programs that had never built


**Needs you: one judgement call, at the bottom. Nothing else.**

**`inform`, `djpeg` and `ed` all build now.** None of them ever had. Each was
verified by RUNNING it, not by linking it:

  - **`inform`** — Graham Nelson's Inform compiler, the thing that produced
    everything in `GAMES/INFORM`. `DOC/INDEX` has said for months that our cpp
    aborts on it. It recompiles the collection's own `hellow.inf` to a story
    file **byte-identical to the `hellow.z3` that has shipped since day one.**
  - **`djpeg`** — the JPEG decoder. Verified by round trip against `cjpeg`.
  - **`ed`** — GNU ed. The audit called it an ANSI tree; it is K&R throughout,
    and the de-ANSIfier we run was *destroying* it.

**Two compiler bugs, both measured, both with small reproductions:**

  1. **`cpp` dies on a source line of 513 characters.** That is the whole of
     the "nested macro" bug we have been carrying — nesting is just how a line
     gets long. It explains our own three-file reproduction exactly: the one
     that crashes expands to 542 characters, the two that compile to 270 and
     222. `c68` has a limit too, 1023. **And cpp does not always crash — in
     some shapes it truncates and exits silently**, which is how an earlier
     pass concluded long lines were fine.
  2. **`o68` miscompiles what `c68 -k` emits**, and only in one construct: the
     true arm of `a ? "this" : "that"` on string literals gets an address
     eight bytes wrong. `one ? "Error" : "Warning"` prints `rning`. That is
     what made inform report impossible diagnostics. Ten-case probe; nine
     cases fine.

**The sweep is re-run — 868 of 913, 95.1%** (it was 876 of 925). The number
went up and the count went down, and it reconciles to the unit: eleven of the
fourteen programs you dropped had been working, `about` and `passwd` joined,
and `postprint` started passing. **935 programs were measured in both sweeps
and exactly TWO changed verdict**, neither a regression. `DOC/STATUS` is
updated throughout, not just the tally.

**`rayshade` builds AND RENDERS** — 78 sources over six nested libraries, the
first package build here. And a finding you will care about: **the rayshade
you ship has never been able to render anything.** It pipes every scene
through a preprocessor called `cccp`, which is on no disk here; it says
`Nothing to be rendered` and stops. The disk does carry GNU cpp as
`CMDS/GCC2/cccp2`, so it is a one-word fix in `config.h`, and it is made. The
sweep never caught it because `rayshade` with no arguments prints a usage
message, which scores as working.

**Also:**

  - **`macutils` is unblocked** — the audit's reason (cpp will not search a
    `-V` directory for an include name with a directory in it) was correct and
    is now obsolete, because GNU cpp does. `binhex` and `unsit` build.
  - A driver bug: two sources sharing a BASENAME silently clobbered each
    other's temporaries, and the link then blamed a missing `main`. Fixed.
  - Five of C News's six programs build — that tree had no recipe at all.
  - The whole tree still builds: **287 of 290 recipes clean**, the same three
    known failures (`ls`, `pdraw`, `pep`). Recipes went 277 -> 288 overnight.
    Four whole-tree builds were run, not one — the third caught a fix of mine
    that worked on one recipe and broke another.
  - **`build.sh` was leaving 228 files in `disk/`** while printing "the tree is
    left as it was found". It had its own stale copy of `tidy.sh`. It calls the
    real one now.
  - **The `strchr(s,0)` grep you wanted is done.** The guidance was too broad:
    `unix.l`'s `strchr` is *correct*; it is `index`, `rindex` and `strrchr`
    that fail on NUL. Only pdksh is exposed and **all six of its sites are
    already patched**. Nothing to do.
  - `mtools` is not a timeout and never was — it is a `gcc2` build like `ls`.
    Settled, off the list.

**The judgement call.** Small source fixes were made in place, each marked with
a comment saying what and why: three ANSI function definitions in `SRC/gtar`,
and one `typedef` guard in `SRC/ed/regex.h`. All four are the OSK porter's own
lines, not upstream code, and the automatic tool cannot do the job without
wrecking the files around them. I took the `jconfig.h` precedent — fix in
place, mark it. **If you would rather source edits lived as patches under
`tools/rebuild/`, say so and I will move them.**

Detail: `notes/CPP-MACRO-CRASH.md` (rewritten), `notes/SESSION-2026-08-23.md`.

---

# 2026-08-23 (evening) — the cpp bug is not what we said it was

**Needs you: one judgement call, below. Nothing else.**

  - **Microware's `cpp` dies on a line of 513 characters.** That is the whole
    bug. It is not "nested macro expansion" — nesting is just how a line gets
    long. Measured, and it explains the three-file reproduction we have been
    carrying: the crashing one expands to 542 characters, the two that compile
    to 270 and 222. `c68` has a limit too, 1023.
  - **`djpeg` builds** — the JPEG decoder, which never has here. Verified by
    decoding, not by linking: compress a test image with `cjpeg`, decompress
    it, the smooth channels come back within about 1 of 255.
  - **`gtar` does not**, but nothing about the preprocessor stands in its way
    now, and the five names still missing are written down.
  - Four headers went into `SRC/COMPAT`, all new names, none able to change
    what an existing build resolves.
  - The disk's JPEG test images are damaged — no byte above 0x7f anywhere in
    any of the three. A 7-bit transfer, long before us. Not worth fixing
    unless you want the IJG self-test to run.

Detail: `notes/CPP-MACRO-CRASH.md` (rewritten), `notes/SESSION-2026-08-23.md`
(second half).

---

# 2026-08-22/23 — the build pass

**Needs you: nothing.** `blarslib` was the one question and you answered it.

**Six lines of what changed:**

  - `ksh` works as shipped, interactively and with `-c`, on os9exec with your
    `I$Read` fix. Nothing os9exec did was wrong all pass.
  - Build recipes went 203 → 277. Last whole-tree run: 271 of 274 clean; the
    three added since are each verified alone but not in a full run.
  - Microware's `cpp` bus-errors on nested macros. **There is a way round it**
    — GNU's `cccp2`, which is in the SDK — and `flex` builds through it.
  - `world`, `patch`, `sonnet` had never compiled for want of one file each,
    and each file was still in the archive it came from.
  - `blarslib` is in, minus thirteen headers that were Microware's. It
    unlocked uucp (26 programs), smail and SB-Prolog. It did **not** unlock
    macutils, which is what I said it would when I asked — that was wrong.
  - Every build used to leave object files in `disk/`, which `mkimage.sh`
    ships. A check refuses that now, and it caught one already committed.

Detail: `notes/SESSION-2026-08-22.md`, `notes/SESSION-2026-08-23.md`.
What is left: `notes/PLAN-next.md`. A cold start:
`notes/START-HERE-NEXT-SESSION.md`.

---

# 2026-08-21 — the repair pass

Detail: `notes/SESSION-2026-08-21.md`. What I was asked and what I decided:
`notes/PLAN-release-2026-08-21.md`.

## 1. Read this first — Microware source was on the shipping disk

**`disk/SRC/msfm`, 21 files of OS-9 file-manager internals — path descriptors,
system globals, process descriptors. I have removed it.**

Byte-identical to EFFO forum disk 12's `SOFTWARE/C/MSFM/SRC`, whose `note.doc`
says:

> Source of original version: Peter Dibble: OS-9 INSIGHTS ... This source code
> is the proprietary confidential property of Microware Systems Corporation,
> and is provided to licensee solely for documentation and educational
> purposes. Reproduction, publication, or distribution in any form to any
> party other than licensee is strictly prohibited.

Three things beyond the removal:

1. **`msfm` was already on the refused list** in `notes/WORK-QUEUE.md` —
   *"Microware's, out of Dibble's OS-9 Insights"*. The MODULE was refused. The
   SOURCE came in by another route and nobody noticed.
2. **The notice was a sibling of the directory somebody copied**, one level up
   from the `SRC/` that was taken, so it stayed behind. The 21 files carry no
   header, no copyright line, nothing.
3. **`tools/screen_microware.py` would have caught it** — it flags 10 of the 21.
   It had only ever been run on candidates before installing them, never over
   what was already on the disk.

`check_disk.py` now has a ninth check, `no unscreened Microware source`, over
`disk/SRC` on the strong rules only. I proved it fires by putting one msfm file
back. Accepted exceptions are in **`tools/screened-src.txt`**, each with a
reason — **please read those and tell me if you disagree**. Most are common
interface headers (`stat.h`, `pwd.h`, the FSF's `getopt.h`), but
`disk/SRC/hc_utils/sys.c` is yours and you would know better than I do.

This is what I would most want a second opinion on before you ship.

---

## 2. Your `/h0` vs `/dd` question — answered

**`/dd`.** Your instinct about `/dd/GAMES` was right, by about five to one.

- **258** programs want the *collection* mounted as `/dd` — their own data is
  here.
- **53** want data at `/h0`.
- 98 more want only `/h0/sys/termcap`, which `TERMCAP` already settles, so they
  do not count either way.

Demonstrated, not just counted: `fortune` prints a fortune as `/dd`, and says
`can't open /dd/GAMES/FORTUNE/fortunes.dat` as `/h0`.

Recommendation: ship as `/dd`, keep the `/h0` hard link (one inode, collects
the 53), steer people away from `/h0`-only — it is the worst of the three and
strands 258 programs. `DOC/README-RUNNING` now says so; arrangement 2 is
marked recommended and arrangement 1's cost is stated honestly (it said "20
programs", it is 174).

Reasoning: **`notes/DECISION-placement.md`**. Measurement:
**`tools/measure_layout.py`**, so you can rerun it rather than trust me.

---

## 3. The missing libraries were not missing

The handoff listed the pdksh rebuild as *blocked on material that does not
exist here*. Every part of that was wrong:

- **`osklib.r` is not a file anybody shipped.** It is a build product,
  `merge`d from 21 objects.
- **Its sources were in the pool all along**, in `SHELLS/pd_ksh.e11.lzh`.
- The import into `disk/SRC/pdksh/` had **dropped the port's entire `OSK/`
  directory** except `OSK/INCL` (renamed `OSK_INCL`). The shipped source could
  not be built by anybody. It is complete now.
- **I built `osklib.r`** — 21 sections, 11 KB.
- **`popen.r` and `netdb.h`** were both in `~/Developer/os9/play/`.
- `strings.r` was already known not to be needed.

**The `ksh` alias crash is FOUND AND FIXED**, and the cause is worth knowing
because it is a trap for anything else built here:

> **`strchr` on this system does not match the terminating NUL.**
> `OSK/DEFS/osk.h` has `#define strchr index`, and `index("print", 0)` returns
> **NULL** — measured with a five-line program, not assumed. `lex.c`'s alias
> path reads the last character of an alias value with
> `strchr(s->str, 0)[-1]`, which is the ANSI idiom for "the end". Here that is
> `NULL[-1]`: a byte read at `$FFFFFFFF`, a bus error, on **every alias
> expansion**. Hence `echo`, `true` and `pwd` dying while `print` and `cd`
> were fine — those three are exactly the aliases `main.c` installs.

With the fix, `ksh -c "x=5; echo x is $x; true; echo status $?"` prints
`x is 5` and `status 0`. **Any `strchr(s, 0)` anywhere in this collection is a
latent bus error** — that is worth a grep some day.

**`ksh` is still not finished**: a SECOND and separate fault loses some stdout
(`print`/`echo` write with `putc` to `shf[1]`; error output goes a different
way and appears). Characterised, with the next thing to try, in
`tools/rebuild/pdksh/README.md`. This only matters if the os9exec fix is never
committed; **ksh works on the collection today**.

Everything in `tools/rebuild/pdksh/README.md`, including a warning worth
having: the port's `fork()` emulation has the child read the parent's address
space through SSM, so a rebuilt ksh may start and still not fork on os9exec.

---

## 4. Things that need YOUR decision

1. **`~/Developer/os9/os9exec` has FOUR modified files, not one.** The handoff
   says *"one file, `consio.c`, 25 lines"*. It is `consio.c` (+127/−13),
   `debug.c`, `filestuff.h`, and `test/Sources/OS9Tests/main.swift` (+101) —
   219 insertions. I have not touched, committed or reverted any of it. But
   the handoff understates what is sitting there.

2. **I replaced your three `keep`/`drop`/`kept` bash scripts with compiled
   modules.** I overwrote them before checking they existed, which was
   careless; I restored them from HEAD and then decided on evidence. The
   evidence: run against a `/dd` that is not the collection — the only case
   `keep` is for — the script version needs `bash` and `/dd/tmp` ON THE
   DESTINATION, has neither, copies nothing, and says almost nothing about
   why. Its own header assumes the collection lives on `/h0`, the premise the
   measurement overturned. Originals kept as `SRC/keep/*.sh`. Reversible.

3. ~~Two headers from the pdksh port were refused as Microware's.~~
   **Reversed, same day, and the reversal is the interesting part.** I refused
   `OSK/DEFS/ioctl.h` and `OSK/DEFS/termios.h` because the screener said they
   matched the SDK. They matched a file under `play/oskBoot` — your WORKING
   BUILD OVERLAY, not a pristine SDK. Neither `ioctl.h` nor `termio.h` exists
   in the pristine tree at all, and no copy of either carries a Microware
   copyright: they are the standard System V definitions, and any two
   expressions of that interface overlap.

   `screen_microware.py` now says **which** SDK a match came from. That one
   change also removes most of the noise from running it over `disk/LIB`,
   where it flagged 113 files, nearly all of them our own `ncurses.l`,
   `libgcc.l` and friends sitting in the overlay. A screen that cries wolf is
   one people stop reading, and this one was close to it.

4. **`CLAUDE.md` is gitignored, and I edited it.** Stale star counts, stale
   `/h0` figures, the `elvis` claim, the missing overlay, the nine checks, and
   the keep/drop section. Those edits live only in the working copy, so they
   are not in the branch you are about to review.

---

## 5. What else changed

**Removed:** `msfm` (above).

**Added — programs:** `passwd` (Matthias Rosenthal's, EFFO forum 5, with
source and his read_me); `dedit` (a reversal decided 2026-08-15 and never
carried out — it is BASIC09 I-code, and its header bytes match `bio` and
`wysetime` exactly); `zoo_2.1` as a REBUILT alternate; `keep`, `drop`, `kept`.

**Added — source, 17 trees, taking coverage from 354 to 406 of 939 (43%):**
`uucpbb` (which `DOC/ORIGINS` had promised for 18 programs since they were
added — there was no such tree), `pdksh/OSK`, `zoo`, `jpeglib`, `macutils`,
`gnuchess`, `ed`, `rcs`, `beav`, `lout`, `gtar`, `pvic`, `smail`, `dm`,
`cnews`, `infoxpress`, `uucp_blars`, `less`.

**Added — documentation:** the `sox` manual (its DOC directory held four audio
samples and no text at all, so the census counted it as documented), the
`msntp` manual, and the full MicroGnuEmacs manual in PostScript and DVI — the
disk ships ghostscript and TeX, so both are readable on it.

**Fixed — tooling:** `tools/rebuild/make_overlay.sh` (the clean `/dd` overlay
had gone missing entirely, and the rebuild machinery was unusable);
`tools/extract_pool.py`, which **silently dropped 16 pool files** and had done
since it was written — `untar` with `ignore_zeros=True` returns zero members
instead of raising, so the not-a-tar fallback never fired. That bug is why the
sox and mg manuals were never found.

**Fixed — documentation.** Every count I could find had drifted. `DOC/INDEX`'s
header contradicted itself in three consecutive sentences. `DOC/README-CIO`
still told people to go and fetch `cio`, months after the five modules started
shipping by Microware's permission — I rewrote it. The readme claimed the
collection ships "with their source"; it is 43%, and it now says so.

---

## 6. Open, in the order I would take them

1. **Read `tools/screened-src.txt`** — six pre-existing strong flags I accepted.
2. ~~`DOC/STATUS` is stale.~~ **DONE.** The full four-stage sweep was re-run
   from scratch: **877 of 926 actual programs, 94.7%**, against the previous
   pass's 877 of 925. The same collection measured again, not a different one.

   `tools/verify_combine.py` is new and produces that number from the four
   stage files — it was hand-work before, so the figure the collection
   advertises most loudly could not be recomputed. It reproduces the previous
   pass's committed result exactly (626 / 211 / 71 / 26 / 17) from the
   previous pass's stage files, which is how I know it is right. It also
   **refuses a stage file left over from an earlier sweep**, and that guard
   earned its place within the hour: stage 4 was killed mid-run and its file
   reverted to the previous pass's, which would have silently produced a
   number that was part one measurement and part another.

   `passwd` is counted separately and said so in `DOC/STATUS`: it went on the
   disk after the sweep began, so it was verified by hand instead.
3. **The ksh alias bug**, if you want the collection self-sufficient on a
   released os9exec.
4. **`APPS/oleo1.6.tar.gz`** is the biggest source gap left — 217 files for
   `oleo` — but it arrives wrapped in a `DEFS/` of 59 files, 27 of which
   overlap the SDK's heavily (`dma68450.h` 100%, `rbf.h` 96%). The sources are
   fine; separating them from the tree is a careful job.
5. **`fpu`** — `NOT-INCLUDED.md` says a grant puts it back in,
   `POOL-ASSESSMENT.md` says it stays out. Two notes disagree. Your call.
6. The four G-Windows programs' licence, still unanswered.
7. **The CI pin is 51 commits behind.** `.github/workflows/build-image.yml`
   pins os9exec to `261b4b69`; `~/Developer/os9/os9exec` HEAD is 51 commits
   past it. The comment says to bump it deliberately, so I have not. Worth
   knowing what it implies: whatever CI builds against is what a person
   downloading a release will effectively be running, and **no released
   os9exec has the `I$Read` fix** — so on a release today, `ksh` is not usable
   interactively. That is the argument for finishing the ksh source rebuild,
   and it is the only thing that would make the collection self-sufficient.

I checked the workflow itself as far as I can without running it:
`tools/gen_catalog.py disk docs/index.html` (the two-argument form CI uses)
works, and `check_disk.py disk` passes. I did not exercise the workflow.
