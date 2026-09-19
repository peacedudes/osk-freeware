# For rdoggett

Things that need YOU to decide or direct -- nothing else.  Nothing here is
decided; anything that gets decided leaves this file the same day.  The item
numbers are cited from notes/START-HERE-NEXT-SESSION.md, so they stay stable
and the gaps are deliberate: a missing number is an answered question.
Updated 2026-09-19.

**Nothing new was added here today.**  utree is finished and on the disk
(item 7's note below), and everything else this session touched was ours to
do.  Four items, all yours.

**Your notes of 2026-09-18 cleared THIRTEEN of these** -- 8, 9, 10, 11, 12,
13, 14, 15, 16, 17, 19, 20 and 22 are done and gone from this file, along
with the removals, rebuilds and additions they called for.  The commits say
what each one did; `git log --since=2026-09-18` is the list.

Two of those closed on your second note.  **17**: you are right that
shipping the source in the collection IS the condition met -- it is in
SRC/xyz now, and it is the source of those very binaries, checked.  **20**:
"find source if you can.  if you can't... ok" -- so DOC/README-GCC now
states exactly what is here (SRC/gcc142, SRC/vh), what is not (gcc 1.39,
g++ 1.40.3, gcc 2.5.6, cc2plus 2.5.8), that we looked, and where the one
lead goes.  It needs nothing further from you.

And the shadow rule you set is machinery now, not a promise: all 27 cards
for programs sharing a name with a utility of yours carry the warning, built
from a measured list the gate checks.

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
   screen-oriented file manager, a portable Unix xtree.  **It is ported,
   it works, and it is on the disk** as of 2026-09-19: the directory tree
   in one pane and the current directory's files in the other, tag a set
   and act on all of them, a shell escape with a history, its own help
   pages.  Nothing there needs you; `SRC/utree/README.OSK` says what the
   port had to deal with, and the card is in the gallery under Files &
   directories.

## Decisions

21. **`cpp` only -- omega is settled.**  You read the evidence and said "it
   sounds like we can't ship omega", so omega is out and stays out; nothing
   of it was ever on the disk, and PLAN-acquisitions records the decision.

   What is left is TOP's OS-9 build of the public-domain DECUS preprocessor.
   It works -- macros, #if, local includes -- and writes Microware's `#P`/`#5`
   line markers, because it was built to replace Microware's own `cpp` pass.
   It is one of the programs your shadow rule is about, and that rule now has
   machinery: every such card carries the warning automatically. So my
   recommendation is: ship it, as `cpp`, and let the card say what it would
   answer for. Say the word and it goes in; it is the only reason this item
   is still here.

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
