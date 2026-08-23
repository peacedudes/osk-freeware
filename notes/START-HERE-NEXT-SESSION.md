# Picking this up cold

Branch `release-pass-2026-08-21`, 107 commits, **nothing pushed**. Working tree
clean, all eleven `check_disk.py` checks green.

## Get running in two minutes

    cd ~/Developer/os9/osk-freeware
    export OS9EXEC=~/Developer/os9/os9exec/os9exec
    export OS9CLEAN=${TMPDIR:-/tmp}/os9clean

    tools/rebuild/make_overlay.sh "$OS9CLEAN"   # the build /dd; ~40s
    tools/build.sh ansi2knr                     # KNR recipes need it in the overlay
    tools/build.sh --missing                    # what has no recipe, and why
    tools/check_disk.py disk                    # eleven checks
    tools/rebuild/tidy.sh                       # after ANY build, always

`tools/build.sh` builds every recipe (~1.5 hours, 277 of them). One program:
`tools/build.sh flex`.

## The one thing that is NOT verified

The last whole-tree build was **271 of 274 clean**. Since then three recipes
were added — `ansi2knr`, `cjpeg`, `flex` — each verified on its own but never
in a full run. **Run `tools/build.sh` once and trust that number, not this
paragraph.**

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
