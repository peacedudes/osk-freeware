# For rdoggett

Open questions only, two sentences each. Ask and I will explain any of them;
the detail lives in `notes/START-HERE-NEXT-SESSION.md` under the same number.
Updated 2026-09-24 (early morning).

## Needs you

**1. Push os9exec, then pin `e2c7f7b'.**
It was `d992145'; `e2c7f7b' (2026-09-24) adds the two fixes boa and
whetstone need -- SS_Ready on a listening socket, and clock() counting a
process's own ticks -- and the os9exec session gated it.  The full suite
on it, as tester, is the last step before this collection's commit.

**45. Patch elm's user check (one instruction)?**  As any user but the
super-user, elm answers "You have no password entry!": it compares the
password file's user number with getuid(), which on OS-9 is the whole
group.user word, so the two never match.  tools/patch_elm_uid.py makes it
compare the whole word (6 bytes at 0x18738, CRC recomputed; it refuses any
other elm); tester's home files for it are staged.  Recommend: yes.

## No action, just so you know

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

**Done 2026-09-23:** 36 settled (WebAssembly build committed in docs/try, disk.gz built by CI); 28 done (five READMEs reworded, gate widened).

**Answered 2026-09-23 (37):** ship `UAC_view`, leave `checksoa` out, ship
`ttcp`/`nslookup`/`nsquery` with the ISP static link recorded.
Earlier: 29-35.
