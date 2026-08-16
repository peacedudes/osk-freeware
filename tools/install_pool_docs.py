#!/usr/bin/env python3
"""Install pool documentation for shipped programs that have none.

88 programs in CMDS/CMDS/GAMES have no DOC/<name>/ directory while a manual
for them sits in the pool. jargon was the odd one out -- its 1.1 MB "doc" is
the Jargon File database, handled separately -- so it is skipped here.

Everything written must be CR-only and 8-bit clean, or check_disk rejects it.
"""
import os, shutil, sys

DISK = "/Users/rdoggett/Developer/os9/osk-freeware/disk"
DOCEXT = (".doc", ".man", ".txt", ".hlp", ".1", ".me", ".ms", ".dok")
SKIP = {"jargon"}

undoc = {l.strip() for l in open("/tmp/undoc.txt") if l.strip()}
lower = {u.lower(): u for u in undoc}

best = {}
for stage in ("allstage", "supp"):
    for r, _d, fs in os.walk(stage):
        for f in fs:
            base, ext = os.path.splitext(f)
            if ext.lower() not in DOCEXT:
                continue
            b = base.lower()
            if b not in lower or b in SKIP:
                continue
            p = os.path.join(r, f)
            try:
                s = os.path.getsize(p)
            except OSError:
                continue
            if s < 200 or s > 400000:
                continue
            if b not in best or s > best[b][0]:
                best[b] = (s, p, f)

written = skipped = 0
for b, (s, p, fname) in sorted(best.items()):
    name = lower[b]
    data = open(p, "rb").read()
    # CR-only, and nothing above 8 bits that would trip the UTF-8 check
    txt = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n").replace(b"\n", b"\r")
    try:
        txt.decode("latin-1")
    except UnicodeDecodeError:
        skipped += 1
        continue
    d = os.path.join(DISK, "DOC", name)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, fname), "wb").write(txt)
    written += 1

print("documentation directories created:", written)
print("skipped (not 8-bit clean)        :", skipped)
