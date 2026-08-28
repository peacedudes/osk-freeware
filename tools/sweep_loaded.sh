#!/bin/bash
# Run every program under disk/CMDS with the LIBRARY MODULES LOADED, and
# classify what happens -- the sweep `notes/PLAN-verification.md` calls step 0.
#
# WHY THIS EXISTS.  Every sweep this collection has ever run started every
# program with an EMPTY module directory.  A program that links a library
# MODULE rather than a file -- the RTF Fortran set links `os9lib', the Atari
# demos link `Graph', `ptxminst' links `Ptxm' -- exits at F$Link before it
# prints anything, and was recorded SILENT on a condition that cannot happen
# on a real system.  Six programs sat in "silent in every stage" for weeks
# for that reason alone.
#
# What makes this possible is that the disk now HAS a `load': CMDS/load,
# clean-room, contributed 2026-08-27.  Before that the only one available was
# Microware's, from an SDK outside the tree.
#
# Each program gets its own emulator start, because a module directory does
# not survive one: the run is `bash <script>' where the script loads the
# libraries and then runs the one program.  That costs about a second more
# per program than `verify_all.sh' and buys the only condition a real system
# would ever present.
#
# ONE DIFFERENCE FROM `verify_all.sh' WORTH KNOWING: this runs each program
# from bash rather than as the emulator's own boot program, so the program
# inherits bash's environment -- TERM=dumb rather than unset, for one.  A
# program that reports `unknown terminal type dumb' here and `unknown
# terminal type' there has not changed behaviour.  Compare VERDICTS, not
# evidence strings.
#
# Usage:  tools/sweep_loaded.sh [<disk-dir> [<image>]]
# Env:    OS9EXEC   path to os9exec        JOBS  parallel runs (default 6)
# Verdicts, as `verify_all.sh' uses them, plus one:
#   NOTPROG  bash refused it -- a trap module, a driver, a data file.  Bare,
#            those score NOSTART; through a shell they get its complaint
#            instead, and the first run of this sweep read thirty of them as
#            OK because the complaint was output.
#
# THE ENVIRONMENT IS THE ONE A PERSON ARRIVES WITH -- what SYS/login sets --
# because that is the condition being measured: not "bare plus a load" but
# "run the way the disk is meant to be run".  `aterm' and `snake' both need
# it, and both were CRASH in the bare sweep.
#
# Output: notes/verify-loaded.tsv   program, directory, verdict, evidence
#         and, where notes/verify-bare.tsv exists, what CHANGED.
set -u
here=$(cd "$(dirname "$0")/.." && pwd)
disk=${1:-$here/disk}
image=${2:-$here/osk-freeware.dd}
exe=${OS9EXEC:-$here/../os9exec/os9exec}
jobs=${JOBS:-6}
out=$here/notes/verify-loaded.tsv
work=$(mktemp -d)

[ -x "$exe" ]   || { echo "no os9exec at $exe -- set OS9EXEC" >&2; exit 2; }
[ -f "$image" ] || { echo "no image at $image -- build it first" >&2; exit 2; }

newer=$(/usr/bin/find "$disk/CMDS" -type f -newer "$image" 2>/dev/null | /usr/bin/head -5)
if [ -n "$newer" ]; then
  echo "$image is older than these, and the sweep would report them missing:" >&2
  printf '  %s\n' $newer >&2
  exit 2
fi

# CMDS/archives holds archive files, not programs.
find "$disk/CMDS" -type f -not -path '*/archives/*' \
  | sed "s|^$disk/||" \
  | awk -F/ '{n=$NF; sub("/"n"$","",$0); print n"\t"$0}' OFS='' \
  | sed 's|\t.*/CMDS|\tCMDS|' > "$work/list"
total=$(wc -l < "$work/list")
echo "sweeping $total programs with os9lib, Graph and Ptxm loaded ($jobs at a time)"

