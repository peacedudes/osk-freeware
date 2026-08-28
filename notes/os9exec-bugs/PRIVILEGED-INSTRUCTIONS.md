# os9exec is always a 68020, and that stops 68000-era programs

Measured 2026-08-27, against os9exec at `~/Developer/os9/os9exec`.

## The finding

`creadoc`, part of the RTF Fortran-77 system, stops with

    Exception: pid=3 vector=$08 err=#000:108
    Executing: -->00098d44: 40c0  MVSR2.W D0        (= MOVE SR,D0)

`MOVE SR,<ea>` is **user-legal on the MC68000** and **privileged from the
MC68010 onwards**. (The 68010 is where Motorola made it privileged and added
`MOVE CCR,<ea>` for user code that only wanted the condition codes.)

os9exec hardcodes a 68020 and offers no way to ask for a 68000:

    Source/OS9AppEmu/os9_uae.c:261
        currprefs.cpu_level = 3;   // 68020+68881

    Source/OS9AppEmu/UAE68emulator/cpuemu.c:12170   op_40c0_0  /* MVSR2 */
        if (!regs.s) { Exception(8,0); ... }

So the instruction traps unconditionally. `creadoc` is not damaged and is not
mis-built: it is a 68000 program, doing something a 68000 permits, on an
emulator that is not a 68000.

**This is a fidelity gap, not obviously a defect** -- os9exec chose to be a
68020 and says so. It is recorded because the symptom (`vector=$08` on an
ordinary-looking program) is otherwise unreadable, and because the collection
was previously calling error 108 something it is not.

## Error 108 is E_VIOLAT, not E_BUSERR

From os9exec's own `Source/OS9exec_core/os9defs/os9errno.h`:

    #define E_BUSERR    102  /* bus error (exception 2) */
    #define E_VIOLAT    108  /* privilege violation (exception 8) */

`DOC/STATUS` called 108 "E_BUSERR" in three places. Corrected 2026-08-27.
The two are different exceptions with different causes and the distinction is
the whole diagnosis: 102 means a bad address, 108 means a legal address and
an instruction this processor will not run in user state.

## What actually faults, with modules loaded

The four-stage sweep runs every program with NOTHING loaded, so a program
that links a module never reaches its own code and its recorded verdict says
nothing about it. Re-run with Microware's `load` (the trap-free `NOCSL/load`
build -- the ordinary one stops on `csl traphandler mismatch` against our
edition-16 `csl`), 70 NEEDS WORK programs, 46 reached before batch timeouts:

    program                vec  meaning                instruction
    CMDS/devprc            $02  bus error              CMP.W #$4afc,(A0)
    CMDS/oleo              $04  illegal instruction    ILLEGAL
    CMDS/os9lib            $02  bus error              MOVE.W (A0),D1
    CMDS/ptxminst          $02  bus error              MOVEA.L (A0,$03a4),A0
                                                       == $aaaaae48
    CMDS/GAMES/g           $08  PRIVILEGE VIOLATION    RTE
    CMDS/GAMES/graphdemo   $08  PRIVILEGE VIOLATION    RTE
    CMDS/GAMES/graphsave   $08  PRIVILEGE VIOLATION    RTE
    CMDS/GAMES/showpic     $08  PRIVILEGE VIOLATION    RTE
    CMDS/GAMES/sine        $08  PRIVILEGE VIOLATION    RTE
    CMDS/GAMES/striche     $08  PRIVILEGE VIOLATION    RTE

Two separate causes wearing the same vector:

  - **The Graph six** fault on `RTE`, at ONE address inside the shared
    library. `RTE` is supervisor-only on every 68k. This CONFIRMS what
    `DOC/STATUS` already concluded from the library's own documentation --
    it runs with the supervisor bit set -- and replaces a guess about "its
    own first instruction" with the instruction. `apfel` is the seventh and
    was cut off by a batch timeout, not observed to differ.
  - **`creadoc`** faults on `MOVE SR`, which is a 68000/68010 difference and
    nothing to do with supervisor state. A real 68000 runs it.

`ptxminst` is neither: it reads a fill pattern (`$aaaa...`) through a
structure nothing set up. `DOC/STATUS` used to say it "needs supervisor
state"; that was a guess and the fault does not support it. Corrected.

## The methodological point, which is bigger than any of these

**Every sweep this collection has run loaded no modules.** For any program
that links one, the recorded verdict measured a condition that would never
occur on a real system -- the program exiting early because `F$Link` failed.
`DOC/STATUS`'s "silent in every stage" group is full of these, and the six
Fortran programs sat in it for weeks.

A verification pass that means anything has to `load` first. That is now
possible without OS9MDIR, which was an os9exec environment variable being
documented to users as though it were OS-9.
