#!/bin/bash
#
# Build the clean /dd overlay that every rebuild here needs, and that nothing
# in this repo previously knew how to make.
#
# `rebuild.sh` has always required $OS9CLEAN -- "a /dd overlay ... whose
# cstart* copies have their 64-byte Author psect overwritten with spaces" --
# and listed it under "Prerequisites, none of which are in this repo".  So the
# overlay was somebody's local directory, and on 2026-08-21 it was gone: the
# whole rebuild machinery was unusable until it was worked out again from the
# README.  This script is that work, written down.  Run it and you have a
# working toolchain.
#
# Usage:  make_overlay.sh [<destination>]        default: $TMPDIR/os9clean
#         export OS9CLEAN=<destination>
#
# The SDK location comes from tools/paths.py, which is the single place that
# knows where anything lives.
#
# WHY A COPY AND NOT SYMLINKS
#
# The obvious build -- symlink everything, make LIB real -- does not work, and
# fails in the most expensive possible way.  os9exec will not open a symlink
# through its host-directory RBF emulation: a symlinked CMDS gives
# `E_FNA (214): 'shell'`, and so does a real CMDS full of symlinked files.
# Worse, that error arrives on a `#` line, so the standard `grep -v '^# '`
# used to strip emulator chatter hides it completely and the run looks like a
# success that merely printed nothing.  This cost a cycle here even knowing to
# watch for it.  41 MB of copy is the price of a toolchain that works.
#
# WHY THE STAMP MATTERS
#
# `cc` links Microware's `cstart.r` into every C program it builds, and that
# cstart carries a 64-byte Author psect.  Whoever owns the SDK copy gets their
# name written into every binary built through it -- the SDK here is stamped
# `from the disk of Robert Doggett`.  Blanking the psect BEFORE linking is the
# only way to get a clean binary out of a fresh build; `tools/blank_author.py`
# does the same edit after the fact, for modules that cannot be rebuilt.
# `check_disk.py` fails on a new stamp, so a build made without this overlay
# will be caught -- but only after you have made it.
#
set -eu

HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/../.." && pwd)
DEST=${1:-${TMPDIR:-/tmp}/os9clean}

SDK=$(python3 -c "import sys; sys.path.insert(0,'$REPO/tools'); import paths; print(paths.sdk())")
[ -d "$SDK" ] || { echo "$0: no SDK at $SDK" >&2; exit 1; }

echo "SDK:     $SDK"
echo "overlay: $DEST"

rm -rf "$DEST"
cp -R "$SDK" "$DEST"
chmod -R u+w "$DEST"

python3 - "$DEST/LIB" <<'PY'
import glob, os, re, sys

# The same pattern tools/blank_author.py matches, and the same replacement:
# spaces, exactly as long as what they replace.  A ROF (.r) has no module CRC
# -- the linker computes that for the finished module -- so this is a plain
# byte edit with nothing downstream to fix up.
STAMP = re.compile(rb">{4,}from the disk of[^<]*<{4,}")

blanked = 0
for path in sorted(glob.glob(os.path.join(sys.argv[1], "*"))):
    if not os.path.isfile(path):
        continue
    data = open(path, "rb").read()
    if not STAMP.search(data):
        continue
    clean = STAMP.sub(lambda m: b" " * len(m.group(0)), data)
    assert len(clean) == len(data), path
    open(path, "wb").write(clean)
    blanked += 1
    print("  blanked", os.path.basename(path))

if not blanked:
    sys.exit("no author stamp found in any LIB file -- has the SDK changed? "
             "Refusing to report a clean overlay that was never cleaned.")
print(f"  {blanked} cstart copies blanked")
PY

# The collection's own os9lib.l, which several recipes link and which is NOT
# part of the SDK -- it lives on the disk, in GNULIB. Without it those recipes
# fail with an unresolved symbol that looks like missing source.
if [ -f "$REPO/disk/GNULIB/os9lib.l" ]; then
    cp "$REPO/disk/GNULIB/os9lib.l" "$DEST/LIB/os9lib.l"
    echo "  added the collection's own os9lib.l"
fi

