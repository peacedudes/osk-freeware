# Start here, next session

One page.  The plan is `notes/PLAN.md`; what needs rdoggett is
`notes/FOR-RDOGGETT.md`; everything that happened before 2026-09-24 is in
`notes/HISTORY-2026-08.md` and `notes/HISTORY-2026-09.md`.  Keep this file
to a page: a finding goes in the file it belongs to, and a finished
session's narrative goes into the history file, not here.

## Where it stands, 2026-09-24 (evening)

- **Every program on the image has a card taken by running it**, and
  `tools/check_disk.py disk` is the gate -- read its list, not a count.
- **Harnesses run as `tester`**, not the super-user.  A family that needs
  the super-user says `user su`; a stanza says `super`.
- **Emulator pinned at os9exec `e2c7f7b`** (scratch copy for harness runs:
  `$OS9EXEC`).  docs/try runs the same build.
- **Final verification on a fresh image, as tester**: suite pass 1
  1002/1003, pass 2 1004/1004.  The one miss was `wisecrack`/`ask` giving
  up after 30 tries; now 200 (text.cases says why).  Play-tests: see the
  commit that updated this line.
- **GitHub: PRIVATE**, https://github.com/peacedudes/osk-freeware.  Push
  the working branch `release-pass-2026-08-21` only; never `main` or a tag
  (either starts CI, which needs os9exec's branch published).  Never make
  it public.
- `tools/audit_cards.py`: 0 cards flagged.  `tools/worklist.py --programs
  --no-test`: 6 programs, all display-bound or needing Microware's
  `netdb` -- see PLAN section 3.

## Needs rdoggett (FOR-RDOGGETT)

1 (push os9exec, pin `e2c7f7b`), 45-49 (five one-instruction or header
patches to shipped binaries -- elm, bash, logname + ELM filter, mw, frm +
newmail -- each with a staged tool under `tools/patch_*.py`).  Binary patches are his
call; do not apply them.

## Work, in order -- take the top one not done, never ask which

1. **Defects found and not yet fixed** (each needs a measurement first):
   nn's `st_gid` from os9lib's stat is never filled; ELM `fastmail` and
   `newmail` mask getuid() the way filter does (FOR-RDOGGETT 47 covers
   filter); the `mw` screen's `-1[%dX` glitch.  Settled 2026-09-24: ksh's
   `test -O` is not a defect -- this pdksh spells it `-U`, and `-U`/`-G`
   hold for tester (perluid.cases); lpsched's `user&&0xffff` is recorded
   in DOC/STATUS (untestable here); frm's "no mail" is FOR-RDOGGETT 49.
   `browse` printing the year as 126 is period behaviour and stays.
   **The ELM 2.4 source is in InfoXpress_FrontEnd.lzh** (the pool), which
   the disk's notes said did not exist -- read it before guessing at any
   ELM program.
2. **`snake`'s stray cursor moves.**  PLAN section 3 lists what was ruled
   out; the source's own comment (disk/SRC/snake/move.c, above `cook()`)
   has the byte stream.  If it is the emulator's, write a repro for the
   os9exec session -- never edit os9exec.
3. **`tools/panel-exceptions.psv`** (80 lines): re-test the reasons.  The
   three shapes that keep recurring: the disk ships what the reason says
   is missing; nobody started the provider; the card filtered the content
   away.  `mailx` came off on 2026-09-24 by giving it a MAIL directory.
4. **Pages not run on a real terminal.**  If a page disagrees with the
   program, the program wins.
5. **Housekeeping** (PLAN section 5): notes stay small.

## The routine

    export OS9SDK=$HOME/Developer/os9/play/oskBoot OS9EXEC=<pinned os9exec>
    OS9EXEC_DIR=<dir holding it> tools/mkimage.sh disk <image>     # 4 s
    python3 tools/datatest.py tools/datatests/<family>.cases --image <image>
    python3 tools/playtest.py tools/playtests/<prog>.keys --image <image> --out <dir>
    python3 tools/screenshots.py tools/screenshots/<sheet> --only <shot> --image <image>
    python3 tools/gen_screens.py; python3 tools/gen_catalog.py disk docs/index.html
    python3 tools/check_disk.py disk          # the gate; exit status counts

No full suite until a backlog is through; then twice on a fresh image, then
play-tests, then rebuild `osk-freeware.dd` (rdoggett's `free` alias opens
it) and `gzip -c osk-freeware.dd > docs/try/disk.gz`.

## Traps met on 2026-09-24

- **Python's text mode turns CR into LF on read.**  `disk/` text is CR;
  `tools/datatests/*.cases` and `tools/playtests/*.keys` are LF host
  files.  Open disk files in binary, or with `newline=''`.
- **A play-test's `key` sends its argument literally** unless the whole
  argument is one named key (`\r`, `\e`, `\003`).  Type text with `keys`,
  then `key \r`.
- **This bash sets `$!` to 0** and `kill %1` fails; a background server
  that is not ended holds the family until the 300-second timeout.  The
  cases end one with `kill $!`, which works for them.
- **`timeout` (SYSADMIN) ends the Microware shell that ran it** -- ksh
  survives it.  Test it under `/h1/CMDS/shell "chx /h1/CMDS; ..."`.
- **`rmail` and `mailx` read MAIL as a DIRECTORY** with one mailbox
  directory per user; elm, frm and SYS/login treat MAIL as the file.
