#!/usr/bin/env python3
"""Program paths a sheet or case file names that the disk cannot satisfy.

    tools/stale_paths.py [disk]

Two lists, and they mean different things:

  NOT ON THE DISK AT ALL -- `/dd/CMDS/<name>' where no file of that name
  exists anywhere under `disk/CMDS'. Either the program was removed and the
  reference was left behind, or it was renamed. Both have happened:
  `drop' became `unkeep' on 2026-09-09 and `system7.drive' still drives
  `/dd/CMDS/drop'; `easter' came off the disk and `cal2.drive' still runs it,
  which is why every run of that sheet opens with three E$PNNF lines.

  WRONG DIRECTORY -- the program IS here, under a different directory, so the
  stanza names a path that cannot work while the program it wanted is fine.
  `/dd/CMDS/tex' is at `CMDS/TEXCMDS/tex'; `/dd/CMDS/readmsg' is at
  `CMDS/ELM/readmsg' -- which is the very program whose bare-name fork
  DOC/README-RUNNING warns about.

WHY THIS IS NOT A GATE.  Some of these are deliberate, and one of them is
deliberate in the WRONG-DIRECTORY list, which is the trap: `untested.cases'
runs `/dd/CMDS/bincheckr' and `/dd/CMDS/mkdict' and then EXPECTS
`(E$PNNF)' from both, because the point of that case is to record that they
live under `CMDS/GAMES'.  "Correcting" those two paths would delete the
assertion.  `no-such-module' is the point of the case that names it, and a
case may name `shell' precisely to show what happens when the reader's own
shell is absent.  A checker that failed on those would be turned off within
a week.  So this REPORTS, and the judgement stays with the person removing
or renaming a program -- run it then, and after any pass that moves a
program between directories.

It reads `tools/drives/*.drive', `tools/screenshots/*.sheet' and
`tools/datatests/*.cases', ignores comment lines, and only considers paths
under `/dd/CMDS' -- a data file under `/dd/tmp' or `/dd/small.dvi' is usually
made by the run itself, and listing those buries the answer in noise.
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = ("tools/drives", "tools/screenshots", "tools/datatests")
PROG = re.compile(r"(/dd/CMDS/[A-Za-z0-9_./-]+)")


def programs(tree):
    """Every program file under CMDS, by exact path and by bare name."""
    exact, byname = set(), {}
    root_cmds = os.path.join(tree, "CMDS")
    for root, _, files in os.walk(root_cmds):
        for f in files:
            full = os.path.join(root, f)
            rel = "/dd/" + os.path.relpath(full, tree)
            exact.add(rel.lower())
            byname.setdefault(f.lower(), []).append(rel)
    return exact, byname


def scan(tree):
    exact, byname = programs(tree)
    gone, elsewhere = {}, {}
    for d in SOURCES:
        full = os.path.join(REPO, d)
        if not os.path.isdir(full):
            continue
        for sheet in sorted(os.listdir(full)):
            path = os.path.join(full, sheet)
            if not os.path.isfile(path):
                continue
            for line in open(path, encoding="latin-1"):
                if line.lstrip().startswith("#"):
                    continue
                for m in PROG.findall(line):
                    m = m.rstrip(".,;")
                    if m.lower() in exact:
                        continue
                    if os.path.isdir(os.path.join(tree, m[4:])):
                        continue
                    name = m.rsplit("/", 1)[-1].lower()
                    bucket = elsewhere if name in byname else gone
                    bucket.setdefault(m, set()).add(sheet)
    return gone, elsewhere, byname


def main(argv):
    tree = argv[0] if argv else os.path.join(REPO, "disk")
    if not os.path.isdir(os.path.join(tree, "CMDS")):
        sys.exit("stale_paths: no CMDS under %s" % tree)
    gone, elsewhere, byname = scan(tree)

    print("NOT ON THE DISK AT ALL (%d)" % len(gone))
    for m in sorted(gone):
        print("   %-28s %s" % (m, " ".join(sorted(gone[m]))))
    print()
    print("WRONG DIRECTORY -- the program is here, under another name (%d)"
          % len(elsewhere))
    for m in sorted(elsewhere):
        name = m.rsplit("/", 1)[-1].lower()
        print("   %-28s is at %-26s %s"
              % (m, byname[name][0], " ".join(sorted(elsewhere[m]))))
    print()
    print("Neither list is a failure on its own -- read the docstring.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
