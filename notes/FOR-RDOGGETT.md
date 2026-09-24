# For rdoggett

Open questions only, two sentences each. Ask and I will explain any of them;
the detail lives in `notes/START-HERE-NEXT-SESSION.md` under the same number.
Updated 2026-09-23 (night).

## Needs you

**1. Push os9exec, then pin `d992145`.**
Nothing is pushed, so CI has never run.  `d992145' is the tip the os9exec
session gated and named safe (2026-09-23); the whole suite passes on a
fresh image built with it, 912 of 912, twice.  docs/try is built from it.

**38. Run the harnesses as `tester', not `su'?**
Every card, case and probe runs as super-user, which RBF lets past
permission checks.  Recommend: switch at the final verification pass
(one full re-shoot and suite run), not piecemeal.  Measured: every case
family as `tester' passes 169 of 173; the four are the super-user's by
design (inews admin, uupoll's private spool) or combine's output having no
permissions at all, now said on its card.  Running as tester has since
found one real multi-user fault su hid: nn's GROUPS file is owner-only
after `nnmaster -I' (README-NEWS now says `attr -pr' it).

**39. Two more gccs with full source -- ship either?**
gcc 1.37.1 (CERN, 1991, binaries + source) and gcc 2.7.2 (1995-97, 21 MB
source + binaries) sit in the pool; the disk has gcc 1.39 and 2.5.6
binaries with no source.  Recommend: neither -- size and era, and gcc
needs cio either way.

**40. K5JB k37 source for `net`?**  The shipped `net' is K5JB k35c with
no source; k37 (two revisions later, GPL-ish per-file grants) builds
clean and runs the same.  Recommend: ship k37's tree in SRC labelled
"nearest available source", keep the k35c binary; K5JB's own `bm' mailer
stays out (its name is taken by the Boyer-Moore grep).

**41. tass -- a second MNews?**  tass builds and draws, but reads the
1993 MNews "pre-2" spool format, not the 1990 one that ships with nn;
shipping it working means a second news system.  Recommend: leave out.

**42. Small ones, recommend no to all three:** 22 TeX font metrics with
no bitmaps to print them (TeX could typeset, nothing could print);
Vprint, whose only copy is a 1997 Linux rewrite; `pc2os9', which
`toos9' already covers.

## No action, just so you know

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
