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

That ratio is close to the disk's own (360 unstarred, 134 starred), which is
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
| **WN 1.14.3** | An HTTP server for OSK, with CGI examples and a hit counter. John Franks, 1996 | GPL (confirm before shipping) |
| **KA9Q net (K5JB, 1994)** | TCP/IP over SLIP or AX.25 -- telnet client, ftp, smtp -- plus the `bm` mailer and the full docs | amateur-radio freeware (confirm) |
| **osknet 1.2** | Networking with its own doc set (`howto`, `protcols`, `smtp`, `techref`) | Charles Hedrick, 1987, "anyone may reproduce" |
| **smail 2.5 / pathalias / philmail** | Mail routing | to read |
| terminals & transfer | `tterm`+`xyt`, `blastem` (X/Ymodem), `sterm`, KWIN `terminal`, `gport`, `linkup`, `xydown`, `txmod`/`rxmod` | `tterm` freely distributable; KWIN `terminal` shareware but "give it to as many as you wish" |
| editors | `umacs` (MicroEMACS), `sedt` (VT220 and generic) | sedt: free redistribution to facilitate porting |
| languages | `adl` -- compiler, runtime, debugger and `adltouch` | to read |
| TeX | `dvips`, `afm2tfm`, `MakeTeXPK` | to read |
| games | `backgammon`, `teachgammon`, `cyberwar`, `puzzle`, `wisecrack` | to read |
| utilities | `modinfo`, `btree`, `msfm` (an **MS-DOS file manager**), `clear`, `repeat`, `passwd`, `phone`, `trunc`, `getsys`, `spline`, `mvolformat`, `vc`, `ynad`, `xlharc` | to read |
| drivers | 10, for CT68000/CT68020 floppy, Atari OMTI hard disc, Gepard and Hercules terminals, MTH serial | to read |

## Excluded already, with the reason measured

| | |
|---|---|
| `rz` / `sz` (ZMODEM) | **Omen Technology commercial licence.** The archive carries the order form: $20 per user, 1-10 users, "payment of this license authorizes the installation and use". Not ours to ship. |
| `smbfm` (Samba file manager, with `samba` and `smbdrv`) | The author encourages free copying, then: *"No part of this material may be distributed with other software packages without the express permission from the author."* A curated collection is exactly that. Would need his permission. |
| `csl` | Microware's C shared library, redistributed inside `STerm68k.lzh`. Their product. It does not go on this disk, and finding it in a freeware archive changes nothing. |
| `fpu` | Ships with the same archive, and `xyz`'s own readme says its binaries need it because they were built with Ultra C 1.3. Same answer -- but `xyz`'s **source** is there, so `xy`/`z`/`k` can be rebuilt instead. |
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

## Still to do

- Read the remaining licences (marked "to read" above).
- Fold the survivors into `DOC/INDEX`, `DOC/ORIGINS`, `SOURCES.txt` and the
  categories, the same as everything else.
- The 51 non-program modules -- 23 descriptors, 10 drivers, 6 data, 3 traps,
  3 subroutine, 2 file managers -- need their own decision. A driver is not
  meant to be *run*, which is the reasoning that already brought the seven
  MM/1 drivers in (`notes/NOT-INCLUDED.md`).
