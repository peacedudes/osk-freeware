#!/usr/bin/env python3
"""Stop CMDS/bash handing every open path to the commands it runs.

    tools/patch_bash_forkpaths.py disk/CMDS/bash               # report only
    tools/patch_bash_forkpaths.py disk/CMDS/bash --check       # 0 if patched
    tools/patch_bash_forkpaths.py disk/CMDS/bash --apply out   # write a copy

bash runs a command through its C library's execve() (and execl, execle,
execlp, execv, execvp beside it -- all six share one helper).  None of them
passes a fixed path count to F$Fork: the helper at $2B476 asks fcntl() about
paths 31, 30, ... 0 and returns the highest OPEN one plus one, and that is
what goes to os9forkc() in d3.  In a pipeline bash has the /pipe open on a
path of its own above 2 while it forks each side, so each child is handed
that path as well as the dup on its 0 or 1.  The writer then holds the pipe
twice; when the reader exits the pipe still has another user, so the write
never gets E$Write and `cat file | head -n 1' waits for ever.  Microware's
shell forks with three paths, and `list file ! head' ends at once.

The patch is one byte: the helper's scan starts at path 2 instead of 31
(`moveq #31,d2' $741F -> `moveq #2,d2' $7402), so a child is given paths
0-2 -- or fewer, if bash itself has 2 or 1 closed -- exactly as Microware's
shell gives them.  The module CRC is re-sealed; the header is untouched, so
its parity stands.  The cost: a path above 2 no longer reaches a child, so
`cmd 3>file' opens the file and the command never sees it.

It refuses anything but the expected bash: the input must be a sealed
module whose helper has exactly the old bytes, once, at $2B476.  Report-
only by default; `--apply <out>' writes a COPY and never touches its input.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rename_module import crc24, parity   # noqa: E402

AT = 0x2B476
# movel d2,-(sp) / moveq #N,d2 / clrl -(sp) / pea 1 / movel d2,-(sp) / bsr fcntl
OLD = bytes.fromhex("2f02741f42a7487800012f026100634e")
NEW = bytes.fromhex("2f02740242a7487800012f026100634e")
CRC_BYTES = 3


def sealed(b):
    size = int.from_bytes(b[4:8], "big")
    return (size == len(b) and parity(bytes(b)) == 0xFFFF
            and crc24(bytes(b[:size - CRC_BYTES]))
            == int.from_bytes(b[size - CRC_BYTES:], "big"))


def state(b):
    here = bytes(b[AT:AT + len(OLD)])
    return ("patched" if here == NEW and not b.count(OLD) else
            "unpatched" if here == OLD and b.count(OLD) == 1 else
            "not the expected bash")


def main(argv):
    if not argv or len(argv) > 3:
        sys.exit(__doc__.strip().splitlines()[0])
    src = argv[0]
    b = bytearray(open(src, "rb").read())
    if not sealed(b):
        sys.exit("%s: not a sealed OS-9 module" % src)
    now = state(b)
    if argv[1:] == ["--check"]:
        print("%s: %s" % (src, now))
        return 0 if now == "patched" else 1
    if len(argv) == 1:
        print("%s: %s; path-count scan at $%X would start at path 2"
              % (src, now, AT))
        return 0
    if argv[1] != "--apply" or len(argv) != 3:
        sys.exit(__doc__.strip().splitlines()[0])
    if now != "unpatched":
        sys.exit("%s: %s -- refusing" % (src, now))
    b[AT:AT + len(NEW)] = NEW
    size = len(b)
    b[size - CRC_BYTES:] = crc24(bytes(b[:size - CRC_BYTES])).to_bytes(
        CRC_BYTES, "big")
    if not sealed(b) or state(b) != "patched":
        sys.exit("patched copy failed to verify")
    open(argv[2], "wb").write(bytes(b))
    print("%s -> %s: path-count scan at $%X starts at 2, CRC re-sealed"
          % (src, argv[2], AT))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
