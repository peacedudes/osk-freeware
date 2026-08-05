#!/usr/bin/env python3
"""Check the invariants of the disk tree that are cheap to get wrong.

    tools/check_disk.py disk

Each check has been made to fail on purpose at least once. A check that
cannot fail is worse than no check: this collection has already produced a
verifier that reported 20/20 OK having run nothing, and a builder that
reported "copied 3287/3287" while every copy failed.

  1. NO TEXT FILE CONTAINS LF. OS-9 ends a line with CR alone. An LF-ended
     file is read by OS-9's cpp as one enormous line, surfacing as "source
     line too long" -- which has bitten this collection more than once, and
     is invisible until something tries to read the file. Binaries are
     skipped: 0x0A is an ordinary byte in a module.

  2. EVERY COMMAND IS NAMED IN DOC/INDEX. INDEX is what tells a reader what
     a program is; a command absent from it is undiscoverable.

  3. DOC/DEPENDS IS UP TO DATE. It is generated, and drifts the moment
     anything is added -- delegated to gen_depends.py, which owns the rule.
"""
import os, re, subprocess, sys

MODULE_MAGIC = b"\x4a\xfc"
TEXT_RATIO   = 0.97
CMD_DIRS     = ["CMDS", "CMDS/GAMES"]


def is_text(data):
    """True for a file worth holding to the CR-only rule.

    An OS-9 module is exempt by its magic; anything else counts as text when
    almost every byte is printable, which keeps fonts and other binary data
    out without needing a list of them.
    """
    if not data or data[:2] == MODULE_MAGIC:
        return False
    printable = sum(1 for b in data if 32 <= b < 127 or b in (9, 10, 13, 12))
    return printable / len(data) > TEXT_RATIO


def check_line_endings(root):
    bad = []
    for dirpath, _, names in os.walk(root):
        for name in names:
            path = os.path.join(dirpath, name)
            try:
                data = open(path, "rb").read()
            except OSError:
                continue
            if is_text(data) and b"\n" in data:
                bad.append((os.path.relpath(path, root), data.count(b"\n")))
    for path, n in sorted(bad):
        print("    %s: %d LF" % (path, n))
    return not bad, "%d text file(s) contain LF" % len(bad)


def check_index_names(root):
    index = os.path.join(root, "DOC", "INDEX")
    words = set(re.findall(r"[A-Za-z0-9_.]+",
                open(index, "rb").read().decode("latin-1")))
    missing = [os.path.join(d, n)
               for d in CMD_DIRS
               for n in sorted(os.listdir(os.path.join(root, d)))
               if os.path.isfile(os.path.join(root, d, n)) and n not in words]
    for m in missing:
        print("    not in DOC/INDEX: %s" % m)
    return not missing, "%d command(s) missing from DOC/INDEX" % len(missing)


def check_depends(root):
    gen = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen_depends.py")
    done = subprocess.run([sys.executable, gen, root, "--check"],
                          capture_output=True, text=True)
    if done.returncode:
        print("    " + done.stdout.strip())
    return done.returncode == 0, "DOC/DEPENDS is stale"


CHECKS = [
    ("line endings are CR-only", check_line_endings),
    ("every command is in DOC/INDEX", check_index_names),
    ("DOC/DEPENDS is up to date", check_depends),
]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: check_disk.py <disk-tree>")
    root = sys.argv[1]
    if not os.path.isdir(os.path.join(root, "CMDS")):
        raise SystemExit("not a disk tree (no CMDS): %s" % root)

    failed = 0
    for label, check in CHECKS:
        ok, complaint = check(root)
        print("  %-32s %s" % (label, "ok" if ok else "FAILED -- " + complaint))
        failed += not ok

    raise SystemExit(1 if failed else 0)
