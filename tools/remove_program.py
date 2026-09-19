#!/usr/bin/env python3
"""Take a program OFF the disk, everywhere the machine can see it.

    tools/remove_program.py [--dry-run] <name> [<name> ...]

WHY.  A program here is a binary, usually a source tree, four documents ON
the disk and a dozen hand-maintained tables beside it.  The 2026-08-22
removals were done by hand and the tree was smaller; twenty-five came off on
2026-09-18 and by hand that is a hundred and fifty edits, every one of them a
chance to leave a row pointing at a file that is gone.

WHAT IT DOES, and only this:

  * deletes `disk/CMDS/<name>' wherever under CMDS it lives, the program's
    own `disk/DOC/<name>' directory, its captured help and published screen,
    its play-test and its drive sheet;
  * deletes its row from the per-program tables (categories, help, howto,
    terms, requires, language, the recipes and the three backlogs);
  * deletes its DOC/INDEX entry with its continuation lines, and its name
    from the star grid at the head of that file, rewriting the grid and its
    `All N' header;
  * deletes its DOC/ORIGINS row.

WHAT IT REFUSES TO DO, and reports instead: SOURCES.txt paragraphs, card
stanzas, datatest cases, the source tree (one tree often holds several
programs, so deleting it on one name's account would take the others with
it), and any PROSE that names the program -- another entry's cross-reference,
a README, a family chooser.  Those are judgement, and the report is the list
to work through.  `tools/program_refs.py' is the wider search.

AFTERWARDS, always: `tools/gen_depends.py disk', `tools/gen_catalog.py',
`tools/gen_screens.py', then `tools/check_disk.py disk' -- the gate is what
proves the removal complete, and it has a check for each of the tables above.

The disk's own files are CR-terminated and are read and written as bytes on
that basis; nothing here converts a line ending.
"""
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY = False

# name|... tables, one row per program, keyed on the first field.
PIPE_TABLES = ["tools/categories.psv", "tools/help.psv", "tools/howto.psv",
               "tools/terms.psv", "tools/requires.psv", "tools/language.psv",
               "tools/rebuild/recipes.psv", "tools/panel-exceptions.psv"]
# one bare name per line
LIST_TABLES = ["tools/help-backlog.txt", "tools/panel-backlog.txt",
               "tools/terms-backlog.txt", "tools/try-backlog.txt"]


def read(path):
    with open(path, "rb") as f:
        return f.read().decode("latin-1")


def write(path, text):
    if DRY:
        return
    with open(path, "wb") as f:
        f.write(text.encode("latin-1"))


def drop_file(rel, out):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        return
    out.append("   deleted  %s" % rel)
    if DRY:
        return
    shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)


def binary_path(name):
    """Where the program's own binary lives under disk/CMDS, if it does."""
    for base, dirs, files in os.walk(os.path.join(ROOT, "disk", "CMDS")):
        if name in files:
            return os.path.relpath(os.path.join(base, name), ROOT)
    return None


def strip_rows(name, out):
    for t in PIPE_TABLES:
        p = os.path.join(ROOT, t)
        if not os.path.exists(p):
            continue
        text = read(p)
        eol = "\r" if "\r" in text and "\n" not in text else "\n"
        lines = text.split(eol)
        keep = [l for l in lines if not l.startswith(name + "|")]
        if len(keep) != len(lines):
            out.append("   row gone %-32s (%d)" % (t, len(lines) - len(keep)))
            write(p, eol.join(keep))
    for t in LIST_TABLES:
        p = os.path.join(ROOT, t)
        if not os.path.exists(p):
            continue
        text = read(p)
        lines = text.split("\n")
        keep = [l for l in lines if l.strip() != name and l.split()[:1] != [name]]
        if len(keep) != len(lines):
            out.append("   row gone %-32s (%d)" % (t, len(lines) - len(keep)))
            write(p, "\n".join(keep))


