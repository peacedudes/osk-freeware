# For rdoggett

Things that need YOU -- nothing else. Anything decided leaves this file the
same day. Numbers are cited from `notes/START-HERE-NEXT-SESSION.md` and stay
stable, so a gap means an answered question. The evidence for every item is
in the handoff under the same name; this file is the asking.
Updated 2026-09-21.

**Nothing new needs you.**  Answered 2026-09-22: 31 (no stand-in
`shell'; load yours from /h1/CMDS/shell, as SYS/login does), 32 (the EFFO
vi's helpers come off), 33 (bash patched).  Programs found and left out
are catalogued for readers in DOC/README-NOT-SHIPPED.

**Before that, nothing new needed you except item 31, and item 1 changed.** The night of
the 20th and the morning of the 21st went on exception reasons, harness
faults and tests, none of which is yours to decide: `panel-exceptions.psv'
is 65 rows with about 27 of them re-tested, seven programs came off the
untested list (17 to 10), the gate is green, the suite is **877 of 877
twice**, and `check_the_checks' catches 43 of 43. It is all in the handoff,
which now opens with the ORDER of what is left so no session has to ask.

**Item 1 gained a name to pin and a reason to ask before pinning** -- the
os9exec tip that night carried a flake its own author caught.

**Four items closed on your earlier answers** -- 21 (ship `cpp`), 23
(ispell), 24 (drop the plain duplicates) and 26 (patch the SIR reader).

## Yours alone

**1. Nothing is pushed, and the pin waits on it.**
`.github/workflows/build-image.yml` now names the branch os9exec is actually
working on (`fix/scf-pd-eor`) rather than the released line, on your
instruction. That branch is **253 commits** ahead of `github/master` and
unpushed, so CI cannot run until you push -- it never has. At tagging the
ref must be frozen to a **commit**, and the next paragraph says which:
NOT the tip.
*Four fixes we depend on are on no remote: `40facae` `d401ce2` `685a4c3`
`00fcec5`.*

**The commit to pin is `60d4b0a`, and ASK THEM before taking any other.**
This is not hypothetical and it caught one on its first outing. On the
evening of 2026-09-20 the tip was `d64163b` -- exactly what a freeze that
night would have taken -- and the os9exec session told me unprompted that
an idle-wait cap raised from one system tick to 50ms in that same range
made their own XOFF input test fail about one run in three. They have
since put the cap back and measured it: seventeen clean full-suite runs,
several with two suites running at once so the contention the failures
preferred was present, then green gates across the board. `60d4b0a` is
that correction, and it contains everything `d64163b` had.

**The tip has already moved past it** -- `c5cf21e` as of the morning of the
21st, two commits on -- which is the whole argument in one line: whatever is
at the top when you tag is not a thing either of us has tested.

The `-d` tracing fix we depend on is two commits below the tip and both
commits above it are independent of it, so the verification I did against
`d64163b` still describes `60d4b0a`. Ask them for the commit they want
named rather than taking whatever is at the top: a pin is forever in a
way a test run is not.

**3. Nobody has tried this on real hardware.**
The guides say so plainly. If you know someone with a real system, that is
the paragraph to check.

**7. usenet-rewind: CANCELLED, access until 2026-10-14.**
Nothing needed. Nothing is lost either -- the archive stores full message
bodies and all 1.2 GB is on this machine, with MNews, Tass and Ptyman 1.3
already extracted (shar postings are plain text and came through whole;
raw uuencoded ATTACHMENTS are stripped by the service, so those were never
obtainable through it at all -- one 1997 posting is affected and it is a
kernel file manager, out of scope). **The key stays** (`~/.config/usenet-rewind/os9`) with
`pull.py` and `mine.py` beside the archive, until access expires or we
publish, whichever comes first -- your call, 2026-09-20, in case something
turns up that wants one more fetch. Delete the key after that; it is the
only credential here.

## Decisions

**28. Should "name what the reader HAS" reach the shipped READMEs?**
The gate covers `DOC/INDEX`, `howto.psv` and the card sheets. Four
`DOC/README-*` files use the phrasing and all four read as fact rather than
discouragement; two are about Microware's own files being deliberately
absent, which is the respectful thing to say. Widening the FILE LIST is one
line and safe; widening the PATTERNS would flag seven captions that are
right. **Recommend: widen the list, leave the patterns.**

**29. Your username was on six published cards; what stays is yours to say.**
All nine occurrences are gone and a gate with a breaker keeps them gone. What
I kept: `Robert Doggett` in `zot.1`, `zot.c`, `qt.c`, `snap/main.c` and
`fgrep.c`, where the files' own headers record who ported them -- the
archive's line, not ours -- the same in a period disk image, "Robert Doggett
asked Allan at Microware" in `SOURCES.txt`, and the os9exec URL. Each is one
line in the gate's allowed list if you want it gone.
*You corrected me for writing those up as authorship; they are port credits,
and the disk credits the original authors.*

**30. `fpu`: I acted, and you can reverse it.**
The `fpu` we shipped was not the copy its grant travels with, and `fpu040`
had no grant at all -- both came from a terminal program's archive carrying
no document. I swapped `fpu` for the granted copy (12,724 bytes, md5
`3f5b0760`, also the newer module) and removed `fpu040`. If you read
"Permission to distribute FPU" as covering the module generally rather than
that copy, `git revert` puts `fpu040` back.
*The other five runtime modules rest on Allan's permission, which names the
modules rather than copies, and are fine.*

## Not a question, but you should know

**19. The stray save file stays.**
`GAMES/HACK/PLAYGROUND/save/0tester` is committed, so every rebuild puts it
back, per your "don't overdo it". The harness bug that created it is fixed,
and rebuilding `osk-freeware.dd` is the last step of a session here now --
your `free` alias opens that same file.
