# osk-freeware — open items

Moved out of os9exec's ROADMAP.md when the collection got its own repo.

## Open, as of 2026-08-08

### Next session starts at notes/PLAN-keep-drop.md

`keep` / `drop` — taking selected programs off the collection onto your own
`/dd`, with a receipt that makes removal exact and cannot eat your saves. The
design is settled apart from where files land; that one is blocking and is
written up there.

### Data files programs want -- FOUR FOUND, 2026-08-13

`magic` (file), `less.hlp` (less), `dm.hlp` (dm) and the cal holiday data
were all in the archive pool and are now in `SYS/`. `file` names real
formats instead of only OS-9 modules, and `cal -h` prints holidays. See
`SOURCES.txt`. **Four of these were recovered 2026-08-16** once the whole pool
was extracted: vi's `vi_usage`, `vi_errmsg` and `.exrc` from EFFO forum 13
(`SOFTWARE/C/VI/SYS`, the same disk its source came from), and ephem's
`ephem.cfg` and `ephem.db` from EFFO pd9. Both programs were then run: `vi -x`
opens a file, reports its size and quits cleanly; `ephem` draws its title page
-- *"Ephem - an interactive astronomical ephemeris program, Version 4.13,
April 3 1990"* -- and then asks for `math`, which is its ordinary starred
dependency. Still missing: mg's `mgrc` and forth's `lib/tile`, neither of
which is anywhere in the pool. `utmp` is a login
record a running system creates, not shipped data.

### Data files programs want that this disk does NOT have

Found by scanning for `/dd` paths that do not resolve here -- a hole in the
earlier scan, which only kept paths that DID resolve and so filed every gap as
"the user's problem". rdoggett spotted `utmp` by hand, which is what prompted
the recount.

| wanted by | path |
|---|---|
| `ci co rcs rcsdiff rcsmerge rlog` | `/dd/SYS/utmp` |
| `vi` | `/dd/SYS/vi_errmsg`, `/dd/SYS/vi_usage`, `/dd/SYS/.exrc` |
| `less` | `/dd/sys/less.hlp` |
| `cal` | `/dd/sys/cal.holidays`, `cal.init`, `holidays` |
| `ephem ephem881` | `/dd/sys/ephem.cfg`, `ephem.db` |
| `file` `dm` `mg` `forth` | `/dd/SYS/magic`, `dm.hlp`, `mgrc`, `/dd/lib/tile` |

Some are runtime-created and need only a writable directory (`utmp` is a login
record; the `XXXXXX` names are mktemp templates). The rest are real absences
worth hunting on h4/h2 before assuming they are lost. Not one problem -- do not
treat them as a batch.

### Microware C is available, and an earlier note here implied otherwise

`tools/rebuild/rebuild.sh` has always driven `cc`; 203 programs on this disk
were built with it. The rule is only that the IMAGE BUILD must not need
Microware, because it runs on GitHub -- binaries are committed, and CI never
sees a compiler. Verified this session against the SDK at
`~/Developer/os9/play/oskBoot`: `cc -qm=16k -n=hi` produced a module that runs
on the freeware disk with no `cio` present at all.

`gcc` on the disk cannot substitute: it is starred, and a compile attempt gives
`**** Can't install trap handler **** cio`. `as0`, `as1`, `lnk`, `ar`, `make`
and `tar` are all trap-free. `tar`'s source is `SRC/eff_tar/tar.c`, one file.

### OS-9 modules can be generated from nothing, and it is verified

Both header integrity rules were derived from the corpus and checked against it
before use:

- the CRC (poly `$800063`, complemented) reproduces **all 362** modules exactly
- header parity -- the 24 header words XOR to `$FFFF` -- reproduces **all 361**

A Swift emitter then produced a working program module with no assembler and no
linker anywhere in the path, and os9exec ran it. Two things this unlocks:
patching an existing module and re-CRCing it (proven on `gnuchessc`, whose
`/h0` paths were rewritten to `/dd` and which then found its data), and
generating data modules host-side.

