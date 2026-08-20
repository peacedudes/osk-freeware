# play/h4/ARR — the 1989 usenet collection, opened and triaged

Written 2026-08-19. Tool: `tools/mine_arr.py`, which extracts each archive with
the collection's own `ar2` under os9exec and screens every member with
`tools/screen_microware.py`.

**What this is.** rdoggett's personal collection, grabbed off usenet around
1989, built, and filed. In his words: junk and stuff, archived mainly to
shrink it; some of it not worth sharing; expect redundant lint and don't fret
tossing things. He also said it **once contained proprietary Microware source
files** and believed those were removed. Belief is not a check, so every one
of the 1,192 members was screened.

    65  archives          1,192 members
     1  archive flagged for Microware source  -> EXCLUDED
    33  members are junk (empty files, .bak/.orig leftovers)
    50  archives already have a matching disk/SRC tree

## The one that mattered

**`curses.ar` — EXCLUDED, and this is the find.** It holds a curses
implementation with full C source, a `curses.l` linkable library, and two
headers: `curses.h` is **82% line-identical to the SDK's `curses.h`**, and
`curseslib.h` is 80%. That is Microware source, and source is precisely the
category that matters — see below. It was never on the disk, so nothing had to
be removed; the screen caught it at the candidate stage, which is what the
screen is for.

## Why source is the category, and not binaries

Relayed by rdoggett, 2026-08-19: Microware's concern is **source code**,
because **infrastructure in Japan and Germany runs OS-9/68k today** and they do
not want source published that might expose vulnerabilities nobody has found
yet. It is an operational worry, not a commercial one.

That also explains why permission for `cio`, `csl`, `math`, `math881` and
`csl020` was straightforward: those are runtime **binaries** and expose
nothing. So a Microware binary found in an archive is merely their property; a
Microware **source** file — kernel, file manager, driver, system internals — is
the one that could hurt somebody. `screen_microware.py` weights it that way.

## What was actually new

**`chess.ar` — installed.** Four engine source trees (`CH`, `CH3`, `CH4`,
`CH5`, 23 files) for the `chess` in `CMDS/GAMES`, which has no source.
`DOC/ORIGINS` already promised a `SRC/chess` tree and there was none; now
there is. `fuddle`, also in this archive, is already on the disk.

## What was already mined — most of it

**`ARR/x` was a false alarm of mine.** I reported it as holding source for five
games on the disk that had none — `pacman`, `valspeak`, `newsgen`, `worms`, `rain`.
Wrong: all of it is already in `disk/SRC/toys`, 11 of 15 files byte-identical.
The error was searching for a *directory* named after each program instead of
the files inside a tree named for the archive — the exact mistake CLAUDE.md
warns about ("a source tree in SRC/ is named by ARCHIVE, not by program"), made
anyway. The four that differ do so by exactly 19 bytes each, a header line.
The remainder of `ARR/x` is junk: a two-line `cc` build script, `make.news`,
`makval`, and `screen.h.bk` / `wish.orig` backups.

**`wand3.ar`** — 114 members, Wanderer with `WAND_SCREENS`, icons and bitmaps.
Adds nothing: the disk already carries **51** screens to the archive's 50, and
every shared name is byte-identical. `wanderer` runs and draws its board.

**`unix.lib.ar`, `de.ar`, `srt.ar`** — already present as `SRC/unixlib`,
`SRC/deansi`, and the `sort` already here. `de.ar` additionally carries `tst.out`
and a file called `mine`, which is scratch.

**Known refusals, unchanged** — `cdecl` (ANSI C source, Microware C is K&R),
`phan` (18 corrupt bytes in every copy), `gammon` and `tet2` (want BSD
`sgtty.h`), `hack` (source damaged in all three copies; the binary is here).

## Worth a look, not yet acted on

  - **`pcomm.ar`** — Pcomm v1.1, Emmet P. Gray, comp.sources.misc vol 16.
    Its own posting says **public domain**; a telecommunications program in
    the ProComm style. It is an 8-part usenet shar (`1`..`8` plus `bug0`-`bug3`
    and two patches) written for Unix, so it needs reassembly and a port. Not
    a quick win, but the licence is clean and `CMDS/COMMS` is where it belongs.
  - **`fft.ar`** — an FFT library: `complex.h`, `fft.l`, `realfft.l`, a readme
    and worked examples. A library rather than a program, so it belongs here only if
    the collection decides libraries are in scope.
  - **`dates.ar`** — twelve month files and `shortdates`. Data for something;
    no program identified.
  - **`curses.vax.ar`** — 46 members, not screened in detail because its
    sibling `curses.ar` is excluded. Check it before ever taking it.

## Method note

`mine_arr.py` judges extraction by **what landed on disk**, never by what
os9exec printed — its stdout carries NULs and escape sequences, and matching
on it once reported FAILED for three pool archives that had extracted
perfectly. Same rule as the pool extractor.
