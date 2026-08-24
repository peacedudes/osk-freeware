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
  printf 'cc %s %s %s%s -n=%s -f=/h6/%s/R_%s -V=/h6/%s -V=/h7 %s%s' \
         "$2" "$QMFLAG" "$3" "$4" "$5" "$1" "$5" "$1" "$6" "$7"
  printf '%s\n' "$QMLIBS"
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
# Is this one source to go through ansi2knr?  Bare `KNR\' means every source in
# the recipe; `KNR=a.c,b.c\' means only those.  The selective form exists
# because ansi2knr is safe on an ANSI tree and NOT safe on a K&R one: given
# gtar\'s wildmat.c, whose parameters are declared `register char *s;\' on the
# lines after a K&R header, it emits `wildmat(s, p)  s; p;\' and adds two bogus
# declarations -- and a tree with five ANSI definitions among nineteen files
# came back with more damage than it started with.  JPEG is ANSI throughout and
# takes the bare form; gtar names its three.
knr_wanted() {     # $1 source file as the recipe spells it
  [ "$KNRMODE" = 1 ] || return 1
  [ -n "$KNRFILES" ] || return 0
  case " $KNRFILES " in *" $1 "*) return 0;; esac
  return 1
}

# THE TEMPORARY NAME FOR ONE SOURCE, on the CPP2 path.
#
# The basename, EXCEPT where two sources in the same recipe share one -- then
# the second and later get `_1\', `_2\' and so on.  macutils\' `binhex\' is the
# case: it names BINHEX/binhex.c, the program, AND CRC/binhex.c, its CRC table,
# and it wants both.  With a plain basename both became ctmp_binhex, the second
# overwrote the first, and the link reported `Symbol \'main\' unresolved\' with
# nothing anywhere to say why.
#
# FLATTENING THE PATH WAS THE FIRST FIX AND IT WAS WRONG: `../libray/LIBCOMMON/
# expr.c\' becomes `ctmp_libray_LIBCOMMON_expr.raw\', which is 31 characters,
# and **an OS-9 filename may be at most 29** -- measured 2026-08-23 by creating
# names of each length; 29 works, 30 does not.  cccp2 then cannot create its
# output and says `file not found\' about the file it is trying to WRITE, the
# shell\'s abort-on-error ends the run, and rayshade went from building to not.
# Suffixing only on a collision leaves every other recipe\'s names untouched.
#
# The plain-cc paths cannot do this -- there `cc -r\' names the object after the
# source and the collision is cc\'s, not ours -- so a same-basename recipe needs
# CPP2 for now.
tmpbase() {        # $1 source file  $2 the recipe\'s whole source list
  local b n=0 x y
  b=$(basename "$1"); b=${b%.cc}; b=${b%.c}; b=${b%.a}
  for x in $2; do
    [ "$x" = "$1" ] && break
    y=$(basename "$x"); y=${y%.cc}; y=${y%.c}; y=${y%.a}
    [ "$y" = "$b" ] && n=$((n+1))
  done
  if [ "$n" = 0 ]; then printf '%s' "$b"; else printf '%s_%d' "$b" "$n"; fi
}

# The object a source compiles to.  A translated source compiles as
# ctmp_<base>.c and so lands as ctmp_<base>.r; an untranslated one keeps its
# own name.  The merge list has to agree, or `merge\' stops at the first file
# it cannot open and the link then reports every symbol in the recipe
# unresolved -- which reads like a missing library, not a naming slip.
obj() {            # $1 source file
  if knr_wanted "$1"; then printf 'ctmp_%s.r' "$(basename "$1" .c)"
  else                     printf '%s.r' "$(basename "$1" .c)"; fi
}

