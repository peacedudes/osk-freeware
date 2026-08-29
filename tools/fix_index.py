#!/usr/bin/env python3
"""Rewrite one DOC/INDEX entry, safely.

    from tools.fix_index import fix
    fix("greg", ["converts a JULIAN DAY NUMBER to a Gregorian date.",
                 "`greg 2461281' answers `2026 8 29'.  Corrected 2026-08-29"])

WHY THIS EXISTS.  DOC/INDEX is CR-terminated, its entries are a name in a
fixed column followed by continuation lines indented to match, and the head
of the file carries a GRID of the same names in four columns.  Editing it by
hand or by a one-off `replace' got all three of those wrong on 2026-08-29:

  * a `\\n' crept in and `check_disk.py' caught it -- the file must stay
    CR-only, so this reads and writes bytes and joins on "\\r";
  * the same name matched twice, because the grid at the head of the file
    lists it too.  The grid rows are four bare names with no prose, so an
    entry is the match whose remainder reads like a sentence;
  * two entries in DIFFERENT files were being edited by matching the first
    two spaces, and unstarred entries have two leading spaces where starred
    ones have one and a `*'.  Both forms are handled here.

A star before a name means the program wants Microware's `cio'; it is
preserved, because `check_disk.py' validates the star grid against it.

WHAT TO WRITE.  The point of an entry is what the program IS, measured by
running it -- not what its name suggests.  Sixteen entries were found on
2026-08-29 describing a different program from the one that runs.  End a
corrected entry with `Corrected <date>' or `Clarified <date>' so the next
pass can tell what has been checked; `tools/README.md' has the method.
"""
import re

INDEX = "disk/DOC/INDEX"


def fix(name, newlines, path=INDEX):
    """Replace the entry for `name' with `newlines'. Returns a status string."""
    text = open(path, "rb").read().decode("latin-1")
    lines = text.split("\r")
    pat = re.compile(r"^ (\*| )?%s\s{2,}" % re.escape(name))
    hits = [i for i, l in enumerate(lines) if pat.match(l)]

    def prose(line):
        rest = pat.sub("", line)
        return len(rest.split()) > 3 and any(c in rest for c in ".,:;-()'")

    real = [i for i in hits if prose(lines[i])]
    if len(real) != 1:
        return "SKIP %s (%d matches, %d of them prose)" % (name, len(hits),
                                                           len(real))
    i = real[0]
    j = i + 1
    while j < len(lines) and lines[j].startswith("               "):
        j += 1
    star = pat.match(lines[i]).group(1) or " "
    head = " %s%s%s" % (star, name, " " * max(1, 15 - len(star) - len(name)))
    lines[i:j] = [head + newlines[0]] + ["                 " + x
                                         for x in newlines[1:]]
    open(path, "wb").write("\r".join(lines).encode("latin-1"))
    return "ok   %s" % name


if __name__ == "__main__":
    import sys
    sys.exit(__doc__)
