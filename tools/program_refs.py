#!/usr/bin/env python3
"""Every place a program's NAME is recorded -- run before removing one.

    tools/program_refs.py <name> [<name> ...]

A program here is not one file.  It is a binary under `disk/CMDS', usually a
source tree under `disk/SRC', a row in four documents ON the disk, a row in
nine hand-maintained tables under `tools/', a build recipe, cases, drive
sheets, card stanzas, a captured help file and published output under
`docs/'.  The 2026-08-22 removals missed none of that because the tree was
smaller; it is not smaller now.

This prints what it FINDS, never guesses, and touches nothing.  Read its
report, delete by hand, then run `tools/check_disk.py disk' -- the gate is
what proves the removal complete.

The disk's own documents are CR-terminated, so they are read and split on
CR as well as LF: a plain line-reader sees one enormous line and reports a
hit with no line number worth having.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (path, how the name appears) for the files that carry one row per program.
TABLES = [
    "disk/DOC/INDEX", "disk/DOC/ORIGINS", "disk/DOC/CATEGORIES",
    "disk/DOC/DEPENDS", "disk/SOURCES.txt", "disk/DOC/README-CIO",
    "tools/categories.psv", "tools/help.psv", "tools/howto.psv",
    "tools/terms.psv", "tools/requires.psv", "tools/language.psv",
    "tools/rebuild/recipes.psv", "tools/module-name-duplicates.txt",
    "tools/panel-exceptions.psv", "tools/panel-backlog.txt",
    "tools/help-backlog.txt", "tools/terms-backlog.txt",
    "tools/try-backlog.txt", "tools/screened-src.txt",
]

# Directories searched file by file, because a name can appear anywhere in them.
# `disk/DOC' is NOT among them on purpose: it is prose, and a whole-word search
# for a short name (`e', `ci', `vi') matches English rather than the program --
# 308 hits for one such scan, which hides the rows that matter instead of
# showing them.  The DOC/<name> directory a program owns is caught by the
# "files named for it" pass above.
TREES = ["tools/drives", "tools/datatests", "tools/screenshots",
         "tools/playtests", "docs/help"]

# Below this length a name matches ordinary words too often for the sheet scan
# to be read at all; it is reported, not silently skipped.
SHORT = 3


def lines(path):
    """The file's lines, however it terminates them."""
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("latin-1")
    return re.split(r"\r\n|\r|\n", text)


def word_hits(path, name):
    """Line numbers where `name' appears as a whole word."""
    pat = re.compile(r"(?<![A-Za-z0-9_.])" + re.escape(name) + r"(?![A-Za-z0-9_])")
    out = []
    for n, line in enumerate(lines(path), 1):
        if pat.search(line):
            out.append((n, line.strip()[:110]))
    return out


def report(name):
    print("=" * 72)
    print("%s" % name)
    print("=" * 72)

    print("\n-- files named for it")
    for base, _, files in os.walk(os.path.join(ROOT, "disk")):
        rel = os.path.relpath(base, ROOT)
        if os.path.basename(base) == name:
            print("   DIR  %s" % rel)
        for f in files:
            stem = f.rsplit(".", 1)[0]
            if f == name or stem == name or f.startswith(name + "."):
                print("   %s" % os.path.join(rel, f))
    for d in ("tools/drives", "tools/datatests", "tools/playtests",
              "tools/screenshots", "docs/help", "docs/screens"):
        p = os.path.join(ROOT, d)
        if not os.path.isdir(p):
            continue
        for f in sorted(os.listdir(p)):
            if f.split(".")[0] == name:
                print("   %s" % os.path.join(d, f))

    print("\n-- rows in the per-program tables")
    for t in TABLES:
        p = os.path.join(ROOT, t)
        if not os.path.exists(p):
            continue
        for n, line in word_hits(p, name):
            print("   %-34s %5d  %s" % (t, n, line))

    print("\n-- mentioned in sheets, cases and captured help")
    if len(name) < SHORT:
        print("   (name is %d characters -- too short to search prose for; read"
              " the sheets and cases by hand)" % len(name))
        print()
        return
    for tree in TREES:
        base = os.path.join(ROOT, tree)
        if not os.path.isdir(base):
            continue
        for d, _, files in os.walk(base):
            for f in sorted(files):
                p = os.path.join(d, f)
                rel = os.path.relpath(p, ROOT)
                if rel in TABLES:
                    continue
                try:
                    hits = word_hits(p, name)
                except OSError:
                    continue
                if hits:
                    print("   %-46s %d line(s), first %d" % (rel, len(hits), hits[0][0]))
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for n in sys.argv[1:]:
        report(n)
