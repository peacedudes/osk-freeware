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
import re
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
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
    """Move the grid's stated count by one.

    THE COUNT IS READ, NOT TYPED.  This said `All 349,' until 2026-09-02,
    when dropping two programs made it 347 and the break silently stopped
    breaking anything -- the tool reported the check BLIND, which is the
    right answer to the wrong question. A prober that hardcodes a figure
    from the tree it probes rots the first time the tree moves.
    """
    p = os.path.join(root, "DOC", "INDEX")
    t = open(p, "rb").read().decode("latin-1")
    m = re.search(r"All (\d+),", t)
    if not m:
        return None
    n = int(m.group(1))
    t = t.replace("All %d," % n, "All %d," % (n + 1), 1)
    w(p, t.encode("latin-1"))
    return "the star grid's stated count moved by one (%d -> %d)" % (n, n + 1)


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


def break_pathlists(root):
    """A card caption made to carry a full pathlist.

    Like `break_card_dependency', this reads `tools/screenshots', not the
    disk copy, so it is verified by hand rather than auto-probed: on
    2026-09-05, inserting `cap  reads /dd/CMDS/gnuchess' into games.sheet
    made `cards carry no full pathlists' report one, and removing it made it
    pass.  Not automated, for the same reason as the card-dependency check.
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


def break_author_stamp(root):
    """The SDK author stamp, put back into a module.

    `no new SDK author stamps' has a threshold of ZERO and searches every
    file in the tree for one byte string, so the smallest honest break is to
    append it to a module. The module is left invalid by that (its CRC no
    longer covers the tail) which does not matter here: the stamp check runs
    on bytes and this tool restores the file straight after.
    """
    p = os.path.join(root, "CMDS", "cat")
    w(p, open(p, "rb").read() + b"from the disk of somebody or other")
    return "CMDS/cat given the SDK author stamp"


def break_recipe_tree(root):
    """A source tree a recipe names, renamed out from under it.

    This is the exact shape the check was written for: a program removed and
    its recipe left behind, which `rebuild.sh' then reports as a FAILED
    BUILD rather than as the leftover it is. Any tree named by a recipe will
    do, so the first one is taken from the recipe file itself rather than
    typed here -- a name typed here would rot the day that program moved.
    """
    recipes = os.path.join(REPO, "tools", "rebuild", "recipes.psv")
    src = os.path.join(root, "SRC")
    for line in open(recipes):
        if line.startswith("#") or "|" not in line:
            continue
        tree = line.split("|")[1].strip().split("/")[0]
        if tree and os.path.isdir(os.path.join(src, tree)):
            os.rename(os.path.join(src, tree),
                      os.path.join(src, "zzz" + tree))
            return "SRC/%s renamed, leaving its recipes pointing nowhere" % tree
    return None


def break_screened_source(root):
    """A file under SRC that names OS-9 system internals.

    `no unscreened Microware source' only acts on the STRONG rules, and
    SYSTEM SOURCE wants TWO distinct system symbols in one source file --
    which is what `disk/SRC/msfm' had, and what shipped for months. Two
    system-globals offsets in a .c file is the smallest thing that is
    honestly that.
    """
    p = os.path.join(root, "SRC", "zzzsysglob.c")
    w(p, b"/* offsets into the OS-9 system globals */\r"
         b"#define SYSGLOB_MODDIR  D_ModDir\r"
         b"#define SYSGLOB_PRCDBT  D_PrcDBT\r"
         b"#define SYSGLOB_BLKMAP  D_BlkMap\r")
    return "SRC/zzzsysglob.c added, naming three system globals"


def break_login_env(root):
    """SYS/login made to disagree with the harness's copy of it.

    The drift this catches actually happened: login was changed to
    `SHELL=$ROOT/CMDS/ksh' -- the one shell here whose invocation serves
    system() -- and `tools/screenshots.py's hand-written copy still said
    bash, so the `latex' card was a capture of E$PNNF while the program
    worked. Putting bash back is that drift exactly.
    """
    p = os.path.join(root, "SYS", "login")
    t = open(p, "rb").read()
    if b"CMDS/ksh" not in t:
        return None
    w(p, t.replace(b"CMDS/ksh", b"CMDS/bash", 1))
    return "SYS/login made to export SHELL=bash again"


def break_cio_scan(root):
    """A name the cio-macro scan is required to find, removed.

    Taking a guard name off the disk is the "scan has stopped working"
    case, which is the failure the guard exists for -- a silent scan agrees
    with any number in README-CIO.

    This used to remove `CMDS/REBUILT/kermit_cio', picked as the one name
    that could never be rebuilt away. It was dropped from the collection on
    2026-09-12 as a duplicate, which is a way for a guard to expire that
    nobody had allowed for, and this breaker returned None -- silently
    testing nothing -- until it was repointed. `liborder' is the guard now.
    """
    p = os.path.join(root, "CMDS", "liborder")
    if not os.path.exists(p):
        return None
    os.remove(p)
    return "CMDS/liborder removed, so the scan's guard is gone"



def break_panel_backlog_forgets(root):
    """A failing program on neither list: the gate must miss it.

    While the backlog had names, dropping one was the break.  It emptied on
    2026-09-04 and this breaker crashed on names[0] -- the tool that exists
    to prove checks can fail had stopped being able to run.  Now, with an
    empty backlog, the same failure is made by taking a program OFF the
    exceptions list instead: it fails the audit and is on neither file.
    """
    import audit_panels
    work = os.path.dirname(root)
    src = os.path.join(REPO, "tools", "panel-backlog.txt")
    names = [l.strip() for l in open(src) if l.strip() and not l.startswith("#")]
    if names:
        copy = os.path.join(work, "panel-backlog.txt")
        open(copy, "w").write("\n".join(names[1:]) + "\n")
        os.environ["OSK_PANEL_BACKLOG"] = copy
        return "`%s' dropped from a COPY of panel-backlog.txt" % names[0]
    exc = os.path.join(REPO, "tools", "panel-exceptions.psv")
    rows = [l for l in open(exc) if l.strip() and not l.startswith("#")]
    copy = os.path.join(work, "panel-exceptions.psv")
    open(copy, "w").write("".join(rows[1:]))
    os.environ["OSK_PANEL_EXCEPTIONS"] = copy
    return "`%s' dropped from a COPY of panel-exceptions.psv" % rows[0].split("|")[0]