**The trap worth remembering: `M$IData` and `M$IRefs` may not be zero.** Zero
does not mean "none" -- the loader reads eight bytes AT that offset as
`{destination, count}`, so zero makes it parse the module header as a
descriptor, read `$4AFC0001` as a destination, and reject the module with
`E_BMID`. Point them at an empty descriptor and a terminated table. Derived
from os9exec's `prepData()` after the first attempt failed.

### The /h0 vs /dd rewrite -- decided AGAINST, and why

Patching device prefixes in the binaries was proven to work and then dropped in
favour of `keep`. Recorded because the proof stands and the decision could be
revisited: rewriting is byte-length-preserving (`/h0` and `/dd` are both three
characters) and CRC-correct.

Under the premise that everyone has a Microware boot disk, the direction would
be `/dd` -> `/h0`, not the reverse: **41 programs** name `/dd` data this
collection provides, against **94** naming `/h0`. More to the point, the ~20
left alone would be the ones that prove it -- `bash`, `sh`, `ksh`, `chown`
naming `/dd/SYS/errmsg`, `/dd/sys/password`, `/dd/CMDS`, `/dd/tmp`. Those are
the user's system and must stay; the other direction would have had to get
every one of them wrong.

## Open, as of 2026-08-06

Written down because they were found in conversation and would otherwise be
lost with the session.

### cd and pwd -- FIXED, and the earlier note here was wrong

An earlier version of this entry said `cd` aborts the shell. It does not.
`pwd` is the one that kills a session, and the difference matters because
`pwd` is what a person types when they are already lost. Measured:

| arrangement          | `cd`                     | `pwd`             |
|----------------------|--------------------------|-------------------|
| `/dd` is an RBF disk | works                    | **hangs**         |
| no RBF `/dd`         | **bus error, kills bash**| getwd error       |

Both are the same cause: bash's `getwd()` walks `..` looking for a directory
that is its own parent, and OS-9 has one root per DEVICE with nothing above
them. The walk has no stopping point.

`/dd/.bashrc` now defines `cd` and `pwd` as functions that track the path by
string. `cd` still calls `builtin cd` to actually move -- only the getwd part
is replaced. Verified for absolute, relative, `.`, `..`, `../DOC` and a bare
`cd`, in both arrangements.

**The reason it can be fixed there at all is that the old note was wrong
twice.** `SYS/login` claimed bash "CANNOT read a startup file. Its `.' builtin
fails with E$Unit on every path". It reads `$HOME/.bashrc` perfectly well from
an RBF image; E$Unit is what a HOST DIRECTORY mounted as a device gives, and
that is the device, not bash. So `.bashrc` is a real file that really runs,
and `SYS/login` now sets `HOME` to the disk to guarantee it is read.

Still true and worth knowing: there is no `chd` or `pd` here -- those are
OS-9 shell builtins, not programs.

**`SYS/login`'s `builtin cd $ROOT` is load-bearing and must not be tidied
away.** Where /dd is not an RBF disk, the FIRST getwd of an *interactive*
shell aborts it with a bus error, but the identical failure inside a *script*
is survivable. Spending it in the login script is what leaves `cd` working in
the shell that follows. Measured both ways: remove that line and the first
`cd` a user types kills bash; keep it and `cd`, `pwd` and `ls` all work with
no OS9DISK set at all. Its stderr goes to `/nil` because the message it prints
is alarming and means nothing to the reader.

The one warning still shown in that arrangement, `shell-init: getwd: cannot
access parent directories`, comes from bash before any of our code runs and
cannot be suppressed from inside. Documented as harmless in README-RUNNING.

Starting bash bare remains a trap -- no PATH, no HOME, no working cd. Now
called out at the top of README-RUNNING's shell section, because it is what a
person naturally tries first.

### TERMCAP removes most of the /h0 problem

69 programs name `/h0/sys/termcap` outright, and **all 69 read the `TERMCAP`
environment variable first** -- measured, no exceptions. `SYS/login` now
exports it, so those 69 run with the disk mounted anywhere and no `/h0` at
all. That takes the programs needing a real `/h0` from 94 down to 37, and
most of the 37 are gcc passes and the linker.

`vi_nocio` (PVic) drives a vt100 with no termcap file whatsoever, which makes
it the editor to point people at. Plain `vi` is the EFFO build.

### Category calls that are mine, not measured

