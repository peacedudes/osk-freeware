# snake draws corrupt escape sequences -- what is ruled OUT, 2026-08-27

rdoggett: *"snake is still dead to me. It is not because of echo."* He is
right. This is what the evidence says, so nobody repeats the eliminations.

## The symptom

Cursor-positioning sequences arrive with the ESC missing, so the terminal
prints the rest as text and the board fills with things like `[10;25H'.

    -----------------------------------------[10;25H<ESC><ESC>[C I
                                              ^^^^^^^^^ no ESC
                                                        ^^^^^^ two ESCs

## THE ESCs ARE MISPLACED, NOT LOST

Counted over one capture:

    total ESC bytes        38
    ESC[ sequences         29
    orphaned [n;nX          7
    ESC ESC pairs           6

29 + 7 = 36, and the two extra ESCs are the legitimate `ESC=' in the `ks'
capability. Every sequence still owns an ESC somewhere; it has simply landed
about eight bytes late. This is a REORDERING, not a dropped byte, and that
rules out anything that would lose data.

## Ruled out, each by measurement

  - **NOT echo.** Turning echo off with `_gs_opt'/`_ss_opt' removes the
    echoed characters from the board (5 to 0) and leaves the orphan count
    unchanged at 17.
  - **NOT os9exec's baud pacing.** An escape-emitting probe is clean with and
    without `-r': 301 sequences intact, 0 orphaned, both ways.
  - **NOT concurrent read and write.** A probe that polls `_gs_rdy' and reads
    keys WHILE writing cursor moves is clean, with and without keystrokes.
  - **NOT the terminal path at all.** Redirect snake's output to a FILE --
    no tty, no SCF echo, no pty -- and the corruption is still there, 7
    orphans among 29 sequences. This is the strongest single result: whatever
    is wrong happens before the bytes leave the program.
  - **NOT termlib.** Captured what `tputs' actually emits:

        cm capability   1b 5b 25 69 25 64 3b 25 64 48   ESC [ %i %d ; %d H
        tgoto(CM,25,10) 1b 5b 31 31 3b 32 36 48         ESC [ 1 1 ; 2 6 H
        tputs emitted   1b 5b 31 31 3b 32 36 48         identical

  - **NOT the C library or the emulator's stdio.** `pcprobe' writes 200
    cursor sequences one character at a time through `putchar', exactly the
    way snake's `outch' does, interleaved with 70-character border runs and
    periodic `fflush' -- 16090 bytes, 401 sequences, **0 orphaned, 0 doubled**.
  - **NOT something we introduced.** The ARCHIVE binary shows it too.

## Where to look next

It is in snake's own code. Two candidates, neither confirmed:

  1. ~~`pstring()' dropping escapes.~~ **TESTED AND IT IS NOT THE CAUSE.**
     `pstring' in move.c really does discard every byte below space
     (`if (s[0] < ' ') break;'), and letting ESC through instead recovered
     five sequences in a typical run -- ESC bytes went 38 to 43, `ESC['
     29 to 34. **The orphan count did not move: 7 before, 7 after**, and the
     `ESC ESC' pairs stayed at 6. So pstring silently swallows some escapes,
     which is a real if minor defect, and it is NOT what corrupts the board.
     The experiment was reverted; a change that does not fix the reported
     problem should not ship.
  2. `static char str[80]' in move.c is shared by `__printf' and `a__printf'
     via `sprintf', with no bound. An overflow would corrupt the statics
     beside it.

## Separately: an intermittent startup hang, also pre-existing

About one run in eight snake emits its keypad-init string and stops before
drawing anything -- 289 bytes instead of ~780. Measured on the ARCHIVE
binary: 18 of 20 drew with keys, 17 of 20 without, so keystrokes are not the
trigger. Do not conclude anything here from fewer than twenty runs; a
six-run sample said 6/6 against 4/6 and sent one session down a wrong path.
