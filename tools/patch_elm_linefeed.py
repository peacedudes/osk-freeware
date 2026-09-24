#!/usr/bin/env python3
"""Let ELM's frm and newmail see the blank line that ends a message header.

    patch_elm_linefeed.py <disk-dir>            report only
    patch_elm_linefeed.py <disk-dir> --apply    write them

Both count a message when a line of the folder begins with LINE_FEED --
`if (buffer[0] == LINE_FEED)', UTILS/from.c and UTILS/newmail.c of the
ELM 2.4 tree these binaries were built from, SRC/infoxpress/BNU/ELM_2.4.
The port's HDRS/defs.h defines LINE_FEED as '\\012' under OSK, a real
line feed, but an OS-9 folder's blank line is a carriage return.
So the header never ends and nothing is counted: frm answers "You have no
mail." over a folder that elm and messages both read one message from.
Measured 2026-09-24 as tester and as the super-user; a folder whose header
ends in a lone LF byte is listed at once, which is the proof.  elm itself
is not affected -- SRC/newmbox.c also accepts an empty line.

  CMDS/ELM/frm      read_headers(): cmpi.b #$0A,$444(a7) -> #$0D
  CMDS/ELM/newmail  the same test:  cmpi.b #$0A,$10(a7)  -> #$0D

One byte each.  Module header untouched; the CRC is recomputed.  Same
shape as tools/patch_uid_mask.py.
"""
import os
import sys

PATCHES = {
    "CMDS/ELM/frm":     [(0xfca, bytes.fromhex("0c2f000a0444"),
                          bytes.fromhex("0c2f000d0444"))],
    "CMDS/ELM/newmail": [(0xa52, bytes.fromhex("0c2f000a0010"),
                          bytes.fromhex("0c2f000d0010"))],
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
