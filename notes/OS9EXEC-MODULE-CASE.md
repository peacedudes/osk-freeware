# WITHDRAWN as written: `Graph` is not a case bug. What it actually is.

**Filed 2026-08-26, corrected the same day** after review. The original claim
was that os9exec's module load is case-sensitive where RBF is not. **That is
wrong**, and the evidence I gave for it, while true, was about a different
code path from the one that fails.

## The disproof

Put ONLY the lowercase `graph` in the module directory and `g` runs -- the
trap handler installs, no error. Case never mattered. My "fix" earlier put a
directory containing BOTH `graph` and `Graph` on the search path, and I
credited the capital one.

## What actually happens

    # Installing Traphandler for pid=2, Trap #5, mpath='Graph'
    # load_module: searching module 'Graph' (exec, linking)
    # load_module: mid=4 isPath=0 exedir=1
    # load_module: trying to load from OS9MDIR: /Users/rdoggett/Developer/os9/OS9MDIR
    # install_traphandler: link_load('Graph') for pid=2 returned err=$D8

**The search goes to `OS9MDIR` -- a HOST directory -- and when that variable
is unset it falls back to `<something>/OS9MDIR`, which does not exist.** It
never looks on `/dd` at all. So `E_PNNF` is correct: the loader looked
somewhere real and the file was not there.

That also explains why my RBF evidence was beside the point. RBF's opens ARE
case-insensitive -- `wc` reads the same 5138 bytes from `graph`, `GRAPH` and
`Graph` on the image, and `ls` on a genuinely absent name errors with 216, so
the control holds -- but the module search never reaches RBF.

**Microware's manual on the underlying question, for the record**
(*Using Professional OS-9 v2.4*, on file naming): *"OS-9 does not distinguish
upper case letters from lower case letters. The names FRED and fred are
considered the same name."* So case-insensitivity is specified, not a
convention -- it is simply not what is failing here.

## What is left, and it is a real problem for a user

Eight programs -- `g`, `striche`, `apfel`, `sine`, `showpic`, `graphdemo`,
`graphsave`, and `rxmod` against `vmod_trap` -- link a library module that
lives in the SAME directory as they do on the image, and cannot find it.

A user following `DOC/README-RUNNING` sets `OS9DISK` and nothing else, so
`OS9MDIR` is unset and these eight fail. **And they cannot work around it:
there is no `load` on this disk.** `disk/CMDS/load` does not exist, so the
"load graph first" answer is unavailable to anyone who has only this
collection. Microware's own `load` needs a matching `csl`; the SDK's `load`
with the DISK's `csl` stops at `**** csl traphandler mismatch ****`, and only
the SDK's own `csl` beside it works.

So there are three candidate repairs and they belong to different owners:

  1. **os9exec** -- should a trap-handler link search the process's execution
     directory on the mounted disk before falling back to a host `OS9MDIR`?
     That is the question for the maintainers. I am NOT asserting it is a
     defect; I could not find where the exec-directory case is supposed to be
     handled, and guessing is what produced the withdrawn claim above.
  2. **the collection** -- ship a `load`, so a user can preload `graph`. That
     is ours and is probably the cheapest real fix.
  3. **the collection** -- or document `OS9MDIR` in `DOC/README-RUNNING`.

Nothing was renamed and nothing was patched.

## The lesson, since it is the second time tonight

I had a mechanism that fit the evidence and I stopped there. The disproof cost
one command -- remove the capitalised file and re-run -- and I did not run it
because the story was already satisfying. `notes/` says "make every check fail
once before believing it"; a check that only ever succeeded is the same trap
wearing a different hat.
