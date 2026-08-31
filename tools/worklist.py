#!/usr/bin/env python3
"""One row per program, with everything needed to decide what to do about it.

    tools/worklist.py                       # every program, TSV, to stdout
    tools/worklist.py --cat Games           # one category
    tools/worklist.py --undriven            # no tools/drives sheet runs it
    tools/worklist.py --no-test             # no datatest case and no play-test
    tools/worklist.py --brief               # name, dir, desc only

Why this exists
---------------
The work left on this collection is per-program: run it with real arguments,
check that what it does matches what DOC/INDEX says it does, and leave behind
something that can fail again.  Deciding which program to pick up next means
knowing, for each one: what the index claims, what its own usage line says,
whether a card photographs it, whether any test asserts anything about it,
and whether anybody has driven it yet.  That was five greps per program.

EVERYTHING HERE IS DERIVED, including "has this been driven": that comes
from whether a committed `tools/drives/*.drive' sheet runs the program, not
from a ledger somebody has to remember to update.  Nothing here can go stale
on its own.

Columns:

    name  dir  star  category  sub  size  src  doc  howto  card  test  driven
    usage   the program's own first usage/syntax line, lifted from the binary
    desc    its DOC/INDEX line, whitespace collapsed
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import gen_catalog                                       # noqa: E402
import screenshots                                       # noqa: E402

CASES = os.path.join(REPO, "tools", "datatests")
PLAYTESTS = os.path.join(REPO, "tools", "playtests")
SHEETS = os.path.join(REPO, "tools", "screenshots")

WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_.]*")


def carded():
    """Every program name a gallery card is hung on -- `shot' and `for'."""
    names = set()
    for f in sorted(os.listdir(SHEETS)):
        if not f.endswith(".sheet"):
            continue
        for shot in screenshots.parse(os.path.join(SHEETS, f)):
            names.add(shot["name"])
            for key, val in shot["acts"]:
                if key == "for":
                    names.update(val.split())
    return names


def tested(known):
    """Which of `known' any datatest case or play-test script names.

    A NAME MATCH, not proof the case tests that program -- a case about
    something else may well `run /dd/CMDS/cp' to stage a file.  It answers
    "is this program under any harness at all", which is the question the
    gap is about, and it errs towards saying yes: a program it calls
    untested really is one.

    Matched by WORD rather than by path, because the case files reach their
    programs through a `setup' variable -- `$P/pnmcut' is how the whole
    netpbm family is written, and a path-shaped pattern found none of it.
    """
    names = set()
    for d, pat in ((CASES, ".cases"), (PLAYTESTS, "")):
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if pat and not f.endswith(pat):
                continue
            path = os.path.join(d, f)
            if not os.path.isfile(path):
                continue
            for line in open(path, errors="replace"):
                head = line.lstrip().split(" ", 1)[0]
                if head not in ("run", "setup", "load", "case"):
                    continue
                names.update(w for w in WORD.findall(line) if w in known)
            if os.path.splitext(f)[0] in known:
                names.add(os.path.splitext(f)[0])
    return names


def driven(known):
    """Which programs a `tools/drives/*.drive' sheet actually runs.

    DERIVED, not a ledger.  A hand-kept list of "programs I have run" is one
    more thing to forget to update, and this collection's rule is that a
    figure nobody can re-derive is a figure that has already drifted.  A
    sheet naming a program IS the record that it was driven: the sheet is
    committed, the transcript is reproducible from it, and deleting the
    stanza is the only way to lose the claim.
    """
    names, sheets = {}, os.path.join(REPO, "tools", "drives")
    if not os.path.isdir(sheets):
        return names
    for f in sorted(os.listdir(sheets)):
        if not f.endswith(".drive"):
            continue
        fam = f[:-len(".drive")]
        for line in open(os.path.join(sheets, f)):
            head, _, rest = line.strip().partition(" ")
            if head == "drive" and rest.strip() in known:
                names[rest.strip()] = fam
            elif head == "run":
                for w in WORD.findall(rest):
                    if w in known:
                        names.setdefault(w, fam)
    return names


def rows():
    progs, _uncat, _unseen = gen_catalog.gather(
        os.path.join(REPO, "disk"), os.path.join(REPO, "tools",
                                                 "categories.psv"))
    known = {p["name"] for p in progs}
    cards, done = carded(), driven(known)
    tests = tested(known)
    for p in progs:
        usage = (p.get("usage") or "").split("\n")[0].strip()
        desc = " ".join((p.get("desc") or "").split())
        yield {
            "name": p["name"], "dir": p.get("dir", ""),
            "star": "*" if p.get("star") else "",
            "cat": p.get("cat", ""), "sub": p.get("sub", ""),
            "size": str(p.get("size", "")),
            "src": "src" if p.get("hassrc") else "",
            "doc": "doc" if p.get("docs") else "",
            "howto": "howto" if p.get("howto") else "",
            "card": "card" if p["name"] in cards else "",
            "test": "test" if p["name"] in tests else "",
            "driven": done.get(p["name"], ""),
            "usage": usage, "desc": desc,
        }


COLS = ("name", "dir", "star", "cat", "sub", "size", "src", "doc", "howto",
        "card", "test", "driven", "usage", "desc")


def main(argv):
    want_cat = want_sub = None
    brief = only_undriven = only_untested = only_uncarded = False
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--cat":
            i += 1
            want_cat = argv[i]
        elif a == "--sub":
            i += 1
            want_sub = argv[i]
        elif a == "--brief":
            brief = True
        elif a == "--undriven":
            only_undriven = True
        elif a == "--no-test":
            only_untested = True
        elif a == "--no-card":
            only_uncarded = True
        else:
            sys.exit(__doc__)
        i += 1

    cols = ("name", "dir", "desc") if brief else COLS
    n = 0
    for r in rows():
        if want_cat and r["cat"] != want_cat:
            continue
        if want_sub and r["sub"] != want_sub:
            continue
        if only_undriven and r["driven"]:
            continue
        if only_untested and r["test"]:
            continue
        if only_uncarded and r["card"]:
            continue
        n += 1
        print("\t".join(r[c] for c in cols))
    print("# %d programs" % n, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
