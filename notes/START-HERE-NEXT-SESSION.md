# Start here, next session

## 2026-09-12: seven programs added, 1000 total, 24 commits

Added and carded: **browse** and **uustat** (the two B5 called blocked -- the
scan that "proved" it looked only in `disk/LIB/`, and the library is
`disk/GNULIB/os9lib.l', already on the build path), **almanac**, **zc** with
its 780 KB zipcode table, **cfscores**, **rot22**, **reversi**, **gnugo**.

Fixed, each found by measurement rather than report: `ls' printed a literal
`%s' where the filename belongs (error.c defined variadic error() with fixed
parameters) and had silently blanked two cards whose whole point was showing
a file gone; `infoxpress' published os9exec's own pty announcement as its
entire panel; `xcrypt', `liborder' and `unpacklib.os9' all claimed things
their own captures contradicted; `disk/readme' endorsed leaving the reader's
OS-9 on /dd two lines after saying not to.

Settled: rdoggett's `/h1' shell load (see FOR-RDOGGETT); Q1 (non-commercial
terms) recorded as settled so nobody re-asks; the twenty-four command names
this disk shares with OS-9's own, noted in README-KEEP.

**Assessed and ready to pick up, in order:**

- **scrabble** -- DONE 2026-09-12, commit 9d6aa1e4.  It ships, reads
  GAMES/words and draws its board.  The estimate below was the right shape
  but for the wrong reason; see the next bullet.
- **napoleon** -- IN PROGRESS 2026-09-12.  **The "71 unconditional ANSI
  prototypes, a day" was the wrong measurement**, and the correction is
  worth more than the program.  `ansi2knr' -- the KNR recipe flag -- rewrites
  function DEFINITIONS and never touches DECLARATIONS.  Napoleon has 90
  definitions, which the flag does for nothing, and 69 declarations, 66 of
  them in `adv.h' alone: one scripted edit of one header.  Scrabble was the
  same shape (46 free, 40 by hand).  **Count declarations, not prototypes,
  when sizing an ANSI tree.**  What actually costs time is the things no
  prototype count shows: an ANSI function-pointer struct (scrabble), a
  variadic definition ansi2knr cannot convert (napoleon's `format'), and
  `const'/`signed'/adjacent string literals.  All recorded in
  `tools/rebuild/README.md'.

  Napoleon specifics, all measured: `-DPURE_ANSI' removes the GNU readline
  dependency outright -- the author supplies an fgets-based `readline' behind
  it -- so the missing history library is a non-issue.  `difftime.c' must be
  DROPPED: the SDK's <time.h> defines difftime as a MACRO and the file's own
  definition would be expanded into nonsense.  `vsprintf' comes from
  `../unixlib/vsprintf.c', as bc and fiz already do.  **Generate the parser
  with the DISK's own yacc, not the host's**: macOS `/usr/bin/yacc' is bison
  in disguise and emits a 67 KB skeleton full of `__builtin_alloca',
  <libintl.h> and <stddef.h>; the disk's yacc emits 30 KB with no `const',
  no alloca, no ANSI definitions and no line over 80 characters.
- **TOP's own source trees** (`Scraped/.../os9/top/src/') -- OS-9 ports of
  programs this disk ships as binaries.  Verified 2026-09-12 against
  `src_census.py' (694 of 1003 programs have source here, 69%; 309 do not)
  and against ORIGINS read as entries rather than by substring:

      gawk    gawk2.0      15 .c   10,026 lines   no source here, no ORIGINS row
      bison   bison        19 .c    8,380 lines   no source here, no ORIGINS row
      emacs   emacs_3.10   23 .c   18,135 lines   no source here, no ORIGINS row

  Those three are genuine gaps.  compress, less, rcs, diff and flex are NOT:
  we already have their source, filed by ARCHIVE rather than by program
  (`SRC/hc_utils/compress.c', `SRC/less/less_332/', `SRC/rcs', `SRC/diff',
  `SRC/flex') -- checking `disk/SRC/<program>' finds nothing and is the wrong
  test, which cost me three false findings tonight.  Q2 is rdoggett's call.

  NOTE when sizing any TOP tree: its files are CR-terminated with zero LF, so
  `wc -l' reports 0 for all of them.  Count CRs.

**Left out deliberately, with reasons in PLAN-acquisitions.md:** `flicker'
(an unstoppable ANSI loop), `dumpinit' (six mod_config members this SDK's
<module.h> does not have), `adven2' (Fortran).

