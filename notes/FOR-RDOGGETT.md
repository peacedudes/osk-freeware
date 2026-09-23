# For rdoggett

Open questions only, two sentences each. Ask and I will explain any of them;
the detail lives in `notes/START-HERE-NEXT-SESSION.md` under the same number.
Updated 2026-09-23 (evening).

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

## No action, just so you know

**3.** Nobody has tried this on real hardware, and the guides say so.

**7.** usenet-rewind is cancelled; access and the key last until 2026-10-14,
and nothing is lost either way.

**19.** The stray `GAMES/HACK/PLAYGROUND/save/0tester` stays, per your
"don't overdo it".

**Done 2026-09-23:** 36 settled (WebAssembly build committed in docs/try, disk.gz built by CI); 28 done (five READMEs reworded, gate widened).

**Answered 2026-09-23 (37):** ship `UAC_view`, leave `checksoa` out, ship
`ttcp`/`nslookup`/`nsquery` with the ISP static link recorded.
Earlier: 29-35.
