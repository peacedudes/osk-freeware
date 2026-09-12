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
| agrep 2.01 | `CSU/volume26/agrep-2.01/`; also MW 4310 | 1992 | non-profit only -- **Q1** |
| vttest | `CSU/volume7/vttest/` | 1986 | non-commercial -- **Q1** |
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
Measure first: which binaries need cio (run against an image without the
five runtime modules); every hardcoded `/h0/USR/GAMES/...` path; whether
the native tools expect `/dd/SYS/utmp`, group, password or smail.

### B7 -- games and screen toys                                         open
| prog | source | date | terms | port |
|---|---|---|---|---|
| phoon (Poskanzer) | `CSU/volume8/phoon.gz` | 1987 | permission granted | DONE (fc775046) -- numeric date, tws.c stands in for libtws |
| globe (Poskanzer) | `CSM/volume43/globe/part01.gz` | 1994 | permission granted | DONE (597b2a9e) -- built unchanged |
| atc | `NET2/games/atc` | 1990 | BSD | curses, lex/yacc, setitimer->alarm |
| canfield (+cfscores) | `NET2/games/canfield` | 1980 | BSD | canfield DONE (8c133d0b) -- curses; _tty/SIGTSTP/SIGTERM shimmed; cfscores companion open |
| trek (Allman) | `NET2/games/trek` | 1980 | BSD | sgtty/select bits |
| monop, wump, fish, arithmetic | `NET2/games/...` | 1980-90 | BSD | wump DONE (70fe4c6d), fish DONE (73cb6958), monop DONE (830dee5e) -- self-contained, getopt bundled, instructions embedded.  monop's board, properties and cards are .dat files #INCLUDED as C initialisers, so they had to be CR like source, not like data |
| bs (ESR battleships) | `CSG/volume8/bs/part01.gz` | 1989 | no notice | DONE (cee1197c) -- OSK curses arm shims beep/chtype/ungetch, cbreak parenthesised |
| scrabble | `CSG/volume6/scrabble/` | 1989 | redistribute in any manner | ASSESSED 2026-09-12, not yet built.  Wayne Christopher, Berkeley; "Permission is granted to modify and re-distribute this code in any manner".  18 files, 2,781 lines, curses.  Three obstacles, all known shapes: ~48 ANSI prototypes across eight .c files plus 29 in scrabble.h (the KNR flag will NOT do this -- see reversi); util.c wants gettimeofday, getrusage and getpwuid, none of which exist here, but all three are inside that one 144-line file and are shimmable; and DICT_FILE defaults to /usr/dict/words, which the author deliberately did not ship ("too large").  disk/GAMES/words is a CR-terminated 164KB one-word-per-line list already on the disk -- crypto, hang and wanderer read it -- so `-DDICT_FILE=\"/dd/GAMES/words\"' is the obvious pointing, and its own Makefile already parameterises that.  A focused afternoon, not a tail-of-session job |
| saa (Streets and Alleys) | `CSG/volume12/saa/` | 1991 | permission granted | DONE (d72a0cea) -- built unchanged with -DNON_ANSI_C |
| accordian | `CSG/volume15/accordian/` | 1992 | public domain | DONE (6a512987) -- curses solitaire; RANDOM->rand, popen/getpwuid dropped, win log local |
| mastrm | `CSG/volume2/mastrm.gz` | 1987 | public domain | DONE (0a75970f) -- system(clear) -> ANSI clrscr |
| hexa (hexagonal sokoban) | `ALT/volume93/Jan/930127.01.gz` | 1993 | no notice | DONE (c6aae0a7) -- 216-byte binary level maps in GAMES/HEXA |
| corewars | `CSG/volume6/corewars/` | 1989 | public domain | curses |
| castle | `CSG/volume8/castle/` | 1990 | public domain | ATTEMPTED 2026-09-11, parked.  Compiles clean (SIGILL/SEGV/TERM/FPE/BUS guarded in both the `signal()' calls and the `catch()' case labels; savetty/resetty shimmed; the `-DFILES' quote-hack replaced with literal paths; `sys/time.h' dropped).  Will NOT LINK: "non-remote data allocation exceeds 64k".  The globals in `INCLUDE/castle.h' are declared without `extern' and five .c files include it, so static data totals ~80K; `short'->`char' on the two graphics arrays made it WORSE (93844), so c68 is not common-merging the tentative definitions.  The fix is to extern-ise castle.h's globals with one definition per global in a single .c.  Terms fine (CSG no-notice basis).  Work is in the other session's scratch, not in the tree |
| othello3 / reversi | `CSG/volume12/othello3/`; `CSG/volume15/reversi/` | 1991-92 | free / GPL | othello3 DONE (77b95c01) as othello -- getchar->getch, LINES/COLS clash removed; reversi (2-part) still open |
| jotto, conn4 (Sicherman) | `CSG/volume11/jotto/`, `CSG/volume12/conn4/` | 1990-91 | no notice | conn4 DONE (39eb5990) as c4; jotto DONE (0a75970f) -- built-in word list |
| yahtzee2 | `CSG/volume8/yahtzee2/` | 1989 | no notice | one fork |
| rot2.2 ("software rot") | `CSG/volume1/rot22.gz` | 1987 | no notice | name clashes with CMDS/rot |
| flicker | `CSG/volume5/flicker.gz` | 1988 | no notice | LEFT OUT 2026-09-12, deliberately.  Gene H. Olson's ANSI teaser: `for(;;) write(1, buf, N*s)' of insert-line/delete-line escapes, forever.  No exit but Interrupt, no terminal restore, and the author's own README says "Enjoy, and be sensible.  (Use Interrupt to exit the program.)"  It would hang the capture harness and hand a reader a terminal to break out of.  Two files, extracted and read; nothing to build. |
| ASCII plasma | `ALT/volume93/Feb/930203.12.gz` | 1993 | no notice | VT100 |
| Toon 1.0, Juggle 1.0 | `ALT/volume94/May/940508.36-.40`; `ALT/volume95/Apr/950426.08.gz` | 1994-95 | GPL | curses, setitimer |
| rogue 5.3 clone (Stoehr) | `CSG/volume1/rogue/` | 1987 | not for profit -- **Q1** | curses, sgtty |
| gnugo, napoleon, adven2 | `CSG/volume6/gnugo/`, `CSG/volume17/napoleon/`, `CSG/volume11/adven2/` | 1989-93 | GPL/GPL/none | ASSESSED 2026-09-12.  **gnugo**: v06i019, GPL with COPYING, 34 members / 4,207 lines / 27 C files, no curses -- and TOP shipped BOTH an OS-9 source tree and a working OSK binary, so a reference build exists to check against.  The best next candidate.  **napoleon**: ASSESSED 2026-09-12, viable but not small.  Pete Chown 1992, GPL v1 or later, its own `copyright' file.  19 members, 4,391 lines.  The yacc question is settled -- the disk's `yacc' and `bison 1.19' both run, and no pre-generated parser ships, so lang.y must go through one of them.  Its Makefile offers `-DPURE_ANSI' for non-Unix hosts and adv.h:31 `#error's unless exactly one of PURE_ANSI and UNIX is defined; PURE_ANSI is right for us, because <termios.h> and <unistd.h> are inside the UNIX arm and neither exists here.  But the switch does NOT solve the real obstacle: 71 ANSI prototypes, unconditional, with no PROTO() indirection -- adv.h:76 onward is bare `extern void format(char *,...);' -- and Microware's cc is K&R.  Unlike scrabble there is no single file to shim; it is a tree-wide de-ANSIfication, and ansi2knr cannot do declarations.  A day's work, not an evening's.  **adven2**: FORTRAN (aamain.f, asetup.f, asubs.f, iors.f, split .xaa/.xab parts joined by combine.sh), no terms stated.  Out of scope for the C toolchain: it would need the RTF Fortran chain, which CLAUDE.md records as only partly working (`for' and `lnk' print the command they would run and stop).  Left alone |
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
| EFFO PD disks 100-123 (1993-95), forum disks 18 and 19 | EFFO material after what the pool has | not found |
| OS-9 Users Group disk library | user-group software | not found |
| CompuServe OS9 SIG library | names survive at lcurtisboyle.com: cawf, defrag, dskcat, hpdisp, spel68, aplrts, swtool, g261 | files not found |
| colorcomputerarchive.com (~150 OS-9 zips), archive.org `cdrom-coco-archive` | 6809 OS-9, some C | few opened |
| Microware archive, the rest | `os9/mw/*.tsv`: 127 OSK files the pool never fetched, the MM/1 tree (84), USERGROUPS, BENCHMARKS, FAQ, DOCS (incl. a 1994 chestnut.index) | listed, not all fetched |

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
