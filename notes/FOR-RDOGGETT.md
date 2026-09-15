# For rdoggett

Open questions only. Nothing here is decided. Updated 2026-09-14 (late).

## Yours alone -- nothing I can do about these

1. **Nothing is pushed, tagged or merged.** The branch has never left this
   machine; the CI pin is an old os9exec commit and has never run.
   **Before a release, that pin MUST move past an os9exec fix that is not
   in yet** (2026-09-13): the Linux build of os9exec renames every file
   starting with `.' on an RBF image, and CI builds the image on Ubuntu --
   so a CI-built image would carry `.bashrc', `.newsrc' and `.ELM' under
   wrong names.  Fixed in os9exec **4d26520** (fix/scf-pd-eor, not pushed
   yet); the CI pin must be at or past it.  The handoff has the detail.

   **That branch now also carries a CPU fix, and the pin should take it
   too** (2026-09-14): NEG and NBCD never set the 68000's X flag, so
   Microware's software doubles came out wrong -- 1.0-1.0 was -2^-20.
   209b35c, reviewed by the os9exec session, with its tests at d56b1bd,
   the branch tip.  The image a CI build writes is not affected (tar
   extracts no floating point), but every figure a program prints under
   an older os9exec is, and this repo's cases, cards and
   DOC/README-FLOATINGPOINT are now written against the fixed one.
   `notes/os9exec-bugs/X-FLAG.md` has it.  The pin today is 261b4b6.

3. **Nobody has tried this on real hardware.** The guides say so plainly.
   If you know someone with a real system, that is the paragraph to check.

7. **Cancel usenet-rewind before it renews, about 2026-10-13, and delete
   the key.**  You bought one month of Researcher on 2026-09-13 for the
   OS-9 newsgroup pull.  Cancelling happens on their site, in your account.
   The key is `~/.config/usenet-rewind/os9`; once the pull is verified a
   session can delete that file for you if you say so.

18. **`disk/` is hard-linked to a second copy I cannot find, and my edits
   reach it.**  8,896 of the 9,927 files under `disk/` have a link count of
   2.  `find` over your home (skipping `~/mine`, `~/Library`, `~/.Trash`) finds
   no other name, so the twin is in one of those or on another volume.
   Every in-place write here goes through to it: tonight that was
   `DOC/INDEX`, `DOC/DEPENDS`, `DOC/CATEGORIES` and `CMDS/GAMES/monop`.  A
   write by rename does the opposite and breaks the link -- `CMDS/rsconvert`
   was installed that way, so the twin keeps the old one.  What is the
   twin, and should edits reach it?  Until you say, I keep writing in place,
   as every generator here always has; rsconvert is the one file detached.

## Licence and authorship questions the card-terms pass turned up (2026-09-14)

Every card must now state its terms, so every program's source was read for
them. Most answer plainly. These do not, and each is yours to decide -- nothing
has been removed or rebuilt.  All are quoted from the files, and each file and
line is recorded in `tools/terms.psv` or the handoff.

8. **`time` and `timid` meet the rule you set for utilities written at
   Microware.**  `SRC/hc_utils/time.c`'s revision history is `rfd` twice
   ("Created rfd 08-15-85"); `timid.c` says "Cloned from sys.c rfd 85/02/02",
   and sys.c is already on the removed list.  Both shipped binaries are built
   from those sources (recipes `time` and `timid`; the strings match).
   SOURCES.txt's own test -- "grep the edition-history rows for the
   initials" -- says remove them, source and binary, with their INDEX,
   ORIGINS, categories, help.psv, devtools card and bench.cases entries.
   Recommended; not done, because removing a program is your call.
   (`DOC/time/time.doc` is David J. Partington's submission of a DIFFERENT
   TIME program, and would go or stay separately.)

9. **`deton`, `sysid`, `sysmax`, `sysmin`** sit in the same `SRC/hc_utils`
   and look like system utilities, but carry no revision history and no author
   line, so the test above cannot catch them.  Are they yours?

10. **Explicit restrictions on programs that ship:**
   - `greed` -- "Please don't redistribute this." (Matthew T. Day, greed.c).
   - `travesty` -- Bernstein's grant ran "Until January 1, 1994" and says the
     rights "are automatically revoked on January 1, 1994".
   - `sysmon` -- its header calls the source "the proprietary confidential
     property of MAX PLANCK INSTITUTE KERNPHYSIK HEIDELBERG ... distribution in
     any form ... is prohibited", then the author writes "I have decided to
     distribute the source code to everybody on request !"
   - `vi` (SRC/effo_vi) -- "originates from the sources of vi running under
     the XENIX operating system", adapted for OS-9; nobody grants anything.
   - `puzzle15`, `puz15`, `udate`, `uwho` -- their authors allow unmodified
     copies only, and what ships are OS-9 builds.
   The utime.c rule ("if there is any question about it we have to exclude.
   Don't delete") would take these out of the build; that is your ruling to
   apply or not.

11. **`break` is a disassembly.**  `SRC/forum5/break.a` is headed
   "Disassembled 1987 by L.Zeller" of "object code at disassembly time", and
   the program "invokes the system level debugger".  If what was disassembled
   is Microware's own `break`, this is Microware code in source form, which
   the Microware-source screen does not catch because no notice survived.

12. **Programs that ship with no grant at all.**  Blars UUCP's uupoll and uux,
   the smail five, the twelve Dhrystone builds, sterm, the six smallutils
   programs, and about 120 more from the source-tree reading, each recorded on
   its card as "No copyright or licence statement".  The utime.c rule applies
   to such files; the question is whether it applies to programs that have
   shipped all along.

13. **`make` links the `utime.c` your ruling keeps out of the build.**  The
   ruling (2026-09-11, in PLAN-acquisitions): "`utime.c', which has a bare
   copyright and NO grant, stays out of the build".  Three utime.c files are
   on the disk; only one has a copyright line at all --
   `SRC/eff_make/utime.c`, whose whole notice is "Copyright (c) 1988 by
   Michael Hoffmann, Muenchen" -- and `tools/rebuild/recipes.psv` builds
   `CMDS/make` from `make.c parse.c stat.c tstring.c utime.c` in that tree.
   (blarslib's and ELM's OSK copies carry no copyright line.)  The ruling
   does not name its tree, so this is the likeliest match, not a proven one.
   Options: rebuild make with a utime() of the collection's own, as the
   perl port did for pipe(); leave it; or say the ruling meant another file.
   Asked in conversation as "we did include utime.c, right?" -- and the
   answer is yes, in make.

