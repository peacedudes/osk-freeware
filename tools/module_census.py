#!/usr/bin/env python3
"""What KIND of module is every file under CMDS?

Not everything in a command directory is a command. This disk holds seven trap
libraries, four system modules, two device drivers, three BASIC09 I-code
subroutine modules, two data modules and five shell scripts among its 925
programs -- and running any of those "as a program" is a meaningless test whose
failure means nothing.

That confusion cost real work. `CMDS/GAMES/graph` was catalogued as "Atari
graphics demonstration" for as long as the catalogue existed. It is a type-$0B
trap handler: the `Graph' library that g, striche, apfel, sine, showpic,
graphdemo and graphsave all link against. And `bio` and `blackjack` were
recorded as failing with an illegal instruction; both are BASIC09 I-code, which
no amount of cio will run -- they need Microware's `runb`.

Header fields read (OS-9/68000, base header $30 bytes, exec extension after):

    $00  M$ID     $4AFC
    $04  M$Size   module length -- a FILE longer than this holds more modules
    $0C  M$Name   offset to a NUL-terminated name (68k; not 6809 high-bit)
    $12  M$Type   $01 prog  $02 subr  $03 multi  $04 data  $0B trap
                  $0C system  $0D filemgr  $0E driver  $0F descriptor
    $13  M$Lang   $01 68k code  $02 BASIC09 I-code

Usage:  tools/module_census.py [<disk-dir>] [--all]
        --all also lists the 68k programs, one line each.
Exit:   0 always -- this reports, it does not judge.
"""
import os, sys, collections

TYPE = {0x01: "prog", 0x02: "subr", 0x03: "multi", 0x04: "data", 0x0b: "trap",
        0x0c: "system", 0x0d: "filemgr", 0x0e: "driver", 0x0f: "descriptor"}
LANG = {0x00: "data", 0x01: "68k", 0x02: "basic09-icode", 0x03: "pascal",
        0x04: "c", 0x05: "cobol", 0x06: "fortran"}


def read_module(path):
    """(name, type, lang, declared size, file size) -- name None if not a module."""
    with open(path, "rb") as f:
        head = f.read(0x50)
    size = os.path.getsize(path)
    if head[:2] != b"\x4a\xfc":
        return None, "not-a-module", "-", 0, size
    at = int.from_bytes(head[0x0c:0x10], "big")
    with open(path, "rb") as f:
        f.seek(at)
        name = f.read(64).split(b"\0")[0].decode("latin1", "replace")
    return (name,
            TYPE.get(head[0x12], "type%02x" % head[0x12]),
            LANG.get(head[0x13], "lang%02x" % head[0x13]),
            int.from_bytes(head[0x04:0x08], "big"),
            size)


def modules_in(path):
    """Every module in a file, as (name, type byte, size).

    A file may hold a module GROUP: `cyberwar` is four modules -- two programs
    and two window descriptors -- and `blackjack` is three BASIC09 I-code
    subroutines. Reading only the first header calls the first one the file.
    """
    data = open(path, "rb").read()
    found, at = [], 0
    while at < len(data) - 8:
        i = data.find(b"\x4a\xfc", at)
        if i < 0:
            break
        size = int.from_bytes(data[i + 4:i + 8], "big")
        if not 0 < size <= len(data) - i:
            at = i + 2
            continue
        off = i + int.from_bytes(data[i + 0x0c:i + 0x10], "big")
        name = data[off:off + 64].split(b"\0")[0].decode("latin1", "replace")
        found.append((name, data[i + 0x12], size))
        at = i + size
    return found


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = os.path.join(args[0] if args else "disk", "CMDS")
    show_all = "--all" in sys.argv

    rows = []
    for here, _dirs, files in os.walk(root):
        if os.path.basename(here) == "archives":
            continue
        for f in sorted(files):
            name, kind, lang, declared, actual = read_module(os.path.join(here, f))
            rows.append((os.path.relpath(here, os.path.dirname(root)), f,
                         name, kind, lang, declared, actual))

    print("%d files under %s" % (len(rows), root))
    for (kind, lang), n in sorted(collections.Counter((r[3], r[4]) for r in rows).items(),
                                  key=lambda kv: -kv[1]):
        print("   %-14s %-14s %d" % (kind, lang, n))

    odd = [r for r in rows if (r[3], r[4]) != ("prog", "68k")]
    print("\nnot a 68k program -- %d files.  Running these as programs proves nothing:" % len(odd))
    for d, f, name, kind, lang, _dec, _act in odd:
        print("   %-18s %-14s %-14s %-14s %s" % (f, d, kind, lang, "" if name == f else "module name: %s" % name))

    mism = [r for r in rows if r[2] and r[2] != r[1]]
    print("\nfilename does not match the module name inside -- %d files:" % len(mism))
    for d, f, name, _k, _l, _dec, _act in mism:
        print("   %-18s %-14s reports itself as %s" % (f, d, name))

    # A file bigger than its first module usually just has trailing padding --
    # seven of the Atari GRAPH programs are 2 to 34 bytes long that way.  Only
    # a second $4AFC header makes it a group, so count headers, not bytes.
    groups = []
    for d, f, name, _k, _l, _dec, _act in rows:
        if not name:
            continue
        mods = modules_in(os.path.join(os.path.dirname(root), d, f))
        if len(mods) > 1:
            groups.append((d, f, mods))
    print("\nmodule GROUPS -- %d files hold more than one module.  OS-9 loads the whole" % len(groups))
    print("group and keeps it resident until the combined link count is zero, so the extra")
    print("modules are not junk; a type-$04 `_win' companion is a window descriptor:")
    for d, f, mods in groups:
        print("   %-18s %-14s %s" % (f, d, ", ".join(
            "%s (%s)" % (n, TYPE.get(ty, "type%02x" % ty)) for n, ty, _s in mods)))

    if show_all:
        print("\n68k programs:")
        for d, f, name, kind, lang, _dec, _act in rows:
            if (kind, lang) == ("prog", "68k"):
                print("   %-18s %s" % (f, d))


main()
