# Picking this up cold — updated 2026-08-28, end of session

Branch `release-pass-2026-08-21`. **Tree clean, all eleven `check_disk.py`
checks green, `osk-freeware.dd` current.** Nothing is half-finished; every
change below is committed.

## WHAT HAPPENED 2026-08-28 (fourth session): reading the screens

Taking a picture is not the job. **Reading it is**, and rdoggett said so:
*"you have to read the output you are collecting, to make sure it makes
sense."* Every card was read against its caption. Sixteen more programs
turned out to be labelled wrong in DOC/INDEX -- `fc`, `rdoc`, `screen`,
`bcheck`, `ask`, `ynad`, `launch`, `gawk`, `divide`, `vc` among them --
and each is corrected in the index and on the card. `notes/FOR-RDOGGETT.md`
has the list with what each one really is.

**Seven programs cannot be reached by name at all**: `break`, `enable`,
`fc`, `for`, `help`, `if` and `trap` are bash builtins or keywords, so the
shell answers first and never says it did. DOC/STATUS names them.

Three things the HARNESS learned, all in `tools/screenshots.py`:

  - **os9exec's abort dump lands on top of a program's picture.** Scoring
    now ignores dump lines, so the moment before the kill wins where there
    is a picture under it, and the dump still stands where it is all there
    is (`graphlib`, `top`).
  - **A command longer than the terminal loses its head.** The line wraps,
    the top scrolls, and the card opens mid-word. Long pipelines are split
    into steps in the sheets; `size` inside a stanza now sets that stanza's
    window and nothing else.
  - `gen_screens.py` splits a prompt that a program's last unterminated
    write left on its line, and drops head's misplaced filename banner.
  - **Two stanzas whose names differ only in case shared one capture file.**
    `VI` overwrote `vi`, so the EFFO vi's card carried PVIC's screen. Both
    tools now refuse such a sheet; the stanza is `pvic` now. Found by the
    drift check, which is why `--check` exists and why **CI runs
    `tools/gen_screens.py --check` and `tools/gen_catalog.py disk --check`**.

**Data tests: 151 of 154 pass**, the three failures deliberate and
commented (`zip`, `todos`, `pnmtosir`). New families since: `rebuilt.cases`
(the CMDS/REBUILT alternates) and cases for printf, nsort, cjpeg and shar.

**Two harness bugs were found by their own output, 2026-08-29.** A capture
file was shared by two stanzas whose names differed only in case, and
`datatest.py` stripped `#` anywhere in a line -- so `absent  #!/bin/sh`
became a bare `absent` matching the empty string. Both are fixed and both
now refuse the input rather than accept it quietly. The second one surfaced
because a case that said `expect motd` was passing on the word `motd`
INSIDE the error message `No read access for file: /dd/SYS/motd`.

## WHAT HAPPENED 2026-08-27 (third session): the screens

**Every program's card in `docs/index.html` carries its own SAMPLE OUTPUT**,
photographed while running -- ALL 918 of them as of 2026-08-28, from
471 distinct captures (one card can cover a family). `tools/screenshots.py`
takes the pictures: ONE bash session on a pty, many programs per session,
the bytes each one wrote rendered by `ansiscreen.py`. A sheet
(`tools/screenshots/*.sheet`) is the source; `tools/gen_screens.py` folds
the captures into `docs/screens.js`, which the catalogue reads, and
`docs/screens/*.txt`.

**There is ONE catalogue.** The screens had a gallery page of their own for
a day; rdoggett, 2026-08-28: *"They need to be incorporated with the other
html; it's one catalog... this is sample output (you already have sample
help)."* A second page listing the same programs is a second catalogue to
keep true, and it is gone.

**Commands in the screens are typed the way a person types them** -- `banner
OS-9`, not `/dd/CMDS/banner OS-9`. rdoggett: *"It's kind of unnatural /
annoying that you ALWAYS use complete /dd/CMDS/thing paths... It's just
excess noise, right?"* It is. `SYS/login` puts every program directory on
PATH, and the sheets use bare names; a path in a screen now means a FILE
being operated on, which is real.

