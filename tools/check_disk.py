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



def tools_dir():
    """Where the hand-maintained tables and sheets live.

    OSK_TOOLS_DIR points this at a COPY, which is how check_the_checks
    breaks a check that reads tools/ rather than the disk tree.  Without
    it such a check reads the real tools/ whatever tree it is handed, and
    so can never be made to fail -- six were in that position until
    2026-09-19, one of them with a docstring saying a breaker was
    impossible.
    """
    return os.environ.get("OSK_TOOLS_DIR",
                          os.path.dirname(os.path.abspath(__file__)))


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


def check_no_build_litter(root):
    """No build product may be sitting in the tree that becomes the image.

    Added 2026-08-22, after `tools/build.sh` was run for the first time on a
    clean checkout. Every recipe compiles IN PLACE -- cc writes `foo.r' beside
    `foo.c' and the linked module as `R_<prog>' -- and `mkimage.sh' reads
    `disk/' off the filesystem. So a build immediately before an image build
    shipped 77 object files, fourteen overwritten copies of the ARCHIVE's own
    `.r' files, and five `ctmp.*' temporaries cc left behind when a compile was
    interrupted.

    `.r' files cannot be screened by name: 432 of them are the archives' own
    and belong on the disk. `R_', `ctmp.' and `ctmp_' are unambiguous --
    nothing in any archive here is named any of them -- so those are what this
    looks for. The KNR path writes `ctmp_<base>.c' per source and the first
    version of this check matched only the dot, so 27 of them were committed.
    """
    bad = []
    for here, dirs, files in os.walk(root):
        for name in files:
            if (name.startswith("R_") or name.startswith("ctmp.")
                    or name.startswith("ctmp_")):
                bad.append(os.path.relpath(os.path.join(here, name), root))
    for path in sorted(bad)[:12]:
        print("    build product: %s" % path)
    if len(bad) > 12:
        print("    ... and %d more" % (len(bad) - 12))
    return not bad, "%d build product(s) left in the tree" % len(bad)


def check_recipes(root):
    """Every build recipe must name a source tree that is actually here.

    Added 2026-08-22. Removing a program leaves its recipe behind pointing at
    a tree that no longer exists, and `rebuild.sh` then reports that recipe as
    a FAILED BUILD -- which reads exactly like broken source and is not. Six
    such recipes were left over from one afternoon's removals, and two more
    (`eff_tsmon2`, `eff_indent/SRC`) had been wrong for long enough that
    nobody could say when.

    The disk itself does not carry recipes, so this checks the repository. It
    is skipped when the tree being checked is not the repository's own disk/.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    recipes = os.path.join(here, "rebuild", "recipes.psv")
    src = os.path.join(root, "SRC")
    if not (os.path.exists(recipes) and os.path.isdir(src)):
        return True, ""
    trees = set(os.listdir(src))
    bad = []
    for line in open(recipes):
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split("|")
        if len(parts) < 2:
            continue
        prog, tree = parts[0].strip(), parts[1].strip()
        if tree.split("/")[0] not in trees:
            bad.append((prog, "SRC/%s, which is not here" % tree))
            continue
        # ...and the sources it names must exist, or the recipe is for a
        # program somebody removed and its build will be reported as a FAILURE
        # rather than as the leftover it is. Nine such recipes survived one
        # afternoon's removals.
        srcs = [s for s in parts[2].split() if not s.startswith("-")]
        gone = [s for s in srcs
                if not os.path.exists(os.path.join(src, tree, s))]
        if srcs and len(gone) == len(srcs):
            bad.append((prog, "sources that are all gone from SRC/%s" % tree))
    for prog, why in bad:
        print("    recipe for %s names %s" % (prog, why))

    # A duplicate line builds the same program twice and reports it twice, so
    # a run of eleven recipes printed fifteen rows and three of the failures
    # were the same failure. It happened by appending a batch of recipes that
    # had already been appended -- silently, because nothing looked.
    seen, dup = set(), []
    for line in open(recipes):
        line = line.rstrip("\n")
        if line.startswith("#") or not line.strip():
            continue
        if line in seen:
            dup.append(line.split("|")[0])
        seen.add(line)
    for prog in dup:
        print("    recipe for %s appears more than once" % prog)
    return (not bad and not dup,
            "%d recipe(s) point at source that is gone, %d duplicated"
            % (len(bad), len(dup)))


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


def check_manpages(root):
    """DOC/MANPAGES must list the manual pages actually on the disk.

    `man' reads that index rather than searching 363 directories, so a stale
    index is a silent failure of exactly the wrong kind: the page is there,
    and `man' says there is none.  Same shape as the DEPENDS check above, and
    the same fix -- run the generator.
    """
    gen = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen_manpages.py")
    done = subprocess.run([sys.executable, gen, root, "--check"],
                          capture_output=True, text=True)
    if done.returncode:
        print("    " + done.stdout.strip())
    return done.returncode == 0, "DOC/MANPAGES is stale"


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


# Extension -> (offset, [signatures]).  Only formats with a fixed,
# unambiguous signature are listed; a guess costs more than it catches.  LZH
# is the reason this carries an offset at all: its first two bytes are a
# header length and checksum that vary per archive, and the `-lh?-' method tag
# sits at offset 2.  A first cut of this check assumed offset 0 and reported
# all seven of the tree's .lzh files as damaged.
MAGIC = {
    ".jpg":  (0, [b"\xff\xd8\xff"]),
    ".jpeg": (0, [b"\xff\xd8\xff"]),
    ".gif":  (0, [b"GIF87a", b"GIF89a"]),
    ".Z":    (0, [b"\x1f\x9d"]),
    ".gz":   (0, [b"\x1f\x8b"]),
    ".zip":  (0, [b"PK\x03\x04", b"PK\x05\x06"]),
    ".zoo":  (0, [b"ZOO "]),
    ".lzh":  (2, [b"-lh", b"-lz"]),
    ".ppm":  (0, [b"P6", b"P3"]),
    ".pgm":  (0, [b"P5", b"P2"]),
    ".pbm":  (0, [b"P4", b"P1"]),
}

# `SRC/netpbm/PGM/Makefile.pgm' is a makefile, not a greymap.  Matching on the
# extension alone called it damaged too.
MAGIC_SKIP = ("makefile",)


def check_binary_magic(root):
    """Binary files still start with the bytes their format requires.

    THIS EXISTS BECAUSE TEN FILES FAILED IT.  On 2026-08-29 every binary under
    `disk/SRC' -- two JPEGs, a GIF, a PPM, a .zoo, three compress archives and
    GNU Chess's data and hash tables -- was found to have been run through what
    the byte pattern says was an `iconv ... //TRANSLIT' and a LF->CR pass:
    every byte >= 0x80 had become `?', a `\xb0' had become the three letters
    `deg', and every LF had become a CR.  `testimg.jpg' began `???a'.  Nothing
    reported it, because the tree's own checks are about TEXT being CR-only
    and ASCII, and a mangled binary passes both with room to spare.

    All ten were restored from the archives they came from, which the pool
    still had; the LIVE copies of the GNU Chess data (GNUCHESS4.0/MISC, the
    ones gnuchessc actually reads) were byte-identical to the archive and had
    never been touched, which is why no program ever misbehaved and why this
    went unnoticed.

    Extension-driven and therefore partial: it says nothing about a file whose
    format has no signature, and nothing about content past the first bytes.
    It would have caught all ten.
    """
    bad = []
    for base, _, files in os.walk(root):
        for f in files:
            ext = os.path.splitext(f)[1]
            if ext not in MAGIC or f.lower().startswith(MAGIC_SKIP):
                continue
            path = os.path.join(base, f)
            off, sigs = MAGIC[ext]
            head = open(path, "rb").read(off + 8)
            if not any(head[off:].startswith(m) for m in sigs):
                bad.append((os.path.relpath(path, root), head[:8]))
    for rel, head in sorted(bad)[:12]:
        print("    %s starts %s" % (rel, head.hex(" ")))
    if len(bad) > 12:
        print("    ... and %d more" % (len(bad) - 12))
    return not bad, "%d file(s) do not start with their format's magic" % len(bad)



def check_hand_lists_have_no_duplicate_keys(root):
    """One line per program in `tools/howto.psv' and `tools/categories.psv'.

    Added 2026-09-02, having found FIFTEEN duplicated names in howto.psv --
    four of them added the same evening. `gen_catalog' builds a dict, so the
    LAST line silently wins and the other is dead text nobody will ever see
    again, including the one somebody carefully measured. `orbit' had two,
    and the losing one still said neither shell could move the OS-9 data
    directory, which stopped being true when `ksh -c "cd X; prog"' was
    measured on 2026-09-01.

    Nothing about a duplicate is visible in the output, which is what makes
    it worth a check rather than a habit.
    """
    # OSK_TOOLS_DIR lets check_the_checks point this at a COPY of tools/ so
    # the check can be made to fail.  A check reading the real tools/
    # whatever tree it is given cannot be broken and so has never been
    # proved able to fail, which is the one thing this collection insists on.
    here = tools_dir()
    problems = []
    for fname in ("howto.psv", "categories.psv"):
        path = os.path.join(here, fname)
        if not os.path.exists(path):
            continue
        seen = {}
        for n, line in enumerate(open(path, encoding="utf-8"), 1):
            line = line.strip()
            if not line or line.startswith("#") or "|" not in line:
                continue
            name = line.split("|", 1)[0]
            if name in seen:
                problems.append("%s: `%s' on lines %d and %d -- the later "
                                "wins and the earlier is dead text"
                                % (fname, name, seen[name], n))
            else:
                seen[name] = n
    for p in problems[:10]:
        print("    " + p)
    if problems:
        return False, "%d duplicated name(s) in the hand lists" % len(problems)
    return True, ""


