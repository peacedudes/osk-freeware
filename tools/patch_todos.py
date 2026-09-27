#!/usr/bin/env python3
"""Make todos and toos9 put the converted file in place, and stop adding a byte.

    patch_todos.py <disk-dir>            report only
    patch_todos.py <disk-dir> --apply    write them

DESIGNA VLT's UTIL 2.80, no source anywhere.  Both write the converted
text to `<prog>.$$$.<n>' and then hand `del <file>' and `rename <tmp>
<file>' to system(), which forks $SHELL.  Under the disk's SYS/login that
is ksh, and ksh reads `$$' as its own process id: measured 2026-09-26,
`rename todos.${$}$.3 n.txt' -> `can't open "todos.4$.3"' -- and the del
had already run, so the ORIGINAL WAS GONE and the text sat under a name
nobody typed.  Microware's own shell leaves `$' alone, which is why it
worked where it was written.

  1. both   the temp-name template `.$$$' -> `.___'  (three bytes, same
            length; nothing else reads the name)

  2. toos9  `c = getc(in)' lands in an unsigned char, and the EOF test is
            `cmpi.w #-1' against it zero-extended -- never true, so the
            $FF of EOF was written as the file's last byte.
            cmpi.w #$FFFF,d0 -> cmpi.w #$00FF,d0 (one byte).  A real $FF
            in a DOS text file is dropped with it; CP437 gives it a
            non-breaking space, and OS-9 text has no use for one.

  3. todos  do { fgets; fputs; fputs("\\n"); } while (!feof(in)) -- the
            failing fgets at EOF still earns a line feed, one stray LF at
            the end of every file.  The loop is rewritten in place to test
            fgets' return and leave, with the feof test at the foot
            replaced by a branch back: the four bytes `tst.l d0; beq' go
            in after the fgets, the 50 bytes of body move down four, and
            their three bsr and one lea displacements drop by four.
            Same length overall (three nops pad the end).

Module header untouched; the CRC is recomputed.  Same shape as
tools/patch_elm_linefeed.py.
"""
import os
import sys

# todos: the loop at $3AA..$3FD as shipped.
TODOS_LOOP_OLD = bytes.fromhex(
    "2f2f02e8223c0000019041ef0106200861000340588f"      # fgets(buf,400,in)
    "222f02e441ef0102200861000354"                      # fputs(buf,out)
    "4878000a41fa0235220841ef0106200861000334588f"      # sprintf(buf,"%c",10)
    "222f02e441ef0102200861000330"                      # fputs(buf,out)
    "206f02e808280004000d67ac")                         # while (!feof(in))


def todos_loop_new():
    """The same loop with `if (!fgets(...)) break;' and no feof test."""
    head = TODOS_LOOP_OLD[:0x16]                        # up to addq #4,sp
    body = bytearray(TODOS_LOOP_OLD[0x16:0x48])         # $3C0..$3F1
    # pc-relative operands inside the body, as offsets into it: each
    # moves down four bytes, so each displacement shrinks by four.
    for at in (0x0c, 0x14, 0x20, 0x30):                 # bsr, lea, bsr, bsr
        disp = int.from_bytes(body[at:at + 2], "big") - 4
        body[at:at + 2] = disp.to_bytes(2, "big")
    return (head
            + bytes.fromhex("4a80")                     # tst.l d0
            + bytes.fromhex("673a")                     # beq.s $3FE (exit)
            + bytes(body)                               # now $3C4..$3F5
            + bytes.fromhex("60b2")                     # bra.s $3AA
            + bytes.fromhex("4e714e714e71"))            # nop x3 to $3FE


PATCHES = {
    "CMDS/todos": [(0x5af, b"$$$", b"___"),
                   (0x3aa, TODOS_LOOP_OLD, todos_loop_new())],
    "CMDS/toos9": [(0x778, b"$$$", b"___"),
                   (0x468, bytes.fromhex("0c40ffff"),
                    bytes.fromhex("0c4000ff"))],
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
        if len(old) != len(new):
            return "%s: patch at 0x%x changes length -- refused" % (path, at)
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
