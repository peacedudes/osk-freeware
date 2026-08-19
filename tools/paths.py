#!/usr/bin/env python3
"""Where the material this collection was built from actually lives.

Every tool that reads the archive pool got its own hardcoded copy of the path,
and on 2026-08-18 all eight broke at once when the material moved out of
`~/mine` -- which is now off limits entirely, by rdoggett's instruction. This
module is the single place that knows, so the next move costs one edit.

Each accessor takes an environment override and FAILS LOUDLY when the
directory is not there. That is deliberate and it is the whole point: this
collection has produced a verifier that reported 20/20 OK having run nothing,
and a builder that reported 3287/3287 copies while every copy failed. A tool
that quietly finds an empty pool reports "nothing missing" and is believed.

Usage:

    from paths import pool, sdk, manuals
    for category in os.listdir(pool()):
        ...
"""
import os
import sys

OS9 = "/Users/rdoggett/Developer/os9"

# The pool proper: 465 files across 18 category directories, plus download.log.
POOL = f"{OS9}/Scraped/os9/PUBCMDS/microware-archive"

# 32 further 68k archives and the 512 files already extracted from them. Not
# part of the pool and not covered by any audit note as of 2026-08-18.
EXTRA_ARCHIVES = f"{OS9}/Scraped/os9/PUBCMDS/68k"
EXTRA_UNPACKED = f"{OS9}/Scraped/os9/PUBCMDS/68k_unpacked"

# 65 OS-9 `ar` archives -- the usenet ones DOC/ORIGINS cites by name -- plus
# loose C sources under ARR/x. Found 2026-08-19; no note mentioned this tree.
USENET_AR = f"{OS9}/play/h4/ARR"

# Microware's own manuals. HERE TO ANSWER QUESTIONS, NEVER TO BE COPIED ONTO
# THE DISK: they are Microware's, and OS-9 is a product they still sell.
MANUALS_PDF = f"{OS9}/Scraped/os9/resources"
MANUALS_TXT = f"{OS9}/Scraped/os9/txtResources"

# The SDK. Build with it; nothing from it ships except the five runtime
# modules Microware gave permission for, which are already in disk/CMDS.
SDK = f"{OS9}/play/oskBoot"
SDK_FULL = f"{OS9}/Scraped/sdk-copyrighted/OS9"

EMULATOR = f"{OS9}/os9exec"


def _resolve(default, env_var, what):
    """Return an existing directory, or exit with a message naming both tries.

    `env_var` wins when set, so a tool can be pointed at a copy without an
    edit. Absence is fatal rather than empty: see this module's docstring.
    """
    path = os.environ.get(env_var) or default
    if not os.path.isdir(path):
        sys.exit(
            f"{sys.argv[0]}: no {what} at {path}\n"
            f"  set {env_var} to point at it, or see tools/paths.py.\n"
            f"  NOTE: ~/mine is off limits -- the material moved to {OS9} on 2026-08-18."
        )
    return path


def pool():
    """The archive pool: 18 category directories of original archives."""
    return _resolve(POOL, "OSK_POOL", "archive pool")


def extra_archives():
    """The 68k archive tree that sits beside the pool."""
    return _resolve(EXTRA_ARCHIVES, "OSK_EXTRA", "68k archive tree")


def extra_unpacked():
    """Files already extracted from the 68k archives."""
    return _resolve(EXTRA_UNPACKED, "OSK_EXTRA_UNPACKED", "unpacked 68k tree")


def usenet_ar():
    """The usenet `ar` archives DOC/ORIGINS names as a source."""
    return _resolve(USENET_AR, "OSK_USENET_AR", "usenet ar archives")


def manuals(text=True):
    """Microware's manuals -- text by default, PDF on request."""
    return (_resolve(MANUALS_TXT, "OSK_MANUALS_TXT", "manuals as text") if text
            else _resolve(MANUALS_PDF, "OSK_MANUALS_PDF", "manuals as PDF"))


def sdk():
    """The OS-9 SDK used for rebuilding. Never shipped."""
    return _resolve(SDK, "OSK_SDK", "OS-9 SDK")


def os9exec():
    """The emulator binary itself, not its directory."""
    d = _resolve(EMULATOR, "OS9EXEC_DIR", "os9exec checkout")
    binary = os.path.join(d, "os9exec")
    if not os.access(binary, os.X_OK):
        sys.exit(f"{sys.argv[0]}: {binary} is not executable")
    return binary


def repo():
    """This repository, derived from where this file sits."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


if __name__ == "__main__":
    for name, fn in (("pool", pool), ("extra archives", extra_archives),
                     ("extra unpacked", extra_unpacked), ("usenet ar", usenet_ar),
                     ("manuals (text)", manuals), ("sdk", sdk),
                     ("os9exec", os9exec), ("repo", repo)):
        print(f"  {name:18} {fn()}")
