#!/usr/bin/env python3
"""Let fuddle draw its board at an ANSI (vt100, xterm) terminal.

    patch_fuddle.py <disk-dir>            report only
    patch_fuddle.py <disk-dir> --apply    write it

fuddle has no source anywhere (DOC/ORIGINS: chess.ar, whose SRC/chess
trees are four other chess programs).  It was built for a TeleVideo /
ADM-3A terminal and keeps that terminal's codes as five strings and one
cursor routine, found by disassembly (m68k-elf-objdump):

  0x278  lea home(pc)    "\\036"          the home key code
  0x280  lea clear(pc)   "\\032"          clear screen (and home)
  0x288  lea clreol(pc)  "\\033T"         clear to end of line
  0x290  lea cm(pc)      "\\033="         cursor address prefix
  0x2df6 the cursor routine: sprintf(buf, "%s%c%c", cm, row+32, col+32)
         -- two `addi.l #32' at 0x2e04 and 0x2e0e, the format at 0x2f8d
         reached by `lea' at 0x2e1a
  IData  six pointers to the pieces drawn in reverse, "\\033G4K\\033G0"...

At an ANSI terminal none of it is understood and the board lands in the
wrong places.  The patch gives each the ANSI equivalent:

  cm      "\\033=" -> "\\033["          in place, one byte
  addi    #32 -> #1                     rows and columns count from 1
  format  "%s%c%c" -> "%s%d;%dH"        ESC [ row ; col H
  home    "\\033[H", clear "\\033[H\\033[2J", clreol "\\033[K"
  pieces  "\\033[7mK\\033[m" and the rest: reverse video

The longer strings do not fit where the old ones sit, so they are
appended to the module after its IRefs table, before the CRC, and the
four `lea' displacements and six IData pointers are pointed at them.
M$Size, the header parity and the CRC are recomputed.  Checked: every
byte this changes is compared with the expected original first.
"""
import os
import sys

REL = "CMDS/GAMES/fuddle"
SIZE = 18238                       # the binary this was written against

# (offset, old, new) -- changed in place
INPLACE = [
    (0x0664, b"=", b"["),                                  # cm "\033=" -> "\033["
    (0x2e04, bytes.fromhex("068000000020"), bytes.fromhex("068000000001")),
    (0x2e0e, bytes.fromhex("068000000020"), bytes.fromhex("068000000001")),
]

# strings appended; name -> bytes (NUL-terminated)
NEW = [
    ("home",   b"\x1b[H\0"),
    ("clear",  b"\x1b[H\x1b[2J\0"),
    ("clreol", b"\x1b[K\0"),
    ("fmt",    b"%s%d;%dH\0"),
] + [("piece" + p, b"\x1b[7m" + p.encode() + b"\x1b[m\0") for p in "KQRBNP"]

# lea d16(pc),a0 at these offsets: (instruction, old target, new string)
LEAS = [(0x0278, 0x065c, "home"), (0x0280, 0x065e, "clear"),
        (0x0288, 0x0660, "clreol"), (0x2e1a, 0x2f8d, "fmt")]

# IData longs holding code offsets of the reverse-video pieces
PIECES = [(0x0ac6, "pieceK"), (0x0ace, "pieceQ"), (0x0ad6, "pieceR"),
          (0x0ade, "pieceB"), (0x0ae6, "pieceN"), (0x0aee, "pieceP")]


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
    acc = 0
    for i in range(0, 0x2e, 2):
        acc ^= int.from_bytes(d[i:i + 2], "big")
    return acc ^ 0xFFFF


def patch(path, apply):
    d = bytearray(open(path, "rb").read())
    size = int.from_bytes(d[4:8], "big")
    if crc24(bytes(d[:size - 3])) != int.from_bytes(d[size - 3:size], "big"):
        return "%s: CRC already bad -- left alone" % path
    if size != SIZE:
        return ("%s: %d bytes, not %d -- already patched, or a different "
                "binary" % (path, size, SIZE))
    for at, old, new in INPLACE:
        if d[at:at + len(old)] != old:
            return "%s: bytes at 0x%x are %s, not %s" % (
                path, at, d[at:at + len(old)].hex(), old.hex())
    for at, target, _ in LEAS:
        disp = int.from_bytes(d[at + 2:at + 4], "big", signed=True)
        if d[at:at + 2] != b"\x41\xfa" or at + 2 + disp != target:
            return "%s: no lea to 0x%x at 0x%x" % (path, target, at)
    idata = int.from_bytes(d[0x40:0x44], "big")
    irefs = int.from_bytes(d[0x44:0x48], "big")
    slots = {}
    for target, name in PIECES:
        want = target.to_bytes(4, "big")
        at = d.find(want, idata, irefs)
        if at < 0 or d.find(want, at + 1, irefs) >= 0:
            return "%s: piece pointer 0x%x not found once in IData" % (path, target)
        slots[name] = at
    if not apply:
        return "%s: would patch" % path

    body, place = bytearray(), {}
    for name, text in NEW:
        place[name] = size - 3 + len(body)
        body += text
    if len(body) & 1:
        body += b"\0"
    for at, old, new in INPLACE:
        d[at:at + len(new)] = new
    for at, _, name in LEAS:
        d[at + 2:at + 4] = (place[name] - (at + 2)).to_bytes(2, "big", signed=True)
    for name, at in slots.items():
        d[at:at + 4] = place[name].to_bytes(4, "big")
    d = d[:size - 3] + body + b"\0\0\0"
    size = len(d)
    d[4:8] = size.to_bytes(4, "big")
    d[0x2e:0x30] = parity(d).to_bytes(2, "big")
    d[size - 3:size] = crc24(bytes(d[:size - 3])).to_bytes(3, "big")
    open(path, "wb").write(d)
    e = open(path, "rb").read()
    ok = crc24(e[:size - 3]) == int.from_bytes(e[size - 3:size], "big")
    return "%s: patched to %d bytes, CRC %s" % (path, size, "ok" if ok else "VERIFY FAILED")


def main(argv):
    root, apply = argv[0], "--apply" in argv
    print(patch(os.path.join(root, REL), apply))


if __name__ == "__main__":
    main(sys.argv[1:])
