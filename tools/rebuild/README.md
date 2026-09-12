# Rebuilding the freeware disk's programs

Everything on the freeware disk that could be rebuilt from source has been,
so that no binary carries the author stamp from the SDK copy it was first
built with. This is the machinery that did it, kept so the next person does
not have to rediscover 200 build recipes.

```sh
export OS9CLEAN=/path/to/clean-dd-overlay          # see Prerequisites
./rebuild.sh recipes.psv <source-pool> [<pool2>]   # builds R_<prog>, installs nothing
./verify.sh  <results.tsv> <source-pool> [<pool2>]
```

`rebuild.sh` installs nothing on purpose. It writes `R_<prog>` beside each
program's sources and a results table; you decide what gets copied onto the
disk, after `verify.sh` has run each one.

## relink_cio.sh has a gate, and it is the point of the script now

`-qixm` links the SDK's `LIB/cio.l`, and that library is the **$44 vintage** —
the one whose `putc`/`getc` are macros calling trap-13 selectors `$41`/`$42`,
where every `cio` *module* anyone has puts a memory routine. A relinked
program is therefore a $44 program: if it ever runs one of those macros on a
`FILE` it opens your file, reads not one byte, and reports on it anyway.

Eleven programs shipped broken that way and were rebuilt `-qm` on 2026-08-31
to fix them. `relink_cio.sh` now asks `tools/cio_macro_scan.py` first and
**refuses** any program the scan names, rather than reporting it and leaving
the judgement to whoever reads the results — which is what shipped
`CMDS/REBUILT/kermit_cio`, a relink carrying the call sites and the one build
of kermit here that could only be driven in send mode.

It also refuses to run at all if the scan names nothing, because a scan that
has stopped working leaves the gate open and looks exactly like a clean disk.

## recipes.psv

One line per program, `|`-separated:

    prog|srctree|sources|defines|extra libs|extra cc flags

`|` rather than TAB is deliberate. Tab is an IFS *whitespace* character, so
bash collapses runs of them, and a program with no defines silently shifts its
libraries into the defines field — which is how twenty builds came to be
compiled with `-D/dd/LIB/math.l`.

The source tree is named by **archive**, not by program: `divutils` holds
`gen`, `run` and `if`. `freeware/DOC/ORIGINS` is the map.

## Prerequisites, none of which are in this repo

- **`OS9CLEAN`** — a `/dd` overlay: symlinks to the OS-9 system disk for
  everything except `LIB`, which is a real directory whose `cstart*` copies
  have their 64-byte `Author` psect overwritten with spaces. `cc` links
  `cstart.r` into every C program, so without this overlay every binary is
  stamped with whoever owns the SDK copy. Do not substitute a stock Microware
  `cstart` — this `l68` rejects it as *"created by assembler too new for this
  linker"*.
- **`OS9COMPAT`** — headers OS-9 does not ship (`string.h`, `pwd.h`, …).
  Defaults to `freeware/SRC/COMPAT`, which is on the disk.
- **`gtimeout`** — coreutils. macOS has no plain `timeout`, and a sweep built
  with one completes in seconds having compiled nothing.

## The SDK's cstart is untagged at source now -- REMAKE YOUR OVERLAY

2026-08-27: `$SDK/LIB/cstart.r` was replaced with a build carrying no
licensee banner at all (the tagged original is kept beside it as
`cstart.r.tagged-orig`). It is 1274 bytes against the tagged 1355, and it is
the same generation -- assembling `cstart.a` with the Author block removed
reproduces it.

Two consequences, both measured here:

- **A rebuild comes out 68 bytes shorter than the same source built through
  an older overlay.** `load` built through an overlay made before that change
  is 17084 bytes; through one made after, 17016. Nothing else differs. If a
  size you recorded earlier no longer reproduces, this is why -- check the
  overlay's date before suspecting the source.
- **`make_overlay.sh` no longer requires that it found a stamp to blank.**
  It used to exit with "no author stamp found in any LIB file", which would
  have turned the improvement into a hard failure the day the SDK arrived
  clean. What it checks now is the invariant that matters: that no stamp is
  left in `LIB` when it finishes. The numbered `cstart.1/.23/.45/.67` are
  still tagged, so it still has work to do.

## Two flags that are not optional

