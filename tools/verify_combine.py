#!/usr/bin/env python3
"""Combine the four sweep stages into one verdict per program.

    tools/verify_combine.py            -> notes/verify-final.tsv, and a summary

The sweep is four passes because each of the first three produces answers the
next one overturns, and running them in the wrong order gives a confidently
wrong number:

    verify_all.sh        every program, nothing on stdin        -> verify-bare.tsv
    verify_filters.sh    the SILENT ones, with text on stdin    -> verify-filters.tsv
    verify_in_session.sh what is left, through SYS/login        -> verify-session.tsv
    verify_usage.sh      the remainder, asked for usage         -> verify-usage.tsv

This existed only as somebody's hand-work: `notes/verify-final.tsv` was in the
repository with no tool that could produce it, so the one number the collection
advertises most loudly -- "877 of 925 run" -- could not be recomputed. Now it
can.

The verdict strings match what `verify-final.tsv` already used, so the file
stays comparable across passes.
"""
import os
import re
import subprocess
import sys

NOTES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "notes")

# Later stages only ever IMPROVE a verdict: a program that printed something
# bare is not re-judged by whether it also answers `-?`.
STAGES = [
    ("verify-bare.tsv",    {"OK": "OK bare"}),
    ("verify-filters.tsv", {"FILTER": "OK as a filter"}),
    ("verify-session.tsv", {"SESSION-OK": "OK in a session"}),
    ("verify-usage.tsv",   {"USAGE-OK": "OK given arguments"}),
]


def read(name):
    path = os.path.join(NOTES, name)
    if not os.path.exists(path):
        return None
    rows = {}
    for line in open(path, encoding="latin-1"):
        parts = line.rstrip("\n").split("\t")
        if len(parts) >= 3 and parts[0] != "program":
            rows[(parts[0], parts[1])] = parts[2]
    return rows


def not_programs(disk):
    """The files under CMDS that are not 68k programs, per module_census.py.

    DOC/STATUS quotes its percentage against ACTUAL PROGRAMS, not against every
    file in CMDS: a trap library, a driver, a BASIC09 I-code module or a data
    module proves nothing by failing to run. `module_census.py` owns that
    judgement -- it reads M$Type and M$Lang out of each header -- so ask it
    rather than keeping a second copy of the rule that can drift.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    census = os.path.join(here, "module_census.py")
    out = subprocess.run([sys.executable, census, disk],
                         capture_output=True, text=True).stdout
    names, seen = set(), False
    for line in out.splitlines():
        if line.startswith("not a 68k program"):
            seen = True
            continue
        if seen:
            m = re.match(r"   (\S+)\s+(\S+)\s", line)
            if not m:
                break
            names.add((m.group(1), m.group(2)))
    return names


def main():
    bare = read("verify-bare.tsv")
    if not bare:
        sys.exit("no notes/verify-bare.tsv -- run tools/verify_all.sh first")

    final = {k: "NEEDS WORK" for k in bare}
    missing = []
    for name, wins in STAGES:
        rows = read(name)
        if rows is None:
            missing.append(name)
            continue
        for key, verdict in rows.items():
            if key in final and final[key] == "NEEDS WORK" and verdict in wins:
                final[key] = wins[verdict]

    out = os.path.join(NOTES, "verify-final.tsv")
    with open(out, "w") as f:
        f.write("program\tdirectory\tverdict\n")
        for (prog, where) in sorted(final, key=lambda k: (k[1], k[0])):
            f.write(f"{prog}\t{where}\t{final[(prog, where)]}\n")

    tally = {}
    for v in final.values():
        tally[v] = tally.get(v, 0) + 1
    ran = sum(n for v, n in tally.items() if v.startswith("OK"))
    print(f"wrote {out}  ({len(final)} rows)")
    for v, n in sorted(tally.items(), key=lambda kv: -kv[1]):
        print(f"  {n:5}  {v}")
    print("  -----")
    print(f"  {ran:5}  of {len(final)} FILES under CMDS"
          f"  ({100 * ran / len(final):.1f}%)")

    disk = os.path.join(NOTES, "..", "disk")
    if os.path.isdir(disk):
        skip = not_programs(disk)
        progs = {k for k in final if k not in skip}
        pran = sum(1 for k in progs if final[k].startswith("OK"))
        print(f"  {pran:5}  of {len(progs)} ACTUAL PROGRAMS"
              f"  ({100 * pran / len(progs):.1f}%)   <- the DOC/STATUS figure")
        print(f"         ({len(skip)} files are not 68k programs at all --"
              f" see DOC/README-MODULES)")
    if missing:
        print("\nSTAGES NOT RUN, so their programs are still NEEDS WORK:")
        for m in missing:
            print("   ", m)
        print("The percentage above is a FLOOR, not the answer.")


if __name__ == "__main__":
    main()
