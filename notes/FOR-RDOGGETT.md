# For rdoggett

Open questions only. Nothing here is decided. Updated 2026-09-13.

## Yours alone -- nothing I can do about these

1. **Nothing is pushed, tagged or merged.** The branch has never left this
   machine; the CI pin is an old os9exec commit and has never run.

2. **The release does not carry the tar.** CI builds the image only.

3. **Nobody has tried this on real hardware.** The guides say so plainly.
   If you know someone with a real system, that is the paragraph to check.

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
