#!/usr/bin/env python3
"""Let uuencode take the `infile name' pair its own usage line names.

    patch_uuencode.py <disk-dir>            report only
    patch_uuencode.py <disk-dir> --apply    write it

CMDS/uuencode (EFFO public-domain disk 3, UU; no source anywhere -- the
uuencode.c in SRC/uucpbb is a different program) prints

    USAGE: uuencode >outfile [infile] name

and then refuses exactly that: given two arguments it prints the line and
exits 11.  Disassembled, main() opens argv[1] when argc > 1, decrements
argc, and then demands argc == 1 -- so only the one-argument form ever
worked, with the file's own pathlist written as the name on the `begin'
line.  With no argument at all it read standard input and wrote a null
pointer as the name.

The patch rewrites the 58 bytes after the fopen() (0x2ca-0x303) and one
branch (0x280) so that:

    uuencode file          as before -- the name is the pathlist given
    uuencode file name     now works -- `begin 644 name'
    uuencode               the usage line, exit 11 (was a null name)
    three or more          the usage line, exit 11 (was the usage line)

The name is argv[argc-1]:  move.l 8(sp),d0 / lsl.l #2,d0 / movea.l
12(sp),a0 / move.l -4(a0,d0.l),-(sp), in the place of movea.l 12(sp),a0 /
move.l 4(a0),-(sp).  The usage exit is the original's, moved down eight
bytes with its three PC-relative displacements recomputed; three NOPs fill
the gap.  Module header untouched; the CRC is recomputed.  Same shape as
tools/patch_elm_linefeed.py.
"""
import os
import sys

OLD_TAIL = bytes.fromhex(
    "53af0008"      # 2ca  subq.l #1,8(sp)           argc--
    "6008"          # 2ce  bra.s  2d8
    "41ee801e"      # 2d0  lea    -32738(a6),a0      stdin
    "2f480004"      # 2d4  move.l a0,4(sp)
    "7001"          # 2d8  moveq  #1,d0
    "b0af0008"      # 2da  cmp.l  8(sp),d0
    "6716"          # 2de  beq.s  2f6                argc == 1 or usage
    "41fa02f8"      # 2e0  lea    usage(pc),a0
    "2208"          #      move.l a0,d1
    "41ee8056"      #      lea    stderr,a0
    "2008"          #      move.l a0,d0
    "61000422"      #      bsr    fprintf
    "700b"          #      moveq  #11,d0
    "6100062a"      #      bsr    exit
    "2ebc000001a4"  # 2f6  move.l #420,(sp)          mode 644
    "206f000c"      # 2fc  movea.l 12(sp),a0
    "2f280004")     # 300  move.l 4(a0),-(sp)        name = argv[1]

NEW_TAIL = bytes.fromhex(
    "7003"          # 2ca  moveq  #3,d0
    "b0af0008"      # 2cc  cmp.l  8(sp),d0
    "6d16"          # 2d0  blt.s  2e8                argc > 3: usage
    "2ebc000001a4"  # 2d2  move.l #420,(sp)          mode 644
    "202f0008"      # 2d8  move.l 8(sp),d0
    "e588"          # 2dc  lsl.l  #2,d0
    "206f000c"      # 2de  movea.l 12(sp),a0
    "2f3008fc"      # 2e2  move.l -4(a0,d0.l),-(sp)  name = argv[argc-1]
    "601c"          # 2e6  bra.s  304                on to `begin'
    "41fa02f0"      # 2e8  lea    usage(pc),a0       the usage exit
    "2208"
    "41ee8056"
    "2008"
    "6100041a"      #      bsr    fprintf
    "700b"          #      moveq  #11,d0
    "61000622"      #      bsr    exit
    "4e714e714e71") # 2fe  nop x3

PATCHES = {
    "CMDS/uuencode": [
        # argc <= 1 goes to the usage exit, not to standard input
        (0x280, bytes.fromhex("6c4e"), bytes.fromhex("6c66")),
        (0x2ca, OLD_TAIL, NEW_TAIL),
    ],
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
    assert len(OLD_TAIL) == len(NEW_TAIL) == 0x304 - 0x2ca
    root, apply = argv[0], "--apply" in argv
    for rel, edits in PATCHES.items():
        print(patch(os.path.join(root, rel), edits, apply))


if __name__ == "__main__":
    main(sys.argv[1:])
