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
# The tree moved out of freeware/ when this repo was split off; the old default
# silently pointed at nothing, so every <stdlib.h> and <pwd.h> came back as
# "can't open /dd/DEFS/..." for anyone who ran this script directly instead of
# through tools/build.sh.
: "${OS9COMPAT:=$REPO/disk/SRC/COMPAT}"
[ -d "$OS9COMPAT" ] || { echo "no COMPAT headers at $OS9COMPAT" >&2; exit 2; }
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
# A LIBRARY, not a program.  A recipe whose first field ends in `.l' is built
# by compiling each source and merging the objects -- there is no main() and
# nothing to link.  SRC/unixlib is the one that wants this: its own makefile
# ends `merge -b99 -z=lib_list', and the result is what somebody would put in
# their own LIB rather than name source-by-source in every recipe.
compile_lib() {    # $1 arch  $2 sources  $3 oskdef  $4 defines  $5 name  $6 dir  $7 extra
  : > "$6/ctmp.list"
  for s in $2; do
    printf '%s\r' "$(basename "$s" .c).r" >> "$6/ctmp.list"
  done
  printf 'setenv CLIB /dd/LIB\nsetenv CDEF /dd/DEFS\nchx /dd/CMDS\nchd /h6/%s\n' "$1"
  for s in $2; do
    printf 'cc %s %s%s -r=/h6/%s -V=/h6/%s -V=/h7 %s\n' "$s" "$3" "$4" "$1" "$1" "${7:-}"
  done
  # The shell's `>' will NOT overwrite -- E_CEF (218) -- so a second build
  # silently keeps the first one's library and reports it as fresh.
  printf 'del R_%s\n' "$5"
  printf 'merge -z=ctmp.list >R_%s\n' "$5"
  printf '\033\n\004\n'
}

# THE LONG-ARGUMENT PATH.  SCF will not read a line longer than 512 bytes.
# That is the operating system, not a bug and not something to work around at
# the far end -- a command line longer than that arrives cut off.  `mtools' has
# 45 sources and its cc line ran to 900 characters, so what arrived was cut in
# the middle of `-V=/h6/mtools/MTOOLS_3.6' with every library gone, and the
# error was "can't open /dd/DEFS/stdlib.h" -- which reads like a missing
# header.  So: keep the line short enough to be read.
#
# So above that length each source is compiled on its own short line, the
# objects are gathered with `merge -z=<file>' -- which takes its file list from
# a FILE and therefore has no line limit -- and the module is linked from the
# one object holding main() plus that gathering as a library.
#
# The gathered file must be a LIBRARY passed with -l=, not an object: l68 reads
# one ROF from a plain filename and would take only the first of the 44.
# ANSI C, run through ansi2knr first.  A recipe asks for this with the KNR
# pseudo-define, the way NOOSK opts out of -DOSK.  Microware's cc is K&R and
# will not read a prototype; ansi2knr is the standard de-ANSIfier, is itself
# K&R so it bootstraps, and builds here.  Each source is translated into a
# ctmp_<base>.c beside it and that is what gets compiled.
#
# KNR implies the long path whatever the line length: the one-line form has
# nowhere to put the intermediate.
compile_knr() {    # $1 arch  $2 sources  $3 oskdef  $4 defines  $5 prog  $6 extra  $7 libs  $8 dir
  local mainsrc="" s base
  for s in $2; do
    /usr/bin/tr '\r' '\n' < "$8/$s" |
      /usr/bin/grep -qaE '^([A-Za-z_][A-Za-z0-9_ *]*[ *])?main[[:space:]]*\(' &&
        mainsrc=$s
  done
  [ -n "$mainsrc" ] || { echo "  $5: no main() among its sources" >&2; return 1; }

  : > "$8/ctmp.list"
  for s in $2; do
    [ "$s" = "$mainsrc" ] && continue
    printf '%s\r' "ctmp_$(basename "$s" .c).r" >> "$8/ctmp.list"
  done

  printf 'setenv CLIB /dd/LIB\nsetenv CDEF /dd/DEFS\nchx /dd/CMDS\nchd /h6/%s\n' "$1"
  for s in $2; do
    base=$(basename "$s" .c)
    printf 'del ctmp_%s.c\nansi2knr %s ctmp_%s.c\n' "$base" "$s" "$base"
    printf 'cc ctmp_%s.c %s%s -r=/h6/%s -V=/h6/%s -V=/h7 %s\n' \
           "$base" "$3" "$4" "$1" "$1" "$6"
  done
  printf 'del ctmp.parts.l\nmerge -z=ctmp.list >ctmp.parts.l\n'
  printf 'cc ctmp_%s.r -qm=16k -n=%s -f=/h6/%s/R_%s -l=ctmp.parts.l -l=ctmp.parts.l -l=ctmp.parts.l %s%s' \
         "$(basename "$mainsrc" .c)" "$5" "$1" "$5" "$6" "$7"
  printf ' -l=/dd/LIB/curses.l -l=/dd/LIB/termlib.l -l=/dd/LIB/unix.l -l=/dd/LIB/math.l\n'
  printf '\033\n\004\n'
}