**Photographing the disk found more than any sweep has.** Twelve programs the
four-stage sweep scored OK do not work -- `gawk` reads no input at all, `m4`
mangles its output, `oleo` aborts, `date` says 2100, `cpu` answers and then
traps -- and two DOC/INDEX entries described the wrong program (`rot`
transposes a file, `edir` lists OS-9 events). All in `DOC/STATUS` under
WHAT PHOTOGRAPHING THEM FOUND.

**83 programs were invisible in the web guide.** `gen_catalog` scanned eleven
of the eighteen program directories under CMDS, so TeX and LaTeX, elm, the WN
web server, the network and serial-line sets and ADL were never in it. 917
programs now, not 834. `SYS/login` had the same gap on PATH -- `tex` could not
find `virtex` -- and now lists every one of them.

Also measured and documented: seventeen programs want a RAM disk at `/r0`
that os9exec cannot make (`mount` creates h0..hz and nothing else); five
programs need a newer `csl` than the edition 16 that ships; the JPEG tools
cannot read a PNM, so no JPEG can be made here.

**If you add screens: one stanza per program**, and then READ WHAT IT TOOK.
rdoggett, 2026-08-28, looking at the `cvtbase` card: *"I asked you to
capture an interesting screen shot, this is what you saved"* -- twenty-four
copies of `No more memory !!!`. And at `divide`: a caption about integer
division over a screen showing `Can't open file ??`, with another program's
checksums underneath. Both had passed every check there was.

So there are three now, and none of them replaces looking:

  - `tools/audit_screens.py` flags a screen that is one line repeated, one
    with almost nothing on it, one that is only the command typed.
  - `tools/gen_screens.py` reports DRIFT -- a stanza with no capture, and a
    capture whose stanza has changed since (each capture carries a hash of
    what its stanza says, so editing one stanza does not flag its
    neighbours).
  - The screens themselves read as a session: the commands are there with a
    `$`, the prompt is not, and a program is called the way a person calls
    it. `hack` is the one exception and its file says why.

`tools/README.md` has the rest.

## DO THIS FIRST — the next three actions, in order

Do not re-plan. `notes/PLAN-verification.md` is the plan and it is current.
Do not stop between items to report; commit and start the next one.

**A. ~~Re-run stage 2 the loaded way.~~ DONE 2026-08-28, and stage 4 with
   it.** `tools/sweep_filters_loaded.sh` gave the 272 silent programs real
   input -- 211 are filters -- and `tools/sweep_usage_loaded.sh` asked the
   rest for their usage; 30 answered. So all four stages have now been run
   the way a person runs the disk:

       922 programs (945 files less 23 that are not programs)
       871 demonstrated running -- 94.5%
        31 silent at every stage, 18 crash, 2 want a trap handler

   **Do not compare that percentage with the old 95.0%**: the denominators
   differ, because 23 files that are not programs came out of this one.
   DOC/STATUS has the whole thing under RUN THE WAY A PERSON RUNS IT, and
   the 51 that remain are almost all already explained further down it.

**B. ~~Tier A, the families with no cases yet.~~ DONE 2026-08-28** -- files
   (14 cases) and maths (12). Seven families now, 131 cases, 128 passing;
   the three failures are the known defects. Writing them found `cvtbase`
   and `printf` flooding `No more memory`, `divide` being a FILE SPLITTER
   rather than integer division, `find` refusing the Unix syntax, and
   `queens` working perfectly when given a NUMBER instead of prose.

**C. ~~`cp` takes a bus error.~~ ANSWERED 2026-08-28.** `cp` COPIES
   correctly -- md5 in, md5 out -- and crashes only when run with no
   arguments, inside I$Open after printing its usage. `top` is the other way
   round and has no invocation that gets past its heading. The remaining
   sixteen crashes are the documented groups.

## WHAT TO DO NEXT, then

**1. Coverage is done: `docs/screens.js` covers 918 of 918.** The last
   forty-nine were closed on 2026-08-28 -- some with new cards (`roff`,
   `btop`, `memtools`, `mtst`, `tplot`, `ttyexp`, `mgif`, `fontgen`,
   `draw`, `lorenz3d`, `bush`), the rest by naming them on the card that
   already showed what they do: the sixteen netpbm readers with no file to
   read share `noreader`, the G-Windows three share one card, and the four
   csl-mismatch programs share theirs. What is left to IMPROVE is quality,
   not coverage: `tools/audit_screens.py` flags eight, of which four are
   honest (a wall of plus signs is what `puzzle` draws).

