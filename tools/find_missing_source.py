#!/usr/bin/env python3
"""Which shipped programs have a same-named source inside a pool archive?

`tools/src_census.py' says how many programs have source HERE. This says where
the rest might be found: it crosses the programs under disk/CMDS that have no
matching file in disk/SRC against the archive-content index written by
tools/index_archives.py -- which sees inside archives nobody ever unpacked, and
that is the whole point. A plain `find' over the hoard cannot answer this.

    tools/index_archives.py > notes/pool-archive-contents.tsv
    tools/find_missing_source.py > notes/source-candidates.tsv

**A NAME MATCH IS A LEAD, NOT A FINDING.** This collection has already shipped
a recipe pointing at the wrong `pep' -- a German EPROM programmer, where what
ships is a text filter of the same name -- and `notes/` records three more
source files that only shared a name. Every row here has to be opened and read
before it is believed. The column that helps most is the archive: a name found
in the same package as other things we ship is worth more than a name found in
a grab-bag.
"""
import collections
import os
import sys

SRC_EXT = (".c", ".a", ".asm")


def shipped_without_source(root):
    progs, have = set(), set()
    for dirpath, _d, files in os.walk(os.path.join(root, "CMDS")):
        for f in files:
            if not f.startswith("."):
                progs.add(f)
    for dirpath, _d, files in os.walk(os.path.join(root, "SRC")):
        for f in files:
            if f.endswith(SRC_EXT):
                have.add(os.path.splitext(f)[0].lower())
    return sorted(p for p in progs if p.lower() not in have)


def archive_index(path):
    idx = collections.defaultdict(list)
    with open(path, encoding="latin-1") as fh:
        for line in fh:
            if "\t" not in line:
                continue
            arch, member = line.rstrip("\n").split("\t", 1)
            stem, ext = os.path.splitext(os.path.basename(member))
            if ext.lower() in SRC_EXT:
                idx[stem.lower()].append((arch, member))
    return idx


def main(argv):
    root = argv[0] if argv else "disk"
    index = argv[1] if len(argv) > 1 else "notes/pool-archive-contents.tsv"
    if not os.path.isfile(index):
        sys.exit(f"no archive index at {index} -- run tools/index_archives.py first")
    idx = archive_index(index)
    missing = shipped_without_source(root)
    print("program\tarchive\tmember")
    hits = 0
    for prog in missing:
        for arch, member in idx.get(prog.lower(), []):
            print(f"{prog}\t{arch}\t{member}")
            hits += 1
    names = len({p for p in missing if p.lower() in idx})
    print(f"# {len(missing)} shipped programs with no same-named source in SRC; "
          f"{names} of them appear in {hits} archive members", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
