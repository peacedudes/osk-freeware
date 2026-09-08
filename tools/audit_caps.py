#!/usr/bin/env python3
"""Words set in capitals in the text a reader sees.

    tools/audit_caps.py                 # counts per source, worst first
    tools/audit_caps.py --show captions # every flagged line of one source
    tools/audit_caps.py --names         # program names, for a batch

rdoggett, 2026-09-08: "I'd also prefer avoiding ALL CAPS, since it has long
become synonymous with SHOUTING AT PEOPLE."  The captions, DOC/INDEX and
the how-to notes lean on capitals for emphasis -- IGNORES A FILENAME
ARGUMENT, IT STILL RUNS HERE -- and every one of those wants rewriting as a
sentence that carries its own weight.

A word counts when it is two or more capitals in a row and is not a name
that is genuinely spelt that way: OS-9, GNU, TeX, RBF, a program that calls
itself ATerm, a file format.  The list of those is below and grows as the
audit meets them; it is a prompt to go and look, not a verdict.
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(REPO, "tools")
sys.path.insert(0, TOOLS)

# Spelt in capitals by their owners, or capitals by nature: acronyms,
# file formats, key names, the disk's own directories.
NAMES = set("""
OS-9 OS9 OSK GNU TeX LaTeX DVI PK GF TFM PS EPS PDF ASCII EBCDIC CP437 ANSI
VT100 VT52 VT220 DEC IBM PC MS-DOS DOS CP/M CPM RBF SCF SBF PIPEMAN GFM
RAM ROM CPU MMU FPU I/O SCSI IDE EFFO CERN RTF SNOBOL SNOBOL4 BASIC BASIC09
C C++ K&R ANSI-C UUCP SMTP NNTP POP FTP TCP IP TCP/IP UDP ARP PPP SLIP
PORT URL HTTP HTML WN ELM MH RCS SCCS CVS ZIP ARC ZOO LZH LHA TAR CPIO AR
PBM PGM PPM PNM PNG GIF TIFF JPEG JPG BMP PICT MacPaint XBM XPM XWD ILBM
IFF RLE SGI TGA YUV RGB HSV CMYK NTSC PAL PCX PI1 PI3 MGR CMU
CRC MD5 UUE XX BinHex HQX PATH TERM TERMCAP HOME USER SHELL MAIL PWD
CMDS DOC SYS GAMES SRC LIB DEFS USR SPOOL TMP LOG NETPBM REBUILT TEXCMDS
COMMS NETWORK NEWS ADL DEMOS DHRY GCC GCC2 GCC139 ELM UUCP WN SBPROLOG
CTRL ESC RETURN ENTER DEL TAB BS CR LF EOF XOFF XON NUL
A-Z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
II III IV VI VII VIII IX XI XII MM1 MM/1 X11 X11R6 SYSV BSD 4.3BSD
ATerm AtoB BtoA FStat UnMacpack PrintCards PrintLabels EditLibr Librarian
Ascii2Libr Libr2Ascii X11R6shl SEDT PVIC PVic GSHELL MSHELL WORLD ADVENT
ZORK Infocom ZIP CANON HP HPGL LJ LJ2 QMS PS LN03 LN03+ NEC OKI
ID PID GID UID CIO CSL MATH FPU040 CIO020 CSL020 MATH881
SDK GPL KA9Q OSKNET CGI USENET MM/1 CPU32 SLIP PK144 PK300 SIR YUV
UUCPbb LZH DVI TeX RTF/68K RTF ATP GNU_ATP_1_40 I-CODE OS9DISK OS9H0
SOURCES CDEF CLIB K5JB AX.25 ZMODEM XMODEM YMODEM NAME=value
ABC ISO DIN UTC GMT AM PM
""".split())

# A run of capitals that is a whole word: not the `XM' of XModem, not the
# `XPK' of MakeTeXPK, not the `HC11' of 68HC11.
WORD = re.compile(r"(?<![A-Za-z0-9])[A-Z][A-Z0-9'/+.-]*[A-Z0-9](?![a-z])")


def disk_names():
    """Every file and directory name on the disk, as spelt: CMDS, DOC,
    README-CIO, GAMES/adv -- a path in capitals is a name, not a shout."""
    names = set()
    root = os.path.join(REPO, "disk")
    for here, dirs, files in os.walk(root):
        for n in dirs + files:
            names.add(n)
    return names


ON_DISK = None


def shouting(text):
    global ON_DISK
    if ON_DISK is None:
        ON_DISK = disk_names()
    out = []
    for m in WORD.finditer(text):
        w = m.group(0).rstrip(".")
        if len(w) < 2 or w in NAMES or w.rstrip("S") in NAMES:
            continue
        # A path, or a name the disk spells that way.
        if "/" in w or w in ON_DISK or w.rstrip("S") in ON_DISK:
            continue
        # A word of digits and one letter -- 68K, 3B1 -- is a name, not a shout.
        if sum(c.isalpha() for c in w) < 2:
            continue
        out.append(w)
    return out


def captions():
    import screenshots
    out = []
    d = os.path.join(TOOLS, "screenshots")
    for f in sorted(os.listdir(d)):
        if f.endswith(".sheet"):
            for shot in screenshots.parse(os.path.join(d, f)):
                cap = " ".join(shot["cap"])
                hits = shouting(cap)
                if hits:
                    out.append((shot["name"], f, hits, cap))
    return out


def index():
    import gen_catalog
    progs, _, _ = gen_catalog.gather(os.path.join(REPO, "disk"),
                                     os.path.join(TOOLS, "categories.psv"))
    out = []
    for p in progs:
        hits = shouting(p.get("desc") or "")
        if hits:
            out.append((p["name"], "DOC/INDEX", hits, p["desc"]))
    return out


def howto():
    out = []
    for raw in open(os.path.join(TOOLS, "howto.psv")):
        if raw.startswith("#") or "|" not in raw:
            continue
        name, _, text = raw.rstrip("\n").partition("|")
        hits = shouting(text)
        if hits:
            out.append((name.strip(), "howto.psv", hits, text))
    return out


SOURCES = {"captions": captions, "INDEX": index, "howto": howto}


def main(argv):
    if "--show" in argv:
        src = argv[argv.index("--show") + 1]
        for name, where, hits, text in SOURCES[src]():
            print("%-14s %s\n    %s\n" % (name, " ".join(hits), text[:300]))
        return 0
    if "--names" in argv:
        names = sorted({n for fn in SOURCES.values() for n, _, _, _ in fn()})
        print(" ".join(names))
        return 0
    for src, fn in SOURCES.items():
        rows = fn()
        print("%-10s %4d entries shout, e.g. %s" % (
            src, len(rows), ", ".join(sorted({h for _, _, hs, _ in rows for h in hs})[:12])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
