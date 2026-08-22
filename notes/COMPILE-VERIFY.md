# "If it's source, it should compile, right?"

rdoggett's question, 2026-08-22. This is where the answer stands.

    170  source trees under disk/SRC
     99  have a build recipe in tools/rebuild/recipes.psv  -> 194 programs
         that are KNOWN to compile
     71  have no recipe.  Nobody had ever established whether their source
         is complete

`tools/try_compile.sh` closes that gap one tree at a time. It makes the naive
attempt -- every `.c` in the tree, the standard flags -- and classifies the
failure against the table in `tools/rebuild/README.md`.

## First 18 trees (the ones mapping to exactly one shipped program)

    BUILDS   eff_tsmon(tsmon2)  indent  rob(robots)  today  wish  xlisp
    FAILS    adv argproc cursive draw flex hist ioccc nobs pep proff
             shuffle snake

Six of eighteen build with no work at all.

## The failures are NOT mostly broken source

Grouped by what the message actually means:

## UPDATE, same day: four of the five library gaps are filled

`disk/SRC/unixlib` now has `execv.c`, `getopt.c`, `vsprintf.c` (which also
supplies `vfprintf` and `vprintf`) and `ctype.c` (the `isupper` family as real
FUNCTIONS, not only macros). They are written in the tree's own house style and
each says in its header which program it unblocked.

    argproc  BUILDS  with vsprintf.c and bcopy.c
    shuffle  BUILDS  with getopt.c
    nobs     BUILDS  with ctype.c

That is three more trees compiling from source that is ON THE DISK, needing
nothing from the SDK. Recipes added.

**`adv` is still stuck, and not on a missing function.** With `execv` supplied
it gets further and then collides: `adv/main.c` defines its own `chain`, and
referencing `chainc` drags in `clibn.l`'s `process_a` psect, which defines
`chain` too. Its tree also carries three files with `main()` -- `main.c`,
`okplay.c`, `test.c` -- so any recipe must name sources explicitly. Both are
ordinary recipe problems, not missing library.

**`draw` links `/dd/LIB/mytime.r`**, an SDK object with no source here. It
builds, but it is the one recipe that reaches outside the collection.

### The original diagnosis, for the record

  - **A library function this C library does not have — 5 trees.**
    `execv` (adv), `vsprintf` (argproc), `optarg`/getopt (shuffle),
    `isupper` (nobs), `mytime` (draw). `disk/SRC/unixlib` supplies `bcopy`
    and `execl` but not these. **This is the single highest-leverage thing
    for source completeness**: the same few functions block several programs,
    and `vsprintf` is the same gap that blocks pdksh. A fuller unixlib would
    move more trees at once than any per-tree work.
    (`mytime.r` exists as an object in `~/Developer/os9/play/*/LIB/`, so that
    one is a link away rather than a rewrite.)
  - **Source list too long or too short — 2 trees.** `cursive` and `proff`
    fail on `duplicate symbol names`, which per the README means a whole-tree
    link pulled in a second `main`. A recipe naming the right files fixes it;
    that is what a recipe IS.
  - **Genuine source problems — 2 trees.** `hist` (undeclared identifier in
    its own `h_var.h`) and `pep` (already documented as wanting an EPROM
    programmer's driver that does not exist here).
  - **A header that is nowhere — 1 tree.** `snake` wants `a.out.h`, which is
    not on the disk and not in the SDK.
  - **Not yet read — 2 trees.** `flex` and `ioccc` produced no line the
    classifier recognised.

## One trap this found, in my own tool

Three of the first-pass failures were the prober, not the source: without
`-V=/h6/<tree>` the tree's OWN directory is not on the include path, so a
source writing `#include <boolean.h>` for a header sitting right beside it
fails with `can't open /dd/DEFS/boolean.h`. That reads exactly like a missing
file and is not one. `rebuild.sh` has always passed that flag.

## Worth knowing: unixlib has a correct strchr

`disk/SRC/unixlib/strchr.c` handles the terminating NUL properly -- its own
comment says *"The null character terminating a string is considered to be
part of the string"*, which is the ANSI behaviour. pdksh's `osk.h` does
`#define strchr index`, and OS-9's `index(s,0)` returns NULL, which is what
made six `strchr(s,0)` sites in pdksh into bus errors (see
`tools/rebuild/pdksh/README.md`).

**Dropping that one `#define` and linking `unixlib/strchr.c` would fix all six
at once**, and any future use as well. The six sites are patched individually
at present, which works but does not protect the next one written.

## Next

The remaining 53 un-recipe'd trees are multi-program or have their sources in
subdirectories, so they need a recipe written rather than a naive attempt.
Run `tools/try_compile.sh <tree> <program>` on one and read what it says.
