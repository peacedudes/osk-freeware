#!/bin/bash
# Second pass: everything that did NOT run trap-free, re-run with Microware's
# cio, csl and math881 present.  This is the question the star in DOC/INDEX
# actually answers -- "does it work for someone who has their own licence?" --
# as opposed to "does it work bare".  The trap modules are borrowed from the
# SDK boot disk for the test and are never copied into disk/.
set -u
S=/private/tmp/claude-501/-Users-rdoggett-Developer-os9-osk-freeware/2819709a-7a1e-4d9f-b0f0-9628c0581438/scratchpad
REPO=/Users/rdoggett/Developer/os9/osk-freeware
OS9EXEC=${OS9EXEC:-/Users/rdoggett/Developer/os9/os9exec/os9exec}
B=$HOME/Developer/os9/play/oskBoot/CMDS
: > "$S/probe/verdicts2.tsv"
awk -F'\t' '$2!="RUNS"{print $1"\t"$3}' "$S/probe/verdicts.tsv" | while IFS=$'\t' read -r prog path; do
  d="$S/t2/$prog"; rm -rf "$d"; mkdir -p "$d"
  cp "$B/cio" "$B/csl" "$B/math881" "$d/" 2>/dev/null
  cp "$S/newstage/$path" "$d/" 2>/dev/null || { printf '%s\tMISSING\t%s\n' "$prog" "$path" >> "$S/probe/verdicts2.tsv"; continue; }
  out=$( cd "$REPO" && gtimeout 20 env OS9DISK="$REPO/osk-freeware.dd" OS9MDIR="$d" \
           "$OS9EXEC" -r "$(basename "$path")" < /dev/null 2>&1 \
         | /usr/bin/tr -d '\000' | /usr/bin/sed $'s/\033\\[[0-9?]*[a-zA-Z=]//g' \
         | /usr/bin/grep -vE '^# |^#$' )
  if   printf '%s' "$out" | /usr/bin/grep -q 'install trap handler'   ; then v=STILL-TRAP
  elif printf '%s' "$out" | /usr/bin/grep -qE "can't execute"         ; then v=NOEXEC
  elif printf '%s' "$out" | /usr/bin/grep -qE 'error #[0-9]'          ; then v=OS9ERR
  else v=WORKS-WITH-TRAPS; fi
  printf '%s\t%s\t%s\n' "$prog" "$v" "$path" >> "$S/probe/verdicts2.tsv"
  rm -rf "$d"
done
awk -F'\t' '{c[$2]++} END {for (k in c) printf "  %-18s %d\n", k, c[k]}' "$S/probe/verdicts2.tsv" | sort -k2 -rn
