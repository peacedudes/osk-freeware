# Does the source compile?

rdoggett, 2026-08-22: *"verify we have it all (if it's source, it should
compile, right?)"*

Right. Until now that had only ever been established for the trees that have a
recipe. This is the count, and the method for closing the rest.

## Where it stands, 2026-08-22 (end of the build pass)

Run `tools/build.sh` for the live answer and `tools/build.sh --missing` for
the trees that still have no recipe. As measured on 2026-08-22:

    237 of 240 recipes build clean

and the three that do not, plus every tree with no recipe at all, are
accounted for below. Nothing in this list is "unknown" any more.

### The three recipes that fail

  - **`ls`** — a gcc2 build, and **it compiles now** (GCC flag, 2026-08-23).
    **It is still not adopted and has no recipe, deliberately**: `SRC/ls` is
    the PRE-FIX tree. Its `os9stubs.c` gives every regular file the same
    fabricated mode and never sets `st_mtime`, and the build bus-errors on
    `ls -l`. The shipped binary prints real per-file modes and real dates, so
    it came from a later source that is on no disk here. See
    `notes/SESSION-2026-08-23.md`.
  - **`pdraw`** — wants X11 headers. They are not here and are not coming.
  - **`pep`** — calls `standby()` and `init_via()`, which live in the mc
    EPROM programmer's own hardware library. Its own header says it runs only
    on that board, so this one is correct as it stands.

### Trees with no recipe, and why

**Wrong language or wrong compiler.**

  - `homelibr` — C++ (`.cc`). No C++ compiler here.
  - `aterm`, `serload` — 68k assembly only. `r68` would do it; nothing in
    `rebuild.sh` drives the assembler yet.
  - `graph` — three `.c` and eight `.a`; same.
  - ~~`ed`~~ — **wrong, and corrected 2026-08-23: `ed` is K&R throughout and
    BUILDS.** Running `ansi2knr` over it is destructive. Its only real blocker
    was `ed.h`'s `REALLOC` macro joining into ~1400 characters, past cpp's
    512; `CPP2` clears it. See its recipe.
  - `lout`, `gnuchess/GNUCHESS4.0` — ANSI C. `lout`'s `externs` uses typed
    bitfields; GNU Chess 4.0's header is several hundred ANSI prototypes.
  - `rtf` — Fortran.

**Something genuinely absent.**

  - `rcs` — `rcssyn.c`, `rcsrev.c`, `rcsutil.c` missing from the tree AND from
    `rcs4.lha` in the pool. RCS **version 4** (Purdue, 1987); GNU's 5.7 files
    are not drop-in.
  - `calc` wants `h_grafik.h`, `cgrafik` wants `graf.h` — neither is anywhere
    on the disk or in the pool.
  - `mgif` wants `screenbaseaddress` from `/h0/lib/gpprim.r`, a graphics
    primitive library that is not here.
  - `deansi` is lex output and wants a lex runtime (`yyreject`).
  - `rayshade` — **BUILDS 2026-08-23**, and renders. 78 sources over six
    nested libraries, the first package build here. Four walls, all in its
    recipe's note.
  - `spooler` wants its author's `local.h` — the one with `loop` and `ERROR`
    in it, not the `auxlib` one this disk carries.
  - `gtar` wants **blarslib**, which IS in the pool. See
    `notes/BLARSLIB.md`; that is a decision, not a search.
  - ~~`macutils`~~ — **UNBLOCKED 2026-08-23.** The reason given below (cpp
    will not search a `-V` directory for an include name with a directory in
    it) was correct and is now obsolete: GNU cpp does, and a recipe's `-V=`
    reaches that pass. `binhex` and `unsit` build.
  - ~~`mtools`~~ — **BUILDS, 2026-08-23, with the GCC flag.** It was never a
    timeout and `ansi2knr` was never going to reach it: its OSK port is a
    `gcc2` build and the disk carries a whole GCC 2.5.6 in `CMDS/GCC2`. What
    stopped anyone was that gcc2 here could not compile a two-line program
    until `DEFS/GCC2` was repaired. 45 sources; `mdir` runs.

