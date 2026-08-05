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

## Freeware disk: elvis has docs and source but no binary — BUILDABLE

`DOC/elvis/` carries the full man-page set and `CMDS/archives/elvis1.7.lzh`
has the source, but the elvis binary is not on the disk. Building it would
remove a documented-but-absent program, the same class of defect as SRC/ls.

**It is not a lost cause — the OS-9 port already exists inside that archive.**
`README.OSK` says it plainly:

> version 1.7 of elvis by Steve Kirkendall, ported to os9 by Peter Reinig.
> Repacked and brushed up by Martin Gregorie and Peter Smulders.
> This port is for the old Microware C compiler (V2.3).

What is in the archive:

- `osk.c` / `osk.h` — the OS-9/68k platform layer, from upstream elvis 1.7
- `makefile` (1998), with `make`, `make install` and `make -i clob.os9`
- `alias.c` beside `alias.c.orig`, so the OS-9 patch is visible
- the `.os9` link scripts (`linkelv`, `linkvi`, `linkview`, `linkinput`) are
  all **zero bytes** in the archive — that is the one gap, and the makefile
  may not need them

It builds four programs, not one: elvis, vi, view and input. Its `ctags` is
also a free replacement for Microware's. Worth a run through
`tools/rebuild/`; the recipe would be the first that drives a whole makefile
rather than a file list.

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

- **`.larn.help` was genuinely absent** — that was the only remaining
  complaint, and it cost the in-game `?` help. Recovered, along with
  `.lfortune` and `.larnmaze`, from the larn 12.2p4 sources at
  `github.com/HunterZ/larn` (`larn.hlp`, `larn.ftn`, `larn.maz`), converted to
  CR to match the disk and ularn's own data files. All three now read without
  complaint and `?` shows the help.

**The version is not an exact match and should be watched.** The binary
reports 12.0; no 12.0 source has survived anywhere we can find, and the
earliest in that repository is 12.2p4. Help and fortune text are inert, but
`.larnmaze` defines level layouts — it was only exercised on the first level.
If a level ever renders wrong deep in the dungeon, that file is the first
suspect, and deleting it costs nothing: larn lays out its own levels without
it. `SOURCES.txt` records where all three came from.

No larn source on the disk: no `SRC` tree, nothing in `CMDS/archives/`, and
`DOC/ORIGINS` mentions neither larn nor `ularn`.

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

Known wrinkles, none blocking:

- **The workflow pins os9exec to a moving branch.** `arm64-uae-integration`,
  because `master` has no `mount -k` at all. A force-push or a regression
  there breaks this build with no warning. Pin to a commit SHA once the
  branch settles.
- **`DOC/DEPENDS` has no generator in `tools/`**, though it is meant to be
  regenerated whenever the tree changes. Its larn line was corrected by hand,
  twice. It is a scan of every binary for absolute paths — worth writing,
  and the only way the file can be trusted after a change.
- **The image is not byte-reproducible, by 352 bytes** — the LSN0 volume date
  and 351 directory creation dates come from the clock. Content is exact and
  `mktar.py` output is byte-identical run to run. Fixing it needs either a
  fixed clock in os9exec or a host-side pass over the finished image.

## Licence — DONE, but check the name on it

The root `LICENSE` is **not** a licence grant, deliberately. It is a statement
of terms: the collection was gathered from public archives, every program
keeps its own author's copyright, nothing here relicenses any of it, and
`disk/SOURCES.txt` is where to look before redistributing. It ends with an
offer to remove anything a rightsholder objects to.

An earlier draft put MIT at the root with a scope note. That was wrong: GitHub
labels a repository by its root licence file, so the whole collection would
have been advertised as MIT — a claim nobody here can make. The MIT text now
lives in `tools/LICENSE`, covering only what was written for this repository.
Expect GitHub to show no licence badge as a result, which is the honest
outcome.

MIT was chosen for the tooling over a public-domain dedication mainly for its
warranty disclaimer: `mkimage.sh` writes 125 MB disk images, and "AS IS" is
worth having when someone points it at the wrong path. Copyright is asserted
as "2026 Robert Doggett" — change that if it should read otherwise.

## Dropping the emulator from the build entirely

Not needed, and worth knowing the shape of anyway. Shipping a pre-made blank
image in the repo does NOT do it: populating the image is what needs os9exec,
because only the emulator can run the collection's own `tar`. A committed
blank would only relax WHICH os9exec you need — the populate step works with
a much older one than `mount -k -v=` does. A blank 125 M image is 127 KB
gzipped, 19 KB xz, so committing one is cheap if that coupling ever hurts;
the cost is a fixed size, where `mkimage.sh` currently sizes to content.

What would actually remove the dependency is writing the populate step
host-side — directory entries, file descriptors, allocation bitmap. That is a
few hundred lines of Python against a format this repo already understands.
It would also make the build instant and fully reproducible. Nobody needs it
today.
