#!/usr/bin/env python3
r"""Find text telling the reader they have not got something they have.

    tools/absence_phrasing.py           # candidates, with the sentence
    tools/absence_phrasing.py <tree>    # a disk tree other than this repo's

WHY THIS EXISTS.  The house rule is that the reader HAS Microware OS-9, so
`copy', `time', `dir' and `del' are on their machine; saying "there is no
`copy' program on this disk" is false from where they stand.  `check_disk'
enforces it under `text names what the reader has', and that check is
deliberately narrow: it matches "not on this disk" and "neither is on this
disk" and nothing else, because a wider net would catch the many places
where the absence of DATA or HARDWARE is exactly what a reader needs told.

A NARROW PATTERN IS STILL A PATTERN, and on 2026-09-19 two pieces of
shipped text said the same thing in words the check does not carry:

  dback's card    "There is no `copy' program on this disk, so nothing is
                  copied" -- and issuing copies through the reader's own
                  `copy' is the entire point of dback, so the sentence
                  explaining the program contradicted the reason it works.
  sieve's entry   "there is no timing command here to pair it with" --
                  `time' is Microware's and came off this disk on terms
                  the day before.

**BOTH WERE ABOUT A UTILITY WE HAD JUST REMOVED**, and that is the pattern
worth carrying away: a program leaving on terms turns every sentence that
mentioned it into a candidate, because the honest way to say "we took it
out" is one short step from "you have not got one".  Run this after any
removal, beside `ghost_names.py'.

A REPORT, NOT A GATE, and it has to be: most of what the wide pattern
finds is right.  The accepted ones are listed below with their reason,
and anything else is for a person to read.
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The claim, in every phrasing seen here.  `check_disk' owns the first two;
# these are the ones it does not carry.
WIDE = re.compile(
    r"this disk does not (?:carry|have)"
    r"|there is no [^.]{0,44} here"
    r"|no [^.]{0,28} on this disk"
    r"|not (?:here|present) on this disk",
    re.I)

# Judged once, on 2026-09-19.  Each is the absence of DATA or of HARDWARE,
# which is what a reader needs told -- not the absence of a utility they
# own.  Keyed by the words themselves so that rewording brings it back for
# a fresh look.
ACCEPTED = [
    ("no host table on this disk", "msntp: data, not a utility"),
    ("No PackIt archive is on this disk", "macunpack: no sample to open"),
    ("no file on this di", "noreader: the formats have no sample here"),
    ("this disk does not carry, so it draws no board",
     "gnuchessc: a compiled-in path, not a program"),
    ("no Tektronix terminal here", "wgen: hardware"),
    ("no X server here", "basicwin: hardware"),
    ("the graphics system this disk\ncap     does not carry",
     "the G-Windows cards, whose category says the same thing"),
    ("the graphics system this disk does not carry",
     "the G-Windows cards, whose category says the same thing"),
]


def accepted(text):
    return any(a in text for a in (a for a, _ in ACCEPTED))


def shipped(disk, tools):
    """The prose this collection wrote: the index files and the captions."""
    for name in ("DOC/INDEX", "DOC/CATEGORIES", "readme"):
        p = os.path.join(disk, name)
        if os.path.isfile(p):
            yield p
    sheets = os.path.join(tools, "screenshots")
    if os.path.isdir(sheets):
        for f in sorted(os.listdir(sheets)):
            if f.endswith(".sheet"):
                yield os.path.join(sheets, f)


def main(argv):
    paths = [a for a in argv if not a.startswith("-")]
    if len(paths) > 1:
        sys.stderr.write("absence_phrasing: one tree at a time\n")
        return 2
    disk = os.path.abspath(paths[0]) if paths else os.path.join(REPO, "disk")
    if not os.path.isdir(disk):
        sys.stderr.write("absence_phrasing: %s is not a directory\n" % disk)
        return 2
    tools = os.environ.get("OSK_TOOLS_DIR", os.path.join(REPO, "tools"))

    hits = 0
    for p in shipped(disk, tools):
        raw = open(p, "rb").read().decode("latin-1")
        lines = raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        for n, line in enumerate(lines, 1):
            if line.lstrip().startswith("#"):
                continue          # a sheet's own working comment, not shipped
            body = line[8:] if line.startswith("cap     ") else line
            m = WIDE.search(body)
            if not m:
                continue
            # A caption wraps, so take the sentence from the lines around it
            # before deciding: half a phrase is not enough to judge.
            around = "\n".join(lines[max(0, n - 3):n + 2])
            if accepted(around) or accepted(m.group(0)):
                continue
            hits += 1
            where = os.path.relpath(p, REPO)
            if where.startswith(".."):
                where = p
            print("  %s:%d  %s" % (where, n, body.strip()[:70]))

    print("\n%d place(s) saying the reader has not got something -- read each "
          "one" % hits)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
