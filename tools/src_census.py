#!/usr/bin/env python3
"""How many programs on this disk have source here, and which do not.

The companion to doc_census.py, and it exists for the same reason. The figure
in CLAUDE.md -- "390 of 938 distinct programs have source identifiable here,
42%" -- was taken by hand on 2026-08-21 and could not be re-derived, and a
number nobody can re-derive is a number nobody should quote.

A program counts as having source by one of four routes, tried in order. The
order matters: each is stronger evidence than the one below it.

  RECIPE    tools/rebuild/recipes.psv builds it, and names the tree. This is
            not an inference -- a recipe that is in that file has been run.
  DIRECT    disk/SRC/<program>/ exists, or some file under disk/SRC is named
            <program>.c, .cc or .a
  ARCHIVE   disk/SRC/<archive>/ exists, where DOC/ORIGINS says the program
            came from <archive>. A source tree here is named by ARCHIVE, not
            by program -- SRC/divutils holds gen, run and if -- and skipping
            this route over-counts "no source" wildly.
  NONE      nothing. Most of CMDS is this, and that is the point of the
            collection: the binaries are the artefact, because for most of
            them no source survives anywhere.

Build products are NOT source. A run leaves ctmp_*.c and ctmp_*.a beside the
sources -- c68 emits assembly -- so counting *.a naively during a build turns
187 files into evidence for programs that have none. Run this on a clean tree;
it refuses to guess and says so if it finds any.

  tools/src_census.py disk                 summary
  tools/src_census.py disk --list          + every program with no source
  tools/src_census.py disk --tsv <file>    program, directory, verdict, where
"""
import os
import re
import sys

SRC_SUFFIX = (".c", ".cc", ".a", ".y", ".l", ".p", ".f", ".mod", ".pas")


def cr_text(path):
    """Read an OS-9 text file. They are CR-terminated, so splitlines() on the
    raw bytes gives one enormous line and every grep over it lies."""
    return open(path, "rb").read().decode("latin-1").replace("\r", "\n")


def src_index(srcroot):
    """Two indexes over disk/SRC: the top-level tree names, and every stem of
    a source FILE anywhere beneath. Both lowercased. Also counts the build
    leftovers it deliberately ignores, so the caller can refuse to report."""
    trees, stems, leftovers = {}, {}, 0
    if not os.path.isdir(srcroot):
        return trees, stems, leftovers
    for d in sorted(os.listdir(srcroot)):
        if os.path.isdir(os.path.join(srcroot, d)):
            trees[d.lower()] = os.path.join(srcroot, d)
    for dirpath, _dirs, files in os.walk(srcroot):
        for f in files:
            if f.startswith("ctmp_") or f.startswith("ctmp."):
                leftovers += 1
                continue
            stem, ext = os.path.splitext(f)
            if ext.lower() in SRC_SUFFIX and stem:
                stems.setdefault(stem.lower(), os.path.join(dirpath, f))
    return trees, stems, leftovers


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


def recipe_map(repo):
    """program -> source tree, from tools/rebuild/recipes.psv."""
    path = os.path.join(repo, "tools", "rebuild", "recipes.psv")
    out = {}
    if not os.path.isfile(path):
        return out
    for line in open(path, encoding="latin-1"):
        line = line.rstrip("\n")
        if not line or line.startswith("#") or "|" not in line:
            continue
        prog, tree = line.split("|")[0], line.split("|")[1]
        out[prog] = tree
    return out


def programs(root):
    """Every program file under CMDS, as (name, directory-relative-to-disk)."""
    out = []
    for dirpath, _dirs, files in os.walk(os.path.join(root, "CMDS")):
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
    repo = os.path.dirname(os.path.abspath(root)) if os.path.basename(
        os.path.abspath(root)) == "disk" else os.path.abspath(root)
    want_list = "--list" in argv
    tsv = argv[argv.index("--tsv") + 1] if "--tsv" in argv else None

    trees, stems, leftovers = src_index(os.path.join(root, "SRC"))
    if leftovers:
        print(f"  {leftovers} build leftover(s) under SRC -- run "
              f"tools/rebuild/tidy.sh first.", file=sys.stderr)
        print("  (they are excluded, but a build may also be running, and "
              "then\n   the tree is half one state and half another.)",
              file=sys.stderr)
    origins = origins_map(os.path.join(root, "DOC"))
    recipes = recipe_map(repo)

    rows = []
    counts = {"RECIPE": 0, "DIRECT": 0, "ARCHIVE": 0, "NONE": 0}
    for prog, d in programs(root):
        low = prog.lower()
        arch = origins.get(prog, "").lower()
        if prog in recipes:
            verdict, where = "RECIPE", "SRC/" + recipes[prog]
        elif low in trees:
            verdict, where = "DIRECT", os.path.relpath(trees[low], root)
        elif low in stems:
            verdict, where = "DIRECT", os.path.relpath(stems[low], root)
        elif arch and arch in trees:
            verdict, where = "ARCHIVE", os.path.relpath(trees[arch], root)
        else:
            verdict, where = "NONE", ""
        counts[verdict] += 1
        rows.append((prog, d, verdict, where))

    total = len(rows)
    have = total - counts["NONE"]
    print(f"  programs under CMDS        {total}")
    print(f"  source identifiable here   {have}  ({have * 100 // total}%)")
    print(f"      built by a recipe      {counts['RECIPE']}")
    print(f"      a tree or file named   {counts['DIRECT']}")
    print(f"      via DOC/ORIGINS        {counts['ARCHIVE']}")
    print(f"  no source anywhere here    {counts['NONE']}")

    by_dir = {}
    for p, d, v, _w in rows:
        if v == "NONE":
            by_dir.setdefault(d, []).append(p)
    if by_dir:
        print("\n  no source, by directory:")
        for d in sorted(by_dir, key=lambda k: -len(by_dir[k]))[:12]:
            print(f"    {len(by_dir[d]):4d}  {d}")
        if want_list:
            for d in sorted(by_dir):
                print(f"\n  {d}:")
                for i in range(0, len(by_dir[d]), 6):
                    print("    " + "  ".join(f"{p:<14}"
                                             for p in by_dir[d][i:i + 6]))

    if tsv:
        with open(tsv, "w") as fh:
            fh.write("program\tdirectory\tverdict\twhere\n")
            for r in rows:
                fh.write("\t".join(r) + "\n")
        print(f"\n  wrote {tsv} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
