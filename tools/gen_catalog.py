#!/usr/bin/env python3
"""Build the browsable catalogue of what is on the disk.

    tools/gen_catalog.py disk docs/index.html
    tools/gen_catalog.py disk --check       # exit 1 if a program is uncategorised

DOC/INDEX answers "what is this program?" for someone who already has a name.
It cannot answer "I want a better shell" or "is there anything else like
rain?", because it is alphabetical and 700 lines long. This produces the other
view: grouped by what a program is FOR, searchable, with everything the disk
knows about each one behind a click.

Everything is derived from the disk except the category assignment, which
lives in tools/categories.psv because no rule gets it right -- see the header
of that file. A program missing from it is an error, not a silent "Other".

Sources, all of them already on the disk:

    DOC/INDEX     name, one-line description, and the cio star
    DOC/ORIGINS   which archive it came out of, and its SRC tree
    DOC/DEPENDS   what else it opens at run time, and whether that is here
    DOC/<prog>/info_<prog>   the EFFO metadata files: author, version, terms
    the tree      size, where it lives, and whether it is BASIC09 I-code

The output is one self-contained file: no CDN, no fonts, no scripts fetched
at run time, matching how the rest of this repo builds things.
"""
import json, os, re, sys

# ---------------------------------------------------------------- reading

def read(root, rel):
    return open(os.path.join(root, rel), "rb").read().decode("latin-1").replace("\r", "\n")


def from_index(root):
    """name -> {desc, section}, plus the set of starred names.

    Two blocks in INDEX list names in COLUMNS rather than one per line: the
    "All N" starred block and the gcc directory. Read as ordinary entries,
    the first name on a column line acquires the next three as its
    description and those three vanish -- which is how 42 of 169 netpbm
    programs used to survive, until 2026-09-09, when the netpbm section
    was rewritten as one entry per program with a real description and
    left the columnar list.
    """
    lines = read(root, "DOC/INDEX").split("\n")
    # The gcc heading reads "/dd/CMDS/GCC139 and /dd/CMDS/GCC2 --", so the
    # separator is not always right after the first path.
    SECTION = re.compile(r"^/dd/(\S+).* --")
    # Entries are indented two spaces, a star taking the place of the second.
    # A few sit four deep inside a sub-list -- `who` and `mscheck` were lost
    # that way. Requiring two spaces BEFORE the description is what keeps
    # wrapped continuation lines (single-spaced prose) from matching.
    ENTRY   = re.compile(r"^ {1,4}(\*?) ?([A-Za-z0-9_.][\w.]*)\s{2,}(\S.*)$")
    # SECTION captures to the first space, so the gcc heading yields this:
    COLUMNAR = ("CMDS/GCC139",)
    # Continuations sit far enough right that no entry could match.
    CONT     = re.compile(r"^ {10,}\S")

    progs, section, in_stars, last = {}, None, False, None
    for line in lines:
        if line.startswith("All ") and "verified" in line:
            in_stars = True
            continue
        if in_stars:
            if line.startswith("---") or line.startswith("/dd"):
                in_stars = False
            else:
                continue
        m = SECTION.match(line)
        if m:
            section = m.group(1)
            continue
        if section in COLUMNAR and line.startswith("  "):
            if not re.match(r"^\s+[A-Za-z].*\(\d+\)\s*$", line):
                for tok in line.split():
                    if re.match(r"^[a-z][a-z0-9_.]*$", tok):
                        progs.setdefault(tok, {"name": tok, "desc": "", "section": section})
            continue
        m = ENTRY.match(line)
        if m and section:
            progs.setdefault(m.group(2), {"name": m.group(2), "desc": m.group(3).strip(),
                                          "section": section})
            last = m.group(2)
            continue
        # A wrapped description continues under the first line, indented past
        # where a name would sit. Those lines used to be dropped, so a
        # multi-line entry showed only its first line in the guide and
        # everything explaining it was lost. Fold them back in.
        if section and last and CONT.match(line):
            progs[last]["desc"] += " " + line.strip()
            continue
        if not line.strip():
            last = None

    start = next(i for i, l in enumerate(lines) if l.startswith("All ") and "verified" in l)
    starred = set()
    for l in lines[start+1:]:
        if l.startswith("---") or l.startswith("/dd"):
            break
        starred.update(l.split())
    return progs, starred


def netpbm_groups(root):
    """name -> which of netpbm's own three groups it belongs to.

    The section heads its own lists 'INTO the PNM formats', 'OUT OF ...' and
    'editing, generating and analysing'. Reuse those rather than invent a
    grouping for 169 near-identically named converters.
    """
    HEAD = {"INTO the PNM formats": "NETPBM: into PNM",
            "OUT OF the PNM formats": "NETPBM: out of PNM",
            "editing, generating and analysing": "NETPBM: edit & analyse"}
    out, inside, group = {}, False, None
    for l in read(root, "DOC/INDEX").split("\n"):
        if l.startswith("/dd/CMDS/NETPBM --"):
            inside = True
            continue
        # a real section header, not the wrapped "/dd/CMDS would bury..." line
        if inside and re.match(r"^/dd/\S+ --", l):
            break
        if not inside:
            continue
        m = re.match(r"^\s+([A-Za-z].*?) \(\d+\)\s*$", l)
        if m and m.group(1) in HEAD:
            group = HEAD[m.group(1)]
            continue
        if group and l.startswith("  ") and l.strip():
            for tok in l.split():
                out[tok] = group
    return out


