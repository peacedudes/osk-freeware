#!/usr/bin/env python3
"""Compare a re-shot sheet against its published cards -- with tonight's traps built in.

Every one of these cost time on 2026-09-13:

  RAW vs PUBLISHED.  A capture in notes/playtests still says `bash# cmd'
  where the published card says `$ cmd', and screenshots.ink() discards
  any line containing `bash#'.  Comparing the two directly undercounts
  the raw side in proportion to how many commands a stanza runs.  So
  everything here goes through gen_screens.trim() first.

  A GAIN CAN BE A SCROLL.  `config' came back 503 -> 726 and was on its
  way into the gallery: it had lost its command and opening lines, and
  scored higher because the grid kept a denser later section.  A sound
  capture's first line is the stanza's own `try' command.

  A GAIN CAN BE ERROR TEXT.  `newmail' gained a line, and the line was
  `uuname: nowhere found' -- a failed bare-name fork.  Worse, not better.

  AND SOME STANZAS ARE NOT COMPARABLE THIS WAY AT ALL.  `zot' is
  frames=True: filmstrip() samples evenly when there are more frames than
  rows, so its ink tracks how many animation frames a run produced, not
  whether anything was lost.  `back', `backgammon' and `teachgammon' are
  burst=True and captured through a separate unthrottled path.  Reporting
  those four as LOWER is a measurement artefact, which is exactly what
  happened to zot in the games sweep.

Usage:  tools/sweep_measure.py <sheet.sheet>

Run it after re-shooting a sheet, BEFORE promoting anything.  The whole
point is that four different things look like "this card got worse" and
only one of them is.

The sweep that goes with it is measure-only and restores afterwards, so
nothing can reach the gallery while you are still deciding:

    cp notes/playtests/<each>.shot.{txt,hash}  <backup>/     # first
    tools/screenshots.py tools/screenshots/<sheet>           # OS9SDK set
    tools/sweep_measure.py <sheet>
    cp <backup>/*.shot.txt <backup>/*.shot.hash notes/playtests/
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import gen_screens as G          # noqa: E402
import screenshots as S          # noqa: E402

ERR = re.compile(r"nowhere found|cannot execute|can't execute")

# MEASURED non-reproducible: the ink differs run to run and nothing is wrong.
# Reported in their OWN bucket rather than suppressed -- silently excluding a
# stanza would let a real regression hide behind a design excuse.
NONREPRO = {
    "pgmcrater": "pgmtopbm without -threshold: dither differs every run",
    "fish":      "deals a different hand each run",
    "freeb":     "reports live disk statistics",
    "blackjack": "persisted bankroll, a clock time, and a shuffled deck",
    "hang":      "picks a random word, so the letters shown differ",
    "cuts":      "floods `No more memory' -- the refusal count varies, and it "
                 "trips screenshots.py's own `starved' session replacement",
    "ape":       "a Markov text generator: different prose every run",
    "cookie":    "prints a random saying: ink tracks how long it is",
    "fortune":   "prints a random saying: ink tracks how long it is",
}

sheet = sys.argv[1]
real, scroll, errtext, worse, same, skipped = [], [], [], [], 0, []
nonrepro = []
for s in S.parse(os.path.join(REPO, "tools", "screenshots", sheet)):
    n = s["name"]
    cap = os.path.join(REPO, "notes/playtests", n + ".shot.txt")
    pub = os.path.join(REPO, "docs/screens", n + ".txt")
    if not (os.path.exists(cap) and os.path.exists(pub)):
        continue
    if s["frames"] or s["burst"]:
        skipped.append(n)                       # not comparable by ink
        continue
    t = (s["try"] or "").strip()
    out = G.trim(open(cap, errors="replace").read(), t)
    new, old = G.ink(out), G.ink(open(pub, errors="replace").read())
    if not old:
        continue
    if n in NONREPRO:
        if new < old * 0.9 or new > old * 1.1:
            nonrepro.append((n, old, new))
        else:
            same += 1
        continue
    if new < old * 0.9:
        worse.append((n, old, new))
    elif new > old * 1.1:
        first = re.sub(r"^\$\s?", "", out.split("\n")[0]).strip()
        gained_err = bool(ERR.search(out)) and not bool(
            ERR.search(open(pub, errors="replace").read()))
        if first != t:
            scroll.append((n, old, new))
        elif gained_err:
            errtext.append((n, old, new))
        else:
            real.append((n, old, new))
    else:
        same += 1

fmt = lambda rs: ", ".join("%s %d->%d" % r for r in rs[:10])
print("   equivalent      : %d" % same)
print("   REAL candidates : %d  %s" % (len(real), fmt(real)))
print("   gain=scroll     : %d  %s" % (len(scroll), fmt(scroll)))
print("   gain=error text : %d  %s" % (len(errtext), fmt(errtext)))
print("   LOWER           : %d  %s" % (len(worse), fmt(worse)))
if nonrepro:
    print("   non-reproducible: %d  %s  (ink varies by design, see the handoff)"
          % (len(nonrepro), fmt(nonrepro)))
if skipped:
    print("   not comparable  : %d  %s  (frames/burst: measured another way)"
          % (len(skipped), ", ".join(skipped)))
