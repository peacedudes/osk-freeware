#!/usr/bin/env python3
"""Stop head reporting every file it read as an error.

    patch_head_close.py <disk-dir>            report only
    patch_head_close.py <disk-dir> --apply    write it

GNU textutils 1.0 head, no source on the disk.  After it copies the lines
head_file() does `if (close (fd) != 0) { error (0, errno, "%s", file);
return 1; }', and this build's close() returns the PATH NUMBER on success:
its I$Close stub branches to the library's shared exit that keeps d0 (the
one open() rightly uses) instead of the one four bytes on that clears it.
So `head -n 2 file' printed its two lines, then `/dd/CMDS/head: file' on
stderr, and exited 1 -- measured 2026-09-26; from standard input it was
clean, because that path is never closed.  The seven other GNU utilities
here share the stub (split expand join sort tac sum unexpand) and test
close() in ways a positive return passes; each measured rc 0, no message.

  CMDS/head  0x4ce4: bra.w disp $0458 -> $0462 (to `bcs err; moveq #0,d0')

One byte.  Module header untouched; the CRC is recomputed.  Same shape as
tools/patch_elm_linefeed.py.
"""
import os
import sys

# close(): link; movem; trap #0 I$Close; bra.w <exit>
PATCHES = {
    "CMDS/head": [(0x4cd6, bytes.fromhex("4e55000048e760804e40008f60000458"),
                   bytes.fromhex("4e55000048e760804e40008f60000462"))],
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
