# Audit: what the archive pool holds, and what we left behind

Written 2026-08-12, after `lua` turned out to have been excluded on a rule
this collection contradicts 95 times over. If one exclusion was wrong, the
list needed re-reading rather than trusting.

**Answer: yes, we dropped the ball, and not by a little.** 101 of 274
archives contribute nothing to the disk. A handful were correctly left out.
Most were never assessed at all.

## SCOPE: the missing 152 were recovered 2026-08-14, and are NOT audited below

The five absent categories -- DRIVERS, EFFO, GWINDOWS, NETWORK, TELECOM --
were re-fetched from Microware's OS-9 Archive with `tools/refetch_archive.py`.
**The pool is now complete at 432 files.** Everything below still describes
the original 281. The 152 new archives hold 6508 members
(`pool-newcategories-members.txt`, (deleted in the 2026-08-27 notes prune; `git log --diff-filter=D --name-only -- notes/` finds it)) and nothing in them has been
assessed -- including 36 EFFO forum and public-domain disks, which are where
European OS-9 community software lived.

## Superseded scope warning (kept for the record)


`notes/DOWNLOADS-68k.md` records 17 categories fetched from the Microware
hobbyist archive. The pool directory holds 13. **DRIVERS (13 files), EFFO (36,
12.8 MB), GWINDOWS (7), NETWORK (20, 8.3 MB) and TELECOM (77, 11.2 MB) are
absent** -- 153 archives, about 34 MB, that nothing below has examined. The
pool's own `download.log` covers only the surviving 13, so those five were
fetched in another pass and not kept. (`notes/MGR.md` had the detail; (deleted in the 2026-08-27 notes prune; `git log --diff-filter=D --name-only -- notes/` finds it).)

## Where the pool is

**Moved 2026-08-18, and `~/mine` is now off limits entirely.** rdoggett
relocated everything this project needs; copyrighted source he may not share
stays behind and must not be read, at any depth.

`~/Developer/os9/Scraped/os9/PUBCMDS/microware-archive` — **465 files, 79 MB**,
in eighteen category directories, with a `download.log`. Beside it sit two
trees no audit note has ever covered: `../68k` (32 archives) and
`../68k_unpacked` (512 files already extracted). A third, 65 usenet `ar`
archives, is at `~/Developer/os9/play/h4/ARR`.

**Do not hardcode any of these.** `tools/paths.py` is the single place that
knows, and every accessor fails loudly rather than returning an empty
directory. Eight tools broke at once when this moved, because each carried
its own copy of the path.

Two earlier notes still name dead paths and cannot be trusted on this point:
`notes/DOWNLOADS-68k.md` says `scratchpad/web/dl/`, which is empty, and the
figure of 281 files above describes the pool before the 152 missing archives
were recovered.

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
The full list was `pool-modules-absent.txt`, (deleted in the 2026-08-27 notes prune; `git log --diff-filter=D --name-only -- notes/` finds it). The substantial ones:

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
- `pool-absent.txt` — the 101 with no program on the disk; (deleted in the 2026-08-27 notes prune; `git log --diff-filter=D --name-only -- notes/` finds it)

## 2026-09-22 -- the unlistable archives, listed at last (in universe)

rdoggett: *"you tried these archives in universe?  That's where they were
probably made."*  They were.  `tools/list_archive.py` now runs the DISK's own
`zoo`, `arc`, `ar2`, `lharc` and `unzip` under os9exec, all archives in one
session, and falls back to host readers only where there is no image.  **56
of the 57 archives no host tool could read are now listed**; only
`APPS/ant.ytar` resists (no reader anywhere for that format).

Two traps met: `ar2`'s listing option is `-t`, not `t` -- given `t` it prints
its usage, which reads exactly like a 12-member listing and fooled the first
pass.  And the host Zoo reader truncates a long member name to 13 characters
(`grafikde.c`) where the disk's `zoo` prints `grafikdemo.c`, because Zoo keeps
the long name in the entry's varying part.  Another reason to ask the disk.

