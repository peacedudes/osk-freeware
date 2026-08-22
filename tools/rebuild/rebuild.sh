#!/bin/bash
#
# Rebuild freeware-disk programs from source, through a /dd overlay whose
# cstart carries no author stamp.  Writes R_<prog> beside each program's
# sources and installs nothing -- verify.sh and your own judgement decide
# what gets copied onto the disk.
#
# Usage:  rebuild.sh <recipes.psv> <source-pool> [<second-pool>]
#
#   recipes.psv   prog|srctree|sources|defines|extra libs|extra cc flags
#   source-pool   directory holding the <srctree> directories.  A second pool
#                 may be given; a tree is looked up in the first pool first.
#
# Prerequisites, none of which are in this repo:
#   OS9CLEAN   a /dd overlay -- symlinks to the OS-9 system disk except LIB,
#              which is a real directory whose cstart* copies have their
#              64-byte Author psect overwritten with spaces.  Without this
#              every binary is stamped with whoever owns the SDK copy.
#   OS9COMPAT  include directory of shims for headers OS-9 does not ship
#              (string.h, pwd.h, ...).  Ships on the disk as SRC/COMPAT.
#   gtimeout   coreutils; macOS has no plain `timeout`.
#
set -u

RECIPES=$1
POOL1=$2
POOL2=${3:-$POOL1}

HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/../.." && pwd)
: "${OS9CLEAN:?set OS9CLEAN to the clean /dd overlay}"

# The emulator. This used to be a bare `./os9exec' relative to the repository
# root, which meant the driver only worked if somebody had dropped a binary or
# a symlink there -- and when nobody had, every build failed with
# `env: ./os9exec: No such file or directory' and was reported as FAIL, which
# looks exactly like a broken source tree. Same convention as every other tool
# here: $OS9EXEC, else the sibling checkout.
EXE=${OS9EXEC:-$REPO/../os9exec/os9exec}
[ -x "$EXE" ] || { echo "no os9exec at $EXE -- set OS9EXEC" >&2; exit 2; }
: "${OS9COMPAT:=$REPO/freeware/SRC/COMPAT}"
WORK=${TMPDIR:-/tmp}/os9rebuild.$$
mkdir -p "$WORK"
trap 'rm -rf "$WORK"' EXIT

OUT=${OUT:-$WORK/results.tsv}; : > "$OUT"
LOG=${LOG:-$WORK/build.log};   : > "$LOG"
total=$(/usr/bin/grep -cvE '^\s*(#|$)' "$RECIPES")
i=0

# The cc line every build shares.  -qm makes the binary trap-free (no cio, no
# math trap handler), which is what lets these run on a disk with no Microware
# SDK on it.  -n names the module: without it the module name comes from the
# -f output filename and every program reports itself as "R_<prog>" in its own
# usage message.
compile() {   # $1 arch  $2 sources  $3 oskdef  $4 defines  $5 prog  $6 extra  $7 libs
  printf 'setenv CLIB /dd/LIB\nsetenv CDEF /dd/DEFS\nchx /dd/CMDS\nchd /h6/%s\n' "$1"
  printf 'cc %s -qm=16k %s%s -n=%s -f=/h6/%s/R_%s -V=/h6/%s -V=/h7 %s%s' \
         "$2" "$3" "$4" "$5" "$1" "$5" "$1" "$6" "$7"
  printf ' -l=/dd/LIB/curses.l -l=/dd/LIB/termlib.l -l=/dd/LIB/unix.l -l=/dd/LIB/math.l\n'
  printf '\033\n\004\n'
}

# The output goes to a FILE and only a bounded slice of it reaches a shell
# variable.  ed.h carries a REALLOC macro whose continuation lines join into one
# logical line of about 1400 characters; cc says "source line too long" and, on
# 2026-08-22, said it 161 MEGABYTES' worth.  Capturing that with out=$(run ...)
# left the driver spinning on a 161 MB string for five minutes with no os9exec
# running and no sign of what it was doing.  Head and tail together because the
# reason lives at both ends: cc's diagnostics come first, l68's "Symbol 'x'
# unresolved" comes last.
run() {       # $1 pool  $2 command-file  $3 output file
  ( cd "$REPO" && gtimeout 240 env OS9DISK="$OS9CLEAN" OS9H6="$1" OS9H7="$OS9COMPAT" \
      "$EXE" -r shell < "$2" 2>&1 | /usr/bin/tr -d '\000' ) > "$3"
  /usr/bin/head -c 400000 "$3"
  [ "$(/usr/bin/wc -c < "$3")" -gt 500000 ] && printf '\n[... output truncated ...]\n'
  /usr/bin/tail -c 100000 "$3"
}

