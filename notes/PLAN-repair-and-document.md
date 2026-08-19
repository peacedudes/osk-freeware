# Plan — repair what does not run, document what has no docs, and finish
# looking through what we collected

Written 2026-08-18, for a day or so of unattended work while rdoggett is away.
Supersedes the "Pick up here" list in `notes/HANDOFF.md`.

## The three things asked for

1. **Everything that is not working** — find out why, and coax it into good
   where it can be coaxed.
2. **The documentation anyone would need** to use these programs — collected
   where it exists, found where it is hiding.
3. **No stone left uncovered** in what we already collected.

## Standing decisions for this pass

Settled with rdoggett before he left, and not to be relitigated:

- **Work on a branch.** `main` stays where it was. Each self-contained piece
  commits on its own once `tools/check_disk.py` passes and the image builds.
  Commit whenever it is the best moment; no approval needed per commit.
- **Nothing is pushed to GitHub.** Not this pass. The repo is not for sharing
  until rdoggett says it is.
- **`fpu` may be USED but never COMMITTED.** It is in the SDK at
  `Scraped/sdk-copyrighted/OS9/68000/CMDS/BOOTOBJS/fpu`, with `p2init` beside
  it. Run the two programs that need it, verify they work, record the result.
  The module does not enter `disk/`, and no commit contains it. Do not draft a
  permission request unless the count needing it turns out to be materially
  more than the two known.
- **Real documentation first, generated only as fallback.** What genuinely
  exists in the archives gets installed. Where nothing survives, the program's
  own measured usage output is recorded, and it is marked as measured output
  rather than dressed up as a manual.
- **Build from source wherever we have source — but do not replace working
  shipped binaries with our own builds for its own sake.** Rebuilding is a
  diagnostic and a repair, not a policy. A shipped binary that works stays.
  Host-side module patching stays available where it is the only route
  (`devprc`'s CRC, `graph`'s module name); every patched module keeps its
  original beside it and a line saying what changed and why.

- **Retire the trap-free rebuilds — see front E.** A set of programs was
  rebuilt `-qm` (trap-free, no `cio`) before it was known that `cio` and
  `csl` would ship by permission. That reason has expired and the builds are
  several times larger than the cio-linked equivalents. Toss them; use the
  cio version where one already exists, rebuild against the libraries where
  one does not.

## Where things are, now that ~/mine is closed

`~/mine` is off-limits entirely as of 2026-08-18. Everything needed was moved:

| what | where |
|---|---|
| the archive pool, 465 files, all 18 categories | `~/Developer/os9/Scraped/os9/PUBCMDS/microware-archive` |
| 32 further 68k archives, and 512 files already extracted from them | `~/Developer/os9/Scraped/os9/PUBCMDS/68k`, `68k_unpacked` |
| Microware manuals, PDF | `~/Developer/os9/Scraped/os9/resources` |
| the same manuals as text | `~/Developer/os9/Scraped/os9/txtResources` |
| the SDK | `~/Developer/os9/Scraped/sdk-copyrighted/OS9`, `~/Developer/os9/play/oskBoot` |

The manuals are Microware's. They are here to **answer questions**, not to be
copied onto the disk.

## How every claim in this pass gets made

The sweep that preceded this one produced two confident wrong numbers before
it produced a right one. The rules that caught them hold for everything below:

- **Keep os9exec's `#` lines.** They carry `E_BMID`, `E_NEMOD` and
  `unintialized User Trap`. Filtering them scored 91 dead programs as working.
- **Run in a login session whenever environment could matter.** Bare, there is
  no `TERM` and no `TERMCAP`; `aterm` and `snake` take bus errors without it
  and are perfectly fine with it. A bus error is not proof of a broken program.
- **`grep -a`, always.** Plain grep calls the stream binary and silently
  replaces a failing program's error text with `Binary file matches`.
- **Make every check fail once before believing it.** This collection has
  produced a verifier that reported 20/20 having run nothing, and a builder
  that reported 3287/3287 copies while every copy failed.
- **Distinguish "starts" from "works".** The previous sweep measured that a
  program starts. `top`, `digclk`, `draw`, `greed`, `suicide`, `mail`,
  `makedb`, `adlrun`, `wn` and `inetd` all start and all fail later.

---

# A. Groundwork — do this first, everything else depends on it

**A1. Repoint the tools at the new pool.** Eight files hardcode the old
`~/mine` path and will now fail: `list_pool.py`, `list_pool_modules.py`,
`list_new_modules.py`, `sniff_pool.py`, `gather_pool_programs.py`,
`fill_archive_gaps.py`, `probe_runnability.sh`, `probe_runnability_traps.sh`.
The last two also name an os9exec that has moved. Read the path from an
environment variable with the new location as the default, and make each tool
stop loudly if the pool is not there — a tool that silently finds nothing is
exactly the failure mode this collection keeps producing. Fix the "Where the
pool is" section of `notes/AUDIT-pool.md` in the same commit.

