#!/usr/bin/env python3
r"""Run one command on a REAL TERMINAL and count what comes back.

    tools/pty_probe.py "load nosuchmodule"
    tools/pty_probe.py "tree /nosuchdir" --seconds 30
    tools/pty_probe.py "..." --image <other.dd> --os9exec <other binary>

IT IGNORES OS9DISK AND OS9H0 IN THE ENVIRONMENT, on purpose.  Both are
commonly exported on this machine -- OS9DISK at the SDK overlay, OS9H0 at
a symlink -- and a first version of this tool took them as defaults.  It
then booted the SDK as /dd, found no /dd/SYS/login, and died before it
could type anything, reporting an `Input/output error' from the pty
rather than "I measured the wrong disk".  A tool that answers about a
tree nobody pointed it at is the shape this collection keeps producing;
the image and the emulator are named in the output of every run.

WHY THIS EXISTS.  Every other harness here -- `screenshots.py',
`datatest.py', `drive.py', `os9try.py' -- captures os9exec through a PIPE.
A fault that only appears when a path is an SCF TERMINAL is invisible to
all of them, which means invisible to 956 published cards and 868 cases.

On 2026-09-19 rdoggett reported that `load nosuchmodule' repeats its error
for ever.  Piped, it printed once, and the first two attempts to reproduce
it both said the report was wrong.  Under a pty it reproduced immediately
-- about 850 repeats in twenty seconds.  The cause was os9exec's F$PErr
SEARCHING the path it was handed, which for `prerr(2, ...)' is standard
error: searching a terminal meant reading it, the read parked the process
and returned empty, and the dispatcher resumes a parked process by
re-running its call.  Redirecting made that read report EOF instead of
parking, which is exactly why every piped harness was green.

NOT A GATE and not a sweep: one command, one session, the output printed
raw with a count of how many times its longest line repeats.  Reach for it
when a report contradicts a green sweep.

The session gets a soft landing -- `exit', a pause, and a signal only if
it is still there afterwards.
"""
import os
import pty
import re
import select
import signal
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run(command, seconds, image, emulator):
    pid, fd = pty.fork()
    if pid == 0:                                  # the child IS the terminal
        env = dict(os.environ)
        env["OS9DISK"] = image
        env["OS9H0"] = image
        env["TERM"] = "vt100"
        os.execve(emulator, [emulator, "/dd/CMDS/bash", "/dd/SYS/login"], env)

    out = bytearray()

    def pump(limit):
        end = time.time() + limit
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.3)
            if not r:
                continue
            try:
                data = os.read(fd, 65536)
            except OSError:                        # the child closed the pty
                return
            if not data:
                return
            out.extend(data)

    pump(6)                                        # let login finish
    mark = len(out)
    os.write(fd, (command + "\r").encode())
    pump(seconds)
    tail = bytes(out[mark:]).decode("latin-1", "replace")

    # Soft landing: ask it to leave, give it time, and only then insist.
    try:
        os.write(fd, b"exit\r")
    except OSError:
        pass
    pump(4)
    try:
        os.kill(pid, 0)
        os.kill(pid, signal.SIGTERM)
    except OSError:
        pass
    try:
        os.waitpid(pid, 0)
    except OSError:
        pass
    return tail


def main(argv):
    command = "load nosuchmodule"
    seconds = 20
    opts, rest = {}, []
    i = 0
    while i < len(argv):
        if argv[i] in ("--seconds", "--image", "--os9exec") \
                and i + 1 < len(argv):
            if argv[i] == "--seconds":
                seconds = int(argv[i + 1])
            else:
                opts[argv[i]] = argv[i + 1]
            i += 2
            continue
        if argv[i].startswith("--"):
            sys.stderr.write("pty_probe: unknown option %s\n" % argv[i])
            return 2
        rest.append(argv[i])
        i += 1
    if rest:
        command = rest[0]

    # NOT os.environ: see the header.  OS9DISK is exported on this machine
    # and points at the SDK overlay, not at the collection.
    image = opts.get("--image", os.path.join(REPO, "osk-freeware.dd"))
    emulator = opts.get(
        "--os9exec", os.path.expanduser("~/Developer/os9/os9exec/os9exec"))
    for p in (image, emulator):
        if not os.path.exists(p):
            sys.stderr.write("pty_probe: no %s\n" % p)
            return 2

    print("image     %s" % image)
    print("os9exec   %s" % emulator)
    print("command   %s\n" % command)
    tail = run(command, seconds, image, emulator)
    print(tail)

    lines = [l.strip() for l in re.split(r"[\r\n]+", tail) if l.strip()]
    worst, count = "", 0
    for line in set(lines):
        n = lines.count(line)
        if n > count:
            worst, count = line, n
    print("---- %d byte(s) in %ds; most-repeated line appears %d time(s)%s"
          % (len(tail), seconds, count,
             (": " + worst[:60]) if count > 2 else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
