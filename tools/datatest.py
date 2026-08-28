#!/usr/bin/env python3
"""PROVE a program did its job, by checking the DATA it produced.

    tools/datatest.py <family.cases> [<family.cases> ...] [--image <dd>]
    tools/datatest.py --all

Why this exists
---------------
`tools/verify_all.sh' asks "did it print anything" and `tools/playtest.py'
asks "what did the screen look like". Neither is the right question for the
390 programs on this disk that take data in and put data out. A netpbm
converter that writes a corrupt image prints nothing at all and passes both.

So this asks the only question that settles it: **run the program, then
measure what it wrote.** Dimensions, pixel values, byte-identity after a
round trip, counts. A machine can check those and a person can trust them.

It is also the only harness here that scales. `playtest.py' starts one
emulator per program and takes minutes each; this one puts a whole family
into a SINGLE bash procedure file, starts the emulator ONCE, and splits the
output on markers afterwards. 169 netpbm programs is minutes, not hours.

Case-file format (one directive per line, # comments ignored)
------------------------------------------------------------
    family  netpbm              what to call this set
    setup   P=/dd/CMDS/NETPBM   shell lines run once, before any case
    load    /dd/CMDS/os9lib     module to `load' before anything runs

    case    pnmcut-crops        start a case; everything after is part of it
    run     $P/pnmcut 0 0 16 4 /dd/tmp/s.pgm > /dd/tmp/c.pgm
    run     $P/pnmfile /dd/tmp/c.pgm
    expect  16 by 4             text that MUST appear in this case's output
    absent  Bad                 text that must NOT appear
    exact   <file>              this case's output must equal the file's bytes

A case passes when every `expect' appeared, no `absent' did, and the emulator
reported no exception against it.

THE TRAPS THIS ALREADY KNOWS ABOUT
----------------------------------
  - **A case that produces NO output is a failure, not a pass.** An empty
    capture matching zero `expect' lines vacuously is the exact shape of
    every false pass this collection has produced. A case must assert
    something; a case file with a bare `run' and no expectation is rejected
    when it is parsed, not silently counted as green.
  - **`grep -a' everywhere, LC_ALL=C everywhere.** OS-9 programs emit bytes
    above 127 freely and the capture pipeline used to abort on the first one,
    classifying the program on nothing at all.
  - **The marker has to survive being written next to binary.** Cases here
    redirect image data to files, but a program that writes junk to the
    terminal can run into the next marker. Markers are matched at line start
    and a case's output is everything up to the NEXT marker, so a run-on
    costs that case and not the whole family.
"""
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OS9EXEC = os.environ.get("OS9EXEC", os.path.join(REPO, "..", "os9exec", "os9exec"))
# Microware's `load', TESTING ONLY -- it is never committed into disk/.
# The trap-free build: the ordinary one stops with `csl traphandler mismatch'
# against the edition-16 csl this collection ships.
SDK_LOAD = os.environ.get(
    "OS9LOAD", os.path.expanduser("~/Developer/os9/play/oskBoot/CMDS/NOCSL/load"))
MARK = "@@CASE@@"


class Case:
    def __init__(self, name):
        self.name = name
        self.runs = []
        self.expect = []
        self.absent = []

    def asserts(self):
        return len(self.expect) + len(self.absent)


