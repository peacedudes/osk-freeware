#!/usr/bin/env python3
"""What the import left behind in the usenet archives.

    tools/missing_from_archive.py [<staging-dir>]

`world' would not compile because `parame.inc' was not in SRC/world. It was
never meant to be -- it is generated from `vocab.dat', which was not there
either. Both `vocab.dat' and `vtext.dat' were still sitting in
play/h4/ARR/world.ar, which the import had read only partly. The game has
been unbuildable ever since for want of two files nobody had noticed were
gone.

That is the kind of gap this looks for, across every tree at once: for each
source tree the disk carries, open the archive DOC/ORIGINS says it came from
and list the members that did not make it in.

It PROPOSES; it copies nothing. Some absences are deliberate -- object files,
scratch, and anything the Microware screen objects to -- so the output is a
list to read, not a patch to apply.

Extraction runs in-universe: Carl Kreider's `+AR0.0+' format has no host-side
reader and the collection's own `ar2' is the only thing that opens it. That
needs the built image, so build it first.
"""
import os
import subprocess
import sys

import paths

# Absences that are not gaps. Object files rebuild from the source beside
# them, and the rest is a working directory swept into an archive.
DULL_SUFFIX = (".r", ".o", ".bak", ".orig", ".old", ".rej", "~", ".tmp",
               ".lst", ".map", ".sym", ".bk")
DULL_NAMES = {"core", "a.out", "makefile.bak", "tmp", "temp", "junk"}


def origins(repo):
    """{tree: {archive names}} from DOC/ORIGINS' `usenet archive  x.ar' lines."""
    path = os.path.join(repo, "disk", "DOC", "ORIGINS")
    out = {}
    for line in open(path, "rb").read().decode("latin-1").replace("\r", "\n").split("\n"):
        if not line.startswith("  ") or line[2:3] == " ":
            continue
        parts = line.split()
        if len(parts) < 4 or "archive" not in line:
            continue
        for token in parts:
            if token.endswith(".ar"):
                out.setdefault(parts[1], set()).add(token)
    return out


def extract(archive, dest, exe, image):
    """Unpack one .ar with the disk's own ar2. Returns what landed."""
    os.makedirs(dest, exist_ok=True)
    name = os.path.basename(archive)
    open(os.path.join(dest, name), "wb").write(open(archive, "rb").read())
    script = f"cd /h6\n/dd/CMDS/ar2 -x /h6/{name}\nexit\n"
    env = dict(os.environ, OS9DISK=image, OS9H6=os.path.abspath(dest))
    try:
        subprocess.run([exe, "-r", "bash", "/dd/SYS/login"],
                       input=script.encode(), capture_output=True,
                       env=env, timeout=180)
    except subprocess.TimeoutExpired:
        pass            # bash may not quit on EOF; what landed is the answer
    os.remove(os.path.join(dest, name))
    return sorted(os.listdir(dest))


def dull(name):
    low = name.lower()
    return low in DULL_NAMES or low.endswith(DULL_SUFFIX)


def main(argv):
    repo = paths.repo()
    exe = paths.os9exec()
    image = os.path.join(repo, "osk-freeware.dd")
    if not os.path.isfile(image):
        sys.exit(f"no image at {image} -- build it first:\n"
                 f"  OS9EXEC_DIR=... tools/mkimage.sh disk {image}")
    arr = paths.usenet_ar()
    stage = os.path.abspath(argv[0]) if argv else os.path.join(
        os.environ.get("TMPDIR", "/tmp"), "os9missing")

    trees = origins(repo)
    gaps = 0
    for tree in sorted(trees):
        here = os.path.join(repo, "disk", "SRC", tree)
        if not os.path.isdir(here):
            continue
        have = {f.lower() for f in os.listdir(here)}
        for archive in sorted(trees[tree]):
            src = os.path.join(arr, archive)
            if not os.path.isfile(src):
                continue
            dest = os.path.join(stage, tree, archive)
            members = extract(src, dest, exe, image)
            if not members:
                print(f"{tree:16} {archive:16} -- nothing extracted")
                continue
            absent = [m for m in members if m.lower() not in have]
            interesting = [m for m in absent if not dull(m)]
            print(f"{tree:16} {archive:16} {len(members):3} members, "
                  f"{len(absent):3} not in SRC/{tree}"
                  + (f", {len(interesting)} worth a look" if interesting else ""))
            for m in interesting:
                size = os.path.getsize(os.path.join(dest, m))
                print(f"                     {m:28} {size:8}")
                gaps += 1
    print(f"\n{gaps} file(s) in the archives that the disk does not carry.")
    print(f"Extracted under {stage} -- read before copying anything in.")


if __name__ == "__main__":
    main(sys.argv[1:])
