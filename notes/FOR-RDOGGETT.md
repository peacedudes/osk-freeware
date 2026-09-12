# For rdoggett

Only what is waiting on a decision of yours. Everything done, and why, is in
git history and `notes/START-HERE-NEXT-SESSION.md`; this file carries none
of it. Updated 2026-09-11, night.


## One decision: a `shell' module, and the hazard attached to it

Programs that call `system()' do nothing on this disk, and tonight we found
out why. Microware's C library `system()' forks the bare module name
`shell' and never reads `$SHELL' at all. This disk has bash, ksh, sh,
gshell and mshell -- nothing named `shell' -- so the fork fails with
"module not found", nothing runs, and `system()' hands back a junk number
that changes between runs. Traced under `os9exec -d 0x0002', and confirmed
independently by the os9exec session against its own SDK-built probe.

**What fixing it buys: one program.** `m4's `syscmd' is silent without it
and prints its answer with it. That is the only shipped program affected.
gawk's OS-9 port disabled `system()' outright; `make' calls `os9exec()'
directly; and `tex', `latex', `eo' and `maketexpk' give identical output
either way -- which disproves what `DOC/README-SHELLS' and `SYS/login' have
both claimed since 2026-08-31. Both are now corrected. (`ed' does call
`system()', but its `!' escape fails earlier, on a scratch file it opens as
`/r0/ed.XXXXXX', so this alone would not revive it.)

**Why I have not just done it.** A real OS-9 system already has
`/dd/CMDS/shell' -- Microware's own. This collection is meant to be
installed onto a user's own `/dd', and the tar route would overwrite theirs
with a public-domain ksh. The bug exists only where this collection is the
whole world, which is the emulator; the hazard exists only where the bug
does not.

Three ways, all measured tonight:

  (a) Ship nothing. `README-SHELLS' now explains it. `m4's `syscmd' stays
      silent when the collection runs on its own.
  (b) Ship a copy of our own ksh as `CMDS/pdshell', with the MODULE renamed
      to `shell', and `load' it from `SYS/login'. No file called `shell'
      ever exists, so nothing of yours is overwritten, and the name is only
      claimed in memory. Measured: `system()' returns 0 and m4 answers.
      **This is the one I would take.**
  (c) Ship it as `CMDS/shell'. Simplest, and the one that can overwrite a
      real system's own shell.

Licence is not the obstacle: ours is pdksh, "Public Domain Korn Shell 4.3",
so a second copy under another name is free. The only question is whether
(b) is worth a 118 KB duplicate to restore one program's feature.

### 1. dvi2tty and disdvi -- built, working, not staged

`dvi2tty' prints a TeX .DVI file as text; `disdvi' dumps its structure.
Both build and run: pointed at `DOC/mg/mg_doc.dvi' it prints "The MG
Reference Manual / Release MG2A / Sandra J. Loosemore". It fills a real gap
-- TeX is here with eight DVI PRINTER drivers and nothing that shows a DVI
on screen.

The archive (Microware OS-9 archive 3861) states no terms. Its group's
`tex_readme' points at "the 'copying' and 'readme' files in ctexdoc.ar" --
and that turns out to be Pat Joseph Monardo's notice for **Common TeX**, a
different program by a different author. dvi2tty is Marcel J.E. Mol's C
translation (Delft, 1989-90) of Svante Lindahl's Pascal (KTH), and carries
no grant of its own. The one permission sentence in its README -- "use it
and improve as you wish" -- is about `disdvi' specifically.

Precedent cuts both ways: `cdecl', `xargs' and `which' ship worded "posted
to Usenet and freely redistributed since. No licence text accompanies the
source." But those were newsgroup postings; this came through the Microware
archive, and its author is alive and findable (Mol later released dvi2tty
under the GPL). **Ship on the no-notice precedent, ask Mol, or leave it
out?**

Second, smaller: its README's signature block ends with a Lennon lyric
containing an obscenity. `ORIG/' convention ships a release verbatim. Ship
it as-is, keep ORIG but leave the README out of `DOC/', or neither?

(The binaries live only in a session scratchpad and will not survive. That
does not expire the decision -- the archive and the build are recorded, and
rebuilding is about ten minutes.)

### 2. os9lib -- a compilation under four sets of terms

TOP's `os9lib' is what `uustat', `Browse' and several TOP games link
against, so this decides a batch rather than a program. Counted file by
file, all 47 sources:

     32  Ocker / Dessauer / Mellin, 1988 -- "distributed freely for any
         non-commercial purposes", commercial incorporation by permission.
         **Your existing ruling covers these.**
      2  `regexp.c', `regsub.c' -- Henry Spencer, Toronto 1986. Permissive.
     12  No notice, but identifiable: `rnd.c' is Berkeley 4.2 `random.c',
         `crypt.c' is Tanenbaum's textbook DES, the rest small shims.
      1  **`utime.c' -- Michael Hoffmann, 1988. Bare copyright, NO GRANT.**

I left `utime.c' out of the build rather than decide it: nothing in os9lib
calls it, `uustat' does not either, so dropping it costs nothing. Say if you
would rather it stayed.

One condition worth knowing even though it permits distribution: `info.c'
is Ocker's SYSINFO -- "please DON'T CHANGE ANYTHING ... You may not
distribute any modified versions". Unmodified is fine; that file must not be
patched.

**The question:** does os9lib ship on the 32-file non-commercial basis plus
the above? If yes, uustat and Browse follow, and so do the TOP games the
other session is holding. If you would rather leave TOP alone entirely, say
so and we both stop spending time on it.

(os9lib does not link yet for unrelated technical reasons. That is in
`notes/PLAN-acquisitions.md' under B6, not here.)


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
