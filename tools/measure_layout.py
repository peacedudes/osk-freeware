#!/usr/bin/env python3
"""Measure where the programs on this disk expect their files to be.

Answers, by counting rather than by reading anybody's notes, the question that
decides how this collection should be arranged: **should the collection be
`/dd`, or `/h0`?**

Every count in `DOC/README-RUNNING`, `DOC/INDEX` and `CLAUDE.md` about `/h0`
paths, termcap and `/dd` data has been hand-maintained and every one of them
had drifted by 2026-08-21 -- README-RUNNING said 444 programs and 94 `/h0`
paths when the real figures were 597 and 111. Hand-edited counts rot. This
prints them, so they can be regenerated instead.

  tools/measure_layout.py disk            human-readable summary
  tools/measure_layout.py disk --tsv      one row per program, for grepping

WHAT IT MEASURES, AND THE ONE SUBTLETY

A program's absolute paths are scanned out of its binary. `/dd` references
then split into two kinds, and the split is the whole point:

  * paths THIS DISK PROVIDES -- `/dd/GAMES/adv/glorkz`, `/dd/LIB/tmac.s`.
    These want the COLLECTION mounted as `/dd`.
  * paths it does not -- `/dd/CMDS/shell`, `/dd/CMDS/del`, `/dd/DEFS/sys`.
    These want a real OS-9 SYSTEM as `/dd`, and no arrangement of this
    collection satisfies them; they are mostly Microware's own utilities.

Existence is tested case-insensitively, because OS-9's file opens are, and
`bash`'s `-f` test is not -- which is why the project's own notes warn that
`[ -f /h0/games/hack/playground ]` is false for a file that `ls` finds.

`/h0/sys/termcap` is counted apart from other `/h0` paths because it is
already settled: `SYS/login` exports TERMCAP and the programs read that first,
so those need no `/h0` at all.
"""
import os
import re
import sys

H0 = re.compile(rb'/[hH]0((?:/[A-Za-z0-9_.$-]+)+)')
DD = re.compile(rb'/[dD][dD]((?:/[A-Za-z0-9_.$-]+)+)')
TERMCAP = b'/h0/sys/termcap'
MODULE = b'\x4a\xfc'


def disk_index(disk):
    """Every path on the disk, lowercased and relative to its root."""
    seen = set()
    for root, dirs, files in os.walk(disk):
        rel = os.path.relpath(root, disk)
        for name in files + dirs:
            seen.add((rel + "/" + name).lower().lstrip("./"))
    return seen


def provided(path, index):
    """Is `/dd/foo/bar` a file this disk actually carries?"""
    return path.count("/") >= 2 and path.split("/", 2)[2].lower() in index


def scan(disk):
    """Yield (directory, name, h0 paths, dd-ours, dd-system) per program."""
    index = disk_index(disk)
    cmds = os.path.join(disk, "CMDS")
    for root, dirs, files in os.walk(cmds):
        if os.path.basename(root) == "archives":   # source archives, not programs
            continue
        for name in sorted(files):
            data = open(os.path.join(root, name), "rb").read()
            if data[:2] != MODULE:
                continue
            where = os.path.relpath(root, cmds)
            h0 = {m.group(0).lower() for m in H0.finditer(data)}
            ours, sysm = set(), set()
            for m in DD.finditer(data):
                p = m.group(0).decode().lower()
                (ours if provided(p, index) else sysm).add(p)
            yield ("CMDS" if where == "." else where), name, h0, ours, sysm


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__.strip().splitlines()[0])
    disk = sys.argv[1]
    rows = list(scan(disk))
    if "--tsv" in sys.argv:
        for where, name, h0, ours, sysm in rows:
            print(f"{where}\t{name}\t{len(h0)}\t{len(ours)}\t{len(sysm)}")
        return

    def count(sel, group=None):
        return sum(1 for r in rows if (group is None or r[0] in group) and sel(r))

    tc  = lambda r: any(p.startswith(TERMCAP) for p in r[2])
    oth = lambda r: any(not p.startswith(TERMCAP) for p in r[2])

    for label, group in (("CMDS and CMDS/GAMES", {"CMDS", "GAMES"}),
                         ("everything under CMDS", None)):
        n = count(lambda r: True, group)
        print(f"\n{label} -- {n} programs")
        print(f"  carry a /h0 path              {count(lambda r: bool(r[2]), group)}")
        print(f"    want /h0/sys/termcap        {count(tc, group)}   (settled by TERMCAP)")
        print(f"    want other /h0 data         {count(oth, group)}")
        print(f"    want both                   {count(lambda r: tc(r) and oth(r), group)}")
        print(f"  want THIS disk as /dd         {count(lambda r: bool(r[3]), group)}")
        print(f"  want an OS-9 system as /dd    {count(lambda r: bool(r[4]), group)}")
        print(f"  name no /dd path at all       {count(lambda r: not r[3] and not r[4], group)}")

    ours = count(lambda r: bool(r[3]))
    h0   = count(oth)
    print(f"\nThe arrangement question, in one line:")
    print(f"  {ours} programs want the collection at /dd; {h0} want data at /h0.")
    if h0:
        print(f"  Ratio {ours / h0:.1f} to 1 in favour of /dd.")


if __name__ == "__main__":
    main()
