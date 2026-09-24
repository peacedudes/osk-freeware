# osk-freeware

Three decades of community software for **OS-9/68000 (OSK)**, gathered in one
place and made to run again, with the documentation and the source that could
be found for them and a record of where each one came from. Seven tenths of it
has source here; most of the rest never had any that survived.

OS-9 is Microware's, and still a current product. This is the software the
community wrote for it, and it is meant to be run on a real OS-9 system.

Not for the 6809 line — these are 68k binaries.

## What it is

The community's software for OS-9, made to run again on OS-9. It ships as
**`osk-freeware.dd`**, one RBF disk image built from `disk/`, with room
left for scores, saves and your own work. The build sizes it from the
tree -- a little under twice what the tree takes -- so the figure moves;
`ls -l osk-freeware.dd` answers it, and today that is 312 MiB.

It is a data disk for an OS-9 system you already have, or for os9exec:
your system boots as it always did, and this mounts beside it.

    disk/       the tree the image is built from
      CMDS/       the commands, plus GAMES/ REBUILT/ NETPBM/ GCC*/ and the rest
      SRC/        C source for seven tenths of it
      DOC/        per-package documentation, plus the index files below
      GAMES/      game data
      SYS/ LIB/ DEFS/
    tools/      how the image gets built (see tools/README.md)

## On a real OS-9 system

Give the collection a disk of its own, reached by two device names: `/dd`,
where most programs look for their data (`advent` wants
`/dd/GAMES/adv/glorkz`, `fortune` `/dd/GAMES/FORTUNE/fortunes.dat`, `nroff`
`/dd/LIB/tmac.*`), and `/h0`, which a smaller number carry inside instead.
On most OS-9 systems `/dd` already names the `/h0` drive, so that is the
usual arrangement. Your own system disk takes another name -- `SYS/login`
puts `/h1/CMDS` on the path, so `/h1` is the one it expects -- and your own
`runb`, shell, `r68` and `l68` are found there by the programs that want
them.

To get it onto that disk, write `osk-freeware.dd`, the raw RBF image, whole
onto a disk your system mounts.

Then `bash /dd/SYS/login` from your own shell gives you a session with the
paths set, or use the programs directly: `SYS/login` says what it sets.

We have not done this on hardware ourselves. `DOC/README-RUNNING` on the
disk says what is known and what has been measured; if you have, what
worked is worth writing down there.

Nothing has to be fetched. `cio`, `csl`, `csl020`, `math` and `math881` --
the Microware runtime modules the starred programs need -- **ship on the
disk, with Microware's permission**. `SOURCES.txt` records the exchange.

## Trying it first, with os9exec

os9exec is a community emulator that builds on macOS, Linux, Windows and
most anything with a C compiler: point it at the image and it runs, no OS-9
of your own needed. Its devices are named by environment variables -- the
image as both `OS9DISK` and `OS9H0`, your own OS-9 system or SDK as
`OS9H1` if you have one:

    OS9DISK=$PWD/osk-freeware.dd OS9H0=$PWD/osk-freeware.dd OS9H1=<your OS-9> \
        os9exec -r bash /dd/SYS/login

With `OS9H1` set, the programs that want `runb` or Microware's shell find
them. Keep the collection as an RBF image rather than unpacking it into a
host directory: on the image, file permissions and record locking work as
OS-9 expects, and a host directory gives neither. os9exec's own `mount -k`
makes a blank image when you want one of your own. Everything in `docs/`
was captured this way.

### Taking a few programs onto your own system disk

The disk carries **`keep`**, **`kept`** and **`unkeep`**, written for this
collection: `keep cookie` copies cookie and the files `DOC/DEPENDS` says it
reads from `/dd` onto your disk on `/h1`, laid out the way cookie expects
them, and records every file; `kept` lists them; `unkeep cookie` removes them,
leaving any you have changed since. See `DOC/README-KEEP`. `docs/index.html`
builds the command for you: tick programs and it writes out `keep a b c`.

### Two things worth knowing either way

