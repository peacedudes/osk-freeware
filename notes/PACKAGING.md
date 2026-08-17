# Packaging: what device this collection has to be, and when

Written 2026-08-16, after shipping Microware's runtime modules changed what is
possible. Numbers here are measured, not recalled.

## How device-dependent is the collection, really?

Of the 497 programs in `CMDS` and `CMDS/GAMES`:

| | |
|---:|---|
| **318 (64%)** | name **no device at all** -- they run wherever the collection is mounted |
| 87 | name both `/dd` and `/h0` |
| 79 | name `/dd` only |
| 13 | name `/h0` only |

So 179 carry a device name they cannot outrun -- and the surprise is the
direction. **166 of them name `/dd`, only 100 name `/h0`.** The long-standing
worry here has been the `/h0` paths; the bigger group was always `/dd`.

`SYS/login` is already device-independent: it works out `ROOT` from the path it
was invoked by, so `os9exec -r bash /h1/SYS/login` sets `PATH`, `TERMCAP` and
`HOME` to `/h1` without being told. Verified.

## The two arrangements, and what each needs

**1. The tour, under os9exec.** Mount the collection as `/dd` and run it. Since
the Microware runtime ships (`cio`, `math`, `math881`, `csl`, `csl020`), this
now needs **nothing else at all** -- no boot disk, no system disk, no modules
to find. All 124 starred programs were run this way and 123 work. The `/dd`
paths in 166 binaries are correct by construction, because the collection *is*
`/dd`.

This is the strongest the collection has ever been, and it is the arrangement
to lead with.

**2. A real OS-9 machine.** Here `/dd` is the user's own boot device and this
image is a secondary drive -- `/h1`, `/h2`, whatever is free. `/h0` may well be
taken. In that arrangement:

- the 318 device-free programs run straight off the collection
- the 166 that name `/dd` look at the USER'S disk, and do not find their data
- trap modules load from `/dd/CMDS`, so the collection's own `cio` is not
  found -- but a real OS-9 machine already has one, which is the point

## `keep` is the bridge, and it resolves the `/dd` problem by accident

A program that names `/dd/GAMES/cookie/sayings` is broken while the collection
sits at `/h1` -- and **correct the moment it is kept onto the user's `/dd`**,
because `keep` puts the data at the same relative place the binary already
looks. Demonstrated end to end with the collection at `/h1` and a separate
`/dd`:

    $ keep cookie
    kept /dd/CMDS/cookie
    kept /dd/GAMES/cookie/sayhash
    kept /dd/GAMES/cookie/sayings
    $ /dd/CMDS/cookie
    To be awake is to be alive.  -- Henry David Thoreau, in "Walden"

So the hardcoded `/dd` paths are not a defect to be patched out. They are
correct for the destination, and `keep` is what moves a program to where its
own assumptions hold.

`keep` had the same disease and was cured: it hardcoded `C=/dd/CMDS` and broke
the moment the collection was not `/dd`. It now works out where it lives from
its own invocation path, exactly as `SYS/login` does.

## One bootstrap trap worth knowing

On a bare `/dd` with the collection elsewhere, `cp` itself stops with
`**** Can't install trap handler **** cio` -- you need `cio` to run `cp`, and
`cp` to keep `cio`. It does not arise on a real OS-9 machine, whose `/dd`
already has the runtime. It only bites if someone points this at an empty
disk, and the answer there is to mount the collection as `/dd` instead.

## Open

Nobody here knows how other people organise their drives. What is written
above assumes `/dd` is the user's boot device and the collection is a
secondary -- true of OS-9 by convention, but the device LETTER is a guess.
Nothing in the collection depends on it being `/h0` any more except the 100
binaries that say so, and `DOC/README-RUNNING` covers giving them one.
