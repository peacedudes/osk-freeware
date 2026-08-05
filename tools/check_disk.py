#!/usr/bin/env python3
"""Check the invariants of the disk tree that are cheap to get wrong.

    tools/check_disk.py disk

Each check has been made to fail on purpose at least once. A check that
cannot fail is worse than no check: this collection has already produced a
verifier that reported 20/20 OK having run nothing, and a builder that
reported "copied 3287/3287" while every copy failed.

  1. NO TEXT FILE CONTAINS LF. OS-9 ends a line with CR alone. An LF-ended
     file is read by OS-9's cpp as one enormous line, surfacing as "source
     line too long" -- which has bitten this collection more than once, and
     is invisible until something tries to read the file. Binaries are
     skipped: 0x0A is an ordinary byte in a module.

  2. NO UTF-8 ON AN 8-BIT DISK. An em dash typed host-side reaches OS-9 as
     three garbage characters. Legacy 8-bit archive content is left alone,
     told apart by the fact that it does not decode as UTF-8.

  3. NO EDITOR OR HOST LEFTOVERS. mkimage.sh reads disk/ off the filesystem,
     so .gitignore does not keep a vim swap file out of the shipped image.

  4. NO NEW SDK AUTHOR STAMPS. Removing them was the point of the rebake;
     the 15 that remain are documented individually.

  5. EVERY COMMAND IS NAMED IN DOC/INDEX. INDEX is what tells a reader what
     a program is; a command absent from it is undiscoverable.

  6. THE DOCUMENTED COUNTS MATCH THE TREE. The readme opened with "409
     programs that run" -- a figure no combination of directories produces.
     Numbers in prose rot silently, so the ones that matter are derived.

  7. DOC/DEPENDS IS UP TO DATE. It is generated, and drifts the moment
     anything is added -- delegated to gen_depends.py, which owns the rule.
"""
import os, re, subprocess, sys

MODULE_MAGIC = b"\x4a\xfc"
TEXT_RATIO   = 0.97
CMD_DIRS     = ["CMDS", "CMDS/GAMES"]


def is_text(data):
    """True for a file worth holding to the text rules.

    An OS-9 module is exempt by its magic. Beyond that the test is the
    ABSENCE of binary markers, not the presence of ASCII: a NUL byte, or more
    than a trace of odd control characters.

    High-bit bytes deliberately do NOT count against a file. Much of this
    archive is genuinely 8-bit -- fortunes.dat, the unaxcess docs -- and
    scoring those as binary would quietly exempt exactly the files most
    likely to be wrong. An earlier version of this function did that, and
    skipped a short file made almost entirely of one em dash.
    """
    if not data or data[:2] == MODULE_MAGIC or b"\x00" in data:
        return False
    odd = sum(1 for b in data if b < 32 and b not in (9, 10, 12, 13, 27))
    return odd / len(data) < 1 - TEXT_RATIO


def check_line_endings(root):
    bad = []
    for dirpath, _, names in os.walk(root):
        for name in names:
            path = os.path.join(dirpath, name)
            try:
                data = open(path, "rb").read()
            except OSError:
                continue
            if is_text(data) and b"\n" in data:
                bad.append((os.path.relpath(path, root), data.count(b"\n")))
    for path, n in sorted(bad):
        print("    %s: %d LF" % (path, n))
    return not bad, "%d text file(s) contain LF" % len(bad)


def check_no_utf8(root):
    """Catch modern text that has leaked onto a disk read by an 8-bit OS.

    OS-9 has no UTF-8. An em dash written host-side arrives as three garbage
    characters, which is how DOC/REBUILT-NOTES.md shipped for a while.

    Plenty of the archive material legitimately carries high-bit bytes -- the
    unaxcess docs, fortunes.dat, several C sources -- and must not be touched.
    The two are told apart by DECODING: legacy 8-bit content is not valid
    UTF-8, so a text file that decodes cleanly AND has a high-bit byte was
    almost certainly typed on a modern machine.
    """
    bad = []
    for dirpath, _, names in os.walk(root):
        for name in names:
            path = os.path.join(dirpath, name)
            try:
                data = open(path, "rb").read()
            except OSError:
                continue
            if not is_text(data) or not any(b > 127 for b in data):
                continue
            try:
                data.decode("utf-8")
            except UnicodeDecodeError:
                continue                     # legacy 8-bit: leave it alone
            bad.append(os.path.relpath(path, root))
    for path in sorted(bad):
        print("    UTF-8 on an 8-bit disk: %s" % path)
    return not bad, "%d file(s) carry UTF-8" % len(bad)


AUTHOR_STAMP   = b"from the disk of"
STAMPED_KNOWN  = 15     # notes/FREEWARE-REBAKE.md: 224 -> 15, each documented


