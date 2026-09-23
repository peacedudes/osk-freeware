#!/usr/bin/env python3
"""List what is inside a pool archive, using the collection's own tools.

    tools/list_archive.py <archive> [<archive> ...]
    tools/list_archive.py --names <archive> ...     one member name per line

WHY.  The pool still holds archives nobody has looked into, and the survey of
2026-09-22 could only judge 236 of them by their FILENAME, because the host
has no unpacker for a Zoo, an Arc or an OS-9 `ar'.  A verdict from a filename
is a guess.

IN UNIVERSE FIRST.  rdoggett, 2026-09-22: "you tried these archives in
universe?  That's where they were probably made."  They were: these are
OS-9 archives, and the disk ships the tools that read them -- `zoo', `arc',
`lharc', `unzip', `ar2', `booz'.  So the listing is done by running those
under os9exec with the archives on /h6, all of them in ONE session, which is
both faithful and quick.  Host readers for Zoo and Arc are kept below as a
fallback for a machine with no image built yet.  They were written first,
and they agree on sizes but NOT always on names: Zoo keeps a long name in
the entry's varying part, so the host reader shows `grafikde.c' where the
disk's `zoo' shows `grafikdemo.c'.  Another reason to ask the disk.

`.tar', `.tar.Z' and `.tar.gz' go to the host's tar: nothing about them is
OS-9's, and the disk's own tar would want them uncompressed first anyway.
"""
import os
import re
import struct
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
ZOO_MAGIC = 0xFDC4A7DC

# What the disk uses to list each kind.  `ar2' is Carl Kreider's Ar V2.00,
# which reads the V1.2 archives `ar' writes as well as its own.
IN_UNIVERSE = {".zoo": "zoo l", ".arc": "arc l", ".ar": "ar2 -t",
               ".lzh": "lharc l", ".lha": "lharc l", ".zip": "unzip -l"}
NOISE = re.compile(r"^(Archive|Name|Length|=====|-----|Total|Filename|\s*$|"
                   r"#|.*rc=\d|\s*\d+ files?)", re.I)


def image_and_exec():
    image = os.path.join(REPO, "osk-freeware.dd")
    exe = os.environ.get("OS9EXEC", os.path.join(REPO, "..", "os9exec", "os9exec"))
    return (image, exe) if os.path.isfile(image) and os.path.isfile(exe) else (None, None)


def in_universe(paths):
    """Run the disk's own lister over each archive, in one emulator session.

    Returns {path: [lines]} for the ones it could handle, or {} with no image.
    """
    image, exe = image_and_exec()
    if not image:
        return {}
    todo = [p for p in paths
            if os.path.splitext(p.lower())[1] in IN_UNIVERSE]
    if not todo:
        return {}
    sys.path.insert(0, HERE)
    from os9env import emulator_env
    out = {}
    with tempfile.TemporaryDirectory() as h6:
        script = ["PATH=/dd/CMDS", "export PATH"]
        for i, p in enumerate(todo):
            name = "a%02d%s" % (i, os.path.splitext(p.lower())[1])
            open(os.path.join(h6, name), "wb").write(open(p, "rb").read())
            script.append('echo "@@%d@@"' % i)
            script.append("%s /h6/%s" % (IN_UNIVERSE[os.path.splitext(p.lower())[1]], name))
        script.append('echo "@@end@@"')
        open(os.path.join(h6, "l.sh"), "wb").write(
            ("\r".join(script) + "\r").encode("latin-1"))
        env = emulator_env(LC_ALL="C", OS9DISK=image, OS9H6=h6)
        try:
            r = subprocess.run([exe, "-r", "bash", "/h6/l.sh"], env=env,
                               capture_output=True, timeout=60 + 20 * len(todo))
        except subprocess.TimeoutExpired as exc:
            r = exc
    text = (r.stdout or b"").decode("latin-1").replace("\r", "\n")
    parts = re.split(r"@@(\d+|end)@@", text)
    for i in range(1, len(parts) - 1, 2):
        if parts[i] == "end":
            break
        out[todo[int(parts[i])]] = [l.rstrip() for l in parts[i + 1].split("\n")
                                    if l.strip() and not NOISE.match(l.strip())]
    return out


