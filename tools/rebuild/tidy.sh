#!/bin/bash
#
# Put disk/ back the way a build found it.
#
# Every recipe compiles IN PLACE, so a build leaves object files beside the
# sources, `ctmp.*' temporaries, and `R_<prog>' modules -- and `mkimage.sh'
# reads disk/ off the filesystem, so all of that would ship.
#
# It touches ONLY files a build could have made. Twice in one session a
# hand-typed `git checkout -- disk/SRC' reverted deliberate source fixes along
# with the object files; this exists so that command never has to be typed.
set -u
here=$(cd "$(dirname "$0")/../.." && pwd)
cd "$here" || exit 1

find disk/SRC -name 'ctmp.*' -type f -delete
mkdir -p built
find disk/SRC -name 'R_*' -type f | while IFS= read -r m; do
    mv "$m" "built/$(basename "$m" | sed 's/^R_//')"
done
# Ours, not theirs: restore any archive .r we overwrote, drop any we made.
# The pathspec is anchored on the SUFFIX, so a .c or .h edit is never touched.
git diff --name-only -- 'disk/SRC/**/*.r' 'disk/SRC/*.r' | while IFS= read -r f; do
    git checkout -- "$f"
done
git ls-files --others --exclude-standard -- disk/SRC |
    /usr/bin/grep '\.r$' | while IFS= read -r f; do rm -f "$f"; done
