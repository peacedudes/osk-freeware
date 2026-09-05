# F$Mem is not implemented, and `subber' stops on it

Found 2026-09-03 by the Text tools batch, against os9exec at
`~/Developer/os9/os9exec`.

`subber' -- Carl Kreider's "substitute text in a stream, ,old,new style" --
calls F$Mem (change data memory size) for its first allocation and gets
this on the console instead of memory:

    bash# subber /dd/tmp/TEXTA/subs /dd/tmp/TEXTA/fox.txt
    # unimplemented F$Mem called by pid=3
    bash#

No exception dump: os9exec prints the line and the program exits. F$Mem is
an ordinary OS-9/68000 system call (the skill's `68k/syscall-reference.md`
lists it) and on a real system subber would run.

To reproduce, any sheet with that stanza through `tools/probe_sheet.py`;
the two files are anything at all, subber never reads them.

`aprocs' is already recorded in DOC/INDEX as stopped the same way by an
F$SetSys it cannot get, and `getsys' reads a page of system globals os9exec
answers with zero. This is a second program stopped by an unimplemented
call rather than by a wrong one.

## Resolved 2026-09-04: os9exec `7fa2899` implements F$Mem per the manual

Query returns size and top; contraction that would reach the stack pointer
is E$DelSP; expansion takes the arena directly above the data area when it
is free and is otherwise E$MemFul, which the manual permits.

Measured on subber the same evening.  Bare, it is refused: a `cc` program
links cio right above its data area, so the first expansion has nowhere to
go.  `load /dd/CMDS/cio` first and it substitutes.  `subber #256k words
file` from Microware's shell runs with no expansion at all; `#128k` does
not.  The call site is the C library's own (every C program here carries
it); subber is the one program that reaches it.

Correction, later the same evening: `#256k` was not what made it run.  A
second run in the same session succeeded or failed by what the previous
process had left above the new data area, whatever the modifier said.
What holds: every ibrk goes through F$Mem (256 bytes at a time); it works
when nothing is directly above; cio loaded first from Microware's shell
gives that; bash never does.