**2. Tier B has been played: 104 of 108 pass.** `tools/playtest.py --all`,
   run 2026-08-28, about two and a quarter hours. Write-up in `DOC/STATUS`
   under PLAYED, NOT JUST RUN. The four failures are kept failing on
   purpose and each script says why -- pacman writes control bytes for a
   terminal that is not a vt100, puzzle is G-Windows, valspeak exits at
   once, and **snake plays but scatters text over its own board**: 17
   cursor moves arrive as literal `[13;49H' instead of as motion. A fresh
   build from the fixed source behaves identically, so the echo fix in
   `SRC/snake/move.c` is not the cure -- that comment is corrected and has
   the byte stream. What is left here is writing scripts for the Tier B
   programs that still have none.

**3. The three data-test failures are deliberate** -- zip, todos, pnmtosir --
   and a FOURTH would be a regression. Run `tools/datatest.py --all` before
   believing anything else.

The three that were here are done and are kept below, because each one found
something that is worth not re-deriving.

**1. ~~Text tools — `tools/datatests/text.cases`.~~ DONE 2026-08-28**, 21
   cases, and writing them found that `sed` did not work at all: every script
   answered `No more memory !!!`. The alternate build, `REBUILT/sed_1.06`,
   works and now ships as `sed`. Three cases assert a program's ERROR on
   purpose -- gawk reading no input, m4 mangling its output, subber calling
   an unimplemented system call -- so they pass while it is broken and fail
   the day it is fixed. **`datatest.py` now restarts a family after a case
   that kills the session** (subber and gawk both do), instead of reporting
   every later case as "never ran".

**2. ~~Finish the archive family.~~ DONE 2026-08-28.** 24 cases: lha, lharc,
   ar, ar2, marc, shar, zoo 2.1, compress_4.0, four gzip builds and gtar, all
   by round trip where one is possible. What it found: `ar` refuses an
   ABSOLUTE path; `marc` is the archive MERGER, not an archiver; and BOTH
   `arc` builds fail exactly as `zip` does -- compress, write a temporary,
   then cannot move it into place. The reason is measured and in DOC/STATUS:
   this C library has neither `rename()` nor `link()`.

**3. ~~Re-sweep with `load`.~~ DONE 2026-08-28** -- `tools/sweep_loaded.sh`,
   table in `notes/verify-loaded.tsv`, written up in `DOC/STATUS` under RUN
   THE WAY A PERSON RUNS IT. Every file under CMDS, each from bash, with the
   environment `SYS/login` sets and `os9lib`, `graph` and `Ptxm` loaded.
   **It is one stage of four**, so no percentage comes off it; what it is for
   is the DELTA against the bare sweep. Five programs came alive for the load
   (the RTF Fortran set), seven for the environment, seven moved from "wants
   a trap handler" to "crashes inside it" (the Atari GRAPH group, confirming
   what DOC/STATUS had inferred), and 23 stopped being scored as programs at
   all -- they are modules, drivers and shell scripts.

   **Its first run was wrong and the reason is worth keeping**: bash answers
   `cannot execute binary file` for a trap module, and the classifier counted
   that as the program printing something -- thirty false OKs. A shell in the
   path means its complaints have to be recognised as its own.

   **All four stages have now been run this way** and the write-up in
   `DOC/STATUS` is current: 922 programs, 630 printed bare, 211 as filters,
   30 when asked `-?' -- 871 demonstrated running, 31 silent, 18 crashed, 2
   wanting a trap handler. The tables are `notes/verify-loaded.tsv`,
   `notes/verify-filters-loaded.tsv` and `notes/verify-usage-loaded.tsv`.
   A note here that said stage 2 was outstanding was stale; checked
   2026-08-29 against the files' own dates and contents.

