#!/bin/bash
#
# Build the collection's programs from source.  One command, no setup.
#
#     tools/build.sh              build everything there is a recipe for
#     tools/build.sh ls cat vi    build just these
#     tools/build.sh --list       what can be built, and from which tree
#     tools/build.sh --missing    programs with no recipe yet
#
# rdoggett, 2026-08-22: "You are to build everything, and make it easily
# buildable on demand."  This is the on-demand part.  Everything it needs it
# works out or makes:
#
#   * the clean /dd overlay, via tools/rebuild/make_overlay.sh, cached in
#     $TMPDIR so the second run does not pay for it again
#   * the SDK location, from tools/paths.py
#   * the os9exec binary, from $OS9EXEC or the sibling checkout
#
# It INSTALLS NOTHING.  Each build lands beside its sources as R_<program>,
# and what goes onto the disk stays a decision somebody makes on purpose --
# that is tools/rebuild/rebuild.sh's rule and it is a good one.
#
# WHY THE SOURCE IS NOT ALWAYS ENOUGH
#
# Roughly a third of the collection has source here at all; most programs
# arrived as binaries with nothing behind them and can only be preserved.  Of
# the trees that DO have source, the ones with a recipe are known to compile,
# because that is what a recipe means.  `--missing' lists the rest.  See
# notes/COMPILE-VERIFY.md, and tools/try_compile.sh for settling one of them.
set -u

here=$(cd "$(dirname "$0")/.." && pwd)
recipes=$here/tools/rebuild/recipes.psv
overlay=${OS9CLEAN:-${TMPDIR:-/tmp}/os9clean}

case "${1:-}" in
  --list)
    printf '%-18s %-16s %s\n' PROGRAM TREE SOURCES
    grep -v '^[[:space:]]*\(#\|$\)' "$recipes" |
      while IFS='|' read -r prog tree srcs rest; do
        printf '%-18s %-16s %s\n' "$prog" "$tree" "$(echo "$srcs" | cut -c1-46)"
      done
    exit 0;;
  --missing)
    python3 - "$here" <<'PY'
import os, sys
here = sys.argv[1]
trees = {d for d in os.listdir(os.path.join(here, "disk/SRC"))
         if os.path.isdir(os.path.join(here, "disk/SRC", d))}
rec = set()
for line in open(os.path.join(here, "tools/rebuild/recipes.psv")):
    if line.startswith("#") or not line.strip():
        continue
    # A recipe may name a SUBDIRECTORY -- `chess/CH5', `hist/SRC' -- so the
    # tree it covers is the first component. Comparing the whole string
    # reported chess and others as unrecipe'd when they are not.
    rec.add(line.split("|")[1].strip().split("/")[0])
missing = sorted(trees - rec)
print(f"{len(trees)} source trees, {len(trees) - len(missing)} with a recipe, "
      f"{len(missing)} without:\n")
for i in range(0, len(missing), 5):
    print("   " + "".join(f"{n:<17}" for n in missing[i:i+5]))
print("\ntools/try_compile.sh <tree> <program> tries one and says what stopped it.")
print("notes/COMPILE-AUDIT.md says why each of these has none -- read it first,")
print("because most of them are accounted for and only some are work.")
PY
    exit 0;;
esac

# The overlay is the one prerequisite, and it used to be somebody's undocumented
# local directory -- which is how the whole rebuild machinery came to be
# unusable when it went missing.  Make it if it is not there.
if [ ! -d "$overlay/LIB" ]; then
    echo "building the clean /dd overlay in $overlay ..."
    "$here/tools/rebuild/make_overlay.sh" "$overlay" >/dev/null || exit 1
fi
export OS9CLEAN=$overlay
export OS9COMPAT=${OS9COMPAT:-$here/disk/SRC/COMPAT}

if [ $# -eq 0 ]; then
    use=$recipes
else
    # Build only the named programs, by filtering the recipe file.
    use=$(mktemp)
    trap 'rm -f "$use"' EXIT
    for want in "$@"; do
        grep "^$want|" "$recipes" >> "$use" || echo "no recipe for '$want'" >&2
    done
    [ -s "$use" ] || { echo "nothing to build"; exit 1; }
fi

"$here/tools/rebuild/rebuild.sh" "$use" "$here/disk/SRC"
status=$?

# TIDY THE TREE -- by calling the one script that does it, not a second copy.
# Every recipe compiles IN PLACE: cc writes `foo.r' beside `foo.c' and l68
# writes the module as `R_<prog>'.  `mkimage.sh' reads `disk/' off the
# filesystem, so a build immediately before an image build shipped 77 object
# files, five temporaries and -- worse -- fourteen of the ARCHIVES' OWN `.r'
# files, overwritten by ours.  `check_disk.py' refuses a tree with build
# products in it; this is what keeps that check quiet.
#
# It used to be an inline copy of `tools/rebuild/tidy.sh', and the copies
# drifted: tidy.sh learned to delete `ctmp_<base>.c' when the KNR path started
# writing one per source, and this did not.  A full build then finished saying
# "the tree is left as it was found" and left 228 files in it, which is exactly
# the check that then failed.  One implementation, called from both places.
"$here/tools/rebuild/tidy.sh"
built=$(find "$here/built" -type f 2>/dev/null | wc -l | tr -d ' ')
echo "  $built module(s) in $here/built/  (the tree is left as it was found)"
exit $status
