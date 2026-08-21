#!/usr/bin/env python3
"""Screen candidate files for Microware intellectual property before adding anything.

OS-9 is Microware's and is still a product they sell. Their utilities, headers,
libraries and system source may not be redistributed. Freeware archives from
the period are NOT clean by default: people copied a DEFS file into their own
package all the time, and an EFFO public-domain disk carried a lightly-edited
copy of Microware's own `oskdefs.d` -- caught on 2026-08-19 only because the
typo in its header comment ("resrtictions") survived the edit.

So a candidate is screened four ways, cheapest first:

  NAME      its basename matches a file in the SDK
  CONTENT   its lines overlap an SDK file's heavily, whatever it is called
  CLAIM     it carries a Microware copyright or ownership string
  KIND      it is a file type only Microware is included (.l libraries, DEFS .d/.h)

NAME alone is weak -- `makefile` and `math.h` collide with everything. CONTENT
is the one that catches a renamed or lightly-edited copy, and it is why this
compares text rather than hashes.

  tools/screen_microware.py <path>...        one line per file
  tools/screen_microware.py -q <path>...     only the ones that flag

Exit status is 1 if anything flagged, so it can gate an install.
"""
import hashlib
import os
import re
import sys

import paths

# Overlap above this fraction of the candidate's distinct lines reads as a copy
# rather than a coincidence. Set from the oskdefs.d case: 35 of its ~50 lines
# matched Microware's, which is 0.70. Two unrelated assembly files share far
# less -- blank lines and comment banners are stripped before counting.
COPY_THRESHOLD = 0.45
MIN_LINES = 8          # below this, line overlap means nothing
MIN_BYTES = 64         # below this, an identical hash is a coincidence

# An OWNERSHIP assertion, not a mention. Freeware source says "Microware" all
# the time -- "compiled with Microware C", "OS9/68000" banners -- and matching
# a bare mention flagged 30 files that merely name the compiler they were built
# with. Require a word of ownership next to the name.
CLAIM = re.compile(
    rb"(copyright[^\n]{0,40}microware"
    rb"|microware[^\n]{0,40}(?:corporation|systems|all rights reserved)"
    rb"|property\s+of\s+microware"
    rb"|licensed[^\n]{0,30}microware)", re.I)

# Extensions Microware is included and freeware generally does not.
MICROWARE_KINDS = {".l": "linkable library", ".d": "assembler defs"}

# Microware runtime modules BY NAME, because they turn up loose inside other
# people's archives: a 14,572-byte `fpu' was found bundled in TELECOM's
# STerm68k package, a different build from the SDK's 12,848-byte copy, so
# neither hashing nor line-overlap would have caught it.
#
# cio, csl, csl020, math and math881 are NOT here: Microware gave permission
# for exactly those five and they already ship in disk/CMDS. Everything else
# of theirs is still theirs.
MICROWARE_MODULES = {
    "fpu": "floating-point emulator", "fpu040": "floating-point emulator",
    "cio020": "C I/O trap handler", "p2init": "system extension installer",
    "sysgo": "system startup", "os9p1": "kernel part 1",
    "os9p2": "kernel part 2", "init": "system init module",
    "rbf": "RBF file manager", "scf": "SCF file manager",
    "pipeman": "pipe file manager", "sbf": "SBF file manager",
    "ioman": "I/O manager", "clock": "system clock module",
}

# SOURCE is the category that actually matters, and this is why: Microware's
# concern is not lost licence revenue, it is that infrastructure in Japan and
# Germany runs OS-9/68k TODAY and published source could expose vulnerabilities
# nobody has found yet (rdoggett, 2026-08-19). That is also why permission for
# cio/csl/math was straightforward -- those are runtime BINARIES and expose
# nothing. So a Microware binary in an archive is merely their property; a
# Microware SOURCE file, especially system internals, is the one that could
# hurt somebody. These markers name the internals.
SOURCE_EXT = (".c", ".a", ".asm", ".s", ".h", ".d", ".mk")

