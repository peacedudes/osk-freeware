#!/bin/bash
# Second half of the sweep.  verify_all.sh runs every program with nothing on
# its standard input; a filter at end-of-file correctly prints nothing, so it
# lands in the SILENT pile alongside anything genuinely dead.  This script runs
# the SILENT ones again with real text on stdin and separates the two:
#
#   FILTER  produced output when given input -- working, and the large majority
#   QUIET   printed nothing either way -- read DOC/STATUS before concluding
#           anything; most of the QUIET set is correct too (generators that
#           want options, a program that writes to a pipe, a timer that waits)
#
# Usage:  tools/verify_filters.sh [<image>]
# Env:    OS9EXEC   path to the os9exec binary (default ../os9exec/os9exec)
# Input:  notes/verify-bare.tsv    written by verify_all.sh
# Output: notes/verify-filters.tsv program, directory, verdict, first output

set -u
here=$(cd "$(dirname "$0")/.." && pwd)
image=${1:-$here/osk-freeware.dd}
exe=${OS9EXEC:-$here/../os9exec/os9exec}
bare=$here/notes/verify-bare.tsv
out=$here/notes/verify-filters.tsv
list=$(mktemp)
feed=$(mktemp)

[ -x "$exe" ]   || { echo "no os9exec at $exe -- set OS9EXEC" >&2; exit 2; }
[ -f "$bare" ]  || { echo "no $bare -- run tools/verify_all.sh first" >&2; exit 2; }

printf 'the quick brown fox\njumped over 3 lazy dogs\nthe quick brown fox\n' > "$feed"
LC_ALL=C awk -F'\t' '$3=="SILENT"{print $1"\t"$2}' "$bare" > "$list"
total=$(wc -l < "$list")
echo "re-running $total silent programs with input"

: > "$out"
while IFS=$'\t' read -r prog dir; do
  # Same rule as verify_all.sh: os9exec's own '#' lines are not program
  # output, and a blank line is not output either.  Judging on raw non-empty
  # text called a missing program a working filter.
  # EVERY tool in this pipeline needs LC_ALL=C. Without it `tr' and `cut'
  # abort with "Illegal byte sequence" on the first 8-bit byte a program
  # emits, and that program is then judged on an empty capture -- QUIET,
  # which reads as dead. Measured 2026-08-26: it hit two programs here and
  # five in verify_all.sh.
  text=$( cd "$here" && gtimeout 10 env OS9DISK="$image" OS9H0="$image" \
            "$exe" -r "/dd/$dir/$prog" < "$feed" 2>&1 \
          | LC_ALL=C /usr/bin/tr -d '\000' | LC_ALL=C /usr/bin/tr '\r' '\n' \
          | /usr/bin/head -c 4000 \
          | LC_ALL=C /usr/bin/grep -v '^#' \
          | LC_ALL=C /usr/bin/grep -v '^[[:space:]]*$' \
          | /usr/bin/head -2 | LC_ALL=C /usr/bin/tr '\n' ' ' \
          | LC_ALL=C /usr/bin/cut -c1-64 )
  [ -z "$text" ] && v=QUIET || v=FILTER
  printf '%s\t%s\t%s\t%s\n' "$prog" "$dir" "$v" "$text" >> "$out"
done < "$list"

wrote=$(wc -l < "$out")
rm -f "$list" "$feed"
LC_ALL=C awk -F'\t' '{c[$3]++} END {for (k in c) printf "  %-8s %d\n", k, c[k]}' "$out"
[ "$wrote" -eq "$total" ] || { echo "INCOMPLETE: $wrote of $total rows" >&2; exit 1; }
echo "wrote $out ($wrote rows)"