**Two build rules learned the hard way:**
- `KNR' ON AN ALREADY-K&R TREE IS HARMFUL.  ansi2knr rewrites parameter
  declarations that are already K&R and c68 then reports `multiple
  definition' on plainly-correct lines.  Symptom is distinctive; the fix is
  to REMOVE the flag.  In `tools/rebuild/README.md' too.
- `build.sh' deletes its temp directory on exit, so a failed build's log is
  gone before you can read it.  Pass `OUT=' and `LOG=' in the environment --
  rebuild.sh honours them and build.sh does not override.


## 2026-09-11: two tracks running

- **Acquisitions plan**: `notes/PLAN-acquisitions.md` (committed b241bfac) --
  eleven batches of software the collection lacks, with verified URLs and
  licence terms, from two deep archive sweeps. Claim a batch by message
  before starting; one session at a time regenerates DEPENDS/CATEGORIES/
  README/docs or rebuilds the image, announced first. Two questions wait on
  rdoggett: non-commercial licences, and GPL source for shipped gcc/dvips.
- **keep is now a real installer** (`notes/keep-installer-2026-09-11.md`): it
  fetches termcap-when-missing and a program's data directories, leaves the
  system directories to your own disk, refcounts shared files, preserves
  scores on re-install (`unkeep -a` clears them), takes every build of a
  name (gcc 1.39 and 2), and unkeep now removes the directories it empties.
  Verified across 440+ programs; three bugs found and fixed in the pass.

## 2026-09-10: the guides, corrected twice by rdoggett, both committed

- **Real OS-9 comes first.** Every reader-facing guide (front page,
  `README.md', `disk/readme', `DOC/README-RUNNING') opens with the real
  system: a disk of its own reached as `/dd' and `/h0', the reader's own
  OS-9 on `/h1', the image written whole or `osk-freeware.tar' unpacked
  with the `tar' module beside it.  os9exec comes second, as the test-drive.
  Never a bare emulator line as the first thing a reader sees.
- **os9exec is named by its variables, never by a link.**  `OS9DISK' and
  `OS9H0' may be the SAME image -- os9exec says `# /h0: using OS9H0=...'
  and mounts it -- so the `ln osk-freeware.dd h0' every guide used to
  teach is gone, along with the claim that the emulator "will not mount
  one path as two devices".  It builds on macOS, Linux, Windows and most
  anything with a C compiler.  RBF images are the preferred format:
  permissions and record locking work as OS-9 expects on an image and not
  on a host directory; `mount -k' makes a blank one.  **The `h0' symlink in
  the repo root is NOT stale and must not be deleted** -- this file said
  "nothing reads it" and that was wrong: rdoggett's `free' alias passes
  `.../osk-freeware/h0' as BOTH OS9DISK and OS9H0, so removing it removed
  his disk and os9exec stopped with `E_MNF: bash' before emulation began.
  Deleted on a sibling session's report 2026-09-12, restored the same night.
  The evidence that would stop you is in `~/.zshrc', not in the tree.
- **One arrangement for running and keeping**: `keep' copies from `/dd'
  onto `/h1'; `unkeep' (was `drop') takes it back.  `DOC/README-KEEP'.
- **Spot-check fixes from rdoggett's own reading of the page.** `zot':
  its styles are ANIMATIONS (letters sliding, bouncing, sorting in, each
  frame a CR-rewrite of one line), invisible under `os9exec -r`, which
  drops the pacing; the card is now a filmstrip via the new sheet
  directive `frames'.  `robots': every score read "your name" because the
  OS-9 port's getlogin() stub in `SRC/rob/os9stuff.c' returned that
  literal; it now reads USER, LOGNAME, then group.user, rebuilt and
  installed, verified against an emptied list ("tester", today's date).
  The shipped 1987 score files are untouched.  Card shows the board in
  play, not the top ten.  `sonnet': the card says what `-l' takes (a poem
  sonnet wrote with `w'; sonnet.out by default).  `oleo' aborts, is
  carded as such, and is on FOR-RDOGGETT's best-forgotten list with piano
  and rstory2 -- recommendation: drop all three; his call.

## Where it stands (2026-09-09, evening): every card carries its own captured help

The second pass `notes/PLAN-recard.md' asked for is done in its mechanical
half and its reading half, category by category, in fourteen commits:

- **The scrape is gone.** `usage_of()' is out of `gen_catalog.py'.
  `tools/help.psv' says, per program, which command asks it for help (or
  `none' with a note), `tools/helpcap.py' runs that at Microware's shell and
  keeps the whole answer in `docs/help/<name>.txt', and the card shows the
  command and the text under **its own help** -- unfolded, on the card,
  not behind the details.  `tools/help-backlog.txt' is the ratchet and it
  is EMPTY: all 935 programs have a line.  The gate `cards carry real help
  text' fails on a missing, stale, hung, empty or cut-off capture, and
  `check_the_checks.py' proves it both ways.
- **The page**: help is its own section after "see it run"; "details and
  provenance" is always open (it was a fold that closed on every shell
  switch).  Both were rdoggett's asks.
