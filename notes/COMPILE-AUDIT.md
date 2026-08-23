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

  - **`ls`** — a gcc2 build. K&R `cc` will not take it.
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
  - `ed`, `lout`, `gnuchess/GNUCHESS4.0` — ANSI C. GNU `ed` also carries a
    macro that `cpp` calls too long; `lout`'s `externs` uses typed bitfields;
    GNU Chess 4.0's header is several hundred ANSI prototypes.
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
  - `spooler` wants its author's `local.h` — the one with `loop` and `ERROR`
    in it, not the `auxlib` one this disk carries.
  - `macutils`, `mtools`, `gtar` want **blarslib**, which IS in the pool.
    See `notes/BLARSLIB.md`; that is a decision, not a search.

**A `cpp` defect.**

  - `flex` — see `notes/CPP-MACRO-CRASH.md`.

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
    not reachable  lua -- lua.h declares prototypes unconditionally and there
                   is no switch; the headers would have to be converted by
                   hand, and ansi2knr does not do declarations

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
