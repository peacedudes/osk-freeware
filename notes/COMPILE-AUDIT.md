# Does the source compile?

rdoggett, 2026-08-22: *"verify we have it all (if it's source, it should
compile, right?)"*

Right. Until now that had only ever been established for the trees that have a
recipe. This is the count, and the method for closing the rest.

## Where it stands, 2026-08-22 (end of the build pass)

Run `tools/build.sh` for the live answer and `tools/build.sh --missing` for
the trees that still have no recipe. As measured on 2026-08-22:

    237 of 240 recipes build clean

and the three that do not, plus every tree with no recipe at all, are
accounted for below. Nothing in this list is "unknown" any more.

### The three recipes that fail

  - **`ls`** — a gcc2 build, and **it compiles now** (GCC flag, 2026-08-23).
    **It is still not adopted and has no recipe, deliberately**: `SRC/ls` is
    the PRE-FIX tree. Its `os9stubs.c` gives every regular file the same
    fabricated mode and never sets `st_mtime`, and the build bus-errors on
    `ls -l`. The shipped binary prints real per-file modes and real dates, so
    it came from a later source that is on no disk here. See
    `notes/SESSION-2026-08-23.md`.
  - **`pdraw`** — wants X11 headers. They are not here and are not coming.
  - **`pep`** — calls `standby()` and `init_via()`, which live in the mc
    EPROM programmer's own hardware library. Its own header says it runs only
    on that board, so this one is correct as it stands.

### Trees with no recipe, and why

**Wrong language or wrong compiler.**

  - `homelibr` — C++ (`.cc`). No C++ compiler here.
  - `aterm`, `serload` — 68k assembly only. `r68` would do it; nothing in
    `rebuild.sh` drives the assembler yet.
  - `graph` — three `.c` and eight `.a`; same.
  - ~~`ed`~~ — **wrong, and corrected 2026-08-23: `ed` is K&R throughout and
    BUILDS.** Running `ansi2knr` over it is destructive. Its only real blocker
    was `ed.h`'s `REALLOC` macro joining into ~1400 characters, past cpp's
    512; `CPP2` clears it. See its recipe.
  - `lout`, `gnuchess/GNUCHESS4.0` — ANSI C. `lout`'s `externs` uses typed
    bitfields; GNU Chess 4.0's header is several hundred ANSI prototypes.
  - `rtf` — Fortran.

**Something genuinely absent.**

  - `rcs` — `rcssyn.c`, `rcsrev.c`, `rcsutil.c` missing from the tree AND from
    `rcs4.lha` in the pool. RCS **version 4** (Purdue, 1987); GNU's 5.7 files
    are not drop-in.
  - `calc` wants `h_grafik.h`, `cgrafik` wants `graf.h` — neither is anywhere
    on the disk or in the pool.
  - `mgif` wants `screenbaseaddress` from `/h0/lib/gpprim.r`, a graphics
    primitive library that is not here.
  - `deansi` is lex output and wants a lex runtime (`yyreject`).
  - `rayshade` — **BUILDS 2026-08-23**, and renders. 78 sources over six
    nested libraries, the first package build here. Four walls, all in its
    recipe's note.
  - `spooler` wants its author's `local.h` — the one with `loop` and `ERROR`
    in it, not the `auxlib` one this disk carries.
  - `gtar` wants **blarslib**, which IS in the pool. See
    `notes/BLARSLIB.md`; that is a decision, not a search.
  - ~~`macutils`~~ — **UNBLOCKED 2026-08-23.** The reason given below (cpp
    will not search a `-V` directory for an include name with a directory in
    it) was correct and is now obsolete: GNU cpp does, and a recipe's `-V=`
    reaches that pass. `binhex` and `unsit` build.
  - ~~`mtools`~~ — **BUILDS, 2026-08-23, with the GCC flag.** It was never a
    timeout and `ansi2knr` was never going to reach it: its OSK port is a
    `gcc2` build and the disk carries a whole GCC 2.5.6 in `CMDS/GCC2`. What
    stopped anyone was that gcc2 here could not compile a two-line program
    until `DEFS/GCC2` was repaired. 45 sources; `mdir` runs.