What the listings show:

  * **`GRAPHICS/pbmsrc.ar` and `pbmdoc.ar` add almost nothing.**  They are the
    original PBM (1988 Poskanzer, adapted 1993).  Of their 25 programs, 14 are
    not on the disk by name -- and netpbm's `pnm` equivalents cover every one
    of them (`pnmcrop`, `pnmcut`, `pnmenlarge`, `pnmflip`, `pnminvert`,
    `pnmcat`, `pnmtops`, `rasttopnm`, `pnmtorast`, `xwdtopnm`, `pnmpaste`).
    The only pair with no equivalent here is `cbmtopbm`/`pbmtocbm`, a compact
    bitmap format nothing else on the disk reads and for which no sample
    ships.
  * **`APPS/hl10osrc.zoo` is already mined** -- the Home Librarian source is
    `SRC/homelibr`.
  * **`PROGRAMME/C/PROFF/ZOO/proff.zoo`**, which `proff` itself came from,
    also holds `CMDS/ltb`, never installed.  It is not a user program: ltb.c
    (which DOES ship, in `SRC/proff`) is proff's Lexical Table Builder, the
    tool that compiles `lextab.d` into `lextab.h` when proff is rebuilt.  A
    first build of it from the shipped source failed; worth an hour if anyone
    wants proff rebuildable end to end, worth nothing otherwise.
  * **`mw/dl/osk_ctexsrc.ar` (268 K) is a real candidate**: TeX in C, 41
    files, 1992.  The disk's TeX binaries come from `TeXSystem.lzh` and have
    NO source here.  Whether this source corresponds to those binaries is
    unchecked -- shipping source that does not build the shipped program
    would be worse than shipping none.
  * The rest are out of scope or already answered: the `c09_*` and
    `OS9_6X09_*` archives are 6809/CoCo (smallc, potd, qtip20, scribe40,
    uptime, verdisk, uucpsrc, helpsrc, makesrc); `rzsz_*` and `sterm.ar` are
    refused already; `LIB/unix.zoo` and `LIB/auxlib.ar` are compatibility
    headers and libraries, most of which `SRC/COMPAT` and `LIB` already
    carry; `bigdev.zoo` is one 2 MB screen dump; `scf14.ar` is an IPC patch
    note; `bix.arc` is a BIX download set.

## 2026-09-22 -- MINING PASS 1, six buckets in parallel

rdoggett wants every unmined archive put through the emulator quickly, because
an unfamiliar binary is what finds holes in os9exec and his release waits on
that confidence.  650 deduplicated archives (87 MB) were split six ways; each
agent had its own image copy, its own scratch directory and read-only access
to the repo.  Extraction host-side where the host can, and with the DISK's own
`zoo'/`arc'/`ar2' where it cannot; then `tools/smoke_pool.py' runs every
$4AFC module once, bare, stdin /nil, 8 second limit.

### Buckets 2, 3 and 6 (327 archives, 529 modules)

**What looked like an emulator finding was NOT one -- measured by the os9exec
session, 2026-09-22, and the correction matters more than the guess.**  Three
programs die when their input is /nil, and every one of them is the PROGRAM:
at EOF `scanf' never assigns, the conversion then runs on a value it never
got, and the C library's own overflow check fires TRAPV.  Real hardware would
do the same.  The `RTS' in every dump is simply the NEXT instruction, because
a TRAPV saves the PC after the one that trapped.  The read path is right:
I$ReadLn on /nil returns E$EOF in d1 as documented.  And the "emulator message
table readable from guest memory" I reported was OUR OWN disk/SYS/errmsg,
which a guest program had read in.  The programs:
  * `textb' -- SHIPPED, md5 09246838 -- prints its four prompts and dies,
    `vector=$07' at an RTS on the I$WritLn path.  The same program's 68020
    build (textb.020, same archive) reads /nil and exits 0, and the shipped
    68000 build given real input draws its Mandelbrot correctly.  A 68000/68020
    pair from one source is a bisect handle.
  * `xlisp' from EFFO pd4/pd5 (md5 f8acbfb1, NOT our copy) never sees EOF:
    re-prompts for ever, megabytes of `r' and NULs, then vector=$02 at
    I$SetStt.  The xlisp WE ship (md5 0038e019, another build) exits 0.
  * `cpu' dies vector=$07 after its banner, on a terminal as well as on
    /nil, so its trap is its own arithmetic rather than anything about EOF.
    Its "22-Sep-19126" is the program's own Y2K bug too.

