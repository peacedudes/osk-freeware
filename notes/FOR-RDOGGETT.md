# For rdoggett

Things that need YOU to decide or direct -- nothing else.  Nothing here is
decided; anything that gets decided leaves this file the same day.  The item
numbers are cited from notes/START-HERE-NEXT-SESSION.md, so they stay stable
and the gaps are deliberate: a missing number is an answered question.
Updated 2026-09-18.

**Your notes of 2026-09-18 cleared eleven of these** -- 8, 9, 10, 11, 12, 13,
14, 15, 16, 19 and 22 are done and gone from this file, along with the
removals and rebuilds they called for.  The commits say what each one did;
`git log --since=2026-09-18` is the list.  Four questions survive, with more
known about them than before, and one is new.

## Yours alone -- nothing I can do about these

1. **Nothing is pushed, tagged or merged, and the CI pin must move first.**
   The branch has never left this machine and the workflow has never run.
   `.github/workflows/build-image.yml` pins os9exec at 261b4b6; before a
   release it needs to be at or past **40facae** -- Linux renaming every
   dot-file on an RBF image (a CI-built image would carry `.bashrc` and
   `.newsrc` under wrong names), the 68000 X flag, two RBF update paths
   losing each other's writes, and F$Alarm.  os9exec's tip today is
   **e4ffa20**, which is well past all four.  The detail is in the handoff,
   PLAN.md, ROADMAP-freeware.md and notes/os9exec-bugs/X-FLAG.md; what is
   yours is pushing, tagging and moving the pin.

3. **Nobody has tried this on real hardware.** The guides say so plainly.
   If you know someone with a real system, that is the paragraph to check.

7. **usenet-rewind: CANCEL IT.  The pull is finished.**  Nine more groups
   came down on 2026-09-18 and every one matches the site's own index --
   fj.sys.x68000 (4,482), comp.sources.unix (2,817), comp.sources.games
   (1,987), comp.sources.misc (6,165), comp.sources.reviewed (276),
   mod.sources (798), net.sources (6,437), fj.sources (2,132) and
   alt.sources (15,923).  That is ~41,000 messages on top of the OS-9
   groups, 1.2 GB, and it closes every "no mirror found" row in the
   acquisitions recovery table.  Nothing is left to fetch.
   Cancelling happens on their site, in your account.  The key is
   `~/.config/usenet-rewind/os9`; say the word and I will delete it.

   The message you sent was **utree 3.03b-um** -- Peter Klingebiel's
   screen-oriented file manager, a portable Unix xtree, all eight parts
   pulled.  Its terms allow non-commercial redistribution, which is the
   shape you already ruled on, and the disk has no full-screen file manager
   at all, so it is a candidate: `notes/PLAN-acquisitions.md`.

## Decisions

17. **`k`, `xy` and `z` are the three affected** -- you asked which.  They
   are Tim Kientzle's xmodem, ymodem and zmodem file-transfer programs, in
   CMDS and CMDS/COMMS.  His notice, the same header in every `ft*.c` of
   TELECOM/xyz.lzh, permits redistribution "in source or binary form ...
   only under the following conditions", and one of them is that code
   received as part of an application "may only be redistributed with the
   complete source of that program".  The disk ships the three binaries and
   not that source.  The source IS in the pool archive, so the choice is:
   ship it beside them, or drop the three.  Ship it and the condition is
   met; either way it is a content decision.

20. **The GPL binaries still have no source, and there is now a real lead.**
   CMDS/GCC139 (gcc 1.39, g++ pass 1.37.1), CMDS/GCC2 (gpp/cc1plus 1.40.3,
   gcc2 2.5.6, cc2plus 2.5.8) and CMDS/TEXCMDS/dvips (dvipsk 5.495b) ship
   without it.

   The usenet pull turned up **GCC 1.37 ported to OS-9/68000** --
   comp.sources.misc v13i005..v13i011, May 1990, Mr. Seyama's port posted by
   NIIMI Makoto as diffs against stock GCC 1.37 with English documentation.
   Saved to `Scraped/usenet-rewind/extracted/gcc137-osk/`.  It is the first
   OS-9 GCC source this project has found anywhere.  It is also not the
   version we ship and **part 2 of 7 is missing from the archive**, so it
   does not close the question -- it just makes "fetch the near matches" a
   real option rather than a hope.  Keep the binaries, fetch what can be
   fetched, or remove them?

   **The other half of your question is answered and needs nothing from
   you.**  "Do we need them all, or mostly just the latest (are they
   backward compatible)?  How do we advise people which to choose?"
   DOC/README-GCC now opens with that: take GCC2 (2.5.6) unless the machine
   is short of memory, because GCC139 compiles C in about half the space
   (563 KB of passes against 1085 KB, measured), and 1.39's C++ is 1.37.1 --
   no templates.  Code 1.39 compiles, 2.5.6 compiles; not the reverse.  They
   cannot both be installed, so it is a real choice, and the file now makes
   it for the reader.

