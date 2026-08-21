# Rebuilding pdksh (ksh) from source

Everything here exists because `notes/HANDOFF.md` recorded the pdksh rebuild as
**blocked on material that does not exist here** — `osklib.r`, which its
`dmakefile` links, was said to be "not on the disk, in the SDK, or in the
pool". That was wrong, and the reason it was wrong is worth keeping.

## What was actually missing

`osklib.r` is not a file anybody ever shipped. It is a **build product**,
`merge`d from 21 object files, and its sources were in the pool all along, in
`microware-archive/SHELLS/pd_ksh.e11.lzh`.

The import into `disk/SRC/pdksh/` took `sh/`, `std/`, `etc/`, `machines/`,
`Makefile` and `manifest` — and dropped the entire `OSK/` directory except
`OSK/INCL`, which it renamed `OSK_INCL`. So the disk carried the port's
`#include`-fragments and none of the port itself: no `OSK/SRC` (osklib), no
`OSK/DEFS` (17 headers), no `OSK/DOC/Readme.osk`. **The shipped source tree
could not be built by anyone**, and the earlier note that `OSK_INCL` "holds
what look like its sources" was a reasonable guess at the wrong directory.

`disk/SRC/pdksh/OSK/` now holds the recovered tree, all of it.

Two headers — `DEFS/ioctl.h` and `DEFS/termios.h` — were refused at first and
then RESTORED the same day, and the round trip is worth recording. Both matched
a file under `play/oskBoot`, which is a WORKING BUILD OVERLAY, not a pristine
SDK. Neither `ioctl.h` nor `termio.h` is in the pristine tree at all, and no
copy of either carries a Microware copyright. They are the standard System V
definitions, which is exactly why they overlap. `screen_microware.py` now says
which SDK a match came from, so the difference is visible instead of having to
be remembered. German comments in `ssmpermit.a`, `ssmprotect.a` and
`SAMPLE/envi.ksh` were transliterated to ASCII (`ä`→`ae`), because the disk is
7-bit by rule.

The port is Heike C. Zimmerer's, edition 11, based on pd-ksh v4.3 from Usenet;
`OSK/DOC/Readme.osk` is his. `OSK/CMDS/ksh` in the archive is **byte-identical
to `disk/CMDS/ksh`**, so the shipped binary is this archive's, unmodified.

## The recipe that works

Needs `OS9CLEAN` from `tools/rebuild/make_overlay.sh`.

    OSK/SRC:  cc -r <each>.c -V=<OSK/DEFS> -V=<COMPAT> -V=/dd/DEFS \
                  -DKSH -DDT_INET=9
    sh:       cc -r <each>.c -V=<OSK/DEFS> -V=<COMPAT> -V=/dd/DEFS \
                  -D_SYSV -DBIT8 -DDT_INET=9 -DUSE_SIGNAL -DNSIG=255 \
                  -Dopendir=_x_opendir -Dopen=_x_open \
                  -Daccess=_x_access -Dcreat=_x_creat
    then:     merge the 21 osklib objects  -> osklib.r
              merge the 26 sh objects + osklib.r -> kshobjs.r
              cc kshobjs.r -qm=32k -n=ksh -f=<out> -l=/dd/LIB/os9lib.l

`merge` is the SDK's; the OS-9 shell truncates a command line long before 47
filenames fit, which is why the `dmakefile` merges rather than passing them all
to `l68`. **The shell's `>` will not overwrite** — `E_CEF (218)` — so delete
the target first or you will silently keep measuring the previous build.

Use ONE include path for every object. Compiling some with `std/stdc` on the
path and some without gives different translation units different `time.h`,
`stdlib.h` and `limits.h`, which is a struct-layout mismatch waiting to happen.
`limits.h` is the only header `std/stdc` was needed for; a copy in `OSK/DEFS`
settles it.