def check_hand_files_name_real_programs(root):
    """tools/howto.psv, tools/categories.psv, tools/requires.psv,
    tools/shadowed-names.txt and disk/DOC/USAGE must name programs that exist.

    All three are hand-maintained or generated-then-kept, and a program removed
    from the disk leaves its lines behind.  On 2026-08-30 `howto.psv' still
    carried six: `lac', `main', `pow', `scope' and `sin' were deliberately
    dropped from the collection on 2026-08-22 and their entries were not, four
    of them still claiming "`q' quits -- tested"; `MakeTeXPK' had never been on
    the disk at all.  Nothing pointed at them, because these files are read by
    NAME -- an entry nobody looks up is an entry nobody notices.

    `shadowed-names.txt' joined on 2026-09-18.  It is what puts the warning on
    a card -- "your OS-9 has a `dir' of its own" -- so a name that has left the
    disk means a warning nobody sees, and the file is exactly the kind that
    drifts: it is measured against an SDK that is not in this repository.

    DOC/USAGE was added to this check on 2026-08-31, having been found with
    EIGHTEEN stale entries: eleven Microware-era utilities removed 2026-08-22,
    four `.nocio' REBUILT builds that no longer exist, and `input.elvis',
    renamed to `elvis_input' the same morning by the session that then found
    this.  DOC/USAGE ships on the disk, so a stale entry there is a document
    describing a program the reader does not have.
    """
    import gen_catalog
    ondisk = set()
    for d in gen_catalog.PROGRAM_DIRS:
        full = os.path.join(root, d)
        if os.path.isdir(full):
            ondisk |= {f for f in os.listdir(full)
                       if os.path.isfile(os.path.join(full, f))}
    # DOC/USAGE names programs in every directory, not only PROGRAM_DIRS.
    everywhere = set()
    for base, _, files in os.walk(os.path.join(root, "CMDS")):
        if os.path.basename(base) == "archives":
            continue
        everywhere |= set(files)

    here = os.path.dirname(os.path.abspath(__file__))
    bad = []
    for fname in ("howto.psv", "categories.psv", "requires.psv",
                  "shadowed-names.txt"):
        path = os.path.join(here, fname)
        if not os.path.exists(path):
            continue
        for line in open(path):
            if line.startswith("#") or "|" not in line:
                continue
            name = line.split("|")[0].strip()
            if name and name not in ondisk:
                bad.append("%s: %s" % (fname, name))

    usage = os.path.join(root, "DOC", "USAGE")
    if os.path.exists(usage):
        text = open(usage, "rb").read().decode("latin-1").replace("\r", "\n")
        for m in re.finditer(r"^  (\S+)\s+\((\S+)\)\s*$", text, re.M):
            if m.group(1) not in everywhere:
                bad.append("DOC/USAGE: %s" % m.group(1))
    for b in bad[:12]:
        print("    names a program that is not on the disk -- %s" % b)
    return not bad, "%d stale line(s) in a hand-maintained file" % len(bad)



# The disk's own documentation, with the size below which something has gone
# wrong.  Deliberately generous -- this is a tripwire for truncation, not a
# word count.
KEY_DOCS = {
    "DOC/INDEX": 40000, "DOC/STATUS": 30000, "DOC/DEPENDS": 20000,
    "DOC/ORIGINS": 10000, "DOC/CATEGORIES": 10000, "SOURCES.txt": 20000,
    "readme": 1000, "DOC/README-RUNNING": 3000,
}


def check_docs_not_truncated(root):
    """The disk's main documents are still their proper size.

    THIS EXISTS BECAUSE AN EMPTY FILE PASSES EVERYTHING ELSE.  On 2026-08-30
    a rewrite of DOC/STATUS left it ZERO BYTES -- `open(path, "wb")' truncates
    the moment it is evaluated, and the expression that was to be written
    raised before it produced anything.  All thirteen checks then reported ok:
    an empty file has no LF in it, no UTF-8, no leftovers and no bad magic.
    Only `git diff' caught it.

    A file that has legitimately grown past its floor should have the floor
    raised, not the check removed.
    """
    bad = []
    for rel, floor in sorted(KEY_DOCS.items()):
        path = os.path.join(root, rel)
        if not os.path.exists(path):
            bad.append("%s is MISSING" % rel)
            continue
        size = os.path.getsize(path)
        if size < floor:
            bad.append("%s is %d bytes, expected at least %d" % (rel, size, floor))
    for b in bad:
        print("    %s" % b)
    return not bad, "%d document(s) look truncated" % len(bad)



