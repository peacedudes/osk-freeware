#!/usr/bin/env python3
r"""Build the screen gallery, and the screens the catalogue shows.

    tools/screenshots.py --all       # photograph the programs, many per run
    tools/playtest.py --all          # play the interactive ones and judge
    tools/gen_screens.py             # turn the captures into the gallery

    docs/screens.html   the gallery, grouped the way the catalogue groups
    docs/screens.js     the same screens, keyed by program, for docs/index.html
    docs/screens/*.txt  the chosen screens as text, because notes/ is scratch

Every screen here was PHOTOGRAPHED FROM A RUNNING PROGRAM on the real disk
image: keystrokes went into os9exec's console and the terminal stream that
came back was rendered by tools/ansiscreen.py. Nothing is mocked up, nothing
is retyped, and a program that failed is shown failing.

Two things are decided here rather than at capture time:

  * THE HIGH HALF IS READ AS CP437. `cal' rules its columns off with $C4 and
    `dm' draws its box with $C9 $CD $BB -- IBM-PC line drawing, which is what
    the terminals these programs were written for displayed. Read as Latin-1
    the same bytes are `A-umlaut', which is what the first version of this
    gallery published. Where a program meant some other set the picture is
    wrong in exactly that way and no other.

  * THE FILES STAY ASCII. The HTML and the JavaScript carry the real
    characters as numeric escapes, so the sources are plain ASCII; the .txt
    copies fold the line drawing down to `-', `|' and `+', which is lossy and
    says so here rather than in a surprise.
"""
import json
import os
import re
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import gen_catalog                                       # noqa: E402
import screenshots                                       # noqa: E402

CAPS = os.path.join(REPO, "notes", "playtests")
SHEETS = os.path.join(REPO, "tools", "screenshots")
DOCS = os.path.join(REPO, "docs")
KEEP = os.path.join(DOCS, "screens")

