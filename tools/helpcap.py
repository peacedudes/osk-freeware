#!/usr/bin/env python3
r"""Capture each program's OWN help text, complete, the way it prints it.

    tools/helpcap.py                          # every entry in tools/help.psv
    tools/helpcap.py --only roff,bm           # just those
    tools/helpcap.py --probe [--out DIR]      # ask `-?' of every program NOT
                                              # yet in the table, into DIR,
                                              # to decide what to write there
    tools/helpcap.py --backlog                # rewrite tools/help-backlog.txt
    tools/helpcap.py --disk disk              # regenerate disk/DOC/USAGE
    tools/helpcap.py --disk disk --check      # is it current?  exit 1 if not

Why this exists
---------------
The card's "its own help" used to be lifted out of the binary by a regex
(`usage_of' in gen_catalog.py, retired 2026-09-09).  A regex over strings
stops where the strings stop looking like options, so `roff' was published
as three lines ending at `Options:' with the options cut off, and the
program's real `-?' output appeared nowhere on its card.  A scrape is
uniform and individually wrong.  This runs the program and keeps what it
said, whole.

tools/help.psv is the table this reads, ONE LINE PER PROGRAM, written by
somebody who has just run the thing:

    <name>|<command>|<note>

    roff|roff -?|
    cookie|none|it takes no options; run it and it prints a saying
    lnk.org|load /dd/CMDS/os9lib; lnk.org -?|
    cvtbase|cvtbase -? << 255|

The command is what a reader types at the shell to get the help -- `-?' is
the OS-9 convention and is not universal: some want `-h', `--help', `help',
a bare run, and games, editors and screen programs mostly have none.  A
leading `load X;', `chd X;' or `chx X;' is hidden setup (the same as a sheet's).  `<<'
gives standard-input lines, `\r'-separated, for a program that asks before
it answers.  `none' says the program has no help of its own; the note says
what the card should say instead, and nothing is captured.

The capture goes to docs/help/<name>.txt, first line `$ <command>', then
the program's words, LF-terminated and ASCII.  gen_catalog.py reads those
files; the card shows the command and the text under "its own help".

Every capture runs at Microware's shell through tools/os9try.py's machinery
-- one emulator per program, the login environment set, the collection on
/dd and /h0 and the reader's OS-9 (the SDK) on /h1 -- because that is the
shell a `help' line is spelt for and it is what verifies the `os9' lines
too.  It needs OS9SDK to point at an OS-9 system with a CMDS/shell.

A program that hangs on its flag leaves `[no answer in Ns]' in the file
and the gate (`cards carry real help text') fails on it: the table entry
is wrong, not the program.  So does a file whose last line ends in `:',
which is what a cut-off option list looks like -- the roff scrape, made
into a rule.
"""
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import imagelock                                        # noqa: E402
import os9try                                           # noqa: E402

TABLE = os.path.join(REPO, "tools", "help.psv")
BACKLOG = os.path.join(REPO, "tools", "help-backlog.txt")
HELPDIR = os.path.join(REPO, "docs", "help")
TIMEOUT = 20
NO_ANSWER = "[no answer in "

# Programs never to probe blind: each one damages the disk or the session
# in a way a `-?' does not necessarily avoid.  flink aliases a file's FD in
# the current directory, corrupting it; dedit writes raw sectors; disktest
# measures the disk it is run on and ends the session.
NEVER_PROBE = {"flink", "dedit", "disktest"}

ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z=]|\x1b[()][A-Za-z0-9]|\x1b[A-Za-z=>]")


def load_table(path=TABLE):
    """name -> (command, note); `command' is None for a `none' entry."""
    table = {}
    if not os.path.exists(path):
        return table
    for raw in open(path, encoding="ascii"):
        line = raw.rstrip("\n")
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("|")
        if len(parts) < 2:
            sys.exit("%s: not name|command|note: %s" % (path, line))
        name, cmd = parts[0].strip(), parts[1].strip()
        note = parts[2].strip() if len(parts) > 2 else ""
        table[name] = (None if cmd == "none" else cmd, note)
    return table


