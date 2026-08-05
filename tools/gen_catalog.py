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

    progs, section, in_stars = {}, None, False
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
    for d in ("CMDS", "CMDS/GAMES", "CMDS/NETPBM", "CMDS/BROKEN", "CMDS/REBUILT",
              "CMDS/GCC139", "CMDS/GCC2"):
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


def load_categories(path):
    cats = {}
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, cat, sub = line.split("|")
        cats[name] = (cat, sub)
    return cats


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

    cats = load_categories(catfile)
    out, uncategorised = [], []
    for p in sorted(progs.values(), key=lambda x: x["name"].lower()):
        if not p.get("dir"):
            continue                      # named in INDEX but not on the disk
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
 "Shells":"The stock OS-9 shell is thin. These give you history, job control and a command line worth living in.",
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
        "docs","hassrc","military","basic09","needs","info")

def render(progs, template):
    slim = [{k: v for k, v in p.items() if k in KEEP and v not in (None, "", False, [])}
            for p in progs]
    html = open(template, encoding="utf-8").read()
    html = html.replace("__DATA__",  json.dumps(slim, separators=(",", ":")))
    html = html.replace("__BLURB__", json.dumps(BLURB))
    html = html.replace("__ORDER__", json.dumps(ORDER))
    assert "__DATA__" not in html
    return html


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

    out = args[1] if len(args) > 1 else os.path.join(here, os.pardir, "docs", "index.html")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    html = render(progs, os.path.join(here, "catalog.template.html"))
    open(out, "w", encoding="utf-8").write(html)
    print("  %s: %d programs, %d categories" % (out, len(progs), len(set(p["cat"] for p in progs))))