# ---- the program's own help text -------------------------------------

def load_help(root):
    """name -> what the card shows as "its own help".

    tools/help.psv says, per program, which command asks it for help (or
    that it has none), and docs/help/<name>.txt is what the program said,
    captured whole by tools/helpcap.py -- first line `$ <command>', then the
    text.  Until 2026-09-09 this was a regex over the binary's strings that
    stopped at the first line not shaped like an option, which is how roff's
    help was published as three lines ending at `Options:'.  Nothing here is
    read out of a binary any more.

    Returns {"cmd": ..., "text": ...} for a captured help, or {"note": ...}
    for a program the table says has none; a program on the backlog (no
    table line yet) gets nothing and the card shows nothing.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, here)
    import helpcap
    out = {}
    for name, (cmd, note) in helpcap.load_table().items():
        if cmd is None:
            out[name] = {"note": note or "it prints no help of its own"}
            continue
        path = os.path.join(helpcap.HELPDIR, name + ".txt")
        if not os.path.exists(path):
            continue
        first, _, text = open(path, encoding="ascii").read().partition("\n")
        # The card shows the command a reader types, not the hidden
        # setup (a `load' or `chx') that let the capture run it by name.
        shown = helpcap.split_command(first[2:])[1]
        out[name] = {"cmd": shown, "text": text.rstrip("\n")}
    return out


# The origin phrases DOC/ORIGINS actually uses, longest first so that
# `EFFO public-domain disk' is not eaten by `EFFO forum'.  This listed four
# of them until 2026-08-30 and matched 224 of the file's 512 entry lines:
# 242 programs whose origin is `Microware OS-9 archive' -- the single largest
# source on the disk -- showed no provenance at all in the guide, and nothing
# said so.  `unmatched_origins' below is why it cannot go quiet again.
ORIGIN_KINDS = ("Microware OS-9 archive", "EFFO public-domain disk",
                "Usenet", "EFFO forum",
                "hc disk", "PD disk", "microware",
                "Larry Crane",   # a person, for hackwish -- see SOURCES.txt
                "4.3BSD Net/2",  # whereis
                "4.4BSD",        # rev
                "CPAN")          # perl
ORIGIN_RX = re.compile(r"^  (\S+)\s+(\S+)\s+(%s)\b(.*)$"
                       % "|".join(re.escape(k) for k in ORIGIN_KINDS))
# An entry line is a name, a source-tree name, and something after them.
ORIGIN_ENTRY = re.compile(r"^  (\S+)\s+(\S+)\s+(\S.*)$")


def unmatched_origins(root):
    """Entry-shaped ORIGINS lines whose origin phrase is not one we know.

    REPORTED, NOT ENFORCED.  DOC/ORIGINS is prose as well as data -- its own
    legend at the top, and paragraphs about the netpbm archives -- and plenty
    of that is shaped like an entry.  What is worth a human eye is the
    handful of REAL entries whose origin is phrased once and never again:
    `cxref' and `delbak' (a note where the origin goes), `dmake' and `ksh'
    (a bare archive filename), `makelex' ("same archive as sonnet"), `mines',
    `sonnet' ("usenet/comp.sources.games") and `load' ("CONTRIBUTED by the
    os9exec project").  Each would need its own phrase in ORIGIN_KINDS, and
    that is a decision about the FILE, not about the parser.
    """
    out = []
    for line in read(root, "DOC/ORIGINS").split("\n"):
        if ORIGIN_ENTRY.match(line) and not ORIGIN_RX.match(line):
            out.append(line.strip())
    return out


def from_origins(root, progs):
    for line in read(root, "DOC/ORIGINS").split("\n"):
        m = ORIGIN_RX.match(line)
        if m and m.group(1) in progs:
            arch = m.group(4).strip()
            # A bare archive FILENAME (toys.ar, zot.ar, foo.lzh) is not on the
            # disk and means nothing to a reader -- rdoggett, 2026-09-11: "the
            # toys.ar part is worse than noise".  Drop it; keep descriptive
            # provenance (a person, a forum, a disk).
            if re.match(r"^[\w.+-]+\.(ar|lzh|lha|zoo|arc|tar|Z|gz)$", arch):
                arch = ""
            # `--' in the tree column is ORIGINS' "no source tree", not a
            # directory: printed as-is it made 234 cards say `Source: SRC/--'.
            progs[m.group(1)].update(src="" if m.group(2) == "--" else m.group(2),
                                     origin=m.group(3),
                                     archive=arch)


def on_disk(root, path):
    """Where an absolute OS-9 path lands in the tree, or None.

    `/dd/GAMES/adv/glorkz', `/DD/SYS/motd' and `/h0/sys/termcap' all name
    files of this collection (it is /dd and /h0, the same image twice), and RBF
    is case-insensitive where the host may not be -- so each segment is
    matched without regard to case.
    """
    m = re.match(r"^/(?:dd|h0)/(.+)$", path, re.I)
    if not m:
        return None
    here = root
    for seg in m.group(1).strip("/").split("/"):
        try:
            names = os.listdir(here)
        except OSError:
            return None
        hit = next((n for n in names if n.lower() == seg.lower()), None)
        if hit is None:
            return None
        here = os.path.join(here, hit)
    return here


def from_depends(root, progs):
    """What each program reads, and -- for the page's keep preview -- how
    big each of those files is.  `bytes' is None for a directory or for a
    path that is not here; keep copies neither, and the page says so the
    same way keep does."""
    cur = None
    for line in read(root, "DOC/DEPENDS").split("\n"):
        m = re.match(r"^  (\S+)\s+\((\S+)\)$", line)
        if m:
            cur = m.group(1)
            continue
        if cur and line.startswith("      /") and cur in progs:
            path = line[6:].rstrip()
            missing = path.endswith("--")
            path = path.replace("--", "").strip()
            where = None if missing else on_disk(root, path)
            isdir = bool(where and os.path.isdir(where))
            nfiles = 0
            files = []
            if isdir:
                # Capture the names keep will copy, so the card can list them
                # (the page shows them only for a small directory).  Capped so
                # a compiler's LIB does not bloat the JSON; nfiles is the true
                # total either way.
                CAP = 24
                for _r, _d, _f in sorted(os.walk(where)):
                    for fn in sorted(_f):
                        nfiles += 1
                        if len(files) < CAP:
                            fp = os.path.join(_r, fn)
                            rel = os.path.relpath(fp, where).replace(os.sep, "/")
                            files.append({"name": rel,
                                          "bytes": os.path.getsize(fp)})
            progs[cur].setdefault("needs", []).append(
                {"path": path, "missing": missing, "dir": isdir,
                 "nfiles": nfiles, "files": files,
                 "bytes": (os.path.getsize(where)
                           if where and os.path.isfile(where) else None)})


INFO_FIELDS = {"$VERSION":"version", "$AUTHOR-NAME":"author", "$PURPOSE":"purpose",
 "$AVAILABILITY":"availability", "$CONDITIONS":"conditions", "$COPYRIGHT":"copyright",
 "$RESTRICTIONS":"restrictions", "$SOURCE-LANGUAGE":"language",
 "$HARDWARE":"hardware", "$STATUS":"status"}

def from_effo(root, progs):
    """The EFFO info_ files are structured metadata, meant to be extracted.

    A value runs from just after its $KEYWORD line to the next one. Some of
    these files indent the value and some start it at column 0, so the only
    reliable terminator is the next '$'.
    """
    docdir = os.path.join(root, "DOC")
    for d in sorted(os.listdir(docdir)):
        path = os.path.join(docdir, d, "info_" + d)
        if not os.path.isfile(path) or d not in progs:
            continue
        info, key = {}, None
        for l in open(path, "rb").read().decode("latin-1").replace("\r", "\n").split("\n"):
            m = re.match(r"^(\$[A-Z-]+)", l)
            if m:
                key = INFO_FIELDS.get(m.group(1))
                continue
            if key and l.strip():
                info.setdefault(key, []).append(l.strip())
        if info:
            progs[d]["info"] = {k: " ".join(v)[:400] for k, v in info.items()}


def from_tree(root, progs, starred):
    # Every directory holding programs must be listed here or its contents are
    # invisible in the guide -- which is where people actually go looking.
    # CMDS/DEMOS, CMDS/DHRY and CMDS/MM1 were added in 2026-08 and were absent
    # from the catalogue until someone noticed the gap.  Seven more were found
    # the same way on 2026-08-27, while capturing the disk: ADL, COMMS,
    # ELM, NETWORK, NEWS, TEXCMDS and WN -- 83 programs, TeX and elm among
    # them, all present in DOC/INDEX and none of them in the guide.  Only
    # CMDS/archives stays out, and that holds .lzh source archives, not
    # programs.
    for d in PROGRAM_DIRS:
        full = os.path.join(root, d)
        if not os.path.isdir(full):
            continue
        for n in os.listdir(full):
            p = os.path.join(full, n)
            if not os.path.isfile(p) or n not in progs:
                continue
            head = open(p, "rb").read(0x20)
            progs[n]["dir"] = d
            progs[n]["size"] = os.path.getsize(p)
            if len(head) > 0x14 and head[:2] == b"\x4a\xfc" and head[0x13] == 2:
                progs[n]["basic09"] = True      # I-code: needs runb, not the kernel

    docs = {x.lower() for x in os.listdir(os.path.join(root, "DOC"))
            if os.path.isdir(os.path.join(root, "DOC", x))}
    srcs = {x.lower() for x in os.listdir(os.path.join(root, "SRC"))}
    for p in progs.values():
        p["star"]     = p["name"] in starred
        p["docs"]     = p["name"].lower() in docs
        p["hassrc"]   = p.get("src", "").lower() in srcs or p["name"].lower() in srcs
        p["military"] = "no military use" in p.get("desc", "")
    # tools/language.psv: the programs that speak German (or another language)
    # at the terminal.  The card says so under Needs, and the page offers them
    # as a filter -- a reader who has the language wants exactly these.
    langs = load_languages(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "language.psv"))
    for p in progs.values():
        if p["name"] in langs:
            p["lang"], p["langnote"] = langs[p["name"]]


def load_languages(path):
    """name -> (language, what is in it), from tools/language.psv."""
    out = {}
    if not os.path.exists(path):
        return out
    for raw in open(path):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        name, lang, note = (line.split("|", 2) + ["", ""])[:3]
        out[name.strip()] = (lang.strip(), note.strip())
    return out


def load_categories(path):
    cats = {}
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, cat, sub = line.split("|")
        cats[name] = (cat, sub)
    return cats


def load_shadowed(path):
    """Programs whose NAME is also the name of a utility the reader owns.

    rdoggett, 2026-09-18, on shipping a `dir' beside theirs: "I might prefer
    the freeware version (as a user) and want to overwrite Microware's,
    but... I want to do it with informed consent."  So the card says so.
    `tools/shadowed-names.txt' is the measured list and DOC/README-NAMES the
    explanation; this only decides which cards carry the line.
    """
    out = {}
    if not os.path.exists(path):
        return out
    for line in open(path, encoding="latin-1"):
        line = line.strip()
        if not line or line.startswith("#") or "|" not in line:
            continue
        name, where = line.split("|", 1)
        out[name.strip()] = where.strip()
    return out


def load_terms(path):
    """What each card says about a program's terms, from tools/terms.psv.

    name|terms|where it is recorded.  Only the terms reach the card; the
    third field is for whoever checks a line against SOURCES.txt.  A program
    with no line here has not been looked up yet -- see terms-backlog.txt --
    and its card says so rather than guessing.
    """
    out = {}
    if not os.path.exists(path):
        return out
    for line in open(path, encoding="latin-1"):
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.rstrip("\n").split("|")
        if len(parts) >= 2 and parts[1].strip():
            out[parts[0]] = parts[1].strip()
    return out


def load_requires(path):
    """What a program needs that no scan records, from tools/requires.psv.

    name|requirement|where it is stated.  A name may appear on more than one
    line; each requirement becomes one entry under the card's Needs.
    """
    out = {}
    if not os.path.exists(path):
        return out
    for line in open(path, encoding="latin-1"):
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.rstrip("\n").split("|")
        if len(parts) >= 2 and parts[1].strip():
            out.setdefault(parts[0], []).append(parts[1].strip())
    return out


def load_changes(path):
    """What this collection changed in a program, from tools/changes.psv.

    rdoggett, 2026-09-24: "Anything we do alter or rename, we should scribble
    notes on the card if we have that information still."  One line per
    program, `name|note'.  A program ported here with ORIG/ and README.OSK
    beside its source gets a pointer to that README without a line here.
    """
    out = {}
    if not os.path.exists(path):
        return out
    for line in open(path, encoding="ascii"):
        line = line.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        name, _, note = line.partition("|")
        out[name] = note
    return out


def load_excluded(path):
    """Programs found and deliberately left out, from tools/excluded.psv.

    `name|category it would have held|what it is|why it is not here|where it
    came from'.  They are cards of their own in a "Not included" kind, off by
    default, so a reader who wonders where something went can find out --
    and go and look for it themselves.
    """
    out = []
    if not os.path.exists(path):
        return out
    for line in open(path, encoding="ascii"):
        line = line.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        f = line.split("|")
        if len(f) != 5:
            raise SystemExit("%s: want 5 fields: %s" % (path, line))
        name, would, what, why, where = f
        out.append({"name": name, "cat": EXCLUDED_KIND, "sub": would,
                    "desc": what, "why": why, "origin": where, "out": True})
    return out


def load_howto(path):
    """Hand-written "how do I run this" notes, from tools/howto.psv.

    Separate from categories.psv because it answers a different question and
    covers a handful of programs rather than all of them. Most programs need
    no entry -- their own captured help (tools/help.psv, docs/help/) says how
    they are called.
    """
    notes = {}
    if not os.path.exists(path):
        return notes
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, text = line.split("|", 1)
        notes[name] = text
    return notes


# The program directories from_tree walks; also used to check that nothing on
# the disk is invisible to the catalogue.
PROGRAM_DIRS = ("CMDS", "CMDS/GAMES", "CMDS/NETPBM", "CMDS/REBUILT",
                "CMDS/GCC139", "CMDS/GCC2", "CMDS/GCC137", "CMDS/GCC272", "CMDS/DRIVERS", "CMDS/X68K", "CMDS/SYSADMIN", "CMDS/DEMOS", "CMDS/DHRY", "CMDS/MM1",
                "CMDS/UUCP", "CMDS/ADL", "CMDS/COMMS", "CMDS/ELM", "CMDS/NETWORK",
                "CMDS/NEWS", "CMDS/MNEWS", "CMDS/TEXCMDS", "CMDS/WN")


def shared_names(root):
    """Program names that exist in more than one directory, with their sizes.

    THE CATALOGUE CAN ONLY SHOW ONE OF EACH.  Everything here is keyed by
    NAME -- DOC/INDEX, categories.psv, howto.psv and `progs' itself -- so
    where two directories hold different programs under one name, whichever
    `from_tree' walks last supplies the size and the
    directory, and the other is not in the guide at all.

    As measured 2026-08-30 there are nine, eight of them different programs
    rather than copies: `gcc' and `gpp' (GCC139 and GCC2 are different
    compilers), `gnuchess' (CMDS and CMDS/GAMES), and `wish' (the shipped
    build and the one in GAMES).
    CLAUDE.md already says a checker over this collection must compare per
    FILE and not per name; the catalogue does not, and fixing that means
    keying it by path, which changes the guide's shape and is a decision for
    rdoggett rather than a tidy-up.  Reported so it is not forgotten.
    """
    where = {}
    for d in PROGRAM_DIRS:
        full = os.path.join(root, d)
        if not os.path.isdir(full):
            continue
        for f in sorted(os.listdir(full)):
            path = os.path.join(full, f)
            if os.path.isfile(path):
                where.setdefault(f, []).append((d, os.path.getsize(path)))
    return {k: v for k, v in where.items() if len(v) > 1}


def unseen(root, progs):
    """Programs on the disk that DOC/INDEX never named, so gather cannot see them.

    `from_tree' only ANNOTATES entries that `from_index' already found, so a
    program the index does not name in a shape from_index recognises is
    silently absent from the guide -- no category to be missing, nothing to
    report.  On 2026-08-30 an edit to the ADL section of DOC/INDEX deleted a
    four-line list of names, and `adlcomp', `adldebug' and `adltouch' dropped
    out of the catalogue while `--check' still said every program had a
    category.  A check that cannot fail is worse than no check.
    """
    # WALK THE WHOLE OF CMDS, not PROGRAM_DIRS.  Checking only the listed
    # directories would share the blind spot it is meant to catch: a new
    # subdirectory nobody added to the list would be invisible to the
    # catalogue AND to this.  CMDS/archives is the one exception and holds
    # the original .lzh archives, not programs.
    missing = []
    for base, _, files in os.walk(os.path.join(root, "CMDS")):
        rel = os.path.relpath(base, root)
        if os.path.basename(base) == "archives":
            continue
        for n in sorted(files):
            if os.path.isfile(os.path.join(base, n)) and n not in progs:
                missing.append("%s/%s" % (rel, n))
    return missing


def gather(root, catfile):
    progs, starred = from_index(root)
    groups = netpbm_groups(root)
    from_origins(root, progs)
    from_depends(root, progs)
    from_effo(root, progs)
    from_tree(root, progs, starred)
    cats  = load_categories(catfile)
    shadowed = load_shadowed(os.path.join(os.path.dirname(catfile),
                                          "shadowed-names.txt"))
    howto = load_howto(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "howto.psv"))
    helps = load_help(root)
    terms = load_terms(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "terms.psv"))
    requires = load_requires(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                          "requires.psv"))
    changes = load_changes(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "changes.psv"))
    out, uncategorised = [], []
    for p in sorted(progs.values(), key=lambda x: x["name"].lower()):
        if not p.get("dir"):
            continue                      # named in INDEX but not on the disk
        if p["name"] in howto:
            p["howto"] = howto[p["name"]]
        if p["name"] in helps:
            p["help"] = helps[p["name"]]
        if p["name"] in terms:
            p["terms"] = terms[p["name"]]
        if p["name"] in requires:
            p["requires"] = requires[p["name"]]
        sub = (p.get("dir") or "").replace("CMDS/", "", 1)
        note = changes.get("%s/%s" % (sub, p["name"])) or changes.get(p["name"])
        if note:
            p["changed"] = note
        s = p.get("src") or p["name"]
        if os.path.isdir(os.path.join(root, "SRC", s, "ORIG")) and \
           os.path.isfile(os.path.join(root, "SRC", s, "README.OSK")):
            p["changedsrc"] = "SRC/%s/README.OSK" % s
        if p["name"] in shadowed:
            p["shadows"] = shadowed[p["name"]]
        if p["name"] in cats:
            p["cat"], p["sub"] = cats[p["name"]]
        elif p["name"] in groups:
            p["cat"], p["sub"] = "Graphics & images", groups[p["name"]]
        else:
            uncategorised.append(p["name"])
            p["cat"], p["sub"] = "Uncategorised", "Uncategorised"
        out.append(p)
    return out, uncategorised, unseen(root, progs)


# ---------------------------------------------------------------- writing

EXCLUDED_KIND = "Not included"

BLURB = {
 EXCLUDED_KIND:"Programs that were found in the archives and left out on purpose, each with the reason and where it came from, so you can go and look for yourself.  None of them is on the disk.",
 "Shells":"Unix shells to sit beside OS-9's own -- bash and ksh bring history, job control, and scripts that come across unchanged.",
 "Editors":"vi and emacs in several flavours, line and stream editors, and editors for binary and hex.",
 "Text tools":"Search, sort, compare, reformat, split and spell-check.",
 "Files & directories":"Listing, copying, finding, renaming, and knowing what you have.",
 "Developer tools":"Version control, tags, cross-reference, formatters, a debugger and benchmarks.",
 "Compilers & build":"C compilers and their passes, assemblers, linkers, make and parser generators.",
 "Languages":"Interpreters and language systems beyond C.",
 "Archives & compression":"Pack, unpack and shrink -- lha, zip, tar, arc, zoo, and OS-9 module libraries.",
 "Encoding & conversion":"Between text encodings, line endings, Macintosh formats, ciphers and hashes.",
 "Communications":"Kermit in several builds, terminal sessions, and networking.",
 "Graphics & images":"The netpbm toolkit, JPEG, a ray tracer, and things that draw.",
 "Games":"Adventures, board and card games, arcade ports, dungeon crawls and puzzles.",
 "Screen toys":"Animations and screen effects -- they draw on the terminal rather than print to it. Some run until you stop them.",
 "Amusements":"Generators, simulators and diversions that are not quite games.",
 "System & modules":"OS-9 module and process tools, devices, system state and scheduling.",
 "Disk & DOS":"Reading and writing MS-DOS media with the mtools set.",
 "Time & calendar":"Calendars, clocks and astronomy.",
 "Maths & calculators":"Calculators, plotting, orbits and number theory.",
 "Printing":"Spoolers, page formatting and PostScript.",
 "Documentation":"Pagers, readers and the help system.",
 "G-Windows":"Programs for G-Windows, OS-9's graphical display.  There is no G-Windows here, so what their cards show is each one declining in its own words -- `Unable to access \"/win\" device', `dclock only runs under G-Windows', a status of 208 or 221.  None of them can be exercised without the display; they are listed for a real OS-9 workstation that has it.",
 "Needs hardware":"Programs that drive hardware this collection has no way to reach -- a graphics display of the kind a GEPARD or an MM/1 carries, or a printer on its own SCF device.  WE CANNOT TEST ANY OF THESE, at all: what is written about them comes from their own text and their code, not from watching them work.  They are here for a real machine that has the hardware.",
}
ORDER = ["Shells","Editors","Text tools","Files & directories","Developer tools",
 "Compilers & build","Languages","Archives & compression","Encoding & conversion",
 "Communications","Graphics & images","Games","Screen toys","Amusements",
 "System & modules","Disk & DOS","Time & calendar","Maths & calculators",
 "Printing","Documentation","G-Windows","Needs hardware","Uncategorised",
 EXCLUDED_KIND]