**A2. Make the documentation count reproducible.** `tools/install_pool_docs.py`
reads two staging directories that no longer exist and a `/tmp/undoc.txt`. The
coverage figure it worked from cannot be recomputed today. Write
`tools/doc_census.py`: for every program in `DOC/INDEX`, report whether any
file or directory under `disk/DOC` is named for it, for its source archive
(via `DOC/ORIGINS`), or for its family (via its `CMDS` subdirectory). Today's
measurement, to be checked rather than trusted: 402 of 925 covered, 523 not,
and the real hole is 325 in `CMDS` plus 58 in `GAMES` — `NETPBM` is fine
because it has a family doc tree.

---

# B. The 55 that do not run

Grouped by cause, cheapest and most certain first. Each group is one commit.

**B1. The two that want an FPU — `os9lib`, `config`.** Run both with `fpu` and
`p2init` from the SDK present. Record what they do. Then sweep all 925 for
68881 instructions and the line-F vector to find out whether the true count is
two or twenty; that number decides whether the permission question is worth
reopening, and it has never been measured. `fpu` does not get committed.

**B2. The five SNOBOL4 games — `poker`, `blackjak`, `rpoem`, `rstory`,
`stone`.** All fail identically with `Illegal instruction: 4afc`, which is
control jumping into a module header. `rstory2` and `tformat` are from the same
archive and both run, so the bug is one code path in the shared library, not
five separate faults. Full K&R source is at `SRC/effo_snobol`. Read the two
paths against each other; rebuild all seven if that is what it takes. Five
programs for one fix, and the best value on this list.

**B3. `devprc`.** Bad module CRC as shipped — stored `6CF320`, computed
`9F16E0`, header parity fine. The EFFO forum-16 copy is byte-identical and
equally bad, so this is not damage the collection introduced. Source is at
`SRC/devprc`; the recipe in `tools/rebuild/recipes.psv` is marked UNTESTED and
the makefile wants `getsys.a`, which is 68k assembly. Establish first whether
the SDK has an assembler that will take it — `as0`/`as1`/`as4`/`as5`/`as11` on
the disk are 6800/6801/6804/6805/68HC11 cross-assemblers and will not.
If it rebuilds, this is the only outright "will not load" on the disk closed.

**B4. The seven that want the `Graph` trap library.** `CMDS/GAMES/graph` IS
that library — a type-`$0B` trap module whose own module name is lowercase
`graph` while all seven programs ask for `Graph`. os9exec only found it through
a case-insensitive host filename lookup; real OS-9 matches module names
exactly. Rename the module host-side (M$Name string, then CRC, then header
parity) and confirm the seven get past "can't install trap handler".

**Then actually try the graphics.** The previous pass wrote these off as
wanting Atari hardware. **os9exec itself came from the Atari world**, so the
assumption that nothing can come of it is exactly the kind of untested
inference this collection keeps having to retract. Find out what the library
drives and whether os9exec answers any of it. The expected outcome is still
"wants hardware", but expected is not measured, and seven programs are worth
the hour.

**B5. The three that fault before their first system call — `firq`, `souper`,
`sysmem`.** All three die on `MOVEA.L (A0,$4C),A4` with `A0 = $AAAAAAA4`,
os9exec's uninitialised fill, in a login session as well as bare. `sysid`,
`sysmax` and `sysmin` are from the same suite and run. The blocking question —
whether OS-9/68000 specifies what a program is handed in `A0` at entry — could
not be settled last pass for want of a reference. **The v2.4 Technical
Reference Manual is now available in `txtResources`.** Answer it there. The
answer decides whether this is an os9exec gap with three sound programs behind
it, or three programs reading a register they had no right to. Either way it
is a real finding; do not settle it by running them.

**B6. `oleo`, `rxmod`, `trap`.** `oleo` is GNU Oleo 1.6 dying on `Illegal
instruction: 0009`. `rxmod` wants a `Vmod` trap library nobody has; `trap` is
a trap-handler demonstration reporting `tlink: -1`. Diagnose; expect two of
the three to end as documented dependencies rather than repairs.

**B7. The 28 that are silent in every stage.** The long tail, and the largest
single piece of work here:

    arepdaemon  authwn    bincheckr  biory      bootlogger  creadoc
    cron        cyberwar  dir        elvprsv    for         inetdc
    infoxpress  lfmaker   lnk        lnk.org    makecrc     pri
    ptxminst    puzzle    read_mail  rtf        scriptmaster
    splman      splprt    suse       sysid      t