# THE GNU PREPROCESSOR PATH.  A recipe asks for this with the CPP2
# pseudo-define, and it is the way round Microware `cpp\'s bus error on nested
# macro expansion (notes/CPP-MACRO-CRASH.md), which is what stops flex, gtar,
# djpeg and inform.
#
# `cccp2\' is GNU cpp 2.5.6 and it is in the SDK.  cc\'s phases are
# cpp -> c68 -> o68 -> r68, so this runs cccp2 in cpp\'s place and starts the
# chain at c68.  It takes TWO os9exec runs with a host-side pass between them,
# for two reasons that are not obvious:
#
#   * `# 1 "file"\' MARKERS MUST GO.  Microware\'s `.m\' is a directive stream,
#     not preprocessed C, and c68 reads a leading `#\' as a directive whose
#     argument is the NEXT LINE.  GNU\'s markers therefore swallow a line each.
#     Sixteen of them survive `-P\' in flex\'s misc.c, and one sits directly
#     before `extern char _chcodes[];\' -- which is why that identifier was
#     reported undeclared 1100 lines below where it is plainly declared.
#   * A PSECT PREAMBLE MUST GO IN FRONT.  `#P<name>_c\' is where c68 learns the
#     psect name; without it c68 emits no `psect\' line and r68 then rejects
#     every mnemonic in the file.
#
# Both edits happen host-side, between the runs, because /h6 is a host
# directory. Doing them with the OS-9 shell is not possible: `echo #P\' writes
# nothing, `#\' being a comment.
#
# CPP2 AND KNR TOGETHER.  A recipe may name both, and `djpeg\' is why: it is
# ANSI C, so it needs the ansi2knr pass, AND one of its thirty sources
# (jdmarker.c) is the one that bus-errors Microware\'s cpp.  Neither flag alone
# builds it -- KNR alone dies in cpp, CPP2 alone hands c68 a prototype.  When
# both are set the ansi2knr pass runs FIRST and cccp2 reads its output, because
# ansi2knr rewrites C and cccp2\'s output is no longer C that ansi2knr could
# read.
#
# THE RECIPE\'S OWN INCLUDE DIRECTORIES REACH THIS PASS TOO.  A recipe names an
# extra header directory as `-V=<dir>\' in its last field, which is what
# Microware `cc\' understands; GNU cpp spells the same thing `-I\'.  The first
# draft of this path passed only the three built-in directories, so a CPP2
# recipe\'s `-V=\' was silently ignored and every header under it came back
# `file not found\' -- gtar wants <grp.h> and <bcopy.h> out of /dd/DEFS/os9lib,
# and that is how it presented.  Translating here keeps ONE spelling in the
# recipe file whichever path builds it.
#
# They go in AHEAD of /h7 and /dd/DEFS, second only to the tree's own directory,
# because a recipe that names a header directory is usually naming the one its
# port was written against, and wants it to WIN.  gtar again: /dd/DEFS/os9lib
# is a complete alternate DEFS set whose <errno.h> carries the Unix codes and
# `extern int errno\', and behind /dd/DEFS it never gets looked at at all.
compile_cpp2_pre() {   # $1 arch  $2 sources  $3 oskdef  $4 defines  $5 extra
  local inc="" x
  for x in ${5:-}; do
    case "$x" in -V=*) inc="$inc -I${x#-V=}";; esac
  done
  printf 'chx /dd/CMDS\nchd /h6/%s\n' "$1"
  for s in $2; do
    base=$(tmpbase "$s" "$2")
    src=$s
    if knr_wanted "$s"; then
      printf 'del ctmp_%s.c\nansi2knr %s ctmp_%s.c\n' "$base" "$s" "$base"
      src=ctmp_$base.c
    fi
    printf 'del ctmp_%s.raw\n' "$base"
    printf 'cccp2 -P -traditional %s%s -I/h6/%s%s -I/h7 -I/dd/DEFS %s ctmp_%s.raw\n' \
           "$3" "$4" "$1" "$inc" "$src" "$base"
  done
  printf '\033\n\004\n'
}

# The third host-side edit: RE-WRAP LINES GNU cpp MADE TOO LONG.
#
# Two limits govern this and BOTH were measured on 2026-08-23, by feeding each
# tool one-line files of rising length, rather than read off any manual:
#
#   * Microware `cpp\' bus-errors on a source line of 513 characters or more.
#     512 is fine.  That single 512-byte line buffer -- not "nested macro
#     expansion" -- is what stops flex, gtar, djpeg and inform; nesting is just
#     the usual way a line gets that long.  See notes/CPP-MACRO-CRASH.md.
#   * c68 reads at most 1022 characters in a line and says `input line too
#     long\' at 1023.
#
# So GNU cpp gets past the first limit and can walk straight into the second:
# Microware\'s cpp keeps a source\'s backslash-newline continuations, GNU\'s
# splices them, and gtar\'s tar.c usage text -- five fputs and fprintf calls
# written across forty continued lines -- arrives as 2113 characters on one.
#
# THE CUT MUST FALL OUTSIDE A STRING LITERAL.  c68 has neither of the two ways
# a long literal is normally split: adjacent-literal concatenation (`"a" "b"\')
# is ANSI and it is K&R, and a backslash-newline INSIDE a literal is spliced in
# translation phase 2, which for a `.m\' file already happened -- in Microware\'s
# cpp, which is the phase being replaced.  Both were tried and both give
# `unterminated string\'.  So a literal is indivisible here and the wrap breaks
# only at whitespace between tokens, which is enough because what makes these
# lines long is several STATEMENTS joined, not one enormous literal: tar.c\'s
# longest single literal is 622 characters, comfortably inside c68\'s 1022.
#
# When no cut fits, the line is left alone rather than cut somewhere unsafe --
# `input line too long\' is a diagnostic somebody can act on, and a literal
# broken in half is a mystery.
cpp2_fixup() {         # $1 sources  $2 dir
  python3 - "$2" $1 <<'FIXUP'
import os, sys

WIDTH = 1000         # inside c68's measured 1022

def breakpoints(line):
    """Indices of the whitespace outside any literal, where a cut is safe."""
    pts, instr, inchr, esc = [], False, False, False
    for i, c in enumerate(line):
        if esc:
            esc = False
        elif c == "\\" and (instr or inchr):
            esc = True
        elif instr:
            instr = c != '"'
        elif inchr:
            inchr = c != "'"
        elif c == '"':
            instr = True
        elif c == "'":
            inchr = True
        elif c in " \t" and i:
            pts.append(i)
    return pts

def wrap(line):
    if len(line) <= WIDTH:
        return [line]
    pts, out, start = breakpoints(line), [], 0
    while len(line) - start > WIDTH:
        fits = [i for i in pts if start < i <= start + WIDTH]
        if not fits:
            break                    # nothing safe within reach: leave it long
        out.append(line[start:fits[-1]])
        start = fits[-1] + 1
    out.append(line[start:])
    return out

d, srcs = sys.argv[1], sys.argv[2:]
for i, s in enumerate(srcs):
    base = os.path.basename(s)[:-2]
    n = sum(1 for e in srcs[:i] if os.path.basename(e) == os.path.basename(s))
    if n:
        base = "%s_%d" % (base, n)
    raw = os.path.join(d, "ctmp_%s.raw" % base)
    if not os.path.exists(raw):
        continue
    body = open(raw, "rb").read().decode("latin-1")
    kept = []
    for l in body.split("\r"):
        if not l.startswith("#"):
            kept.extend(wrap(l))
    head = "#P\r%s_c\r0\r#7\r%s\r%s_c\r#5\r0\r" % (base, s, base)
    open(os.path.join(d, "ctmp_%s.m" % base), "wb").write(
        (head + "\r".join(kept)).encode("latin-1"))
FIXUP
}

