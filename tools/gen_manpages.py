#!/usr/bin/env python3
"""Regenerate disk/DOC/MANPAGES -- the index `man' looks a page up in.

    tools/gen_manpages.py disk

WHY AN INDEX.  This disk carries about 360 roff manual pages, scattered
one or two to a package directory under DOC.  Searching for one at run time
means walking 363 directories, and the `find' here is an OS-9 find whose
options are `-n=' and `-l=' -- workable, but slow and easy to get wrong in a
script.  Every other cross-reference on this disk is a GENERATED index
(DOC/INDEX, DOC/DEPENDS, DOC/ORIGINS), so this is one too: `man' greps it.

WHAT COUNTS AS A PAGE.  A file under DOC whose name ends in a manual
section -- .1 to .8, .l, .n -- or in `.man', AND whose text contains a roff
macro line (`.TH', `.SH', `.PP', `.B', `.I') in its first 40 lines.  That
second test is what keeps `xc.man' in and a plain README called `.1' out;
without it the index promises pages that nroff renders as one long
paragraph.

THE ROW is the page's name padded into a column, then its path -- name
first, so `man ls' is a grep for a line starting `ls '.  `man' takes the
path with `set -- $line', so the separator is any run of spaces and the
file stays readable by eye.  Sorted, so the first match of a duplicated
name is stable rather than depending on directory order.

CR-terminated and ASCII, like every other document on the disk.
"""
import os
import re
import sys

SECTIONS = tuple(".%s" % s for s in "12345678ln") + (".man",)
MACRO = re.compile(rb"^\.(TH|SH|PP|B|I|IP|LP|TP|nf|fi)\b", re.M)


def pages(root):
    out = {}
    doc = os.path.join(root, "DOC")
    for base, dirs, files in os.walk(doc):
        for f in sorted(files):
            stem, _, ext = f.rpartition(".")
            if not stem or ("." + ext) not in SECTIONS:
                continue
            p = os.path.join(base, f)
            try:
                head = open(p, "rb").read(4000).replace(b"\r", b"\n")
            except OSError:
                continue
            if not MACRO.search(head):
                continue
            rel = "/dd/" + os.path.relpath(p, root).replace(os.sep, "/")
            out.setdefault(stem, []).append(rel)
    return out


def main(root, check=False):
    found = pages(root)
    rows = []
    for name in sorted(found):
        for path in sorted(found[name]):
            rows.append("%-22s %s" % (name, path))
    text = "\r".join(rows) + "\r"
    assert all(ord(c) < 128 for c in text), "MANPAGES must be plain ASCII"
    out = os.path.join(root, "DOC", "MANPAGES")
    if check:
        # A stale index is a silent failure: `man' simply says there is no
        # page for something that is right there on the disk.
        old = open(out, "rb").read().decode("latin-1") if os.path.exists(out) else ""
        if old != text:
            print("    DOC/MANPAGES is STALE -- run tools/gen_manpages.py disk")
            return 1
        return 0
    open(out, "wb").write(text.encode("latin-1"))
    print("  %s: %d pages, %d names" % (out, len(rows), len(found)))
    return 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    sys.exit(main(args[0] if args else "disk", "--check" in sys.argv))