**A `cpp` defect -- and it is now MEASURED, not guessed.**

  Microware's `cpp` bus-errors on a source line of **513 characters or more**;
  `c68` stops at **1023**. Both measured 2026-08-23 -- see
  `notes/CPP-MACRO-CRASH.md`, whose title is now the only wrong thing left in
  it. It is not "nested macro expansion"; nesting is just how a line gets long.

  - `flex` -- BUILDS, through `CPP2`.
  - `djpeg` -- BUILDS, through `CPP2` and `KNR` together, 2026-08-23. The
    IJG's own round-trip test passes on it.
  - `gtar` -- past `cpp`, past `c68`'s line limit, past its includes and its
    three ANSI definitions. Stopped on five or six names (`ERROR`, `TRUE`,
    `S_IFREG`, Unix `errno`) that want narrow COMPAT additions. The
    `DEFS/os9lib` set has them all and is a dead end; the note says why.
  - `inform` -- not attempted since the measurement.

**Not program trees.**

  - `COMPAT` is headers. `unixlib` is a library and now has a recipe of its
    own kind (`unix.l`).

**ANSI C.** This is the big remaining category, and it is one job, not
several: these trees declare prototypes, and Microware's `cc` is K&R.

  - `lua`, `jpeglib`, `gnuchess/GNUCHESS4.0`, `ed`, `lout`, and probably
    `cnews`, `rayshade` and `infoxpress`.

  **The lever exists and is in** -- the `KNR` recipe flag, 2026-08-23. It runs
  every source through `ansi2knr` before `cc`. `cjpeg` builds that way; that
  is JPEG's whole compressor, 27 sources, and it had never compiled here.

  **But it only goes so far.** `ansi2knr` rewrites function DEFINITIONS and
  leaves headers alone, so a tree is only reachable if its own headers can be
  told to stop declaring prototypes:

    reachable      JPEG -- jconfig.h has HAVE_PROTOTYPES, `const', and
                   INCOMPLETE_TYPES_BROKEN, which is provided for compilers
                   exactly like this one
    not reachable  lua -- by ansi2knr, yes.  But that was the wrong question:
                   lua compiles fine under the GCC flag (16 of 17 sources, and
                   luac 17 of 17).  Both stop on ABSENT MATERIAL instead --
                   ldblib.h for lua, and Ultra C's syscall library for luac.

  So `lua`, and probably `ed` and `lout`, are header work rather than a flag.
  `djpeg` is neither: it is the cpp defect.

**Still ordinary work, nobody has done it.**

  - `inform`, `ioccc` (eight more contest entries), `macutils` (blocked on
    an include-path knot, see `notes/SESSION-2026-08-23.md`), `pdksh` (has its
    own `build_ksh.sh` rather than a recipe).

---

# The 2026-08-22 morning pass, as it stood then

## Where it stands

    170  source trees under disk/SRC
     99  had a build recipe          -- 194 programs, known to compile
     71  had none                    -- never established either way

Of the 71, **18 map to exactly one shipped program**, which makes them the
cheapest to settle. `tools/try_compile.sh --all` tries each with the naive
recipe -- every `.c` in the tree, the standard flags -- and reports what
happened.

    8  BUILD, and now have a recipe
   10  do not, each for a reason below

`recipes.psv` is 212 recipes now, up from 204.

## The eight

`tsmon2`, `indent`, `robots`, `today`, `wish` and `xlisp` build with nothing
but the naive recipe. Two needed one library each:

  - **`draw`** wants `mytime` -- `/dd/LIB/mytime.r`, which is in the SDK LIB
    as a loose object, not inside any `.l`, so it has to be named explicitly.
  - **`shuffle`** wants `optarg` -- `/dd/LIB/os9lib.l`.

## The ten, and what each is waiting for

| tree | program | stops at |
|---|---|---|
| `adv` | advent | `execv` unresolved; not in os9lib either |
| `argproc` | argproc_demo | `bcopy` unresolved -- `shims/os9bcopy.c` should do it |
| `nobs` | nobs | `isupper` unresolved; it is in `csl.l`, which a `-qm` build cannot use |
| `snake` | snake | `#include <a.out.h>`, which is on no disk here |
| `cursive` | cursive | duplicate symbols -- the all-`.c` list is too long, two mains |
| `proff` | proff | duplicate symbols, same shape |
| `hist` | hist | undeclared identifier in its own `h_var.h:77` -- an `#ifdef` arm |
| `pep` | pep | undeclared identifier, `plain.c:165`; it also wants an EPROM driver |
| `flex` | flex | no single diagnostic; read the log |
| `ioccc` | queens, bjack, jaw, trigraph | Four of the twelve 1990 entries build (2026-09-15): baruch.c as queens unchanged; cmills.c, jaw.c and scjones.c from changed copies in SRC/ioccc/OSK, whose README.OSK lists every change (include spacing, jaw's P macro and remote tables and '\n', scjones's trigraphs translated). Not built: westley links short of a putchar function; tbr needs pipe(); stig is a ksh joke, not a program; dds needs LANDER.BAS, which is not on the forum disk; tried 2026-09-15 and not built: dg writes every directive as `#d' after `#define d define', which Microware's cpp rejects ("illegal '#'"); loco prints `choo choo' and then loops forever by design; theorem includes stdio.h a second time by design, and Microware's has no guard ("multiple definition"); pjr makes Microware's cpp itself abort |

