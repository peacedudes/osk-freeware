# Second pass — what did not work

Written 2026-08-17. Data: `verify-bare.tsv`, `verify-filters.tsv`,
`verify-session.tsv`, `verify-usage.tsv`, combined in `verify-final.tsv`.
Tools: `tools/verify_all.sh` → `verify_filters.sh` → `verify_in_session.sh` →
`verify_usage.sh`, run in that order.

    949  program files under disk/CMDS
     24  are not programs at all (trap libraries, drivers, BASIC09 I-code,
         data modules, shell scripts) -- see disk/DOC/README-MODULES
    925  actual programs
    870  demonstrated running -- 94.1%
     55  did not

## Read this before trusting any sweep of this disk

Two false results were produced and caught during this work. Both would have
shipped a wrong number in `DOC/STATUS`.

**os9exec's `#` lines are the verdict, not noise.** `grep -v '^#'` to isolate
program output throws away `Emulation could not start due to OS-9 error
#000:205 (E_BMID)` and `Process pid=2 aborted due to unintialized User Trap
#5`. With those gone the remaining blank line counts as output, and 91
programs that do not load at all were reported working — including
`blackjack`, which `DOC/STATUS` has always listed as broken. Keep the `#`
lines; only `# /h0:` / `# /dd:` startup notices are noise.

**Running bare is not a fair test.** A program started as os9exec's first
process has no environment: no TERM, no TERMCAP, no PATH. 69 programs on this
disk read TERMCAP and `SYS/login` is what sets it. Run bare, `cribbage` says
"Environment variable TERM not defined", `crib` says "Unknown terminal type
''", and `aterm` and `snake` take **bus errors**. All four work in a login
session. So the same missing TERMCAP appears as a clean message in one program
and as a bus error in another, depending on whether its terminal library checks
the pointer before following it. A bus error is not proof a program is broken.

Host environment variables do not reach an OS-9 program — setting TERM in the
launching shell changes nothing. Going through `SYS/login` is the only way.

**Also:** `head -c` in the sweep pipeline is load-bearing. It closes the pipe,
os9exec takes SIGPIPE, and chatty programs finish immediately instead of
running out the 10-second timeout. Without it the sweep takes seven hours
instead of one. And a `while read` loop fed from a *pipe* loses most of its
input when the body runs os9exec — read from a file and check the output row
count against the input row count.

## Worth real effort

**`ksh` interactive loop.** `ksh -c '<commands>'` works completely — `for`
loops, variables, `$PWD`. Interactively it prints no prompt and executes
nothing, on a pty as well as a pipe, with CR, LF or CRLF line endings. A shell
that cannot be typed at is the biggest single gap on the disk.
`disk/SYS/profile.ksh` exists and may never be read; `ENV` is not set by
`SYS/login`. Start there.

**`devprc` — bad module CRC (E_BMCRC 232), and rebuildable.** Verified: stored
`6CF320`, computed `9F16E0`; header parity is fine, so only the body/CRC is
wrong. The copy in EFFO forum disk 16 is byte-identical and equally bad, so it
shipped that way — this is not damage the collection introduced. Source is now
on the disk at `SRC/devprc` (`devprc.c`, `getopt.c`, `getsys.a`, `makefile`,
`Devprc.man`). A recipe line would be `devprc|devprc|devprc.c getopt.c|||`,
but note `getsys.a` is assembly and the makefile will want it.