`tools/categories.psv` is hand-maintained and some entries are judgement:
whether "Amusements" and "Screen toys" should be one category; whether
`banner`, `cursive` and `gothic` belong in Text tools where I put them. A
one-line edit each -- that is why the file exists.

### Sweeps done, and what came of them

`h4` gave up advent's `glorkz` and larn's complete data. `h2` holds the same
`GAMES` tree as `h4`, nothing new. `he` is 200 KB and effectively empty. `h1`
is a Microware system disk -- `OS9Boot`, `SYSMODS`, `IO`, `DEFS`, `LIB` -- and
nothing was taken from it. Its root directory is unreadable to toolshed
(`error 214`); read read-only with `tools/fixattrs.py`'s reader instead.

`GAMES/DOGADV` on h4 was deliberately left: unknown provenance, and rdoggett
said no.

### Smaller things

- **GitHub Pages is not enabled**, so the workflow's publish step is skipped
  and `docs/index.html` is only readable after downloading the repo.
- **The catalogue extracts usage text for 266 of 439** non-netpbm programs.
  The rest either carry none or compose it at run time.
- **`tools/gen_catalog.py` has no test.** It is 500 lines of parsing against
  documents that have already surprised us four times.
- **`disk/.login` is gone.** It was the previous owner's Microware-shell login
  script -- wrong `PATH`, `umacs` as EDITOR, and a `MAILOPTS` naming their
  print spooler and mail host. Not dead weight either: Microware's `shell`
  runs `.login` at login, so with this disk as `/dd` it would have executed.
  In git history if it is ever wanted.

### Games: a play-test found one real bug and a lot of arrangement

rdoggett played through the games on 2026-08-07 while running with the
collection as `/h0` and **no `OS9DISK` at all**. Most of what that turned up
was the arrangement rather than the games.

**The one real bug, now fixed: data files shipped read-only.** `mktar.py` gave
every non-module file 0444, so `sokoban`'s `sok.score`, larn's `.lscore12.0`,
hack's `record` and bones, cribbage's `criblog`, wanderer's `hiscore` and the
`SAVES` trees were all unwritable. **As `0.0` you cannot see this** — RBF gives
the super-user a software bypass, so every write succeeds and the disk looks
fine. Log in as anyone else and `sokoban` stops with "cannot open score file".
Every file here is owned `0.0` (tar writes uid 0 and an RBF file descriptor
keeps its creator), so a real user is never the owner and only the PUBLIC
write bit counts. Data is now 0666; modules stay 0555. This is the same root
cause as the earlier "logged in as dog and couldn't run advent".

**Arrangement, not defect** — all confirmed working with the disk as `/dd`:
`bog` (dict is in `GAMES/BOG`), `hang` (`GAMES/dict`), `snake`, `wanderer`
(screens are in `GAMES/WAND/screens` — INDEX said "SCREEN DATA MISSING" and
was wrong), `sokoban`, `advent`. `advent` needing a `chd` into
`/h0/games/adv` is the same thing seen from the other side: it opens
`/dd/GAMES/adv/glorkz` by absolute path, and with no `/dd` only the working
directory saves it.

### The broken games, diagnosed from their source (2026-08-13)

Read rather than guessed at, which changes what each one needs.

- **`tet` — the raw-mode setup is compiled out.** `tet.c` puts the terminal
  into raw mode with `ioctl(TCGETA/TCSETA)` and reopens stdin `O_NDELAY`, but
  **all of it sits inside `#ifndef OSK`**. The OS-9 branch is `srand(0)` and
  nothing else. So the binary never sets raw mode and never gets a
  non-blocking read: it draws the board and the keystrokes stay in the line
  buffer. This is not "was it linked against an ioctl", which is what the
  entry below assumed — there is no ioctl call in the OS-9 build to link.
  Two ways out: set the terminal from outside first (Microware's `tmode`,
  which this disk does not carry, is the obvious one), or write an OSK branch
  that does the same job with `_ss_opt`. `LIB/alib.l` (auxlib) now provides
  both `ioctl` and `_ss_opt` if the first route is preferred.
- **`snake` does set raw mode** — `snake.c` calls curses `raw()`, and the file
  carries no OSK conditionals at all. Whatever stops it, it is not the
  terminal mode, so the guess that it and `tet` share a cause is wrong.
