#!/usr/bin/env python3
r"""Turn the captures into the SAMPLE OUTPUT the catalogue shows.

    tools/screenshots.py --all       # capture the programs, many per run
    tools/playtest.py --all          # play the interactive ones and judge
    tools/gen_screens.py             # fold the captures into the catalogue
    tools/gen_screens.py --check     # exit 1 if any capture has drifted

    docs/screens.js     one screen per program, read by docs/index.html
    docs/screens/*.txt  the same screens as text, because notes/ is scratch

THERE IS ONE CATALOGUE.  These screens used to have a gallery page of their
own, and that was a second catalogue listing the same programs and needing
the same maintenance.  A screen belongs on the program's card, beside its
usage line: sample help, sample output.

Every screen here was CAPTURED FROM A RUNNING PROGRAM on the real disk
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
MANIFEST = os.path.join(DOCS, "screens.stanzas")
PLAYTESTS = os.path.join(REPO, "tools", "playtests")

# What a play-test capture is showing, and which of its snapshots to use.
# The sheets carry their own captions; this covers tools/playtests/*.keys.
CAPTIONS = {
    "tet":      ("Tetris. Pieces stack, rows score, and the high-score table "
                 "at the right is written to /dd/GAMES/tet.hs.", "final"),
    "tet-speed": ("The same board captured 3 seconds into a game. Pieces "
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
    "backgammon": ("The OTHER backgammon -- it asks three questions a single "
                   "key at a time (rules, instructions, colour) and then "
                   "draws its board frame. The points and the pieces do not "
                   "arrive on this terminal; `back' is the one that draws a "
                   "whole board.", "board"),
    "banner":   ("banner, the letters made of their own initials.", "final"),
    "beav":     ("beav, the binary editor, on a file of this disk's own "
                 "documentation: hex on the left, characters on the right.",
                 "final"),
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

# A play-test whose script is named for the SESSION rather than for one
# program: what it illustrates has to be said, or the screen lands in
# `Uncategorised' and hangs on no program's card.
PLAYTEST_FOR = {
    "netpbm":         ["pgmramp", "pgmtopbm", "pbmtoascii", "pnmfile"],
    "netpbm-convert": ["pnmcut", "pnmfile", "pgmramp"],
    "tet-speed":      ["tet"],
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


SHELL_NOISE = ("/.bashrc:", "# /h0:", "# /dd:")
# GNU head announces the file it is reading -- `head: /dd/SYS/motd' on
# its own line, after the text, on stderr. It is a heading printed in the
# wrong place, not an error, and on a card it reads as one. Only the bare
# form goes; `head: unrecognized option `-l'' has more words and stays.
HEAD_BANNER = re.compile(r"^(head|tail): \S+$")
# The shell's prompt, and what to show instead of it. DROPPING the prompt
# lines outright -- which this did at first -- takes the COMMANDS with them,
# so a five-command screen came out as one command and one listing with an
# unexplained gap in the middle. A screen is a session: show the commands,
# just not the prompt they were typed at.
PROMPT = re.compile(r"^bash#\s?")
# A program that ends its output without a newline leaves the next prompt
# sitting on the same line -- `August 28, 2100 04:45:27bash# date -t'. That is
# one line on the terminal and two things to a reader, so it gets split.
RUNON = re.compile(r"(?<=.)bash#(?:\s|$)")
# os9exec's own file-table dump, printed when it reports a crash. The lines
# that NAME the crash are kept -- a program that died should be seen dying --
# but the open-path list belongs to the emulator, not to the program.
DUMP = re.compile(r"^\s*\d\d f(Cons|Pipe|RBF|Disk)\b")


def trim(text, first=""):
    """Drop the shell's own lines, then leading and trailing blank ones.

    A capture holds whatever it took to get the program going -- the emulator
    banner, the exports, the prompt it came back to. None of that is the
    program, and a gallery showing somebody else's shell prompt is not a
    gallery of this software.
    """
    lines = []
    for raw in text.split("\n"):
        # A program whose last write has no newline leaves the next prompt on
        # its own line -- `04:45:27bash# date -t'. Two things to a reader.
        for ln in RUNON.sub("\n$ ", raw).split("\n"):
            if any(n in ln for n in SHELL_NOISE) or DUMP.match(ln):
                continue
            if HEAD_BANNER.match(ln):
                continue
            if ln.startswith("export ") and "PATH" in ln:
                continue                   # the harness's own login lines
            if PROMPT.match(ln):
                rest = PROMPT.sub("", ln).rstrip()
                if not rest:
                    continue               # a bare prompt is not a line
                ln = "$ " + rest
            if ln.strip() == "$":
                continue
            lines.append(ln.rstrip())
    # THE EMULATOR'S OWN DIAGNOSTICS ARE NOT THE PROGRAM'S OUTPUT.  os9exec
    # prints `F$SetSys: unimplemented 03D8' to the console when a program
    # reads a system global it does not model, and the C run-time of
    # several programs here reads that one four times at start-up.  It is
    # noise about os9exec on a card about the program; recorded in
    # notes/os9exec-bugs, and left off the picture.
    lines = [ln for ln in lines if not ln.startswith("F$SetSys: unimplemented")]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    # THE FIRST COMMAND HAS NO PROMPT: the screen was cleared before it was
    # typed, so the shell's prompt is on the line the clear took away. It is
    # still a command, and a screen whose first line is the only one without
    # a `$' reads as though something is missing.
    if lines and first and lines[0].strip() == first.strip():
        lines[0] = "$ " + lines[0].strip()
    return "\n".join(lines)


def ink(text):
    return len(re.sub(r"\s", "", text))


def collapse(text, keep=3):
    """Fold a run of identical lines into one line and a count.

    A program that floods -- `No more memory !!!' filling the grid -- is
    worth showing ONCE with the number beside it. Twenty-four copies is not
    sample output, it is a wall, and it pushes the command that caused it off
    the top of the card. rdoggett, 2026-08-28, looking at cvtbase: "I asked
    you to capture an interesting screen shot, this is what you saved".
    """
    out, lines = [], text.split("\n")
    i = 0
    while i < len(lines):
        j = i
        while j + 1 < len(lines) and lines[j + 1] == lines[i]:
            j += 1
        run = j - i + 1
        if run > keep and lines[i].strip():
            out.append(lines[i])
            out.append("        ... the same line %d times over" % run)
        else:
            out.extend(lines[i:j + 1])
        i = j + 1
    return "\n".join(out)


def sheet_shots():
    """Every stanza in every sheet: its caption and what it illustrates."""
    shots = {}
    if not os.path.isdir(SHEETS):
        return shots
    for f in sorted(os.listdir(SHEETS)):
        if not f.endswith(".sheet"):
            continue
        parsed = screenshots.parse(os.path.join(SHEETS, f))
        screenshots.check_names(parsed)
        # AND ACROSS SHEETS. check_names only sees one sheet at a time, and
        # two sheets can name the same stanza: `greg' was defined in both
        # system.sheet and calendars.sheet on 2026-08-29, the later one won
        # silently, and the drift report said the capture was stale for ever
        # because it was being compared against the OTHER stanza's hash.
        for shot in parsed:
            if shot["name"] in shots:
                sys.exit("%s: `%s' is already defined in %s.sheet -- two "
                         "stanzas of one name share one capture file"
                         % (f, shot["name"], shots[shot["name"]]["sheet"]))
        for shot in parsed:
            first = next((v for k, v in shot["acts"] if k == "run"), "")
            shots[shot["name"]] = {"hash": screenshots.stanza_hash(shot),
                                   "first": first,
                                   # Everything the stanza actually typed, so
                                   # `demonstrated' below can tell a program
                                   # that was RUN from one merely credited.
                                   "typed": " ".join(
                                       v for k, v in shot["acts"]
                                       if k in ("run", "send", "setup")),
                                   "cap": " ".join(shot["cap"]),
                                   "for": shot["for"] or [shot["name"]],
                                   "sheet": f[:-6],
                                   "path": os.path.join(SHEETS, f)}
    return shots


