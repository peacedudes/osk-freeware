#!/usr/bin/env python3
"""One writer at a time for a disk image.

WHY.  `screenshots.py`, `playtest.py` and `datatest.py` all point os9exec at
`osk-freeware.dd` itself, and every one of them WRITES to it -- they redirect
into /dd/tmp, they patch files with `pbyte`, `datatest.py` makes and removes
whole directories.  Two of them running at once are two OS-9 kernels writing
one RBF image with no idea the other exists, and RBF keeps its allocation map
in memory.  The failure that produces is not a wrong test result; it is a
corrupt image, discovered later, with nothing to say when it happened.

This is an ADVISORY lock and deliberately simple: a file beside the image
holding the pid and the tool that took it.  A stale lock from a killed run is
reported by name so it can be removed on purpose, never silently stolen -- a
lock that breaks itself is not a lock.

    with held(image, "screenshots"):
        ...

Nothing here waits.  A harness that finds the image busy should say so and
stop, because the alternative is a half-hour run whose results cannot be
trusted.
"""

import contextlib
import os
import sys


def path_for(image):
    """The lock file that guards `image'."""
    return os.path.abspath(image) + ".lock"


def _alive(pid):
    """Is there still a process with this pid?  Signal 0 asks without acting."""
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True                      # someone else's, but it is there
    return True


@contextlib.contextmanager
def held(image, who):
    """Hold the lock on `image' for the duration, or exit saying who has it."""
    lock = path_for(image)
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        try:
            owner = open(lock).read().strip()
            pid = int(owner.split()[0])
        except (OSError, ValueError, IndexError):
            owner, pid = "an unreadable lock file", -1
        if pid > 0 and not _alive(pid):
            sys.exit("%s: %s is locked by %s, which is no longer running.\n"
                     "   Remove %s if you are sure nothing else is using it."
                     % (who, os.path.basename(image), owner, lock))
        sys.exit("%s: %s is in use by %s -- wait for it to finish.\n"
                 "   Two harnesses writing one image corrupt it."
                 % (who, os.path.basename(image), owner))
    try:
        os.write(fd, ("%d %s\n" % (os.getpid(), who)).encode())
        os.close(fd)
        yield
    finally:
        try:
            os.unlink(lock)
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    sys.exit(__doc__)
