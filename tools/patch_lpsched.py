#!/usr/bin/env python3
"""Send lpsched's job-done mail to the job's owner, not to user 1.

    patch_lpsched.py <disk-dir>            report only
    patch_lpsched.py <disk-dir> --apply    write it

When a job queued with `lp -m' is printed, lpsched looks up whom to tell
with

    getpwuid(queue->jobs[jo].user&&0xffff)       SRC/eff_lp/lpsched.c l.92

-- a logical AND, which is 1 for every user, so the mail went to whoever
has user number 1 (here `uucp', 3.1).  lp.c makes the same lookup with
`getuid()&0xffff', and the getpwuid linked into this binary compares the
USER half of each /dd/SYS/password entry, so `&' is what was meant.

Why a byte patch and not the rebuild: the archive's binary carries a
getpwuid that reads /dd/SYS/password.  This SDK's libraries have none,
and a rebuild links tools/rebuild's USER shim, which answers $USER --
the name of whoever started the DAEMON, not of the job's owner.  So the
shipped binary keeps its own library and loses only the `&&'.

  0xb16  tst.l 0(a0,d0.l) / beq / moveq #1 / bra / moveq #0   (16 bytes)
     -> move.l 0(a0,d0.l),d0 / andi.l #$ffff,d0 / nop x3

The call to getpwuid follows at 0xb26, unchanged.  Module header
untouched; the CRC is recomputed.  Same shape as
tools/patch_elm_linefeed.py.  SRC/eff_lp/lpsched.c carries the same fix.
"""
import os
import sys

PATCHES = {
    "CMDS/lpsched": [
        (0xb16, bytes.fromhex("4ab00800670000087001600000047000"),
                bytes.fromhex("20300800" "02800000ffff" "4e714e714e71")),
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
    root, apply = argv[0], "--apply" in argv
    for rel, edits in PATCHES.items():
        print(patch(os.path.join(root, rel), edits, apply))


if __name__ == "__main__":
    main(sys.argv[1:])