## How to run the three test harnesses

    export OS9EXEC=~/Developer/os9/os9exec/os9exec

    tools/datatest.py --all          # Tier A: data in, data out. FAST --
                                     # one emulator start per family.  The
                                     # `modules' family LOADS os9lib first,
                                     # with the disk's own CMDS/load
    tools/playtest.py --all          # Tier B: pty, screen read. SLOW, hours
    tools/check_disk.py disk         # eleven invariants; read the OUTPUT

Current: **105 data cases, 102 passing** (`tools/datatest.py --all`, verified
at end of session). The three failures are EXPECTED and are real defects in
shipped programs, kept failing on purpose:

    archives  zip-cannot-write-its-archive
    encoding  todos-must-change-the-file
    netpbm    sir-round-trip-is-lossy

If one of those starts passing, something was fixed -- find out what before
celebrating. If a FOURTH appears, that is a regression.

## `load` SHIPS NOW — and OS9MDIR is gone

**CMDS/load is on the disk, with its source in SRC/load.** It is a clean-room
reimplementation of Microware's utility, written from the published manuals
and contributed by the os9exec project on 2026-08-27; rdoggett: *"Move load.c
into your files; you own it now."* It is built here with the ordinary `-qm`,
so it links no trap handler and needs no `cio`:

    load /dd/CMDS/os9lib        and the RTF Fortran set comes alive

Its `-?` says what it is, so nobody meets it and wonders. Verified: `-?`, a
load that works, a load that fails (`Error #000:216`), and `-l`.

**`OS9MDIR` IS NO LONGER USED ANYWHERE.** rdoggett, 2026-08-27: *"Please stop
using OS9MDIR, it shouldn't be needed anymore."* All five host-side users are
converted and the only mentions left in the tree are comments saying what
replaced them:

  - `mkimage.sh` -- `sh` cannot find `tar` once `chd` has moved to the new
    image, so the build now runs `load /dd/CMDS/tar` first and F$Fork finds
    the module without touching the filesystem. Verified: 8602/8602 extracted.
  - `probe_runnability.sh`, `install_relink.sh`, `compare_relink.sh` -- the
    scratch directory is MOUNTED as `/h5` and the program run as `/h5/<name>`.
  - `probe_runnability_traps.sh` -- the same, plus `OS9CMDS` so that the
    execution directory is that directory too, which is where F$Load looks
    for a trap handler and the whole point of that probe.
  - `extract_pool.py` -- `load /h5/cio` before the unpacker runs.

The Microware `load` at `~/Developer/os9/play/oskBoot/CMDS/NOCSL/load` is no
longer needed for anything.

## Get running in two minutes

    cd ~/Developer/os9/osk-freeware
    export OS9EXEC=~/Developer/os9/os9exec/os9exec
    export OS9CLEAN=${TMPDIR:-/tmp}/os9clean

    tools/rebuild/make_overlay.sh            # the SDK build overlay
    tools/mkimage.sh $PWD/disk $PWD/osk-freeware.dd     # ~1 min
    tools/check_disk.py disk                 # eleven checks
    OS9DISK=osk-freeware.dd os9exec -r bash /dd/SYS/login    # a shell on the disk

**`osk-freeware.dd` is a build artefact and goes stale.** It cost a whole
exchange on 2026-08-25: the documented run command opened a five-hour-old image
and two new programs "did not exist". `verify_all.sh` now refuses to run
against an image older than the tree; nothing else checks. Rebuild it after
touching `disk/`.

## Where things stand

**THE SWEEP HAS NEVER LOADED A MODULE, and that invalidates part of it.**
Found 2026-08-27. All four stages run every program with nothing loaded, so
any program that links a library module exits early on `F$Link` and is
recorded on a condition that cannot occur on a real system. The six RTF
Fortran programs sat in the "silent in every stage" group for weeks for this
reason alone. Any verification pass that means anything has to `load` first --
see item 2. `notes/os9exec-bugs/PRIVILEGED-INSTRUCTIONS.md` has the re-run.


**The collection runs: 870 of 916 programs, 95.0%** — `DOC/STATUS`, measured
2026-08-26, all four sweep stages from scratch. 46 real programs need work
(`notes/verify-final.tsv`); the other 24 of the raw 70 are trap handlers,
libraries and shell scripts that were never meant to run bare.

