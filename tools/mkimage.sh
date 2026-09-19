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
#   * `sh` has the real `chd` this needs, and once the working directory is
#     the new image it can no longer find `tar` -- it resolves a bare name
#     against the data directory, and refuses an absolute pathname outright.
#     So `tar` is LOADED INTO THE MODULE DIRECTORY first, by the collection's
#     own `load`, and F$Fork then finds it without touching the filesystem.
#     This used to be done with os9exec's OS9MDIR environment variable, which
#     is an emulator mechanism rather than an OS-9 one; `load` is the OS-9
#     answer and the disk now carries it.
#   * To use the result as both /dd and /h0 under os9exec, name it twice:
#     OS9DISK=<image> OS9H0=<image>.  No link is needed.
set -u

SRC=${1:-}; OUT=${2:-}; MB=${3:-0}

# BOTH PATHS ARE MADE ABSOLUTE, and the source one is the reason.  The
# extract step below cd's to the output directory, and passes $SRC to the
# emulator as OS9DISK from THERE -- so a relative `disk' works only when the
# image is written into the repository root, and anywhere else the emulator
# stops with `#000:221 (E_MNF): bash' before emulation begins, which reads
# exactly like a source tree with no shell on it.  Measured 2026-09-18,
# building into a scratch directory.
[ -n "$SRC" ] && [ -d "$SRC" ] && SRC=$(cd "$SRC" && pwd)
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

# CLUSTER SIZE, and why this is not always 1. RBF's allocation bitmap holds one
# bit per cluster, and `mount -k' cannot address more than 512000 sectors of
# 256 bytes -- 125 MiB -- at one sector per cluster. Ask for more and it stops
# with "cluster size is too small for this device", which reads like a bad
# argument and is really the disk having outgrown the geometry. The collection
# crossed that line in August 2026. Double the cluster until the sector count
# fits; os9exec reports the minimum it needs, so this agrees with it.
SECTORS_PER_MB=4096
MAX_SECTORS=512000
CLUSTER=1
while [ $(( MB * SECTORS_PER_MB / CLUSTER )) -gt $MAX_SECTORS ]; do
  CLUSTER=$(( CLUSTER * 2 ))
done

# .DS_Store IS NOT A DECISION.  macOS's Finder writes one into any directory
# it looks at, including this one, and it reappears between a `rm' and the
# next command.  It is gitignored, it can never belong on an OS-9 disk, and
# leaving it to `check_disk' means a build that fails at random depending on
# whether somebody opened a window.  Removed here, quietly, before anything
# looks at the tree -- every other leftover the check names is a real one.
find "$SRC" -name .DS_Store -delete 2>/dev/null || true

nfiles=$(find "$SRC" -type f | wc -l | tr -d ' ')
ndirs=$(find "$SRC" -mindepth 1 -type d | wc -l | tr -d ' ')
echo "  $SRC ($(du -sh "$SRC" | cut -f1)) -> ${MB}M image, cluster $CLUSTER, volume '$VOL'"
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

# THE IMAGE LOCK. `screenshots.py', `playtest.py', `datatest.py' and
# `drive.py' all take it before pointing os9exec at the image; this did not,
# and it is the one thing here that REPLACES the image rather than writing
# inside it. A rebuild while a half-hour datatest run was reading the same
# file would swap the disk out from under a live OS-9 kernel, and the
# results would be wrong in ways nothing would explain afterwards.
#
# `tools/imagelock.py' is Python and this is bash, so the lock is taken by
# hand in the same format: the file beside the image holds `<pid> <who>'.
# Advisory, never stolen -- a stale lock is reported by name, exactly as the
# Python side does, because a lock that breaks itself is not a lock.
LOCK="$OUT.lock"
if ! ( set -o noclobber; echo "$$ mkimage" > "$LOCK" ) 2>/dev/null; then
  owner=$(cat "$LOCK" 2>/dev/null || echo "an unreadable lock file")
  pid=${owner%% *}
  if [ -n "$pid" ] && ! kill -0 "$pid" 2>/dev/null; then
    echo "mkimage: $(basename "$OUT") is locked by $owner, which is no longer running."
    echo "   Remove $LOCK if you are sure nothing else is using it."
  else
    echo "mkimage: $(basename "$OUT") is in use by $owner -- wait for it to finish."
    echo "   Rebuilding under a running harness swaps the disk out from under it."
  fi
  exit 1
fi

TMP=$(mktemp -d)
# $WORK is removed too. A failed run that left its half-built image behind
# would make the NEXT run refuse with "already exists", which reads like a
# second, different fault. On success the mv has already taken it away.
trap 'rm -rf "$TMP"; rm -f "$WORK"; rm -f "$LOCK"' EXIT

# ---- 1. the archive, host-side
python3 "$HERE/mktar.py" "$SRC" "$TMP/collection.tar" || exit 1

# ---- 2. the blank image, written by the emulator into $OUTDIR
( cd "$OUTDIR" && "$EXEC" -r mount -k="${MB}M" -c="$CLUSTER" -v="$VOL" "$DEV" ) 2>&1 \
  | tr -d '\000' | grep -aiE "error|cannot" && { echo "  FAILED: mount -k"; exit 1; }
[ -e "$WORK" ] || { echo "  FAILED: mount -k created no image at $WORK"; exit 1; }

# ---- 3. populate, using the collection's own tar
# Verbose on purpose: the count of extracted files is the only honest check
# that anything happened. This collection has produced a builder that
# reported "copied 3287/3287" while every copy failed.
printf '/dd/CMDS/load /dd/CMDS/tar\r/dd/CMDS/sh -c "chd /%s; tar xvf /h6/collection.tar"\r' \
      "$DEV" > "$TMP/extract.sh"
( cd "$OUTDIR" && env OS9DISK="$SRC" \
      "OS9H${DEV#h}=$WORK" OS9H6="$TMP" \
      "$EXEC" -r bash /h6/extract.sh ) 2>&1 \
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

# tar ignores the mode on a directory entry and applies its own, which leaves
# every directory read-only. Nothing can then create a file in it -- advent
# cannot write glorkz, larn cannot post a score -- and it is not a question of
# who you are logged in as. `makdir` gave d-ewrewr; this restores that.
python3 "$HERE/fixattrs.py" "$WORK" || exit 1

mv "$WORK" "$OUT"
# The image is the one thing this writes.  A tar of the tree used to be left
# beside it as a second download for real OS-9 systems; rdoggett withdrew it
# on 2026-09-13 -- one download is cleaner, and it can come back if someone
# with a real system needs it.  $TMP/collection.tar above is still how the
# image gets filled.
echo "  wrote $OUT ($(du -h "$OUT" | cut -f1))"
