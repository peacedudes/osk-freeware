# Audit: what the archive pool holds, and what we left behind

Written 2026-08-12, after `lua` turned out to have been excluded on a rule
this collection contradicts 95 times over. If one exclusion was wrong, the
list needed re-reading rather than trusting.

**Answer: yes, we dropped the ball, and not by a little.** 101 of 274
archives contribute nothing to the disk. A handful were correctly left out.
Most were never assessed at all.

## SCOPE WARNING: this audits 281 files, not the 419 that were downloaded

`notes/DOWNLOADS-68k.md` records 17 categories fetched from the Microware
hobbyist archive. The pool directory holds 13. **DRIVERS (13 files), EFFO (36,
12.8 MB), GWINDOWS (7), NETWORK (20, 8.3 MB) and TELECOM (77, 11.2 MB) are
absent** -- 153 archives, about 34 MB, that nothing below has examined. The
pool's own `download.log` covers only the surviving 13, so those five were
fetched in another pass and not kept. See `notes/MGR.md`.

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

## First pass of actual testing -- two of my top five did not survive

The list above was built from archive listings, not from running anything.
Testing started 2026-08-12 and immediately demoted two of them. Recorded
because a ranked list that is never checked is exactly the failure this
project keeps repeating.

- **`APPS/trminfo1.lzh` -- ALREADY HERE.** 28 of its 30 terminal descriptions
  are in `SYS/TERM` already. Only `c/coco` and `readme.terminfo` are missing.
  It read as absent because its members are `SYS/TERM/...` data paths, not
  program names, so nothing matched. Worth taking `coco`; not a find.
- **`ARCHIVERS/gziposk124.tar` -- MARGINAL.** `CMDS/gzip` is 77778 bytes and
  so is `ARCHIVERS/gzip_1_2_2.bin`: the disk already ships that build, and it
  is already trap-free. The 1.2.4 set adds 68020 and CPU32 variants and a
  `_nocsl` 68k build. CPU variants for hardware nobody here is emulating.
- **`SRC/msdos_diskaccess.lzh`** is the source for `CMDS/mtools`, which is on
  the disk. Useful as source; not a missing program.

**Still genuinely absent, confirmed by name against `CMDS`:** `man`,
`Librarian`/`EditLibr` and the rest of HomeLibrary, `gnuplot`, `sox`,
`inform`, `p2c`, `dhry`, `ccheck`, `lwf`, `hdump`.

### GIF images: the converters finally have something to convert

`GRAPHICS/mgif.lzh` holds `gulls.gif` (320x200), `jessica1.gif` (320x396) and
`school46.gif` (512x320), all GIF87a. Verified on the disk:

    giftopnm /h1/gulls.gif | pnmfile        ->  PPM raw, 320 by 200
    giftopnm | ppmtopgm | pnmscale -width 78 | pgmtopbm | pbmtoascii

renders a real photograph as terminal art. That is the first actual picture
this collection has ever had.

**Not shipped, pending a decision.** The porter's readme says only "I have
included some gif pictures for you to test the stuff" -- which covers the
bundle, not the photographs' own copyright. `jessica1` and `school46` look
like photographs of identifiable people, possibly children. Adding those to a
public repository on an implied 1992 permission is not a call to make quietly.
They are being used as test material only.

**`mgif` itself does not belong here.** Its own OS-9 port note: "it runs on
ST's only, if you don't change the source" -- `flicker.c` writes straight to
Atari ST graphics memory. The GIF *decoder* source is portable and is what
has value. Its author is Bill Rosenkranz, the same person who wrote this
disk's `nroff`.

## The archive-level pass was the wrong unit -- 75 modules were hiding

The first cross-reference asked "does this archive contain any program that is
on the disk?" and called the archive represented if so. That is the wrong
question. `gnu.bin.t.gz` counted as covered because `cat` and `ls` are here,
while `cp`, `mv`, `rm`, `mkdir`, `head`, `tac` and eleven more inside it had
never been looked at.

Redone at the module level -- every archive extracted, every 4AFC module found,
its name read from `M$Name` at header offset `0x0C` rather than from its
filename. **278 distinct module names in the pool; 75 are not on this disk.**
The full list is `notes/pool-modules-absent.txt`. The substantial ones:

| | |
|---|---|
| `oleo` | GNU Oleo, a spreadsheet, 403 KB. Nothing like it here except `sc`. |
| `gs403` | Ghostscript 4.03, 1.2 MB. The disk carries gs33 (3.33). |
| `gnuplot` 3.2 | Newer than the 2.0 added on 2026-08-13, with an X11 driver. |
| carlutil | Twelve of Carl Kreider's utilities -- `cmake`, `dedit`, `tplot`, `dearc`, `splman`/`splprt`/`splstat`, `charcnt`, `tcmp`, `subber`, `unp`, `bsplt68`. He wrote the `ar` this disk already ships. |
| macutils | Nine Macintosh format tools -- `binhex`, `hexbin`, `macbin`, `mcvert`, `unsit`, `macunpack`, `unmacpack`, `macsave`, `macstream`. |
| sh_utils73 | `env`, `expr`, `ggrep`, `logname`, `su`, `whoami` -- excluded once for wanting cio. |
| zoo, unzip | `booz`, `fiz`, `funzip`, `zipinfo`. |
| less | `lesskey`, `lessecho`. |
| gcc 1.42 | `cc1`, `cccp` passes. |

