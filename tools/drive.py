#!/usr/bin/env python3
r"""RUN programs with real arguments and keep everything they said.

    tools/drive.py tools/drives/<sheet>.drive [...] [--image osk-freeware.dd]
    tools/drive.py <sheet> --lines 12        # first 12 lines of each program
    tools/drive.py <sheet> --quiet           # transcript to the file only

Why this exists beside the other three harnesses
------------------------------------------------
`verify_all.sh' asks "did it print anything".  `screenshots.py' takes a
picture.  `datatest.py' asserts a fact you already know.  None of them is the
thing rdoggett asked for on 2026-08-31: **run the program the way its own
usage line says, with real arguments, and look at what came back** -- which
is how you find out that `hc' is a text filter and not a hex calculator.

Doing that by hand costs an emulator start per program and reads one program
at a time.  This runs a whole sheet -- forty programs, a hundred command
lines -- in ONE emulator session and writes a transcript with each program's
output under its own heading, so a batch can be read in one pass and the
findings written up together.

It ASSERTS NOTHING and it JUDGES NOTHING.  When a run settles a question, the
answer belongs in a `tools/datatests/*.cases' case, which can fail again; a
transcript cannot.  Think of this as the step before that one.

Sheet format (one directive per line, `#' comments at line start only)
---------------------------------------------------------------------
    family  textfilters              what to call the transcript
    setup   T=/dd/SYS/termcap         shell lines run once, before anything
    load    /dd/CMDS/os9lib           module to `load' first

    drive   hc                        start a program's stanza
    why     is it a hex calculator?   a note carried into the transcript
    run     /dd/CMDS/hc +8 /dd/SYS/motd

Every stanza runs under the environment `SYS/login' sets, because that is
what a person arrives with: TERM, TERMCAP, PATH over every command
directory, USER, MAIL, PEP.  74 programs read TERMCAP and several stop dead
without USER, and a harness that leaves them unset measures its own
omission.  The preamble is READ OUT OF `disk/SYS/login' rather than copied
here, so it cannot drift from what ships.

Traps this already knows about
------------------------------
  * **A program that takes the session down takes every stanza after it.**
    The run restarts from where the output stopped, exactly as `datatest.py'
    does, so one fatal program costs one stanza and not the rest of the sheet.
  * `grep -a' and Latin-1 throughout: these programs emit bytes above 127
    freely and a decode error would classify a program on nothing at all.
  * A stanza that produced NOTHING is reported as `(silent)' rather than
    quietly leaving a blank -- silence is a finding, not an absence of one.
"""
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from os9env import emulator_env, stage_reader_load
import imagelock                                    # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OS9EXEC = os.environ.get("OS9EXEC", os.path.join(REPO, "..", "os9exec",
                                                 "os9exec"))
SHEETS = os.path.join(REPO, "tools", "drives")
OUT = os.path.join(REPO, "notes", "drives")
MARK = "@@DRIVE@@"
# See the same constant in datatest.py: a storming program must not cost
# 200 MB of transcript.
CAP = 4 << 20


def login_preamble():
    """`SYS/login' minus the parts that would end the run.

    Its `exec bash -i' would replace our procedure file with an interactive
    shell and its two `echo' lines would land in the first stanza's output.
    Everything else -- the whole environment -- is what a person has when
    they run one of these programs, so it is taken from the shipped file
    rather than restated here.
    """
    path = os.path.join(REPO, "disk", "SYS", "login")
    text = open(path, "rb").read().decode("latin-1").replace("\r", "\n")
    keep = [ln for ln in text.split("\n")
            if not ln.startswith("exec ") and not ln.startswith("echo ")]
    return keep


class Stanza:
    def __init__(self, name):
        self.name = name
        self.why = []
        self.runs = []


