# "If it's source, it should compile, right?"

rdoggett, 2026-08-22. Right, and now it does, for all but a handful with
named reasons.

## One command

    tools/build.sh                 build everything there is a recipe for
    tools/build.sh ls cat vi       build just these
    tools/build.sh --list          what can be built, and from which tree
    tools/build.sh --missing       source trees with no recipe yet

No setup. It makes the clean `/dd` overlay itself (that used to be an
undocumented local directory, and its disappearance made the whole rebuild
machinery unusable), finds the SDK through `tools/paths.py`, and takes the
emulator from `$OS9EXEC`. It INSTALLS NOTHING: each build lands beside its
sources as `R_<program>`, and what goes on the disk stays a deliberate act.

## Where it stands

**191 of 197 recipes compile clean.** The six that do not each want something
that is genuinely not here:

| program | wants | |
|---|---|---|
| `convert` | `parame.inc` | not in the pool, not in the SDK, nowhere |
| `sonnet` | `lex.i` | likewise |
| `patch` | `config.h` | GNU patch GENERATES this from Configure; the tree shipped without it, and writing one would be inventing the porter's configuration |
| `pdraw` | `X/Xlib.h` | needs X11 headers |
| `pep` | `standby` | an EPROM programmer's hardware routine |
| `ls` | — | a gcc2 build whose objects Microware's `l68` will not link |

That is the honest floor. Everything else on this disk that has source, and a
recipe, builds.

## What it took, and what each fix was

Nine of the earlier failures were **not broken source**. They are worth
listing because the same shapes will recur:

  - **`rebuild.sh` called a bare `./os9exec`** at the repository root. With no
    binary there, EVERY build failed with `env: No such file or directory` and
    was recorded as FAIL -- indistinguishable from broken source. It honours
    `$OS9EXEC` now, like every other tool here.
  - **Nine recipes pointed at source that had been removed.** Deleting a
    program leaves its recipe behind, and the next build reports it as a
    failure forever. `check_disk.py` has a tenth check now: a recipe must name
    a tree that exists AND sources that exist. Both halves were made to fail
    on purpose.
  - **Two recipes had been wrong for a long time** -- `eff_tsmon2` and
    `eff_indent/SRC` name trees that do not exist. Retargeted.
  - **`hist`** was one of those, and builds once pointed at `SRC/hist`.
  - **`devprc`** wanted `_gs_sopt`, which its own `getsys.a` supplies; the
    recipe named neither that nor its own `getopt.c`.
  - **`bmgtest`, `bmgtest2`, `lp`, `lpq`** named sources that live in other
    trees. Recipes can reach them as `../unixlib/bcopy.c` and the like.
  - **`gen`, `if`, `run`** include `"../defs/misc.h"` and `"../DEFS/bool.h"`,
    a directory layout that never shipped -- the headers sit beside the
    sources. Changed to `"misc.h"` and `"bool.h"`.
  - **`chess`** used `errno` without including `<errno.h>`: K&R code relying
    on an implicit declaration this compiler will not make.

## Four functions this C library never had

`disk/SRC/unixlib` now supplies them, written in the tree's own house style,
each naming in its header the program it unblocked:

    execv.c      exec with an argument vector -- adv
    getopt.c     the System V option parser -- shuffle, and the commonest
                 single reason a ported Unix program will not link here
    vsprintf.c   vsprintf, vfprintf and vprintf; there was no v-printf family
                 at all and no _doprnt to build one on -- argproc, and the
                 same gap that blocks pdksh
    ctype.c      isupper and its family as FUNCTIONS; <ctype.h> has them only
                 as macros over _chcodes -- nobs

Read `vsprintf.c`'s header before touching it: it is safe for a stated reason
(68k passes every scalar as one 32-bit word), not by luck, and it cannot carry
a `double`.

`adv` is the one that got away. With `execv` supplied it collides instead:
`adv/main.c` defines its own `chain`, and referencing `chainc` drags in
`clibn.l`'s `process_a`, which defines `chain` too. Its tree also holds three
files with `main()`. Both are recipe problems, not missing library.

## The trees with no recipe

`tools/build.sh --missing` lists them. They are mostly multi-program archives
or have their sources in subdirectories, so each needs a recipe written rather
than a naive attempt. `tools/try_compile.sh <tree> <program>` makes that naive
attempt and classifies what stopped it against the table in
`tools/rebuild/README.md`.

Remember that a tree is named by ARCHIVE, not by program: `SRC/divutils` holds
`gen`, `run` and `if`; `toys` builds `wish`. Counting trees against program
names over-counts badly, and `DOC/ORIGINS` is the map.
