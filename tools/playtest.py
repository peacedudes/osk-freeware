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
    until   Dungeon level             WAIT FOR THIS TEXT to appear, up to 60
                                    seconds, instead of guessing at a number.
                                    A program whose start-up time varies --
                                    hack takes anywhere from 5 to 15 seconds
                                    to reach the dungeon -- cannot be driven
                                    by fixed waits without being flaky, and a
                                    flaky test is worse than no test.
    key     p                       one keystroke
    keys    jkl                     several, spaced by `rate'
    rate    1.0                     seconds between keys (default 0.6)
    esc                             the ESC key
    snap    inventory               SAVE THE SCREEN HERE, under this label
    expect  Tetrix                  text that must appear on the final screen
    absent  Couldn't open           text that must NOT appear anywhere
    minbytes 2000                   pass on RAW OUTPUT VOLUME instead of ink,
                                    for a screen animation that clears as it
                                    goes and is therefore blank at any instant
    size    20 80                   drive and render at a NON-STANDARD window
                                    size, to test what a program does when
                                    the terminal is not the 80x24 its
                                    termcap claims it is
    allow   trap handler            a COMPLAINT phrase to forgive for this
                                    program -- an editor showing a file full
                                    of error messages is not itself failing

Exit status is 0 when every `expect' was met and no `absent' appeared.
"""
import fcntl
import os
import pty
import struct
import subprocess
import sys
import termios
import threading
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import ansiscreen                                        # noqa: E402
# One writer at a time: all three harnesses write to the image itself.
import imagelock                                         # noqa: E402
from os9env import emulator_env                          # noqa: E402

OS9EXEC = os.environ.get("OS9EXEC",
                         os.path.join(REPO, "..", "os9exec", "os9exec"))
TERMCAP = "/dd/SYS/termcap"

# After `clear', the only thing on screen before the program draws is the
# command line itself -- about 30 characters. A program that leaves less than
# this behind did not really run: `pacman' exits the instant it starts and
# scored 35, which was all echo. Raised from 10 on 2026-08-27 after pacman,
# chess and lorenz3d all passed on the strength of the shell prompt.
MIN_INK = 8
# How long `until' will wait for its text before giving up and carrying on.
# Long enough for hack to reach the dungeon on a slow run, short enough that
# a script with a typo in its marker does not hang the sweep.
UNTIL_TIMEOUT = 60
# CONTROL-C DISCARDS WHAT IS STILL QUEUED FOR THE SCREEN.  SCF does that on
# a real system and os9exec does it too (utilstuff.c, pd_int ->
# baud_flush_device), so a program stopped mid-frame loses the tail of an
# escape sequence and the next one can arrive without its ESC.  `card' failed
# on exactly that, once in the eight runs measured.  The bytes after it
# are what a person sees as well; they are not corruption, so the orphaned-
# escape check stops at the first Control-C the script types.
INTERRUPT = "\003"
INTERRUPTED = object()                 # a `marks' entry that is not a snap


def parse(path):
    spec = {"name": os.path.basename(path).replace(".keys", ""),
            "prog": None, "setup": [], "acts": [], "expect": [], "absent": [],
            "allow": [], "minbytes": 0, "rate": 0.6, "size": (24, 80)}
    for raw in open(path):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        word, _, rest = line.partition(" ")
        rest = rest.strip()
        if word in ("name", "prog"):
            spec[word] = rest
        elif word == "minbytes":
            spec["minbytes"] = int(rest)
        elif word == "rate":
            spec["rate"] = float(rest)
        elif word == "size":
            rows, cols = rest.split()
            spec["size"] = (int(rows), int(cols))
        elif word == "setup":
            spec["setup"].append(rest)
        elif word == "wait":
            spec["acts"].append(("wait", float(rest)))
        # `until' WAS DOCUMENTED AND HANDLED BY feed() FROM 2026-08-29 AND
        # NEVER PARSED: the line fell through every branch here and was
        # dropped, so hackquit, moria and tass each ran with one wait fewer
        # than they were written with, and nothing said so.
        elif word == "until":
            spec["acts"].append(("until", rest))
        elif word == "key":
            named = {"\\r": "\r", "\\n": "\n", "\\e": "\033", "\\s": " "}
            if rest in named:
                rest = named[rest]
            elif rest.startswith("\\") and rest[1:].isdigit():
                rest = chr(int(rest[1:], 8))      # \003 -> Ctrl-C
            spec["acts"].append(("send", rest))
        elif word == "esc":
            spec["acts"].append(("send", "\033"))
        elif word == "keys":
            for ch in rest:
                spec["acts"].append(("send", ch))
        elif word == "snap":
            spec["acts"].append(("snap", rest))
        elif word in ("expect", "absent", "allow"):
            spec[word].append(rest)
    if not spec["prog"]:
        sys.exit("%s: no `prog' line" % path)
    return spec


def feed(spec, master, with_keys, cap=None, marks=None,
         until_times=None):
    """Write the shell lines, then the keystrokes, at human speed.

    `marks' collects (label, byte-offset) pairs at each `snap'. The offset is
    how much output had been written when the snapshot was asked for, so the
    screen at that moment is the render of the capture's first N bytes. That
    is how a mid-game screen -- hack's inventory, tet's board in play -- gets
    captured without stopping the program.
    """
    def out(s):
        os.write(master, s.encode("latin-1"))
    if True:
        # LET os9exec COME UP FIRST. On a pty the terminal echoes whatever is
        # typed before the emulator has taken the line, so a command sent too
        # early is simply lost -- `export TERM=vt100' vanished that way and
        # hack then stopped with "Unknown terminal type: dumb."
        time.sleep(3.5)
        # AS `tester', NOT THE SUPER-USER (2026-09-23): RBF lets 0.0 past
        # every permission check, so a play-test as su can pass a game whose
        # score file a reader could not write.  HARNESS_USER=su plays the
        # old way.
        user = os.environ.get("HARNESS_USER", "tester")
        if user != "su":
            out("/dd/CMDS/su -s /dd/CMDS/bash %s\r" % user)
            time.sleep(2.0)
        # THE ENVIRONMENT A PERSON ACTUALLY ARRIVES WITH. Running bash bare is
        # not how anyone meets this disk -- SYS/login sets these first, and a
        # program that wants one of them fails in a way that looks like a bug
        # in the program. `sokoban' stops with "cannot get your username"
        # without USER, and the harness scored that PASS until 2026-08-27.
        for line in ("export TERM=vt100",
                     "export TERMCAP=%s" % TERMCAP,
                     "export HOME=/dd",
                     "export USER=tester",
                     "export LOGNAME=tester",
                     # EVERY program directory, the way SYS/login sets it,
                     # so a play-test types `hack' rather than
                     # /dd/CMDS/GAMES/hack -- which is what a person types
                     # and all anybody wants to watch.
                     "export PATH=/dd/CMDS:/dd/CMDS/GAMES:/dd/CMDS/NETPBM:"
                     "/dd/CMDS/UUCP:/dd/CMDS/TEXCMDS:/dd/CMDS/ELM",
                     "export PATH=$PATH:/dd/CMDS/COMMS:/dd/CMDS/NETWORK:"
                     "/dd/CMDS/NEWS:/dd/CMDS/MNEWS:/dd/CMDS/WN:/dd/CMDS/ADL",
                     "export PATH=$PATH:/dd/CMDS/REBUILT:/dd/CMDS/DEMOS:"
                     "/dd/CMDS/DHRY:/dd/CMDS/GCC139:/dd/CMDS/SYSADMIN:"
                     "/dd/CMDS/DRIVERS:/dd/CMDS/MM1:/dd/CMDS/X68K:.",
                     "export HELPDIR=/dd/SYS/HELP",
                     # CLEAR THE SETUP OFF THE SCREEN. Those eight export
                     # lines are ~150 characters of ink, and `ink' is how this
                     # tool decides a program drew something. pacman, chess
                     # and lorenz3d all scored PASS on the strength of my own
                     # shell prompt while drawing nothing at all.
                     "clear"):
            out(line + "\r")
            time.sleep(0.5)
        for line in spec["setup"]:
            out(line + "\r")
            time.sleep(0.6)
        out(spec["prog"] + "\r")
        time.sleep(3.0)
        for kind, val in spec["acts"]:
            if kind == "wait":
                time.sleep(val)
            elif kind == "until":
                # THE KEYED PASS WATCHES; THE CONTROL PASS REPLAYS THE CLOCK.
                # Polling in both would leave the control run waiting out the
                # whole timeout for text its silent program never prints, and
                # the two passes have to cost the same wall clock or the
                # comparison between them means nothing.
                if with_keys:
                    began = time.time()
                    deadline = began + UNTIL_TIMEOUT
                    needle = val.encode("latin-1")
                    while time.time() < deadline:
                        try:
                            if needle in open(cap, "rb").read():
                                break
                        except OSError:
                            pass
                        time.sleep(0.4)
                    if until_times is not None:
                        until_times.append(time.time() - began)
                elif until_times:
                    time.sleep(until_times.pop(0))
                else:
                    time.sleep(5.0)
            elif kind == "snap":
                time.sleep(0.8)                # let the screen settle
                if marks is not None and cap:
                    try:
                        marks.append((val, os.path.getsize(cap)))
                    except OSError:
                        pass
            elif with_keys:
                if val == INTERRUPT and marks is not None and cap:
                    try:
                        marks.append((INTERRUPTED, os.path.getsize(cap)))
                    except OSError:
                        pass
                out(val)
                time.sleep(spec["rate"])
            else:
                time.sleep(spec["rate"])       # same wall clock, no keys
        time.sleep(2.0)


def run(spec, image, with_keys, cap, marks=None, until_times=None):
    """Drive the program on a REAL PSEUDO-TERMINAL.

    This used to use a FIFO, and a FIFO is not a terminal. Programs that ask
    `isatty()', or that reopen their own tty by name the way `tet' does, take
    a different path -- and so does os9exec, which puts a tty into raw
    character-at-a-time mode at startup and leaves a pipe alone. `hack' hung
    under the FIFO harness and works perfectly for a person at a terminal:
    the harness was wrong, not hack.

    A pty also lets the window size be SET, which matters because OS-9 has no
    way to ask for it: everything believes the 24x80 in the termcap entry, so
    a mismatch with the real window is what makes `life' fall apart. The
    `size' directive is how a script asks for that mismatch, and the render
    grid is set to match it, so the capture is what a person would see.
    """
    # /h0 IS THE IMAGE TOO.  Without OS9H0 os9exec falls back to <startPath>/h0,
    # which in this repo is a link to the working osk-freeware.dd -- so every
    # play-test mounted THAT as /h0, beside whatever emulator has it open, and
    # programs reading /h0 paths saw the wrong disk (found 2026-09-14 with
    # nethack3).  datatest.py and screenshots.py have always passed both.
    # emulator_env, not dict(os.environ): see tools/os9env.py.
    env = emulator_env(OS9DISK=image, OS9H0=image)
    master, slave = pty.openpty()
    rows, cols = spec["size"]
    fcntl.ioctl(slave, termios.TIOCSWINSZ,
                struct.pack("HHHH", rows, cols, 0, 0))

    collected = []

    def drain():
        while True:
            try:
                chunk = os.read(master, 65536)
            except OSError:
                break
            if not chunk:
                break
            collected.append(chunk)
            with open(cap, "ab") as fh:      # so `snap' can size the capture
                fh.write(chunk)

    open(cap, "wb").close()
    reader = threading.Thread(target=drain)
    reader.daemon = True
    reader.start()

    proc = subprocess.Popen([OS9EXEC, "bash"], stdin=slave, stdout=slave,
                            stderr=slave, env=env, close_fds=True)
    os.close(slave)
    feed(spec, master, with_keys, cap, marks, until_times)
    try:
        proc.wait(timeout=15)
    except subprocess.TimeoutExpired:
        proc.terminate()                     # ask, then allow time
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()                      # only after a polite stop failed
    reader.join(timeout=5)
    os.close(master)
    return b"".join(collected)


