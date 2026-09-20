# For rdoggett

Things that need YOU to decide or direct -- nothing else.  Nothing here is
decided; anything that gets decided leaves this file the same day.  The item
numbers are cited from notes/START-HERE-NEXT-SESSION.md, so they stay stable
and the gaps are deliberate: a missing number is an answered question.
Updated 2026-09-19.

**START AT ITEM 30.**  It is the only one that touches somebody else's
property: the `fpu' on the disk was not the copy its grant covers, and
`fpu040' had no grant at all.  I have already acted -- swapped one,
removed the other -- and both are one command to reverse if you read the
grant more broadly than I did.

**Item 25 opened and closed in one night, and I owe you a correction on
it.**  I reported five libraries in LIB/ with no SOURCES.txt entry and said
one of them, `unet.l', might be Microware's because it was byte-identical
to a file on your oskBoot SDK.  **That was a false alarm and the tooling
had already warned me**: `tools/screen_microware.py' says in its own
docstring that oskBoot is your working BUILD OVERLAY and carries this
collection's own libraries, and it printed "[build overlay only -- may be
OUR file, check before acting]" next to the match.  I read that and wrote
the item anyway.  Checked properly against the pristine SDK, `unet.l' is
not there and never was Microware's.

What was real underneath it: LIB/ had never been screened at all, and TEN
of its fifteen libraries had no entry here.  All are now recorded, `unet.l'
is dropped on your word (nothing linked it, nobody could place it), and a
gate check keeps LIB/ answerable from now on.  Nothing here needs you.