def check_readme_cross_references(root):
    """Every DOC/README-* that DOC/README names is actually on the disk.

    THIS EXISTS BECAUSE TWO OF THEM WERE NOT.  On 2026-09-01 `DOC/README'
    advertised `README-KERMIT' ("six kermits -- which one to take") and
    `README-GREP' ("six ways to search a file") in the same voice as the
    fifteen that were there, and neither file had ever been written.  Every
    check passed: a document that does not exist has no LF in it, no UTF-8,
    no leftovers and no bad magic, and `check_docs_not_truncated' only knows
    about the documents somebody remembered to put in KEY_DOCS.

    The failure mode is the worst kind for a collection whose whole purpose
    is helping somebody choose what to take: the index promises the help and
    the help is not there.

    Both directions are checked.  A README-* on the disk that DOC/README does
    NOT name is also reported, because a chooser nobody can find is the same
    problem seen from the other end.
    """
    docdir = os.path.join(root, "DOC")
    index = os.path.join(docdir, "README")
    if not os.path.exists(index):
        return False, "DOC/README is missing"
    text = open(index, "rb").read().decode("latin-1").replace("\r", "\n")
    named = set(re.findall(r"\bREADME-[A-Z0-9-]+", text))
    present = {f for f in os.listdir(docdir) if f.startswith("README-")}
    problems = []
    for n in sorted(named - present):
        problems.append("DOC/README names %s and it is not on the disk" % n)
    for n in sorted(present - named):
        problems.append("DOC/%s is on the disk and DOC/README does not name it" % n)
    for b in problems:
        print("    %s" % b)
    return not problems, "%d README cross-reference(s) wrong" % len(problems)


def check_modules_start_with_4afc(root):
    """Every program under CMDS still begins with OS-9's module sync bytes.

    `binaries start with their magic' is EXTENSION-DRIVEN and says so in its
    own docstring -- it looks at `.jpg', `.gif', `.zoo' and the rest, and an
    OS-9 module has no extension, so nothing checked the 900-odd files that
    ARE the collection.  Found 2026-09-01 by `tools/check_the_checks.py',
    which blanked `CMDS/cat's first byte and watched every check stay green
    except one that noticed by accident.

    A module whose $4AFC is gone is not a program any more: `F$Load' rejects
    it and the shell says `module not found'. Nothing else here would say
    which file.

    `mscheck', `who' and `man' are SHELL SCRIPTS, not modules, and are the
    only three exceptions -- the same ones `module_census.py' reports as
    not-a-module.  `man' was written for this collection on 2026-09-18 and
    is a script on purpose: what it does is find a page in DOC/MANPAGES and
    hand it to nroff and less, which is three lines of shell and would be a
    hundred of C.
    `wn.stb' and `rtfdat' are type-$04 DATA modules and still carry $4AFC,
    so they need no exception.
    """
    import gen_catalog
    SCRIPTS = {"mscheck", "who", "man"}
    bad = []
    for d in gen_catalog.PROGRAM_DIRS:
        full = os.path.join(root, d)
        if not os.path.isdir(full):
            continue
        for f in sorted(os.listdir(full)):
            if f in SCRIPTS:
                continue
            path = os.path.join(full, f)
            if not os.path.isfile(path):
                continue
            if open(path, "rb").read(2) != b"\x4a\xfc":
                bad.append("%s/%s does not start with $4AFC" % (d, f))
    for b in bad[:10]:
        print("    %s" % b)
    return not bad, "%d file(s) under CMDS are not modules" % len(bad)


def check_no_absence_phrasing(root):
    """Reader-facing text names what the reader HAS, never what this disk lacks.

    CLAUDE.md's rule, and it had no enforcement until 2026-09-12, when a
    sweep found six violations that had been shipping: `version' said "there
    is no `ident' here", `map' said of mfree and free "neither is on this
    disk", `listalias' said "`egrep', which is not on this disk", and the
    `if' card said Microware's shell "is not on this disk, so here it does
    nothing".

    Why it matters rather than being fussy: the reader HAS OS-9.  `ident' and
    `mfree' are Microware's own utilities and are sitting on their machine, so
    telling them the utility does not exist is both discouraging and, from
    where they are standing, false.

    THE FIRST PATTERN SAID ONLY `not on this disk' AND MISSED A REAL ONE.
    `map' read "neither is on this disk" -- no "not" in it -- so one of the
    six violations this check exists for would have walked back in.  Found by
    running the check against the old wording, NOT by watching it go green on
    a tree already cleaned.  That is what "make every check fail once" is for.

    NARROW ON PURPOSE.  Two literal shapes only.  `there is no help flag'
    (27 of them in help.psv) means the PROGRAM has no flag and is a
    different sense entirely; `no sound device here' and `wants an IEEE-488
    bus and there is none' are hardware facts.  A wider net would catch all
    three and teach whoever hits it to phrase around the checker.
    """
    pats = [re.compile(r"\b(?:not|neither)\b[^.]{0,40}?on this disk"),
            re.compile(r"there is no `[^']+' here")]
    targets = [os.path.join(root, "DOC", "INDEX")]
    here = os.path.dirname(os.path.abspath(__file__))
    targets.append(os.path.join(here, "howto.psv"))
    sheets = os.path.join(here, "screenshots")
    if os.path.isdir(sheets):
        targets += [os.path.join(sheets, f) for f in sorted(os.listdir(sheets))
                    if f.endswith(".sheet")]
    bad = []
    for path in targets:
        if not os.path.exists(path):
            continue
        text = open(path, "rb").read().decode("latin-1").replace("\r", "\n")
        for n, line in enumerate(text.split("\n"), 1):
            for pat in pats:
                if pat.search(line):
                    bad.append("%s:%d %s" % (os.path.basename(path), n,
                                             line.strip()[:60]))
    for b in bad[:8]:
        print("    %s" % b)
    return not bad, "%d place(s) say what this disk lacks" % len(bad)


