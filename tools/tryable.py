#!/usr/bin/env python3
"""Which cards get a "Try it" button, and what trying one needs.

    tools/tryable.py            counts, and the cards in the two smaller classes
    tools/tryable.py <name>     one card's class and why

The collection is hosted whole in a browser page (os9exec built to
WebAssembly), with the reader's own OS-9 attachable as /h1, and a card offers
Try It only when it can actually be run.

Every card was captured running, under the same emulator the page runs, so
the question is not what fails.  Three classes:

  disk  runs from this disk alone.
  h1    needs the reader's own OS-9 on /h1: the card's set-up loads
        something from /h1, runs `load' (the collection ships none -- the
        reader's is on /h1), or tools/requires.psv says the program wants the
        reader's shell or another of their commands.  The page offers these
        only once an /h1 is attached.
  no    needs something no browser tab has -- tools/try-no.psv, by hand,
        with the reason.  No button; the reason is shown instead.

Only a card that is published counts: gen_screens.py calls classify() for
the cards it writes, so a program with no capture never claims a button.
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# A requires.psv line that names the reader's own OS-9.
READER_OS9 = re.compile(r"your own OS-9|module named `shell'|Microware's "
                        r"(shell|pd|grep|copy|tmode|runb|r68|l68|del)\b")


# A `load' command in a card's run lines, however it is reached.
LOAD = re.compile(r"(^run\s+|[;&|(]\s*)(\S*/)?load\s", re.M)


def _table(name):
    rows = {}
    for line in open(os.path.join(HERE, name)):
        if line.startswith("#") or "|" not in line:
            continue
        key, rest = line.rstrip("\n").split("|", 1)
        rows.setdefault(key, []).append(rest.split("|")[0])
    return rows


def stanzas():
    """Card name -> the text of its stanza, over every sheet."""
    out = {}
    for path in sorted(glob.glob(os.path.join(HERE, "screenshots", "*.sheet"))):
        for st in re.split(r"\n(?=shot\s)", open(path).read()):
            if st.startswith("shot"):
                out[st.split()[1]] = st
    return out


def classify(name, stanza, requires=None, refused=None):
    """Return (class, reason) for one card: class is disk, h1 or no."""
    requires = _table("requires.psv") if requires is None else requires
    refused = _table("try-no.psv") if refused is None else refused
    if name in refused:
        return "no", refused[name][0]
    run = "\n".join(l for l in stanza.split("\n")
                    if not l.startswith(("cap", "try", "os9")))
    if "/h1" in run:
        return "h1", "its card loads from your own OS-9 on /h1"
    if LOAD.search(run):
        return "h1", "it wants a module made resident, with your own OS-9's load"
    for need in requires.get(name, []):
        if READER_OS9.search(need):
            return "h1", need
    return "disk", ""


def main(argv):
    req, refused, st = _table("requires.psv"), _table("try-no.psv"), stanzas()
    stale = sorted(n for n in refused if n not in st)
    if argv:
        for n in argv:
            c, why = classify(n, st.get(n, ""), req, refused)
            print("%-14s %-5s %s" % (n, c, why))
        return 0
    by = {"disk": [], "h1": [], "no": []}
    for n in sorted(st):
        by[classify(n, st[n], req, refused)[0]].append(n)
    print("%4d cards: %d disk, %d h1, %d no" % (
        len(st), len(by["disk"]), len(by["h1"]), len(by["no"])))
    for c in ("h1", "no"):
        print("\n%s: %s" % (c, " ".join(by[c])))
    if stale:
        print("\ntry-no.psv names cards that do not exist: %s" % " ".join(stale))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
