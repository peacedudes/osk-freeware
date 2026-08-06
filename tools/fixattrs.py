#!/usr/bin/env python3
"""Set directory attributes in a finished RBF image.

    tools/fixattrs.py osk-freeware.dd

A DIRECTORY HAS TO BE WRITABLE or nothing can create a file in it. advent
writes `glorkz` into GAMES/ADV, larn writes its scoreboard, and 35 programs
use /dd/tmp. This is not about who you log in as: with no `w` bit, not even
0.0 can write there.

The old build got this for free -- `makdir` leaves a directory `d-ewrewr` --
but the tar build cannot. The collection's `tar` IGNORES the mode bits on a
directory entry and applies its own, so the archive has no say: setting
MODE_DIR to 0777 in mktar.py changes nothing in the image. Verified by
building it both ways and comparing.

Files are already right and are left alone: tar does honour the mode on a
regular file, giving modules `--e-re-r` and data `----r--r`.

The attribute byte, high bit first: d s pe pw pr e w r. A directory with
everything a directory needs is 0xBF, which is exactly what os9exec's own
BuildBlankImage writes for the root.
"""
import os, sys

DIR_ATTR   = 0xBF          # d + pe pw pr + e w r
ENTRY_SIZE = 32            # 29 bytes of name, then a 3-byte LSN
SEG_BASE   = 0x10          # first segment descriptor in an FD
SEG_COUNT  = 48


def word(b, off, n):
    return int.from_bytes(b[off:off+n], "big")


class Image:
    def __init__(self, path):
        self.f = open(path, "r+b")
        sec0 = self.read_sector(0, 256)
        self.sect = word(sec0, 0x68, 2) or 256
        sec0 = self.read_sector(0, self.sect)
        self.root = word(sec0, 0x08, 3)          # DD.DIR: root directory FD

    def read_sector(self, lsn, size=None):
        size = size or self.sect
        self.f.seek(lsn * size)
        return self.f.read(size)

    def segments(self, fd):
        """The (lsn, count) runs that make up a file, from its FD."""
        out = []
        for i in range(SEG_COUNT):
            off = SEG_BASE + i * 5
            lsn, num = word(fd, off, 3), word(fd, off + 3, 2)
            if not num:
                break
            out.append((lsn, num))
        return out

    def entries(self, fd_lsn):
        """Yield (name, child_fd_lsn) for a directory whose FD is at fd_lsn."""
        fd = self.read_sector(fd_lsn)
        for start, count in self.segments(fd):
            for s in range(start, start + count):
                data = self.read_sector(s)
                for i in range(0, len(data), ENTRY_SIZE):
                    e = data[i:i+ENTRY_SIZE]
                    if len(e) < ENTRY_SIZE or e[0] in (0x00, 0x2E):
                        continue                  # unused, or "." / ".."
                    name = bytearray()
                    for b in e[:29]:
                        if b == 0:
                            break
                        name.append(b & 0x7F)
                        if b & 0x80:
                            break
                    child = word(e, 29, 3)
                    if child:
                        yield name.decode("latin-1"), child

    def set_attr(self, fd_lsn, value):
        self.f.seek(fd_lsn * self.sect)
        cur = self.f.read(1)[0]
        if cur == value:
            return False
        self.f.seek(fd_lsn * self.sect)
        self.f.write(bytes([value]))
        return True


def walk(img, fd_lsn, seen, changed, depth=0):
    if fd_lsn in seen or depth > 24:
        return
    seen.add(fd_lsn)
    for name, child in img.entries(fd_lsn):
        fd = img.read_sector(child)
        if fd[0] & 0x80:                          # it is a directory
            if img.set_attr(child, DIR_ATTR):
                changed.append(name)
            walk(img, child, seen, changed, depth + 1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: fixattrs.py <image.dd>")
    img = Image(sys.argv[1])
    changed, seen = [], set()
    if img.set_attr(img.root, DIR_ATTR):
        changed.append("(root)")
    walk(img, img.root, seen, changed)
    img.f.close()
    print("  made %d director%s writable" % (len(changed), "y" if len(changed) == 1 else "ies"))
