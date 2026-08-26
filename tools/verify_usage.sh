#!/bin/bash
# Fourth and last stage.  Everything the first three stages left behind gets
# asked `-?`, which is the OS-9 convention for "print your usage line".
#
# Most of what survives to here wants arguments: `dir`, `find`, `make`,
# `banner`, `tex` and `cxref` have nothing to say when handed nothing, and a
# program that answers `-?` with a syntax line is working, not broken.  What is
# still silent after this is the genuinely quiet set, and it is short enough to
# look at by hand.
#
# Usage:  tools/verify_usage.sh [<image>]
# Env:    OS9EXEC   path to the os9exec binary (default ../os9exec/os9exec)
# Input:  notes/verify-session.tsv   written by verify_in_session.sh
# Output: notes/verify-usage.tsv     program, directory, verdict, evidence
#
# Verdicts: USAGE-OK   answered -? with something
#           NO-USAGE   silent even then

set -u
here=$(cd "$(dirname "$0")/.." && pwd)
image=${1:-$here/osk-freeware.dd}
exe=${OS9EXEC:-$here/../os9exec/os9exec}
session=$here/notes/verify-session.tsv
out=$here/notes/verify-usage.tsv
list=$(mktemp)
raw=$(mktemp)

[ -x "$exe" ]      || { echo "no os9exec at $exe -- set OS9EXEC" >&2; exit 2; }
[ -f "$session" ]  || { echo "no $session -- run tools/verify_in_session.sh first" >&2; exit 2; }

# Only the ones that said nothing at all.  A program that already printed a
# diagnostic has been heard from and belongs in the report, not here.
LC_ALL=C awk -F'\t' '$3=="STILL-BAD" && $4==""{print $1"\t"$2}' "$session" > "$list"
total=$(wc -l < "$list")
echo "asking $total programs for their usage line"

: > "$out"
while IFS=$'\t' read -r prog dir; do
  printf '/dd/%s/%s -?\nexit\n' "$dir" "$prog" \
    | gtimeout 20 env OS9DISK="$image" OS9H0="$image" \
        "$exe" -r bash /dd/SYS/login 2>&1 \
    | LC_ALL=C /usr/bin/tr -d '\000' | LC_ALL=C /usr/bin/tr '\r' '\n' \
    | /usr/bin/head -c 8000 > "$raw"

  text=$( LC_ALL=C /usr/bin/grep -vE '^#|^os9\$|^OS-9 freeware|^cat and less|^exit$|^$' "$raw" \
          | LC_ALL=C /usr/bin/grep -vF "/dd/$dir/$prog" \
          | /usr/bin/head -3 | LC_ALL=C /usr/bin/tr '\n' ' ' | LC_ALL=C /usr/bin/cut -c1-100 )

  if [ -n "$text" ] \
     && ! printf '%s' "$text" | LC_ALL=C /usr/bin/grep -qiE 'Exception:|Exit code|could not start|trap handler|User Trap|Illegal instruction|No more memory|command not found'; then
    v=USAGE-OK
  else
    v=NO-USAGE
  fi
  printf '%s\t%s\t%s\t%s\n' "$prog" "$dir" "$v" "$text" >> "$out"
done < "$list"

wrote=$(wc -l < "$out")
rm -f "$list" "$raw"
LC_ALL=C awk -F'\t' '{c[$3]++} END {for (k in c) printf "  %-10s %d\n", k, c[k]}' "$out"
[ "$wrote" -eq "$total" ] || { echo "INCOMPLETE: $wrote of $total rows" >&2; exit 1; }
echo "wrote $out ($wrote rows)"
