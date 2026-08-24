# What is left, in order — written 2026-08-22 as rdoggett went to sleep

He said: *"You seem done, yet I feel there is lots more to do."* He is right,
and this is the list. It is ordered so that whoever picks it up — me tonight,
him tomorrow — starts at the top and does not have to decide.

The four capabilities he named are the measure: **findable, live-demoable,
easy to install on a target, easy to install buildable source, documentation
accessible in universe.** Everything below serves one of them.

---

---

## 0. THE NEXT POOL PASS — what to look for, before anything else

rdoggett, 2026-08-23: *"we will make another pass at all of the collected
treasures, and should look for ls or its missing piece specifically."*

### ls — TRY os9lib's stat FIRST, before hunting for the lost source

**Found 2026-08-24, and it may make the hunt unnecessary.** `LIB/os9lib.l`
already contains a `stat()` that WORKS -- distinct inodes, real sizes, real
mtimes -- provided it is compiled against **os9lib's own `<stat.h>`**, because
the library fills os9lib's `struct stat` and not the one `DEFS/UNIX` supplies.
Measured with a five-line probe; the numbers are in
`notes/SESSION-2026-08-23.md`.

`SRC/ls/os9stubs.c` fabricates precisely the fields os9lib's stat gets right.
**So the first thing to try is deleting os9stubs.c's stat/fstat and letting
os9lib's be linked instead**, with `-V=/dd/DEFS/os9lib` and the overlay
mounted as `/h0` (os9lib/time.h needs `</h0/defs/setsys.h>`, and `ls`'s own
`system.h` already pre-defines `D_TckSec` to dodge that). That is a far
cheaper experiment than finding the lost file, and if it works the collection
can rebuild `ls` from what it already ships.

If it does not work, then hunt:

### ls — the one missing file, and how to recognise it

The collection ships a good `ls` and cannot rebuild it. **What is missing is
one file: a fixed `os9stubs.c`.** Everything else in `SRC/ls` compiles.

**Do not go by version.** The shipped binary answers `--version` with
`ls - 3.13-os9`, which is exactly what the pre-fix tree's `config.h` says. The
fixed source is a later revision of the same port carrying the same string.

Recognise it by CONTENT. The pre-fix `stat()` is:

    buf->st_mode = S_IFREG | S_IRUSR | S_IXUSR | S_IROTH;   /* every file */

and there is no `st_mtime` anywhere in the file. **The fixed one must read the
real file descriptor** -- `_gs_gfd` returns the FD sector, which carries the
attribute byte and the modification date -- and set `st_mode` and `st_mtime`
from it. So:

    grep -l '_gs_gfd'   over any os9stubs.c
    grep -l 'st_mtime'  over any os9stubs.c
    or any ls/fileutils tree whose os9stubs.c is not byte-identical to ours

Already searched and NOT there: everything under `~/Developer/os9`, including
`play/oskBoot/SRC/ls` (byte-identical to ours) and the 2026-08-10 salvage
tree (its `src2/ls` holds an empty `sys/`).

Sizes, for quick elimination: shipped binary **47892** bytes; a build from the
pre-fix tree comes out **46522**.

### Also worth a targeted look while the pool is open

  - **`oleo`** -- `APPS/oleo1.6.tar.gz`, 217 files, the biggest single source
    gap left. It arrives wrapped in a `DEFS/` of 59 files, 27 overlapping the
    SDK heavily, so separating the sources is the careful part.
  - **`ldblib.h`**, for lua -- named by `lua.c` under `#ifdef _OSK` and in no
    copy of the tree.
  - **Ultra C's syscall library** (`_os_crc`, `_os_ss_attr`, `_os9_id`), for
    luac. `os_lib.l` here is not a relocatable module.
  - **`rcs`** -- `rcssyn.c`, `rcsrev.c`, `rcsutil.c`, missing from the tree and
    from `rcs4.lha`. RCS **version 4** (Purdue, 1987); GNU 5.7 is not drop-in.
  - **`h_grafik.h`** (calc), **`graf.h`** (cgrafik), **`gpprim.r`** (mgif),
    **`local.h`** with `loop`/`ERROR` in it (spooler) -- one file each, and
    each is the whole blocker for its tree.

## 1. The trees with no recipe — what is actually left

`tools/build.sh --missing` lists them and `notes/COMPILE-AUDIT.md` says why
each has none. As of 2026-08-23 (end of the overnight pass): **290 recipes, 17 trees
without one** -- `cnews`, `ed`, `inform`, `rayshade` and `macutils` all gained
one during it. Most of
those 24 are accounted for (wrong language, material genuinely absent, not a
program tree). What is real work, in the order I would take it:

**a. The `cpp` victims — three down, one to go.** UPDATED 2026-08-24: `gtar`
BUILDS through the GCC flag and reads and extracts real tar archives
byte-identically. Creating them is wrong (the stat mismatch above) and gtar
warns loudly on every file; do not install it over anything until that is
fixed. `inform` and `djpeg` are done; only `flex` was already done.

The defect is now measured rather than guessed: `cpp` bus-errors on a source
line of **513 characters or more**, `c68` stops at **1023**, and neither has
anything to do with macro nesting. `notes/CPP-MACRO-CRASH.md` has both
measurements and the reproduction they explain.

  - `flex` — builds, through `CPP2`.
  - **`djpeg` — BUILDS.** It needed `CPP2` and `KNR` at once, which the driver
    could not do; it can now. Verified by round-trip against `cjpeg`, not just
    by linking.
  - **`gtar` — much closer, and the remaining work is named.** Everything
    blamed on the preprocessor is cleared. What stops it is five or six
    undeclared names (`ERROR`, `TRUE`/`FALSE`, `S_IFREG`, Unix `errno` and
    friends) that want narrow `SRC/COMPAT` additions. Do **not** reach for
    `DEFS/os9lib`, which has all of them — it is ANSI-era, it collides with
    COMPAT's `struct stat`, and two hours have already been spent proving it.
  - **`inform` — BUILDS**, 2026-08-23. Three blockers, none of them "bad
    character": cpp's 512-char line, a `SRC/COMPAT/limits.h` that was useless
    in a `#if`, and `o68` miscompiling `c68 -k`. It recompiles the
    collection's own `hellow.inf` to a story file byte-identical to
    `GAMES/INFORM/hellow.z3`.

**b. `mtools` — SETTLED, and it was never a timeout.** It finishes in minutes;
c68 rejects a prototype on nearly every line. Its port is a `gcc2` build, same
category as `ls`. `ansi2knr` cannot reach it — see the left-margin rule in
`tools/rebuild/README.md`. Nothing further to do unless somebody wants a gcc2
on this disk.

**c. `ed` — BUILDS**, 2026-08-23, and the audit's "ANSI C" was wrong: it is
K&R throughout. At runtime it wants `/r0`, which os9exec cannot provide; the
shipped `disk/CMDS/ed` has the same dependency, so that is the archive's and
not new.

**Still open in this area:** `lua` (genuinely ANSI, unreachable by ansi2knr),
`lout`, GNU Chess 4.0, `gtar` (a port decision, see CPP-MACRO-CRASH.md),
`macutils`, and `cnews`/`rayshade`/`infoxpress`/`rcs`, none of which has been
tried since the two limits were measured. `cnews` scores 454/2 on the
left-margin count and is the most promising.

**d. `macutils` — UNBLOCKED, and so is anything else with that shape.** The
include-path knot was real: `cpp` will not search a `-V` directory for an
include name containing a directory. GNU cpp does, and a recipe's `-V=` now
reaches it, so **`CPP2` is the general answer to that whole class**. `binhex`
and `unsit` build; `mcvert` wants `ftime()` and `macsave`/`macunpack` are not
run down.

**e. `rayshade` — BUILDS and RENDERS.** The first package build here, 78
sources over six nested libraries. Its recipe note has the four walls. Two
scenes still fail (`csg.ray` truncates, `blob.ray` bus-errors) and neither has
been run down. Separately: the SHIPPED rayshade could never render anything,
because it asks for a preprocessor called `cccp` and the disk has `cccp2`.

**Method that has been right every time:** read the tree's own makefile for the
object list. Guessing "every .c in the directory" was wrong for `adv`,
`cursive`, `gnu`, `snake`, `zoo` and `blarslib`, and right for none of them.

## 2. Take the counts out of the two docs that still carry them

