#!/usr/bin/env python3
"""Extract every archive in the pool, dispatching on CONTENT.

Extension-based dispatch left 133 pool files unopened and was wrong 27 times:
`rn.tar.Z` and `KA9Q9501.gz` are LHA archives, `elm24.lzh` and `cnews.tar.Z`
are bare OS-9 modules, `rtclock1287.lzh` is a ZIP, and twelve files are named
`fileNNNN` with no extension at all. Several more named `.lzh` are plain
description text the archive serves under an archive-looking name -- not
failed downloads, just mislabelled upstream.

OS-9 `ar` and zoo archives are extracted BY THE COLLECTION'S OWN `ar2` and
`zoo`, running under os9exec. Nothing host-side reads Carl Kreider's format,
and the disk's V1.2 `ar` answers "unknown compression algo" -- V2.00 (`ar2`)
reads them. Both are starred, which is why OS9CIO must point at a directory
holding a cio.

Usage:  extract_pool.py <pool-dir> <out-dir>
Env:    OS9EXEC   path to the os9exec binary   (needed for .ar)
        OS9IMAGE  path to a built disk image   (needed for .ar)
        OS9CIO    directory holding cio        (needed for .ar)
"""
import io, os, subprocess, sys, tarfile, zipfile

def sniff(p):
    try:
        with open(p, "rb") as f:
            h = f.read(512)
    except OSError:
        return "unreadable"
    if not h:                                     return "empty"
    if h[:2] == b"\x4a\xfc":                      return "module"
    if h[:7] == b"+AR0.0+":                       return "os9ar"
    if h[:3] == b"ZOO":                           return "zoo"
    if h[:2] == b"PK":                            return "zip"
    if h[:2] == b"\x1f\x8b":                      return "gzip"
    if h[:2] == b"\x1f\x9d":                      return "compress"
    if h[2:5] == b"-lh":                          return "lha"
    if len(h) > 262 and h[257:262] == b"ustar":   return "tar"
    if h[:5] == b"begin":                         return "uue"
    if len(h) > 156 and h[148:156].strip(b"\0 ").isdigit(): return "tar"
    return "other"

def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, **kw)

def untar(data, dest):
    """Unpack a tar, returning how many files came out.

    ignore_zeros: mnews.t.Z has a stray block that makes bsdtar reject the
    whole archive, and it holds 200 members.

    THE COUNT IS LOAD-BEARING. With ignore_zeros set, tarfile does not raise
    on input that is not a tar at all -- it reports zero members and returns
    quietly. The caller's `except Exception` fallback therefore never fired,
    and 16 pool files that decompress to a single plain payload were silently
    dropped by every sweep that has ever run here. Among them the sox manual
    for a program that ships with no documentation, the MicroGnuEmacs manual,
    and two host-side builds of Carl Kreider's `ar`. Return the count and make
    the caller check it.
    """
    n = 0
    with tarfile.open(fileobj=io.BytesIO(data), ignore_zeros=True) as t:
        for m in t.getmembers():
            if m.isdir():
                continue
            out = os.path.join(dest, m.name.lstrip("./").replace("..", "_"))
            os.makedirs(os.path.dirname(out) or dest, exist_ok=True)
            f = t.extractfile(m)
            if f:
                open(out, "wb").write(f.read())
                n += 1
    return n

def extract_in_universe(path, dest, cmd):
    """Run one of the collection's OWN archivers under os9exec, with the target
    directory mounted as /h6.

    Two formats here have no host-side reader: Carl Kreider's `+AR0.0+` and
    zoo. Both are on the disk, both are starred, and both do the job -- so the
    collection unpacks its own archives, the way it populates itself with its
    own `tar`.
    """
    exe, img, cio = (os.environ.get("OS9EXEC"), os.environ.get("OS9IMAGE"),
                     os.environ.get("OS9CIO"))
    if not (exe and img and cio):
        return False
    os.makedirs(dest, exist_ok=True)
    name = os.path.basename(path)
    open(os.path.join(dest, name), "wb").write(open(path, "rb").read())
    # `load' puts cio in the module directory before the unpacker asks for it
    # -- the reader's own, staged at /h1/CMDS/load, since the disk ships none.
    import tempfile
    from os9env import emulator_env, stage_reader_load
    h1 = tempfile.mkdtemp(prefix="xp_h1.")
    stage_reader_load(h1)
    script = ("/h1/CMDS/load /h5/cio\ncd /h6\n%s /h6/%s\nexit\n" % (cmd, name))
    env = emulator_env(OS9DISK=img, OS9H1=h1, OS9H5=cio,
                       OS9H6=os.path.abspath(dest))
    try:
        subprocess.run([exe, "-r", "bash", "/dd/SYS/login"], input=script.encode(),
                       capture_output=True, env=env, timeout=60)
    except subprocess.TimeoutExpired:
        pass                    # bash may not quit on EOF; the files are what matter
    os.remove(os.path.join(dest, name))
    # Success is what LANDED, not what was printed. os9exec's output carries
    # NULs and escape sequences, and matching on it reported FAILED for three
    # archives that had in fact extracted perfectly well.
    return any(fs for _, _, fs in os.walk(dest))

def extract(path, dest):
    """True if something was unpacked into dest."""
    k = sniff(path)
    if k in ("module", "other", "empty", "unreadable"):
        return False
    os.makedirs(dest, exist_ok=True)
    try:
        if k == "lha":
            run(["lha", "xqfw=" + dest, os.path.abspath(path)])
        elif k == "zip":
            with zipfile.ZipFile(path) as z:
                z.extractall(dest)
        elif k == "tar":
            untar(open(path, "rb").read(), dest)
        elif k in ("gzip", "compress"):
            data = run(["gzip", "-dc", path]).stdout
            if not data:
                return False
            try:
                if untar(data, dest) == 0:
                    raise ValueError("decompressed to something that is not a tar")
            except Exception:
                base = os.path.basename(path)
                for suf in (".gz", ".Z", ".z", ".tgz"):
                    if base.lower().endswith(suf.lower()):
                        base = base[:-len(suf)]; break
                open(os.path.join(dest, base or "data"), "wb").write(data)
        elif k == "uue":
            run(["uudecode", "-o", os.path.join(dest, "decoded"), os.path.abspath(path)])
        elif k == "os9ar":
            return extract_in_universe(path, dest, "/dd/CMDS/ar2 -x")
        elif k == "zoo":
            return extract_in_universe(path, dest, "/dd/CMDS/zoo -extract")
    except Exception:
        return False
    return any(fs for _, _, fs in os.walk(dest))

def main():
    pool, out = sys.argv[1], sys.argv[2]
    n = 0
    for cat in sorted(os.listdir(pool)):
        d = os.path.join(pool, cat)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            p = os.path.join(d, f)
            if os.path.isfile(p) and extract(p, os.path.join(out, cat, f.replace(".", "_"))):
                n += 1
    print("archives unpacked:", n)
    # nested archives, to a fixpoint
    for _ in range(5):
        again = 0
        for r, _dirs, fs in os.walk(out):
            for f in fs:
                p = os.path.join(r, f)
                dst = p + ".x"
                if not os.path.isdir(dst) and extract(p, dst):
                    again += 1
        print("  nested pass:", again)
        if not again:
            break


# Guarded so the module can be imported and its parts tested. Without this,
# `from extract_pool import extract` runs the whole pool sweep and then dies
# on sys.argv.
if __name__ == "__main__":
    main()
