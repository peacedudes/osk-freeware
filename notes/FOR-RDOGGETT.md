# For rdoggett

Only what is waiting on a decision of yours. Everything done, and why, is in
git history and `notes/START-HERE-NEXT-SESSION.md`; this file carries none
of it. Updated 2026-09-11, night.


## Settled 2026-09-12: the `shell' module, your way

You chose a fourth option and it is in (`4bdd22e6'): `SYS/login' now loads
YOUR Microware shell from /h1, beside the line that already loads runb --

    load /h1/CMDS/shell >/nil 2>/nil

Nothing of Microware's ships to make it work, no file called `shell' goes on
this disk where it could overwrite yours, and with no /h1 the line finds
nothing and moves on.  Measured both ways: with /h1 present `system()'
returns 0 and m4's `syscmd' prints its answer; without it, silence.

Two things recorded rather than left to be rediscovered.  `DOC/README-SHELLS'
and the SYS/login comment had both claimed since 2026-08-31 that SHELL=ksh is
what makes tex, latex, eo and maketexpk work; measured, all four give
identical output with SHELL unset, and the return value of `system()' tells
you nothing in either direction -- junk here, 0 on another machine -- so the
sound test is whether a redirect target was created.  Both documents say that
now.

Still open only if you want it: m4's `syscmd' stays silent for someone
running the collection standalone with no /h1.  That is the emulator
test-drive case, where the user has no Microware licence anyway.  Shipping a
renamed pdksh as a resident `shell' would fix it; you said you would sleep on
that, and nothing here needs it.

## Q2 again, with the sources located

You have had this one a while: the disk ships gcc, g++, VH, dvips, gawk,
bison and emacs as binaries without their source.  Measured 2026-09-12,
`src_census.py' puts it at 307 of 1005 programs with no source here, and
three of the named ones have a TOP tree sitting in the pool ready to stage:

    gawk   -> Scraped/.../os9/top/src/gawk2.0
    bison  -> Scraped/.../os9/top/src/bison
    emacs  -> Scraped/.../os9/top/src/emacs_3.10

Also `DRIVERS/nulman.lzh' from the refetch is dvips 5.5 source, misnamed.

Nothing is staged and nothing will be until you say so.  Say the word and
they go in with their own licence blocks read and recorded; say no and I
will note it settled so it stops coming back.

## One licence call: Microware's `fpu' module

The TELECOM refetch turned up `fpu' inside `xyz.lzh', and it carries its own
permission:

    FPU - (C) 1995 Microware Systems Corp.
    Permission to distribute FPU is granted so long as this file is retained.

That is a grant, in the file, from Microware.  But CLAUDE.md's rule lists
`fpu040' among the things that stay out, against the five modules you asked
Allan for and he agreed to.  I have not added it and will not without you.

It matters only a little: it is the floating-point emulation an Ultra C
build wants on a machine with no 68881, and the three programs in that
archive which need it (`k', `xy', `z') already run here without it.  So this
is tidiness, not a blocker.

## Programs that may be best forgotten

Each is measured and carded honestly as far as it goes. Removing any is
yours; none has been removed.

**Needs a display os9exec has not got.** G-Windows: `cyberwar', `puzzle',
`scriptmaster', `colortest', `dclock'. The Graph trap library: `apfel',
`g', `showpic', `sine', `striche', `graphdemo', `graphsave'. A TeleVideo
terminal: `umusek'. (`pacman' was wrongly on this list -- it is a keypad
ASCII maze game and draws fine. Kept.)

**Needs hardware or a peer it cannot have.** `splman', `lpsched' (a
printer). The RTF Fortran drivers `for', `lnk', `lnk.org' -- they print the
command they would run and stop; `rtf' is the working program of that set.
(`oleo' WAS on this list and is now off it: two F$STrap fixes in os9exec
on 2026-09-11 made it run, and it draws its copyright screen and its
spreadsheet grid and takes input. Verified here, not taken on report.)

**Broken or brittle here.** `dedit' spins for want of `tmode' and writes
raw sectors -- do not run it unsupervised. `names' prints garbage and never
terminates; `modinfo' does its job. `rstory2' forks four story programs
that never shipped with it. `ff' (German file-finder) hands off to
Microware's shell and `find' supersedes it. `splitalf' writes `<name>_0'
and stops, whatever it is given. `cuts -e' asks for gigabytes (`-d' decodes
fine). `dearc' reads MS-DOS ARC files and nothing here writes one -- it
could be given a sample the way the zip readers were, if you want it kept.
`game' and `postprint' want the `chess.lst' gnuchess writes on `list',
which the checkgame card already produces; not re-measured.

**Duplicates, one decision each:** the five GNU Chess builds, and `wc.cio'.
(`puz15' and `puzzle15' are NOT duplicates -- two different programs with
their own sources. Both stay.)


## Yours because the repos are yours

**os9exec -- nothing needed from you.** Both items that were here are
resolved or ours: `F$GPrDBT'/`F$GPrDsc' were fixed on 2026-09-05 (c024fbc)
and `devprc -a' and `aprocs' now run clean; `top' still crashes, but that is
top's own bug (it asks for PID 0, gets the documented refusal, ignores it
and reads an unfilled buffer) and would do the same on real hardware. The
emulator's two noisy lines go to STDERR, not stdout as this file used to
say, so `2>/nil' on a capture drops them -- that is ours to do, not theirs.
Giving emulator diagnostics their own channel is on the os9exec roadmap,
with our four affected cards recorded as the reason.

**creadoc**, if you want it runnable. It is an early Fortran documentation
extractor -- a 1988 forerunner of javadoc -- and worth keeping as that. It
reads the filename from column 53 of a `dir -eadu' listing and this disk's
`dir' puts it at 54 (the 2026 date, printed `126', pushes it along), so it
opens a space-prefixed name and stops. One constant (`fnpos = 53') in
`SRC/rtf/creadoc.f'. Rebuilding needs the RTF Fortran chain plus Microware's
r68/l68 on /h1, and it edits an archived binary. I would keep it as
documented historical software; rebuild only if you want it running.

**The `os9-dev` skill** (`~/Developer/os9/os9-dev-skill`): three gaps in
`references/common/using-os9exec-repl.md` -- the cio selector mismatch is
absent, "a usage message is a pass" is unsafe for that class, and a bare
relative `OS9Hx' path breaks file opens while module loading works. Say the
word and I write them in.


## Real OS-9, and the release

**The hardware step is written from what we know, not from doing it.**
Every guide opens with the real-system arrangement and offers two routes
onto a real disk -- the image written whole, or `osk-freeware.tar' unpacked
with the `tar' module shipped beside it. The guides say plainly we have not
done it on hardware. If you know anyone with a real system, that paragraph
is the one to have checked.

**The CI workflow does not publish the tar.** It builds the image; the tar
and the `tar' module are newer artefacts and want adding to what a release
carries -- your call with the release itself.

**Nothing is pushed or tagged.** The branch has never been pushed. The CI
pin in `.github/workflows/build-image.yml` is an old os9exec commit and has
never run for real. I can bump it and run the workflow locally; the push,
the tag and the merge to main are yours.