**Everything else that threw an exception was the harness's own doing:**
`os9lib' (shipped, byte-identical) is the RTF Fortran LIBRARY with M$Type=1,
so the smoke driver forks it and it bus-errors on a garbage A0 -- running a
library is not a use.  `world' from TOP is a different build from ours; the
shipped one plays.  Every TIMEOUT was an interactive program waiting (rz, sz,
kermit, sc, sysmon, SEDT, dm, less, the WN cgihtml demos): none hung.

**Traps worth remembering:** five tars fell through a one-file fallback
because the filesystem is CASE-INSENSITIVE (`less.tar.Z' holds `LESS/' and the
decompressed file was `less'); `ar2' lists with `-t', not `t'; and several
archives are misnamed -- `DRIVERS/y2kit.tgz' is an LHA of the PTYS driver
source, `DRIVERS/ptylev.zip' is LHA, `EFFO/pd0.lzh' is a compress stream,
`TELECOM/rn_4_3_blars.lzh' is a text note about WN, `NETWORK/smbfm11t.zip' is
a gzip of osknet.tar, and `DRIVERS/ptxm.lzh' is a README with no members.

**Candidates these three buckets turned up** (none acted on yet):
  * `os9/top/top.tar.Z' is the big one: 117 modules, 60 not here -- the whole
    Notesfile system (notes, nfmail, nfprint...), nethack, tetrix, sokoban2,
    wanderer2, robots2, yahtzee, stevie, more, diff3, v7make, crontab, vcron.
  * `ttcp' (mw/dl/osk_ttcp.tar) -- a TCP throughput tester, which would
    exercise os9exec's new socket layer.
  * rz/sz 3.36 and 3.24 with full source; SMB file manager at six versions
    (terms REQUIRE complete unmodified distribution -- Ilja V. Levinson);
    LinkUp for KWindows; Sterm and MSterm with source; `time' and `loglist'
    from EFFO pd1/pd2; the CPUCACHE package; F68K's loader; ntp/NETTIME.
  * Source-only, no binaries: nn 6.3.10, rn 4.3 (twice), MNews, OSKBox
    (rsh/rcp/lpr over the net), uutools, rex, Vprint, view 4.5a, CTeX.

### Pass 1 complete -- all six buckets, 2026-09-22

**650 archives, 1,010 modules run, ZERO os9exec defects.**  15 exception rows:
3 programs that overflow at EOF (above), 4 runs of `os9lib' (a library the
harness wrongly forked), 2 archive builds -- xlisp and `world' -- whose
SHIPPED counterparts run fine, 1 module with a bad CRC in the archive itself
(forum13's vi), and `cpu'.  About 42 timeouts, every one an interactive
program waiting for a terminal.

**Tool lessons, both now fixed or written down:**
  * `smoke_pool.py' used one helper-script name, so two runs over one
    directory overwrote each other's script and modules ran each other's
    commands -- one bucket's table showed `cat' printing `watch's usage and
    two programs recorded TIMEOUT that never ran.  Each run now writes
    `_smoke.<pid>.sh'.
  * Archives lie about their format: `.tgz' that is LHA, `.zip' that is a
    PDF, `.zip' that is a gzipped tar, `.lzh' that is a README or a compress
    stream or a bare module, `.ytar' that is a compress'd tar.  Sniff, do not
    trust the suffix.
  * OS-9 tars write typeflag `0x20' where POSIX writes `0', so python's
    tarfile skips every member; and the host filesystem is case-insensitive,
    so unpacking `less.tar.Z' (which holds `LESS/') beside a file called
    `less' silently loses the tree.

**What pass 1 found, for pass 2 to weigh** (nothing added yet):
  * `os9/top/top.tar' -- the TOP Muenchen release, 117 modules, 59 not here:
    the complete Notesfile system (18), nethack, tetrix, sokoban2, wanderer2,
    robots2, yahtzee, puzzle15, stevie, more, diff3, hd, errno, upatch,
    V7make, watch, where, crontab, vcron, logon, rz, sz.
  * `TELECOM/rn.tar.Z' (really an LZH) -- the whole RCIS BBS, 120 modules
    with 29 man pages.
  * `omega' (540 KB, top's GAMES) -- already ruled out 2026-09-18.
  * `ttcp' (osk_ttcp.tar) and `ntp'/NETTIME -- would exercise os9exec's new
    socket layer.  BIND 4.8.3's `nslookup', `nsquery', `checksoa'.
  * rz/sz 3.24 and 3.36 with source; LinkUp and LaTerm for KWindows; Sterm
    and MSterm with source; `time' and `loglist' from the EFFO disks; the
    CPUCACHE package; F68K's loader; `isofont'; `UAC_view'; `PwDialog',
    `x9eyes', `setbgptn', `RGTool' (all want the PW/X GUI).
  * Source only, program not here: MNews, tass, nn 6.3.10, rn 4.3, OSKBox,
    compface, LinkUp, dmode, raypaint, mtools 3.6, CTeX, gdbm 1.4.
  * **Terms that forbid or restrict shipping:** the SMB file manager
    (Levinson: distribute complete and unmodified, no bundling), SYSMON (Max
    Planck "proprietary confidential"), and EFFO forum 12 carries an `msfm'
    binary -- the same name this collection already screens as Microware's.
  * The pool also holds `OS-9_6809_Level1_Source.tar.gz' WITH a copyright
    notice.  6809, out of scope, and not to be mined.


## 2026-09-23 -- MINING PASS 2, the network and BBS candidates

Four candidate groups went out in parallel.  Two are settled here.

### `ttcp' -- TAKE IT, and it found three things in os9exec's socket layer

`mw/dl/osk_ttcp.tar` (identical to `ftp/mw/OSK_NETWORK_ISP/ttcp.tar`):
README, the Unix man page, a FasTrak makefile, `ttcp.c`, the OS-9 binary
`ttcp.os9` (31,114 bytes, module name `ttcp`, links NOTHING at run time --
no `cio`, so an unstarred entry) and a SunOS a.out that is not ours.

**Terms are clean and explicit**, in the source shipped beside the binary:
"Mike Muuss and Terry Slattery have released this code to the Public
Domain."  Ported to OS-9 by Pete Kockritz, 31 July 1996.  The makefile
carries a third party's home path and would be stripped if it ships.

It runs, prints a full two-screen usage unaided, and **fails with a named
error rather than silence**: `ttcp-r: socket: 000:221 (E$MNF)`, because it
opens `/socket` and there is no stack here presenting one -- which is
exactly what `DOC/INDEX` already says of the shipped `inetd`.

**THREE os9exec FINDINGS, measured, not inferred.**  They are recorded here
because they are what the mining is for; they have NOT been sent anywhere.

  1. **`/socket` is not routed to the SPF file manager.**  os9exec
     classifies a socket path by the single prefix `/ip0`, and the
     1993-96 Microware socket library opens `/socket`, so `I$Open`
     answers E$MNF (221) and no ISP-1.x program can reach the new layer
     at all.  Repro: `ttcp -r -s`.  The shipped `inetd` and `wn` are in
     the same position.

  2. **The older library uses the direct setstat codes, which are
     unimplemented.**  With the path patched to `/ip0` in a SCRATCH copy
     of the module (nothing in `disk/` was touched), the open succeeds
     and then `SS_Bind` ($6C) and `SS_Connect` ($6E) answer E$UnkSvc
     (208): os9exec implements those operations only INSIDE an `SS_SPF`
     ($48) block, where this library issues them as the setstat function
     itself.  Same numbers, one level out.

  3. **`SS_Resv` ($6F) is answered 0 for every path -- a silent success.**
     That code with a 12-byte block is how the library asks for
     `socket(domain, type, protocol)`.  os9exec returns success having
     created nothing, so `ttcp` prints its own "socket" progress line and
     carries on holding a path that is not a socket.  This collection's
     own "make every check fail once" rule, in the emulator.

If 1 and 2 were fixed, `ttcp` stops being a for-a-real-system entry and
becomes the collection's first live network demo against a host listener.

### NETTIME `ntp' -- REJECTED, no terms

`mw/dl/osk_ntp.tar.gz`, module `ntp`, 5,938 bytes.  **No copyright, no
licence, no grant anywhere in the archive**, and the pre-OS-9 original is
not named -- only "adopted to OS9 6/14/95 by Allan R. Batteiger".  Its own
header describes it as an example of RFC 867/868, which reads like a
published textbook example, unverified.  It also links Microware's
`inetdb`, which is not ours to ship, and it prints NOTHING on failure
(`tcp_open` is `exit(errno)` with no message).  `msntp` already ships and
does the job.  Nothing here is worth the terms risk.

### RCIS BBS (`TELECOM/rn.tar.Z') -- REJECTED on terms

The file is an LHa, not a tar: 230 members, 842,542 bytes, Nov/Dec 1993.
RCIS 2.3, a multi-user dial-up BBS for OS-9/68000 K-Windows by Steve
Rottinger.  123 modules, 29 man pages, **no source of any kind**.

"All rights reserved.  RCIS Systems, Inc. Hereby grants the purchaser one,
and only one copy of this product."  It is a crippled demo with a postal
registration procedure: `rcis` and `conference` read `/dd/datafiles/licence`
and refuse to run anywhere but `/term`.  A clearer no than Notesfiles, which
merely had no terms.

Two further reasons agree.  **81 of the 123 modules are BASIC09 I-code**
(type $02/lang $02) needing Microware's `runb`, which this disk loads from
the reader's own system.  And nothing in it does anything visible without
the BBS data tree, a resident `conmod`, a modem port and that licence file
-- a usage line or a banner is the ceiling.  Its only freely-distributable
member, Info-ZIP's `zipinfo`, is ALREADY on the disk.

Worth knowing for future mining: **bash reports an I-code module as
`cannot execute binary file`**, which reads like a corrupt binary and is
not.  Check `M$Lang` at header offset 0x13 before believing it.

### BIND 4.8.3 -- `nslookup' and `nsquery' worth taking, `checksoa' is a terms question

`ftp/mw/OSK_NETWORK_ISP/bind.4.8.3.lzh`, 189 files, ported by Andrzej
Kotanski (Cracow, 23 September 1994) with gcc2 2.5.8 under OS-9 2.4 and
Microware ISP 1.3.  Pass 1 never opened this archive, so these were run for
the first time on 2026-09-23.  Binaries AND the whole source tree with the
OSK changes marked `#ifdef OSK`, plus nine man pages.

`nslookup` 85,744, `nsquery` 30,708, `checksoa` 32,520; module name equals
filename in all three.

**Terms: 4-clause Berkeley, advertising clause PRESENT**, on 95 files, and
condition (2) binds us -- shipping the binaries obliges the disk to display
"This product includes software developed by the University of California,
Berkeley and its contributors" in its documentation.  Cheap, but it has to
be written into SOURCES.txt, not merely noted.

**`checksoa` carries NO notice of any kind.**  It is the example code from
Albitz and Liu's "DNS and BIND" (O'Reilly, 1992) -- `EXAMPLES/Readme` says
so and a diff against `EXAMPLES/ch13.check_soa.c` is three include swaps and
an event block.  Unattributed example code from a copyrighted book with two
named authors is the "real question" shape, not the "unattributed but
public" shape.  Held for rdoggett.