Four of those (`cursive`, `proff`, `hist`, `pep`) are ordinary recipe work --
the file list is wrong, or a define is missing. `adv`, `nobs` and `snake` are
waiting on something that is genuinely absent.

## A bug this found in itself, worth not repeating

The first run reported `argproc`, `hist` and `proff` as **missing headers they
in fact ship**: `boolean.h`, `h_def.h` and `lextab.d` are all sitting in their
own trees. The prober had copied them but had not put the tree's own directory
on the include path, so a source writing `#include <boolean.h>` rather than
`"boolean.h"` looked in `/dd/DEFS` and found nothing. `rebuild.sh` passes
`-V=/h6/<tree>` for exactly this reason and the first draft here did not copy
it.

The lesson is the collection's own: **make the check fail once before believing
it.** Three "missing header" verdicts were the checker's fault, not the
source's.

## What is left

The other 53 un-recipe'd trees map to several programs each, or to none that
ships. Those need the archive-versus-program mapping read out of `DOC/ORIGINS`
first -- `SRC/divutils` holds `gen`, `run` and `if`, and counting by tree name
over-counts badly. That is the next increment.


## C++ works. homelibr still does not. (2026-08-24)

**The disk can compile, link and run C++.** Proven end to end with a class,
a constructor and a method call: it printed what it was supposed to. What it
took, none of it obvious:

  - **`gcc2` cannot start the C++ front end at all.** Its suffix table has no
    entry for a `.cc` -- it calls one a "linker input file unused since
    linking not done" -- and `-Fcc2plus`, which the homelibr makefiles use,
    does not change that. The only door is `gpp`.
  - **`gpp` forks `cccp`, and nothing on this disk answers to that name.**
    The preprocessor ships as `cccp2`, which is what `gcc2` forks. A plain
    copy under the other name is enough; the module inside is still called
    `cccp2` and os9exec runs it.
  - **`collect` is in `CMDS/GCC2`, not `CMDS`.** Any program with a global
    constructor needs it, or the link stops on `__CTOR_LIST__` and
    `__DTOR_LIST__` unresolved. Only gpp's spec runs it.
  - **`collect` opens `gpp.l`; the disk ships `libgpp.l`.** Another copy.
  - The link must go through `gpp`, not `l68` by hand the way the C path
    does it -- and gpp has no `-n=`, so **the module takes its name from the
    output FILE**. Write the file as `<prog>` and rename the file afterwards.

`make_overlay.sh` makes all three names now, and `rebuild.sh` has a `GPP`
recipe flag. **No recipe uses it yet**, because the only C++ in the tree is
homelibr and homelibr does not build.

### What blocks homelibr

Six programs -- `Ascii2Libr`, `EditLibr`, `Libr2Ascii`, `Librarian`,
`PrintCards`, `PrintLabels` -- all six already on the disk as working
binaries. Fixed so far: `Include/common.h` had `#include <sgstat.h>`
commented out, so `Terminal.h`'s two `sgbuf` members were an undeclared type
and every file that reached that header stopped. That one is done and marked.

What is left is a **dialect** problem and a **library** problem, and neither
is a five-minute fix:

  - **Pre-standard class constants.** `const bufSize = 512;` inside a class,
    then `char Terminal::termBuf[bufSize];` at file scope in the `.cc`.
    GCC 2.5.6 wants `Terminal::bufSize`. Same for `TCapsLen` and
    `maxblocks` -- eight or so sites across `Terminal.cc`, `Card.cc`,
    `PTree.cc`.
  - **`fstream.h` does not exist here, and cannot.** `EditForm.cc` declares
    `ofstream` and `ifstream`. `LIB/libgpp.l` is libg++ **1.x**: it has
    `filebuf` and `File`, and no `fstream`, `ifstream` or `ofstream` at all.
    Writing the header would mean writing the classes.
  - **`<stdlib.h>` collides.** With `-I/dd/DEFS/CC` on the path, `<stdlib.h>`
    is libg++'s, not the SDK's, so `os9forkc` -- which `Terminal.cc` passes
    to `os9exec` -- is undeclared. Putting the SDK's first breaks the C++
    headers instead.
  - `ParseExpr.tab.cc` includes `"ParseExpr.tab.h"` and cccp2 does not search
    the source file's own directory, so that one needs `-V=<tree>/Lib`.

