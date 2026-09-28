# Start here, next session

One page.  The plan is `notes/PLAN.md`; what needs rdoggett is
`notes/FOR-RDOGGETT.md`; everything that happened before 2026-09-24 is in
`notes/HISTORY-2026-08.md` and `notes/HISTORY-2026-09.md`.  Keep this file
to a page: a finding goes in the file it belongs to, and a finished
session's narrative goes into the history file, not here.

## Resuming after a reboot (2026-09-27)

The tree is clean and pushed (branch release-pass-2026-08-21).  The
session scratchpad under /private/tmp is gone after a reboot; rebuild what
you need from it:

- **The emulator the suite runs on**, os9exec a1d433e (tip 1318f5b only
  adds a test):
      mkdir -p $SCR/pa1/src
      (cd ~/Developer/os9/os9exec && git archive a1d433e) | tar -x -C $SCR/pa1/src
      (cd $SCR/pa1/src && make OBJDIR=$SCR/pa1/obj EXE=$SCR/pa1/os9exec prod)
  Harness runs: `export OS9SDK=~/Developer/os9/play/oskBoot OS9EXEC=$SCR/pa1/os9exec`,
  images with `SKIP_CHECKS=1 OS9EXEC_DIR=$SCR/pa1 tools/mkimage.sh disk <img>`.
- **Rebuilding programs** (tools/rebuild/rebuild.sh) used OS9EXEC=an os9exec
  built the same way from d992145, and OS9CLEAN=the overlay that
  tools/rebuild/make_overlay.sh makes.
- **The commit gate** was a scratch script: run `python3 tools/check_disk.py
  disk`, commit only on exit 0, stage only the paths the change is about.
- **The browser page**: docs/try/os9exec.{js,wasm} are a1d433e's
  (tools/wasm-web.sh in its tree, run on osk-freeware.dd with
  `bash /dd/SYS/login`).  docs/try/disk.gz is gitignored; CI makes it, and
  locally `gzip -9 -c osk-freeware.dd > docs/try/disk.gz`.  To look at it:
  `cd docs && python3 -m http.server 8765`, then http://localhost:8765/.

Open, in order: rdoggett's Safari check of a card's `man <name>' panel
(docs/try `?man=<name>&embed=1'; never tried in a real browser); then the
work list below.  Nothing is half-done.

## Where it stands, 2026-09-27

- **Every program on the image has a card taken by running it**, and
  `tools/check_disk.py disk` is the gate -- read its list, not a count.
- **Harnesses run as `tester`**, not the super-user.  A data-test family
  that needs the super-user says `user su`; a card stanza says `super`; a
  play-test says `user su`.  Play-tests mount no /h1.
- **Emulator: os9exec `a1d433e`** (branch release-v4.1.0, pushed
  2026-09-26): pipe progress per reader, an orphan's exit no longer ends
  the emulator, and one image named as /dd and /h0 is one RBF device.
  Verified 2026-09-27, built from `git archive a1d433e`, fresh image, as
  tester: suite 1048/1048 twice, play-tests 156/156; after the man and
  documentation work, 1057/1057 (man.cases added).  check_the_checks 43/43.  docs/try runs it.
  CI tracks the branch; freeze OS9EXEC_REF to os9exec's merge commit when
  it sends one.
- **CI has run** (first time, 2026-09-26, manual run on this branch):
  green end to end on Linux -- gate, catalogue, os9exec from
  release-v4.1.0, image built and read back.  Its first runs found three
  things this Mac hides: captures are gitignored (the gate now skips that
  check in a fresh clone), directory walks were unsorted (DEPENDS came out
  in another order), and `Info_help' matched `info_help' only on a
  case-insensitive disk.  Release and Pages steps run only on main or a
  tag.
