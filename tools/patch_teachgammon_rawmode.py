#!/usr/bin/env python3
"""Give teachgammon's raw-mode terminal options a starting point.

    patch_teachgammon_rawmode.py <disk-dir>            report only
    patch_teachgammon_rawmode.py <disk-dir> --apply    write it

BSD teachgammon, no source on the disk.  At start-up it reads the
terminal's options with _gs_opt into one 128-byte block and keeps three
more beside it: the original, a raw-mode block and a no-echo block.  It
copies the original into the no-echo block and clears two bytes there,
but it never copies anything into the raw-mode block -- it only clears
that block's echo byte.  So the block it hands to _ss_opt for raw mode is
128 bytes of zero, and every field it did not mean to touch goes with it:
the end-of-record and end-of-file characters, the interrupt and quit
characters, the page length, and PD_BAU.  Measured 2026-10-02 with an
instrumented os9exec that logged each console SS_Opt: PD_BAU went from
$0F (19200) to $00 (50 baud), and os9exec, which paces the console to
PD_BAU, printed its text at five characters a second.

The four blocks lie 128 bytes apart -- the _gs_opt buffer, the original,
the raw-mode block, the no-echo block -- and the loop that saves the
original copies 32 longs from the first to the second.  Copying 64 longs
instead carries on into the raw-mode block from the original it has just
written, so raw mode starts as the terminal's own options with echo off,
which is all the program then changes.

  CMDS/GAMES/teachgammon  0x577e: moveq #31,d0 -> moveq #63,d0

One byte.  Module header untouched; the CRC is recomputed.  Same shape as
tools/patch_head_close.py.
"""
import os
import sys

# lea -30956(a6),a0; lea -30828(a6),a1; moveq #N,d0; move.l (a0)+,(a1)+; dbf
PATCHES = {
    "CMDS/GAMES/teachgammon": [(0x5776,
                                bytes.fromhex("41ee871443ee8794701f22d851c8fffc"),
                                bytes.fromhex("41ee871443ee8794703f22d851c8fffc"))],
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