**THAT 95.0% IS SUPERSEDED** by the four stages run with an environment and
the library modules loaded, 2026-08-28: 871 of 922, 94.5%, and the two
figures are not comparable because 23 files that are not programs came out
of the denominator. What follows is why the old one was not to be trusted
either, and it still applies to any figure scored by what a program PRINTS.

**TREAT THAT 95.0% AS STALE IN BOTH DIRECTIONS.** It is too kind, because it
scores a program by what it PRINTS -- `zip`, `todos` and `pnmtosir` are all in
the 870 and all three are broken, which the data tests proved on 2026-08-27.
It is also too harsh, because it loaded no modules (above) and because nine
netpbm programs have since been repaired. The honest figure needs the re-sweep
plus the Tier A suites. Do not quote 95.0% as if it meant "works".

**Source coverage 66%** — 626 of 939, up from 41% on 2026-08-25. Run
`tools/src_census.py disk` rather than quoting that.

---

# THE THING TO UNDERSTAND FIRST: version skew, not emulator bugs

Most of 2026-08-26 went into three claimed os9exec defects. **Two were
withdrawn or reattributed, and the reason matters more than the bugs.**

## The rule

> **"Trap-library build fails, static build works" is a VERSION-SKEW
> signature on this collection, not evidence about the emulator.**

A `-qm` build never enters cio, so it cannot testify about how os9exec handles
cio. I used that inference twice in one night and it was unsound both times.
It is now in `CLAUDE.md`.

## What is actually skewed, measured

    what we SHIP            bytes   edition
      cio                   18058     6
      csl                   47192    16      <-- nine editions behind the SDK
      csl020                43794    15
      math                   7798    13
      math881                3220     6

Every `csl` in the SDK — 68000, 68020 and CPU32, three different builds — is
**edition 25**. Ours is 16, and our `csl020` is 15, so our two are not even the
same edition as each other. Direct evidence, hit twice: the SDK's `load` run
against the disk's `csl` stops with `**** csl traphandler mismatch ****` and
runs clean against the SDK's own.

`cio` shows no skew by edition — three distinct binaries on this machine and
**all three are edition 6**, which is itself odd. There is exactly ONE `cio.l`
anywhere (4453 bytes, 1990-05-24, identical on `oskBoot` and `h4`), so every
program here was linked against that one library. No fourth cio exists on this
machine: I checked all 530 archives in the content index and swept the
filesystem.

## Why this is NOT a nightmare, and what to do about it

**The skew does not touch what ships.** The archive binaries that use cio were
built by their own authors against their own matching runtime, and they work —
`banner`, `cursive` and `fortune` all pass, and 621 programs run bare. The
2026-08-26 sweep is the evidence.

**It only bites programs WE rebuild with `-qixm`**, which links the SDK-era
`cio.l` and then runs against the older shipped `cio`. Nothing built by the
driver is currently installed, so **nothing shipped is affected today**.

**`-qm` IS the driver's default as of 2026-08-27** — but not for the reason
this section originally gave. A `-qixm` binary's stdout does not work under
os9exec **even with the SDK's own matched `csl`**, so the skew is not the
cause. The skew is real, measured, and a separate fact. Either way: `cio` keeps
shipping for the 367 starred archive binaries that need it, and we stop trying
to reconcile Microware's editions, which we cannot do and do not need to.

Two recipes already carry `TRAPFREE` for exactly this reason (`card`,
`travesty`) and say so in the file.

## The one thing that may still be an os9exec defect

`notes/os9exec-bugs/` — the `F$SRqMem` storm. A cio-linked program asks for
413,256 bytes once per `putchar`, never frees, exhausts the arena.
Independently reproduced by the os9exec session on a licensed disk with a
different cio edition, same counts. **Attribution is unsettled** and the
os9exec side now believes it is ABI skew rather than their bug.

What I contributed and what is still open is in that directory's README. Two
things there are worth not re-deriving:
  - the `a3+$3C` correlation is a coincidence — it does not hold on this build
  - the absurd value is `process data block base + $48`, invariant across
    `-qixm=4k/16k/64k` while cio's own code address moves

