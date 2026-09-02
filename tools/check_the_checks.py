#!/usr/bin/env python3
"""Make every `check_disk.py' check FAIL once, mechanically.

    tools/check_the_checks.py            # all of them
    tools/check_the_checks.py star docs  # just the ones whose id matches

Why this exists
---------------
`check_disk.py' is the gate on every commit in this collection, and this
collection's own rule -- written down in CLAUDE.md after it was learnt the
hard way several times -- is MAKE EVERY CHECK FAIL ONCE BEFORE BELIEVING IT.
That had never been done for the gate itself.

The tree has produced a remarkable number of checks that could not fail: a
verifier that reported 20/20 OK having run nothing, because `tr' had fallen
out of PATH; a builder that reported "copied 3287/3287" while every copy
failed; a magic-number test that skipped every file because `od' separates
bytes with two spaces and the grep looked for one.  And on 2026-09-01,
`worklist.py's `carded()' -- which read `for'-credited names out of the wrong
key, so the loop could never match and a headline figure was wrong for days.

So: copy the disk tree, break ONE thing, run the ONE check that should
notice, and require it to say so.  A check that stays green over a break it
is supposed to catch is reported as BLIND, which is the finding.

What a break looks like
-----------------------
Each break below is the smallest edit that ought to trip its check, and is
written to be obviously wrong rather than subtly wrong -- this tool is
asking "does the check fire at all", not "how sensitive is it".

The copy is made once, mutated and restored in place per check, and removed
at the end.  Nothing under `disk/' is touched.
"""
import os
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECKER = os.path.join(REPO, "tools", "check_disk.py")


def w(path, data):
    with open(path, "wb") as fh:
        fh.write(data)


def add_line_ending(root):
    """A single LF in a DOC file: OS-9 text is CR-terminated."""
    p = os.path.join(root, "DOC", "INDEX")
    w(p, open(p, "rb").read() + b"a line ending the wrong way\n")
    return "DOC/INDEX given one LF-terminated line"


def add_utf8(root):
    p = os.path.join(root, "DOC", "INDEX")
    w(p, open(p, "rb").read() + "an em dash — here\r".encode("utf-8"))
    return "DOC/INDEX given a UTF-8 em dash"


def add_leftover(root):
    p = os.path.join(root, "DOC", "INDEX~")
    w(p, b"an editor backup\r")
    return "DOC/INDEX~ created (an editor leftover)"


def add_build_litter(root):
    p = os.path.join(root, "SRC", "R_something")
    w(p, b"\x4a\xfc\x00\x00")
    return "SRC/R_something created (a build product)"


def break_index_names(root):
    """A command with no line in DOC/INDEX."""
    p = os.path.join(root, "CMDS", "zzznosuchprogram")
    shutil.copy(os.path.join(root, "CMDS", "cat"), p)
    return "CMDS/zzznosuchprogram added and not indexed"


def break_star_grid(root):
    """Put a name in the grid that is not a program."""
    p = os.path.join(root, "DOC", "INDEX")
    t = open(p, "rb").read().decode("latin-1")
    t = t.replace("All 349,", "All 350,", 1)
    w(p, t.encode("latin-1"))
    return "the star grid's stated count moved by one"


def break_categories(root):
    p = os.path.join(root, "CMDS", "zzzuncategorised")
    shutil.copy(os.path.join(root, "CMDS", "cat"), p)
    return "CMDS/zzzuncategorised added with no category"


def break_depends(root):
    p = os.path.join(root, "DOC", "DEPENDS")
    w(p, open(p, "rb").read().replace(b"\r", b"\r", 1) + b"stale\r")
    return "DOC/DEPENDS given an extra line"


def break_binary_magic(root):
    """A JPEG that no longer starts like one.

    `binaries start with their magic' is EXTENSION-driven and an OS-9 module
    has no extension, so blanking `CMDS/cat' -- which the first version of
    this break did -- proved nothing about it. That miss is what earned the
    `every command is a real module' check below.
    """
    for base, _, files in os.walk(os.path.join(root, "SRC")):
        for f in files:
            if f.lower().endswith((".jpg", ".gif")):
                p = os.path.join(base, f)
                d = bytearray(open(p, "rb").read())
                d[0] = 0x00
                w(p, bytes(d))
                return "%s's magic number blanked" % f
    return None


def break_module_magic(root):
    """An OS-9 module whose $4AFC is gone."""
    p = os.path.join(root, "CMDS", "cat")
    d = bytearray(open(p, "rb").read())
    d[0] = 0x00
    w(p, bytes(d))
    return "CMDS/cat's module sync bytes blanked"


def break_module_names(root):
    """Two files registering one module name."""
    shutil.copy(os.path.join(root, "CMDS", "cat"),
                os.path.join(root, "CMDS", "zzzcatcopy"))
    return "CMDS/zzzcatcopy added, a second file claiming module `cat'"


