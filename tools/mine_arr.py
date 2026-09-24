#!/usr/bin/env python3
"""Open the 65 usenet `ar` archives in play/h4/ARR and say what is in them.

This is rdoggett's own 1989 usenet collection -- things grabbed off the net,
built, and filed. His description, 2026-08-19: junk and stuff, some of it not
worth sharing, archived mainly to shrink it. Names like `misc.ar`, `toys.ar`
and `de.ar` are grab-bags, and scratch files got swept in.

**It once contained proprietary Microware source.** He believes those were
removed; belief is not a check, so every member is screened before anything
is proposed for the disk -- see tools/screen_microware.py.

So this tool proposes, it never installs. For each archive it reports:

  members         what is inside
  on the disk     which member names already exist under disk/CMDS
  source known    which already have a disk/SRC tree
  FLAGGED         anything the Microware screen objects to
  junk            zero-length, scratch and editor leftovers

Carl Kreider's `+AR0.0+` format has no host-side reader. The collection's own
`ar2` is the only thing that opens it (V1.2 `ar` answers "unknown compression
algo"), so extraction runs under os9exec with the target as /h6 -- the same
in-universe route the pool extractor uses.

  tools/mine_arr.py <staging-dir>
"""
import os
import subprocess
import sys

import paths
import screen_microware

# Swept-in scratch: things that are evidence of a working directory, not
# software anybody wants. Judged by name; content decides the close calls.
JUNK_NAMES = {"core", "a.out", "tmp", "temp", "scratch", "junk", "x", "xx",
              "foo", "bar", "test.out", "makefile.bak", ".ds_store"}
JUNK_SUFFIX = (".bak", ".orig", ".rej", ".old", "~", ".tmp", ".bk", ".swp",
               ".lst", ".map", ".sym")


def extract_one(archive, dest, exe, image):
    """Unpack one .ar with the disk's own ar2. True if anything landed."""
    os.makedirs(dest, exist_ok=True)
    name = os.path.basename(archive)
    open(os.path.join(dest, name), "wb").write(open(archive, "rb").read())
    script = f"cd /h6\n/dd/CMDS/ar2 -x /h6/{name}\nexit\n"
    env = dict(os.environ, OS9DISK=image, OS9H6=os.path.abspath(dest))
    try:
        subprocess.run([exe, "-r", "bash", "/dd/SYS/login"],
                       input=script.encode(), capture_output=True,
                       env=env, timeout=120)
    except subprocess.TimeoutExpired:
        pass                # bash may not quit on EOF; what landed is the answer
    os.remove(os.path.join(dest, name))
    # Judge by what LANDED. os9exec's stdout carries NULs and escapes, and
    # matching on it reported FAILED for three pool archives that were fine.
    return any(fs for _, _, fs in os.walk(dest))


def is_junk(path):
    n = os.path.basename(path).lower()
    if n in JUNK_NAMES or n.endswith(JUNK_SUFFIX):
        return "scratch name"
    try:
        if os.path.getsize(path) == 0:
            return "empty"
    except OSError:
        return "unreadable"
    return None


def main(argv):
    if not argv:
        sys.exit("usage: mine_arr.py <staging-dir>")
    stage = os.path.abspath(argv[0])
    repo = paths.repo()
    exe = paths.os9exec()
    image = os.path.join(repo, "osk-freeware.dd")
    if not os.path.isfile(image):
        sys.exit(f"no image at {image} -- build it first")

    arr = paths.usenet_ar()
    archives = sorted(f for f in os.listdir(arr) if f.endswith(".ar"))
    print(f"# {len(archives)} archives in {arr}", file=sys.stderr)

    # What the disk already has, by bare name.
    on_disk, src_trees = set(), set()
    for dirpath, _d, files in os.walk(os.path.join(repo, "disk", "CMDS")):
        on_disk.update(f.lower() for f in files)
    src_root = os.path.join(repo, "disk", "SRC")
    if os.path.isdir(src_root):
        src_trees = {d.lower() for d in os.listdir(src_root)}

    by_name, texts, digests = screen_microware.sdk_index()

    rows = []
    for a in archives:
        tree = os.path.basename(a)[:-3]
        dest = os.path.join(stage, tree)
        if not os.path.isdir(dest) or not any(fs for _, _, fs in os.walk(dest)):
            extract_one(os.path.join(arr, a), dest, exe, image)
        members = []
        for dirpath, _d, files in os.walk(dest):
            for f in files:
                members.append(os.path.join(dirpath, f))
        flagged, junk = [], []
        for m in members:
            reasons = screen_microware.screen(m, by_name, texts, digests)
            strong = [r for r in reasons
                      if "IDENTICAL" in r or "of its lines" in r or "claims:" in r]
            if strong:
                flagged.append((os.path.relpath(m, dest), "; ".join(strong)))
            j = is_junk(m)
            if j:
                junk.append((os.path.relpath(m, dest), j))
        rows.append({
            "archive": a, "tree": tree, "members": len(members),
            "have_src": tree in src_trees,
            "on_disk": sorted({os.path.basename(m).lower() for m in members}
                              & on_disk),
            "flagged": flagged, "junk": junk,
        })
        print(f"  {a:18s} {len(members):4d} members"
              f"{'  SRC on disk' if tree in src_trees else ''}"
              f"{'  FLAGGED ' + str(len(flagged)) if flagged else ''}",
              file=sys.stderr)

    print("archive\tmembers\thave_src\ton_disk\tflagged\tjunk")
    for r in rows:
        print("\t".join((r["archive"], str(r["members"]),
                         "yes" if r["have_src"] else "no",
                         ",".join(r["on_disk"]) or "-",
                         ";".join(f"{p}: {why}" for p, why in r["flagged"]) or "-",
                         str(len(r["junk"])))))
    tot_flag = sum(len(r["flagged"]) for r in rows)
    print(f"\n# {sum(r['members'] for r in rows)} members, "
          f"{tot_flag} Microware-flagged, "
          f"{sum(len(r['junk']) for r in rows)} junk", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
