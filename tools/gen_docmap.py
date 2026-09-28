#!/usr/bin/env python3
"""Write DOC/DOCS and DOC/WHATIS -- the library's catalogue cards, for `man'.

    tools/gen_docmap.py disk            write both
    tools/gen_docmap.py disk --check    exit 1 if either is stale

WHY.  DOC holds hundreds of files, and a reader who wants to know whether
`hp' has any documentation had to go looking -- or type `man hp' and hope.
rdoggett, 2026-09-27: "We are the librarians, how do we make this more
accessible?"  These two files are the answer the disk carries, and the
disk's own `man' reads them: every program, every document that belongs to
it, and where its source is.

DOC/DOCS    one line per (program, kind, path), paths relative to the disk:

                hp             man  DOC/hp/hp.1
                westley        src  SRC/ioccc/westley.c

            kind is `man' for a roff page (nroff -man formats it), `doc' for
            text to read as it is, `src' for source.  One path to a line,
            so no line comes near SCF's 512-byte limit and `grep "^hp "'
            finds them all.

DOC/WHATIS  one line per program: its name and the first sentence of its
            DOC/INDEX entry.  `man -k' searches it, `man -f' prints a line.

WHAT BELONGS TO A PROGRAM is decided by tools/doc_census.py's four routes --
its own name, its source archive, its CMDS family, or doc-shared.psv --
so the census and the map cannot disagree.  A directory named for the
program contributes every text file in it; one shared with others (an
archive's or a family's) contributes only the files named for the program,
or failing that its own READMEs.  Binary files are left out: a reader can
page text, not a .dvi.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doc_census                                       # noqa: E402
from gen_catalog import from_index                      # noqa: E402

ROFF = re.compile(r"\.([1-9][a-z]?|man|l)$", re.I)
NOT_TEXT = re.compile(r"\.(ps|eps|dvi|gif|jpe?g|png|pbm|pgm|ppm|tfm|pk|gf|"
                      r"vf|Z|gz|lzh|zoo|arc|ar|tar|r|l[ib]?|ch|vpl|web)$", re.I)
README = re.compile(r"^(readme|read\.me|index|about|intro|overview)", re.I)
TOO_MANY = 24          # a program's own directory is listed whole up to this


LISTS = re.compile(r"^(manifest|files|packing\.list)(\.te?xt)?$", re.I)


def is_text(path):
    """True for a file a reader can page: no NUL, mostly printable -- and
    not a MANIFEST, which is a list of the other files and nothing more."""
    if NOT_TEXT.search(path) or LISTS.match(os.path.basename(path)):
        return False
    head = open(path, "rb").read(4096)
    if not head or b"\0" in head:
        return False
    odd = sum(1 for b in head if b < 9 or 13 < b < 32 and b != 27)
    return odd * 50 < len(head)


def stem(name):
    return doc_census.DOC_SUFFIX.sub("", ROFF.sub("", name)).lower()


def files_under(path):
    if os.path.isfile(path):
        return [path]
    out = []
    for d, dirs, fs in os.walk(path):
        dirs.sort()
        out += [os.path.join(d, f) for f in sorted(fs)]
    return out


def order(prog, paths):
    """Roff pages first, those named for the program first among them;
    then READMEs; then the rest."""
    low = prog.lower()
    return sorted(paths, key=lambda p: (not ROFF.search(p),
                                        stem(os.path.basename(p)) != low,
                                        not README.match(os.path.basename(p)),
                                        p.lower()))


def is_roff(path, manpages):
    """A roff page is one DOC/MANPAGES lists, or one that starts like one."""
    if path in manpages:
        return True
    if not ROFF.search(path):
        return False
    head = open(path, "rb").read(200).lstrip()
    return head.startswith(b".") or head.startswith(b"'\\\"")


def documents(root, prog, verdict, where):
    """Every paged document that belongs to prog, most useful first."""
    if not where:
        return []
    everything = [p for p in files_under(where) if is_text(p)]
    if verdict == "DIRECT" and os.path.basename(where).lower() == prog.lower():
        mine = everything
    else:
        mine = [p for p in everything
                if stem(os.path.basename(p)) == prog.lower()]
        if not mine:
            mine = [p for p in everything
                    if os.path.dirname(p) == where
                    and README.match(os.path.basename(p))]
        if not mine and os.path.isfile(where):
            mine = everything
    return order(prog, mine)[:TOO_MANY]


def sources(root, prog, tree):
    """The source files named for prog in its tree, else its README.OSK."""
    src = os.path.join(root, "SRC")
    for t in (tree, prog):
        if not t or t == "--":
            continue
        d = os.path.join(src, t)
        if not os.path.isdir(d):
            continue
        named = [p for p in files_under(d)
                 if os.path.basename(p).split(".")[0].lower() == prog.lower()
                 and "/ORIG/" not in p and not p.endswith((".ori", ".orig"))
                 and is_text(p)]
        if named:
            return order(prog, named)[:8]
        osk = doc_census.osk_readme(d)
        return [osk] if osk else []
    return []


def first_sentence(desc):
    desc = " ".join(desc.split())
    m = re.match(r"(.+?[.;:])(\s|$)", desc)
    s = m.group(1).rstrip(";:") if m else desc
    return s if len(s) <= 180 else s[:177].rsplit(" ", 1)[0] + " ..."


def build(root):
    docroot = os.path.join(root, "DOC")
    names = doc_census.doc_names(docroot)
    origins = doc_census.origins_map(docroot)
    shared = doc_census.shared_docs()
    manpages = set()
    mp = os.path.join(docroot, "MANPAGES")
    if os.path.isfile(mp):
        for line in doc_census.cr_text(mp).split("\n"):
            f = line.split()
            if len(f) == 2:
                manpages.add(os.path.join(root, f[1].replace("/dd/", "", 1)))
    progs, _ = from_index(root)

    rows, whatis, seen = [], [], set()
    body = lambda p: open(p, "rb").read()                    # noqa: E731
    for prog, d in doc_census.programs(root):
        if prog in seen:
            continue
        seen.add(prog)
        low = prog.lower()
        verdict, where = "NONE", ""
        if low in names:
            verdict, where = "DIRECT", names[low]
        elif origins.get(prog, "").lower() in names:
            verdict, where = "ARCHIVE", names[origins[prog].lower()]
        elif doc_census.FAMILY.get(d, "") in names:
            verdict, where = "FAMILY", names[doc_census.FAMILY[d]]
        elif shared.get(prog, "").lower() in names:
            verdict, where = "SHARED", names[shared[prog].lower()]
        rel = lambda p: os.path.relpath(p, root)             # noqa: E731
        # A roff page or a .doc kept beside the source is documentation
        # still -- elm's manual is SRC/.../ELM_2.4/DOC/elm.1, dm's help
        # dm.hlp -- so both places are pooled and put in one order, manual
        # pages first.  One copy of the same bytes is enough.
        docs, srcs, kept = list(documents(root, prog, verdict, where)), [], set()
        for p in sources(root, prog, origins.get(prog)):
            if is_roff(p, manpages) or doc_census.DOC_SUFFIX.search(p) \
               or os.path.basename(p).lower() == "readme.osk":
                docs.append(p)
            else:
                srcs.append(p)
        for p in order(prog, docs):
            if body(p) in kept:
                continue
            kept.add(body(p))
            rows.append((prog, "man" if is_roff(p, manpages) else "doc", rel(p)))
        for p in srcs:
            if body(p) not in kept:
                kept.add(body(p))
                rows.append((prog, "src", rel(p)))
        desc = progs.get(prog, {}).get("desc", "")
        if desc:
            whatis.append("%-14s - %s" % (prog, first_sentence(desc)))

    docs = ["DOCS -- every program's documents and source, for `man'",
            "=" * 58, "",
            "Generated by tools/gen_docmap.py from DOC/INDEX, DOC/ORIGINS and",
            "the files themselves; do not edit.  One path to a line: `man'",
            "for a roff page, `doc' for text, `src' for source.", ""]
    docs += ["%-14s %-4s %s" % r for r in rows]
    what = ["WHATIS -- one line for every program, for `man -k' and `man -f'",
            "=" * 63, "",
            "Generated by tools/gen_docmap.py from DOC/INDEX; do not edit.", ""]
    what += sorted(whatis, key=str.lower)
    return ("\r".join(docs) + "\r").encode("latin-1"), \
           ("\r".join(what) + "\r").encode("latin-1")


def main(argv):
    if not argv:
        sys.exit(__doc__.strip().splitlines()[0])
    root = argv[0]
    docs, what = build(root)
    targets = ((os.path.join(root, "DOC", "DOCS"), docs),
               (os.path.join(root, "DOC", "WHATIS"), what))
    if "--check" in argv:
        stale = [p for p, b in targets
                 if not os.path.exists(p) or open(p, "rb").read() != b]
        for p in stale:
            print("    %s is stale -- run tools/gen_docmap.py" % p)
        return 1 if stale else 0
    for p, b in targets:
        open(p, "wb").write(b)
        print("  %s: %d lines" % (p, b.count(b"\r")))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
