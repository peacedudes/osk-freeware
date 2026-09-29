#!/usr/bin/env bash
# run_workflow_locally.sh -- do everything .github/workflows/build-image.yml
# does, here, without pushing anything.
#
#     tools/ci/run_workflow_locally.sh /path/to/a/scratch/dir
#
# WHY.  A workflow step that can only fail on the runner is found late.  The
# first run of this script found one that could never have passed:
# `basename /a/b/c' answers "c" followed by a CR, because OS-9 ends a line
# with CR, and the step tested it with `grep -qx c'.  The image was fine.
#
# It exports the tree with `git archive HEAD', so it tests what a CLEAN
# CHECKOUT would get -- not your working directory.  That matters: the
# screen captures are gitignored, and the drift check has to fall back to
# docs/screens.stanzas exactly as it would on a runner.
#
# It builds os9exec (OS9EXEC_SRC, a checkout; OS9EXEC_REF, the ref the
# workflow uses unless you say otherwise) into the scratch directory and
# leaves your own os9exec tree alone.
#
# The two readback checks were confirmed on 2026-08-30 to FAIL against a
# blank image, which is what makes them worth running.
set -u
SP="$1"
REPO=$(cd "$(dirname "$0")/../.." && pwd)
OS9EXEC_SRC=${OS9EXEC_SRC:-$HOME/Developer/os9/os9exec}
REF=${OS9EXEC_REF:-release-v4.1.0}
W="$SP/cirun"
rm -rf "$W"; mkdir -p "$W"
fail=0
step() { printf '\n=== %s\n' "$1"; }

# Leave the repository first.  If PATH holds `.', a `tar' in the current
# directory -- the repo root has held the OS-9 tar module -- answers for the
# host tar, exports nothing, and every later step reports on an empty tree.
cd "$SP"
step "Check out the collection (git archive, as a clean checkout)"
git -C "$REPO" archive HEAD | tar -x -C "$W"
echo "  exported $(find "$W" -type f | wc -l | tr -d ' ') files"

cd "$W"
step "Check the disk tree"
tools/check_disk.py disk; [ $? -eq 0 ] || fail=1

step "Check every program is catalogued"
tools/gen_catalog.py disk --check; [ $? -eq 0 ] || fail=1

step "Check no screen has drifted from its stanza"
tools/gen_screens.py --check; [ $? -eq 0 ] || fail=1

step "Check out os9exec at the pinned ref, and build it"
mkdir -p "$W/os9exec"
git -C "$OS9EXEC_SRC" archive "$REF" | tar -x -C "$W/os9exec"
make -C "$W/os9exec" -j8 >"$W/build.log" 2>&1 || { echo "  BUILD FAILED"; fail=1; }
echo "  built $(ls -l "$W/os9exec/os9exec" | awk '{print $5}') bytes"

step "Check os9exec can create a named blank image"
if ! ./os9exec/os9exec -r mount '-?' 2>&1 | tr -d '\000' | grep -q -- '-v=<name>'; then
  echo "  ::error:: no 'mount -k -v=<name>'"; fail=1
else echo "  mount -k -v=<name> present"; fi

step "Build the image"
OS9EXEC_DIR="$W/os9exec" tools/mkimage.sh disk osk-freeware.dd 2>&1 | tail -4
[ -s osk-freeware.dd ] || { echo "  NO IMAGE"; fail=1; }

step "Read the image back"
img="$W/osk-freeware.dd"
runit() { OS9DISK="$img" ./os9exec/os9exec -r "$@" 2>&1 | tr -d '\000\r' | grep -v '^#'; }
runit wc /dd/startup | grep -q '/dd/startup' \
  && echo "  reads /dd/startup" || { echo "  ::error:: cannot read /dd/startup"; fail=1; }
runit basename /a/b/c | grep -qx 'c' \
  && echo "  loads and runs a module" || { echo "  ::error:: cannot run a module"; fail=1; }

step "Compress"
gzip -9 -c osk-freeware.dd > osk-freeware.dd.gz
ls -lh osk-freeware.dd osk-freeware.dd.gz | awk '{print "  "$5, $9}'

step "Rebuild the catalogue"
tools/gen_catalog.py disk docs/index.html >/dev/null && echo "  catalogue rebuilt" || fail=1

printf '\n===== WORKFLOW %s =====\n' "$([ $fail -eq 0 ] && echo PASSED || echo FAILED)"
exit $fail