# NAMED OS-9 internals, not a pattern. A first attempt matched /V_[A-Z]+/ and
# /D_[A-Z]+/ case-insensitively and flagged 30 innocent files: Tetris's
# V_TYPE, Phantasia's D_BEYOND, and POSIX's own d_name. A regex over that
# shape cannot tell a device driver's static storage from a game's enum, so
# these are the actual symbols, case-sensitive, and TWO distinct ones are
# required before anything is said.
SYSTEM_SYMBOLS = (
    # system globals (D_ prefix in Microware's sysglob)
    "D_ModDir", "D_PrcDBT", "D_Clock", "D_TotRAM", "D_MinPty", "D_SysPrc",
    "D_Slice", "D_ModEnd", "D_BlkMap", "D_SysDis", "D_UsrDis", "D_Init",
    "D_IRQ", "D_Poll", "D_DevTbl", "D_PolTbl", "D_SysMem", "D_SysStk",
    # path descriptor
    "PD_PD", "PD_MOD", "PD_CNT", "PD_DEV", "PD_CPR", "PD_RGS", "PD_BUF",
    "PD_FST", "PD_DTB", "PD_OPT",
    # device static storage a driver defines
    "V_PORT", "V_LPRC", "V_BUSY", "V_WAKE", "V_USER", "V_STAT", "V_NDRV",
    "V_PATHS", "V_DRIVEX",
    # privileged system calls and psect kinds
    "F$SetSys", "F$AllRAM", "F$AllPrc", "F$VModul", "F$SSvc", "F$IODel",
    "ModSub", "ModTrap", "ModDrivr", "ModFlMgr", "ModSystm",
    # the defs files themselves
    "os9defs", "systype.d", "sysglob", "iodefs",
)
SYSTEM_SOURCE = re.compile(
    b"(" + b"|".join(re.escape(x.encode()) for x in SYSTEM_SYMBOLS) + b")")


def norm_lines(path):
    """Distinct, meaningful lines of a text file; empty set if binary."""
    try:
        raw = open(path, "rb").read()
    except OSError:
        return set()
    if b"\0" in raw[:4096]:
        return set()
    text = raw.decode("latin-1").replace("\r\n", "\n").replace("\r", "\n")
    out = set()
    for line in text.split("\n"):
        line = line.strip()
        if len(line) < 4 or set(line) <= set("*=-# "):
            continue
        out.add(line)
    return out


def sdk_index():
    """Microware's OWN files, indexed by basename and by content lines."""
    # ONLY the directories Microware actually is included. `play/oskBoot` is a
    # WORKING disk: its SRC/ and USR/ hold this project's own repairs (the
    # GNU fileutils `ls` build, the `rob` game) plus loose scratch files, and
    # indexing those made the screener report our own work as Microware's --
    # 60 false positives, every one of them 100% "identical".
    roots = [os.path.join(paths.SDK, d) for d in ("CMDS", "DEFS", "LIB")]
    roots.append(paths.SDK_FULL)
    # ...minus the per-account directories this project made INSIDE the SDK's
    # CMDS. CLAUDE/ and SHARE/ are ours (CLAUDE.md's "personal execution
    # directory inside the shared CMDS"), and indexing them reported our own
    # files as Microware's.
    # oskBoot/SYS is excluded outright for the same reason: its HELP directory
    # holds 33 .hlp files named for FREEWARE programs (effo, gshell, tar, the
    # unaxcess BBS) which this project installed there. Microware's own SDK
    # tree has exactly one. Indexing it accused us of copying our own docs.
    ours = ("/CLAUDE/", "/SHARE/", "/ALICE/")
    by_name, texts, digests = {}, [], {}
    for root in roots:
        if not os.path.isdir(root):
            continue
        for dirpath, _dirs, files in os.walk(root):
            if any(o in dirpath + "/" for o in ours):
                continue
            for name in files:
                p = os.path.join(dirpath, name)
                by_name.setdefault(name.lower(), []).append(p)
                try:
                    raw = open(p, "rb").read()
                except OSError:
                    continue
                # An empty file hashes like every other empty file, and both
                # SDKs have several. Matching one is not evidence of anything.
                if len(raw) >= MIN_BYTES:
                    digests[hashlib.sha1(raw).hexdigest()] = p
                lines = norm_lines(p)
                if len(lines) >= MIN_LINES:
                    texts.append((p, lines))
    return by_name, texts, digests


