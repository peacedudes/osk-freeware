#!/usr/bin/env python3
"""Run every OS-9 module in a directory once, and say what happened.

    tools/smoke_pool.py <dir> [--image <dd>] [--timeout 8] [--tsv out.tsv]

WHY.  Mining pass 1, 2026-09-22.  rdoggett wants the unmined archives put
through the emulator quickly -- "smoke testing everything quickly to find
how many appear to be broken" -- because an unfamiliar binary is what finds
the holes in os9exec, and his release waits on that confidence.

WHAT IT DOES.  Finds every file whose first two bytes are OS-9's $4AFC sync,
mounts the directory as /h6 beside the collection as /dd (and /h0), and runs
each module BY PATH with its input from /nil and a short timeout.  Nothing is
installed and the image is never written to, so several of these can run at
once on copies of the same image without touching each other.

WHAT IT REPORTS, one row per module:

    file, module name, bytes, seconds, status, first line of output

  status is the first of these that fits, and each means something different
  to whoever reads the table:
    EXCEPTION   the emulator reported a processor exception -- look here
                first: this is either the program or os9exec, and telling
                them apart is the point of the exercise
    TIMEOUT     still running when the clock ran out (interactive, or hung)
    NEEDS-MOD   stopped with E_MNF or a trap-handler message: it wants a
                module that is not here (cio, a library, a helper)
    SILENT      ran, said nothing, exited cleanly -- usual for a filter
    SPOKE       printed something and exited
    E_xxx       exited with an OS-9 error of its own

A module that prints its usage line is working, and a module that wants cio
is fine on this disk; neither is a defect.  This table is for finding the
ones that are.
"""
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SYNC = b"\x4a\xfc"
EXC = re.compile(r"vector=\$[0-9A-Fa-f]+|Exception:")
MNF = re.compile(r"E_MNF|module not found|Can't install trap handler|"
                 r"traphandler mismatch|can't install", re.I)
ERR = re.compile(r"#000:(\d+)|\(E_(\w+)\)")


def modules(top):
    for base, _, files in os.walk(top):
        for f in sorted(files):
            p = os.path.join(base, f)
            try:
                if open(p, "rb").read(2) == SYNC:
                    yield p
            except OSError:
                continue


def module_name(path):
    b = open(path, "rb").read()
    try:
        at = int.from_bytes(b[12:16], "big")
        return b[at:at + 32].split(b"\0")[0].decode("latin-1", "replace")[:24]
    except Exception:                                    # noqa: BLE001
        return ""


def run(path, top, image, exe, seconds):
    sys.path.insert(0, HERE)
    from os9env import emulator_env
    rel = "/h6/" + os.path.relpath(path, top).replace(os.sep, "/")
    # ONE SCRIPT NAME PER RUN.  Two runs over the same directory used to share
    # `_smoke.sh', so each overwrote the other's script and modules ran each
    # other's commands -- `cat' printed `watch's usage, and two programs were
    # recorded as TIMEOUT that were never run at all (mining pass 1, bucket 1,
    # 2026-09-22).  A table that quietly reports another program's behaviour is
    # worse than no table.
    script = os.path.join(top, "_smoke.%d.sh" % os.getpid())
    open(script, "wb").write(
        ("PATH=/dd/CMDS\rexport PATH\r%s < /nil\recho \"@@rc=$?\"\r" % rel)
        .encode("latin-1"))
    guest = "/h6/" + os.path.basename(script)
    env = emulator_env(LC_ALL="C", OS9DISK=image, OS9H0=image, OS9H6=top)
    started = time.time()
    try:
        r = subprocess.run([exe, "-r", "bash", guest], env=env,
                           capture_output=True, timeout=seconds)
        out = r.stdout.decode("latin-1", "replace")
        timed = False
    except subprocess.TimeoutExpired as exc:
        out = (exc.stdout or b"").decode("latin-1", "replace")
        timed = True
    took = time.time() - started
    text = out.replace("\r", "\n")
    body = [l for l in text.split("\n")
            if l.strip() and not l.startswith("#") and "@@rc=" not in l]
    rc = re.search(r"@@rc=(\d+)", text)
    status = ("EXCEPTION" if EXC.search(text) else
              "TIMEOUT" if timed else
              "NEEDS-MOD" if MNF.search(text) else
              "SPOKE" if body else
              "E_%s" % rc.group(1) if rc and rc.group(1) not in ("0",) else
              "SILENT")
    first = body[0][:90] if body else ""
    return status, round(took, 1), first


def main(argv):
    if not argv or argv[0].startswith("--"):
        sys.exit(__doc__.strip().splitlines()[0])
    top = os.path.abspath(argv[0])
    image = argv[argv.index("--image") + 1] if "--image" in argv else \
        os.path.join(REPO, "osk-freeware.dd")
    exe = os.environ.get("OS9EXEC", os.path.join(REPO, "..", "os9exec", "os9exec"))
    seconds = int(argv[argv.index("--timeout") + 1]) if "--timeout" in argv else 8
    out = open(argv[argv.index("--tsv") + 1], "w") if "--tsv" in argv else sys.stdout
    found = list(modules(top))
    print("# %d modules under %s" % (len(found), top), file=out)
    for p in found:
        status, took, first = run(p, top, image, exe, seconds)
        print("\t".join([os.path.relpath(p, top), module_name(p),
                         str(os.path.getsize(p)), str(took), status, first]),
              file=out, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