def check_no_chained_parent_paths(root):
    """A card's pathlist climbs with dots, not with `../..'.

    Professional OS-9 v2.4, "Accessing Files and Directories: The Pathlist",
    p. 4-9: "Add a period for each higher directory level ... to specify a
    directory two levels above the current directory, three periods are
    required."  So two levels up is `...' and three is `....'.

    THIS DOES NOT MAKE `../..' INVALID, and an earlier version of this
    docstring said it did.  rdoggett, who has run the real hardware, states
    the opposite: a component made only of dots climbs (dots - 1) levels and
    components ADD UP, so `../..' is two one-level components and reaches the
    same place as `...'.  His example is `../......./.././file'.  p. 4-9
    teaches the dotted form without excluding chaining, and no Microware line
    settling chaining either way has been found, so treat `../..' as legal
    OS-9 that this collection simply does not use.

    THE GATE IS ABOUT HOUSE STYLE FIRST, AND PORTABILITY SECOND.  NEITHER
    IS ABOUT VALIDITY.  rdoggett settled both halves on 2026-09-13: real
    OS-9 accepts the chained form -- "yes real os-9 accepts ../../../.. no
    problem" -- and the gate should stay anyway, because the cards should
    use the dotted form "because it's uniquely os9".  That is the reason:
    `...' is the spelling this system has and Unix does not, and a
    collection teaching OS-9 should show it.  `../..' is legal and simply
    is not how we write it here.

    The practical half supports it.  The dotted form works on real OS-9 and
    on every os9exec build; `../..' relative to a subdirectory FAILED on an
    RBF image with E_PNNF until os9exec 985e0d8 (2026-09-13) -- so a card
    shipping it would break for every reader whose emulator predates that,
    which is nearly all of them.  A card has to work on the system the
    reader already has.

    And measured 2026-09-12, BEFORE that fix, the failure did not announce
    itself: `cat ../../SYS/motd' from /dd/CMDS/GCC2 gave E_PNNF naming the
    FILE though /dd/SYS/motd plainly existed, and three layers disagreed --
    a shell forking `../../CMDS/for' resolved it, `chd ../..' climbed two
    levels, and a program's own open() climbed one.  Whether 985e0d8 has
    made those agree has not been re-measured here.

    EXECUTABLE LINES ONLY, and the first version got this wrong.  It read
    whole files including DOC/INDEX and SOURCES.txt, so this sentence --

        OS-9 counts dots: two levels up is ... and not ../.. as on Unix

    -- would have been FLAGGED.  A gate that fails somebody for documenting
    the rule it enforces teaches them the rule is arbitrary, and a gate
    nobody believes gets routed around.  Found by probing the check with text
    it ought to ACCEPT, which a green run on a clean tree can never show;
    os9-dev-skill-fc hit the mirror-image hole in a check of their own the
    same evening and described the method.

    So: only the directives that RUN something -- try, os9, run, send,
    expect -- in the sheets and the case and drive files.  A malformed
    pathlist costs nothing where nothing executes it.  Host-side Python,
    shell and Makefiles are not screened at all: `../..' is the host's
    correct spelling.

    IT HAS A BREAKER NOW, and the reason it went without one for a week is
    worth keeping.  This docstring used to say a breaker was impossible --
    "that harness copies the DISK tree, while this reads the sheets under
    tools/, which are never copied".  True of the harness as it stood, and
    the wrong conclusion: the answer was to let the check be POINTED
    somewhere else, which is what `OSK_TOOLS_DIR' does and what
    `OSK_HELP_TABLE' had already been doing for another check in the same
    file.  "This cannot be tested" is nearly always "this cannot be tested
    the way the harness works today".  The manual proof below stands as the
    record of the week it was true:

        a throwaway sheet carrying `run  ../../CMDS/for div.f'
            -> `check_disk.py disk' EXITS 1 and prints this check FAILED
        the probe removed
            -> exits 0, prints ok

    Running the CLI is what separates a REGISTERED check from a merely
    defined one, and reading the exit-code line is not the same as running
    it: the sibling check's breaker was written, looked correct, was never
    added to BREAKS, and check_the_checks reported "24 of 24 breaks were
    caught" throughout.  A function can be perfect and unreachable.
    """
    here = tools_dir()
    targets = []
    for sub in ("screenshots", "datatests", "drives", "playtests"):
        d = os.path.join(here, sub)
        if os.path.isdir(d):
            targets += [os.path.join(d, f) for f in sorted(os.listdir(d))
                        if f.rsplit(".", 1)[-1] in ("sheet", "cases", "drive", "keys")]
    pat = re.compile(r"\.\./\.\.")
    runs = re.compile(r"^\s*(try|os9|run|send|expect|keys)\s")
    bad = []
    for path in targets:
        if not os.path.exists(path):
            continue
        text = open(path, "rb").read().decode("latin-1").replace("\r", "\n")
        for n, line in enumerate(text.split("\n"), 1):
            if not runs.match(line):
                continue                 # prose may name the wrong spelling
            if pat.search(line):
                bad.append("%s:%d %s" % (os.path.basename(path), n,
                                         line.strip()[:58]))
    for b in bad[:8]:
        print("    %s" % b)
    return not bad, "%d OS-9 path(s) chain `../..' instead of counting dots" % len(bad)


def check_cards_do_not_depend_on_each_other(root):
    """A gallery card may build on `setup-image' and on nothing else.

    THE FAILURE THIS CATCHES COST FIVE CARDS AT ONCE.  `ppmntsc' read
    `/dd/tmp/w.ppm', which the `pnmfilters' card writes -- and pnmfilters
    allowed 25 seconds for a `giftopnm | pnmscale' that needs most of a
    minute, so the capture was taken before the write finished and w.ppm was
    left unwritten.  Every line of ppmntsc's card then failed with
    `ppmntsc: /dd/tmp/w.ppm -', and `audit_cards' scored FIVE CONVERTERS as
    broken when none of them is.  Found 2026-09-01.

    A card that depends on another card's leftovers is one card's timing
    away from lying, and nothing about the failure points at the card that
    caused it.

    `setup-image' is the ONE sanctioned exception: it is the first stanza of
    graphics.sheet, it exists to make the two test images that twenty round
    trips start from, and saying so once is better than twenty cards each
    generating their own gingham.  Everything else must make what it reads.

    Approximate on purpose: only a `>' or `>>' redirect counts as writing,
    so a card whose program writes a file WITHOUT a redirect (`lha a k.lzh',
    `des d.txt') reads as not writing it -- which is why the check asks
    "does another CARD write this" rather than "does this card write this".
    A path nobody redirects into is nobody's dependency and is ignored.
    """
    import screenshots
    sheets = os.path.join(tools_dir(), "screenshots")
    if not os.path.isdir(sheets):
        return True, ""
    SETUP = "setup-image"
    cards, writers = {}, {}
    for f in sorted(os.listdir(sheets)):
        if not f.endswith(".sheet"):
            continue
        for shot in screenshots.parse(os.path.join(sheets, f)):
            runs = [v for k, v in shot["acts"] if k == "run"]
            wrote, read = set(), set()
            for r in runs:
                wrote |= set(re.findall(r">>?\s*(/dd/tmp/[\w./-]+)", r))
                read |= set(re.findall(r"(/dd/tmp/[\w./-]+)", r))
            cards[shot["name"]] = (wrote, read)
            for path in wrote:
                writers.setdefault(path, set()).add(shot["name"])
    # A path `setup-image' writes is sanctioned however many other cards
    # also write it: `plotters' regenerates base.pbm with setup-image's own
    # command before using it, which is belt-and-braces and made this check
    # fire on six innocent cards the first time it ran.
    sanctioned = cards.get(SETUP, (set(), set()))[0]
    bad = []
    for name, (wrote, read) in sorted(cards.items()):
        for path in sorted(read - wrote - sanctioned):
            owners = writers.get(path, set()) - {name, SETUP}
            if owners:
                bad.append("card `%s' reads %s, which only `%s' writes"
                           % (name, path, "/".join(sorted(owners))))
    for b in bad:
        print("    %s" % b)
    return not bad, "%d card(s) depend on another card" % len(bad)