**A `cpp` defect -- and it is now MEASURED, not guessed.**

  Microware's `cpp` bus-errors on a source line of **513 characters or more**;
  `c68` stops at **1023**. Both measured 2026-08-23 -- see
  `notes/CPP-MACRO-CRASH.md`, whose title is now the only wrong thing left in
  it. It is not "nested macro expansion"; nesting is just how a line gets long.

  - `flex` -- BUILDS, through `CPP2`.
  - `djpeg` -- BUILDS, through `CPP2` and `KNR` together, 2026-08-23. The
    IJG's own round-trip test passes on it.
  - `gtar` -- past `cpp`, past `c68`'s line limit, past its includes and its
    three ANSI definitions. Stopped on five or six names (`ERROR`, `TRUE`,
    `S_IFREG`, Unix `errno`) that want narrow COMPAT additions. The
    `DEFS/os9lib` set has them all and is a dead end; the note says why.
  - `inform` -- not attempted since the measurement.

**Not program trees.**

  - `COMPAT` is headers. `unixlib` is a library and now has a recipe of its
    own kind (`unix.l`).

**ANSI C.** This is the big remaining category, and it is one job, not
several: these trees declare prototypes, and Microware's `cc` is K&R.

  - `lua`, `jpeglib`, `gnuchess/GNUCHESS4.0`, `ed`, `lout`, and probably
    `cnews`, `rayshade` and `infoxpress`.

  **The lever exists and is in** -- the `KNR` recipe flag, 2026-08-23. It runs
  every source through `ansi2knr` before `cc`. `cjpeg` builds that way; that
  is JPEG's whole compressor, 27 sources, and it had never compiled here.

  **But it only goes so far.** `ansi2knr` rewrites function DEFINITIONS and
  leaves headers alone, so a tree is only reachable if its own headers can be
  told to stop declaring prototypes:

    reachable      JPEG -- jconfig.h has HAVE_PROTOTYPES, `const', and
                   INCOMPLETE_TYPES_BROKEN, which is provided for compilers
                   exactly like this one
    not reachable  lua -- by ansi2knr, yes.  But that was the wrong question:
                   lua compiles fine under the GCC flag (16 of 17 sources, and
                   luac 17 of 17).  Both stop on ABSENT MATERIAL instead --
                   ldblib.h for lua, and Ultra C's syscall library for luac.

  So `lua`, and probably `ed` and `lout`, are header work rather than a flag.
  `djpeg` is neither: it is the cpp defect.

**Still ordinary work, nobody has done it.**

  - `inform`, `ioccc` (eleven more contest entries), `macutils` (blocked on
    an include-path knot, see `notes/SESSION-2026-08-23.md`), `pdksh` (has its
    own `build_ksh.sh` rather than a recipe).

---

# The 2026-08-22 morning pass, as it stood then

## Where it stands

    170  source trees under disk/SRC
     99  had a build recipe          -- 194 programs, known to compile
     71  had none                    -- never established either way

Of the 71, **18 map to exactly one shipped program**, which makes them the
cheapest to settle. `tools/try_compile.sh --all` tries each with the naive
recipe -- every `.c` in the tree, the standard flags -- and reports what
happened.

    8  BUILD, and now have a recipe
   10  do not, each for a reason below

`recipes.psv` is 212 recipes now, up from 204.

## The eight

`tsmon2`, `indent`, `robots`, `today`, `wish` and `xlisp` build with nothing
but the naive recipe. Two needed one library each:

  - **`draw`** wants `mytime` -- `/dd/LIB/mytime.r`, which is in the SDK LIB
    as a loose object, not inside any `.l`, so it has to be named explicitly.
  - **`shuffle`** wants `optarg` -- `/dd/LIB/os9lib.l`.

## The ten, and what each is waiting for

| tree | program | stops at |
|---|---|---|
| `adv` | advent | `execv` unresolved; not in os9lib either |
| `argproc` | argproc_demo | `bcopy` unresolved -- `shims/os9bcopy.c` should do it |
| `nobs` | nobs | `isupper` unresolved; it is in `csl.l`, which a `-qm` build cannot use |
| `snake` | snake | `#include <a.out.h>`, which is on no disk here |
| `cursive` | cursive | duplicate symbols -- the all-`.c` list is too long, two mains |
| `proff` | proff | duplicate symbols, same shape |
| `hist` | hist | undeclared identifier in its own `h_var.h:77` -- an `#ifdef` arm |
| `pep` | pep | undeclared identifier, `plain.c:165`; it also wants an EPROM driver |
| `flex` | flex | no single diagnostic; read the log |
| `ioccc` | queens | no single diagnostic; deliberately obfuscated C, so expect nothing helpful |

