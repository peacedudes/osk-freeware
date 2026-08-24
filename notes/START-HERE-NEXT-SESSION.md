# Picking this up cold

Branch `release-pass-2026-08-21`, 107 commits, **nothing pushed**. Working tree
clean, all eleven `check_disk.py` checks green.

## Get running in two minutes

    cd ~/Developer/os9/osk-freeware
    export OS9EXEC=~/Developer/os9/os9exec/os9exec
    export OS9CLEAN=${TMPDIR:-/tmp}/os9clean

    tools/build.sh --from-scratch               # THE WHOLE THING, one command:
                                                # discards the cached overlay,
                                                # rebuilds it, bootstraps
                                                # ansi2knr, builds all 290
    tools/build.sh --missing                    # what has no recipe, and why
    tools/check_disk.py disk                    # eleven checks
    tools/rebuild/tidy.sh                       # only if you drove rebuild.sh
                                                # directly; build.sh calls it

`tools/build.sh` builds every recipe (~1.5 hours, 290 of them). One program:
`tools/build.sh flex`.

## Where the build stands

**323 of 325 recipes clean**, whole tree, from a clean clone, measured
2026-08-24: `tools/build.sh --from-scratch`, overlay discarded and remade.
The two that fail have always failed and neither is a linkage problem --
`pdraw` wants X11 headers that are not here, `pep` wants an EPROM board's own
assembly. Re-measure rather than trust this paragraph.

`tools/src_census.py disk` for coverage: 390 of 937 programs have source
here, 313 of them built by a recipe. Both move whenever a recipe lands.

## Rules that cost time to learn

  - **Never edit a script, a recipe file, or anything under `disk/` while a
    build is running.** `bash` reads a script by byte offset; a mid-run edit
    killed a 40-minute build with a syntax error on a good line. And a build
    measures the tree at the moment each recipe is reached, so an edit makes
    the results a mixture.
  - **Never `git checkout -- disk/SRC`.** It ate deliberate source fixes twice.
    `tools/rebuild/tidy.sh` touches only files a build could have made.
  - **Grep CR-only files through `tr '\r' '\n'` first**, or you dump the whole
    file. Set `LC_ALL=C` or `tr` fails on 8-bit bytes.
  - **`zsh` does not word-split unquoted variables.** Two loops died of it.
  - Read `check_disk.py`'s OUTPUT, not its exit code. Committing past a red
    check has happened three times.

## Where the work is

`notes/PLAN-next.md`, in order. `notes/COMPILE-AUDIT.md` says why each tree
without a recipe has none — most are accounted for, only some are work.

For rdoggett: `notes/FOR-RDOGGETT.md`, which is short on purpose. He stops
reading when notes are long or report things he cannot act on. Lead with what
needs him, one line each, and say plainly when the answer is nothing.
