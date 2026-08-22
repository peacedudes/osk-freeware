# Does the source compile?

rdoggett, 2026-08-22: *"verify we have it all (if it's source, it should
compile, right?)"*

Right. Until now that had only ever been established for the trees that have a
recipe. This is the count, and the method for closing the rest.

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