# One worker.  $1 = program  $2 = directory under /dd
cat > "$work/one.sh" <<'WORKER'
#!/bin/bash
prog=$1; dir=$2; work=$3; image=$4; exe=$5
n=$(printf '%s' "$dir/$prog" | /usr/bin/tr -c 'A-Za-z0-9' '_')
h1=$work/h1.$n; mkdir -p "$h1"
# CR-only, or bash reads the whole script as one enormous line.  The loads go
# to /nil: a library that is not there is not this program's verdict.
{ printf 'export TERM=vt100\r'
  printf 'export TERMCAP=/dd/SYS/termcap\r'
  printf 'export HOME=/dd\r'
  printf 'export USER=tester\r'
  printf 'export LOGNAME=tester\r'
  printf 'export TMACDIR=/dd/LIB\r'
  printf 'export HELPDIR=/dd/SYS/HELP\r'
  printf 'export SIMPATH=/dd/SBPROLOG/MODLIB\r'
  printf 'export PEP=/dd/SYS/PEP\r'
  printf '/dd/CMDS/load /dd/CMDS/os9lib >/nil 2>/nil\r'
  printf '/dd/CMDS/load /dd/CMDS/GAMES/graph >/nil 2>/nil\r'
  printf '/dd/CMDS/load /dd/CMDS/ptxm >/nil 2>/nil\r'
  printf '/dd/%s/%s\r' "$dir" "$prog"; } > "$h1/run.sh"
raw=$work/raw.$n
gtimeout 14 env OS9DISK="$image" OS9H0="$image" OS9H1="$h1" \
    "$exe" -r bash /h1/run.sh < /dev/null 2>&1 \
  | LC_ALL=C /usr/bin/tr -d '\000' | LC_ALL=C /usr/bin/tr '\r' '\n' \
  | /usr/bin/head -c 8000 \
  | LC_ALL=C /usr/bin/grep -vE '^# /[a-z0-9]+: (using|no) ' > "$raw"
diag=$( LC_ALL=C /usr/bin/grep '^#' "$raw" | /usr/bin/head -2 | LC_ALL=C /usr/bin/tr '\n' ' ')
mine=$( LC_ALL=C /usr/bin/grep -v '^#' "$raw" | LC_ALL=C /usr/bin/grep -v '^[[:space:]]*$' \
        | /usr/bin/head -3 | LC_ALL=C /usr/bin/tr '\n' ' ')
# BASH'S OWN COMPLAINT IS NOT THE PROGRAM'S OUTPUT.  The first run of this
# sweep scored thirty NOSTARTs as OK because bash answered `cannot execute
# binary file' for every trap module and driver under CMDS -- which are not
# programs at all -- and the classifier counted that as the program printing
# something.  A shell in the path means its errors have to be recognised.
if   printf '%s' "$mine" | LC_ALL=C /usr/bin/grep -qE 'cannot execute binary file|command not found|Permission denied|is a directory'; then v=NOTPROG
elif printf '%s' "$diag$mine" | LC_ALL=C /usr/bin/grep -q 'could not start'; then v=NOSTART
elif printf '%s' "$diag$mine" | LC_ALL=C /usr/bin/grep -qiE 'trap handler|User Trap'; then v=TRAP
elif printf '%s' "$diag$mine" | LC_ALL=C /usr/bin/grep -qE 'E_[A-Z]+\([0-9]+\)|err=#[0-9]'; then v=CRASH
elif [ -n "$mine" ]; then v=OK
else v=SILENT; fi
case $v in OK|SILENT) ev=$mine ;; *) ev=$diag$mine ;; esac
printf '%s\t%s\t%s\t%s\n' "$prog" "$dir" "$v" "$(printf '%s' "$ev" | LC_ALL=C /usr/bin/cut -c1-100)"
rm -rf "$h1" "$raw"
WORKER
chmod +x "$work/one.sh"

# xargs runs the workers; each prints one row, and a row is short enough that
# the writes do not interleave.
LC_ALL=C /usr/bin/awk -F'\t' '{print $1"\t"$2}' "$work/list" \
  | xargs -P "$jobs" -n 2 -I@ sh -c 'exec "$0" $1 "$2" "$3" "$4" "$5"' \
      "$work/one.sh" @ "$work" "$image" "$exe" 2>/dev/null > "$out.tmp"

sort "$out.tmp" > "$out"; rm -f "$out.tmp"
wrote=$(wc -l < "$out")
LC_ALL=C awk -F'\t' '{c[$3]++} END {for (k in c) printf "  %-8s %d\n", k, c[k]}' "$out"
echo "wrote $out ($wrote of $total rows)"

bare=$here/notes/verify-bare.tsv
if [ -f "$bare" ]; then
  echo ""
  echo "CHANGED against the sweep that loaded nothing:"
  LC_ALL=C join -t$'\t' -j 1 \
      <(LC_ALL=C awk -F'\t' '{print $2"/"$1"\t"$3}' "$bare" | sort) \
      <(LC_ALL=C awk -F'\t' '{print $2"/"$1"\t"$3}' "$out"  | sort) \
    | LC_ALL=C awk -F'\t' '$2 != $3 {printf "  %-34s %-8s -> %s\n", $1, $2, $3}'
fi
rm -rf "$work"