utree is finished and on the disk (item 7's note), and everything else this
session touched was ours to do.  Four items.

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

   **The os9exec session says you have already settled the shape of this**
   -- relayed 2026-09-19, so check it against what you actually said: ONE
   push rather than push-then-fix, os9exec waiting until the work here that
   drives it settles (it expects about a week), then a fleet sweep, then the
   two pushed together.  Nothing on its branch `fix/scf-pd-eor' has left
   that machine either, so there is no newer commit to pin to today and I
   have written none into anything.  If that is right, this item waits on
   nothing of mine.

   **MEASURED 2026-09-19, against the os9exec checkout rather than taken on
   anyone's word, because the numbers matter here:**

     github/master tip           0f83437, 2026-08-16
     our CI pin  261b4b6         an ancestor of it -- fetchable today
     the branch tip 665ca8c      **215 commits ahead of github/master,
                                 and not pushed**

   So a CI build today compiles an os9exec of **2026-08-04**, and NONE of
   the fixes this collection now depends on are on GitHub: `40facae'
   (F$Alarm and the Linux dot-file rename), `d401ce2' (the signed F$STrap
   handler offset -- this is why `config' no longer looks like it wants a
   68881), `685a4c3' (SS_EOF on host-directory files) and today's
   `00fcec5' with its test `665ca8c' (F$PErr looping for ever on a
   terminal, which is what made `load' hang).  All five are ancestors of
   665ca8c, so ONE push carries the lot.

   The os9exec session warned me that 261b4b6 might not be in its history
   at all.  It is -- checked with `git merge-base --is-ancestor' -- and it
   is on `github/master'.

   **THE PIN NOW NAMES THE BRANCH, on your instruction 2026-09-20: "you
   need to be the local branch your sibling claude is updating for you,
   not the released version."**  `.github/workflows/build-image.yml' reads
   `fix/scf-pd-eor' where it read 261b4b6.  Everything in `tools/' already
   ran the binary built from that working tree -- `tools/paths.py' resolves
   the emulator to `~/Developer/os9/os9exec' -- so CI was the only place
   still looking at the released version, and it would have built an
   emulator without any of the four fixes and reported success.

   Until the branch is pushed the workflow cannot run at all, which is the
   right failure and not a new blocker: it has never run.  **At release,
   freeze it** -- put the tip COMMIT in place of the branch name, taken at
   the moment of tagging, so a force-push cannot change what a tagged build
   produced.  The tip moves fast: 665ca8c to 7d54fa1 inside a few hours on
   2026-09-19.

   One thing landed there today that changes what a program here can do:
   its per-process memory ceiling went from 512 allocation blocks to 8192
   (their c0e68fa, unpushed).  `utree' on the whole of /dd runs out under
   the old one; I will record whether the new one reads it.

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

26. **One line of 1991 source would make `pnmtosir'/`sirtopnm' round-trip,
   and I have not touched it.**  The SIR pair comes back the right size with
   the colour planes rotated over the first pixels; that has been in
   DOC/INDEX as a known fault since August with no cause.  The cause is two
   bytes: `pnmtosir' writes a header of 1536 little-endian shorts -- 256 file
   header, 256 colour-map header, 1024 map, three aligned blocks, 3072 bytes,
   and a 4x1 image is 3084 bytes on the nose -- while `sirtopnm' reads five
   shorts and then

       for ( i = 1; i < 1531; i++ )

   skips 1530 more.  1535 shorts, 3070 bytes.  It starts on the pixels two
   bytes early and every plane it reads is shifted by two.

   I checked that by PREDICTION rather than by patching: the shift says solid
   red must come back green, green, red, red and solid green must come back
   blue, blue, green, green, and both are exactly what the disk produces.
   Three data-test cases now pin it.

   The header is three aligned blocks, so the reader is the one that is
   wrong, and `i < 1532' is the whole fix.  **But the loop is as the 1991
   original has it**, so this is an upstream defect and fixing it means
   shipping a netpbm that differs from the archive -- against the grain of a
   collection that preserves period software.  Both programs are ours to
   rebuild (SRC/netpbm/PNM, recipes in place), so it is a ten-minute job
   whenever you say.  Ship the patched pair, or keep the archive's and leave
   the note?

28. **Does "name what the reader HAS" reach the shipped READMEs?**  The
   gate enforces it on `DOC/INDEX', `tools/howto.psv' and the gallery
   sheets, and its docstring says the PATTERNS are narrow on purpose.  It
   does not read the shipped `DOC/README-*' files, and four of them use the
   phrasing:

       README-GCC:172       "and is not on this disk, so nothing that
                             included <stdio.h> could be"
       README-BUSERR:90     "it is in the SDK and it is deliberately not on
                             this disk" (about `sysglob.h')
       README-METAFONT:85   "three Microware utilities that are not on this
                             disk"
       README:43            "the docs are here but the BINARY is not on this
                             disk"

   I fixed only the unambiguous one, `DOC/rayshade/README-RAYSHADE', which
   said "THIS DISK HAS NO `shell': it has bash and sh" -- misleading as well
   as against the rule, since the reader's own OS-9 has one and the document
   goes on to tell them to make the name with a copy.

   The other four read to me as facts rather than discouragement, and two of
   them are about Microware's own files being deliberately absent, which is
   the respectful thing to say.  Do you want the rule to reach those
   documents, or is the narrow scope right?  If it should reach them, the
   check takes one line -- the file list, not the patterns.

   **More evidence, 2026-09-19: the PATTERNS are narrow too, and one real
   violation was hiding behind that.**  The gate looks for "not on this
   disk" and "neither is on this disk".  Sweeping the captions for the
   same claim in other words -- "this disk does not carry", "there is no
   X here" -- found eight.  Seven are facts about data or hardware ("no
   PackIt archive is on this disk to open", "no Tektronix terminal here",
   "there is no X server here") and read correctly.  The eighth was
   `dback': *"There is no `copy' program on this disk, so nothing is
   copied"* -- and `copy' is Microware's, so the reader HAS it and the
   card was telling them their own utility does not exist.  Rewritten to
   say it calls their own OS-9's `copy'.

   So the same question applies to the patterns as to the file list, and
   the answer may differ: widening the file list is safe, widening the
   patterns would flag seven captions that are right.

