#!/bin/bash
# Classify every candidate module from the five re-fetched pool categories by
# running it, with no cio/csl/math present, straight from os9exec -- no shell
# in the path, because the freeware disk's `sh` would not resolve commands
# here and every verdict came back a false NOTFOUND.
#
# An empty capture is its own verdict and never a pass.
set -u
S=/private/tmp/claude-501/-Users-rdoggett-Developer-os9-osk-freeware/2819709a-7a1e-4d9f-b0f0-9628c0581438/scratchpad
REPO=/Users/rdoggett/Developer/os9/osk-freeware
OS9EXEC=/Users/rdoggett/mine/os9/xxx/os9exec/os9exec-git_code/os9exec
: > "$S/probe/verdicts.tsv"
while IFS=$'\t' read -r prog path; do
  f="$S/newstage/$path"
  [ -f "$f" ] || { printf '%s\tMISSING\t%s\n' "$prog" "$path" >> "$S/probe/verdicts.tsv"; continue; }
  out=$( cd "$REPO" && gtimeout 20 env OS9DISK="$REPO/osk-freeware.dd" OS9MDIR="$(dirname "$f")" \
           "$OS9EXEC" -r "$(basename "$f")" < /dev/null 2>&1 \
         | /usr/bin/tr -d '\000' | /usr/bin/sed $'s/\033\\[[0-9?]*[a-zA-Z=]//g' \
         | /usr/bin/grep -vE '^# |^#$' )
  if   [ -z "$out" ]                                                    ; then v=NOOUTPUT
  elif printf '%s' "$out" | /usr/bin/grep -q 'install trap handler'      ; then
       v=NEEDS-$(printf '%s' "$out" | /usr/bin/sed -n 's/.*\*\*\*\* \([a-z0-9]*\) \*\*\*\*.*/\1/p' | head -1)
  elif printf '%s' "$out" | /usr/bin/grep -qE "can't execute|not found"  ; then v=NOEXEC
  elif printf '%s' "$out" | /usr/bin/grep -qE 'error #[0-9]'             ; then
       v=ERR$(printf '%s' "$out" | /usr/bin/sed -n 's/.*error #[0-9]*:\([0-9]*\).*/\1/p' | head -1)
  else v=RUNS; fi
  printf '%s\t%s\t%s\n' "$prog" "$v" "$path" >> "$S/probe/verdicts.tsv"
done < "$S/probe/list.tsv"
awk -F'\t' '{c[$2]++} END {for (k in c) printf "  %-12s %d\n", k, c[k]}' "$S/probe/verdicts.tsv" | sort -k2 -rn
