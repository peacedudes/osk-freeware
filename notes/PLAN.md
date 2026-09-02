# The plan — osk-freeware, from here to releasable

Hand this file to a fresh session. It is self-contained: you do not need the
rest of `notes/`, and you should not read it unless something here sends you
there.

---

## What this is

A curated collection of OS-9/68000 (OSK) community software, published as one
RBF disk image. `disk/` is the tree that gets maintained; `osk-freeware.dd` is
a build artefact, gitignored, never hand-edited.

The point of the collection is that someone can **take part of it onto their
own OS-9 media**. Keep that reader in mind; it decides most questions.

## Get running (two minutes)

```sh
OS9EXEC_DIR=~/Developer/os9/os9exec tools/mkimage.sh disk osk-freeware.dd
tools/check_disk.py disk          # 17 invariants -- read the list it prints,
                                  # never a number typed anywhere else
tools/gen_catalog.py disk --check # every program catalogued and categorised
tools/gen_screens.py --check      # no card has drifted from its stanza
```

Longer, and worth running before you claim anything is finished:

```sh
tools/datatest.py --all --image osk-freeware.dd   # 324 cases
tools/playtest.py --all --image osk-freeware.dd   # 116 tests, 112 pass
tools/ci/run_workflow_locally.sh /tmp/scratch     # the whole GitHub workflow
```

**The two tools the per-program loop runs on**, both added 2026-08-31:

```sh
tools/worklist.py --no-test --no-card    # what still has nothing at all
tools/drive.py <sheet>                   # run a sheet of programs, one
                                         # emulator session, transcript out
tools/audit_cards.py                     # cards that show help or an error
```

`worklist.py` prints one row per program with everything needed to pick the
next one: the `DOC/INDEX` claim, the binary's own usage line, whether a card
captures it, whether any test asserts anything, and which drive sheet runs
it. Every column is derived, so none of it can go stale. `drive.py` is the
step before a `datatest` case: it asserts nothing and shows you what came
back, forty programs to an emulator start.

The known failures are deliberate and each says why in its own file: three in
`datatest` -- `zip-cannot-write-its-archive`, `todos-must-change-the-file`,
`sir-round-trip-is-lossy` -- and four in `playtest` (pacman, puzzle, snake,
valspeak). A full `datatest --all` run is **420 of 423**, measured
2026-08-31.

**SEVEN CASES RESTART THE FAMILY THEY ARE IN, and that is expected.**
`paranoia` pauses for a key, `checkfile` is full-screen, and `cookhash`,
`sqrtx`, `chardef`, `xy` and `break` end the emulator session outright. The
harness restarts from where the output stopped, so each costs one restart and
not the rest of its family. A run that reports no restarts at all has probably
not run those seven.

**Each restart costs up to the 300-second per-attempt timeout**, so a full
`--all` run is dominated by them: seven session-enders is up to thirty-five
minutes of the hour it takes. `xy` and `break` are both in `last2.cases` and
are its LAST TWO CASES for that reason -- a session-ender must be last in its
family or everything after it pays for a restart it did not need.

**One harness at a time** — they all write to the image and take a lock, and a run
killed part-way leaves `osk-freeware.dd.lock` behind for the next one to
clear.

## Where it stands, measured

| | |
|---|---|
| Programs catalogued | 939 |
| Of those, RUNNABLE (a type-$01 module) | 915 -- the rest are drivers, descriptors and trap libraries |
| **Under no test at all** | **75** — was 209 when the measurement was fixed |
| No gallery card runs it by name | **81** |
| `datatest` cases | **633 in 44 families**, 3 deliberate failures |
| `tools/drives` sheets | **72** |
| Screens | 485 cards, **17** still flagged by `audit_cards.py` (3 of those excepted by name) |

