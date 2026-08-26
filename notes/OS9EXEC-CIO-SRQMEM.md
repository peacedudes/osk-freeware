# A cio-linked program asks F$SRqMem for a POINTER-sized block, once per
# character, until the arena is gone

**Found 2026-08-26, chasing why `card` crashed.** This is an os9exec-side
finding, not a collection one, and it is the reason `card` was the only
program that needed `TRAPFREE`.

rdoggett's question was the right one: *"I do not understand why some program
can crash if built with cio but not crash without it."* The answer is that the
cio build is the only one that goes through os9exec's trap-handler path, and
something on that path is handing `F$SRqMem` a pointer where a byte count
belongs.

## Reproduction -- twelve lines, deterministic

`notes/cio-srqmem/putchar.c`:

    #include <stdio.h>
    main()
    {
        int i;
        for (i = 0; i < 4000; i++)
            putchar('x');
        fprintf(stderr, "\nSURVIVED 4000 putchar\n");
        exit(0);
    }

Built two ways against the same SDK overlay:

    cc pc.c -qixm=16k -DOSK -n=pcio -f=R_pcio          <- cio trap handler
    cc pc.c -qm=16k   -DOSK -n=pcm  -f=R_pcm  ...      <- stdio linked in

Run under os9exec with this collection as `/dd`:

| build | x's written | os9exec "No more memory !!!" | verdict |
|---|---|---|---|
| `-qixm` (cio) | **2** | **3920** | broken |
| `-qm` | 4002 | 0 | correct |

Not a size problem: `-qixm=4k`, `=16k` and `=64k` behave identically, to the
same counts.

## What the trace says

`os9exec -d1 0x0042` (memory + syscalls). The whole of what pid 3 does:

    4001  F$SRqMem      <- one per putchar, plus one
       3  I$Close
       2  I$WritLn      <- the only two characters that ever left
       1  I$GetStt
       1  F$TLink       <- linking cio
       1  F$SRtMem
       1  F$SetSys
       1  F$Exit

and every one of those requests is the same:

    >>> Pid=03: OS9 F$SetSys : D0.w=$007C D1.l=$80000004 D2.l=$64E1E
    <<< Pid=03: OS9 F$SetSys returns: D2.l=$800
    >>> Pid=03: OS9 F$SRqMem : D0.l=$64E48
    # get_mem: allocate block at 0x748046edc0 (size=413312)   582400
    <<< Pid=03: OS9 F$SRqMem returns: D0.l=$64E50 A2=$70BC0
    >>> Pid=03: OS9 F$SRqMem : D0.l=$64E48
    # get_mem: allocate block at 0x7480470bc0 (size=413312)   995712
    ...

`$64E48` is **413,256 bytes**. Nothing frees any of it -- the running total
climbs monotonically past 10 MB until the 32 MB arena is exhausted, and from
then on every putchar prints os9exec's own `No more memory !!!`
(`Source/OS9exec_core/memstuff.c:782`) into the program's output.

## What is proven, and what is not

**Proven.** The reproduction, the counts, the monotonic growth, and that
`F$SRqMem` itself is innocent: `OS9_F_SRqMem` in `fcalls.c` implements the
documented contract exactly (d0.l in = size, d0.l out = actual, a2 = block).
It is the REQUEST that is absurd, not the service.

**PROVEN 2026-08-26, by moving the memory layout underneath it.** D0 at
`F$SRqMem` is carrying an ADDRESS, not a byte count. Rebuild os9exec with
`OS9MINSYSALLOC` (the `D_BlkSiz` answer) changed from 2048 to 8192 and run the
same module:

| `D_BlkSiz` | requested "size" | block landed at | x's written |
|---|---|---|---|
| 2048 | `$64E48` | `$70BC0` | 2 |
| 8192 | `$63E48` | `$6FBC0` | 444 |

**The request moved by exactly `$1000`, the same distance the allocation moved.**
A genuine buffer size does not move when the heap moves; an address does. The
low twelve bits stay `$E48` in both -- the same object at a shifted base.

That also means the amount of output that escapes is an accident of layout: 2
characters at one block size, 444 at another. Neither is "working".

A
pointer arriving in D0 where a byte count belongs is the signature of a
register set up wrongly on entry to the trap handler -- which is os9exec's
job, in `F$TLink` and the trap dispatch. cio is Microware's, shipped and
long-tested; os9exec's trap-handler entry is the newer code and the only layer
the working builds do not touch.

**Still open: where the address comes from.** The shape fits cio computing a
span -- `end - start` -- with a wrong `start`: `$64E48` is a plausible END of
this process's data, so a `start` of 0 would produce exactly this. Two of
os9exec's answers in that area are admittedly nominal: `D_BlkSiz` is
`OS9MINSYSALLOC`, whose own comment is *"a value that makes sense (bfo)"* --
chosen, not measured against real OS-9 -- and `D_FreMem` is answered as NULL
with *"no list available"*. Changing `D_BlkSiz` moves the symptom but does not
cure it, so it is not the whole story. The next place to look is what os9exec
hands the trap handler at `F$TLink` and on trap entry, since that is the only
layer the working builds never touch.

## Why this matters more than one Christmas card

  - **It is invisible unless you look.** The `-qixm` build LINKS CLEAN. `card`
    drew forty moves before dying; `putchar.c` printed two characters and
    exited 0, reporting SURVIVED. A test that checks the exit status passes.
  - **367 programs on this disk are starred**, meaning they use cio. They were
    measured as running, and they do -- because most of them print a little
    and exit before anything has to grow. This is not a claim that they are
    broken. It IS a reason to distrust "it ran" for any cio program that
    produces sustained output.
  - **`-qixm` is the build driver's DEFAULT.** Nothing built by it is
    installed today, so nothing shipped is affected -- but the next recipe
    that installs a `-qixm` binary inherits this.

## The immediate consequence for the collection

`card`'s recipe carries `TRAPFREE` and the measurement table that led here.
That stays until this is fixed; it is a workaround, and the recipe says so.

Files: `notes/cio-srqmem/putchar.c` (minimal), `tputs.c` (the first, larger
reproduction, via termlib), `trace-excerpt.txt`, `syscall-tally.txt`.
