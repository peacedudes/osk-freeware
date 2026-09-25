#!/usr/bin/env python3
"""Make collect2's scan loop enter on the file it read, not on a stale register.

    patch_collect_entry.py <disk-dir>            report only
    patch_collect_entry.py <disk-dir> --apply    write them

The three 1991 collect2 binaries -- GCC2/collect, gpp_collect (the same
file) and GCC139/gcc_collect -- build the table of C++ global constructors
a link needs.  scan_rof() reads the object file into a malloc'd buffer and
loops `while (ptr < data+size)', but ptr (register a3) is first set INSIDE
the loop: the entry test compares the end of the buffer with whatever main
left in a3, a pointer into collect's static area.  When the heap lands
above that area the loop runs; when it lands below, the loop never runs and
collect writes an empty table (`dc.l 0') with no error -- the link then
succeeds and the program's global objects are never constructed.  Measured
2026-09-25: `gpp -c', `mdir', then any of the three gives the empty table
at a heap of $13C180; fresh, at $246700, the right one.  No source for
these builds survives; the 1994 collect_osk.c (SRC/gccsrc272) sets ptr
before the loop, which is the fix this reproduces.

The loop's back-branch goes past the entry test, so that test runs exactly
once.  Comparing the end with the START of the buffer (a4) instead of a3
makes it "enter if the file is not empty" -- and the body sets a3 before it
reads it.

  CMDS/GCC139/gcc_collect  0x646: cmpl a3,d0 (b08b) -> cmpl a4,d0 (b08c)
  CMDS/gpp_collect         0x63c: the same
  CMDS/GCC2/collect        0x63c: the same

One byte each, checked against its surrounding bytes first.  Module header
untouched; the CRC is recomputed.  Same shape as tools/patch_elm_linefeed.py.
"""
import os
import sys

# The ten bytes before the test -- a4 = buffer, d0 = a4 + size -- then the
# test, then the start of the branch past the loop.
BEFORE = bytes.fromhex("286dfff2200cd0adfff6")
OLD = bytes.fromhex("b08b6300")
NEW = bytes.fromhex("b08c6300")

PATCHES = {
    "CMDS/GCC139/gcc_collect": 0x646,
    "CMDS/gpp_collect":        0x63c,
    "CMDS/GCC2/collect":       0x63c,
}


def crc24(data):
    acc = 0xFFFFFF
    for b in data:
        acc ^= b << 16
        for _ in range(8):
            acc <<= 1
            if acc & 0x1000000:
                acc ^= 0x800063
        acc &= 0xFFFFFF
    return acc ^ 0xFFFFFF


def patch(path, at, apply):
    d = bytearray(open(path, "rb").read())
    size = int.from_bytes(d[4:8], "big")
    if crc24(bytes(d[:size - 3])) != int.from_bytes(d[size - 3:size], "big"):
        return "%s: CRC already bad -- left alone" % path
    if d[at - len(BEFORE):at] != BEFORE:
        return "%s: bytes before 0x%x are not the expected ones -- a different binary" % (path, at)
    if d[at:at + len(NEW)] == NEW:
        return "%s: already patched" % path
    if d[at:at + len(OLD)] != OLD:
        return ("%s: bytes at 0x%x are %s, not %s -- a different binary"
                % (path, at, d[at:at + len(OLD)].hex(), OLD.hex()))
    if not apply:
        return "%s: would patch 0x%x" % (path, at)
    d[at:at + len(NEW)] = NEW
    d[size - 3:size] = crc24(bytes(d[:size - 3])).to_bytes(3, "big")
    open(path, "wb").write(d)
    e = open(path, "rb").read()
    ok = crc24(e[:size - 3]) == int.from_bytes(e[size - 3:size], "big")
    return "%s: patched, CRC %s" % (path, "ok" if ok else "VERIFY FAILED")


def main(argv):
    root, apply = argv[0], "--apply" in argv
    for rel, at in PATCHES.items():
        print(patch(os.path.join(root, rel), at, apply))


if __name__ == "__main__":
    main(sys.argv[1:])
