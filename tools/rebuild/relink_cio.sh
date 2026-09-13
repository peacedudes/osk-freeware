#!/bin/bash
# Rebuild trap-free programs against cio, which is now on the disk by permission.
#
# 199 programs were built `-qm' -- trap-free, stdio linked in -- because when
# they were rebuilt it was not known that Microware would permit cio, csl,
# csl020, math and math881. That reason expired on 2026-08-16. The builds are
# several times larger than the cio-linked equivalent: `wc' was 14,978 bytes
# trap-free and 1,430 linked against cio.
#
#   tools/rebuild/relink_cio.sh <list.tsv> <outdir> [max]
#
# <list.tsv>: prog TAB current-path TAB current-size TAB recipe-line
# Nothing is installed. Each result is reported and left in <outdir> for
# tools/rebuild/verify.sh and a human to judge.
#
# A GATE, ADDED 2026-08-31, AND IT IS NOT OPTIONAL.
#
# `-qixm' links the SDK's `LIB/cio.l', and that library is the $44 VINTAGE --
# the one whose `putc'/`getc' are MACROS whose slow path calls trap-13
# selectors $41/$42, where every `cio' MODULE anyone has puts a memory
# routine. So a relinked program is a $44 program, and if it ever runs one of
# those macros on a FILE it breaks exactly like the thirty in DOC/README-CIO:
# it opens your file, reads not one byte, and reports on it anyway.
#
# Eleven programs were shipped broken this way and had to be rebuilt `-qm' on
# 2026-08-31 to fix them. Relinking is not size-for-free; it is size in
# exchange for that risk, and the risk is only acceptable where the program
# has no such call site.
#
# `tools/cio_macro_scan.py' IS THE GATE. Relink where it is silent about a
# program; build `-qm' where it is not. This script now refuses a program the
# scan names, rather than leaving the judgement to whoever reads the results.
# `kermit_cio' is what that judgement cost last time: a relink this repository
# made, carrying the call sites, and the one build of kermit here that could
# only be driven in send mode.  It shipped for a fortnight and was dropped
# 2026-09-12; this gate is what came of it.
#
# Two flags are not optional and the reasons are old and expensive:
#   -qixm  links cio (this is the point; -qm is what we are undoing)
#   -n=    names the module. WITHOUT IT the module name comes from the -f
#          output filename, and 203 programs once reported themselves as
#          `R_make' in their own usage text.
#
# OS9CLEAN must be an SDK copy whose LIB/cstart* have the 64-byte Author psect
# blanked -- overwritten with spaces, SAME LENGTH, so no offset in the
# relocatable moves. Without it every binary is stamped with whoever owns the
# SDK, and check_disk.py counts those.
set -u
here=$(cd "$(dirname "$0")/../.." && pwd)
list=${1:?usage: relink_cio.sh <list.tsv> <outdir> [max]}
out=${2:?usage: relink_cio.sh <list.tsv> <outdir> [max]}
max=${3:-9999}

exe=${OS9EXEC:-$here/../os9exec/os9exec}
clean=${OS9CLEAN:?set OS9CLEAN to a clean SDK overlay}
src=$here/disk/SRC
compat=${OS9COMPAT:-$here/disk/SRC/COMPAT}

[ -x "$exe" ]   || { echo "no os9exec at $exe" >&2; exit 2; }
[ -d "$clean" ]  || { echo "no clean overlay at $clean" >&2; exit 2; }
[ -d "$compat" ] || { echo "no COMPAT headers at $compat" >&2; exit 2; }
mkdir -p "$out"

# The gate. A program with a putc/getc macro call site must not be relinked.
# ONE SPACE-SEPARATED LINE, not the newline-separated one awk emits: the
# `case' below matches on " $prog ", and against a newline-separated list that
# pattern never matches and the gate is silently open. It was, first time.
unsafe=$("$here/tools/cio_macro_scan.py" "$here/disk" 2>/dev/null \
         | awk '/_flshbuf=/ {n=split($1,p,"/"); print p[n]}' | tr '\n' ' ')
