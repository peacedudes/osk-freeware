# osk-freeware

Three decades of community software for **OS-9/68000 (OSK)**, gathered in one
place and made to run again: 614 programs with their source, their
documentation, and a record of where each one came from.

OS-9 itself is Microware's, and still a current product. This is the software
the community wrote for it.

Not for the 6809 line — these are 68k binaries.

## What it is

A single OS-9 RBF disk image, ~125 MB, built from `disk/`. It is **not a boot
disk**: os9exec is the kernel, and this is the disk it mounts as `/dd` — the
root and home. There is no established name for that role.

    disk/       the tree the image is built from
      CMDS/       364 commands, plus GAMES/ REBUILT/ BROKEN/ NETPBM/ GCC*/
      SRC/        C source for most of it
      DOC/        per-package documentation, plus the index files below
      GAMES/      game data
      SYS/ LIB/ DEFS/
    tools/      how the image gets built (see tools/README.md)

## Running it

    ln osk-freeware.dd h0        # one inode, two names; os9exec needs both
    OS9DISK=$PWD/osk-freeware.dd OS9H0=$PWD/h0 \
        os9exec /dd/CMDS/bash /dd/SYS/login

The trailing `/dd/SYS/login` is not optional. bash on this disk cannot read a
startup file — its `.` builtin fails on every path — so started bare it has no
`PATH`, no `HOME` and no `TERM`, finds no command, and complains about a
missing `.bashrc`. `SYS/login` is a script that exports the three and hands
over to an interactive shell. Without `TERM`, `vi` clears the screen, draws
nothing and ignores `:q` — which reads as a lock-up and is a missing terminal
type.

## What is actually in it

**[docs/CATALOG.md](docs/CATALOG.md) — every program, grouped by what it is for.**
That is the one to open first. `DOC/INDEX` on the disk is alphabetical and 700
lines long, which is no help until you already know the name you want.

<!-- CATEGORIES:START -->

| Category | | |
|---|--:|---|
| **Shells** | 16 | The stock OS-9 shell is thin. These give you history, job control and a command line worth living in. |
| **Editors** | 18 | vi and emacs in several flavours, line and stream editors, and editors for binary and hex. |
| **Text tools** | 71 | Search, sort, compare, reformat, split and spell-check. |
| **Files & directories** | 31 | Listing, copying, finding, renaming, and knowing what you have. |
| **Developer tools** | 28 | Version control, tags, cross-reference, formatters, a debugger and benchmarks. |
| **Compilers & build** | 33 | C compilers and their passes, assemblers, linkers, make and parser generators. |
| **Languages** | 3 | Interpreters and language systems beyond C. |
| **Archives & compression** | 20 | Pack, unpack and shrink -- lha, zip, tar, arc, zoo, and OS-9 module libraries. |
| **Encoding & conversion** | 16 | Between text encodings, line endings, number bases, ciphers and hashes. |
| **Communications** | 20 | Kermit in several builds, terminal sessions, and networking. |
| **Graphics & images** | 189 | The netpbm toolkit, JPEG, a ray tracer, and things that draw. |
| **Games** | 58 | Adventures, board and card games, arcade ports, dungeon crawls and puzzles. |
| **Screen toys** | 6 | Things to watch rather than play. Start one and leave it going. |
| **Amusements** | 18 | Generators, simulators and diversions that are not quite games. |
| **System & modules** | 32 | OS-9 module and process tools, devices, system state and scheduling. |
| **Disk & DOS** | 20 | Reading and writing MS-DOS media with the mtools set. |
| **Time & calendar** | 12 | Calendars, clocks and astronomy. |
| **Maths & calculators** | 11 | Calculators, plotting, orbits and number theory. |
| **Printing** | 8 | Spoolers, page formatting and PostScript. |
| **Documentation** | 4 | Pagers, readers and the help system. |

<!-- CATEGORIES:END -->

`docs/index.html` is the same catalogue as a searchable page: filter by
category, hide anything needing `cio`, and click a program for what it needs,
where it came from and on what terms. GitHub shows HTML files as source rather
than rendering them, so **download the repository and open that file** — it is
self-contained, no server and nothing to install.

## Start here

| | |
|---|---|
| [`docs/CATALOG.md`](docs/CATALOG.md) | what is here, by category |
| `disk/readme` | the front door |
| `disk/DOC/README-RUNNING` | three ways to run it — read this first |
| `disk/DOC/INDEX` | what every program is |
| `disk/DOC/ORIGINS` | which archive each one came from |
| `disk/DOC/DEPENDS` | what each program needs besides its own binary |
| `disk/SOURCES.txt` | licence terms, per program |
| `disk/DOC/README-CIO` | the starred programs, and what they need |

## Licensing

Everything under `disk/` was written by other people and gathered from public
archives — it is collected here as a convenience, and **nothing here
relicenses any of it**. Each program keeps its own author's terms, which
`SOURCES.txt` records per program. Read `LICENSE` before redistributing
anything out of this collection; read it rather than assuming, because the
terms are a patchwork:

- GPL and BSD packages, with their `COPYING` files in `disk/DOC/<pkg>/`
- public domain, and author-distributable usenet postings
- SB-Prolog under SUNY Stony Brook's own licence, which **requires** that
  licence travel with the program (`disk/DOC/sbprolog/COPYING`)
- four EFFO programs whose authors asked for no military use — their
  `info_*` files ship alongside them, which is what those terms ask
- a few with no stated terms at all, recorded as such rather than guessed at

If you hold rights in something here and would rather it were not, say so and
it will be removed.

Separately, and covering none of the above: the tooling written for this
repository — `tools/`, `.github/`, this README, `notes/` — is MIT, in
`tools/LICENSE`.

No Microware product is in this repo: no utilities, no headers, no libraries.
The programs were built with Microware's `cc`, which is what a compiler is
for. Programs that want Microware's `cio` at runtime are marked with a star
in `disk/DOC/INDEX`; `disk/DOC/README-CIO` explains how to point at your own.

## Building the image

Needs the [os9exec](https://github.com/peacedudes/os9exec) binary, and nothing
else — no Microware utility and no OS-9 system disk.

    OS9EXEC_DIR=/path/to/os9exec tools/mkimage.sh disk osk-freeware.dd

os9exec's own `mount -k` writes the blank image, `tools/mktar.py` packs the
tree host-side with the finished disk's attributes already in the mode bits,
and the collection's **own** `tar` extracts it — so the disk populates itself.
Takes about four seconds. See `tools/README.md`.

The image is a release artefact and is not committed.

## Rebuilding programs from source

`tools/rebuild/` holds the driver, the shims, and **203 known-good build
recipes** — one line per program, so nobody has to re-derive them. See
`tools/rebuild/README.md`.

Most of the 621 modules under `CMDS/` have no source anywhere and can only be
preserved, not rebuilt. That is why the binaries are committed.
