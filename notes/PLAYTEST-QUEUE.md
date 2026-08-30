# Play-test queue

Things that need a human at a real terminal, with exactly what to type. Each
one is a candidate I could take no further from a pipe: os9exec's stdin is not
a tty, and several of these programs ask the terminal about itself before they
will work.

## 1. tet, rebuilt -- does it take keys now?

**Why:** `GAMES/tet` draws its board and ignores the keyboard. The cause is in
its source: the raw-mode setup (`ioctl(TCGETA)`, reopening stdin `O_NDELAY`)
is entirely inside `#ifndef OSK`, so the OS-9 build has no terminal setup at
all and its `read(0, combuf, 1)` never sees a keystroke.

`REBUILT/tet.unixlib` is the same source compiled with that path **enabled**,
linked against `LIB/unix.l`, whose `ioctl.c` implements TCGETA/TCSETA over
`_ss_opt`. It draws identically to the original. Whether it now reads keys can
only be seen at a terminal.

    chd /dd/CMDS/REBUILT
    tet.unixlib

**Third attempt, 2026-08-13.** Still no keys after the TCSETAW fix, which
pointed past the ioctl entirely. The real stopper was two lines above it:

    close (0);
    open (ttnam, O_NDELAY);

`O_NDELAY` is a Unix open() *flag*; OS-9's `open()` takes an *access mode*,
and `DEFS/os9lib/fcntl.h` defines `O_NDELAY` as **0** -- no read, no write.
tet closed its own stdin and reopened it unreadable. Writes on fd 1 still
worked, which is precisely why the board draws and nothing is ever read. No
ioctl fix could have helped. Now opens `S_IREAD`.

That exposed a second thing: `GetKey()` loops until `read` returns 0, so it
needs a non-blocking read -- what `O_NDELAY` was for. OS-9 has no such flag
on a path, so `GetKey` now calls `_gs_rdy(0)` first and returns when nothing
is waiting. Without that the game would block between keystrokes and the
piece would never fall.

All three faults and the build line are written up in `SRC/tet/README`, and
the patched source is in `SRC/tet` so the change is readable.

**Second attempt, 2026-08-13.** The first rebuild still echoed keys and
ignored them, which was the useful result: echo still on means the mode never
changed. The cause was a second fault underneath the first -- `LIB/unix.l`'s
`ioctl.c` implements `TCSETA` but **not `TCSETAW`**, and `TCSETAW` is the call
tet uses to go raw. It fell through silently. `SRC/unixlib/ioctl.c` now sends
`TCSETAW` and `TCSETAF` into the `TCSETA` case, `LIB/unix.l` is rebuilt, and
tet is relinked against it. Also needed a `randint` shim
(`tools/rebuild/shims/os9randint.c`): tet's makefile links a `/dd/lib/rand.r`
that exists nowhere.

Keys are on its own menu: `q` quits, `p` pauses, `b` is the boss key, `s`
shows the score. **What to report:** does `q` quit? If yes it is fixed, and
it should replace `GAMES/tet`. If it still ignores everything, the raw-mode
call is failing and the next thing to look at is whether `_ss_opt` accepts
what ioctl.c sends it.

## 2. The other stuck games

- **`lander`** -- takes no input, corrupt screen after a crash. Its OSK
  conditionals are about `M_PI` and `random`, not input; it reads with curses
  `wgetch`. The live theory is still its README's: it wants SysV curses line
  drawing that vt100 termcap does not provide. Worth trying under a terminal
  type with line-drawing if you have one.
- **`snake`** -- starts and sits. It DOES call curses `raw()`, so the terminal
  mode is not the problem and it does not share tet's cause. Unknown.
- **`maze`** -- starts and sits. No source anywhere, so it can only be
  play-tested, not diagnosed.

## 3. The three vi editors

`DOC/README-VI` compares them on paper -- source lineage, option counts,
documentation. What it cannot say is which is pleasant to use. All three are
worth ten minutes each:

    vi /dd/tmp/x        the real Berkeley ex/vi
    elvis /dd/tmp/x     the clone with the most options
    vi_nocio /dd/tmp/x  the small one

## 4. Anything curses

`oleo`, `mines`, `checkfile`, `sc` and `scqref` all want a real TERM and were
only checked far enough to see them start.

## The "how do I quit" gap -- found 2026-08-16

rdoggett ran `ephem` on the finished disk and reported: *"seems boring to me,
doesn't do much and i cant figure out how to quit"*. Both halves of that are
our fault, not the program's. It quits on **control-D**, from command mode,
and the way to make it do something is to set StpSz and NStep and let it run
time forward -- none of which is discoverable from the screen. A how-to note
now says so.

