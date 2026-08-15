# The 152 recovered archives: what is in them

Written 2026-08-14, after `tools/refetch_archive.py` restored the five pool
categories that had gone missing -- DRIVERS, EFFO, GWINDOWS, NETWORK, TELECOM.
The pool is now complete at 432 files. `notes/AUDIT-pool.md` describes the
other 281 and does not cover any of this.

## The measurement

`tools/list_new_modules.py` extracts the five categories, recurses into nested
archives to a fixpoint (the EFFO forum disks are archives of archives -- one
pass finds 8 modules where there are 538), and reads each module's real name
from `M$Name`.

| | |
|---|---|
| distinct modules | 538 |
| already on the disk | 310 |
| **not on the disk** | **228** -- of which 177 are programs |

The full list is `notes/pool-newcategories-modules.txt`; every archive member
name is in `notes/pool-newcategories-members.txt` (6508 rows).

Two parsing rules cost a pass each and are worth writing down:

- **68k module names are NUL-terminated, not high-bit terminated.** The 6809
  convention sets the high bit on the last character; reading a 68k module
  that way turns `ls` into `'ls\x00\x000'`, and every name mismatched, so the
  first run reported 228 of 228 "not on the disk" when the true figure is 228
  of 538.
- **`M$Type` at 0x12 is a whole byte** (`0x01` prog, `0x0C` system, `0x0D`
  file manager, `0x0E` driver), not a nibble.

## Do they run? 171 of 177 do

Every one of the 177 programs was run, twice: bare on the freeware disk with no
trap handlers present, then again with Microware's `cio`, `csl` and `math881`
alongside it. `tools/probe_runnability.sh` and `tools/probe_runnability_traps.sh`;
results in `notes/pool-newcategories-runnability.tsv`.

| | |
|---|---|
| run with nothing supplied | **69** |
| run once `cio`/`csl`/`math` are there -- the star in `DOC/INDEX` | **102** |
| need a trap handler nobody here has | 4 |
| no output at all, unclassified | 2 |

That ratio is close to the disk's own (369 unstarred, 135 starred), which is
the reassuring answer: this is ordinary OS-9 freeware, not a pile of wreckage.

The four that stay broken want something specific, not the usual libraries:
`striche` and `g` (an Atari GRAPH demo pair) want a trap module named `Graph`,
`lunisolar` wants one whose name does not even print, and `CyberWar` wants
`math` proper. Two more were **false alarms from the probe** and do work --
`cpu` draws its speed-test screen, and `spline` emits PostScript, which also
means it is not the Tektronix-only `spline` that `NOT-INCLUDED.md` records.

Worth recording while it was measured: **`math` and `math881` both carry the
module name `math`** -- confirmed by reading `M$Name` out of each file on the
SDK disk. Same name, two files, which is exactly why either satisfies a
program that asks for `math`.

## What this adds, by cluster

The current disk has almost nothing for communications. This is where the
weight of the haul falls.

| cluster | what | licence |
|---|---|---|
| **UUCPbb 2.1** | A complete store-and-forward mail and news system: `uucico`, `uucp`, `uux`, `uuxqt`, `uuname`, `uupoll`, `uulog`, `uuclean`, `rmail`, `rnews`, `readnews`, `postnews`, `expire`, `subscribe`, `unsubscribe`, `fileserv`, `dotilde`, `fixtext` | **GPL v2**, `copying` in the archive |
| **Elm 2.4** | Full-screen mail reader plus ~20 helpers (`frm`, `newmail`, `readmsg`, `filter`, `answer`, `autoreply`, `newalias`, `checkalias`, `fastmail`, `messages`, `printmail`, `arepdaemon`) | **Elm General Public License** -- distribution expressly permitted |
| **WN 1.14.3** | An HTTP server for OSK, with CGI examples and a hit counter. John Franks, 1996 | GPL |
| **KA9Q net (K5JB, 1994)** | TCP/IP over SLIP or AX.25 -- telnet client, ftp, smtp -- plus the `bm` mailer and the full docs | amateur-radio freeware |
| **osknet 1.2** | Networking with its own doc set (`howto`, `protcols`, `smtp`, `techref`) | Charles Hedrick, 1987, "anyone may reproduce" |
| **smail 2.5 / pathalias / philmail** | Mail routing | free, no terms stated |
| terminals & transfer | `tterm`+`xyt`, `blastem` (X/Ymodem), `sterm`, KWIN `terminal`, `gport`, `linkup`, `xydown`, `txmod`/`rxmod` | `tterm` freely distributable; KWIN `terminal` shareware but "give it to as many as you wish" |
| editors | `umacs` (MicroEMACS), `sedt` (VT220 and generic) | sedt: free redistribution to facilitate porting |
| languages | `adl` -- compiler, runtime, debugger and `adltouch` | EFFO disk 3, no terms stated |
| TeX | `dvips`, `afm2tfm`, `MakeTeXPK` | free, TeX-world terms |
| games | `backgammon`, `teachgammon`, `cyberwar`, `puzzle`, `wisecrack` | cyberwar and puzzle shareware, copying allowed; rest unstated |
| utilities | `modinfo`, `btree`, `clear`, `repeat`, `passwd`, `phone`, `trunc`, `getsys`, `spline`, `mvolformat`, `vc`, `ynad`, `xlharc` (**not** `msfm` -- see below) | EFFO disks, no terms stated |
| drivers | 10, for CT68000/CT68020 floppy, Atari OMTI hard disc, Gepard and Hercules terminals, MTH serial | EFFO disks, no terms stated |