# LONGREF: `c68 -k\', AND NO o68 PASS -- the two are inseparable.
#
# A module whose code passes 32K cannot reach all of itself with the 68000\'s
# 16-bit BSR displacement, and r68 says `*** error - branch out of range ***\'
# once per call.  `c68 -k\' (force long PC-relative references) is the answer,
# and `inform\' -- one 4,400-line source, 100K of code -- is the program that
# needs it.
#
# But `o68\', the object-code improver, MISCOMPILES what -k emits, and it does
# so silently.  Measured 2026-08-23 with a ten-case probe: given a conditional
# expression choosing between two string LITERALS, the TRUE arm gets the wrong
# address -- `one ? "Error" : "Warning"\' prints `rning\'.  Nothing else in the
# probe moved: plain literals, an array of them, if/else, switch, and a
# function returning one are all correct with -k, and every case is correct
# with -k and no o68.  inform showed it as two impossible diagnostics on every
# source it compiled ("Names are not permitted to start with an _" against a
# `for\' loop) and a summary reading "0 warningsput)".
#
# Dropping o68 costs some optimisation and nothing else: r68 assembles c68\'s
# output directly.  With it dropped, inform compiles the collection\'s own
# hellow.inf to a story file BYTE-IDENTICAL to the hellow.z3 in GAMES/INFORM.
#
# If you ever want -k on the ordinary `cc\' path instead, it is `-K=0CL\' --
# and you must add `-O\' with it, for the same reason.
#
# M020: THE 68020 BACKEND, and it is a different answer to a different wall.
# r68 says `*** error - value out of range ***' when a stack displacement
# passes the 68000's signed 16-bit limit -- rayshade's shadow.c reaches
# 39586(sp).  `cc -K=2L' answers that by running c68020 and r68020 instead of
# c68 and r68, and this is the same thing for the CPP2 path.
#
# The o68 bug above does NOT apply here, measured the same day: `cc -K=2L'
# runs c68020 -k AND o68, and the ten-case probe comes back perfect.  So the
# defect is o68 mis-optimising the 68000 c68's long-PC-relative output
# specifically, and the one existing -K=2L recipe (`xcrypt') was never at risk.
# M020 therefore keeps the o68 pass; LONGREF is the one that must drop it.
#
# The cost is a 68020-only binary, so ask for it only where the program
# already wants one -- rayshade's own makefile says `-mc68040'.
compile_cpp2_post() {  # $1 arch  $2 sources  $3 prog  $4 extra  $5 libs  $6 dir
  local mainsrc="" s base
  for s in $2; do
    [ -n "$mainsrc" ] && break                 # FIRST match, not last -- see below
    /usr/bin/tr '\r' '\n' < "$6/$s" |
      /usr/bin/grep -qaE '^([A-Za-z_][A-Za-z0-9_ *]*[ *])?main[[:space:]]*\(' &&
        mainsrc=$s
  done
  [ -n "$mainsrc" ] || { echo "  $3: no main() among its sources" >&2; return 1; }

  : > "$6/ctmp.list"
  for s in $2; do
    base=$(tmpbase "$s" "$2")
    [ "$s" = "$mainsrc" ] || printf '%s\r' "ctmp_$base.r" >> "$6/ctmp.list"
  done

  printf 'setenv CLIB /dd/LIB\nsetenv CDEF /dd/DEFS\nchx /dd/CMDS\nchd /h6/%s\n' "$1"
  for s in $2; do
    base=$(tmpbase "$s" "$2")
    printf 'del ctmp_%s.a\ndel ctmp_%s.o\ndel ctmp_%s.r\n' "$base" "$base" "$base"
    if [ "$M020" = 1 ]; then
      printf 'c68020 ctmp_%s.m -t -k -o=ctmp_%s.a\n' "$base" "$base"
      printf 'o68 ctmp_%s.a ctmp_%s.o\n' "$base" "$base"
      printf 'r68020 ctmp_%s.o -q -o=/h6/%s/ctmp_%s.r\n' "$base" "$1" "$base"
    elif [ "$LONGREF" = 1 ]; then
      printf 'c68 ctmp_%s.m -t -k -o=ctmp_%s.a\n' "$base" "$base"
      printf 'r68 ctmp_%s.a -q -o=/h6/%s/ctmp_%s.r\n' "$base" "$1" "$base"
    else
      printf 'c68 ctmp_%s.m -t -o=ctmp_%s.a\n' "$base" "$base"
      printf 'o68 ctmp_%s.a ctmp_%s.o\n' "$base" "$base"
      printf 'r68 ctmp_%s.o -q -o=/h6/%s/ctmp_%s.r\n' "$base" "$1" "$base"
    fi
  done
  printf 'del ctmp.parts.l\nmerge -z=ctmp.list >ctmp.parts.l\n'
  printf 'cc ctmp_%s.r %s -n=%s -f=/h6/%s/R_%s -l=ctmp.parts.l -l=ctmp.parts.l -l=ctmp.parts.l %s%s' \
         "$(tmpbase "$mainsrc" "$2")" "$QMFLAG" "$3" "$1" "$3" "$4" "$5"
  printf '%s\n' "$QMLIBS"
  printf '\033\n\004\n'
}

