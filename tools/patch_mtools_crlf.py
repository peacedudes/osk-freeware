#!/usr/bin/env python3
"""Make mtools end a DOS text line CR LF, not LF CR.

    patch_mtools_crlf.py <disk-dir>            report only
    patch_mtools_crlf.py <disk-dir> --apply    write it

With -t (text), mscopy, mswrite and the mtools multi-call binary turn each
OS-9 line end into DOS's two bytes.  The port's write_filter() in
SRC/mtools/MTOOLS_3.6/filter.c stores 0x0A and then '\\n', which on OS-9 is
CR -- so a file copied to a DOS disk ended every line LF CR, measured
2026-09-28 with a dump of motd copied out and read back.  DOS wants CR LF.
Reading is unaffected: read_filter() drops the LF wherever it falls.

The two stores are `move.b #$0A,(a1)' and, sixteen bytes on,
`move.b #$0D,(a1)'.  Swapping the two immediate bytes swaps the order.

A rebuild from the same source was tried first and rejected: this SDK's
libraries answer stat() and time() a time-zone apart, so the rebuilt
commands took a fresh .mcwd for six hours old and forgot every mscd.  The
archive binaries do not, and keeping them is worth more than the rebuild.

Two bytes per file; module header untouched; the CRC is recomputed.
"""
import os
import sys

OLD = bytes.fromhex("12bc000a52adfff02248d3edfff012bc000d52adfff0")
NEW = bytes.fromhex("12bc000d52adfff02248d3edfff012bc000a52adfff0")
PATCHES = {
    "CMDS/mscopy": [(0xa30e, OLD, NEW)],
    "CMDS/msread": [(0xa30e, OLD, NEW)],
    "CMDS/mswrite": [(0xa30e, OLD, NEW)],
    "CMDS/mstype": [(0xa312, OLD, NEW)],
    "CMDS/mtools": [(0x12f8e, OLD, NEW)],
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


def patch(path, edits, apply):
    d = bytearray(open(path, "rb").read())
    size = int.from_bytes(d[4:8], "big")
    if crc24(bytes(d[:size - 3])) != int.from_bytes(d[size - 3:size], "big"):
        return "%s: CRC already bad -- left alone" % path
    if all(d[at:at + len(new)] == new for at, old, new in edits):
        return "%s: already patched" % path
    for at, old, new in edits:
        if len(old) != len(new):
            return "%s: patch at 0x%x changes length -- refused" % (path, at)
        if d[at:at + len(old)] != old:
            return ("%s: bytes at 0x%x are %s, not %s -- a different binary"
                    % (path, at, d[at:at + len(old)].hex(), old.hex()))
    if not apply:
        return "%s: would patch %s" % (path, ", ".join("0x%x" % e[0] for e in edits))
    for at, old, new in edits:
        d[at:at + len(new)] = new
    d[size - 3:size] = crc24(bytes(d[:size - 3])).to_bytes(3, "big")
    open(path, "wb").write(d)
    e = open(path, "rb").read()
    ok = crc24(e[:size - 3]) == int.from_bytes(e[size - 3:size], "big")
    return "%s: patched, CRC %s" % (path, "ok" if ok else "VERIFY FAILED")


def main(argv):
    root, apply = argv[0], "--apply" in argv
    for rel, edits in PATCHES.items():
        print(patch(os.path.join(root, rel), edits, apply))


if __name__ == "__main__":
    main(sys.argv[1:])