All three RUN and fail fast with a message naming the cause: they open
`/h0/resolv.conf` (compiled in, and parsed correctly -- `nslookup` echoes
the nameserver back), then `/socket` once, then exit.  No hang, no loop.
The port is TCP-only by Kotanski's own admission.

`RES/select.c` -- a `select()` that works on SOCKMAN paths, built from the
Munich TOP group's PD implementation -- is the scarcest thing in the archive
and belongs in `SRC/` whatever is decided about the binaries.

Two defects, both the porter's, neither os9exec's: `nsquery.c` copies a
12-byte template into `char evname[10]`, and `nslookup` still looks for its
help at `/usr/share/misc/nslookup.help`, a path the port never patched.

**A SECOND, INDEPENDENT SIGHTING OF THE `/socket` GAP.**  This agent and the
`ttcp` one reached the same place from different archives, and it is worth
recording that os9exec ALREADY CARRIES a built-in `socket` descriptor
(`modstuff.c`, names `sockdvr`/`sockman`/`socket`) which `F$Link` can find
and which `I$Open("/socket")` never reaches.  Its caveat is also worth
keeping: the SDK's own `socket.l` opens `/ip0#1/tcp0` where this generation
of `socklib.l` opens `/socket`, so widening the prefix test may only move
the failure -- two generations of Microware networking, possibly two
protocols.  Four programs want it: `ttcp`, `nslookup`, `nsquery` and the
SHIPPED `CMDS/WN/inetd`.