## Fixes in this directory, and why each is needed

  - **`time.h`** — v2.4's `<time.h>` defines `struct sgtbuf` and has no
    include guard, and `OSK/DEFS/SYS/types.h` reaches it by absolute path
    (`/dd/defs/time.h`) so cpp cannot tell it is the same file as a plain
    `<time.h>`. Any file including both gets every member redefined. The shim
    goes in `OSK/DEFS`, which leads the include path, and includes the real one
    once. `OSK_DEFS_SYS_types.h.patch` routes types.h through the search path
    so the guard actually applies.
  - **`OSK_SRC_setvbuf.c.patch`** — `stdio.h` declares `setvbuf()`, implicitly
    int; the port defines it `void`, which this compiler calls a declaration
    mismatch.
  - **`sh_tree.c.patch`** — `os9unix/varargs.h` expands its `type` argument
    seven times inside a nested `?:`. Two `va_arg`s on one line, one of them
    with the two-token type `unsigned int`, **aborts cpp outright** —
    `E_PRCABT`, no diagnostic, just a dead process. One per statement, same
    meaning.
  - **`sh_sh.h.patch`** — the `dmakefile` passes `-DSHELL="ksh"` and
    `-DSHELLENV="SHELL=ksh"`, whose embedded quotes do not survive being typed
    at the OS-9 shell. `main.c` needs `SHELLENV` unconditionally.
  - **`memmove.c`** — not in the K&R library; `vi.c` needs it 17 times and
    `emacs.c` 4, every one an overlapping slide inside an edit buffer.
  - **`vfprintf.c`** — there is no v-printf family at all in this library, and
    no `_doprnt` to build one on. `io.c`'s `shellf()` and `errorf()` need it.
    Read its header comment before touching it; it is safe for a stated reason,
    not by luck, and pdksh prints no floating point anywhere (checked).
  - **`sh_lex.c.patch`** — **the reason to care about any of this.** It reads
    the command line a byte at a time instead of asking for 256, which is what
    makes `ksh` usable on an os9exec that does NOT have the `I$Read`
    end-of-record fix. See `notes/OS9EXEC-IREAD.md`.

## Where it stands — one bug left, and it is well cornered

The build completes. `ksh` links at ~137 KB, is correctly named, carries no
author stamp, and **starts**. `cd`, assignments and `print` all work.

**Every command that is an alias aborts** with a bus error reading address
`$FFFFFFFF` — `MOVE.B (A0,-1),D0` with `A0 = 0`, i.e. the byte before a NULL
string. `echo`, `true` and `pwd` fail; `print`, `cd` and `x=5` do not. Those
three are exactly the aliases `main.c` installs in `initcoms[]`
(`echo=print`, `true=:`, `pwd=print -r "$PWD"`), so the alias entries are being
created with a null value and something then reads the character before it.

Ruled out by experiment, so do not re-test these:

  - **Not the `lex.c` patch.** Rebuilt with pristine `lex.c`: identical abort.
  - **Not trap-free vs `cio`.** Built both ways (`-qm=32k` and `-i -m=10`):
    identical abort.
  - **Not the include-path inconsistency.** Fixed and rebuilt: identical abort.
  - **Not `$ENV`.** Setting it changes nothing.

Start at `c_ksh.c`'s `c_alias` and how it stores a value, and at `table.c`'s
`tenter`. The shipped binary from the same archive does not have this fault, so
it is the build, not the sources.

## The thing to know before spending a day on this

`OSK/INCL/ijobs.c` — the port's `fork()` emulation — re-execs the shell as
`ksh -__child__` and has the child **read the parent's address space directly**
via `ssmpermit`/`ssmprotect` (`F$Permit`/`F$Protect`). That is how it inherits
the environment and the command tree. Whether os9exec emulates SSM at all is
unknown and untested. So a rebuilt `ksh` may well start and still not fork,
and this port may not be reachable on this emulator no matter how the alias
bug goes.

**`ksh` already works on this collection** via the os9exec `I$Read` fix. This
rebuild is worth finishing only for the case that fix is never committed — it
would make the collection self-sufficient on a released emulator. Judge it
against that, not against "ksh is broken", because it is not.