**Do not spend more time on it without a specific question to answer.** It is
interesting and it is not blocking anything.

---

# What to work on, in order

**STEP 1 OF THE PLAN IS DONE AND STEP 2 IS UNDER WAY, 2026-08-27.**
`tools/datatest.py` proves a program by the DATA it wrote, one emulator start
per family. Three suites exist -- `netpbm` (43), `encoding` (10),
`archives` (10) -- **63 cases, 60 passing.**

What it repaired: **nine netpbm programs died of a 3072-byte stack** and now
ask for 64k, via the new `tools/set_stack.py` (patches `M$Stack` in place and
recomputes the CRC; the field is past the 48-byte header so parity is
untouched, and that is asserted either side). Five went from broken to
working, four stopped crashing on input they cannot read.

What it found and did NOT fix -- all three kept as FAILING cases on purpose,
and all three documented in `DOC/INDEX` for users:

  - **`zip` cannot write its archive.** Deflates, writes `_Z000003`, fails to
    rename it over the target. Two directories tried.
  - **`todos`/`toos9` are no-ops.** Byte-identical in and out on CR-only OS-9
    text, which is exactly what they claim to convert. **This is the case
    that justifies the method**: the round trip passes precisely BECAUSE
    neither does anything.
  - **`pnmtosir`/`sirtopnm` do not round-trip.** Right size, channels rotated
    over the first half of the pixels.

Also: `uuencode`'s own usage line is wrong -- give it ONE argument, the input
file, and redirect.

**THE PLAN IS `notes/PLAN-verification.md`.** Written 2026-08-27 at rdoggett's
request. It sets the bar (every program PROVEN TO DO ITS JOB), splits the 834
catalogued programs into four tiers by what would actually prove them, and
gives an order and an estimate -- about fifteen working sessions, not a
lifetime. The list below is what was open before that plan existed; the plan
subsumes items 3, 5 and 6.


1. ~~Make `-qm` the default for installed rebuilds.~~ **DONE 2026-08-27, and
   the REASON in this file was wrong.** `-qixm` does not fail because of our
   version skew. Re-measured against the SDK overlay, with the SDK's OWN `csl`
   present: `-qixm` putchar wrote 0 characters and 3888 x "No more memory !!!";
   `-qm` wrote all 4000. Skew is not what breaks it. Attribution — os9exec's
   `F$SRqMem` or cio's ABI — stays unsettled; the decision does not depend on
   it. `notes/os9exec-bugs/SRQMEM.md` has the run.
2. ~~Ship a `load` command.~~ **DONE 2026-08-27.** The os9exec project
   contributed a clean-room implementation, rdoggett handed the source over
   (*"Move load.c into your files; you own it now"*), and it is built here
   trap-free and installed as `CMDS/load` with its source in `SRC/load`. Its
   `-?` names itself as a clean-room reimplementation. `OS9MDIR` is out of
   every tool -- see the section above for what each one does instead.

3. **The programs that need work** — `notes/verify-final.tsv`, filtered by
   `tools/module_census.py` for what is actually a program. Read `DOC/STATUS`
   FIRST: most of the 45 are already explained and closed there (supervisor
   state, no FPU, `F$SysID` unimplemented, silent-by-design daemons). Subtract
   item 2's six and the genuinely open residue is small.
4. ~~netpbm recipes.~~ **DONE 2026-08-27: 152 of 168 build**, four libraries
   installed in `disk/LIB`. `notes/COMPILE-AUDIT.md` has the 16 that do not,
   grouped by measured cause, and one OPEN constraint worth knowing: through
   the shell a `cc` line with 19 `-l=` flags silently loses its `-V=` flags,
   forking `cc` directly with the same argv does not, and it is NOT line
   truncation -- the line is 469 characters against SCF's 512. Mechanism
   unknown.
5. **The rest of the pool pass** — `tools/index_archives.py` and
   `tools/find_missing_source.py` are new and did most of tonight's work.
   32 candidates remain, and `COMPILE-AUDIT.md` lists twelve already REFUTED
   so they are not re-chased.