def split_command(cmd):
    """(setup lines, the command, stdin lines) from a table command."""
    stdin = []
    if "<<" in cmd:
        cmd, _, fed = cmd.partition("<<")
        stdin = [s for s in fed.strip().split("\\r") if s]
    parts = [p.strip() for p in cmd.split(";")]
    setup, command = parts[:-1], parts[-1]
    for s in setup:
        # `setenv NAME VALUE' too: robots, shuffle and gnuchess answer
        # `Unknown terminal type' until TERM and TERMCAP are set (2026-09-26).
        if not re.match(r"^(load|chd|chx)\s+\S|^setenv\s+\S+\s+\S", s):
            sys.exit("only `load X', `chd X', `chx X' or `setenv N V' may precede the command: %s" % cmd)
    return setup, command, stdin


def clean(text):
    """The program's words: no escapes, no NULs, ASCII, no trailing blanks."""
    text = ANSI.sub("", text).replace("\x00", "")
    text = "".join(ch if 32 <= ord(ch) < 127 or ch in "\n\t" else "?" for ch in text)
    lines = [ln.rstrip() for ln in text.split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    # A program that prints its usage and exits non-zero makes the shell
    # (run -x) report the status -- `Error #000:002 (S_Abort) ...' -- after
    # the program's own words.  That line is the shell's, not the help; it
    # goes, unless it is all there is, in which case it is the answer.
    while len(lines) > 1 and re.match(r"^Error #\d{3}:\d{3}", lines[-1]):
        lines.pop()
        while lines and not lines[-1]:
            lines.pop()
    while lines and not lines[0]:
        lines.pop(0)
    return "\n".join(lines)


def capture(image, cmd, timeout=TIMEOUT):
    """Run one table command at Microware's shell; the cleaned text."""
    setup, command, stdin = split_command(cmd)
    chds = [s[4:] for s in setup if s.startswith("chd ")]
    # `load' and `chx' lines go into the procedure file as they are; a
    # chx is how a program off the command path -- the GCC drivers in
    # their own directory -- is asked by its bare name.
    loads = [s for s in setup if s.startswith(("load ", "chx "))]
    text = os9try.run(image, command, chds[-1] if chds else None, loads,
                      stdin, timeout=timeout)
    text = text.replace("[os9try: no answer", NO_ANSWER.rstrip())
    return clean(text)


def programs(root):
    """Every program file the catalogue can see, name -> directory."""
    import gen_catalog
    names = {}
    for d in gen_catalog.PROGRAM_DIRS:
        full = os.path.join(root, d)
        if not os.path.isdir(full):
            continue
        for f in sorted(os.listdir(full)):
            if os.path.isfile(os.path.join(full, f)):
                names.setdefault(f, d)
    return names


def write_capture(name, cmd, text, outdir=HELPDIR):
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, name + ".txt"), "w", encoding="ascii") as f:
        f.write("$ %s\n%s\n" % (cmd, text))


def rewrite_backlog(root, table, path=BACKLOG):
    """The programs not yet in the table -- rebuilt wholesale, never edited
    by hand, so concurrent batches cannot race on it."""
    names = sorted(n for n in programs(root) if n not in table)
    with open(path, "w") as f:
        f.write("# help-backlog.txt -- programs with no line in tools/help.psv yet.\n"
                "# Generated by `tools/helpcap.py --backlog'; visiting a program\n"
                "# means writing its help.psv line, then regenerating this.\n")
        f.write("".join(n + "\n" for n in names))
    return len(names)


