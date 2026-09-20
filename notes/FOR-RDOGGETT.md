# For rdoggett

Things that need YOU -- nothing else. Anything decided leaves this file the
same day. Numbers are cited from `notes/START-HERE-NEXT-SESSION.md` and stay
stable, so a gap means an answered question. The evidence for every item is
in the handoff under the same name; this file is the asking.
Updated 2026-09-20.

## Yours alone

**1. Nothing is pushed, and the pin waits on it.**
`.github/workflows/build-image.yml` now names the branch os9exec is actually
working on (`fix/scf-pd-eor`) rather than the released line, on your
instruction. That branch is 215 commits ahead of `github/master` and
unpushed, so CI cannot run until you push -- it never has. At tagging, freeze
the ref to the tip **commit**, taken at that moment.
*Four fixes we depend on are on no remote: `40facae` `d401ce2` `685a4c3`
`00fcec5`.*

**3. Nobody has tried this on real hardware.**
The guides say so plainly. If you know someone with a real system, that is
the paragraph to check.

**7. usenet-rewind: CANCELLED, access until 2026-10-14.**
Nothing needed. Nothing is lost either -- the archive stores full message
bodies and all 1.2 GB is on this machine, with MNews, Tass and Ptyman 1.3
already extracted. **The key stays** (`~/.config/usenet-rewind/os9`) with
`pull.py` and `mine.py` beside the archive, until access expires or we
publish, whichever comes first -- your call, 2026-09-20, in case something
turns up that wants one more fetch. Delete the key after that; it is the
only credential here.

## Decisions

**21. `cpp`: ship it?**
TOP's OS-9 build of the public-domain DECUS preprocessor works and writes
Microware's line markers. It shares a name with a utility of yours, and the
shadow-rule machinery handles that automatically now. **Recommend: ship it
as `cpp`.** Omega is settled and out.

**23. ispell: one speller, and not the one the disk recommends.**
Your source turns out to be the source of the shipped `CMDS/ispell`, so
tossing it would remove the only source for the binary that works.
`CMDS/ispell` and `CMDS/buildhash` agree with each other;
`REBUILT/ispell_rebuilt` works only with one pre-existing hash that nothing
here can reproduce, and given a freshly built one it reports NO misspellings
in text full of them. Your dictionary is the better of the two: 17,632 words
against 15,044. **Recommend:** keep `CMDS/ispell`, rebuild the hash from your
dictionary, ship your `dict.191` in `SRC/ispell`, retire `ispell_rebuilt`.
*If its source ships, the 1989 README grants permission to POST rather than a
licence, and `SOURCES.txt` should say exactly that.*

**24. Twelve "second build of" programs -- gone, or kept and explained?**
You asked of `vi_cio`: "we don't need both (are there others like this)??"
They are three different things -- our rebuilds kept beside a period binary
on purpose, a genuinely different implementation worth having, and plain
duplicates. **Recommend: keep the first two, drop the third**, which on that
reading is `emacs.mm1` alone.

**26. `pnmtosir`/`sirtopnm`: patch the 1991 bug, or preserve it?**
One loop bound in the reader -- `i < 1531` where the header is 1532 shorts --
so every colour plane comes back shifted two bytes. I predicted the exact
wrong colours before touching anything and the disk produces them; three
cases pin it. **But the loop is as the original has it**, so fixing it ships
a netpbm that differs from the archive. Ten minutes either way.

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

**18. `disk/` is hard-linked to a twin I cannot find.**
8,896 files have a link count of 2. Every generator writes in place, which
goes through to it; a write by rename would detach. I keep writing in place,
as they always have. If you ever find what the twin is and it should not be
tracking us, say so.

**19. The stray save file stays.**
`GAMES/HACK/PLAYGROUND/save/0tester` is committed, so every rebuild puts it
back, per your "don't overdo it". The harness bug that created it is fixed,
and rebuilding `osk-freeware.dd` is the last step of a session here now --
your `free` alias opens that same file.
