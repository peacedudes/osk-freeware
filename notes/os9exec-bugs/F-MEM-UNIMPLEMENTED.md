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
