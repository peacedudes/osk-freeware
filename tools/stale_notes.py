#!/usr/bin/env python3
r"""Find DOC/STATUS notes that say a program is broken after it was fixed.

    tools/stale_notes.py            # candidates, one per line
    tools/stale_notes.py --context  # with the whole note under each

WHY THIS EXISTS.  `DOC/STATUS' is where every "this program does not work"
note lives, and a note that records a failure OUTLIVES THE FIX -- nobody
goes back.  On 2026-09-19 six of them were two days to three weeks out of
date: `patch' (fixed the day before, and DOC/INDEX already said so),
`aprocs', `devprc', `config', `top' and `dm'.  Each had a card in the
gallery showing the program doing its job while the note still called it a
crash.

That is the whole method, and it is what this prints: a program whose
DOC/STATUS line carries a failure word AND whose published panel scores
`work' in tools/audit_panels.py is a CANDIDATE -- the two disagree, so one
of them is wrong.

THIS IS A REPORT, NOT A GATE, on purpose.  Whether a note is stale is not
mechanically decidable: `unstr', `cvtbase' and `etags' are listed here as
the record of how a whole class failed, under a paragraph that says they
were rebuilt and work, and that is the right way to keep them.  So this
prints candidates for a person to run, never a verdict.  RUN THE PROGRAM
before changing a word: the collection's own rule.

It reads only table rows -- two to six spaces, a name, two spaces, prose --
because that is where per-program verdicts live.  A failure word in a
paragraph is usually about a class rather than a program.
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import audit_panels                                      # noqa: E402

FAILURE = re.compile(
    r"\b(floods?|hangs?|never returns?|aborts?|dies|crash\w*|does nothing|"
    r"prints nothing|silent|broken|wedges?|cannot|can't|fails?)\b", re.I)
ROW = re.compile(r"^ {2,6}([A-Za-z_][A-Za-z0-9_.]{1,20})\s{2,}(\S.*)$")


def rows(status):
    """Every table row in DOC/STATUS: (line number, name, prose, rest)."""
    lines = status.split("\n")
    for n, line in enumerate(lines, 1):
        m = ROW.match(line)
        if not m:
            continue
        # The continuation lines of a row are indented past its name.
        tail = []
        for more in lines[n:]:
            if not more.strip() or ROW.match(more):
                break
            if more.startswith(" " * 8):
                tail.append(more.strip())
            else:
                break
        yield n, m.group(1), m.group(2), tail


def main(argv):
    # This one reads THIS repo -- DOC/STATUS against `audit_panels', which
    # scores the published gallery -- so there is no tree to point it at.
    # It used to accept `stale_notes.py disk' and ignore it, which reads
    # like a path argument that works.  Say so instead.
    stray = [a for a in argv if not a.startswith("-")]
    if stray:
        sys.stderr.write("stale_notes: takes no path -- it reads this "
                         "repo's disk/DOC/STATUS and the gallery\n")
        return 2

    path = os.path.join(REPO, "disk", "DOC", "STATUS")
    status = open(path, "rb").read().decode("latin-1").replace("\r", "\n")
    working = {p for p, v, _ in audit_panels.audit() if v == "work"}
    found = 0
    for n, name, prose, tail in rows(status):
        if name not in working or not FAILURE.search(prose):
            continue
        # A row that already records the change is not a stale note: the
        # four-stage sweep's tables put the old verdict and the new one on
        # the same line, `SILENT -> OK', and the old half is a failure word
        # by construction.
        if "-> OK" in prose:
            continue
        found += 1
        print("STATUS:%d  %-14s %s" % (n, name, prose[:72]))
        if "--context" in argv:
            for t in tail:
                print("%22s%s" % ("", t[:72]))
            print()
    print("\n%d row(s) whose note and whose card disagree -- run each one"
          % found)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
