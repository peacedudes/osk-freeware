#!/bin/bash
#
# Build ksh (pdksh 4.3, Heike Zimmerer's OS-9 port edition 11) from source.
#
#     tools/rebuild/pdksh/build_ksh.sh [<output module>]
#
# The recipe was prose in README.md and nobody could run it. This is the same
# recipe, executable, so that changing one line of the port and measuring the
# result is a two-minute loop instead of an afternoon.
#
# It stages a COPY: `disk/SRC/pdksh' is never written to. Patches in this
# directory are applied to the copy, so what ships stays the archive's.
#
# Three things about this build that are not obvious:
#
#   * ONE include path for every object. Compiling some with `std/stdc' on the
#     path and some without gives different translation units a different
#     `time.h' and `limits.h', which is a struct-layout mismatch waiting to
#     happen. `std/stdc' stays OFF; `OSK/DEFS' carries the one header
#     (`limits.h') it was needed for.
#
#   * `merge', not a long l68 line. The OS-9 shell truncates a command line at
#     about 600 characters and 47 filenames do not fit. `merge -z=<file>' takes
#     its list from a file.
#
#   * The shell's `>' will NOT overwrite -- E_CEF (218). Every output file is
#     deleted first, or you silently keep measuring the previous build.
#
set -u
here=$(cd "$(dirname "$0")" && pwd)
repo=$(cd "$here/../../.." && pwd)
out=${1:-$repo/built/ksh}
exe=${OS9EXEC:-$repo/../os9exec/os9exec}
overlay=${OS9CLEAN:-${TMPDIR:-/tmp}/os9clean}
work=${TMPDIR:-/tmp}/os9ksh.$$

[ -x "$exe" ] || { echo "no os9exec at $exe -- set OS9EXEC" >&2; exit 2; }
[ -d "$overlay/LIB" ] || { echo "no overlay at $overlay -- run make_overlay.sh" >&2; exit 2; }

rm -rf "$work"; mkdir -p "$work/pdksh"
cp -R "$repo/disk/SRC/pdksh/." "$work/pdksh/"
chmod -R u+w "$work/pdksh"

# The patches name their targets by path, with `_' for `/'.
for p in "$here"/*.patch; do
    rel=$(basename "$p" .patch | tr '_' '/')
    # sh_lex.c -> sh/lex.c ; OSK_DEFS_SYS_types.h -> OSK/DEFS/SYS/types.h
    target="$work/pdksh/$rel"
    [ -f "$target" ] || { echo "patch $p has no target $rel" >&2; exit 1; }
    patch -s -p0 -d / "$target" < "$p" 2>/dev/null ||
      patch -s "$target" < "$p" ||
      { echo "failed to apply $(basename "$p")" >&2; exit 1; }
    echo "  patched $rel"
done
cp "$here/memmove.c" "$here/vfprintf.c" "$work/pdksh/sh/"
cp "$here/time.h" "$work/pdksh/OSK/DEFS/"

D="-V=/h6/pdksh/OSK/DEFS -V=/h6/pdksh/etc -V=/h7 -V=/dd/DEFS"
OSKDEF="-DKSH -DDT_INET=9"
SHDEF="-D_SYSV -DBIT8 -DDT_INET=9 -DUSE_SIGNAL -DNSIG=255 \
-Dopendir=_x_opendir -Dopen=_x_open -Daccess=_x_access -Dcreat=_x_creat"

osklib=$(cd "$work/pdksh/OSK/SRC" && ls *.c | tr '\n' ' ')
shsrc=$(cd "$work/pdksh/sh" && ls *.c | tr '\n' ' ')

# The two merge lists, CR-terminated the way `merge -z' wants them.
: > "$work/pdksh/OSK/SRC/ctmp.list"
for c in $osklib; do printf '%s\r' "${c%.c}.r" >> "$work/pdksh/OSK/SRC/ctmp.list"; done
: > "$work/pdksh/sh/ctmp.list"
for c in $shsrc; do printf '%s\r' "${c%.c}.r" >> "$work/pdksh/sh/ctmp.list"; done
printf 'osklib.r\r' >> "$work/pdksh/sh/ctmp.list"

{
  printf 'setenv CLIB /dd/LIB\nsetenv CDEF /dd/DEFS\nchx /dd/CMDS\n'
  printf 'chd /h6/pdksh/OSK/SRC\n'
  for c in $osklib; do printf 'cc %s %s %s -r=/h6/pdksh/OSK/SRC\n' "$c" "$OSKDEF" "$D"; done
  printf 'del ctmp.parts.l\nmerge -z=ctmp.list >ctmp.parts.l\n'
  printf 'chd /h6/pdksh/sh\n'
  printf 'del osklib.r\ncopy /h6/pdksh/OSK/SRC/ctmp.parts.l osklib.r\n'
  for c in $shsrc; do printf 'cc %s %s %s -r=/h6/pdksh/sh\n' "$c" "$SHDEF" "$D"; done
  printf 'del ctmp.all.r\nmerge -z=ctmp.list >ctmp.all.r\n'
  printf 'del /h6/R_ksh\n'
  printf 'cc ctmp.all.r -qm=32k -n=ksh -f=/h6/R_ksh -l=/dd/LIB/os9lib.l\n'
  printf '\033\n\004\n'
} > "$work/cmd"

echo "building (this takes a few minutes) ..."
( cd "$repo" && gtimeout 1800 env OS9DISK="$overlay" OS9H6="$work" \
    OS9H7="$repo/disk/SRC/COMPAT" "$exe" -r shell < "$work/cmd" 2>&1 |
    tr -d '\000' ) > "$work/log"

if [ -f "$work/R_ksh" ]; then
    mkdir -p "$(dirname "$out")"
    cp "$work/R_ksh" "$out"
    echo "built $out  ($(ls -l "$out" | awk '{print $5}') bytes)"
    echo "log: $work/log   staging: $work/pdksh"
    exit 0
fi
echo "FAILED -- log at $work/log"
/usr/bin/grep -aE "unresolved|duplicate|\*\*\*\*|can't open" "$work/log" | sort -u | head -20
exit 1
