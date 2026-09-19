#!/usr/bin/env python3
"""Write the collection as a ustar archive for the disk's own `tar` to extract.

This is half of a build that uses NO Microware utility. `mkimage.sh` creates a
blank image with os9exec's `mount -k`, then runs the collection's own `tar`
(GNU tar 1.10, unstarred -- it needs no `cio`) to populate it. Nothing else on
the disk can do the job: `cp` and `mkdir` are both starred, so they need the
very `cio` we are trying not to depend on.

The archive carries the ATTRIBUTES the finished disk should have, because tar
sets them from the mode bits as it extracts. That removes the separate `attr`
pass the old build needed:

    OS-9 module (4AFC magic)  0555  ->  e+pe+r+pr, not writable
    everything else           0666  ->  r+w+pr+pw, no execute
    directory                 0777  ->  d+e+w+r+pe+pw+pr

DATA FILES ARE PUBLICLY WRITABLE, and the "publicly" is the whole point.
Everything on this disk is owned by 0.0, because tar writes uid 0 and an RBF
file descriptor keeps the owner it was created with. A person logged in as
anybody else -- 1.3, say -- is therefore never the owner of anything here,
so the OWNER write bit does nothing for them and only the PUBLIC one counts.

Shipping data 0444 meant every file a game has to update was read-only:
sokoban's sok.score, larn's .lscore12.0, hack's record and bones files,
cribbage's criblog, wanderer's hiscore, the SAVES trees. As 0.0 you never
see it -- RBF gives the super-user a software bypass, so the write just
works and the disk looks fine. Log in as yourself and sokoban stops with
"cannot open score file". That is the bug this mode fixes, and it is why
testing as 0.0 could not find it.

A DIRECTORY MUST BE WRITABLE or the programs that create files in it fail --
advent writes glorkz into GAMES/ADV, larn its scoreboard, and 35 programs use
/dd/tmp. 0555 here made every directory read-only, which the old `makdir`
build never did: it left them d-ewrewr. The symptom is a program that refuses
to save, and it does not depend on who you are logged in as; not even 0.0 can
write to a directory with no w bit.

Two things that are easy to get wrong:

  * DIRECTORIES ARE EMITTED EXPLICITLY, parent before child. tar creates
    missing parents on its own, but only for a directory that contains a
    file. That is not enough on its own either -- the tar on this disk
    creates a TOP-LEVEL directory entry but silently skips a NESTED empty
    one, so `A/` appears and `A/B/` does not. The collection currently has
    no empty directory, so nothing trips it; if one is ever added, it will
    vanish from the image without a word.

  * EVERY VARYING FIELD IS PINNED -- fixed mtime, uid/gid 0, sorted order --
    so two runs produce byte-identical output. Git does not record mtimes,
    so taking them from the working tree would make a CI build differ from a
    local one for no reason at all.

ustar caps a path at 100 characters. The longest here is 51, so the limit is
not close; the check stays in because exceeding it silently truncates.
"""
import os, sys, tarfile

MODULE_MAGIC = b"\x4a\xfc"
MODE_MODULE, MODE_DATA, MODE_DIR = 0o555, 0o666, 0o777


def is_command(path):
    """Is this a COMMAND that is not an OS-9 module?

    Everything under CMDS is a command by definition -- DOC/INDEX names them
    all and check_disk.py enforces it -- but two of them are shell PROCEDURE
    FILES rather than modules: `who' and `mscheck'. The module test alone gave
    those 0666, no execute bit, so they shipped as data and could not be run
    at all. rdoggett found it from the outside on 2026-08-27: "/h0/cmds/who
    isn't even executable".

    Keyed off the directory, not the content: a procedure file has no magic
    number to test for, and guessing from the first bytes would be the same
    class of proxy this collection keeps getting wrong.
    """
    parts = os.path.normpath(path).split(os.sep)
    if "CMDS" not in parts:
        return False
    # CMDS/archives is the ONE place under CMDS that holds data: the .lzh
    # source archives for ed, elvis, grep and friends. DOC/INDEX does not
    # count them as commands and neither does check_disk.py, and marking them
    # executable would also take away the public write bit every data file on
    # this disk is supposed to keep.
    if "archives" in parts:
        return False
    return not os.path.basename(path).startswith(".")
