# `No more memory !!!` is a cio ABI mismatch, not an os9exec defect

**Root cause found 2026-08-31 by the os9exec session**, which disassembled both
sides. This file records it for the collection; `SRQMEM.md` and
`SRQMEM-SHIPPED.md` are the earlier, wrongly-attributed reads of the same
symptom and are marked as such.

## The mismatch

A cio-linked program reaches the C library through `TRAP #13` with a selector
word: the bytes `4E4D 00xx`. The archives on this disk were linked against a
`cio.l` whose stub table ends

    $3B malloc  $3C calloc  $3D realloc  $3E free  $3F _freemin
    $40 makdir  $41 _flshbuf  $42 _filbuf  $43 fputc  $44 fgetc

Every `cio` MODULE available -- oskBoot's, this collection's (byte-identical to
it), and both SDK builds -- agrees with that table up to `$40` and then has
**five memory routines at `$41..$45` instead**. So a program calling `$41`
expecting `_flshbuf(FILE *, c)` lands on the module's raw allocator, which
reads `d0` as a byte count. `d0` holds the `FILE *`.

That closes the arithmetic exactly: for `cvtbase`, a `d0` of about `$48A18` --
`a6-$7FC6`, its stdin `FILE` -- gives the `$48A20` seen at `F$SRqMem`, via the
allocator's own `((d0+7)>>3 + 1)<<3`.

The allocation succeeds, so `_flshbuf` "returns" a pointer, the `FILE`'s
`ptr`/`end` are never updated, the next `putc` takes the slow path again, and
every character leaks a fresh chunk until the arena is gone.

**This is why the "size" moves with the heap.** Earlier work here established
that and concluded os9exec was substituting an address. It is an address --
one the PROGRAM put in `d0` on purpose. os9exec passes `d0` through untouched
and `F$SRqMem` honours its documented contract.

`cio020` stops at `$40` and cannot serve `$41` at all, so it wild-jumps
instead of storming. The `CIO_Cookie` handshake cannot catch any of this: a
program writes 8 and the module accepts anything up to 9.

## Which programs

353 program modules on this disk link `cio`. **41 contain a branch to their
own `$41` or `$42` stub.** `tools/cio_macro_scan.py` produces the list;
`DOC/README-CIO` carries it for the reader, and `check_disk.py` fails if the
two stop agreeing.

**Reachability cannot tighten it, and that was tried.** A call site inside a
function nothing calls cannot fire, so a call graph would separate the 41 into
live and dead. It does not work here: `cstart` dispatches with an indexed
PC-relative `jsr` (`4EBB 0800`), so a BFS from `M$Exec` is severed at the
first hop and reports every site dead -- including `logisim`'s and
`cvtbase`'s, which have both been watched storm. Widening the roots to "any
function whose address is taken" makes nearly everything reachable and
tightens nothing. The finding is in the script's header so nobody re-derives
it.

What does tighten it is running the 41 with realistic input and watching for
an `F$SRqMem` whose `d0` is wildly larger than that module's own
`M$Mem`+`M$Stack` -- `logisim` asks 643,624 against 39,236, about sixteen
times. That request appears on the FIRST character, hundreds of thousands of
lines before any flood, so a run can be stopped the moment it shows. Two
hints from the disassembly: a site whose `FILE` operand is `lea fp@(-N),a0`
with N near `$7FC6` is on `_iob` and fires in ordinary use; one whose operand
arrives in a register needs the program to have opened a file first.

**That is an upper bound, and the gap matters.** A call site only fires if it
is reached. All 41 run bare with stdin closed print their usage and exit
cleanly, because a usage message goes through the module's own `printf` and
never touches the `putc` macro. `ascii` prints its whole table correctly for
the same reason. Two are confirmed to reach it:

    echo 255 | cvtbase d h        439,689 lines of "No more memory !!!"
    setenv PORT /term; logisim /dd/DOC/logisim/flipflop.lsi    284 lines

**The rule for a reader:** a program fails this way when it executes a
`putc`/`getc` MACRO on a `FILE`. It is fine when it uses `printf`, `fprintf`,
`fwrite`, `read` or `write`. That is why feeding 272,000 bytes to all 368
starred binaries came back with zero floods -- `cat`, `detab` and `autolf`
never take that path. `autolf` even CARRIES the stubs and still does not
flood, which is why counting stubs is not the measurement; counting branches
to them is.

## What is genuinely os9exec's

One line. `Source/OS9exec_core/memstuff.c:782` prints `No more memory !!!` to
the console unconditionally on every failed allocation. Real OS-9 returns
`E$NORAM` silently and lets the caller decide. That single difference is why
an ABI fault inside a program reads as an emulator failure: the emulator's
voice arrives on the program's standard output, drowning it. It is being
raised separately.

## What this cost, and the lesson

The `CMDS/sed` swap of 2026-08-28 stands -- with the `cio` module here that
build genuinely cannot run -- but the reason recorded for it was wrong, and a
note in this repository briefly argued the collection had been made poorer by
an emulator bug. It had not.

Being right that `d0` held an address was not the same as being right about
who put it there. The heap-shift test proves an address; it says nothing about
whether the program or the runtime supplied it. Answering the second question
needed the disassembly of both sides, and no amount of tracing from outside
would have settled it.