def strip_index(name, out):
    """The entry, its continuations, and the name in the star grid."""
    p = os.path.join(ROOT, "disk/DOC/INDEX")
    lines = read(p).split("\r")

    # The grid runs from the `All N' header to the next rule or path line.
    head = next((i for i, l in enumerate(lines)
                 if l.startswith("All ") and "verified" in l), None)
    end = head
    if head is not None:
        end = head + 1
        while end < len(lines) and not (lines[end].startswith("---")
                                        or lines[end].startswith("/dd")):
            end += 1
    grid = range(head + 1, end) if head is not None else range(0)

    pat = re.compile(r"^ {1,3}(\*)?%s\s{2,}" % re.escape(name))
    hits = [i for i, l in enumerate(lines) if pat.match(l) and i not in grid]
    for i in reversed(hits):
        j = i + 1
        while j < len(lines) and lines[j].startswith("               "):
            j += 1
        out.append("   entry gone  DOC/INDEX line %d (%d line(s))" % (i + 1, j - i))
        del lines[i:j]

    if head is None:
        write(p, "\r".join(lines))
        return
    # Rebuild the grid without the name, four columns as the file keeps them.
    head = next(i for i, l in enumerate(lines)
                if l.startswith("All ") and "verified" in l)
    end = head + 1
    while end < len(lines) and not (lines[end].startswith("---")
                                    or lines[end].startswith("/dd")):
        end += 1
    names, blanks = [], []
    for l in lines[head + 1:end]:
        (names.extend(l.split()) if l.strip() else blanks.append(l))
    if name in names:
        names.remove(name)
        out.append("   star grid   %s dropped, All %d" % (name, len(names)))
        rows = []
        for i in range(0, len(names), 4):
            rows.append("  " + "".join(n.ljust(16) for n in names[i:i + 4]).rstrip())
        header = re.sub(r"^All \d+", "All %d" % len(names), lines[head])
        lines[head:end] = [header] + rows + blanks
    write(p, "\r".join(lines))


def strip_usage_status(name, out):
    """DOC/USAGE keeps a BLOCK per program -- a header line naming the
    directory, indented lines under it, a blank line -- and DOC/STATUS one
    line.  Neither is generated by anything, so nothing else would drop them,
    and `name lists point at real programs' fails on what is left."""
    p = os.path.join(ROOT, "disk/DOC/USAGE")
    lines = read(p).split("\r")
    head = re.compile(r"^ {2}%s\s{2,}\(" % re.escape(name))
    i = next((n for n, l in enumerate(lines) if head.match(l)), None)
    if i is not None:
        j = i + 1
        while j < len(lines) and (lines[j].startswith("    ") or not lines[j].strip()):
            if not lines[j].strip() and j + 1 < len(lines) and not lines[j + 1].startswith("    "):
                j += 1
                break
            j += 1
        out.append("   block gone  DOC/USAGE line %d (%d line(s))" % (i + 1, j - i))
        del lines[i:j]
        write(p, "\r".join(lines))

    p = os.path.join(ROOT, "disk/DOC/STATUS")
    lines = read(p).split("\r")
    row = re.compile(r"^ {2}%s\s{2,}" % re.escape(name))
    keep = [l for l in lines if not row.match(l)]
    if len(keep) != len(lines):
        out.append("   row gone    DOC/STATUS (%d)" % (len(lines) - len(keep)))
        write(p, "\r".join(keep))


def strip_origins(name, out):
    p = os.path.join(ROOT, "disk/DOC/ORIGINS")
    lines = read(p).split("\r")
    keep = [l for l in lines if l.split()[:1] != [name]]
    if len(keep) != len(lines):
        out.append("   row gone    DOC/ORIGINS (%d)" % (len(lines) - len(keep)))
        write(p, "\r".join(keep))


def strip_card(name, out):
    """The gallery stanza headed `shot <name>'.

    A stanza runs from its `shot' line to the next one, and the banner comment
    above it belongs to it only when it names it.  A stanza that CREDITS other
    programs (`for' lines) is never deleted here -- cards here routinely credit
    three to five, and taking one out on one name's account would take the
    others with it; that case is reported instead.  Other stanzas that merely
    MENTION the name in a `run' line are reported too, because what to do about
    them is judgement: a setup line may need rewriting rather than deleting.
    """
    base = os.path.join(ROOT, "tools/screenshots")
    for f in sorted(os.listdir(base)):
        if not f.endswith(".sheet"):
            continue
        p = os.path.join(base, f)
        lines = read(p).split("\n")
        starts = [i for i, l in enumerate(lines) if l.split()[:2] == ["shot", name]]
        for i in reversed(starts):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("shot"):
                j += 1
            credits = [l for l in lines[i:j] if l.startswith("for")]
            if credits:
                out.append("   CARD KEPT   %s stanza credits others: %s"
                           % (f, " ".join(c.split(None, 1)[1] for c in credits)))
                continue
            k = i
            while k > 0 and (not lines[k - 1].strip()
                             or (lines[k - 1].startswith("#") and name in lines[k - 1])):
                k -= 1
            while j > i and not lines[j - 1].strip():
                j -= 1
            out.append("   card gone   %s (%d line(s))" % (f, j - k))
            del lines[k:j]
            write(p, "\n".join(lines))


