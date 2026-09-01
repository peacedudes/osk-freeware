#!/usr/bin/env python3
"""Which gallery cards show a program WORKING, and which do not.

    tools/audit_cards.py                # the flagged ones, worst first
    tools/audit_cards.py --all          # every card and its score
    tools/audit_cards.py --show <name>  # one card's capture, in full

WHY THIS EXISTS, and why `audit_screens.py' is not enough
--------------------------------------------------------
`audit_screens.py' flags a card whose EVERY line is an error.  On a real
capture the typed command line is one of those lines and is not an error, so
the rule almost never fires: it reported 2 of 407 on 2026-08-31.  That is a
check that cannot fail, which is this collection's oldest recurring defect.

rdoggett, 2026-08-31: *"Sample output that does nothing more than show the
help is only valuable if the help isn't shown some other way, and there is no
more interesting output from the program to show."*  And, of `hc': a card
that shows a FAILED invocation, captioned as though the program were at
fault, is worse than no card.

So this scores each card by what its lines ARE, per command run:

    USAGE     the program answered with its own usage or syntax line
    ERROR     an OS-9 error, a trap, a "not found", a "can't"
    WORK      anything else -- the program doing its job

A card is flagged when it has no WORK at all, or when errors outnumber work.
It is a PROMPT TO GO AND LOOK, not a verdict: `spiff' prints nothing because
the two files matched, which is the point of that card, and a diff tool
saying "files differ" is doing its job in words that read like an error.
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAPS = os.path.join(REPO, "notes", "playtests")

# The shell's own prompt, in every form the captures carry it.
PROMPT = re.compile(r"^(bash#|os9\$|\$)\s?")

USAGE = re.compile(r"(?i)^\s*(usage|syntax|use\b|options?)\s*[:\-]"
                   r"|^\s*usage\s*$")
ERROR = re.compile(
    r"(?i)(error\s*#|\berror\b|can't|cannot|couldn't|unable to|not found"
    r"|no such|\*\*\*\*|unknown option|illegal|invalid|bad |permission"
    r"|E\$[A-Za-z]|vector=\$|not accessible|no more memory|abort)")


def sheet_commands():
    """shot name -> the set of command lines its stanza runs."""
    sys.path.insert(0, os.path.join(REPO, "tools"))
    import screenshots                                   # noqa: E402
    out = {}
    sheets = os.path.join(REPO, "tools", "screenshots")
    for f in sorted(os.listdir(sheets)):
        if not f.endswith(".sheet"):
            continue
        for shot in screenshots.parse(os.path.join(sheets, f)):
            runs = {v.strip() for k, v in shot["acts"] if k == "run"}
            out.setdefault(shot["name"], set()).update(runs)
    return out


def commands(name, sheets):
    """The exact command lines this card typed, from its own sheet stanza.

    A capture does NOT reliably prefix an echoed command with a prompt -- the
    shell's prompt is overwritten by a program that clears the screen, so the
    next command lands bare.  Scoring those bare echoes as the program's own
    output was worth several points of `work' on every card and hid exactly
    the cards this tool is for.  The sheet knows what was typed; ask it.
    """
    return sheets.get(name, set())


def classify(path, typed):
    usage = err = work = 0
    body = []
    for raw in open(path, errors="replace").read().split("\n"):
        line = raw.rstrip()
        stripped = PROMPT.sub("", line).strip()
        if not stripped:
            continue
        if PROMPT.match(line) or not body or stripped in typed:
            # The command that was typed: not evidence either way.
            body.append(stripped)
            continue
        body.append(stripped)
        if USAGE.search(stripped):
            usage += 1
        elif ERROR.search(stripped):
            err += 1
        else:
            work += 1
    return usage, err, work, body


def main(argv):
    show = None
    everything = False
    i = 0
    while i < len(argv):
        if argv[i] == "--all":
            everything = True
        elif argv[i] == "--show":
            i += 1
            show = argv[i]
        else:
            sys.exit(__doc__)
        i += 1

    if show:
        p = os.path.join(CAPS, "%s.shot.txt" % show)
        if not os.path.exists(p):
            sys.exit("no capture for %s" % show)
        sys.stdout.write(open(p, errors="replace").read())
        return 0

    sheets = sheet_commands()
    rows = []
    # TWO CARDS ARE FLAGGED CORRECTLY BY THE RULE AND WRONGLY BY THE POINT.
    # `perr' turns an OS-9 error number into its message, so error text IS
    # its output and a screen full of `Error #000:216' is exactly right.
    # Listing them here rather than weakening the rule: a rule that stopped
    # noticing error-only screens would stop finding the ones that matter.
    fine = {"perr": "perr PRINTS error messages -- error text is its output",
            "perr-print": "the same program, printing a wider range",
            "csl-mismatch": "the card's SUBJECT is the csl edition skew -- "
                            "four programs that stop before they start, and "
                            "the message is the whole finding"}
    for f in sorted(os.listdir(CAPS)):
        if not f.endswith(".shot.txt"):
            continue
        name = f[:-len(".shot.txt")]
        usage, err, work, body = classify(os.path.join(CAPS, f),
                                          commands(name, sheets))
        why = ("NOTHING" if not (usage or err or work) else
               "HELP-ONLY" if work == 0 and usage and not err else
               "ERROR-ONLY" if work == 0 and err and not usage else
               "HELP+ERROR" if work == 0 else
               "MOSTLY-ERROR" if err > work else
               "MOSTLY-HELP" if usage > work else
               # A usage line plus two or three lines of anything is still a
               # card whose subject is the help text.  rdoggett's test is
               # whether there is MORE INTERESTING OUTPUT to show, and a
               # near-empty screen carrying a syntax line says there is not.
               "THIN-HELP" if usage and work <= 3 else "")
        if name in fine:
            why = ""
        rows.append((name, why, usage, err, work, body))

    flagged = [r for r in rows if r[1]]
    order = {"NOTHING": 0, "ERROR-ONLY": 1, "HELP+ERROR": 2, "HELP-ONLY": 3,
             "MOSTLY-ERROR": 4, "MOSTLY-HELP": 5, "THIN-HELP": 6, "": 9}
    for name, why, u, e, w, body in sorted(everything and rows or flagged,
                                           key=lambda r: (order[r[1]], r[0])):
        first = next((b for b in body[1:]), "") if body else ""
        print("%-20s %-12s help=%-3d err=%-3d work=%-4d %s"
              % (name, why or "ok", u, e, w, first[:44]))
    print("\n%d of %d cards flagged" % (len(flagged), len(rows)))
    for name, why in sorted(fine.items()):
        print("  (not flagged, by name: %-12s %s)" % (name, why))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