# SRC/COMPAT/sys/ goes into DEFS, not just onto the -V path.  `cpp' finds a
# plain `<stdlib.h>' through -V but NOT a `<sys/types.h>': given a name with a
# directory in it, it reports `can't open /dd/DEFS/sys/types.h' and stops,
# having apparently never tried the -V directories at all.  mtools and lwf both
# fail that way, and the error reads like a missing header when the header is
# right there in COMPAT.  Copying the directory in is the whole fix.
if [ -d "$REPO/disk/SRC/COMPAT/sys" ]; then
    mkdir -p "$DEST/DEFS/sys"
    cp "$REPO/disk/SRC/COMPAT/sys/"* "$DEST/DEFS/sys/"
    echo "  added SRC/COMPAT/sys to DEFS (cpp will not find <sys/x.h> via -V)"
fi

# A STAND-IN FOR THE ULTRA C LAYOUT some OSK ports were compiled against.
# lua's SRC/LUAC/luamod.c opens with
#
#     #include </dd/ucc/defs/types.h>          /* LUA uses its own types.h */
#
# an ABSOLUTE path, which no -I or -V can redirect -- the same trap
# DEFS/blarsdefs/errno.h exists for.  process_id is the one type it needs that
# the SDK headers do not carry.
#
# THE OVERLAY ONLY.  Nothing like this goes on the shipped disk, where a `ucc'
# directory would read as Microware's Ultra C being installed here.
mkdir -p "$DEST/ucc/defs"
printf '%s\r' \
  '/* Stand-in for the Ultra C layout an OSK porter compiled against.' \
  '   BUILD OVERLAY ONLY -- see tools/rebuild/make_overlay.sh. */' \
  '#include "/dd/DEFS/types.h"' \
  '#ifndef _OSK_PROCESS_ID' \
  '#define _OSK_PROCESS_ID' \
  'typedef unsigned short process_id;' \
  '#endif' > "$DEST/ucc/defs/types.h"
echo "  added ucc/defs/types.h (lua names it by absolute path)"

