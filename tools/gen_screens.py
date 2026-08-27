#!/usr/bin/env python3
"""Build docs/screens.html from the play-test captures.

    tools/playtest.py --all          # play everything, capture the screens
    tools/gen_screens.py             # turn the captures into a gallery

Every screen here was PHOTOGRAPHED FROM A RUNNING PROGRAM: keystrokes went in
through os9exec's console at human speed and the terminal stream that came
back was rendered by tools/ansiscreen.py. Nothing is mocked up and nothing is
retyped. That is the point -- the four-stage sweep can only say a program
printed something, and it credited `tet' as working while `tet' ignored the
keyboard.

`notes/playtests/' is scratch and gitignored, so the chosen screens are copied
into `docs/screens/' where they survive.
"""
import os
import re
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAPS = os.path.join(REPO, "notes", "playtests")
OUT = os.path.join(REPO, "docs", "screens.html")
KEEP = os.path.join(REPO, "docs", "screens")

# Which snapshot to show, and what to say about it. A program is worth a
# caption that tells you what you are looking at; "screenshot" is not one.
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
    "hack":     ("hack -- currently HANGS after taking your name. Kept here "
                 "because the failure is the finding.", "named"),
}

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
 .lede{color:var(--dim);max-width:46rem;margin:0 0 2rem}
 .shot{background:var(--card);border:1px solid var(--rule);border-radius:8px;
       padding:1rem 1.1rem;margin:0 0 1.6rem;overflow:hidden}
 .shot h2{font-size:1.05rem;margin:0 0 .15rem;font-family:var(--mono);
          color:var(--accent)}
 .shot p{margin:0 0 .7rem;color:var(--dim);font-size:.92rem}
 pre{margin:0;font-family:var(--mono);font-size:11.5px;line-height:1.18;
     background:#0E1113;color:#CFE3CF;padding:.85rem 1rem;border-radius:5px;
     overflow-x:auto;white-space:pre}
 footer{color:var(--dim);font-size:.85rem;margin-top:2.5rem;
        border-top:1px solid var(--rule);padding-top:1rem}
</style>
<div class="wrap">
<h1>Screens</h1>
<p class="lede">Every screen below was photographed from a running program.
Keystrokes were fed to os9exec's console at human speed and the terminal
stream that came back was rendered into the grid a vt100 would have shown.
Nothing here is mocked up.</p>
"""


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def trim(text):
    """Drop leading/trailing blank lines; keep the shape of what is left."""
    lines = [l.rstrip() for l in text.split("\n")]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def ink(text):
    return len(re.sub(r"\s", "", text))


def pick(name):
    """The captured screen to publish: the asked-for one, else the fullest."""
    want = CAPTIONS.get(name, (None, "final"))[1]
    cands = []
    for f in os.listdir(CAPS):
        m = re.match(re.escape(name) + r"\.([A-Za-z0-9_]+)\.txt$", f)
        if not m or m.group(1) == "control":
            continue
        label = "final" if m.group(1) == "screen" else m.group(1)
        body = trim(open(os.path.join(CAPS, f)).read())
        cands.append((label, body, ink(body)))
    if not cands:
        return None
    for label, body, n in cands:
        if label == want and n > 10:
            return label, body
    label, body, _ = max(cands, key=lambda c: c[2])
    return label, body


def main():
    if not os.path.isdir(CAPS):
        sys.exit("no captures in %s -- run tools/playtest.py --all first" % CAPS)
    os.makedirs(KEEP, exist_ok=True)
    names = sorted({f.split(".")[0] for f in os.listdir(CAPS)
                    if f.endswith(".txt")})
    body, kept = [], 0
    for name in names:
        got = pick(name)
        if not got:
            continue
        label, screen = got
        if ink(screen) < 30:
            continue                      # nothing worth looking at
        caption = CAPTIONS.get(name, ("", ""))[0] or "Captured while running."
        open(os.path.join(KEEP, "%s.txt" % name), "w").write(screen + "\n")
        body.append('<div class="shot">\n<h2>%s</h2>\n<p>%s</p>\n'
                    '<pre>%s</pre>\n</div>' % (esc(name), esc(caption),
                                               esc(screen)))
        kept += 1
    with open(OUT, "w") as f:
        f.write(PAGE_HEAD)
        f.write("\n".join(body))
        f.write('\n<footer>Captured by <code>tools/playtest.py</code> and '
                'rendered by <code>tools/ansiscreen.py</code>. '
                'Re-make with <code>tools/playtest.py --all && '
                'tools/gen_screens.py</code>.</footer>\n</div>\n')
    print("wrote %s -- %d screens" % (OUT, kept))
    print("kept the text in %s" % KEEP)


if __name__ == "__main__":
    main()