KEEP = ("name","desc","cat","sub","star","dir","size","origin","archive","src","shadows",
        "docs","hassrc","military","basic09","needs","info","help","howto","terms","requires",
        "lang","langnote","changed","changedsrc","out","why")

def render_markdown(progs):
    """A catalogue GitHub will actually render in the repository view.

    GitHub shows Markdown and refuses HTML, so the browsable page is invisible
    to anyone who has not cloned or enabled Pages. This is the same content in
    the form that works where people arrive: collapsed per category, so the
    page opens short and expands to the part you want.
    """
    total = len(progs)
    free  = sum(1 for p in progs if not p.get("star") and not p.get("basic09"))
    by = {}
    for p in progs:
        by.setdefault(p["cat"], {}).setdefault(p["sub"], []).append(p)

    L = ["# What is on this disk",
         "",
         "%d programs of OS-9/68K community software, gathered from the archives that "
         "kept it and made to run again. **%d of them need nothing but this disk**; the "
         "rest want Microware's `cio`, marked below with a star."
         % (total, free),
         "",
         "`DOC/INDEX` on the disk lists everything alphabetically. This is the same "
         "collection sorted by what each program is *for*, which is the more useful "
         "order when you do not yet know what you are looking for.",
         "",
         "> Open a program in `docs/index.html` for its **sample output** --\n"
         "> captured from that program running on the disk image.\n"
         ">\n"
         "> Prefer to click around? `docs/index.html` is a searchable version with "
         "per-program detail — what it needs, where it came from, on what terms. "
         "GitHub will not render it here; download the repository and open it, "
         "or enable Pages.",
         ""]

    L.append("| Category | Programs | |")
    L.append("|---|--:|---|")
    for cat in ORDER:
        if cat not in by:
            continue
        n = sum(len(v) for v in by[cat].values())
        L.append("| [%s](#%s) | %d | %s |" %
                 (cat, cat.lower().replace(" & ", "--").replace(" ", "-"), n, BLURB.get(cat, "")))
    L.append("")

    for cat in ORDER:
        if cat not in by:
            continue
        subs = by[cat]
        n = sum(len(v) for v in subs.values())
        L += ["## %s" % cat, "", "*%s*" % BLURB.get(cat, ""), "",
              "<details><summary>%d programs</summary>" % n, ""]
        for sub in sorted(subs, key=str.lower):
            if len(subs) > 1:
                L += ["**%s**" % sub, ""]
            L += ["| | |", "|---|---|"]
            for p in sorted(subs[sub], key=lambda x: x["name"].lower()):
                star = "&#9733; " if p.get("star") else ""
                cell = star + p.get("desc", "").replace("|", "\\|")
                # How to run it, which is what a reader actually wants next:
                # the written note, or else the first line of the help the
                # program printed when asked (docs/help/<name>.txt).
                if p.get("howto"):
                    cell += "<br>**How:** " + p["howto"].replace("|", "\\|")
                elif p.get("help", {}).get("text"):
                    one = p["help"]["text"].strip().splitlines()[0].strip()
                    if one:
                        # FENCE LONGER THAN ANYTHING INSIDE.  A captured
                        # help line may itself contain a backtick -- nine do,
                        # all of the form `join: unrecognized option `-?''
                        # -- and a single-backtick span closes on the first
                        # one, mangling the row.  Markdown's rule is a fence
                        # longer than the longest run within, padded when the
                        # content starts or ends with one.  Fixed here rather
                        # than in CATALOG.md, which is regenerated.
                        txt = one.replace("|", "\\|")
                        runs = re.findall(r"`+", txt)
                        fence = "`" * ((max(len(r) for r in runs) if runs else 0) + 1)
                        pad = " " if txt.startswith("`") or txt.endswith("`") else ""
                        cell += "<br>%s%s%s%s%s" % (fence, pad, txt, pad, fence)
                L.append("| `%s` | %s |" % (p["name"], cell))
            L.append("")
        L += ["</details>", ""]

    out = load_excluded(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "excluded.psv"))
    if out:
        L += ["<details>", "<summary><b>%s</b> &middot; %d</summary>" % (EXCLUDED_KIND, len(out)), "",
              BLURB[EXCLUDED_KIND], "",
              "| | | |", "|---|---|---|"]
        for x in sorted(out, key=lambda x: x["name"].lower()):
            L.append("| `%s` | %s<br>**Why not:** %s | %s |" % (
                x["name"], x["desc"].replace("|", "\\|"),
                x["why"].replace("|", "\\|"), x["origin"].replace("|", "\\|")))
        L += ["", "</details>", ""]

    L += ["---", "",
          "&#9733; marks a program that uses Microware's `cio`, which ships "
          "on the disk, included with Microware's permission; "
          "`DOC/README-CIO` has the details.", "",
          "Generated by `tools/gen_catalog.py` from the disk's own documents. "
          "Do not edit by hand; it will be overwritten."]
    return "\n".join(L) + "\n"