> **THE FIGURE THIS TABLE USED TO LEAD WITH WAS WRONG, and the correction is
> worth more than the number.** "Programs with neither a test nor a card" ran
> 421 → 97 → 42 over two days and it was measured by a filter that could not
> do its job: `worklist.py`'s `carded()` looked for `for'-credited names in
> `shot["acts"]`, and `screenshots.parse` puts them in `shot["for"]`. The loop
> never matched. Every program credited on a shared card -- and cards here
> routinely credit three to five -- counted as having no card.
>
> Fixing it literally counted `for' and the answer went to **zero**, which is
> the trap `gen_screens` already names: *"918 of 918 have sample output"
> cannot fail while grouping satisfies it.* So `carded()` now means what
> `gen_screens` means by it -- **a card RUNS the program BY NAME** -- and the
> honest backlog is the first row above: **209 programs under no test**.
>
> The work done under the old figure was real: 79 cases, five rebuilds, four
> cards. The number describing what was left was not.
| Source here | 625 (66%) |
| Documented beyond one index line | 602 (63%) |

Re-measured 2026-08-31 evening. The tools are the authority, not this table:
`tools/worklist.py --programs --no-test --no-card`, `tools/audit_cards.py`,
`tools/src_census.py disk`, `tools/doc_census.py disk`.

Read those two middle rows together. "Driven" means somebody typed a real
invocation and looked at the answer; "under a test" means a machine will
notice if it stops being true. The gap between them is programs whose
behaviour was read once and not written down, and it is the cheapest work
left.

---

## The work, in order

> **Read this first if you are new here.** On 2026-08-31 rdoggett asked for
> one thing above all: *run the programs with real arguments and check they
> actually work — not just that they do not die; capture `-?` and compare it
> against the documentation; and take screenshots that show a program working
> rather than its usage line.*
>
> **That is now the thing being done, and it has a shape.** 448 programs are
> driven by a committed sheet in `tools/drives/`, 534 are under a test that
> can fail again, and 97 runnable programs have neither. The loop is:
>
> ```sh
> tools/worklist.py --programs --no-test --no-card    # pick a batch
> # write tools/drives/<name>.drive with REAL invocations
> tools/drive.py <name>                               # one emulator session
> # read the transcript, fix DOC/INDEX where it disagrees,
> # write tools/datatests/<family>.cases for what the run settled
> tools/datatest.py tools/datatests/<family>.cases
> ```
>
> **A program that looks broken usually has the wrong invocation.** That is
> the single most useful thing this pass has learnt, and it has been true
> more often than not: eight netpbm converters wrote zero bytes until they
> were given a quantised image; eleven Dhrystone builds looked mute because
> they were waiting for a run count on stdin; `tangle` could not open a
> `.web` because the file it could not open was the absent CHANGE file;
> `booz` wanted a bare letter and not `-l`. Check the invocation before you
> write the program off, and write down what the right one is.

### 1. Module-name collisions — the five in REBUILT are done, 27 names remain

Done 2026-08-31: `CMDS/REBUILT/{arc,compress,kermit,screen,VI}` are now
`arc_5.12`, `compress_rebuilt`, `kermit_cio`, `screen_nocio` and `vi_1.0`,
file and module together, with `tools/rename_module.py`. `bush` also left the
disk (a countdown to the end of a 1989 administration). `makeinfo` and
`gnuchess` are NOT done.

**The measurement that mattered.** The plan used to say "ten names in two
directories, eight sharing a module name". Measured per FILE rather than per
name, it is **32 module names over 76 files**. The five above were the ones
the decision covered; the rest fall into three groups:

- **Must not be renamed.** `csl`/`csl020` and `math`/`math881` are Microware
  trap libraries: a program links them BY NAME, and the second of each pair
  exists to answer to that name on another CPU. `MM1/msdrv.901_340` and
  `msdrv_340.901.ms` are two editions of one driver, bound by a descriptor.
- **The gcc passes.** `gcc_cc1plus`, `gpp_cc1plus` and `GCC2/cc1plus` are all
  module `cc1plus`, and the same for `cccp2`, `collect` and `cc2`. They are
  forked by FILENAME, so a compiler run is not misdirected; it is still a
  reason not to load both compilers. Documented in `DOC/STATUS`, not changed.
- **Alternates whose filename is already distinct but whose module is not** —
  about 25 files: `compress_4.0`, `diff_1.1`, `m4_0.5`, `sed_1.06`, `zoo_2.1`,
  the six `gzip*`, `vi.elvis`, `ctags.elvis`, `input.elvis`, `wc.cio`,
  `vi_cio`, `kermit2`, the four `*.070` jpeg tools, `emacs.mm1`, `ephem881`,
  `infocom.tcap`, `lnk.org`. Making each module match the filename it already
  has takes nothing away from the archive and is the obvious next batch.

  **One hazard, found before it bit.** Elvis's wrappers pick their personality
  from the LAST LETTER of `argv[0]` — `alias.c` maps `w`→`-R` (view),
  `t`→`-i` (input), anything else→plain vi. If `argv[0]` comes from the module
  name rather than the filename, renaming `input.elvis`'s module from `input`
  to `input.elvis` ends the letter on `s` and turns it into plain vi. **Measure
  which one OS-9 passes before renaming those three.** `input.elvis` is the
  discriminating test: its file already ends in `s` and its module in `t`.

Still open from the original decision: `makeinfo` (`CMDS` and `GCC139` are
BYTE-IDENTICAL — delete the GCC139 copy) and `gnuchess` (`CMDS` and `GAMES`
are different ports; the CMDS one has siblings `gnuchessn` and `gnuchessr` and
shares their `-x xwndw` usage line, so `gnuchessx` would keep that family
together while leaving GAMES the plain name). `wish` collides by filename
only — `wish` against `B_wish` — and is lowest priority.

### 1a. Gallery cards that show nothing but a usage line — 27 left of 31 found

rdoggett, 2026-08-31: *"Sample output that does nothing more than show the
help is only valuable if the help isn't shown some other way, and there is no
more interesting output from the program to show."*

**There is a detector now and it works: `tools/audit_cards.py`.** It scores
each card's lines as USAGE, ERROR or WORK and flags a card with no WORK, or
with more error than work, or with a usage line and almost nothing else. It
reports 31 of 407. Two earlier attempts lied and are described in the tool's
own header; the thing that made this one honest is reading the card's SHEET to
find out which lines were commands, because a capture does not reliably prefix
an echoed command with a prompt and those echoes were being scored as the
program's own output.

**Two of the 31 are false positives and stay.** `perr` and `perr-print` print
the text of an OS-9 error number, so error text IS their output — the one
place in the gallery where a screen full of `Error #000:216` is exactly right.

