#!/usr/bin/env python3
"""Reader-facing text that reveals how the library was made.

    tools/audit_craft.py                # counts per source, worst first
    tools/audit_craft.py --show INDEX   # every flagged entry of one source
    tools/audit_craft.py --names        # just the program names, for a batch

rdoggett, 2026-09-03: a card must not carry "(Oh, it's not only a this,
it's a THAT)" or any other comment revealing the craft of creating the
library.  The reader is a stranger, possibly far in the future; what they
need is what the program is and how to run it.  The same holds for the
index line and the how-to-run note, both of which the guide now shows.

What this looks for, in the four texts a reader sees -- card captions in
tools/screenshots/*.sheet, the CAPTIONS table in gen_screens.py, the
entries of DOC/INDEX, and tools/howto.psv:

    a date                      2026-08-31, "on 2026-09-01"
    the maintainer's record     measured, re-measured, verified, tested,
                                corrected, rebuilt here, this said, used to,
                                until, it turns out, the card, its card,
                                this collection, DOC/INDEX called it
    the emulator                os9exec, the emulator -- unless the program's
                                stop under it is the subject (that is a
                                judgement; it is flagged, not forbidden)

It is a PROMPT TO GO AND LOOK, and it is deliberately broad: "tested" in
"tested for primality" is fine and gets flagged anyway.  A batch reads its
own names off `--names' and rewrites what needs it.
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(REPO, "tools")
sys.path.insert(0, TOOLS)

CRAFT = re.compile(
    r"(?i)\b20[0-9]{2}-[01][0-9](-[0-3][0-9])?\b"
    r"|\b(re-?measured|measured|verified|tested|corrected|re-?checked)\b"
    r"|\brebuilt here\b|\bthis said\b|\bused to\b|\buntil 20|\bit turns out\b"
    r"|\b(the|its|this) card\b|\bthis collection\b|\bDOC/INDEX (called|said|had)"
    r"|\bos9exec\b|\bthe emulator\b|\bthe sweep\b|\bsession\b")


def why(text):
    return sorted({m.group(0).lower() for m in CRAFT.finditer(text)})


def captions():
    import screenshots
    out = []
    d = os.path.join(TOOLS, "screenshots")
    for f in sorted(os.listdir(d)):
        if f.endswith(".sheet"):
            for shot in screenshots.parse(os.path.join(d, f)):
                cap = " ".join(shot["cap"])
                for prog in [shot["name"]] + list(shot["for"]):
                    out.append((prog, f, cap))
    return out


def playtest_captions():
    import gen_screens
    return [(name, "gen_screens.py CAPTIONS", cap)
            for name, (cap, _) in gen_screens.CAPTIONS.items()]


def index_entries():
    import gen_catalog
    progs, _ = gen_catalog.from_index(os.path.join(REPO, "disk"))
    return [(n, "DOC/INDEX", p["desc"]) for n, p in sorted(progs.items())]


def howto():
    out = []
    for raw in open(os.path.join(TOOLS, "howto.psv")):
        if raw.startswith("#") or "|" not in raw:
            continue
        name, _, note = raw.rstrip("\n").partition("|")
        out.append((name.strip(), "howto.psv", note))
    return out


SOURCES = [("captions", captions), ("play-test captions", playtest_captions),
           ("INDEX", index_entries), ("howto", howto)]


def main(argv):
    show = argv[argv.index("--show") + 1] if "--show" in argv else None
    names = "--names" in argv
    flagged_names = set()
    for label, fn in SOURCES:
        rows = fn()
        bad = [(n, f, t, why(t)) for n, f, t in rows if CRAFT.search(t)]
        progs = {n for n, _, _, _ in bad}
        flagged_names |= progs
        if names:
            continue
        print("%-20s %4d of %4d entries, %d programs"
              % (label, len(bad), len(rows), len(progs)))
        if show and show.lower() in label.lower():
            for n, f, t, w in bad:
                print("  %-16s %-18s %s\n      %s" % (n, f, ", ".join(w), t[:160]))
    if names:
        print("\n".join(sorted(flagged_names)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