## Excluded already, with the reason measured

| | |
|---|---|
| `rz` / `sz` (ZMODEM) | **Omen Technology commercial licence.** The archive carries the order form: $20 per user, 1-10 users, "payment of this license authorizes the installation and use". Not ours to ship. |
| `smbfm` (Samba file manager, with `samba` and `smbdrv`) | The author encourages free copying, then: *"No part of this material may be distributed with other software packages without the express permission from the author."* A curated collection is exactly that. Would need his permission. |
| `csl` | Microware's C shared library, redistributed inside `STerm68k.lzh`. Their product. It does not go on this disk, and finding it in a freeware archive changes nothing. |
| ~~`fpu`~~ | **Reversed.** Microware granted distribution in writing -- see below. It may ship as long as `fpu.doc` ships with it. |
| `msfm` (MS-DOS file manager) | Tempting -- reading and writing DOS floppies from OS-9 -- and not ours. Its own `note.doc` names the origin: Peter Dibble's *OS-9 Insights*, carrying Microware's notice that the source is *"proprietary confidential property of Microware Systems Corporation ... Reproduction, publication, or distribution in any form to any party other than licensee is strictly prohibited."* |

## EFFO's own terms

Thirty-six of the 152 archives are EFFO disks, so it is worth stating what EFFO
was. From `read_me` on disk 12, May 1990: *"The European Forum For OS-9 (EFFO)
is a non-profit, computer and company independent union of idealistic
OS-9/68k-users"*, whose stated goals include *"collection and distribution of
user written programs"* and *"management and taking care for all available OS-9
based public domain software and freeware"*, anticipating *"wide diffusion"*.

That is a distribution mandate, not a restriction. It does **not** override the
terms of individual programs carried on those disks -- the same forum disks also
carry `arc` under System Enhancement Associates' copyright, and `msfm` under
Microware's. Per-program checking still governs.

## The gathering, complete

Every one of the 177 was traced to its pool archive, run twice, and had the
terms of the archive it arrived in read by hand. `tools/gather_pool_programs.py`
builds the table (`notes/pool-newcategories-gathered.tsv`, one row per
program: origin, both runnability verdicts, licence, evidence, doc and source
counts). All 177 come from the five recovered categories and none of those 50
archives duplicates anything already in the pool -- checked, not assumed.

### Terms, by what the archive actually says

| how many | terms | note |
|---:|---|---|
| 87 | EFFO forum disk | EFFO's charter is distribution; per-program terms still govern, and most state nothing |
| 17 | GPL v2 | UUCPbb 2.1 -- **already integrated**, `CMDS/UUCP` |
| 14 | Elm licence | distribution expressly permitted |
| 10 | GPL | WN 1.14.3, the web server |
| 20 | free, but unstated | no terms found anywhere in the archive |
| 8 | shareware, distribution NOT stated | KWIN LaTerm and LinkUp -- worth asking, not assuming |
| 5 | freely distributable | tterm/xyt, XmodemUpDown ("distribute freely as long as this file is included") |
| 3 | shareware, copying expressly allowed | Carville's cyberwar, puzzle; KWIN Terminal |
| 3 | free (TeX world) | dvips and friends |
| 3 | free, needs `fpu` | Kientzle's xy/z/k, Ultra C builds |
| 1 | public domain | XYDown, in as many words |
| 1 | free, attribution | osknet (Hedrick, 1987) |
| 1 | amateur-radio freeware | KA9Q net |
| 1 | vendor demo | RCIS |
| **3** | **must not ship** | rz, sz (Omen Technology, $20/user) and smbmount (no bundling) |