None of it is impossible. It is a port, not a recipe, and the payoff is
reproducibility for six binaries that already work.

## Assembly: aterm reproduces exactly, the other two cannot be built (2026-08-24)

`tools/rebuild/` has an `ASM` flag now. `aterm` builds through it and is
**byte-for-byte the binary that ships**. The other two assembly trees are
blocked on files that are not in this repo and not in
`~/Developer/os9/Scraped`:

  - **`serload`** -- its own `dependencies` file names `../rt_comm/setopt.a`,
    `../rt_comm/rt_comm.a`, `../rt_comm/pack.a`, `../rt_comm/unpack.a` and
    `../rt_comm/rdlin_tim.a`. There is no `rt_comm` directory anywhere. Two
    programs, `txmod` and `rxmod`, both on the disk.
  - **`graph`** -- `sine.a` and its siblings `use <graphmakros>` and
    `use <mathmakros>`, which r68 resolves to `/dd/defs/graphmakros` and
    `/dd/defs/mathmakros`. Neither exists. Six programs, all on the disk:
    `apfel`, `sine`, `graph`, `showpic`, `graphdemo`, `graphsave`. If those
    two macro files ever turn up, each is one recipe line.

`devprc/getsys.a` is NOT the shipped `getsys`: its psect is type 0, language
0, entry 0 -- a subroutine object holding `_gs_sdevn()` for C callers.

---

## sc -- source FOUND 2026-08-26, does not link yet

The shipped `sc` spreadsheet had no source here, and the STUFF drop's `sc.ar`
was a partial set. **The complete source is in the pool**, in
`Scraped/os9/PUBCMDS/microware-archive/EFFO/pd8.lzh`, an EFFO public-domain
disk: `SRC/` carries sc.c, sc.h, lex.c, gram.y, gram.c, interp.c, cmds.c,
range.c, xmalloc.c, help.c, crypt.c, psc.c, getopt.c, the two `.sed` files,
experres.h, statres.h, y.tab.[ch] and its own makefile -- plus `DOC/sc.doc`,
`DOC/psc.doc` and a built `CMDS/sc` (108658 bytes, NOT the 233050-byte binary
we ship, so ours is a different build).

It was found with `tools/index_archives.py`, which is new: no `find` could see
it, because it had never been unpacked.

