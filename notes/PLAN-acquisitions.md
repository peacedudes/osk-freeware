# Acquisitions -- what "the works" still lacks, and how to bring it in

Started 2026-09-11.  Self-contained: a session picking this up needs only this
file, `CLAUDE.md`, and the recipe below.

rdoggett, 2026-09-11: the collection is "mostly a collecting project ... we're
sort of calling ourself the works.  If there is an os9 group that has code and
we're not including it, we should be."  Era: late 1980s to the mid-1990s;
1997 is fine when the thing is worth it; a modern rewrite of a period program
is not a substitute.  `which` and `whereis` (commit `f838ddf2`) are the model:
found in the archives, adapted to OS-9, carded, tested, committed in an evening.

**"There is plenty to do, but we have working tools."**  Work the batches in
order, a few programs at a time, and retry the unreachable archives a little
each day (see "Recovery, day by day").

---

## Where the material is

Everything the 2026-09-11 searches downloaded is kept, outside the repo, at

    ~/Developer/os9/Scraped/acquisitions-2026-09-11/
      os9/top/        TOP release 2 (top.tar.Z, 8.9 MB) and its members
      os9/mw/         Microware archive files fetched by ID; mw/{osk,mm1,m6809,m6809b}.tsv
                      list the whole archive (5,059 files, 250 categories)
      os9/ftp/        funet os9 listings; ftp/mw-tree.tsv
      os9/usenet/     comp.os.os9 threads from the utzoo copy
      os9/community/  third-party OS-9 sites
      os9/REPORT-top-draft.txt   TOP member-by-member notes
      unix/posts/     every opened Usenet posting, each with a URLS file
      unix/net2/      net2.tar.gz and extracted candidates
      unix/altsrc/    subjects.tsv indexes all 12,026 alt.sources articles
                      (funet, Aug 1989 - Dec 1996); cand/ holds candidates
      unix/*-index*.txt, dirs-*.tsv   per-volume listings of the source groups

URL prefixes used below (all fetched successfully on 2026-09-11):

    CSG  https://ftp.sunet.se/mirror/archive/ftp.sunet.se/pub/usenet/ftp.uu.net/comp.sources.games
    CSM  .../ftp.uu.net/comp.sources.misc        CSU  .../comp.sources.unix
    CSR  .../comp.sources.reviewed
    ALT  http://ftp.funet.fi/pub/archive/alt.sources
    NET2 https://www.tuhs.org/cgi-bin/utree.pl?file=Net2/usr/src
         (tarball https://www.tuhs.org/Archive/Distributions/UCB/Net2/net2.tar.gz)
    44BSD https://www.tuhs.org/cgi-bin/utree.pl?file=4.4BSD/usr/src
    MW   https://microware.com/index.php/os-9-archive-new/file/<ID>-os-9-archive
         (the file comes back from a POST of that page's form --
         tools/refetch_archive.py does it)
    TWN  https://usenet.trashworldnews.com/?thread=<N>  (utzoo; archive.org
         withdrew its copy in 2020)

**Licences.**  Net/2 is BSD 4-clause (keep the notice, carry the Berkeley
acknowledgement -- whereis shows how).  Do NOT take `units.c`, `bc.y` or
`dc.c` from 4.4BSD: those carry the encumbered "subject to the Berkeley
Software License" wording.  Every licence quoted in the batches below was
read out of the file itself; "no notice" means a grep for copyright, public
domain, permission and distribute found nothing.

**The pool's filenames are shifted** in `Scraped/os9/PUBCMDS/microware-archive`
categories DRIVERS, EFFO, GWINDOWS, NETWORK and TELECOM: names do not match
contents (`TELECOM/file4352` is rn 4.3; `TELECOM/rn.tar.Z` is the RCIS BBS).
Name a pool file by what `file`/its listing shows, never by its filename.

---

## Open questions for rdoggett (do not ship these until answered)

1. **"Free, but non-commercial" terms.**  TOP's os9lib, vcron, scpp; the rogue
   clone; agrep 2.01; MNews; PtyMan.  Accept, recorded in SOURCES.txt?
   (Recommendation: yes.)
2. **GPL source for binaries already shipped.**  The disk ships gcc, g++, VH
   and dvips binaries without their source trees.  Sources exist: MW 4073,
   4074 (gcc 1.42, g++ 1.39.1), funet
   `pub/unix/os9/gnu/gcc-1.37.1-osk-src.tar.Z`, pool `MISC/vh_1.4.lzh`, pool
   `DRIVERS/nulman.lzh` (dvips 5.5, misnamed).  0.6-1.4 MB each.
   (Recommendation: add them.)
3. **`jive` (1987, comp.sources.games v01i003).**  It builds and runs --
   `Sheeit, dis be a big-ass scribblin'` -- but it is a joke filter built on
   a racial caricature of Black speech, and a gallery card would showcase
   that.  Held, not shipped.  Everything needed is kept at
   `Scraped/acquisitions-2026-09-11/unix/jive-built-2026-09-11/` (flex output,
   `libl.c` for `yywrap`, the posting, the built module).  Ship or leave?
4. **`xmas` signs off "from The ghost of Robert past"** -- the OS-9 port's own
   change to the line the source invites you to change.  Kept as the port
   shipped it, with nothing on the card saying whose it is.  Say if it
   should read otherwise.

Settled: the Star Wars ASCIImation is dropped (no grant from its author).
`sl` is left out (only a 2015 rewrite survives).  The VT100 `.vt` movies are
not worth adding.

---

## The recipe for one program -- as which/whereis went

1. **Keep the original.**  `disk/SRC/<tree>/ORIG/` holds the posting's files
   byte-for-byte (CR line endings, check the shar's own character counts).
2. **Adapt in `disk/SRC/<tree>/<prog>.c`**, K&R, with a header note saying
   what the OS-9 version changes and why.  Read `tools/rebuild/README.md`
   first.  Traps met on which/whereis:
   - a path opened `S_IEXEC` alone cannot be read (I$Read wants read or
     update mode) -- open `S_IEXEC | S_IREAD` to read a file found via chx;
   - RBF directory entries are 32 bytes: 28-byte name, top bit on the last
     character, 4-byte FD sector; `opendir`/`readdir` in clib.l work too;
   - `open(path, S_IREAD | S_IFDIR)` is the cheap "is it a directory" test.
3. **Recipe line** in `tools/rebuild/recipes.psv`; `tools/build.sh <prog>`
   builds `-qm` into `built/`; copy to `disk/CMDS`, `chmod 755`.
4. **Try it on a test image**: `SKIP_CHECKS=1 tools/mkimage.sh ...` is for a
   test image only, never before a commit; `tools/drive.py <scratch>.drive`
   for Bash, `tools/os9try.py -c "<cmd>"` for Microware's shell (with
   `OS9SDK` set, `/h1` is the SDK).
5. **Paperwork**: `DOC/INDEX` entry (what it does, no author), `DOC/ORIGINS`
   line (a kind `gen_catalog.py` knows -- add one to `ORIGIN_KINDS` if
   needed), `SOURCES.txt` entry (source URL, licence as stated, what the
   OS-9 version changed), `tools/categories.psv`, `tools/help.psv`,
   `DOC/<prog>/` reader documentation.
   **Edit CR files in binary or with `newline=""`.**  Python's text mode turns
   CR into LF on read; an anchor with `\r` then never matches, and writing the
   text back would make the whole file LF.
6. **Card** in the right `tools/screenshots/*.sheet` (the `try` line, a
   window wide enough for the output), shot with
   `tools/screenshots.py <sheet> --only <prog>`; `python3 tools/helpcap.py
   --only <prog>`; verify with `tools/os9try.py <sheet> --only <prog>`.
7. **Cases** in an existing `tools/datatests/*.cases` family; **make each fail
   once** (copy with a broken expectation, see FAIL) before believing PASS.
8. `tools/gen_depends.py disk`, `tools/gen_screens.py`, `tools/gen_catalog.py
   disk`, a real `tools/mkimage.sh`, then `tools/check_disk.py disk` --
   **gate on its exit status**.
9. **Commit only your own paths**, never `git add -A`.

---

## Two sessions, one tree

The main freeware session (osk-freeware-57 on 2026-09-11) is the primary in
this repo.  An acquisitions session works beside it:

- **Claim a batch by message** (SendMessage) before starting it, and say when
  it is committed.  The committing session marks the batch's status line in
  this file in the same commit.
- **Shared generated files -- `DOC/DEPENDS`, `DOC/CATEGORIES`, `README.md`,
  `docs/` -- are regenerated by one session at a time.**  Announce before
  regenerating or rebuilding `osk-freeware.dd`, and say when done.  A
  harness that only needs to try things uses a scratch copy of the image.
- The primary may have uncommitted work in the tree at any moment; stage by
  path.

---

## The batches, in order

Status: `open`, `claimed <session>`, or `done <commit>`.

### B1 -- already on the disk as source, never built    done 2026-09-11: worm, xmas; jive held (Q3)
- `xmas` (asciixmas, Larry Bartz 1989): `disk/SRC/hc_loose/xmas.c`, which already
  carries an OS-9 `cc ... curses.l termlib.l` line.
- `worm` (BSD growing-worm game): `disk/SRC/toys/worm.c`, never built by the toys
  makefile; Net/2 copy is 6,125 bytes (curses, alarm, signal).
- `jive`: `jive.l` in `CSG/volume1/jive-val.gz` (1987, no notice); its sibling
  `valspeak` already ships from the same posting.
Done when: each runs, has its card, a case, and INDEX/ORIGINS/SOURCES lines.

### B2 -- unshar    done 2026-09-11 (cshar 2.0 pl3; 30/30 files identical to sh)
cshar (Rich Salz, 1988): `CSU/volume15/cshar/` part01-03 + patches, 182,681 b,
public domain ("do what you want, but let your conscience be your guide").
Its `parser.c` interprets shell archives itself, so unshar needs no sh --
and the disk's `shar` is broken.  Unlocks every other shar posting here.
Done when: `unshar` unpacks the which6 posting on OS-9 byte-identically
(the shar's own counts: which6.c 5970, which.1 2384, Makefile 443).

### B3 -- Net/2 small tools, one batch (BSD)    done 2026-09-11: 16 + look; leave not ported (forks and sleeps)
From `NET2/usr.bin/` and `NET2/games/`, all K&R and stdio unless noted:
`look` (or `CSM/volume5/s5look.gz`, PD 1988), `fold`, `comm`, `column`
(stub one ioctl) and `colrm`, `col` and `ul` (termcap; useful since nroff
ships), `tsort`, `factor` and `primes`, `caesar`, `morse`/`ppt`/`bcd`,
`number`, `rev` (`44BSD/usr.bin/rev`, BSD 4-clause), `yes`, `leave`.
Checked absent by FUNCTION against INDEX and against Microware's commands.

### B4 -- period Usenet utilities                                       open
| prog | source | date | terms as stated |
|---|---|---|---|
| cdecl | `CSU/volume14/cdecl2/` (or `CSU/volume6/cdecl.gz`) | 1988 | no notice |
| tput | `CSU/volume7/tput2.gz`; djb-tput `ALT/volume93/May/930530.05` | 1986/93 | public domain |
| mmv | `CSU/volume21/mmv/` | 1990 | "may be used and distributed freely" |
| xd (reversible hex dump) | `CSM/volume37/xd/` | 1993 | public domain |
| slice (csplit-like) | `CSU/volume13/slice.gz` | 1988 | free, keep notice |
| calendar (Minow) | `CSU/volume3/calendar.gz` | 1986 | no notice |
| remind 2.3.0 | `ALT/volume91/Feb/910220.09,.12,.18,.19` | 1991 | free, do not charge |
| units | `CSM/volume7/un.gz` (1988, copyright, no terms) or Mariano 1993 via NetBSD `usr.bin/units/units.c` (BSD, ANSI) | | |
| rot13 | `ALT/volume91/Jan/910130.04.gz` | 1991 | public domain |
| nums/series/numbers | `CSU/volume4/nums.gz`, `ALT/volume94/May/940525.37.gz`, `ALT/volume93/Feb/930217.05.gz` | | no notice / "No copyrights" |
| xargs | `CSU/volume3/xargs.gz` (uses system) | 1986 | no notice |
| vilearn | `CSM/volume33/vilearn/` | 1992 | permission granted |
| calc (trig, many bases) | `CSU/volume14/calc.gz` | 1988 | redistribute at will |
| agrep 2.01 | `CSU/volume26/agrep-2.01/`; also MW 4310 | 1992 | non-profit only -- **Q1** |
| vttest | `CSU/volume7/vttest/` | 1986 | non-commercial -- **Q1** |
Not found anywhere searched: `nl`, true `csplit`, a clean `dc`, apropos/whatis.

### B5 -- OS-9-native programs and code                          mimecode done
| prog | where | date | terms | note |
|---|---|---|---|---|
| Browse (P. da Silva, OSK port C. Emde) | TWN 653558 (3 parts, complete) | 1990 | none in the port | K&R + termcap + os9lib; help at `/h0/SYS/browse.hlp` |
| unc (68000 module disassembler) | pool `SRC/unc.lzh`; MW 4308 | 1991 | none | links `GNULIB/os9lib.l` |
| almanac 3.2 (J. Semler) | MW 2313 (has almanac.OSK) | ~1992 | none | terminal card candidate |
| freeb | MW 3921; TWN 653668 | | PD | |
| howfrag | MW 4223 | | PD | |
| uustat, ancient, hdump/undump | MW 3970, 3894, 3928 | | per item | |
| dumpinit (init module lister) | MW 2240 | ~1994 | none | generic though filed MM/1 |
| mimecode (base64) | MW 2503 | 1995 | author's permission | DONE -- built -qm, tested, carded; Tim Kientzle/DDJ, Gene Heskett's OS-9 pack |
| zc ZipCode + ZIPDATA | MW 2248, 2250 | 1995 | PD | needs `/dd/sys/zipcodes.txt` |
| os9dsk / rsdsk (read CoCo .DSK images) | MW 2244, 2246 | 1995-97 | freely distributed | |
| BIX one-page telecom (Dibble/Schmitt) | TWN 653653 | 1989 | distribution permitted | teaching example, asm |
| OS-9 International code disk (EFFO) | MW 5041 `effo.lzh` -> `EFFO/OS9_INTERNATIONAL/*.lzh` | 1993-94 | EFFO: personal, not commercial/military | disp SCF driver in C, lfcrman, watchdog, cache control; for real OS-9 |
| EFFO system examples | pool `EFFO/forum16.lzh` SOFTWARE/ASSEMBLER (4007); `forum12.lzh` SOFTWARE/C/ERROR (4003) | 1990-91 | "Public" | uacct, exception handler, F$CCtl/F$Permit bindings |
| kings, vt100 (MM/1 tree, terminal) | MW 2191, 2180 | 1991-95 | mostly unstated | |
| dvi2tty (+ Common TeX source) | MW 3861, 3860 | ~1991 | see ctexdoc.ar | disk has TeX and no DVI viewer |
| BRU/OS-9 1.2 | MW 2330 | 1991 | GPL-style | 6809 C, plausible port |
| rnclone 1.0 | MW 3740 | 1993-94 | free, keep head comments | 6809 C, has 68k porting notes |
| K5JB k37 source (for shipped `net`, `bm`) | https://github.com/johnsonjh/k5jb | 1993-95 | no licence file | check it matches the binaries |

### B6 -- TOP, "The OS-9 Project", release 2 (Munich 1989-90)           open
https://ftp.funet.fi/pub/unix/os9/top.tar.Z (8,900,473 b; index beside it);
the same release per file in MW category 159-top (IDs 4489 on).  Local:
`acquisitions-2026-09-11/os9/top/`, notes in `os9/REPORT-top-draft.txt`.
Effectively none of its 564 members is on the disk or in the pool.
- NetHack 3.0f pl5 OSK (F. Kaefer): `USR/GAMES/CMDS/nethack3.Z` + data; NetHack GPL; binary only.
- UMoria: binary + 59-file source (`USR/SRC/moria.t.Z`) -- a `-qm` rebuild is possible.
- Omega 0.71 beta: binary + `LIB` (56 files); Omega's own terms not included.
- Games with source: tetrix, yahtzee (HCR), gnugo 1.1 (GPL), bandit (PD), bs, typefast, sokoban2, wanderer2 (+30 screens).
- OS-9-native, binaries only, no terms stated: oxm mailer, notes + 20 nf* tools, mmenu, mwb, mmon, logon, watch, timeout, getinfo, errlog/erradm, **mw (Mazewar, 8 players)**, sod, robots2, speak, msg, uid, where, times, wns, dc, hd.
- Sources: os9lib (54 .c + 32 man; non-commercial -- **Q1**), vcron (don't sell -- **Q1**), v7make (PD), cpp.decus (PD), scpp (**Q1**), cdecl, clock.  Leave `zmodem.t.Z` (no grant).
Measure first: which binaries need cio (run against an image without the
five runtime modules); every hardcoded `/h0/USR/GAMES/...` path; whether
the native tools expect `/dd/SYS/utmp`, group, password or smail.

### B7 -- games and screen toys                                         open
| prog | source | date | terms | port |
|---|---|---|---|---|
| phoon (Poskanzer) | `CSU/volume8/phoon.gz` | 1987 | permission granted | DONE (fc775046) -- numeric date, tws.c stands in for libtws |
| globe (Poskanzer) | `CSM/volume43/globe/part01.gz` | 1994 | permission granted | stdio |
| atc | `NET2/games/atc` | 1990 | BSD | curses, lex/yacc, setitimer->alarm |
| canfield (+cfscores) | `NET2/games/canfield` | 1980 | BSD | curses, easy |
| trek (Allman) | `NET2/games/trek` | 1980 | BSD | sgtty/select bits |
| monop, wump, fish, arithmetic | `NET2/games/...` | 1980-90 | BSD | monop has a fork to remove |
| bs (ESR battleships) | `CSG/volume8/bs/part01.gz` | 1989 | no notice | curses |
| scrabble | `CSG/volume6/scrabble/` | 1989 | redistribute in any manner | curses |
| saa (Streets and Alleys) | `CSG/volume12/saa/` | 1991 | permission granted | curses |
| accordian | `CSG/volume15/accordian/` | 1992 | public domain | curses |
| mastrm | `CSG/volume2/mastrm.gz` | 1987 | public domain | stdio |
| hexa (hexagonal sokoban) | `ALT/volume93/Jan/930127.01.gz` | 1993 | no notice | curses |
| corewars | `CSG/volume6/corewars/` | 1989 | public domain | curses |
| castle | `CSG/volume8/castle/` | 1990 | public domain | curses |
| othello3 / reversi | `CSG/volume12/othello3/`; `CSG/volume15/reversi/` | 1991-92 | free / GPL | curses |
| jotto, conn4 (Sicherman) | `CSG/volume11/jotto/`, `CSG/volume12/conn4/` | 1990-91 | no notice | |
| yahtzee2 | `CSG/volume8/yahtzee2/` | 1989 | no notice | one fork |
| rot2.2 ("software rot") | `CSG/volume1/rot22.gz` | 1987 | no notice | name clashes with CMDS/rot |
| flicker | `CSG/volume5/flicker.gz` | 1988 | no notice | ANSI escapes |
| ASCII plasma | `ALT/volume93/Feb/930203.12.gz` | 1993 | no notice | VT100 |
| Toon 1.0, Juggle 1.0 | `ALT/volume94/May/940508.36-.40`; `ALT/volume95/Apr/950426.08.gz` | 1994-95 | GPL | curses, setitimer |
| rogue 5.3 clone (Stoehr) | `CSG/volume1/rogue/` | 1987 | not for profit -- **Q1** | curses, sgtty |
| gnugo, napoleon, adven2 | `CSG/volume6/gnugo/`, `CSG/volume17/napoleon/`, `CSG/volume11/adven2/` | 1989-93 | GPL/GPL/none | napoleon ANSI |
| text toys: spew, silly.tar (kraut, b1ff, chef, fudd) | `CSG/volume1/spew.gz`; `ALT/volume92/Dec/921220.11` | 1987-92 | spew free; silly mixed | lex |
Leave: cdungeon ("COMMERCIAL USAGE STRICTLY PROHIBITED", Infocom); hearts,
dots2, diph (sockets/fork/select); X11-only; umoria/omega/nethack from Usenet
(TOP has OSK builds -- B6).

### B8 -- bc                                                            open
GNU bc 1.01 `CSR/volume01/GNU_bc/` (Nov 1991, GPL, K&R-safe, yacc/lex --
bison and flex ship) or C-BC (Hopkins) `ALT/volume93/Oct/931006.03-.07.gz`
(1993, public domain).  Nothing on the disk does arbitrary precision.

### B9 -- news and pseudo-terminals                                     open (Q1)
MNews (Dessauer) MW 3840/3841; tass pool `TELECOM/tass.lzh` (needs MNews'
8bit.l); rn 4.3 pool `TELECOM/file4352`; nn 6.3.10 MW 3843.  PtyMan 1.3 /
PtyDrv (Mellin) TWN 653174 + 653173 (source), 653172 (binaries); MW 3990,
3989; 1995 fixes in pool `DRIVERS/rtclock1287.lzh` -- a file manager for
real OS-9 (os9exec will not load one).

### B10 -- GPL source for shipped binaries                              open (Q2)
See open question 2.

### B11 -- 6809 C that plausibly ports                                  open
jumble, unTC (PD), Solve (PD), Spencer regexp, uptime, verdisk, sgrep, sortc,
SmallTeX, bawk, disa 1.00 (TWN 653675): MW 2464, 2677, 2864, 3697, 3712,
3713, 2575, 2588, 2594, 2585, 2324, 2751.  Also 1990 IOCCC entries (pool
forum16), editline (CSM v31, OS-9 support), pscat (`#ifdef OSK`).

### Leave alone
Microware-owned: 6809 system source, PIPELINES, Training, qpascal, ucc
support, csl/fpu inside STerm68k.lzh, bfed.  Restrictive: StG V3 BBS,
grammar.ar, OAI, CEnv, Dominion, QuickSpell, mplay/hrecplay (shareware),
Solitaire (begware), K9 FidoNet parts, reboot.lzh.  Hardware-bound: MM/1
viewers/screensavers/sound, IronCurtain, gr_classic, CD-i, X68000 PWIN,
G-Windows fonts.  Networking that needs Microware ISP (rdate, ttcp, bind,
boa, wn 1.16.7) is for real systems only -- later, if at all.

---

## Recovery, day by day

On 2026-09-11 these refused or were not found.  Retry a few each day, log
the outcome here, and fold anything found into a batch above.

| target | what it should hold | 2026-09-11 |
|---|---|---|
| Google Groups comp.os.os9, sub.os.os9, de.comp.os.os9 | comp.os.os9 mid-1991 to 1996 (utzoo stops mid-1991) | HTTP 429 |
| de.comp.sources.os9 | moderated German OS-9 source group, early-mid 90s | no copy found |
| Wayback: chestnut.cs.wisc.edu, lucy.ifi.unibas.ch, German university OS-9 FTPs | 1990s OSK FTP mirrors | HTTP 429 |
| ftp.uni-kl.de, ftp.informatik.uni-hamburg.de, ftp.leo.org, ftp.cs.tu-berlin.de, ftp.informatik.tu-muenchen.de, ftp.ethz.ch | same | no connection |
| os9forum.de, os9.org, effo.org, ftp.rtsi.com | OS-9 community archives | no connection |
| minkirri.apana.org.au | Australian OS-9 archive | timed out |
| usenetarchives.com | Usenet | HTTP 403 |
| comp.sources.misc v48+, comp.sources.games v19+ | later postings | no mirror found |
| alt.sources 1987 to mid-1989, May 1992, April 1993 | gaps in funet's copy | not on funet |
| EFFO PD disks 100-123 (1993-95), forum disks 18 and 19 | EFFO material after what the pool has | not found |
| OS-9 Users Group disk library | user-group software | not found |
| CompuServe OS9 SIG library | names survive at lcurtisboyle.com: cawf, defrag, dskcat, hpdisp, spel68, aplrts, swtool, g261 | files not found |
| colorcomputerarchive.com (~150 OS-9 zips), archive.org `cdrom-coco-archive` | 6809 OS-9, some C | few opened |
| Microware archive, the rest | `os9/mw/*.tsv`: 127 OSK files the pool never fetched, the MM/1 tree (84), USERGROUPS, BENCHMARKS, FAQ, DOCS (incl. a 1994 chestnut.index) | listed, not all fetched |

### Recovery log
- 2026-09-11: first sweep; table above.
