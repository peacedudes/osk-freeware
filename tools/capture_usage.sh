#!/bin/bash
# Ask every undocumented program to describe itself, and keep what it says.
#
#   tools/capture_usage.sh <undocumented.tsv> <out.tsv>
#
# 352 programs on this disk have nothing but their one-line DOC/INDEX entry.
# The pool has no manual for most of them -- checked -- and most never had
# one. What they DO have is their own usage text, and a program's own words
# about itself are worth more than anything a third party could write for it
# forty years later.
#
# This captures, it does not compose. Every line in the output came out of the
# program. Where a program says nothing, that is recorded as nothing rather
# than filled in.
#
# `-?' is the OS-9 convention. It is not universal -- TeX prompts with `**'
# and reads stdin, which is correct behaviour and not a usage message -- so a
# silent result here is not evidence of a broken program.
set -u
here=$(cd "$(dirname "$0")/.." && pwd)
list=${1:?usage: capture_usage.sh <undocumented.tsv> <out.tsv>}
out=${2:?usage: capture_usage.sh <undocumented.tsv> <out.tsv>}
exe=${OS9EXEC:-$here/../os9exec/os9exec}
image=${OS9IMAGE:-$here/osk-freeware.dd}

[ -x "$exe" ]   || { echo "no os9exec at $exe" >&2; exit 2; }
[ -f "$image" ] || { echo "no image at $image" >&2; exit 2; }

: > "$out"
n=0
while IFS=$'\t' read -r prog dir rest; do
  case "$prog" in program|"") continue;; esac
  n=$((n+1))
  # `head -c` closes the pipe, so a chatty program finishes at once instead of
  # running out the timeout. It is what keeps this at minutes, not hours.
  text=$( gtimeout 6 env OS9DISK="$image" "$exe" -r "/dd/$dir/$prog" '-?' </dev/null 2>&1 \
          | /usr/bin/tr -d '\000' \
          | LC_ALL=C /usr/bin/sed $'s/\033\\[[0-9?;]*[a-zA-Z=]//g' \
          | LC_ALL=C /usr/bin/grep -av '^#' \
          | /usr/bin/head -c 600 \
          | LC_ALL=C /usr/bin/tr '\r' '\n' \
          | LC_ALL=C /usr/bin/grep -av '^[[:space:]]*$' \
          | /usr/bin/head -4 \
          | LC_ALL=C /usr/bin/tr '\n' '|' )
  printf '%s\t%s\t%s\n' "$prog" "$dir" "$text" >> "$out"
done < "$list"

got=$(awk -F'\t' '$3!=""' "$out" | wc -l | tr -d ' ')
echo "  asked $n programs, $got answered" >&2
[ "$(wc -l < "$out")" -eq "$n" ] || echo "  INCOMPLETE: $(wc -l < "$out") rows of $n" >&2
