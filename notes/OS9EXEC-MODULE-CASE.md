# Module load is case-sensitive where RBF is not -- eight programs on this disk

**Found 2026-08-26**, working the sweep's "needs work" list. Third os9exec
defect of the night, and the cheapest of the three to describe.

## What happens

Eight programs stop with:

    **** Can't install trap handler ****
     **** Graph

`Graph` is the Atari graphics library, and `DOC/README-MODULES` already
records that it IS a library rather than a demo. All eight live in
`CMDS/GAMES` alongside it, so the execution directory is right.

With `-d1 0x0120`:

    # Installing Traphandler for pid=2, Trap #5, mpath='Graph'
    # load_module: searching module 'Graph' (exec, linking)
    # load_module: load path (exec) = Graph
    # install_traphandler: link_load('Graph') for pid=2 returned err=$D8

`$D8` is 216, `E_PNNF` -- path name not found. **The module is named `Graph`
and the file is named `graph`.**

## Why it is a defect and not a naming mistake

**RBF's own opens are case-insensitive, measured on this image:**

    os9$ ls /dd/CMDS/GAMES/graph      ->  /dd/CMDS/GAMES/graph
    os9$ ls /dd/CMDS/GAMES/GRAPH      ->  /dd/CMDS/GAMES/GRAPH
    os9$ ls /dd/CMDS/GAMES/Graph      ->  /dd/CMDS/GAMES/Graph

All three find the file. So the path layer is case-insensitive, as RBF is on
real hardware, and os9exec's module-load path is not. That is an inconsistency
inside os9exec, not a property of OS-9.

Confirmed from the other side: put a file named `Graph` where the loader looks
and the trap handler installs, `g` starts and draws. Nothing else changed.

## What it costs this collection

Eight programs, all of them the `Graph` library's own demos: `g`, `striche`,
`apfel`, `sine`, `showpic`, `graphdemo`, `graphsave`, and `rxmod` fails the
same way against `vmod_trap`. That is a sixth of the 46 programs the
2026-08-26 sweep lists as needing work.

**Nothing was renamed on the disk.** A file called `Graph` beside `graph`
would make these eight work today and would also hide the defect, and this
collection ships 63 modules whose name differs from their filename -- 61 of
them the original author's own capitalisation, which `CLAUDE.md` says to leave
alone. Renaming to suit one emulator's lookup is the wrong repair. If they are
wanted working before os9exec is fixed, that is a one-line change and a
deliberate decision.

Related: `notes/OS9EXEC-CIO-SRQMEM.md`, `notes/OS9EXEC-CIO-STDIN-EOF.md`.
