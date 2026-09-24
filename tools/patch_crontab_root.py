#!/usr/bin/env python3
"""Stop crontab letting any user act for another with -u.

    patch_crontab_root.py <disk-dir>            report only
    patch_crontab_root.py <disk-dir> --apply    write it

`-u=<user>' lets the super-user list, replace or remove another user's
crontab, and crontab.c (SRC/vcron, line 371) guards it with
`if ((user_id & 0xff00) != ROOT_UID)', where user_id is getuid() --
OS-9's whole group.user word, 0x00010007 for 1.7.  The mask keeps bits of
the USER number, not the group, so every user whose number is below 256
passes as privileged.  Measured 2026-09-24: as tester, `crontab -u=su -l'
is accepted and answers "no crontab for su" where it should refuse with
"must be privileged to use -u".

  CMDS/SYSADMIN/crontab  main(): andi.l #$0000ff00,d0 -> andi.l #$ffff0000,d0

so the test is on the group, which is OS-9's own rule for the super-user.
This is the archive binary; crontab has no recipe here.

Module header untouched; the CRC is recomputed.  Same shape as
tools/patch_uid_mask.py.
"""
import os
import sys

PATCHES = {
    "CMDS/SYSADMIN/crontab": [(0x8d4, bytes.fromhex("02800000ff00"),
                               bytes.fromhex("0280ffff0000"))],
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
