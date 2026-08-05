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

It handles **one** shim per program. `uwho` needs two (`getpwuid` and
`geteuid`), so it names them in its recipe's source list instead. If a program
fails on a second missing symbol after a shim retry, that is why.

## What a failing build usually means

In rough order of how often it was the answer:

| symptom | cause |
|---|---|
| `Symbol 'x' unresolved` | the makefile rule lists only the sources *that rule* needs. Add the rest of the tree's non-`main` `.c` files. |
| `duplicate symbol names` | the opposite — a full-tree link pulled in another program's `main`, or a compat source the C library already provides (`make`'s `mktime.c`). |
| `can't open <header>` | sources are in a subdirectory, or the header wants `SRC/COMPAT`. |
| `undeclared identifier` | a conditional-compilation arm. Read the `#ifdef` maze before adding anything: `make` needs `-DOS9` because `union wait` is in the `#ifndef OS9` branch. |
| `*** error - value out of range ***` | this is **r68**, the assembler, not the compiler. `-K=2L`. |
| `source line too long` | an LF-terminated file. OS-9 text is CR-terminated, and `cpp` reads an LF file as one enormous line. This bites files you wrote yourself. |

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
