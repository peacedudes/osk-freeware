#!/usr/bin/env python3
"""PLAY a program on the disk and show the screen it drew.

    tools/playtest.py <script.keys> [--image osk-freeware.dd] [--out DIR]
    tools/playtest.py --all [--out DIR]

Why this exists
---------------
`tools/verify_all.sh' asks "did it print anything". That is not the same
question as "does it work", and the difference is not academic: it scored
`tet' as OK BARE while `tet' ignored every keypress, and scored it OK again
when `tet' ran so fast it was unplayable. Anything whose value is in its
INPUT handling -- games, editors, anything full-screen -- gets false credit
from that sweep and always will.

This drives the program the way a person does: keystrokes arrive one at a
time, at human speed, through a FIFO into os9exec's console. What comes back
is rendered by tools/ansiscreen.py into the 80x24 grid a vt100 would show,
and saved. A play-test is then something you can LOOK at.

It also runs a CONTROL pass with no keys at all. A program that draws the
same screen whether or not you type is not reading the keyboard, and that
comparison is the only reliable way to tell from outside.

Script format (one directive per line, # comments ignored):

    name    tet                     what to call this test
    prog    /dd/CMDS/GAMES/tet      what to run
    setup   export FOO=bar          extra shell line before the program
    wait    4                       seconds
    key     p                       one keystroke
    keys    jkl                     several, spaced by `rate'
    rate    1.0                     seconds between keys (default 0.6)
    esc                             the ESC key
    snap    inventory               SAVE THE SCREEN HERE, under this label
    expect  Tetrix                  text that must appear on the final screen
    absent  Couldn't open           text that must NOT appear anywhere

Exit status is 0 when every `expect' was met and no `absent' appeared.
"""
import os
import subprocess
import sys
import threading
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import ansiscreen                                        # noqa: E402

OS9EXEC = os.environ.get("OS9EXEC",
                         os.path.join(REPO, "..", "os9exec", "os9exec"))
TERMCAP = "/dd/SYS/termcap"


def parse(path):
    spec = {"name": os.path.basename(path).replace(".keys", ""),
            "prog": None, "setup": [], "acts": [], "expect": [], "absent": [],
            "rate": 0.6}
    for raw in open(path):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        word, _, rest = line.partition(" ")
        rest = rest.strip()
        if word in ("name", "prog"):
            spec[word] = rest
        elif word == "rate":
            spec["rate"] = float(rest)
        elif word == "setup":
            spec["setup"].append(rest)
        elif word == "wait":
            spec["acts"].append(("wait", float(rest)))
        elif word == "key":
            spec["acts"].append(("send", rest))
        elif word == "esc":
            spec["acts"].append(("send", "\033"))
        elif word == "keys":
            for ch in rest:
                spec["acts"].append(("send", ch))
        elif word == "snap":
            spec["acts"].append(("snap", rest))
        elif word in ("expect", "absent"):
            spec[word].append(rest)
    if not spec["prog"]:
        sys.exit("%s: no `prog' line" % path)
    return spec


def feed(spec, fifo, with_keys, cap=None, marks=None):
    """Write the shell lines, then the keystrokes, at human speed.

    `marks' collects (label, byte-offset) pairs at each `snap'. The offset is
    how much output had been written when the snapshot was asked for, so the
    screen at that moment is the render of the capture's first N bytes. That
    is how a mid-game screen -- hack's inventory, tet's board in play -- gets
    captured without stopping the program.
    """
    with open(fifo, "w") as f:
        def out(s):
            f.write(s)
            f.flush()
        out("export TERM=vt100\r")
        time.sleep(0.6)
        out("export TERMCAP=%s\r" % TERMCAP)
        time.sleep(0.6)
        for line in spec["setup"]:
            out(line + "\r")
            time.sleep(0.6)
        out(spec["prog"] + "\r")
        time.sleep(3.0)
        for kind, val in spec["acts"]:
            if kind == "wait":
                time.sleep(val)
            elif kind == "snap":
                time.sleep(0.8)                # let the screen settle
                if marks is not None and cap:
                    try:
                        marks.append((val, os.path.getsize(cap)))
                    except OSError:
                        pass
            elif with_keys:
                out(val)
                time.sleep(spec["rate"])
            else:
                time.sleep(spec["rate"])       # same wall clock, no keys
        time.sleep(2.0)


