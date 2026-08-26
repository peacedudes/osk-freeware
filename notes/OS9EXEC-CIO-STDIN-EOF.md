# A cio-linked program never sees end-of-file on stdin, and hangs forever

**Found 2026-08-26**, an hour after the `F$SRqMem` runaway
(`notes/OS9EXEC-CIO-SRQMEM.md`), while trying to work out why `travesty`
"reproduced its input verbatim". It did no such thing. It never produced any
output at all, and never will, because it never finishes reading.

This is a second, independent defect on the same trap-handler path.

## Reproduction -- nine lines

`notes/cio-srqmem/getchar.c`:

    #include <stdio.h>
    main()
    {
        int ch, n = 0;
        while ((ch = getchar()) != EOF)
            n++;
        fprintf(stderr, "READ %d bytes from stdin\n", n);
        exit(0);
    }

Built both ways, run with the redirect done ON THE OS-9 SIDE, against a
37-byte file:

    os9exec -r sh -c "gcio < /h6/tiny.txt"     hangs until killed, no output
    os9exec -r sh -c "gcm  < /h6/tiny.txt"     READ 37 bytes from stdin, exit 0

`-qixm` is cio. `-qm` links stdio into the module. Same source, same file,
same redirect.

## Two ways to be fooled, and I was fooled by both

**1. Redirecting os9exec's OWN stdin does not work either.** With
`os9exec -r prog < file`, BOTH builds hang -- `-qm` included. The bytes reach
the program (they even appear on the console) but end-of-file never arrives.
The only redirect that behaves is one the OS-9 shell performs.

That matters for every test harness here: `tools/verify_all.sh` feeds
`< /dev/null`, which is fine because it is empty and returns EOF at once. A
sweep that fed real input from the host side would hang on every filter.

**2. What looks like program output can be the console echo of stdin.**
`travesty -n60 -o1 < med.txt` printed 4085 bytes -- the size of the INPUT, not
of the 60 characters asked for. I read that as "it reproduces its input",
wrote it up as a broken Markov implementation, and said so twice. It was
os9exec echoing the redirected input to the terminal while the program sat
blocked in `getchar`. A 37-byte input produces exactly 37 bytes of "output".

**The tell either way is the count.** Output whose length equals the INPUT's,
and ignores the flag that sets output length, is not output.

## travesty is fine

Rebuilt `TRAPFREE` and given the redirect on the OS-9 side, DJB's travesty
works, at the archive's source, unmodified:

    age.  This perfor multiple, the for pred OS-9 reate terminality a
    callowindow is the window or pred with the associate is
    ver, used function that degread (when with minimage offer.

That is a correct order-3 travesty of `DOC/screen/screen.doc`. It is now on
the disk, `TRAPFREE`, with the recipe saying that the flag is a workaround for
this defect and should come off when it is fixed.

**Two things I concluded earlier and withdraw**: that travesty's source was
damaged, and that its `_cpymem`-based `copy` macro was wrong. Both were
inferences from the phantom output. The archive's source builds and runs
unmodified; I tested the original against my "fix" and they behave
identically, so nothing of mine ships.

(The one real oddity stands and is inert: the `#ifndef OSK` arm contains a
bare `else seed = 0;` with no `if`, so that copy will not compile on a Unix
host until it is repaired. It is behind the `#ifdef` and never reaches cc
here.)

## Why it matters

`travesty` is a filter, and filters are what this defect eats. Anything that
reads to end-of-file -- a formatter, a compressor, a `wc`, a `sort` -- built
with the driver's DEFAULT `-qixm` will hang rather than finish. The programs
already on the disk are archive binaries and are not affected by how our
driver links; but every recipe that installs a filter is.

Both cio defects have the same shape: **the statically-linked build is
correct and the trap-handler build is not.** That is one layer, and it is
os9exec's.
