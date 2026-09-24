#!/usr/bin/env python3
"""Let smail find the sender's name for a user outside group 0.

    patch_smail_uid.py <disk-dir>            report only
    patch_smail_uid.py <disk-dir> --apply    write it

smail signs a letter with the name pwuid(getuid()) finds, and pwuid()
compares getuid() -- OS-9's whole group.user word, 0x00010007 for 1.7 --
against the user number alone: pw.c's pwparse() stores `pwent->pw_uid',
the low half of the port's passwd union (SRC/smail/BNU/SMAIL_2.5/SRC,
HDRS/pwd.h and OSK/pwent.c, which builds the whole word as pw_giduid).
Only the super-user matches, so everyone else's mail goes out `From
nobody', and the uux command it builds says -a'nobody'.  Measured
2026-09-24 as tester and as the super-user, routing through a path file
made by the disk's own pathalias.

  CMDS/UUCP/smail  pwparse(): moveq #0,d0; move.w 10(a0),d0
                             -> move.l 8(a0),d0; nop        (pw_giduid)

With it applied tester's letter is `From: tester@milkyway' and the super
user's is unchanged.  This is the 1993 binary from smail25.lzh.  The
recipe in tools/rebuild is NOT a replacement for it: it links blarslib's
getpwent, which reads a UNIX-style /dd/sys/passwd, where this binary reads
/DD/SYS/Password through the port's own OSK/pwent.c.

Module header untouched; the CRC is recomputed.  Same shape as
tools/patch_uid_mask.py.
"""
import os
import sys

PATCHES = {
    "CMDS/UUCP/smail": [(0x2ca0, bytes.fromhex("70003028000a"),
                         bytes.fromhex("202800084e71"))],
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
