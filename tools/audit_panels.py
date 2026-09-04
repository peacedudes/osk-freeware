#!/usr/bin/env python3
"""What each PROGRAM's panel shows of that program -- not what its card shows.

    tools/audit_panels.py                 # the failing programs, worst first
    tools/audit_panels.py --all           # every runnable program and its verdict
    tools/audit_panels.py --summary       # the histogram only
    tools/audit_panels.py --show <name>   # one program's published panel
    tools/audit_panels.py --gate          # the ratchet: exit 1 if a program fails
                                          # and is not on the backlog, or a backlog
                                          # entry now passes

WHY THIS EXISTS beside `audit_cards.py'
---------------------------------------
The gallery is built and audited per CARD and read per PROGRAM.  408 cards
credit 932 programs; 539 of those programs borrow another program's card.
A capture is one final screen, so on a card that runs five programs the
first three have scrolled off before the picture is taken -- and
`audit_cards' scores the card as a whole, so a program rides on its
neighbour's output and the tool said 0 of 408 flagged on the day
rdoggett opened `lessecho' and found `helpindex's help text, `lesskey's
usage line and a bare `lessecho < /nil'.  A check that cannot fail, again.

So this scores what the reader actually sees: the panel published for THIS
program in docs/screens.js, and only the lines that follow THIS program's
own command on it.  The verdicts, worst first:

    no-panel        nothing is published for it
    not-run         its panel is a card that never types it
    scrolled-off    the card types it, but the command is not on the screen
    silent          its command is there and nothing follows it
    error-only      only OS-9 errors, traps, "can't"
    help-only       only its own usage or syntax line
    mostly-error    more error lines than working ones
    play-error      a play-test panel with an error line on it
    work            the program doing its job
    play            a play-test panel with no error on it (still needs eyes)

THE RATCHET.  `tools/panel-backlog.txt' lists the programs known to fail,
one per line.  `--gate' -- what check_disk.py runs -- fails on a program
that fails and is NOT listed, and on a listed program that now PASSES, so
that fixing a card is a line removed from that file and nobody can quietly
regress one.  `tools/panel-exceptions.psv' (name|reason) is for the few
whose panel is right as it stands: `perr' prints error text because error
text is its output.  An exception is a debt with a reason attached; the
backlog is a debt with none.

`OSK_PANEL_BACKLOG' and `OSK_PANEL_EXCEPTIONS' override the two files, so
`check_the_checks.py' can point the gate at a mutated COPY rather than edit
the live ones.
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(REPO, "tools")
sys.path.insert(0, TOOLS)
import audit_cards                                      # noqa: E402
import gen_catalog                                      # noqa: E402
import screenshots                                      # noqa: E402
import worklist                                         # noqa: E402

SCREENS_JS = os.path.join(REPO, "docs", "screens.js")
SHEETS = os.path.join(TOOLS, "screenshots")
PLAYTESTS = os.path.join(TOOLS, "playtests")
BACKLOG = os.environ.get("OSK_PANEL_BACKLOG",
                         os.path.join(TOOLS, "panel-backlog.txt"))
EXCEPTIONS = os.environ.get("OSK_PANEL_EXCEPTIONS",
                            os.path.join(TOOLS, "panel-exceptions.psv"))

FAILING = ("no-panel", "not-run", "scrolled-off", "silent", "error-only",
           "help-only", "mostly-error", "play-error")
ORDER = {v: i for i, v in enumerate(FAILING + ("play", "work"))}


def screens():
    """docs/screens.js: program -> {n: card, c: caption, s: screen}."""
    if not os.path.exists(SCREENS_JS):
        return {}
    js = open(SCREENS_JS).read()
    return json.loads(js[js.index("{"):js.rindex("}") + 1])


def stanzas():
    """card -> the command lines its stanza types."""
    out = {}
    if not os.path.isdir(SHEETS):
        return out
    for f in sorted(os.listdir(SHEETS)):
        if f.endswith(".sheet"):
            for shot in screenshots.parse(os.path.join(SHEETS, f)):
                out[shot["name"]] = [v.strip() for k, v in shot["acts"]
                                     if k == "run"]
    return out


def played():
    """play-test -> every shell line and program name its .keys file has."""
    out = {}
    if not os.path.isdir(PLAYTESTS):
        return out
    for f in sorted(os.listdir(PLAYTESTS)):
        if not f.endswith(".keys"):
            continue
        words = []
        for raw in open(os.path.join(PLAYTESTS, f)):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            word, _, rest = line.partition(" ")
            if word in ("prog", "shell", "setup", "run"):
                words.append(rest.strip())
        out[f[:-5]] = words
    return out


def names_it(prog, line):
    """Does this command line run `prog' -- by bare name or by path?"""
    return re.search(r"(^|[\s/|;=(\"'])%s(?=$|[\s|;<>)\"'])" % re.escape(prog),
                     line) is not None


def typed_here(line, runs):
    """Which typed command this screen line is the echo of, if any.

    A command longer than the screen wraps, so the echo is only its first
    row; match on prefix for anything long enough to have wrapped.
    """
    for r in runs:
        if line == r or (len(line) >= 60 and r.startswith(line)):
            return r
        # bash 1.12 scrolls a line longer than the window sideways and
        # marks it with a leading `<': the echo is then the TAIL of what
        # was typed.
        if line.startswith("<") and len(line) >= 40 and r.endswith(line[1:]):
            return r
    return None


