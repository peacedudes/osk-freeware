# For rdoggett

Things that need YOU -- nothing else. Anything decided leaves this file the
same day. Numbers are cited from `notes/START-HERE-NEXT-SESSION.md` and stay
stable, so a gap means an answered question. The evidence for every item is
in the handoff under the same name; this file is the asking.
Updated 2026-09-22, after your letter to Allan.

**Three need you: 1 (push, then pin), 36 (how the browser page gets onto
Pages) and 28 (a wording question, one line either way).**  Everything else
is answered.

**Closed since you last read this:** 29 (your 1988 lines in the archives'
own files stay; the SOURCES line naming you and Allan is gone, and the gate
now catches the name, not just the username), 30 (`fpu' -- below), 31 (load
your shell from /h1), 32 (the EFFO vi's helpers came off), 33 (bash
patched), 34 (the `t' stub came off), 35 (`load' deleted, not just
withheld).  Programs found and left out are catalogued for readers in
DOC/README-NOT-SHIPPED.

## What backs the three claims in your letter

  * **"no Microware code apart from the runtime modules you ok'd, as well
    as fpu ... unchanged".**  Checked 2026-09-22: exactly five modules ship
    (cio, csl, csl020, math, math881), plus `fpu' -- 12,724 bytes, md5
    3f5b0760, the copy its own notice travels with, with DOC/fpu.doc beside
    it.  `fpu040' and `cio020' are not on the disk, and no Microware
    utility, header, library or compiler is.  **That closes item 30: the
    granted copy is what ships, unchanged.**  The one program NAMED for a
    Microware utility -- the clean-room `load' the os9exec project wrote --
    was deleted on your word, so nothing here is even a rewrite of theirs.
    DOC/ORIGINS now carries a row for every file under CMDS.
  * **"making sure things run and the sources compile".**  Every program
    has a card taken by running it; the suite is 875 of 875, twice, on a
    fresh image; 573 of the 771 programs whose source is here are built by
    a recipe.  Mining pass 1 is closing the gaps in that: `gawk' shipped
    with the WRONG version's source (2.00 Beta against a 2.11 binary) until
    today, and `proff' could not be rebuilt at all until `ltb' and its
    symbol file came back.
  * **"tried in a browser with no download or setup".**  The page runs the
    whole disk, and every card knows whether it can run there and on what:
    877 on the disk alone, 45 needing your own OS-9 attached as /h1, 37
    that need hardware and say so instead of offering a button.

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

**36. The browser page: commit the build, or build it in CI?**
Your letter settles that it goes on GitHub with the collection's
documentation, so only HOW is left.  EITHER commit the four built files into
docs/try -- disk.gz is ~49 MB, inside GitHub's 100 MB, rebuilt only at
releases -- OR let the Pages workflow build them, which adds an Emscripten
setup action to CI, a new dependency.  **Recommend: commit the build.**  Say
which and I will do it; the Try It links on the cards appear the moment
docs/try/index.html exists.


**28. Should "name what the reader HAS" reach the shipped READMEs?**
The gate covers `DOC/INDEX`, `howto.psv` and the card sheets. Four
`DOC/README-*` files use the phrasing and all four read as fact rather than
discouragement; two are about Microware's own files being deliberately
absent, which is the respectful thing to say. Widening the FILE LIST is one
line and safe; widening the PATTERNS would flag seven captions that are
right. **Recommend: widen the list, leave the patterns.**

## Not a question, but you should know

**19. The stray save file stays.**
`GAMES/HACK/PLAYGROUND/save/0tester` is committed, so every rebuild puts it
back, per your "don't overdo it". The harness bug that created it is fixed,
and rebuilding `osk-freeware.dd` is the last step of a session here now --
your `free` alias opens that same file.
