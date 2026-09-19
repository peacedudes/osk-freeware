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

## Rulings from rdoggett -- ALL FOUR ARE ANSWERED

This is a record, not a queue.  **The live list of what needs him is
`notes/FOR-RDOGGETT.md` and nothing else.**  Two files holding open
questions is how both came to hold answered ones; if something here
reopens, it goes there, not back into this section.

1. **"Free, but non-commercial" terms.**  TOP's os9lib, vcron, scpp; the rogue
   clone; agrep 2.01; MNews; PtyMan.  **SETTLED 2026-09-11: accepted.**
   rdoggett, asked once too often: *"I don't understand the question.  I
   thought we have had os9lib for awhile, and used it to compile some
   thing(s). ...  We are non commercial. why do you keep asking about this?"*
   Record each item's terms in SOURCES.txt and ship it.  **Do not raise this
   again** -- the `Q1' marks left in the B6 and B7 tables below mean "covered
   by this ruling", not "still waiting".  (One condition survives and is not
   about commerce: TOP's `info.c' says "please DON'T CHANGE ANYTHING ... You
   may not distribute any modified versions", so that file ships unmodified
   or not at all.  `utime.c', which has a bare copyright and NO grant, stays
   out of the build -- rdoggett: "if there is any question about it we have
   to exclude.  Don't delete, we may change our mind sometime later.")
2. **GPL source for binaries already shipped.**  The disk ships gcc, g++, VH
   and dvips binaries without their source trees.  Sources exist: MW 4073,
   4074 (gcc 1.42, g++ 1.39.1), funet
   `pub/unix/os9/gnu/gcc-1.37.1-osk-src.tar.Z`, pool `MISC/vh_1.4.lzh`, pool
   `DRIVERS/dvips_source.lzh` (641 KB, archive 3978).  NOT `nulman.lzh':
   the REFETCHED nulman.lzh is ncf.a + nulman.a, a null-device manager,
   correctly named.  The pool's `DRIVERS_nulman_lzh/' directory does
   hold dvips.c -- that is the filename shift this file warns about in
   these five categories, not a misnamed archive at the source.
   (Recommendation: add them.)
   **SETTLED IN PART 2026-09-14 (rdoggett's decision 1): the source was
   staged.**  SRC/gawk2.0 (28 files), SRC/bison (39) and SRC/dvips (65
   top-level .c/.h plus the archive's own OS9/ port files), all CR-only and
   recorded in SOURCES.txt with their terms.  What is still undecided is the
   REST -- GCC139, the other GCC2 passes and dvipsk 5.495b, for which no
   matching source exists here -- and that is FOR-RDOGGETT item 20.  Do not
   re-ask the general question; ask only about those.
3. **`jive` (1987, comp.sources.games v01i003).**  It builds and runs --
   `Sheeit, dis be a big-ass scribblin'` -- but it is a joke filter built on
   a racial caricature of Black speech, and a gallery card would showcase
   that.  Held, not shipped.  Everything needed is kept at
   `Scraped/acquisitions-2026-09-11/unix/jive-built-2026-09-11/` (flex output,
   `libl.c` for `yywrap`, the posting, the built module).
   **SETTLED 2026-09-13 (decision 3): jive stays OUT.**  No N-word in it,
   but `wet-back' and `greaser' are in its vocabulary, which is the test
   rdoggett set even though the word he named is absent.  `valspeak', the
   companion filter from the same distribution, ships and is clean.
4. **`xmas` signs off "from The ghost of Robert past"** -- the OS-9 port's own
   change to the line the source invites you to change.  Kept as the port
   shipped it, with nothing on the card saying whose it is.
   **SETTLED (decision 9, which rdoggett left to me): xmas stays as the
   port shipped it.**  It is a real animated program and the sign-off is
   the OS-9 porter's own, not ours to rewrite.

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

### B4 -- period Usenet utilities            done: tput, xd, xargs, cdecl
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
| agrep 2.01 | `CSU/volume26/agrep-2.01/`; also MW 4310 | 1992 | non-profit only -- **Q1** | ASSESSED 2026-09-15: the MW archive's osk_agrep is plain agrep 2.01 SOURCE, no OS-9 changes and no binary (24 files).  Built straight it fails on memory, not portability: BlockSize and Max_record are 49152, MaxNext 66000 (two 528K `unsigned' arrays in main.c, file-scope AND again as locals), mgrep.c's MAXPATFILE 260000 -- over a megabyte of static data against l68's 64K, and ~98K stack locals past a 16-bit displacement (`value out of range', 998 of them in asearch.c alone).  MEASURED the way out: this SDK's c68 takes `remote' data -- a file-scope `remote char big[300000]' and a function-local `static remote char buf[200000]' both compile, link and run right (scratch remotepool).  So: file-scope buffers `remote', big locals `static remote' (none of those functions recurse), and checkfile.c's S_ISREG/S_ISDIR/S_ISBLK/S_ISSOCK shimmed.  A build-level port.
| vttest | `CSU/volume7/vttest/` | 1986 | non-commercial -- **Q1** | DONE (3f5a1258) -- a local sgtty.c maps gtty/stty/FIONREAD onto _gs_opt/_ss_opt/_gs_rdy; tests unchanged.  Assessment kept: ASSESSED 2026-09-15: 2 parts, main.c + esc.c; drives the terminal with sgtty stty() RAW/CBREAK/CRMOD/ECHO flags, ioctl FIONREAD, setjmp/signal -- each has an OS-9 equivalent (_ss_opt fields, _gs_rdy) but it is a real port, not a shim.
Not found anywhere searched: `nl`, true `csplit`, a clean `dc`, apropos/whatis.

**B4 landed 2026-09-11: `tput`, `xd`, `xargs`, `cdecl`.**  All four were
built with `cc -qm`, verified running, and carry their source, their ORIG
tree and their own manual page.  `xd` needed NO source changes at all --
it compiled as posted.

Decided against, with the reason, so nobody re-fetches them:

- `calendar` (Minow) -- dropped as redundant.  `cal`, `calen` and
  `calender` are already here and cover it.
- `slice` -- deferred.  It wants BSD `re_comp`/`re_exec`, which this C
  library has not got; it needs a regex shim before it can be built.
- `mmv` -- deferred.  It wants signal and dirent headers this library
  does not supply, and its documentation states terms that may not
  permit redistribution -- read them before spending effort on it.

Two things measured while doing B4 that cost hours and should not be
re-derived:

1. **`system()` launches nothing in a program WE build**, in both a `-qm`
   and a CIOLINK build -- no child runs and a redirect in the command
   line never creates its file.  An archive binary that shells out (`eo`)
   works fine on the same image, so the split is ours-vs-theirs, NOT
   `-qm`-vs-`cio`, and the mechanism is still unknown.  The answer for a
   program that needs it is to fork directly:
   `os9exec(os9fork, av[0], av, environ, 0, 0, 3)`, which is what `xargs`
   now does.  `SRC/xargs/README.OSK` carries the measurement.
2. **bash's `cd` breaks a later pipeline whose producer is a BUILTIN.**
   After a real `cd`, `echo hello | cat` produces nothing -- and it does
   not return empty, it HANGS until the harness timeout.  A pipeline whose
   producer is a real PROGRAM is unaffected.  The cause is already in
   CLAUDE.md: bash's `pwd`/`getwd()` walks `..`, OS-9 has one root per
   device, and a non-interactive bash never reads the `.bashrc` that
   replaces `cd`.  There is no `echo` BINARY here, so `echo` in a
   pipeline is always the builtin.  In sheets and cases, either do not
   `cd`, or use `ksh -c "cd DIR; prog"`.

### B5 -- OS-9-native programs and code                          mimecode done
| prog | where | date | terms | note |
|---|---|---|---|---|
| Browse (P. da Silva, OSK port C. Emde) | TWN 653558 (3 parts, complete) | 1990 | none in the port | DONE a214cf0b -- ships.  NOT blocked: os9lib is disk/GNULIB/os9lib.l.  The thread carries two editions; the 30 Jan shar (browse_2a+2b merged) supersedes the 6 Jan one, which ORIG keeps.  One change: its pager was `more', which this disk has not got |
| unc (68000 module disassembler) | pool `SRC/unc.lzh`; MW 4308 | 1991 | none | DONE df6d23ce -- ships, links `GNULIB/os9lib.l` |
| almanac 3.2 (J. Semler) | MW 2313 (has almanac.OSK) | ~1992 | none | terminal card candidate |
| freeb | MW 3921; TWN 653668 | 1989 | PD | DONE e1a56b0c -- ships |
| howfrag | MW 4223 | | PD | DONE df6d23ce -- ships |
| uustat, ancient, hdump/undump | MW 3970, 3894, 3928 | | per item | hdump+undump DONE e1a56b0c; uustat DONE a214cf0b -- ships, built unchanged, Oldach's own grant; ancient DROPPED, no terms stated |
| dumpinit (init module lister) | MW 2240 | ~1994 | none | ATTEMPTED 2026-09-12, BLOCKED and left out.  Andrzej Kotanski, Cracow 1995; source is CR-clean and no terms are stated anywhere in it.  It will not compile against this SDK's <module.h>: of the 27 `mod_config' members it prints, 21 exist here and six do not -- _msysparam, _mip_id, _mcompat, _mcompat2, _mstacksz, _mcoldretrys, _mmemlist.  The SDK struct ends at _mevents plus _mreserved[14], where his MM/1-era header evidently named the compatibility bytes, the IRQ stack size, the coldstart retry count and the coloured-memory list.  Mapping those onto _mreserved would be inventing an init-module layout, which is measurement this collection does not have.  Source kept out of disk/SRC; the pool copy is at mw/dl/x/mm1_dumpinit |
| mimecode (base64) | MW 2503 | 1995 | author's permission | DONE -- built -qm, tested, carded; Tim Kientzle/DDJ, Gene Heskett's OS-9 pack |
| zc ZipCode + ZIPDATA | MW 2248, 2250 | 1995 | PD | needs `/dd/sys/zipcodes.txt` |
| os9dsk / rsdsk (read CoCo .DSK images) | MW 2244, 2246 | 1997 | freely distributed | DONE 07a11dee -- both ship, with a sample .DSK each |
| BIX one-page telecom (Dibble/Schmitt) | TWN 653653 | 1989 | distribution permitted | teaching example, asm |
| OS-9 International code disk (EFFO) | MW 5041 `effo.lzh` -> `EFFO/OS9_INTERNATIONAL/*.lzh` | 1993-94 | EFFO: personal, not commercial/military | disp SCF driver in C, lfcrman, watchdog, cache control; for real OS-9 |
| EFFO system examples | pool `EFFO/forum16.lzh` SOFTWARE/ASSEMBLER (4007); `forum12.lzh` SOFTWARE/C/ERROR (4003) | 1990-91 | "Public" | uacct, exception handler, F$CCtl/F$Permit bindings |
| kings, vt100 (MM/1 tree, terminal) | MW 2191, 2180 | 1991-95 | mostly unstated | |
| dvi2tty (+ Common TeX source) | MW 3861, 3860 | ~1991 | see ctexdoc.ar | DONE 4d158c64 -- dvi2tty and disdvi ship |
| BRU/OS-9 1.2 | MW 2330 | 1991 | GPL-style | 6809 C, plausible port |
| rnclone 1.0 | MW 3740 | 1993-94 | free, keep head comments | 6809 C, has 68k porting notes |
| K5JB k37 source (for shipped `net`, `bm`) | https://github.com/johnsonjh/k5jb | 1993-95 | no licence file | check it matches the binaries |

**UNPACK IN THE OS-9 UNIVERSE, not host-side.**  rdoggett, 2026-09-11:
*"If you are not doing all this work in the os-9 universe, you are doing it
wrong.  Stay in universe and you don't have to worry about LF/CR issues."*

The evidence was already here and went unread: `dvi2tty' came out of the
disk's own `ar' and compiled first time, while `bc' came out of a host-side
Python unsharer and failed four separate ways -- the first two purely LF
damage.  And the symptom does NOT say "line endings": an LF file reads to
OS-9's cpp as one enormous line, so it surfaces as `source line too long'
on every file at once, which reads like a source defect.

THE METHOD, proved on freeb and now the way to do this:

1. Transport the archive onto the disk AS OS-9 TEXT -- convert line endings
   once, in the copy.  This is the one host-side step, and it is what
   kermit or uucp did in period.  Skipping it fails in a way worth knowing:
   the disk's own `unshar' answers "No shell commands in <file>", because it
   cannot read an LF file either.
2. Unpack with the disk's own tool, into a host-directory device so the
   files land where the build driver wants them:

       OS9H5=<dir> os9exec ksh -c "cd /h5; /dd/CMDS/unshar /dd/tmp/x.txt"

   Every file it writes is CR-terminated by construction.  On freeb this
   produced four files byte-identical to the host-side extraction, with no
   conversion step to get wrong.
3. The disk carries `unshar', `tar', `ar', `gzip', `compress', `lha',
   `lharc', `unzip', `zip', `arc' and `zoo', which covers nearly every
   format in the pool.

**uustat AND Browse ARE NOT BLOCKED, and the measurement that said so was
wrong.**  This block used to read "no `disk/LIB/*.l` defines `info_str' or
`info_is_locked' -- every library was scanned for the symbols", and that scan
covered only `disk/LIB/`.  The library is in **`disk/GNULIB/os9lib.l`**.
Re-measured 2026-09-12 across BOTH directories: every `disk/LIB/*.l` has zero,
and `disk/GNULIB/os9lib.l` has `info_str' six times and `info_is_locked' once,
with `info_c' among its 45 ROF members.

It ships, and it is already on the build path: `tools/rebuild/make_overlay.sh`
copies it into the overlay as `/dd/LIB/os9lib.l', which is why twelve recipes
already link `/dd/LIB/os9lib.l' successfully (ls, zoo, fiz, ed, dbz, gtar,
unc, rayshade, wam.sbprolog and others).

So neither program is B6-dependent.  Build both against `/dd/LIB/os9lib.l'.
The confusion was a name collision this tree has twice over: `CMDS/os9lib' is
the RTF/68K Fortran trap module, a different thing entirely, and looking at it
makes the library look present when the library is elsewhere -- or absent when
it is not.

Provenance of the shipped library, measured the same day: 45 ROF members in
exactly TOP's `OBJS1' + `OBJS2' order (`signals_a' and `utls' included), byte
identical to the archive's prebuilt except for the per-member creation dates
-- ours 1990-05-06, the archive's 1989-07-24.  It is TOP Munich's os9lib,
covered by the Q1 ruling above.

**REPLACING A HEADER BEATS SCREENING IT, when what it describes is a
FORMAT.**  `os9dsk' carried a `coco_direct.h' that was 77% the SDK's
`direct.h' and said in its own first line that it was "modified from the OSK
version".  It was NOT added to `tools/screened-src.txt': that file says an
exception is added when "a person has read and accepted", and after `msfm'
-- 21 files of Microware file-manager internals that shipped for months --
adding Microware-derived headers to an exception list is rdoggett's
decision, not a session's.

Replacing it cost nothing.  What the program needs is the layout of the
MEDIA it reads: a CoCo directory entry gives the name 29 characters and the
descriptor address 3 bytes, where OS-9/68000 uses 28 and a long.  That is a
disk format, and a format can be described afresh.  The rebuilt module is
the same size TO THE BYTE and reads the sample disk identically.  Screening
remains right for the other case -- the two `stat.h' entries on that list --
where a program must match an INTERFACE to call the system at all.

**os9lib: WHERE IT ACTUALLY STANDS, 2026-09-11 night.**  It does not link
yet, and the next session should start from these measurements rather than
from the top.  Everything below was run, not inferred.

WHAT WORKS: the sources extract in universe (`tar' on the disk reads
`os9lib.t'), 42 members are named and 42 objects build, and the merged
container has the same header shape as the author's prebuilt.  Two
18-member half-libraries EACH LINK CLEANLY.

THE FAULT I FIXED: `l68: error - psect '<name>' contains assembly errors'
when linking against the whole library.  It is NOT a bad member -- removing
the named one just moves the error to the next (dbm_c -> popen_c ->
stat_c), because l68 names whichever junction it reaches first.  Proof: the
two halves link, and CONCATENATING the two halves (an OS-9 library is just
concatenated modules) produces a 36-member library with the fault GONE.
The difference from the author's build is the merge: the driver does ONE
pass, `merge -z=ctmp.list > lib'; the makefile does TWO, `merge -b50 OBJS1
>-lib' then `merge -b50 OBJS2 >+lib'.  (`-b50' is a buffer size, NOT
boundary padding -- the author's member spacings mod 50 are 5, 10, 36, 41,
36.)

WHAT IS STILL BROKEN, and the place to start: symbols do not resolve from
the joined library.  `info_str' and `info_is_locked' come back unresolved
although `info.c' is member 25 of it and the symbol text is in the file six
times.  Repeating `-l=' three times does not help (l68 makes one pass).  So
l68 reads the library and does not match the definitions.  That is ONE
question, not a mystery.

FOUR TRAPS, each of which cost a build or more:

1. **A `.l` recipe reports `clean' when `merge' RAN, not when the members
   compiled.**  A library whose first member failed still came back green,
   at 2,914 bytes against the author's 55,032.  For a library recipe, check
   the SIZE and the SYMBOLS, never the verdict.
2. **A `.l` recipe cannot carry a `.a` member.**  The driver names it
   `<source>.r', so `signal.a' became `signal.a.r' and merge could not find
   it.  os9lib is short `signal()'/`_siginit()' for this reason.
3. **CPP2 is required, and it MASKS real failures.**  Without it six members
   fail: `popen.c' and `pipe.c' want S_IREAD/S_IWRITE (no `<modes.h>'),
   `dbm.c' hits os9lib `stat.h''s own "Can not include both stat.h and
   modes.h" #error, `rnd.c' only warns.  Microware's cpp also will not
   resolve `#include "local.h"' from the source's own directory; GNU's
   does.  Three members failed on that until the headers the tar shipped
   (`regexp.h', `regmagic.h', `infomod.h') were staged -- `cp *.c' had left
   them behind.
4. **Count members on a CLEARED tree.**  `.r' objects accumulate across
   runs, so "objects present" counts history.  Every census taken before
   clearing was wrong.

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
Measured 2026-09-15 (TOP game binaries, bare, on a copy of disk/ with the five
runtime modules removed): tetrix, robots2 and sod need cio; yahtzee, bandit,
typefast, sokoban2 and wanderer2 do not.  yahtzee, typefast and wanderer2
reject SYS/termcap (`'vt100': Unknown terminal type').  DUPLICATES, not
new: sokoban2 is the second version of the disk's Usenet sokoban (same
author, same PC-derived screens), and wanderer2 is Steven Shipway's 2.2 of
the disk's wanderer, and yahtzee is Stacey Campbell's 1988 first version
(HCR) of the disk's yahtzee2 (Campbell 1989).  Terms: yahtzee HCR 1988
use/copy/modify/distribute;
bandit (Pete Granger) public domain 1989, no profit; typefast (druco!spear
1986) no notice; wanderer2 credits-file only.
DUPLICATE, measured 2026-09-15: tetrix is the disk's `tet' -- the same Quentin
Neill source with TOP's OSK arms (tet.c, AdvanceP/MoveL/MoveR/NewP/Rotate), and
tet is already a trap-free rebuild of it with an echo fix.  TOP's binary runs
(needs cio and termcap.entry) but adds nothing.  NEW but needing cio: robots2 (a different robots from the disk's -- hall
of fame robots_hof, ROBOTOPTS; no author, no document, binary only), sod
(a maze game, no author or document).
TOP NATIVE TOOLS, triaged 2026-09-15 (each asked `-?' with and without the
five modules; binaries in scratch toptools).  All binary-only, no terms
stated, and ALL BUT `hd' NEED cio.  Duplicates of what the disk has:
`more' (less), `hd' (dump, hdump, xd -- and hd reads `-?' as a file name),
`lfcr' (autolf), `errno' (perr), `times' (time -- its own usage says
`Syntax: time').  Multi-user system tools that want /dd/SYS/utmp, which
the disk does not carry, or a shared machine: `mesg', `newgrp', `uid',
`speak' and `msg' (chat between logged-in users), `oxm' (a mail front end
with a lock file), `mmenu' (a termcap login menu system), `mwb' (edits
manual entries).  And `where' finds a program along PATH (`-l' lists it)
-- which the disk's `which' already does, the way the shell finds it.  So
NOTHING among TOP's native tools is new here.

robots2 DOES NOT RUN, and the cause is in the program (2026-09-15, found by the
os9-dev skill session from its disassembly).  Its tgetent, when TERMCAP holds
the capability string, copies it into a 128-byte malloc until it meets a CR
(offset 0x98EA) -- an environment string ends in NUL, so the copy runs off
into memory; and its termcap-FILE branch never matches an entry.  os9exec's
dump showed F$ID only because `Last syscall' is the last call made, not where
it died; the module is sound (good CRC and parity).  Not shipped.

VCRON ASSESSED 2026-09-15 (scratch vcronpool): TOP's port of Paul Vixie's 1987
cron -- USR/SRC/vcron.t.Z (17 files; an old tar whose `VCRON/' entry both host
tar and Python's tarfile misread, so members were written by hand) plus
CMDS/vcron and CMDS/crontab, both needing cio.  Terms: "Distribute freely,
except: don't sell it" -- the Q1 ruling covers them.  Both binaries run:
crontab prints its usage and `crontab -l' answers "no crontab for su".  But it
is a multi-user system daemon: started from /h0/startup in the background,
only for members of group `Cron' in the SYS group file, crontabs per user in
/h0/SPOOL/VCRON (or a SysInfo CRONDIR), jobs run by setuid and os9fork, output
mailed through /h0/etc/cmds/smail.  TOP's two spool crontabs are TOP's own
site jobs.  Same class as the multi-user tools above; not shipped.

Measure first: which binaries need cio (run against an image without the
five runtime modules); every hardcoded `/h0/USR/GAMES/...` path; whether
the native tools expect `/dd/SYS/utmp`, group, password or smail.

### B7 -- games and screen toys                                         open
| prog | source | date | terms | port |
|---|---|---|---|---|
| phoon (Poskanzer) | `CSU/volume8/phoon.gz` | 1987 | permission granted | DONE (fc775046) -- numeric date, tws.c stands in for libtws |
| globe (Poskanzer) | `CSM/volume43/globe/part01.gz` | 1994 | permission granted | DONE (597b2a9e) -- built unchanged |
| atc | `NET2/games/atc` | 1990 | BSD (4-clause) + Ed James 1987 "copy permission ... provided that this notice is retained" | DONE (219b8188).  Assessment kept: ASSESSED 2026-09-15.  10 .c + grammar.y + lex.l, 7 airport files (Game_List, default, easy, crossover, Killer, game_2, ATC_scores).  Generate grammar.c/lex.c with the DISK's own yacc and flex (dogfood).  Port: sgtty/ioctl TIOCGETP/SETP -> curses cbreak+noecho; setitimer -> alarm (unix.l has alarm; setitimer nowhere); flock/lockf in log.c -> drop; getpwuid -> USER; random/srandom -> rand/srand; bcopy/bzero/index/rindex -> memcpy/memset/strchr/strrchr or os9lib; the `!' shell escape in input.c -> drop.  _PATH_GAMES /usr/share/games/atc/ -> /h0/GAMES/ATC/ beside the other games. |
| canfield (+cfscores) | `NET2/games/canfield` | 1980 | BSD | canfield DONE (8c133d0b) -- curses; _tty/SIGTSTP/SIGTERM shimmed; cfscores DONE (004ae08c) |
| trek (Allman) | `NET2/games/trek` | 1980 | BSD | DONE (219b8188) -- with atc |
| monop, wump, fish, arithmetic | `NET2/games/...` | 1980-90 | BSD | wump DONE (70fe4c6d), fish DONE (73cb6958), monop DONE (830dee5e), arithmetic DONE 2026-09-15 (check_signal() so ^C prints the score) -- self-contained, getopt bundled, instructions embedded.  monop's board, properties and cards are .dat files #INCLUDED as C initialisers, so they had to be CR like source, not like data |
| bs (ESR battleships) | `CSG/volume8/bs/part01.gz` | 1989 | no notice | DONE (cee1197c) -- OSK curses arm shims beep/chtype/ungetch, cbreak parenthesised |
| scrabble | `CSG/volume6/scrabble/` | 1989 | redistribute in any manner | DONE (9d6aa1e4) -- ported to Microware C |
| saa (Streets and Alleys) | `CSG/volume12/saa/` | 1991 | permission granted | DONE (d72a0cea) -- built unchanged with -DNON_ANSI_C |
| accordian | `CSG/volume15/accordian/` | 1992 | public domain | DONE (6a512987) -- curses solitaire; RANDOM->rand, popen/getpwuid dropped, win log local |
| mastrm | `CSG/volume2/mastrm.gz` | 1987 | public domain | DONE (0a75970f) -- system(clear) -> ANSI clrscr |
| hexa (hexagonal sokoban) | `ALT/volume93/Jan/930127.01.gz` | 1993 | no notice | DONE (c6aae0a7) -- 216-byte binary level maps in GAMES/HEXA |
| corewars | `CSG/volume6/corewars/` | 1989 | public domain | DONE (8a5316bf) -- cwasm, cwdis, corewar |
| castle | `CSG/volume8/castle/` (acquisitions-2026-09-11/unix/posts/comp.sources.games-v8-castle) | 1990 | public domain | DONE 2026-09-15 -- v08i093-097 + Patch1 v09i031 (never applied before; it fixes the string[] overrun that locked the game). Links once castle.h/items.h/windows.h/monst.h globals are extern-ised (CASTLE_EXTERN/MONST_EXTERN) and the 8K monster pictures compiled only into monster.c. Two OS-9 defects found by play: ^C hung the game and ^E (save) killed it unsaved -- SCF turns them into signals, the signal aborts curses' read and stdio's error latches; and ESC (SCF's end-of-file char) read as -1, so the inventory could not be closed; tty.c clears kbich/kbach/eofch for the game's life (sc.c's idiom) and restores them, measured. The help pager counted LF on CR data and stopped at page one; LF is '\n'. Trap-free. |
| othello3 / reversi | `CSG/volume12/othello3/`; `CSG/volume15/reversi/` | 1991-92 | free / GPL | othello3 DONE (77b95c01) as othello -- getchar->getch, LINES/COLS clash removed; reversi DONE (d738a8a2) |
| jotto, conn4 (Sicherman) | `CSG/volume11/jotto/`, `CSG/volume12/conn4/` | 1990-91 | no notice | conn4 DONE (39eb5990) as c4; jotto DONE (0a75970f) -- built-in word list |
| yahtzee2 | `CSG/volume8/yahtzee2/` | 1989 | no notice | DONE (49dfcfcb) |
| rot2.2 ("software rot") | `CSG/volume1/rot22.gz` | 1987 | no notice | DONE (eaa11e7b) as rot22 |
| flicker | `CSG/volume5/flicker.gz` | 1988 | no notice | LEFT OUT 2026-09-12, deliberately.  Gene H. Olson's ANSI teaser: `for(;;) write(1, buf, N*s)' of insert-line/delete-line escapes, forever.  No exit but Interrupt, no terminal restore, and the author's own README says "Enjoy, and be sensible.  (Use Interrupt to exit the program.)"  It would hang the capture harness and hand a reader a terminal to break out of.  Two files, extracted and read; nothing to build. |
| ASCII plasma | `ALT/volume93/Feb/930203.12.gz` | 1993 | no notice | LEFT OUT 2026-09-15, for flicker's reason.  Noah Vawter's 1993 `Shifty Death Effect' (unixsrc/altsrc/cand/volume93_Feb_930203.12.gz.txt, 139 lines): `while (1) { plasma(); display(); }' of VT100 cursor moves, no exit but Interrupt; its own usage text calls it a joke.  Read; nothing to build. |
| Toon 1.0, Juggle 1.0 | `ALT/volume94/May/940508.36-.40`; `ALT/volume95/Apr/950426.08.gz` | 1994-95 | GPL | Toon INCOMPLETE (checked 2026-09-15): only part 4 of 5 (940508.39) has a body in altsrc/cand; parts 1-3 and 5 are headers only, so it cannot be built from here.  Juggle 1.0 (950426.08, Glenn Hutchings 1995, GPL): complete shar in cand -- being ported 2026-09-15 |
| rogue 5.3 clone (Stoehr) | `CSG/volume1/rogue/` | 1987 | not for profit -- **Q1** | DONE (520034e2) -- OSK arm in machdep.c; SRC/rogue/README.OSK.  Assessment kept: ASSESSED 2026-09-15 (scratch roguepool): 29 files, ~9,900 lines; v01i011-015 plus Patch1 (v01i032), Patch2 (v01i052) and Patch3 (v12i097, VMS, 1991).  Patches01 and 03 apply clean in order; Patches02's two machdep.c hunks reject against ORIG, and Patch3 ships a whole new machdep.c.  ALL system dependence is in machdep.c's 18 md_ functions, in UNIX / UNIX_BSD4_2 / UNIX_SYSV / VMS arms -- the author's own design, so an OSK arm is the port.  Makefile builds -DUNIX -DUNIX_BSD4_2; -DCURSES uses its own curses.c (TERM/TERMCAP through md_getenv) instead of the system's.  Surface: FIONREAD (md_slurp), TIOCGETC/TIOCGLTC and sgtty cbreak (md_control_keybord, md_cbreak_no_echo_nonl), signals incl. SIGTSTP, stat inode and link count for its save-file check, getlogin.  A real port, not a shim. |
| gnugo, napoleon, adven2 | `CSG/volume6/gnugo/`, `CSG/volume17/napoleon/`, `CSG/volume11/adven2/` | 1989-93 | GPL/GPL/none | ASSESSED 2026-09-12.  **gnugo**: DONE (2b52b2ed).  Assessment kept: v06i019, GPL with COPYING, 34 members / 4,207 lines / 27 C files, no curses -- and TOP shipped BOTH an OS-9 source tree and a working OSK binary, so a reference build exists to check against.  The best next candidate.  **napoleon**: ASSESSED 2026-09-12, viable but not small.  Pete Chown 1992, GPL v1 or later, its own `copyright' file.  19 members, 4,391 lines.  The yacc question is settled -- the disk's `yacc' and `bison 1.19' both run, and no pre-generated parser ships, so lang.y must go through one of them.  Its Makefile offers `-DPURE_ANSI' for non-Unix hosts and adv.h:31 `#error's unless exactly one of PURE_ANSI and UNIX is defined; PURE_ANSI is right for us, because <termios.h> and <unistd.h> are inside the UNIX arm and neither exists here.  But the switch does NOT solve the real obstacle: 71 ANSI prototypes, unconditional, with no PROTO() indirection -- adv.h:76 onward is bare `extern void format(char *,...);' -- and Microware's cc is K&R.  Unlike scrabble there is no single file to shim; it is a tree-wide de-ANSIfication, and ansi2knr cannot do declarations.  A day's work, not an evening's.  **adven2**: FORTRAN (aamain.f, asetup.f, asubs.f, iors.f, split .xaa/.xab parts joined by combine.sh), no terms stated.  Out of scope for the C toolchain: it would need the RTF Fortran chain, which CLAUDE.md records as only partly working (`for' and `lnk' print the command they would run and stop).  Left alone |
| text toys: spew, silly.tar (kraut, b1ff, chef, fudd) | `CSG/volume1/spew.gz`; `ALT/volume92/Dec/921220.11` | 1987-92 | spew free; silly mixed | spew DONE (0a75970f); chef DONE (5b4dbd3e), fudd+drawl DONE (2cd9981e) -- lex filters generated in-universe; kraut/newspeak(big)/plain-C ones open; chef/fudd/drawl/lame DONE; mb + kraut SKIPPED (mb parodies a real person; kraut injects a Nazi salute -- both rdoggett calls) |
Leave: cdungeon ("COMMERCIAL USAGE STRICTLY PROHIBITED", Infocom); hearts,
dots2, diph (sockets/fork/select); X11-only; umoria/omega/nethack from Usenet
(TOP has OSK builds -- B6).

### B8 -- bc                                    done 2026-09-11: GNU bc 1.01
GNU bc 1.01 `CSR/volume01/GNU_bc/` (Nov 1991, GPL, K&R-safe, yacc/lex --
bison and flex ship) or C-BC (Hopkins) `ALT/volume93/Oct/931006.03-.07.gz`
(1993, public domain).  Nothing on the disk does arbitrary precision.

**B8 landed 2026-09-11 (ba55dde7): GNU bc 1.01**, comp.sources.reviewed
volume 1, Philip A. Nelson, GPL v2.  Nothing on the disk did arbitrary
precision before it, and there is still no `dc'.

Three things it taught, none of them specific to bc:

1. **A ported program that PARSES TEXT AT RUN TIME must be tested with CR
   input**, not just with the archive's own test files.  bc's flex scanner
   took only LF, so on this disk a bc script written with the disk's own
   tools was refused as an "illegal character", and so was anything piped
   in -- while its author's LF test files passed perfectly from the first
   build.  Its own `libmath.b' ships CR-terminated and uses backslash
   continuations, so `bc -l' failed too.  Two lexer rules needed widening.
   Keep an LF file as a control so a CR fix cannot silently trade one
   terminator for the other.
2. **A blank CARD with low ink, where the datatests pass, means the
   interactive shell.**  A card runs under bash; a datatest does not.  So
   the `cd' then pipe-from-a-builtin hang shows up ONLY on cards.  bc's
   first card was empty with "left it unusable" and the program was fine.
3. **Look for `.dist' files before reaching for yacc or lex.**  The posting
   ships the generated parser, scanner and token header, so the build is
   plain cc.

Still open in B8's neighbourhood: `dc' is not on the disk and was not found
in the pool.

### B9 -- news and pseudo-terminals                                     open (Q1)
MNews (Dessauer) MW 3840/3841; tass pool `TELECOM/tass.lzh` (needs MNews'
8bit.l); rn 4.3 pool `TELECOM/file4352`; nn 6.3.10 MW 3843.  PtyMan 1.3 /
PtyDrv (Mellin) TWN 653174 + 653173 (source), 653172 (binaries); MW 3990,
3989; 1995 fixes in pool `DRIVERS/rtclock1287.lzh` -- a file manager for
real OS-9 (os9exec will not load one).
MNews measured 2026-09-15: the pool's `APPS_mnews_t_Z/.t' is the WHOLE package as
SOURCE, no binaries -- INEWS (~50 .c), RNEWS, SENDBATCH, MISC, LIB (Sys,
Distributions), MAN (.prf), and NN_OSK, the OS-9 port of nn (~70 files, nn.1).
`mnews_src.t.Z' is a 42-member subset (MISC + INEWS) -- use the full one.  Its
Copyright (Ulrich Dessauer): copy and modify, not for profit (covered by Q1),
AND "(e) redistribute only parts of the package" is not allowed -- so if any
of it ships, the whole package ships in SRC, as the tar has it.
nn 6.3 inside it (NN_OSK/README lines 73-103): "Copyright (c) 1989 by Kim
Fabricius Storm" -- use, modify, reuse and "redistribute it freely", on three
conditions: no responsibility, origin not misrepresented, altered versions
plainly marked.  regexp.c is Henry Spencer's (U. of Toronto 1986, its own
notice); unshar.c carries no notice (K. Greer, S. Shafer, M. Mauldin).

### B10 -- GPL source for shipped binaries                              open (Q2)
See open question 2.
Version matrix measured 2026-09-15 (INDEX's own `gcc -v' readings plus
version strings in the binaries) -- source must match the BINARY, not the
name:
  CMDS/GCC139: gcc 1.39 (cc1, cccp carry "1.39"); gpp 1.37.1 (cc1plus
    carries "1.37").  No 1.39 source in the pool; funet has
    gcc-1.37.1-osk-src.tar.Z, which may cover the g++ 1.37.1 pass only.
  CMDS/GCC2: gcc driver 1.42 -- MATCHES pool mw/dl/osk_gcc_1.42_src.lzh
    (version.c "1.42"); gpp/cc1plus 1.40.3 -- pool osk_gpp_1.39.1.lzh is
    "1.39.1 (based on GCC 1.40)", NOT a match; gcc2 2.5.6 and cc2plus 2.5.8
    -- no source found.
  CMDS/jargon: byte-identical to CMDS/jargon inside pool MISC/vh_1.4.lzh
    (md5 47914da1...) -- VH 1.4 source is an exact match.  ADDED 312d40c0
    as SRC/vh.
  dvips: CMDS/TEXCMDS/dvips is "dvipsk 5.495b" (Radical Eye Software).  The
    pool's DRIVERS/dvips_source.lzh is NOT source: it holds the dvips,
    afm2tfm and MakeTeXPK binaries, .pro PostScript headers, TFM fonts and
    install.text -- no .c at all.  No dvips source found.
  Not fetched, and listed in the MW archive index: 4066
    gcc-1.37.1-osk-src.tar.Z (Blake; also on funet), 4072 gccsrc272.zip (gcc
    2.7.2), 4071 gcc-sun4-os9-2.6.2 (a Sun cross compiler).  No 2.5.6 or 2.5.8
    source is in either index.  osk_gcc_1.42_src.lzh has no COPYING file.

### B11 -- 6809 C that plausibly ports                                  open
jumble, unTC (PD), Solve (PD), Spencer regexp, uptime, verdisk, sgrep, sortc,
SmallTeX, bawk, disa 1.00 (TWN 653675): MW 2464, 2677, 2864, 3697, 3712,
3713, 2575, 2588, 2594, 2585, 2324, 2751.  Also 1990 IOCCC entries (pool
forum16), editline (CSM v31, OS-9 support), pscat (`#ifdef OSK`).

ASSESSED 2026-09-15 (none is on the disk; unpacked copies in
acquisitions-2026-09-11/os9/mw/dl/x/c09_*):
- bawk (Boisy's awk-alike, 6 C files): the disk has GNU `gawk' and `a2p'.
- sortc (D. R. Grafton, multi-key character sort): the disk has GNU `sort'.
- Solve (Jim McDowell): an integer-equation routine for other programs,
  with a test driver -- nothing to run on its own.
- SmallTeX (Mike Meyer 1982, OS-9 changes by Paul Burega; free to
  distribute with source and notices): writes input for Burega's Fancy
  Font `pfont' printer back end, which is not in the archive, so its
  output has nothing here to print it.
- unTC (Tim Koonce 1989, public domain): extracts John Lauro's TC
  archives from Color Computer RSDOS.  NOT SHIPPED 2026-09-15: no TC
  archive exists anywhere in the pool to run it on (the only .tc files are
  Turbo C makefiles), and a card of its usage line alone is a defect.
- jumble (Nick Flor 1987, free to distribute, not for money): DONE (e51b6871),
  built unchanged.
- sgrep (DECUS grep with substitution, not for profit): DONE (f4a2b6f3), built
  unchanged; its manual is DOC/sgrep.doc.

THE REST OF THE c09_ TREE, assessed 2026-09-15 (almanac, reversi and spew
are already on the disk; SmallTeX, Solve, bawk and sortc are above;
Solitaire and StG are under Leave alone):
- kalah (Michael J. Knudsen 1983-84, Kalah and "Pigeon Plague" against the
  computer; a bare copyright, no grant): DONE (726c8243).  Plain stdio; its
  6809 move.a hand-optimises count() and makel(), whose C is movesrc.c,
  marked "for reference only" -- a 68k build needs it.  printf printed
  nothing to its unbuffered stdout, and show.c called count() undeclared.
- kutil (Bruce Isted, free with notice): NOT SHIPPED, it reads and writes
  the kernel track of CoCo floppies and Burke & Burke hard drives.
- peruse 2.0 (Stephen Castello 1991): NOT SHIPPED, it needs Isted's VRN
  driver (CoCo) and is for personal use only.
- nist (John M Semler): NOT SHIPPED, it sets the clock by dialling NIST
  through a modem; an OSK binary came with it.
- lpunch: NOT SHIPPED, it converts punched-card deck records, with nothing
  here to use them.

B11 LEFTOVERS, checked 2026-09-15: editline (Turner and Salz 1992, KA9Q pool,
already with an OS-9 port in sysos9.c) is a LIBRARY for other programs -- its
only program, testit, is "a small slow shell for testing"; not shipped.
uptime and verdisk are OS-9 `ar' archives from the 6809 section (c09_) --
CoCo-world, so last.  No pscat anywhere in the acquisitions.  EFFO forum disk
16 is already mined (hexed, oskversion, puzzle15, rpn, top, clear, fastcc,
demerge, lunisolar, tree) EXCEPT SOFTWARE/C/7TH_C_CONTEST -- the eleven 1990
IOCCC winners with their hint files -- and four assembler tools.  The four,
read 2026-09-15 from their info files, are not user commands: FCCTL and
FPERMIT are C interfaces to F$CCtl and F$Permit/F$Protect/F$GSPUMp for other
programs to link, EXCEPT_HANDLER is a handler that dumps exception information
into a data module, and EXIT_HANDLER adds two new calls to the kernel for exit
routines.  Not shipped.  The 1990 IOCCC entries are next; the contest's rules
required every entry to be public domain.

### The 1990 IOCCC entries (EFFO forum disk 16, 7TH_C_CONTEST)   2026-09-15

Eleven C entries; all public domain under the contest's rule 5.  Four were
already here (queens/baruch.c, bjack/cmills.c, jaw, trigraph/scjones.c).
Of the remaining seven:

  dds       DONE (574622f1) -- a BASIC interpreter in 1536 characters, the contest's
            Best Language Tool.  One line changed: its arrays are `remote'.
  theorem   DONE (574622f1) -- Best of Show, a Runge-Kutta solver that is also a
            reversing filter.  Its duplicate declarations are extern here.
  westley   DONE (574622f1) -- and the reasoning that first rejected it was wrong
            twice over.  I recorded it as unshippable because the fix
            looked like reformatting the artwork; in fact THE CONTEST'S OWN
            common.mk builds this entry through exactly the three
            substitutions used here (`s/signed//', `s/1s/1/g',
            `s/^<tab>#/#/'), so they are sanctioned, not invented.  And the
            undeclared identifier that stopped it was MINE: westley has no
            #include <stdio.h>, so the putchar-through-fputc change I had
            added left stdout undeclared.  With stdio included it builds
            clean.  Five changes in all, each in README.OSK.
  dg        NOT SHIPPED, and the mechanism is worth keeping.  Line 3 is
            `#define d define' and every directive after it is written
            `#d name(x) ...' -- the entry relies on the preprocessor
            EXPANDING THE DIRECTIVE NAME, which standard C does not do, so
            neither cpp here recognises any of its 60 definitions.  Writing
            them out as #define gets further and still fails: cc then runs
            and exits having written nothing at all, no diagnostic and no
            module, which is the silent cpp death of
            notes/CPP-MACRO-CRASH.md.  The author expects it -- his hint
            says that compressing the source further earns "defines nested
            too deeply".  Sixty macros nested that way is past what this
            preprocessor will expand.  Its other documented workarounds
            (the explicit 'A' form, strchr for index) were tried and are
            not the obstacle.
  pjr       NOT SHIPPED.  Same shape: cpp aborts (E_PRCABT) while reading
            it.  Its hint warns that compilers run out of temporary value
            space on the `X=g().s().v()...' chain that IS the program.
  tbr       NOT SHIPPED.  "Best Utility" -- a working shell in 550
            characters, built on fork(), pipe(), execvp() and wait(), none
            of which exist in this C library.
  stig      NOT SHIPPED.  "Strangest Abuse of the Rules": the C file is
            three bytes and the entry is a csh aliasing trick.  The judges
            noted this type would not be permitted again.

### The usenet last-ditch pull, and what was in it  2026-09-18

rdoggett, 2026-09-18: *"We need to make a last ditch attempt at getting
whatever we may want from usenet, then I will end it."*  Done.  **Nine more
groups are pulled whole and every count matches the site's own index**, so
the subscription can be cancelled:

    fj.sys.x68000        4,482     comp.sources.unix     2,817
    comp.sources.games   1,987     comp.sources.misc     6,165
    comp.sources.reviewed  276     mod.sources             798
    net.sources          6,437     fj.sources            2,132
    alt.sources         15,923

fj.sys.x68000 is his: Sharp's X68000 ran an OS-9/68000 port, and the group
carries OS-9 threads from its first month (December 1987) to a 1997 request
for OS-9/X68000 V2.4.  The rest are the "no mirror found" rows of the
recovery table below -- comp.sources.misc v48+, comp.sources.games v19+ and
the alt.sources gaps -- which turned out to be small enough here to take
whole.  ~41,000 messages, 1.2 GB, in
`~/Developer/os9/Scraped/usenet-rewind`.

**What mentions OS-9, OSK or Microware**, measured across the nine:
fj.sys.x68000 189, comp.sources.misc 97, alt.sources 68, fj.sources 26,
net.sources 16, comp.sources.unix 7, mod.sources 7, comp.sources.reviewed 2,
comp.sources.games 1.

**The one find that changes a decision: GCC 1.37 ported to OS-9/68000.**
comp.sources.misc v13i005 to v13i011, May 1990 -- Mr. Seyama's port, posted
for him by NIIMI Makoto of Keio University, as **diffs against stock GCC
1.37** plus documentation in English.  Saved to
`Scraped/usenet-rewind/extracted/gcc137-osk/`.  **Part 2 of 7 (v13i006, the
first of five diff files) is NOT in this archive's copy of the group**; the
other six parts and a repost of part 6 are.

That bears on FOR-RDOGGETT 20, the GPL binaries shipping with no source:
CMDS/GCC139 holds gcc 1.39 and a g++ pass 1.37.1.  This is not that version
and it is incomplete, so it does not close the question -- but it is the
first OS-9 GCC SOURCE this project has found anywhere, and it is a better
lead than the two Microware-archive near-matches.  alt.sources also carries
an "OS-9 GNU C compiler" thread from February 1991 that has not been read.

Nothing else in the nine groups looks like OS-9 software we do not have; the
mentions are mostly ports being discussed rather than posted.

### utree 3.03b-um -- rdoggett's own find, and a candidate  2026-09-18

He sent a usenet-rewind link to message `1992Sep7.214827.26662@PA.dec.com'.
It is **comp.sources.unix v26i065, part 2 of 8 of `utree'** -- Peter
Klingebiel's "screen oriented filesystem utility", a portable Unix version of
the DOS `xtree'.  Paul Vixie's moderator note calls it "dired-like
functionality without the overhead of GNU Emacs".

All eight parts are pulled and unpacked:
`~/Developer/os9/Scraped/usenet-rewind/extracted/utree/part0*.shar` (626 KB).

**Terms permit shipping it**, and they are the non-commercial shape settled
on 2026-09-11 (accept, record, ship).  From `doc/utree.prlist.1`:

> (co) 1991/92 Peter Klingebiel & UNIX Magazin Munich.  Permission is granted
> to copy and distribute utree in modified or unmodified form, for
> noncommercial use, provided (a) this copyright notice is preserved, (b) no
> attempt is made to restrict redistribution of this file, and (c) this file
> is not distributed as part of any collection whose redistribution is
> restricted by a compilation copyright.

Condition (c) is satisfied: nothing restricts the redistribution of this
collection.

**Why it is a candidate and not just portable.**  The disk has `tree', which
prints a directory tree and stops; `browse' and `wndex', which are for text;
and no full-screen file manager at all.  A reader could navigate, copy, move
and delete across a whole filesystem from one screen, which is a thing they
cannot do here today.  That is the bar the CoCo survey set, and this clears it.

**What the port will have to deal with**, read from the shar:
  * it ships 17 `sys/Makefile.*` and five `conf.h.*` -- BSD, V.2, V.3, SCO,
    AIX, SUN, MIPS, ULT and more -- so the porting seam already exists and an
    OSK arm joins it rather than cutting a new one;
  * `tst/fionread.c` and `tst/sigwinch.c` say it wants FIONREAD and SIGWINCH.
    OS-9 has neither; the keyboard read will need SS_Ready, and there is no
    window-size signal, so the screen size comes from the termcap;
  * curses, and a per-terminal key-binding file (`lib/utree.binding`), which
    is the right shape for this disk's termcap.entry arrangement;
  * `sup/getopt.c` is carried, so the getopt bundle trap does not apply.

Not started.  Queued behind the CoCo images.

### The CoCo Community Archive zips -- the last unopened body  2026-09-15

Nine zips in Scraped/acquisitions-2026-09-11/os9/community/cca, and they are
NOT source archives: they hold 26 CoCo .DSK disk images (RSDOS and OS-9
Level 2, 6809).  The programs on them are 6809 binaries and cannot run here.
What could ship is SOURCE found inside them, so the first question for each
image is whether it holds any .c at all.

READ THEM WITH THE DISK'S OWN TOOLS, not with `strings'.  os9dsk and rsdsk
are on this disk for exactly this (DONE 07a11dee): `os9dsk -dir <file>.DSK'
lists an OS-9 disk, `-get' copies a file out, and rsdsk does the same for
the RS-DOS side.  A strings pass over OS9PUB.DSK looked like it found
makefiles and readmes; those were words inside documents, not directory
entries.  The survey wants a -dir over all 26 and then -get on anything
whose name ends .c.

  Bob Van der Poel Public Domain Programs   1 image
  Filters (D.P. Johnston)                   2
  OS-9 L2 Unix Utilities (Mike Sweet)       1
  OS-9 Level 2 Library                     15  (games, filters, comms, maths,
                                                DBM, word processing...)
  OS-9 Public Domain Utilities              1
  Rdump/RayTrace/DispRaw (Walter Zambotti)  2 + a readme
  Sled v2.2 (Mark Griffith)                 2  (one is SLEDSRC.DSK)
  Tree (Tim Kientzle)                       1 + tree.c and tree.txt loose
  Wildcard Commands (Keith Alphonso)        1

**Surveyed so far, 2026-09-15.  Nothing has shipped, and that is the right
answer.**  `ffix' (Bob van der Poel, March 1988), FFIX/ffix.c on the "OS-9
Public Domain Utilities" image, was ported and then WITHDRAWN.  It expands
tabs, which `detab' and `expand' already do, and turns every other control
character into a space, which `pep' -- "a file detergent" -- and `unp'
already do.  The feature its own readme is written around, rewriting named
files in place, needs a `shell' module this disk has not got, so what was
left was the duplicated half.  Terms are a copyright line with no grant.
Do not port it again.

The rest read so far is 6809 and stays where it is: the Bob Van der Poel
and Public Domain Utilities images duplicate each other outside that one
file and are otherwise 6809 assembler and BASIC09; "OS-9 L2 Unix Utilities"
(Mike Sweet) holds chmod, chown, ls, setenv and signal, which duplicate
programs already here and state no terms; Sled is CoCo3 hardware-bound.

About twenty Level 2 Library images are still undescended, and the test for
them is NOT "does it compile".  It is: what can a reader do afterwards that
they could not do before, and is the program mainly Color Computer
business?  rdoggett, 2026-09-15: *"don't just port everything from coco
that you can, make sure it's a useful addition to us and not overly color
computer related."*

Tree is the one already checked, and it is NOT a candidate: `tree' is
already on this disk from EFFO forum disk 13, doing the same job, and
Kientzle's 1992 version sits on Carl R. Kreider's 1984 original which was
"released to the public domain for non-commercial use" -- a narrower grant
than it first reads, and Kientzle's own additions carry no grant at all.

### Leave alone
Microware-owned: 6809 system source, PIPELINES, Training, qpascal, ucc
support, csl/fpu inside STerm68k.lzh, bfed.  Restrictive: StG V3 BBS,
grammar.ar, OAI, CEnv, Dominion, QuickSpell, mplay/hrecplay (shareware),
Solitaire (begware), K9 FidoNet parts, reboot.lzh.  Hardware-bound: MM/1
viewers/screensavers/sound, IronCurtain, gr_classic, CD-i, X68000 PWIN,
G-Windows fonts.  Networking that needs Microware ISP (rdate, ttcp, bind,
boa, wn 1.16.7) is for real systems only -- later, if at all.

---

## A defect found by the skill session, 2026-09-12

`ls' printed a literal `%s' where a filename belongs:

    $ ls nosuchfile
    ls: %s: error 216

`SRC/ls/error.h' declares `void error(int, int, const char *, ...)' and
`SRC/ls/error.c' defined it with three fixed parameters, so the argument
after the format was dropped and the format reached stderr unsubstituted.
Thirteen call sites, every one passing exactly one argument after the
format.  Fixed by taking that argument; vfprintf would be the general
answer but os9lib, the only library the recipe links, has none.

Found by the os9-dev skill session running our own disk as a dogfood test,
which is the second thing that pass has caught that we could not see from
inside.  The first was that our `system()' return value is not a reliable
failure signal -- junk here, 0 on their machine -- and that the sound test
is whether a redirect target was created, since a shell makes the file
named after `>' before it runs the command.

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
| EFFO PD disks 100-123 (1993-95) | EFFO material after what the pool has | not found |
| ~~forum disks 18 and 19~~ | CLOSED 2026-09-12: they do not exist.  `notes/DOWNLOADS-68k.md' records the archive's ids running contiguously `forum17=4008', `forum20=4009' -- EFFO published them, this archive never had them.  Stop looking. | n/a |
| OS-9 Users Group disk library | user-group software | not found |
| CompuServe OS9 SIG library | names survive at lcurtisboyle.com: cawf, defrag, dskcat, hpdisp, spel68, aplrts, swtool, g261 | files not found |
| colorcomputerarchive.com (~150 OS-9 zips), archive.org `cdrom-coco-archive` | 6809 OS-9, some C | few opened |
| Microware archive, the rest | `os9/mw/*.tsv`: 127 OSK files the pool never fetched, the MM/1 tree (84), USERGROUPS, BENCHMARKS, FAQ, DOCS (incl. a 1994 chestnut.index) | listed, not all fetched |

### Microware archive refetch, 2026-09-12

The five categories `notes/DOWNLOADS-68k.md' fetched in August and the pool
did not keep -- they went to a `scratchpad/web/dl/' the note itself calls
temporary -- are back: **153 files, 34 MB, zero failures**, in
`os9/mw/refetch/{DRIVERS,EFFO,GWINDOWS,NETWORK,TELECOM}'.  Fetched from
`osk.tsv' rather than by scraping the category listings: the tsv is
`category<TAB>id<TAB>filename' and its rows match the live pages id for id,
so the pairing comes out of a manifest instead of a regex, and the listing
requests disappear.  `scratchpad/fetch_from_tsv.py' does it.

`61-gwindows' is deliberately NOT in that set.  Ids 56-62 are the
OS-9000/x86 family (`56-msdos', `57-os-9-ce') where 99+ are OSK, and its
three files are `blackjack_x86.uue', `puzzle_386.lzh' and a cyberwar --
wrong architecture.  `refetch_archive.py' mapping GWINDOWS to 122 alone is
right, not an oversight.

**EFFO: no new programs, but licence data for four we ship.**  All 31 disks
(forum1-17, 20-23; pd0-9) came down.  Of the 72 `CMDS/' programs across them,
**70 are already on this disk** -- EFFO has been absorbed thoroughly.  The
only two that are not are `init.lsp', which is XLisp data, and `loglist', a
5,654-byte 1988 binary on pd1 with no source, no documentation and no info
block anywhere: no grant, so it stays out on the `utime.c' rule.

What the harvest DOES carry is 35 `info_<program>' blocks against the 20 on
the disk, and four of the new ones are for programs we already ship, in the
authors' own words:

    beav      $AVAILABILITY public,    no conditions  (Peter Reiley; OSK
              extensions Stephan Paschedag, FORUM17)
    lharc     $AVAILABILITY freeware,  no conditions  (Yooichi Tagawa)
    compress  $AVAILABILITY public domain             (COVE, EFFO)
    m4        $AVAILABILITY public, $CONDITIONS "see file COPYING !"
              -- FSF, so the GPL travels with it

`demerge's block is an unfilled template, every field empty.

Also confirmed from a second source: **forum 18 and 19 do not exist.**  The
EFFO directory runs forum17 then forum20, exactly as DOWNLOADS-68k.md said.

### The other four categories, triaged 2026-09-12 -- nothing shippable

Method that worked, after two that did not: build the inventory from the
ARCHIVE LISTINGS (`lha l`), match an anchored `CMDS/<name>` path, and diff
against `disk/CMDS`.  Do NOT triage on filenames -- the plan warns above that
these five categories' names do not match their contents -- and do not parse
the prose indexes.  One trap: EFFO's disks list as `[generic]` while these
carry real OS-9 permission strings (`------wr`, `d-ewrewr`), so a filter
keyed to a leading bracket silently returns nothing for all of them.

    DRIVERS    4 CMDS/ programs, all here (the 4th is maketexpk.c, a source file)
    GWINDOWS   0 CMDS/ programs; the 7 are G-Windows packages already shipping
    NETWORK  169 CMDS/ programs, ALL 169 already here -- it is netpbm
    TELECOM   39 CMDS/ programs, 30 here, 9 candidates

The nine, and why none of them ships:

    rz, sz          COMMERCIAL.  `mailer.rz' is an Omen Technology licence
                    FORM -- $20 per user, quantity discounts, "Payment of
                    This License authorizes the installation and use".  Not
                    shareware.  Out, and they were the two best candidates.
    linkup,         K-Windows clients from KWIN_LinkUp_1_0.lzh: fonts,
    ansishow,       icons, .wav/.iff media, an installer that overwrites
    audioplay,      /DD.  Same position as the excluded G-Windows set --
    gport,          they need a display this collection has not got.  Their
    terminal        CMDS/kermit, CMDS/xy and CMDS/z also collide with names
                    already here.
    ot              OSKTag, a taglines tool.  NO terms anywhere: 7,778 bytes
                    of osktag.txt and its readme name no author, no
                    copyright and no grant.  Out on the utime.c rule.
    fpu             Microware's own ("(C) 1995 Microware Systems Corp.
                    Permission to distribute FPU is granted so long as this
                    file is retained").  A grant in the file against a house
                    rule that names fpu040 among the excluded -- rdoggett's
                    call, in FOR-RDOGGETT.md.

`k', `xy' and `z' turned out to be already on the disk with no provenance
recorded at all; that is fixed (64cf6cfb), and their Kientzle conditions are
already satisfied because each program prints the required acknowledgement
in its own `-?' output.  Their SOURCE stays out: condition 1 makes
redistribution conditional on owning the book and condition 3 wants the
author's written permission otherwise.

**So the whole 153-file, 34 MB refetch yields no new programs.**  What it did
yield is licence data: lharc and m4 (579f289c) and the three above.

### TOP's 30 source trees, triaged 2026-09-12 -- nothing stageable

`src_census.py disk --tsv' says 999 programs, 701 with source (70%), **298
without**.  TOP release 2 carries 30 source trees; the question was which of
them fill a real gap.  Answer: four, and not one can be staged tonight.

    bison   -> TOP/bison        Q2, rdoggett's call
    emacs   -> TOP/emacs_3.10   Q2
    gawk    -> TOP/gawk2.0      Q2
    larn    -> TOP/larn         BLOCKED ON TERMS, see below

Everything else TOP holds that ships here already has source: clock
(SRC/misc), world, animal, os9lib (SRC/rtf), and the rest by recipe.

**larn is the one worth writing down, because it will tempt the next
reader.**  TOP's tree IS the right source -- it is larn 12.0 and the shipped
binary's own strings read `Larn12.0.ckp' -- so the material matches the
program exactly.  It still cannot go in: all 25 files say only "Larn is
copyrighted 1986 by Noah Morgan", and a search of the whole tree for
permission, redistribute, public domain or freely-copied wording returns
NOTHING.  Bare copyright, no grant: the `utime.c' rule.  The binary already
ships (an older decision); adding the SOURCE would be a new act of
redistribution with nothing behind it.

**Two matching rules, both wrong, in opposite directions.**  Stem-matching
paired TOP's `puzzle15' tree with our source-less `puzzle' -- but `puzzle15'
and `puz15' both HAVE source (SRC/eff_puzzle15, SRC/v_misc) and
`CMDS/GAMES/puzzle' is a third, unrelated program TOP does not hold.  Exact
name matching then missed `emacs_3.10' -> `emacs' and `gawk2.0' -> `gawk'
and reported only two gaps.  Use the census tsv and check the specific pair;
neither rule is safe on its own.

Terms read from the other trees while I was in there, for whoever needs
them: bandit and v7make public domain; upatch Larry Wall 1986 with a copy
grant; clock (c) 1988 George M. Sipe all rights reserved; scpp (c) 1985
Tektronix; zmodem (c) 1986 Stephen Satchell; cpp.decus and typefast state
nothing.  TOP's package readme gives no licence at all -- terms are per
tree.

### DOC/ORIGINS is already mined -- do not plan a sweep through it

Checked 2026-09-12, after nearly starting one.  Of the 309 programs
`src_census.py' reports with no source here, exactly **5 have a DOC/ORIGINS
row** -- and that is not a gap in ORIGINS, which holds 597 program rows and
answers every control thrown at it (mimecode, gnugo, napoleon, maze).  It is
structural: the census's ARCHIVE route already consults ORIGINS ("disk/SRC/
<archive>/ exists, where DOC/ORIGINS says the program came from <archive>"),
so anything ORIGINS can place is counted as HAVING source before it ever
reaches the no-source list.  The 309 are precisely the residue ORIGINS
cannot help with; the ARCHIVE route contributed 12 of the 696.

So there is no cheap join to be had here.  Finding source for those programs
means per-program archive hunting, which is the work the batches above
already represent.

### Recovery log
- 2026-09-11: first sweep; table above.
- 2026-09-12: re-probed every row. **No change in our favour, and one row
  got worse for a reason that is not ours.** The Internet Archive is
  GLOBALLY OFFLINE today -- `web.archive.org/cdx/...` answers HTTP 503 with
  a page headed "Internet Archive services are temporarily offline", and
  `archive.org/wayback/available` answers 429 for every host. The front page
  answers 200, which is how this reads as working if you only check the
  root: **probe the CDX endpoint, not the front page.** So the three Wayback
  rows (chestnut.cs.wisc.edu, lucy.ifi.unibas.ch, the German university
  FTPs) and the `cdrom-coco-archive` row could not be tested at all today;
  their 429 is the outage, not a block on us. Retry when IA is back.
  Still refusing, same as yesterday: Google Groups comp.os.os9 (429),
  usenetarchives.com (403). Still no connection at all: ftp.uni-kl.de,
  ftp.leo.org, os9forum.de, os9.org, ftp.rtsi.com, minkirri.apana.org.au.
  Now answering where the table did not say so: effo.org (200) and
  colorcomputerarchive.com (200) -- both worth a real fetch next session.
  **Everything the pool was actually built from is up**: the sunet
  comp.sources.games mirror, funet's alt.sources, trashworldnews thread
  fetches and microware.com all answer 200. Nothing is blocking more
  harvesting; the blocked rows are the ones that were already blocked.

  **And the "we got cut off about 1990" is a property of the SOURCE, not of
  our access.** Measured in the pool: the tuhs copies we hold are
  `alt.sources` 1988-1991 and `comp.sources.misc` 1988-1991 and stop there,
  because utzoo/tuhs stops mid-1991 -- which is the row already in the table
  above. It is not a fetch that failed partway and can be resumed; there is
  nothing after 1991 at that source to resume to. The later years have to
  come from somewhere else, and one of them is already in hand: funet's
  `alt.sources.index` covers **volume93 through volume99** (5,356 lines)
  plus 1,350 lines of a flat modern `/pub/archive/alt.sources/NNNN.gz`
  section, and funet answers 200 today. So the real hole is **1992 to early
  1993** -- between where tuhs stops and where funet's volumes start -- plus
  the gaps the table already names. Next session's harvest should work
  funet's volume93-95 range, which is in era and untouched.

### Re-probed 2026-09-13 (overnight)

**The Internet Archive is ANSWERING again** -- `archive.org` 200,
`advancedsearch.php` returning real results, `web.archive.org` redirecting
normally. The rows above that assumed otherwise can be retried.

Four things measured tonight, so nobody spends the time again:

- **`utzoo-wiseman-usenet-archive` on IA is a TORRENT-ONLY STUB.** The item
  holds 12 files totalling almost nothing: an introduction, `listing.txt`,
  checksums, and a `.torrent`. `listing.txt` is 161 lines of raw
  `newNNNfN.tgz` news-spool tapes (~700 MB in total) with NO per-group
  index, so there is no way to confirm comp.os.os9 content, or to fetch
  only it, over HTTP. The obvious idea -- "get the early comp.os.os9 from
  utzoo via IA" -- does not work cheaply. It is a torrent and a 700 MB
  unpack, and it stops mid-1991 like every other tuhs/utzoo copy.

- **The comp.os.os9 we hold is 2003-2020 ONLY.** Measured on the harvest:
  `comp.os.os9.(1345).mbox` is 1,345 messages spanning 2003-2020, and
  `giganews-20140404.mbox` is 2003-2014. Across every other local usenet
  corpus (`decoded`, `funet`, `cis`, `alts`, `giga`) exactly ONE pre-2003
  message turns up, a 1990 one in `cis`. So the group's ACTIVE ERA -- the
  years this collection is made of -- is not held at all. That is a
  different hole from the 1992-93 alt.sources gap named above, and a
  bigger one for OSK material specifically.

- **136 issues of the Australian National OS9 Newsletter are on IA**
  (`australian-national-os9-newsletter-YYYY-MM`, 1988 through 1991+).
  Period community material that names programs, authors and disk
  libraries. BUT the OCR is bad -- a sampled issue gives `BasicO`,
  `0S9`, `DS-9 bo^`, `jmrai` -- so mining 136 of them automatically would
  produce mostly noise. Readable by a person; not worth a scraper.

- **RTSI answers 200 but is a Joomla CMS now**, not a file tree.
  `os9archive.rtsi.com` serves CMS pages; `/OS9/`, `/pub/`, `/OSK/`,
  `/OS9Archive/` and `www.rtsi.com/os9/` all 404. Whatever the archive
  still holds is behind the site's own menu, which needs a person.

**alt.sources is EXHAUSTED for OSK material, measured 2026-09-13.** The
local `unix/altsrc/subjects.tsv` indexes 12,026 articles; searching its
SUBJECT column (field 4 -- field 3 is the author, and searching that
matches `x68k.net' and `Jef Poskanzer' and tells you nothing) gives 8
hits for OS-9/OSK/68k/Microware in the whole corpus. All were fetched
and read:

  910227.08  someone ASKING for an OS-9 GNU C compiler. No code.
  910224.30  the reply: binaries sent to an FTP host, 1991. No code.
  910331.02  `gcc-68000 gnulib in *.s' -- a real shar, but generic 68000
             gnulib for gcc (source dir /home/cjp/gcc.68000), and
             GNULIB/gnulib.l and LIB/libgcc.l already ship.
  900915.23  an S-record generator; nothing here reads or writes S-records.
  940713.12  m68kdis, an M68000-family disassembler -- and `unc' already
             ships, which disassembles an OS-9 module back to assembler
             (Microware archive 4308, John Collins / hcz OSK port).

So the 1992-93 alt.sources gap named above is worth closing for
completeness, but should not be expected to yield OSK programs: the
group carried almost none across eight years either side of it.

**Where the real hole is: comp.os.os9, 1987-2002.** See the 2026-09-13
entry above -- what we hold starts in 2003. That is the group where OSK
freeware was actually posted, and no copy of its active era is in hand.

**comp.os.os9 1987-2002 CANNOT be closed from the Internet Archive.**
Searched 2026-09-13, so nobody repeats it. IA holds exactly five items
matching the group or its neighbours:

  FULL-USENET-BACKUP-2020-Oct-comp.os.os9.(1345).mbox.7z   the 531 KB
      archive we ALREADY HOLD, unpacked, 1,345 messages, 2003-2020
  usenet-comp.os            giganews' comp.os collection -- giganews
      begins around 2003, the same era we already have
  usenet-comp.os2, usenet-comp.os-windows,
  usenet-comp.os-mswindows  different groups entirely

There is no pre-2003 comp.os.os9 on IA, per-group or otherwise, and the
utzoo route is torrent-only and stops mid-1991 in any case (above). So
the group's active era has to come from somewhere that is not IA and not
tuhs -- a personal spool, a CD-ROM collection, or one of the German or
Australian OS-9 user-group archives, most of which are in the dead-host
table above. Worth retrying those hosts; not worth re-searching IA.

### The OSKer -- a new source, found 2026-09-13

**Six issues, July 1990 to 1991, at colorcomputerarchive.com** under
`repo/Documents/Magazines/The OSKer/` -- issues 1-4 dated (Jul 90, Aug 90,
Sep 90, Jan 91) and 5-6 undated. Note issue 6 is filed as `OSKer ISsue
#6.pdf`, with the typo, which a fetch loop has to allow for. Not recorded
anywhere in this repo before tonight.

It is an **OSK magazine**, not a CoCo one -- "Nevvs and Views in the World
of OS~/68000 and 6809" on the cover -- which is why it is worth having
even though the rest of that site is 6809 CoCo material and out of scope.
The PDFs have a REAL TEXT LAYER: issue 1 extracts to 151 KB, 15,982 words,
24% common English. (Contrast the Australian National OS9 Newsletter on
IA, whose OCR gives `BasicO', `0S9', `jmrai' and cannot be mined.)

**THE LICENCE CLAUSE, read whole and worth knowing:**

    All Submissions must be in the Public Domain to be considered for
    publication.  Persons who are selected for publication will be given
    the following 6 months of the OSKer for free, in addition to any
    paid-up subscription.

So code SUBMITTED to and printed in the OSKer was required to be public
domain. That is real licence evidence for anything sourced from it.
**But read the scope**: it covers submissions only -- not the magazine's
own text, not its advertisements, and NOT commercial products merely
reviewed in it. `MVCanvas Paint Program V2.0' and `StG Login Package BBS
V3.0' appear in these pages as products being sold, and that clause says
nothing about them.

**Two things that look like leads and are not.** The companion-disk
listing printed in each issue (`Directory of /dd/OSKer/Jul90') is the
ISSUE ITSELF as text files -- `A_Tale_Of_Two_Computers',
`Editors_Ramblings', `Goto_Shell' -- one file per article, not a software
library. And matching the magazine's prose against the 1,016 names we
already hold is useless: it returns 1,300 hits in one issue led by `for'
(244), `if' (117), `what' (72), `about' (55), because a great many OS-9
command names are ordinary English words.

**VERDICT: the OSKer carries NO SOURCE TO ACQUIRE.** Measured across all
six extracted issues: `#include' appears ZERO times in any of them, and
the scattered `main(' and `printf(' counts (2, 5, 0, 0, 0, 4) sit beside
brace totals of 9-95 -- the shape of prose DISCUSSING code, not listings.
"Playing Chess in C" is an article about writing one, not a program.

So its worth is as a REFERENCE and a LICENCE CITATION, not as a haul:
the public-domain submissions clause above, and six issues of period OSK
context naming people, products and user groups. Do not re-mine it for
programs; there are none in it.

### Archive state after the 2026-09-13 sweep -- start here, not at a search engine

    Internet Archive      UP.  advancedsearch works.  But see above:
                          comp.os.os9 1987-2002 is NOT there.
    alt.sources           EXHAUSTED for OSK.  8 subject hits in 12,026
                          articles, all five fetched, none shippable.
    utzoo-wiseman         torrent only, ~700 MB, no per-group index,
                          stops mid-1991.
    ftp.uni-kl.de         answers 200 and is now a DEBIAN/UBUNTU MIRROR.
                          /pub/ is driver gnu linux mozilla tmp tug
                          uninetz windows wireshark.  No OS-9.
    os9archive.rtsi.com   answers 200, but it is a Joomla CMS; /OS9/,
                          /pub/, /OSK/, /OS9Archive/ all 404.  THE
                          CONTENT MOVED: the whole RTSI tree is live at
                          microware.com's archive component -- and it is
                          the SAME corpus os9/mw/osk.tsv already lists,
                          same Phoca ids, zero new filenames.  Nothing
                          to fetch as a discovery.  See the RTSI section
                          below for the download route, the master index
                          (now in hand) and the maintainer's name.
    colorcomputerarchive  UP, mostly 6809 CoCo and out of scope -- except
                          The OSKer, above.
    ftp.rtsi.com          NXDOMAIN -- it does not resolve and never
                          will; the archive it served is the one above.
    ftp.leo.org, os9forum.de, os9.org,
    minkirri.apana.org.au        still dead, no connection at all.

**AND THE WAYBACK ROUTE TO THEM IS CLOSED TOO, surveyed 2026-09-13.**
Thirteen hosts, every one queried through the CDX API: Wayback captured
FRONT PAGES AND LINK TEXT ONLY.  The FTP trees were never crawled.
Across all thirteen there were 1,011 status-200 captures with an archive
extension and **every one is out of scope** -- Debian `.gz', Aminet
`.Z', cygwin, DOS `.zip'.  Zero OS-9/OSK archive files.

    os9forum.de, chestnut.cs.wisc.edu, ftp.rtsi.com   NEVER ARCHIVED --
        zero captures, even domain-wide with no status filter
    os9.org            front page and images; the domain later became
                       an iPhone site (453 rows on iphone.os9.org)
    os9archive.rtsi.com  1,793 real captures, all Joomla CMS or the
                       pre-2004 static site.  0 archive files
    minkirri           a real /pub tree IS captured (585 rows) and it
                       is APANA admin, cygwin, debian, DOS.  EXACTLY
                       TWO OS-9 files in it (below)
    ftp.leo.org, ftp.uni-kl.de, ftp.cs.tu-berlin.de   large mirrors,
                       zero genuine OS-9 (FreeBSD/KDE, Debian/CCC,
                       Aminet/Atari/C64)
    lucy.ifi.unibas.ch, ftp.informatik.uni-hamburg.de, ftp.ethz.ch,
    ftp.informatik.tu-muenchen.de   staff pages, /pub/unihh, a front
                       page, a robots.txt.  Nothing.

**RTSI IS NOT LOST, AND IT IS NOT NEW EITHER -- it is the archive this
pool already inventoried.**  Chased to the end 2026-09-13.

The tree is live, served by a Joomla download component at
`microware.com/index.php/os-9-archive-new/` (`?limit=0` on a category
URL or you get 20 rows; download by
`...os-9-archive-new?download=<PHOCA_ID>:os-9-archive`).  It was verified
by DOWNLOADING, not by reading a listing -- `colossal.lzh' comes back as
`LHarc 1.x/ARX archive data', an 11 MB gcc source tarball as gzip.  597
OSK files, 112.6 MiB; the whole archive is 4,183 files and 931 MiB, of
which OS9_6X09 alone is 548 MiB and is 6809, out of scope.

**Then the manifest was diffed against `os9/mw/osk.tsv' and the answer
is ZERO.**  All 570 distinct filenames are already listed there, and the
Phoca ids are IDENTICAL -- `ant.readme' is 3805 in both files.  So "the
lost RTSI archive" and "the Microware archive" are one corpus on one
host, and this plan mined it on 2026-09-11.  Nothing here is new
material.  **Do not plan a fetch of it as though it were a discovery.**

What IS new and worth having, and is now in hand:

  `os9archive.index'  321,774 bytes, md5 381ea89ddad5ad873294fa452ee44a84,
      4,861 lines -- a full `ls -lR' of the whole archive with sizes and
      dates.  The Wayback survey above concluded it "is not captured
      under any scheme or host", which was true of WAYBACK and beside the
      point: the file was live on the site the whole time.  A lesson
      cheaper to read than to repeat -- when an archive's index is
      missing from a mirror, ask the LIVE site before concluding it is
      gone.
  `osk-manifest.tsv'  597 rows, category path + phoca id + filename: a
      ready fetch list if a specific file is ever wanted.

Both are in `~/Developer/os9/Scraped/acquisitions-2026-09-13/rtsi/`.

**And a contact, which may matter more than the files.**  The archive's
`readme.txt' names its maintainer as **Allan R. Batteiger
<arb@rtsi.com>** -- the same Allan at Microware who was asked about the
five runtime modules and replied "I do not see a problem with those
modules" (`disk/SOURCES.txt`).  A known, already-cooperative contact for
any provenance question about this material.

**Two practical notes for anyone fetching from it:** range requests are
BROKEN (asking for bytes 0-2047 returned 206 with a Content-Range for
the tail and delivered the whole 11 MB), so plan whole-file GETs with no
resume; and three plausible mirrors are dead ends --
`archive.sundby.com/mirror/os9archive.rtsi.com/...` still appears in
search results but 302s every path to its own 404,
`blitter.com/~russtopia/files/OSK/` 404s, and `os9projects.com` is
CoCo/6809 documentation.

**The historical detail worth keeping: RTSI's archive was at
`www.rtsi.com', NOT `ftp.rtsi.com'** -- which is why every probe of it
failed.  `ftp.rtsi.com` is NXDOMAIN; `www.rtsi.com` resolves (Cloudflare)
and serves a Joomla front page whose `/OS9/`, `/pub/` and
`/os9archive.index` all 404.  The content moved to microware.com.

**DO NOT COUNT "what has been fetched" BY MATCHING FILENAMES UNDER
`os9/mw/'.**  Tried 2026-09-13 and it answers 547 of 704 never fetched,
which is nonsense.  The pool keeps three different things in there and a
name match conflates all three: `mw/' itself holds 53 SCRAPER artefacts
(category `.html' pages, `mwget.py', `files.txt'), `mw/refetch/' holds
152 original archive files under their own names, and `mw/dl/x/' holds
material ALREADY UNPACKED into per-program directories (`c09_Solitaire',
`osk_agrep', `c09_peruse_2_0').  So an unpacked archive reads as
missing and a saved HTML page reads as fetched.  **The figure that
stands is the one this plan already carries -- 127 OSK files the pool
never fetched** -- written by the session that built the layout.  If an
exact list is ever wanted, derive it from `osk.tsv' against
`refetch/' plus the DIRECTORY NAMES under `dl/x/', not against a flat
file listing.
`os9archive.rtsi.com/ftparchive.html', captured 2004-04-15, documents
the structure that was lost:

    ftp://www.rtsi.com/OS9/{OSK, OS9_COMMON, DOCS, BENCHMARKS, MISC,
                            MM1, MSDOS, OS-9000, OS-9_6X09, TOP,
                            USERGROUPS, VENDORS, incoming}
    plus os9archive.index -- a 203 KB master listing, 2003-08-26

`OSK' and `OS9_COMMON' are this collection's scope exactly.  None of it
is in Wayback -- all 19 captured `/OS9/' URLs are 404s or forum-paste
artifacts -- and `os9archive.index' is not captured under any scheme or
host.  **Keep the directory list as a MANIFEST for searching other
mirrors**, not as a place to fetch from.

Two genuine OS-9 files came out of the whole survey, and both are
DOCUMENTS, not software: `minkirri.apana.org.au/pub/misc/os9.faq'
(26,310 bytes, the comp.os.os9 FAQ 12th edition by Russ Hoffman) and
its gzip, internal mtime 1994-07-11.  Both fetched, in
`~/Developer/os9/Scraped/acquisitions-2026-09-13/wayback/'.

**A method trap recorded by that survey, worth more than the negative.**
Wayback's CDX `urlkey' normalisation STRIPS `?', so a query pattern like
`os.?9' matched `.../mods/atmos/?952114857' and reported 245 OS-9 hits
on tu-berlin that do not exist.  The filter was sanity-checked first by
requiring it to match 1,793 of 1,793 rows on a host whose name really
does contain `os9' -- which is the only reason the false positives were
caught.  Check a filter against a case it MUST match before trusting a
zero it returns.

**THE LIVE QUESTION IS ANSWERED, 2026-09-13.  comp.os.os9 1987-2002
exists, whole, at `usenet-rewind.com'** -- see the section below.  It is
not IA, not tuhs/utzoo, and not free; it needs a decision from rdoggett,
which is in `notes/FOR-RDOGGETT.md'.

### comp.os.os9 FOUND: usenet-rewind.com, 1987-2023 (2026-09-13)

Erie Data Systems, LLC.  `/newsgroups?group=os.os9' answers 200 and
lists **comp.os.os9, 05/1987 to 12/2023, 17,802 messages** -- and the
claim was checked by READING MESSAGES, not by trusting the row:

  * the oldest comp.os.os9 item is `OS-9 Discussions, V3 #1', 16 May
    1987, Daleske's moderated digest at cbdkc1, and #2-#10 follow
    through that month.  They carry **Dieter Stoll's ARC port to
    OS-9/68K, posted with permission**, and **James Jones' (mcrware)
    Lempel-Ziv compress**.
  * `mod.os.os9' goes back further still: digest #1 from `nyit!os9',
    16 January 1986, with Bob Larson's QT+ 68000 review.
  * the middle years are NOT thin -- per-year counts came back 1990:
    660, 1993: 1,097, 1996: 1,995, 1999: 993, 2002: 738.

The neighbours are there too: `sub.os.os9' (304), `de.comp.os.os9' (82),
`fj.os.os9' (55), `de.alt.comp.os.os9' (78), `mod.os.os9' (38).

**What is free and what is not.**  Full message BODIES render free and
anonymously.  Gated behind a plan: the author's address (shown masked,
`o••••@•••••.UUCP'), the original message download, and full headers --
which is exactly what an archive wants.  Free tier is 25 searches a
month; Researcher at $39.99/month adds a JSON search API.

**Their terms forbid scraping and bulk export and explicitly carve out
"an authorized API plan".**  So the API is the licit route and a scraper
is not, however easy the pages look.  That is the whole reason this is
rdoggett's decision and not a task to pick up.

### Usenet routes that are CLOSED -- do not re-search these

Measured 2026-09-13 alongside the find above.

    narkive              200, but its own header says earliest
                         2003-06-25.  The era we already hold.
    usenetarchives.com   403 Cloudflare JS challenge on EVERY path,
                         robots.txt and sitemap.xml included, by curl
                         and by fetch.  It demonstrably HAS the group
                         (Wayback holds view.php URLs carrying 1980s
                         message-ids) and there is no fetchable route.
    Google Groups        429 on nearly every request.  Its archive did
                         index 1987 -- Wayback has browse_frm/month/
                         1987-05 -- but those captures are 771-byte
                         FRAMESETS whose data frames were never
                         archived.  A trap to know about: timestamps
                         decoded from its 2024 captures repeat
                         identically across unrelated threads.  They
                         are page constants, not message dates.
    Archive Team
    "googlegroups"       1,389 IA shards, and it is the 2011 HOSTED
                         groups project, not Usenet.  Irrelevant.
    Yahoo Groups rescue  no OS-9/OSK group in it.
    groups.io            os9, os-9, nitros9, coco, os9-68k all 404.
    IA giganews
    usenet-comp.os       does hold comp.os.os9, and its CSV sidecars
                         say 1,291 messages, 2003-06-25 to 2014-09-17.
                         2003 is that corpus's wall, confirmed.
    skrenta.com utzoo    the wget-able UTZOO mirror the SDF guide
                         recommends is DEAD -- the domain 301s to
                         LinkedIn and Wayback archived none of the
                         .tgz pieces.
    NetNews CD-ROMs      15 Sterling Software discs on IA, but April
                         1992 to January 1993 ONLY, ~625 MB each, and
                         the spool is "organized in order received"
                         with .XRF cross-post files -- NOT indexed by
                         newsgroup.  About 9 GB to pull for maybe three
                         months of coverage.  A fallback, not a plan.
    olduse.net           46-year replay delay.
    schestowitz          2004+.  darkrealms is Fidonet echomail.

Full working notes, 115 lines, are outside the repo at
`~/Developer/os9/Scraped/acquisitions-2026-09-13/usenet/'.

### Software FOUND in the pulled newsgroups (2026-09-14, first pass)

rdoggett's aim, restated: *"we're not just collecting files, we're looking
for other software that has been published that should belong in the
collection"* -- and *"I don't want to go porting everything from unix, or
necessarily anything at this point."*  So this is a CANDIDATE LIST, not a
work queue.

How it was found: `~/Developer/os9/Scraped/usenet-rewind/mine.py` over the
18,175 unique messages pulled so far (comp.os.os9 1987 to about 1998, plus
mod.os.os9 and the small groups) -- posts carrying a uuencoded file, a
shell archive or `Archive-name:` headers, and posts announcing an FTP path
-- then every name checked against disk/CMDS, disk/SRC, DOC/INDEX,
DOC/ORIGINS, notes/pool-members.tsv and the rtsi os9archive index.
`candidates.tsv` beside the script has every hit with its message URL; it
carries authors' names, never addresses.  Rerun it as the pull completes.

**In the pool already, never evaluated, not on the disk:**

    textb       ALREADY ON THE DISK (CMDS/textb, with a recipe) -- this row was stale.
                OSK/MISC textb.t.Z -- PD Mandelbrot generator, 1990; binary,
                textb.c and textb.doc.  Posted to comp.os.os9 1990-09-20.
    ptxm        OSK/DRIVERS ptybin.lzh -- ptxm, ptxminst, ptxm.txt (a pty
                manager binary); ptylev.zip is unreadable (BadZipFile).
                The PTY file manager source was posted twice: Reiner Mellin
                1989 (binary + sources 1/2) and Ptyman 1.3 by Frank Kaefer,
                comp.sources.os9-style v02i003-005, 1991.
    tass        OSK/TELECOM tass.lzh -- newsreader, 13 C files, no binary.
                Posted as "Tass for OS-9" Part01-03, 1992-12-24.
    mnews       OSK/APPS mnews.t.Z (200 members) + mnews_src.t.Z, and
                TELECOM mtp.lzh is ALSO MNews source (158 members, MNEWS/).
                Full news system, source only; may overlap the news tools
                already on the disk.  MNews.lzh is empty.

**Only in the newsgroup posts (no pool or rtsi copy found):**

    mtp         Alan McIvor, 1992-01-21 -- module transfer protocol, host
                client + OS-9 daemon (mtp.c mtpd.c mtpdc.c mtpvalid.a ...),
                one complete shar.  NOT the disk's `transfer', which is a
                GDOS disk copier from EFFO forum1.
    systemfm    1997-06-12 -- a /proc-like file manager "tested on 68302,
                MVME 177, MVME 167, Eltec E6, Atari ST", uuencoded + gzip.
    tar 1.9     Christian Engel, 1990-09-28 -- an OS-9-native tar (tar.c,
                makefile, tar.doc, tar.hlp); the disk ships GNU tar 1.10.
    ln/link/rename/mv   Bob Larson, 1989-01-15, for os9/68k.
    osk_version()       Wolfgang Ocker, 1990-03-27 -- a library function.
    Isofont     Cumana OS-9 on the Atari ST, 1991 -- hardware-specific.
    br.bas      BASIC09 biorhythm, German, SubNet 1989 (repost 1992) --
                a different program from the disk's C `bio'.

**Checked and already on the disk:** browse (the Emde 1990 port, per
ORIGINS), screen, patch, less, elm, lharc, bash.  **Out of scope, 6809:**
Pete Lyall's Kreider C library, hdkit, ar and 2-pass cc driver (1988-89),
Dru Nelson's mv (1990).

**FTP sites the posts name that these notes did not know:** Wisconsin's
cabrales/chestnut/hermit.cs.wisc.edu `/pub/OSK/...`, zelux7.zel.kfa-juelich.de
`~ftp/pub/os9/BASH` ("OSK bash is now available", 1993), hcshh.hcs.de `/fkk`,
and the os9tools SourceForge project (2000).

**Second pass, 2026-09-14, over ALL 14 OS-9 groups (18,424 unique
messages, every group's count matching the site index except comp.os.OS9,
re-pulled separately).**  Only two posts the first pass lacked: Frank
Kaefer's banner programs (1992, alt.sources + de.comp.sources.os9 -- the
disk's `banner' is from misc.ar and may be a different program) and `br',
Biorhythm v3.0 (comp.sources.misc v41i126, 1994, a later version of the
1989 BASIC09 post).  **Software stopped travelling INSIDE messages after
1992.**

From 1994 it travelled by LINK instead: 2,370 messages carry a
non-quoted web link, peaking 1996-1998.  But only ONE linked archive file
is unknown to the collection and pool (a VxWorks manual, irrelevant) --
the links point either at archives already held or at web PAGES.  So the
later era's software is behind sites, and the sites these notes had never
looked at are:

    dlso.dl.ac.uk:8001/      Daresbury; 1995 "Re: chestnut archive?" -- a
                             possible mirror of Wisconsin's OSK archive
    members.xoom.com/os9/    1999-2000, incl. "OS-9 NFS Client"
    www.pobox.com/~alsplace/os9.html   1998, a personal OS-9 page
    homepage.mac.com/jamiec/Invaders%2009/   2001, probably 6809

`klebsch.de' is only a PGP-key signature line and `dressler.de' a
commercial VMEbus vendor -- not leads.  The Wayback CDX check of the four
is recorded beside this.

### The 44 os9 postings, the rest assessed 2026-09-15

`acquisitions-2026-09-11/os9/usenet/postings' holds 44 posts.  Most are
covered above or in B5/B9 (freeb shipped, ptyman, os9lib, alarmd, simon,
browse, uucp, shar, isofont, nethack, less 8-bit, textb and banner already
on the disk).  The ten nothing here had assessed:

    ln-mv-link-rename  Bob Larson 1989, os9/68k, public domain.  NOT SHIPPED:
                       ln and link make hard links by writing directory
                       entries and the raw disk ("USE AT YOUR OWN RISK ...
                       I'm not sure the locking works"), restricted to the
                       super-user.  That is the RBF alias flink made, and
                       flink corrupted this disk.  The disk's mv is GNU's.
    dynacon            Jim Omura 1989 -- converts CoCo Dynacalc files; a 6809
                       makefile only.  CoCo: last.
    runat, fs walker   James Jones 1984, net.micro.6809.  CoCo: last.
    piped-cc           Larry Harmon 1987 -- replaces the 6809 compiler's cc1
                       pass with pipes.  6809 only.
    icapos9 (2 parts)  Jim Omura 1989 -- Imagewise frame-grabber kit; needs
                       the hardware.
    st-osk-graphics    Pete Lyall 1988 -- Atari ST graphics routines, part
                       assembly; needs the hardware.
    mroff doc tools    Simmule Turner 1989 -- man-page macros for MROFF on
                       OS-9/6809, not a program.
    osk-book           James Jones 1988 -- announces Dibble's OS-9 Insights.
    top-software-list  1989 -- TOP's disk list, already mined in B6.

### The 135 Unix posts, triaged 2026-09-15

`acquisitions-2026-09-11/unix/posts' holds 135.  79 are named somewhere in
the tree or these notes (ported, or assessed above).  The other 56 were
triaged by size, files, curses and stated terms.  Done or decided:

    choose      DONE (1ac41c32) -- random lines, OSK arm (clock, rand, tmp)
    pig         DONE (1ac41c32) -- lex filter, scanner from the disk's flex
    morsecode   NOT SHIPPED: lex plus Pascal, and the disk has `morse'
    center      NOT SHIPPED: "public domain ... Contact author for
                redistribution rights, or inclusion in package" -- the terms
                ask to be asked -- and fgets/feof misuse repeats a line
    chop        NOT SHIPPED: fields and columns, which cut, colrm and field do
    halign      NOT SHIPPED: aligns columns, which column does

    hanoi, hanoimod, telewords, telenum, anagram, psychic, lotto
                DONE (d63c88c4) -- telenum had the putchar double evaluation,
                hanoimod under-allocated, lotto asked forever at end of input

    knight, bks DONE (488587fd, card fix 3e3541a6) -- knight's ESC freed
                before initscr(); bks as BSD with tsleep and _gs_rdy
    revcat      NOT SHIPPED: reverses line order, which tac does
    spiro       NOT SHIPPED: draws through Unix plot(3X), which OS-9 lacks
    therm       NOT SHIPPED: a curses library routine, not a program, and
                "Commercial use prohibited without permission"
    ufo         NOT SHIPPED for now: its game loop runs on ualarm() and
                SIGALRM at millisecond intervals, with ftime() -- a timing
                rewrite, not a port
    malawi      NOT SHIPPED: X11/Xaw only

    mz          PORTED, NOT SHIPPED (2026-09-15): it builds and plays -- the
                raw stream shows the whole maze drawn and the player and
                monster moving -- but every maze row is exactly 80 columns
                and relies on the terminal's auto-margin wrap, which
                tools/ansiscreen.py does not do (START-HERE 2n), so its card
                and play-test screens render as a blank board.  Ship it once
                2n is fixed.  The port, all in mzio.c under #ifdef OSK:
                vttest's sgtty.h/sgtty.c for gtty/stty; get_time() from
                _sysdate(3,...) -- seconds since midnight, the tick in the
                low word and ticks per second in the high word; key_pressed()
                with _gs_rdy(0) for select(), handing a ^C byte to
                request_quit() because sgtty.c clears the interrupt key; the
                usage log (its author's home directory) a no-op.  Recipe:
                mz|mz|mz.c mzio.c sgtty.c||/dd/LIB/termlib.l|.  Terms: "may
                be used and distributed freely ... name retained".

    sol, solx   DONE (33739d93) -- cpp's line limit (about 500, not the
                fixed 512 this row used to name) counted after joining
                continued help strings, even in a skipped #if, so
                they print a line at a time; termlib's BC and UP are
                pointers the programs wrote as arrays; SIGTERM; ioctl shim
    jumble2     DONE (c622dbe9) -- GAMES/words, GAMES/JUMBLE2/scores,
                SIGALRM 5.  `Time ran out.' at the timeout comes from
                straight-line code after the interrupted gets(), not from
                the SIGALRM handler (unix.l defers handlers to
                check_signal(); measured by the skill session)
    calcdate, soelim, ticktalk
                DONE (3a74512d) -- soelim's usage passed *argv[0] to %s
    weekday, repunsel
                DONE (545b494f) -- weekday as posted with Spencer's getopt;
                repunsel's scanner from the disk's flex
    magicsqr    NOT SHIPPED: a REXX script, not C
    mfold       NOT SHIPPED: the post is Patch02 alone, no base program
    bday        NOT SHIPPED: an administrator's tool that mails birthday
                greetings through sendmail from /usr/adm lists
    xmascard    ALREADY ON THE DISK as `card' (Istvan Mohos, 1984)
    rise_set    NOT SHIPPED: computes for one observer, its author's house,
                hard-coded; needs ftime() and atan2(), which this C library
                lacks
    qterm       ASSESSED 2026-09-15, not ported -- a judgement, not a build
                failure: qterm 3.0 (comp.sources.unix v10i072, six files)
                works by SENDING an escape sequence and interpreting what
                the terminal SENDS BACK.  Under os9exec the thing that
                answers is the host's terminal emulator, so a card would be
                reporting on whoever's xterm ran it rather than on anything
                this collection does, and the answer would differ for every
                reader.  Its job is also already done here: SYS/login sets
                TERM and TERMCAP, which is what the 84 termcap programs
                read.  The ioctls would map onto _gs_opt/_ss_opt the way
                vttest's sgtty.c does, so it could be built -- it should not
                be carded.
    ag          DONE (fe2bbc79) -- the ag2 post's generator, default word list
                GAMES/words; Sean Barrett's pref/postf filters kept, not built
    colm        NOT SHIPPED: sets a list out in columns, which `column' does.
                It was ported and works (Spencer's getopt; `static' moved
                before the return type in column.c, which Microware C wants;
                its usage string split, and its %s with no argument filled)
    xtail       ASSESSED 2026-09-15, not ported: everything it calls for IS
                here -- opendir, readdir and struct direct in DEFS/dir.h,
                S_IFMT/S_IFREG/S_IFDIR in DEFS/modes.h, SIGINT and SIGQUIT
                in DEFS/signal.h.  The obstacle is that it never ends by
                design: it sleeps, re-stats and prints for ever, which no
                card or case file here can drive to a finish.  Its shar
                needs a second extractor pattern too -- the end marker
                comes BEFORE the redirect and carries a dot, as in
                `sed -e 's/^X//' << 'END_OF_FILE_xtail.h' > xtail.h' --
                and five of its seven files were silently missed until
                that was noticed.
    xfmt        DONE (db77304e) -- comp.sources.unix v16i071.  The post's
                flex.skel.diff is NOT needed: this disk's flex.skel is
                skeleton 2.16 and already carries both halves of it.  What
                this flex did want: 17 column-1 comments in the rules
                section indented, 15 uses of a definition holding trailing
                context written out in place, and yyin given stdin before
                main()'s file loop -- without that a NAMED file scanned
                nothing and said nothing, while standard input worked.
                SRC/xfmt/README.OSK.
    perp        DONE (796bc613, ORIGINS order 430c07ef) -- data in GAMES/PERP;
                BSD's sprintf returned its buffer and the status panel printed
                that; ^C needed check_signal()
    torus       DONE (0c76281c) -- score files opened without link(), $USER
                for the name, check_signal() in the key read
    molecule    NOT SHIPPED: the simulation writes binary coordinates for a
                display program built on a frame-buffer library (mginit,
                mgihue) that has no counterpart here
    smiley      DONE (0b8de539) -- two changes: an exit() wrapper, because main's
                return value reaches the shell as 0 here, and its write() macros
                through stdio, since a raw write to a terminal gets no line feed
                (bd05465d; the card it smeared, bb5374a3).  The face list ships
                as posted.  rdoggett, 2026-09-15: "If we censor any of it, we
                are positioning ourselves as moral police.  I say take it as it
                is, or reject it in whole."
    marquis     NOT SHIPPED: forks into the background to scroll a message on
                a terminal status line, and no terminal in SYS/termcap has one
                (no ts/fs); it refuses to start without
    xmases      NOT SHIPPED: seasonal joke shell scripts, not a program
    chemtab     DONE (8d537dd8) -- each global defined in one file for l68,
                a one-key getchar, data in LIB/chemtab, manual pages in
                DOC/chemtab; looke.c is continued across shar parts 1-2
    vcraps2     DONE as vcraps (c001e096) -- patches 1-2 applied, rand, w_cols,
                one Return case, getopt, ESC freed from SCF's end of file
    translit    DONE (f15d0115) -- the whole package; tables name end-of-line
                as 0x0A, so under OSK CR is read as LF and LF written as CR;
                the post's KOI8 and ALT examples, decoded on OS-9 with
                uudecode and `autolf -C', give its example.tex except two
                leading spaces the input lacks.  toos9's INDEX entry named
                `autolf -l -C', which converts nothing (fixed, 13ffcea2)
    trek73      DONE (b20bcb93) -- parser and scanner made on OS-9 with
                yacc and flex, flex fed through YY_INPUT, the timed prompt's
                interrupted read handed to check_signal(), no saved games
    yid-slots   DONE as yidslots (4def3472) -- built unchanged but for its names
                file, read from GAMES/YIDSLOTS; rand for random, and the module
                drops the hyphen, since no program name here carries one and the
                catalogue's entry parser does not accept one
    scamper     NOT SHIPPED: X11/Xlib only
    hodge-c     ASSESSED 2026-09-15, not ported -- and THIS ROW'S BLOCKER
                WAS WRONG.  The pipe to a display monitor is one output mode
                among several, not the only one: its manual documents
                `--animation-file-name hodge-%0003d.ppm', so it writes PPM
                files directly, and this disk's netpbm reads them.  What
                actually costs is the size and the option parser: 33 parts,
                2 MB of posting, ANSI throughout with GNU getopt_long, which
                is a substantial parser to convert on a K&R compiler that
                ansi2knr cannot help with (its definitions put the return
                type on the name's line, like thricken's).  GPL v2 is no
                obstacle -- m4, napoleon and juggle already ship under the
                GPL with COPYING beside them.  A real port, worth doing on
                a night that starts with it rather than ends with it.
    banners     ONE SHIPPED, the rest assessed 2026-09-15.  banner1 is DONE
                (8d58010d): banner-01 of the collection, written in 1987 by
                Wolfgang Ocker and described by its own README as "the very
                first banner on OS-9/68000".  It builds UNCHANGED -- the
                #ifdef OSK arms were already in it, and _errmsg() and
                intercept() are both in clib.  The rest are not carried and
                each for a stated reason:
                  banner-04   IS the disk's `banner' (Brian Wallis's
                              sysvbanner) -- confirmed by matching its
                              licence text and its first glyph row, not by
                              name.
                  banner-05   holds the disk's `cursive' (Jan Wolter's),
                              plus block/kban/lban/sban/vban/3db/leb/seb.
                  banner-12   is banner1's own descendant (Ocker 1987 ->
                              Kaefer -> Black), GPL v2.  The same banner
                              twice; the period original is preferred.
                  banner-11   `mb' reads an external font and the author
                              ships NONE -- "I haven't included any, 'cause
                              I don't [know] if they are copyrighted".  It
                              would ship broken.
                  banner-10   scripto is Pascal; banner-03 carries Fortran
                              data files.
                  the others  ordinary Unix banners, duplicating what is
                              already here.
    look_rac    ALREADY ON THE DISK as look (Net/2)
    revcat_db   NOT SHIPPED: backwards cat, which tac does
    more-xmas   NOT SHIPPED: a reply carrying a joke, not a program
    ogre        NOT FETCHED: the post's directory is empty
    map, poker, queens, clock, rain -- these posts are other programs than
                the disk's of the same names (disk blocks, SNOBOL poker, an
                IOCCC entry, misc.ar's clock, toys.ar's rain); not yet
                looked at
    roll        DONE (3508b84c) -- unchanged, rand for random in the recipe
    ski         DONE (3508b84c) -- unchanged, rand for random in the recipe
    wf          DONE (3508b84c) -- 74K of word lists declared remote, four
                `};' made `}'
    curses-clock ALREADY ON THE DISK: the post's gdc is the grand digital
                clock the disk ships as gcl (v_misc.ar)
    rain (v28)  NOT SHIPPED: Col. G. L. Sicherman's 1994 rain -- drops fall and
                pool.  A quick port (its USLEEP path, rand for lrand48), but the
                disk already ships a rain screen toy and the only difference is
                the drop pattern; naming a second one to tell them apart is not
                worth a program's place
    hp          DONE (77989aad) -- floating-point RPN; its parser reads numbers
                out of the line where lex's input() left it, so flex takes
                characters one at a time from hp's reader, made with -I
    xmas_pic    NOT SHIPPED: a uuencoded file of VT100 escapes to cat, not a
                program, author unknown
    lp-posters  NOT SHIPPED: compressed 132-column line-printer pictures and
                a filter; several are copyrighted cartoon characters and two
                are pinups
    dr_mario    DONE as bugs (18246404) -- BUGS I; _gs_rdy for FNDELAY, tsleep
                for select(), globals defined once
    letters     DONE (1c377278) -- _gs_opt/_ss_opt and _gs_rdy for its termio
                keyboard, setterm() renamed away from curses.l's, words from
                GAMES/words, an empty score file.  os9exec returned at once
                from a sleep under a tick (reported; fixed in its 263b94a), so
                a 4/256 floor came in and went out again (see git log)
    cent        NOT SHIPPED: the post carries Steven L. Wagar's rand.c,
                "Copyright (c) 1982 ... All rights reserved." with no grant, and
                ORIG ships a post as posted -- the ground dinkum2 was dropped on.
                cent.c itself allows redistribution with its notice.  The port
                would also want _gs_rdy for FIONREAD, tty ioctls, an nlist() load
                check and a help file run through system()
    pac         ASSESSED 2026-09-15, not ported: the five parts extract and
                read cleanly (29 files, all ASCII, longest line 86), and the
                curses half is ordinary.  The blocker is architectural: pac
                does no arithmetic itself -- `pipes.c' forks `bc' and talks
                to it over a two-way pipe (fork() + execlp("/usr/bin/bc")),
                and the post says so outright.  This C library has no fork,
                no pipe, no popen, no dup and no wait; clib does have
                os9fork/os9exec/modload, and SRC/perl4/osk.c, SRC/pdksh and
                SRC/sc show the shape, so it COULD be rewritten around
                os9fork plus named pipes -- a sub-project with deadlock risk,
                not a port.  SIGTERM/SIGTSTP/SIGCONT are absent here too.
                bc, dc and hp already ship.  Terms: no copyright anywhere,
                only "Author: Istvan Mohos, 1987" in each file header.
    dialog      ASSESSED 2026-09-15, not ported: dialog 0.3 (Savio Lam,
                comp.sources.misc v41i109-111, GPL v2 with COPYING).  The C
                is clean for this disk -- no system(), fork(), popen(),
                signal() or ioctl, only getenv and fopen -- and the ANSI
                work is the same hand conversion thricken had (59
                declarations, 24 definitions, none convertible by ansi2knr).
                THE LIBRARY IS THE PROBLEM.  It draws every box out of the
                ACS line-drawing characters (ACS_HLINE, ACS_RTEE, ACS_LTEE,
                the corners, the arrows) and ACS_ appears in NO ncurses
                header here; start_color, has_colors and init_pair are in
                neither header nor library, and colour is what rc.c and
                colors.h exist to configure.  Supplying those would be
                rewriting the program's presentation layer, which is the
                program.  Note also moria's finding: this ncurses.l cannot
                read SYS/termcap at all without tcentry.c linked ahead of
                it, so the substrate is thin for any new ncurses program.
    craps       DONE (b54b5a4b) -- comp.sources.games v1i009, 1987, public
                domain, K&R already so nothing was converted.  Every blocker
                this row named was real and each had an answer: the link()
                lock is not taken (no link() here, and RBF has no hard links),
                the crypt() cheat and the fork()/csh escape say so instead,
                BSD random needed nothing at all (its XENIX arm is time(),
                srand() and rand(), which is what this library has), getchar()
                became getch() -- crmode() only sets a flag on this curses --
                and REFRESH is undefined before craps defines it.  update()
                collides with curses.l as well.
                TWO THIS ROW DID NOT PREDICT, both worth more than the rest:
                printw() BUS-ERRORS on a floating-point conversion, and craps
                keeps every amount as a double, so it drew nothing at all.  It
                is printw ALONE -- wprintw, mvprintw and mvwprintw render the
                same float, to stdscr as to any window -- so one define fixes
                it and the call sites stand as posted.  And final.c's unneeded
                <sys/types.h> made the program's OWN types.h answer an include
                from inside a system header, pulling unguarded curses.h in
                twice: 62 errors, all of them inside sgstat.h.
    thricken    DONE (c9d4813d) -- comp.sources.games v13i101 with v13i102
                Patch1, the sequel to perp.  The ANSI prototypes were the
                whole of the deferral and `KNR' does NOT answer them here:
                ansi2knr rewrites a definition only when the function NAME is
                at the left margin, and all sixteen of thricken's write the
                return type on the same line, so it converted NONE -- and it
                never touches declarations.  Thirty-two constructs converted
                by hand instead.  Data in GAMES/THRICKEN; SRC/thricken.
    skewlife    NOT SHIPPED, assessed 2026-09-15: the makefile compiles it
                twice with -DN1=1024 -DN2=1025 and -DN1=2048, and its board
                logic comes from a GENERATED results.c that `makeresults'
                writes -- the author's own note says that file is "big
                (>700K)".  Three-quarters of a megabyte of generated C
                through this cpp, for a batch life computation on skewed
                2x2 squares with no display of its own.  The collection
                already carries life in several forms.
    dinkum2     NOT SHIPPED: Gary A. Allen's `strict NO MODIFICATION rule' --
                hacking encouraged but not releasing modified versions, and an
                OS-9 build is one.  It is also ANSI-prototyped throughout.

**RESOLVED 2026-09-16 by sweeping every name against the disk.**  The list
that stood here opened "Still open, then" and named 36 programs.  Not one of
them was open.  Fourteen ship under their own names (craps, torus, perp,
thricken, sol2, jumble2, trek73, ag2, weekday, chemtab, smiley, ticktalk,
calcdate, translit).  Five ship under another name, which is what made the
list look alive: vcraps2 is `vcraps', connect4 is `c4', yid-slots is
`yidslots', xmascard is `card', bj2 is `bjack'.  The rest each carry a
recorded NOT SHIPPED decision in the rows above -- malawi and scamper
X11-only, mfold a patch with no base program, molecule binary output,
xmases shell scripts, magicsqr a REXX script, bday an administrator's tool,
marquis forks into the background, colm duplicates `column', rise_set
computes for its author's house, banners duplicates the Unix banner, and
skewlife, dinkum2, hodge, xtail and qterm each assessed above.

**One live candidate remains, `mz', and its port is NOT IN THE TREE.**
There is no SRC/mz, no binary, no recipe and no INDEX or ORIGINS row; the
port was done in a scratch pool that is gone.  What survives is its row
above, which records the recipe line and every mzio.c change -- enough to
redo it.  It is blocked on 2n, and 2n is still open: tools/ansiscreen.py
CLAMPS the cursor at the last column (line 152) where a real terminal with
autowrap moves to column 0 of the next row, so mz's 80-column maze rows
render as a blank board.  Fixing that renderer is the enabling step, and it
is behind every published screen, so it wants measuring on both sides.

**Do not trust this list again without a sweep.**  That is twice now:
repunsel and soelim on 2026-09-15, and all 36 of these on 2026-09-16.

### The OSK sites the newsgroups name, checked 2026-09-14

rdoggett: *"you should definitely check out the osk sites you uncover in
wisconsin, germany or wherever."*  Done for every host the posts named
that the 2026-09-13 Wayback survey (thirteen hosts, above) had not covered.
Method as before: the Wayback CDX API, domain-wide, then the pages read.

    cabrales.cs.wisc.edu, hermit.cs.wisc.edu   never captured
    dlso.dl.ac.uk (:8001 and :80)              never captured
    members.xoom.com/os9/                      never captured
    zelux7.zel.kfa-juelich.de   9 captures, COSY accelerator-control pages;
                                the ~ftp/pub/os9/BASH tree never crawled
    hcshh.hcs.de                142 captures; the only software is Linux
                                packages under /users/hm (pcvt, ups, ...);
                                Frank Kaefer's /fkk never captured
    tornado.oche.de             157 captures, personal pages and Debian notes
    os9tools.sourceforge.net    captured 2002-2004: Boisy Pitre's HOST-side
                                utilities (os9dir, os9copy, os9dump ...) for
                                OS-9 disk images, ToolShed's forerunner --
                                they run on Linux/Windows, not on OS-9, so
                                OUT OF SCOPE.  sourceforge.net itself answers
                                a Cloudflare challenge (403).
    people.delphi.com/os9al     Allen Huffman's 1997 pages (pobox ~alsplace
                                redirects there, later disneyfans.com): an
                                OS-9 links page and a web-tour generator; no
                                OSK downloads.  Sub-Etha Software was
                                commercial.

**Invaders 09 has an OSK version that no archive we know holds.**
homepage.mac.com/jamiec (captured 2004): Allen Huffman wrote it in 6809
assembly for the CoCo 3 under OS-9 Level II; "in 1995 I rewrote Invaders
09 in C for a 68000 based machine called the MM/1 that ran a version of
OS-9 known as OS-9 68K. I think I released it around 1998"; the page
offers only the 2001 Mac OS X port.  Not in the pool, rtsi or the posts.
A lead, not a fetch: the MM/1 release would have to turn up somewhere.

**Wisconsin's OSK archive is COVERED.**  The 2026-09-11 comparison of
chestnut's 1994 index (`acquisitions-2026-09-11/os9/ftp/chestnut-missing.txt`)
listed three OSK files the pool lacked, and the list is now STALE: the pool
has `diff.tar' (6 members) and `os9_unix' (11 members -- Ivan Powis's rsh,
rshd, rcp, rmt and lpr, 1992, followed in the posts from chestnut to rtsi
through 1998; it needs Microware's ISP networking), and the third,
`mtp.shar.Z', is McIvor's 1992 module transfer protocol, which exists whole
in the comp.os.os9 post.  Everything else on that list is 6809, CoCo 3 or
G-Windows, outside this collection's scope.

### CD-i: could any player run this collection? (2026-09-14, from the posts)

rdoggett: CD-i software may be unusable -- the players have hardware we do
not.  Were any CD-i systems usable as computers?  Answered from the pulled
comp.os.os9 and comp.sys.m68k posts; rec.games.video.cd-i is queued and
may say more.

  * CD-RTOS is OS-9/68K v2.4 by Microware (Microware staff, comp.os.os9,
    1991-10-25), on the Philips/Signetics SCC68070 -- 68000-instruction
    compatible, with an on-chip UART, timers, I2C and DMA.
  * The CONSUMER players (910, 220-class, 450) are not computers: "not
    suitable as a development station" (1991-11-06); base configuration
    1 MB RAM, no floppy, no hard disk, no keyboard as shipped (1994, 1996),
    descriptors in ROM so xmode cannot change them (1995).
  * The PROFESSIONAL players WERE usable as OS-9 machines: the 180 series
    "has floppy drives, SCSI ports, etc. as optional equipment" (1991); the
    CD-i 605 is reported in 1993-2000 running OS-9/68K 2.4 with a shell,
    serial terminal on /t2, keyboard descriptors kb/kb1, SCSI, an Ethernet
    card running Microware's FTP server, floppy + PCF, and mtools built for
    it (1998); a 605T/20 with disk drive, Ethernet and SCSI (2000).  Also
    OptImage Media Mogul's "CD-RTOS shell" on development stations.
  * The two OS-9 COMPUTERS built on the same 68070/VSC chip set -- the
    IMS MM/1 and Frank Hogg's TC70 -- ran full OSK with floppy, SCSI and
    serial ports, and the disk already carries MM/1 builds.

So: this collection's 68000 binaries are the right instruction set for a
605 or 180 with floppy/SCSI and enough RAM (1 MB base is tight; the DV
cartridge adds 1 MB).  Not measured -- no one here has a player, and
cio/csl/math edition requirements and a console that is a TV plus
serial port are the likely obstacles.  A 1999 post announces a CD-i
website "with OS-9 info and software ... for usage on a OS-9/68K
development station" -- worth finding once the CD-i group is in.

### CORRECTION to the candidate list above, and the CD-i site (2026-09-14)

**Most of the "only in the newsgroup posts" list was ALREADY IN HAND.**
The 2026-09-11 session extracted postings from a 1,345-message
comp.os.os9 mbox plus csm/csu/csg/alt.sources indexes into
`acquisitions-2026-09-11/os9/usenet/`, and this session did not read that
directory before writing the list.  Checked against it:

    ALREADY EXTRACTED (postings/, some decoded/):  Ptyman beta, 1989 source
      and 1.3 source+binaries; Ocker's SCF ptys; textb (Mandelbrot); Isofont;
      8-bit less diffs; Larson's ln/mv/link/rename; NetHack 2.2 OSK port
      (Larson/Omura -- port files only, needs the 2.2 source) and NetHack
      3.0f OSK binaries from TOP (B6 above); os9lib; Omura's and Wecker's
      shar; Sampson's UUCP; browse; alarmd; simon.
    KNOWN TO ITS THREAD INDEXES, NOT EXTRACTED:  McIvor's mtp (twn thread
      653171), Engel's tar 1.9 (653410/653606/653637), osk_version (653515),
      GCC 1.37 for OS-9 (NIIMI, csm), Kaefer's banner programs and tass
      (alt.sources index), br Biorhythm (csm index).
    GENUINELY NEW HERE:  the 1997 /proc-like system file manager
      (comp.os.os9 1997-06-12, uuencoded); MNews in the pool; lftocr; the
      Invaders 09 OSK lead; and the CD-i findings below.

The rule this pays for is the one CLAUDE.md already states: read the
existing acquisitions directories before calling anything new.

**The CD-i website** (Jorg Kennis: kennisonline.com/cd-i/ 1999, then
www.icdia.org 2000, which also carried the OS-9 2.4 manuals by Microware's
permission).  Wayback holds `icdia.org/cdprosupport/files/os9/` WITH its
files (directory dated 09-Nov-2000): a Philips/OptImage CD-i developer-BBS
set, 1993-96, for 605 authoring players -- MediaMogul menu_edt fix, DV
plug-ins (dv053196, dv8025, dvworm), 605 tape modules (605exa), a PC
SyQuest descriptor (pch3), ddinits/startnet, Microware's NFS p2init, an ftp
man page, CD-i title helpers (cdi_mmpr, cdi_vol, cdirand).  Product- and
hardware-specific: OUT OF SCOPE.  Exceptions looked at: GED ("FREEware ...
distributed at will") is an MPEG-multiplex entry-point extractor for CD-i
DV authoring -- also out of scope; lftocr (1994) converts LF / CR+LF text
to OS-9 CR in place and the disk has no such converter -- a small
candidate, terms unstated; `tar' and `tar.txt' were listed but never
captured.  Fetched descriptions are in
`~/Developer/os9/Scraped/acquisitions-2026-09-14/icdia/`.

### The CD-i and 6809 groups, read (2026-09-14)

**rec.games.video.cd-i and its three small siblings: 12,306 unique messages,
ZERO software posts** (no uuencode, shar or Archive-name), about 57 that
mention OS-9 or CD-RTOS at all -- it is a games-and-players group.  The
site-wide CDRTOS search added 13 messages, none carrying software.

But it answers rdoggett's question -- could a CD-i player run this
collection? -- better than the professional-model evidence above, because
it says ANY player:

  * Andrew Davidson, Microware, 1995-07-25: "It's possible to launch an
    OS-9 shell from a CD on a CD-i player, assuming you have a terminal
    attached to the serial port. You don't need a hard disk."
  * 1997-09-11: "CD-i players all have an RS-232 port"; use Port 2 as the
    terminal (9600,N,8,1, a PC terminal program will do); the disc's
    startup program launches an application or spawns a shell; "you need
    to have your software environment on the CD-i disc"; anything written
    goes to memory only; Web-i was a CD-i player running as a web-browsing
    computer; a block device over the serial link to a PC's OS-9 partition
    is possible in theory but "you probably need a developer system and
    license from Microware".
  * David Oseas, Philips Media, 1996-02-05: the ROM holds the player shell
    and the OS-9 device drivers; patched drivers are routinely loaded from
    the disc into RAM at run time.

So a burned CD-i disc carrying these OSK modules, a startup that spawns a
shell, and a serial terminal is a plausible way to run the collection on
a consumer player.  The limits: 1 MB RAM base (programs run one at a
time; cio/csl/math must fit alongside), no writable storage (scores and
saves only to a RAM disk), a TV display the collection does not drive,
and Green Book disc mastering we have no tools for.  UNTESTED -- no
player here.

**The 6809 groups** (net.micro.6809 1,005 + comp.sys.m6809 6,627, both
matching the index; one net.micro.6809 page skipped in a network outage
is being re-fetched): 15 software posts touch OSK or the 68000, and 14 of
them were already in the 2026-09-11 material -- Wecker's and Omura's
shar, compress, Pete Lyall's AR, hdkit and the Kreider C library.  The
fifteenth, "AR for OS9/6809" (1988), is 6809-only.  Nothing new.

### The usenet-rewind pull is COMPLETE (2026-09-14)

Every group checked against the site's own index count, and all match:
the 14 OS-9 groups (comp.os.os9 17,803; comp.os.OS9 4 after the
case-variant folder fix), comp.sys.m68k 20,141, comp.sys.m68k.pc 297,
comp.sys.m68K 8, the four CD-i groups (rec.games.video.cd-i 12,261),
net.micro.6809 1,005, comp.sys.m6809 6,627, plus the OSK-only searches
(bit.listserv.coco 1,323; comp.sys.tandy 33; alt.sources 31;
comp.sys.atari.st 25 and .tech 3; comp.sources.misc 20) and CDRTOS
site-wide (13).  6,905 result pages, 166 MB, in
`~/Developer/os9/Scraped/usenet-rewind/` -- PRIVATE, author addresses
included; never commit it.  `pull.py` there is resumable; `mine.py`
finds posted and announced software.

Three pull.py fixes paid for on the way, all in its header: a
capitalised group needs its own folder on this case-insensitive disk; a
page that fails after retries is SKIPPED, not fatal (a twenty-minute
outage stopped a whole group); and a month window may not end after
today (HTTP 422).

What it yielded is recorded above: little new software, the CD-i and
MM/1 findings, four os9exec bugs, and the realisation that the collection
cannot assemble or link on the disk (see the Perl 4 work that followed).