def parse(path):
    fam = {"family": os.path.basename(path).replace(".drive", ""),
           "setup": [], "load": [], "stanzas": []}
    cur = None
    for lineno, raw in enumerate(open(path), 1):
        # A `#' comments only at the START of a line -- stripping it anywhere
        # would eat the argument off `run echo "#!/bin/sh" > /dd/tmp/x'.
        line = "" if raw.lstrip().startswith("#") else raw.rstrip("\n").strip()
        if not line:
            continue
        word, _, rest = line.partition(" ")
        rest = rest.strip()
        if word == "family":
            fam["family"] = rest
        elif word in ("setup", "load"):
            fam[word].append(rest)
        elif word == "drive":
            cur = Stanza(rest)
            fam["stanzas"].append(cur)
        elif word in ("run", "why"):
            if cur is None:
                sys.exit("%s:%d: `%s' before any `drive'" % (path, lineno, word))
            (cur.runs if word == "run" else cur.why).append(rest)
        else:
            sys.exit("%s:%d: unknown directive `%s'" % (path, lineno, word))
    for s in fam["stanzas"]:
        if not s.runs:
            sys.exit("%s: `%s' has no `run'" % (path, s.name))
    if not fam["stanzas"]:
        sys.exit("%s: no stanzas" % path)
    return fam


def script_for(fam, stanzas):
    lines = login_preamble()
    lines += ["/h1/CMDS/load %s" % m for m in fam["load"]]
    lines += fam["setup"]
    for s in stanzas:
        # A BLANK LINE BEFORE EVERY MARKER, and it is not cosmetic. Markers
        # are matched at line start, and a program that ends its output
        # WITHOUT a final CR -- `date -t' is one -- leaves the next marker
        # sitting mid-line where the split cannot see it. The stanza then
        # reads as never run, the harness restarts to catch it, and it
        # happens again: three restarts on the first sheet driven this way.
        lines.append('echo ""')
        lines.append('echo "%s%s"' % (MARK, s.name))
        lines += s.runs
    lines.append('echo ""')
    lines.append('echo "%send"' % MARK)
    return "\r".join(lines) + "\r"


def split_output(text):
    out, cur = {}, None
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith(MARK):
            cur = stripped[len(MARK):]
            out[cur] = []
            continue
        if cur is not None:
            out[cur].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


NOISE = re.compile(r"^(os9\$ ?)+")