6. `sc` builds except for `wrefresh`; `notes/COMPILE-AUDIT.md` has exactly
   where it stops.

## Not urgent, and deliberately not on the list

GitHub: no repo, no remote, Pages off, CI never run. rdoggett, 2026-08-26:
*"we will come to that naturally when we are willing to put this on github.
Why on earth would you prioritize this when we dont even have a repo ready to
share yet?"* It waits on the collection being worth pushing, which is what
items 1-6 are for.

Also open and needing him, not you: the gcc packaging decision (2026-08-24).

**`wc`'s provenance is CLOSED, 2026-08-27.** rdoggett: *"I do not have wc."*
There is no copy to compare against and no thread left. Stop pulling on it.

## PLAY-TESTING: tools/playtest.py, AND THE TWO WAYS IT LIED TO ME

Built 2026-08-27 because rdoggett kept finding broken programs by hand:
*"A very small sampling showed more than half had issues... Would it be
unreasonable to expect you to try running them, not just to see if they crash
BOOM on launch, but to make sure they work as expected."*

    tools/playtest.py --all      # drive every script in tools/playtests/
    tools/gen_screens.py         # fold the captures into the catalogue

It drives a program on a **pseudo-terminal** at human typing speed, runs a
CONTROL pass with no keys, and renders both with `tools/ansiscreen.py` into
the 80x24 grid a vt100 would show, and `gen_screens.py` puts it on the
program's card in the catalogue.

**IT USED A FIFO FIRST, AND A FIFO IS NOT A TERMINAL.** Programs that call
`isatty()` or reopen their own tty take a different path, and so does os9exec
-- it puts a *tty* into raw character-at-a-time mode at startup and leaves a
pipe alone. `hack` "hung" under the FIFO harness and works perfectly for a
person. rdoggett: *"hack works for me."* Use the pty; never go back.

**EVERY FALSE PASS IT HAS GIVEN, so nobody rebuilds them.** Each of these
scored a broken program as working, and each was found by looking at a screen
rather than at a number:

  1. **A FIFO is not a terminal** -- `hack' hung under it and plays fine for a
     person. Use the pty.
  2. **Judging the last frame only** -- `hang' clears the screen when the game
     ends, so a working hangman looked empty. Judge every snapshot.
  3. **No login environment** -- `sokoban' said "cannot get your username".
     The harness now exports what `SYS/login' does.
  4. **Ink counted the shell's own lines** -- `pacman', `chess' and `lorenz3d'
     passed on the strength of my export lines while drawing NOTHING. The
     screen is cleared before the program starts, and ink now ignores any line
     holding `bash#'.
  5. **Complaint keywords convicted prose** -- "No such" matched a line of
     `sonnet's own poetry, and "Can't install trap handler" matched the text
     of README-CIO while `elvis' was displaying it. Phrases are specific now
     and a script can `allow' one.
  6. **Demanding a response from programs it never typed at** -- most of this
     disk is print-and-stop, so seventeen healthy programs failed at once.

**IT SCORED A PROGRAM THAT NEVER STARTED AS PASSING.** `snake` hangs at
startup perhaps one run in eight, so the keyed screen held a bash prompt while
the CONTROL screen held a drawn board. The two differed, so "responds" was
true and it passed. There is now a `starved` check: a keyed run that drew LESS
than the control is a failure.

**The terminal-size class is now testable -- DONE 2026-08-27.** A `size ROWS
COLS` directive sets both the pty's window size and the render grid, so a
script can ask what a program does in a window that is not the 80x24 its
termcap promises. `life` was the exemplar and it is now measured, not asserted:
at 40x12 its status line is written straight through the middle of the board
(`Gene@..@@@: 3`), and the mechanism is NOT scrolling -- it addresses line 24
absolutely and a short terminal clamps that into the picture. The evidence is
in `DOC/README-RUNNING`.

`life.keys` now carries `expect Cycles every 8 generations.`, which is the
assertion that sees it. **It was made to fail before it was believed**: the
same script with `size 12 40` reports `missing=['Cycles every 8 generations.']`.

