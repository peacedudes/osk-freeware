# For rdoggett

Open questions only. Nothing here is decided. Updated 2026-09-13.

## Yours alone -- nothing I can do about these

1. **Nothing is pushed, tagged or merged.** The branch has never left this
   machine; the CI pin is an old os9exec commit and has never run.
   **Before a release, that pin MUST move past an os9exec fix that is not
   in yet** (2026-09-13): the Linux build of os9exec renames every file
   starting with `.' on an RBF image, and CI builds the image on Ubuntu --
   so a CI-built image would carry `.bashrc', `.newsrc' and `.ELM' under
   wrong names.  Fixed in os9exec **4d26520** (fix/scf-pd-eor, not pushed
   yet); the CI pin must be at or past it.  The handoff has the detail.

3. **Nobody has tried this on real hardware.** The guides say so plainly.
   If you know someone with a real system, that is the paragraph to check.

7. **Cancel usenet-rewind before it renews, about 2026-10-13, and delete
   the key.**  You bought one month of Researcher on 2026-09-13 for the
   OS-9 newsgroup pull.  Cancelling happens on their site, in your account.
   The key is `~/.config/usenet-rewind/os9`; once the pull is verified a
   session can delete that file for you if you say so.

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

   **Their terms, read whole on 2026-09-13 (dated that day), were
   OVERSTATED here before.**  They forbid you to "Scrape, bulk-export,
   resell, or repurpose Service data for spam, fraud, identity theft,
   harvesting of email addresses, or any abusive purpose", and to "Place
   automated load on the Service beyond normal interactive use, except
   through an authorized API plan and within its limits."  So paying IS
   the permitted route: the API with your key, within quota, is what the
   terms allow.  Scripting the free web pages is what they do not.

   Only Researcher includes contact details, headers, full-message and
   thread downloads and the API -- Individual ($9.99) has none of them.
   The API (`GET /api/search`, groupname + date range,
   `returnOriginalMessage=1`) gives 10 results a page against 25,000
   searches a month; comp.os.os9 whole is about 1,800 pages.  Caveats:
   keys may not be "shared, pooled, or used concurrently by multiple
   individuals or systems"; addresses must not be harvested (credit by
   name, never republish 1980s addresses); their API page says "Pro plan"
   where pricing says Researcher, worth one email first; and nothing
   grants redistribution of the messages themselves.  One month would
   cover comp.os.os9 1987-2002 plus mod.os.os9, sub.os.os9, fj.os.os9 and
   de.comp.os.os9.

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

   **Three findings from 2026-09-13 that make this moot for now:**
   (a) on a real system the name is TAKEN -- rcsmerge forks a bare
   `merge', which reaches Microware's `/h1/CMDS/merge' ("merge files to
   standard output", concatenation, no `-p'); RCS's helper would need
   another name and a rebuilt rcsmerge.  (b) `SRC/rcs/rcsmerge.c' is
   TRUNCATED -- 3,434 bytes ending mid-statement at `faterror', as
   committed in 46cef22b -- and `rcsutil.c', `rcsrev.c', `rcssyn.c',
   which its makefile links, are absent, so rcsmerge cannot be rebuilt
   from what ships.  (c) `ci' cannot store a second revision here
   (`devtools.cases' asserts "diff failed"), and rcsmerge needs two.
   The order, if RCS is wanted: an intact RCS 4 source, then `ci', then
   the helper under a new name.

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