def provenance(sdk_path):
    """Say which SDK a match came from, because they are not equal evidence.

    `paths.SDK` is rdoggett's WORKING build overlay. Beside Microware's own
    files it carries libraries this collection built or collected --
    `ncurses.l`, `libgcc.l`, `libgpp.l`, `unet.l` and the `os9unix/` headers
    are in it and in NEITHER pristine SDK. A file matching one of those is
    matching OUR OWN work, and reporting it as "IDENTICAL to SDK" is how a
    screen teaches people to stop reading it: run this over `disk/LIB` and it
    flags 113 files, nearly all self-matches.

    So a match under the pristine tree is evidence, and a match found only in
    the overlay is a question. Say which.
    """
    if paths.SDK_FULL in sdk_path:
        return ""
    rel = os.path.relpath(sdk_path, paths.SDK)
    twin = os.path.join(paths.SDK_FULL, rel)
    if os.path.exists(twin):
        return ""
    return "  [build overlay only -- may be OUR file, check before acting]"


# The five Microware GAVE PERMISSION FOR, 2026-08-16. They are Microware's and
# they will match the SDK exactly -- that is expected and is not a finding.
# Saying so here stops a later pass "fixing" it by deleting them.
PERMITTED = {"cio", "csl", "csl020", "math", "math881"}


def screen(path, by_name, texts, digests):
    """Return a list of reasons this file looks like Microware's, or []."""
    reasons = []
    base = os.path.basename(path)
    if os.path.splitext(base)[0].lower() in PERMITTED:
        return []

    try:
        raw = open(path, "rb").read()
    except OSError:
        return ["unreadable"]

    d = hashlib.sha1(raw).hexdigest()
    if len(raw) >= MIN_BYTES and d in digests:
        reasons.append(f"IDENTICAL to SDK {os.path.relpath(digests[d], paths.OS9)}"
                       + provenance(digests[d]))

    if base.lower() in by_name:
        reasons.append(f"name matches SDK {os.path.basename(by_name[base.lower()][0])}")

    if CLAIM.search(raw):
        hit = CLAIM.search(raw).group(0).decode("latin-1", "replace")
        reasons.append(f"claims: {hit!r}")

    stem = os.path.splitext(base)[0].lower()
    if stem in MICROWARE_MODULES:
        reasons.append(f"NAMED MICROWARE MODULE: {MICROWARE_MODULES[stem]}"
                       " -- permission covers only cio, csl, csl020, math, math881")

    ext = os.path.splitext(base)[1].lower()
    if ext in MICROWARE_KINDS:
        reasons.append(f"file kind: {MICROWARE_KINDS[ext]}")

    if ext in SOURCE_EXT:
        hits = {m.group(0).decode("latin-1") for m in SYSTEM_SOURCE.finditer(raw)}
        if len(hits) >= 2:
            reasons.append("SYSTEM SOURCE: names "
                           + ", ".join(sorted(hits)[:4])
                           + " -- read this one yourself")

    mine = norm_lines(path)
    if len(mine) >= MIN_LINES:
        best, best_p = 0.0, None
        for p, theirs in texts:
            shared = len(mine & theirs)
            if shared:
                frac = shared / len(mine)
                if frac > best:
                    best, best_p = frac, p
        if best >= COPY_THRESHOLD:
            reasons.append(
                f"{best:.0%} of its lines are in SDK {os.path.basename(best_p)}"
                + provenance(best_p))
    return reasons


def main(argv):
    quiet = argv and argv[0] == "-q"
    if quiet:
        argv = argv[1:]
    if not argv:
        sys.exit(__doc__.strip().splitlines()[0])

    files = []
    for a in argv:
        if os.path.isdir(a):
            for dirpath, _d, fs in os.walk(a):
                files.extend(os.path.join(dirpath, f) for f in sorted(fs))
        else:
            files.append(a)

    by_name, texts, digests = sdk_index()
    print(f"# screened against {len(digests)} SDK files", file=sys.stderr)

    flagged = 0
    for f in files:
        reasons = screen(f, by_name, texts, digests)
        if reasons:
            flagged += 1
            print(f"FLAG  {f}\n        {'; '.join(reasons)}")
        elif not quiet:
            print(f"ok    {f}")
    print(f"\n{flagged} of {len(files)} flagged", file=sys.stderr)
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