compile_long() {   # $1 arch  $2 sources  $3 oskdef  $4 defines  $5 prog  $6 extra  $7 libs  $8 dir
  # Through `tr' first: these sources are CR-terminated, so grep sees the whole
  # file as ONE line and `^' matches only at its start. Without that, zoo.c's
  # `main(argc, argv)' is invisible and the recipe is reported as having no
  # main() at all.
  local mainsrc="" s
  for s in $2; do
    /usr/bin/tr '\r' '\n' < "$8/$s" |
      /usr/bin/grep -qaE '^([A-Za-z_][A-Za-z0-9_ *]*[ *])?main[[:space:]]*\(' &&
        mainsrc=$s
  done
  [ -n "$mainsrc" ] || { echo "  $5: no main() among its sources" >&2; return 1; }

  : > "$8/ctmp.list"
  for s in $2; do
    [ "$s" = "$mainsrc" ] && continue
    printf '%s\r' "$(basename "$s" .c).r" >> "$8/ctmp.list"
  done

  printf 'setenv CLIB /dd/LIB\nsetenv CDEF /dd/DEFS\nchx /dd/CMDS\nchd /h6/%s\n' "$1"
  for s in $2; do
    printf 'cc %s %s%s -r=/h6/%s -V=/h6/%s -V=/h7\n' "$s" "$3" "$4" "$1" "$1"
  done
  # -l= five times, not once.  l68 makes ONE pass over a library, so a member
  # that calls another member later in the file is left unresolved: zoo's huf.c
  # wants putbits from io.c and came back with 24 unresolved references to it.
  # Repeating the search costs nothing and settles any dependency depth this
  # collection has.
  printf 'del ctmp.parts.l\nmerge -z=ctmp.list >ctmp.parts.l\n'
  printf 'cc %s.r -qm=16k -n=%s -f=/h6/%s/R_%s -l=ctmp.parts.l -l=ctmp.parts.l -l=ctmp.parts.l -l=ctmp.parts.l -l=ctmp.parts.l %s%s' \
         "$(basename "$mainsrc" .c)" "$5" "$1" "$5" "$6" "$7"
  printf ' -l=/dd/LIB/curses.l -l=/dd/LIB/termlib.l -l=/dd/LIB/unix.l -l=/dd/LIB/math.l\n'
  printf '\033\n\004\n'
}

