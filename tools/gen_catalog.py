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
    "All 92" starred block and the netpbm/gcc directories. Read as ordinary
    entries, the first name on a column line acquires the next three as its
    description and those three vanish -- which is how 42 of 169 netpbm
    programs used to survive.
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
    COLUMNAR = ("CMDS/NETPBM", "CMDS/GCC139")
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


# netpbm names are <from>to<to>; the section documents the convention. Nothing
# gives these 169 an individual description, so derive one rather than ship a
# blank row, which is what made them undiscoverable.
FORMATS = {
 "pnm":"PNM","pbm":"PBM (bitmap)","pgm":"PGM (greyscale)","ppm":"PPM (colour)",
 "gif":"GIF","jpeg":"JPEG","tiff":"TIFF","bmp":"BMP","pcx":"PCX","ps":"PostScript",
 "ascii":"ASCII art","fits":"FITS","xwd":"X window dump","x10bm":"X10 bitmap",
 "xbm":"X bitmap","xpm":"XPM","sgi":"SGI","sun":"Sun raster","rast":"Sun raster",
 "macp":"MacPaint","pi1":"Atari PI1","pi3":"Atari PI3","pict":"PICT","tga":"Targa",
 "ilbm":"IFF/ILBM","icon":"Sun icon","g3":"Group 3 fax","hips":"HIPS","mgr":"MGR",
 "img":"GEM IMG","gem":"GEM","cmuwm":"CMU window manager","atk":"Andrew toolkit",
 "brush":"Xerox brush","fs":"Usenix FaceSaver","gould":"Gould scanner",
 "mtv":"MTV ray tracer","qrt":"QRT ray tracer","raw":"raw bytes","spc":"Atari Spectrum",
 "spu":"Atari Spectrum","yuv":"Abekas YUV","zeiss":"Zeiss confocal",
 "biorad":"Bio-Rad confocal","lispm":"Lisp machine","pj":"HP PaintJet",
 "pk":"packed font","pcd":"PhotoCD","hpcd":"PhotoCD","sld":"AutoCAD slide",
}

def derive_netpbm_desc(name):
    m = re.match(r"^(.+?)to(.+)$", name)
    if not m:
        return "netpbm image tool"
    a, b = m.group(1).lower(), m.group(2).lower()
    if a in FORMATS or b in FORMATS:
        return "%s to %s" % (FORMATS.get(a, a), FORMATS.get(b, b))
    return "netpbm image tool"



# ---- the program's own help text -------------------------------------

USAGE_START = re.compile(rb"(?i)(usage|syntax)\s*:")
USAGE_CONT  = re.compile(rb"(?i)^(options?|function|where|flags?|commands?)\s*[:\-]")
USAGE_OPT   = re.compile(rb"(?i)^\s{0,6}-{1,2}[A-Za-z?][\w=]*\s")

def usage_of(path, name, limit=1200):
    """Lift a program's syntax line and option list out of its own binary.

    "WOLK - dam utility" tells a reader nothing they can act on, and no
    second-hand summary beats the program's own account. Almost every OS-9
    program carries its usage text as plain strings.

    Telling that text from the rest of a binary is the awkward part: symbol
    tables and format fragments look similar. Anchor on a syntax line, then
    keep following strings only while they still look like option
    documentation, and stop at the first that does not.
    """
    try:
        data = open(path, "rb").read()
    except OSError:
        return None
    if data[:2] != b"\x4a\xfc":
        return None
    out, taking = [], False
    for m in re.finditer(rb"[ -~\t]{6,}", data):
        line = m.group().rstrip()
        if not line:
            continue
        if not taking:
            # SEARCH, not match: these strings often carry a few bytes of
            # surrounding code, and "N]NuUsage: gnuchess [-a]" starts with a
            # letter, so stripping non-letters off the front never reached it.
            hit = USAGE_START.search(line)
            if hit:
                taking = True
                out.append(line[hit.start():])
            continue
        line = re.sub(rb"^[^A-Za-z/\-]{0,6}", b"", line)
        if USAGE_OPT.match(line) or USAGE_CONT.match(line) or re.match(rb"^\s{2,}\S", line):
            out.append(line)
            if sum(len(x) for x in out) > limit:
                break
        else:
            break
    if not out:
        return None
    text = b"\n".join(out).decode("latin-1")
    text = re.sub(r"[ \t]{3,}", "   ", text)
    # these are printf templates; %s is almost always the program's own name
    text = text.replace("%s", name)
    text = text[:limit]

    # Reject what substitution turned into noise. netpbm composes its usage at
    # run time from "usage:  %s %s", so the argument spec is never in the
    # binary and this yields "usage: pnmcut pnmcut" -- worse than saying
    # nothing, because it looks like the program takes its own name twice.
    body = re.sub(r"(?i)^\s*(usage|syntax)\s*:", "", text).strip()
    body = body.replace(name, "").strip()
    if len(body) < 6 or not re.search(r"[\[<(\-]|\w\s+\w", body):
        return None
    return text