Take them one at a time. Expect several classes: daemons that correctly say
nothing (`cron`, `arepdaemon`, `inetdc`), helpers invoked by another program
rather than by a person (`read_mail` is vi's, `elvprsv` is elvis's), things
wanting a data file, and things wanting hardware. `cyberwar` and `lfmaker` are
module groups containing type-`$04` window descriptors, so they want OS-9's
windowing — start there, they are the two already half-explained. `sysid` is
the genuine oddity: it prints nothing while `sysmax` and `sysmin` from the same
suite both print a value.

**B8. The ten that start and then fail — a separate list, and a separate
sweep.** `top`, `digclk`, `draw`, `greed`, `suicide`, `mail`, `makedb`,
`adlrun`, `wn`, `inetd`. Some are already diagnosed as os9exec defects
(`adlrun`'s `pFread` assertion, `inetd`'s `adapt_inetdb` pointer read) and
those stay diagnosed, not fixed. `mail` wants an `/r0` RAM disk and `makedb`
wants `/dd/usr/lib/smail/palias` — both may be satisfiable from here. Also
close out the unknown quit keys for `digclk`, `draw`, `sc`, `sh` and `vi_cio`;
`tools/try_quit.py` exists for this.

**B9. `ksh`'s interactive loop.** Demoted from the handoff's "biggest single
gap on the disk", which was wrong — `bash` and `sh` are both fully interactive,
measured on a pty this session, and both are load-bearing (`bash` runs
`SYS/login`, `sh` populates the image). `ksh` is a third shell some people
prefer, whose read-eval loop prints no prompt and executes nothing while
`ksh -c` works completely. **pdksh source is on the disk at `SRC/pdksh/sh/`**,
so this is readable rather than a black box. Worth doing, not worth doing
first.

---

# C. Documentation

**C1. Mine the archives for what genuinely exists.** Sources, in order: the
pool at its new path; `68k_unpacked`, 512 files that this project has never
looked at; and the `SRC/` trees already on the disk. Rewrite
`install_pool_docs.py` to read the pool directly instead of dead staging
directories, and to take its list of undocumented programs from
`tools/doc_census.py` rather than a file in `/tmp`. Everything installed must
be CR-only and 8-bit clean or `check_disk.py` will reject it.

**C2. Record measured usage for whatever is still bare afterwards.** The
program's own output, captured by running it, not prose written about it. Keep
it visibly distinct from a real manual — a reader must be able to tell what the
author wrote from what the program said. `verify-usage.tsv` already holds 24 of
these and is the model.

**C3. Fold the results back into the catalogue.** `DOC/INDEX` one-liners get
corrected wherever this pass finds them wrong — last pass corrected five
(`graph`, `snake`, `aterm`, `config`, `cribbage`/`crib`) and there will be
more. `DOC/DEPENDS` gets regenerated. `DOC/STATUS` gets the new counts.

---

# E. Retire the trap-free rebuilds — smaller, and for a reason that still holds

`tools/rebuild/README.md` opens with *"Everything on the freeware disk that
could be rebuilt from source has been"*, and CLAUDE.md makes `-qm` — trap-free,
needs no `cio` — a non-optional flag. That policy was set before Microware
granted permission for `cio`, `math`, `math881`, `csl` and `csl020`, which now
ship. The reason has expired; the cost has not. Measured on the disk today:

| program | our trap-free build | the cio-linked build | |
|---|---:|---:|---|
| `wc` | 14,978 | 1,430 | 10× |
| `strings` | 21,648 | 2,494 | 8.7× |
| `dirname` | 13,932 | 2,074 | 6.7× |
| `basename` | 14,004 | 2,206 | 6.4× |
| `cat` | 14,690 | 5,322 | 2.8× |

For these five the cio version is **already on the disk**, sitting in
`CMDS/REBUILT` as `*.cio`. `cat.cio` still carries its author's 1987 copyright
string, so it is the archive original rather than one of ours.

**E1. Measure the real extent first.** `recipes.psv` has 204 lines, but how
many shipped binaries are actually our trap-free builds is not recorded
anywhere. The test is mechanical: a binary with no `cio\0` reference that has
a starred counterpart in `REBUILT` or the pool. Produce the list and the total
size at stake before changing anything.

**E2. Swap where the cio build already exists.** Those five, plus whatever E1
adds. Retire our build, install the cio one under the plain name, verify it
runs with the shipped `cio` present, and keep the trap-free build in `REBUILT`
rather than deleting it — the star in `DOC/INDEX` moves with it, and a person
who strips the Microware modules out still has somewhere to go.

**E3. Rebuild against the libraries where no cio build exists.** `-qixm` in
place of `-qm`, `-n=<prog>` still mandatory. Only where the source is ours to
build and the saving is real.

**E4. Do not disturb what works for the sake of consistency.** A program with
no cio alternative and no source stays exactly as it is. This front is about
undoing an unnecessary workaround, not about making every binary uniform.

