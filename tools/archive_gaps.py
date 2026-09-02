#!/usr/bin/env python3
"""What each origin archive holds that this disk does NOT.

    tools/archive_gaps.py                 # single-package archives only
    tools/archive_gaps.py --all           # forum disks too, which are noise
    tools/archive_gaps.py pd7.lzh lua     # just these

WHY THIS EXISTS.  Twice in one evening a program was written off as broken
or bare when the missing piece was sitting in the archive we already had:

  * `forth' is TILE Forth, and it looks for its Forth-83 source library in
    `lib/tile'.  The library, the twenty-two programs it shipped with, the
    full C source and sixteen manuals were ALL in EFFO pd7.lzh, four
    directories away from the binary somebody extracted.  The catalogue
    told a reader to go and fetch the package's own data files.
  * `lua' shipped with no example scripts.  Eight came in lua.src.zip.

Nobody had asked the question the other way round -- not "what does the
binary open" (DOC/DEPENDS answers that, and it cannot see a file opened by
a bare name) but "what came in the box that we never took out".

It lists, per archive: the members whose basename appears nowhere under
`disk/'.  Expect noise -- object files, makefiles for other machines, the
author's own build leftovers -- and read it as a prompt, not a defect list.
DOC and example directories are what to look at first.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import paths                                            # noqa: E402

SKIP_EXT = {".r", ".o", ".obj", ".bak", ".old", ".i", ".l"}
# Members at or under this count make the archive a PACKAGE rather than a
# collection; above it, absence is a decision somebody made on purpose.
PACKAGE = 90

SKIP_NAME = {"makefile", "makefile.ori", "makefile.msdos", "makefile.os9",
             "descrip.mms", ".ds_store", "read.me"}


def members(path):
    """Every member name in `path', or [] if we cannot read it."""
    low = path.lower()
    try:
        if low.endswith((".lzh", ".lha")):
            # `lha lq' is one line per member with no header and no ruler;
            # plain `l' wraps a long name onto a second line and the last
            # field of that line is a TIME, which arrived here as a member
            # called `10:31'.
            out = subprocess.run(["lha", "lq", path], capture_output=True,
                                 text=True, timeout=120).stdout
            return [l.split()[-1] for l in out.split("\n") if l.strip()]
        if low.endswith(".zip"):
            out = subprocess.run(["unzip", "-Z1", path], capture_output=True,
                                 text=True, timeout=120).stdout
            return [l.strip() for l in out.split("\n") if l.strip()]
        if low.endswith((".tar.z", ".tar.gz", ".tgz")):
            out = subprocess.run("zcat < %s | tar tf -" % repr(path),
                                 shell=True, capture_output=True,
                                 text=True, timeout=120).stdout
            return [l.strip() for l in out.split("\n") if l.strip()]
    except Exception:
        return []
    return []


def on_disk():
    """Every basename anywhere under disk/, folded to lower case."""
    seen = set()
    for base, _, files in os.walk(os.path.join(REPO, "disk")):
        for f in files:
            seen.add(f.lower())
    return seen


def archives_named():
    """The archive filenames DOC/ORIGINS cites, and who came from each."""
    t = open(os.path.join(REPO, "disk", "DOC", "ORIGINS"),
             newline="").read().replace("\r", "\n")
    out = {}
    for line in t.split("\n"):
        m = re.match(r"^  (\S+)\s+(\S+)\s+(.*)$", line)
        if not m:
            continue
        f = re.search(r"([A-Za-z0-9_.-]+\.(?:lzh|lha|zip|tar\.Z))", m.group(3))
        if f:
            out.setdefault(f.group(1), []).append(m.group(1))
    return out


def find(name):
    """Where that archive lives in the pool, if it is there."""
    for root in (paths.pool(), paths.extra_archives()):
        if not os.path.isdir(root):
            continue
        for base, _, files in os.walk(root):
            for f in files:
                if f.lower() == name.lower():
                    return os.path.join(base, f)
    return None


def main(argv):
    only_packages = "--all" not in argv
    want = [a.lower() for a in argv if a != "--all"]
    have = on_disk()
    named = archives_named()
    total_gaps = 0
    for arch in sorted(named):
        if want and not any(w in arch.lower() or
                            w in " ".join(named[arch]).lower() for w in want):
            continue
        path = find(arch)
        if not path:
            continue
        gaps = []
        for m in members(path):
            base = os.path.basename(m.rstrip("/"))
            if not base or m.endswith("/"):
                continue
            low = base.lower()
            if low in SKIP_NAME or os.path.splitext(low)[1] in SKIP_EXT:
                continue
            if low not in have:
                gaps.append(m)
        if gaps:
            # AN EFFO FORUM DISK IS NOT A PACKAGE.  forum7.lzh holds a whole
            # magazine's contributions and we took two programs from it on
            # purpose; nearly every other member is somebody else's work and
            # its absence is a decision, not an oversight.  A SINGLE-PACKAGE
            # archive is the one worth reading -- that is the shape pd7 and
            # lua.src.zip have, where the missing members belong to the very
            # program we did take.
            all_members = len(members(path))
            package = all_members <= PACKAGE
            if only_packages and not package:
                continue
            total_gaps += len(gaps)
            print("\n%s  (%s)  %d of %d members not here%s"
                  % (arch, ", ".join(sorted(named[arch])[:6]), len(gaps),
                     all_members, "" if package else "  [a forum disk]"))
            for g in sorted(gaps)[:24]:
                print("    %s" % g)
            if len(gaps) > 24:
                print("    ... and %d more" % (len(gaps) - 24))
    print("\n%d member(s) not on the disk" % total_gaps)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
