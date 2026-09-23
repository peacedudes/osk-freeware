# For rdoggett

Open questions only, two sentences each. Ask and I will explain any of them;
the detail lives in `notes/START-HERE-NEXT-SESSION.md` under the same number.
Updated 2026-09-23.

## Needs you

**1. Push os9exec, then pin `a4b338e`.**
Nothing is pushed, so CI has never run.  `a4b338e` carries today's four
fixes the new programs need (F$DatMod, Ev$Wait, /socket, zero-byte
F$SRqMem); MNews, nn, ttcp and BIND were verified against a build of it.

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