- **`lander`'s OSK conditionals are about `M_PI` and `random`**, not input; it
  reads with curses `wgetch`. That leaves the original reading — it wants
  curses line-drawing that vt100 termcap does not provide — as the live
  theory.

**Still broken, and each has source in `SRC/` if anyone wants a run at it:**

- `tet` — draws the board, takes no input. Uses SysV `ioctl(TCGETA/TCSETA)`
  for raw mode; `SRC/unixlib/ioctl.c` implements that over `_ss_opt`, so the
  question is whether this binary was linked against it. Its README also names
  a compile-time `INIT_PAUSE` for machine speed.
- `lander` — no input, and a corrupt screen after a crash. Its README wants
  "SysV.3 curses line drawing", which vt100 termcap does not provide.
- `snake`, `maze` — start and sit. No source for `maze`.
- `bite` — not broken. It is a skull animation, not a game; INDEX now says so.
- `robots` — playable only with `-m`, which its usage string offers and
  nothing explained. INDEX now says use it.

**Removed:** `joke` (rdoggett: not funny and not appropriate); `GAMES/ADV/startup`,
which was never a startup file but 333 bytes of the previous owner's captured
terminal session, error message and all; and `USR/ANON/.login`, the second
stale login script found, with a wrong `PATH` and a `RULESFILE` pointing into
someone's personal tree.

**`puz15` and `puzzle15` are the same program**, built twice — 99.3% identical,
differing in module name and a "Goodbye." string. Both kept, both now
cross-referenced in INDEX. Worth a decision on dropping one.

**Chess:** `nchess` works and prompts "Enter #moves #minutes"; `gnuchessc`
starts its curses display; `gnuchess` finds its opening book at
`/USR/src/chess/gnuchess.book`, which is already on the disk. All of them want
the collection as `/h0`. `chess` itself appears to do nothing and is unexplained.

**The adventure programs are three unrelated systems**, which is why they read
as a muddle: `advent` is Colossal Cave, self-contained; `advcom`/`advint` are
the ADVSYS compiler and interpreter, with **no world file on the disk to feed
them**; `infocom`/`infocom.tcap` are a Z-machine playing the three Inform
demos in `GAMES/INFORM`. INDEX now says which is which.

### readme's per-directory counts had rotted, and nothing checked them

`readme` claimed 354 commands, 57 games, 3 broken and 16 rebuilt against a
tree holding 364, 62, 2 and 10. Every one was wrong. `check_disk.py` only
verified the three headline numbers, so these could drift indefinitely; it now
derives and checks the per-directory counts too. Made to fail on purpose.

### The star list was re-measured, and it holds

Every one of the 439 files in `CMDS`, `CMDS/GAMES`, `CMDS/REBUILT` and
`CMDS/BROKEN` was run with no cio present, four at a time, each worker on its
own image copy. Result: **92 trap, exactly matching `DOC/INDEX`, with no
program starred that runs and none unstarred that traps.**

The one apparent mismatch is not one: `gnuchess` names two different programs,
and `CMDS/gnuchess` traps while `CMDS/GAMES/gnuchess` does not. The star block
is a flat list of names, so it cannot say that, and the name belongs in it.

Seven never started, all four kinds already documented in INDEX: `bio`,
`wysetime` and `blackjack` are BASIC09 I-code needing `runb`; `X11R6shl` is a
trap-handler library and `rtfdat` a data module, neither a program; `who` and
`mscheck` are shell scripts.

Two static shortcuts were tried first and BOTH gave confident wrong answers --
searching binaries for `cio\0`, then for the high-bit-terminated `ci\xef`
form. The second found zero of the 92. Neither is in the tree; running the
programs is the only method that works.

## Freeware disk: two small open items


### Module-name mismatches: 53, not 7, and most are deliberate (2026-08-13)

Measured across every program directory by reading `M$Name` from each header.
Before anyone "fixes" these, three of the four groups are working as intended:

**Case only** -- `aterm`/ATerm, `atob`/AtoB, `btoa`/BtoA, `lha`/LHa,
`fstat`/FStat, `sbreak`/Sbreak, `modbuster`/Modbuster, `hexedit`/hex,
`wam.sbprolog`/SBP. The module keeps its author's capitals; the file is
lowercase so it is easy to type. Leave alone.