def render_disk_usage(root, table, check=False):
    """DOC/USAGE: what every program says when asked for help, CR-only."""
    dirs = programs(root)
    out = ["USAGE -- what each program says when asked for its help",
           "=" * 58, "",
           "Every line below came out of the program named above it, run at",
           "the shell with the command shown.  `-?' is the OS-9 convention",
           "and is not universal; where a program wants another flag, that",
           "is the one shown.  A program listed with no command prints no",
           "help of its own, and the line after its name says what to do",
           "instead.  Nothing here was composed.", ""]
    for name in sorted(table, key=str.lower):
        if name not in dirs:
            continue
        cmd, note = table[name]
        out.append("  %s   (%s)" % (name, dirs[name]))
        if cmd is None:
            out.append("      no help of its own" + (" -- " + note if note else ""))
        else:
            path = os.path.join(HELPDIR, name + ".txt")
            if not os.path.exists(path):
                continue
            body = open(path, encoding="ascii").read().split("\n", 1)
            out.append("      $ " + cmd)
            out += ["      " + ln if ln else "" for ln in body[1].rstrip("\n").split("\n")]
        out.append("")
    data = ("\r".join(out) + "\r").encode("ascii")
    path = os.path.join(root, "DOC", "USAGE")
    if check:
        # A GENERATED FILE WITH NO FRESHNESS GATE GOES STALE QUIETLY.  This
        # one was 267 lines behind on 2026-09-19 and nothing said so, where
        # DOC/DEPENDS and DOC/MANPAGES have had such a check for weeks.
        try:
            return data == open(path, "rb").read()
        except OSError:
            return False
    with open(path, "wb") as f:
        f.write(data)
    return len(out)


def main(argv):
    if "-h" in argv or "--help" in argv:
        sys.exit(__doc__)
    image = os.path.abspath(argv[argv.index("--image") + 1] if "--image" in argv
                            else os.path.join(REPO, "osk-freeware.dd"))
    root = os.path.join(REPO, "disk")
    table = load_table()
    if "--backlog" in argv:
        print("  %d programs still without a help.psv line" % rewrite_backlog(root, table))
        return 0
    if "--disk" in argv:
        root = argv[argv.index("--disk") + 1]
        if "--check" in argv:
            if render_disk_usage(root, table, check=True):
                return 0
            print("  DOC/USAGE is STALE -- run tools/helpcap.py --disk %s" % root)
            return 1
        print("  DOC/USAGE: %d lines" % render_disk_usage(root, table))
        return 0
    if not os.path.isdir(os.path.join(os9try.SDK, "CMDS")):
        sys.exit("no OS-9 system at %s -- set OS9SDK" % os9try.SDK)
    if "--probe" in argv:
        outdir = argv[argv.index("--out") + 1] if "--out" in argv else \
            os.path.join(REPO, "notes", "helpprobe")
        only = set(argv[argv.index("--only") + 1].split(",")) if "--only" in argv else None
        todo = [n for n in programs(root)
                if (only and n in only) or (not only and n not in table)]
        todo = [n for n in todo if n not in NEVER_PROBE]
        with imagelock.held(image, "helpcap"):
            for i, name in enumerate(todo, 1):
                text = capture(image, name + " -?")
                write_capture(name, name + " -?", text, outdir)
                first = text.split("\n")[0][:60] if text else "(silent)"
                print("  %3d/%d %-16s %s" % (i, len(todo), name, first))
        return 0
    only = set(argv[argv.index("--only") + 1].split(",")) if "--only" in argv else None
    hung = 0
    with imagelock.held(image, "helpcap"):
        for name, (cmd, _note) in table.items():
            if cmd is None or (only and name not in only):
                continue
            text = capture(image, cmd)
            write_capture(name, cmd, text)
            flag = ""
            if NO_ANSWER in text:
                flag, hung = "  <-- HUNG", hung + 1
            elif not text:
                flag = "  <-- silent"
            print("  %-16s %-28s %s%s" % (name, cmd, text.split("\n")[0][:40], flag))
    return hung


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
