#!/usr/bin/env python3
"""Blank the SDK author stamp out of a finished module, and fix its CRC.

`cc` links Microware's `cstart.r` into every C program, and that cstart has a
64-byte Author psect. Whoever owns the SDK copy gets their name written into
every binary built through it. `tools/rebuild/` avoids this by building against
an overlay whose cstart has the psect overwritten with spaces BEFORE linking --
but that only helps a program you can rebuild.

Fifteen modules on this disk carry the stamp because they cannot be rebuilt:
seven have no source anywhere, and four have source that will not build here
(`pdraw` wants popen, `wam.sbprolog` wants netdb.h, `ls` is a gcc2 build,
`pep` wants a hardware routine that is not on the disk).

This does the same edit AFTER the fact. The psect is DATA, not code, and the
replacement is the same length, so nothing in the module moves -- no offset,
no relocation, no entry point. Only the CRC changes, and that is recomputed.

  tools/blank_author.py <module>...        report what would change
  tools/blank_author.py --apply <module>...  do it

The CRC and header parity are verified good BEFORE the edit as well as after.
A module whose CRC is already wrong is left alone and reported: patching one
would turn a detectable fault into a silent one.
"""
import re
import sys

STAMP = re.compile(rb">{4,}from the disk of[^<]*<{4,}")


def crc24(data):
    """OS-9 module CRC: polynomial $800063, complemented."""
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
    """Header parity: the 24 header words XOR to $FFFF."""
    p = 0
    for i in range(0, 48, 2):
        p ^= int.from_bytes(d[i:i + 2], "big")
    return p


def process(path, apply):
    d = bytearray(open(path, "rb").read())
    if d[:2] != b"\x4a\xfc":
        return f"{path}: not a module (no $4AFC sync word)"
    size = int.from_bytes(d[4:8], "big")
    if size > len(d):
        return f"{path}: M$Size {size} exceeds the file ({len(d)})"

    stored = int.from_bytes(d[size - 3:size], "big")
    if crc24(bytes(d[:size - 3])) != stored:
        return f"{path}: CRC ALREADY BAD -- left alone"
    if parity(d) != 0xFFFF:
        return f"{path}: header parity ALREADY BAD -- left alone"

    m = STAMP.search(d)
    if not m:
        return f"{path}: no stamp"

    if not apply:
        return f"{path}: stamp at {m.start():#x}, {m.end()-m.start()} bytes"

    # Same length, so every offset in the module stays exactly where it was.
    d[m.start():m.end()] = b" " * (m.end() - m.start())
    new = crc24(bytes(d[:size - 3]))
    d[size - 3:size] = new.to_bytes(3, "big")
    open(path, "wb").write(bytes(d))

    e = open(path, "rb").read()
    ok = (crc24(e[:size - 3]) == int.from_bytes(e[size - 3:size], "big")
          and parity(e) == 0xFFFF and len(e) == len(d))
    return (f"{path}: blanked {m.end()-m.start()} bytes, CRC ${new:06X}"
            f" {'ok' if ok else 'VERIFY FAILED'}")


def main(argv):
    apply = "--apply" in argv
    files = [a for a in argv if a != "--apply"]
    if not files:
        sys.exit(__doc__.strip().splitlines()[0])
    bad = 0
    for f in files:
        line = process(f, apply)
        print("  " + line)
        if "FAILED" in line or "ALREADY BAD" in line:
            bad += 1
    if not apply:
        print("\n  (dry run -- pass --apply to write)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