# What a play-test capture is showing, and which of its snapshots to use.
# The sheets carry their own captions; this covers tools/playtests/*.keys.
CAPTIONS = {
    "tet":      ("Tetris. Pieces stack, rows score, and the high-score table "
                 "at the right is written to /dd/GAMES/tet.hs.", "final"),
    "tet-speed": ("The same board photographed 3 seconds into a game. Pieces "
                  "fall at about 1.5 seconds a cell.", "t03"),
    "greed":    ("Greed: eat digits, each one moves you that far. The whole "
                 "board is generated at random on startup.", "opening"),
    "hang":     ("Hangman, after guessing a e i o u r s t l n -- the guessed "
                 "letters are struck from the alphabet and the gallows grows.",
                 "more"),
    "cribbage": ("Cribbage dealing a hand.", "play"),
    "mille":    ("Mille Bornes, the card game.", "final"),
    "robots":   ("Robots. They chase you; you teleport.", "final"),
    "lander":   ("Lunar lander, with its instrument panel.", "final"),
    "puzzle15": ("The fifteen puzzle.", "final"),
    "bog":      ("Boggle, with its letter grid.", "board"),
    "life":     ("Conway's Life. It detects the oscillator period and says so "
                 "-- this pattern cycles every 8 generations.", "final"),
    "snake":    ("Snake: steer with h j k l, collect the treasure, reach the "
                 "goal without being caught.", "final"),
    "bite":     ("Bite, a snake variant.", "final"),
    "worms":    ("Worms, a screen toy.", "final"),
    "rain":     ("Rain, a screen toy.", "final"),
    "sonnet":   ("Writes (bad) sonnets in iambic pentameter.", "final"),
    "netpbm":   ("A real netpbm pipeline: pgmramp makes a greyscale ramp, "
                 "pgmtopbm dithers it to a bitmap, pbmtoascii renders that as "
                 "text. The gradient is visible in the density of the "
                 "characters.", "asciiart"),
    "wisecrack": ("wisecrack writes to /pipe/txtpipe and prints nothing "
                  "itself; attach a reader and its messages appear.",
                  "ticker"),
    "sc":       ("sc, the spreadsheet, with 42 entered in A0 and the quit "
                 "prompt over it.", "entered"),
    "elvis":    ("Elvis 1.7 -- the best documented of this disk's three vi "
                 "editors -- displaying DOC/README-CIO.", "final"),
    "advent":   ("Colossal Cave Adventure, at the well house where every "
                 "player of it starts.", "final"),
    "animal":   ("The guess-the-animal game, which learns a new question "
                 "every time it loses.", "final"),
    "back":     ("Backgammon, with the board drawn in characters.", "final"),
    "banner":   ("banner, the letters made of their own initials.", "final"),
    "beav":     ("beav, the binary editor, on a file of this disk's own "
                 "documentation: hex on the left, characters on the right.",
                 "final"),
    "bio":      ("bio is BASIC09 I-code, not a 68000 module, and there is no "
                 "runb on this disk -- so the shell says `cannot execute "
                 "binary file'.", "final"),
    "cal":      ("cal printing a month.  It wants flags -- -m for the months "
                 "and -y for the year -- not two bare numbers.", "output"),
    "cam":      ("cam computes camshaft timing: lift, duration and rocker "
                 "ratio for an engine you describe to it.", "final"),
    "card":     ("A Towers of Hanoi whose twelve disks spell out a Christmas "
                 "message.", "final"),
    "chess":    ("The 68k chess port asking how you want to play before it "
                 "sets the board.", "final"),
    "colortest": ("colortest wants G-Windows, which is not here, and says so "
                  "rather than drawing anything: `Not a G-Windows sytem???' "
                  "-- its own spelling.", "final"),
    "crib":     ("Cribbage, offering its instructions first.", "final"),
    "dclock":   ("dclock is another G-Windows program: it says so and stops. "
                 "`digclk' is the clock that works on a terminal.", "final"),
    "ed":       ("GNU ed cannot start here: it makes its temporary file at "
                 "/r0, the RAM disk os9exec has no way to provide.", "final"),
    "editor":   ("The GSHELL editor front end aborts on startup (E_PRCABT).",
                 "final"),
    "england":  ("The weather simulator set in England -- mid-Atlantic, and "
                 "raining.", "final"),
    "fortune":  ("fortune, reading the collection's own quotation file.",
                 "final"),
    "gnuan":    ("gnuan annotates a saved chess game move by move, using GNU "
                 "Chess's opening book -- 9585 of its 12000 entries.",
                 "final"),
    "hexed":    ("hexed writes its work file to /r0 and stops when it cannot "
                 "-- the RAM disk os9exec has no way to provide.", "final"),
    "larn":     ("Larn: your daughter has a strange disease and the dungeon "
                 "has the cure.  Fixed here -- its help, fortune and maze "
                 "files were recovered from the 12.2p4 sources.", "final"),
    "lissaj":   ("A Lissajous figure generator, drawing the curve two "
                 "oscillators trace against each other.", "final"),
    "logisim":  ("A logic-circuit simulator.  It wants a file describing the "
                 "circuit; with none it prints its own syntax.", "final"),
    "me":       ("me, a screen editor, showing DOC/README-CIO.", "final"),
    "mg":       ("mg, the small emacs, showing the same file.", "final"),
    "mines":    ("Minesweeper on a sixteen-by-sixteen board.", "final"),
    "netpbm-convert": ("A netpbm session at the shell: a ramp made, cut down "
                       "with pnmcut, and identified at each step.",
                       "final"),
    "nobs":     ("nobs, a cribbage variant, dealing its cards.", "final"),
    "piano":    ("piano plays notes through the terminal bell; with no "
                 "arguments it prints what it wants.", "final"),
    "puz15":    ("The fifteen puzzle, drawn in a box.", "final"),
    "pwgen":    ("A random password generator; its usage line is what it "
                 "prints when given no length.", "final"),
    "rpoem":    ("A random poem generator -- one of four SNOBOL4 programs "
                 "here, with their data in GAMES/SNOBOL.", "final"),
    "rstory":   ("A random story generator from the same SNOBOL4 shelf, "
                 "writing roff input.", "final"),
    "sokoban":  ("Sokoban: push the boxes onto the marks.  Without USER set "
                 "it stops with `cannot get your username', which is why "
                 "SYS/login sets it.", "final"),
    "suicide":  ("An animation: a stick figure walks off a rooftop.",
                 "final"),
    "teachgammon": ("The backgammon tutor, which explains the rules and then "
                    "plays a practice game against you.", "final"),
    "tess":     ("Beyond The Tesseract, a text adventure of its own.",
                 "final"),
    "textb":    ("The Mandelbrot set in ASCII: it asks for a centre, a range "
                 "and an iteration count.", "final"),
    "today":    ("today prints the date, the time and the phase of the moon "
                 "in words -- and gets the year right, which `date' does "
                 "not.", "final"),
    "touchtype": ("A typing tutor.", "final"),
    "travesty": ("travesty makes a Markov chain of its input and writes new "
                 "text from it.", "final"),
    "tt":       ("Tetris for Terminals, a second Tetris beside `tet'.",
                 "final"),
    "ularn":    ("Ularn, the other Larn, choosing a character class.",
                 "final"),
    "VI":       ("The EFFO vi -- its source in SRC/effo_vi is the Berkeley "
                 "ex source.", "final"),
    "vi_cio":   ("vi as built against cio, showing DOC/README-CIO.", "final"),
    "vi_nocio": ("PVic, the vi that needs no trap handler, on the same "
                 "file.", "final"),
    "view":     ("view, the read-only vi.", "final"),
    "vis":      ("vis, a visual editor with its command line at the top.",
                 "final"),
    "wanderer": ("Wanderer: collect the diamonds, do not be crushed.",
                 "final"),
    "wish":     ("wish tells you what you would have wished for in hack.",
                 "final"),
    "world":    ("WORLD, a wilderness adventure -- its data tables are built "
                 "by `convert' and `vtxtcn', both here.", "final"),
    "zot":      ("zot echoes text `in interesting ways'; with no text it "
                 "prints its options.", "final"),
    "hack":     ("hack, with the inventory open: a fighter starts with a two "
                 "handed sword in hand and ring mail worn. @ is you, d your "
                 "dog, G a gnome, $ gold, + a door.", "inventory"),
}