# $LIMIT seconds per program.  240 is right for a one-line build; the
# long-argument path compiles each source separately and zoo's 35 and mtools'
# 45 both ran past it and were recorded FAIL with no output at all.
LIMIT=240
run() {       # $1 pool  $2 command-file  $3 output file
  ( cd "$REPO" && gtimeout "$LIMIT" env OS9DISK="$OS9CLEAN" OS9H6="$1" OS9H7="$OS9COMPAT" \
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
  KNRMODE=0
  case " $defs " in *" KNR "*) KNRMODE=1; defs="${defs/KNR/}";; esac

  D=""; for x in $defs;  do [ -n "$x" ] && D="$D -D$x"; done
  L=""
  for x in $libs; do
    [ -n "$x" ] || continue
    if [ -e "$OS9CLEAN/LIB/$(basename "$x")" ]; then L="$L -l=$x"
    else echo "  note: $prog wants $x, not present -- omitted" >> "$LOG"; fi
  done

  # One build attempt with whatever source list it is given.  Measures the line
  # that is actually going to be TYPED, not the recipe field: mtools' sources
  # are 430 characters and its cc line is 900, because the output path, the -V
  # directories and four libraries come after them.
  attempt() {   # $1 sources
    if [ "$KNRMODE" = 1 ]; then
      compile_knr "$arch" "$1" "$OSKDEF" "$D" "$prog" "${extra:-}" "$L" "$d" > "$WORK/cmd"
      LIMIT=1800
      run "$POOL" "$WORK/cmd" "$WORK/out"
      return
    fi
    case "$prog" in
      *.l) compile_lib "$arch" "$1" "$OSKDEF" "$D" "$prog" "$d" "${extra:-}" > "$WORK/cmd"
           LIMIT=900
           run "$POOL" "$WORK/cmd" "$WORK/out"
           return;;
    esac
    compile "$arch" "$1" "$OSKDEF" "$D" "$prog" "${extra:-}" "$L" > "$WORK/cmd"
    longest=$(/usr/bin/awk '{ if (length($0) > m) m = length($0) } END { print m+0 }' "$WORK/cmd")
    LIMIT=240
    if [ "$longest" -gt 480 ]; then
      compile_long "$arch" "$1" "$OSKDEF" "$D" "$prog" "${extra:-}" "$L" "$d" > "$WORK/cmd"
      LIMIT=900
    fi
    run "$POOL" "$WORK/cmd" "$WORK/out"
  }

  out=$(attempt "$srcs")
  printf '=== %s (%s)\n%s\n' "$prog" "$arch" "$out" >> "$LOG"

  # Retry with shims when what is missing is a BSD or Unix function OS-9's K&R
  # library never had.  shims/ holds small, documented equivalents.
  #
  # This used to add exactly ONE and give up.  `lwf' wants getpwuid AND popen,
  # so it failed on popen having been given the passwd shim, and the recipe
  # could not name the second because shims live outside disk/SRC.  Now it
  # keeps adding while each round names a shim it has not already tried.
  added=""
  while [ ! -f "$d/R_$prog" ]; do
    shim=""
    case "$out" in
      *"'bcopy' unresolved"*|*"'bzero' unresolved"*|*"'bcmp' unresolved"*)          shim=os9bcopy.c;;
      *"'getpwuid' unresolved"*|*"'getpwnam' unresolved"*|*"'getlogin' unresolved"*) shim=os9getpw.c;;
      *"'gethostname' unresolved"*|*"'gettz' unresolved"*)                       shim=os9hostname.c;;
      *"'srand48' unresolved"*|*"'drand48' unresolved"*|*"'lrand48' unresolved"*)   shim=os9rand48.c;;
      *"'geteuid' unresolved"*|*"'getuid' unresolved"*)                             shim=os9geteuid.c;;
      *"'popen' unresolved"*|*"'pclose' unresolved"*)                               shim=os9popen.c;;
      *"'strucmp' unresolved"*|*"'strnucmp' unresolved"*|*"'strstr' unresolved"*|*"'rename' unresolved"*) shim=os9alib.c;;
    esac
    [ -n "$shim" ] || break
    case " $added " in *" $shim "*) break;; esac      # already tried: stop
    # NEVER shadow a file the tree already has.  SRC/patch carries its own
    # os9popen.c and NAMES it in its recipe; copying the shim over it, and
    # then tidying the shim away afterwards, DELETED the archive's source.
    if [ -e "$d/$shim" ]; then
      echo "  note: $prog wants $shim but SRC/$arch has one of its own" >> "$LOG"
      break
    fi
    cp "$HERE/shims/$shim" "$d/" 2>/dev/null || break
    added="$added $shim"
    out=$(attempt "$srcs$added")
    printf '=== %s (%s) RETRY with%s\n%s\n' "$prog" "$arch" "$added" "$out" >> "$LOG"
  done

  # Take the shims back out.  They are this driver's, not the archive's, and a
  # copy left behind in disk/SRC would ship on the disk as if the port had
  # always carried it.
  for s in $added; do rm -f "$d/$s"; done

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
