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

1. ~~Make `-qm` the default for installed rebuilds.~~ **DONE 2026-08-27, and
   the REASON in this file was wrong.** `-qixm` does not fail because of our
   version skew. Re-measured against the SDK overlay, with the SDK's OWN `csl`
   present: `-qixm` putchar wrote 0 characters and 3888 x "No more memory !!!";
   `-qm` wrote all 4000. Skew is not what breaks it. Attribution — os9exec's
   `F$SRqMem` or cio's ABI — stays unsettled; the decision does not depend on
   it. `notes/os9exec-bugs/SRQMEM.md` has the run.
2. ~~Ship a `load` command.~~ **DECIDED AGAINST, 2026-08-27.** rdoggett asked
   the right question -- *"do you feel load is essential? Like, should we
   rewrite our own load?"* -- and the answer is no.

   `load` is Microware's, it is a standard system utility, and anyone running
   OS-9 has it. Shipping our own reimplementation that behaved *almost* like
   the real one is exactly the kind of trap this collection avoids.

   **And it was never needed.** The only real beneficiaries were the RTF
   Fortran six, and the route already existed: point `OS9MDIR` at a HOST
   directory holding `os9lib`. The repository ships `disk/` as a host tree, so
   that directory is `<repo>/disk/CMDS` and is already on the user's machine.
   Verified that day: with `OS9MDIR=$PWD/disk/CMDS`, `rtf` starts and asks for
   a source file; without it, `rtf` prints nothing. What was actually missing
   was DOCUMENTATION -- `DOC/README-RUNNING` never mentioned `OS9MDIR` at all.
   It does now, and `DOC/README-FORTRAN` names both routes.

   The `Graph` seven and `rxmod` were never candidates: they bus-error on the
   supervisor bit whatever is loaded.

3. **The programs that need work** — `notes/verify-final.tsv`, filtered by
   `tools/module_census.py` for what is actually a program. Read `DOC/STATUS`
   FIRST: most of the 45 are already explained and closed there (supervisor
   state, no FPU, `F$SysID` unimplemented, silent-by-design daemons). Subtract
   item 2's six and the genuinely open residue is small.
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

Also open and needing him, not you: the gcc packaging decision (2026-08-24).

**`wc`'s provenance is CLOSED, 2026-08-27.** rdoggett: *"I do not have wc."*
There is no copy to compare against and no thread left. Stop pulling on it.

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
