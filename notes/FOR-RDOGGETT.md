# For rdoggett

Terse on purpose. Everything before 2026-08-27 is in git history.

Branch `release-pass-2026-08-21`. All eleven `check_disk.py` checks green.

## Where you were right and I was wrong

**`hack` works — my test harness was broken, not hack.** It drove programs
through a FIFO, and a FIFO is not a terminal: programs that call `isatty()` or
reopen their own tty behave differently, and so does os9exec, which puts a
*tty* into raw mode at startup and leaves a pipe alone. Rewritten to use a
real pseudo-terminal. `hack` now plays; its inventory screen is in the gallery.

**`snake`'s startup hang is NOT something I introduced.** Archive binary:
drew 18 of 20 with keys, 17 of 20 without. It hangs about one run in eight,
emitting the keypad-init string and stopping before it draws. I earlier
blamed my own change on a six-run sample (6/6 vs 4/6) and reverted a good fix
on that basis. Twelve runs said 11/12 vs 10/12. Still open.

**`life` and terminal size: you are right and it cannot be fixed in `life`.**
os9exec implements no screen-size call at all, so a program can only learn its
size from termcap, which says 24x80. `DOC/README-RUNNING` now says in bold
that the disk needs an 80x24 terminal. My harness renders 80x24 too, so it
shares the blind spot.

## Fixed and verified this session

  - **`tet`** -- three separate bugs. `tsleep(1)` sleeps NOTHING (500 calls,
    0 seconds; `tsleep(2)` really is 20ms) so the game ran at CPU speed;
    SCF echo corrupted the board; the high-score file pointed at `/usr/tmp`,
    which does not exist here. Plays properly now, ~1.5s a cell, scores kept
    in `/dd/GAMES/tet.hs`.
  - **`life`** -- died with `**** Stack Overflow ****` after one generation.
    The build driver had a hardcoded 16k. Added a `MEM=` recipe flag; `life`
    builds at 64k and now runs to "Generation: 9, cycles every 8 generations".
    That flag will fix other things.
  - **`who` and `mscheck`** -- your find. They were the only two files in
    `/dd/CMDS` shipped WITHOUT an execute bit, because `mktar.py` set it from
    the module magic number and those two are shell procedure files. Fixed at
    the source. (`who` is written in OS-9 *shell* syntax on a disk whose
    shells are bash and sh -- that is why it "partly works", and it needs a
    rewrite, not a permission.)
  - **netpbm** -- 152 of 168 build from source now, plus four libraries.
    Three genuine upstream bugs found doing it.

## Look at this

`docs/screens.html` -- 16 programs photographed while running, linked from the
catalogue. Every screen came from keystrokes fed to a running program.

## Nothing needs you