**111 of the 177 carry no licence statement at all.** That is not a gap in the
search -- it is what this corpus is. People put programs on a forum disk
because they meant them to be passed around, and mostly did not write it down.
It is the same footing the rest of the collection already stands on.

### Microware granted `fpu`, in writing

`xyz.lzh` carries `fpu.doc`, and its first two lines are:

> FPU - (C) 1995 Microware Systems Corp.
> Permission to distribute FPU is granted so long as this file is retained.

So `fpu` **may** ship, provided that file ships beside it -- which reverses the
call made earlier on this page and makes the Ultra C builds (`xy`, `z`, `k`)
usable rather than dead weight. The grant is specific to `fpu`; no such words
were found for `cio` or `csl`, and those stay out.

Two different `fpu` modules turned up, 12724 bytes in `xyz.lzh` and 14572 in
`STerm68k.lzh`. Only the first travels with the grant text.

### EFFO's Info files

EFFO defined a metadata form -- `$PURPOSE`, `$AUTHOR-NAME`, `$HARDWARE`,
`$SOURCE-AVAILABILITY` and more -- and asked contributors to ship one per
program. 31 unique ones are in these archives
(`notes/pool-newcategories-effo-info.json`, `tools/parse_effo_info.py`), and
**every single one states open availability**: "public", "full source
available", "public domain". Not one is restricted.

They mostly describe programs already on the disk (beav, fgrep, sed, m4, yacc,
indent, flex, lharc), so they add little to the 177 -- but they settle the
question of what EFFO thought it was distributing.

One trap worth recording: `Info_empty_form` is the blank template EFFO ships
on every disk. It lists "shareware" among the options a contributor might
write, so a naive text search makes every forum disk look like it carries
shareware. It is skipped.

## Is the pool actually everything? Now it is

The 152 filled five empty categories, but that left the question of whether
the categories we *did* have were complete. They were not.

`tools/fill_archive_gaps.py` compares the archive's listing to the pool **by
name** and fetches the difference. Counting alone would have missed it and
lied twice over: GCC and GNU hold more locally than the site lists, because
those came from elsewhere, so a count comparison shows a surplus where there
is a shortfall.

It found **32 files missing across six categories** and fetched all 32:

| category | what came back |
|---|---|
| apps (16) | **nn 6.3.10**, **mnews** (binary and source), **mg** -- MicroGnuEmacs -- with its DVI and PostScript docs, `elm.lzh`, the HL10 zoo set, `sox.man` |
| graphics (4) | `JPEGSRC.V4`, `pbmsrc.ar`, `pbmview`, `TekDemos` |
| cmds (3) | `finger`, `hpset`, `Scsicmd 0.1` |
| misc (3) | `scsiutil`, `sector0.c`, `ucc_support_386` |
| drivers (2) | the two dvips text manuals |
| telecom (2), network (1), src (1) | WN's readmes, `samba_ref.pdf`, `elm.tar.Z` |

`nn`, `mnews` and `mg` are a threaded newsreader, a mail/news reader and the
small Emacs -- but **all three are source distributions, not binaries**.
`nn6.3.10.lzh` is 147 members of C and shell, `mg2a.tar.Z` is `mg2a/mg/*.c`,
and `mnews.t.Z` holds 200 members and not one OS-9 module. They would have to
be built, which this collection does do (`tools/rebuild/` has 203 recipes) but
which is a different job from adding a binary. Counting them as programs, as
this page first did, was wrong.

The original `download.log` also records two failures, both rejected as too
small: `APPS/btoa.readme` (87 bytes) and `APPS/sc_needs_terminfo` (18 bytes).

## Still to do

- Read the remaining licences (marked "to read" above).
- Fold the survivors into `DOC/INDEX`, `DOC/ORIGINS`, `SOURCES.txt` and the
  categories, the same as everything else.
- The 51 non-program modules -- 23 descriptors, 10 drivers, 6 data, 3 traps,
  3 subroutine, 2 file managers -- need their own decision. A driver is not
  meant to be *run*, which is the reasoning that already brought the seven
  MM/1 drivers in (`notes/NOT-INCLUDED.md`).
