#!/bin/bash
#
# Try to compile a source tree that has no recipe yet, and say what happened.
#
#   tools/try_compile.sh <tree> <program> [<extra cc args>...]
#   tools/try_compile.sh --all              every un-recipe'd single-program tree
#
# The question this answers is rdoggett's: "if it's source, it should compile,
# right?"  `tools/rebuild/recipes.psv` holds 194 programs that are KNOWN to
# build.  71 trees on the disk have no recipe at all, so nobody has ever
# established whether their source is complete.  This is how a tree gets from
# "unknown" to either a recipe or a documented reason.
#
# It deliberately makes the NAIVE attempt first -- every .c in the tree, the
# standard flags -- because that is what a recipe looks like when it works, and
# the failure message is what tells you which of the documented causes it is.
# `tools/rebuild/README.md` has the table: unresolved symbol means the file
# list is short, duplicate symbol means it is too long, "can't open <header>"
# means a subdirectory or SRC/COMPAT, "value out of range" is r68 not cc.
#
# Env:  OS9CLEAN  the overlay from tools/rebuild/make_overlay.sh (required)
#       OS9EXEC   the emulator binary
set -u
here=$(cd "$(dirname "$0")/.." && pwd)
: "${OS9CLEAN:?set OS9CLEAN -- run tools/rebuild/make_overlay.sh first}"
exe=${OS9EXEC:-$here/../os9exec/os9exec}
work=${TMPDIR:-/tmp}/os9try.$$
mkdir -p "$work"
# The LOG SURVIVES. The whole point of this script is the failure message, and
# a one-line summary is often not enough -- "errors in compilation : 1" tells
# you nothing about which line. Its path is printed after every failure.
trap 'rm -rf "$work"/*/ 2>/dev/null' EXIT
KEEP=${TMPDIR:-/tmp}/os9try.log

attempt() {           # $1 tree  $2 program  $3.. extra args
    local tree=$1 prog=$2; shift 2
    local src="$here/disk/SRC/$tree"
    [ -d "$src" ] || { printf '%-14s %-12s %s\n' "$tree" "$prog" "NO SUCH TREE"; return; }
    rm -rf "$work/$tree"; mkdir -p "$work/$tree"
    # .d and .inc travel too: OS-9 sources include them, and `lextab.d' is
    # a header in all but name.
    cp "$src"/*.c "$src"/*.h "$src"/*.d "$src"/*.inc "$work/$tree/" 2>/dev/null
    local cs; cs=$(cd "$work/$tree" && ls *.c 2>/dev/null | tr '\n' ' ')
    [ -n "$cs" ] || { printf '%-14s %-12s %s\n' "$tree" "$prog" "no .c at top level"; return; }

    { printf 'setenv CLIB /dd/LIB\nsetenv CDEF /dd/DEFS\nchx /dd/CMDS\nchd /h6/%s\n' "$tree"
      # -V=/h6/<tree> puts the tree's OWN directory on the include path. Without
      # it a source that writes #include <boolean.h> rather than "boolean.h"
      # fails with `can't open /dd/DEFS/boolean.h' even though the header is
      # sitting right beside it -- which is how this script first reported
      # three trees as missing headers they in fact ship.
      printf 'cc %s -qm=16k -DOSK -n=%s -f=/h6/%s/R_%s -V=/h6/%s -V=/h7 %s' \
             "$cs" "$prog" "$tree" "$prog" "$tree" "$*"
      printf ' -l=/dd/LIB/curses.l -l=/dd/LIB/termlib.l -l=/dd/LIB/unix.l -l=/dd/LIB/math.l\n'
      printf '\033\n\004\n'
    } > "$work/cmd"

    ( cd "$here" && gtimeout 300 env OS9DISK="$OS9CLEAN" OS9H6="$work" \
        OS9H7="$here/disk/SRC/COMPAT" "$exe" -r shell < "$work/cmd" 2>&1 \
        | tr -d '\000' ) > "$work/log"

    if [ -f "$work/$tree/R_$prog" ]; then
        printf '%-14s %-12s BUILDS   %s bytes\n' "$tree" "$prog" \
               "$(ls -l "$work/$tree/R_$prog" | awk '{print $5}')"
        return
    fi
    # First line that says why, in the order the README's table lists them.
    local why
    why=$(grep -a -m1 -E "unresolved|duplicate symbol|can't open|undeclared|out of range|source line too long|no recognized suffix|errors in compilation" "$work/log" \
          | sed 's/^[ \t]*//' | cut -c1-58)
    cp "$work/log" "$KEEP" 2>/dev/null
    printf '%-14s %-12s FAILS    %s\n' "$tree" "$prog" \
           "${why:-unknown -- full log in $KEEP}"
}

if [ "${1:-}" = "--all" ]; then
    printf '%-14s %-12s %s\n' "tree" "program" "result"
    while IFS=' ' read -r tree prog; do
        [ -n "$tree" ] && attempt "$tree" "$prog"
    done <<'LIST'
adv advent
argproc argproc_demo
cursive cursive
draw draw
eff_tsmon tsmon2
flex flex
hist hist
indent indent
ioccc queens
nobs nobs
pep pep
proff proff
rob robots
shuffle shuffle
snake snake
today today
wish wish
xlisp xlisp
LIST
else
    attempt "$@"
fi