Not worth taking, already reasoned about elsewhere: the fifteen `pbmexec`
programs (the 1991 PBM suite, superseded by netpbm), the `updates.lzh` MM/1
drivers, `mgif`, `alps`, `uac_view`, `umusek`, and `ubdemo` (the 68020 build
of the UniBasic demo whose 68000 sibling is already in CMDS/DEMOS).

**Nothing in that list has been run yet.** It is an inventory, not a verdict.

## A trap that silently corrupts what you install

The installer converted line endings for anything that was not an OS-9 module
(4AFC magic). **Linker libraries and relocatable objects are neither.**
`libp2c.l`, both `basic.l` files and dhry's `.r` objects were rewritten
byte-for-byte LF to CR -- same file size, wrong contents, no error anywhere.
p2c and the BASIC compilers would have failed later for no visible reason.

Caught by diffing every installed file against its source. The rule is: treat
a file as binary if it contains a NUL, not if it starts with 4AFC. Verify
installs against their originals; sizes matching proves nothing when the
damage is a one-for-one byte substitution.

## `man` was chased and left out, and here is why

`MISC/man.lzh` looked like the best find on the list -- a `man` command, when
this session had just hand-extended `LIB/tmac.an` so `nroff -man` could format
the netpbm pages. It is not that program.

Its own manual (`Man.prf` in the archive) says it looks in `/dd/USR/MAN` for
`topic.prf` -- **proff-format source** -- or `topic.man`, a plain text file it
lists as-is, and otherwise forks OS-9's `help`. The macro names in its `.man`
file coincide with troff's, which is what made it look familiar, but it is a
front end for a proff-formatted manual tree, not a formatter of the troff man
pages this collection actually has.

Shipping it would mean building a `/dd/USR/MAN` of proff-format files that do
not exist, and it wants `cio` and `/PIPE` besides. `nroff -man` already reads
the 172 pages in `DOC/netpbm`. Left out; revisit only if someone builds that
manual tree.

## Closing the module list: what was taken, and what was not

Every one of the 75 absent modules has now been run or reasoned about.

**Taken** (see SOURCES.txt for terms and provenance): oleo, gs403 with its
fonts, the GNU shellutils (env, expr, whoami, logname, su), zoo's booz and
fiz, Info-ZIP's funzip and zipinfo, lesskey and lessecho, eight of Carl
Kreider's utilities, the nine macutil programs, ar2, checkfile, fstat, mines,
scqref, and six GNU text filters (head, tac, expand, unexpand, split, sum).

**Left, with the reason:**

| | |
|---|---|
| `hex` | The disk's `hexedit` is the same program under its other name. |
| `lharcs` | C-LHarc 1.01; the disk already has lha 2.08 and lharc. |
| `gtar`, `diff_1.1`, `compress_4.0`, `m4_0.5`, `sed_1.06`, `fgrep_1.11`, `lha208.bin` | Duplicates. Two are byte-identical to what ships. |
| `cc1`, `cccp` | gcc 1.42 passes; the disk carries GCC 1.39 and 2.x complete. |
| `f68k`/`os9lader` | F68K is a Forth system, not Fortran as the name suggests. Its OS-9 part is only a loader. |
| `advent0` and colossal.lzh | Already here — `GAMES/adv` holds advent0 and advent1-4.txt, and `SRC/adv` the source. |
| `gnuplot_x11` | An X11 driver, with no X11 here and no gnuplot binary in that archive. |
| `regex`, `strcmp`, `testpad`, `makecrc` | Library and test fragments, not programs. |
| `mgif`, `tplot` | Write to Atari ST graphics memory. |
| `alps` | Drives one 1980s printer. |
| `uac_view`, `umusek` | A private system's data viewer; a program that cannot get a screen address. |
| `dedit` | Will not load: error 205, E_BMID. |
| `cmake`, `dearc` | Carl's own note calls cmake obsolete; arc covers dearc. |
| `ubdemo` (68020) | The 68000 sibling is in CMDS/DEMOS. |
| the 15 `pbmexec` programs, `pbmdoc.ar` | The 1991 PBM suite and its docs, replaced by netpbm. |
| `updates.lzh` drivers | MM/1 hardware. |
| `sddemo` | Taken, actually -- see CMDS/DEMOS. |

**A second lesson about the method.** Matching only against `CMDS` produced
false positives of its own: `advent0` looked absent but lives in `GAMES/adv`,
and trminfo's terminal descriptions in `SYS/TERM`. Programs are not the only
thing a collection ships, and a name absent from `CMDS` is not a name absent
from the disk.

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