def parse(path):
    fam = {"family": os.path.basename(path).replace(".cases", ""),
           "setup": [], "load": [], "cases": []}
    cur = None
    for lineno, raw in enumerate(open(path), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        word, _, rest = line.partition(" ")
        rest = rest.strip()
        if word == "family":
            fam["family"] = rest
        elif word in ("setup", "load"):
            fam[word].append(rest)
        elif word == "case":
            cur = Case(rest)
            fam["cases"].append(cur)
        elif word in ("run", "expect", "absent"):
            if cur is None:
                sys.exit("%s:%d: `%s' before any `case'" % (path, lineno, word))
            (cur.runs if word == "run" else
             cur.expect if word == "expect" else cur.absent).append(rest)
        else:
            sys.exit("%s:%d: unknown directive `%s'" % (path, lineno, word))
    # A CASE THAT ASSERTS NOTHING CANNOT FAIL, so it is not a test. Rejected
    # at parse time rather than counted green -- this is the single most
    # common way a sweep on this collection has lied.
    for c in fam["cases"]:
        if not c.runs:
            sys.exit("%s: case `%s' has no `run'" % (path, c.name))
        if not c.asserts():
            sys.exit("%s: case `%s' asserts nothing -- add an `expect' or "
                     "`absent'" % (path, c.name))
    if not fam["cases"]:
        sys.exit("%s: no cases" % path)
    return fam


def script_for(fam):
    """One bash procedure file for the whole family: ONE emulator start."""
    lines = []
    for mod in fam["load"]:
        lines.append("/h4/load %s" % mod)
    lines += fam["setup"]
    for c in fam["cases"]:
        lines.append('echo "%s%s"' % (MARK, c.name))
        lines += c.runs
    lines.append('echo "%send"' % MARK)
    return "\r".join(lines) + "\r"


def split_output(text, fam):
    """Everything between a case's marker and the next one belongs to it."""
    out = {}
    cur = None
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith(MARK):
            cur = stripped[len(MARK):]
            out[cur] = []
            continue
        if cur is not None:
            out[cur].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def run_family(path, image, workdir):
    fam = parse(path)
    os.makedirs(os.path.join(workdir, "h1"), exist_ok=True)
    sh = os.path.join(workdir, "h1", "%s.sh" % fam["family"])
    open(sh, "w", newline="").write(script_for(fam))

    h4 = os.path.join(workdir, "h4")
    os.makedirs(h4, exist_ok=True)
    dst = os.path.join(h4, "load")
    if fam["load"] and not os.path.exists(dst):
        if not os.path.exists(SDK_LOAD):
            sys.exit("this family needs `load' and none is at %s "
                     "(set OS9LOAD)" % SDK_LOAD)
        import shutil
        shutil.copy2(SDK_LOAD, dst)

    env = dict(os.environ, LC_ALL="C", OS9DISK=image,
               OS9H1=os.path.join(workdir, "h1"), OS9H4=h4)
    proc = subprocess.run(
        ["gtimeout", "300", OS9EXEC, "-r", "bash", "/h1/%s.sh" % fam["family"]],
        env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    text = proc.stdout.decode("latin-1")
    open(os.path.join(workdir, "%s.raw" % fam["family"]), "w").write(text)

    per = split_output(text, fam)
    results = []
    for c in fam["cases"]:
        got = per.get(c.name)
        if got is None:
            results.append((c.name, "FAIL", "never ran (marker not reached)"))
            continue
        missing = [e for e in c.expect if e not in got]
        found = [a for a in c.absent if a in got]
        # An exception against this case is a failure however clean the text.
        blew = re.search(r"vector=\$[0-9A-Fa-f]+", got)
        if missing:
            results.append((c.name, "FAIL", "missing %r" % missing[0]))
        elif found:
            results.append((c.name, "FAIL", "found %r" % found[0]))
        elif blew:
            results.append((c.name, "FAIL", blew.group(0)))
        else:
            results.append((c.name, "PASS", ""))
    return fam["family"], results


def main(argv):
    image = os.path.join(REPO, "osk-freeware.dd")
    workdir = os.environ.get("DATATEST_WORK",
                             os.path.join(REPO, "notes", "datatests"))
    files, i = [], 0
    while i < len(argv):
        if argv[i] == "--image":
            i += 1
            image = argv[i]
        elif argv[i] == "--all":
            d = os.path.join(REPO, "tools", "datatests")
            files += sorted(os.path.join(d, f) for f in os.listdir(d)
                            if f.endswith(".cases"))
        else:
            files.append(argv[i])
        i += 1
    if not files:
        sys.exit(__doc__)
    if not os.path.exists(image):
        sys.exit("no image at %s -- run tools/mkimage.sh first" % image)
    os.makedirs(workdir, exist_ok=True)

    bad = total = 0
    for f in files:
        family, results = run_family(f, image, workdir)
        for name, verdict, why in results:
            total += 1
            if verdict != "PASS":
                bad += 1
            print("%-12s %-26s %-5s %s" % (family, name, verdict, why))
    print("\n%d of %d cases passed" % (total - bad, total))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
