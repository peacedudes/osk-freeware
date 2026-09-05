# Start here, next session

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

## What this session did (2026-09-04), all committed and gate-green

- The tribute voice reached the **captions** (the earlier INDEX/howto pass
  had not): no caption says "not on this disk" any more.
- **The reader's own OS-9 mounts on `/h1`.** `SYS/login` adds `/h1/CMDS` to
  PATH and does a silent `load /h1/CMDS/runb`; the collection stays `/dd`
  (+ hard-link `/h0`). The harness mounts the SDK as `/h1` when `OS9SDK` is
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