def from_origins(root, progs):
    RX = re.compile(r"^  (\S+)\s+(\S+)\s+(usenet archive|EFFO forum|hc disk|PD disk)\b(.*)$")
    for line in read(root, "DOC/ORIGINS").split("\n"):
        m = RX.match(line)
        if m and m.group(1) in progs:
            progs[m.group(1)].update(src=m.group(2), origin=m.group(3),
                                     archive=m.group(4).strip())


def from_depends(root, progs):
    cur = None
    for line in read(root, "DOC/DEPENDS").split("\n"):
        m = re.match(r"^  (\S+)\s+\((\S+)\)$", line)
        if m:
            cur = m.group(1)
            continue
        if cur and line.startswith("      /") and cur in progs:
            path = line[6:].rstrip()
            missing = path.endswith("--")
            progs[cur].setdefault("needs", []).append(
                {"path": path.replace("--", "").strip(), "missing": missing})


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
    # the same way on 2026-08-27, while photographing the disk: ADL, COMMS,
    # ELM, NETWORK, NEWS, TEXCMDS and WN -- 83 programs, TeX and elm among
    # them, all present in DOC/INDEX and none of them in the guide.  Only
    # CMDS/archives stays out, and that holds .lzh source archives, not
    # programs.
    for d in ("CMDS", "CMDS/GAMES", "CMDS/NETPBM", "CMDS/BROKEN", "CMDS/REBUILT",
              "CMDS/GCC139", "CMDS/GCC2", "CMDS/DEMOS", "CMDS/DHRY", "CMDS/MM1",
              "CMDS/UUCP", "CMDS/ADL", "CMDS/COMMS", "CMDS/ELM", "CMDS/NETWORK",
              "CMDS/NEWS", "CMDS/TEXCMDS", "CMDS/WN"):
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
            u = usage_of(p, n)
            if u:
                progs[n]["usage"] = u

    docs = {x.lower() for x in os.listdir(os.path.join(root, "DOC"))
            if os.path.isdir(os.path.join(root, "DOC", x))}
    srcs = {x.lower() for x in os.listdir(os.path.join(root, "SRC"))}
    for p in progs.values():
        p["star"]     = p["name"] in starred
        p["docs"]     = p["name"].lower() in docs
        p["hassrc"]   = p.get("src", "").lower() in srcs or p["name"].lower() in srcs
        p["military"] = "no military use" in p.get("desc", "")


def load_categories(path):
    cats = {}
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, cat, sub = line.split("|")
        cats[name] = (cat, sub)
    return cats


