#!/usr/bin/env python3
"""How many programs on this disk have documentation, and which do not.

The answer had never been measured. It was taken by hand once, in a shell, on
2026-08-19 -- which means it could not be re-derived, and a number nobody can
re-derive is a number nobody should quote. This is that measurement as a tool.

A program counts as documented if anything under disk/DOC is named for it by
any of four routes, tried in order:

  DIRECT    a file or directory named for the program itself
  ARCHIVE   named for its source archive, via DOC/ORIGINS -- a source tree
            here is named by ARCHIVE, not by program, and forgetting that
            over-counts "undocumented" wildly (SRC/divutils holds gen, run
            and if; SRC/toys holds fifteen games)
  FAMILY    named for its CMDS subdirectory, which is how NETPBM's 169
            programs are covered by one DOC/netpbm tree
  SHARED    a document named for something else that covers it -- one of
            the collection's own guides, or an alternate build's sibling --
            for the programs listed by name in tools/doc-shared.psv

Everything else has only its one-line entry in DOC/INDEX, which every program
has by construction -- check_disk enforces it -- and which is a catalogue
entry, not documentation.

  tools/doc_census.py disk                 summary
  tools/doc_census.py disk --list          + every undocumented program
  tools/doc_census.py disk --tsv <file>    program, directory, verdict, where
"""
import os
import re
import sys

# DOC/<name> where <name> is one of these is a family tree, not a program's.
FAMILY = {
    "CMDS/NETPBM": "netpbm", "CMDS/TEXCMDS": "tex", "CMDS/UUCP": "uucpbb",
    "CMDS/ELM": "elm", "CMDS/NEWS": "cnews", "CMDS/WN": "wn",
    "CMDS/COMMS": "comms", "CMDS/DHRY": "dhry", "CMDS/GCC2": "gcc",
    "CMDS/GCC139": "gcc139", "CMDS/ADL": "adl", "CMDS/MM1": "mm1",
}

# Programs documented under ANOTHER program's name, one row each with the
# reason -- see the header of that file for why they are named one by one.
SHARED_PSV = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "doc-shared.psv")


def shared_docs(path=SHARED_PSV):
    """program -> the DOC name that documents it, from doc-shared.psv."""
    out = {}
    for line in open(path):
        if line.startswith("#") or "|" not in line:
            continue
        prog, doc = line.split("|")[:2]
        out[prog.strip()] = doc.strip()
    return out


DOC_SUFFIX = re.compile(
    r"\.(txt|doc|man|hlp|help|me|ms|1|l|dok|nr|prf|readme|md)$", re.I)


def cr_text(path):
    """Read an OS-9 text file. They are CR-terminated, so splitlines() on the
    raw bytes gives one enormous line and every grep over it lies."""
    return open(path, "rb").read().decode("latin-1").replace("\r", "\n")


def doc_names(docroot):
    """Every name under DOC that could stand for a program, lowercased."""
    names = {}
    for dirpath, dirs, files in os.walk(docroot):
        for d in dirs:
            names.setdefault(d.lower(), os.path.join(dirpath, d))
        for f in files:
            p = os.path.join(dirpath, f)
            names.setdefault(f.lower(), p)
            stem = DOC_SUFFIX.sub("", f).lower()
            if stem:
                names.setdefault(stem, p)
    return names


def origins_map(docroot):
    """program -> source archive, from DOC/ORIGINS."""
    path = os.path.join(docroot, "ORIGINS")
    out = {}
    if not os.path.isfile(path):
        return out
    for line in cr_text(path).split("\n"):
        m = re.match(r"^ {2}(\S+)\s+(\S+)\s+\S", line)
        if m and not line.startswith("  -"):
            out[m.group(1)] = m.group(2)
    return out


def programs(root):
    """Every program file under CMDS, as (name, directory-relative-to-disk)."""
    out = []
    cmds = os.path.join(root, "CMDS")
    for dirpath, dirs, files in os.walk(cmds):
        if "archives" in dirpath.split(os.sep):
            continue
        rel = os.path.relpath(dirpath, root)
        for f in sorted(files):
            out.append((f, rel))
    return out


def main(argv):
    if not argv:
        sys.exit(__doc__.strip().splitlines()[0])
    root = argv[0]
    docroot = os.path.join(root, "DOC")
    want_list = "--list" in argv
    tsv = argv[argv.index("--tsv") + 1] if "--tsv" in argv else None

    names = doc_names(docroot)
    origins = origins_map(docroot)
    shared = shared_docs()
    rows, counts = [], {"DIRECT": 0, "ARCHIVE": 0, "FAMILY": 0, "SHARED": 0, "NONE": 0}

    for prog, d in programs(root):
        low = prog.lower()
        if low in names:
            verdict, where = "DIRECT", names[low]
        elif origins.get(prog, "").lower() in names:
            verdict, where = "ARCHIVE", names[origins[prog].lower()]
        elif FAMILY.get(d, "") in names:
            verdict, where = "FAMILY", names[FAMILY[d]]
        elif shared.get(prog, "").lower() in names:
            verdict, where = "SHARED", names[shared[prog].lower()]
        else:
            verdict, where = "NONE", ""
        counts[verdict] += 1
        rows.append((prog, d, verdict, where))

    total = len(rows)
    documented = total - counts["NONE"]
    print(f"  programs under CMDS        {total}")
    print(f"  documented                 {documented}  ({documented*100//total}%)")
    print(f"      by its own name        {counts['DIRECT']}")
    print(f"      by its source archive  {counts['ARCHIVE']}")
    print(f"      by its family tree     {counts['FAMILY']}")
    print(f"      by another's document  {counts['SHARED']}")
    print(f"  NOTHING but the INDEX line {counts['NONE']}")

    if counts["NONE"]:
        by_dir = {}
        for p, d, v, _w in rows:
            if v == "NONE":
                by_dir.setdefault(d, []).append(p)
        print("\n  undocumented, by directory:")
        for d in sorted(by_dir, key=lambda k: -len(by_dir[k])):
            print(f"    {len(by_dir[d]):4d}  {d}")
        if want_list:
            for d in sorted(by_dir):
                print(f"\n  {d}:")
                for i in range(0, len(by_dir[d]), 6):
                    print("    " + "  ".join(f"{p:<14}" for p in by_dir[d][i:i+6]))

    if tsv:
        with open(tsv, "w") as fh:
            fh.write("program\tdirectory\tverdict\twhere\n")
            for r in rows:
                fh.write("\t".join(r) + "\n")
        print(f"\n  wrote {tsv} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
