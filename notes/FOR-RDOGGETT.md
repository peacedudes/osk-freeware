# For rdoggett

Only what is waiting on a decision of yours. Everything done, and why, is in
git history and `notes/START-HERE-NEXT-SESSION.md`; this file carries none
of it. Updated 2026-09-04.

## Content decisions

1. **`DOC/README-RUNNING`'s three numbered arrangements** still describe
   the old swap model (your OS-9 on `/dd`, the collection on `/h0`). Login
   now assumes the collection on `/dd` (hard-linked `/h0`) and your system
   on `/h1`. How the setup is framed for the reader is your call; say the
   shape and I write it.

2. **`CMDS/BROKEN` holds one program, `wysecrack`, and it is not broken** --
   it waits for a Wyse terminal to answer. Drop the directory and move
   wysecrack to `CMDS/COMMS`, or keep BROKEN for it?

3. **`CMDS/gnuchess`, open since 2026-08-31.** It collides by module name
   with `CMDS/GAMES/gnuchess`, wants its book at `/h0/usr/src/chess/`, and
   prints nothing; the GAMES build plays. Drop it, or keep it renamed
   (`gnuchess_h0` is the only name that says what distinguishes it)?

4. **Programs that may be best forgotten.** Each is measured and carded
   honestly; removing one is yours to decide:
   - `pacman` -- G-Windows; draws nothing at a terminal.
   - `rstory2` -- forks four story programs that never shipped with it.
   - `dearc` -- reads MS-DOS ARC files; nothing here writes one. Could be
     given a sample the way the zip readers were, if you want it kept.
   - `splitalf` -- writes `<name>_0` and stops, whatever it is given.
   - `cuts -e` -- the encoder asks for gigabytes; `-d` decodes fine.
   - `game`, `postprint` -- want the `chess.lst` gnuchess writes on `list`;
     not re-measured, an evening's work rather than a removal.
   - Duplicates, one decision each: `puz15`/`puzzle15` (one program built
     twice), five GNU Chess builds, `wc.cio`.

5. **TeX bitmap fonts.** `tex`, `latex` and the DVI drivers run, and
   `dvialw` writes PostScript gs403 can rasterise, so the typeset sample
   could be shown on a card. `SYS/TEX/FONTS/PK300` has no fonts, so every
   driver sets the text at zero size. Metafont here renders cmr10, cmbx10
   and cmsl10 at 300 dpi in a few minutes each. Ship those three `.pk`
   files (a few hundred KB)?

6. **`hex`** sits in `cowen_tools.lzh`, the archive `delbak`, `l` and
   `owner` came from -- 1,916 bytes, C source included. `dump` is already
   the hex dump here. Add it, or note in ORIGINS that it was seen and
   passed over?

## Yours because the repos are yours

7. **os9exec.** Three things still stop cards:
   - `F$GPrDBT` (0x1f) and `F$GPrDsc` (0x18) take a bus error instead of a
     refusal; `devprc -a`, `top` and `sysmon` reach them.
   - The allocator's `# No more memory ...` line goes to the console,
     which is the program's stdout, so it lands on a card (subber's).
     Real OS-9 refuses silently.

8. **The `os9-dev` skill** (`~/Developer/os9/os9-dev-skill`), three gaps in
   `references/common/using-os9exec-repl.md`, written up in git history
   (2026-09-01 entry of this file): the cio selector mismatch is absent; "a
   usage message is a pass" is unsafe for that class; a bare relative
   `OS9Hx` path breaks file opens while module loading works. Say the word.

## Release

9. The branch has never been pushed and nothing is tagged. Before that:
   the CI pin in `.github/workflows/build-image.yml` is an old os9exec
   commit and has never run for real. I can bump it and run the workflow
   locally; the push, the tag and the merge to main are yours.
