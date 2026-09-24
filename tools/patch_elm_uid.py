#!/usr/bin/env python3
"""Patch CMDS/ELM/elm so a user other than the super-user has a password entry.

    patch_elm_uid.py <path-to-elm>            report only
    patch_elm_uid.py <path-to-elm> --apply    write it

elm's init.c (OSK branch) accepts the LOGNAME/USER entry only if
`pass->pw_uid == getuid()'.  On OS-9 getuid() is the 32-bit group.user word
(0x00010007 for tester, 1.7) while pw_uid is the 16-bit USER half of the
entry's giduid (7), so the test fails for everyone but 0.0.  The fallback,
getpwuid(getuid()), then scans on from the line after the LOGNAME entry
without rewinding, finds nothing, and elm stops with "You have no password
entry!".  The super-user escaped only because `os9' (0.0) sits after
`tester' in SYS/password.

At 0x18738 the compare loads the half-word:
    7200 3228 000a    moveq #0,d1 ; move.w 10(a0),d1
and becomes the whole group.user long, which is what getuid() returns:
    2228 0008 4e71    move.l 8(a0),d1 ; nop
Then header parity is unchanged (the header is not touched) and the CRC is
recomputed.
"""
import sys

AT = 0x18738
OLD = bytes.fromhex("72003228000a")
NEW = bytes.fromhex("222800084e71")


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


def main(argv):
    path, apply = argv[0], "--apply" in argv
    d = bytearray(open(path, "rb").read())
    size = int.from_bytes(d[4:8], "big")
    if crc24(bytes(d[:size - 3])) != int.from_bytes(d[size - 3:size], "big"):
        sys.exit("%s: CRC already bad -- left alone" % path)
    if d[AT:AT + 6] == NEW:
        sys.exit("%s: already patched" % path)
    if d[AT:AT + 6] != OLD:
        sys.exit("%s: bytes at 0x%x are %s, not the expected %s -- a different elm"
                 % (path, AT, d[AT:AT + 6].hex(), OLD.hex()))
    if not apply:
        print("%s: would patch 0x%x %s -> %s" % (path, AT, OLD.hex(), NEW.hex()))
        return
    d[AT:AT + 6] = NEW
    d[size - 3:size] = crc24(bytes(d[:size - 3])).to_bytes(3, "big")
    open(path, "wb").write(d)
    e = open(path, "rb").read()
    ok = crc24(e[:size - 3]) == int.from_bytes(e[size - 3:size], "big")
    print("%s: patched, CRC %s" % (path, "ok" if ok else "VERIFY FAILED"))


if __name__ == "__main__":
    main(sys.argv[1:])