**67 full-screen programs have no how-to note at all** -- they read termcap,
take over the screen, and tell you nothing about how to leave. That is the
same trap, 67 more times: `beav`, `hexedit`, `jargon`, `larn`, `hack`,
`greed`, `mille`, `cribbage`, `bog`, `hang`, `lander`, `mg`, `me`, `emacs`,
`gnuchess`, `ispell`, `draw`, `editor` and the rest.

**Done 2026-08-16, by running them.** `tools/try_quit.py` drives each program
through `SYS/login` under a real pty, lets it draw, sends a candidate key, and
watches for the shell prompt to come back -- with a control run that sends no
key, so a program that exits on its own cannot be mistaken for one the key
worked on. 37 of the 67 now have a tested quit key
(`quit-keys-verified.txt`, (deleted in the 2026-08-27 notes prune; `git log --diff-filter=D --name-only -- notes/` finds it)), and those are in `tools/howto.psv`.

Two earlier approaches failed and are worth not repeating: piping to these
proves nothing (with stdin not a terminal they exit at EOF, so every key
"works"), and driving os9exec directly with `-r` fails because it does not
inherit TERM into the OS-9 environment -- the program stops with "TERM
environment variable not set". `SYS/login` is what sets it.

Of the rest: 22 never took the screen (they need an argument, or exited), and
6 were not quit by q, Q, control-C, control-D, control-X control-C or ESC --
`digclk`, `draw`, `greed`, `sc`, `sh` and `vi_cio` still need a person.

31 of the 67 have a documentation directory, so the answers are mostly on
the disk already. **Do not generate these automatically without testing.** A regex over the
manuals produced five candidates and at least three were wrong -- it matched
MicroEMACS's `!RETURN` macro directive and `sh`'s line-editing description as
if they were quit keys. Each note has to be read out of the manual by a person
and, where the program can be driven from a pipe, tried.

## Still broken, with the diagnosis so far (2026-08-16)

- **hack** -- "Cannot get status of hack." and stops. The `%s' is literally
  `hack', not the player and not a path, and it does not change with USER or
  `-u'. Its playground is complete (record, data, help, hh, rumors, three
  bones files) and running from inside it makes no difference. The string sits
  next to "Saved level" and a `l%02d%02d%02d' filename pattern, so it is
  probably stat'ing a lock or level file it expects to find beside itself.
- ~~gnuchess, gnuchessn, jargon~~ **SOLVED, and it was six programs, not
  three.** They share a termcap library that reads TERMCAP as the CAPABILITY
  STRING, not as a filename -- which is why no file, however correct, ever
  satisfied them. `SYS/termcap.entry` holds one in that form; source it and
  **gnuchess, gnuchessn, jargon, hexedit, sc and vi_cio** all draw. Proved by
  running each.
- **top** -- draws its header, then E_PRCABT(228).
- **digclk, draw, greed, sc, sh, vi_cio** -- hold the screen and are not quit
  by q, Q, control-C, control-D, control-X control-C or ESC.

## Re-tested with SYS/termcap.entry, 2026-08-16

Of the 29 that had not held the screen, most were never broken -- they want an
argument and say so: `EditLibr`, `crypto`, `hexedit`, `infocom.tcap`,
`ispell`, `less`, `spiff`, `vis`. Those now have how-to notes.

Genuinely still wrong:

- **top, digclk, draw** -- draw something, then `E_PRCABT(228)`, process
  aborted.
- **greed, suicide** -- start and produce nothing at all.
- ~~hack~~ **SOLVED, and it was how it is invoked.** hack chdirs into its
  playground and then stats **argv[0]** to date-check saved levels. Run as a
  bare `hack` off PATH, argv[0] is just "hack", which cannot resolve from
  inside the playground -- hence "Cannot get status of hack." Run it by its
  full path and it starts:

      /dd/CMDS/GAMES/hack
      Are you an experienced player? [ny]

  `larn` and `ularn` behave the same way and also start. rdoggett called it:
  a configuration issue, not a broken binary. Two of my earlier attempts were
  worthless for a reason worth remembering -- bash's `cd` only tracks the path
  as a string, so "run it from the playground" never actually happened.
- **pow** wants a controller at `/x1`, and **initvdu** wants particular VDU
  hardware. Neither is a defect; both are noted as needing the machine.

## An os9exec bug, found by running ADL (2026-08-16)

