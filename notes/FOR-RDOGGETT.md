# For rdoggett

Open questions only. Nothing here is decided. Updated 2026-09-12.

## One thing I want your steer on

1. **`creadoc`.** You asked me to tell you more. It is not really broken,
   and the "one constant" I said last time was wrong: I read its source
   and ran it, and it works THROUGH YOUR OWN OS-9. `creadoc.f' forks a
   shell twice -- `CALL shell('dir -eadu *.f >'//dirfile)' to list the
   files, and `CALL shell('del '//fn)' to clear its temporary -- so it
   needs a `shell' module plus Microware's `dir' and `del', exactly the
   way `m4' needs a shell. Here it gets as far as writing its temporary
   and then says `can't execute "del"'.

   It has one brittleness of its own on top: it reads each filename from
   column 53 of that listing, where this disk's `dir' puts it at 54, and
   2026 printing as `126' pushes it a column further again.

   So on a real system with the utilities present it is a column fix away
   from working, and that fix is one constant in `SRC/rtf/creadoc.f'. Its
   intended output already ships as `DOC/rtf/biory.doc'.

   My recommendation: ship it as it is, indexed as needing your shell and
   utilities (done), and leave the column alone -- patching a source to
   match one `dir' format would make it wrong on the systems where it is
   currently right. Say if you would rather I patched it.

## Yours alone -- nothing I can do about these

2. **Nothing is pushed, tagged or merged.** The branch has never left this
   machine; the CI pin is an old os9exec commit and has never run.

3. **The release does not carry the tar.** CI builds the image only.

4. **Nobody has tried this on real hardware.** The guides say so plainly.
   If you know someone with a real system, that is the paragraph to check.
