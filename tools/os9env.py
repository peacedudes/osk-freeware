#!/usr/bin/env python3
"""The environment an emulator run gets -- and nothing the operator's shell
happened to be carrying.

WHY THIS EXISTS.  Every harness here built its environment as
`dict(os.environ, OS9DISK=image, OS9H0=image, ...)', which passes through
EVERY other `OS9*' variable the person running it happens to export.  On
2026-09-20 os9exec's own `idevs', typed inside a `pty_probe' session, listed
a device nobody had asked for:

    h3         image    rbf                 <a tree outside this repository>

It was `OS9H3', exported in the operator's shell, mounted into every session
every harness had ever started -- 956 cards, 871 cases and every drive
transcript.  Nothing had ever READ from it (no sheet or case names /h3, and
that was checked), so no published result is wrong.  But an RBF device that
appears because of who ran the tool is exactly the class of thing this
collection keeps being bitten by: a result that cannot be reproduced on
another machine, and that nobody can see in the output.

`OS9T' and `OS9STOP' were being inherited the same way, and those are not
mounts at all -- they change how the emulator behaves.

So: an emulator run gets a CLEAN slate of `OS9*' variables plus exactly what
its harness names, and `dropped()' says what was set aside so a run can
report it rather than hide it.

NOT HANDLED HERE, deliberately: os9exec also takes host variables whose name
begins with `@' (`@TERM', `@TERMCAP' -- see prepParams).  Nobody exports
those from a login shell, and a harness that wants one passes it on purpose,
so stripping them would cost more than it saved.  If that ever changes, this
is the place.
"""
import os

PREFIX = "OS9"


def dropped(environ=None):
    """The OS9* variables in `environ' that an emulator run will NOT see."""
    environ = os.environ if environ is None else environ
    return {k: v for k, v in environ.items() if k.startswith(PREFIX)}


def emulator_env(environ=None, **settings):
    """A copy of `environ' with every OS9* variable removed, then `settings'.

    Pass the devices and knobs the run actually needs:

        env = emulator_env(LC_ALL="C", OS9DISK=image, OS9H0=image)

    A setting whose value is None is left out, so a harness can offer an
    optional device without building the dict twice:

        env = emulator_env(OS9DISK=image, OS9H0=image, OS9H1=sdk_or_None)
    """
    environ = os.environ if environ is None else environ
    env = {k: v for k, v in environ.items() if not k.startswith(PREFIX)}
    for k, v in settings.items():
        if v is not None:
            env[k] = v
    return env


if __name__ == "__main__":
    have = dropped()
    if not have:
        print("no OS9* variables are exported here; "
              "harness runs were already clean")
    else:
        print("these are exported and would reach an emulator run "
              "unless a harness uses emulator_env():")
        for k in sorted(have):
            print("  %-10s %s" % (k, have[k]))


def login_loads():
    """The reader's commands SYS/login makes resident: its `for m in' list."""
    import re
    login = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "disk", "SYS", "login")
    text = open(login, newline="").read().replace("\r", "\n")
    found = re.search(r"^\s*for m in (.*?)\n\s*do\b", text, re.S | re.M)
    if not found:
        raise SystemExit("os9env: no `for m in' load list in %s" % login)
    return tuple(found.group(1).replace("\\", " ").split())


def stage_reader_load(h1):
    """Put the reader's own load and the commands SYS/login loads in <h1>/CMDS, from $OS9SDK.

    The collection ships no `load': the clean-room one written for it was
    withheld on 2026-09-22 and then deleted, because a
    program named after a Microware utility is Microware's to ship.  A
    harness that makes a module resident therefore needs the reader's own,
    on the /h1 it mounts -- exactly the arrangement SYS/login describes.

    Returns the path `load' was staged from, or None when $OS9SDK names no
    load: the caller says so, and the cases that load a module fail with a
    reason.
    CI never needs it -- it builds the image and runs the checks, not the
    suite.
    """
    import shutil
    sdk = os.environ.get("OS9SDK")
    staged = None
    # `unlink' comes with it, and for a reason measured 2026-09-23: most
    # modules here are STICKY, so since os9exec a4b338e one that has run
    # stays resident at link count 0 -- as on a real OS-9 -- and answers for
    # a second file of the same module name run later in the same session.
    # `/h1/CMDS/unlink <name>' between them is what a case does about it.
    # And every command SYS/login loads from the reader's /h1 (2026-09-23),
    # read from that file so the two cannot drift: nnmaster, v7make and
    # creadoc fork the reader's shell, nnmaster -I sorts with qsort, hist
    # sets the line with tmode, and so on -- no case could reach them
    # without.  Plus `dir', which creadoc reads the listing of.  A family
    # that wants one says `load /h1/CMDS/shell', as SYS/login does; staging
    # never makes one resident, so the disk's own `dir' still answers
    # everywhere else.
    for name in ("load", "dir") + login_loads():
        src = os.path.join(sdk, "CMDS", name) if sdk else ""
        # TAKE THE OLD ONE AWAY FIRST.  The work directory survives between
        # runs, so a `load' staged by an earlier run with $OS9SDK set was
        # still there for a later run without it -- and twelve cases that
        # cannot work without a load all passed, on 2026-09-22, for that
        # reason alone.
        dst = os.path.join(h1, "CMDS", name)
        if os.path.exists(dst):
            os.remove(dst)
        if not os.path.isfile(src):
            continue
        os.makedirs(os.path.join(h1, "CMDS"), exist_ok=True)
        shutil.copyfile(src, dst)
        os.chmod(dst, 0o755)
        if name == "load":
            staged = src
    # AND THE READER'S C LIBRARIES AND HEADERS (2026-09-24), for the two gccs
    # added that day: each compiles to assembly and hands it to the reader's
    # own r68 and l68, which link cstart.r and clibn.l from /h1/LIB and read
    # headers from /h1/DEFS.  Without them seven of their nine cases fail.
    # Replaced wholesale each run, for the reason given above.
    for sub, pick in (("LIB", ("cstart.r", "clibn.l", "math.l", "sys.l")),
                      ("DEFS", None)):
        src_dir = os.path.join(sdk, sub) if sdk else ""
        dst_dir = os.path.join(h1, sub)
        if os.path.isdir(dst_dir):
            shutil.rmtree(dst_dir)
        if not os.path.isdir(src_dir):
            continue
        os.makedirs(dst_dir)
        for f in sorted(os.listdir(src_dir)):
            s = os.path.join(src_dir, f)
            if not os.path.isfile(s):
                continue
            if pick is None and not f.endswith(".h"):
                continue
            if pick is not None and f not in pick:
                continue
            shutil.copyfile(s, os.path.join(dst_dir, f))
    return staged