Fixed 2026-08-31 evening, each by running the program and finding the
invocation was wrong rather than the program: `xasm` (five assemblers that
now assemble the samples shipped in `DOC/xasm`), `zoo2` (`booz` takes a bare
letter, not `-l`; `fiz` takes the archive), `upperdir` (now shows the rename),
`elm-suite` (the alias files ship now), `msmove`, `sysmon` (a blank screen
plus the alternatives that do answer), `tangle`/`weave` (a `sample.web` ships
now) and `dhry-all` — that last one **claimed twelve builds and showed one**,
because eleven of them were waiting at a prompt for a run count.

Earlier the same day: `hc`, `join`, `pwgen`, `rndname`, `pbyte`/`chbase`.

**`hc` is still the shape to look for.** `DOC/INDEX` called it a hex
calculator, it was filed under Maths & calculators, and its card ran
`echo 1f * 3 + 7 | hc` and captured the usage line the invocation earned.
It is a text filter. A card that shows a program failing, captioned as though
the program were at fault, is worse than no card.

Still flagged and not yet looked at: `pbmclean`, `pnmfilters`, `argproc_demo`
(a genuine Stack Overflow, whatever it is given), `csl-mismatch`, `wn`,
`game` (wants a `chess.lst` from gnuchess), `newshist`, `p2c`, `ateri`,
`network`, `perr-alps`, `ppmntsc`, `xpm`, `dload`, `texfonts-bitmap`,
`asciitopgm`, `aterm`, `disktest`, `phone`, `silent`, `vi-recovery`.

### 2. Family chooser documents — highest value for the stated purpose

Somebody taking part of this onto their own media has to choose between
several of a thing, and should not have to install all of them to find out
how they differ. `DOC/README-VI` was rewritten as the model on 2026-08-30:
a table of hard facts, the reason you cannot keep several (module names), a
short "take this if" per candidate, and a one-line answer for someone who
wants exactly one file.

Families still needing one, roughly in order of how many people care:

- **shells** — bash, sh, ksh, gshell, mshell. `DOC/README-SHELLS` exists;
  what was blocking it is now SETTLED (2026-09-01, on the shipped RBF image):

  **`ksh -c "cd <dir>; <prog>"` moves the OS-9 data directory.** That is the
  recommendation for anyone who needs to run a program somewhere — and there
  are real programs that need it, `wndex` being the clear one, since it works
  on the current directory and ignores a directory argument. `sh`'s `chd`
  moves it too but `sh` cannot fork an absolute pathname, so `sh` needs the
  program `load`ed first. bash's `cd` is real in a SCRIPT (a non-interactive
  bash never reads `.bashrc`) and a string-tracking shim INTERACTIVELY, which
  is why this looked settled both ways for a fortnight. Asserted in
  `tools/datatests/web.cases`, both halves.

  Static facts already gathered: bash 242604 (no cio, module `bash`), sh 77306
  (no cio), ksh 118554 (needs cio), gshell 23114 (no cio), mshell 7228 (needs
  cio). Verified 2026-08-31: `ksh -c '<abs path> <args>'` runs the program,
  and `sh -c` does NOT — "file not found" for a file that exists, which is the
  fork-an-absolute-pathname failure already recorded for `sh`.