One caveat to carry: the ORIGINAL motive for rebuilding was to clear the
author stamp of whoever's SDK a binary was first built on — not `cio` at all.
Reverting to an archive binary reintroduces that stamp, and `check_disk.py`
has a check watching for exactly that. So prefer *relinking our own source*
against the libraries over reverting to an archive binary, unless the archive
binary's stamp is the original author's own and already accepted (`cat.cio` is
the example). 15 modules already ship carrying an original builder's stamp,
each with a documented reason.

---

# D. The stones not yet turned

**Find them ALL first, by content, and never by filename.** Every previous
pass has discovered another body of material it did not know about, so this
time the sweep comes before the triage. A magic-byte scan of everything under
`~/Developer/os9` finds **462 archives**: 248 LHA, 83 OS-9 `ar`, 70 compress,
29 zip, 27 gzip, 4 zoo, 1 tar. Filenames cannot be trusted — the pool alone
had 27 files whose extension was wrong and 12 with no extension at all, one of
them 1.2 MB. Keep the inventory as a committed tool, not a shell one-liner, so
the next pass starts from a number it can re-derive.

**D0. `play/h4/ARR` — 65 OS-9 `ar` archives this project has never opened.**
Found by that sweep, and the clearest example of the pattern. These are the
usenet archives `DOC/ORIGINS` cites by name, sitting in a tree nothing in
`notes/` mentions. First measurements:

  - 50 of the 65 have a matching `disk/SRC/` tree; **15 do not** — `chess`,
    `curses`, `curses.vax`, `dates`, `de`, `fft`, `pcomm`, `srt`, `unix.lib`,
    `wand3`, plus `cdecl`, `gammon`, `hack`, `phan` and `tet2`, which are the
    documented build failures. `chess` and `hack` both SHIP as binaries with
    no source on the disk — so this is the source for two shipped programs.
  - `pcomm`, `dates`, `de`, `fft`, `srt` and `wand3` have no binary on the
    disk at all and appear in no exclusion list. Genuinely unassessed.
  - **`ARR/x` holds loose C source for five shipped games that have none** —
    `pacman`, `valspeak`, `newsgen`, `worms`, `rain` — and for `joke`, `worm`,
    `play` and `ctime`, which are not on the disk in any form. `ARR/xx` holds
    three unnamed 50 KB files and an `indent` tree.

Work it archive by archive: what is inside, is it on the disk, is its source
on the disk, and is there documentation in it that `DOC/` lacks.

**D1. The 6,508 members of the 152 recovered archives.** `notes/AUDIT-pool.md`
says in as many words that nothing in them has been assessed, and that this
includes 36 EFFO forum and public-domain disks — where European OS-9 community
software actually lived. This is the largest unexamined body of material the
project has, and it is the direct answer to "things we may have missed".

**D2. `68k` and `68k_unpacked`.** 32 archives and 512 extracted files that
have never been compared against the disk at all. Among them: two more C-Kermit
builds, `aprocs`, `Aterm 2.6`, `BEAV 1.40`, `elvis 1.7` — and **the disk has
elvis documentation and source but no binary**, which is a standing open item.
Check that first.

**D3. Reconcile the 419 pool modules the disk does not have.** 274 of them are
programs. Cross them against `notes/NOT-INCLUDED.md` and `SOURCES.txt` to
separate the deliberately excluded from the never-assessed. Report the second
list; do not install anything from it unilaterally beyond obvious repairs like
a missing binary whose docs already ship.

---

# Order of work

1. **A1, A2** — groundwork, small, unblocks the rest.
2. **D — the archive inventory tool**, run over everything. Cheap, and it
   decides how much D0/D1/D2 actually contain.
3. **D2 `elvis`** — a known missing binary that may simply be sitting in
   `68k_unpacked`.
4. **E1, E2** — measure the trap-free rebuilds, swap the ones whose cio build
   already ships. Bounded, immediately verifiable, and it makes the disk
   smaller.
5. **B1, B3, B4** — the FPU pair, `devprc`, the `Graph` seven. Each either
   succeeds or fails clearly.
6. **B2** — the five-for-one.
7. **D0** — the 65 `ar` archives, worked one at a time.
8. **C1, C2** — the documentation sweep, the largest single win for a user.
9. **B7** — the 28, worked one at a time.
10. **B5** answered from the manuals; then B6, B8, B9, E3.
11. **D1, D3** — triage, reported rather than acted on.
12. **C3** — fold everything back into the catalogue; rebuild; all eight
    checks; a written log of every commit and what it changed.

## What "done" looks like for each piece

A program moves out of the failing list only when it has been **run** and seen
to work, in a login session where environment could matter, with os9exec's own
diagnostic lines kept. A program that cannot be made to work gets a written
cause specific enough that the next person does not have to rediscover it —
which module, which instruction, which missing file. "Does not run" is not a
finding; "wants a data file this collection does not have" is.
