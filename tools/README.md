# Tools

    mkimage.sh          build the disk image from disk/
    mktar.py            write disk/ as a ustar archive (used by mkimage.sh)
    check_disk.py       check the disk tree's invariants
    gen_depends.py      regenerate disk/DOC/DEPENDS
    rebuild/            rebuild programs from source (see rebuild/README.md)
    gen_freeware_index.py

## Checking the tree

    tools/check_disk.py disk

Seven invariants, each of which has been made to fail on purpose:

- no text file contains LF -- OS-9 ends a line with CR alone, and an LF-ended
  file is read as one enormous line
- no UTF-8 on an 8-bit disk -- an em dash written host-side arrives as three
  garbage characters. Legacy 8-bit archive content is left alone, told apart
  by the fact that it does not decode as UTF-8
- no more than the 15 documented modules carry the SDK author stamp
- no editor or host litter (a vim swap file reached the tree once, and
  `mkimage.sh` reads `disk/` off the filesystem, so `.gitignore` cannot stop it)
- every command is named in `DOC/INDEX`
- the counts quoted in `readme` and `DOC/INDEX` match the tree
- `DOC/DEPENDS` is up to date

CI runs this before it builds anything. Note the stamp check reads files in
Python on purpose: `grep -r` on this machine is ugrep, which skips binary
files and reports a confident zero.

## Regenerating DOC/DEPENDS

    tools/gen_depends.py disk           # rewrite it
    tools/gen_depends.py disk --check   # exit 1 if it would change

`DOC/DEPENDS` says what each program needs besides its own binary, found by
scanning every binary for `/dd` and `/h0` paths. Run it after adding or
removing anything. It had drifted badly from hand-editing — it listed 110
programs where 158 have dependencies, and attributed one `gnuchess`'s paths to
the other.

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
