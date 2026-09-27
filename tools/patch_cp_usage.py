#!/usr/bin/env python3
"""Make cp stop after its usage message instead of running on into a bus error.

    patch_cp_usage.py <disk-dir>            report only
    patch_cp_usage.py <disk-dir> --apply    write it

carlutil cp, no source.  main() does `if (argc < 2) usage();' and then
carries on to open argv[argc-1] -- so a bare `cp' printed the usage and
died with a bus error in I$Open (vector $02, E_BUSERR, measured
2026-09-26), and `cp file' printed it and then `cp is not directory'.
usage() is called from one other place, the `-?' option, which printed
it and then `bad option ?'.  Both want the same thing: stop.

  CMDS/cp  0x6c6, usage()'s epilogue `addq #4,sp; movem; rts' ->
           `moveq #1,d0; bsr.w exit; nop' -- the library exit() at $FA4,
           the one main's own return reaches, so stdio is flushed.

Eight bytes, same length.  Module header untouched; the CRC is
recomputed.  Same shape as tools/patch_elm_linefeed.py.
"""
import os
import sys

PATCHES = {
    "CMDS/cp": [(0x6c6, bytes.fromhex("588f4cdf01024e75"),
                 bytes.fromhex("7001" "610008da" "4e71"))],
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