def render_disk_index(progs):
    """DOC/CATEGORIES -- the same grouping, for someone already at an OS-9 prompt.

    The HTML and Markdown catalogues only help people who found the repository.
    Anyone who has the disk image and nothing else has DOC/INDEX, which is
    alphabetical. CR-terminated, 80 columns, no high-bit characters.
    """
    by = {}
    for p in progs:
        by.setdefault(p["cat"], {}).setdefault(p["sub"], []).append(p)
    free = sum(1 for p in progs if not p.get("star") and not p.get("basic09"))

    L = ["CATEGORIES -- what is here, grouped by what it is for",
         "=====================================================",
         "",
         "DOC/INDEX lists every program alphabetically and says what each one is.",
         "This is the same set in the order you want when you do not yet know the",
         "name: %d programs, of which %d need nothing but this disk.  A star means" % (len(progs), free),
         "the program wants Microware's cio -- see DOC/README-CIO.",
         ""]
    for cat in ORDER:
        if cat not in by:
            continue
        subs = by[cat]
        n = sum(len(v) for v in subs.values())
        L += ["-" * 70, "%s (%d)" % (cat.upper(), n), "-" * 70, ""]
        blurb = BLURB.get(cat, "")
        while blurb:                                  # wrap the blurb at 70
            cut = blurb.rfind(" ", 0, 70) if len(blurb) > 70 else len(blurb)
            L.append("  " + blurb[:cut])
            blurb = blurb[cut:].lstrip()
        L.append("")
        for sub in sorted(subs, key=str.lower):
            if len(subs) > 1:
                L.append("  %s:" % sub)
            for p in sorted(subs[sub], key=lambda x: x["name"].lower()):
                star = "*" if p.get("star") else " "
                desc = p.get("desc") or ""
                if len(desc) > 52:                 # cut on a word, not mid-word
                    cut = desc.rfind(" ", 0, 52)
                    desc = desc[:cut if cut > 30 else 52].rstrip(" ,;--") + "..."
                L.append("   %s%-16s %s" % (star, p["name"], desc))
                # A written "how do I run this" note, wrapped under the entry.
                # Only a handful of programs carry one, and they are exactly
                # the ones that otherwise look broken -- see tools/howto.psv.
                note = p.get("howto")
                while note:
                    cut = note.rfind(" ", 0, 62) if len(note) > 62 else len(note)
                    L.append("      %s" % note[:cut])
                    note = note[cut:].lstrip()
            L.append("")
    L += ["-" * 70,
          "Generated from DOC/INDEX and the tree.  DOC/INDEX remains the fuller",
          "account: it carries the notes, the caveats and the per-package detail.",
          ""]
    text = "\r".join(L)
    assert "\n" not in text, "DOC/CATEGORIES must be CR-only"
    assert all(ord(c) < 128 for c in text), "DOC/CATEGORIES must be plain ASCII"
    return text