30. **READ THIS ONE FIRST.  The `fpu' we shipped was not the copy the
   grant covers, and `fpu040' had no grant at all.  I swapped one and
   removed the other; both are one command to reverse.**

   On 2026-09-12 you ruled: *"If we follow the rules of a grant, then we
   can include it. So yes, do."*  The grant is `fpu.doc': *"FPU - (C)
   1995 Microware Systems Corp.  Permission to distribute FPU is granted
   so long as this file is retained."*  The commit that added the modules
   says they were "taken from the pool copy that travels with its grant".
   The bytes say otherwise, and I checked them today:

     what shipped    fpu     14,572 bytes  edition 5   md5 4893b5f9
                     fpu040   6,140 bytes  edition 11  md5 30f667f0
     where from      both are byte-identical to the loose modules in
                     TELECOM/STerm68k.lzh, a terminal program's archive
                     that carries no document and no grant
     the granted     fpu     12,724 bytes  edition 12  md5 3f5b0760
     copy            the module in TELECOM/xyz.lzh, in the same archive
                     as the fpu.doc we ship -- and there is NO fpu040
                     anywhere beside a grant

   `disk/DOC/fpu.doc' is byte-identical to the granted document, so the
   condition was being met -- for a file we were not shipping.

   **What I did.**  Replaced `disk/CMDS/fpu' with the granted copy (also
   the newer module: edition 12 against edition 5), and took `fpu040' off
   with `tools/remove_program.py'.  `SOURCES.txt' now records the hashes
   and says plainly which copy is here and why; CLAUDE.md and
   `notes/MICROWARE-PERMISSION.md' are corrected; the gate is green.

   **Why I did not wait for you**, since every other removal here has
   been on your ruling.  Your ruling stands and I followed it: following
   the grant means shipping the file the grant travels with.  What
   changed is a premise, not a decision.  And the disk itself already
   said, in `SOURCES.txt', that `fpu040' was "Still NOT here" -- so it
   was telling a reader something untrue about a Microware module.

   **What is yours to say.**  The grant's words are "Permission to
   distribute FPU", not "this copy of FPU".  If you read that as covering
   the module generally, `fpu040' can come back -- `git revert' of the
   removal commit, and I will re-run the gate.  I took the narrow reading
   because it is the one `notes/MICROWARE-PERMISSION.md' already argued
   for and because it is Microware's property and they are still trading.

29. **Your username was on six published cards, and the name "Robert
   Doggett" is still on the disk in five places.**  The username went
   today: `tools/terms.psv' gave every program we wrote a terms line
   ending *"rdoggett, 2026-09-18: 'anything we write is anybody who wants
   it can have it'"*, and that was on `about', `fact', `keep', `kept',
   `man' and `unkeep' in the gallery.  Four more decision attributions
   were in `disk/SOURCES.txt', one in `DOC/STATUS', one in a port note,
   and two in HTML and JavaScript comments the template copies verbatim
   into the published page.  All nine are gone, the sentence before each
   already said the thing, and `check_disk.py' has a gate now -- `the
   artefact does not name us' -- with a breaker.

   **What I did NOT remove.**  The gate looks for the username, not the
   name.  `Robert Doggett' stays in `DOC/zot/zot.1', `SRC/zot/zot.c',
   `SRC/misc/qt.c', `SRC/snap/main.c' and `SRC/hc_utils/fgrep.c', where
   the files' own headers record who ported them -- "heavily mucked with
   for OSK".  That line is the archive's, not ours, and removing it would
   edit somebody else's file.  `DOC/os9dsk/PUBDOM19.DSK' carries it too,
   in a disk image from the period.  `SOURCES.txt' says *"Robert Doggett
   asked Allan at Microware for permission"*, kept because the record of
   who asked is the provenance.  The os9exec URL stays for the same
   reason -- a reader has to be told where the emulator is.

   **CORRECTED 2026-09-19, by you:** *"I did not write zot or qt or snap
   or any of the others.  I just did trivial porting work to get them
   running.  Credit should go to the original author."*  I had written
   this item up as "you wrote those ports", which is exactly the mistake
   your own standing rule warns about.  The disk itself never made it:
   `SOURCES.txt' says "The files that remain and carry that name are
   PORTS, and say so", and `tools/terms.psv' credits Roger Murray and
   Marc Kriguer for zot, Mike Cowlishaw and Mark Dapoz's C conversion for
   qt, David MacKenzie for snap.  `check_disk''s gate docstring and the
   handoff are corrected to match.

   Say the word if you want any of those lines gone and it is a one-line
   change to the gate's allowed list.

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
   `GAMES/HACK/PLAYGROUND/save/0tester` stays -- it is committed under
   `disk/`, so every rebuild puts it back.  The harness bug that put it
   there in the first place is fixed.  Harnesses DO write to the image
   while they run (scratch files, a mailbox, a RAM disk), and none of it
   survives: the image is rebuilt from `disk/` each time, so only what is
   committed there persists.

   **The stale-image problem is fixed and you need do nothing.**  Your
   `free' alias opens `osk-freeware/h0', which symlinks to the repo's
   `osk-freeware.dd' -- the same file the build writes.  So there was never
   a second copy to keep in step, only one that nobody had rebuilt.  Sector
   0 was four days stale when this was written -- 2026-09-15 07:58 -- and
   has been rebuilt from the current tree several times since, the last of
   them at the end of the 2026-09-19 session.  `utree', `westley',
   `SYS/UTREE' and `DOC/utree' were read back through your own alias to
   check the first of those.  No date is quoted here on purpose: the rule
   this collection keeps learning is that a figure written down drifts, and
   `ls -l osk-freeware.dd' answers it in one line.

   Going forward it is mine to keep current: rebuilding that file is the
   last step of a session here now, and the handoff says so.  If you ever
   want to do it yourself it takes four seconds --
   `OS9EXEC_DIR=~/Developer/os9/os9exec tools/mkimage.sh disk osk-freeware.dd`.