**But the harness still scores a garbled screen as PASS unless a script asserts
against it.** At 40x12 every generic check was happy -- it drew, it responded,
no orphans. Only the `expect` caught it. Any other full-screen program wanting
this coverage needs its own such assertion; there is no automatic detection.

## SNAKE STILL HANGS AT STARTUP ABOUT ONE RUN IN EIGHT

Measured on the ARCHIVE binary, so it is not something we introduced:

    with keys     drew 18 of 20
    without keys  drew 17 of 20
    archive 11/12 vs our rebuild 10/12 -- indistinguishable

A failing run emits the keypad-init string `ESC[?1h ESC=` and stops before
`setup()` ever draws: 289 bytes instead of ~780. Keys are NOT the trigger.
**All of those numbers came from the FIFO harness and are worth re-taking on
the pty before anyone reasons from them.**

A six-run sample said 6/6 against 4/6 and I believed it and reverted a good
change on that basis. Twelve runs said 11/12 against 10/12. Do not conclude
anything here from fewer than about twenty runs.

## THE SWEEP CANNOT TEST INPUT, AND IT SCORES SUCH PROGRAMS AS WORKING

Found 2026-08-27 by rdoggett spot-checking games from `/h0/cmds/games`.

`GAMES/tet` was scored **"OK bare"** by the four-stage sweep and **took no
keys at a real terminal**. The sweep scores a program by what it PRINTS; `tet`
prints its board on startup, so it passed. It cannot press keys, and `tet`
calls `ttyname(0)` and reopens it, so it cannot even be driven through a pipe.

**A working rebuild had been sitting in `CMDS/REBUILT/tet.unixlib` since
2026-08-13**, with a `DOC/INDEX` note saying "if it takes keys for you, it
should replace GAMES/tet" -- waiting on a play-test nobody did. Now installed.

Two lessons, and the second is the bigger one:

  - **Any program whose value is in its INPUT handling is uncredited by the
    sweep**, whatever `DOC/STATUS` says about it. Editors, games, anything
    interactive. `notes/PLAYTEST-QUEUE.md` exists for this and is the thing to
    work through, not the sweep numbers.
  - **The rebuild driver INSTALLS NOTHING.** It writes `R_<prog>` into
    `disk/SRC` and those get deleted after every run, because `check_disk`
    fails on build products in the tree. So "we built a working X" and "the
    disk ships a working X" are separate facts and nothing reconciles them
    automatically. `tet` is where that gap bit. When a rebuild is BETTER, the
    swap is a deliberate, separate act -- do it, or the note saying it should
    happen will sit there for months.

## Rules that cost real time to learn

  - **Never edit a script while a run is reading it.** bash reads a script by
    byte offset. I did this to `verify_all.sh` mid-sweep on 2026-08-26 and it
    died at row 928 of 940 with a syntax error on a good line.
  - **Every tool in a capture pipeline needs `LC_ALL=C`** — `tr`, `cut`, `awk`.
    Four were missing it across the sweep's four stages, so any program
    emitting a byte above 127 was classified on an empty capture. All fixed.
  - **A name match is a lead, not a finding.** Prove source against the binary:
    byte-identical if the archive carries one, or match the binary's own
    distinctive strings. Twelve candidates were refuted that way.
  - **Grep CR-only files through `tr '\r' '\n'` first** or you dump the whole
    file as one line. Cost context three times in one night.
  - **Make every check fail once before believing it.** Two of tonight's three
    "defects" came from a check that had only ever succeeded.
  - Read `check_disk.py`'s OUTPUT, not its exit code.

## Where the detail is

  - `notes/os9exec-bugs/` — the reproductions, and what is unsettled
  - `notes/COMPILE-AUDIT.md` — why each tree has no recipe, and refutations
  - `notes/FOR-RDOGGETT.md` — open questions for rdoggett. Keep it SHORT; he
    has said twice that he skips long files. Answers go here, not there.
  - `DOC/STATUS` — every program, run and classified, with the failures grouped
    by cause. The authority on what does and does not work.

**notes/ was pruned 2026-08-27, 74 files to 36.** Session logs, superseded
plans and pool working data were deleted; `git log --diff-filter=D --name-only`
finds any of them if you need one back.