His instruction, 2026-08-22: *"avoid putting actual numbers of anything in the
docs ... It's a constant update nightmare, just so we can say 99 million
sold."* Done for `disk/readme`, `DOC/README-CIO` and `DOC/README-RUNNING`.
Still to do:

  - **`README.md`** — DONE 2026-08-22. Every hand-written count is out; the
    `CATEGORIES` table keeps its numbers because `tools/gen_catalog.py`
    writes them and nobody maintains them by hand.
  - **`DOC/STATUS`** — LEFT ALONE, deliberately, and here is why rather than
    an unanswered question. Its numbers are not a claim about the collection,
    they are the RESULT of a measurement: the file says MEASURED 2026-08-21
    at the top and every figure in it comes from the four stage files that
    `tools/verify_combine.py` reads. Stripping them would leave a report of a
    measurement with the measurement taken out. It does not drift the way
    `readme` and `DOC/INDEX` did, because it is not maintained — it is
    re-measured, and the date says when.

    What it should eventually be is GENERATED, so that the prose and the
    numbers cannot come apart: `verify_combine.py` already computes every
    figure in its tally block. That is a real piece of work (the file is 444
    lines and most of it is explanation) and it is not started.

## 3. The ksh output fault — much less urgent than it looked

**Measured 2026-08-22: the SHIPPED `ksh` works.** Interactively
(`os9exec -r ksh`: typed commands run, assignments and `$`-expansion work,
`exit` exits) and with `-c` (`print one; print two` prints both lines). That is
`disk/CMDS/ksh` unmodified, on os9exec carrying the `I$Read` fix — the fix
rdoggett has said is going to be released.

So the reason the rebuild existed has largely gone. `sh_lex.c.patch` reads the
command line a byte at a time as insurance against an os9exec WITHOUT that fix,
and that release is not going to happen.

What is still true: **our rebuild of ksh loses all output**, and that is a
port defect in the rebuild, not in what ships. `tools/rebuild/pdksh/README.md`
has what was tried on 2026-08-22 and ruled out — the `flushshf` guard and the
`fdopen(fd, "r+")` mode — and names the one probe that would settle the
remaining FILE-layout theory in two lines.

`tools/rebuild/pdksh/build_ksh.sh` now builds it in one command, about four
minutes, so the next attempt is a short loop rather than an afternoon.

## 4. `adv` — DONE 2026-08-22

It was a recipe problem, exactly as suspected, and the answer was where it
always is: the tree's own makefile. `RFILES = main.r init.r io.r done.r
subr.r vocab.r rand.r` — seven of the tree's files, not all of them, which is
why the all-`.c` attempt kept dragging in `okplay.c`'s and `test.c`'s `main`.
`advent` builds.

## 5. blarslib — DONE 2026-08-23

In, minus thirteen headers that were Microware's. `notes/BLARSLIB.md`.

## 5a. Re-run the verify sweep — nobody has since 2026-08-21

`notes/verify-final.tsv` and `DOC/STATUS` date from the 2026-08-21 measurement.
Since then the disk gained `DOC/START-HERE`, seventeen recovered documents, the
ADVSYS sample, a fixed `about`, `DEFS/blarsdefs` and `LIB/blarslib.l`. None of
that should move the running figure — but that is a prediction, and this
collection has a long history of predictions that measured differently.
`tools/verify_all.sh` then `tools/verify_combine.py`.

## 6. A live-demo affordance

"Simple to live demo" is the one capability with no tool behind it. Today the
answer is "mount it as /dd and type a program name", which is fine but assumes
you know a name worth typing. `about` answers *tell me about X*; nothing
answers *show me something good*.

**DONE 2026-08-22** — `disk/DOC/START-HERE`, and `disk/readme` points at it.
A dozen programs that run with nothing set up, grouped by what they do to the
terminal, with the quit key for each (from `notes/quit-keys-verified.txt`, so
they are measured rather than assumed). It is typed, not generated: which
programs demo well is a taste judgement.

Read it and change what you disagree with — that is the point of it being
short.

---

## Standing rules for whoever works this

  - **All ELEVEN `check_disk.py` checks green before every commit.** Read the
    output, not the exit code — that has gone wrong three times now.
  - **Never edit a script, a recipe file, or anything under `disk/` while a
    build is running**, and never `git checkout -- disk/SRC`. Both cost real
    work. `tools/rebuild/tidy.sh` is the safe cleanup.
  - The `CPP2` and `KNR` recipe flags exist now; `tools/rebuild/README.md`
    explains both and the failure table has grown to match.
  - **Make every check fail once before believing it.**
  - Branch `release-pass-2026-08-21`. Nothing pushed.
  - Counts belong in generated files, never in prose.
  - `~/Developer/os9/os9exec` has uncommitted changes that are deliberate.
    Do not commit or revert them.
  - rdoggett's own Microware-era system utilities do not ship; porting is not
    authorship. The test is the `rfd` initials in the edition history, not his
    name. See `notes/FOR-RDOGGETT.md`.
