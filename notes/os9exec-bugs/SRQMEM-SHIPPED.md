> **SUPERSEDED 2026-08-31, and the attribution in it was wrong.** The root
> cause is an ABI mismatch, not an os9exec defect: the archives were linked
> against a `cio.l` whose stub table ends `$41 _flshbuf, $42 _filbuf`, while
> every `cio` MODULE on these disks has five memory routines at `$41..$45`
> instead. Selector `$41` therefore lands on the raw allocator, which reads
> `d0` -- holding the `FILE *` the program passed -- as a byte count. That is
> why the "size" tracks the heap: it is an address, but the PROGRAM put it
> there on purpose. os9exec passes `d0` through untouched and `F$SRqMem`
> honours its contract.
>
> Found by the os9exec session, which disassembled both sides. See
> `CIO-SELECTOR-MISMATCH.md`. What survives from this file is the evidence
> that shipped archive binaries are affected, and the two reproductions.
> What does not survive is the claim that os9exec is at fault, and the
> section about `sed` -- see below.

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

## A second one, and it is worse: `CMDS/cvtbase`

Also an archive binary. Invoked exactly as its own usage line says --
`cvtbase <input base> <output base>`, with a number on standard input:

    echo 255 | cvtbase d h

**439,689 lines of `No more memory !!!`**, and no conversion. Same on a pipe
and on a pseudo-terminal. The heap-shift test again:

| run | most-repeated request |
|---|---|
| `cvtbase d h` alone | 297,504 bytes (`$48A20`), 300 times |
| the same after `load cat wc grep` | 617,952 bytes (`$96DE0`), 203 times |

The "size" did not merely shift -- it doubled, because the layout changed.
Nothing that is a byte count behaves like that.

**This was already written down and not connected to the defect.** DOC/INDEX
has carried "and then FLOODS `No more memory !!!' without converting anything"
for cvtbase since 2026-08-29, and the same for `lfmaker`, while SRQMEM.md said
nothing shipped was affected. Two documents in one repository disagreeing, and
the one with the reproduction was the one that was wrong.

## The `sed` swap stands -- I got this wrong

This section used to argue that `CMDS/sed`, swapped on 2026-08-28 because it
"answered every script ... with `No more memory !!!'", had been retired to work
around an emulator fault and that the collection was a program poorer for it.

**That was built on the wrong attribution and is withdrawn.** With the `cio`
module this disk ships, that build genuinely cannot run: the mismatch is real
and is in the binary's own linkage, not in the runtime under it. The swap was
correct. Only the REASON recorded for it needs correcting, from "os9exec
memory storm" to "linked against a cio.l whose module is on none of these
disks".

## The population, measured

**Counting floods does not find these.** All 368 starred binaries were run with
272,000 bytes on standard input: **zero** flooded, and 72 passed more than
200 KB through cleanly (`ckermit` moved 794 KB). That is a real negative for
filters -- but it is not a clean bill of health, because 221 of the 368
produced under 200 bytes, so the probe never exercised them. Neither logisim
nor cvtbase is caught by it: neither reads stdin that way.

What the two confirmed cases have in common is that they call `F$SRqMem`
repeatedly from their own loop, where a filter never calls it at all. A trace
sweep looking for an address-shaped request directly -- rather than waiting for
the arena to exhaust -- is the measurement that would find the rest, and is the
right next step.

## What is still open

Whether `lfmaker` is a third. DOC/INDEX says it "FLOODS `No more memory !!!'
as soon as it is given an argument", measured 2026-08-29; run here as
`lfmaker foo` and bare it produced no output and made no `F$SRqMem` call at
all. Either the entry needs a condition it does not state, or it is wrong.

## What it means for the os9exec release

Not what this file first claimed. The mismatch is the archives', and no
os9exec change fixes it. One small os9exec item is real and worth having:
`memstuff.c:782` prints `No more memory !!!` to the console unconditionally on
every failed allocation, where real OS-9 returns `E$NORAM` silently. That is
why an ABI mismatch in a program reads as an emulator failure -- it is the
emulator's voice on the program's stdout. It cost this collection a program's
reputation, and a night of mine.
