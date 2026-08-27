# Three os9exec defects, found 2026-08-26 by running the collection

Each has a reproduction here that fails in seconds. All three were found by
running programs from the osk-freeware disk, and none of them is a defect in
the collection.

Common setup. `$OS9CLEAN` is the SDK build overlay from
`osk-freeware/tools/rebuild/make_overlay.sh`; `$IMG` is `osk-freeware.dd`.
Every source here is CR-terminated, as OS-9 text must be.

    cc <file>.c -qixm=16k -DOSK -n=<name> -f=R_<name>       # cio      -> FAILS
    cc <file>.c -qm=16k   -DOSK -n=<name> -f=R_<name> ...   # standalone -> WORKS

The pattern across all three: **the statically-linked build is right and the
trap-handler build is wrong.** That is one layer, and it is os9exec's.

---

## 1. F$SRqMem is given a pointer where a byte count belongs

`putchar.c` -- twelve lines, `putchar('x')` 4000 times.

    -qixm   2 characters written, then 3920 x os9exec's own "No more memory !!!"
    -qm     4002 characters, correct

Under `-d1 0x0042` the process makes **4001 `F$SRqMem` calls, one per
putchar**, each asking for **413,256 bytes**, never returning one, until the
32 MB arena is gone. Only **2 `I$WritLn`**: the data never reaches the
terminal. `syscall-tally.txt` and `trace-excerpt.txt` are that trace.

**The requested "size" is an address, proven by moving the heap under it.**
Rebuild os9exec with `D_BlkSiz` (`OS9MINSYSALLOC`) 2048 -> 8192 and re-run the
same module:

    D_BlkSiz 2048   requested $64E48   block landed at $70BC0   2 x's
    D_BlkSiz 8192   requested $63E48   block landed at $6FBC0   444 x's

The request moved exactly as far as the allocation did. A buffer size does not
do that; an address does. Low twelve bits `$E48` both times -- the same object
at a shifted base. The "2 versus 444" is an accident of layout, not health.

`OS9_F_SRqMem` in `fcalls.c` is innocent: it implements the documented
contract (d0.l in = size, d0.l out = actual, a2 = block). It is the request
that is absurd. Shape fits cio computing `end - start` with `start` wrongly 0.
Suggested place to look: what os9exec hands the trap handler at `F$TLink` and
on trap entry -- the one layer the working builds never touch.

Symptom seen from the other end: `CMDS/GAMES/card` takes a **bus error** about
forty moves into its animation, and its crash dump shows eighteen 423,344-byte
blocks.

## 2. cio's stdin never returns end-of-file

`getchar.c` -- nine lines, count bytes to EOF. Redirect **on the OS-9 side**:

    os9exec -r sh -c "gcio < /h6/tiny.txt"    hangs until killed, no output
    os9exec -r sh -c "gcm  < /h6/tiny.txt"    READ 37 bytes from stdin, exit 0

Same source, same file, same redirect. This eats filters -- anything that
reads to end-of-file.

**Also worth knowing, and it fooled me for hours:** redirecting os9exec's OWN
stdin (`os9exec -r prog < file`) never delivers EOF either, for BOTH builds.
The bytes arrive and appear on the console, but the program blocks. So a
program can appear to "echo its input" when it has produced no output at all
and is simply stuck in `getchar`. The tell is that the output length equals
the INPUT's and ignores any flag that sets output length.

## 3. WITHDRAWN -- `Graph` is not a case bug

The claim here was that module load is case-sensitive where RBF is not. **It
is wrong.** Put ONLY the lowercase `graph` on the module search path and the
program runs; case never mattered. See `../OS9EXEC-MODULE-CASE.md`.

What actually happens is that the trap-handler search goes to **`OS9MDIR`, a
HOST directory**, and falls back to a path that does not exist when the
variable is unset -- it never looks on `/dd`. `E_PNNF` is therefore correct.

There may still be an os9exec question in there -- should a trap-handler link
search the process's execution directory on the mounted disk first? -- but I
am not asserting it, because I could not localise it and guessing is exactly
what produced the withdrawn claim. **Do not spend maintainer time on this one
until that question is answered on its own terms.**

The user-facing problem is real and is probably OURS: eight programs link a
library that sits beside them on the image and cannot find it, and this disk
ships no `load` for anyone to preload it with.

---

Full write-ups: `../OS9EXEC-CIO-SRQMEM.md`, `../OS9EXEC-CIO-STDIN-EOF.md`,
`../OS9EXEC-MODULE-CASE.md`.
