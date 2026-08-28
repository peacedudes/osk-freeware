#!/bin/bash
# Install the relinked binaries that earned it, and only those.
#
#   tools/rebuild/install_relink.sh <compare.tsv> <relink-outdir> [--apply]
#
# Without --apply it reports what it would do and touches nothing.
#
# The rule, and why each half of it exists:
#
#   SAME         install. Byte-identical output from both binaries.
#   NEW-SPEAKS   install. The old one printed nothing and the new one works;
#                `m4' and `valspeak' are both this.
#   DIFFERENT    RE-CHECK on a shorter prefix, then install only if that
#                matches. Most of these are full-screen programs whose
#                captures were cut at different points by `head -c 2000',
#                not programs that behave differently -- `sedt' draws an
#                identical screen and differs only past the cut.
#   BOTH-QUIET   leave alone. Neither said anything, so there is no evidence
#                the new one works, and no evidence is not a pass.
#   NEW-BROKEN   NEVER. `calen' prompts "Enter calendar specs" and its
#                relinked build prints nothing at all.
#
# The trap-free build is kept beside the installed one as REBUILT/<prog>.nocio
# so any swap is one move to undo, and so a person who strips the Microware
# runtime modules out still has something that runs.
set -u
here=$(cd "$(dirname "$0")/../.." && pwd)
compare=${1:?usage: install_relink.sh <compare.tsv> <outdir> [--apply]}
outdir=${2:?usage: install_relink.sh <compare.tsv> <outdir> [--apply]}
apply=${3:-}

exe=${OS9EXEC:-$here/../os9exec/os9exec}
image=${OS9IMAGE:-$here/osk-freeware.dd}
PREFIX=${PREFIX:-400}      # bytes compared when re-checking a DIFFERENT

capture() {   # $1 = directory to mount as /h5   $2 = program
  gtimeout 8 env OS9DISK="$image" OS9H5="$1" "$exe" -r "/h5/$2" </dev/null 2>&1 \
    | /usr/bin/tr -d '\000' \
    | LC_ALL=C /usr/bin/grep -av '^# /h0:' \
    | /usr/bin/head -c "$PREFIX"
}

installed=0; skipped=0; rechecked=0; saved=0
printf 'program\tdelta\tverdict\taction\n'
while IFS=$'\t' read -r prog old new delta verdict; do
  [ "$prog" = "program" ] && continue
  src=$outdir/$prog/$prog
  cur=$(find "$here/disk/CMDS" -name "$prog" -type f | head -1)
  [ -f "$src" ] && [ -n "$cur" ] || continue

  act=""
  case $verdict in
    SAME|NEW-SPEAKS) act=install ;;
    NEW-BROKEN)      act="skip (new is broken)" ;;
    BOTH-QUIET)      act="skip (no evidence)" ;;
    DIFFERENT)
      rechecked=$((rechecked+1))
      tmp=$outdir/.re.$prog; rm -rf "$tmp"; mkdir -p "$tmp/o" "$tmp/n"
      cp "$cur" "$tmp/o/$prog"; cp "$src" "$tmp/n/$prog"
      a=$(capture "$tmp/o" "$prog"); b=$(capture "$tmp/n" "$prog")
      rm -rf "$tmp"
      if [ "$a" = "$b" ] && [ -n "$a" ]; then act=install
      else act="skip (differs on first ${PREFIX}B)"; fi ;;
    *) act="skip ($verdict)" ;;
  esac

  if [ "$act" = install ]; then
    if [ "$apply" = "--apply" ]; then
      mkdir -p "$here/disk/CMDS/REBUILT"
      keep=$here/disk/CMDS/REBUILT/$prog.nocio
      [ -e "$keep" ] || cp "$cur" "$keep"
      cp "$src" "$cur"
    fi
    installed=$((installed+1)); saved=$((saved+delta))
  else
    skipped=$((skipped+1))
  fi
  printf '%s\t%s\t%s\t%s\n' "$prog" "$delta" "$verdict" "$act"
done < "$compare"

echo >&2
echo "  install: $installed   skip: $skipped   re-checked: $rechecked" >&2
echo "  bytes reclaimed: $saved" >&2
[ "$apply" = "--apply" ] || echo "  (dry run -- pass --apply to write)" >&2