`adlrun` reading a compiled world from a HOST-DIRECTORY mount stops with

    Assertion failed: (buffer!=NULL), function pFread,
    file fileaccess.c, line 336.

The same world on an RBF image plays. So os9exec's host-directory read path
has a case ADL reaches and RBF does not -- worth a look in
Source/OS9exec_core/fileaccess.c. Reproduce:

    adlcomp /dd/ADL/DEMOS/tiny.adl -o /h6/tiny -i /dd/ADL   # /h6 a host dir
    adlrun /h6/tiny                                          # asserts
    adlcomp ... -o /dd/tmp/tiny ... ; adlrun /dd/tmp/tiny     # fine

## Getting WN to actually serve -- how far it got (2026-08-16)

Everything on this side is done and shipped:

- document root at `/h0/c/unid/wn_1.14.3/osk` (the path compiled into the
  binary), with an `index.html` and a WN `index` file
- `wndex` builds the cache: *"Wrote cache file .../index.cache"*
- `mime.types` in `/h0/c/unid/wn_1.14.3/lib`, where wndex looks for it
- the log directory, so `wn` starts and opens `wn.log`

**os9exec CAN do sockets.** `Source/OS9exec_core/network.c` implements
`SS_Bind`, `SS_Listen`, `SS_Accept`, `SS_Connect`, `SS_Recv`, `SS_Send` --
this is not a dead end.

Two things stop it:

1. **`inetd` needs the `inetdb` module** or it stops with "tcp protocol
   unknown". `inetdb` is Microware's, it lives on the SDK boot disk at
   `CMDS/BOOTOBJS/SPF/inetdb`, and it is NOT covered by the permission we
   have (that names cio, math, math881, csl, csl020 only). A user with OS-9
   networking has one. Supplying it does clear the error.

2. **With `inetdb` present, `inetd` dies in os9exec's allocator**:

       No more memory !!!
       Process   Pid: 2, inetd, edition 7
       Exit code: E_BUSERR(102) bus error TRAP 2 occurred

   Unchanged by `-m 4M`, `-mm 4M`, `-M 128M`. os9exec's own comment at
   `memstuff.c:172` says that message is ambiguous -- it is printed both
   when the 68k arena is exhausted AND when the memtable (MAX_MEMALLOC) is
   full -- "the cause is genuinely ambiguous once you are down there". The
   bus error immediately after suggests inetd does not check the failed
   allocation and dereferences it.

   **DIAGNOSED, and it is neither.** The `-d 0x60` trace puts the failure
   inside `F$Link "inetdb"`, immediately after the module loads cleanly:

       # load_module: allocated memory 2008 @ 0x720a447f40
       # load_module: Name of module loaded='inetdb'
       No more memory !!!

   That is `adapt_inetdb()` in `modstuff.c`, which reads a start and an end
   pointer for the module's "hosts" field at fixed offsets and allocates the
   difference:

       b0 = mh + os9_long(*(uint32_t*)(mh + OFFS_HOSTS));      /* 0x34 */
       bL = mh + os9_long(*(uint32_t*)(mh + OFFS_HOSTS + 4));  /* 0x38 */
       size = bL - b0;
       v0 = get_mem(size);
       memcpy(v0, b0, size);

   In the SDK's inetdb, word 0x34 is **0x0100000D** -- not an offset into a
   2008-byte module -- and word 0x38 is 0x74. So `size` comes out
   **4,278,190,183** (a negative difference read as unsigned), `get_mem`
   refuses it, and the NULL goes straight into `memcpy` -- which is the
   `E_BUSERR(102)` a line later.

   Checked all three inetdb modules on the SDK disk (`inetdb`, `inetdb2`,
   `BOOTOBJS/SPF/inetdb2`): every one gives a bogus size, because they are
   **SPF** (SoftStax) modules, while `adapt_inetdb`'s comment says it expects
   the one from the **ISP** (Internet Support Package). Different product,
   different layout, same name.

   Two separate fixes, both small:

   - **os9exec should not trust those offsets.** Bounds-check b0 and bL
     against the module's own length, and check `get_mem`'s return before
     the memcpy. Today a wrong-variant inetdb is an unexplained
     "No more memory" and a bus error.
   - **To actually serve, an ISP-layout `inetdb` is needed.** None is on the
     SDK disk here and none is in the 464-file pool.

Reproduce:

    cp <SDK>/CMDS/BOOTOBJS/SPF/inetdb /tmp/net/
    os9exec -m 4M -r /dd/CMDS/WN/inetd 8080 /dd/CMDS/WN/wn
    curl http://127.0.0.1:8080/