# THE GCC PATH.  A recipe asks for this with the GCC pseudo-define.
#
# WHY IT EXISTS.  Several of the OSK ports here were never written for
# Microware\'s cc at all -- their own makefiles say `CC = gcc\' (gtar,
# rayshade) or `CC = gcc2\' (mtools, jpeglib).  GCC is ANSI, has no
# 512-character line limit, and has -mlong-calls; every one of those is a wall
# the cc path hits.  A complete GCC 2.5.6 is on this disk, in CMDS/GCC2.
#
# It was UNUSABLE until 2026-08-23: `#include <ctype.h>\' followed by
# `#include <stdlib.h>\' -- two lines, no program -- would not compile,
# because DEFS/GCC2/stdlib.h declares the ctype functions the SDK\'s
# <ctype.h> defines as macros, and pulls in a <direct.h> that wants a WORD
# typedef GCC\'s own <stdio.h> does not have.  Both are fixed in those two
# headers; without that fix nothing below works.
#
# FOUR THINGS ARE NOT GUESSABLE:
#
#   * gcc2 PREDEFINES OSK (and _OSK, __OSK__, mc68000), so this path does NOT
#     pass -DOSK.  Passing it again is a redefinition.
#   * `gcc2 -c -o <name>.r <src>\' controls the object name, which is what
#     keeps two sources of the same basename apart -- see tmpbase().
#   * THE LINK CANNOT BE gcc2, because the module would take its name from
#     the output FILE.  We write R_<prog> so as not to clobber an archive
#     binary, and the module would then call itself `R_<prog>\' in its own
#     usage text -- the exact fault the -n= rule exists to prevent, and
#     `-Wl,-n=\' does not reach l68.  So the link is l68 by hand, which is
#     what gcc2 -v shows it running anyway:
#         l68 -o=<out> -a /DD/LIB/cstart.r <objs> -l=libgcc.l -l=clibn.l
#             -l=math.l -l=sys.l
#     plus -n=<prog>.  Verified: gcc2 gives a module called R_wl, l68 -n=
#     gives one called named.
#   * SRC/COMPAT IS **NOT** ON THE PATH HERE -- it is opt-in, as `-V=/h7\'.
#     Every other path adds it automatically, because it exists to fill gaps in
#     Microware cc\'s header set.  GCC brings its own, and COMPAT then SHADOWS
#     them: its <stdlib.h> had neither RAND_MAX nor size_t (fixed since, but it
#     is still thinner), and its <types.h> typedefs off_t, which collides with
#     the one mtools\' sysincludes.h declares for itself under _OSK.  lua does
#     want it -- GCC has no <limits.h> at all -- so lua asks with -V=/h7 and
#     mtools does not.  A shim that shadows a better header has to be at least
#     as complete as the thing it hides, and COMPAT is not trying to be.
#   * `clibn.l\' is the no-cio C library and `cstart.r\' comes from the
#     overlay, whose Author psect is blanked -- so a GCC build is trap-free
#     and unstamped, both of which this collection requires.  Measured.
compile_gcc() {    # $1 arch  $2 sources  $3 defines  $4 prog  $5 extra  $6 libs  $7 dir
  local mainsrc="" s base inc="" lnk="" x
  # -V=<dir> becomes an -I for the compile; anything else in the extra field is
  # for the LINK, which here is l68 -- `-M=32k' for stack, and mtools wants it
  # (mdir bare says `**** Stack Overflow ****' without).
  for x in ${5:-}; do
    case "$x" in -V=*) inc="$inc -I${x#-V=}";; *) lnk="$lnk $x";; esac
  done
  for s in $2; do
    [ -n "$mainsrc" ] && break
    /usr/bin/tr '\r' '\n' < "$7/$s" |
      /usr/bin/grep -qaE '^([A-Za-z_][A-Za-z0-9_ *]*[ *])?main[[:space:]]*\(' &&
        mainsrc=$s
  done
  [ -n "$mainsrc" ] || { echo "  $4: no main() among its sources" >&2; return 1; }

  : > "$7/ctmp.list"
  for s in $2; do
    [ "$s" = "$mainsrc" ] && continue
    printf '%s\r' "ctmp_$(tmpbase "$s" "$2").r" >> "$7/ctmp.list"
  done

  printf 'chx /dd/CMDS\nchd /h6/%s\n' "$1"
  for s in $2; do
    base=$(tmpbase "$s" "$2")
    printf 'del ctmp_%s.r\n' "$base"
    printf 'gcc2 -c %s -I/h6/%s%s -o ctmp_%s.r %s\n' \
           "$3" "$1" "$inc" "$base" "$s"
  done
  # THREE COPIES UNDER THREE NAMES, not one name three times.  l68 makes a
  # single pass per DISTINCT library FILE -- repeating `-l=x.l' buys nothing,
  # which is not what the failure table used to imply.  A member that calls a
  # member defined later in the same file is otherwise left unresolved:
  # mtools' codepage.c calls strtoul, and its own missing_functions.c defines
  # strerror, and both sit after their callers.
  printf 'del ctmp.parts.l\nmerge -z=ctmp.list >ctmp.parts.l\n'
  printf 'del ctmp.parts2.l\ndel ctmp.parts3.l\n'
  printf 'copy -r ctmp.parts.l ctmp.parts2.l\ncopy -r ctmp.parts.l ctmp.parts3.l\n'
  printf 'l68 -o=/h6/%s/R_%s -a -n=%s /dd/LIB/cstart.r ctmp_%s.r' \
         "$1" "$4" "$4" "$(tmpbase "$mainsrc" "$2")"
  printf '%s -l=ctmp.parts.l -l=ctmp.parts2.l -l=ctmp.parts3.l%s' "$lnk" "$6"
  printf ' -l=/dd/LIB/libgcc.l -l=/dd/LIB/clibn.l -l=/dd/LIB/math.l -l=/dd/LIB/sys.l\n'
  printf '\033\n\004\n'
}

