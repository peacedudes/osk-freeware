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

`notes/os9exec-iread/ireadt.a` -- **pure 68000 assembly**, 414 bytes linked.
No C, no `cio`, no library of any kind between it and the syscall, and no
`I$SetStt`, so the path keeps whatever `PD_EOR` the shell handed it (CR).

    r68 ireadt.a -o=ireadt.r
    l68 ireadt.r -o=/h6/ireadt      (name the output PATH: l68 writes -o= to
                                     the EXECUTION directory, not the data one)

Run it on a pty, press a key, then type a line and press Return:

    A: I$Read for 1 byte -- press a key
    X                                     <- typed, echoed
    A: returned                           <- the 1-byte read CAME BACK
    B: I$Read for 256 bytes -- type a line, press return
    hello                                 <- typed, with Return, echoed
                                          <- "B: returned" never appears

The 1-byte read returns on the first keypress. The 256-byte read never
returns, though a complete line terminated by carriage return was typed.

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

---

## A separate finding, while looking at the same file

**os9exec does not execute guest code in supervisor state at all.** The module
attribute word `_mattrev` is read and returned to callers (`F$Link` and
friends, `fcalls.c`) but is never tested for bit 5, and `os9_tick.c` says the
supervisor bit is "kept as an honest guard in case emulated supervisor code is
ever run".

That is the complete explanation for nine more programs on the freeware disk.
`CMDS/GAMES/graph` and `CMDS/COMMS/vmod_trap` are both type-$0B trap libraries
with `M$Attr = $A0` -- bit 5 set -- so a user-state process faults the instant
it enters them. The seven Atari graphics programs, plus `rxmod` and `trap`,
all stop there.

Unlike the I$Read case this is a missing FEATURE, not a defect: nothing in the
emulator claims to support it. It is recorded only so the next person does not
spend a day proving it from the outside, as this pass nearly did.

---

## A second deviation on the same spec line -- NOT fixed

Found while looking for siblings of the first, and proved the same way:
`notes/os9exec-iread/eortest.a`.

The manual's PD_EOR entry governs **both** calls:

    PD_EOR   End of record character
             Defines the last character on each line entered
             (I$Read, I$ReadLn).  An output line is terminated (I$Writln)
             when this character is sent.  Normally PD_EOR should be set to
             $0D.  WARNING: If PD_EOR is set to zero, SCF's I$ReadLn will
             never terminate, unless an EOF or error occurs.

`pConsInLn` passes a hardcoded `CR`, not `ot->_sgs_eorch`:

    err= ConsRead( pid,spP,maxlenP,buffer,true,CR );

`eortest.a` sets PD_EOR to LINEFEED through I$SetStt SS_Opt, then calls
I$ReadLn and waits. Typing text and pressing RETURN -- a CR, which is no
longer the end-of-record character -- the read returns anyway:

    setting PD_EOR to LINEFEED
    now type text and press RETURN (a CR, not a LF)
    abc
    I$ReadLn RETURNED -- so it used CR and ignored PD_EOR

**It was left alone deliberately, and the reasoning matters more than the
finding.** Unlike the I$Read case this has no known victim and a real
downside:

  - Every program on this disk uses the default PD_EOR of CR, so none can
    tell the difference. There is no `ksh' here waiting to be fixed.
  - I$ReadLn is what `bash', `sh' and every line-mode read go through. A
    regression there is far worse than the bug.
  - Matching the spec exactly would import the manual's own documented
    footgun: with PD_EOR zero, the read must never terminate. os9exec's
    hardcoded CR is wrong, but it is wrong in the safe direction.

So: recorded, reproducible, and somebody else's call. The I$Read fix had a
concrete victim and no downside; this one has neither.

## The fields nothing reads

While looking, every SCF path option was checked against the code. Seven are
never read at all: `_sgs_dtp`, `_sgs_dlo`, `_sgs_nul`, `_sgs_rprch`,
`_sgs_pscch`, `_sgs_ovfch`, `_sgs_par`.

None can hang a program, which is what made the I$Read case serious. They
mean a line-editing key does nothing (`rprch` reprint, `pscch` pause-scroll),
no bell on overflow (`ovfch`), or a setting with no meaning on a pty
(`par` parity, `nul` padding for slow terminals, `dlo` delete-line style).
Worth knowing; not worth chasing.