def pick(name, want, first=""):
    """The screen to publish: the asked-for snapshot, else the fullest."""
    cands = []
    for f in os.listdir(CAPS):
        m = re.match(re.escape(name) + r"\.([A-Za-z0-9_]+)\.txt$", f)
        if not m or m.group(1) == "control":
            continue
        label = "final" if m.group(1) == "screen" else m.group(1)
        body = collapse(trim(to_cp437(open(os.path.join(CAPS, f)).read()),
                             first))
        cands.append((label, body, ink(body)))
    if not cands:
        return None
    for label, body, n in cands:
        if label == want and n > 10:
            return label, body
    label, body, _ = max(cands, key=lambda c: c[2])
    return label, body


def collect():
    """One entry per captured program, with what the catalogue knows."""
    progs, _, _ = gen_catalog.gather(os.path.join(REPO, "disk"),
                                  os.path.join(REPO, "tools",
                                               "categories.psv"))
    bycat = {p["name"]: (p["cat"], p["sub"]) for p in progs}
    sheets = sheet_shots()
    names = sorted({f.split(".")[0] for f in os.listdir(CAPS)
                    if f.endswith(".txt")})
    # A CAPTURE NO STANZA DEFINES IS NOT A SCREEN.  Probing a program means
    # writing a throwaway sheet and capturing it, and those captures land in
    # the same directory as the real ones -- `advprobe2' was published to
    # docs/screens/ and committed on 2026-08-29 with no caption and no
    # programs, purely because it had ink in it.  Say what is being skipped;
    # a capture nobody meant to keep is a capture to delete.
    # THREE THINGS DEFINE A SCREEN, not one: a stanza in a sheet, an entry in
    # CAPTIONS, or a play-test -- `playtest.py' writes its screens into the
    # same directory, and gnuchessn, pacman, maze and eight others are
    # published from there.  A first cut of this check knew only about sheets
    # and would have dropped all eleven.
    played = {f[:-5] for f in os.listdir(PLAYTESTS)} if os.path.isdir(PLAYTESTS) else set()
    orphans = [n for n in names
               if n not in sheets and n not in CAPTIONS and n not in played]
    if orphans:
        print("  %d capture(s) belong to no stanza and are NOT published: %s"
              % (len(orphans), " ".join(orphans[:8])))
    names = [n for n in names if n not in orphans]

    out = []
    for name in names:
        meta = sheets.get(name)
        want = meta and "shot" or CAPTIONS.get(name, (None, "final"))[1]
        got = pick(name, want, meta["first"] if meta else "")
        if not got:
            continue
        label, screen = got
        if ink(screen) < 30:
            continue                       # nothing worth looking at
        caption = (meta["cap"] if meta
                   else CAPTIONS.get(name, ("",))[0]) or "Captured while running."
        shows = meta["for"] if meta else PLAYTEST_FOR.get(name, [name])
        cat = next((bycat[p] for p in shows if p in bycat),
                   bycat.get(name, ("Uncategorised", "")))
        # The fingerprint of the stanza AS IT WAS WHEN THIS CAPTURE WAS
        # TAKEN, not as the sheet reads now -- that difference is the whole
        # of the drift check, and it is what goes in the manifest.
        stamp = os.path.join(CAPS, "%s.shot.hash" % name)
        taken = open(stamp).read().strip() if os.path.exists(stamp) else ""
        out.append({"name": name, "cap": caption, "screen": screen,
                    "for": [p for p in shows if p in bycat],
                    "stanza_hash": taken,
                    "cat": cat[0], "sub": cat[1]})
    return out