def blocks(screen, runs):
    """[(typed command, the lines that followed it)] in screen order."""
    out, cur = [], None
    for raw in screen.split("\n"):
        line = audit_cards.PROMPT.sub("", raw).strip()
        if not line:
            continue
        r = typed_here(line, runs)
        if r is not None:
            cur = (r, [])
            out.append(cur)
        elif cur is not None:
            cur[1].append(line)
    return out


def score(lines):
    """USAGE, ERROR and WORK line counts.

    A block whose FIRST line is a usage or syntax line is help all the way
    down: `Function:', `Options:' and the option list that follow are the
    same message, and counting them as work is how `helpindex -?' scored as
    the program working.
    """
    usage = err = work = 0
    if lines and audit_cards.USAGE.search(lines[0]):
        return len(lines), 0, 0
    for line in lines:
        if audit_cards.USAGE.search(line):
            usage += 1
        elif audit_cards.ERROR.search(line):
            err += 1
        else:
            work += 1
    return usage, err, work


def verdict_for(prog, panel, cards, plays):
    if panel is None:
        return "no-panel", ""
    card = panel["n"]
    if card in cards:
        runs = cards[card]
        mine = [r for r in runs if names_it(prog, r)]
        if not mine:
            return "not-run", "on the `%s' card" % card
        found = blocks(panel["s"], runs)
        seen = [b for b in found if b[0] in mine]
        # A PROGRAM'S OWN NAMED CARD is judged by whether THE CARD shows
        # work, not by whether output sits after the program's own command
        # line.  A converter that writes a file silently and a following
        # `pnmfile'/`ls' that confirms it is one card doing one program's
        # job; tying the verdict to the exact command line called all of
        # those `silent'.  The strict per-command rule stays for SHARED
        # cards (card != prog), which is what catches a program riding on a
        # neighbour's output -- the lessecho case this tool exists for.
        if card == prog:
            body = [audit_cards.PROMPT.sub("", l).strip()
                    for l in panel["s"].split("\n")]
            body = [l for l in body if l and l not in runs]
            seen = [("", body)]
        if not found:
            # A FULL-SCREEN PROGRAM CLEARS THE COMMAND THAT STARTED IT.  No
            # typed command is on the screen at all, the card runs this
            # program, so the whole screen is its own: touchtype's playing
            # field, rstory's page, logisim's pulse diagram.
            seen = [("", [l.strip() for l in panel["s"].split("\n")
                          if l.strip()])]
        if not seen:
            return "scrolled-off", "on the `%s' card" % card
        usage, err, work = map(sum, zip(*[score(b[1]) for b in seen]))
        first = next((l for b in seen for l in b[1]), "")
        if usage + err + work == 0:
            return "silent", "after `%s'" % seen[0][0][:40]
        if work == 0 and usage and not err:
            return "help-only", first[:44]
        if work == 0:
            return "error-only", first[:44]
        if err > work:
            return "mostly-error", first[:44]
        return "work", first[:44]
    # A play-test, or a CAPTIONS entry: no typed commands to split on.
    words = plays.get(card, [])
    if words and not any(names_it(prog, w) or w == prog for w in words):
        return "not-run", "on the `%s' play-test" % card
    lines = [l for l in panel["s"].split("\n") if l.strip()]
    usage, err, work = score(lines)
    bad = next((l for l in lines if audit_cards.ERROR.search(l)), "")
    if err:
        return "play-error", bad.strip()[:44]
    return "play", ""