# '|' not TAB: tab is an IFS *whitespace* character, so bash collapses runs of
# them and an empty defines field silently shifts libs into defs -- which
# produced "-D/dd/LIB/math.l" and killed 20 builds before it was noticed.
while IFS='|' read -r prog arch srcs defs libs extra; do
  case "$prog" in ''|'#'*) continue;; esac
  i=$((i+1))

  if [ -d "$POOL1/$arch" ]; then POOL=$POOL1; else POOL=$POOL2; fi
  d=$POOL/$arch
  rm -f "$d/R_$prog"

  # -DOSK is right for most of this corpus but not all of it: name.c takes the
  # SYSV arm when both are set and then skips its "#ifndef OSK" fallback, so
  # rnd() ends up defined by neither.  NOOSK opts a recipe out.
  OSKDEF=-DOSK
  case " $defs " in *" NOOSK "*) OSKDEF=""; defs="${defs/NOOSK/}";; esac

  D=""; for x in $defs;  do [ -n "$x" ] && D="$D -D$x"; done
  L=""
  for x in $libs; do
    [ -n "$x" ] || continue
    if [ -e "$OS9CLEAN/LIB/$(basename "$x")" ]; then L="$L -l=$x"
    else echo "  note: $prog wants $x, not present -- omitted" >> "$LOG"; fi
  done

  compile "$arch" "$srcs" "$OSKDEF" "$D" "$prog" "${extra:-}" "$L" > "$WORK/cmd"
  out=$(run "$POOL" "$WORK/cmd" "$WORK/out")
  printf '=== %s (%s)\n%s\n' "$prog" "$arch" "$out" >> "$LOG"

  # Retry once with a shim if the only thing missing is a BSD/Unix function
  # OS-9's K&R library never had.  shims/ holds small, documented equivalents.
  # Note this handles ONE shim: a program needing two (uwho wants getpwuid and
  # geteuid both) must name them in its recipe's sources instead.
  if [ ! -f "$d/R_$prog" ]; then
    shim=""
    case "$out" in
      *"'bcopy' unresolved"*|*"'bzero' unresolved"*|*"'bcmp' unresolved"*)          shim=os9bcopy.c;;
      *"'getpwuid' unresolved"*|*"'getpwnam' unresolved"*)                          shim=os9getpw.c;;
      *"'srand48' unresolved"*|*"'drand48' unresolved"*|*"'lrand48' unresolved"*)   shim=os9rand48.c;;
      *"'geteuid' unresolved"*|*"'getuid' unresolved"*)                             shim=os9geteuid.c;;
      *"'popen' unresolved"*)                                                       shim=os9popen.c;;
    esac
    if [ -n "$shim" ]; then
      cp "$HERE/shims/$shim" "$d/" 2>/dev/null
      compile "$arch" "$srcs $shim" "$OSKDEF" "$D" "$prog" "${extra:-}" "$L" > "$WORK/cmd"
      out=$(run "$POOL" "$WORK/cmd" "$WORK/out")
      printf '=== %s (%s) RETRY with %s\n%s\n' "$prog" "$arch" "$shim" "$out" >> "$LOG"
    fi
  fi

  if [ -f "$d/R_$prog" ]; then
    st=$(/usr/bin/grep -qa 'from the disk of' "$d/R_$prog" && echo STAMPED || echo clean)
    printf '%s\t%s\t%s\t%s\n' "$prog" "$arch" "$st" "$d/R_$prog" >> "$OUT"
  else
    why=$(printf '%s' "$out" | /usr/bin/grep -aoE "Symbol '[^']+' unresolved|can't open [^ ]+|\*\*\*\*  [a-z ]+ \*\*\*\*" | head -1)
    printf '%s\t%s\tFAIL\t%s\n' "$prog" "$arch" "${why:-unknown}" >> "$OUT"
  fi
  printf '\r  built %d/%d' "$i" "$total"
done < "$RECIPES"

echo ""
/usr/bin/awk -F'\t' '{c[$3]++} END {for (k in c) printf "  %s=%d\n", k, c[k]}' "$OUT"
echo "  results: $OUT"
echo "  log:     $LOG"