def playtest(path, image, outdir):
    spec = parse(path)
    os.makedirs(outdir, exist_ok=True)
    base = os.path.join(outdir, spec["name"])

    # THE CONTROL PASS IS ONLY NEEDED IF WE TYPE. It exists to answer "did
    # the keys change anything", which is a question only worth asking when
    # there were keys. Skipping it for the print-and-stop programs halves the
    # wall clock of a full sweep, and most of this disk is print-and-stop.
    typed_keys = sum(1 for kind, _ in spec["acts"] if kind == "send")
    marks, until_times = [], []
    keyed = run(spec, image, True, base + ".keyed.raw", marks, until_times)
    control = (run(spec, image, False, base + ".control.raw",
                   None, list(until_times))
               if typed_keys >= 2 else b"")

    rows, cols = spec["size"]
    ks = ansiscreen.render(keyed, rows, cols)
    cs = ansiscreen.render(control, rows, cols)
    open(base + ".screen.txt", "w").write(ks.text() + "\n")
    open(base + ".control.txt", "w").write(cs.text() + "\n")

    # JUDGE EVERY SCREEN, NOT THE LAST ONE. A program that tidies up on the
    # way out leaves an empty final frame: `hang' clears the screen when the
    # game ends, so the last frame is bare and the FIRST verdict this tool
    # gave it was FAIL -- while its snapshots showed a working hangman with
    # the guessed letters struck off. The screen worth judging, and the screen
    # worth publishing, is the one with the most on it.
    screens = [("final", ks)]
    cut = len(keyed)
    for label, off in marks:
        if label is INTERRUPTED:
            cut = min(cut, off)
            continue
        snap = ansiscreen.render(keyed[:off], rows, cols)
        open("%s.%s.txt" % (base, label), "w").write(snap.text() + "\n")
        screens.append((label, snap))
    # INK MEANS THE PROGRAM'S OWN OUTPUT, not the shell's. Any line holding
    # the `bash#' prompt is ours -- the command we typed and the prompt we
    # came back to -- and counting it made `valspeak' look like it drew 348
    # characters when it drew none at all.
    def own_ink(scr):
        return sum(1 for line in scr.text().split("\n")
                   if "bash#" not in line and "bash$ " not in line
                   for ch in line if ch != " ")
    best_label, best = max(screens, key=lambda p: own_ink(p[1]))

    alltext = "\n".join(s.text() for _, s in screens)
    # SEARCH THE RAW STREAM TOO, both ways.  `screens' holds the snapshots
    # taken at `snap' marks and the last screen, so anything a program
    # scrolled past between them is not in `alltext' at all -- `orbit' prints
    # a header and then eighty lines of satellite positions, and every line
    # of that header had gone by the time the first snapshot was taken.  A
    # thing the program demonstrably PRINTED satisfies `expect'; `absent' has
    # consulted the raw stream since it was written, and this makes the pair
    # symmetrical.
    raw = keyed.decode("latin-1", "replace")
    missing = [e for e in spec["expect"] if e not in alltext and e not in raw]
    present = [a for a in spec["absent"] if a in alltext or a in raw]
    # ONLY DEMAND A RESPONSE IF WE ACTUALLY TYPED SOMETHING AT IT.
    # Most of this disk's "games" are not interactive at all -- valspeak,
    # wisecrack, colortest and dclock print and stop. A script for one of
    # those sends a single quit key and nothing else, so the keyed and control
    # screens are identical BY CONSTRUCTION and `responds' was false for
    # seventeen perfectly healthy programs. Two or more keystrokes means we
    # were really driving it; one means we were only getting out.
    responds = (ks.text() != cs.text() or best.ink() > cs.ink() + 4
                if typed_keys >= 2 else True)
    orphans = len(ansiscreen.render(keyed[:cut], rows, cols).orphans)

    # A KEYED RUN THAT DREW LESS THAN THE CONTROL IS A FAILURE, not a pass.
    # `snake' fooled the first version of this check: typing made it hang at
    # startup about one run in six, so the keyed screen held a bash prompt and
    # the control held a drawn board. The two texts DIFFERED, so `responds'
    # was true and it was scored PASS -- while the program had not started.
    # Starved means THE PROGRAM NEVER GOT GOING, not merely that it drew less.
    # A ratio, not a difference: keys often make a program QUIT sooner, so the
    # control legitimately ends up with more on screen. `tet' quits on `q' and
    # finishes on its high-score board (282 ink) while the untouched control
    # plays on and stacks the board (366) -- that is healthy, and a plain
    # difference called it a failure. A run that never started sits far lower
    # than that: snake's hung run holds a bash prompt, under a third of what
    # its control drew.
    starved = (own_ink(cs) > 60
               and own_ink(best) < 0.5 * own_ink(cs)) if control else False

    # A PROGRAM THAT SAYS IT FAILED HAS FAILED, however much it drew.
    # `sokoban' printed "cannot get your username" and was scored PASS
    # because something appeared and the screen changed.
    # SPECIFIC PHRASES ONLY. "No such" on its own matched a line of sonnet's
    # own poetry -- "No such the grasp the byte biweekly genius" -- and failed
    # a program that was doing exactly what it is for. A keyword list that
    # reads program OUTPUT has to be narrow enough not to convict prose.
    COMPLAINTS = ("cannot get your", "can't open", "Can't open", "cannot open",
                  "illegal char in", "illegal command line",
                  "No such file", "no such file", "command not found",
                  "unknown terminal", "Unknown terminal", "Stack Overflow",
                  "Can't install trap handler", "bus error", "Bus error")
    complained = [c for c in COMPLAINTS if c in alltext
                  and not any(a in c or c in a for a in spec["allow"])]

    # A SCREEN ANIMATION IS BLANK AT EVERY INSTANT. `ttyexp' is fireworks that
    # clear as they go: 3256 bytes of real cursor motion, and any single frame
    # holds about five characters. For those, volume is the honest measure.
    drew_enough = (len(keyed) >= spec["minbytes"] if spec["minbytes"]
                   else own_ink(best) >= MIN_INK)

    verdict = "PASS"
    if (missing or present or not responds or orphans
            or not drew_enough or starved or complained):
        verdict = "FAIL"

    print("%-14s %-5s ink=%-5d(%s) orphans=%-3d responds=%-3s%s%s"
          % (spec["name"], verdict, own_ink(best), best_label, orphans,
             "yes" if responds else "NO",
             "  missing=%s" % missing if missing else "",
             ("  STARVED (control drew %d)" % own_ink(cs)) if starved
             else ("  SAID: %s" % complained[0]) if complained
             else ("  found=%s" % present if present else "")))
    return verdict == "PASS", spec, best


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
    # AN OS9Hx/OS9DISK PATH MUST BE ABSOLUTE -- see the same line in
    # datatest.py. A bare relative name mounts the device and lets module
    # loading work while ordinary file opens on it silently fail.
    image = os.path.abspath(image)

    with imagelock.held(image, "playtest"):
        for s in scripts:
            ok, _, _ = playtest(s, image, outdir)
            bad += 0 if ok else 1
    print("\n%d of %d passed" % (len(scripts) - bad, len(scripts)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
