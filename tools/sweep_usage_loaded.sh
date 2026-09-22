#!/bin/bash
# Stage 4, run the way a person runs it: ask every program that is still
# quiet for its usage.  A program that wants arguments is not broken, and
# `-?' is what OS-9 programs answer to.
#
#   USAGE  answered with something when asked
#   MUTE   said nothing bare, nothing with input, and nothing when asked.
#          THAT is the list worth reading, and it is short.
#
# Usage:  tools/sweep_usage_loaded.sh [<image>]
# Input:  notes/verify-filters-loaded.tsv
# Output: notes/verify-usage-loaded.tsv
set -u
here=$(cd "$(dirname "$0")/.." && pwd)
image=${1:-$here/osk-freeware.dd}
exe=${OS9EXEC:-$here/../os9exec/os9exec}
jobs=${JOBS:-6}
src=$here/notes/verify-filters-loaded.tsv
out=$here/notes/verify-usage-loaded.tsv
work=$(mktemp -d)
[ -f "$src" ] || { echo "no $src -- run tools/sweep_filters_loaded.sh first" >&2; exit 2; }

LC_ALL=C awk -F'\t' '$3=="QUIET"{print $1"\t"$2}' "$src" > "$work/list"
total=$(wc -l < "$work/list")
echo "asking $total still-quiet programs for their usage ($jobs at a time)"

cat > "$work/one.sh" <<'WORKER'
#!/bin/bash
prog=$1; dir=$2; work=$3; image=$4; exe=$5
n=$(printf '%s' "$dir/$prog" | /usr/bin/tr -c 'A-Za-z0-9' '_')
h1=$work/h1.$n; mkdir -p "$h1"
# The disk ships no `load'; stage the reader's at /h1/CMDS/load (tools/os9env.py).
python3 -c "import sys; sys.path.insert(0, '$(dirname "$0")'); import os9env; os9env.stage_reader_load('$h1')"
{ printf 'export TERM=vt100\r'
  printf 'export TERMCAP=/dd/SYS/termcap\r'
  printf 'export HOME=/dd\r'
  printf 'export USER=tester\r'
  printf 'export LOGNAME=tester\r'
  printf '/h1/CMDS/load /dd/CMDS/os9lib >/nil 2>/nil\r'
  printf '/dd/%s/%s -?\r' "$dir" "$prog"; } > "$h1/run.sh"
text=$( gtimeout 12 env OS9DISK="$image" OS9H0="$image" OS9H1="$h1" \
          "$exe" -r bash /h1/run.sh < /dev/null 2>&1 \
        | LC_ALL=C /usr/bin/tr -d '\000' | LC_ALL=C /usr/bin/tr '\r' '\n' \
        | /usr/bin/head -c 4000 \
        | LC_ALL=C /usr/bin/grep -v '^#' \
        | LC_ALL=C /usr/bin/grep -v '^[[:space:]]*$' \
        | /usr/bin/head -2 | LC_ALL=C /usr/bin/tr '\n' ' ' \
        | LC_ALL=C /usr/bin/cut -c1-64 )
[ -z "$text" ] && v=MUTE || v=USAGE
printf '%s\t%s\t%s\t%s\n' "$prog" "$dir" "$v" "$text"
rm -rf "$h1"
WORKER
chmod +x "$work/one.sh"
LC_ALL=C /usr/bin/awk -F'\t' '{print $1"\t"$2}' "$work/list" \
  | xargs -P "$jobs" -n 2 -I@ sh -c 'exec "$0" $1 "$2" "$3" "$4" "$5"' \
      "$work/one.sh" @ "$work" "$image" "$exe" 2>/dev/null > "$out.tmp"
sort "$out.tmp" > "$out"; rm -f "$out.tmp"
LC_ALL=C awk -F'\t' '{c[$3]++} END {for (k in c) printf "  %-8s %d\n", k, c[k]}' "$out"
echo "wrote $out ($(wc -l < "$out") of $total rows)"
rm -rf "$work"