def break_panel_backlog_stale(root):
    """A passing program ADDED to the backlog: the ratchet must object."""
    import audit_panels
    src = os.path.join(REPO, "tools", "panel-backlog.txt")
    passing = next(p for p, v, _ in audit_panels.audit() if v == "work")
    copy = os.path.join(os.path.dirname(root), "panel-backlog.txt")
    open(copy, "w").write(open(src).read() + passing + "\n")
    os.environ["OSK_PANEL_BACKLOG"] = copy
    return "`%s' (which passes) added to a COPY of panel-backlog.txt" % passing


def break_try_backlog_forgets(root):
    """A stanza with no `try' line dropped from a COPY of the backlog."""
    src = os.path.join(REPO, "tools", "try-backlog.txt")
    names = [l.strip() for l in open(src) if l.strip() and not l.startswith("#")]
    if not names:
        return None
    copy = os.path.join(os.path.dirname(root), "try-backlog.txt")
    open(copy, "w").write("\n".join(names[1:]) + "\n")
    os.environ["OSK_TRY_BACKLOG"] = copy
    return "`%s' dropped from a COPY of try-backlog.txt" % names[0]


def break_try_backlog_stale(root):
    """A stanza that HAS a `try' line added to a COPY of the backlog."""
    import screenshots
    src = os.path.join(REPO, "tools", "try-backlog.txt")
    sheets = os.path.join(REPO, "tools", "screenshots")
    has = next(s["name"] for f in sorted(os.listdir(sheets)) if f.endswith(".sheet")
               for s in screenshots.parse(os.path.join(sheets, f)) if s.get("try"))
    copy = os.path.join(os.path.dirname(root), "try-backlog.txt")
    open(copy, "w").write(open(src).read() + has + "\n")
    os.environ["OSK_TRY_BACKLOG"] = copy
    return "`%s' (which has a try line) added to a COPY of try-backlog.txt" % has