21. **omega: we cannot find out what was modified, and that is the answer.**
   You asked.  TOP shipped omega as a BINARY and its data files -- no source
   anywhere in the release -- and the binary announces itself as stock
   "omega version 0.71 (beta)" with no porter's credit in it.  So the only
   modification anyone can point to is that it is an OS-9/68K module, and
   whether anything in the game changed cannot be established without source
   to compare.  Brothers's licence allows free copying but not distributing
   modifications without his consent.  Your call, with that in hand.

   **`cpp` is the other half of 21 and is still open.**  TOP's OS-9 build of
   the public-domain DECUS preprocessor works -- macros, #if, local includes
   -- and writes Microware's `#P`/`#5` line markers, because it was built to
   replace Microware's own `cpp` pass.  My recommendation is now firmer than
   before: ship it, but NOT under the name `cpp`.  DOC/README-NAMES (new
   today) is about exactly this hazard -- twenty programs here already carry
   the name of a utility the reader owns, and a resident module answers by
   name whatever path you type, so a `cpp` of ours could quietly become the
   one their `cc` finds.  `dcpp` or `cpp.decus` costs nothing and cannot do
   that.

23. **ispell: you said you would send me the source you have.**  Until then:
   CMDS/ispell faults at its first dictionary lookup and is a different
   edition from everything else here, and REBUILT/ispell_rebuilt -- built
   from SRC/ispell, the edition DOC/ispell and LIB/ispell.hash belong to --
   works.  When your source arrives I will see whether it matches the
   shipped binary, and if it does the same treatment as `compress` applies:
   build it, put it in CMDS, drop the twin.

24. **Twelve more programs are "a second build of" something already here,
   and your "we don't need both" would remove them.**  You asked, of
   `vi_cio`: *"we don't need both (are there others like this)??"*  Measured
   from DOC/INDEX, which describes each of these as another build of a
   program on this disk:

       compress_rebuilt (gone today)   diff_1.1        emacs.mm1
       ggrep                           gtar            liborder.os9
       m4_0.5                          sed_1.06        xlharc
       dhry (eleven Dhrystone builds)  vi_1.0          lharcs

   Three kinds are mixed in there, and they are not the same question.
   Some are OUR rebuilds kept beside a period binary on purpose
   (`vi_1.0`, `liborder.os9`); some are a second implementation worth
   having (`ggrep` beside `grep`, `compr` beside `compress`); and some are
   just another copy (`emacs.mm1` is MicroEMACS 4.00 built for an MM/1 --
   the same editor as `emacs`).  I removed `touchtype` and `vi_cio` today
   because each was a duplicate AND the worse of the pair.  Do you want the
   rest gone, or the convention kept and explained?

## Not a question any more, but you should know

18. **`disk/` is hard-linked to a second copy and my edits reach it.**  You
   said you are not qualified to answer, which is fair -- so I will stop
   asking and say what I do.  8,896 of the files under `disk/` have a link
   count of 2 and the twin is not findable under your home.  Every generator
   here writes in place, which goes through to it; a write by rename detaches
   instead.  I keep writing in place, as they always have.  If you ever find
   what the twin is and it should NOT be tracking us, say so and the
   generators can be made to write by rename.

19. **The stray save file on your image**: you said *"I don't mind if you
   left scores on the freeware disk image files.  don't overdo it"*, so
   `GAMES/HACK/PLAYGROUND/save/0tester` stays.  The harness bug that put it
   there is fixed and no harness has touched your image since.

   Worth knowing: **your `osk-freeware.dd` was built 2026-09-15 at 07:58**
   -- that is sector 0's own creation date, not the file's mtime -- so it
   predates `westley` (committed 21:22 that day) and everything since.  That
   is why westley looked missing to you.  Rebuild it when convenient:
   `OS9EXEC_DIR=~/Developer/os9/os9exec tools/mkimage.sh disk osk-freeware.dd`.
