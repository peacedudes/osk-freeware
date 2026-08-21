#!/usr/bin/env python3
"""Module-level inventory of the five re-fetched pool categories.

Recurses: the EFFO forum disks are archives of archives, and a single pass
finds 8 modules where there are hundreds. A module's NAME comes from M$Name,
a 4-byte big-endian offset at header 0x0C -- reading it at offset 4 (an
earlier mistake here) yields garbage like " hu" and "d".
"""
import io, os, struct, subprocess, tarfile, zipfile
import paths

POOL = paths.pool()
CATS = ("DRIVERS", "EFFO", "GWINDOWS", "NETWORK", "TELECOM")
OUT = "newstage"
ARCH = (".lzh", ".lha", ".lhz", ".zip", ".tgz", ".tar.gz", ".tar", ".gz", ".z", ".zoo", ".ar")


def sh(c):
    return subprocess.run(c, capture_output=True)


def untar(data, dest):
    with tarfile.open(fileobj=io.BytesIO(data)) as t:
        for m in t.getmembers():
            if m.isdir():
                continue
            p = os.path.join(dest, m.name.lstrip("./").replace("..", "_"))
            os.makedirs(os.path.dirname(p) or dest, exist_ok=True)
            f = t.extractfile(m)
            if f:
                open(p, "wb").write(f.read())


def extract(path, dest):
    low = os.path.basename(path).lower()
    if not low.endswith(ARCH):
        return False
    os.makedirs(dest, exist_ok=True)
    try:
        if low.endswith((".lzh", ".lha", ".lhz")):
            sh(["lha", "xqfw=" + dest, os.path.abspath(path)])
        elif low.endswith(".zip"):
            with zipfile.ZipFile(path) as z:
                z.extractall(dest)
        elif low.endswith(".zoo"):
            sh(["zoo", "xq//", os.path.abspath(path)])
        elif low.endswith(".ar"):
            return False
        elif low.endswith((".tgz", ".tar.gz", ".tar")):
            untar(open(path, "rb").read(), dest)
        else:
            data = sh(["gzip", "-dc", path]).stdout
            if not data:
                return False
            try:
                untar(data, dest)
            except Exception:
                open(os.path.join(dest, low.rsplit(".", 1)[0]), "wb").write(data)
    except Exception:
        return False
    return True


def module_name(d):
    try:
        off = struct.unpack(">I", d[0x0C:0x10])[0]
        if off <= 0 or off >= len(d):
            return ""
        out = []
        for b in d[off:off + 40]:
            c = b & 0x7F
            if c < 0x21 or c > 0x7E:      # 68k names are NUL-terminated,
                break                      # not high-bit terminated as on 6809
            out.append(chr(c))
        return "".join(out)
    except Exception:
        return ""


def main():
    for c in CATS:
        for f in sorted(os.listdir(os.path.join(POOL, c))):
            extract(os.path.join(POOL, c, f), os.path.join(OUT, c, f.replace(".", "_")))
    for _ in range(4):                       # nested archives, to fixpoint
        again = False
        for r, _dirs, fs in os.walk(OUT):
            for f in fs:
                p = os.path.join(r, f)
                d = p + ".x"
                if not os.path.isdir(d) and extract(p, d):
                    again = True
        if not again:
            break
    mods = {}
    for r, _dirs, fs in os.walk(OUT):
        for f in fs:
            p = os.path.join(r, f)
            try:
                d = open(p, "rb").read(4096)
            except OSError:
                continue
            if d[:2] != b"\x4a\xfc":
                continue
            full = open(p, "rb").read()
            typ = full[0x12] if len(full) > 0x12 else 0
            mods.setdefault(module_name(full).lower() or f.lower(), []).append((typ, len(full), p))
    D = "/Users/rdoggett/Developer/os9/osk-freeware/disk"
    have = set()
    for r, _dirs, fs in os.walk(os.path.join(D, "CMDS")):
        have |= {n.lower() for n in fs}
    TYPES = {0x01: "prog", 0x02: "subr", 0x03: "multi", 0x04: "data", 0x0B: "trap",
             0x0C: "system", 0x0D: "filemgr", 0x0E: "driver", 0x0F: "descriptor"}
    absent = {k: v for k, v in mods.items() if k not in have}
    print("modules in the five new categories : %d distinct names" % len(mods))
    print("of those, not already on the disk  : %d" % len(absent))
    print()
    for k in sorted(absent):
        typ, sz, p = sorted(absent[k], key=lambda x: -x[1])[0]
        print("%-14s %-7s %8d  %s" % (k, TYPES.get(typ, "t%d" % typ), sz, p[len(OUT) + 1:][:78]))


main()
