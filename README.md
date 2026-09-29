# osk-freeware

Over a thousand programs written for **OS-9/68000** by the people who ran
it, gathered on one disk image. Every one has been run. Most come with their
source and their documentation.

Microware Systems Corporation, from the heart of Iowa, wrote OS-9 at the
turn of the 1980s for Motorola's 6809, and brought it to the 68000 in 1983.
Its claim to fame is a real-time, multitasking, Unix-like system on machines
far too small for Unix, built from compact modules that run as happily from
ROM as from disk. That made it at home in the Tandy Color Computer, Fujitsu's
FM computers and the Philips CD-i player, where it ran as CD-RTOS, and on
factory floors, in instruments and in traffic signals. It never stopped:
OS-9 is still developed, sold and supported by Microware LP, at
[microware.com](https://www.microware.com). Microware graciously gave
permission for this collection to include the standard 68000 runtime
modules its programs need.

This collection is the community's work, not Microware's, and Microware does
not endorse it.

## Try it in your browser

Everything here was written for OS-9 and is designed to run on it. Through
WebAssembly and os9exec, a community 68000 emulator, the whole disk also
runs in a web page, and most of it needs nothing more.

**[The catalogue](https://peacedudes.github.io/osk-freeware/)** has a card
for every program: what it is, what it needs, its terms, its own help, and a
screen of it running. Press "Try it in your browser" on any card and it is
running. The rest of your OS-9, if you have one, can come along: "Open disk
as /h1" attaches it, and the few programs that want your `runb` or shell
find them there.

    $ cursive Ad astra
       __
      /  )   /             _/_
     /--/ __/     __.  _   /  __  __.
    /  (_(_/_    (_/|_/_)_<__/ (_(_/|_

That is `cursive`, on the disk, captured as it ran.

**What is here.** bash, ksh and vi. Several C compilers, with yacc, bison,
flex and make. TeX, LaTeX and METAFONT. netpbm, JPEG and a ray tracer. elm,
rn and kermit. Perl, Lisp, Forth and a Fortran. Colossal Cave, rogue, hack,
larn, moria, GNU Chess and GNU Go. The phase of the moon. Rain on the
screen. Written between the mid-1980s and the mid-1990s, and given away.
[docs/CATALOG.md](docs/CATALOG.md) lists them by category.

## On your own OS-9 system

The collection is one RBF image, `osk-freeware.dd`, written whole onto a
disk of its own. Mount it as `/dd` and also name it `/h0`: the programs look
for their data under `/dd`, and some older ones carry `/h0` paths inside
them. On most OS-9 systems `/dd` already names the `/h0` drive. Your own
system goes on `/h1`. Then

    bash /dd/SYS/login

sets the paths and the terminal, and programs run by name. We have not done
this on hardware ourselves; `DOC/README-RUNNING` on the disk has what is
known.

## Keeping what you like

`keep`, `kept` and `unkeep` were written for this collection. They copy the
programs you choose, with every file each one reads, onto your own disk:

    keep cookie       copy cookie, and every file it reads, onto your disk on /h1
    kept              list what you have kept
    unkeep cookie     remove it again, leaving any file you have changed

In the catalogue, tick programs and it writes the `keep` line for you, or
makes a new disk of just those in the browser, to download.
`DOC/README-KEEP` has more.

## On your desktop

os9exec builds on macOS, Linux and Windows, and runs the image with no OS-9
of your own:

    OS9DISK=$PWD/osk-freeware.dd OS9H0=$PWD/osk-freeware.dd OS9H1=<your OS-9> \
        os9exec -r bash /dd/SYS/login

`OS9H1` is optional. Run the image, not a copy unpacked into a directory:
permissions and record locking work only on the image.

## Finding your way on the disk

`DOC/START-HERE` names some programs that run with nothing set up.
**`man`** is the librarian:

    man hp            its manual page, then its other documents
    man -k chess      every program about chess
    man -s westley    its source
    man -w elm        where each of its documents is

A program with no documents gets its one-line description and what it says
when asked for help.

Seven vi files, six kermits, twenty archivers: `DOC/README-VI`,
`DOC/README-EDITORS`, `DOC/README-ARCHIVERS`, `DOC/README-KERMIT`,
`DOC/README-GREP` and `DOC/README-SHELLS` each compare a family and say
which to take.

A star in `DOC/INDEX` means the program uses Microware's `cio`, which is on
the disk; `DOC/README-CIO` explains. `SYS/login` sets `TERM`, `TERMCAP` and
the paths, and most full-screen programs need nothing more; `gnuchess` wants
`SYS/termcap.entry` sourced first. bash's own `pwd` hangs on OS-9, so
`SYS/login` sets `HOME` and `/dd/.bashrc` replaces `cd` and `pwd` with
versions that work.

## By category

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
| **System & modules** | 141 | OS-9 module and process tools, devices, system state and scheduling. |
| **Disk & DOS** | 20 | Reading and writing MS-DOS media with the mtools set. |
| **Time & calendar** | 18 | Calendars, clocks and astronomy. |
| **Maths & calculators** | 20 | Calculators, plotting, orbits and number theory. |
| **Printing** | 11 | Spoolers, page formatting and PostScript. |
| **Documentation** | 8 | Pagers, readers and the help system. |
| **G-Windows** | 6 | Programs for G-Windows, OS-9's graphical display.  There is none here, so each card shows the program saying so. |
| **Needs hardware** | 16 | Programs for hardware out of our reach: a GEPARD or MM/1 display, a printer on its own port.  Untested here; what is said of them comes from their own text and code. |

<!-- CATEGORIES:END -->

## Terms

Everything under `disk/` belongs to its authors, under their own terms.
Nothing here relicenses any of it. `disk/SOURCES.txt` records the terms of
each program; `LICENSE` says how to read them. They include GPL and BSD
packages, with their `COPYING` files in `disk/DOC/`; public domain and
author-distributed usenet postings; SB-Prolog under SUNY Stony Brook's
licence, which travels with it; some whose authors asked for no military
use, or peaceful use only, and `SOURCES.txt` lists them; and a few with no
stated terms, recorded as such.

If you hold rights in something here and want it removed, say so and it
will be.

Six Microware runtime modules ship by permission: `cio`, `csl`, `csl020`,
`math` and `math881` on Microware's word, and `fpu` on the grant in
`DOC/fpu.doc`, which ships beside it. `SOURCES.txt` records both. Nothing
else of Microware's is here.

The tooling written for this repository (`tools/`, `.github/`, this README)
is MIT: `tools/LICENSE`.

## Building

The image needs only the [os9exec](https://github.com/peacedudes/os9exec)
binary:

    OS9EXEC_DIR=/path/to/os9exec tools/mkimage.sh disk osk-freeware.dd

It takes seconds. `tools/check_disk.py disk` is the gate every change passes.
Programs are rebuilt from source with `tools/rebuild/`; some have no source
anywhere, which is why the binaries are committed. `tools/README.md`
describes the tools.
