# Start here, next session

One page.  The plan is `notes/PLAN.md`; what needs rdoggett is
`notes/FOR-RDOGGETT.md`; everything that happened before 2026-09-24 is in
`notes/HISTORY-2026-08.md` and `notes/HISTORY-2026-09.md`.  Keep this file
to a page: a finding goes in the file it belongs to, and a finished
session's narrative goes into the history file, not here.

## Where it stands, 2026-09-25

- **Every program on the image has a card taken by running it**, and
  `tools/check_disk.py disk` is the gate -- read its list, not a count.
- **Harnesses run as `tester`**, not the super-user.  A data-test family
  that needs the super-user says `user su`; a card stanza says `super`; a
  play-test says `user su`.  Play-tests mount no /h1.
- **Emulator: os9exec `8d7d870`** (branch release-v4.1.0, pushed as
  f2954f3 on 2026-09-26 with the same emulator source; CI follows that
  branch until it is frozen to the merge commit), named by the os9exec
  session as the release candidate on 2026-09-25 and not yet pushed there.
  Verified on it: suite 1019/1019 twice on a fresh image as it ships
  (modules publicly writable), play-tests 151/151, as tester.  docs/try
  runs it.  Still to do when os9exec pushes its final commit: freeze
  .github/workflows/build-image.yml's OS9EXEC_REF to that commit (it tracks
  the branch until then, as its own comments say), and re-run if the final
  commit is not 8d7d870.  os9exec says the final commit may add only CI
  workflows and README text, which change nothing the emulator runs.  `lesspipe' needs 2a95c75 or later; mmon's cases
  need 289d55e or later.
- **CI has run** (first time, 2026-09-26, manual run on this branch):
  green end to end on Linux -- gate, catalogue, os9exec from
  release-v4.1.0, image built and read back.  Its first runs found three
  things this Mac hides: captures are gitignored (the gate now skips that
  check in a fresh clone), directory walks were unsorted (DEPENDS came out
  in another order), and `Info_help' matched `info_help' only on a
  case-insensitive disk.  Release and Pages steps run only on main or a
  tag.
- **GitHub: PRIVATE**, https://github.com/peacedudes/osk-freeware.  Push
  the working branch `release-pass-2026-08-21` only; never `main` or a tag.
  Never make it public.
- `tools/audit_cards.py`: 0 flagged.  Untested programs: 5, all needing a
  display or Microware's `netdb`.  Source: 883 of 1123 (78%).
- **2026-09-24, all agreed with rdoggett and done:** seven archive
  binaries patched (FOR-RDOGGETT 45-51; SOURCES "PATCHED"), snake rebuilt
  without stdout unbuffering, RTF's start-up objects in LIB.
- **The browser page** (docs/try) now: runs a card's hidden setup from
  docs/try/setup.json before typing its command (the link names only the
  card); with the OS-9 shell chosen and /h1 attached it `exec shell's and
  types there; names the keys the card typed next.  Cards mark typed text
  in amber; German programs are tinted in the index.
- **Found by reading the program's own source, all corrected:** pri,
  answer, adltouch, rndir, frm, smail, more (it reads its Enter from
  stdin, so it cannot page a pipe), and 16 more INDEX entries.  An INDEX
  line with no source behind it is a guess until checked.

## Needs rdoggett (FOR-RDOGGETT)

1 (merge to main and publish -- his decision; nothing else waits on him).

## Work, in order -- take the top one not done, never ask which

1. **os9exec's final commit**: when it is pushed, freeze CI's
   OS9EXEC_REF to it; if it is not 8d7d870, rebuild docs/try from it and
   run the suite twice and the play-tests again.
2. **Defects still open** (each needs a measurement first): none known.
   nn's `st_gid' is FIXED (2026-09-25): os9lib's stat() leaves it unset,
   so nn would not save twice to its own file for tester; global.c now
   reads the owner from the descriptor (README.OSK).  (ELM `fastmail' is CLEARED,
   2026-09-25: it names the sender with getlogin, not getuid; it needs
   `list' resident, now in SYS/login's list, and a smail whose mailers are
   in /dd/ETC/CMDS -- without them smail retries a minute at a time for
   ten minutes, by design.)  mw's `-1[%dX' is mw sending
   termcap's `ec' without a count -- its bug; the termcap is right.
   `browse' printing the year as 126 is period behaviour and stays.
   mmon is CLEARED (2026-09-25): it wanted its two SysInfo locks and
   logon's path in SYS/mmon.config, and then offers login: on /t1;
   superuser.cases asserts it.
3. **`tools/panel-exceptions.psv`**: re-test the reasons.  The shapes that
   keep recurring: the disk ships what the reason says is missing; nobody
   started the provider; the card filtered the content away; the program
   was given the wrong invocation.
4. **A card's command needs the card's setup** -- docs/try/setup.json
   carries it for the browser.  A card whose hidden setup does something a
   reader could not repeat (staging from /h1, removing a shipped file) is
   worth a second look.
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
