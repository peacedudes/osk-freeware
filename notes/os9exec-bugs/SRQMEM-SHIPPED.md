# The F$SRqMem defect reaches a SHIPPED archive binary, not just our builds

**Found 2026-08-31.** `notes/os9exec-bugs/SRQMEM.md` established that a
cio-linked program can be handed an ADDRESS in D0 where `F$SRqMem` expects a
byte count, and closed with:

> **`-qixm` is the build driver's DEFAULT.** Nothing built by it is installed
> today, so nothing shipped is affected

**That sentence is wrong**, and this file is here to correct it. It conflated
"we have not installed a `-qixm` build" with "no shipped binary goes through
the cio path". 368 shipped binaries are starred, meaning they link cio, and at
least one of them hits the defect.

## The program: `CMDS/logisim`

A logic-circuit simulator from EFFO forum material, archive binary, 11,782
bytes. Nothing of ours: we did not build it and there is no recipe for it.

It needs `PORT` set to a terminal path before it will start at all -- it
reopens the keyboard through it -- and nothing on the disk sets that, which is
why the fault was never seen. Past that check:

    setenv PORT /term
    logisim /dd/DOC/logisim/flipflop.lsi

produces **284 lines of os9exec's own `No more memory !!!` and nothing else**.
The circuit is never drawn. Its two sample circuits ship beside it in
`DOC/logisim`.

## Why this is the SRQMEM defect and not a program that wants too much

`os9exec -d1 0x0042`, logisim is pid 3:

    336  Pid=03  F$SRqMem        <- 335 of them identical
      2          F$SRtMem        <- in the whole trace, both from pid 2

    >>> Pid=03: OS9 F$SRqMem : D0.l=$9D228

`$9D228` is **643,624 bytes**, asked for 335 times and never returned. The
module is 11,782 bytes and declares `M$Mem` = 19,780 and `M$Stack` = 19,456.
It is asking for **thirty-three times its own entire memory requirement**, per
request. That alone is not a size.

**The decisive test is the one SRQMEM.md used -- move the heap and see whether
the "size" moves with it.** That report rebuilt os9exec with a different
`D_BlkSiz`; the same thing can be done from outside by loading modules first,
which shifts where the process lands:

| run | requested "size" |
|---|---|
| logisim alone | `$9D228` |
| after `load cat wc grep` | `$BB228` |

The request moved by `$1E000`, and **the low twelve bits stayed `$228` in both
-- the same object at a shifted base.** A byte count does not move when the
heap moves. An address does. This is the same signature as `$64E48` ->
`$63E48` in SRQMEM.md, reproduced on a binary nobody here compiled.

## What this rules out

- **Not our version skew.** This is the archive's own binary, built by its
  author against its author's runtime. The skew SRQMEM.md describes (we ship
  `csl` edition 16 where the SDK has 25) is about programs WE rebuild.
- **Not a program simply asking for a lot.** 643,624 bytes is not a plausible
  buffer for an 11 KB program, and a plausible buffer does not change size
  because three unrelated modules were loaded first.
- **Not universal to cio programs.** Fed 272,000 bytes on stdin, the starred
  filters `cat`, `detab` and `autolf` each passed all 272,000 bytes through
  with **zero** floods and byte-exact output. Whatever triggers it, sustained
  output alone does not.

## What is still open

Which programs, and why these. The distinguishing feature of logisim seems to
be that it calls `F$SRqMem` repeatedly in a loop where a filter never calls it
at all -- but that is an observation about three programs, not a rule. A sweep
of all 368 starred binaries counting floods is the obvious next measurement
and had not been run when this was written.

## Why it matters for the os9exec release

Before this, the defect could be read as confined to builds the collection
makes with a flag it no longer uses by default. It is not. It is reachable by
software os9exec's users already have, and when it fires the program emits
nothing but the emulator's own error text -- so it looks like a broken
program, not a broken emulator.