# 68k assembly, through r68.  A recipe asks for this with ASM; sources end .a.
#
# NO cstart.  An assembly module carries its own psect -- type, attributes,
# entry point -- so l68 gets the objects and two libraries and nothing else.
#
# Those two libraries are the whole trick.  ATerm refers to 53 names it never
# defines (F$Fork, I$GetStt, SS_Opt, PD_BAU, E$CEF, C$CR ...) and the Microware
# ASSEMBLER definitions file that would supply them is NOT in this SDK copy --
# DEFS/oskdefs.d here is 1470 bytes and holds only the module type and
# permission equates.  `os9.l' and `sys.l' between them resolve all 53, so the
# link that looked like it needed a missing header only needed two -l=.
#
# MODNAME matters, and its CASE matters.  With -n=ATerm this produces a module
# byte-for-byte identical to the aterm that ships; with -n=aterm it differs in
# exactly five bytes, two in the name and the three CRC bytes after it.
compile_asm() {    # $1 arch  $2 sources  $3 defines(unused)  $4 prog  $5 extra  $6 libs  $7 dir
  local s base inc="" lnk="" x objs=""
  for x in ${5:-}; do
    case "$x" in -V=*) inc="$inc -V=${x#-V=}";; *) lnk="$lnk $x";; esac
  done
  printf 'chx /dd/CMDS\nchd /h6/%s\n' "$1"
  for s in $2; do
    base=$(tmpbase "$s" "$2")
    printf 'del ctmp_%s.r\n' "$base"
    printf 'r68 %s -o=ctmp_%s.r%s\n' "$s" "$base" "$inc"
    objs="$objs ctmp_$base.r"
  done
  printf 'del R_%s\n' "$4"
  printf 'l68 -o=/h6/%s/R_%s -a -n=%s%s%s -l=/dd/LIB/os9.l -l=/dd/LIB/sys.l%s\n' \
         "$1" "$4" "${MODNAME:-$4}" "$objs" "$lnk" "$6"
  printf '\033\n\004\n'
}

