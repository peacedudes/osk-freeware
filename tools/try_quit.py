#!/usr/bin/env python3
"""Find what actually quits a full-screen program, by running it as a person does.

Two earlier approaches failed and both failures are worth keeping:

  * Piping to these proves nothing. With stdin not a terminal they exit at EOF
    immediately, so every candidate key "works".
  * Driving os9exec directly with -r still fails: os9exec does not inherit TERM
    into the OS-9 environment, and the program stops with "TERM environment
    variable not set". SYS/login is what sets TERM, TERMCAP and PATH.

So this runs bash through SYS/login under a real pty, types the command, lets
it draw, sends the key, and watches for the SHELL PROMPT to come back. A
control run sends no key at all: if the prompt returns anyway the program left
on its own and the key is unproven.

Usage: try_quit.py '<command line>' --keys q Q '\\003' ...
"""
import os, pty, select, signal, sys, time

EXEC = "/Users/rdoggett/Developer/os9/os9exec/os9exec"
ROOT = "/Users/rdoggett/Developer/os9/osk-freeware"
IMG = os.path.join(ROOT, "osk-freeware.dd")
PROMPT = b"os9$"


def drain(fd, seconds):
    out, end = b"", time.time() + seconds
    while time.time() < end:
        r, _, _ = select.select([fd], [], [], 0.2)
        if r:
            try:
                out += os.read(fd, 65536)
            except OSError:
                break
    return out


def attempt(cmd, key, settle=3.0, wait=6.0):
    """True if the prompt came back after the key was sent."""
    pid, fd = pty.fork()
    if pid == 0:
        os.environ.update(OS9DISK=IMG, OS9H0=IMG, TERM="vt100")
        os.chdir(ROOT)
        os.execv(EXEC, [EXEC, "-r", "bash", "/dd/SYS/login"])
    try:
        drain(fd, 2.0)                                  # login banner
        os.write(fd, cmd.encode() + b"\n")
        before = drain(fd, settle)                      # let the program draw
        if PROMPT in before.split(cmd.encode())[-1]:
            return None                                 # never took the screen
        if key:
            os.write(fd, key)
        after = drain(fd, wait)
        return PROMPT in after
    finally:
        try:
            os.kill(pid, signal.SIGKILL)
            os.waitpid(pid, 0)
        except OSError:
            pass
        os.close(fd)


def main():
    a = sys.argv[1:]
    i = a.index("--keys")
    cmd, keys = a[0], a[i+1:]
    name = cmd.split()[0].split("/")[-1]
    ctrl = attempt(cmd, None)
    if ctrl is None:
        print("  %-12s did not hold the screen (exited or never started)" % name); return
    if ctrl:
        print("  %-12s returns to the prompt on its own -- no key needed" % name); return
    for k in keys:
        key = k.encode().decode("unicode_escape").encode("latin-1")
        if attempt(cmd, key):
            print("  %-12s QUITS ON %s" % (name, repr(k))); return
    print("  %-12s not quit by %s" % (name, " ".join(map(repr, keys))))


main()
