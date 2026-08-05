# osk-freeware

Three decades of community software for **OS-9/68000 (OSK)**, gathered in one
place and made to run again: 629 programs with their source, their
documentation, and a record of where each one came from.

OS-9 itself is Microware's, and still a current product. This is the software
the community wrote for it.

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

## Start here

| | |
|---|---|
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

418 of the 629 modules have no source anywhere and can only be preserved, not
rebuilt. That is why the binaries are committed.
