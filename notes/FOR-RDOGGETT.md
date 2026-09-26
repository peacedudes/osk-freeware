# For rdoggett

Open questions only, two sentences each. Ask and I will explain any of them;
the detail of items before 45 lives in `notes/HISTORY-2026-09.md` under
the same number.
Updated 2026-09-26.

## Needs you

**1. Merge and publish -- your call, when you are ready.**  os9exec is
pushed (release-v4.1.0, f2954f3) and this collection is verified on it:
suite 1019/1019 twice, play-tests 151/151, CI green on Linux.  What is
left is yours: merging this branch to main (a push to main publishes the
catalogue to Pages) and making anything public.  When os9exec sends its
merge commit, I pin CI to it.

**53. A new, empty /h1 in the browser, to keep things onto?**  Your idea
(2026-09-26): with no OS-9 of your own, pick programs from the collection
and save them as a disk of their own.  The parts exist -- `keep' copies a
program with what it needs; the page already attaches, keeps and saves an
/h1 image; os9exec's `mount -k' makes a blank RBF image.  Missing: one
"New empty disk as /h1" button (size, volume name, the standard CMDS/SYS
directories), and the catalogue's picks producing one `keep' line.  Say
yes and I build it; it adds a feature to the public page.

## No action, just so you know

**GitHub:** https://github.com/peacedudes/osk-freeware -- PRIVATE, created
2026-09-24.  The working branch is pushed and is the default there; `main'
is not, because a push to main starts CI, which needs os9exec's branch
published first.  History was rewritten before the push: the utilities
from your own archives and the oversized test transcripts are gone from
every commit and every message.  A pre-rewrite mirror is at
~/Developer/os9/Scraped/osk-freeware-git-backup-2026-09-24 -- delete it
when you are satisfied.


**Source added 2026-09-24:** 35 programs that shipped without source now
have it, each from its own archive (SOURCES.txt, "SOURCE ADDED").  One
judgement you may want to know about: ADL and hotel say to distribute
the sources unmodified / verbatim, and their text was converted LF to
CR like every text file here, nothing else changed.  Say if you would
rather they shipped as the original postings.

**Answered 2026-09-24, evening:** 45-51, all yes; applied the same evening
(SOURCES.txt, "PATCHED 2026-09-24"; each card says what changed).  51
keeps your rule -- group 0 is the super group -- which the old code did
not test: it looked at the high byte of the user number.

**Answered 2026-09-24:** 38 (harnesses run as tester -- done); 39 (both
gccs ship with source); 40 (k37 net replaces k35c, built from its own
source; K5JB's mailer is `bm', the Boyer-Moore grep is `bmg'); 41 (tass
ships, for a pre-2 MNews system; MNews pre-2 ships whole in SRC); 42
(the fonts were made with the disk's own METAFONT and ship; Vprint and
pc2os9 stay out); 44 (Notesfiles stays out).  Also: cards for the
programs left out; notes on every card we changed; programs useful on a
real system but untestable here now ship, marked untested; the utilities
from your own archives are gone from disk, docs, tools and notes, and
will be gone from history before the private GitHub push.


**3.** Nobody has tried this on real hardware, and the guides say so.

**43.** This Mac's data volume was at 99% (1 GB free) tonight; I cleared
20 GB of my own scratch images, but the drive itself is nearly full.

**7.** usenet-rewind is cancelled; access and the key last until 2026-10-14,
and nothing is lost either way.

**19.** The stray `GAMES/HACK/PLAYGROUND/save/0tester` stays, per your
"don't overdo it".

**Done 2026-09-25:** 52 -- collect2's entry test patched in all three
1991 builds (tools/patch_collect_entry.py; SOURCES "PATCHED"); collect.cases
failed on the old binaries and passes on the new.

**Done 2026-09-23:** 36 settled (WebAssembly build committed in docs/try, disk.gz built by CI); 28 done (five READMEs reworded, gate widened).

**Answered 2026-09-23 (37):** ship `UAC_view`, leave `checksoa` out, ship
`ttcp`/`nslookup`/`nsquery` with the ISP static link recorded.
Earlier: 29-35.
