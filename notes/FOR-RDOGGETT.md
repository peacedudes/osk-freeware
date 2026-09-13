# For rdoggett

Open questions only. Nothing here is decided. Updated 2026-09-13.

## Yours alone -- nothing I can do about these

1. **Nothing is pushed, tagged or merged.** The branch has never left this
   machine; the CI pin is an old os9exec commit and has never run.

2. **The release does not carry the tar.** CI builds the image only.

3. **Nobody has tried this on real hardware.** The guides say so plainly.
   If you know someone with a real system, that is the paragraph to check.

## A decision that costs money, and only you can make it

5. **comp.os.os9 1987-2002 has been FOUND, and getting it properly costs
   about $40.**  `usenet-rewind.com' holds the group from May 1987 to
   December 2023, 17,802 messages -- verified by reading the May 1987
   digests themselves, which carry period OSK postings (Dieter Stoll's
   ARC port to OS-9/68K "posted with permission", James Jones' compress
   from mcrware).  This is the hole the acquisitions plan has called the
   live question for two days: the group's active era, where OSK
   freeware was actually posted, held nowhere else we could find.

   Bodies read free.  What is gated is what an archive actually needs --
   the author addresses (masked on the free pages) and the original
   messages with full headers.  Their Researcher plan, $39.99 for a
   month, adds a JSON search API.

   **Their terms forbid scraping and bulk export, and carve out "an
   authorized API plan" by name.**  So there is a licit route and an
   illicit one, and I have not taken either: a scraper would be against
   their terms, and a subscription is your card and your call.  If you
   want it, one month of Researcher would cover comp.os.os9 1987-2002
   plus mod.os.os9, sub.os.os9, fj.os.os9 and de.comp.os.os9.

   Everything else was searched and closed -- narkive starts 2003,
   usenetarchives is behind a Cloudflare challenge on every path, Google
   Groups 429s and its 1987 Wayback captures are empty framesets, the
   giganews corpus walls at 2003, and the UTZOO mirrors stop mid-1991.
   `notes/PLAN-acquisitions.md' has the whole table.

## A licence question, on a file that already ships

6. **`rcsmerge' could be made to work, but the last piece is
   non-commercial-only.**  `rcsmerge' ships and cannot merge, because it
   forks `merge' and no `merge' binary is here.  Everything needed is on
   the disk already: `SRC/rcs/merge.sh' (RCS's own script) and
   `SRC/diff/diff3.c' (part of the GNU diff 1.1 we already ship, just
   never built).  I built diff3 as far as it goes: it compiles once the
   build supplies `-DDIFF_PROGRAM="/dd/CMDS/diff"', and then the LINK
   fails on one symbol, `pipe'.

   The only `pipe()' in the pool is
   `SRC/infoxpress/BNU/ELM_2.4/OSK/pipe.c' -- thirteen lines, and it
   would almost certainly finish the build.  **Its own header says it
   may be copied and distributed freely "for any non-commercial
   purposes", and incorporated into commercial software only with the
   authors' written permission** (Wolfgang Ocker, Ulli Dessauer, Reimer
   Mellin, 1988).  That is NARROWER than the Elm 2.4 package it sits
   inside, which `SOURCES.txt' records under the permissive Elm licence.

   The source already ships and that is not in question.  What I have
   not done is BUILD a binary we ship against it, because that carries
   the non-commercial clause into the collection's own artefacts, and
   this collection has been careful about exactly that (the `utime.c'
   rule, `loglist' left out for want of a grant).  Your call: leave
   `rcsmerge' as a card about a missing helper, write a `pipe()' of our
   own over OS-9's pipe device, or accept the clause for that one
   binary.  Nothing else about diff3 is blocked.

## One question, asked of you by an os9exec session

4. **Is `../..' valid OS-9 because Microware says so, or because you
   recall it working?**  You told us dots-only components climb dots-1
   and add up, so `../..' means three levels; that is now written into
   `tools/check_disk.py' as the reason its dots gate is about
   PORTABILITY and not about validity.  An os9exec session asked which
   footing the claim stands on, and it matters to them: they changed
   os9exec to accept it (`985e0d8'), so if it is a recollection rather
   than documented behaviour, they have encoded a recollection.  A
   manual citation would settle it; "I remember it working" is a fine
   answer too, as long as we label it as one.
