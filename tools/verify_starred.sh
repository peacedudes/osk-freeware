#!/bin/bash
# Every starred program, run on the BARE disk with nothing supplied.
# Before the Microware modules shipped, all of these stopped with
# "**** Can't install trap handler ****".  This counts how many still do.
set -u
E=/Users/rdoggett/Developer/os9/os9exec/os9exec
R=/Users/rdoggett/Developer/os9/osk-freeware
: > /tmp/vstar.tsv
while IFS=$'\t' read -r prog dir; do
  out=$( cd "$R" && gtimeout 20 env OS9DISK="$R/osk-freeware.dd" OS9H0="$R/osk-freeware.dd" \
           "$E" -r "/dd/$dir/$prog" < /dev/null 2>&1 \
         | /usr/bin/tr -d '\000' | /usr/bin/grep -v '^#' )
  if   printf '%s' "$out" | /usr/bin/grep -q 'install trap handler'; then v=STILL-TRAPS
  elif [ -z "$out" ]                                                ; then v=NOOUTPUT
  else v=RUNS; fi
  printf '%s\t%s\n' "$prog" "$v" >> /tmp/vstar.tsv
done < /tmp/starred.txt
awk -F'\t' '{c[$2]++} END {for (k in c) printf "  %-12s %d\n", k, c[k]}' /tmp/vstar.tsv