**`TERMCAP` matters.** A good many programs name `/h0/sys/termcap` outright,
and every one measured reads the `TERMCAP` variable first, so they work with
no `/h0` in sight. `SYS/login` sets it to the PATH of the termcap file, which
is what those programs want. Three want the opposite: `gnuchess`,
`gnuchessn` and `hexedit` were built against a termcap library that reads
`TERMCAP` as the terminal DESCRIPTION rather than as a filename, get the
pathname where they expected a description, and stop with `'vt100': Unknown
terminal type`. `SYS/termcap.entry` exists for them — source it in the shell
where you want one of the three, and the rest of your session is unaffected.
`DOC/README-RUNNING` has it.

**bash's own `pwd` hangs the shell** here: its `getwd()` walks `..` looking for
a single root, and OS-9 has one per device. Setting `HOME` is what makes bash
read `/dd/.bashrc`, where working `cd` and `pwd` are defined.

## What is actually in it

**[docs/CATALOG.md](docs/CATALOG.md) — every program, grouped by what it is for.**
That is the one to open first. `DOC/INDEX` on the disk is alphabetical, which
is no help until you already know the name you want.

<!-- CATEGORIES:START -->

| Category | | |
|---|--:|---|
| **Shells** | 25 | Unix shells to sit beside OS-9's own -- bash and ksh bring history, job control, and scripts that come across unchanged. |
| **Editors** | 22 | vi and emacs in several flavours, line and stream editors, and editors for binary and hex. |
| **Text tools** | 139 | Search, sort, compare, reformat, split and spell-check. |
| **Files & directories** | 37 | Listing, copying, finding, renaming, and knowing what you have. |
| **Developer tools** | 38 | Version control, tags, cross-reference, formatters, a debugger and benchmarks. |
| **Compilers & build** | 41 | C compilers and their passes, assemblers, linkers, make and parser generators. |
| **Languages** | 16 | Interpreters and language systems beyond C. |
| **Archives & compression** | 34 | Pack, unpack and shrink -- lha, zip, tar, arc, zoo, and OS-9 module libraries. |
| **Encoding & conversion** | 34 | Between text encodings, line endings, Macintosh formats, ciphers and hashes. |
| **Communications** | 115 | Kermit in several builds, terminal sessions, and networking. |
| **Graphics & images** | 195 | The netpbm toolkit, JPEG, a ray tracer, and things that draw. |
| **Games** | 116 | Adventures, board and card games, arcade ports, dungeon crawls and puzzles. |
| **Screen toys** | 10 | Animations and screen effects -- they draw on the terminal rather than print to it. Some run until you stop them. |
| **Amusements** | 39 | Generators, simulators and diversions that are not quite games. |
| **System & modules** | 121 | OS-9 module and process tools, devices, system state and scheduling. |
| **Disk & DOS** | 20 | Reading and writing MS-DOS media with the mtools set. |
| **Time & calendar** | 18 | Calendars, clocks and astronomy. |
| **Maths & calculators** | 19 | Calculators, plotting, orbits and number theory. |
| **Printing** | 11 | Spoolers, page formatting and PostScript. |
| **Documentation** | 7 | Pagers, readers and the help system. |
| **G-Windows** | 6 | Programs for G-Windows, OS-9's graphical display.  There is no G-Windows here, so what their cards show is each one declining in its own words -- `Unable to access "/win" device', `dclock only runs under G-Windows', a status of 208 or 221.  None of them can be exercised without the display; they are listed for a real OS-9 workstation that has it. |
| **Needs hardware** | 12 | Programs that drive hardware this collection has no way to reach -- a graphics display of the kind a GEPARD or an MM/1 carries, or a printer on its own SCF device.  WE CANNOT TEST ANY OF THESE, at all: what is written about them comes from their own text and their code, not from watching them work.  They are here for a real machine that has the hardware. |

<!-- CATEGORIES:END -->

`docs/index.html` is the same catalogue as a searchable page: filter by
category, hide anything needing `cio`, and click a program for what it needs,
where it came from and on what terms. GitHub shows HTML files as source rather
than rendering them, so **download the repository and open that file** — it is
self-contained, no server and nothing to install.

**Every program has a picture beside it** — all 936 of them, as of
2026-08-30 — and **864 of those pictures are of the program itself**. The
rest share a card with programs that behave alike: eleven DVI drivers on one
screen, a shelf of device descriptors on another, the netpbm readers with no
file to read on a third. `tools/gen_screens.py` prints both numbers on every
run, because the first one on its own cannot fail — grouping always satisfies
it. Open one in the catalogue and, beside its own help, you get its
**sample output**: captured from that program running on the disk image,
keystrokes fed to os9exec's console and the terminal stream rendered into the
grid a vt100 would have shown. Nothing is mocked up, and where a program
failed the failure is what you see — which is how two dozen programs the
four-stage sweep had scored as working turned out not to be, and how several
entries in `DOC/INDEX` were found to describe a different program from the one
that runs. (The same screens are in `docs/screens/` as plain text.)

## Start here

| | |
|---|---|
| [`docs/CATALOG.md`](docs/CATALOG.md) | what is here, by category |
| `docs/screens/` | the same sample output as plain text |
| `disk/readme` | the front door |
| `disk/DOC/README-RUNNING` | three ways to run it — read this first |
| `disk/DOC/INDEX` | what every program is |
| `disk/DOC/ORIGINS` | which archive each one came from |
| `disk/DOC/DEPENDS` | what each program needs besides its own binary |
| `disk/SOURCES.txt` | licence terms, per program |
| `disk/DOC/README-CIO` | the starred programs, and what they need |

**Several of a thing? There is a chooser for it.** The collection carries
five vi-ish editors, six kermits, twenty archivers — and if you are copying
part of it onto your own media you want *one*, without installing several to
find out how they differ. Each of these is a table of hard facts, a "take
this if" per candidate, and a one-line answer for somebody who wants exactly
one file:

| | |
|---|---|
| `disk/DOC/README-VI` | seven files, three editors — which vi |
| `disk/DOC/README-EDITORS` | the ten editors that are *not* vi |
| `disk/DOC/README-ARCHIVERS` | twenty archivers in seven formats |
| `disk/DOC/README-KERMIT` | six kermits, and the two flags that decide whether a transfer works |
| `disk/DOC/README-GREP` | six ways to search a file |
| `disk/DOC/README-SHELLS` | the five shells, and why `SYS/login` names ksh |

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

Microware's own utilities, headers and libraries are not here — with one
deliberate exception. **Five runtime modules ship by permission**: `cio`,
`csl`, `csl020`, `math` and `math881`. Allan at Microware was asked for exactly
those and replied *"I do not see a problem with those modules."*
`disk/SOURCES.txt` records the exchange.

Most of these programs were compiled with Microware's `cc`, and a good share
of them use `cio` at run time. Those are starred in
`disk/DOC/INDEX`; `disk/DOC/README-CIO` explains what the star means and how to
use your own copy instead if you would rather.

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

`tools/rebuild/` holds the driver, the shims, and the known-good build
recipes — one line per program, so nobody has to re-derive them.
`tools/build.sh` builds everything there is a recipe for and `--missing` names
the trees that still have none. See `tools/rebuild/README.md`.

A third of the modules under `CMDS/` have no source anywhere and can only be
preserved, not rebuilt. That is why the binaries are committed.
`tools/src_census.py disk` counts it — 701 of 999, 70%, as measured
2026-08-29, and the figure moves every time a recipe lands.

## Working on this collection

**`notes/PLAN.md` is the one to read** — self-contained on purpose: what the
collection is, how to build and test it in two minutes, where it stands
measured, the work remaining in order with acceptance criteria, the rules that
matter, and the things already tried that did not work. It is the right first
read whether you are a person coming back after a month or an assistant
opening the repository for the first time, and you should not need the rest of
`notes/` unless it sends you there.

`notes/HISTORY-2026-08.md` is why things are the way they are — background,
not instructions. `notes/FOR-RDOGGETT.md` is what needs a decision, which is
currently nothing.
`notes/SESSION-<date>.md` files are history — read one when the handoff sends
you there, not before.
