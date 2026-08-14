# Play-test queue

Things that need a human at a real terminal, with exactly what to type. Each
one is a candidate I could take no further from a pipe: os9exec's stdin is not
a tty, and several of these programs ask the terminal about itself before they
will work.

## 1. tet, rebuilt -- does it take keys now?

**Why:** `GAMES/tet` draws its board and ignores the keyboard. The cause is in
its source: the raw-mode setup (`ioctl(TCGETA)`, reopening stdin `O_NDELAY`)
is entirely inside `#ifndef OSK`, so the OS-9 build has no terminal setup at
all and its `read(0, combuf, 1)` never sees a keystroke.

`REBUILT/tet.unixlib` is the same source compiled with that path **enabled**,
linked against `LIB/unix.l`, whose `ioctl.c` implements TCGETA/TCSETA over
`_ss_opt`. It draws identically to the original. Whether it now reads keys can
only be seen at a terminal.

    chd /dd/CMDS/REBUILT
    tet.unixlib

Keys are on its own menu: `q` quits, `p` pauses, `b` is the boss key, `s`
shows the score. **What to report:** does `q` quit? If yes it is fixed, and
it should replace `GAMES/tet`. If it still ignores everything, the raw-mode
call is failing and the next thing to look at is whether `_ss_opt` accepts
what ioctl.c sends it.

## 2. The other stuck games

- **`lander`** -- takes no input, corrupt screen after a crash. Its OSK
  conditionals are about `M_PI` and `random`, not input; it reads with curses
  `wgetch`. The live theory is still its README's: it wants SysV curses line
  drawing that vt100 termcap does not provide. Worth trying under a terminal
  type with line-drawing if you have one.
- **`snake`** -- starts and sits. It DOES call curses `raw()`, so the terminal
  mode is not the problem and it does not share tet's cause. Unknown.
- **`maze`** -- starts and sits. No source anywhere, so it can only be
  play-tested, not diagnosed.

## 3. The three vi editors

`DOC/README-VI` compares them on paper -- source lineage, option counts,
documentation. What it cannot say is which is pleasant to use. All three are
worth ten minutes each:

    vi /dd/tmp/x        the real Berkeley ex/vi
    elvis /dd/tmp/x     the clone with the most options
    vi_nocio /dd/tmp/x  the small one

## 4. Anything curses

`oleo`, `mines`, `checkfile`, `sc` and `scqref` all want a real TERM and were
only checked far enough to see them start.