**`-qm`** is the default, and **this is not a size preference.** It links
stdio into the module. `-qixm` links the `cio` trap handler instead and makes
a much smaller binary that DOES NOT WORK. Measured 2026-08-27, against the SDK
overlay and its own matched `csl`:

    putchar.c -- putchar('x') 4000 times
      -qixm    1532 bytes     0 characters written, 3888 x "No more memory !!!"
      -qm     13040 bytes     4000 characters, correct

Eight times the size buys a program that produces its output. There is no
trade to weigh.

**It is not this collection's version skew, either.** That run used the SDK's
own `csl`, not the older edition this disk ships, and it failed the same way.
Whether the fault is os9exec's `F$SRqMem` handling or `cio`'s ABI is
**unsettled** -- `notes/os9exec-bugs/` has the reproduction and the trace.
Either way `-qixm` cannot be the default for anything installed.

The 367 starred ARCHIVE binaries are unaffected and `cio` keeps shipping for
them: their authors linked them against their own runtime, and 621 programs
run bare. This is about what WE build.

**`MEM=<size>`** sets the module's memory allocation, which on OS-9 is where
the STACK lives. The default is 16k and that is not always enough: `life`
drew one generation and died with `**** Stack Overflow ****` until it was
given `MEM=64k`, after which it runs indefinitely and detects its own
oscillator period. If a program dies partway through a run rather than at
startup, and especially if it recurses, try this before anything else --
it costs memory per process and nothing else.

`TRAPFREE` in a recipe is now a no-op, kept so the six recipes carrying it
still parse. `CIOLINK` opts a single build back into `-qixm` for a deliberate
experiment -- never for anything installed.

**This changes only what lands in `built/`.** The driver installs nothing, so
`DOC/INDEX`'s star grid does not move until somebody installs one on purpose;
at that point the star list has to be re-measured, and it is measured by
RUNNING every program against a disk with cio removed. Never by looking for a
`cio` string in a binary -- that was tried again on 2026-08-24 and reports
"no" even for `cat`, which is starred.

**`-n=<prog>`** names the module. Without it the module name comes from the
`-f` output filename, and since builds go to `R_<prog>` to avoid clobbering an
archive's own prebuilt binary, every program ends up reporting itself as
`R_make` in its own usage message. 203 modules had this before it was caught.

## Shims

`shims/` holds small documented replacements for functions OS-9's K&R library
never had — `bcopy`, `getpwuid`, `geteuid`, `srand48`, `popen`. `rebuild.sh`
retries once with the matching shim when a link fails on one of those names.

It adds shims one at a time and keeps going while each round names one it has
not already tried, so a program that wants two gets two: `lwf` needs
`getpwuid` and `popen` both. The shims are removed from the tree afterwards —
they are the driver's, not the archive's, and a copy left behind would ship on
the disk as if the port had always carried it.

Before writing a shim, look in `LIB` first. `rename` is not in `clib.l` and
looks exactly like a missing-function case; it is in `os9lib.l`, which the
recipe can simply ask for. A shim written for it used `link()`, which OS-9 has
no more than it has `rename()`, and the build failed one symbol further on.

## What a failing build usually means

In rough order of how often it was the answer:

