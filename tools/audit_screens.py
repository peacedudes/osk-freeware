#!/usr/bin/env python3
"""Look at what was actually captured, the way a person would.

    tools/screenshots.py --all       # take the pictures
    tools/audit_screens.py           # then LOOK at them

WHY THIS EXISTS.  A harness that collects screens will collect rubbish and
report success: rdoggett, 2026-08-28, reading the `cvtbase' card -- "I asked
you to capture an interesting screen shot, this is what you saved" -- and it
was twenty-four copies of `No more memory !!!'.  Another card carried a
caption about integer division over a screen showing `Can't open file ??'.
Neither is sample output; both passed every check there was.

So this reads every capture and flags the ones not worth showing.  It is a
prompt to go and look, not a verdict: a chess board repeats its rank lines
and a barcode repeats its bars, and both are perfectly good screens.

Flags a screen that is not worth showing:
  WALL      one line repeated more than three times
  THIN      almost nothing on it
  ERRORONLY every line is an error or a diagnostic
  SHELLONLY nothing but the command that was typed
"""
import os, re, sys, collections
CAPS = "notes/playtests"
rows = []
for f in sorted(os.listdir(CAPS)):
    if not f.endswith(".shot.txt"):
        continue
    name = f[:-9]
    lines = [l.rstrip() for l in open(os.path.join(CAPS, f)).read().split("\n")]
    body = [l for l in lines if l.strip() and "bash#" not in l]
    if not body:
        rows.append((name, "SHELLONLY", ""))
        continue
    c = collections.Counter(body)
    top, n = c.most_common(1)[0]
    ink = sum(len(l.strip()) for l in body)
    distinct = len(c)
    if n > 3 and (n >= 0.6 * len(body) or distinct <= 3):
        rows.append((name, "WALL x%d/%d" % (n, len(body)), top[:52]))
    elif ink < 24:
        rows.append((name, "THIN %d" % ink, " ".join(body)[:52]))
    elif all(re.search(r"error|Error|cannot|can't|not found|No such|\*\*\*\*", l)
             for l in body):
        rows.append((name, "ERRORONLY", body[0][:52]))
print("%d screens flagged of %d" % (len(rows), len(os.listdir(CAPS))))
for n, why, ev in rows:
    print("  %-18s %-10s %s" % (n, why, ev))