def break_docs(root):
    p = os.path.join(root, "DOC", "INDEX")
    w(p, b"")
    return "DOC/INDEX truncated to zero bytes"


def break_readme_refs(root):
    p = os.path.join(root, "DOC", "README")
    t = open(p, "rb").read()
    w(p, t + b"  README-NOSUCHTHING   a document that does not exist\r")
    return "DOC/README made to name README-NOSUCHTHING"


def break_card_dependency(root):
    """A card made to read a file only another card writes.

    This one edits `tools/screenshots', not the disk tree -- the check reads
    the sheets, not `disk/'. The tool restores it from the pristine copy
    like everything else, but the copy is of `disk/', so this break is
    undone by hand below.
    """
    return None


def break_hand_files(root):
    """DOC/USAGE, not DOC/STATUS.

    The first version of this break edited DOC/STATUS and the check stayed
    green -- correctly: it reads `tools/howto.psv', `tools/categories.psv'
    and `disk/DOC/USAGE', and says so in its own docstring. A break outside
    a check's stated scope proves nothing about the check.
    """
    p = os.path.join(root, "DOC", "USAGE")
    w(p, open(p, "rb").read()
      + b"\r  zzznosuchprogram   (CMDS)\r      Syntax: zzznosuchprogram\r")
    return "DOC/USAGE made to name a program that is not there"


BREAKS = [
    ("line endings", "line endings are CR-only", add_line_ending),
    ("utf8", "no UTF-8 on an 8-bit disk", add_utf8),
    ("leftovers", "no editor or host leftovers", add_leftover),
    ("build litter", "no build products in the tree", add_build_litter),
    ("index names", "every command is in DOC/INDEX", break_index_names),
    ("star grid", "the star grid is self-consistent", break_star_grid),
    ("categories", "every program has a category", break_categories),
    ("depends", "DOC/DEPENDS is up to date", break_depends),
    ("binary magic", "binaries start with their magic", break_binary_magic),
    ("module magic", "every command is a real module", break_module_magic),
    ("module names", "one module name, one file", break_module_names),
    ("docs intact", "the disk's documents are intact", break_docs),
    ("readme refs", "README names documents that exist", break_readme_refs),
    ("name lists", "name lists point at real programs", break_hand_files),
    # `cards do not depend on each other' is NOT probed here: its input is
    # tools/screenshots, not the disk tree this tool copies, so a break
    # would edit the live sheets. It was made to fail by hand on
    # 2026-09-01 -- put `fcomp' back on `cdiff's leftovers and it reports
    # two cards -- and that is recorded rather than automated, because a
    # prober that edits files outside its own copy is a worse idea than an
    # unprobed check.
]


def run_checker(root):
    out = subprocess.run([sys.executable, CHECKER, root],
                         capture_output=True, text=True)
    return out.stdout


def failing_labels(text):
    """The labels of the checks that FAILED.

    NOT `split("  ")': `check_disk' prints `"  %-32s %s"', so a label of 32
    characters or more leaves exactly ONE space before `FAILED' and a
    two-space split returns the whole line. Two checks are that long, and
    the first version of this tool reported both as blind when they had
    fired perfectly -- which is the same class of bug this tool exists to
    find, in the tool itself.
    """
    out = set()
    for ln in text.split("\n"):
        if "FAILED" in ln:
            out.add(ln.strip().rsplit("FAILED", 1)[0].strip())
    return out


def main(argv):
    want = [a.lower() for a in argv]
    work = tempfile.mkdtemp(prefix="checkprobe.")
    root = os.path.join(work, "disk")
    print("copying the tree to %s ..." % root)
    shutil.copytree(os.path.join(REPO, "disk"), root, symlinks=True)

    base = run_checker(root)
    if failing_labels(base):
        print("THE COPY DOES NOT START GREEN -- nothing below means anything:")
        print(base)
        shutil.rmtree(work, ignore_errors=True)
        return 2

    blind, fired = [], 0
    for ident, label, breaker in BREAKS:
        if want and not any(k in ident for k in want):
            continue
        pristine = os.path.join(work, "pristine")
        shutil.rmtree(pristine, ignore_errors=True)
        shutil.copytree(root, pristine, symlinks=True)
        what = breaker(root)
        failing = failing_labels(run_checker(root))
        ok = label in failing
        print("  %-34s %s   (%s)"
              % (label, "fails as it should" if ok else "DID NOT FIRE", what))
        if ok:
            fired += 1
        else:
            blind.append((label, what, sorted(failing)))
        shutil.rmtree(root)
        shutil.move(pristine, root)

    shutil.rmtree(work, ignore_errors=True)
    print("\n%d of %d breaks were caught by the check meant to catch them"
          % (fired, fired + len(blind)))
    for label, what, other in blind:
        print("  BLIND: %s did not notice %s" % (label, what))
        if other:
            print("         (these fired instead: %s)" % ", ".join(other))
    return 1 if blind else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
