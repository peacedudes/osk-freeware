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

## There are TWO cio.l vintages, and the binary shows which it linked

Found by the os9exec session and verified here independently. Count the
distinct trap-13 selectors a program's stub table carries; its maximum
identifies the library it was linked against. Across the 353 cio-linked
programs:

| max selector | programs | with a `$41`/`$42` call site |
|---|---|---|
| `$45` -- the 70-entry library | 96 | **0** |
| `$44` -- the 69-entry library | 116 | **41** |
| `$2B`..`$40` -- partial tables | 139 | 0 |

Not one program from the 70-entry library calls `$41`/`$42`, and every one of
the 41 comes from the 69-entry one. Our `cio` modules dispatch `$00..$45`, so
**the 70-entry library is the one that matches them and the 69-entry library
is the mismatched one.**

The difference is what `putc`/`getc` compile to. In the matched vintage they
are ordinary FUNCTION calls -- selectors `$12` and `$09` -- and the buffering
happens inside the module, where it is consistent. In the mismatched vintage
the header inlines them and the slow path calls `_flshbuf`/`_filbuf` at
`$41`/`$42`. That is the whole of it, and it explains `autolf`: it carries the
stubs and never floods because it does not have the macro at all.

**`ksh` is fine, and this is why.** It calls `$12`/`$09`, never `$41`/`$42`.
Its 188 requests of 262,576 bytes come from `malloc` (`$3B`) reaching the
module's own allocator -- one chunk, reused, which is that allocator working
correctly, not a leak per character. Worth stating because 188 identical large
requests look exactly like the fault from outside.

`oskBoot` ships the 69-entry `LIB/cio.l` beside a module that wants the
70-entry one, which is why anything built `-qixm` here is broken by
construction rather than by choice.

(Counting from this end gives 96 in the `$45` bucket where the os9exec session
counted 98, and turns up one spurious "selector" of `$454E` -- the ASCII `EN`,
a `4E4D` byte pair that is not a stub. Scanning noise at the edges; the
separation itself is exact.)

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

**Two ways of tightening it were tried and BOTH failed. Do not repeat them.**

*A generic invocation sweep is vacuous.* Driving each program with a text file
on stdin and as an argument, and watching its `F$SRqMem` traffic, reports
`logisim` and `cvtbase` CLEAN -- the two programs that have been watched storm.
Neither invocation reaches the macro: `logisim` exits at its `PORT` check and
`cvtbase` prints its usage without arguments. A usage message goes through the
module's own `printf` and never touches `putc`. So "did not flood under X" is
scoped to X and is not a negative about the program, and a sweep that forgets
that hardens into a false all-clear.

*A 16x threshold on `M$Mem`+`M$Stack` does not separate them either.* The
suggestion was to flag any `F$SRqMem` whose `d0` is wildly larger than the
module's own requirement, 16x being generous:

    logisim   needs 39,236   asks 643,624   16.4x   caught
    cvtbase   needs 20,486   asks 297,504   14.5x   MISSED

`cvtbase` slips under with the RIGHT invocation, so the threshold would have
to come down to about 10x, and at that point it is a guess rather than a
discriminator. What actually characterises the bad request is that it is an
address: the SAME non-round value, repeated hundreds of times, never freed,
and moving when the heap moves. Repetition and heap-dependence are the real
signals; magnitude alone is not.

Two hints from the disassembly, for anyone driving these by hand: a site whose
`FILE` operand is `lea fp@(-N),a0` with N near `$7FC6` is on `_iob` and fires
in ordinary use; one whose operand arrives in a register needs the program to
have opened a file first.

## The 41 driven, one at a time -- 2 storm, 38 do not

Done 2026-08-31, after the two sweeps above failed. Each program was given the
arguments its OWN usage line asks for, and the invocation is recorded with the
result, because "did not flood under X" is a statement about X:

| | |
|---|---|
| storm | **2** -- `cvtbase` (`cvtbase d h`, number on stdin), `logisim` (`PORT`, `TERM`, `TERMCAP` and a circuit file) |
| driven, no flood | **39** |
| not driven | none |

Of the 38: 31 were run here with file arguments taken from their usage lines
(`chksum`, `snap`, `spiff`, `unifdef`, `diff`, `nroff`, `ape`, `xrf`, `etags`,
`cookhash`, `lp`, `pagefraz`, `pagekwic`, `undel`, `dam`, `loan`, `printf`,
`strfile`, `ascii`, `crypto`, `unstr`, `unpacklib`, `liborder`, `cdiff`,
`makelex`, `hexed`, `vis`, `yacc`, `setfont`, `sedt`, `wish`); six are games
that pass their play-tests on a pseudo-terminal, which means they reach
character output (`blackjak`, `poker`, `stone`, `tess`, `rpoem`, `newsgen`);
and `valspeak` exits at once producing nothing at all, which is a fault of its
own recorded since 2026-08-27 and not this one.

`REBUILT/kermit_cio` was the last gap and is now closed. It rejects
`kermit sl /t1 <file>` with its usage line whatever the spacing, but plain
`kermit s <file>` runs send mode over the console -- 529 bytes out, no flood --
and `kermit r` enters receive. os9exec will also give it a real serial line
(`OS9T1=pty`, then `/t1`), which was not needed in the end.

`ascii` is worth singling out: it prints its whole 66-line table correctly
while carrying two `_flshbuf` call sites. Carrying the call is not the same as
running it.

**So two programs on this disk are actually broken by the mismatch**, out of
353 that link `cio`. That is the number to quote.

## The statement that carries its own reason

Even so, the count above rests on the linkage rather than on the runs:

> 41 programs were built against a `cio.l` whose `putc`/`getc` macros call
> selectors `$41`/`$42`; every `cio` module we have implements those as
> memory routines.

Tightening the 2 means driving each program the way it is meant to be used and
recording the invocation beside every result. That is a per-program SETUP
problem, not an endurance one: the slow path fires on the FIRST character
through a `FILE`, so each program need only be made to produce one character
of real output or consume one of real input. `logisim` needed `PORT`, `TERM`,
`TERMCAP` and a circuit file; `cvtbase` needed two arguments and a number.

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
