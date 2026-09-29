#!/usr/bin/env python3
"""Where the things this repository builds WITH, but does not contain, live.

Rebuilding programs needs an OS-9 SDK, and screening candidate files for
Microware material wants a pristine copy of one to compare against.  Neither
ships here.  This module is the single place that knows where they are, and
each location can be overridden from the environment.

Each accessor FAILS LOUDLY when the directory is not there.  That is
deliberate: a tool that quietly finds nothing reports "nothing found" and is
believed.

    OS9_HOME          the directory holding the rest  (default ~/Developer/os9)
    OS9SDK            the SDK the rebuilds use       (default $OS9_HOME/play/oskBoot)
    OS9SDK_PRISTINE   an untouched SDK, for provenance (default
                      $OS9_HOME/Scraped/sdk-copyrighted/OS9)
    OS9EXEC_DIR       an os9exec checkout            (default $OS9_HOME/os9exec)
"""
import os
import sys

OS9 = os.environ.get("OS9_HOME") or os.path.expanduser("~/Developer/os9")

# The SDK.  Build with it; nothing from it ships except the runtime modules
# Microware gave permission for, which are already in disk/CMDS.
SDK = os.environ.get("OS9SDK") or f"{OS9}/play/oskBoot"

# An untouched SDK.  The one above is a working build overlay and carries
# this collection's own libraries beside Microware's, so only this one
# settles whether a file is Microware's.
SDK_FULL = os.environ.get("OS9SDK_PRISTINE") or f"{OS9}/Scraped/sdk-copyrighted/OS9"

EMULATOR = os.environ.get("OS9EXEC_DIR") or f"{OS9}/os9exec"


def _resolve(path, env_var, what):
    """Return an existing directory, or exit with a message naming the fix."""
    if not os.path.isdir(path):
        sys.exit(f"{sys.argv[0]}: no {what} at {path}\n"
                 f"  set {env_var} to point at it (see tools/paths.py)")
    return path


def sdk():
    """The OS-9 SDK used for rebuilding.  Never shipped."""
    return _resolve(SDK, "OS9SDK", "OS-9 SDK")


def sdk_pristine():
    """An untouched SDK, for deciding what is Microware's."""
    return _resolve(SDK_FULL, "OS9SDK_PRISTINE", "pristine OS-9 SDK")


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
    for name, fn in (("sdk", sdk), ("pristine sdk", sdk_pristine),
                     ("os9exec", os9exec), ("repo", repo)):
        print(f"  {name:14} {fn()}")