# The COLLECTION's own DEFS as well.  disk/DEFS carries headers the SDK does
# not -- auxlib/local.h, os9lib, os9unix, ncurses, p2c.h -- and programs on
# this disk were built against them.  `spooler' asks for <local.h> and there is
# no other copy.  Only what the SDK does not already have is copied, so an SDK
# header is never shadowed by an older one from the disk.
if [ -d "$REPO/disk/DEFS" ]; then
    added=0
    overridden=0
    for f in "$REPO/disk/DEFS"/*; do
        name=$(basename "$f")
        if [ -d "$f" ] && [ -d "$DEST/DEFS/$name" ]; then
            # MERGE, do not skip.  The SDK has its own DEFS/ncurses, so
            # skipping the whole directory left out the collection's
            # ncurses.h -- which is the only reason gnuchess 4.0 wants it.
            for g in "$f"/*; do
                if [ -e "$DEST/DEFS/$name/$(basename "$g")" ]; then
                    # ...UNLESS WE EDITED IT ON PURPOSE.  A header under
                    # disk/DEFS carrying the marker `osk-freeware' is one this
                    # collection has deliberately repaired, and it has to win
                    # over the SDK's copy or the repair is inert.  Four files
                    # in DEFS/GCC2 are in that position -- stdio.h, stdlib.h,
                    # errno.h -- and they only ever worked because somebody
                    # hand-copied them into the overlay.  `build.sh
                    # --from-scratch' is what exposed that: a clean overlay
                    # had the originals back and thirteen builds changed
                    # behaviour with no edit to blame.
                    /usr/bin/grep -ql 'osk-freeware' "$g" 2>/dev/null || continue
                    overridden=$((overridden+1))
                fi
                cp -R "$g" "$DEST/DEFS/$name/"
                added=$((added+1))
            done
            continue
        fi
        [ -e "$DEST/DEFS/$name" ] && continue
        cp -R "$f" "$DEST/DEFS/$name"
        added=$((added+1))
    done
    # ...and auxlib's headers by name too: a program writes <local.h>, not
    # <auxlib/local.h>, and cpp will not search a subdirectory for it.
    if [ -d "$REPO/disk/DEFS/auxlib" ]; then
        for f in "$REPO/disk/DEFS/auxlib"/*.h; do
            name=$(basename "$f")
            [ -e "$DEST/DEFS/$name" ] && continue
            cp "$f" "$DEST/DEFS/$name"
            added=$((added+1))
        done
    fi
    echo "  added $added header(s) from the collection's own DEFS"
    [ "$overridden" -gt 0 ] &&
      echo "  ...$overridden of them replacing an SDK copy, marked osk-freeware"
fi

# blarslib's headers and library, so a recipe can ask for them.  Bob Larson's
# own note says the DEFS directory "cannot and should not be merged with
# /dd/defs, since it supplies replacements which require the /dd/defs version
# as well" -- so it goes in as its own directory and a recipe reaches it with
# -V=/dd/DEFS/blarsdefs.
if [ -d "$REPO/disk/DEFS/blarsdefs" ] && [ ! -d "$DEST/DEFS/blarsdefs" ]; then
    cp -R "$REPO/disk/DEFS/blarsdefs" "$DEST/DEFS/blarsdefs"
    echo "  added blarsdefs"
fi
# ...and its <sys/*.h> into DEFS/sys, for the same reason SRC/COMPAT/sys goes
# there: cpp will not search a -V directory for an include name that has a
# directory in it.  Only names DEFS/sys does not already have, so COMPAT's are
# never shadowed.
if [ -d "$REPO/disk/DEFS/blarsdefs/sys" ]; then
    mkdir -p "$DEST/DEFS/sys"
    for f in "$REPO/disk/DEFS/blarsdefs/sys"/*.h; do
        [ -e "$DEST/DEFS/sys/$(basename "$f")" ] && continue
        cp "$f" "$DEST/DEFS/sys/"
    done
fi
# ...and at /dd/blarsdefs as well, because macutils' sources do not #include
# <sys/types.h> -- they write the ABSOLUTE path "/dd/blarsdefs/sys/types.h",
# which no -V can redirect.
if [ -d "$REPO/disk/DEFS/blarsdefs" ] && [ ! -d "$DEST/blarsdefs" ]; then
    cp -R "$REPO/disk/DEFS/blarsdefs" "$DEST/blarsdefs"
fi
if [ -f "$REPO/disk/LIB/blarslib.l" ]; then
    cp "$REPO/disk/LIB/blarslib.l" "$DEST/LIB/blarslib.l"
    echo "  added blarslib.l"
fi

# DEFS/types.h has no include guard.  It sets `_types' at the BOTTOM and
# nothing at the top, so a source that reaches it twice -- gnuchess 4.0 asks
# for <types.h> and <sys/types.h> both -- gets "multiple definition" on every
# typedef in it.  Wrap it here, in the overlay, where the edit is disposable
# and nothing ships.  The marker is the header's own.
python3 - "$DEST/DEFS/types.h" <<'GUARD'
import sys
p = sys.argv[1]
t = open(p, "rb").read()
if b"_types" in t and not t.lstrip().startswith(b"#ifndef _types"):
    open(p, "wb").write(b"#ifndef _types\r" + t + b"\r#endif\r")
    print("  guarded DEFS/types.h (it had none, and gnuchess reaches it twice)")
GUARD

# ansi2knr, if it has been built.  Recipes flagged KNR run every source
# through it before cc, because Microware's cc is K&R and will not read a
# prototype.  It is not on the disk -- it is a BUILD tool -- so it comes from
# built/, which means `tools/build.sh ansi2knr' has to have been run once.
# A KNR recipe fails with "ansi2knr: command not found" until it has.
if [ -f "$REPO/built/ansi2knr" ]; then
    cp "$REPO/built/ansi2knr" "$DEST/CMDS/ansi2knr"
    chmod 755 "$DEST/CMDS/ansi2knr"
    echo "  added ansi2knr (KNR recipes need it)"
fi

# Make the check fail once before believing it.  If any stamp survives in LIB,
# every binary built through this overlay would carry it.
if grep -rl "from the disk of" "$DEST/LIB" >/dev/null 2>&1; then
    echo "$0: a stamp survived in $DEST/LIB -- do not build with this" >&2
    exit 1
fi

echo
echo "ready.  export OS9CLEAN=$DEST"