def check_author_stamps(root):
    """Fail if more modules carry the SDK author stamp than the known 15.

    The SDK copy these were built with has a 64-byte `Author` psect added to
    its `cstart.r`, so every binary built through it is stamped with whoever
    owns that copy. Removing them was the point of the rebake: 224 down to 15,
    and those 15 are listed in notes/FREEWARE-REBAKE.md with a reason each --
    no source, or rebuilding would regress a working program.

    The count is asserted rather than the names, so rebuilding one of the 15
    is not a failure but reintroducing a stamp is. Note the file must be read
    in Python: `grep -r` here is ugrep, which skips binary files and reports
    a confident zero.
    """
    stamped = []
    for dirpath, _, names in os.walk(root):
        for name in names:
            path = os.path.join(dirpath, name)
            try:
                if AUTHOR_STAMP in open(path, "rb").read():
                    stamped.append(os.path.relpath(path, root))
            except OSError:
                continue
    if len(stamped) > STAMPED_KNOWN:
        for path in sorted(stamped):
            print("    stamped: %s" % path)
    return (len(stamped) <= STAMPED_KNOWN,
            "%d modules stamped, %d documented" % (len(stamped), STAMPED_KNOWN))


LEFTOVERS = (".swp", ".swo", ".bak", ".rej", "~", ".DS_Store", ".pyc")
LEFTOVER_NAMES = ("core", "Thumbs.db", ".DS_Store")


def check_no_leftovers(root):
    """Fail on editor and host litter that has landed in the disk tree.

    `mkimage.sh` reads `disk/` straight off the filesystem, so .gitignore does
    not protect the image: a stray file here is baked into what ships. A vim
    swap file is the one that actually happened, and it carried the host
    username inside it.

    `.orig` is deliberately NOT in this list. Thirteen `Makefile.orig` files
    are pristine upstream makefiles kept beside their OS-9 adaptations, which
    is provenance worth having, not litter.
    """
    bad = []
    for dirpath, _, names in os.walk(root):
        for name in names:
            if name in LEFTOVER_NAMES or name.endswith(LEFTOVERS):
                bad.append(os.path.relpath(os.path.join(dirpath, name), root))
    for path in sorted(bad):
        print("    leftover: %s  (close the editor, or delete it)" % path)
    return not bad, "%d editor/host leftover(s) in the tree" % len(bad)


def check_index_names(root):
    index = os.path.join(root, "DOC", "INDEX")
    words = set(re.findall(r"[A-Za-z0-9_.]+",
                open(index, "rb").read().decode("latin-1")))
    missing = [os.path.join(d, n)
               for d in CMD_DIRS
               for n in sorted(os.listdir(os.path.join(root, d)))
               if os.path.isfile(os.path.join(root, d, n)) and n not in words]
    for m in missing:
        print("    not in DOC/INDEX: %s" % m)
    return not missing, "%d command(s) missing from DOC/INDEX" % len(missing)


def check_counts(root):
    """The counts quoted in readme and DOC/INDEX must match the tree.

    They had drifted: the readme opened with "409 programs that run", a figure
    no combination of directories produces, and INDEX's section headers were
    two short. Numbers in prose rot silently, so the ones that matter are
    derived here and compared.

      total   = files in CMDS and CMDS/GAMES
      starred = the names listed in INDEX's own "All N" block
      plain   = total - starred, the ones needing no Microware module
    """
    total = sum(1 for d in CMD_DIRS
                  for n in os.listdir(os.path.join(root, d))
                  if os.path.isfile(os.path.join(root, d, n)))

    text  = open(os.path.join(root, "DOC", "INDEX"), "rb").read().decode("latin-1")
    lines = text.replace("\r", "\n").split("\n")
    start = next(i for i, l in enumerate(lines)
                 if l.startswith("All ") and "verified" in l)
    starred = set()
    for l in lines[start+1:]:
        if l.startswith("---") or l.startswith("/dd"):
            break
        starred.update(l.split())

    readme = open(os.path.join(root, "readme"), "rb").read().decode("latin-1")
    want = {str(total), str(total - len(starred)), str(len(starred))}
    missing = [n for n in want if n not in readme]

    # INDEX's own "All N" wording must agree with the list under it.
    declared = int(re.match(r"All (\d+)", lines[start]).group(1))

    ok = not missing and declared == len(starred)
    if not ok:
        print("    tree: %d programs, %d starred, %d need nothing else"
              % (total, len(starred), total - len(starred)))
        if missing:
            print("    readme does not mention: %s" % ", ".join(sorted(missing)))
        if declared != len(starred):
            print("    DOC/INDEX says 'All %d' but lists %d" % (declared, len(starred)))
    return ok, "documented counts disagree with the tree"


def check_depends(root):
    gen = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen_depends.py")
    done = subprocess.run([sys.executable, gen, root, "--check"],
                          capture_output=True, text=True)
    if done.returncode:
        print("    " + done.stdout.strip())
    return done.returncode == 0, "DOC/DEPENDS is stale"


CHECKS = [
    ("line endings are CR-only", check_line_endings),
    ("no UTF-8 on an 8-bit disk", check_no_utf8),
    ("no editor or host leftovers", check_no_leftovers),
    ("no new SDK author stamps", check_author_stamps),
    ("every command is in DOC/INDEX", check_index_names),
    ("documented counts match the tree", check_counts),
    ("DOC/DEPENDS is up to date", check_depends),
]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: check_disk.py <disk-tree>")
    root = sys.argv[1]
    if not os.path.isdir(os.path.join(root, "CMDS")):
        raise SystemExit("not a disk tree (no CMDS): %s" % root)

    failed = 0
    for label, check in CHECKS:
        ok, complaint = check(root)
        print("  %-32s %s" % (label, "ok" if ok else "FAILED -- " + complaint))
        failed += not ok

    raise SystemExit(1 if failed else 0)