| symptom | cause |
|---|---|
| `Symbol 'x' unresolved` | the makefile rule lists only the sources *that rule* needs. Add the rest of the tree's non-`main` `.c` files. |
| `duplicate symbol names` | the opposite — a full-tree link pulled in another program's `main`, or a compat source the C library already provides (`make`'s `mktime.c`). |
| `can't open <header>` | sources are in a subdirectory, or the header wants `SRC/COMPAT`. |
| `undeclared identifier` | a conditional-compilation arm. Read the `#ifdef` maze before adding anything: `make` needs `-DOS9` because `union wait` is in the `#ifndef OS9` branch. |
| `*** error - value out of range ***` | this is **r68**, the assembler, not the compiler. `-K=2L`. |
| `source line too long` | an LF-terminated file. OS-9 text is CR-terminated, and `cpp` reads an LF file as one enormous line. This bites files you wrote yourself. A macro whose continuation lines join into something very long does it too — that is `ed.h`, and there `cpp` said so 161 MB worth. |
| `can't open /dd/DEFS/sys/types.h` | `cpp` does not search the `-V` directories for an include name that has a DIRECTORY in it. `SRC/COMPAT/sys` is copied into the overlay's `DEFS` by `make_overlay.sh` for exactly this — **but the general answer is `CPP2`**: GNU cpp does search `-I` for such names, which is what unblocked `rayshade` and `macutils`. |
| `Symbol 'main' unresolved`, or a symbol you can see in a named source | two sources in the recipe share a BASENAME. On the CPP2 path `tmpbase()` keeps them apart; on the plain-cc paths `cc -r` names the object after the source and they still collide, so give such a recipe `CPP2`. |
| a tool says `file not found` about a file it is WRITING | **an OS-9 name stops addressing at 27 characters** — re-measured 2026-08-31 on both a host-directory mount and a fresh RBF image. 27 opens; 28 is the dangerous one, because on RBF `makdir` CREATES it and reports success while only the 27-character prefix can ever reach it afterwards; 29 and longer are refused outright. This row said 29 until then, from a 2026-08-23 measurement that has not reproduced. `cccp2` reports a too-long output name exactly like a missing input, and the shell's abort-on-error then ends the run at the first source with nothing to say it did. |
| a header that IS in `SRC/COMPAT` still "can't open" | `$OS9COMPAT` is not set. `tools/build.sh` sets it; calling `rebuild.sh` directly used to fall back to a path that has not existed since this repo was split out. |
| the error names something that is not on the command line at all | **SCF will not read a line longer than 512 bytes** — that is the OS, always has been, and there is nothing to fix. A longer command line arrives cut off. `mtools` has 45 sources and its `cc` line ran to 900 characters; it was cut mid-option and the error was `can't open /dd/DEFS/stdlib.h`. `rebuild.sh` measures the line it is about to type and compiles each source separately when it would be too long. |
| unresolved symbols that are plainly IN the link | `l68` makes **one pass** per DISTINCT library FILE. A member calling another member further down the file is left unresolved — `zoo`'s `huf.c` wanted `putbits` from `io.c` 24 times. **Repeating `-l=x.l` does NOT buy another pass** (measured 2026-08-23 on mtools: five repetitions changed nothing). Give l68 COPIES under different names, which is what `compile_gcc` does. |
| `E_BUSERR` from `cpp` itself | a source line of **513 characters or more** — measured, 2026-08-23. Nesting is not the cause, it is just how a line usually gets that long. Use the `CPP2` flag. See `notes/CPP-MACRO-CRASH.md`. |
| `cpp` reports nothing and the build fails anyway | in some shapes it does not crash on an over-long line, it **truncates and exits quietly**. Check the size of the `.m`, not the exit status. |
| `**** input line too long ****` from `c68` | **1023 characters or more** — measured, same day. Only reachable through the `CPP2` path, because GNU cpp splices the backslash-newline continuations Microware's cpp keeps. `cpp2_fixup` re-wraps for this. |

## The four recipe flags

These four words are read out of the defines field and never reach `cc` as a
`-D`. They compose: `djpeg` uses `KNR` and `CPP2` together, and `gtar` would
use `KNR=<files>` with `CPP2`.

| flag | what it does |
|---|---|
| `NOOSK` | drop the `-DOSK` every other recipe gets |
| `KNR` | run every source through `ansi2knr` first |
| `KNR=a.c,b.c` | run only those sources through it |
| `CPP2` | preprocess with GNU's `cccp2` instead of Microware's `cpp` |
| `LONGREF` | `c68 -k` for long PC-relative branches, and NO `o68` pass |
| `M020` | the 68020 backend, `c68020`/`r68020`, for oversized stack frames |
| `GCC` | build with the disk's own GCC 2.5.6, which is what several ports were written for |
| `TRAPFREE` | link stdio into the module (`-qm`) instead of using the `cio` trap handler |

`CPP2` is worth reaching for beyond the 512-character line it was written for:
it also searches `-I` directories for an include name containing a DIRECTORY,
which Microware's cpp will not do, and it is the only path whose temporaries
survive two sources sharing a basename.

## ANSI C: the KNR flag

Microware's `cc` is K&R and will not read a prototype, which is what stops
`lua`, `jpeglib`, GNU Chess 4.0, `ed` and `lout`. `ansi2knr` -- the standard
de-ANSIfier, from the JPEG distribution, itself written in K&R so it
bootstraps -- **builds here**, and a recipe with `KNR` in its defines runs
every source through it before `cc`.