README_START = "<!-- CATEGORIES:START -->"
README_END   = "<!-- CATEGORIES:END -->"

def update_readme(progs, path):
    """Refresh the category table between the markers in README.md.

    Not the whole list -- docs/CATALOG.md is that, and repeating 614 rows on
    the front page helps nobody. This is the shape of the collection at a
    glance, so a visitor knows what is here before deciding to click.
    """
    if not os.path.exists(path):
        return False
    text = open(path, encoding="utf-8").read()
    if README_START not in text or README_END not in text:
        return False
    counts = {}
    for p in progs:
        counts[p["cat"]] = counts.get(p["cat"], 0) + 1
    rows = ["| Category | | |", "|---|--:|---|"]
    for cat in ORDER:
        if cat in counts:
            rows.append("| **%s** | %d | %s |" % (cat, counts[cat], BLURB.get(cat, "")))
    block = "%s\n\n%s\n\n%s" % (README_START, "\n".join(rows), README_END)
    new = re.sub(re.escape(README_START) + r".*?" + re.escape(README_END),
                 lambda _: block, text, flags=re.S)
    if new != text:
        open(path, "w", encoding="utf-8").write(new)
    return True


def render(progs, template, standalone=True):
    """Fill the template. `standalone` wraps it as a complete document.

    docs/index.html is opened by double-clicking it after downloading the
    repository, so it needs the whole skeleton -- without a doctype the
    browser drops into quirks mode and the layout goes soft.
    """
    out = load_excluded(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "excluded.psv"))
    here = {p["name"] for p in progs}
    clash = [x["name"] for x in out if x["name"] in here]
    if clash:
        raise SystemExit("tools/excluded.psv names programs that ARE on the "
                         "disk: %s" % " ".join(clash))
    slim = [{k: v for k, v in p.items() if k in KEEP and v not in (None, "", False, [])}
            for p in progs + out]
    html = open(template, encoding="utf-8").read()
    # Escape '<' as \u003c. sed's own usage line is "sed [-n] <script> [<path>]",
    # and that literal <script> closes the element early -- the page dies at the
    # letter s. Valid JSON either way; the browser parses it back to '<'.
    data = json.dumps(slim, separators=(",", ":")).replace("<", "\\u003c")
    html = html.replace("__DATA__", data)
    html = html.replace("__BLURB__", json.dumps(BLURB))
    html = html.replace("__ORDER__", json.dumps(ORDER))
    html = html.replace("__TOTAL__", str(len(progs)))
    # The browser page, when it has been built into docs/try; until then no
    # card offers to run anything there.
    docs = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
    # `try/index.html', not `try/': opened from the Finder over file://, a
    # directory link just opens another Finder window (rdoggett hit this).
    # Naming the file at least opens the page, which then says it needs to be
    # served -- fetch() and WebAssembly both refuse a file:// origin.
    html = html.replace("__TRY_PAGE__", json.dumps(
        "try/index.html" if os.path.exists(os.path.join(docs, "try", "index.html"))
        else ""))
    assert "__DATA__" not in html and "__TOTAL__" not in html
    if not standalone:
        return html
    return ('<!doctype html>\n<html lang="en">\n<head>\n'
            '<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<meta name="description" content="A guide to the %d programs on the '
            'OS-9/68K freeware disk, grouped by what they are for.">\n'
            '<meta name="color-scheme" content="light dark">\n'
            % len(progs)) + html.replace("</style>", "</style>\n</head>\n<body>", 1) \
            + "\n</body>\n</html>\n"


