# withheld/

Things made for this collection that do not ship on the disk, kept here
rather than deleted until rdoggett rules on them.

- `load/` -- a clean-room reimplementation of Microware's `load` utility,
  written by the os9exec project from the published manuals (2026-08-27).
  Not Microware's code, but a program named for one of theirs is theirs to
  ship, so it came off the disk on 2026-09-22.  Readers use their own
  `load` from /h1.  The test harnesses still stage this copy at
  /h1/CMDS/load when no SDK is at hand (`tools/os9env.py`,
  `stage_reader_load`), so CI can run the cases that load a module.
