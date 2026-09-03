#!/usr/bin/env python3
"""Run a scratch sheet through the REAL capture harness and print the screens.

    tools/probe_sheet.py my.sheet [--image copy.dd]

The step before committing a stanza: it drives `tools/screenshots.py's own
Session and capture, so what it prints is exactly what a card would show,
and it SAVES NOTHING -- no capture lands in notes/playtests, no hash is
written.  Write a stanza, probe it, adjust, probe again, and only then put
it in a sheet under tools/screenshots/ and shoot it for real.

Same sheet format as screenshots.py; `size' goes right after `shot', or
it attaches to the stanza before.  A stanza that leaves the session
unusable is followed by a fresh session, as in the real harness.
"""
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import imagelock                                        # noqa: E402
import screenshots                                      # noqa: E402


def main(argv):
    if not argv:
        sys.exit(__doc__)
    sheet = argv[0]
    image = os.path.join(REPO, "osk-freeware.dd")
    if "--image" in argv:
        image = argv[argv.index("--image") + 1]
    image = os.path.abspath(image)
    shots = screenshots.parse(sheet)
    with imagelock.held(image, "probe"):
        for size in sorted({s["size"] for s in shots}):
            group = [s for s in shots if s["size"] == size]
            sess = screenshots.Session(image, size[0], size[1])
            try:
                for shot in group:
                    scr, died = screenshots.capture(sess, shot)
                    print("======== %s  size %dx%d %s"
                          % (shot["name"], size[0], size[1],
                             "-- TOOK THE EMULATOR DOWN" if died else ""))
                    print(scr.text().rstrip())
                    if died or not sess.ready():
                        sess.close()
                        sess = screenshots.Session(image, size[0], size[1])
            finally:
                sess.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
