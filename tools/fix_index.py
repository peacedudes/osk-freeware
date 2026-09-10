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
    # Entries sit at one or two leading spaces, a starred one at " *".
    # A few live in indented SUB-LISTS four spaces in -- the shell
    # scripts under CMDS, for instance -- and those this does not touch;
    # edit them by hand and keep the indent.
    # Entries sit at one to three leading spaces, starred ones with a `*'
    # in the last of them (` *name', `  *name') or before the name.
    pat = re.compile(r"^ {1,3}(\*)?%s\s{2,}" % re.escape(name))
    # NEVER a row of the star grid.  Its rows are bare names, but some
    # names ARE small words -- `in', `is', `mail' are programs -- so the
    # prose test below took a grid row for a sentence and wrote the whole
    # of `messages's new entry into the grid (2026-09-09).  The grid runs
    # from the `All N, verified' line to the next rule, so it is skipped
    # by position, not by look.
    grid = set()
    inside = False
    for i, l in enumerate(lines):
        if l.startswith("All ") and "verified" in l:
            inside = True
        elif inside and (l.startswith("---") or l.startswith("/dd")):
            inside = False
        elif inside:
            grid.add(i)
    hits = [i for i, l in enumerate(lines) if pat.match(l) and i not in grid]

    # A grid row is up to four bare names; an entry reads like a sentence.
    # Punctuation is one sign; a small word -- `a', `as', `the' -- is the
    # other, and `print text as a gothic/blackletter banner' has only the
    # second (it was SKIPped on 2026-09-08 for want of a comma).
    SMALL = {"a", "an", "the", "to", "of", "in", "as", "for", "and", "or",
             "is", "it", "its", "on", "by", "at", "not", "no", "with",
             "from", "that", "into", "than", "then", "one", "two", "what"}

    def prose(line):
        rest = pat.sub("", line)
        words = rest.split()
        return (len(words) > 4 or any(c in rest for c in ".,:;-()'")
                or any(w.lower() in SMALL for w in words))

    # One match is unambiguous whatever it looks like: a short entry like
    # `gen  generate a program frame' has no punctuation and would fail the
    # prose test, and there is nothing else it could be.
    real = hits if len(hits) == 1 else [i for i in hits if prose(lines[i])]
    if len(real) != 1:
        return "SKIP %s (%d matches, %d of them prose)" % (name, len(hits),
                                                           len(real))
    # Say so when a name appears more than once.  `gnuchess' has a prose entry
    # in the main list and a terse one in the games list; editing the first and
    # not knowing about the second is how the two came to disagree.
    other = "" if len(hits) == 1 else "  (%d other entries for this name left alone)" % (len(hits) - 1)
    i = real[0]
    j = i + 1
    while j < len(lines) and lines[j].startswith("               "):
        j += 1
    star = pat.match(lines[i]).group(1) or " "
    # 17, to match the continuation indent below and the column the file
    # already keeps for 617 of its 748 entries.  This read 15 until
    # 2026-08-29 and put every head it wrote one column left of its own
    # continuations.
    head = " %s%s%s" % (star, name, " " * max(1, 16 - len(star) - len(name)))
    lines[i:j] = [head + newlines[0]] + ["                 " + x
                                         for x in newlines[1:]]
    open(path, "wb").write("\r".join(lines).encode("latin-1"))
    return "ok   %s%s" % (name, other)


if __name__ == "__main__":
    import sys
    sys.exit(__doc__)
