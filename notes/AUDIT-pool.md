# Audit: what the archive pool holds, and what we left behind

Written 2026-08-12, after `lua` turned out to have been excluded on a rule
this collection contradicts 95 times over. If one exclusion was wrong, the
list needed re-reading rather than trusting.

**Answer: yes, we dropped the ball, and not by a little.** 101 of 274
archives contribute nothing to the disk. A handful were correctly left out.
Most were never assessed at all.

## Where the pool is

`/Users/rdoggett/mine/os9/xxx/os9exec/os9/PUBCMDS/microware-archive` —
281 files, 41 MB, in category directories, with a `download.log`.

`notes/DOWNLOADS-68k.md` says the archives live in `scratchpad/web/dl/` and
calls that temporary. **That path is now empty.** A session trusting the note
concludes the archives are lost; they are not, they were moved. Do not read
above `.../xxx/os9exec` — copyrighted material rdoggett cannot share lives
there.

## Method

`tools/list_pool.py` opens every archive and records its members to
`notes/pool-members.tsv` (7704 rows, 274 archives). An archive that cannot be
opened is recorded as such rather than skipped, because "we could not look"
must be visible.

- `.lzh/.lha` via host `lha lq`; `.zip` via python zipfile; `.tar/.tgz/.Z`
  via python `tarfile` (**macOS bsdtar rejects these old-format tars** with
  "Unrecognized archive format"; python reads them).
- OS-9 `.ar` and `.zoo` via **the collection's own `ar` and `zoo`**, run under
  os9exec with the pool mounted as `/h1`. `ar` is trap-free; `zoo` needs both
  `cio` and `csl`.
- One archive is still unread: `APPS/ant.ytar` — a format nothing here opens.

**A parser bug worth remembering.** The first version filtered out lines
starting with `---` to skip `lha`'s header rule. Every OS-9 permission string
also starts with dashes (`-----ewr`), so it discarded every member of every
`.lzh` and reported 4689 tidy rows of nothing. It was caught only by checking
`cal.lzh` by hand against a program known to be on the disk. Same lesson as
the rest of this project: make the check fail once before believing it.

## Correctly excluded — leave these out

- **Commercial demos.** `DEMOS/UB_68000.LZH`, `UB_68020.LZH`, `UB68K.ABS`
  (UniBasic), `LANGUAGES/OB68_116.*` (OmniBasic), `MISC/speedisk.lzh`.
- **`SHELLS/tshell.zip`** — the author's own terms say free for private use
  only, which is not redistribution.
- **PBMPLUS**, wherever it appears: the 1991 ancestor of the netpbm already
  in `CMDS/NETPBM`, which is newer, trap-free and now ships its manual.
- **`GRAPHICS/pbmdoc.ar`** — documentation for that same older PBM (1993:
  `FORMATS`, `pbm.man`, and man pages for programs we do not carry, like
  `pbmcrop` and `pbmtocbm`). Superseded by `DOC/netpbm`. Its `FORMATS` file
  is a decent short explanation of the formats if we ever want one.

## Found, and worth having — ranked by what they fix

1. **`MISC/man.lzh`** — a `man` command (`man.c`, `Man.prf`, `.man`). This
   session hand-extended `LIB/tmac.an` so `nroff -man` could format the
   netpbm pages. There was a man command in the pool the whole time.
2. **`GRAPHICS/mgif.lzh`** — a GIF viewer, and it contains **`gulls.gif`, an
   actual image**. The disk has 169 image converters and, until we wrote
   `DEMO/sphere.pgm`, not one picture. This was sitting in the pool.
3. **`APPS/trminfo1.lzh`** — 60 terminal descriptions (`adm3a`, `abm85`,
   `vt52`...). Directly useful given how much of this collection's trouble is
   termcap.
4. **`ARCHIVERS/gziposk124.tar`** — gzip built six ways, including
   `gzip68k_nocsl`, `gzip020_nocsl`, `gzipcpu32_nocsl`. Explicitly trap-free
   builds.
