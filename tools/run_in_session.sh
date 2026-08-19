#!/bin/bash
# Run ONE command line inside a login session and show exactly what came back.
#
#   tools/run_in_session.sh '/dd/CMDS/suse /dd/CMDS/cat'
#   tools/run_in_session.sh -q '/dd/CMDS/sysid'      # -q: drop the login noise
#
# The sweep scripts answer "did this program work" for 949 programs at a time.
# This answers "what exactly does THIS one do", which is the question every
# individual diagnosis starts from, and doing it by hand each time invites the
# mistakes the sweeps already made:
#
#   * os9exec's `#` lines carry E_BMID, E_NEMOD and `unintialized User Trap`.
#     They are the verdict, not noise, so they are SHOWN by default. -q drops
#     only login's banner and bash's echo of the command, never a `#` line.
#   * `grep -a` throughout: OS-9 programs emit control bytes freely, and plain
#     grep answers `Binary file matches` and throws the evidence away.
#   * Run through SYS/login, because bare there is no TERM and no TERMCAP and
#     69 programs read TERMCAP. `aterm` and `snake` take BUS ERRORS without it
#     and are perfectly fine with it.
#   * NUL stripped and CR translated to LF, or the host terminal eats lines.
#
# Env:  OS9EXEC  the emulator binary       OS9IMAGE  the built .dd
#       TIMEOUT  seconds, default 20
set -u
here=$(cd "$(dirname "$0")/.." && pwd)
exe=${OS9EXEC:-$here/../os9exec/os9exec}
image=${OS9IMAGE:-$here/osk-freeware.dd}
secs=${TIMEOUT:-20}

quiet=0
[ "${1:-}" = "-q" ] && { quiet=1; shift; }
[ $# -ge 1 ] || { echo "usage: run_in_session.sh [-q] '<command line>' [<stdin text>]"; exit 1; }
cmd=$1
stdin_text=${2:-}

[ -x "$exe" ]   || { echo "no os9exec at $exe -- set OS9EXEC" >&2; exit 2; }
[ -f "$image" ] || { echo "no image at $image -- set OS9IMAGE or build one" >&2; exit 2; }

raw=$(mktemp)
trap 'rm -f "$raw"' EXIT

# The program's own stdin comes first, then `exit` to end the bash session.
{ printf '%s\n' "$cmd"
  [ -n "$stdin_text" ] && printf '%s\n' "$stdin_text"
  printf 'exit\n'
} | gtimeout "$secs" env OS9DISK="$image" OS9H0="$image" \
      "$exe" -r bash /dd/SYS/login 2>&1 \
  | /usr/bin/tr -d '\000' | LC_ALL=C /usr/bin/tr '\r' '\n' > "$raw"

if [ "$quiet" = 1 ]; then
  # Drop the line that IS the echoed command, never a line that merely NAMES
  # it. An earlier `grep -vF "$cmd"` here swallowed
  #   /dd/CMDS/no_such_program:  (E$PNNF) That path name doesn't lead ...
  # and reported the run as silent -- a program that could not even be found
  # scored the same as one that ran and said nothing.
  LC_ALL=C /usr/bin/grep -av -E '^os9\$|^OS-9 freeware|^cat and less|^exit$|^$' "$raw" \
    | LC_ALL=C /usr/bin/awk -v c="$cmd" '$0 != c'
else
  cat "$raw"
fi