# C++, through gpp.  A recipe asks for this with GPP, and sources end in .cc.
#
# gcc2 cannot start the C++ front end AT ALL: its suffix table has no entry for
# a .cc and it answers `linker input file unused since linking not done'.  The
# only door is `gpp', which make_overlay.sh has to supply two extra names for
# (see the comment there) -- `cccp', which gpp forks, and `gpp.l', which
# collect opens.
#
# The LINK goes through gpp as well, and NOT through l68 by hand the way the C
# path does it.  A C++ program with any global constructor needs
# __CTOR_LIST__ and __DTOR_LIST__, only `collect' builds those, and only gpp's
# spec runs collect.  gpp has no -n=, so the module takes its name from the
# OUTPUT FILE -- which is exactly what is wanted here: write the file as
# <prog>, so the module inside is called <prog>, and rename the FILE to
# R_<prog> afterwards.  Renaming a file does not touch the module name.
compile_gpp() {    # $1 arch  $2 sources  $3 defines  $4 prog  $5 extra  $6 libs  $7 dir
  local s base inc="" lnk="" x objs=""
  for x in ${5:-}; do
    case "$x" in -V=*) inc="$inc -I${x#-V=}";; *) lnk="$lnk $x";; esac
  done
  printf 'chx /dd/CMDS\nchd /h6/%s\n' "$1"
  for s in $2; do
    base=$(tmpbase "$s" "$2")
    printf 'del ctmp_%s.r\n' "$base"
    printf 'gpp -c %s -I/h6/%s%s -o ctmp_%s.r %s\n' "$3" "$1" "$inc" "$base" "$s"
    objs="$objs ctmp_$base.r"
  done
  # The output file MUST be called <prog>, because that is where the module
  # gets its name -- and in this tree <prog> is very often also the name of a
  # DIRECTORY (homelibr/Librarian holds Librarian.cc).  The first version of
  # this wrote <prog> in place and then renamed it, which on a failed link
  # renamed the SOURCE DIRECTORY to R_<prog>.  So: link inside a scratch
  # directory, where no name can collide, and copy the result out.  A failed
  # link leaves no R_<prog>, which is exactly how a failure should read.
  printf 'makdir ctmpout\n'
  printf 'del ctmpout/%s\ndel R_%s\n' "$4" "$4"
  printf 'gpp -o ctmpout/%s%s%s%s\n' "$4" "$objs" "$lnk" "$6"
  printf 'copy -r ctmpout/%s R_%s\n' "$4" "$4"
  printf 'del ctmpout/%s\n' "$4"
  printf '\033\n\004\n'
}

# ANSI C, run through ansi2knr first.  A recipe asks for this with the KNR
# pseudo-define, the way NOOSK opts out of -DOSK.  Microware's cc is K&R and
# will not read a prototype; ansi2knr is the standard de-ANSIfier, is itself
# K&R so it bootstraps, and builds here.  A translated source becomes a
# ctmp_<base>.c beside it and that is what gets compiled.
#
# `KNR' translates every source; `KNR=a.c,b.c' translates only those.  Reach
# for the selective form on a tree that is mostly K&R -- see knr_wanted().
#
# KNR implies the long path whatever the line length: the one-line form has
# nowhere to put the intermediate.
compile_knr() {    # $1 arch  $2 sources  $3 oskdef  $4 defines  $5 prog  $6 extra  $7 libs  $8 dir
  local mainsrc="" s base
  for s in $2; do
    [ -n "$mainsrc" ] && break                 # FIRST match, not last
    /usr/bin/tr '\r' '\n' < "$8/$s" |
      /usr/bin/grep -qaE '^([A-Za-z_][A-Za-z0-9_ *]*[ *])?main[[:space:]]*\(' &&
        mainsrc=$s
  done
  [ -n "$mainsrc" ] || { echo "  $5: no main() among its sources" >&2; return 1; }

  : > "$8/ctmp.list"
  for s in $2; do
    [ "$s" = "$mainsrc" ] && continue
    printf '%s\r' "$(obj "$s")" >> "$8/ctmp.list"
  done

  printf 'setenv CLIB /dd/LIB\nsetenv CDEF /dd/DEFS\nchx /dd/CMDS\nchd /h6/%s\n' "$1"
  for s in $2; do
    base=$(basename "$s" .c)
    if knr_wanted "$s"; then
      printf 'del ctmp_%s.c\nansi2knr %s ctmp_%s.c\n' "$base" "$s" "$base"
      printf 'cc ctmp_%s.c %s%s -r=/h6/%s -V=/h6/%s -V=/h7 %s\n' \
             "$base" "$3" "$4" "$1" "$1" "$6"
    else
      printf 'cc %s %s%s -r=/h6/%s -V=/h6/%s -V=/h7 %s\n' \
             "$s" "$3" "$4" "$1" "$1" "$6"
    fi
  done
  printf 'del ctmp.parts.l\nmerge -z=ctmp.list >ctmp.parts.l\n'
  printf 'cc %s %s -n=%s -f=/h6/%s/R_%s -l=ctmp.parts.l -l=ctmp.parts.l -l=ctmp.parts.l %s%s' \
         "$(obj "$mainsrc")" "$QMFLAG" "$5" "$1" "$5" "$6" "$7"
  printf '%s\n' "$QMLIBS"
  printf '\033\n\004\n'
}

