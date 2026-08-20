#!/bin/bash
# Compare a relinked binary against the one currently on the disk, and say
# whether it is safe to swap.
#
#   tools/rebuild/compare_relink.sh <relink-results.tsv> <relink-outdir>
#
# Smaller is not better if it is broken. `wc.cio' is 10 times smaller than the
# trap-free `wc' and prints NOTHING for a file argument, where the trap-free
# one correctly reports "81 455 3157". That one was caught only because each
# swap was tested individually, so every swap gets tested individually.
#
# Each program is run twice against the same input -- once as it is on the
# disk, once from the relink output -- and the two captures compared.
#
# Verdicts:
#   SAME        byte-identical output; safe to swap
#   BOTH-QUIET  neither printed anything; no evidence either way, do NOT swap
#   DIFFERENT   outputs differ; a human decides
#   NEW-BROKEN  the old one spoke and the new one did not
#   NEW-SPEAKS  the new one spoke and the old one did not (an improvement)
#
# os9exec's own `#' lines are kept in the capture: they carry E_BMID, E_NEMOD
# and `unintialized User Trap', and filtering them once scored 91 programs
# that do not load at all as working.
set -u
here=$(cd "$(dirname "$0")/../.." && pwd)
results=${1:?usage: compare_relink.sh <results.tsv> <outdir>}
outdir=${2:?usage: compare_relink.sh <results.tsv> <outdir>}
exe=${OS9EXEC:-$here/../os9exec/os9exec}
image=${OS9IMAGE:-$here/osk-freeware.dd}
secs=${TIMEOUT:-10}

[ -x "$exe" ]   || { echo "no os9exec at $exe" >&2; exit 2; }
[ -f "$image" ] || { echo "no image at $image" >&2; exit 2; }

# Run one binary from a module directory, capture what a user would see.
# `head -c` closes the pipe so chatty programs finish at once instead of
# running out the timeout -- it is what keeps a sweep at one hour, not seven.
capture() {   # $1 = module dir  $2 = program name
  gtimeout "$secs" env OS9DISK="$image" OS9MDIR="$1" "$exe" -r "$2" </dev/null 2>&1 \
    | /usr/bin/tr -d '\000' \
    | LC_ALL=C /usr/bin/sed $'s/\033\\[[0-9?;]*[a-zA-Z=]//g' \
    | LC_ALL=C /usr/bin/grep -av '^# /h0:' \
    | /usr/bin/head -c 2000
}

printf 'program\told\tnew\tdelta\tverdict\n'
while IFS=$'\t' read -r prog tree old new delta verdict; do
  [ "$verdict" = "built" ] || continue
  [ -f "$outdir/$prog/$prog" ] || continue

  cur=$(find "$here/disk/CMDS" -name "$prog" -type f | head -1)
  [ -n "$cur" ] || continue

  # Each binary needs its own directory, or OS9MDIR finds the wrong one.
  tmp=$outdir/.cmp.$prog; rm -rf "$tmp"; mkdir -p "$tmp/old" "$tmp/new"
  cp "$cur" "$tmp/old/$prog"; cp "$outdir/$prog/$prog" "$tmp/new/$prog"

  a=$(capture "$tmp/old" "$prog")
  b=$(capture "$tmp/new" "$prog")
  rm -rf "$tmp"

  if   [ "$a" = "$b" ] && [ -n "$a" ]; then v=SAME
  elif [ -z "$a" ] && [ -z "$b" ];      then v=BOTH-QUIET
  elif [ -n "$a" ] && [ -z "$b" ];      then v=NEW-BROKEN
  elif [ -z "$a" ] && [ -n "$b" ];      then v=NEW-SPEAKS
  else                                       v=DIFFERENT
  fi
  printf '%s\t%s\t%s\t%s\t%s\n' "$prog" "$old" "$new" "$delta" "$v"
done < "$results"