**Deliberate disambiguation** -- where two builds share one module name, the
FILE carries the distinguishing suffix: `cjpeg.070`, `djpeg.070`,
`rdjpgcom.070`, `wrjpgcom.070`, `emacs.mm1`, `ephem881`, `infocom.tcap`,
`kermit2`, `kermit3`, `vi_cio`, `lnk.org`, and everything in REBUILT with a
`.cio`, `.elvis`, `_csl`, `_nocsl` or version suffix, plus `ub68020demo` and
the MM/1 drivers. This is the alternates convention doing its job -- six
`gzip*` files all say `gzip` because they are the same program for different
CPUs. Leave alone.

**`ckermit` says `wermit`** -- C-Kermit's own internal name. Upstream's, not
ours.

**Genuinely accidental, and the ones the entry below means:**

| file | says | why |
|---|---|---|
| `REBUILT/compress` | `R_compress` | built without `-n=`, so the name came from the `-f=R_<prog>` output file |
| `REBUILT/kermit` | `R_kermit` | same |
| `REBUILT/screen` | `R_screen` | same |
| `hc` | `B_hc` | the original author's `B_` build prefix |
| `tabs` | `B_tabs` | same |
| `GAMES/wish` | `B_wish` | same |
| `queens` | `B_baruch` | same prefix, and a different name entirely |

The three `R_` ones are `tools/rebuild/`'s own documented trap. They could be
rebuilt with `-n=`, or the name patched in place and the CRC and header parity
recomputed -- both are proven techniques here. **But note the side effect:**
`REBUILT/compress` and `CMDS/compress` would then both be module `compress`,
and the same for `kermit`. That collision may be why the prefix was left. The
`B_` four need their source identified first; `DOC/ORIGINS` names a tree for
all but `tabs`, and the named tree has no matching `.c`.

- **7 modules still report a module name that is not their filename**:
  hc, queens, tabs, GAMES/wish, REBUILT/compress, REBUILT/kermit,
  REBUILT/screen. Each needs its source tree identified before it can be
  rebuilt with `-n=`; `DOC/ORIGINS` names a tree for all but `tabs`, but the
  named tree has no `<prog>.c` in it. `GAMES/wish` is the interesting one:
  ORIGINS lists two different `wish` programs, yet the two binaries differ by
  exactly the 2 bytes of the `B_` name prefix — so either ORIGINS is wrong or
  one copy is a stale duplicate of the other.

## Documented, with source, and no binary — the pattern to sweep for

Three found so far. The signature is a `DOC/<pkg>/` directory and a `SRC/`
tree with nothing in `CMDS/` to match, which reads to a browser as a program
that ought to be here.

- **elvis** — BUILT 2026-08-13, all nine programs. See below.
- **spline** — `DOC/spline/` (readme + makefile) and `SRC/eff_spline/spline.c`
  are here; only `mtst`, its test driver, ships. The makefile wants `tek.l`
  and `-t=/r0`, so it was built for a Tektronix-graphics machine and may not
  be worth reviving as-is. Paul William Farquhar, Augsburg.
- **snobol** — FIXED, and it was a wording problem rather than a missing
  program. `DOC/snobol/` and `SRC/effo_snobol/` describe Robert Heller's
  SNOBOL4-in-C: a C library that simulates SNOBOL4's pattern matcher. Seven
  programs advertised themselves as a "SNOBOL demo", which sent people looking
  for an interpreter that was never part of it. DOC/INDEX now says so plainly.

Worth a proper sweep: `DOC/` has 23 directories with no program of the same
name, and most are package names whose programs are named differently
(`pdksh` is `ksh`, `wolk` is `dam`/`ssl`/`ff`). Only the three above document
something genuinely absent.

## Freeware disk: elvis — BUILT, 2026-08-13

All nine programs are on the disk, built from `CMDS/archives/elvis1.7.lzh`:
`elvis`, `view`, `ref`, `elvrec`, `fmt`, `elvprsv` in CMDS, and `vi.elvis`,
`ctags.elvis`, `input.elvis` in REBUILT where the names were already taken.
All trap-free, none carrying an author stamp. `SOURCES.txt` has the recipe.

