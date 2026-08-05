#!/bin/bash
#
# Check that each rebuilt module actually forks, and that its module name
# matches its filename.  Reads rebuild.sh's results.tsv; writes the same rows
# back with a verdict column.
#
# Usage:  verify.sh <results.tsv> <source-pool> [<second-pool>]
#
# An empty capture must NOT read as success.  An earlier version of this lost
# `tr` from PATH, so the captured output was always empty and the "can't
# execute" test could never match -- it reported 20/20 OK having run nothing.
# Absolute tool paths, and NOOUTPUT is its own verdict rather than a pass.
#
set -u

RESULTS=$1
POOL1=$2
POOL2=${3:-$POOL1}

HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/../.." && pwd)
: "${OS9CLEAN:?set OS9CLEAN to the clean /dd overlay}"
WORK=${TMPDIR:-/tmp}/os9verify.$$
mkdir -p "$WORK"
trap 'rm -rf "$WORK"' EXIT
: > "$WORK/empty"

OUT=${OUT:-${RESULTS%.tsv}_verified.tsv}; : > "$OUT"

# The module's own name, read from the header: M$Name at 0x0C is a 4-byte
# offset to a high-bit-terminated string.  A name that does not match the
# filename means the build did not pass -n, and the program will report the
# wrong name in its own usage text.
modname() { /usr/bin/python3 -c '
import sys, struct
b = open(sys.argv[1], "rb").read()
if b[:2] != b"\x4a\xfc": print(""); raise SystemExit
off = struct.unpack(">I", b[0x0C:0x10])[0]
out = bytearray()
for i in range(off, min(off + 48, len(b))):
    c = b[i]
    if c & 0x7F < 0x20: break
    out.append(c & 0x7F)
    if c & 0x80: break
print(out.decode("latin-1", "replace").split()[0] if out else "")' "$1"; }

while IFS=$'\t' read -r prog arch st path; do
  [ "$st" = clean ] || continue
  if [ -d "$POOL1/$arch" ]; then POOL=$POOL1; else POOL=$POOL2; fi

  name=$(modname "$path")
  if [ "$name" != "$prog" ]; then
    printf '%s\t%s\t%s\tBADNAME(%s)\n' "$prog" "$arch" "$path" "$name" >> "$OUT"; continue
  fi
  if /usr/bin/grep -qa 'from the disk of' "$path"; then
    printf '%s\t%s\t%s\tSTAMPED\n' "$prog" "$arch" "$path" >> "$OUT"; continue
  fi

  printf 'chx /dd/CMDS\n/h6/%s </h7/empty\n\033\n\004\n' "${path#$POOL/}" > "$WORK/cmd"
  out=$( cd "$REPO" && gtimeout 60 env OS9DISK="$OS9CLEAN" OS9H6="$POOL" OS9H7="$WORK" \
           ./os9exec -r shell < "$WORK/cmd" 2>&1 | /usr/bin/tr -d '\000' )

  if [ -z "$out" ];                                        then v=NOOUTPUT
  elif printf '%s' "$out" | /usr/bin/grep -q "can't execute"; then v=FAIL
  else v=OK; fi
  printf '%s\t%s\t%s\t%s\n' "$prog" "$arch" "$path" "$v" >> "$OUT"
done < "$RESULTS"

/usr/bin/awk -F'\t' '{c[$4]++} END {for (k in c) printf "  %s=%d\n", k, c[k]}' "$OUT"
echo "  verified: $OUT"