def check_cards_have_no_pathlists(root):
    """A card's caption or `try' line must never carry a full absolute path.

    rdoggett, told many times and finally angrily (2026-09-05): `DO NOT USE
    FULL PATHLISTS in explanation on cards.  Arrange to not need them.'  A
    reader browsing hundreds of programs does not benefit from
    `/dd/CMDS/subber /dd/tmp/SUB/words' where `subber words in' would do.
    Name a file by its bare or short-relative name, or arrange the demo with
    a `chd' so the shown command reads short.  A bare device (`mount as /h0')
    is fine; a rooted pathlist (`/h0/usr/src/...') is not.
    """
    sheets = os.path.join(tools_dir(), "screenshots")
    if not os.path.isdir(sheets):
        return True, ""
    pathlist = re.compile(r"(?:/dd|/h0|/h1|/h5|/h6)/[\w.]")
    # ONE scoped exception: hack's `try' line.  hack relaunches itself by the
    # name it was started with, and bash passes a program only the bare word
    # typed (Microware's shell passes the whole pathlist), so under bash hack
    # must be given its full path or it cannot re-open itself.  The `os9' line
    # stays bare.  The card's caption explains it.  This is the copy-paste
    # rule winning over the no-pathlist rule for the one command that needs it.
    path_ok = {("hack", "try")}
    bad = []
    for f in sorted(os.listdir(sheets)):
        if not f.endswith(".sheet"):
            continue
        shot = None
        for raw in open(os.path.join(sheets, f)):
            line = raw.rstrip("\n")
            word = line.split(None, 1)[0] if line.split() else ""
            rest = line.split(None, 1)[1] if len(line.split(None, 1)) > 1 else ""
            if word == "shot":
                shot = rest.strip()
            elif word in ("cap", "try", "os9") and pathlist.search(rest) \
                    and (shot, word) not in path_ok:
                bad.append("%s: `%s' %s line names a full path: %s"
                           % (f, shot, word, pathlist.search(rest).group(0) + "..."))
    for b in bad:
        print("    %s" % b)
    return not bad, "%d card caption/try line(s) carry a full pathlist" % len(bad)


def check_cards_have_a_try_line(root):
    """Every card says what to type -- ratcheted.

    The card's `Try it' box shows the stanza's `try' line, and without one
    it falls back to the bare program name.  On 2026-09-07 one card in 906
    had a `try' line, so `gothic' -- whose picture was made with `gothic -h
    OS-9' -- told the reader to type `gothic', which prompts for a file
    name and waits.  rdoggett: "notice: no argument, wtf?".

    `tools/try-backlog.txt' names the stanzas still without one.  A stanza
    that has neither a `try' line nor a backlog entry fails; so does a
    backlog entry whose stanza now has one, until its line comes out.
    Writing the `try' line is part of looking at the program, so the
    backlog shrinks as the per-program pass goes round.
    """
    tools = os.path.dirname(os.path.abspath(__file__))
    sheets = os.path.join(tools, "screenshots")
    if not os.path.isdir(sheets):
        return True, ""
    backlog_path = os.environ.get("OSK_TRY_BACKLOG",
                                  os.path.join(tools, "try-backlog.txt"))
    backlog = set()
    if os.path.exists(backlog_path):
        backlog = {ln.strip() for ln in open(backlog_path)
                   if ln.strip() and not ln.startswith("#")}
    has_try, stanzas = set(), set()
    for f in sorted(os.listdir(sheets)):
        if not f.endswith(".sheet"):
            continue
        shot = None
        for raw in open(os.path.join(sheets, f)):
            parts = raw.split(None, 1)
            if not parts or raw.lstrip().startswith("#"):
                continue
            if parts[0] == "shot":
                shot = parts[1].strip()
                stanzas.add(shot)
            elif parts[0] == "try" and shot:
                has_try.add(shot)
    bad = []
    for name in sorted(stanzas - has_try - backlog):
        bad.append("`%s' has no try line and is not on the backlog" % name)
    for name in sorted(backlog & has_try):
        bad.append("`%s' has a try line now -- take it off the backlog" % name)
    for name in sorted(backlog - stanzas):
        bad.append("`%s' is on the backlog and is not a stanza" % name)
    for b in bad[:12]:
        print("    %s" % b)
    if len(bad) > 12:
        print("    ... and %d more" % (len(bad) - 12))
    return not bad, "%d problem(s); %d cards still without a try line" % (
        len(bad), len(stanzas - has_try))


def check_module_names(root):
    """No two files under CMDS register the same MODULE name.

    THE FILENAME IS NOT THE NAME.  OS-9 finds a program by the name in its
    module header once that module is resident, whatever path you type, so two
    files sharing one name are two paths to one program and the loser is
    unreachable.  Measured 2026-08-30: after `load /dd/CMDS/REBUILT/arc',
    running /dd/CMDS/arc gave ARC 5.12 rather than the 5.21 that lives at that
    path, and nothing warned.

    32 names over 76 files were like that when this was first counted. Renaming
    the FILE alone does not fix it and makes it worse, because the filenames
    then promise a distinction the modules do not have -- so this checks the
    module header, not the directory listing.

    A module name that merely DIFFERS from its filename is fine and common:
    65 files here report the original author's own capitalisation (`ATerm',
    `FStat', `wermit', `B_hc'). That is preserved deliberately. What is not
    fine is two files answering to one name, and the ones that legitimately do
    are listed in tools/module-name-duplicates.txt with a reason each.
    """
    accepted = {}
    listing = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "module-name-duplicates.txt")
    if os.path.exists(listing):
        for line in open(listing):
            line = line.rstrip()
            if not line.strip() or line.lstrip().startswith("#") or line[:1] in " \t":
                continue
            name, _, why = line.partition(" ")
            if not why.strip():
                print("    %s: '%s' has no reason beside it" % (listing, name))
                return False, "an accepted duplicate carries no reason"
            accepted[name] = why.strip()

    seen = {}
    for base, _, files in os.walk(os.path.join(root, "CMDS")):
        for f in sorted(files):
            path = os.path.join(base, f)
            head = open(path, "rb").read(0x30)
            if head[:2] != b"\x4a\xfc":
                continue
            body = open(path, "rb").read()
            off = int.from_bytes(body[0x0c:0x10], "big")
            if off >= len(body) or b"\0" not in body[off:]:
                continue
            name = body[off:body.index(b"\0", off)].decode("latin-1")
            seen.setdefault(name, []).append(os.path.relpath(path, root))

    bad = {n: v for n, v in seen.items() if len(v) > 1 and n not in accepted}
    for n in sorted(bad):
        print("    module '%s' is registered by %s" % (n, ", ".join(sorted(bad[n]))))
    stale = [n for n in accepted if len(seen.get(n, [])) < 2]
    for n in sorted(stale):
        print("    '%s' is listed as an accepted duplicate but no longer is one" % n)
    return (not bad and not stale,
            "%d module name(s) claimed by more than one file, %d stale exception(s)"
            % (len(bad), len(stale)))


