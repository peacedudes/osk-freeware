#!/bin/bash
# Stage 2, run the way a person runs it: every program that came back SILENT
# from `tools/sweep_loaded.sh' gets real text on its standard input, from
# bash, with the environment SYS/login sets and the library modules loaded.
#
# A FILTER AT END-OF-FILE CORRECTLY PRINTS NOTHING, which is why stage 1
# leaves hundreds of working programs in the SILENT pile.  This separates
# them:
#
#   FILTER  produced output when given input -- working
#   QUIET   printed nothing either way.  Read DOC/STATUS before concluding
#           anything: most of the QUIET set is correct too -- generators
#           that want options, a daemon that writes to a pipe, a timer
#
# Usage:  tools/sweep_filters_loaded.sh [<image>]
# Env:    OS9EXEC   path to os9exec       JOBS  parallel runs (default 6)
# Input:  notes/verify-loaded.tsv
# Output: notes/verify-filters-loaded.tsv
set -u
here=$(cd "$(dirname "$0")/.." && pwd)
image=${1:-$here/osk-freeware.dd}
exe=${OS9EXEC:-$here/../os9exec/os9exec}
jobs=${JOBS:-6}
src=$here/notes/verify-loaded.tsv
out=$here/notes/verify-filters-loaded.tsv
work=$(mktemp -d)

[ -x "$exe" ]  || { echo "no os9exec at $exe -- set OS9EXEC" >&2; exit 2; }
[ -f "$image" ] || { echo "no image at $image" >&2; exit 2; }
[ -f "$src" ]  || { echo "no $src -- run tools/sweep_loaded.sh first" >&2; exit 2; }

printf 'the quick brown fox\rjumped over 3 lazy dogs\rthe quick brown fox\r' > "$work/feed"
LC_ALL=C awk -F'\t' '$3=="SILENT"{print $1"\t"$2}' "$src" > "$work/list"
total=$(wc -l < "$work/list")
echo "re-running $total silent programs with input ($jobs at a time)"

cat > "$work/one.sh" <<'WORKER'
#!/bin/bash
prog=$1; dir=$2; work=$3; image=$4; exe=$5
n=$(printf '%s' "$dir/$prog" | /usr/bin/tr -c 'A-Za-z0-9' '_')
h1=$work/h1.$n; mkdir -p "$h1"
# The disk ships no `load'; stage the reader's at /h1/CMDS/load (tools/os9env.py).
python3 -c "import sys; sys.path.insert(0, '$(dirname "$0")'); import os9env; os9env.stage_reader_load('$h1')"
cp "$work/feed" "$h1/feed"
# The program reads /h1/feed rather than the harness's stdin, because bash is
# what is being started and its own stdin is not the program's.
{ printf 'export TERM=vt100\r'
  printf 'export TERMCAP=/dd/SYS/termcap\r'
  printf 'export HOME=/dd\r'
  printf 'export USER=tester\r'
  printf 'export LOGNAME=tester\r'
  printf '/h1/CMDS/load /dd/CMDS/os9lib >/nil 2>/nil\r'
  printf '/dd/%s/%s < /h1/feed\r' "$dir" "$prog"; } > "$h1/run.sh"
text=$( gtimeout 12 env OS9DISK="$image" OS9H0="$image" OS9H1="$h1" \
          "$exe" -r bash /h1/run.sh < /dev/null 2>&1 \
        | LC_ALL=C /usr/bin/tr -d '\000' | LC_ALL=C /usr/bin/tr '\r' '\n' \
        | /usr/bin/head -c 4000 \
        | LC_ALL=C /usr/bin/grep -v '^#' \
        | LC_ALL=C /usr/bin/grep -v '^[[:space:]]*$' \
        | /usr/bin/head -2 | LC_ALL=C /usr/bin/tr '\n' ' ' \
        | LC_ALL=C /usr/bin/cut -c1-64 )
[ -z "$text" ] && v=QUIET || v=FILTER
printf '%s\t%s\t%s\t%s\n' "$prog" "$dir" "$v" "$text"
rm -rf "$h1"
WORKER
chmod +x "$work/one.sh"

LC_ALL=C /usr/bin/awk -F'\t' '{print $1"\t"$2}' "$work/list" \
  | xargs -P "$jobs" -n 2 -I@ sh -c 'exec "$0" $1 "$2" "$3" "$4" "$5"' \
      "$work/one.sh" @ "$work" "$image" "$exe" 2>/dev/null > "$out.tmp"
sort "$out.tmp" > "$out"; rm -f "$out.tmp"
wrote=$(wc -l < "$out")
LC_ALL=C awk -F'\t' '{c[$3]++} END {for (k in c) printf "  %-8s %d\n", k, c[k]}' "$out"
echo "wrote $out ($wrote of $total rows)"
rm -rf "$work"
