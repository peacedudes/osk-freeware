#!/usr/bin/env python3
"""Pool modules that share a NAME with something on the disk but differ in CONTENT.

The absent-module inventory answers "is this name on the disk?", which quietly
hides every alternate build: a different edition, a build for another CPU, or
an entirely different program that happens to share a name. `Blackjack` is the
clearest -- the disk's `blackjack` is 6 KB of BASIC09 I-code in CMDS/BROKEN,
and the pool's is a 157 KB 68k G-Windows game. Nothing but content tells them
apart.

Compares by module name (M$Name) on both sides and reports where no md5 on the
disk matches. CMDS/REBUILT is where alternates already live.

Usage: find_alternates.py <extracted-pool>... <disk-tree>
"""
import hashlib, os, struct, sys


def info(p):
    try:
        d = open(p, "rb").read()
    except OSError:
        return None
    if d[:2] != b"\x4a\xfc" or len(d) < 0x20:
        return None
    off = struct.unpack(">I", d[0x0C:0x10])[0]
    if not 0 < off < len(d):
        return None
    out = []
    for b in d[off:off + 40]:
        c = b & 0x7F
        if c < 0x21 or c > 0x7E:      # names end at NUL -- stop, never filter,
            break                      # or the terminator you split on is gone
        out.append(chr(c))
    return "".join(out), d[0x12], d[0x13], len(d), hashlib.md5(d).hexdigest()


def gather(root):
    out = {}
    for r, _d, fs in os.walk(root):
        for f in fs:
            p = os.path.join(r, f)
            i = info(p)
            if i and i[0]:
                out.setdefault(i[0].lower(), []).append((i, os.path.relpath(p, root)))
    return out


def main():
    *stages, disk = sys.argv[1:]
    d = gather(os.path.join(disk, "CMDS"))
    pool = {}
    for s in stages:
        for k, v in gather(s).items():
            pool.setdefault(k, []).extend(v)
    rows = []
    for name, entries in pool.items():
        if name not in d:
            continue
        known = {e[0][4] for e in d[name]}
        fresh = [e for e in entries if e[0][4] not in known]
        if fresh:
            rows.append((name, sorted(fresh, key=lambda e: -e[0][3])[0], d[name][0]))
    print("alternates (same module name, content the disk does not have): %d" % len(rows))
    print()
    print("%-16s %9s %-5s %9s %-5s  %s" % ("module", "pool", "t/l", "disk", "t/l", "pool path"))
    for name, (i, rel), (dd, drel) in sorted(rows):
        print("%-16s %9d %02X/%02X %9d %02X/%02X  %s"
              % (name, i[3], i[1], i[2], dd[3], dd[1], dd[2], rel[:70]))


main()