### The six small candidates

**`strcmp' -- TAKEN, 2026-09-23.**  `SHELLS/sh75.lzh`, 6,250 bytes, and it
is the fourth of a set of which three already ship: the disk's `basename` is
BYTE-IDENTICAL to that archive's copy, so they came from here.  Same terms,
already quoted in SOURCES.txt for its siblings.  It is `test` for strings,
with `ct` (contains) and `bw` (begins with), which a shell's own test has no
operator for.  **Measured cio-less: it DOES need cio**, so it is starred and
in the grid, which is now All 315.  **Its own manual is wrong**: it says a
parameter error returns 4, and it returns 0.
**This corrects the row above** that lumped `strcmp` in with "library and
test fragments, not programs" -- it is a program, with a manual and a demo
script.

**The WN CGI samples -- worth taking, four of five.**  `TELECOM/wn2.zip`,
the OSK release: `counter`, `envi`, `doform.cgi`, `sample.cgi`, all with C
source, all under WN 1.14.3's GPL which this disk already carries.  They
were served for real through the disk's own `wn`, including a server-side
include whose counter increments across requests.  **`qr.cgi` is NOT clean**
-- "Copyright (C) 1996 Eugene Eric Kim / All Rights Reserved", built against
a cgihtml library whose source and licence are not in the archive.  Take
`EXAMPLES/counter` (1,638), not `COUNTER/counter` (1,992): the latter emits
an `<img>` per digit and those GIFs are not in the archive.  Two traps when
carding: `counter.data` must ship PUBLICLY WRITABLE or it fails, and
`COUNTER/index` carries the porter's email address, which would be published
verbatim in a served page.

**`UAC_view' -- works, and is the best thing in the batch, but has NO
terms.**  `CMDS/uac_tar.z`, 124,206 bytes, plus 15 real data files (~470 KB)
from a live 1996 OS-9/68040 VMEbus machine.  Driven on a pty it draws a full
VT100 review screen -- site `BVM4000`, 15 sessions, 116 processes, free
memory at startup, CPU type -- with menus for the process dependency tree,
hardware exceptions, interrupt and I/O monitoring.  Down a pipe it draws but
never sees `Q` (the known getc-in-raw-mode shape, not a defect).  No
copyright anywhere, author "P. Enlund"; published on Microware's own public
hobbyist archive.  The data holds no people's names.  **The no-terms
question is rdoggett's.**  This corrects the row above rejecting it as "a
private system's data viewer" -- that was decided without running it.