def runnable():
    """Every type-$01 module the catalogue lists, with its directory."""
    progs, _, _ = gen_catalog.gather(os.path.join(REPO, "disk"),
                                     os.path.join(TOOLS, "categories.psv"))
    out = []
    for p in progs:
        rel = os.path.join(p.get("dir", ""), p["name"])
        if worklist.modtype(os.path.join(REPO, "disk"), rel) == "prog":
            out.append(p["name"])
    return sorted(out)


def audit():
    """[(program, verdict, note)] for every runnable program."""
    scr, cards, plays = screens(), stanzas(), played()
    return [(p,) + verdict_for(p, scr.get(p), cards, plays)
            for p in runnable()]


def read_list(path, split=False):
    out = {}
    if not os.path.exists(path):
        return out
    for raw in open(path):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        name, _, reason = line.partition("|")
        out[name.strip()] = reason.strip()
    return out


def gate():
    """The ratchet.  Returns (ok, [complaints])."""
    backlog, excepted = read_list(BACKLOG), read_list(EXCEPTIONS)
    known = set(runnable())
    bad = []
    for name in sorted(set(backlog) | set(excepted)):
        if name not in known:
            bad.append("`%s' is listed but is not a runnable program" % name)
    for name in sorted(set(backlog) & set(excepted)):
        bad.append("`%s' is on the backlog AND excepted -- pick one" % name)
    for prog, v, note in audit():
        failing = v in FAILING
        if failing and prog not in backlog and prog not in excepted:
            bad.append("`%s' panel is %s (%s) and is not on the backlog"
                       % (prog, v, note))
        if not failing and prog in backlog:
            bad.append("`%s' now passes (%s) -- take it off the backlog"
                       % (prog, v))
    return not bad, bad


def main(argv):
    if "--show" in argv:
        name = argv[argv.index("--show") + 1]
        panel = screens().get(name)
        if not panel:
            sys.exit("no panel published for %s" % name)
        print("card: %s\n%s\n-- %s" % (panel["n"], panel["s"], panel["c"]))
        return 0
    if "--gate" in argv:
        ok, bad = gate()
        for b in bad:
            print("  %s" % b)
        print("%s: %d problem(s)" % ("ok" if ok else "FAILED", len(bad)))
        return 0 if ok else 1
    rows = audit()
    hist = {}
    for _, v, _ in rows:
        hist[v] = hist.get(v, 0) + 1
    if "--summary" not in argv:
        excepted = read_list(EXCEPTIONS)
        show = rows if "--all" in argv else [r for r in rows if r[1] in FAILING]
        for prog, v, note in sorted(show, key=lambda r: (ORDER[r[1]], r[0])):
            tag = " (excepted: %s)" % excepted[prog] if prog in excepted else ""
            print("%-18s %-13s %s%s" % (prog, v, note, tag))
        print()
    for v in sorted(hist, key=ORDER.get):
        print("%-14s %4d" % (v, hist[v]))
    failing = sum(n for v, n in hist.items() if v in FAILING)
    print("%d of %d runnable programs have a panel that shows them working"
          % (len(rows) - failing, len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
