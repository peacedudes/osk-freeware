# osk-freeware — open items

Moved out of os9exec's ROADMAP.md when the collection got its own repo.

## Freeware disk: two small open items


- **7 modules still report a module name that is not their filename**:
  hc, queens, tabs, GAMES/wish, REBUILT/compress, REBUILT/kermit,
  REBUILT/screen. Each needs its source tree identified before it can be
  rebuilt with `-n=`; `DOC/ORIGINS` names a tree for all but `tabs`, but the
  named tree has no `<prog>.c` in it. `GAMES/wish` is the interesting one:
  ORIGINS lists two different `wish` programs, yet the two binaries differ by
  exactly the 2 bytes of the `B_` name prefix — so either ORIGINS is wrong or
  one copy is a stale duplicate of the other.

## Freeware disk: elvis has docs and source but no binary

`DOC/elvis/` carries the full man-page set and `CMDS/archives/elvis1.7.lzh`
has the source, but the elvis binary is not on the disk. It is a vi clone
worth having (and its ctags is the free replacement for the quarantined
Microware one). Building it would remove a documented-but-absent program,
which is the same class of defect as SRC/ls.

## Freeware disk: larn plays; only its help file is absent — FIXED

The old entry here claimed larn's data was lost and the binary should move to
`CMDS/BROKEN`. That was wrong, and would have retired a working game.

larn names `.larnmaze`, `.larn.help`, `.lfortune`, `.playerids` and
`.holidays` under `/h0/GAMES/larn/PLAYGROUND` — all five strings really are in
the binary — but naming is not needing. Run with the disk as both `/dd` and
`/h0`, larn lays out a level, keeps score and takes commands with none of them
present.

Two different things were being conflated:

- **`.lscore12.0`/`.llog12.0` are written by larn, not shipped with it.** They
  were never lost. The whole defect was that `GAMES/LARN` had no `PLAYGROUND`
  under it, so larn had nowhere to write and failed with `error 216`. The disk
  now carries `GAMES/LARN/PLAYGROUND/.lscore12.0`, the scoreboard larn created
  for itself; larn reads it back on the next run without complaint.

- **`.larn.help` is genuinely absent** and is the only remaining complaint. It
  costs the in-game `?` help text and nothing else.

No larn source anywhere: no `SRC` tree, nothing in `CMDS/archives/`, and
`DOC/ORIGINS` does not mention larn or `ularn` at all. larn 12.0 is freely
redistributable and widely archived, so `.larn.help` could be recovered from
an outside distribution — nothing in this repo has it.

`gnuchessc`/`gnuan` had a real missing-data problem and are FIXED — theirs was
recovered from the download pool into `GNUCHESS4.0/MISC/`.

## Build the image in CI

The build no longer needs anything proprietary — that half is done. It was
blocked because `mkimage.sh` drove `chx`, `makdir`, `copy` and `attr` out of a
Microware system disk, and none of those is on this collection. Three pieces
replaced all four:

- os9exec's internal `mount -k` writes the blank image; it needs no disk.
- `tools/mktar.py` writes `disk/` as ustar, host-side, with the finished
  disk's attributes already in the mode bits — so there is no `attr` pass.
- The collection's **own** `tar` extracts it. Unstarred, so no `cio`. `cp` and
  `mkdir` are on the disk but both are starred, so neither could have done it.

A full build takes about four seconds and is verified at 3288/3288 files and
351/351 directories.

**Still to do: the workflow itself.** This repo has no `.github`. It needs
only the os9exec binary, so a CI leg can build os9exec and then run
`tools/mkimage.sh`. Worth adding alongside it, since they cost nothing: CR-only
line endings on the text files, `DOC/DEPENDS` regenerating identically, every
module named somewhere in `DOC/INDEX`, and the star list still matching a live
measurement.

Two known wrinkles, neither blocking:

- **The image is not byte-reproducible, by 352 bytes** — the LSN0 volume date
  and 351 directory creation dates come from the clock. Content is exact and
  `mktar.py` output is byte-identical run to run.
- **`DOC/DEPENDS` has no generator in `tools/`**, though it is meant to be
  regenerated whenever the tree changes. Its larn line was last corrected by
  hand.
