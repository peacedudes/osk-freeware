# Two unrelated programs die on the same illegal instruction at the same address

Seen 2026-09-03. `oleo` (GNU Oleo 1.6, a spreadsheet) and `editor` (Uwe
Simon's GSHELL front end for umacs, only when given a path on its command
line) both stop like this, from a login session:

    Illegal instruction: 0009 at 000465d2

    Process   Pid: 3, oleo, edition 7
        Exit code: E_PRCABT(228) Process Aborted

and the same two lines with `editor` in place of `oleo`, also edition 7.
Same opcode word, same PC, in two programs from different authors and
archives, neither of which uses a trap library. Either 0x465d2 is where
os9exec puts something both reach through a bad pointer, or both were
built with the same faulty run-time. Not investigated further; recorded
because two programs sharing one crash address is a pattern, and the
pattern belongs to the emulator side to explain. `editor` run bare works.
