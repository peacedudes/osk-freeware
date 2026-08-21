# osk-freeware

Three decades of community software for **OS-9/68000 (OSK)**, gathered in one
place and made to run again: 612 programs with their source, their
documentation, and a record of where each one came from.

OS-9 is Microware's, and still a current product. This is the software the
community wrote for it, and it is meant to be run on a real OS-9 system.

Not for the 6809 line — these are 68k binaries.

## What it is

A single OS-9 RBF disk image, ~125 MB, built from `disk/`. It is **not a boot
disk**: os9exec is the kernel, and this is the disk it mounts as `/dd` — the
root and home. There is no established name for that role.

    disk/       the tree the image is built from
      CMDS/       363 commands, plus GAMES/ REBUILT/ BROKEN/ NETPBM/ GCC*/
      SRC/        C source for most of it
      DOC/        per-package documentation, plus the index files below
      GAMES/      game data
      SYS/ LIB/ DEFS/
    tools/      how the image gets built (see tools/README.md)

## Running it

**If you have OS-9, keep your own system as `/dd` and mount this as `/h0`:**

    OS9DISK=<your own disk>  OS9H0=<this image, named h0>  os9exec shell
    setenv PATH /dd/CMDS:/h0/CMDS:/h0/CMDS/GAMES

That is the arrangement to prefer. Your `cio`, `csl` and `math` are on `/dd`
where the programs expect them, so the 92 starred programs run alongside the
rest — you get all 612, not the 520 that need nothing. The image must be a
file *named* `h0`; os9exec resolves an image by filename.

One thing to know either way: **20 programs read their data from `/dd`** —
`advent` wants `/dd/GAMES/adv/glorkz`, `fortune` wants
`/dd/GAMES/FORTUNE/fortunes.dat`, `nroff` wants `/dd/LIB/tmac.*`. With your own
disk as `/dd` those paths are yours, not ours, so those programs will not find
their files. `DOC/README-RUNNING` covers the ways round it, and `DOC/DEPENDS`
lists every path each program opens.

### Without an OS-9 of your own

The collection runs by itself:

    OS9DISK=$PWD/osk-freeware.dd os9exec -r bash /dd/SYS/login

What you give up is `cio`: the 92 starred programs in `DOC/INDEX` want it and
stop with "Can't install trap handler". The other 520 do not need it, and
`DOC/README-CIO` explains how to supply your own if you have one.

`SYS/login` works out where the disk is mounted from the path you hand it,
then sets `PATH`, `HOME`, `TERM` and `TERMCAP`. That last one matters: 69
programs name `/h0/sys/termcap` outright, and every one of them reads
`TERMCAP` first — measured, no exceptions — so they work with no `/h0` in
sight. Setting `HOME` is also what makes bash read `/dd/.bashrc`, where `cd`
and `pwd` are defined; **bash's own `pwd` hangs the shell** here, because its
`getwd()` walks `..` looking for a single root and OS-9 has one per device.

Only 37 programs, mostly compiler passes, still want data under a real `/h0`.
If you want those too, give os9exec the image under a second name
(`ln -s osk-freeware.dd h0`, then `OS9H0=$PWD/h0`) — one image behind two
device names, each with its own sector cache, so read through both freely but
do not write through both at once.

## What is actually in it

**[docs/CATALOG.md](docs/CATALOG.md) — every program, grouped by what it is for.**
That is the one to open first. `DOC/INDEX` on the disk is alphabetical and 700
lines long, which is no help until you already know the name you want.

<!-- CATEGORIES:START -->

| Category | | |
|---|--:|---|
| **Shells** | 21 | Unix shells to sit beside OS-9's own -- bash and ksh bring history, job control, and scripts that come across unchanged. |
| **Editors** | 24 | vi and emacs in several flavours, line and stream editors, and editors for binary and hex. |
| **Text tools** | 82 | Search, sort, compare, reformat, split and spell-check. |
| **Files & directories** | 36 | Listing, copying, finding, renaming, and knowing what you have. |
| **Developer tools** | 47 | Version control, tags, cross-reference, formatters, a debugger and benchmarks. |
| **Compilers & build** | 34 | C compilers and their passes, assemblers, linkers, make and parser generators. |
| **Languages** | 6 | Interpreters and language systems beyond C. |
| **Archives & compression** | 35 | Pack, unpack and shrink -- lha, zip, tar, arc, zoo, and OS-9 module libraries. |
| **Encoding & conversion** | 26 | Between text encodings, line endings, number bases, ciphers and hashes. |
| **Communications** | 51 | Kermit in several builds, terminal sessions, and networking. |
| **Graphics & images** | 204 | The netpbm toolkit, JPEG, a ray tracer, and things that draw. |
| **Games** | 66 | Adventures, board and card games, arcade ports, dungeon crawls and puzzles. |
| **Screen toys** | 6 | Things to watch rather than play. Start one and leave it going. |
| **Amusements** | 20 | Generators, simulators and diversions that are not quite games. |
| **System & modules** | 130 | OS-9 module and process tools, devices, system state and scheduling. |
| **Disk & DOS** | 20 | Reading and writing MS-DOS media with the mtools set. |
| **Time & calendar** | 10 | Calendars, clocks and astronomy. |
| **Maths & calculators** | 13 | Calculators, plotting, orbits and number theory. |
| **Printing** | 14 | Spoolers, page formatting and PostScript. |
| **Documentation** | 6 | Pagers, readers and the help system. |

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

Microware's own utilities, headers and libraries are not here; they come with
OS-9 and you will already have them. Most of these programs were compiled with
Microware's `cc`, and 92 of them use its `cio` at run time — those are starred
in `disk/DOC/INDEX`, and `disk/DOC/README-CIO` explains how to point them at
your copy.

## Building the image

Needs the [os9exec](https://github.com/peacedudes/os9exec) binary. Nothing
else has to be installed, which is what lets CI rebuild the image.

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
