#!/usr/bin/env python3
"""Extract EVERY pool archive and list every OS-9 module inside.

The earlier pass only opened the 101 archives that contributed nothing to the
disk, and classified an archive as "represented" if ANY member matched a
program here. That hid absent programs inside archives which merely happened
to contain one we already had -- gnu.bin.t.gz counted as covered because cat
and ls are here, while cp, mv, rm, mkdir and thirteen others were never looked
at. This pass works at the module level and does not care which archive a
module arrived in.

A module is identified by its 4AFC magic, and its NAME is read from the module
header rather than the filename, because the two disagree often enough to
matter (7 programs on the disk already report a name that is not their file).
"""
import io, os, struct, subprocess, sys, tarfile, zipfile
import paths

POOL = paths.pool()
OUT = "allstage"
LZH = (".lzh", ".lha", ".lhz")


def sh(c):
    return subprocess.run(c, capture_output=True)


def untar(data, dest):
    with tarfile.open(fileobj=io.BytesIO(data)) as t:
        for m in t.getmembers():
            if m.isdir() or m.name.endswith("/"):
                continue
            p = os.path.join(dest, m.name.lstrip("./"))
            os.makedirs(os.path.dirname(p) or dest, exist_ok=True)
            f = t.extractfile(m)
            if f:
                open(p, "wb").write(f.read())


def extract(path, dest):
    low = os.path.basename(path).lower()
    os.makedirs(dest, exist_ok=True)
    try:
        if low.endswith(LZH):
            sh(["lha", "xqfw=" + dest, path])
        elif low.endswith(".zip"):
            with zipfile.ZipFile(path) as z:
                z.extractall(dest)
        elif low.endswith((".tgz", ".tar.gz", ".tar")):
            untar(open(path, "rb").read(), dest)
        elif low.endswith((".gz", ".z")):
            data = sh(["gzip", "-dc", path]).stdout
            try:
                untar(data, dest)
            except Exception:
                open(os.path.join(dest, os.path.basename(low).rsplit(".", 1)[0]), "wb").write(data)
        else:
            return
    except Exception:
        return


def module_name(data):
    """Name from the module header: offset 4 is M$Name, a big-endian offset
    to a high-bit-terminated string."""
    try:
        off = struct.unpack(">H", data[4:6])[0]
        out = []
        for b in data[off:off + 40]:
            out.append(chr(b & 0x7F))
            if b & 0x80:
                break
        return "".join(out)
    except Exception:
        return ""


def main():
    for r, _, fs in os.walk(POOL):
        for f in fs:
            extract(os.path.join(r, f), os.path.join(OUT, f.replace(".", "_")))
    mods = {}
    for r, _, fs in os.walk(OUT):
        for f in fs:
            p = os.path.join(r, f)
            try:
                d = open(p, "rb").read()
            except OSError:
                continue
            if d[:2] != b"\x4a\xfc":
                continue
            mods.setdefault(module_name(d).lower() or f.lower(), []).append((f, len(d), p))
    D = "/Users/rdoggett/Developer/os9/osk-freeware/disk"
    have = set()
    for sub in ("CMDS", "CMDS/GAMES", "CMDS/NETPBM", "CMDS/REBUILT",
                "CMDS/GCC139", "CMDS/GCC2", "CMDS/DEMOS", "CMDS/DHRY"):
        p = os.path.join(D, sub)
        if os.path.isdir(p):
            have |= {n.lower() for n in os.listdir(p) if os.path.isfile(os.path.join(p, n))}
    absent = {k: v for k, v in mods.items() if k not in have and
              not any(os.path.basename(x[0]).lower() in have for x in v)}
    print("modules found in the pool : %d distinct names" % len(mods))
    print("of those, not on the disk : %d" % len(absent))
    print()
    for k in sorted(absent):
        f, sz, p = sorted(absent[k], key=lambda x: -x[1])[0]
        print("%-16s %8d  %s" % (k, sz, p[len(OUT) + 1:]))


main()
