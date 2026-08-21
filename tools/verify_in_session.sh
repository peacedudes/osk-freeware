#!/bin/bash
# Third stage of the sweep, and the one that keeps it honest.
#
# verify_all.sh runs each program as os9exec's FIRST process, which means it
# runs with no environment at all -- no TERM, no TERMCAP, no PATH.  That is not
# how anybody uses this disk, and it is not a fair test: `cribbage` says
# "Environment variable TERM not defined" and `crib` says "Unknown terminal
# type ''", and both then abort.  Neither is broken.  69 programs on this disk
# read TERMCAP, and SYS/login is what sets it.
#
# So anything the bare sweep did not clear gets run again HERE, inside a
# bash session started through /dd/SYS/login, exactly as a user would meet it.
# Host environment variables do not reach an OS-9 program -- setting TERM in
# the shell that launches os9exec changes nothing -- so going through login is
# the only way to give these programs their environment.
#
# Usage:  tools/verify_in_session.sh [<image>]
# Env:    OS9EXEC   path to the os9exec binary (default ../os9exec/os9exec)
# Input:  notes/verify-bare.tsv   written by verify_all.sh
# Output: notes/verify-session.tsv  program, directory, verdict, evidence
#
# Verdicts: SESSION-OK  ran and printed something once it had an environment
#           STILL-BAD   failed the same way with the environment present

set -u
here=$(cd "$(dirname "$0")/.." && pwd)
image=${1:-$here/osk-freeware.dd}
exe=${OS9EXEC:-$here/../os9exec/os9exec}
bare=$here/notes/verify-bare.tsv
filters=$here/notes/verify-filters.tsv
out=$here/notes/verify-session.tsv
list=$(mktemp)
raw=$(mktemp)

[ -x "$exe" ]  || { echo "no os9exec at $exe -- set OS9EXEC" >&2; exit 2; }
[ -f "$bare" ] || { echo "no $bare -- run tools/verify_all.sh first" >&2; exit 2; }

# Stage 3 looks at everything the first two stages did not clear: the outright
# failures from the bare sweep, plus anything verify_filters.sh found still
# QUIET with input.  `env` and `printenv` are in the second group for the
# obvious reason -- run bare there IS no environment to print.
awk -F'\t' '$3!="OK" && $3!="SILENT"{print $1"\t"$2}' "$bare" > "$list"
[ -f "$filters" ] && awk -F'\t' '$3=="QUIET"{print $1"\t"$2}' "$filters" >> "$list"
total=$(wc -l < "$list")
echo "re-running $total programs inside a login session"

: > "$out"
while IFS=$'\t' read -r prog dir; do
  printf '/dd/%s/%s\nexit\n' "$dir" "$prog" \
    | gtimeout 20 env OS9DISK="$image" OS9H0="$image" \
        "$exe" -r bash /dd/SYS/login 2>&1 \
    | /usr/bin/tr -d '\000' | LC_ALL=C /usr/bin/tr '\r' '\n' \
    | /usr/bin/head -c 8000 > "$raw"

  # login prints a two-line banner and bash echoes the prompt, the command and
  # the `exit` that ends the session; none of that is the program talking.
  # Scoring bash's echoed `exit` as output marked 23 non-programs SESSION-OK,
  # including four MM/1 drivers -- drop it explicitly.
  text=$( LC_ALL=C /usr/bin/grep -vE '^#|^os9\$|^OS-9 freeware|^cat and less|^exit$|^$' "$raw" \
          | LC_ALL=C /usr/bin/grep -vF "/dd/$dir/$prog" \
          | /usr/bin/head -3 | LC_ALL=C /usr/bin/tr '\n' ' ' | /usr/bin/cut -c1-100 )

  # `No more memory !!!` is os9exec declining to fork something that is not a
  # program; `command not found` is bash rejecting Microware shell syntax.
  if [ -n "$text" ] \
     && ! printf '%s' "$text" | LC_ALL=C /usr/bin/grep -qiE 'not defined|unknown terminal|Exception:|Exit code|could not start|trap handler|User Trap|Illegal instruction|No more memory|command not found'; then
    v=SESSION-OK
  else
    v=STILL-BAD
  fi
  printf '%s\t%s\t%s\t%s\n' "$prog" "$dir" "$v" "$text" >> "$out"
done < "$list"

wrote=$(wc -l < "$out")
rm -f "$list" "$raw"
awk -F'\t' '{c[$3]++} END {for (k in c) printf "  %-12s %d\n", k, c[k]}' "$out"
[ "$wrote" -eq "$total" ] || { echo "INCOMPLETE: $wrote of $total rows" >&2; exit 1; }
echo "wrote $out ($wrote rows)"