def load_howto(path):
    """Hand-written "how do I run this" notes, from tools/howto.psv.

    Separate from categories.psv because it answers a different question and
    covers a handful of programs rather than all of them. Most programs need
    no entry -- usage_of() lifts their usage line straight out of the binary,
    which cannot go stale the way a written note can.
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


def gather(root, catfile):
    progs, starred = from_index(root)
    groups = netpbm_groups(root)
    from_origins(root, progs)
    from_depends(root, progs)
    from_effo(root, progs)
    from_tree(root, progs, starred)
    for p in progs.values():
        if p.get("section") == "CMDS/NETPBM" and not p["desc"]:
            p["desc"] = derive_netpbm_desc(p["name"])

    cats  = load_categories(catfile)
    howto = load_howto(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "howto.psv"))
    out, uncategorised = [], []
    for p in sorted(progs.values(), key=lambda x: x["name"].lower()):
        if not p.get("dir"):
            continue                      # named in INDEX but not on the disk
        if p["name"] in howto:
            p["howto"] = howto[p["name"]]
        if p["name"] in cats:
            p["cat"], p["sub"] = cats[p["name"]]
        elif p["name"] in groups:
            p["cat"], p["sub"] = "Graphics & images", groups[p["name"]]
        else:
            uncategorised.append(p["name"])
            p["cat"], p["sub"] = "Uncategorised", "Uncategorised"
        out.append(p)
    return out, uncategorised


# ---------------------------------------------------------------- writing

BLURB = {
 "Shells":"Unix shells to sit beside OS-9's own -- bash and ksh bring history, job control, and scripts that come across unchanged.",
 "Editors":"vi and emacs in several flavours, line and stream editors, and editors for binary and hex.",
 "Text tools":"Search, sort, compare, reformat, split and spell-check.",
 "Files & directories":"Listing, copying, finding, renaming, and knowing what you have.",
 "Developer tools":"Version control, tags, cross-reference, formatters, a debugger and benchmarks.",
 "Compilers & build":"C compilers and their passes, assemblers, linkers, make and parser generators.",
 "Languages":"Interpreters and language systems beyond C.",
 "Archives & compression":"Pack, unpack and shrink -- lha, zip, tar, arc, zoo, and OS-9 module libraries.",
 "Encoding & conversion":"Between text encodings, line endings, number bases, ciphers and hashes.",
 "Communications":"Kermit in several builds, terminal sessions, and networking.",
 "Graphics & images":"The netpbm toolkit, JPEG, a ray tracer, and things that draw.",
 "Games":"Adventures, board and card games, arcade ports, dungeon crawls and puzzles.",
 "Screen toys":"Things to watch rather than play. Start one and leave it going.",
 "Amusements":"Generators, simulators and diversions that are not quite games.",
 "System & modules":"OS-9 module and process tools, devices, system state and scheduling.",
 "Disk & DOS":"Reading and writing MS-DOS media with the mtools set.",
 "Time & calendar":"Calendars, clocks and astronomy.",
 "Maths & calculators":"Calculators, plotting, orbits and number theory.",
 "Printing":"Spoolers, page formatting and PostScript.",
 "Documentation":"Pagers, readers and the help system.",
}
ORDER = ["Shells","Editors","Text tools","Files & directories","Developer tools",
 "Compilers & build","Languages","Archives & compression","Encoding & conversion",
 "Communications","Graphics & images","Games","Screen toys","Amusements",
 "System & modules","Disk & DOS","Time & calendar","Maths & calculators",
 "Printing","Documentation","Uncategorised"]

KEEP = ("name","desc","cat","sub","star","dir","size","origin","archive","src",
        "docs","hassrc","military","basic09","needs","info","usage","howto")

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
         "> Screens photographed from the running programs: `docs/screens.html`.\n"
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
        for sub in sorted(subs, key=lambda s: -len(subs[s])):
            if len(subs) > 1:
                L += ["**%s**" % sub, ""]
            L += ["| | |", "|---|---|"]
            for p in sorted(subs[sub], key=lambda x: x["name"].lower()):
                star = "&#9733; " if p.get("star") else ""
                cell = star + p.get("desc", "").replace("|", "\\|")
                # How to run it, which is what a reader actually wants next.
                # The usage line comes out of the binary; the note is written.
                # Both were previously generated and then shown only in the
                # HTML, where most people never see them.
                if p.get("howto"):
                    cell += "<br>**How:** " + p["howto"].replace("|", "\\|")
                elif p.get("usage"):
                    one = p["usage"].strip().splitlines()[0].strip()
                    if one:
                        cell += "<br>`%s`" % one.replace("|", "\\|")
                L.append("| `%s` | %s |" % (p["name"], cell))
            L.append("")
        L += ["</details>", ""]

    L += ["---", "",
          "&#9733; needs Microware's `cio`, which is not on the disk — "
          "`DOC/README-CIO` explains how to point at your own.", "",
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
        for sub in sorted(subs, key=lambda s: -len(subs[s])):
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
    slim = [{k: v for k, v in p.items() if k in KEEP and v not in (None, "", False, [])}
            for p in progs]
    html = open(template, encoding="utf-8").read()
    # Escape '<' as \u003c. sed's own usage line is "sed [-n] <script> [<path>]",
    # and that literal <script> closes the element early -- the page dies at the
    # letter s. Valid JSON either way; the browser parses it back to '<'.
    data = json.dumps(slim, separators=(",", ":")).replace("<", "\\u003c")
    html = html.replace("__DATA__", data)
    html = html.replace("__BLURB__", json.dumps(BLURB))
    html = html.replace("__ORDER__", json.dumps(ORDER))
    html = html.replace("__TOTAL__", str(len(progs)))
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
    progs, uncategorised = gather(root, os.path.join(here, "categories.psv"))

    if uncategorised:
        print("  %d program(s) missing from tools/categories.psv:" % len(uncategorised))
        for n in uncategorised[:20]:
            print("     %s" % n)
        if check:
            raise SystemExit(1)
    elif check:
        print("  every program on the disk has a category")
        raise SystemExit(0)

    repo = os.path.abspath(os.path.join(here, os.pardir))
    out  = args[1] if len(args) > 1 else os.path.join(repo, "docs", "index.html")
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
