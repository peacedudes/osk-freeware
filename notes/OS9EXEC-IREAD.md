# os9exec: I$Read on a terminal waits for the full byte count

Measured 2026-08-20. This is an **os9exec defect**, not a fault in any program
on this disk, and it is the complete explanation for `ksh`'s dead interactive
loop — the thing that has been called the biggest single gap on the disk.

## The measurement

Two reads from path 0, in one program, on a pty:

| call | result |
|---|---|
| `read(0, buf, 1)` | **returns 1** on the first keypress |
| `read(0, buf, 256)` | **never returns**, however much is typed |

The second read sits for ever while `LINE1<CR>LINE2<CR>` is typed and echoed.
It is not that terminal input is unavailable — the 1-byte read in the *same
program*, moments earlier, got its character immediately.

Line-mode reads are unaffected:

| call | result |
|---|---|
| `fgets(buf, n, stdin)` — `I$ReadLn` | works, returns the line |
| `read(0, buf, n)` — `I$Read` | blocks unless n is small enough to fill |

So `bash` and `sh` are interactive here and `ksh` is not, and that is the whole
difference between them.

## The reproduction

```c
#include <stdio.h>
main()
{
    char buf[300];
    printf("1-byte read -- press any key:\n"); fflush(stdout);
    printf("  read(0,buf,1) returned %d\n", read(0, buf, 1)); fflush(stdout);
    printf("256-byte read -- press a key then return:\n"); fflush(stdout);
    printf("  read(0,buf,256) returned %d\n", read(0, buf, 256)); fflush(stdout);
    exit(0);
}
```

Build it with the SDK (`cc rd1.c -qixm=8k -n=rd1 -fd=rd1`) and run it under a
pty. The first line prints and reports 1. The second prints and then nothing
ever follows.

**It must be run on a PTY.** Piped or redirected input hides the defect
completely, because the data is already there to satisfy the whole request.
That is presumably why it has gone unnoticed.

## Where it is, in one line

rdoggett asked the right question: does ksh, or anything else, disable EOR or
change it? If a program deliberately asks for raw input, waiting for the full
count would be CORRECT and there would be no defect here.

**Nothing disables it.** os9exec's own header documents the field --
`os9defs/sgstat_from_book.h`:

    uint8_t  _sgs_eorch;  /* 0x0B  PD_EOR   end-of-record (CR) character */

and os9exec honours it in three places: on writes (`ConsPutcEdit`, consio.c),
on `I$ReadLn`, and on pipes (`pipefiles.c` reads `ot->_sgs_eorch`). The read
path is the exception, and the two calls sit side by side in `consio.c`:

    pConsIn   (I$Read)    ConsRead( pid,spP, maxlenP,buffer, false, 0  );
    pConsInLn (I$ReadLn)  ConsRead( pid,spP, maxlenP,buffer, true,  CR );

`pConsIn` passes a literal `0` as the end character rather than
`ot->_sgs_eorch`. So the terminator is not disabled by anybody -- it is never
consulted on that path in the first place.

The control experiment is the reproduction below: it does no `ioctl` and no
`SS_Opt` at all, so the path is in its default state with EOR = CR, and the
256-byte read still never returns.

(For completeness: pdksh's `edit.c` DOES put the terminal in raw mode via
`x_mode()` when its line editor is active. But with the editor off -- `set +o
emacs` -- `lex.c`'s plain `read(ttyfd, line, LINE)` runs with the terminal
untouched, and it hangs just the same.)

## Why it kills ksh

pdksh reads its command line at `SRC/pdksh/sh/lex.c` line 559:

    c = read(ttyfd, line, LINE);

and `sh.h` has `#define LINE 256`. The syscall trace agrees exactly:

    >>> Pid=02: OS9 I$Read : D0.w=$000A D1.l=$100 A0=$B50BE      ($100 = 256)
    (no return, ever)

Nobody types 256 characters, so the read never completes, so ksh never sees a
command. It is not a parser problem or a job-control problem: `ksh -c '...'`
works completely — loops, variables, `$PWD` — because that path never reads a
terminal.

Path 10 in the trace is not significant, by the way. pdksh dups its shell
descriptors up out of the way of user redirections (16 `I$Dup` calls, path 0
to paths 3..18); a duplicate of path 0 reads exactly as path 0 does. The
byte count is the whole story.

## Two things that are NOT the cause, both checked

- **`isatty` works.** `SS_Opt` succeeds on paths 0 and 1, so ksh does set
  `FTALKING` and does believe it is interactive.
- **The line editor is not to blame.** Setting `ENV` to a file containing
  `set +o emacs` and `set +o vi` makes the **prompt appear** — proving ksh
  reads and executes its ENV file happily — and the command read still never
  returns. Editing off or on, the read is the same `read(ttyfd, line, LINE)`.

## A source fix exists, and is blocked on something else

`lex.c` can be patched to read a byte at a time up to the newline, guarded by
`#ifdef OSK`, which the tree already uses. That patch is written and is
correct as far as it goes.

**pdksh cannot currently be rebuilt here**, for reasons that have nothing to
do with the patch:

  - `osklib.r`, which its `dmakefile` links, **exists nowhere** — not on this
    disk, not in the SDK, not anywhere in the archive pool. `OSK_INCL` holds
    what look like its sources (`ic_ksh.c`, `iexec.c`, `ijobs.c`, `imisc.c`),
    so it could perhaps be reconstructed, but that is a port bring-up.
  - The `std/` header tree wants `/usr/include/sys/types.h` and friends. It is
    meant to be configured by its own `mklinks` against a real Unix system's
    headers.
  - `os9lib.l` is not in the SDK either, though it IS in the pool three times
    over (`EFFO/forum20.lzh`, `GCC/libgpp_2.5.3_lib.lzh`,
    `GRAPHICS/gnuplot32x.tar.Z`).

So the honest position is: **the cause is known exactly, the fix is known, and
the build is blocked on a missing support library.**

## Fixing os9exec would be better anyway

A program is entitled to ask for more bytes than are available; a terminal
read should return what has arrived. Fixing it in the emulator fixes ksh
without touching pdksh.

**Nothing else on this disk is affected, checked 2026-08-20.** Every one of
the 43 programs that do not run was traced for a large `I$Read`. Two do one —
`dir` asks for `$180` and `read_mail` for `$200` — but both are reads from a
FILE on path 3, not from a terminal, and both of those programs now work
anyway. `ksh` is the only casualty.

os9exec lives at `~/Developer/os9/os9exec`. Nothing here has been changed in
it; that is rdoggett's call.