def break_help_backlog_forgets(root):
    """A program on neither list: the gate must miss it.

    While the backlog had names, dropping one was the break.  It emptied
    on 2026-09-09, so the same failure is made the other way round: a
    line is dropped from a COPY of help.psv, which OSK_HELP_TABLE points
    the gate at, and that program is then on neither file.
    """
    src = os.path.join(REPO, "tools", "help-backlog.txt")
    names = [l.strip() for l in open(src) if l.strip() and not l.startswith("#")]
    work = os.path.dirname(root)
    if names:
        copy = os.path.join(work, "help-backlog.txt")
        open(copy, "w").write("\n".join(names[1:]) + "\n")
        os.environ["OSK_HELP_BACKLOG"] = copy
        return "`%s' dropped from a COPY of help-backlog.txt" % names[0]
    table = os.path.join(REPO, "tools", "help.psv")
    rows = open(table).read().split("\n")
    i = next(i for i, r in enumerate(rows) if r.strip() and not r.startswith("#"))
    copy = os.path.join(work, "help.psv")
    open(copy, "w").write("\n".join(rows[:i] + rows[i + 1:]))
    os.environ["OSK_HELP_TABLE"] = copy
    return "`%s' dropped from a COPY of help.psv" % rows[i].split("|")[0]


def break_help_truncated(root):
    """A capture cut off at `Options:' in a COPY of docs/help -- the roff
    scrape, re-enacted."""
    import helpcap
    name = next((n for n, (c, _) in helpcap.load_table().items()
                 if c and os.path.exists(os.path.join(helpcap.HELPDIR, n + ".txt"))), None)
    if name is None:
        return None
    copy = os.path.join(os.path.dirname(root), "help")
    shutil.copytree(helpcap.HELPDIR, copy)
    path = os.path.join(copy, name + ".txt")
    lines = open(path).read().split("\n")
    open(path, "w").write("\n".join(lines[:2] + ["Options:"]) + "\n")
    os.environ["OSK_HELP_DIR"] = copy
    return "`%s's capture cut off after `Options:' in a COPY of docs/help" % name


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
    ("author stamps", "no new SDK author stamps", break_author_stamp),
    ("recipes", "every recipe names a real tree", break_recipe_tree),
    ("screened src", "no unscreened Microware source",
     break_screened_source),
    ("login env", "harness env matches SYS/login", break_login_env),
    ("cio macro", "the cio-macro list is current", break_cio_scan),
    # Both directions of the ratchet, through a COPY of the backlog that
    # OSK_PANEL_BACKLOG points the gate at -- the live file is never edited.
    ("panel forgets", "panels show their own program", break_panel_backlog_forgets),
    ("panel stale", "panels show their own program", break_panel_backlog_stale),
    ("try forgets", "every card says what to type", break_try_backlog_forgets),
    ("try stale", "every card says what to type", break_try_backlog_stale),
    ("help forgets", "cards carry real help text", break_help_backlog_forgets),
    ("help truncated", "cards carry real help text", break_help_truncated),
    # `one line per name in the hand lists' is NOT probed here: its input is
    # tools/howto.psv and tools/categories.psv, not the disk tree this tool
    # copies, so a break would edit the live lists. It was made to fail by
    # hand on the day it was written -- it found `about' twice in
    # categories.psv and fifteen names twice in howto.psv, which is how it
    # earned its place -- and that is recorded rather than automated, for
    # the same reason as the card-dependency check above.
    # NINETEEN of the twenty checks are probed above, as of 2026-09-01.
    # Five of them were added that day, and every one fired first time --
    # which is the boring outcome and the one worth recording, because the
    # five that came before had all needed a second try.
    #
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
        if what is None:
            # The break cannot be built from the tree as it stands -- the
            # try-line backlog emptied on 2026-09-09 and there is no stanza
            # left to drop from it.  That is not blindness; say so and
            # move on rather than count a check that was never probed.
            print("  %-34s not applicable   (nothing left to break with)" % label)
            shutil.rmtree(root)
            shutil.move(pristine, root)
            continue
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
        os.environ.pop("OSK_PANEL_BACKLOG", None)
        os.environ.pop("OSK_PANEL_EXCEPTIONS", None)
        os.environ.pop("OSK_TRY_BACKLOG", None)
        os.environ.pop("OSK_HELP_BACKLOG", None)
        os.environ.pop("OSK_HELP_DIR", None)
        os.environ.pop("OSK_HELP_TABLE", None)
        shutil.rmtree(os.path.join(work, "help"), ignore_errors=True)

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
