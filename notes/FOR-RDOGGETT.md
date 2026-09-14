# For rdoggett

Open questions only. Nothing here is decided. Updated 2026-09-14.

## Yours alone -- nothing I can do about these

1. **Nothing is pushed, tagged or merged.** The branch has never left this
   machine; the CI pin is an old os9exec commit and has never run.
   **Before a release, that pin MUST move past an os9exec fix that is not
   in yet** (2026-09-13): the Linux build of os9exec renames every file
   starting with `.' on an RBF image, and CI builds the image on Ubuntu --
   so a CI-built image would carry `.bashrc', `.newsrc' and `.ELM' under
   wrong names.  Fixed in os9exec **4d26520** (fix/scf-pd-eor, not pushed
   yet); the CI pin must be at or past it.  The handoff has the detail.

   **That branch now also carries a CPU fix, and the pin should take it
   too** (2026-09-14): NEG and NBCD never set the 68000's X flag, so
   Microware's software doubles came out wrong -- 1.0-1.0 was -2^-20.
   209b35c, reviewed by the os9exec session, with its tests at d56b1bd,
   the branch tip.  The image a CI build writes is not affected (tar
   extracts no floating point), but every figure a program prints under
   an older os9exec is, and this repo's cases, cards and
   DOC/README-FLOATINGPOINT are now written against the fixed one.
   `notes/os9exec-bugs/X-FLAG.md` has it.  The pin today is 261b4b6.

3. **Nobody has tried this on real hardware.** The guides say so plainly.
   If you know someone with a real system, that is the paragraph to check.

7. **Cancel usenet-rewind before it renews, about 2026-10-13, and delete
   the key.**  You bought one month of Researcher on 2026-09-13 for the
   OS-9 newsgroup pull.  Cancelling happens on their site, in your account.
   The key is `~/.config/usenet-rewind/os9`; once the pull is verified a
   session can delete that file for you if you say so.

## ANSWERED -- the newsgroup archive

5. ~~**comp.os.os9 1987-2002 has been FOUND, and getting it properly costs
   about $40.**~~  **You bought the Researcher month on 2026-09-13** and
   the pull is complete: every OS-9, m68k and CD-i group plus the
   OSK-mention searches, each checked against the site's own index, 6,905
   pages in `~/Developer/os9/Scraped/usenet-rewind/` -- private, author
   addresses included, never committed.  What it yielded (little new
   software, the CD-i and MM/1 findings, four os9exec bugs, and the push
   to port perl) is in `notes/PLAN-acquisitions.md`.  Item 7 is what is
   left of it: cancel before the renewal and delete the key.

## ANSWERED -- rcsmerge was never a licence question

6. ~~**`rcsmerge' could be made to work, but the last piece is
   non-commercial-only.**~~  **Wrongly put to you.**  Non-commercial terms
   were settled on 2026-09-11 -- accepted, record the terms, ship -- and
   the `utime.c' rule is only for a file with a bare copyright and no
   grant.  ELM's OSK `pipe.c' has a grant, so it could simply be used; and
   a `pipe()' of the collection's own now exists in `SRC/perl4/osk.c'
   anyway.

   What actually stops rcsmerge is technical, and none of it is yours:
   `SRC/rcs/rcsmerge.c' is truncated mid-statement and three of the
   sources its makefile links are absent, so it cannot be rebuilt; `ci'
   cannot store a second revision here, and a merge needs two; and the
   helper it forks is named `merge', which on a real system is Microware's
   concatenating utility -- so loading that first does not help, and
   RCS's three-way merge would need another name.  An intact RCS source is
   where it would start.  The handoff carries it.

## ANSWERED -- the dots question is closed

4. ~~**Is `../..' valid OS-9 because Microware says so, or because you
   recall it working?**~~  **You answered this on 2026-09-13**, relayed
   here by an os9exec session: *"yes real os-9 accepts ../../../.. no
   problem"*, and you expect `./../.../...././file' to work too.  So it
   is YOUR WORD rather than a manual citation, which is a perfectly good
   footing and is now labelled as one wherever it is written down.  The
   os9exec side reports that form working live after `985e0d8', climbing
   exactly six levels from seven deep and NOT reaching seven -- so no
   overclimb.

   You also said to KEEP the gate: cards should use `...' rather than
   `../..' **"because it's uniquely os9"**.  So the gate's reason is now
   house style first -- that spelling is the one this system has and Unix
   does not, and a collection teaching OS-9 should show it -- with
   portability second (the chained form failed on RBF images until
   os9exec `985e0d8', which is newer than most readers' builds).
   `tools/check_disk.py' says exactly that now.  Nothing here needs you
   again.