Installed as `disk/SRC/sc`, screened clean. **No recipe yet**, and here is
exactly how far it gets, so nobody re-derives it:

  - `y.tab.h` is NOT redundant with `gram.c` -- `lex.c` includes it. Deleting
    it as a duplicate costs you a build.
  - `SIGALRM` is undefined on OS-9. The archive ships `DEFS/signal.h.add`
    saying `#define SIGALRM 14`; passing `-DSIGALRM=14` in the recipe's
    defines is enough and leaves the archive's source untouched.
  - `popen`/`pclose` are wanted; the driver's `os9popen.c` shim supplies them
    by itself.
  - **What stops it: `wrefresh`.** The overlay's `curses.l` defines it in two
    psects, sc references symbols from both, and l68 refuses --
    `Symbol 'wrefresh' from psect 'screen_c' ... caused name clashes`. Adding
    `os9lib.l` (which the archive's own makefile links) makes it worse: that
    has a curses too.
  - `ncurses.l`, which the disk DOES ship, is not a drop-in: it lacks
    `wattrset`, `wattron` and `_bootdrive`.
  - The archive ships its own `LIB/curses.l`, which is very likely the curses
    sc was built against. Building with it would work; it cannot be committed
    without knowing whose it is, and a recipe that needs a library not in the
    repo is not reproducible. **That is the open question for sc.**

The documentation is in regardless: `DOC/sc/sc.doc`, `psc.doc`, `README` and
`CHANGES` join the `sc.man` and `tutorial.sc` that were already there.

`psc`, sc's input formatter, is a second program in the same archive and is
not on the disk at all.

---

## Candidates REFUTED 2026-08-26 -- same name, different program

`tools/find_missing_source.py` proposes leads by name. Where the archive also
carried a binary, tonight's installs were confirmed by comparing it with ours
byte for byte. Where it did not, the test was to pull the distinctive printable
strings out of OUR binary and look for them in the candidate source.

Two passed and are in: **makeinfo** (75 of 210 strings, including
``No closing brace for footnote `%s'``) and **upperdir** (6 of 11, the usage
line matching exactly).

**These scored 0, 1 or 2 and are NOT our programs.** They are recorded so the
next pass does not spend the same hour: `collect` (0/23), `compr` (0/20),
`env` (0/28), `infocom` (1/56), `lgrep` (0/9), `lharc` (2/170 -- and both
"matches" were runs of spaces), `md5` (1/20), `rm` (0/142), `smail` (0/64),
`su` (0/43), `tail` (0/17), `wndex` (2/36).

`advent`, `eset`, `m4` and `split` DO have a binary in their archive and it
differs from ours, so those are different builds or different versions; they
are worth a closer look but were not taken on trust.

The lesson this repo keeps relearning: a name match is a lead, not a finding.
It has already shipped a recipe pointing at the wrong `pep`.

---

## netpbm -- 152 of 168 build, 2026-08-27

Recipes are in `tools/rebuild/recipes.psv`: four libraries (`pbm.l pgm.l ppm.l
pnm.l`, installed in `disk/LIB`) then 152 one-source programs. **The shipped
binaries already work -- this buys rebuildability, not function.**

### What it took, and three of them were upstream bugs

  - **`-D_OSK`** -- the port's own guard. `pbmplus.h` skips `<unistd.h>` when
    `_OSK` is defined; gcc2 predefines it, Microware's `cc` does not.
  - **`-DSYSV`** -- the port's own switch for a System V C library, which is
    what OS-9 has: `random`/`srandom` onto `rand`/`srand`, `index`/`rindex`
    onto `strchr`/`strrchr`, `bcopy`/`bzero`/`bcmp` onto the `mem*` ones, and
    `<string.h>` rather than BSD's `<strings.h>`.
  - **`disk/SRC/COMPAT/malloc.h`, NEW** -- SYSV makes `pbmplus.h` include
    `<malloc.h>`, which OS-9 does not ship. Turning SYSV on without it broke
    three of the four libraries.
  - **`libpbm1.c` -- upstream typo, fixed.** The `NEED_VFPRINTF2` block ends
    `return nc;` and `nc` is declared nowhere in the file, so that block could
    never have compiled anywhere. OS-9 is the first system here to need it: it
    has neither `vfprintf` nor `_doprnt`.
  - **`pgmnoise.c` -- upstream omission, fixed.** Uses `time_t` and never
    includes `<time.h>`; it compiled elsewhere only because `pbmplus.h` pulls
    `<time.h>` in on the MSDOS/AMIGA arm.
  - **`pbm.l` named three times** in every recipe -- `l68` makes ONE pass per
    `-l=`, and `libpbm5` calls `libpbm2`'s `pbm_readpbm`.

### The 16 that do not build, with their MEASURED causes

**Static data over 64k -- 7.** `l68: non-remote data allocation of NNNNN bytes
value exceeds 64k`, or `r68: *** error - value out of range ***`.

    g3topbm  spctoppm  sputoppm  tgatoppm  ppmqvga  ppmtomap  giftopnm

  `LONGREF` is NOT enough -- tried, with `CPP2` so that it is actually
  implemented, and all seven still fail. Needs a real look at the data model.

**Source problems -- 7.**

    bmptoppm ppmtobmp   undefined struct/union tag referenced
    picttoppm           cannot initialize
    hpcdtoppm ppmshift ppmspread   undeclared identifier
    pnmtoxwd            identifier missing

**Missing pieces -- 2.**

    ppmpat      Symbol 'atan2' unresolved -- math.l has no atan2, though
                blarslib carries an atan2.c
    fitstopnm   can't open /dd/DEFS/float.h -- OS-9 ships no float.h

### An OPEN constraint, measured and NOT explained

Through the **shell**, a `cc` line carrying 19 `-l=` flags fails with
`can't open /dd/DEFS/ppm.h` -- the `-V=` flags are lost. Eleven works. Forking
`cc` DIRECTLY with the identical 19 flags builds fine.

**It is not line truncation, and I said twice that it was.** The failing line
measures **469 characters** against SCF's 512. The mechanism is unknown. It is
worked around by naming only `pbm.l` three times instead of all four
libraries, which is what the recipes do.