**REJECTED: `isofont'** -- not a program but a data module (an ISO 8859/1
screen font), derived from a font "supplied with OS-9" on Cumana's Atari ST
product, loaded by a `setscreen` this disk has not got.  **`dsw'** --
"Copyright (C) 1994 by OS-9 International and Marc Balmer ... All rights
reserved", plus EFFO's "personal use only" disclaimer.  **`j'** -- a joke
program, same magazine's copyright, whose own usage line says it "does not
provide any meaningful user-accessible functionality".

**A pool defect worth knowing**: `usenet/decoded/isofont-cumana-1991__isofont.Z`
is 3,116 bytes where the posting's own `size` line says 3,086, and a clean
re-decode gives exactly 3,086.  That is the shar off-by-one trap, so
anything else in `decoded/` should be re-checked against its size line.

### Source-only candidates, 2026-09-23 -- four judged

**`dmode' -- TAKEN** (e68753f2).  Voights 1988, Gregorie's OS-9/68000
port to 2.5 (2005).  Built -qm.  Its `rbfparams.h' is Microware's
`rbf.h' options structure copied out (OS-9 3.0 generation) and is NOT
shipped; the recipe is therefore not in recipes.psv -- to rebuild, take
the header from pool `CMDS/dmode.lzh'.  os9exec presents no RBF
descriptor modules, so the card loads the SDK's `r0' from /h1.