def check_cio_macro_population(root):
    """DOC/README-CIO's count of putc/getc-macro programs must match the disk.

    Those programs answer with hundreds of thousands of lines of the
    EMULATOR's `No more memory !!!' and do their work not at all, because they
    were linked against a `cio.l' whose trap-13 selector $41 is `_flshbuf'
    where every `cio' module here has a memory routine -- so `putc' hands the
    raw allocator a FILE pointer as a byte count.  Root cause and mechanism:
    notes/os9exec-bugs/CIO-SELECTOR-MISMATCH.md.

    README-CIO tells a reader how many programs can do this.  That number is
    the sort this collection has watched drift over and over, so it is checked
    rather than trusted.

    Two guards travel with it, and both are the ones that catch the mistake
    everyone makes here.  `autolf' CARRIES the $41/$42 stubs and never calls
    them, so it must NOT be listed -- counting stubs instead of calls to them
    is the wrong measurement.  And the scan must still FIND something: it is
    an easy scan to break into silence, and a silent scan agrees with any
    number in README-CIO.

    The positive guard used to name `logisim' and `cvtbase', the two watched
    to storm.  BOTH WERE REBUILT `-qm' ON 2026-08-31 and no longer link cio at
    all, so naming them would fail for the right reason and the wrong one at
    once.  `hexed' took over and has now gone the same way -- it was one of
    six more rebuilt later that day.

    THE GUARD WAS `kermit_cio' AND IT HAD TO MOVE AFTER ALL.  It was chosen
    because it was the one name here that could never be rebuilt away -- it
    was DELIBERATELY the cio build, which is what its name said -- and then
    on 2026-09-12 it left the disk for a different reason entirely: a second
    kermit needing cio to do what the first does without it is a duplicate,
    and the collection dropped it.  A guard can expire by deletion as well as
    by rebuilding, which the note it replaces did not allow for.

    So the guard is now `liborder' and `unpacklib', the two holders of the
    most call sites, PLUS A FLOOR.  Both are rebuild candidates like
    everything else on the list, so this half is expected to need moving one
    day; the check prints which name it wanted, and moving it is a one-line
    edit.  The floor is what actually catches a scan gone silent, and it is
    set well below the current population rather than at it, so that an
    ordinary rebuild does not read as a broken scanner.
    """
    import cio_macro_scan
    total, rows = cio_macro_scan.survey([root])
    listed = {name.split("/")[-1] for name, _, _ in rows}
    problems = []
    for n in ("autolf", "cat", "detab"):
        if n in listed:
            problems.append("%s is listed and must not be (it never calls the stub)" % n)
    for n in ("liborder", "unpacklib"):
        if n not in listed:
            problems.append("%s is NOT listed and must be -- it is one of the "
                            "two holders of the most call sites, so a scan "
                            "that misses it has stopped working.  If it has "
                            "just been rebuilt `-qm', move this half of the "
                            "guard to the next name in README-CIO's list" % n)
    if len(rows) < 15:
        problems.append("the scan found only %d programs; it has probably "
                        "stopped scanning rather than the disk having changed"
                        % len(rows))

    doc = os.path.join(root, "DOC", "README-CIO")
    if os.path.exists(doc):
        text = open(doc, "rb").read().decode("latin-1").replace("\r", "\n")
        m = re.search(r"(\d+) modules here link cio; (\d+) contain the call", text)
        if not m:
            problems.append("README-CIO no longer states the population")
        elif (int(m.group(1)), int(m.group(2))) != (total, len(rows)):
            problems.append("README-CIO says %s/%s; the disk has %d/%d"
                            % (m.group(1), m.group(2), total, len(rows)))
    for pr in problems:
        print("    %s" % pr)
    return not problems, "%d problem(s) with the cio-macro population" % len(problems)


def check_cards_state_their_terms(root):
    """Every program's card states its terms -- ratcheted.

    rdoggett, 2026-09-14: "You must note on each card it's requirements,
    copyrights, whatever."  On that day 19 of 997 cards carried a copyright
    or conditions line, all from EFFO info files; what SOURCES.txt records
    never reached a card.  `tools/terms.psv' holds what the card says,
    and `tools/terms-backlog.txt' names the programs not looked up yet.  A
    catalogued program in neither fails; so does a backlog name that now
    has a line, and a line or backlog name that is not a program.
    """
    tools = tools_dir()
    sys.path.insert(0, tools)
    # Every CATALOGUE entry, not only the runnable modules: cio, math and
    # the other trap libraries have cards too, and a reader keeping one
    # needs its terms as much as a program's.
    import gen_catalog
    catalogued, _, _ = gen_catalog.gather(root, os.path.join(tools, "categories.psv"))
    progs = {p["name"] for p in catalogued}
    def names(path, sep):
        out = set()
        if os.path.exists(path):
            for line in open(path, encoding="latin-1"):
                line = line.strip()
                if line and not line.startswith("#"):
                    out.add(line.split(sep)[0] if sep else line)
        return out
    have = names(os.path.join(tools, "terms.psv"), "|")
    backlog = names(os.path.join(tools, "terms-backlog.txt"), None)
    bad = []
    for n in sorted(progs - have - backlog):
        bad.append("`%s' has no terms line and is not on the backlog" % n)
    for n in sorted(backlog & have):
        bad.append("`%s' has terms now -- take it off the backlog" % n)
    for n in sorted((have | backlog) - progs):
        bad.append("`%s' is in the terms files and is not a catalogued program" % n)
    for b in bad[:12]:
        print("    %s" % b)
    if len(bad) > 12:
        print("    ... and %d more" % (len(bad) - 12))
    return not bad, "%d problem(s); %d cards still without terms" % (
        len(bad), len(progs - have))


