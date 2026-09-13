# For rdoggett

Open questions only. Nothing settled, nothing done. Updated 2026-09-12.

## Ship or not

1. **Q2 -- source for binaries we already ship.** gcc, g++, VH, dvips,
   gawk, bison, emacs ship without source. Three are staged and waiting:
   `top/src/gawk2.0`, `top/src/bison`, `top/src/emacs_3.10`, and dvips
   from `DRIVERS/dvips_source.lzh` (641 KB, archive 3978). Add them?

2. **Microware's `fpu`.** Carries its own grant -- "Permission to
   distribute FPU is granted so long as this file is retained" -- but
   CLAUDE.md lists `fpu040` among the Microware products that stay out.
   Grant in the file vs the house rule. In or out?

3. **`jive`.** Builds and runs; a joke filter built on a racial caricature
   of Black speech. Held, not shipped. Ship or drop it for good?

## Remove or keep

4. **Needs a display we have not got:** cyberwar, puzzle, scriptmaster,
   colortest, dclock, apfel, g, showpic, sine, striche, graphdemo,
   graphsave, umusek.

5. **Needs hardware we have not got:** splman, lpsched, for, lnk, lnk.org.

6. **Broken or brittle:** dedit (spins, writes raw sectors), names (garbage,
   never terminates), rstory2 (forks programs that never shipped), ff,
   splitalf, `cuts -e`, dearc (no sample to read).

7. **Duplicates, one call each:** the five GNU Chess builds, and `wc.cio`.

## Small yes/no

8. **creadoc** -- one constant (`fnpos = 53`) makes it run. Rebuild it, or
   keep it as documented historical software?

9. **`xmas`** signs off "from The ghost of Robert past" -- the OS-9 port's
   own change to the line the source invites you to change. Kept as it
   shipped, with nothing on the card naming whose it is. Leave it?

10. **The `os9-dev` skill** -- three gaps I can write in. Say the word.

## Yours alone

11. **Nothing is pushed, tagged or merged.** The branch has never left this
    machine; the CI pin is an old os9exec commit and has never run.

12. **The release does not carry the tar.** CI builds the image only.

13. **Nobody has tried this on real hardware.** The guides say so plainly.
    If you know someone with a real system, that is the paragraph to check.
