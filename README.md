# osk-freeware

Over a thousand community programs for **OS-9/68000**, on one disk image.
Every one has been run on it. Most come with their source and their
documentation.

## OS-9

OS-9 is Microware's. It never stopped: OS-9/68000 still runs industrial
systems around the world, and OS-9 is still sold and supported today.
Plenty of people will be surprised to hear it.

## This collection

This is what the community wrote for OS-9, gathered, repaired where it was
broken, and catalogued. It is not Microware's work, and Microware does not
endorse it. They know of it, and gave permission for the runtime modules
it needs to ship on the disk.

## Running it

**On your own OS-9 system.** Write `osk-freeware.dd` whole onto a disk and
mount it as `/dd`, also named `/h0`. Put your own system on `/h1`. Then:

    bash /dd/SYS/login

We have not done this on hardware ourselves. `DOC/README-RUNNING` on the
disk has what is known.

**With os9exec**, a community emulator for macOS, Linux and Windows:

    OS9DISK=$PWD/osk-freeware.dd OS9H0=$PWD/osk-freeware.dd OS9H1=<your OS-9> \
        os9exec -r bash /dd/SYS/login

`OS9H1` is optional; a few programs want your `runb` or shell from it.

**In a web browser.** The published catalogue runs the whole disk in the
page: any card's "Try it in your browser".

## Finding things

**`docs/index.html`** has a card for every program: what it is, what it
needs, where it came from, its terms, its own help, and a screen of it
running, captured from the disk. A card can open the program in the browser,
or its documents.

**`man`** does the same on the disk. It is the collection's librarian:

    man hp            its manual page, then its other documents
    man -k chess      every program about chess
    man -s westley    its source
    man -w elm        where each of its documents is

A program with no documents gets its one-line description and what it says
when asked for help.

**[docs/CATALOG.md](docs/CATALOG.md)** is the list by category, readable
here on GitHub:

<!-- CATEGORIES:START -->

| Category | | |
|---|--:|---|
| **Shells** | 25 | Unix shells to sit beside OS-9's own -- bash and ksh bring history, job control, and scripts that come across unchanged. |
| **Editors** | 22 | vi and emacs in several flavours, line and stream editors, and editors for binary and hex. |
| **Text tools** | 140 | Search, sort, compare, reformat, split and spell-check. |
| **Files & directories** | 38 | Listing, copying, finding, renaming, and knowing what you have. |
| **Developer tools** | 39 | Version control, tags, cross-reference, formatters, a debugger and benchmarks. |
| **Compilers & build** | 49 | C compilers and their passes, assemblers, linkers, make and parser generators. |
| **Languages** | 16 | Interpreters and language systems beyond C. |
| **Archives & compression** | 34 | Pack, unpack and shrink -- lha, zip, tar, arc, zoo, and OS-9 module libraries. |
| **Encoding & conversion** | 34 | Between text encodings, line endings, Macintosh formats, ciphers and hashes. |
| **Communications** | 123 | Kermit in several builds, terminal sessions, and networking. |
| **Graphics & images** | 191 | The netpbm toolkit, JPEG, a ray tracer, and things that draw. |
| **Games** | 117 | Adventures, board and card games, arcade ports, dungeon crawls and puzzles. |
| **Screen toys** | 10 | Animations and screen effects -- they draw on the terminal rather than print to it. Some run until you stop them. |
| **Amusements** | 39 | Generators, simulators and diversions that are not quite games. |
| **System & modules** | 142 | OS-9 module and process tools, devices, system state and scheduling. |
| **Disk & DOS** | 20 | Reading and writing MS-DOS media with the mtools set. |
| **Time & calendar** | 18 | Calendars, clocks and astronomy. |
| **Maths & calculators** | 20 | Calculators, plotting, orbits and number theory. |
| **Printing** | 11 | Spoolers, page formatting and PostScript. |
| **Documentation** | 8 | Pagers, readers and the help system. |
| **G-Windows** | 6 | Programs for G-Windows, OS-9's graphical display.  There is none here, so each card shows the program saying so. |
| **Needs hardware** | 16 | Programs for hardware out of our reach: a GEPARD or MM/1 display, a printer on its own port.  Untested here; what is said of them comes from their own text and code. |

<!-- CATEGORIES:END -->

## Keeping what you like

`keep`, `kept` and `unkeep` were written for this collection.

    keep cookie       copy cookie, and every file it reads, onto your disk on /h1
    kept              list what you have kept
    unkeep cookie     remove it again, leaving any file you have changed

On `docs/index.html`, tick programs and it writes the `keep` line for you,
or makes a new empty disk of them in the browser to download.
`DOC/README-KEEP` has the details.

## Choosing one of several

Seven vi files, six kermits, twenty archivers. Each of these compares a
family and says which to take:

| | |
|---|---|
| `DOC/README-VI` | which vi |
| `DOC/README-EDITORS` | the editors that are not vi |
| `DOC/README-ARCHIVERS` | archivers, by format |
| `DOC/README-KERMIT` | kermits, and the two flags that decide a transfer |
| `DOC/README-GREP` | ways to search a file |
| `DOC/README-SHELLS` | the shells, and why `SYS/login` names ksh |

## Worth knowing

- A star in `DOC/INDEX` means the program uses Microware's `cio`, which is on
  the disk. `DOC/README-CIO` explains.
- `SYS/login` sets `TERM`, `TERMCAP` and the paths. Most full-screen programs
  need nothing more. `gnuchess` wants the terminal description itself in
  `TERMCAP`: source `SYS/termcap.entry` first.
- bash's own `pwd` hangs on OS-9. `SYS/login` sets `HOME`, and `/dd/.bashrc`
  replaces `cd` and `pwd` with versions that work.

## Terms

Everything under `disk/` belongs to its authors, under their own terms.
Nothing here relicenses any of it. `disk/SOURCES.txt` records the terms of
each program; `LICENSE` says how to read them. They include:

- GPL and BSD packages, with their `COPYING` files in `disk/DOC/`
- public domain and author-distributed usenet postings
- SB-Prolog under SUNY Stony Brook's licence, which travels with it
- some whose authors asked for no military use, or peaceful use only;
  `SOURCES.txt` lists them
- a few with no stated terms, recorded as such

If you hold rights in something here and want it removed, say so and it
will be.

Six Microware runtime modules ship by permission: `cio`, `csl`, `csl020`,
`math` and `math881` on Microware's word, and `fpu` on the grant in
`DOC/fpu.doc`, which ships beside it. `SOURCES.txt` records both. Nothing
else of Microware's is here.

The tooling written for this repository (`tools/`, `.github/`, `notes/`,
this README) is MIT: `tools/LICENSE`.

## Building

The image needs only the [os9exec](https://github.com/peacedudes/os9exec)
binary:

    OS9EXEC_DIR=/path/to/os9exec tools/mkimage.sh disk osk-freeware.dd

It takes seconds. `tools/check_disk.py disk` is the gate every change passes.
Programs are rebuilt from source with `tools/rebuild/` (see its README);
some have no source anywhere, which is why the binaries are committed.

Working on the collection starts at `notes/PLAN.md`.