- **archivers** — arc/marc/dearc, lha/lharc/xlharc, zoo/booz/fiz, tar/gtar,
  zip/unzip, compress/compr/gzip and its four builds.
- **kermit** — kermit, kermit2, kermit3, xkermit, ckermit.
- **editors beyond vi** — ed, em, me, emacs, umacs, mg, sedt, new_e, beav.
- **grep-likes** — grep, ggrep, fgrep, lgrep, bm, gep.

Everything you need is derivable without running them: size, whether it needs
`cio` (the star in `DOC/INDEX`), module name (collisions), source present
(`tools/src_census.py`), documentation present (`tools/doc_census.py`), and
provenance (`DOC/ORIGINS`). Run the programs only where the table cannot
answer the question.

Done when: each family has a `DOC/README-<family>` that a stranger can act on
without installing anything.

### 3. Tests that can fail again — 659 programs have none

277 of 936 have a data case or a play-test. The rest rest on a capture
nobody re-checks: if a rebuild broke one tomorrow, only the 277 would notice.

The gap is not uniform. The netpbm set is covered densely as a family (a
round trip through `pnmarith -difference` requiring an all-zero result is a
strong assertion). The games have play-tests. **The thin part is the ordinary
utilities** — text filters, file tools, system commands — where a case costs
about four lines and would catch a real regression.

Write them into the existing families in `tools/datatests/`. Make each new
case fail once before believing it.

### 4. Documentation depth — 336 programs have only an index line

And 815 of 892 index entries carry no dated stamp, meaning nobody has run the
program and checked that the entry describes it. This is where the collection
is thinnest and where its errors have historically been.

**Do not compare an entry against its CARD.** Tried 2026-08-30: a description
and a program's screen output naturally share no words (`cal` prints "August
2026", `banner` prints `@` signs), so the flag fired on 208 entries and nearly
all were fine.