**The five SNOBOL4 games.** `poker`, `blackjak`, `rpoem`, `rstory`, `stone` —
all from `effo_snobol` (Robert Heller's SNOBOL4-in-C, EFFO forum disk 9) — fail
identically, bare and in a session: `Error #255:255 (E_???)` then `Illegal
instruction: 4afc at 000516c8`. `$4AFC` is both the 68000 ILLEGAL opcode and
the OS-9 module magic, so control has jumped into a module header. `rstory2`
and `tformat` are from the same archive and both run, which puts the bug in one
code path of the shared library, not in the disk. Full K&R source in
`SRC/effo_snobol`; `DOC/snobol` has the author's readme and the pattern files.
Five programs for one fix.



**Two programs want floating-point hardware, and this is the case for `fpu`.**
`os9lib` stops with `NON-IMPLEMENTED FLOATING POINT INSTRUCTION`. `config`
prints char, short, int, long, pointer and float properties correctly and then
aborts on vector `$0B` — the 68000 line-F emulator vector, which is how a
coprocessor instruction announces there is no coprocessor — exactly where
`double` begins. Microware's `fpu` is the emulator for this and `p2init`
installs it as a system extension. The permission obtained covers cio, math,
math881, csl and csl020. These two are the concrete example if that request is
ever reopened. (The earlier decision was "if we don't need them we don't ask";
this is what needing them looks like.)

**`oleo`** — GNU Oleo 1.6, `Illegal instruction: 0009 at 000465d2`.

## Want hardware or a module nobody has

  - **`graph` is the `Graph' trap library, not a game.** It is a type-`$0B`
    trap module and it is what `g`, `striche`, `apfel`, `sine`, `showpic`,
    `graphdemo` and `graphsave` all link. With `OS9MDIR` pointed at
    `disk/CMDS/GAMES` the trap installs and the failure changes from "Can't
    install trap handler" to an abort inside the library, which drives Atari
    hardware. One caveat for real OS-9: the module's name is lowercase `graph`
    while the programs ask for `Graph`, and real OS-9 matches module names
    exactly — os9exec only found it through a case-insensitive host filename
    lookup. Renaming the module (M$Name string, then CRC and header parity)
    would fix that, unverifiably from here.
  - `rxmod` — wants a `Vmod` trap library. `trap` — a trap-handler
    demonstration, reports `tlink: -1`.
  - `wysecrack` — probes for a Wyse terminal. Correctly in `CMDS/BROKEN`.
  - `cyberwar` and `lfmaker` are module GROUPS containing type-`$04` **window
    descriptors** (`cyber_start_win`, `cyber_retry_win`, `lfmaker_win`), so
    they want OS-9's windowing, which is not on this disk. That is probably why
    both are silent in every stage.

## Silent in every stage — 34, and a shortlist of 28

Ran without complaint and printed nothing bare, with input, in a session, and
asked `-?`. Six are explained and closed (`wisecrack` writes to
`/PIPE/txtpipe`; `vtxtcn` writes `world`'s `.inc` files; `byteflip` needs a dbz
database; `wysecrack` needs Wyse hardware; `tex`/`latex`/`slitex` prompt with
`**` and read stdin, which they do — `-?` is not TeX's convention).

The remaining 28 want individual attention:

    arepdaemon  authwn    bincheckr  biory      bootlogger  creadoc
    cron        cyberwar  dir        elvprsv    for         inetdc
    infoxpress  lfmaker   lnk        lnk.org    makecrc     pri
    ptxminst    puzzle    read_mail  rtf        scriptmaster
    splman      splprt    suse       t



## Corrections this pass made to the catalogue

  - `graph` was "Atari graphics demonstration" for as long as the catalogue
    existed. It is a trap library.
  - `snake` was "starts and then sits". It draws its board.
  - `aterm` was recorded as a bus error. It prints its banner and runs.
  - `config` was "the RICO configuration tool". It reports C type properties.
  - `cribbage` and `crib` were failures. They play.
  - `DOC/STATUS` said 426 programs and 87 needing cio; the disk has 925
    programs and 241 starred names.

## Carried over from earlier passes, unchanged

  - **WN web server / inetd** — os9exec's `adapt_inetdb` in `modstuff.c` reads
    hosts-field pointers at fixed offsets 0x34/0x38. The SPF-variant `inetdb`
    has `$0100000D` there, so `size` becomes 4,278,190,183, `get_mem` fails,
    NULL reaches `memcpy`, and the process dies `E_BUSERR(102)`. os9exec
    defect, diagnosed not fixed.
  - **`adlrun` from a host-directory mount** — `Assertion failed:
    (buffer!=NULL), function pFread, file fileaccess.c, line 336`. Works from
    an image. os9exec defect.
  - **`top`, `digclk`, `draw`** — draw correctly, then `E_PRCABT(228)`.
  - **`greed`, `suicide`** — start, produce no output.
  - **`mail`** wants an `/r0` RAM disk; **`makedb`** wants
    `/dd/usr/lib/smail/palias`.
  - **Quit keys unknown** for `digclk`, `draw`, `sc`, `sh`, `vi_cio`.
  - **`mg`'s `mgrc`** and **forth's `lib/tile`** are not in the pool.
  - **RCIS** — 37 programs plus 81 BASIC09 I-code modules; needs Microware's
    `runb`, which the permission does not cover. `bio`, `wysetime` and
    `blackjack` on this disk are in the same position.
  - **`elvis`** — full documentation and source on the disk, no binary.
  - **os9exec's `-m`/`-M` numeric options do not parse** in this build:
    `-m 64k`, `-m64k` and `-M64M` all fail with `Error in decimal number`
    naming the *program* as the number. Untested territory as a result.