Four of those (`cursive`, `proff`, `hist`, `pep`) are ordinary recipe work --
the file list is wrong, or a define is missing. `adv`, `nobs` and `snake` are
waiting on something that is genuinely absent.

## A bug this found in itself, worth not repeating

The first run reported `argproc`, `hist` and `proff` as **missing headers they
in fact ship**: `boolean.h`, `h_def.h` and `lextab.d` are all sitting in their
own trees. The prober had copied them but had not put the tree's own directory
on the include path, so a source writing `#include <boolean.h>` rather than
`"boolean.h"` looked in `/dd/DEFS` and found nothing. `rebuild.sh` passes
`-V=/h6/<tree>` for exactly this reason and the first draft here did not copy
it.

The lesson is the collection's own: **make the check fail once before believing
it.** Three "missing header" verdicts were the checker's fault, not the
source's.

## What is left

The other 53 un-recipe'd trees map to several programs each, or to none that
ships. Those need the archive-versus-program mapping read out of `DOC/ORIGINS`
first -- `SRC/divutils` holds `gen`, `run` and `if`, and counting by tree name
over-counts badly. That is the next increment.


## C++ works. homelibr still does not. (2026-08-24)

**The disk can compile, link and run C++.** Proven end to end with a class,
a constructor and a method call: it printed what it was supposed to. What it
took, none of it obvious:

  - **`gcc2` cannot start the C++ front end at all.** Its suffix table has no
    entry for a `.cc` -- it calls one a "linker input file unused since
    linking not done" -- and `-Fcc2plus`, which the homelibr makefiles use,
    does not change that. The only door is `gpp`.
  - **`gpp` forks `cccp`, and nothing on this disk answers to that name.**
    The preprocessor ships as `cccp2`, which is what `gcc2` forks. A plain
    copy under the other name is enough; the module inside is still called
    `cccp2` and os9exec runs it.
  - **`collect` is in `CMDS/GCC2`, not `CMDS`.** Any program with a global
    constructor needs it, or the link stops on `__CTOR_LIST__` and
    `__DTOR_LIST__` unresolved. Only gpp's spec runs it.
  - **`collect` opens `gpp.l`; the disk ships `libgpp.l`.** Another copy.
  - The link must go through `gpp`, not `l68` by hand the way the C path
    does it -- and gpp has no `-n=`, so **the module takes its name from the
    output FILE**. Write the file as `<prog>` and rename the file afterwards.

`make_overlay.sh` makes all three names now, and `rebuild.sh` has a `GPP`
recipe flag. **No recipe uses it yet**, because the only C++ in the tree is
homelibr and homelibr does not build.

### What blocks homelibr

Six programs -- `Ascii2Libr`, `EditLibr`, `Libr2Ascii`, `Librarian`,
`PrintCards`, `PrintLabels` -- all six already on the disk as working
binaries. Fixed so far: `Include/common.h` had `#include <sgstat.h>`
commented out, so `Terminal.h`'s two `sgbuf` members were an undeclared type
and every file that reached that header stopped. That one is done and marked.

What is left is a **dialect** problem and a **library** problem, and neither
is a five-minute fix:

  - **Pre-standard class constants.** `const bufSize = 512;` inside a class,
    then `char Terminal::termBuf[bufSize];` at file scope in the `.cc`.
    GCC 2.5.6 wants `Terminal::bufSize`. Same for `TCapsLen` and
    `maxblocks` -- eight or so sites across `Terminal.cc`, `Card.cc`,
    `PTree.cc`.
  - **`fstream.h` does not exist here, and cannot.** `EditForm.cc` declares
    `ofstream` and `ifstream`. `LIB/libgpp.l` is libg++ **1.x**: it has
    `filebuf` and `File`, and no `fstream`, `ifstream` or `ofstream` at all.
    Writing the header would mean writing the classes.
  - **`<stdlib.h>` collides.** With `-I/dd/DEFS/CC` on the path, `<stdlib.h>`
    is libg++'s, not the SDK's, so `os9forkc` -- which `Terminal.cc` passes
    to `os9exec` -- is undeclared. Putting the SDK's first breaks the C++
    headers instead.
  - `ParseExpr.tab.cc` includes `"ParseExpr.tab.h"` and cccp2 does not search
    the source file's own directory, so that one needs `-V=<tree>/Lib`.

None of it is impossible. It is a port, not a recipe, and the payoff is
reproducibility for six binaries that already work.