def check_against_manifest():
    """Drift check for a checkout with no captures -- CI, or a fresh clone.

    Compares each sheet stanza against the fingerprint recorded in
    `docs/screens.stanzas' when its screen was published.  It cannot tell a
    stanza that was never captured from one whose screen is simply not
    published (a card under the ink threshold), so it reports only DRIFT.
    """
    if not os.path.exists(MANIFEST):
        sys.exit("gen_screens: no captures and no %s -- nothing to check "
                 "against" % os.path.basename(MANIFEST))
    taken = {}
    for line in open(MANIFEST):
        if line.startswith("#") or not line.split():
            continue
        name, _, h = line.partition(" ")
        taken[name] = h.strip()
    drifted = [n for n, meta in sorted(sheet_shots().items())
               if n in taken and taken[n] != meta["hash"]]
    if drifted:
        sys.exit("gen_screens: %d stanza(s) have been edited since their "
                 "screen was published: %s\n   Re-shoot them with "
                 "tools/screenshots.py --only %s"
                 % (len(drifted), " ".join(drifted[:8]), ",".join(drifted[:8])))
    print("  %d published screens, none drifted from its stanza" % len(taken))
    return 0


def main():
    if not os.path.isdir(CAPS) or not os.listdir(CAPS):
        # NO CAPTURES IS THE NORMAL STATE OF A FRESH CHECKOUT: they are
        # gitignored.  Before 2026-08-29 this exited 1 whatever was asked of
        # it, which made the `--check' step in CI fail on every push.
        if "--check" in sys.argv:
            return check_against_manifest()
        sys.exit("no captures in %s -- run tools/screenshots.py --all first"
                 % CAPS)
    entries = collect()

    # Start clean: a screen that no longer qualifies must not linger from a
    # previous run and end up in the catalogue by accident.
    if os.path.isdir(KEEP):
        shutil.rmtree(KEEP)
    os.makedirs(KEEP, exist_ok=True)

    # WHICH CARD A PROGRAM'S SCREEN COMES FROM, in three tiers.  These were
    # assigned in one pass, first card to claim a name -- which is
    # alphabetical order and nothing more -- and it published the wrong
    # screen twice over.  `rdoc' has a card of its own showing it turn C
    # source into a structure chart and published the `helpindex' usage
    # message, because helpindex sorts first and lists rdoc in its `for'
    # line: 47 programs were affected.  Then `autolf' published the `expand'
    # card, which never types it, while the `todos' card does: 13 more.
    #
    #   1. the card NAMED for the program
    #   2. a card that actually RUNS it
    #   3. anything that credits it
    #
    # Tier 3 is not a failure -- eleven DVI drivers sharing one screen is
    # right -- it is just the weakest claim, and should lose to the other
    # two rather than to the alphabet.
    sheets_by_name = sheet_shots()

    def types(card, prog):
        meta = sheets_by_name.get(card)
        return bool(meta) and bool(
            re.search(r"(^|[/ ])%s\b" % re.escape(prog), meta.get("typed", "")))

    screens = {}
    ordered = sorted(entries, key=lambda x: x["name"].lower())
    for tier in (1, 2, 3):
        for e in ordered:
            for prog in e["for"]:
                rank = 1 if prog == e["name"] else 2 if types(e["name"], prog) else 3
                if rank == tier:
                    screens.setdefault(prog, {"n": e["name"], "c": e["cap"],
                                              "s": e["screen"]})
    for e in ordered:
        open(os.path.join(KEEP, "%s.txt" % e["name"]), "w").write(
            fold_ascii(e["screen"]) + "\n")

    with open(os.path.join(DOCS, "screens.js"), "w") as f:
        f.write("// Generated by tools/gen_screens.py -- do not edit.\n"
                "// One captured screen per program: docs/index.html shows\n"
                "// it on that program's card, under `Sample output'.\n"
                "window.SCREENS = ")
        json.dump(screens, f, ensure_ascii=True, separators=(",", ":"),
                  sort_keys=True)
        f.write(";\n")

    # THE FINGERPRINT OF THE STANZA EACH PUBLISHED SCREEN WAS TAKEN FROM,
    # committed.  The captures themselves are not in the repository (they are
    # a hundred megabytes of terminal grids and `.gitignore' has always said
    # so), and without this file the drift check below has nothing to compare
    # on a fresh checkout: it reported all 478 stanzas as uncaptured and
    # exited 1.  A CI step added on 2026-08-29 to run `--check' would have
    # failed on every push for exactly that reason.
    manifest = {e["name"]: e["stanza_hash"] for e in entries
                if e.get("stanza_hash")}
    with open(MANIFEST, "w") as f:
        f.write("# Generated by tools/gen_screens.py -- do not edit.\n"
                "# <stanza> <sha1 of the stanza the published screen came\n"
                "# from>.  `--check' compares these against the sheets, which\n"
                "# is the only way to detect drift where the captures are not.\n")
        for name in sorted(manifest):
            f.write("%s %s\n" % (name, manifest[name]))

    # KEEPING THIS TRUE IS THE HARD PART, so say what has drifted rather than
    # leaving it to be noticed. A stanza edited after its capture was taken
    # publishes the OLD screen under the NEW caption, which is the one way
    # this can lie without anybody touching a program.
    stale, missing = [], []
    for name, meta in sorted(sheet_shots().items()):
        cap = os.path.join(CAPS, "%s.shot.txt" % name)
        stamp = os.path.join(CAPS, "%s.shot.hash" % name)
        if not os.path.exists(cap):
            missing.append(name)
        elif os.path.exists(stamp) and open(stamp).read() != meta["hash"]:
            stale.append(name)
    if missing:
        print("  %d stanzas have no capture -- re-shoot them: %s"
              % (len(missing), " ".join(missing[:8])))
    if stale:
        print("  %d captures are OLDER than the sheet that defines them: %s"
              % (len(stale), " ".join(stale[:8])))

    # HOW MANY OF THOSE PROGRAMS WERE ACTUALLY RUN.  A stanza's `for' line
    # credits a screen to several programs, and that is right where they
    # behave alike -- eleven dvi drivers, a shelf of device descriptors.  It
    # is not right everywhere: the `scsiutil' card credited `read_mail' and
    # `add_errmsg', which have nothing to do with SCSI and which it never
    # typed.  "918 of 918 have sample output" cannot fail while grouping
    # satisfies it, so say the number that can.
    # DISTINCT programs, to be comparable with the total beside it: a
    # program credited on two cards and run on one has been run.
    shown = set()
    for meta in sheet_shots().values():
        typed = meta.get("typed", "")
        for prog in meta["for"]:
            if re.search(r"(^|[/ ])%s\b" % re.escape(prog), typed):
                shown.add(prog)
    shown = len(shown & set(screens))
    print("  %d screens, %d programs (%d of them run by name on their own "
          "card; the rest are credited to one)" % (len(entries), len(screens), shown))
    print("  %s" % os.path.join(DOCS, "screens.js"))
    print("  %s" % KEEP)

    # --check MAKES THE DRIFT FATAL. Printing it was not enough: a stanza
    # edited after its capture was taken publishes the OLD screen under the
    # NEW caption, and that is the one way a card can lie without anybody
    # touching a program. It happened four times in one session and was
    # caught each time only because somebody read the line. CI reads nothing.
    if "--check" in sys.argv and (missing or stale):
        sys.exit("gen_screens: %d without a capture, %d stale -- "
                 "re-shoot them with tools/screenshots.py before committing"
                 % (len(missing), len(stale)))


if __name__ == "__main__":
    main()