14. **More from the last research pass, each checked against the binary:**
   - `dclock` and `colortest` ship, but SOURCES.txt (G-Windows section,
     line ~2043) says both "were NOT taken, because adding a new program on
     unstated terms is a different question".  dclock says only "Copyright
     1996 by High-G Software."; colortest states nothing.
   - `cyberwar`, `puzzle`, `scriptmaster` -- Stephen Carville copyrights with
     no distribution terms; SOURCES.txt already marks them "FLAGGED FOR
     REVIEW, not settled".
   - `backgammon`, `teachgammon`, `cribbage` -- "Copyright (c) 1980 Regents
     of the University of California.  All rights reserved." and no grant in
     what ships.
   - `ub68020demo` -- its demo terms want "ALL of the files ... kept intact",
     and CMDS/archives holds UB_68000.LZH but not a UB_68020 archive.

15. **The last research pass found four more, each checked against its file:**
   - **RCS** (`ci`, `co`, `rcs`, `rcsdiff`, `rcsident`, `rcsmerge`, `rlog`,
     and `SRC/rcs`) -- `SRC/rcs/READ_ME` is Purdue's non-disclosure form:
     "RCS will be used internally only" and "RCS will not be distributed in
     any form or by any means without prior written permission by the
     author, Walter Tichy."
   - **SEDT** (`e`, `new_e`) -- "Sedt binaries are being made available for
     customers and Digital internal use on the condition that ... no
     modifications are made to the program" (EFFO forum 11, sedt.doc).
   - **`btree`, `isam`** -- btree.doc: no longer public domain, "sondern wird
     gegen einen 'modesten' Betrag ($65 ?) verkauft"; contact the author.
   - **The collection's own programs** -- `keep`, `kept`, `unkeep`, `about`,
     and os9exec's `load` -- state no licence anywhere; the repository's
     LICENSE grant covers `tools/`, not `disk/`.  What should their cards say?

16. **Eight programs' documentation directories hold another program's
   manual, and none of those other programs is on the disk.**  Each card
   points a reader at the wrong document:
   - `DOC/bm/bm.doc` -- "User Manual for BM, Bdale's MS-Dos Mailer";
     `bm` is a Boyer-Moore grep.
   - `DOC/dump/dump.1` -- terminfo's "dump \- Print the contents of a
     compiled terminfo file"; `dump` is a file and module dumper.
   - `DOC/join/Join.doc`, `DOC/uniq/Uniq.doc` -- Gregorie's join and
     `drop`; the binaries are GNU textutils join and a different uniq.
   - `DOC/whoami/whoami.man` -- UUCP's whoami page; the binary is GNU's.
   - `DOC/tail/tail.doc` -- Eric Williams' tail; the binary is DESIGNA VLT's
     (both happen to take `-l=`).
   - `DOC/screen/screen.doc` -- "Microware Screen Control Package", a manual
     for Microware's curses package, beside the README of `screen`, which is
     Screens.  Besides being misfiled it is Microware's own document, and the
     Microware screen (tools/screen_microware.py) only looks at disk/SRC.
   - `DOC/m4/readme` -- the readme of a different, public-domain m4 ("This
     code *is* PD"); `m4` is GNU m4 0.50.
   - (Not misfiled, but for another version: `DOC/ckermit/ckermit.doc`
     documents C-Kermit 4E(068) of 1988, the binary is 5A(190); and
     `DOC/less/less.man` is version 330's manual, the binary is less 290.)
   Options: remove them (they document nothing that ships); keep them under
   a name that no card claims; or leave them.  Recommended: remove, since
   git keeps them -- but it is the disk's contents, so it is yours.

17. **`k`, `xy` and `z` ship as binaries, and their licence ties
   redistribution to source.**  Tim Kientzle's notice (the same header in
   every ft*.c of TELECOM/xyz.lzh): "Redistribution in source or binary form
   is permitted only under the following conditions" -- among them, code
   received "as a part of an application program ... may only be
   redistributed with the complete source of that program", and otherwise
   not "without explicit written permission from Tim Kientzle".  The disk
   ships the three binaries without that source.  Ship the source beside
   them, or decide otherwise.