5. **`APPS/hl10obin.lzh`** — HomeLibrary 1.0: `Librarian`, `EditLibr`,
   `Ascii2Libr`, `Libr2Ascii`, `PrintCards`, `PrintLabels`. A complete
   six-program application, with docs (`hl10odoc.lzh`) and 74 files of source
   (`hl10osrc.lzh`). Entirely absent from the disk.
6. **`GRAPHICS/gnuplot2.0_881.tar.Z`** — gnuplot, with `1.dat`/`2.dat`/`3.dat`
   sample data. Plots to a terminal.
7. **`APPS/sox_osk.lzh`** — sox, with four `.iff` audio samples.
8. **`GAMES/informosk.lha`** — the Inform compiler and `inform.c`, plus the
   `dejavu`/`hellow` sources. `DOC/INDEX` currently says the disk plays the
   Inform demos; the compiler that makes them was here too.
9. **`MISC/xasm.ar`** — source for the five assemblers **and `asm.doc`**,
   which settles the mislabelling below.
10. **`LANGUAGES/p2c.lha`** (Pascal to C, with `libp2c.l`),
    **`LANGUAGES/xlate.lzh`**, **`SRC/msdos_diskaccess.lzh`** (94 files, the
    mtools source), **`SRC/dhry.lzh`** (Dhrystone, several builds),
    **`LIB/auxlib.ar`** (`alib.l`, `alib020.l` and nine headers).

Smaller, still real: `ccheck`, `lwf`, `hdump`, `uudecode`/`uustat`, `freeb`,
`ancient`, `dmode`, `reboot`, `alps`, `textb`, `stf`, `lgrep`, `howfrag`,
`RSDir`, `oscom10`, `libsplit`, `gsort14`, `macbin`, `fstat`, `checkfile`,
`setterm` (with `termcap.extra`), `UMusEK`, `UAC`.

And the `GNU/*.Z` binaries the old note dismissed as "162 need cio" —
`sed_1.06`, `gawk_2.11`, `m4_0.5`, `diff_1.1`, `fgrep_1.11`, `compress_4.0`,
`gtar_1_10`. Needing `cio` is not a reason; see `SOURCES.txt`.

## The assemblers are mislabelled, now from a primary source

`MISC/xasm.ar` contains `asm.doc`, which opens:

> The IBM PC **6800/01/04/05/09/11** cross assemblers
> … named `as*.exe` where `*` is any of **0, 1, h1, 4, 5, 9 or 11**

So `as0 as1 as4 as5 as11` are **6800, 6801, 6804, 6805 and 68HC11** — 8-bit
Motorola parts. `DOC/INDEX` calls them 68000/68010/68040/68050, which is wrong
for four of the five, and there has never been a 68050. `as09` (6809) is the
one entry that is right. The source (`do0.c`, `do1.c`, `do4.c`, `do5.c`,
`do11.c`, matching `table*.h`) is in that archive too, for five programs
`ORIGINS` lists no tree for.

`CLAUDE.md` also tells future sessions `as0`/`as1` are trap-free assemblers
available for rebuilding modules. For 68k work that is false.

## What has not been done

- **Nothing above has been tested.** These are archive listings, not verdicts.
  Each candidate still needs the treatment in `PLAN-runnability-triage.md`:
  run it, find what it needs, write down what happened.
- `APPS/ant.ytar` is unopened.
- Three OS-9 `.ar` archives report `ar: file not archive or damaged` after
  listing their contents cleanly — `ckfile.ar`, `fstat.ar`, `macbin.ar`.
  Trailing data, or two archives concatenated. The members list fine.
- The 101 absentees have not been checked for licence terms. `tshell` was
  caught only because someone read its readme.

## Files

- `tools/list_pool.py` — the lister, rerunnable
- `notes/pool-members.tsv` — every archive and every member
- `notes/pool-absent.txt` — the 101 with no program on the disk
