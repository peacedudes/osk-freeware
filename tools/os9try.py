#!/usr/bin/env python3
r"""Run a card's command at MICROWARE'S SHELL and show what came back.

    tools/os9try.py tools/screenshots/texttools.sheet --only gothic,grep
    tools/os9try.py -c "gothic OS-9" [--chd /dd/tmp/X] [--load /dd/CMDS/os9lib]
    tools/os9try.py -c "cvtbase d h" --stdin "255"

Every card carries a `try' line -- the command at bash or ksh -- and, where
the same thing is spelt differently at Microware's shell, an `os9' line.
This is how an `os9' line is VERIFIED before it is written down: the
collection is mounted as /dd (and /h0), the reader's own OS-9 -- here the
SDK, from OS9SDK -- as /h1, and Microware's shell is booted on a CR-only
procedure file that sets the login environment, moves to the stanza's
directory, loads what the stanza loads, and runs the command.  Lines after
the command are the program's standard input.

What it takes from a stanza: every hidden `builtin cd X' / `cd X' becomes
`chd X'; every `load X' is kept; `export' lines are dropped (the login
environment is set here); anything else typed before the picture -- an
`echo' that stages a file, a `mkdir', a `cp' -- is NOT re-run.  Those ran
under bash when the sheet was shot, and the image keeps their results, so
shoot the sheet first.  Then the `os9' line, or the `try' line where there
is none, and `send' lines as standard input.

One emulator per stanza, so a program that prompts and eats the rest of the
file eats nothing that matters.  The image is not written to any more than
the program itself writes; take the lock all the same, because the harnesses
do.

Exit status is the number of stanzas whose command the shell could not run
(`can't execute', an `Error #' from the shell itself); what a program says
for itself is printed and left to the reader.
"""
import os
import re
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
from os9env import emulator_env
import imagelock                                        # noqa: E402
import screenshots                                      # noqa: E402

OS9EXEC = screenshots.OS9EXEC
SDK = os.environ.get("OS9SDK",
                     os.path.join(os.path.expanduser("~"),
                                  "Developer", "os9", "play", "oskBoot"))

# The same environment SYS/login gives a bash session, spelt for Microware's
# shell.  SHELL is Microware's own: a program that shells out forks $SHELL
# with the whole command line as one argument, which is exactly how that
# shell is invoked.
ENV = (
    "setenv HOME /dd",
    "setenv TERM xterm-256color",
    "setenv TERMCAP /dd/SYS/termcap",
    "setenv USER tester",
    "setenv LOGNAME tester",
    "setenv MAIL /dd/SPOOL/MAIL/tester",
    "setenv PATH /dd/CMDS:/dd/CMDS/GAMES:/dd/CMDS/NETPBM:/dd/CMDS/UUCP:"
    "/dd/CMDS/TEXCMDS:/dd/CMDS/ELM:/dd/CMDS/COMMS:/dd/CMDS/NETWORK:"
    "/dd/CMDS/NEWS:/dd/CMDS/WN:/dd/CMDS/ADL:/dd/CMDS/REBUILT:/dd/CMDS/DEMOS:"
    "/dd/CMDS/DHRY:/dd/CMDS/GCC139:/h1/CMDS:/h1/CMDS/GAMES",
    "setenv TMACDIR /dd/LIB",
    "setenv HELPDIR /dd/SYS/HELP",
    "setenv SIMPATH /dd/SBPROLOG/MODLIB",
    "setenv PEP /dd/SYS/PEP",
    "setenv SHELL /h1/CMDS/shell",
    "chx /dd/CMDS",
    "chd /dd",
)

SHELL_ERROR = re.compile(r"can't execute|^Error #|^shell:", re.M)


def setup_from(shot):
    """The chd and load lines a stanza's hidden setup amounts to."""
    lines, stdin = [], []
    for kind, what in shot["acts"]:
        if kind == "run":
            cmd = what.strip()
            m = re.match(r"^(?:builtin\s+)?cd\s+(\S+)", cmd)
            if m:
                lines.append("chd " + m.group(1))
            elif cmd.startswith("load "):
                lines.append(cmd)
        elif kind == "send":
            # Keys meant for the program: each `\r'-ended piece is a line
            # of standard input.  Control characters are not typeable here.
            for piece in what.split("\r"):
                if piece and not any(ord(c) < 32 for c in piece):
                    stdin.append(piece)
    return lines, stdin


