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

## Addendum 2026-09-03: `biory` is the second casualty, and it is a card that cannot be made

`biory`, the RTF Fortran biorhythm program, takes its three answers and
then stops the same way, inside the run-time rather than the program:

    PC=00077DE2 SR=0005
    Executing: -->00077de2: 40c0 4880 0c40 0005 6704 MVSR2.W D0
                  00077de4: 4880 ...                  EXT.W D0
    Exception: pid=3 vector=$08 err=#000:108

`MOVE SR,D0; EXT.W D0; CMP.W #5,D0; BEQ` -- the run-time reading the
status register before it writes the first line of the chart.  rdoggett
named biory on 2026-09-03 as the model card (German prompts, translated,
answered, and the chart shown), and the chart cannot be shown on os9exec as
built.  A 68000 CPU mode -- or emulating `MOVE SR,<ea>` in user state the
way a 68010+ OS-9 kernel's privilege-violation handler can -- would make
both biory and creadoc run.  Whether Microware's kernel does that emulation
is not settled by anything in the os9-dev skill; it is a question for the
manuals.

## Seen alongside, not a fault: `F$SetSys: unimplemented 03D8 (size=80000004)`

Printed to the console four to eight times at start-up by biory and also by
`scales`, a plain C program, so it is the run-time reading a 4-byte system
global at offset $3D8 that os9exec does not model; os9exec answers 0 and
both programs go on.  `getsys` reads a page of them ($076C-$08EC).  The
message is os9exec's dbgAnomaly diagnostic, on by default, and it lands
on every card the program is on, so `gen_screens.py` now leaves those
lines off the published screen.  Which global $3D8 is has not been looked
up.

## Resolved 2026-09-04: os9exec no longer traps MOVE from SR in user state

os9exec commit `852dddd` ("MOVE from SR is user-legal, as on the 68000 it
was built for") removes the privilege check from the MVSR2 handlers, with a
test (`t50`) that failed first.  MOVE to SR, RTE, STOP and RESET stay
privileged, so the Graph six still fault on RTE and that is right.

Measured against the rebuilt binary the same evening:

- **`biory` writes its chart.**  Three answers, then Biory.Lis, 3558 bytes,
  twelve months of Koerper/Seele/Geist, and it loops back to the name
  prompt.  Its card now shows the chart.
- **`creadoc` runs past the instruction** and reaches a stop of its own:
  it reads file names from a fixed column of a `dir -eadu` listing
  (`fnpos = 53` in creadoc.f) and expects a two-digit year there, being a
  1989 program.  OS-9 prints 2026 as `126', one digit wider, so the name
  lands a column right and creadoc opens `" biory.f"' -- a leading space --
  and gets 214.  This is a pre-Y2K program meeting a post-1999 date, NOT
  the parser: F$PrsNam follows the 68k manual and does not skip a leading
  space (rdoggett/os9exec, 2026-09-05).  Date the sources before 2000 and
  the column is right, and creadoc still writes nothing -- a second stop,
  not yet found, and not a MOVE SR matter.

The Graph programs are unchanged: RTE is supervisor-only on every 68k.