def tidy(text):
    """Drop the shell's prompt echo and trailing blank lines; keep the rest."""
    lines = []
    for ln in text.replace("\r", "\n").split("\n"):
        ln = NOISE.sub("", ln.replace("\000", "")).rstrip()
        lines.append(ln)
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def run_sheet(path, image, seconds):
    fam = parse(path)
    work = os.path.join(OUT, "work")
    os.makedirs(os.path.join(work, "h1"), exist_ok=True)
    sh = os.path.join(work, "h1", "%s.sh" % fam["family"])
    stage_reader_load(os.path.join(work, "h1"))
    # emulator_env, not dict(os.environ): see tools/os9env.py.  A harness
    # names the devices it wants and inherits none.
    env = emulator_env(LC_ALL="C", OS9DISK=image, OS9H0=image,
                       OS9H1=os.path.join(work, "h1"))

    per, todo, raw = {}, list(fam["stanzas"]), ""
    # STRAIGHT TO A FILE, not to a pipe read at the end. A stanza that hangs
    # costs the whole timeout, and with the output buffered there is no way to
    # see WHICH one is hanging until the run gives up -- so the transcript is
    # written as it happens and `tail -f' works on it.
    live = os.path.join(work, "%s.raw" % fam["family"])
    open(live, "wb").close()
    seen = 0
    for _attempt in range(len(fam["stanzas"]) + 1):
        open(sh, "w", newline="").write(script_for(fam, todo))
        with open(live, "ab") as fh:
            # CAPPED. A program caught in the cio storm writes `No more
            # memory !!!' without bound -- one datatest case of `cvtbase'
            # produced a 207 MB capture on 2026-08-31 before this was here.
            # Nothing downstream reads past the first few megabytes.
            proc = subprocess.Popen(
                ["gtimeout", str(seconds), OS9EXEC, "-r", "bash",
                 "/h1/%s.sh" % fam["family"]],
                env=env, stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            total = 0
            while True:
                blk = proc.stdout.read(65536)
                if not blk:
                    break
                fh.write(blk)
                total += len(blk)
                if total >= CAP:
                    fh.write(b"\n@@CAPPED@@ output passed %d bytes\n" % CAP)
                    proc.terminate()
                    try:
                        proc.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        proc.kill()
                    break
            proc.stdout.close()
            proc.wait()
        with open(live, "rb") as fh:
            fh.seek(seen)
            chunk = fh.read().decode("latin-1")
            seen = fh.tell()
        raw += chunk
        got = split_output(chunk)
        for k, v in got.items():
            per.setdefault(k, v)
        if not [s for s in todo if s.name in got]:
            per.setdefault(todo[0].name, "")       # the first one killed it
        todo = [s for s in todo if s.name not in per]
        if not todo:
            break
        print("   %s: restarting -- the session did not survive `%s'"
              % (fam["family"], todo[0].name), file=sys.stderr)
    return fam, per, raw


def main(argv):
    image = os.path.join(REPO, "osk-freeware.dd")
    seconds, limit, quiet = 300, 0, False
    files, i = [], 0
    while i < len(argv):
        a = argv[i]
        if a == "--image":
            i += 1
            image = argv[i]
        elif a == "--lines":
            i += 1
            limit = int(argv[i])
        elif a == "--seconds":
            i += 1
            seconds = int(argv[i])
        elif a == "--quiet":
            quiet = True
        else:
            files.append(a if os.path.exists(a)
                         else os.path.join(SHEETS, a + ".drive"))
        i += 1
    if not files:
        sys.exit(__doc__)
    if not os.path.exists(image):
        sys.exit("no image at %s -- run tools/mkimage.sh first" % image)
    os.makedirs(OUT, exist_ok=True)

# AN OS9Hx DEVICE PATH MUST BE ABSOLUTE.  Measured 2026-09-01: with
# `--image osk-freeware.dd' -- a bare relative name, which is what
# `datatest.py --all' was documented to take -- os9exec mounts the device
# and MODULE LOADING WORKS, while ordinary file opens on it silently fail.
# The whole WN web-server family went from 200 to 404 on that difference and
# nothing said why: `wn' itself loaded and ran, and only the file it wanted
# to serve could not be opened.  os9exec's own note about a leading `./'
# breaking every ordinary open is the same shape.  So the path is made
# absolute here rather than trusting the caller to type one.
    image = os.path.abspath(image)

    with imagelock.held(image, "drive"):
        for f in files:
            fam, per, raw = run_sheet(f, image, seconds)
            dest = os.path.join(OUT, "%s.txt" % fam["family"])
            report = []
            for s in fam["stanzas"]:
                report.append("=" * 68)
                report.append("== %s" % s.name)
                for w in s.why:
                    report.append("== ? %s" % w)
                for r in s.runs:
                    report.append("== $ %s" % r)
                report.append("=" * 68)
                body = tidy(per.get(s.name, ""))
                report += body if body else ["(silent)"]
                report.append("")
            open(dest, "w").write("\n".join(report) + "\n")
            open(os.path.join(OUT, "work", "%s.raw" % fam["family"]),
                 "w").write(raw)
            if not quiet:
                for s in fam["stanzas"]:
                    print("=" * 68)
                    print("== %s" % s.name)
                    for w in s.why:
                        print("== ? %s" % w)
                    for r in s.runs:
                        print("== $ %s" % r)
                    body = tidy(per.get(s.name, "")) or ["(silent)"]
                    if limit and len(body) > limit:
                        body = body[:limit] + ["... (%d more lines, see %s)"
                                               % (len(body) - limit, dest)]
                    print("\n".join(body))
                    print()
            print("# %s: %d stanzas -> %s"
                  % (fam["family"], len(fam["stanzas"]), dest),
                  file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
