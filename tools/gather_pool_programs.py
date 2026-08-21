#!/usr/bin/env python3
"""Per-program provenance, with documentation found by PROXIMITY.

An EFFO forum disk carries dozens of unrelated programs, so "this archive
contains a file mentioning a licence" says nothing about any one of them.
This walks outward from the program's own directory -- its own dir, then its
parent, then the parent's parent -- and stops at the first level that has
documentation, which is where a package keeps its own readme.
"""
import os, re, json, collections
import paths

A = paths.pool()
CATS = ("DRIVERS", "EFFO", "GWINDOWS", "NETWORK", "TELECOM")
STAGE = "newstage"

arch = {}
for c in CATS:
    for f in os.listdir(os.path.join(A, c)):
        arch[f.replace(".", "_")] = "%s/%s" % (c, f)

DOCEXT = (".doc", ".man", ".txt", ".hlp", ".1", ".me", ".ms", ".dok")
DOCNAME = ("read", "notice", "copying", "licen", "manual", "inhalt", "info")
SRCEXT = (".c", ".h", ".a", ".asm", ".p", ".mod", ".f", ".s", ".y", ".l")
TERMS = [
 ("GPL",        re.compile(rb"GNU GENERAL PUBLIC LICENSE", re.I)),
 ("public domain", re.compile(rb"public domain", re.I)),
 ("freely distributable", re.compile(rb"freely (?:be )?(?:distribut|copi)|"
                                     rb"may be freely|distribute .{0,20}freely", re.I)),
 ("shareware",  re.compile(rb"shareware|please send \$|registration fee", re.I)),
 ("restricted", re.compile(rb"may not be (?:distribut|redistribut|sold|copied)|"
                           rb"strictly prohibited|not for (?:sale|distribution)|"
                           rb"express(?:ed)? (?:written )?permission", re.I)),
 ("copyright asserted", re.compile(rb"copyright|\(c\)\s*19", re.I)),
]

def isdoc(f):
    low = f.lower()
    return low.endswith(DOCEXT) or any(low.startswith(x) for x in DOCNAME)

def scan_level(d):
    """Docs directly in d (and in a DOC/ child of d)."""
    out = []
    for cand in (d, os.path.join(d, "DOC"), os.path.join(d, "doc")):
        if not os.path.isdir(cand):
            continue
        try: names = os.listdir(cand)
        except OSError: continue
        for f in names:
            p = os.path.join(cand, f)
            if os.path.isfile(p) and isdoc(f):
                out.append(p)
    return out

rows = []
for line in open("probe/verdicts.tsv"):
    prog, bare, path = line.rstrip("\n").split("\t")
    full = os.path.join(STAGE, path)
    d = os.path.dirname(full) or STAGE
    # climb: own dir, parent, grandparent -- stop at first level with docs
    docs, level = [], 0
    cur = d
    for level in range(4):
        docs = scan_level(cur)
        if docs: break
        nxt = os.path.dirname(cur)
        if not nxt or nxt == cur or cur == STAGE or os.path.basename(cur) in CATS: break
        cur = nxt
    terms = set(); evidence = {}
    for p in docs[:12]:
        try: b = open(p, "rb").read(40000)
        except OSError: continue
        for name, pat in TERMS:
            m = pat.search(b)
            if m:
                terms.add(name)
                evidence.setdefault(name, os.path.relpath(p, STAGE))
    src = sum(1 for f in os.listdir(d) if f.lower().endswith(SRCEXT)) if os.path.isdir(d) else 0
    top = path.split("/")[0]
    if top in CATS: top = path.split("/")[1]
    rows.append({"prog": prog, "bare": bare, "path": path,
                 "archive": arch.get(top, top), "docdir": os.path.relpath(cur, STAGE),
                 "ndocs": len(docs), "src": src,
                 "terms": sorted(terms), "evidence": evidence})

json.dump(rows, open("gathered.json", "w"), indent=1)
c = collections.Counter()
for r in rows:
    c[", ".join(r["terms"]) or "(nothing found)"] += 1
print("%d programs\n" % len(rows))
for k, v in c.most_common():
    print("  %3d  %s" % (v, k))
print("\n  with local docs : %d" % sum(1 for r in rows if r["ndocs"]))
print("  with local source: %d" % sum(1 for r in rows if r["src"]))
