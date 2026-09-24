#!/usr/bin/env python3
"""Give CMDS/GAMES/mw the module owner 0.0, so an ordinary user can start it.

    patch_mw_owner.py <path-to-mw>            report only
    patch_mw_owner.py <path-to-mw> --apply    write it

mw (Mazewar, TOP release 2) looks up `games' in SYS/password and calls
setuid() to that id -- 90.90 when there is no such entry, as on this disk --
and stops with "Can't setuid, please check File/Moduleowner!" if refused.
F$SUser allows the change for the super-user, for a primary module owned by
0.0, and for a change to the module's own owner.  The shipped module is owned
by 30.95, the id of the machine it was linked on, which matches none of
those, so every user but the super-user was refused (found 2026-09-24 when
the play-tests moved to `tester').

Every file on this disk is owned 0.0, and the message itself asks for the
owner to be checked.  This sets M$Owner ($008) to 0.0 -- the module form of a
set-user-id program -- fixes the header parity word ($02E) and recomputes the
CRC.  No code changes.
"""
import sys

OWNER_AT = 0x08
OLD_OWNER = bytes.fromhex("001e005f")        # 30.95
NEW_OWNER = bytes.fromhex("00000000")        # 0.0
PARITY_AT = 0x2E


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


def parity(d):
    """The word that makes the first 24 header words XOR to $FFFF."""
    acc = 0
    for at in range(0, PARITY_AT, 2):
        acc ^= int.from_bytes(d[at:at + 2], "big")
    return acc ^ 0xFFFF


def check(d, size):
    return (crc24(bytes(d[:size - 3])) == int.from_bytes(d[size - 3:size], "big")
            and parity(d) == int.from_bytes(d[PARITY_AT:PARITY_AT + 2], "big"))


def main(argv):
    path, apply = argv[0], "--apply" in argv
    d = bytearray(open(path, "rb").read())
    size = int.from_bytes(d[4:8], "big")
    if not check(d, size):
        sys.exit("%s: CRC or header parity already bad -- left alone" % path)
    if d[OWNER_AT:OWNER_AT + 4] == NEW_OWNER:
        sys.exit("%s: already owned 0.0" % path)
    if d[OWNER_AT:OWNER_AT + 4] != OLD_OWNER:
        sys.exit("%s: owner is %s, not the expected %s -- a different mw"
                 % (path, d[OWNER_AT:OWNER_AT + 4].hex(), OLD_OWNER.hex()))
    if not apply:
        print("%s: would set M$Owner 30.95 -> 0.0" % path)
        return
    d[OWNER_AT:OWNER_AT + 4] = NEW_OWNER
    d[PARITY_AT:PARITY_AT + 2] = parity(d).to_bytes(2, "big")
    d[size - 3:size] = crc24(bytes(d[:size - 3])).to_bytes(3, "big")
    open(path, "wb").write(d)
    e = bytearray(open(path, "rb").read())
    print("%s: owner 0.0, parity and CRC %s"
          % (path, "ok" if check(e, size) else "VERIFY FAILED"))


if __name__ == "__main__":
    main(sys.argv[1:])
