#!/usr/bin/env python3
"""Find documentation in the archive pool for programs that ship without any.

Feeds off tools/doc_census.py: for every program with NOTHING but its one-line
DOC/INDEX entry, look through the pool's member inventory for a file that is
plausibly that program's manual, then extract only the archives that scored a
hit. Extracting all 454 archives to find a few hundred files would take an hour
and is unnecessary -- notes/pool-members.tsv already lists every member.

A member is a candidate when its basename, minus a documentation extension,
equals the program name. That is deliberately strict. Loosening it to
"contains the name" matches `ls` inside `tools.doc`, `false` inside
`falsecolour.txt`, and several hundred others -- the kind of near-miss that
produces a big number and a useless result.

Nothing is installed. This writes a plan; tools/install_pool_docs.py applies
one after tools/screen_microware.py has passed it.

  tools/find_pool_docs.py disk <members.tsv> [--out plan.tsv]
"""
import os
import re
import sys

import doc_census
import paths

DOC_EXT = (".doc", ".man", ".txt", ".hlp", ".help", ".me", ".ms", ".1",
           ".dok", ".nr", ".prf", ".readme", ".rme", ".notes")

# A manual is prose. Below this it is a stub; above it, it is a database
# masquerading as documentation -- jargon's 1.1 MB "doc" is the Jargon File.
MIN_BYTES, MAX_BYTES = 200, 400_000


# A package's manual is very often not named for the program at all -- it is
# `readme' inside a directory that is. PROGRAMME/C/GREG/greg.doc is caught by
# the name rule; SOFTWARE/C/DEVPRC/readme is only caught by this one, and that
# shape is the commoner of the two in this pool.
GENERIC_DOC = {"readme", "read.me", "read_me", "readme.1st", "readme.txt",
               "readme.os9", "readme.osk", "read.1st", "liesmich", "doc",
               "manual", "manual.txt", "usage", "usage.txt", "help",
               "info", "info.txt", "notes", "changes", "history"}


def candidate_names(prog):
    """The filenames that would be this program's manual."""
    p = prog.lower()
    return {p + e for e in DOC_EXT} | {p + ".v" + e for e in DOC_EXT}


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__.strip().splitlines()[0])
    root, members = argv[0], argv[1]
    out = argv[argv.index("--out") + 1] if "--out" in argv else None

    # 1. who needs a manual
    names = doc_census.doc_names(os.path.join(root, "DOC"))
    origins = doc_census.origins_map(os.path.join(root, "DOC"))
    need = {}
    for prog, d in doc_census.programs(root):
        low = prog.lower()
        if low in names:
            continue
        if origins.get(prog, "").lower() in names:
            continue
        if doc_census.FAMILY.get(d, "") in names:
            continue
        need[low] = (prog, d)
    print(f"  {len(need)} programs have no documentation", file=sys.stderr)

    # 2. index every candidate filename once, then stream the inventory past it
    wanted = {}
    for low, (prog, d) in need.items():
        for cand in candidate_names(prog):
            wanted.setdefault(cand, []).append(prog)

    hits = {}
    with open(members) as fh:
        next(fh, None)
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 5:
                continue
            cat, archive, size, status, member = parts[:5]
            base = os.path.basename(member).lower()
            if base in wanted:
                for prog in wanted[base]:
                    hits.setdefault(prog, []).append((cat, archive, member))
            elif base in GENERIC_DOC:
                parent = os.path.basename(os.path.dirname(member)).lower()
                if parent in need:
                    hits.setdefault(need[parent][0], []).append(
                        (cat, archive, member))

    print(f"  {len(hits)} of them have a candidate in the pool", file=sys.stderr)

    rows = []
    for prog in sorted(hits):
        for cat, archive, member in hits[prog]:
            rows.append((prog, need[prog.lower()][1], cat, archive, member))

    if out:
        with open(out, "w") as fh:
            fh.write("program\tdirectory\tcategory\tarchive\tmember\n")
            for r in rows:
                fh.write("\t".join(r) + "\n")
        print(f"  wrote {out} ({len(rows)} candidate files)", file=sys.stderr)

    archives = sorted({(c, a) for _p, _d, c, a, _m in rows})
    print(f"  they live in {len(archives)} archives", file=sys.stderr)
    for prog in sorted(hits)[:40]:
        c, a, m = hits[prog][0]
        print(f"    {prog:<16} {a:<26} {m}")
    if len(hits) > 40:
        print(f"    ... and {len(hits)-40} more")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
