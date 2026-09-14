# NEG and NBCD never set X -- Microware's double arithmetic came out wrong

**Genuine os9exec defect, fixed** on os9exec branch `fix/scf-pd-eor`,
`209b35c` (core) and `d819c40` (regression test), 2026-09-14. Not pushed.
Found porting perl 4.036, whose `<=>` never answered 0 for equal numbers.

## What was wrong

On the 68000, `NEG`, `SUB`/`SUBI`/`SUBQ` and `NBCD` leave X equal to C.
In `cpuemu.c` every `NEG` and `NBCD` handler, and 120 `SUB`-family
handlers in the 68000 and 68010 tables, set C and never copied it into X.
os9exec runs the 68020 table, whose `SUB` handlers were right, so in
practice the bug was `NEG` and `NBCD`.

Microware's software doubles (`_T$DAdd`/`_T$DSub` in `math.l`, and the same
code in the `math` module) form a two's-complement 64-bit mantissa as
`neg.l` of the low word then `negx.l` of the high word. A stale X made the
high word borrow when the low word was zero. That is one unit in the lowest
mantissa bit of the high longword, exactly what was measured.

## Measured before the fix (`fsub.c`, built `-qm`)

    1-1     beb00000 00000000     -2^-20, not 0
    3-3     bec00000 00000000     -2^-19
    2-1     3feffffe 00000000     0.99999...
    2.5-.5  3fffffff 80000000     1.99999...
    exp(1)  2.7182831246371366    host 2.718281828459045
    %.15g of 0.1 printed 0.100000000046566

After: every sum and difference exact, `exp`/`log`/`sin`/`pow` agree with
the host to 15-16 digits, and 0.1 prints as 0.1. os9exec `make test`
237/0 and `make conformance` 58/58 after the change.

**What it means for the collection:** any program doing double arithmetic
ran slightly wrong under os9exec, archive binaries included. Figures
captured from such programs before the fix (cards, datatests, notes about
"Microware's pow is imprecise") are suspect. The math library was never
at fault.

## Reproductions

- `fsub.c`: prints differences as raw bytes. Build it with the rebuild
  driver (`fsub|fsub|fsub.c|||`).
- `xflgtst.a`: hand-written assembly. Each case sets X to the opposite of
  what the instruction must leave and reads it back with `addx.l d0,d0`.
  Assemble on the SDK disk with `r68` and `l68`. On the parent commit four of
  its seven cases fail: NEG.L/NEGX.L, NEG.L, NEG.B and NBCD.