def run(spec, image, with_keys, cap, marks=None):
    fifo = cap + ".fifo"
    if os.path.exists(fifo):
        os.unlink(fifo)
    os.mkfifo(fifo)
    env = dict(os.environ, OS9DISK=image)
    # The writer goes FIRST, on its own thread. Opening a FIFO read-only blocks
    # until a writer appears, so this ordering is what lets os9exec take the
    # read end as an ordinary blocking stdin -- the same arrangement that works
    # by hand as `os9exec bash < fifo'. Handing Popen an O_RDWR descriptor
    # instead looked equivalent and was not: bash came up and never saw a byte.
    writer = threading.Thread(target=feed,
                              args=(spec, fifo, with_keys, cap, marks))
    writer.daemon = True
    writer.start()
    with open(cap, "wb") as sink:
        rfd = os.open(fifo, os.O_RDONLY)
        proc = subprocess.Popen([OS9EXEC, "bash"], stdin=rfd,
                                stdout=sink, stderr=subprocess.STDOUT, env=env)
        writer.join(timeout=180)
        try:
            proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            proc.terminate()               # ask it to stop, then give it time
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()                # only after a polite stop failed
        os.close(rfd)
    os.unlink(fifo)
    return open(cap, "rb").read()


def playtest(path, image, outdir):
    spec = parse(path)
    os.makedirs(outdir, exist_ok=True)
    base = os.path.join(outdir, spec["name"])

    marks = []
    keyed = run(spec, image, True, base + ".keyed.raw", marks)
    control = run(spec, image, False, base + ".control.raw")

    ks = ansiscreen.render(keyed)
    cs = ansiscreen.render(control)
    open(base + ".screen.txt", "w").write(ks.text() + "\n")
    for label, off in marks:
        snap = ansiscreen.render(keyed[:off])
        open("%s.%s.txt" % (base, label), "w").write(snap.text() + "\n")
    open(base + ".control.txt", "w").write(cs.text() + "\n")

    text = ks.text()
    missing = [e for e in spec["expect"] if e not in text]
    present = [a for a in spec["absent"]
               if a in text or a in keyed.decode("latin-1", "replace")]
    responds = ks.text() != cs.text()

    verdict = "PASS"
    if missing or present or not responds or ks.orphans:
        verdict = "FAIL"

    print("%-14s %-5s ink=%-5d orphans=%-3d responds=%-3s%s%s"
          % (spec["name"], verdict, ks.ink(), len(ks.orphans),
             "yes" if responds else "NO",
             "  missing=%s" % missing if missing else "",
             "  found=%s" % present if present else ""))
    return verdict == "PASS", spec, ks


def main(argv):
    image = os.path.join(REPO, "osk-freeware.dd")
    outdir = os.path.join(REPO, "notes", "playtests")
    scripts, i = [], 0
    while i < len(argv):
        a = argv[i]
        if a == "--image":
            i += 1
            image = argv[i]
        elif a == "--out":
            i += 1
            outdir = argv[i]
        elif a == "--all":
            d = os.path.join(REPO, "tools", "playtests")
            scripts += sorted(os.path.join(d, f) for f in os.listdir(d)
                              if f.endswith(".keys"))
        else:
            scripts.append(a)
        i += 1
    if not scripts:
        sys.exit(__doc__)
    if not os.path.exists(image):
        sys.exit("no image at %s -- run tools/mkimage.sh first" % image)

    bad = 0
    for s in scripts:
        ok, _, _ = playtest(s, image, outdir)
        bad += 0 if ok else 1
    print("\n%d of %d passed" % (len(scripts) - bad, len(scripts)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