def run(image, command, chd=None, loads=(), stdin=(), timeout=60):
    """Boot Microware's shell on a procedure file and return the text."""
    scratch = tempfile.mkdtemp(prefix="os9try.")
    proc = ["-nx"] + list(ENV)
    if chd:
        proc.append("chd " + chd)
    proc += list(loads)
    proc.append(command)
    proc += list(stdin)
    with open(os.path.join(scratch, "p.proc"), "wb") as f:
        f.write(("\r".join(proc) + "\r").encode("latin-1", "replace"))
    # emulator_env, not dict(os.environ): see tools/os9env.py.
    env = emulator_env(OS9DISK=image, OS9H0=image, OS9H1=SDK,
                       OS9H5=scratch)
    try:
        out = subprocess.run([OS9EXEC, "-r", "/h1/CMDS/shell", "/h5/p.proc"],
                             stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, env=env,
                             timeout=timeout)
        text = out.stdout
    except subprocess.TimeoutExpired as e:
        text = (e.stdout or b"") + b"\n[os9try: no answer in %ds]" % timeout
    text = text.decode("latin-1").replace("\r\n", "\n").replace("\r", "\n")
    text = "\n".join(ln for ln in text.split("\n")
                     if not ln.startswith("# /h0: using OS9H0"))
    return text.strip("\n")


def main(argv):
    if not argv or "-h" in argv:
        sys.exit(__doc__)
    image = os.path.join(REPO, "osk-freeware.dd")
    if "--image" in argv:
        image = argv[argv.index("--image") + 1]
    image = os.path.abspath(image)
    if not os.path.isdir(os.path.join(SDK, "CMDS")):
        sys.exit("no OS-9 system at %s -- set OS9SDK" % SDK)
    if "-c" in argv:
        cmd = argv[argv.index("-c") + 1]
        chd = argv[argv.index("--chd") + 1] if "--chd" in argv else None
        loads = ["load " + argv[argv.index("--load") + 1]] if "--load" in argv else []
        stdin = argv[argv.index("--stdin") + 1].split("\\r") if "--stdin" in argv else []
        with imagelock.held(image, "os9try"):
            print(run(image, cmd, chd, loads, stdin))
        return 0
    only = set(argv[argv.index("--only") + 1].split(",")) if "--only" in argv else None
    failed = 0
    with imagelock.held(image, "os9try"):
        for sheet in [a for a in argv if a.endswith(".sheet")]:
            for shot in screenshots.parse(sheet):
                if only and shot["name"] not in only:
                    continue
                cmd = shot.get("os9") or shot.get("try")
                label = "os9" if shot.get("os9") else "try"
                if not cmd:
                    # No try line yet: the command the picture was made
                    # with, which is the first visible run after the last
                    # clear -- so the verifier is useful while a card is
                    # still being written.
                    runs = [w for k, w in shot["acts"] if k == "run"]
                    while "clear" in runs:
                        runs = runs[runs.index("clear") + 1:]
                    cmd = next((r for r in runs
                                if not re.match(r"^(builtin\s+)?cd\s|^load\s|^export\s", r)), None)
                    label = "run"
                if not cmd:
                    print("== %s: nothing to run" % shot["name"])
                    continue
                setup, stdin = setup_from(shot)
                chds = [s for s in setup if s.startswith("chd ")]
                loads = [s for s in setup if s.startswith("load ")]
                chd = chds[-1][4:] if chds else None
                print("== %s  (%s: %s)%s" % (shot["name"], label, cmd,
                                             "  in " + chd if chd else ""))
                text = run(image, cmd, chd, loads, stdin)
                print(text)
                if SHELL_ERROR.search(text):
                    failed += 1
                    print("   ^^ the SHELL could not run that")
                print()
    return failed


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
