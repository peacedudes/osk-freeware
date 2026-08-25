# Picking this up cold

Branch `release-pass-2026-08-21`, 343 commits, **nothing pushed**. Working tree
clean, all eleven `check_disk.py` checks green.

## Get running in two minutes

    cd ~/Developer/os9/osk-freeware
    export OS9EXEC=~/Developer/os9/os9exec/os9exec
    export OS9CLEAN=${TMPDIR:-/tmp}/os9clean

    tools/build.sh --from-scratch               # THE WHOLE THING, one command:
                                                # discards the cached overlay,
                                                # rebuilds it, bootstraps
                                                # ansi2knr, builds all 325
    tools/build.sh --missing                    # what has no recipe, and why
    tools/check_disk.py disk                    # eleven checks
    tools/rebuild/tidy.sh                       # only if you drove rebuild.sh
                                                # directly; build.sh calls it

`tools/build.sh` builds every recipe (~2 hours, 325 of them). One program:
`tools/build.sh flex`.

## Where the build stands

**323 of 325 recipes clean**, whole tree, from a clean clone, measured
2026-08-24: `tools/build.sh --from-scratch`, overlay discarded and remade.
The two that fail have always failed and neither is a linkage problem --
`pdraw` wants X11 headers that are not here, `pep` wants an EPROM board's own
assembly. Re-measure rather than trust this paragraph.

`tools/src_census.py disk` for coverage: 390 of 937 programs have source
here, 313 of them built by a recipe. Both move whenever a recipe lands.

## What changed on 2026-08-23/24, in one screen

Read `notes/SESSION-2026-08-24.md` for the detail. The headlines:

  - **`ls` is rebuilt from `SRC/ls` and INSTALLED** -- 39 of 40 option cases
    byte-identical to the binary it replaced, `-i` better (real inodes).
    The only shipped binary changed in this pass.
  - **Recipes 290 -> 325**, programs built by a recipe **279 -> 313**.
    18 mtools commands, 6 macutils, elvis's 4 helpers, 5 singles, `aterm`.
  - **`aterm` assembles byte-for-byte identical to the shipped binary.**
    New `ASM` recipe flag; `os9.l` + `sys.l` resolve the 53 system names.
  - **The disk can build C++**, and the gcc toolchains are documented and
    usable for the first time -- see below.
  - **`tools/src_census.py`** is new: source coverage as a re-derivable
    number instead of a hand count. 390 of 937, 41%.

## The gcc toolchains -- the thing most likely to bite you

`DOC/README-GCC` is the full story. The short version, because it wasted
hours: **gcc2 and gpp find their passes by a hardcoded prefix, and it is a
DIFFERENT prefix for each.**

    gcc2   /dd/CMDS/gcc_<pass>    and  /h0/CMDS/gcc_<pass>
    gpp    /dd/CMDS/gpp_<pass>    and  /h0/CMDS/gpp_<pass>

Everything else it runs -- `r68`, `l68`, `del` -- is forked by bare name and
found in the EXECUTION directory, normally `/dd/CMDS`. The passes ship in
`/dd/CMDS/GCC2`, which is none of those places, so out of the box you get
`Can't fork 'cccp2'`. That is not a broken binary.

`r68`, `l68`, `clibn.l` and `cstart.r` are Microware's and are NOT on the
disk. gcc compiles to assembly and stops there without them. Bring an SDK.
With one, both C and C++ compile, link and run -- verified 2026-08-24.

**A trap that cost a wrong recommendation:** the BUILD OVERLAY has a flat
`CMDS` and the SDK headers, so everything gcc works there. The DISK has
neither. Proving something in the overlay proves nothing about the disk.

## One decision waiting for rdoggett

Whether to ship five files in `/dd/CMDS` -- `gcc_cccp2`, `gcc_cc2`,
`gpp_cccp`, `gpp_cc1plus`, `gpp_collect` (~1 MB, `cccp2` twice) -- so the
compilers work without the user first reading README-GCC. Alternatives: one
`gccsetup` script, or leave it to the documentation. He has not answered.
Do not do it unasked; `disk/CMDS` is his.

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
