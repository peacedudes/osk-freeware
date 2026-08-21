#!/usr/bin/env python3
"""Identify every pool file by CONTENT, not by name.

Dispatching on the extension missed real archives three separate ways:
  rn.tar.Z and cnews.tar.Z are LHA archives wearing a .Z name
  elm24.lzh is not an archive at all -- it is a bare OS-9 module
  twelve files are named fileNNNN, with no extension, and are LHA or ZIP
"""
import os, sys, collections
import paths

A = paths.pool()

def kind(p):
    with open(p, "rb") as f:
        h = f.read(512)
    if not h:                                   return "empty"
    if h[:2] == b"\x4a\xfc":                    return "os9 module"
    if h[:7] == b"+AR0.0+":                     return "os9 ar"
    if h[:3] == b"ZOO":                         return "zoo"
    if h[:2] == b"PK":                          return "zip"
    if h[:2] == b"\x1f\x8b":                    return "gzip"
    if h[:2] == b"\x1f\x9d":                    return "compress"
    if h[2:6] in (b"-lh0-", b"-lh1-", b"-lh5-", b"-lhd-") or h[2:7].startswith(b"-lh"):
        return "lha"
    if len(h) > 262 and h[257:262] == b"ustar":  return "tar"
    if h[:5] == b"begin":                       return "uuencoded"
    if h.lstrip()[:1] in (b"#", b"") and b"shar" in h[:400].lower(): return "shar"
    try:
        h.decode("ascii"); return "text"
    except UnicodeDecodeError:
        pass
    # old tar: name field then octal mode at 100
    if len(h) > 156 and h[148:156].strip(b"\0 ").isdigit(): return "tar (old)"
    return "unknown"

c = collections.Counter(); rows = []
for cat in sorted(os.listdir(A)):
    d = os.path.join(A, cat)
    if not os.path.isdir(d): continue
    for f in sorted(os.listdir(d)):
        p = os.path.join(d, f)
        if not os.path.isfile(p): continue
        k = kind(p); c[k] += 1
        rows.append((cat + "/" + f, k))
for k, v in c.most_common(): print("  %-12s %3d" % (k, v))
print("  %-12s %3d" % ("TOTAL", sum(c.values())))
open("sniffed.tsv","w").write("".join("%s\t%s\n" % r for r in rows))
print("\nfiles whose real kind disagrees with their extension:")
n=0
for path, k in rows:
    ext = os.path.splitext(path)[1].lower()
    exp = {".lzh":"lha",".lha":"lha",".zip":"zip",".gz":"gzip",".tgz":"gzip",
           ".z":"compress",".ar":"os9 ar",".zoo":"zoo",".uue":"uuencoded",".tar":"tar"}.get(ext)
    if exp and exp != k:
        print("   %-42s named %-6s is %s" % (path, ext, k)); n+=1
print("  (%d)" % n)
