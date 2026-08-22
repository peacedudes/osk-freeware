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

  7. EVERY PROGRAM HAS A CATEGORY. tools/categories.psv drives the guide;
     a program missing from it is invisible to anyone browsing by purpose.

  8. DOC/DEPENDS IS UP TO DATE. It is generated, and drifts the moment
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
STAMPED_KNOWN = 0   # was 15; rdoggett's name was taken out 2026-08-20


def check_author_stamps(root):
    """Fail if ANY module carries the SDK author stamp.

    Was "no more than the known 15" until 2026-08-20, when rdoggett asked for
    his name taken out of the binaries. Five were rebuilt or removed; the other
    eleven could not be rebuilt (no source, or source that will not build here)
    and were edited instead -- the Author psect is DATA and the replacement is
    the same length, so nothing in the module moved and only the CRC changed.
    tools/blank_author.py does it and re-verifies CRC and header parity.

    The threshold is now ZERO. A stamp reappearing means something was built
    against an SDK whose cstart still carries one.

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
LEFTOVER_NAMES = ("core", "Thumbs.db", ".DS_Store",
                  # shells write these into $HOME, which is /dd. Running the
                  # tree directly leaves a session's history in the source.
                  ".bash_history", ".sh_history", ".pdksh_hist", ".ksh_history")


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
    """Every command under CMDS must be named in DOC/INDEX.

    This walks the WHOLE of CMDS, not just CMD_DIRS. Checking only the two
    counted directories meant a new subdirectory documented nothing and still
    passed: CMDS/UUCP arrived with eighteen programs and all eight checks
    stayed green until this was widened.

    KNOWN WEAKNESS, measured 2026-08-22 and left alone deliberately. The test
    is "the name appears as a word anywhere in DOC/INDEX", including inside
    ordinary prose -- so a program whose name is an English word can pass
    without being documented at all. `about` did exactly that, on the strength
    of "says more about each one".

    Tightening it to "appears as an entry line" was tried and is WRONG: INDEX
    documents in at least four shapes -- entry lines, four-per-line name grids
    for the 169 netpbm converters, single-spaced runs like
    `GCC139 (7) gcc gcc_cc1 gcc_cc1plus ...`, and the star grid. A stricter
    rule reported 14 programs as undocumented and every one of them was in
    fact documented. False alarms are worse than this hole, because they train
    people to ignore the check.

    The real protection is `about <program>`, which shows a reader at once
    whether a program has an entry, a category, an origin, source and docs.
    """
    index = os.path.join(root, "DOC", "INDEX")
    words = set(re.findall(r"[A-Za-z0-9_.]+",
                open(index, "rb").read().decode("latin-1")))
    missing = []
    for dirpath, _, names in os.walk(os.path.join(root, "CMDS")):
        if os.path.basename(dirpath) == "archives":   # the original tarballs
            continue
        for n in sorted(names):
            if os.path.isfile(os.path.join(dirpath, n)) and n not in words:
                missing.append(os.path.relpath(os.path.join(dirpath, n), root))
    for m in missing:
        print("    not in DOC/INDEX: %s" % m)
    return not missing, "%d command(s) missing from DOC/INDEX" % len(missing)


def check_star_grid(root):
    """DOC/INDEX's star grid must say how many names it holds, and be right.

    THIS REPLACED `documented counts match the tree`, 2026-08-22, on rdoggett's
    instruction: "avoid putting actual numbers of anything in the docs ...
    Suppose we release the collection, and somebody writes sometime later
    offering us a new trove? It's a constant update nightmare, just so we can
    say 99 million sold."

    He is right, and the old check was the evidence: it existed only because
    hand-written counts in `readme` and `DOC/INDEX` drifted every time the tree
    changed, and keeping them true cost an edit in five files per removal. The
    counts are gone from the prose now. `DOC/CATEGORIES` and the catalogue are
    generated and can carry numbers safely; prose cannot.

    What is still worth checking is INTERNAL consistency, which costs nobody
    an edit: the grid announces "All N" and must then list N names, and every
    name must be a real file under CMDS. That catches the failure the grid
    actually has -- `gzipcpu32k_csl` and `head` once sat in it as the single
    run-together token `gzipcpu32k_cslhead`, which kept the count agreeing with
    itself while naming a program that does not exist and losing one that does.
    """
    text = open(os.path.join(root, "DOC", "INDEX"), "rb").read().decode("latin-1")
    lines = text.replace("\r", "\n").split("\n")
    try:
        start = next(i for i, l in enumerate(lines)
                     if l.startswith("All ") and "verified" in l)
    except StopIteration:
        return False, "DOC/INDEX has no 'All N' star grid"

    claimed = int(re.match(r"All (\d+)", lines[start]).group(1))
    names = []
    for l in lines[start + 1:]:
        if l.startswith("---") or l.startswith("/dd"):
            break
        names.extend(l.split())

    where = set()
    for d, _, fs in os.walk(os.path.join(root, "CMDS")):
        where.update(fs)
    missing = sorted(n for n in names if n not in where)

    ok = True
    if len(names) != claimed:
        print("    grid says All %d but lists %d names" % (claimed, len(names)))
        ok = False
    if len(set(names)) != len(names):
        dup = sorted({n for n in names if names.count(n) > 1})
        print("    duplicated in the grid: %s" % ", ".join(dup[:6]))
        ok = False
    for n in missing:
        print("    starred in DOC/INDEX but no such file: %s" % n)
    return (ok and not missing), "the star grid disagrees with itself or the tree"


def check_categories(root):
    """Every program on the disk must have a category in tools/categories.psv.

    Delegated to gen_catalog.py, which owns the rule. Without this a new
    program joins the disk and lands nowhere in the guide -- visible in the
    alphabetical index and invisible to anyone browsing by what they want.
    """
    gen = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen_catalog.py")
    done = subprocess.run([sys.executable, gen, root, "--check"],
                          capture_output=True, text=True)
    if done.returncode:
        print("    " + done.stdout.strip().replace("\n", "\n    "))
    return done.returncode == 0, "some programs have no category"


def check_depends(root):
    gen = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen_depends.py")
    done = subprocess.run([sys.executable, gen, root, "--check"],
                          capture_output=True, text=True)
    if done.returncode:
        print("    " + done.stdout.strip())
    return done.returncode == 0, "DOC/DEPENDS is stale"


def check_src_screened(root):
    """No unreviewed Microware material in the shipped source trees.

    `tools/screen_microware.py` existed and was run on candidates BEFORE they
    were installed. It had never been run over what was already on the disk,
    and on 2026-08-21 that turned out to matter: `disk/SRC/msfm` was 21 files
    of OS-9 file-manager internals, byte-identical to EFFO forum disk 12,
    whose `note.doc` -- a sibling of the SRC/ directory somebody copied, and
    therefore left behind -- carries Microware's proprietary-confidential
    notice. It shipped for months.

    Only the STRONG rules count here: an identical or heavily-overlapping SDK
    file, an ownership claim, or system-source symbols. The NAME rule alone
    matches 212 files under disk/SRC -- every `makefile` and `string.h` in the
    collection -- and a check that cries wolf 212 times is one nobody reads.

    Accepted files are listed, with reasons, in tools/screened-src.txt.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    screen = os.path.join(here, "screen_microware.py")
    allow = os.path.join(here, "screened-src.txt")

    # Entries are stored the way a person would type them, `disk/SRC/...`,
    # but the tree being checked is not always called `disk`: mkimage.sh
    # builds a copy elsewhere for the "does it work with no Microware modules
    # present" release check, and that must not fail on path spelling alone.
    # So compare on the part below the tree root.
    known = set()
    if os.path.exists(allow):
        for line in open(allow):
            line = line.strip()
            if line and not line.startswith("#"):
                known.add(line.split("/", 1)[1] if "/" in line else line)

    src = os.path.join(root, "SRC")
    if not os.path.isdir(src):
        return True, ""
    files = [os.path.join(r, f) for r, _, fs in os.walk(src) for f in fs]
    done = subprocess.run([sys.executable, screen, "-q"] + files,
                          capture_output=True, text=True)

    STRONG = ("SYSTEM SOURCE", "IDENTICAL to", "Microware copyright",
              "proprietary", "% of its lines")
    bad, path = [], None
    for line in done.stdout.splitlines():
        if line.startswith("FLAG"):
            path = line.split(None, 1)[1].strip()
        elif path and any(s in line for s in STRONG):
            if os.path.relpath(path, root) not in known:
                bad.append((path, line.strip()))
            path = None
    for p, why in bad:
        print("    %s\n      %s" % (p, why))
    if bad:
        print("    Read each one. If it is all right, add it to"
              " tools/screened-src.txt with the reason.")
    return not bad, "unreviewed Microware material under SRC"


CHECKS = [
    ("line endings are CR-only", check_line_endings),
    ("no UTF-8 on an 8-bit disk", check_no_utf8),
    ("no editor or host leftovers", check_no_leftovers),
    ("no new SDK author stamps", check_author_stamps),
    ("every command is in DOC/INDEX", check_index_names),
    ("the star grid is self-consistent", check_star_grid),
    ("every program has a category", check_categories),
    ("DOC/DEPENDS is up to date", check_depends),
    ("no unscreened Microware source", check_src_screened),
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
