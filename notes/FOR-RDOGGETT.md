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
that the disk needs an 80x24 terminal.

My harness no longer shares the blind spot. It can size the terminal now, and
`life` at 40x12 writes its status line straight through the middle of the
board -- `Gene@..@@@: 3`. So the warning in README-RUNNING is measured rather
than asserted, and `life`'s play-test carries the assertion that catches it.
The mechanism turned out not to be scrolling: `life` addresses line 24
absolutely and a short terminal clamps that into the picture, overwriting the
board in place. Nothing scrolls off, which is why it still looks like a board.

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

## 2026-08-27, second session

**You were right about `OS9MDIR` and it was worse than one bad habit.**
Purged from all four shipped docs and the web catalogue. Chasing it turned up
that **every sweep this collection has ever run loaded no modules** -- so any
program linking a library was scored on a state that cannot happen on a real
machine. That is why the six Fortran programs sat in "silent" for weeks. Using
Microware's trap-free `load` for testing only, never into `disk/`, until yours
lands.

**There is a plan now** -- `notes/PLAN-verification.md`. Four tiers by what
would actually prove a program, an order, and an estimate: about fifteen
working sessions, not a lifetime. Your bar, "proven to do its job", is what it
is built on.

**Three broken programs found, nine repaired.** A new harness
(`tools/datatest.py`) checks the DATA a program wrote rather than whether it
printed anything. 63 cases, 60 pass.

  - repaired: nine netpbm programs that died of a 3072-byte stack
  - broken, documented, left failing: `zip` (cannot write its archive),
    `todos`/`toos9` (do literally nothing), `pnmtosir` (corrupts half the
    image)

`todos` is the one worth knowing about: it round-trips perfectly *because* it
does nothing, so any test that only checked "does it come back the same"
would have certified it.

**The 95.0% figure in DOC/STATUS is stale in both directions** and should not
be quoted as "works" -- `zip` and `todos` are both inside the 870.

## Nothing needs you