**`mtools' 3.6 -- ALREADY SHIPPED.**  CMDS/ms*, SRC/mtools/MTOOLS_3.6.
The pass-1 row was stale.

**CTeX (`mw/dl/osk_ctexsrc.ar') -- NOT TAKEN.**  It is Pat Monardo's
CommonTeX (1992, 41 files).  The disk's TeX says "This is TeX, C
Version 3.14" and reads `tex.pool' -- a tangle-to-C build, not CommonTeX
-- so this is not the source of anything shipped, and a second TeX adds
nothing.  Kept in the pool.

**`gdbm' 1.4 (`LIB/gdbm_1.4.t.Z') -- NOT TAKEN.**  GPL, an OSK port
(jl, 1992) of the library alone: the test programs its README lists
(testgdbm.c, testdbm.c, testndbm.c, conv2gdbm.c) are not in the archive,
nothing on the disk uses gdbm, and its dbm/ndbm layer creates `file.dir'
with link(), which RBF has no equivalent of.  Kept in the pool.

**OSKBox (`TELECOM/OSKBox.lzh') -- NOT YET; revisit when os9exec's
`/socket' front end lands.**  Ivan Powis (Nottingham, 1992): rsh, rshd,
rcp, lpr, rmt and GNU tar remote-device diffs, SOURCE ONLY (its CMDS is
empty).  Built against ISP 1.3's `socklib.l' -- the same generation as
ttcp and BIND -- which the SDK here does not carry (it has the later
`socket.l').  No licence of Powis's own; BSD notices on the BSD parts.
With a working /socket, rsh/rcp against a host daemon would be the first
live network demo, so it is worth a second look then, not before.

### `rn' 4.3 (`TELECOM/file4352') -- BUILDS, parked behind C News's relay

Bob Larson's OS-9 port of Larry Wall's rn 4.3 (Wall: copy freely, no
profit, no pretending you wrote it).  rn, Pnews, newsetup and norm.saver
all build clean on 2026-09-23 through the GNU-cpp path; the recipes, for
a tree named `rn43', are:

    rn|rn43|addng.c art.c artio.c artsrch.c backpage.c bits.c cheat.c final.c head.c help.c init.c intrp.c kfile.c last.c ng.c ngdata.c ngsrch.c ngstuff.c only.c rcln.c rcstuff.c respond.c rn.c search.c sw.c term.c util.c|CPP2 NOCOMPAT|/dd/LIB/blarslib.l /dd/LIB/termlib.l|-V=/dd/DEFS/os9unix -V=/dd/DEFS/blarsdefs
    Pnews|rn43|Pnews.c|CPP2 NOCOMPAT|/dd/LIB/blarslib.l /dd/LIB/termlib.l|-V=/dd/DEFS/os9unix -V=/dd/DEFS/blarsdefs
    newsetup|rn43|newsetup.c|CPP2 NOCOMPAT|/dd/LIB/blarslib.l /dd/LIB/termlib.l|-V=/dd/DEFS/os9unix -V=/dd/DEFS/blarsdefs
    norm.saver|rn43|norm.saver.c|CPP2 NOCOMPAT|/dd/LIB/blarslib.l /dd/LIB/termlib.l|-V=/dd/DEFS/os9unix -V=/dd/DEFS/blarsdefs

(`gethostname' comes from the driver's shim.)  Two findings on the way:
`<sgstat.h>' must come from DEFS/os9unix, whose copy adds the B50..B19200
baud codes rn's term.c switches on -- blarsdefs' copy is Microware's bare
header -- and `<sys/stat.h>' needs CPP2 because Microware's cpp will not
search -V for a name with a directory in it.

WHY PARKED: rn reads a C News spool (numbered article files, a
`group high low flag' active file at /h0/ulib/news/active), and Larson's
Pnews does not write that spool -- it drops the article in C News's
incoming directory for `newsrun'/relay to file.  The disk carries C News
as source (SRC/cnews) with only six small tools built; relay is the
`package build, not a recipe' recipes.psv already describes.  MNews's
spool is a different layout (`grp:low high' active, pointer files for
crossposts), so rn cannot sit on MNews instead.  Next step, when this is
picked up: build C News's relay and newsrun from SRC/cnews, then rn.
