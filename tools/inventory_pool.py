#!/usr/bin/env python3
"""Every OS-9 module in an extracted pool tree, and whether the disk has it.

Reads module names from M$Name (a 4-byte big-endian offset at 0x0C, pointing
at a NUL-terminated string -- 68k, not the 6809 high-bit convention) and the
module type from the whole byte at 0x12.

Usage: inventory_pool.py <extracted-pool> <disk-tree>
"""
import os, struct, sys, collections

TYPES = {0x01: "prog", 0x02: "subr", 0x03: "multi", 0x04: "data", 0x0B: "trap",
         0x0C: "system", 0x0D: "filemgr", 0x0E: "driver", 0x0F: "descriptor"}


def name_of(d):
    try:
        off = struct.unpack(">I", d[0x0C:0x10])[0]
        if not 0 < off < len(d):
            return ""
        out = []
        for b in d[off:off + 40]:
            c = b & 0x7F
            if c < 0x21 or c > 0x7E:
                break
            out.append(chr(c))
        return "".join(out)
    except Exception:
        return ""


def main():
    stage, disk = sys.argv[1], sys.argv[2]
    mods = collections.defaultdict(list)
    for r, _d, fs in os.walk(stage, followlinks=True):
        for f in fs:
            p = os.path.join(r, f)
            try:
                with open(p, "rb") as fh:
                    head = fh.read(0x20)
                    if head[:2] != b"\x4a\xfc":
                        continue
                    fh.seek(0)
                    d = fh.read()
            except OSError:
                continue
            mods[(name_of(d) or f).lower()].append(
                (d[0x12] if len(d) > 0x12 else 0, len(d), os.path.relpath(p, stage)))

    have = set()
    for r, _d, fs in os.walk(os.path.join(disk, "CMDS")):
        have |= {n.lower() for n in fs}

    absent = {k: v for k, v in mods.items() if k not in have}
    print("distinct modules in the pool : %d" % len(mods))
    print("already on the disk          : %d" % (len(mods) - len(absent)))
    print("NOT on the disk              : %d" % len(absent))
    print()
    by = collections.Counter(TYPES.get(sorted(v, key=lambda x: -x[1])[0][0], "?")
                             for v in absent.values())
    for k, n in by.most_common():
        print("   %-11s %d" % (k, n))
    print()
    for k in sorted(absent):
        t, sz, p = sorted(absent[k], key=lambda x: -x[1])[0]
        print("%-16s %-11s %8d  %s" % (k, TYPES.get(t, "t%d" % t), sz, p[:86]))


main()
