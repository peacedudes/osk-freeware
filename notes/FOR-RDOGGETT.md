# For rdoggett

Only what is waiting on a decision of yours. Everything done, and why, is in
git history and `notes/START-HERE-NEXT-SESSION.md`; this file carries none
of it. Updated 2026-09-05.

## Full pathlists on cards -- captions ruled, shown commands remain

The rule is made and enforced: `check_disk.py`'s `cards carry no full
pathlists' fails the build on any `/dd/...`, `/h0/...` or `/h1/...` in a
card's caption or `try' line, and check_the_checks records the by-hand
proof.  The ten caption lines that still named absolute paths are reworded.

**What is left: the shown COMMANDS.** 180 of 907 captures still echo a
full path in the command line itself -- `arc a m.arc /dd/SYS/motd', not
`arc a m.arc motd' -- because their sheet `run' line uses full paths.  Each
one is a stanza reworked to `chd' into a short work directory with
short-named files, then re-shot (the subber card is the model).  It is a
few hours of captures, so I have not swept it blind; say the word and I run
it down, or I chip at it whenever a card is touched anyway.  I did not put
an automated check on the shown commands: telling a real command-path from
a legitimate one (the `about' card deliberately shows `hack's full path,
because its name collides) needs judgement a regex would get wrong.

## The gallery, recast for a browser (2026-09-05)

Done, per your science-fair steer -- the program panel (docs/index.html, from
tools/catalog.template.html) now leads with what it does, a **Try it**
command (short, no pathlists), **See it run** (the capture, moved up), and
**Needs** (only real requirements -- data files and directories from
DEPENDS, and runb for a BASIC09 program). Version, author, provenance, its
own help and see-also are folded into a collapsed Details section. cio is
de-emphasised as you asked: the star on every cio program, the "uses cio"
flag and the "Runs without cio" filter are gone -- the modules ship, so it
is a non-event. A new `try' sheet directive gives a card its command;
without one the card shows the bare program name, which is what you type for
most. The format is documented in tools/screenshots.py's sheet-format help.

**What is left on this, for a later pass, not a blocker:** the per-card
"what it does" line. Sampled, most are already clean one-liners; a minority
still carry how-it-was-got-working prose. It is a category-by-category
editing pass, not a redesign. Authoring `try' for the arg-needing cards
(most just take their name) is the same kind of incremental work.

## Content decisions

1. **Programs that may be best forgotten.** Each is measured and carded
   honestly; removing one is yours to decide. Since the last pass:
   - `pacman` -- a keypad ASCII maze game (not G-Windows, as I had wrongly
     said); it draws in raw keyboard mode. Kept.
   - `rstory2` -- forks four story programs that never shipped with it.
   - `dearc` -- reads MS-DOS ARC files; nothing here writes one. It could
     be given a sample the way the zip readers were, if you want it kept.
   - `splitalf` -- writes `<name>_0` and stops, whatever it is given.
   - `cuts -e` -- the encoder asks for gigabytes; `-d` decodes fine.
   - `game`, `postprint` -- want the `chess.lst` gnuchess writes on `list`,
     which the checkgame card already produces; not re-measured, an
     evening's work rather than a removal.
   - `puz15` and `puzzle15` are NOT duplicates -- two different programs,
     each with its own source (`SRC/v_misc/puz15.c`, `SRC/eff_puzzle15`).
     Both stay. The five GNU Chess builds and `wc.cio` are the real
     duplicate question, one decision each.

## Yours because the repos are yours

2. **os9exec.** What still stops a card, now that MOVE SR, F$Mem and
   F$SysID are fixed:
   - `F$GPrDBT` (0x1f) and `F$GPrDsc` (0x18) take a bus error instead of a
     refusal; `devprc -a`, `top` and `sysmon` reach them. You said os9exec
     is being worked on for these.
   - The allocator's `# No more memory ...` line goes to the console, which
     is the program's stdout, so it can land on a card. Real OS-9 refuses
     silently. (subber now has a working card -- `#1000k' pre-sizes its
     data area so it never asks os9exec to grow one.)
   - `creadoc` is an early Fortran documentation extractor (it pulls the
     `C++ ... C--' header block out of a `.f' source into creadoc.txt, a
     1988 forerunner of javadoc) and is worth keeping as that. It does not
     run here: it reads the file name from column 53 of a `dir -eadu'
     listing, and this disk's dir puts it at 54 (the 2026 date, printed
     `126', pushes it further) -- so it opens a space-prefixed name and
     stops. A dir-column brittleness (its fnpos=53 vs this dir's 54), one
     constant in SRC/rtf/creadoc.f. Rebuilding it means the RTF Fortran
     chain plus Microware's r68/l68 on /h1, and it edits an archived
     binary. I'd keep it as interesting historical software, documented,
     with DOC/rtf/biory.doc as the example of its output; rebuild only if
     you want it runnable. Your call.

3. **The `os9-dev` skill** (`~/Developer/os9/os9-dev-skill`), three gaps in
   `references/common/using-os9exec-repl.md`, written up in git history
   (2026-09-01 entry of this file): the cio selector mismatch is absent; "a
   usage message is a pass" is unsafe for that class; a bare relative
   `OS9Hx` path breaks file opens while module loading works. Say the word
   and I write them in.

## Release

4. The branch has never been pushed and nothing is tagged. Before that:
   the CI pin in `.github/workflows/build-image.yml` is an old os9exec
   commit and has never run for real. I can bump it and run the workflow
   locally; the push, the tag and the merge to main are yours.
