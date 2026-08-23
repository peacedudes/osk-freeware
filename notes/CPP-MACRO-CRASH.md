# Microware's `cpp` bus-errors on a source line of 513 characters or more

> **The title of this file used to say "on nested macro expansion", and that
> was wrong.** Nesting is not the cause, it is just the usual way a line gets
> long. Corrected 2026-08-23 by measurement; the filename is kept because
> several other notes and the driver point at it.

Two limits govern the whole of this collection's building, and neither is
written down in any manual we have. Both were measured on 2026-08-23 by
feeding each tool one-line files of rising length:

| tool | limit | what happens past it |
|---|---|---|
| `cpp` edition 37 | **512 characters per line** | bus error at 513 — or, in some shapes, silent truncation |
| `c68` | **1022 characters per line** | `**** input line too long ****` at 1023 |

Both are per LOGICAL line: `cpp` splices backslash-newline continuations
before it counts.

## How the cpp limit was measured

A file of the shape

    main(){
    fputs ("yyyy...", stderr);          <- this line exactly N characters
    int j = 2;
    }

512 preprocesses cleanly. 513 and 514 both give

    # Exception: pid=3 vector=$02 err=#000:102

**It does not always crash, and that is what hid it.** Where the over-long
line was the whole program on one line, `cpp` instead wrote about a kilobyte
of output and exited with no diagnostic at all — 500, 1000, 2000 and 4000
character cases all produced the same 1110-byte truncated `.m`. An earlier
pass on this same file read those silent truncations as passes and concluded
that long lines were fine. They are not: **distrust a `cpp` run that reports
nothing; check the size of its output.**

## It explains the original reproduction exactly

`notes/cpp-macro-crash/` holds the three files this was first bisected to.
Expanding each of them (any preprocessor will do) gives:

| file | longest expanded line | limit | result |
|---|---|---|---|
| `crash5.c` | **542** | 512 | bus error |
| `ok4.c` | 270 | 512 | compiles |
| `ok5tiny.c` | 222 | 512 | compiles |

Five levels of nesting with a twelve-character body reaches 542 characters;
four levels reaches 270, and five levels of `a;` reaches 222. That is the
whole of the "neither depth alone nor expansion length alone" puzzle — it was
always just the length, and the two non-crashing cases are the two that come
in under 512.

The old note also recorded that a flat `#define` of 2000 characters, and one
continued over 8000, both compiled. They do, and that is consistent: a
`#define` is consumed by the directive parser and never becomes an output
line unless something expands it.

## Whose bug it is

`cpp`'s. A fixed-size line buffer overruns the same way on real hardware —
it would smash the same memory and take the same trap — and os9exec's part in
it is only to report it, which it does cleanly and with enough of a dump to
diagnose. Recorded here because rdoggett is exercising os9exec before
publishing, and because "the compiler died" is otherwise indistinguishable
from "the emulator died".

The register dump names the text it was chewing when the buffer went: on
gtar's `tar.c` the address registers held `$74732028` (`ts (`) and
`$6D61785F` (`max_`) — pieces of `fputs (` and `current_max_dfa_size`.

## The way round it, and the second wall behind it

**`CPP2`**, a recipe flag. GNU cpp 2.5.6 ships in the SDK as `cccp2` and has
no such limit. `rebuild.sh` runs it in `cpp`'s place and starts the chain at
`c68`. Three host-side edits between the two os9exec runs make that work, and
none of them is guessable:

  1. **Strip GNU's `# 1 "file"` markers.** A `.m` is a directive stream, and
     `c68` reads a leading `#` as a directive whose argument is the NEXT line,
     so each marker swallows a line.
  2. **Put a `#P<name>_c` preamble in front.** That is where `c68` learns the
     psect name; without it `r68` rejects every mnemonic in the file.
  3. **Re-wrap lines GNU cpp made too long** — the second wall. Microware's
     cpp KEEPS a source's backslash-newline continuations; GNU's splices
     them. gtar's `tar.c` usage text, written as forty continued lines, comes
     out of `cccp2` as 2113 characters on one, and walks straight into c68's
     1022.

**The re-wrap may only cut OUTSIDE a string literal**, because `c68` has
neither way of splitting a long one: adjacent-literal concatenation
(`"a" "b"`) is ANSI and it is K&R, and a backslash-newline inside a literal is
spliced in translation phase 2 — which for a `.m` already happened, in the
very preprocessor being replaced. Both were tried; both give
`**** unterminated string ****`. That bounds what this route can build: a
program whose single longest literal exceeds 1022 characters cannot go
through it. In practice they do not — what makes these lines long is several
STATEMENTS joined, and tar.c's longest single literal is 622.

## Where the four victims stand

    flex     dfa.c        BUILDS, through CPP2
    djpeg    jdmarker.c   BUILDS, through CPP2 + KNR together   (2026-08-23)
    gtar     tar.c        past cpp and past c68's line limit; stopped
                          elsewhere -- see below
    inform   informosk.c  not attempted since the measurement

### gtar, as far as it got (2026-08-23)

Everything the preprocessor was blamed for is now cleared, and what is left is
ordinary header work:

  - `CPP2` plus the re-wrap gets every one of its nineteen sources through
    `cpp` and `c68`'s line limit.
  - `-DUSG -DNO_REMOTE` are the right OS-9 answers to two of its switches:
    `USG` skips the `<sys/mtio.h>` include (there is no tape ioctl here, and
    every use of one is guarded on `MTIOCTOP`), and `NO_REMOTE` maps the whole
    `rmt*` family to plain `open`/`read`/`ioctl` and drops `rtape_lib.c`.
  - `-DVARARGS_MSG`, not the makefile's `-DSTDC_MSG`: the STDC arm of `port.c`
    declares `msg(char *str,...)`, which is a prototype.
  - `SRC/COMPAT` gained `sys/ioctl.h`, `sys/sysmacros.h`, `grp.h` and
    `bcopy.h` — all four are forwards or a handful of macros, and each says in
    its own header why it is there.
  - Three ANSI function definitions, all additions by the OSK porter rather
    than FSF code, are K&R now and marked as changed in place:
    `create.c:to_unix_mode`, `list.c:to_os9_format`,
    `buffer.c:rmt_jl_open`. **`ansi2knr` cannot do this job here** — see
    `knr_wanted()` in the driver: on a K&R definition whose parameters are
    declared on the following lines it emits `wildmat(s, p)  s; p;` and adds
    bogus `int` declarations that then fight the real ones.

**What stops it now**: `ERROR`, `TRUE`/`FALSE`, `S_IFREG`, and the Unix
`errno`/`EBADF`/`ENOSPC`/`EIO`/`ENXIO` are all undeclared. The port was
written against `DEFS/os9lib`, a complete alternate DEFS set that has every
one of them — and that set is a **dead end for this toolchain**: it is
ANSI-era (`_cmpnam( char *, char *, int)`, `const char *`), its `struct stat`
and `dev_t` collide with the ones COMPAT already supplies, and its `time.h`
includes `</h0/defs/setsys.h>` by absolute path. Two hours went into proving
that; do not spend them again.

The next step is narrow COMPAT-style additions for those five or six names,
not a wholesale DEFS swap.
