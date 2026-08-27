# Picking this up cold — written 2026-08-27

Branch `release-pass-2026-08-21`, **184 commits ahead of main, nothing pushed**
(there is no git remote and no GitHub repo yet — see "not urgent" below).
Working tree clean, all eleven `check_disk.py` checks green.

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

**The collection runs: 870 of 916 programs, 95.0%** — `DOC/STATUS`, measured
2026-08-26, all four sweep stages from scratch. 46 real programs need work
(`notes/verify-final.tsv`); the other 24 of the raw 70 are trap handlers,
libraries and shell scripts that were never meant to run bare.

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

**The recommendation, and it is one line:** make `-qm` the driver's default
for anything we install. `-qm` has never failed this way. It costs size
(the driver's own measurement: 14286 bytes against 2610 for `ascii.c`) and
buys a binary that stands alone and cannot skew. `cio` keeps shipping for the
367 starred archive binaries that need it. Stop trying to reconcile Microware's
editions; we cannot, and we do not need to.

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

1. **Make `-qm` the default for installed rebuilds** and write down why. Small,
   settles the whole class above. Then the two `TRAPFREE` recipes lose their
   special-case comments.
2. **The 46 programs that need work** — `notes/verify-final.tsv`, filtered by
   `tools/module_census.py` for what is actually a program. Eight of them are
   the `Graph` group, which needs a `load` on the disk (see below), not an
   emulator fix.
3. **Ship a `load` command.** Eight programs link a library module sitting
   beside them on the image and cannot find it, because a user following
   `DOC/README-RUNNING` never sets `OS9MDIR` and this disk has no `load`.
   That is ours, and it is the cheapest real fix on the list.
4. **netpbm recipes** — all 169 now have source; `notes/COMPILE-AUDIT.md` has
   the shape of the work (four library recipes, then 169 one-source ones). Big,
   mechanical, ideal for a long unattended run.
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

Also open and needing him, not you: the gcc packaging decision (2026-08-24),
and `wc`'s provenance (unsettled, nothing left to pull on).

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

  - `notes/SESSION-2026-08-26.md` — the whole overnight pass
  - `notes/os9exec-bugs/README.md` — the reproductions and what is unsettled
  - `notes/COMPILE-AUDIT.md` — why each tree has no recipe, and refutations
  - `notes/FOR-RDOGGETT.md` — what needs him, newest first, short on purpose
  - `notes/AGENDA-2026-08-26.md` — the ordered list this replaces