- **DOC/INDEX** was read entry by entry with the probe beside it: craft,
  author names and shouting out; the 169 netpbm programs now have one real
  entry each (the columnar block is gone, `from_index' no longer special-
  cases NETPBM); the ADL usage table, the duplicate rxmod/vmod_trap and
  `about' entries and the "Where a few programs live" list are cleaned up.
  `DOC/USAGE' is regenerated from the captures (`helpcap.py --disk disk').
- **Demos recut** where the help section made a `-?' demo redundant: the
  serial-transfer programs (xy, z, k, dld, uld, blastem, xydown, xyt,
  sterm, tterm, connect, uucico) now show what they do without a line.

**Not done, and honest about it:** the cards were read as text dumps, not
rendered in a browser (opening Safari on rdoggett's screen is disruptive).
Open `docs/index.html' and read a few at random -- that is the acceptance
test PLAN-recard names, and it has not been run by eye.

**Traps met today, for the next session:**
- `fix_index.fix' used to match star-grid rows (some names ARE small
  words: `in', `is', `mail') and entries at three spaces or `  *name'; both
  fixed, and it now pads a 16-letter name to two spaces (compress_rebuilt
  had dropped out of the catalogue).  Deleting the rule line after the star
  grid makes the grid parser eat the prose that follows -- keep it.
- **Gate the commit on `check_disk.py`'s EXIT STATUS**, never on `grep -v
  ok` (which succeeds when it finds failures).  One commit went in red that
  way and was fixed in the next.
- At Microware's shell under os9exec, bare `mv' runs the emulator's
  built-in `move'; `load /dd/CMDS/mv' first (help.psv does).  A `chx' away
  from CMDS loses `cio'; `load /dd/CMDS/cio' first (the GCC drivers do).
- A heredoc python patch that asserts halfway leaves NOTHING written;
  check the file after, not the "ok" you expected.

---

## The all-card sweep is DONE (2026-09-09)

Every program card (~900) was reviewed one at a time and carries a `try'
line; the try-line backlog is zero and every `check_disk.py' check is green.
All twenty gallery sheets swept, captions rewritten for a stranger, author
names and ALL-CAPS out of the reader-facing text, captures freshly shot.
The machinery built for it: line-folding is opt-in (`fold'), cards carry a
`try' line (gated) and an `os9' line where Microware's shell differs
(verified by `tools/os9try.py'), draw-once full-screen programs are captured
unthrottled (`burst'), and the web page has a bash / OS-9 shell switch, a
keep preview, more contrast and no capitals.  logisim's label bug was fixed
at its source and rebuilt.  What is left is polish, not sweep: see
`notes/FOR-RDOGGETT.md' (DOC/INDEX de-shouting for four categories whose
agents hit the session limit, and the best-forgotten candidates).

---



Branch `release-pass-2026-08-21`, never pushed. Tree clean, every
`check_disk.py` check green (read the list the tool prints, do not trust a
number), `osk-freeware.dd` current.

**`notes/PLAN.md` is the authority and the work. `CLAUDE.md` has the rules and
is not optional. This file is only the cold start; the rest of `notes/` is
background you do not need first.**

## What 2026-09-05 did (all committed, gate-green)

- **TeX renders.** The sixteen Plain TeX Computer Modern fonts are built at
  300 dpi (virmf/CanonCX) and ship as .pk in SYS/TEX/FONTS/PK300 and .gf in
  SYS/TEX/FONTS. All eleven DVI drivers now render the sample instead of
  zero-size text -- five at 300 dpi, five by nearest-neighbor scaling; only
  dvips cannot, for want of its tex.pro header. README-METAFONT and the
  driver cards are corrected.
- **gnuchess plays the book.** CMDS/gnuchess reads USR/src/chess/gnuchess.book
  (reachable as /h0/...), is first on PATH, and answers 1.e4 with the
  Sicilian. The collision with the GAMES build is accepted; the card shows
  the book move.
- **wysecrack left BROKEN** (moved to CMDS/COMMS -- it probes a Wyse
  terminal, not broken); CMDS/BROKEN is retired.
- **pacman** corrected -- a keypad ASCII maze game, not G-Windows.
- **subber** carried as an exception: it grows its data area with F$Mem, a
  6.5 KB request os9exec's arena cannot grant in place; runs on real OS-9.
- **creadoc** re-explained: a pre-Y2K column shift (2026 prints as `126'),
  not F$PrsNam, and it writes nothing even when the column is right.
- **README-RUNNING** rewritten to the settled /dd + /h0 + /h1 arrangement.
- os9exec fixes that landed and were measured here: MOVE from SR (biory
  draws its chart), F$Mem (per the manual), F$SysID (sysid reports).

## Where it stands (2026-09-05)

Per-program **cards** show each program doing its own job: 814 of 912
runnable programs score "work" or "play"; the rest are honest exceptions
in `tools/panel-exceptions.psv`, each with a reason, and
`tools/panel-backlog.txt` is empty. The gate `panels show their own program`
enforces it. The web page is the three-column layout in `docs/`.

The **tribute voice** governs every reader-facing word (cards, `DOC/INDEX`,
`tools/howto.psv`, the READMEs, the page): lead with what a program IS and how
to run it; name what it uses -- runb, cio, the shell, r68/l68 -- as the
reader's own OS-9, never by its absence ("not on this disk" is banned). The
reader HAS Microware OS-9; os9exec is only the convenience. See the memories
`os9-collection-is-a-tribute` and `os9-card-rules-2026-09-03`.

## What the last session did (2026-09-07), all committed and gate-green

- **Every gallery demo recut to the simple style rdoggett asked for**: the
  visible line is the program and its arguments, and the `cd', the `load'
  and the file staging are hidden before the `clear'.  A reader new to a
  command sees what to type, not a `ksh -c "cd X; ..."' shell-in-a-shell.
  All 55 wrapped cards were done across amusements, archives, calendars,
  documentation, editors, comms, compilers, devtools, encoding, games,
  system and tex -- five commits, each sheet-group its own.
- **screenshots.py now resets the data directory (`builtin cd /dd') at the
  head of every stanza.**  Stanzas in a size-group share a session, so a
  hidden `builtin cd' would otherwise leak into the next stanza; the reset
  is what makes the bare-command style safe.  Verified a no-op for the old
  sheets (an untouched card recaptures byte-identical).
- **Three cards keep their `ksh -c "cd"' wrapper on purpose**, noted in
  FOR-RDOGGETT: `creadoc' (known-broken, needs /h1), `vtxtcn' (leaves the
  session unusable unless run in a subshell), `mkdict' (fragile; and it no
  longer bus-errors, so its caption is stale).
- **gothic runs non-interactively now** (`gothic -h OS-9'), and the config
  for testing the Microware shell is settled: freeware on /dd and /h0, the
  SDK on /h1 (absolute path -- a tilde does not expand into OS9H1).

## What the last session did (2026-09-06), all committed and gate-green

- **Shown-command pathlists swept.** Visible `run' lines across the sheets
  now use short relative names reached by one `chd'/`cd'; captions and
  `try' lines were already clean and gated. What still shows a path in a
  panel is program output, the sanctioned single-`cd' form, or a typed path
  the caption explains (`mv'/`move'/`fc' dodge a ksh built-in; the GCC
  drivers must be pathed). See `notes/FOR-RDOGGETT.md'.
- **Four panels restored** after the sweep: `pgmedge' and `lesskey' re-shot
  in full-sheet context (a partial re-shot had skipped the stanza that
  makes their work directory); `ppmtopj' and `ppmtorgb3' write to files and
  became honest `panel-exceptions.psv' entries beside `vtxtcn', the
  following round-trip/`ls' being their evidence.

## What this session did (2026-09-04), all committed and gate-green

- The tribute voice reached the **captions** (the earlier INDEX/howto pass
  had not): no caption says "not on this disk" any more.
- **The reader's own OS-9 mounts on `/h1`.** `SYS/login` adds `/h1/CMDS` to
  PATH and does a silent `load /h1/CMDS/runb`; the collection stays `/dd`
  (+ `/h0`, the same image). The harness mounts the SDK as `/h1` when `OS9SDK` is
  set. `load` fails gracefully with no `/h1`, so standalone boot is unchanged.
- **`date` removed** -- a broken shadow of Microware's date (it decoded the
  year as 2100). The clock itself is fine: F$Time returns 2026, only that
  442-byte binary misread it. The three entries that cited its 2100 (setime,
  rcsdiff, udate) are corrected.
- **`wysetime` kept** -- it is a BASIC09 clock-setter (`runb wysetime` emits
  a Wyse terminal's clock-set escape sequence), carded. It had been wrongly
  removed as "uncallable"; a packed BASIC09 module IS a type-2 subroutine
  module, exactly like bio, and `runb <name>` runs it.
- **`bio`** kept (F. Kaefer's Biorhythm), verbatim source in `SRC/bio/bio`,
  carded via runb with a typed date. Its "Wrong input!" on RETURN is bio's
  own 1987 `.19` century hardcode, not os9exec.
- **`lua`** works now (the csl edition-25 swap); msntp, basicwin, xengine
  reach honest walls (no network, no X server); runc is the Lua runtime
  engine.
- `TERM=xterm-256color` in login (was mislabelled `vt100`, an alias of the
  same termcap entry).

## What this session did (2026-09-04, evening)

- **os9exec `852dddd` no longer traps MOVE from SR in user state.** `biory`
  draws its chart and its card shows it. `creadoc` runs on to a stop of its
  own (it reads file names from column 53 of `dir -eadu`; this dir prints
  them from 54) -- carded and documented as such.
- **`blackjack` plays** under runb; "error 56 at line 8" was chx off CMDS,
  where runb cannot find the `math` trap handler. Moved out of
  `CMDS/BROKEN` into `CMDS` beside bio and wysetime, carded.
- **The five zip readers have an archive**: `DOC/zip/sample.zip` (unzip's
  own readme and ziprules). unzip, zipinfo, zipnote, zipsplit and funzip
  are carded on it and `archives.cases` asserts the md5s.
- **F$Mem is implemented in os9exec (`7fa2899`)** as the manual describes.
  `subber` grows its data area with it 256 bytes at a time, which succeeds
  only while nothing sits directly above the area: from Microware's shell
  with cio loaded first it substitutes; under bash it is always refused,
  so its card shows the refusal, excepted with the reason. The `#256k`
  route written earlier tonight was layout luck, not the modifier.

## What needs rdoggett -- `notes/FOR-RDOGGETT.md`

- `DOC/README-RUNNING`'s three numbered arrangements still describe the
  pre-`/h1` swap model (its opening is fixed). They want rewriting to lead
  with the `/h1` arrangement -- his call how the setup is framed.
- The branch has never been pushed and nothing is tagged: a release is his.
- "Best forgotten" candidates, re-measured 2026-09-04 evening (blackjack,
  bio and the zip readers came off it), and the remaining os9exec gaps
  (the RCS same-second clock, F$GPrDBT) are listed there.

## The loop, for card and test work

```sh
tools/worklist.py --programs --no-test --no-card    # what still has nothing
tools/drive.py <sheet>                              # run a sheet, read the transcript
tools/audit_panels.py                               # panels that do not show their program

# Capture a card THROUGH THE HARNESS (it shuts down cleanly). A BASIC09 or
# runb-only program needs the SDK on /h1, so set OS9SDK:
OS9SDK=~/Developer/os9/play/oskBoot \
  tools/screenshots.py tools/screenshots/<sheet>.sheet --only <name> --image "$PWD/osk-freeware.dd"

tools/gen_screens.py        # publish captures to docs/screens.js
tools/gen_catalog.py disk   # rebuild the page from INDEX/categories/howto (also DOC/CATEGORIES, README)
```

Build and gate (gate EVERY commit on check_disk being green):

```sh
rm -f disk/.DS_Store        # macOS recreates it; packed, it fails the build
OS9EXEC_DIR=~/Developer/os9/os9exec tools/mkimage.sh disk osk-freeware.dd
tools/check_disk.py disk
```

## Gotchas that cost time this session

- **`disk/.DS_Store` recurs** (macOS) and breaks the build as an extra
  packed file. `rm -f disk/.DS_Store` right before mkimage and before every
  commit.
- **Capture through `tools/screenshots.py`, never an ad-hoc gtimeout-wrapped
  pty loop.** A gtimeout that kills a hung pty-driven os9exec leaves an
  orphan process you cannot clean (killing is gated). The harness lands
  softly; confirm `pgrep os9exec` is 0 afterwards.
- **`runb` and the reader's Microware tools are on `/h1`** (the SDK), not on
  the disk. `bio`, `wysetime` and `blackjack` are BASIC09: `load /h1/CMDS/runb`
  then `runb <name>`. Under Microware's own shell the bare name auto-runbs;
  under the collection's bash it does not (bash says "cannot execute binary
  file").

## If you remember four things

1. OS-9 text is CR-terminated (0x0D), never LF -- `check_disk` catches LF.
2. Measure, do not infer -- every proxy tried here has been wrong both ways.
3. Make every check fail once before believing it.
4. A program that looks broken usually has the wrong invocation.

## Where the answers live

| Question | File |
|---|---|
| What to do next / the whole picture | `notes/PLAN.md` |
| The rules | `CLAUDE.md` |
| What each program is / does it work | `disk/DOC/INDEX`, `disk/DOC/STATUS` |
| How to run it | `tools/howto.psv` |
| What it needs besides its binary | `disk/DOC/DEPENDS` |
| Where it came from, on what terms | `disk/DOC/ORIGINS`, `disk/SOURCES.txt` |
| Which panels are not worth showing, and why | `tools/panel-exceptions.psv` |
| What needs rdoggett | `notes/FOR-RDOGGETT.md` |
| Why it is like this | `notes/HISTORY-2026-08.md` |

## Outstanding: 20 captures no longer match their stanza (2026-09-12)

Measured with the project's own `screenshots.stanza_hash', not a proxy:

    comms.sheet   bdecode c7decode dbz dotilde fastmail filter fixtext
                  input lcasep listalias makedb nptx pathalias read_mail
                  rnews uux wn
    games.sheet   vtxtcn
    maths.sheet   oleo
    played.sheet  tess

Nothing is missing a capture; these twenty have had their caption or their
commands edited since the shot was taken, so each publishes an OLD screen
under a NEW caption.  Re-shoot with `tools/screenshots.py <sheet> --only
<names>'.

**Do not reach for mtime or git log to second-guess this.**  The check is a
content hash of the stanza; the tool's message used to say "OLDER than the
sheet that defines them", which sent me to compare file mtimes -- a sheet
touched to add ONE stanza then looks like it invalidated every stanza in it,
and a naive mtime sweep across all sheets reports 836 stale out of 900.  The
message is fixed to say what it compares.
