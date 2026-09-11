# keep became a real installer (2026-09-11)

Report of the autonomous pass you asked for: make `keep` fetch the files a
program needs to run, place them right, never clobber a system directory,
preserve personalised files across a re-install, and have `unkeep` decide
carefully what to give back. Committed as `a366bd83`, gate green (25/25).

## What it does now

`keep <name>` brings, onto the target on /h1:

- the program;
- every data FILE DOC/DEPENDS says it opens that is here, by name;
- every data DIRECTORY it names, **copied whole** -- hack's playground,
  larn's PLAYGROUND, sokoban's screens and SAVES, wanderer's screens --
  dotfiles included, with empty directories created so the game has
  somewhere to save;
- a **termcap** entry, but only when the target has none of its own.

The old behaviour was the complaint you raised: a directory was "left for
you to decide about", and termcap was "nothing to do" -- true only when the
target WAS this collection. A plain OS-9 system has neither the playground
nor a SYS/termcap nor the login that sets TERMCAP, so a curses game kept
onto it could not find a terminal or its data. It can now.

## The safety rules

**Re-install.** Keeping a program a second time restores anything missing
and touches nothing you have made your own. A file keep wrote and you have
not changed is "already kept"; one you have changed -- a score, a save -- is
"left as is". So someone who thinks they trashed something can re-keep
without losing high scores.

**unkeep refcounts shared files.** termcap is the one that matters: keep two
curses programs and both record it on the receipt; unkeep one and the file
stays because the other still claims it. Only the last unkeep takes it.

**unkeep preserves your work by default, and `-a` clears it.** A file whose
checksum has changed since keep wrote it is left alone (that is how saves
survive). `unkeep -a <name>` removes those too, for a clean sweep rather
than a rescue -- the option you suggested instead of a prompt, since these
run non-interactively as often as not.

## Two bugs found and fixed on the way

Both in the new `keep_tree`, both caught by the harness, not by reading:

1. **larn's data files are real dotfiles** (`.larnmaze`, `.lscore12.0`).
   The first cut skipped any name starting with `.` to drop `.` and `..`;
   it now skips only those two exactly.
2. **A DEPENDS path that ends in `/`** (larn's `PLAYGROUND/`) does not read
   back as a directory under os9exec -- the directory read never reaches
   EOF, so it looped thousands of times over fragments of names. Trailing
   slashes are now normalised away, and a 20000-entry guard in `keep_tree`
   stops any runaway read from filling the disk. (Whether the non-EOF read
   is an os9exec bug in its own right is a separate question; normalising
   the slash is the right thing on real OS-9 regardless.)

## How it was tested

A minimal OS-9 target built fresh and cloned per test:
`scratchpad/target-base.dd` -- the shells, Microware's runtime (cio, csl,
math), and a login, but **no termcap and no game data**. Built with
`tools/mkimage.sh` from `scratchpad/minitree`, SKIP_CHECKS=1 (a minimal tree
is not the collection and does not pass the collection's own checks).

Verified, each on a fresh clone:

- `keep hack` -> hack, its whole playground, termcap, a receipt. Run from
  the target ALONE as /dd+/h0 it reaches the same first screen as from the
  full collection (it then hits the same pre-existing "illegal instruction"
  that hack throws when Ctrl-C interrupts a read under os9exec -- identical
  on both images, so not keep's doing).
- `keep larn` -> its PLAYGROUND dotfiles all land; larn shares termcap.
- `keep sokoban wanderer` -> screens/ and SAVES/ come whole.
- refcount: `unkeep hack` leaves termcap (larn needs it); `unkeep larn`
  then takes it.
- re-install: change `.lscore12.0`, `keep larn` again -> "changed, left as
  is", my content intact; unchanged files -> "already kept", 0 written.
- `unkeep larn` leaves the changed score; `unkeep -a larn` removes it.

The harness images are in the session scratchpad, not the repo.

## Build note

keep/unkeep/kept are one source, `disk/SRC/keep/keep.c`, three modules via
`MODE_UNKEEP`/`MODE_KEPT`. Rebuild with the recipe file in the scratchpad:

    OS9CLEAN=<overlay> OS9EXEC=<...>/os9exec \
      tools/rebuild/rebuild.sh scratchpad/keep.recipes disk/SRC
    cp disk/SRC/keep/R_{keep,unkeep,kept} disk/CMDS/    # then remove the R_ files
    tools/gen_depends.py disk ; tools/mkimage.sh disk osk-freeware.dd

The baseline build was confirmed byte-identical to the shipped binaries
before any change, so the toolchain is faithful.

## Left undone

- **fuddle's card** -- you reported it captures badly and garbles the
  terminal (escape sequences and a position dump leaking). Separate from
  keep; being looked at next.
- The DEPENDS improvement once imagined for the directory cases (listing
  each file) is **not needed** -- copying the directory whole supersedes it.
- Minor: README-KEEP's worked transcript still shows an older "keeping into
  /dd" example; cosmetic, left as is.