# WHICH SOURCE HOLDS main().  The FIRST one in the recipe that has it, not the
# last -- and the difference is not academic.  GNU `ed' builds getopt1.c, whose
# tail is a `#ifdef TEST' self-test with a main() of its own; taking the last
# match linked `ed' as getopt1's test harness, silently, with no diagnostic
# anywhere.  A recipe names the program's own source first by convention, and
# now that convention is what decides.
compile_long() {   # $1 arch  $2 sources  $3 oskdef  $4 defines  $5 prog  $6 extra  $7 libs  $8 dir
  # Through `tr' first: these sources are CR-terminated, so grep sees the whole
  # file as ONE line and `^' matches only at its start. Without that, zoo.c's
  # `main(argc, argv)' is invisible and the recipe is reported as having no
  # main() at all.
  local mainsrc="" s
  for s in $2; do
    [ -n "$mainsrc" ] && break                 # FIRST match, not last
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
  printf 'cc %s.r %s -n=%s -f=/h6/%s/R_%s -l=ctmp.parts.l -l=ctmp.parts.l -l=ctmp.parts.l -l=ctmp.parts.l -l=ctmp.parts.l %s%s' \
         "$(basename "$mainsrc" .c)" "$QMFLAG" "$5" "$1" "$5" "$6" "$7"
  printf '%s\n' "$QMLIBS"
  printf '\033\n\004\n'
}