**KNR ON AN ALREADY-K&R TREE IS HARMFUL, not merely useless.**  Measured on
`reversi` (2026-09-12): with `KNR` in the recipe, `cc` reported `**** multiple
definition ****` on every ordinary K&R parameter declaration --
`main(argc, argv) int argc; char **argv;` and five more like it, across two
files -- and the same sources compiled cleanly with the flag removed.
ansi2knr rewrites a definition it has already rewritten, and the duplicate
parameter declarations are what c68 then objects to.  So reach for `KNR` only
when a prototype is actually stopping the build, and take it out again the
moment the errors change shape.  Its symptom is distinctive: `multiple
definition' pointing at a line that is plainly correct K&R.

**ansi2knr only sees a function whose NAME IS AT THE LEFT MARGIN.** Its own
header says so:

> ansi2knr recognizes functions by seeing a non-keyword identifier at the left
> margin, followed by a left parenthesis ... the function name must be the
> first thing on the line.

JPEG writes the return type on its own line and the name at the margin, so
ansi2knr converts it. `mtools` and `lua` write `static void f(void)` all on
one line -- that begins with a keyword, ansi2knr skips it, and every prototype
reaches c68 intact. This is a code-style limit, and it is the FIRST thing to
check before reaching for the flag; the tree's config header is the second.

Counting, per tree, headers with the name at the left margin against those
starting with a keyword: JPEG 348/12 (reachable), mtools 3/477, lua 1/236
(not). **The count alone does not settle it**, because a K&R definition also
has its name at the left margin -- `ed` scores 118/0 and is not an ANSI tree
at all. The count says whether ansi2knr will TOUCH a tree, not whether it will
help.

**`ansi2knr` is only safe on a tree that is ANSI throughout.** Given a K&R
definition whose parameters are declared on the lines *after* the header --
which is the ordinary K&R shape --

    int
    wildmat(s, p)
        register char   *s;
        register char   *p;

it reads `s, p` as an ANSI parameter list and emits

    wildmat(s, p)  s; p;
        register char   *s;

adding two `int` declarations that then fight the real ones. gtar came back
from a blanket `KNR` with more damage than it started with. Where a mostly-K&R
tree has a handful of ANSI definitions, name them: `KNR=create.c,list.c`. A
source that is NOT translated compiles under its own name, so its object is
`<base>.r` rather than `ctmp_<base>.r`, and the merge list follows.

    tools/build.sh ansi2knr        once, first: make_overlay.sh takes it
                                   from built/ into the overlay

It rewrites function DEFINITIONS and leaves headers alone, so a tree's own
config header still has to stop declaring prototypes. For JPEG that is
`jconfig.h`: `HAVE_PROTOTYPES` off, `const` defined empty, `HAVE_STDDEF_H` on
(`size_t` is only there, and `jpeglib.h`'s `size_t free_in_buffer;` is the
first thing that fails without it).

Status: 26 of jpeglib's 27 sources compile this way. `jccoefct.c` does not --
`coef->whole_image[0]`, an array of pointers to an incomplete struct, draws
"undefined struct/union tag referenced" and "can't determine size". Nothing
else in the tree does that, and it has not been run down.

## Do not edit a script while it is running

`bash` reads a script by BYTE OFFSET as it goes. Editing `tools/build.sh`
during a 40-minute full build shifted every offset after the edit, and the
running copy died with a syntax error on a line that is perfectly good — after
the last program was built and before the tidy-up, so it left 440 modified
object files behind and reported nothing. The file was never wrong; `bash -n`
said so immediately.

The same applies to `rebuild.sh` and to this repository's other long-running
shell scripts. Wait, or copy the script and edit the copy.

## Verify, and check that the check can fail

`verify.sh` runs each module and rejects it if the module name does not match
the filename, if it is stamped, or if it will not fork. Empty output is its
own verdict (`NOOUTPUT`), never a pass — an earlier version lost `tr` from
`PATH`, so its capture was always empty, the "can't execute" test could never
match, and it reported 20/20 OK having run nothing.

Two more checks in this work reported confidently wrong results, both because
a pool path moved underneath them: the driver called 38 successes "38 FAIL"
while the binaries sat on disk, and the verifier called 23 good modules "23
FAIL". Before believing a sweep, break something on purpose and confirm the
number moves.

## Building against os9lib

`LIB/os9lib.l` is A. Seyama's OSK library, and its `stat()` is the only one
here that tells the truth -- distinct inodes, real sizes, real dates. `ls` and
`gtar` both need that, and both reach it the same way:

    -V=/h7/OS9LIB -V=/dd/DEFS/os9lib -V=/h7

in that ORDER, with `/dd/LIB/os9lib.l` in the libs field. Three things make
the order load-bearing:

  - `COMPAT/OS9LIB/sys/stat.h` has to be found before COMPAT's own, which
    routes `<sys/stat.h>` to `<UNIX/stat.h>` and its `<modes.h>` -- and
    os9lib's `<stat.h>` stops with `#error Can not include both stat.h and
    modes.h.`
  - `COMPAT/OS9LIB/fcntl.h` has to be found before os9lib's, which ends
    `#define open unix_open` / `#define creat unix_creat` and expects a
    companion **no library on this disk carries**. It keeps os9lib's `O_*`
    values -- they are OS-9's own access modes, `O_RDONLY` is 1 and not
    Unix's 0 -- and drops just the two renames.
  - os9lib's DEFS has to come before COMPAT for everything else.

