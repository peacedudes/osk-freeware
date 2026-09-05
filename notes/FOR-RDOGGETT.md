# For rdoggett

Only what is waiting on a decision of yours. Everything done, and why, is in
git history and `notes/START-HERE-NEXT-SESSION.md`; this file carries none
of it. Updated 2026-09-05.

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
     silently. (subber is now carried as an exception rather than a card.)
   - `creadoc` writes nothing even when its dir-column year is two digits.
     Its first stop (the `126' year shifting the filename) is a pre-Y2K
     program, not os9exec; the second stop is unidentified and may be
     either side.

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