def check_cards_carry_real_help(root):
    """Every card's "its own help" is what the program printed -- ratcheted.

    Until 2026-09-09 the help on a card was lifted out of the binary by a
    regex that stopped at the first string not shaped like an option, so
    `roff' was published as three lines ending at `Options:' with the
    options cut off.  Now tools/help.psv says, per program, which command
    asks it for help (or that it has none) and docs/help/<name>.txt is what
    it answered, captured whole by tools/helpcap.py.

    The ratchet: a program is in the table or on tools/help-backlog.txt,
    never both and never neither.  For each table entry with a command, the
    capture must exist, begin `$ <that command>' (a table line changed
    without a re-capture fails), hold some text, hold no `[no answer in'
    marker (the program hung on that flag: the table is wrong), and not
    end on a line ending in `:' -- a cut-off option list, the roff scrape
    made into a rule.
    """
    tools = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, tools)
    import helpcap
    table = helpcap.load_table(os.environ.get("OSK_HELP_TABLE", helpcap.TABLE))
    helpdir = os.environ.get("OSK_HELP_DIR", helpcap.HELPDIR)
    backlog_path = os.environ.get("OSK_HELP_BACKLOG", helpcap.BACKLOG)
    backlog = set()
    if os.path.exists(backlog_path):
        backlog = {ln.strip() for ln in open(backlog_path)
                   if ln.strip() and not ln.startswith("#")}
    ondisk = set(helpcap.programs(root))
    bad = []
    for name in sorted(ondisk - set(table) - backlog):
        bad.append("`%s' has no help.psv line and is not on the backlog" % name)
    for name in sorted(backlog & set(table)):
        bad.append("`%s' is in help.psv now -- regenerate the backlog" % name)
    for name in sorted(set(table) - ondisk):
        bad.append("`%s' is in help.psv and is not on the disk" % name)
    for name, (cmd, _note) in sorted(table.items()):
        if cmd is None:
            continue
        path = os.path.join(helpdir, name + ".txt")
        if not os.path.exists(path):
            bad.append("`%s': no capture in docs/help" % name)
            continue
        first, _, text = open(path, encoding="ascii").read().partition("\n")
        text = text.rstrip("\n")
        if first != "$ " + cmd:
            bad.append("`%s': capture is of `%s', table says `%s'" % (name, first[2:], cmd))
        elif not text.strip():
            bad.append("`%s' printed nothing for `%s'" % (name, cmd))
        elif helpcap.NO_ANSWER in text:
            bad.append("`%s' hangs on `%s'" % (name, cmd))
        elif re.match(r"^[A-Za-z][A-Za-z ]{0,30}:$", text.rstrip().split("\n")[-1].strip()):
            # A bare heading as the last line -- `Options:', `Commands:' --
            # is an option list cut off before it began.  A usage line
            # that happens to end in a colon (`Usage: mslabel [-vscV]
            # drive:') is not, and was a false alarm on 2026-09-09.
            bad.append("`%s': help ends at `%s' -- cut off?" % (name, text.rstrip().split("\n")[-1].strip()))
    for b in bad[:12]:
        print("    %s" % b)
    if len(bad) > 12:
        print("    ... and %d more" % (len(bad) - 12))
    return not bad, "%d problem(s); %d programs still without a help line" % (
        len(bad), len(backlog))


def check_harness_env_matches_login(root):
    """The harnesses' idea of the login environment must match SYS/login's.

    `tools/screenshots.py' carries a hand-written copy of what SYS/login
    exports, because it types commands at a shell rather than sourcing a
    file.  A copy drifts, and on 2026-08-31 it did: login was changed to set
    `SHELL=$ROOT/CMDS/ksh' -- the one shell here that can serve system() --
    and the copy still said bash, so the `latex' card was a capture of
    E$PNNF while the program itself worked.

    This compares the two on every variable BOTH of them set, which is the
    part that has to agree.  A variable only one of them sets is fine:
    login has PWD and a `builtin cd' that no harness needs.
    """
    login = os.path.join(root, "SYS", "login")
    harness = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "screenshots.py")
    if not (os.path.exists(login) and os.path.exists(harness)):
        return True, ""

    def assignments(text, prefix=""):
        found = {}
        for line in text.replace("\r", "\n").split("\n"):
            line = line.strip()
            if prefix:
                if not line.startswith(prefix):
                    continue
                line = line[len(prefix):].strip().strip('",')
            if line.startswith("export "):
                line = line[len("export "):]
            m = re.match(r"^([A-Z][A-Z0-9_]*)=(\S*)$", line)
            if m:
                found.setdefault(m.group(1), m.group(2))
        return found

    def resolve(value):
        """The few shell expansions login uses, as the harness would see them.

        login is written to work for whoever runs it -- `${USER:-tester}',
        `$ROOT', `$USER' -- and the harness writes the value those come out
        as. Resolving them here is what keeps the check from crying wolf on
        three variables that agree perfectly.
        """
        value = re.sub(r"\$\{[A-Z_]+:-([^}]*)\}", r"\1", value)
        value = value.replace("$ROOT", "/dd").replace("$USER", "tester")
        return value.rstrip('")')

    want = assignments(open(login, "rb").read().decode("latin-1"))
    got = assignments(open(harness).read(), prefix='"export ')
    bad = []
    for name, value in sorted(got.items()):
        if name not in want:
            continue
        expect, value = resolve(want[name]), resolve(value)
        if expect != value:
            bad.append("%s: SYS/login says %s, screenshots.py says %s"
                       % (name, expect or "(empty)", value or "(empty)"))
    return (not bad), "; ".join(bad)



def check_every_program_is_accounted_for(root):
    """A catalogued program is in screens.js, the backlog, or the exceptions.

    THE PANEL RATCHET READS docs/screens.js, so a program that never reached
    the catalogue is invisible to it -- not failing, not excepted, not on the
    backlog, simply unseen.  Both ratchets then report zero outstanding while
    the program has neither a card nor a recorded reason for lacking one.

    Written 2026-09-12 after `dedit', `who', `fpu' and `fpu040' appeared to
    fall through.  THEY DO NOT: none is a type-$01 program, so the panel
    system ignores them correctly, and the first version of this check
    demanded cards for things nothing can show.  It failed the gate on four
    correctly-handled names before the predicate was narrowed to
    audit_panels.runnable().  The lesson kept rather than the false alarm:
    a check over a WIDER set than the system it guards will invent work.

    So this is the hole rather than its instances: every name in
    categories.psv must appear in ONE of the three places, and a new program
    that shows nothing must say why in panel-exceptions.psv.
    """
    import json
    here = os.path.dirname(os.path.abspath(__file__))
    js = os.path.join(os.path.dirname(here), "docs", "screens.js")
    seen = set()
    if os.path.exists(js):
        text = open(js).read()
        seen = set(json.loads(text[text.index("{"):].rstrip().rstrip(";")).keys())
    def names(path, sep):
        out = set()
        if not os.path.exists(path):
            return out
        for line in open(path):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            out.add(line.split(sep)[0] if sep else line)
        return out
    # The panel system's universe is audit_panels.runnable() -- every type-$01
    # module the catalogue lists -- NOT every name in categories.psv.  Asking
    # about the wider set makes this a false-positive generator: `fpu' and
    # `fpu040' are type-$0C descriptors, `who' is a shell script and `dedit'
    # is type-$02 I-code, so nothing is expected to show any of them, and
    # cio/math/csl are traplibs credited to another card.  The first version
    # of this check failed on exactly those four and I nearly "fixed" them.
    sys.path.insert(0, here)
    import audit_panels
    cats = set(audit_panels.runnable())
    backlog = names(os.path.join(tools_dir(), "panel-backlog.txt"), None)
    excepted = names(os.path.join(tools_dir(), "panel-exceptions.psv"), "|")
    missing = sorted(cats - seen - backlog - excepted)
    for m in missing[:10]:
        print("    %s is catalogued but has no card, no backlog line and no "
              "exception" % m)
    return not missing, "%d program(s) accounted for nowhere" % len(missing)


