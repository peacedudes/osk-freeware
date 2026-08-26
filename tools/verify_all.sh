#!/bin/bash
# Run every program under disk/CMDS bare -- no arguments, no input, the built
# image as the only disk -- and classify what happens.
#
# THE CLASSIFIER IS THE WHOLE DIFFICULTY.  os9exec writes its own diagnostics
# with a leading '#', and those lines are the verdict for anything that never
# reaches its own code:
#
#   # Emulation could not start due to OS-9 error #000:205 (E_BMID)
#   # main loop: Process pid=2 aborted due to unintialized User Trap #5
#
# A first version of this sweep did `grep -v '^#'` to get at program output and
# so threw those away, then called the empty remainder OK because os9exec's
# blank line was not empty.  It reported 91 programs working that do not load
# at all, `blackjack` among them -- a program DOC/STATUS has always listed as
# broken.  Keep the '#' lines.  Only the startup `# /h0:` / `# /dd:` notices
# are noise.
#
# Run verify_filters.sh afterwards.  It is not optional: a stdin filter that
# prints nothing at end-of-file has succeeded, and this sweep alone marks
# hundreds of healthy programs SILENT.
#
# Verdicts:
#   OK       printed something of its own
#   SILENT   ran, printed nothing -- verify_filters.sh separates these
#   NOSTART  os9exec could not load the module (E_BMID, E_NEMOD, ...)
#   TRAP     wanted a trap handler that is not installed
#   CRASH    started and died (E_PRCABT, bus error, ...)
#
# Usage:  tools/verify_all.sh [<disk-dir> [<image>]]
# Env:    OS9EXEC   path to the os9exec binary (default ../os9exec/os9exec)
# Output: notes/verify-bare.tsv   program, directory, verdict, evidence

set -u
here=$(cd "$(dirname "$0")/.." && pwd)
disk=${1:-$here/disk}
image=${2:-$here/osk-freeware.dd}
exe=${OS9EXEC:-$here/../os9exec/os9exec}
out=$here/notes/verify-bare.tsv
list=$(mktemp)
raw=$(mktemp)

[ -x "$exe" ]   || { echo "no os9exec at $exe -- set OS9EXEC" >&2; exit 2; }
[ -f "$image" ] || { echo "no image at $image -- build it first" >&2; exit 2; }

# CMDS/archives holds archive files, not programs.
find "$disk/CMDS" -type f -not -path '*/archives/*' \
  | sed "s|^$disk/||" \
  | awk -F/ '{n=$NF; sub("/"n"$","",$0); print n"\t"$0}' OFS='' \
  | sed 's|\t.*/CMDS|\tCMDS|' > "$list"
total=$(wc -l < "$list")
echo "verifying $total programs"

: > "$out"
while IFS=$'\t' read -r prog dir; do
  # `head -c` is load-bearing, not tidying.  It closes the pipe once enough has
  # been read, os9exec takes SIGPIPE, and a chatty program ends in a moment
  # EVERY `tr' here needs LC_ALL=C, and one of them did not have it until
  # 2026-08-26.  Without it, `tr -d' aborts with "Illegal byte sequence"
  # the moment a program emits an 8-bit byte -- so the capture is
  # truncated or empty and the program is classified on nothing.  The
  # symptom is a pile of `tr: Illegal byte sequence' on stderr, which is
  # easy to read as noise; it is the sweep silently losing programs.
  # instead of running out the timeout.  Without it this sweep takes seven
  # hours instead of one, because every program that prints a lot waits for
  # gtimeout to shoot it.
  gtimeout 10 env OS9DISK="$image" OS9H0="$image" \
      "$exe" -r "/dd/$dir/$prog" < /dev/null 2>&1 \
    | LC_ALL=C /usr/bin/tr -d '\000' | LC_ALL=C /usr/bin/tr '\r' '\n' \
    | /usr/bin/head -c 8000 \
    | LC_ALL=C /usr/bin/grep -vE '^# /[a-z0-9]+: (using|no) ' > "$raw"

  diag=$( LC_ALL=C /usr/bin/grep '^#' "$raw" | /usr/bin/head -2 \
          | LC_ALL=C /usr/bin/tr '\n' ' ' )
  mine=$( LC_ALL=C /usr/bin/grep -v '^#' "$raw" | LC_ALL=C /usr/bin/grep -v '^[[:space:]]*$' \
          | /usr/bin/head -3 | LC_ALL=C /usr/bin/tr '\n' ' ' )

  if   printf '%s' "$diag$mine" | LC_ALL=C /usr/bin/grep -q 'could not start'; then v=NOSTART
  elif printf '%s' "$diag$mine" | LC_ALL=C /usr/bin/grep -qiE 'trap handler|User Trap'; then v=TRAP
  elif printf '%s' "$diag$mine" | LC_ALL=C /usr/bin/grep -qE 'E_[A-Z]+\([0-9]+\)|err=#[0-9]'; then v=CRASH
  elif [ -n "$mine" ]; then v=OK
  else v=SILENT; fi

  case $v in OK|SILENT) ev=$mine ;; *) ev=$diag$mine ;; esac
  printf '%s\t%s\t%s\t%s\n' "$prog" "$dir" "$v" "$(printf '%s' "$ev" | /usr/bin/cut -c1-100)" >> "$out"
done < "$list"

wrote=$(wc -l < "$out")
rm -f "$list" "$raw"
awk -F'\t' '{c[$3]++} END {for (k in c) printf "  %-8s %d\n", k, c[k]}' "$out"
[ "$wrote" -eq "$total" ] || { echo "INCOMPLETE: $wrote of $total rows" >&2; exit 1; }
echo "wrote $out ($wrote rows)"