if __name__ == "__main__":
    args  = [a for a in sys.argv[1:] if not a.startswith("--")]
    check = "--check" in sys.argv
    if not args:
        raise SystemExit("usage: gen_catalog.py <disk-tree> [<out.html>] [--check]")
    root = args[0]
    here = os.path.dirname(os.path.abspath(__file__))
    progs, uncategorised, invisible = gather(root, os.path.join(here, "categories.psv"))

    shared = shared_names(root)
    if shared:
        differ = {k: v for k, v in shared.items()
                  if len({sz for _, sz in v}) > 1}
        print("  %d program name(s) exist in more than one directory, %d of "
              "them" % (len(shared), len(differ)))
        print("  different programs -- the guide can show only one of each: %s"
              % " ".join(sorted(differ)))

    stray = unmatched_origins(root)
    if stray:
        print("  %d line(s) in DOC/ORIGINS look like entries and record an"
              % len(stray))
        print("  origin this parser does not know -- see unmatched_origins()")

    if invisible:
        print("  %d program(s) on the disk are NOT NAMED IN DOC/INDEX, so the"
              % len(invisible))
        print("  catalogue cannot see them at all:")
        for n in invisible[:20]:
            print("     %s" % n)
        if check:
            raise SystemExit(1)

    if uncategorised:
        print("  %d program(s) missing from tools/categories.psv:" % len(uncategorised))
        for n in uncategorised[:20]:
            print("     %s" % n)
        if check:
            raise SystemExit(1)
    repo = os.path.abspath(os.path.join(here, os.pardir))
    out  = args[1] if len(args) > 1 else os.path.join(repo, "docs", "index.html")

    if check:
        # Every program having a category is not the same as the published
        # page saying what DOC/INDEX says: on 2026-09-23 an INDEX edit passed
        # the whole gate while docs/index.html still carried the old text.
        md = os.path.join(os.path.dirname(os.path.abspath(out)), "CATALOG.md")
        wanted = [(out, render(progs, os.path.join(here, "catalog.template.html"))),
                  (md, render_markdown(progs)),
                  (os.path.join(root, "DOC", "CATEGORIES"), render_disk_index(progs))]
        stale = [p for p, text in wanted
                 if not os.path.exists(p)
                 or open(p, encoding="utf-8", newline="").read() != text]
        for p in stale:
            print("  %s is stale -- run tools/gen_catalog.py %s"
                  % (os.path.relpath(p, repo), root))
        if stale:
            raise SystemExit(1)
        print("  every program on the disk is in the catalogue and has a category")
        raise SystemExit(0)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    open(out, "w", encoding="utf-8").write(
        render(progs, os.path.join(here, "catalog.template.html")))

    # The Markdown twin, for GitHub -- which renders Markdown and not HTML.
    md = os.path.join(os.path.dirname(os.path.abspath(out)), "CATALOG.md")
    open(md, "w", encoding="utf-8").write(render_markdown(progs))

    # And the same grouping on the disk itself, for anyone who has only that.
    disk_doc = os.path.join(root, "DOC", "CATEGORIES")
    open(disk_doc, "wb").write(render_disk_index(progs).encode("ascii"))

    print("  %s" % out)
    print("  %s" % md)
    print("  %s" % disk_doc)
    if update_readme(progs, os.path.join(repo, "README.md")):
        print("  %s (category table)" % os.path.join(repo, "README.md"))
    print("  %d programs, %d categories" % (len(progs), len(set(p["cat"] for p in progs))))
