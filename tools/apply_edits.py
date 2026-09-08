#!/usr/bin/env python3
r"""Apply a batch's edits to the three hand-maintained files, one writer.

    tools/apply_edits.py <batch>.edits [...]

A sweep batch runs on its own copy of the image and owns its own sheet,
but DOC/INDEX, tools/howto.psv and tools/categories.psv are shared by
every batch -- two batches editing one of them at once is how a line goes
missing.  So a batch writes what it wants changed to a `.edits' file, and
the session that dispatched it applies them here, serially, and commits.

One edit per line, pipe-separated, `#' comments and blank lines ignored:

    index|<name>|<the whole entry, as one line; wrapped here>
    howto|<name>|<one line, imperative; empty to remove the note>
    cat|<name>|<Category>|<Sub-category>

An `index' edit replaces the entry's text and keeps its star.  A `howto'
edit replaces the note or adds one; `howto|name|' removes it.  A `cat'
edit moves the program.  The name must be a program that exists, and the
text must be ASCII: DOC/INDEX ships on an 8-bit disk.
"""
import os
import re
import sys
import textwrap

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(REPO, "tools")
sys.path.insert(0, TOOLS)
import fix_index                                        # noqa: E402

INDEX = os.path.join(REPO, "disk", "DOC", "INDEX")
HOWTO = os.path.join(TOOLS, "howto.psv")
CATS = os.path.join(TOOLS, "categories.psv")

# An INDEX entry's text starts in column 18 and the disk is read on
# 80-column terminals; 60 characters of prose a line keeps it inside.
WIDTH = 60


def edit_index(name, text):
    lines = textwrap.wrap(" ".join(text.split()), WIDTH) or [""]
    return fix_index.fix(name, lines, INDEX)


def edit_psv(path, name, fields, remove=False):
    """Replace the line for `name' in a pipe-separated file, or add it."""
    rows = open(path).read().split("\n")
    key = name + "|"
    hit = [i for i, r in enumerate(rows) if r.startswith(key)]
    new = "|".join([name] + fields)
    if remove:
        for i in reversed(hit):
            del rows[i]
        return "removed" if hit else "was not there"
    if hit:
        rows[hit[0]] = new
        for i in reversed(hit[1:]):
            del rows[i]
        verdict = "replaced"
    else:
        # Append before the trailing blank line, so the file ends as it did.
        while rows and rows[-1] == "":
            rows.pop()
        rows.append(new)
        rows.append("")
        verdict = "added"
    open(path, "w").write("\n".join(rows))
    return verdict


def main(argv):
    if not argv:
        sys.exit(__doc__)
    n = 0
    for path in argv:
        for raw in open(path):
            line = raw.rstrip("\n")
            if not line.strip() or line.startswith("#"):
                continue
            try:
                line.encode("ascii")
            except UnicodeEncodeError:
                sys.exit("%s: not ASCII: %s" % (path, line[:60]))
            kind, _, rest = line.partition("|")
            name, _, text = rest.partition("|")
            name = name.strip()
            if kind == "index":
                print("  index  %-14s %s" % (name, edit_index(name, text)))
            elif kind == "howto":
                text = text.strip()
                print("  howto  %-14s %s" % (name, edit_psv(HOWTO, name, [text], remove=not text)))
            elif kind == "cat":
                cat, _, sub = text.partition("|")
                print("  cat    %-14s %s" % (name, edit_psv(CATS, name, [cat.strip(), sub.strip()])))
            else:
                sys.exit("%s: unknown edit kind `%s'" % (path, kind))
            n += 1
    print("%d edit(s) applied" % n)


if __name__ == "__main__":
    main(sys.argv[1:])