def zoo(path):
    """Members of a Zoo archive, read host-side: (name, size, packed).

    Zoo's fields are LITTLE-endian whatever wrote them: "ZOO <version>
    Archive.", a long magic, the offset of the first entry; then each entry
    is magic, type, method, next offset, data offset, date, time, CRC, the
    size before and after packing, two version bytes, a deleted flag, a
    structure byte, a comment offset and size, and a 13-byte name.
    """
    b = open(path, "rb").read()
    if not b.startswith(b"ZOO ") or struct.unpack("<I", b[20:24])[0] != ZOO_MAGIC:
        return None
    out, at, seen = [], struct.unpack("<I", b[24:28])[0], set()
    while 0 < at < len(b) - 0x55 and at not in seen:
        seen.add(at)
        e = b[at:at + 0x55]
        if struct.unpack("<I", e[0:4])[0] != ZOO_MAGIC:
            break
        nxt = struct.unpack("<I", e[6:10])[0]
        name = e[38:51].split(b"\0")[0].decode("latin-1", "replace")
        if name and not e[30]:
            out.append("%-24s %8d %8d" % (name, struct.unpack("<I", e[20:24])[0],
                                          struct.unpack("<I", e[24:28])[0]))
        at = nxt
    return out


def arc(path):
    """Members of a SEA ARC archive, read host-side."""
    b = open(path, "rb").read()
    if not b or b[0] != 0x1A:
        return None
    out, at = [], 0
    while at + 29 <= len(b) and b[at] == 0x1A:
        method = b[at + 1]
        if method == 0:
            break
        name = b[at + 2:at + 15].split(b"\0")[0].decode("latin-1", "replace")
        packed = struct.unpack("<I", b[at + 15:at + 19])[0]
        orig = packed if method == 1 else struct.unpack("<I", b[at + 25:at + 29])[0]
        out.append("%-24s %8d %8d" % (name, orig, packed))
        at += 29 + packed
    return out


def tar_members(data):
    """Members of a tar, read header by header.

    macOS's tar refuses a v7 archive with no `ustar' magic -- CMDS/
    compress.tar.Z is one -- so the headers are walked here instead: a
    100-byte name, and the size as octal at offset 124.
    """
    out, i = [], 0
    while i + 512 <= len(data):
        head = data[i:i + 512]
        if head.strip(b"\0") == b"":
            break
        name = head[:100].split(b"\0")[0].decode("latin-1", "replace")
        raw = head[124:136].replace(b"\0", b" ").strip() or b"0"
        try:
            size = int(raw, 8)
        except ValueError:
            return out or None
        if not name:
            return out or None
        out.append("%-40s %8d" % (name, size))
        i += 512 + (size + 511) // 512 * 512
    return out or None


def host(path):
    """Whatever the host can list, and a decompressed file is not always a tar.

    `.Z' and `.gz' wrap one file as often as they wrap a tar -- compress.tar.Z
    is a tar, ckermit.doc.Z is a document -- so decompress first and look for
    tar's `ustar' magic before deciding.  A lone file is reported as itself,
    which is the honest listing for it, and a shar by the files it writes.
    """
    low = path.lower()
    data = None
    if low.endswith((".gz", ".tgz")):
        data = subprocess.run(["gzip", "-dc", path], capture_output=True).stdout
    elif low.endswith(".z"):
        data = subprocess.run(["uncompress", "-c", path], capture_output=True).stdout
    if data is not None:
        if not data:
            return None
        got = tar_members(data)
        if got:
            return got
        kind = ("text" if all(32 <= c < 127 or c in (9, 10, 13) for c in data[:400])
                else "OS-9 module" if data[:2] == b"\x4a\xfc" else "data")
        return ["%-28s %8d  (one %s, not an archive)"
                % (os.path.basename(path).rsplit(".", 1)[0], len(data), kind)]
    if low.endswith(".tar"):
        return tar_members(open(path, "rb").read())
    cmd = (["lha", "l", path] if low.endswith((".lzh", ".lha")) else
           ["unzip", "-l", path] if low.endswith(".zip") else None)
    if cmd:
        r = subprocess.run(cmd, capture_output=True)
        return [l for l in r.stdout.decode("latin-1").splitlines()
                if l.strip() and not NOISE.match(l.strip())] or None
    if low.endswith(".shar"):
        text = open(path, "rb").read().decode("latin-1", "replace")
        got = re.findall(r"^(?:sed [^>]*>\s*|cat\s*>\s*)'?\"?([\w.+/-]+)", text, re.M)
        return ["%-28s  (shar member)" % n for n in got] or None
    if low.endswith(".zoo"):
        return zoo(path)
    if low.endswith(".arc"):
        return arc(path)
    return None

def main(argv):
    names_only = "--names" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        sys.exit(__doc__.strip().splitlines()[0])
    universe = in_universe(paths)
    rc = 0
    for path in paths:
        lines = universe.get(path) or host(path)
        if names_only:
            for l in lines or []:
                print(l.split()[-1] if l.split() else "")
            continue
        where = "the disk's own tools" if path in universe else "the host"
        print("== %s (%d bytes, by %s)" % (path, os.path.getsize(path), where))
        if not lines:
            print("   nothing could list it")
            rc = 1
            continue
        for l in lines:
            print("   %s" % l.strip())
        print("   %d line(s)" % len(lines))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