**Two things the entry below had wrong.** The zero-byte `.os9` files are not
missing link scripts — `linkelv.os9` and the rest are makefile TARGETS, and
the empty files are leftovers from the rule's own `touch $@`. Nothing was
absent. What actually stops a plain `make` is that OS-9 make has no implicit
`.c` to `.r` rule, so it stops at *"can't find source file to make blk.r"*;
drive `cc` directly instead. Also: the makefile's `-O=2` is rejected by this
`cc`, and `ctags`/`fmt` need `osk.r` linked for `perror` while `elvprsv` must
not have it.

The original entry follows, for the record.

## Freeware disk: elvis has docs and source but no binary — BUILDABLE

`DOC/elvis/` carries the full man-page set and `CMDS/archives/elvis1.7.lzh`
has the source, but the elvis binary is not on the disk. Building it would
remove a documented-but-absent program, the same class of defect as SRC/ls.

**It is not a lost cause — the OS-9 port already exists inside that archive.**
`README.OSK` says it plainly:

> version 1.7 of elvis by Steve Kirkendall, ported to os9 by Peter Reinig.
> Repacked and brushed up by Martin Gregorie and Peter Smulders.
> This port is for the old Microware C compiler (V2.3).

What is in the archive:

- `osk.c` / `osk.h` — the OS-9/68k platform layer, from upstream elvis 1.7
- `makefile` (1998), with `make`, `make install` and `make -i clob.os9`
- `alias.c` beside `alias.c.orig`, so the OS-9 patch is visible
- the `.os9` link scripts (`linkelv`, `linkvi`, `linkview`, `linkinput`) are
  all **zero bytes** in the archive — that is the one gap, and the makefile
  may not need them

It builds four programs, not one: elvis, vi, view and input. Its `ctags` is
also a free replacement for Microware's. Worth a run through
`tools/rebuild/`; the recipe would be the first that drives a whole makefile
rather than a file list.

## Freeware disk: larn plays; only its help file is absent — FIXED

The old entry here claimed larn's data was lost and the binary should move to
`CMDS/BROKEN`. That was wrong, and would have retired a working game.

larn names `.larnmaze`, `.larn.help`, `.lfortune`, `.playerids` and
`.holidays` under `/h0/GAMES/larn/PLAYGROUND` — all five strings really are in
the binary — but naming is not needing. Run with the disk as both `/dd` and
`/h0`, larn lays out a level, keeps score and takes commands with none of them
present.

Two different things were being conflated:

- **`.lscore12.0`/`.llog12.0` are written by larn, not shipped with it.** They
  were never lost. The whole defect was that `GAMES/LARN` had no `PLAYGROUND`
  under it, so larn had nowhere to write and failed with `error 216`. The disk
  now carries `GAMES/LARN/PLAYGROUND/.lscore12.0`, the scoreboard larn created
  for itself; larn reads it back on the next run without complaint.

- **`.larn.help` was absent, and so was the rest of the data** — but not
  lost. `.larn.help`, `.larnmaze`, `.lfortune`, `.holidays`, `.larnopts` and
  the original `.llog12.0` were all sitting in `h4/GAMES/LARN/PLAYGROUND`,
  on a disk we had. They are in now, and `?` shows the help.

**An earlier pass fetched 12.2p4 substitutes off the internet for three of
those.** They are gone, replaced by the originals. The version mismatch that
worried me never existed: these are what the 12.0 binary shipped with. The
lesson is cheaper than the one I wrote down — look at the disks you were
given before fetching anything.

No larn source on the disk: no `SRC` tree, nothing in `CMDS/archives/`, and
`DOC/ORIGINS` mentions neither larn nor `ularn`.

## advent — FIXED, from the same disk

`advent` stopped at "Cannot open data file /dd/GAMES/adv/glorkz" in every
image built here, the pre-tar one included. `glorkz` is Colossal Cave's 67 K
data file and it was on `h4/GAMES/ADV`. Copied in, advent loads its twelve
sections and prints "Advent is ready." Its `startup` came with it.