[ -n "$unsafe" ] || { echo "cio_macro_scan.py named nothing -- the gate would" \
                           "be open; refusing to relink anything" >&2; exit 2; }

printf 'program\ttree\told\tnew\tdelta\tverdict\n'
n=0
while IFS=$'\t' read -r prog path oldsize recipe; do
  n=$((n+1)); [ "$n" -gt "$max" ] && break
  IFS='|' read -r rprog tree sources defines libs flags <<< "$recipe"
  # THE GATE. See the header: -qixm links the $44 cio.l, so a program with a
  # putc/getc macro call site comes out broken. Refused rather than reported,
  # because the last time this was a judgement call it shipped kermit_cio.
  case " $unsafe " in
    *" $prog "*)
      printf '%s\t%s\t%s\t-\t-\tREFUSED: has a putc/getc macro call site\n' \
             "$prog" "$tree" "$oldsize"
      continue ;;
  esac
  [ -d "$src/$tree" ] || { printf '%s\t%s\t%s\t-\t-\tNO SOURCE TREE\n' "$prog" "$tree" "$oldsize"; continue; }

  work=$out/$prog
  rm -rf "$work"; mkdir -p "$work"
  cp "$src/$tree"/* "$work/" 2>/dev/null

  # -D for each define; extra libs and flags pass through verbatim
  dflags=""; for d in $defines; do dflags="$dflags -D$d"; done
  lflags=""; for l in $libs;    do lflags="$lflags -l=$l"; done

  # Mirrors tools/rebuild/rebuild.sh exactly, except -qixm where it uses -qm.
  # -V adds include directories: /h6 for the tree's own headers, /h7 for the
  # COMPAT shims (string.h, pwd.h, assert.h) OS-9 does not ship. Without /h7,
  # `yacc' stops at `can't open /dd/defs/assert.h'. The four libraries are
  # linked unconditionally because rebuild.sh does; wanderer wants math.l for
  # `_T$LtoD' and fails without it.
  log=$work/.build.log
  gtimeout 400 env OS9DISK="$clean" OS9H6="$work" OS9H7="$compat" "$exe" -r shell \
      "setenv CLIB /dd/LIB; setenv CDEF /dd/DEFS; chx /dd/CMDS; chd /h6; \
       cc $sources -qixm=16k $dflags -n=$prog -fd=$prog -V=/h6 -V=/h7 $flags $lflags \
       -l=/dd/LIB/curses.l -l=/dd/LIB/termlib.l -l=/dd/LIB/unix.l -l=/dd/LIB/math.l" \
      < /dev/null > "$log" 2>&1
  tr -d '\000' < "$log" > "$log.clean" && mv "$log.clean" "$log"

  if [ ! -f "$work/$prog" ]; then
    why=$(grep -aiE 'unresolved|l68: error|cannot|error' "$log" | head -1 | cut -c1-46)
    printf '%s\t%s\t%s\t-\t-\tBUILD FAILED: %s\n' "$prog" "$tree" "$oldsize" "${why:-no output}"
    continue
  fi

  newsize=$(stat -f%z "$work/$prog")
  # An author stamp here means OS9CLEAN was not actually clean.
  if grep -aq 'from the disk of' "$work/$prog"; then
    printf '%s\t%s\t%s\t%s\t-\tAUTHOR STAMP -- overlay not clean\n' "$prog" "$tree" "$oldsize" "$newsize"
    continue
  fi
  printf '%s\t%s\t%s\t%s\t%s\tbuilt\n' \
      "$prog" "$tree" "$oldsize" "$newsize" "$((oldsize-newsize))"
done < "$list"

# `< /dev/null` on the os9exec call above is load-bearing: without it the
# emulator reads the loop's own stdin and eats the rest of the list. Six
# programs in, the loop was being handed fragments of recipe lines as if they
# were program names. This collection's notes already warn about it.
