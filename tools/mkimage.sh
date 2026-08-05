#!/bin/bash
# Build an RBF disk image from a host directory tree.
#
#   mkimage.sh <source-tree> <output-image> [sizeMB]
#
# NO MICROWARE UTILITY IS USED, and that is the point. The old build drove
# `chx`, `makdir`, `copy` and `attr` out of a licensed OS-9 system disk, so it
# could not run anywhere that disk was absent -- which is every CI machine.
# Three pieces replace all four commands:
#
#   1. os9exec's own `mount -k` writes the blank image. It is an internal
#      command of the emulator, not an OS-9 program, so it needs no disk.
#   2. tools/mktar.py writes the tree as a ustar archive, host-side, with the
#      finished disk's ATTRIBUTES already in the mode bits.
#   3. The collection's OWN `tar` extracts it. GNU tar 1.10, unstarred, so it
#      runs with no `cio` -- the disk populates itself. `cp` and `mkdir` are
#      on the disk too but both are starred, so neither could do this.
#
# Because the attributes ride in the archive, there is no `attr` pass at all.
#
# Things that will bite you, all of them found the hard way:
#
#   * `mount -k` creates <CWD>/hX and IGNORES OS9Hx. So this script cd's to
#     the output directory first. Do not "fix" that by setting OS9Hz.
#   * OS-9 does not group command-line arguments with quotes, so a volume
#     name CANNOT contain a space. Refused below rather than silently split.
#   * F$Load searches the execution directory, which `chd /hz` moves away
#     from. OS9MDIR loads modules regardless of the data directory, which is
#     what lets tar keep running once the working directory is the image.
#   * os9exec will not mount one host path as two devices. To use the result
#     as both /dd and /h0, hard-link it: `ln osk-freeware.dd h0`.
set -u

SRC=${1:-}; OUT=${2:-}; MB=${3:-0}
[ -n "$SRC" ] && [ -n "$OUT" ] || { echo "usage: mkimage.sh <source-tree> <output-image> [sizeMB]"; exit 1; }
[ -d "$SRC" ] || { echo "no such tree: $SRC"; exit 1; }

HERE=$(cd "$(dirname "$0")" && pwd)

# os9exec: honour OS9EXEC_DIR, else take it from PATH. Its system disk is NOT
# needed -- only the emulator binary.
if [ -n "${OS9EXEC_DIR:-}" ]; then
  EXEC=$OS9EXEC_DIR/os9exec
else
  EXEC=$(command -v os9exec || true)
fi
[ -x "$EXEC" ] || { echo "no os9exec -- set OS9EXEC_DIR or put it on PATH"; exit 1; }

# The disk populates itself, so the source tree must carry its own tar and sh.
for m in tar sh; do
  [ -f "$SRC/CMDS/$m" ] || { echo "source tree has no CMDS/$m -- it cannot populate itself"; exit 1; }
done

# A volume name cannot contain a space; see the header.
VOL=${RBF_VOLNAME:-OSK-Freeware}
case $VOL in
  *" "*) echo "volume name must not contain a space: '$VOL'"; exit 1 ;;
esac

DEV=hz
OUTDIR=$(cd "$(dirname "$OUT")" && pwd)
WORK=$OUTDIR/$DEV
[ -e "$WORK" ] && { echo "refusing: $WORK already exists"; exit 1; }

# Room to work in, not room for its own sake: score files, saves, /dd/tmp for
# flex and rayshade. Content plus ~90% is generous without being silly.
[ "$MB" -eq 0 ] && MB=$(( $(du -sm "$SRC" | cut -f1) * 19 / 10 + 8 ))

nfiles=$(find "$SRC" -type f | wc -l | tr -d ' ')
ndirs=$(find "$SRC" -mindepth 1 -type d | wc -l | tr -d ' ')
echo "  $SRC ($(du -sh "$SRC" | cut -f1)) -> ${MB}M image, volume '$VOL'"
echo "  $ndirs dirs, $nfiles files"

# The image is built from the working tree, not from git, so .gitignore is no
# protection: a vim swap file sitting in disk/ would be packed into what ships.
# Two seconds here is cheaper than finding out after release. SKIP_CHECKS=1
# exists for bisecting a build, not for routine use.
if [ "${SKIP_CHECKS:-0}" != "1" ]; then
  "$HERE/check_disk.py" "$SRC" || {
    echo "  refusing to build from a tree that fails its own checks"
    echo "  (set SKIP_CHECKS=1 to override, and know why you are doing it)"
    exit 1
  }
fi

TMP=$(mktemp -d)
# $WORK is removed too. A failed run that left its half-built image behind
# would make the NEXT run refuse with "already exists", which reads like a
# second, different fault. On success the mv has already taken it away.
trap 'rm -rf "$TMP"; rm -f "$WORK"' EXIT

# ---- 1. the archive, host-side
python3 "$HERE/mktar.py" "$SRC" "$TMP/collection.tar" || exit 1

# ---- 2. the blank image, written by the emulator into $OUTDIR
( cd "$OUTDIR" && "$EXEC" -r mount -k="${MB}M" -v="$VOL" "$DEV" ) 2>&1 \
  | tr -d '\000' | grep -aiE "error|cannot" && { echo "  FAILED: mount -k"; exit 1; }
[ -e "$WORK" ] || { echo "  FAILED: mount -k created no image at $WORK"; exit 1; }

# ---- 3. populate, using the collection's own tar
# Verbose on purpose: the count of extracted files is the only honest check
# that anything happened. This collection has produced a builder that
# reported "copied 3287/3287" while every copy failed.
( cd "$OUTDIR" && env OS9DISK="$SRC" OS9MDIR="$SRC/CMDS" \
      "OS9H${DEV#h}=$WORK" OS9H6="$TMP" \
      "$EXEC" -r sh -c "chd /$DEV; tar xvf /h6/collection.tar" ) 2>&1 \
  | tr -d '\000' > "$TMP/out"

if grep -aiE "cannot create|no more memory|error #" "$TMP/out" | head -4 | grep -q .; then
  echo "  FAILED -- the emulator reported:"
  grep -aiE "cannot create|no more memory|error #" "$TMP/out" | head -4 | sed 's/^/    /'
  exit 1
fi

got=$(grep -ac '^x ' "$TMP/out")
if [ "$got" -ne "$nfiles" ]; then
  echo "  FAILED: tar extracted $got files, expected $nfiles"
  exit 1
fi
echo "  extracted $got/$nfiles files"

mv "$WORK" "$OUT"
echo "  wrote $OUT ($(du -h "$OUT" | cut -f1))"
