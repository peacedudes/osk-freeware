#!/usr/bin/env python3
"""Fix the off-by-one that crashes CMDS/bash when its memory is above 16 MB.

    tools/patch_bash_version.py disk/CMDS/bash out/bash     # write a patched copy
    tools/patch_bash_version.py disk/CMDS/bash --check      # say which it is

bash 1.12 builds BASH_VERSION with sprintf("%s.%d", dist_version, build)
into a 12-byte stack buffer.  The shipped dist_version is "     1.12", five
leading spaces, so the result "     1.12.12" is twelve characters and its NUL
is the thirteenth byte: it lands on the most significant byte of the saved
A5 above the buffer.  Below 16 MB that byte is already $00 and nothing
happens.  Above it the saved frame pointer loses its top byte, the next
UNLK/RTS jumps into low memory, and the process dies with an illegal
instruction wherever the slide through zeroed memory stops ($465D2 and
$46612 were both seen).  Real 68020 hardware with more than 16 MB would
fault the same way.  Diagnosed by the os9exec session on 2026-09-21.

The patch drops ONE leading space -- "    1.12", NUL-padded to the same
ten bytes -- so BASH_VERSION reads "    1.12.12" and fits, and re-seals
the module CRC.  The header is untouched, so its parity stands.  No source
for this bash is on the disk, so a byte patch is the only way to fix it.

It writes a COPY and never touches its input: replacing the shipped file
is a separate, deliberate step.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rename_module import crc24, parity   # noqa: E402

OLD = b"     1.12\0"
NEW = b"    1.12\0\0"
CRC_BYTES = 3


def sealed(b):
    size = int.from_bytes(b[4:8], "big")
    return (size == len(b) and parity(bytes(b)) == 0xFFFF
            and crc24(bytes(b[:size - CRC_BYTES]))
            == int.from_bytes(b[size - CRC_BYTES:], "big"))


def main(argv):
    if len(argv) != 2:
        sys.exit(__doc__.strip().splitlines()[0])
    src = argv[0]
    b = bytearray(open(src, "rb").read())
    if not sealed(b):
        sys.exit("%s: not a sealed OS-9 module" % src)
    if argv[1] == "--check":
        state = ("patched" if b.count(NEW) == 1 and not b.count(OLD) else
                 "unpatched" if b.count(OLD) == 1 else "not the expected bash")
        print("%s: %s" % (src, state))
        return 0 if state == "patched" else 1
    if b.count(OLD) != 1:
        sys.exit("%s: expected exactly one %r" % (src, OLD))
    at = b.find(OLD)
    b[at:at + len(OLD)] = NEW
    size = len(b)
    b[size - CRC_BYTES:] = crc24(bytes(b[:size - CRC_BYTES])).to_bytes(
        CRC_BYTES, "big")
    if not sealed(b):
        sys.exit("patched copy failed to verify")
    open(argv[1], "wb").write(bytes(b))
    print("%s -> %s: dist_version at $%X, CRC re-sealed" % (src, argv[1], at))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
