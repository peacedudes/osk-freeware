#!/usr/bin/env bash
# run_workflow_locally.sh -- do everything .github/workflows/build-image.yml
# does, here, without pushing anything.
#
#     tools/ci/run_workflow_locally.sh /path/to/a/scratch/dir
#
# WHY.  The workflow triggers on `main', on a PR to `main', and on a tag.
# This branch is hundreds of commits ahead of `main' and has never been
# pushed, so until 2026-08-30 not one step of it had ever run -- and one of
# them could never have passed.  `basename /a/b/c' answers "c" followed by a
# CR, because OS-9 ends a line with CR, and the step tested it with
# `grep -qx c', which wants the whole line.  The image was perfectly good.
# The workflow now strips CR as well as NUL; this script is what found it.
#
# It exports the tree with `git archive HEAD', so it tests what a CLEAN
# CHECKOUT would get -- not your working directory.  That matters: the
# screen captures are gitignored, and the drift check has to fall back to
# docs/screens.stanzas exactly as it would on a runner.
#
# It builds os9exec from the PINNED commit into the scratch directory and
# leaves your own os9exec tree alone.
#
# The two readback checks were confirmed on 2026-08-30 to FAIL against a
# blank image, which is what makes them worth running.
set -u
SP="$1"
REF=261b4b69ce2eced889ec18b50c9b611f9ca19881
W="$SP/cirun"
rm -rf "$W"; mkdir -p "$W"
fail=0
step() { printf '\n=== %s\n' "$1"; }

step "Check out the collection (git archive, as a clean checkout)"
git -C /Users/rdoggett/Developer/os9/osk-freeware archive HEAD | tar -x -C "$W"
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
git -C /Users/rdoggett/Developer/os9/os9exec archive "$REF" | tar -x -C "$W/os9exec"
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