# The line drawing, folded to what a plain ASCII file can hold.
FOLD = {0x2500: "-", 0x2501: "-", 0x2550: "=", 0x2502: "|", 0x2503: "|",
        0x2551: "|", 0x2591: "#", 0x2592: "#", 0x2593: "#", 0x2588: "#",
        0x25a0: "#", 0x2584: "#", 0x2580: "#", 0x00b7: ".", 0x2022: "*",
        0x00b0: "o", 0x00b1: "+", 0x00f7: "/", 0x00d7: "x", 0x2219: ".",
        0x221a: "v", 0x2261: "=", 0x2264: "<", 0x2265: ">", 0x2248: "~"}


def to_cp437(text):
    """Re-read the captured high half as the character set it was written in."""
    out = []
    for ch in text:
        if ch < "\x80":
            out.append(ch)
        else:
            try:
                out.append(bytes([ord(ch)]).decode("cp437"))
            except (ValueError, UnicodeDecodeError):
                out.append(" ")
    return "".join(out)


def fold_ascii(text):
    """Everything above ASCII down to something a .txt file can carry."""
    out = []
    for ch in text:
        if ch < "\x7f":
            out.append(ch)
        elif ord(ch) in FOLD:
            out.append(FOLD[ord(ch)])
        elif 0x2500 <= ord(ch) <= 0x257f:      # the rest of the box drawing
            out.append("+")
        else:
            out.append(".")
    return "".join(out)


def esc(s):
    """HTML-escape, and push everything above ASCII into numeric escapes."""
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return "".join(c if c < "\x7f" else "&#%d;" % ord(c) for c in s)


SHELL_NOISE = ("bash#", "/.bashrc:", "# /h0:", "export ", "# /dd:")
# os9exec's own file-table dump, printed when it reports a crash. The lines
# that NAME the crash are kept -- a program that died should be seen dying --
# but the open-path list belongs to the emulator, not to the program.
DUMP = re.compile(r"^\s*\d\d f(Cons|Pipe|RBF|Disk)\b")


