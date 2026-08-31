#!/usr/bin/env python3
"""Rename an OS-9/68000 module in place, so its module name matches its file.

OS-9 finds a program by MODULE name once it is resident, whatever path you
typed. Two files with the same module name are therefore one program with two
filenames: `load /dd/CMDS/REBUILT/VI` and then running `/dd/CMDS/vi` gives you
PVIC, not the EFFO editor, and nothing warns you. Measured 2026-08-30.

Renaming the FILE alone does not fix that -- it makes it worse, because the
filenames then promise a distinction the modules do not have. This renames the
module too.

  tools/rename_module.py <file> <newname>            report what would change
  tools/rename_module.py --apply <file> <newname>    do it

Why the name is APPENDED rather than overwritten
------------------------------------------------
The name string sits at $48, in the gap between the program header extension
(M$Exec through M$IRefs, $30..$47) and the first instruction -- padded only to
the next even address. `arc\\0' is four bytes and code starts at $4C. There is
no slack, so a longer name cannot be written where the old one is without
moving every byte of code.

So the new name goes at the END of the module instead, after the M$IRefs
table's four-zero terminator and before the pad byte and CRC, and M$Name is
pointed at it. Nothing already in the module moves: every offset -- M$Exec,
the initialised-data and reference tables, the entry point -- is still valid.
The old name string stays where it was, unreferenced.

M$Size grows by the length of the appended string, which is why this cannot be
done with `fixmod' alone.

What is checked
---------------
CRC and header parity are verified good BEFORE the edit as well as after. A
module whose CRC is already wrong is left alone and reported: patching one
would turn a detectable fault into a silent one.
"""
import struct
import sys

MODULE_MAGIC = b"\x4a\xfc"
HEADER_WORDS = 48          # the universal header, $00..$2F -- what parity covers
M_SIZE = 0x04
M_NAME = 0x0C
CRC_BYTES = 3
NAME_MAX = 29              # an OS-9 name addresses at most 29 characters


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
    """Header parity: the 24 universal-header words XOR to $FFFF."""
    p = 0
    for i in range(0, HEADER_WORDS, 2):
        p ^= int.from_bytes(d[i:i + 2], "big")
    return p


def read_long(d, off):
    return struct.unpack(">I", d[off:off + 4])[0]


def write_long(d, off, value):
    d[off:off + 4] = struct.pack(">I", value)


def module_name(d):
    """The name this module registers itself under, whatever the file is called."""
    off = read_long(d, M_NAME)
    return d[off:d.index(b"\0", off)].decode("latin-1")


def rename(path, newname, apply):
    d = bytearray(open(path, "rb").read())
    if d[:2] != MODULE_MAGIC:
        return f"{path}: not a module (no $4AFC sync word)"
    size = read_long(d, M_SIZE)
    if size > len(d):
        return f"{path}: M$Size {size} exceeds the file ({len(d)})"
    if len(newname) > NAME_MAX:
        return f"{path}: '{newname}' is {len(newname)} characters, over the {NAME_MAX} limit"
    if not newname.isascii() or any(c < " " for c in newname):
        return f"{path}: '{newname}' is not printable ASCII"

    stored = int.from_bytes(d[size - CRC_BYTES:size], "big")
    if crc24(bytes(d[:size - CRC_BYTES])) != stored:
        return f"{path}: CRC ALREADY BAD -- left alone"
    if parity(d) != 0xFFFF:
        return f"{path}: header parity ALREADY BAD -- left alone"

    was = module_name(d)
    if was == newname:
        return f"{path}: already '{newname}'"
    if not apply:
        return f"{path}: '{was}' -> '{newname}', module grows {len(newname) + 1} bytes"

    # Append the name where the CRC used to be. Every module on this disk is an
    # even number of bytes long, CRC included; keep it that way.
    string = newname.encode("latin-1") + b"\0"
    at = size - CRC_BYTES
    if (at + len(string) + CRC_BYTES) % 2:
        string += b"\0"
    body = d[:at] + string
    write_long(body, M_NAME, at)
    write_long(body, M_SIZE, len(body) + CRC_BYTES)
    body[0x2E:0x30] = b"\0\0"
    body[0x2E:0x30] = (parity(body) ^ 0xFFFF).to_bytes(2, "big")
    out = bytes(body) + crc24(bytes(body)).to_bytes(CRC_BYTES, "big")
    open(path, "wb").write(out)

    e = open(path, "rb").read()
    newsize = read_long(bytearray(e), M_SIZE)
    ok = (len(e) == newsize
          and parity(e) == 0xFFFF
          and crc24(e[:newsize - CRC_BYTES]) == int.from_bytes(e[newsize - CRC_BYTES:newsize], "big")
          and module_name(bytearray(e)) == newname)
    return (f"{path}: '{was}' -> '{newname}', {size} -> {newsize} bytes"
            f" {'ok' if ok else 'VERIFY FAILED'}")


def main(argv):
    apply = "--apply" in argv
    rest = [a for a in argv if a != "--apply"]
    if len(rest) != 2:
        sys.exit(__doc__.strip().splitlines()[0])
    line = rename(rest[0], rest[1], apply)
    print("  " + line)
    if not apply:
        print("\n  (dry run -- pass --apply to write)")
    # Anything that is not a completed rename, a clean dry run, or a no-op is a
    # failure. Listing the failures instead would let a new one exit zero.
    return 0 if line.endswith(" ok") or "grows" in line or "already '" in line else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
