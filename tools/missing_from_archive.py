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

# Names so common that finding one SOMEWHERE on the disk proves nothing about
# THIS package. `DOC/gnu/COPYING' would otherwise hide the fact that diff's own
# COPYING never arrived. These are compared against the tree's own places only.
GENERIC = {"readme", "readme.1st", "copying", "copyright", "license",
           "licence", "makefile", "manifest", "help", "save", "man",
           "man.cat", "changelog", "install", "todo", "notes", "index"}


def origins(repo):
    """({tree: archives}, {tree: programs}) from DOC/ORIGINS."""
    path = os.path.join(repo, "disk", "DOC", "ORIGINS")
    out, progs = {}, {}
    for line in open(path, "rb").read().decode("latin-1").replace("\r", "\n").split("\n"):
        if not line.startswith("  ") or line[2:3] == " ":
            continue
        parts = line.split()
        if len(parts) < 4 or "archive" not in line:
            continue
        for token in parts:
            if token.endswith(".ar"):
                out.setdefault(parts[1], set()).add(token)
                progs.setdefault(parts[1], set()).add(parts[0])
    return out, progs


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

    # Every basename the disk carries ANYWHERE, not just in SRC. A game's data
    # lives under GAMES and its manual under DOC, so comparing against SRC
    # alone called `glorkz', `gnuchess.book' and `sokoban.help' missing when
    # all three ship -- 30-odd false gaps out of 142, which is enough to make
    # the list not worth reading.
    everywhere = set()
    for here, dirs, files in os.walk(os.path.join(repo, "disk")):
        for f in files:
            everywhere.add(f.lower())
        # DIRECTORIES too: sokoban's `screens' and `SAVES' are directories on
        # the disk and files in the archive, and walking only the files called
        # both of them missing.
        for d in dirs:
            everywhere.add(d.lower())

    trees, progs = origins(repo)
    gaps = 0
    for tree in sorted(trees):
        here = os.path.join(repo, "disk", "SRC", tree)
        if not os.path.isdir(here):
            continue
        have = {f.lower() for f in os.listdir(here)}
        # ...and the DOC directory of every program that came from this tree,
        # which is where a README or a man page actually lands.
        for prog in progs.get(tree, ()):
            doc = os.path.join(repo, "disk", "DOC", prog)
            if os.path.isdir(doc):
                have |= {f.lower() for f in os.listdir(doc)}
        doc = os.path.join(repo, "disk", "DOC", tree)
        if os.path.isdir(doc):
            have |= {f.lower() for f in os.listdir(doc)}
        for archive in sorted(trees[tree]):
            src = os.path.join(arr, archive)
            if not os.path.isfile(src):
                continue
            dest = os.path.join(stage, tree, archive)
            members = extract(src, dest, exe, image)
            if not members:
                print(f"{tree:16} {archive:16} -- nothing extracted")
                continue
            absent = [m for m in members
                      if m.lower() not in have
                      and (m.lower() in GENERIC or m.lower() not in everywhere)]
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