def check_panels_show_their_program(root):
    """Every runnable program's panel shows THAT program working -- ratcheted.

    The gallery is built per CARD and read per PROGRAM, and `audit_cards'
    scoring the card as a whole is how `lessecho' came to publish
    `helpindex's help text with a bare `lessecho < /nil' under it and 0 of
    408 flagged.  `tools/audit_panels.py' scores what the reader sees of
    the program itself.  474 programs failed it on 2026-09-03, so the gate
    is a ratchet: `tools/panel-backlog.txt' names the known failures, a
    NEW failure fails the build, and a listed program that now passes fails
    it too until its line comes out.  `tools/panel-exceptions.psv' holds the
    few that are right as they stand, each with its reason.

    The audit reads docs/screens.js and the sheets, not the disk tree, so
    `root' is unused here; the prober points the gate at a mutated copy of
    the backlog through OSK_PANEL_BACKLOG rather than editing the live file.
    """
    import audit_panels
    ok, bad = audit_panels.gate()
    for b in bad[:12]:
        print("    %s" % b)
    if len(bad) > 12:
        print("    ... and %d more" % (len(bad) - 12))
    return ok, "%d problem(s); run tools/audit_panels.py --gate" % len(bad)



def check_libraries_are_recorded(root):
    """Every .l in LIB/ must be named in SOURCES.txt.

    LIB/ HAD NEVER BEEN SCREENED. SOURCES.txt says DEFS/ is third-party
    collections only and `tools/screen_microware.py' enforces that on
    anything NEW, but the libraries that arrived with the initial import
    were never checked against it -- and five of fifteen had no entry at
    all. One, `unet.l', could not be placed by anybody: no copyright
    string, no entry, nothing on the disk linking it, and BSD networking
    symbols inside. It was removed on 2026-09-19.

    A library is the one thing here a reader links into their OWN program,
    so "what is this and may I use it" is a fair question to be able to
    answer for each. Matching a file on rdoggett's build overlay does NOT
    answer it -- that overlay carries this collection's own libraries, and
    reading a match there as evidence is what turned this into a false
    alarm about Microware for an hour. The pristine SDK under
    `paths.SDK_FULL' is the one that settles provenance.
    """
    libdir = os.path.join(root, "LIB")
    if not os.path.isdir(libdir):
        return True, ""
    sources = os.path.join(root, "SOURCES.txt")
    if not os.path.isfile(sources):
        return False, "no SOURCES.txt to check LIB/ against"
    text = open(sources, "rb").read().decode("latin-1")
    missing = [f for f in sorted(os.listdir(libdir))
               if f.endswith(".l") and f not in text]
    if missing:
        return False, ("%d librar%s in LIB/ not named in SOURCES.txt: %s"
                       % (len(missing), "y is" if len(missing) == 1 else "ies are",
                          " ".join(missing)))
    return True, ""



def check_cards_make_their_own_directories(root):
    """A stanza must create the /dd/tmp directory it writes into.

    `cards do not depend on each other' catches a stanza that reads a FILE
    another stanza wrote.  It does not catch the same dependency on a
    DIRECTORY, and eleven stanzas in archives.sheet had it: only `cat' and
    `compr' ran `mkdir -p /dd/tmp/ARC', and every other stanza in the sheet
    wrote into it and worked only because one of those two had gone first.
    Shot on its own -- which is what `--only' does when one card is being
    corrected -- `compress' answered "I/O error: opening file
    tmp/ARC/idx4, error 216" and published that.

    The failure is silent in a full sheet run and appears only when someone
    re-shoots one card, which is exactly when nobody is looking at the
    other sixty.  Found 2026-09-19 while re-shooting a card that turned out
    not to be stale after all.
    """
    sheets = os.path.join(tools_dir(), "screenshots")
    if not os.path.isdir(sheets):
        return True, ""
    bad = []
    for f in sorted(os.listdir(sheets)):
        if not f.endswith(".sheet"):
            continue
        lines = open(os.path.join(sheets, f), errors="replace").read().split("\n")
        starts = [i for i, l in enumerate(lines) if l.startswith("shot ")]
        for si, s in enumerate(starts):
            e = starts[si + 1] if si + 1 < len(starts) else len(lines)
            body = "\n".join(lines[s:e])
            name = lines[s].split(None, 1)[1].strip()
            used = set(re.findall(r"/dd/tmp/([A-Za-z0-9_]+)/", body))
            made = set(re.findall(r"mkdir\s+(?:-p\s+)?/dd/tmp/([A-Za-z0-9_]+)",
                                  body))
            for d in sorted(used - made):
                bad.append("%s:%s wants /dd/tmp/%s" % (f, name, d))
    if bad:
        return False, ("%d stanza(s) write into a directory they never make: %s"
                       % (len(bad), "; ".join(bad[:4])))
    return True, ""


CHECKS = [
    ("line endings are CR-only", check_line_endings),
    ("no UTF-8 on an 8-bit disk", check_no_utf8),
    ("no editor or host leftovers", check_no_leftovers),
    ("no build products in the tree", check_no_build_litter),
    ("no new SDK author stamps", check_author_stamps),
    ("every command is in DOC/INDEX", check_index_names),
    ("the star grid is self-consistent", check_star_grid),
    ("every recipe names a real tree", check_recipes),
    ("every program has a category", check_categories),
    ("DOC/DEPENDS is up to date", check_depends),
    ("the manual index is up to date", check_manpages),
    ("no unscreened Microware source", check_src_screened),
    ("every library is recorded", check_libraries_are_recorded),
    ("binaries start with their magic", check_binary_magic),
    ("every command is a real module", check_modules_start_with_4afc),
    ("one module name, one file", check_module_names),
    ("the cio-macro list is current", check_cio_macro_population),
    ("name lists point at real programs", check_hand_files_name_real_programs),
    ("one line per name in the hand lists",
     check_hand_lists_have_no_duplicate_keys),
    ("the disk's documents are intact", check_docs_not_truncated),
    ("README names documents that exist", check_readme_cross_references),
    ("text names what the reader has", check_no_absence_phrasing),
    ("OS-9 paths count dots", check_no_chained_parent_paths),
    ("cards do not depend on each other", check_cards_do_not_depend_on_each_other),
    ("cards make their own directories",
     check_cards_make_their_own_directories),
    ("cards carry no full pathlists", check_cards_have_no_pathlists),
    ("every card says what to type", check_cards_have_a_try_line),
    ("cards carry real help text", check_cards_carry_real_help),
    ("every card states its terms", check_cards_state_their_terms),
    ("harness env matches SYS/login", check_harness_env_matches_login),
    ("every program is accounted for", check_every_program_is_accounted_for),
    ("panels show their own program", check_panels_show_their_program),
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
