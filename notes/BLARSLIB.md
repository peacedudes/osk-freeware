# blarslib — in, minus the Microware headers (rdoggett, 2026-08-22)

**What it is:** Bob Larson's Unix-compatibility library for OS-9/68k —
`getcwd`, `popen`, `putenv`, `getopt`, `alloca`, the BSD string functions, the
`v*printf` family. blarson@usc.edu. Its Readme says *"All may be distributed
for free."* `alloca` is credited to Doug Gwyn and many of the string functions
to Henry Spencer. Found in the pool at
`microware-archive/LIB/blarslib.tar.Z`.

**What shipped:**

  - `disk/SRC/blarslib/` — his source and the four headers of his own that are
    genuinely his (thin guards that include the real Microware header once).
  - `disk/DEFS/blarsdefs/` — those, plus one-line forwards **of our own** for
    the names his tarball carried as byte-identical copies of Microware's.
  - `disk/LIB/blarslib.l` — the built library, 21 KB.
  - `SOURCES.txt` records all of that.

**Thirteen headers of his did NOT ship**, because they were byte identical to
the SDK's or near enough: `assert.h`, `curses.h`, `errno.h`, `fileinfo.h`,
`pwd.h`, `sgstat.h`, `signal.h`, `string.h`, `strings.h`, `term.h`,
`terminfo.h`, `termio.h`, `varargs.h`.

**What that costs.** 31 of the library's 37 objects build. Six do not, and
they are the ones that needed the removed headers or a define the OS-9 shell
cannot carry:

    stat.c        wants <sgstat.h>
    getpw.c       wants <pwd.h>
    ftime.c makenv.c putenv.c    time_t, reachable with more include-path work
    gethostname.c its makefile passes -DHOSTNAME="name", quotes and all

**And macutils still does not build.** When this was proposed the claim was
that blarslib would unblock `macutils`, `mtools` and `gtar`. It has not:
`macutils/FILEIO/rdfile.c` uses `struct stat` as blarslib defines it, and
blarslib's `stat.c` is one of the six. Getting it would mean restoring
`sgstat.h`, which is Microware's structure definition and is exactly what was
excluded.

So the decision stands and the library is useful on its own terms; the
macutils argument for it turned out not to hold.