A recipe doing this must NOT also `-D` the `S_IF*` names: os9lib's `stat.h`
reads a defined `S_IFMT` as proof that `modes.h` got there first and stops
with that same `#error`.

**os9lib's `stat()` sign-extends the attribute byte.** A directory (`0xbf`,
bit 7 set) arrives as `0xffbf` and a plain file (`0x1b`) as `0x001b`. Only the
low byte means anything, and within it only bit 7 says anything about type --
so `S_ISDIR` is `(m & 0x0080) != 0` and there is no separate regular-file bit
to test. An `S_IFMT` of `0x0380` matches the sign fill instead of the type,
which is what made `ls -l` print a directory instead of listing it.

## ASM -- assembling a module with r68

One recipe uses it, `aterm`, and it comes out **byte-for-byte identical to the
binary that ships**. That is the strongest check this machinery has produced,
so it is worth writing down what it took:

  - **No cstart.** An assembly module carries its own psect: type, language,
    attributes, edition, stack, entry point. l68 gets the object and two
    libraries and nothing else.
  - **`-l=/dd/LIB/os9.l -l=/dd/LIB/sys.l`.** ATerm refers to 53 names it does
    not define -- `F$Fork`, `I$GetStt`, `SS_Opt`, `PD_BAU`, `E$CEF`, `C$CR`
    and the rest. Microware's assembler definitions file would supply them and
    **is not in this SDK copy**: `DEFS/oskdefs.d` here is 1470 bytes and holds
    only the module-type, attribute and permission equates. Those two
    libraries resolve all 53. Without them the link fails on every one and
    reads exactly like a missing header.
  - **`MODNAME=`, and its case.** The file is `aterm`, the module inside is
    `ATerm`. With `-n=aterm` the result differs from the shipped binary in
    five bytes: two of the name, and the three CRC bytes that follow from it.
  - `use <name>` resolves to `/dd/defs/name`, which is how every assembly
    source here reaches `oskdefs.d`.

## `clean` means it compiled and linked. Nothing more.

`build.sh` prints `clean` when a module came out the other end. It is not a
claim that the program works, and on 2026-08-24 that distinction cost a real
bug: `mtools` had been in the known-good set for weeks, building `clean`
every time, and the binary printed

        1 file(s)      bytes

where the one that ships prints

        1 file(s)               139 bytes

`mdir.c`'s `dotted_num()` asks `sprintf` to pad an INTEGER to a precision --
`"%.*ld"` with a width of 26. **No C library on this disk does that.**
Measured, all four: `clibn`, `clib`, `cio` and `os9lib` each answer `139` for
`%.26ld`. `len` comes out 3, and the function returns `buf + 3 - 13` -- ten
bytes before its own buffer.

The only thing that found it was building the program and **running it beside
the binary that ships**. Do that for anything you add a recipe for. Where
there is no shipped binary to compare against, say so rather than letting
`clean` stand in for `works`.