**A sharper signal exists, found 2026-08-31: compare the entry against the
program's own `Function:` line.** Many OS-9 utilities print one, and
`DOC/USAGE` already captured them — so this compares a description with a
description rather than with a screenful of output. 78 programs print one, 68
of those are in `DOC/INDEX`, and requiring no word in common flags **23**. Most
of those are synonyms (`lpq`: "shows spoolerqueue" against "shows the spooler
queue"), which is fine — 23 entries is a list a person can read in ten minutes,
where 208 is not.

Three real errors came out of the first pass, each confirmed by running the
program:

- `btop` "bitmap to Gepard fat-font" and `ptob` "Gepard fat-font back to
  bitmap" — they convert characters to bit patterns and back. 40 bytes in, 640
  out, 40 back, byte-identical. The Gepard font is an application of the pair,
  not what either program does.
- `ediff` "visual file compare" — it does not compare anything. It reformats
  `diff`'s OUTPUT: `diff f1 f2 ! ediff` prints "-------- 1 line changed at 3
  from: ... to: ...".

All three are fixed and asserted in `tools/datatests/encoding.cases`.

**THE OTHER FLAGGED ENTRIES HAVE NOW BEEN READ (2026-09-01) and the trick is
spent.** Re-run over the 65 programs whose capture carries a `Function:`
line, 22 flag and NINETEEN ARE FINE — synonyms (`bcheck`: "check sourcefile
for correct bracketcount" against "count brackets in a source file"),
entries that describe a program's PLACE rather than its job (`diff_1.1`,
`m4_0.5`, `sed_1.06` are all "another build of"), and four artefacts where
the parser matched a name in the star grid rather than an entry.

Three were real and are corrected:

- `editor` "GSHELL front-end for the editor" — it is a front end for
  `umacs' SPECIFICALLY; its own line says "a menue driven umacs shell".
- `fstat` "Report a file's status and attributes" — it displays the RBF
  FILE DESCRIPTOR sector, which is not the attribute bits `attr` shows.
- `fc` "split a big file in two" — the cut is at exactly 350,000 BYTES,
  not at the halfway point.

**There is nothing more this comparison can find.** The 274 programs with no
`Function:` line still need running one at a time, and that is what the
per-program pass has been doing.

### 5. Housekeeping

- `notes/` is 7300 lines across 42 files. It was pruned once, at rdoggett's
  request, and has grown back. A finding belongs in the file it belongs to —
  the handoff, `DOC/STATUS`, `COMPILE-AUDIT.md` — not in a new dated file.
- Older prose in `DOC/STATUS` and `DOC/INDEX` still shouts in places. Fix it
  where you are editing anyway; do not do a sweep, an automated pass was
  tried and lower-cased filenames and table labels.

---

## Rules that matter

- **Commit your own work.** rdoggett does not approve commits. The gate is all
  `check_disk.py` checks green -- read the list the tool prints rather than a
  number typed here -- and the tree left clean. Group related
  changes; no mixed-bag commits. `git add -A` will sweep in unrelated work —
  stage deliberately.
- **OS-9 text files are CR-terminated (0x0D), never LF.** Write with
  `open(p,"wb").write(text.replace("\n","\r").encode("latin-1"))`, and build
  the bytes *before* opening the file — `open(p,"wb")` truncates the moment it
  is evaluated, which emptied `DOC/STATUS` once.
- **Never call the disk "bootable".** os9exec is the kernel; it runs a program
  with this disk mounted as `/dd`.
- **Measure, do not infer.** Every proxy tried here has been wrong in both
  directions. Do not derive the `cio` list from strings in a binary; do not
  derive the `shell` list either (122 modules carry the word because the C
  library links `popen()` into everything).
- **Make every check fail once** before believing it. This collection has
  produced a remarkable number that could not fail.
- **Do not shout.** Section headings in capitals are this collection's
  convention; mid-sentence capitals are not. "It works, with one flaw" — not
  "IT WORKS".
- Microware is a current vendor and this collection supports them. State
  provenance as fact; never write about them adversarially.

## Things already tried that did not work — do not repeat

- Bulk-checking index entries against their cards (see 4).
- An automated pass to lower-case shouting: it lower-cased `DOC/README-FORTRAN`,
  `/dd/SPL/SPLQ` and table labels like `SILENT`.
- Deriving the "needs a shell" or "needs cio" lists from strings in binaries.
- `sh` as a way to `chd` and then run something under os9exec: it cannot
  launch a program at all there — `today: nowhere found` bare, `file not
  found` by absolute path, with PATH set and `chx` done.

## Open with rdoggett

Nothing. The four questions on `notes/FOR-RDOGGETT.md` were answered on
2026-08-30; item 1 above is his decision, waiting only on execution.

---

## Settled on 2026-08-31 (evening), so nobody re-derives it

- **`SYS/login` sets `SHELL=$ROOT/CMDS/ksh`.** This C library's `system()`
  forks `$SHELL` with the whole command line as ONE argument, and only `ksh`
  parses it that way. `tex`, `latex`, `eo` and `maketexpk` went from doing
  nothing at all to working. `DOC/README-SHELLS` compares all five shells;
  `check_disk.py` now fails if `screenshots.py`'s copy of the login
  environment disagrees with `SYS/login`, because it already had.
- **The eleven cio casualties are rebuilt and installed.** `cvtbase`,
  `cdiff`, `nroff`, `etags`, `yacc`, `xrf`, `unstr`, `cookhash`, `logisim`,
  `pagekwic`, `pagefraz`. All trap-free, all unstarred, all asserted in
  `tools/datatests/cio11.cases`. `relink_cio.sh` now refuses a program with a
  putc/getc call site rather than reporting one.

- **AND THEN THE OTHER TWENTY-NINE WERE RUN, and twenty-four were fine.**
  This is the more useful half. `cio_macro_scan.py` still named twenty-nine
  programs after the eleven left, every one of them with a recipe already in
  `tools/rebuild/recipes.psv`. All twenty-nine were rebuilt `-qm` — and then,
  before installing any of them, all twenty-nine of the SHIPPED binaries were
  run with real arguments against real files (`tools/drives/cio29.drive`,
  then `cio29b.drive` for the seven whose first answer was the sheet's fault
  rather than the program's).

  **Five were broken and are now replaced**: `printf`, `valspeak`, `unifdef`,
  `ape`, `hexed` — asserted in `tools/datatests/cio5.cases`, each case made
  to fail against the binary it replaced before it was believed. The star
  grid went 354 to 349.

  **`setfont` looked like a sixth and is not.** It writes no byte for a real
  font file — to `/term`, to `$PORT`, or to a file `$PORT` names — and never
  reaches its own `Can't open` message. It was rebuilt, installed, and then
  TAKEN BACK OUT, because the `-qm` build does exactly the same thing. **A
  rebuild that changes nothing is the cheap way to rule the mismatch out**,
  and it is worth doing before replacing an archive binary with one of ours.

  **The other twenty-three do their work correctly** — `ascii` writes its
  whole 4,290-byte table, `loan` prints a full amortisation schedule, `diff`
  and `spiff` both diff, `strfile`, `makelex`, `crypto`, `snap`, `vis`, `lp`,
  `undel`, `dam`, `sedt`, `wish`, `rpoem`, `newsgen`, `blackjak`, `poker`,
  `stone`, `tess`, `liborder`, `unpacklib`, `chksum`. **Carrying the call
  site is not making the call**, and the scan's own header says so; this is
  the measurement that shows how loose the upper bound is.

- **`printf` mattered more than its own entry.** It dropped every literal
  character before the first conversion, so a format with NO conversion wrote
  a **zero-byte file** — and seven committed drive sheets built their input
  that way (`misc1`, `misc2`, `misc3`, `rcs`, `rcs2`, `rcs3`, `rcs4`, and
  `mail2`, which is how `nptx` came to be recorded as silent). Those sheets
  were measuring their own setup. `mail2.drive` is corrected; the rest are
  worth re-running now that printf works. **Write a sheet's input with bash's
  `echo`, or with `printf '%s\r'` — never with a format that has no `%`.**
- **`No more memory` has three causes, not one.** The cio selector mismatch
  (41, now 30); an ADDRESS used as a length (`lfmaker`, proved by the request
  moving with an environment pad, and only once the module is resident); and
  an honest fixed request for the whole arena (`texidx`, 0x2000040 every
  time). Addendum in `notes/os9exec-bugs/CIO-SELECTOR-MISMATCH.md`.
- **Both halves of the JPEG/PNM header disagreement.** `cjpeg` wants LF
  between PNM header fields and this disk's netpbm writes CR; `djpeg` writes
  LF and this disk's `pnmfile` cannot read it. `pbyte <file> <offset> 0a` is
  the patch, in whichever direction you are going.
- **`pgmtopbm` without `-threshold` is NOT reproducible** -- its dither
  differs every run, and anything asserting a length or an md5 downstream of
  it will flap. Both netpbm case files say so now.
- **Twelve `DOC/INDEX` entries described a different program** and are fixed:
  `checkfile` (a cheque-book program), `paranoia` (a text adventure),
  `remove` (modules, not files), `preset` (terminal function keys), `eo`,
  `dotilde`, `vecho`, `lfmaker`, `timid`, `udate`, `wysetime`, `gpp`.

### What is left, in the order it is worth doing

1. **75 runnable programs under no test.** They are the awkward residue and
   they divide into three kinds -- wrong invocation, ends-the-session, and
   wants-hardware -- which `notes/START-HERE-NEXT-SESSION.md` lists. Decide
   which one you have before spending time on it.

   **The three hazards this pass found are worth more than any of the
   cases.** A work directory collision under the shared `/dd/tmp` cost
   eleven programs a wrong verdict; `flink` corrupted `/dd/CMDS/cat` into a
   DIRECTORY and produced five more apparently-broken programs in an hour;
   and a relative `--image` path broke every file open on `/h0` while
   module loading kept working. **Rebuild the image before believing a
   strange answer** -- it takes four seconds.

1a. **(historical) 42 runnable programs with neither a test nor a card.**
   `tools/worklist.py --programs --no-test --no-card` prints them. Most are
   already driven -- their transcripts are reproducible from the sheets in
   `tools/drives/` -- and only need a case written. The ones left are the
   awkward ones: the seven gcc PASSES (forked by the driver, not run by
   hand), the three Atari GRAPH demos that want a display, and a handful
   that end the emulator session and so cannot be a `datatest` case at all
   (`pbmtobbnbg`, `wysecrack`, `cron`, `byteflip`). **A program that ends
   the session belongs in DOC/INDEX and in a drive transcript, not in a
   case** -- datatest fails any case whose session took an exception, and
   that rule is right.
2. **17 gallery cards still flagged.** `tools/audit_cards.py`. THREE are
   excepted by name and should stay: `perr` and `perr-print` print the text
   of an error number, so error text IS their output, and `csl-mismatch`'s
   whole subject is the edition skew.
3. **The family chooser documents.** `DOC/README-SHELLS` was written this
   session as the second one after `DOC/README-VI`. Archivers, kermit,
   editors and grep-likes are still to do, and everything they need is
   derivable without running anything.
