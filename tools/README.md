# Tools

    mkimage.sh          build the disk image from disk/
    mktar.py            write disk/ as a ustar archive (used by mkimage.sh)
    rebuild/            rebuild programs from source (see rebuild/README.md)
    gen_freeware_index.py

## Building the image

    OS9EXEC_DIR=/path/to/os9exec  tools/mkimage.sh disk osk-freeware.dd

Only the **os9exec binary** is needed — not its OS-9 system disk. The build
uses no Microware utility at all, so it runs on a clean machine:

1. os9exec's internal `mount -k` writes the blank image. It is a command of
   the emulator, not an OS-9 program, so it needs no disk to run.
2. `mktar.py` writes `disk/` as a ustar archive, host-side, with the finished
   disk's attributes already in the mode bits.
3. The collection's **own** `tar` extracts it — GNU tar 1.10, unstarred, so it
   runs without `cio`. The disk populates itself.

Because the attributes ride in the archive, there is no `attr` pass. The old
build drove `chx`, `makdir`, `copy` and `attr` out of a licensed system disk;
all four are gone.

`rebuild/` still needs a full Microware SDK — rebuilding a program from source
means running their compiler. That is a separate job from assembling the image
and is not part of a CI build.

## What the build checks

`tar` is run verbosely and the count of extracted files is compared against an
independently taken `find` count. If they disagree the build fails and writes
no image. This is not ceremony: this collection has produced a builder that
reported "copied 3287/3287" while every copy failed and wrote a blank 125 MB
image. Shrink the size argument below the content size to watch the check
fire.

## Two constraints worth knowing

**A volume name cannot contain a space.** OS-9 does not group command-line
arguments with quotes, so `-v=` takes the first word and the rest become stray
arguments. `mkimage.sh` refuses a name with a space rather than let it split.
Override the default with `RBF_VOLNAME`.

**The image is not byte-reproducible, by 352 bytes.** Content is exact and
`mktar.py` output is byte-identical between runs, but RBF stamps a creation
time into LSN0 and into each of the 351 directory descriptors, and those come
from the clock. File contents and file dates are deterministic; tar sets the
latter from the archive.

## Using the result

os9exec will not mount one host path as two devices. To have the image be both
`/dd` and `/h0` — which 108 programs with hardcoded `/h0` paths want — hard-link
it, so one inode has two names:

    ln osk-freeware.dd h0