- **2026-09-26: an editor's pass over every card.**  Four fresh reviewers
  read all 1108 cards as a publisher would (910 findings, 129 HIGH); six
  agents fixed them sheet by sheet, and their changes to shared files came
  back as proposals applied centrally.  About 80 programs that borrowed a
  sibling's screen have cards of their own; 80 screens cut off at the top
  were found by re-shooting in an 80-row window.  The superuser is `root';
  super-user cards say so.  The renderer knows MM/1 colour codes, VT52
  cursor codes, a Datamedia 1520 (`term dm1520') and C0 bytes inside a CSI;
  a stanza can publish several screens (`pages', dm's help).  SYS/motd and
  the welcome letter no longer talk about an emulator.  The review tooling
  is scratch-only: review bundles, apply.py and apply_index.py.
- **2026-09-27: `man' is the librarian.**  `man <name>' reads everything
  the disk has about a program (DOC/DOCS), `man -k' searches what programs
  do (DOC/WHATIS), `-f', `-w', `-s' (source); both files come from
  tools/gen_docmap.py and the gate checks them.  Each card lists its
  documents and has a `man <name>' button that boots the disk in a panel
  and runs it (docs/try `?man=<name>&embed=1', entered by the page, name
  held to [\w.+-]).  The panel is NOT yet tested in a browser.  23
  programs fixed on 2026-09-26 (SOURCES.txt, changes.psv); three byte
  patches wait on rdoggett (FOR-RDOGGETT 2).
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

1. **The reader-facing rewrite** (rdoggett, 2026-09-27), by the rules in
   memory `os9-write-like-a-librarian'.  DONE 2026-09-27: README.md,
   disk/readme, the catalogue intro and blurbs, README-DOCS, README-RUNNING,
   README-KEEP, START-HERE, STATUS' opening, the seven choosers and the
   other fifteen README-* guides, and DOC/STATUS whole (one entry a
   program, every failure claim re-run; KEY_DOCS floor now 15000), and
   DOC/INDEX's 190 longest entries (tools/fix_index.py).  Done unless a
   reader-facing file turns up that was missed.
2. **ksh DONE 2026-09-27**: rebuilt from SRC/pdksh, trap-free (no cio),
   `read' fixed (second loop over a file; runs of spaces).  Suite 1067/1067
   twice and play-tests 156/156 on it.  SRC/pdksh/README.OSK; ksh.cases.
   The driver faults it found are fixed (fe09d496): a .a source's object
   is x.r, and the verdict counts every object the merge list names.
3. **Defects still open** (each needs a measurement first): none known.
   nn's `st_gid' is FIXED (2026-09-25): os9lib's stat() leaves it unset,
   so nn would not save twice to its own file for tester; global.c now
   reads the owner from the descriptor (README.OSK).  (ELM `fastmail' is CLEARED,
   2026-09-25: it names the sender with getlogin, not getuid; it needs
   `list' resident, now in SYS/login's list, and a smail whose mailers are
   in /dd/ETC/CMDS -- without them smail retries a minute at a time for
   ten minutes, by design.)  mw's `-1[%dX' is mw sending
   termcap's `ec' without a count -- its bug; the termcap is right.
   `browse' printing the year as 126 is period behaviour and stays.
   DONE 2026-09-28: the cio mismatch reaches $43 (fputc) and $44 (fgetc)
   too -- read off LIB/cio.l's C$ equates, measured on the archive cuts
   (30 MB from 24 bytes).  cio_macro_scan.py counts all four; nothing
   shipped calls $43/$44 (cuts was rebuilt -qm on 2026-09-26); README-CIO
   says so.
   Reported to os9exec 2026-09-26, their call: the pipe byte counter shared
   by readers (ppmtopict | wc), an orphan's F$Exit ending the emulator
   (vcron), and one image as /dd and /h0 being two RBF instances.
   mmon is CLEARED (2026-09-25): it wanted its two SysInfo locks and
   logon's path in SYS/mmon.config, and then offers login: on /t1;
   superuser.cases asserts it.
4. **`tools/panel-exceptions.psv`**: re-test the reasons.  The shapes that
   keep recurring: the disk ships what the reason says is missing; nobody
   started the provider; the card filtered the content away; the program
   was given the wrong invocation.
5. **A card's command needs the card's setup** -- docs/try/setup.json
   carries it for the browser.  A card whose hidden setup does something a
   reader could not repeat (staging from /h1, removing a shipped file) is
   worth a second look.
6. **Housekeeping** (PLAN section 5): notes stay small.

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
