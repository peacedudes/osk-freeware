#!/usr/bin/env python3
r"""Find files on the disk that are byte-identical to Microware's SDK.

    tools/sdk_overlap.py <sdk-tree> [<disk-tree>]

WHY THIS EXISTS.  The hard rule is that none of Microware's PRODUCTS ships
here -- utilities, headers, libraries, the compiler -- and the only
exceptions are the runtime modules they gave permission for.  Every check
in `check_disk.py' looks at what a file SAYS: it screens `disk/SRC' for
proprietary notices, it screens prose for adversarial phrasing.  None of
them looks at what a file IS, and a Microware binary carries no notice at
all.

The sweep that earned this tool was about `fpu': the disk was shipping a
copy that was NOT the one its distribution grant travels with, and nothing
short of an md5 could have told anybody.  See SOURCES.txt.

NOT A GATE, and it cannot be one: the SDK tree is not in this repository
and is not on the machine that builds the image.  It is a report to run
when the collection's contents change materially, and before a release.

ACCEPTED, with reasons.  Three files match on purpose:

    CMDS/cio    CMDS/csl    CMDS/math

Those are three of the five runtime modules Microware gave permission for
by name on 2026-08-16 -- SOURCES.txt records the exchange -- and that
permission is for the MODULES, so the copy does not matter.  `math881' and
`csl020' are the other two and happen not to be in the SDK tree at all.

A NEW NAME HERE IS NOT AUTOMATICALLY WRONG, but it does need somebody to
say which of three things it is: a module covered by that permission, a
file that carries its own grant (check the grant travels with THAT COPY --
that is the fpu lesson), or something that has to come off the disk.
"""
import hashlib
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Byte-identical to the SDK on purpose.  Each is one of the five runtime
# modules Microware permitted by name; the permission names the module,
# not a copy, so any build of it is within it.
ACCEPTED = {
    "disk/CMDS/cio": "runtime module, permitted by name 2026-08-16",
    "disk/CMDS/csl": "runtime module, permitted by name 2026-08-16",
    "disk/CMDS/math": "runtime module, permitted by name 2026-08-16",
}

# Below this, a match is coincidence rather than evidence -- an empty file,
# a one-line script, a short header both trees happen to carry.
MIN_BYTES = 64


def digests(root):
    """md5 -> [paths], for every file in a tree worth comparing."""
    out = {}
    for base, _, files in os.walk(root):
        for f in files:
            p = os.path.join(base, f)
            try:
                b = open(p, "rb").read()
            except OSError:
                continue
            if len(b) < MIN_BYTES:
                continue
            out.setdefault(hashlib.md5(b).hexdigest(), []).append(p)
    return out


def main(argv):
    if not argv:
        sys.stderr.write(__doc__.split("\n\n")[1] + "\n")
        sys.stderr.write("sdk_overlap: give me the SDK tree to compare against\n")
        return 2
    sdk = os.path.abspath(os.path.expanduser(argv[0]))
    disk = os.path.abspath(argv[1]) if len(argv) > 1 \
        else os.path.join(REPO, "disk")
    for d in (sdk, disk):
        if not os.path.isdir(d):
            sys.stderr.write("sdk_overlap: %s is not a directory\n" % d)
            return 2

    index = digests(sdk)
    print("%d file(s) indexed under %s" % (sum(len(v) for v in index.values()),
                                           os.path.basename(sdk)))
    expected, surprises = [], []
    for base, _, files in os.walk(disk):
        for f in sorted(files):
            p = os.path.join(base, f)
            try:
                b = open(p, "rb").read()
            except OSError:
                continue
            if len(b) < MIN_BYTES:
                continue
            match = index.get(hashlib.md5(b).hexdigest())
            if not match:
                continue
            rel = os.path.relpath(p, REPO)
            if rel.startswith(".."):
                rel = p
            row = (rel, os.path.relpath(match[0], sdk))
            (expected if rel in ACCEPTED else surprises).append(row)

    for rel, where in sorted(expected):
        print("  ok        %-28s %s" % (rel, ACCEPTED[rel]))
    for rel, where in sorted(surprises):
        print("  LOOK AT   %-28s same bytes as %s" % (rel, where))
    # Only meaningful against this repo's own tree: pointed at a copy,
    # every accepted line would read as gone and say nothing.
    if disk == os.path.join(REPO, "disk"):
        for rel in sorted(set(ACCEPTED) - {r for r, _ in expected}):
            print("  gone      %-28s accepted here and no longer matches -- "
                  "take the line out" % rel)

    print("\n%d expected, %d to look at" % (len(expected), len(surprises)))
    return 1 if surprises else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
