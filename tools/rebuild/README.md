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

## Two flags that are not optional

**`-qm`** makes the binary trap-free: no `cio`, no `math` trap handler. That
is what lets these run on a disk with no Microware SDK on it. Never `-qixm`.

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
| `can't open /dd/DEFS/sys/types.h` | `cpp` does not search the `-V` directories for an include name that has a DIRECTORY in it. `SRC/COMPAT/sys` is copied into the overlay's `DEFS` by `make_overlay.sh` for exactly this. |
| a header that IS in `SRC/COMPAT` still "can't open" | `$OS9COMPAT` is not set. `tools/build.sh` sets it; calling `rebuild.sh` directly used to fall back to a path that has not existed since this repo was split out. |
| the error names something that is not on the command line at all | **SCF will not read a line longer than 512 bytes** — that is the OS, always has been, and there is nothing to fix. A longer command line arrives cut off. `mtools` has 45 sources and its `cc` line ran to 900 characters; it was cut mid-option and the error was `can't open /dd/DEFS/stdlib.h`. `rebuild.sh` measures the line it is about to type and compiles each source separately when it would be too long. |
| unresolved symbols that are plainly IN the link | `l68` makes **one pass** over a library. A member calling another member further down the file is left unresolved — `zoo`'s `huf.c` wanted `putbits` from `io.c` 24 times. Name the library more than once. |
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

## ANSI C: the KNR flag

Microware's `cc` is K&R and will not read a prototype, which is what stops
`lua`, `jpeglib`, GNU Chess 4.0, `ed` and `lout`. `ansi2knr` -- the standard
de-ANSIfier, from the JPEG distribution, itself written in K&R so it
bootstraps -- **builds here**, and a recipe with `KNR` in its defines runs
every source through it before `cc`.

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
