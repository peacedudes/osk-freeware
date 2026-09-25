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
- **Emulator: os9exec `289d55e`** (fix/scf-pd-eor) is the checkpoint last
  verified -- suite 1017/1017 twice on 2026-09-25 (after the list and
  mmon changes; nn's fix after it was checked by its own families),
  play-tests 151/151 on 2026-09-24, as tester on a fresh image.  docs/try runs it.  The os9exec
  release commit is still to come (CPU/FPU review, console restructure):
  when it is named, pin it, rebuild docs/try from it (tools/wasm-web.sh in
  a `git archive' export; keep our page's own edits), and re-run.
  `lesspipe' needs 2a95c75 or later; mmon's cases need 289d55e or later.
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

1 (push os9exec and name its release commit) and 52 (patch the 1991
collect2 binaries, or leave them with the note their cards now carry).

## Work, in order -- take the top one not done, never ask which

1. **os9exec's release commit**: when the os9exec session names it, pin it,
   rebuild docs/try, run the suite twice and the play-tests as tester, and
   drive pagers and pipelines on a real terminal (tools/playtests/lesspipe).
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
