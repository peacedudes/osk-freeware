# For rdoggett

Open questions only, two sentences each. Ask and I will explain any of them;
the detail lives in `notes/START-HERE-NEXT-SESSION.md` under the same number.
Updated 2026-09-23.

## Needs you

**1. Push os9exec, then pin commit `60d4b0a`.**
Nothing is pushed, so CI has never run, and `60d4b0a` is the commit we
actually tested -- ask them before taking any other, because the tip has
already moved past it twice.

**36. The browser page: commit the build, or build it in CI?**
Committing puts four files in `docs/try` (disk.gz is ~49 MB, rebuilt only at
releases); the alternative adds an Emscripten setup action to CI.
**Recommend: commit the build.**

**28. Should "name what the reader HAS" reach the shipped READMEs?**
The gate covers `DOC/INDEX`, `howto.psv` and the card sheets; four
`DOC/README-*` files use the phrasing and all four read as fact.
**Recommend: widen the file list, leave the patterns alone.**

## No action, just so you know

**3.** Nobody has tried this on real hardware, and the guides say so.

**7.** usenet-rewind is cancelled; access and the key last until 2026-10-14,
and nothing is lost either way.

**19.** The stray `GAMES/HACK/PLAYGROUND/save/0tester` stays, per your
"don't overdo it".

**Answered 2026-09-23 (37):** ship `UAC_view`, leave `checksoa` out, ship
`ttcp`/`nslookup`/`nsquery` with the ISP static link recorded.
Earlier: 29-35.
