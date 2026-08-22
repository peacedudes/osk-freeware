# blarslib — found, not added. Your call.

Found 2026-08-22 while trying to build `macutils`. Five of its programs, plus
`mcvert` and `unsit`, fail with `can't open /dd/blarsdefs/sys/types.h` and
link against `/dd/lib/blarslib.l`. Neither is on this disk and nothing here
said what they were.

**What it is:** Bob Larson's Unix-compatibility library for OS-9/68k 2.3 —
`alloca`, `getcwd`, `getopt`, `getpw`, `gethostname`, `ln`/`rename`, `mkdir`,
`popen`, `putenv`, `signal`, `stat`, the BSD string functions, `utime`,
`usleep`, and the whole `v*printf` family. Which is to say: most of the gap
this collection keeps papering over with `tools/rebuild/shims/`.

**Where:** `Scraped/os9/PUBCMDS/microware-archive/LIB/blarslib.tar.Z` — in the
pool the whole time. It is a `compress`ed tar with a pre-POSIX header, so
`bsdtar` will not open it; `gzip -dc` then Python's `tarfile` will.

**Terms:** its Readme says, in as many words, *"All may be distributed for
free."* Alloca is credited to Doug Gwyn and many of the string functions to
Henry Spencer. Contact given as blarson@usc.edu.

## Why it is not on the disk

**Its DEFS directory carries copies of Microware's headers.**
`tools/screen_microware.py` flags 25 of its 67 files, and eight are BYTE
IDENTICAL to the SDK's:

    assert.h  curses.h  fileinfo.h  string.h  strings.h
    term.h    terminfo.h  varargs.h

That is the exact thing `check_disk.py`'s ninth check exists to catch, and the
exact thing that shipped for months in `disk/SRC/msfm`. Bob Larson's own note
explains why they are there — *"The Defs directory cannot and should not be
merged with /dd/defs, since it supplies replacements which require the
/dd/defs version as well"* — he shipped a full include directory because that
is how `cc -v=` works. It is his convenience, not his authorship.

So adding blarslib means deciding what to do about those eight files, and that
is a provenance decision, which is yours.

## What it would unlock

`macutils` (binhex, hexbin, macunpack, mcvert, unsit) builds against it
directly. `mtools`, `gtar` and several EFFO recipes name `blarslib.l` too.
Beyond that, its `Source/` is the honest version of what
`tools/rebuild/shims/` has been reinventing one function at a time.

## If you want it

  1. Take `Source/` and the four DEFS the screen calls clean; drop the eight
     that are Microware's and the thirteen that merely share a name until each
     has been looked at.
  2. `blarslib.l|blarslib|<the Source .c files>|||` — `rebuild.sh` builds a
     library from a recipe whose first field ends in `.l` (see `unix.l`).
  3. `make_overlay.sh` would need to put the surviving DEFS in as `blarsdefs`
     and the built library in `LIB`, the way it already does for
     `SRC/COMPAT/sys` and the collection's own `DEFS`.
  4. `SOURCES.txt` gets the "may be distributed for free" line and the three
     attributions.

Extracted for reading at the path in this session's log; nothing was copied
into `disk/`.
