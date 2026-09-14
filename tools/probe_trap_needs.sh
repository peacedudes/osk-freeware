#!/bin/bash
# Which programs need a trap module that is not beside them?
#
#     tools/probe_trap_needs.sh <scratch image> <work dir> [module ...]
#
# Each program under disk/CMDS runs from its own execution directory holding
# cio, math and math881, plus any modules named on the command line, and
# NOTHING ELSE -- F$Load looks for a trap handler there -- on a copy of a
# scratch image.  NEVER osk-freeware.dd: rdoggett keeps an emulator open on it.
# A missing trap module fails at startup and names itself, so five seconds a
# program is enough.  Measured 2026-09-14: "**** can't install csl ****",
# "**** Can't install trap handler **** / **** csl ****", "can't install Vmod
# Trap handler", "**** can't install X11R6shl trap handler ****".
#
# The first version matched only the exact words "install trap handler" and
# so filed a program asking for X11R6shl as needing nothing; this one reports
# any "can't install" line and the module it names.  Run it once with no
# modules to find csl needs, then again supplying csl to find what comes next.
# flink is skipped: it corrupts the disk it links on.
set -u
[ $# -ge 2 ] || { echo "usage: $0 <scratch image> <work dir> [module ...]" >&2; exit 2; }
IMG=$1; W=$2; shift 2
case "$(basename "$IMG")" in osk-freeware.dd) echo "refusing osk-freeware.dd" >&2; exit 2;; esac
R=$(cd "$(dirname "$0")/.." && pwd)
E=${OS9EXEC:-$R/../os9exec/os9exec}
mkdir -p "$W"; OUT=$W/trap-needs.tsv; : > "$OUT"
find "$R/disk/CMDS" -type f ! -path '*/archives/*' | sort | while IFS= read -r f; do
  [ "$(xxd -p -l 2 "$f" 2>/dev/null)" = "4afc" ] || continue
  name=$(basename "$f"); rel=${f#$R/disk/}
  case "$name" in flink|cio|csl|csl020|math|math881) continue;; esac
  d=$W/x; rm -rf "$d"; mkdir -p "$d"
  cp "$R/disk/CMDS/cio" "$R/disk/CMDS/math" "$R/disk/CMDS/math881" "$d/"
  for m in "$@"; do cp "$R/disk/CMDS/$m" "$d/" 2>/dev/null; done
  cp "$f" "$d/$name"
  out=$(gtimeout 5 env -i OS9DISK="$IMG" OS9H0="$IMG" OS9H5="$d" OS9CMDS="$d" "$E" -r "/h5/$name" < /dev/null 2>&1 \
        | tr -d '\000' | LC_ALL=C tr '\r' '\n' | grep -a -v -E '^# |^#$|^$' | head -4 | tr '\n' ' ')
  mod=$(printf '%s' "$out" | LC_ALL=C grep -a -o -i -E "can't install ([A-Za-z0-9_]+ )?(trap handler|[A-Za-z0-9_]+)|\*\*\*\* [A-Za-z0-9_]+ \*\*\*\*" | head -2 | tr '\n' ' ')
  if printf '%s' "$out" | LC_ALL=C grep -a -q -i "can't install"; then v=NEEDS-MODULE; else v=STARTS; fi
  printf '%s\t%s\t%s\t%s\t%s\n' "$name" "$rel" "$v" "$mod" "$(printf '%s' "$out" | cut -c1-160)" >> "$OUT"
done
awk -F'\t' '{c[$3]++} END {for (k in c) printf "  %-13s %d\n", k, c[k]}' "$OUT" | sort
echo "results in $OUT"