def trim(text):
    """Drop the shell's own lines, then leading and trailing blank ones.

    A capture holds whatever it took to get the program going -- the emulator
    banner, the exports, the prompt it came back to. None of that is the
    program, and a gallery showing somebody else's shell prompt is not a
    gallery of this software.
    """
    lines = [ln.rstrip() for ln in text.split("\n")
             if not any(n in ln for n in SHELL_NOISE) and not DUMP.match(ln)]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def ink(text):
    return len(re.sub(r"\s", "", text))


def sheet_shots():
    """Every stanza in every sheet: its caption and what it illustrates."""
    shots = {}
    if not os.path.isdir(SHEETS):
        return shots
    for f in sorted(os.listdir(SHEETS)):
        if not f.endswith(".sheet"):
            continue
        for shot in screenshots.parse(os.path.join(SHEETS, f)):
            shots[shot["name"]] = {"cap": " ".join(shot["cap"]),
                                   "for": shot["for"] or [shot["name"]],
                                   "sheet": f[:-6]}
    return shots


def pick(name, want):
    """The screen to publish: the asked-for snapshot, else the fullest."""
    cands = []
    for f in os.listdir(CAPS):
        m = re.match(re.escape(name) + r"\.([A-Za-z0-9_]+)\.txt$", f)
        if not m or m.group(1) == "control":
            continue
        label = "final" if m.group(1) == "screen" else m.group(1)
        body = trim(to_cp437(open(os.path.join(CAPS, f)).read()))
        cands.append((label, body, ink(body)))
    if not cands:
        return None
    for label, body, n in cands:
        if label == want and n > 10:
            return label, body
    label, body, _ = max(cands, key=lambda c: c[2])
    return label, body


def collect():
    """One entry per photographed program, with what the catalogue knows."""
    progs, _ = gen_catalog.gather(os.path.join(REPO, "disk"),
                                  os.path.join(REPO, "tools",
                                               "categories.psv"))
    bycat = {p["name"]: (p["cat"], p["sub"]) for p in progs}
    sheets = sheet_shots()
    names = sorted({f.split(".")[0] for f in os.listdir(CAPS)
                    if f.endswith(".txt")})
    out = []
    for name in names:
        meta = sheets.get(name)
        want = meta and "shot" or CAPTIONS.get(name, (None, "final"))[1]
        got = pick(name, want)
        if not got:
            continue
        label, screen = got
        if ink(screen) < 30:
            continue                       # nothing worth looking at
        caption = (meta["cap"] if meta
                   else CAPTIONS.get(name, ("",))[0]) or "Captured while running."
        shows = meta["for"] if meta else [name]
        cat = next((bycat[p] for p in shows if p in bycat),
                   bycat.get(name, ("Uncategorised", "")))
        out.append({"name": name, "cap": caption, "screen": screen,
                    "for": [p for p in shows if p in bycat],
                    "cat": cat[0], "sub": cat[1]})
    return out