**Still on h4 and deliberately NOT taken: `GAMES/DOGADV`** — eight files
making an ADVSYS adventure (`dog.adv`, `dog.adi`, `objects.adi`,
`advsys.doc`). The collection already carries `advint`, the ADVSYS
interpreter, so it would run. Left out because its provenance is unknown: it
reads as somebody's own adventure rather than anything out of the archives,
and this collection only carries what it can say the origin of. Worth a
decision rather than a default.

`gnuchessc`/`gnuan` had a real missing-data problem and are FIXED — theirs was
recovered from the download pool into `GNUCHESS4.0/MISC/`.

## Build the image in CI

The build no longer needs anything proprietary — that half is done. It was
blocked because `mkimage.sh` drove `chx`, `makdir`, `copy` and `attr` out of a
Microware system disk, and none of those is on this collection. Three pieces
replaced all four:

- os9exec's internal `mount -k` writes the blank image; it needs no disk.
- `tools/mktar.py` writes `disk/` as ustar, host-side, with the finished
  disk's attributes already in the mode bits — so there is no `attr` pass.
- The collection's **own** `tar` extracts it. Unstarred, so no `cio`. `cp` and
  `mkdir` are on the disk but both are starred, so neither could have done it.

A full build takes about four seconds and is verified at 3288/3288 files and
351/351 directories.

**Still to do: the workflow itself.** This repo has no `.github`. It needs
only the os9exec binary, so a CI leg can build os9exec and then run
`tools/mkimage.sh`. Worth adding alongside it, since they cost nothing: CR-only
line endings on the text files, `DOC/DEPENDS` regenerating identically, every
module named somewhere in `DOC/INDEX`, and the star list still matching a live
measurement.

Known wrinkles, none blocking:

- **The workflow pins os9exec to a moving branch.** `arm64-uae-integration`,
  because `master` has no `mount -k` at all. A force-push or a regression
  there breaks this build with no warning. Pin to a commit SHA once the
  branch settles.
- **`DOC/DEPENDS` has no generator in `tools/`**, though it is meant to be
  regenerated whenever the tree changes. Its larn line was corrected by hand,
  twice. It is a scan of every binary for absolute paths — worth writing,
  and the only way the file can be trusted after a change.
- **The image is not byte-reproducible, by 352 bytes** — the LSN0 volume date
  and 351 directory creation dates come from the clock. Content is exact and
  `mktar.py` output is byte-identical run to run. Fixing it needs either a
  fixed clock in os9exec or a host-side pass over the finished image.

## Licence — DONE, but check the name on it

The root `LICENSE` is **not** a licence grant, deliberately. It is a statement
of terms: the collection was gathered from public archives, every program
keeps its own author's copyright, nothing here relicenses any of it, and
`disk/SOURCES.txt` is where to look before redistributing. It ends with an
offer to remove anything a rightsholder objects to.

An earlier draft put MIT at the root with a scope note. That was wrong: GitHub
labels a repository by its root licence file, so the whole collection would
have been advertised as MIT — a claim nobody here can make. The MIT text now
lives in `tools/LICENSE`, covering only what was written for this repository.
Expect GitHub to show no licence badge as a result, which is the honest
outcome.

MIT was chosen for the tooling over a public-domain dedication mainly for its
warranty disclaimer: `mkimage.sh` writes 125 MB disk images, and "AS IS" is
worth having when someone points it at the wrong path. Copyright is asserted
as "2026 Robert Doggett" — change that if it should read otherwise.

## Dropping the emulator from the build entirely

Not needed, and worth knowing the shape of anyway. Shipping a pre-made blank
image in the repo does NOT do it: populating the image is what needs os9exec,
because only the emulator can run the collection's own `tar`. A committed
blank would only relax WHICH os9exec you need — the populate step works with
a much older one than `mount -k -v=` does. A blank 125 M image is 127 KB
gzipped, 19 KB xz, so committing one is cheap if that coupling ever hurts;
the cost is a fixed size, where `mkimage.sh` currently sizes to content.

What would actually remove the dependency is writing the populate step
host-side — directory entries, file descriptors, allocation bitmap. That is a
few hundred lines of Python against a format this repo already understands.
It would also make the build instant and fully reproducible. Nobody needs it
today.
