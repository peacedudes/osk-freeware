#!/usr/bin/env python3
"""List what is inside every archive in the hoard, without unpacking any of it.

Every pool pass so far has asked the same question -- "is <file> anywhere?" --
and answered it with `find`, which only ever sees what somebody already
unpacked. 459 archives sit under ~/Developer/os9 and their contents were
invisible to that search. This writes the index once so the question becomes a
grep.

    tools/index_archives.py [<root>] > notes/pool-archive-contents.tsv

Output is `archive<TAB>member`, one line per file inside an archive.

OS-9 `ar` archives (Carl Kreider's +AR0.0+) are NOT handled here: nothing
host-side reads that format, which is why tools/mine_arr.py exists and runs
the collection's own `ar2` under the emulator. They are listed in the summary
as skipped so the gap is visible rather than silent.

Failures are reported, never swallowed: an archive that cannot be listed is
the interesting kind, and a silent skip would make the index look complete.
"""
import os
import subprocess
import sys

# ext -> (argv builder, how to pull names out of the output)
def _lha(path):   return ["lha", "l", path]
def _zip(path):   return ["unzip", "-l", path]
def _targz(path): return ["tar", "tzf", path]


def _names_lha(out):
    """lha's listing: a two-line header, a rule, then rows ending in the name.

    The name is the LAST field, and names here do not contain spaces -- these
    are OS-9 and MS-DOS era archives. A trailing summary line starting with
    '---' ends the table.
    """
    names = []
    started = False
    for line in out.splitlines():
        stripped = line.strip()
        # The rule line is dashes and spaces and NOTHING else. Testing
        # `startswith("---")' looked right and skipped every data row: an lha
        # listing begins each row with its permission field, `----r-wr', which
        # starts with three dashes too. 40 archives indexed as empty that way.
        if stripped and set(stripped) <= {"-", " "}:
            started = not started
            continue
        if not started or not stripped:
            continue
        parts = line.split()
        if parts:
            names.append(parts[-1])
    return names


def _names_zip(out):
    names, started = [], False
    for line in out.splitlines():
        if line.startswith("---"):
            started = not started
            continue
        if not started or not line.strip():
            continue
        parts = line.split(None, 3)
        if len(parts) == 4:
            names.append(parts[3])
    return names


def _names_tar(out):
    return [l for l in out.splitlines() if l.strip()]


def _names_rawtar(data):
    """List an old tar by walking its 512-byte headers ourselves.

    bsdtar refuses these -- "Unrecognized archive format" -- because pre-POSIX
    V7 tars carry no `ustar' magic, and a good deal of the hoard is that old
    (`compress.tar.Z' is one). The format needed here is trivial: name at
    offset 0, size in octal at 124, contents rounded up to a 512-byte block.
    Refusing to read them would have left 68 archives permanently invisible.
    """
    names, off, n = [], 0, len(data)
    while off + 512 <= n:
        hdr = data[off:off + 512]
        if hdr[:1] == b"\0":                      # end-of-archive padding
            break
        name = hdr[:100].split(b"\0", 1)[0].decode("latin-1", "replace").strip()
        raw = hdr[124:136].split(b"\0", 1)[0].strip()
        try:
            size = int(raw, 8) if raw else 0
        except ValueError:                        # not a tar header after all
            break
        if name:
            names.append(name)
        off += 512 + (size + 511) // 512 * 512
    return names


HANDLERS = {
    ".lzh": (_lha, _names_lha), ".lha": (_lha, _names_lha),
    ".zip": (_zip, _names_zip),
    ".tar.gz": (_targz, _names_tar), ".tgz": (_targz, _names_tar),
    ".tar.z": (_targz, _names_tar), ".tar": (_targz, _names_tar),
    ".z": (_targz, _names_tar),
}


MAGIC = [
    (b"\x1f\x9d", "compress"),   # .Z -- LZW, what `compress' wrote
    (b"\x1f\x8b", "gzip"),
    (b"PK\x03\x04", "zip"),
]


def sniff(path):
    """What a file ACTUALLY is, by its first bytes. The extension lies.

    Measured 2026-08-26: `pd0.lzh' is compress'd data, `elm24.lzh' is an OS-9
    module, `dvips.lzh' is CR-terminated ASCII. Fifteen archives were indexed
    as unreadable because the name was believed over the content, and one of
    them was an entire EFFO public-domain disk.
    """
    try:
        head = open(path, "rb").read(8)
    except OSError:
        return None
    for magic, kind in MAGIC:
        if head.startswith(magic):
            return kind
    if head[:3] == b"-lh" or head[2:5] == b"-lh":
        return "lha"
    return None


def handler_for(name):
    low = name.lower()
    for suffix in (".tar.gz", ".tar.z"):        # two-part suffixes first
        if low.endswith(suffix):
            return HANDLERS[suffix]
    ext = os.path.splitext(low)[1]
    return HANDLERS.get(ext)


def _raw_fallback(path):
    """Decompress if we must, then walk the tar headers by hand. [] if hopeless."""
    low = path.lower()
    try:
        if low.endswith((".z", ".gz", ".tgz")):
            r = subprocess.run(["gzip", "-dc", path], capture_output=True, timeout=120)
            data = r.stdout
            if not data:
                r = subprocess.run(["uncompress", "-c", path],
                                   capture_output=True, timeout=120)
                data = r.stdout
        else:
            data = open(path, "rb").read()
    except Exception:                             # noqa: BLE001
        return []
    return _names_rawtar(data)


def main(argv):
    root = os.path.expanduser(argv[0] if argv else "~/Developer/os9")
    listed = failed = skipped_ar = 0
    for dirpath, _dirs, files in os.walk(root):
        if "/osk-freeware/" in dirpath + "/":     # our own tree, not the hoard
            continue
        for f in sorted(files):
            path = os.path.join(dirpath, f)
            if f.lower().endswith(".ar"):
                skipped_ar += 1
                continue
            h = handler_for(f)
            kind = sniff(path)
            # Content wins over the extension when they disagree.
            if kind == "compress" or kind == "gzip":
                h = (_targz, _names_tar)
            elif kind == "zip":
                h = (_zip, _names_zip)
            elif kind == "lha" and not h:
                h = (_lha, _names_lha)
            if not h:
                continue
            build, parse = h
            try:
                r = subprocess.run(build(path), capture_output=True, timeout=120)
                names = parse(r.stdout.decode("latin-1", "replace"))
                # `lha' puts its listing on stderr when stdout is not a
                # terminal, so stdout alone reported 40 good archives as EMPTY.
                # Try stderr only as a SECOND pass: folding it in unconditionally
                # fed tar's error text to the tar parser as though those lines
                # were member names, which cost 700 real members and looked like
                # a success -- 15 more archives "listed", fewer files in them.
                if not names:
                    names = parse(r.stderr.decode("latin-1", "replace"))
                if not names:
                    names = _raw_fallback(path)
            except Exception as e:                # noqa: BLE001 -- report, do not hide
                print(f"# FAILED {path}: {e}", file=sys.stderr)
                failed += 1
                continue
            if not names:
                print(f"# EMPTY  {path}", file=sys.stderr)
                failed += 1
                continue
            listed += 1
            for n in names:
                print(f"{path}\t{n}")
    print(f"# {listed} archives listed, {failed} unreadable, "
          f"{skipped_ar} OS-9 .ar skipped (see tools/mine_arr.py)", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
