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

# Make the check fail once before believing it.  If any stamp survives in LIB,
# every binary built through this overlay would carry it.
if grep -rl "from the disk of" "$DEST/LIB" >/dev/null 2>&1; then
    echo "$0: a stamp survived in $DEST/LIB -- do not build with this" >&2
    exit 1
fi

echo
echo "ready.  export OS9CLEAN=$DEST"