MTIME    = 1785801600      # 2026-08-04T00:00:00Z -- any fixed instant will do
USTAR_MAX = 100


# Shell PROCEDURE FILES that live outside CMDS and still have to be runnable.
# Keyed by path, not by a mode bit on the host copy: 38 files under disk/
# carry a stray execute bit from whatever archive they were unpacked out of
# (every DOC/bix/B_* and a handful of headers), so the host bit says nothing
# about intent. utree's Backup command runs the program its BACKUP variable
# names and this collection is where that program comes from; ksh answers
# "cannot execute" for a script without the bit, whether it is run by name or
# handed to ksh as an argument.
EXECUTABLE_DATA = frozenset({
    "SYS/UTREE/utree.backup",
})


def is_executable_data(path, root):
    """Is this one of the runnable scripts that live outside CMDS?"""
    rel = os.path.relpath(path, root).replace(os.sep, "/")
    return rel in EXECUTABLE_DATA


def is_module(path):
    """True if the file begins with the OS-9 module magic 4AFC."""
    with open(path, "rb") as f:
        return f.read(2) == MODULE_MAGIC


def entry(name, mode, typeflag, size=0):
    """A TarInfo with every field that could vary between runs pinned."""
    info = tarfile.TarInfo(name)
    info.mode, info.type, info.size, info.mtime = mode, typeflag, size, MTIME
    info.uid = info.gid = 0
    info.uname = info.gname = ""
    return info


def survey(src):
    """Return (dirs, files) relative to src, each sorted parent-before-child."""
    dirs, files = [], []
    for root, dnames, fnames in os.walk(src):
        dnames.sort()
        rel = os.path.relpath(root, src)
        if rel != ".":
            dirs.append(rel)
        files.extend(os.path.join(rel, f) if rel != "." else f
                     for f in sorted(fnames))
    return sorted(dirs), sorted(files)


def build(src, out):
    """Write src to out as ustar. Returns (ndirs, nfiles, nmodules)."""
    dirs, files = survey(src)

    # A stale entry here would ship a data file as a program, or -- worse and
    # quieter -- leave a renamed script unrunnable with nothing saying so.
    have = {f.replace(os.sep, "/") for f in files}
    missing = sorted(EXECUTABLE_DATA - have)
    if missing:
        raise SystemExit("EXECUTABLE_DATA names files that are not in the "
                         "tree: %s" % ", ".join(missing))

    too_long = [p for p in dirs + files if len(p) > USTAR_MAX]
    if too_long:
        raise SystemExit("paths exceed the %d-char ustar limit: %s"
                         % (USTAR_MAX, ", ".join(too_long[:3])))

    modules = 0
    with tarfile.open(out, "w", format=tarfile.USTAR_FORMAT) as tar:
        for d in dirs:
            tar.addfile(entry(d, MODE_DIR, tarfile.DIRTYPE))
        for f in files:
            full = os.path.join(src, f)
            mod  = is_module(full)
            modules += mod
            info = entry(f, MODE_MODULE
                         if (mod or is_command(full)
                             or is_executable_data(full, src))
                         else MODE_DATA,
                         tarfile.REGTYPE, os.path.getsize(full))
            with open(full, "rb") as fh:
                tar.addfile(info, fh)

    return len(dirs), len(files), modules


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: mktar.py <source-tree> <out.tar>")
    src, out = sys.argv[1], sys.argv[2]
    if not os.path.isdir(src):
        raise SystemExit("no such tree: %s" % src)
    nd, nf, nm = build(src, out)
    print("  %d dirs, %d files (%d modules, %d data), %d bytes"
          % (nd, nf, nm, nf - nm, os.path.getsize(out)))
