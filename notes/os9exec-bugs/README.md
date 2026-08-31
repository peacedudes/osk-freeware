# os9exec defects found by running the collection

Each has a reproduction here that fails in seconds. All were found by running
programs from the osk-freeware disk, and none of them is a defect in the
collection.

**`No more memory !!!` IS NOT AN os9exec DEFECT. Read
`CIO-SELECTOR-MISMATCH.md` first.** The root cause was found 2026-08-31: the
archives were linked against a `cio.l` whose stub table has `_flshbuf` at
selector `$41`, while every `cio` MODULE here has a memory routine there, so
`putc` lands on the raw allocator and hands it a `FILE *` as a byte count.
os9exec passes `d0` through untouched.

`SRQMEM.md` (2026-08-26) and `SRQMEM-SHIPPED.md` (2026-08-31) are the earlier
reads of the same symptom. Both were right that `d0` carries an address and
wrong about who put it there. They are kept for their reproductions and their
measurements; their attributions are not to be quoted.

The one genuine os9exec item is small and is in `CIO-SELECTOR-MISMATCH.md`:
`memstuff.c:782` announces every failed allocation on the console, where real
OS-9 returns `E$NORAM` silently -- which is why a fault inside a program reads
as a fault in the emulator.

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
program runs; case never mattered. See `MODULE-CASE.md`.

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

Full write-ups: `SRQMEM.md`, `STDIN-EOF.md`,
`MODULE-CASE.md`.

---

# Second pass, 2026-08-26 evening -- after independent reproduction

Reviewed by another session on a licensed disk with a different cio edition
and a separate build. Same counts: 4001 `F$SRqMem`, 2 `I$WritLn`. The symptoms
are confirmed; the ATTRIBUTION below is what changed.

## Two corrections to what I wrote above

**Bug 2 is not an EOF bug.** Traced under cio, the child makes ONE `F$TLink`
and then no syscalls at all -- it never reaches a read. The static build on the
identical path does 2 `I$Read`s and exits clean, so EOF delivery works. cio
hangs in its own setup. "stdin never returns EOF" names a layer above where it
dies. **Bugs 1 and 2 are very likely ONE defect**: `putchar` turns it into an
allocation storm, `getchar` into a spin.

**My inference was unsound.** I argued "the static build is right and the
trap-handler build is wrong, therefore os9exec's layer". The static build never
enters cio, so it cannot testify about os9exec's handling of cio. That is the
same shape as the withdrawn claim 3, and I used it twice.

## Measurements that narrow it -- and kill one lead

The other session found the request equalling `a3+$3C` and flagged it as
pointer-where-a-value-belongs. **That correlation does not hold here.** With
the same reproduction on this build, `a3` MOVES between calls (it is the block
just returned) while `d0` stays fixed, so the two cannot be related:

    ### SRqMem absurd: d0=$47DC8  a3=$52138   a3+$3C=$52174   no match
    ### SRqMem absurd: d0=$47DC8  a3=$53A48   a3+$3C=$53A84   no match

**What does hold: `d0` is the process's own data block, plus $48.** Measured
across three builds differing only in requested memory:

    -qixm=4k    block #0 base $47D80  size 10192   d0=$47DC8   pc=$4A72E
    -qixm=16k   block #0 base $47D80  size 22480   d0=$47DC8   pc=$4D72E
    -qixm=64k   block #0 base $47D80  size 71632   d0=$47DC8   pc=$5972E

`d0` is invariant. The data area's SIZE changes by 7x and the value does not
move; cio's own return address (`pc`) does move, which is just cio being
loaded after the data area. So the absurd "size" is **a pointer 72 bytes into
the process's own data block** -- constant because the block's base is
constant, not because it is a constant.

That also explains the earlier `D_BlkSiz` experiment: 2048 -> 8192 moved the
value $64E48 -> $63E48 because it shifted the whole arena, not because the
value has anything to do with block size. My "proven to be an address" claim
survives; my implied "and therefore os9exec computed it" does not.

Full register set at the trap, first call, 16k build:

    d0=$00047DC8  a0=$00047DBA      d0-a0 = $E
    d1=$00000078  a1=$0004D60A
    d2=$00047D9E  a2=$00052138
    d3=$0004D54C  a3=$00052138
    d4=$00008FB9  a4=$0004D548
    d5=$00008FB8  a5=$0004D4DA
    d6=$000057D0  a6=$00059C40
    d7=$00000000  a7=$0004D4D6

`d0`, `a0` and `d2` all point into the first 72 bytes of the data block.

## Where I stop

**I cannot say whether this is os9exec's or cio's, and I am not going to guess
a third time tonight.** The walk-back proposed by the other session is the
right next step, and the measurement above gives it a target: find what
writes, or reads, `data_block_base + $48`. If that word is something os9exec
put there, it is ours; if cio computed it from its own state, it is cio's or a
kernel service we do not provide.

The instrumentation that produced these numbers is a three-line dump in
`OS9_F_SRqMem` in a SCRATCH build of os9exec. rdoggett's os9exec tree is
untouched.
