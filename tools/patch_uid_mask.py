#!/usr/bin/env python3
"""Stop two archive binaries from masking getuid() before a whole-word
getpwuid(), so a user outside group 0 finds their own password entry.

    patch_uid_mask.py <disk-dir>            report only
    patch_uid_mask.py <disk-dir> --apply    write them

On OS-9/68000 getuid() returns the whole group.user word (0x00010007 for
1.7).  Each of these programs clears the group half -- `getuid() & 0xffff',
the idiom of Ocker's os9lib, whose getpwuid() compares the user number
only -- and then calls a getpwuid() that compares the WHOLE word.  Only a
group-0 user can match, so the super-user never sees the fault.

  CMDS/logname     chkpw(): and.l #$ffff,d0 -> nop nop nop
                   tester gets `logname: no login name'
  CMDS/ELM/filter  main(): moveq #0,d1; move.w d0,d1 -> move.l d0,d1; nop
                   tester: `Cannot get password entry for this uid!', exit 1

Both measured as tester on a scratch image: logname then answers `tester',
and filter reads /dd/USR/TESTER/.elm/filter_rules as it reads su's.
ELM/fastmail and ELM/newmail carry the same masked call (cuserid/chome at
0x1f78, 0x1fbc and 0x6040, 0x6084) but are NOT patched here: newmail's
lookup fails for the super-user too, so the patch could not be shown to
change anything, and fastmail's result only reaches a delivered header.

Module header untouched; the CRC is recomputed.  Same shape as
tools/patch_elm_uid.py.
"""
import os
import sys

ANDI = bytes.fromhex("02800000ffff")
NOP3 = bytes.fromhex("4e714e714e71")
PATCHES = {
    "CMDS/logname":       [(0xd04, ANDI, NOP3)],
    "CMDS/ELM/filter":    [(0x1148, bytes.fromhex("72003200"), bytes.fromhex("22004e71"))],
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
