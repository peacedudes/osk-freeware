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

## The alias crash: FOUND AND FIXED

**`strchr` here does not match the terminating NUL, and `lex.c` depends on it
doing so.**

`OSK/DEFS/osk.h` has `#define strchr index`, and the alias-expansion path in
`lex.c` reads the last character of an alias value to spot a trailing space:

    c = strchr(s->str, 0)[-1];

ANSI says `strchr` matches the terminating null and returns a pointer to it.
**OS-9's `index` returns NULL** for that search -- measured, with a five-line
program, not assumed:

    index("print", 0)  -> NULL
    index("print",'i') -> found

So the expression was `NULL[-1]`: a byte read at address `$FFFFFFFF`, a bus
error, on EVERY alias expansion. That is exactly the symptom -- `echo`, `true`
and `pwd` died and `print` and `cd` did not, because those three are the
aliases `main.c` installs in `initcoms[]` and the other two are not aliases at
all.

`sh_lex.c.patch` replaces it with `s->str[strlen(s->str) - 1]`, which is the
same value; `s->str[0]` is known non-zero immediately above, so the length is
at least 1.

**The crash is gone.** With the fix, `x=5; echo x is $x; true; echo status $?`
prints `x is 5` and `status 0` from a `-c` invocation.

Worth keeping in mind for the rest of this port: **any `strchr(s, 0)` in this
codebase is a latent bus error.** It is the idiom for "find the end", and it
does not work here.

## Where it stands — one bug left, and it is well cornered

**Some stdout is still lost**, and it is a different fault from the crash.
`print` and `echo` write with `putc` to `shf[1]`; error messages go through
`shellf` -> `vfprintf` to `shf[2]` and those DO appear. Observed with the cio
build:

    ksh -c "x=5; echo x is $x; true; echo status $?"   -> both lines, correct
    ksh -c "for i in a b c; do echo n=$i; done"        -> n=b and n=c, no n=a
    ksh -c "echo ALIAS FIXED"                          -> nothing
    ksh -c "print hello"                               -> nothing

So it is not simply "the first line is lost"; two-command sequences print
both. ### What the second fault actually is, as far as measurement goes

It is **not** the alias path. `ksh -c "print one; print two"` -- no alias in
sight -- prints only `two`. It is **the first command's output, whatever the
command**, and it is lost to a FILE as well as to the terminal, so it is not a
terminal artefact:

    ksh -c "for i in a b c; do echo n=$i; done" > file   -> n=b, n=c
    the shipped ksh, same line                           -> n=a, n=b, n=c

The decisive clue: **change `io.c`'s `setvbuf(shf[fd], NULL, _IOFBF, BUFSIZ)`
to `_IONBF` and each write emits exactly ONE CHARACTER** (`print one; print
two` prints `t`). Unbuffered should print everything. That is not a flushing
problem; that is the `FILE` structure being written through a layout the
library does not share.

Where to look, in order:

  1. **The FILE layout.** `std/stdc/stdio.h` declares its own `FILE`
     (`_ptr, _base, _end, _flag, _fd, _save, _bufsiz`) and osklib's
     `setvbuf.c` pokes `stream->_flag` directly. This build deliberately keeps
     `std/stdc` OFF the include path -- it shadows the SDK's `time.h` and
     `limits.h` -- so the compiler sees the SDK's `<stdio.h>`. If the two
     disagree about where `_flag` sits, every stdio call through this port is
     writing to the wrong offset. **Compare the two structs first.** It is one
     `diff` and it either explains everything or rules the theory out.
  2. **`setvbuf` itself is in `clib.l` and `clibn.l` as well as in osklib.**
     Which one the link chose decides whether `_IOFBF` allocates a real buffer
     or just clears a flag bit.
  3. **osklib's `fputc` had to be dropped**: it collides with `clibn.l`'s
     `putc_c` psect, and that psect also carries `fflush`. Dropping one
     changed which library object supplies the other.

### Ruled out by experiment, so do not re-test

  - **Not the `lex.c` read patch.** Rebuilt with pristine `lex.c`: same.
  - **Not the include-path inconsistency.** Fixed and rebuilt: same.
  - **Not `$ENV`.** Setting it changes nothing.
  - The crash and the missing output are **two separate faults**; fixing the
    first did not touch the second.

## The old section, kept because its ruled-out list is still valid

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