PAGE_HEAD = """<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>OS-9/68K Freeware &mdash; screens</title>
<style>
 :root{ --paper:#F4F5F3; --card:#FFF; --ink:#191D21; --dim:#5A646B;
        --rule:#DDE1DE; --accent:#B26A00;
        --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;
        --sans:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; }
 @media (prefers-color-scheme:dark){ :root{
        --paper:#131619; --card:#1A1E22; --ink:#E3E7EA; --dim:#98A4AC;
        --rule:#2A3036; --accent:#E0A040; } }
 *{box-sizing:border-box}
 body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);
      line-height:1.5;padding:2rem 1rem 4rem}
 .wrap{max-width:78rem;margin:0 auto}
 h1{font-size:1.6rem;margin:0 0 .25rem}
 h2.cat{font-size:1.1rem;margin:2.4rem 0 .9rem;padding-bottom:.3rem;
        border-bottom:1px solid var(--rule);letter-spacing:.01em}
 .lede{color:var(--dim);max-width:48rem;margin:0 0 1.5rem}
 .toc{margin:0 0 1rem;font-size:.9rem;color:var(--dim)}
 .toc a{color:var(--accent);text-decoration:none;margin-right:.9rem;
        white-space:nowrap}
 .shot{background:var(--card);border:1px solid var(--rule);border-radius:8px;
       padding:1rem 1.1rem;margin:0 0 1.6rem;overflow:hidden}
 .shot h3{font-size:1.05rem;margin:0 0 .15rem;font-family:var(--mono);
          color:var(--accent)}
 .shot p{margin:0 0 .7rem;color:var(--dim);font-size:.92rem}
 pre{margin:0;font-family:var(--mono);font-size:11.5px;line-height:1.18;
     background:#0E1113;color:#CFE3CF;padding:.85rem 1rem;border-radius:5px;
     overflow-x:auto;white-space:pre}
 footer{color:var(--dim);font-size:.85rem;margin-top:2.5rem;
        border-top:1px solid var(--rule);padding-top:1rem}
 a.back{color:var(--accent)}
</style>
<div class="wrap">
<h1>Screens</h1>
<p class="lede">Every screen below was photographed from a running program on
the disk image. Keystrokes were fed to os9exec's console at human speed and
the terminal stream that came back was rendered into the grid a vt100 would
have shown. Nothing here is mocked up &mdash; where a program failed, its
failure is what you see. <a class="back" href="index.html">Back to the
catalogue</a>.</p>
"""


def slug(cat):
    return re.sub(r"[^a-z0-9]+", "-", cat.lower()).strip("-")


def main():
    if not os.path.isdir(CAPS):
        sys.exit("no captures in %s -- run tools/screenshots.py --all first"
                 % CAPS)
    entries = collect()
    order = [c for c in gen_catalog.ORDER
             if any(e["cat"] == c for e in entries)]
    order += sorted({e["cat"] for e in entries} - set(order))

    # Start clean: a screen that no longer qualifies must not linger from a
    # previous run and end up in the gallery by accident.
    if os.path.isdir(KEEP):
        shutil.rmtree(KEEP)
    os.makedirs(KEEP, exist_ok=True)

    body = ['<p class="toc">' + " ".join(
        '<a href="#%s">%s</a>' % (slug(c), esc(c)) for c in order) + '</p>']
    screens = {}
    for cat in order:
        body.append('<h2 class="cat" id="%s">%s</h2>' % (slug(cat), esc(cat)))
        for e in sorted((x for x in entries if x["cat"] == cat),
                        key=lambda x: x["name"].lower()):
            open(os.path.join(KEEP, "%s.txt" % e["name"]), "w").write(
                fold_ascii(e["screen"]) + "\n")
            body.append('<div class="shot" id="s-%s">\n<h3>%s</h3>\n<p>%s</p>\n'
                        '<pre>%s</pre>\n</div>'
                        % (esc(e["name"]), esc(e["name"]), esc(e["cap"]),
                           esc(e["screen"])))
            for prog in e["for"]:
                screens.setdefault(prog, {"n": e["name"], "c": e["cap"],
                                          "s": e["screen"]})

    with open(os.path.join(DOCS, "screens.html"), "w") as f:
        f.write(PAGE_HEAD)
        f.write("\n".join(body))
        f.write('\n<footer>Captured by <code>tools/screenshots.py</code> and '
                '<code>tools/playtest.py</code>, rendered by '
                '<code>tools/ansiscreen.py</code>. Re-make with '
                '<code>tools/screenshots.py --all</code> then '
                '<code>tools/gen_screens.py</code>.</footer>\n</div>\n')

    with open(os.path.join(DOCS, "screens.js"), "w") as f:
        f.write("// Generated by tools/gen_screens.py -- do not edit.\n"
                "// One photographed screen per program, for the catalogue.\n"
                "window.SCREENS = ")
        json.dump(screens, f, ensure_ascii=True, separators=(",", ":"),
                  sort_keys=True)
        f.write(";\n")

    print("  %d screens over %d categories" % (len(entries), len(order)))
    print("  %s" % os.path.join(DOCS, "screens.html"))
    print("  %s -- %d programs" % (os.path.join(DOCS, "screens.js"),
                                   len(screens)))
    print("  %s" % KEEP)


if __name__ == "__main__":
    main()