def sync_cio_count(out):
    """DOC/README-CIO states how many modules link cio, and `check_disk'
    compares that figure with a scan of the disk.  Taking a starred program
    off changes it, so the document is brought back into line here rather
    than being left for the gate to fail on -- which it did, twice, on the
    2026-09-18 removals."""
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import cio_macro_scan
    total, rows = cio_macro_scan.survey([os.path.join(ROOT, "disk")])
    p = os.path.join(ROOT, "disk/DOC/README-CIO")
    text = read(p)
    m = re.search(r"(\d+) modules here link cio; (\d+) contain the call", text)
    if not m:
        out.append("   README-CIO no longer states the population -- check by hand")
        return
    if (int(m.group(1)), int(m.group(2))) == (total, len(rows)):
        return
    new = "%d modules here link cio; %d contain the call" % (total, len(rows))
    out.append("   README-CIO  %s -> %s" % (m.group(0), new))
    write(p, text.replace(m.group(0), new))


def mentions(name):
    """Files that still NAME the program and need a person to read them."""
    found = []
    pat = re.compile(r"(?<![A-Za-z0-9_.])%s(?![A-Za-z0-9_])" % re.escape(name))
    for rel in ["disk/SOURCES.txt"]:
        if pat.search(read(os.path.join(ROOT, rel))):
            found.append(rel)
    for tree in ["tools/screenshots", "tools/datatests", "tools/drives"]:
        base = os.path.join(ROOT, tree)
        for f in sorted(os.listdir(base)):
            p = os.path.join(base, f)
            if os.path.isfile(p) and pat.search(read(p)):
                found.append(os.path.join(tree, f))
    # Data of its own -- a score file, a library directory -- lives outside
    # CMDS and DOC and no table names it.  `greed' keeps GAMES/LIB/greed.hs,
    # and DEPENDS knows about it only until DEPENDS is regenerated.
    for base, dirs, files in os.walk(os.path.join(ROOT, "disk")):
        rel = os.path.relpath(base, ROOT)
        if rel.startswith(("disk/CMDS", "disk/DOC", "disk/SRC")):
            continue
        for f in files + dirs:
            if f == name or f.rsplit(".", 1)[0] == name:
                found.append(os.path.join(rel, f))

    src = os.path.join(ROOT, "disk/SRC")
    for d in sorted(os.listdir(src)):
        if os.path.isdir(os.path.join(src, d)) and (
                d == name or os.path.exists(os.path.join(src, d, name + ".c"))):
            found.append("disk/SRC/" + d)
    return found


def remove(name):
    out = []
    print("=" * 70)
    print(name)
    b = binary_path(name)
    if b:
        drop_file(b, out)
    else:
        out.append("   NO BINARY under disk/CMDS -- check the name")
    for rel in ["disk/DOC/" + name, "docs/help/%s.txt" % name,
                "docs/screens/%s.txt" % name, "tools/playtests/%s.keys" % name,
                "tools/drives/%s.drive" % name]:
        drop_file(rel, out)
    strip_rows(name, out)
    strip_index(name, out)
    strip_origins(name, out)
    strip_usage_status(name, out)
    strip_card(name, out)
    sync_cio_count(out)
    print("\n".join(out) if out else "   nothing found")
    left = mentions(name)
    if left:
        print("   BY HAND -- still names it:")
        for f in left:
            print("      %s" % f)


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--dry-run" in args:
        DRY = True
        args.remove("--dry-run")
    if not args:
        sys.exit(__doc__)
    for n in args:
        remove(n)