# $LIMIT seconds per program.  240 is right for a one-line build; the
# long-argument path compiles each source separately and zoo's 35 and mtools'
# 45 both ran past it and were recorded FAIL with no output at all.
LIMIT=240
# /h0 IS THE OVERLAY TOO -- the arrangement the finished disk ships under,
# mounted as /dd and hard-linked as /h0 (notes/DECISION-placement.md).  Headers
# here carry /h0-absolute includes because the people who wrote them kept their
# tools there: DEFS/os9lib/time.h asks for </h0/defs/setsys.h>, and no -V or -I
# can redirect an absolute path.  Without an /h0 the whole os9lib DEFS set is
# unusable -- and os9lib is the only place on this disk with uid_t, S_IRUSR,
# S_ISUID, ERROR, TRUE, FALSE and the Unix errno codes, which is what gtar and
# GNU ls were both written against.
run() {       # $1 pool  $2 command-file  $3 output file
  ( cd "$REPO" && gtimeout "$LIMIT" env OS9DISK="$OS9CLEAN" OS9H0="$OS9CLEAN" \
      OS9H6="$1" OS9H7="$OS9COMPAT" \
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
  # One pass over the field, not three substitutions: `${defs/KNR/}' turns
  # `KNR=a.c,b.c' into `=a.c,b.c', which then reaches cc as `-D=a.c,b.c'.
  OSKDEF=-DOSK
  KNRMODE=0; KNRFILES=""; CPP2MODE=0; LONGREF=0; M020=0; GCCMODE=0; GPPMODE=0; ASMMODE=0; MODNAME=""; TRAPFREE=0; keep=""
  for x in $defs; do
    case "$x" in
      NOOSK)  OSKDEF="";;
      KNR)    KNRMODE=1;;
      KNR=*)  KNRMODE=1
              KNRFILES=$(printf '%s' "${x#KNR=}" | /usr/bin/tr ',' ' ');;
      CPP2)   CPP2MODE=1;;
      LONGREF) LONGREF=1;;
      M020)   M020=1;;
      GCC)    GCCMODE=1;;
      GPP)    GPPMODE=1;;
      ASM)    ASMMODE=1;;
      MODNAME=*) MODNAME=${x#MODNAME=};;
      TRAPFREE) TRAPFREE=1;;
      *)      keep="$keep $x";;
    esac
  done
  defs=$keep

  # A word that already begins with `-\' is passed through as it stands, so a
  # recipe can say `-U_OSK\'.  gcc2 PREDEFINES _OSK, and lua\'s lua.c reaches
  # for a header the tree does not carry when it is set; there is no other way
  # to turn a predefine off.  Everything else becomes -D<word> as before.
  # -qixm LINKS THE cio TRAP HANDLER; -qm links stdio into the module instead.
  # cio, csl, math, math881 and csl020 SHIP on this disk now, with Microware's
  # permission, so a program that needs cio works for anybody using the
  # collection -- and it is markedly smaller: 7478 bytes against 11476 for the
  # same source, measured 2026-08-24.  -qm was the right default only while
  # cio could not be shipped.
  #
  # A recipe says TRAPFREE when a binary has to stand alone anyway.  Note this
  # changes only what lands in built/; nothing is installed by this driver, so
  # DOC/INDEX's star grid does not move until somebody installs one on purpose.
  # THREE WAYS TO LINK, and the smallest is not always available.  Measured on
  # SRC/misc/ascii.c, 2026-08-24:
  #
  #     -qm     14286 bytes   clibn.l + math.l   stands alone
  #     -qxm    10022          clib.l            uses the math trap
  #     -qixm    2610          cio.l + clib.l    uses cio and math
  #
  # cio, csl, math and math881 ship on this disk by Microware's permission, so
  # depending on them is free for anybody using the collection, and -qixm is a
  # fifth of the size.  But cc hands l68 BOTH cio.l and clib.l for -qixm, and
  # this SDK's clib.l is not a reduced library -- it is 38667 bytes against
  # clibn.l's 38523, so it still has printf and time.  Whether that collides
  # depends on which members l68 happens to pull: `banner' links, `joke' stops
  # with `Symbol printf from psect cio_a ... caused name clashes'.  Thirteen of
  # 290 broke that way.  CLAUDE.md already said "never -qixm"; this is why.
  #
  # So take the best each program can actually have: try -qixm, and on a
  # duplicate-symbol failure drop to -qxm, which links clib.l alone and still
  # saves a third.  TRAPFREE forces the standalone build.
  QMFLAG=-qixm=16k
  QMLIBS=' -l=/dd/LIB/curses.l -l=/dd/LIB/termlib.l'
  # $TRAPFREE, not $defs: the pseudo-define loop above has already taken the
  # word out of defs, so testing defs here always failed and TRAPFREE silently
  # did nothing.
  if [ "$TRAPFREE" = 1 ]; then
    QMFLAG=-qm=16k
    QMLIBS=' -l=/dd/LIB/curses.l -l=/dd/LIB/termlib.l -l=/dd/LIB/unix.l -l=/dd/LIB/math.l'
  fi

  D=""
  for x in $defs; do
    [ -n "$x" ] || continue
    case "$x" in -*) D="$D $x";; *) D="$D -D$x";; esac
  done
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
    if [ "$ASMMODE" = 1 ]; then
      compile_asm "$arch" "$1" "$D" "$prog" "${extra:-}" "$L" "$d" > "$WORK/cmd" || return
      run "$POOL" "$WORK/cmd" "$WORK/out"
      return
    fi
    if [ "$GPPMODE" = 1 ]; then
      compile_gpp "$arch" "$1" "$D" "$prog" "${extra:-}" "$L" "$d" > "$WORK/cmd" || return
      LIMIT=2400
      run "$POOL" "$WORK/cmd" "$WORK/out"
      return
    fi
    if [ "$GCCMODE" = 1 ]; then
      compile_gcc "$arch" "$1" "$D" "$prog" "${extra:-}" "$L" "$d" > "$WORK/cmd" || return
      LIMIT=1800
      run "$POOL" "$WORK/cmd" "$WORK/out"
      return
    fi
    if [ "$CPP2MODE" = 1 ]; then
      LIMIT=1800
      compile_cpp2_pre "$arch" "$1" "$OSKDEF" "$D" "${extra:-}" > "$WORK/cmd"
      run "$POOL" "$WORK/cmd" "$WORK/out1"
      cpp2_fixup "$1" "$d"
      compile_cpp2_post "$arch" "$1" "$prog" "${extra:-}" "$L" "$d" > "$WORK/cmd" || return
      /bin/cat "$WORK/out1"
      run "$POOL" "$WORK/cmd" "$WORK/out"
      return
    fi
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

  # THE LINK FALLBACK.  Try the smallest linkage first and step down until one
  # produces a module.  Each step is tried at most once and only if the last
  # left no R_<prog> behind, so a program that links small keeps the small
  # build and nothing is rebuilt for the sake of it.
  if [ "$QMFLAG" = "-qixm=16k" ] && [ "$TRAPFREE" != 1 ]; then
    for step in qxm qm; do
      [ -f "$d/R_$prog" ] && break
      case "$step" in
        qxm) QMFLAG=-qxm=16k
             # math.l as well: -x says "reach the math library through traps",
             # and l68 still wants _T$LtoD and friends resolved at link time.
             # cc's own -qxm line does not supply them; `robots' found it.
             QMLIBS=' -l=/dd/LIB/curses.l -l=/dd/LIB/termlib.l -l=/dd/LIB/math.l';;
        qm)  QMFLAG=-qm=16k
             QMLIBS=' -l=/dd/LIB/curses.l -l=/dd/LIB/termlib.l -l=/dd/LIB/unix.l -l=/dd/LIB/math.l';;
      esac
      out=$(attempt "$srcs")
      printf '=== %s (%s) RETRY linkage %s\n' "$prog" "$arch" "$step" >> "$LOG"
    done
  fi
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
      *"'geteuid' unresolved"*|*"'getuid' unresolved"*|*"'unix_getuid' unresolved"*) shim=os9geteuid.c;;
      *"'ftime' unresolved"*)                                                     shim=os9ftime.c;;
      *"'_ss_wfm' unresolved"*)                                                   shim=os9sswfm.c;;
      *"'popen' unresolved"*|*"'pclose' unresolved"*)                               shim=os9popen.c;;
      *"'strucmp' unresolved"*|*"'strnucmp' unresolved"*|*"'strstr' unresolved"*|*"'rename' unresolved"*) shim=os9alib.c;;
      *"'ctime' unresolved"*)                                                     shim=os9ctime.c;;
      *"'strtol' unresolved"*|*"'strtoul' unresolved"*)                            shim=os9strtol.c;;
      *"'isgraph' unresolved"*)                                                   shim=os9isgraph.c;;
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
