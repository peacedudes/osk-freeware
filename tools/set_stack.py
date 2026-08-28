#!/usr/bin/env python3
"""Raise a module's M$Stack, in place, and recompute its CRC.

    tools/set_stack.py <bytes> <module> [<module> ...]      # apply
    tools/set_stack.py --check <module> [...]               # report only

Why this exists
---------------
Nine of the 169 netpbm programs died with `**** Stack Overflow ****' before
doing anything. They all ship with the SAME `M$Stack' of 3072 -- every netpbm
module on the disk does -- so this is not a damaged header, it is a handful of
programs that legitimately want more stack than their siblings and were built
in one batch that gave them all the same.

There is no source-level fix to make here and no rebuild needed: the stack
request is a field in the module header. Raising it is the same kind of
in-place repair as the one-byte `dir' MOVEQ fix recorded in DOC/STATUS.

MEASURED 2026-08-27, at 64k. 16k is NOT enough for ppmtoxpm and was tried
first. Five programs go from broken to working; four that were fed a format
they do not read stop crashing and print their own diagnostic instead:

    ppmnorm      now remaps and writes a valid PPM
    pnmtosir     now writes SIR, and sirtopnm reads it back
    ppmtoxpm     now writes XPM, and xpmtoppm reads it back
    xpmtoppm     "
    pbmtext      `pbmtext hello' now renders 51 by 29
    fstopgm      "invalid header" instead of a crash
    hipstopgm    "error reading header"
    imgtoppm     exits quietly
    xvminitoppm  "bad magic number - not a XV thumbnail picture"

What is safe about this
-----------------------
`M$Stack' sits at offset $3C, which is PAST the 48-byte header, so header
parity -- the 24 header words XOR to $FFFF -- is not affected and is asserted
unchanged either side of the edit. Only the module CRC has to be recomputed.
Nothing moves, so the module keeps its size and every other offset in it.

This refuses to touch a module whose CRC or parity is already bad, because
then the edit would be hiding damage rather than repairing a field.
"""
import struct
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from blank_author import crc24, parity                     # noqa: E402

M_STACK = 0x3C


def look(path):
    d = bytearray(open(path, "rb").read())
    if d[:2] != b"\x4a\xfc":
        return None, "not a module (no $4AFC sync word)"
    size = int.from_bytes(d[4:8], "big")
    if size > len(d):
        return None, "M$Size %d exceeds the file (%d)" % (size, len(d))
    if crc24(bytes(d[:size - 3])) != int.from_bytes(d[size - 3:size], "big"):
        return None, "CRC ALREADY BAD -- left alone"
    if parity(d) != 0xFFFF:
        return None, "header parity ALREADY BAD -- left alone"
    return d, size


def main(argv):
    if len(argv) >= 1 and argv[0] == "--check":
        for p in argv[1:]:
            d, size = look(p)
            print("%-44s %s" % (p, size if d is None else
                                "M$Stack %d" % int.from_bytes(
                                    d[M_STACK:M_STACK + 4], "big")))
        return 0
    if len(argv) < 2:
        sys.exit(__doc__)
    want = int(argv[0], 0)
    bad = 0
    for p in argv[1:]:
        d, size = look(p)
        if d is None:
            print("%-44s SKIPPED: %s" % (p, size))
            bad += 1
            continue
        was = int.from_bytes(d[M_STACK:M_STACK + 4], "big")
        if was >= want:
            print("%-44s already %d, left alone" % (p, was))
            continue
        d[M_STACK:M_STACK + 4] = struct.pack(">I", want)
        # The whole safety argument in one line: the edit is past the header.
        assert parity(d) == 0xFFFF, "%s: parity moved -- it must not" % p
        d[size - 3:size] = crc24(bytes(d[:size - 3])).to_bytes(3, "big")
        assert crc24(bytes(d[:size - 3])) == int.from_bytes(
            d[size - 3:size], "big")
        open(p, "wb").write(d)
        print("%-44s M$Stack %d -> %d, CRC recomputed" % (p, was, want))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
