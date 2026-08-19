#!/usr/bin/env python3
"""List the members of every archive in the OS-9 freeware pool.

Writes TSV: category, archive, bytes, status, member.

An archive that cannot be opened is recorded as such rather than skipped --
the whole point of this pass is that filenames have hidden things before, so
"we could not look" must be visible in the output.

macOS bsdtar rejects the old-format tars in this pool ("Unrecognized archive
format"); Python's tarfile reads them, which is why this is not a shell
script. Unix compress (.Z) is handed to gzip(1), which Python cannot do.
"""
import io, os, subprocess, sys, tarfile, zipfile
import paths

POOL = paths.pool()
LZH = (".lzh", ".lha", ".lhz")


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, **kw)


def tar_names(data):
    with tarfile.open(fileobj=io.BytesIO(data)) as t:
        return t.getnames()


def members(path, low):
    """(status, [member, ...])"""
    try:
        if low.endswith(LZH):
            # `lha lq' prints data lines only. Columns are
            # perm uid/gid size ratio MON DD YEAR-or-TIME NAME, and NAME may
            # contain spaces, so take field 8 onward. Do NOT filter on a
            # leading "---": every permission string starts with dashes, and
            # an earlier version of this threw away every member for it.
            out = sh(["lha", "lq", path]).stdout.decode("latin-1", "replace")
            names = []
            for l in out.splitlines():
                f = l.split(None, 7)
                if len(f) == 8 and "/" in f[1]:
                    names.append(f[7].strip())
            return ("ok", names) if names else ("lzh_empty", [])
        if low.endswith(".zip"):
            with zipfile.ZipFile(path) as z:
                return "ok", z.namelist()
        if low.endswith((".tgz", ".tar.gz")):
            return "ok", tar_names(open(path, "rb").read())
        if low.endswith(".gz"):
            data = sh(["gzip", "-dc", path]).stdout
            try:    return "ok", tar_names(data)
            except Exception: return "plain_gz", [os.path.basename(low)[:-3]]
        if low.endswith(".z"):
            data = sh(["gzip", "-dc", path]).stdout
            try:    return "ok", tar_names(data)
            except Exception: return "plain_Z", [os.path.basename(low)[:-2]]
        if low.endswith(".tar") or low.endswith(".ytar"):
            return "ok", tar_names(open(path, "rb").read())
        if low.endswith(".ar"):
            return "os9_ar", []          # handled by the disk's own ar
        if low.endswith(".zoo"):
            return "zoo", []             # handled by the disk's own zoo
        if low.endswith(".shar"):
            out = open(path, "rb").read().decode("latin-1", "replace")
            names = [l.split()[-1] for l in out.splitlines()
                     if l.startswith("# ") and len(l.split()) == 2]
            return "shar", names
        head = open(path, "rb").read(2)
        return ("os9_module" if head == b"\x4a\xfc" else "bare_file",
                [os.path.basename(path)])
    except Exception as e:
        return "ERROR:%s" % type(e).__name__, []


def main(out_path):
    rows = 0
    with open(out_path, "w") as out:
        for root, _, files in os.walk(POOL):
            for name in sorted(files):
                path = os.path.join(root, name)
                rel = os.path.relpath(path, POOL)
                cat = rel.split(os.sep)[0] if os.sep in rel else "(root)"
                size = os.path.getsize(path)
                st, ms = members(path, name.lower())
                for m in (ms or [""]):
                    out.write("\t".join((cat, name, str(size), st, m)) + "\n")
                    rows += 1
    print("wrote %d member rows" % rows)


main(sys.argv[1])
