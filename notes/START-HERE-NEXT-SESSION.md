# Picking this up cold — updated 2026-08-27, end of session

Branch `release-pass-2026-08-21`. **Tree clean, all eleven `check_disk.py`
checks green, `osk-freeware.dd` current.** Nothing is half-finished; every
change below is committed.

## DO THIS FIRST — the next three actions, in order

Do not re-plan. `notes/PLAN-verification.md` is the plan and it is current.
Do not stop between items to report; commit and start the next one.

**1. Text tools — `tools/datatests/text.cases` (does not exist yet).**
   81 programs in Tier A, the largest untested block after netpbm. Same shape
   as the three suites that exist: known input, checked output. Model it on
   `tools/datatests/encoding.cases` and remember its lesson -- a program that
   does NOTHING round-trips perfectly, so every transform also asserts that
   it CHANGED something.

**2. Finish the archive family** — `tools/datatests/archives.cases` covers
   compress, gzip, tar, zoo. Still untested: `ar`, `ar2`, `lha`, `lharc`,
   `shar`, `marc`/`dearc`, `arc`, `booz` extraction, `funzip`, `zipsplit`.

**3. Re-sweep with `load`** (step 0 of the plan, still not done). Every sweep
   this collection has ever run loaded NO modules, so every program that
   links a library was recorded on a condition that cannot occur on a real
   system. Until this is redone `DOC/STATUS` overstates what is broken.

## How to run the three test harnesses

    export OS9EXEC=~/Developer/os9/os9exec/os9exec

    tools/datatest.py --all          # Tier A: data in, data out. FAST --
                                     # one emulator start per family
    tools/playtest.py --all          # Tier B: pty, screen read. SLOW, hours
    tools/check_disk.py disk         # eleven invariants; read the OUTPUT

Current: **63 data cases, 60 passing** (`tools/datatest.py --all`, verified
at end of session). The three failures are EXPECTED and are real defects in
shipped programs, kept failing on purpose:

    archives  zip-cannot-write-its-archive
    encoding  todos-must-change-the-file
    netpbm    sir-round-trip-is-lossy

If one of those starts passing, something was fixed -- find out what before
celebrating. If a FOURTH appears, that is a regression.

## Using `load` — Microware's, for now

rdoggett, 2026-08-27: *"You should NOT be using OS9MDir the way that you are.
You should not use it at all. I will provide an implementation of load that
you will be able to use. For now you may use Microware's load."*

**`OS9MDIR` is gone from all user-facing documentation and must stay gone.**
It is an os9exec environment variable and documenting it taught an emulator
mechanism as if it were OS-9. It survives only in host-side TOOLING
(`mkimage.sh`, both `probe_runnability*`, two `rebuild/*`, `extract_pool.py`)
where it is load-bearing until his `load` lands.

Use the SDK's **trap-free** build -- the ordinary one stops with
`**** csl traphandler mismatch ****` against our edition-16 `csl`:

    ~/Developer/os9/play/oskBoot/CMDS/NOCSL/load

**TESTING ONLY. It must never be committed into `disk/`.** Working shape:

    env OS9DISK=$PWD/osk-freeware.dd OS9H1=<scratch> OS9H4=<sdk>/CMDS \
        os9exec -r bash /h1/script.sh
    # inside the script:  /h4/NOCSL/load /dd/CMDS/os9lib

`tools/datatest.py` already does this itself for any `.cases` file with a
`load` line; it copies the binary to a scratch `h4` and never into the tree.

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
2. **Ship a `load` command.** REOPENED 2026-08-27 by rdoggett, who is
   providing a freeware implementation: *"You should NOT be using OS9MDir the
   way that you are. You should not use it at all. I will provide an
   implementation of load that you will be able to use. For now you may use
   Microware's load."*

   The 2026-08-27 decision AGAINST this was wrong, and the reason it was wrong
   is worth keeping: it rested on `OS9MDIR` being an acceptable substitute.
   It is not. `OS9MDIR` is an **os9exec environment variable**, and
   documenting it to users taught an emulator mechanism as if it were OS-9 --
   the same class of error as calling this a "boot disk". It has been purged
   from `DOC/README-RUNNING`, `DOC/README-FORTRAN`, `DOC/INDEX`, `DOC/STATUS`
   and the generated web catalogue.

   **For now use Microware's `load`, for TESTING ONLY -- it must never be
   committed into `disk/`.** Use the trap-free build at
   `~/Developer/os9/play/oskBoot/CMDS/NOCSL/load`; the ordinary one stops with
   `**** csl traphandler mismatch ****` against our edition-16 `csl`.
   Working invocation:

       env OS9DISK=$PWD/osk-freeware.dd OS9H4=<sdk>/CMDS \
           os9exec -r bash /h1/script.sh
       # inside: /h4/NOCSL/load /dd/CMDS/os9lib

   `OS9MDIR` is still used by host-side TOOLING -- `mkimage.sh`, both
   `probe_runnability*` scripts, two `rebuild/*` scripts, `extract_pool.py`.
   It is load-bearing there and comes out when the freeware `load` lands.

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
    tools/gen_screens.py         # turn the captures into docs/screens.html

It drives a program on a **pseudo-terminal** at human typing speed, runs a
CONTROL pass with no keys, and renders both with `tools/ansiscreen.py` into
the 80x24 grid a vt100 would show. `docs/screens.html` is the gallery.

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
