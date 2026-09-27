#!/usr/bin/env python3
"""Let ELM's filter read back the temp file it wrote, so `save' works.

    patch_filter_pid.py <disk-dir>            report only
    patch_filter_pid.py <disk-dir> --apply    write it

save_message() in FILTER/actions.c of the ELM 2.4 tree this binary was
built from (SRC/infoxpress/BNU/ELM_2.4) sets `filter_pid = getpid()'
inside the `#ifndef OSK' fork-for-group block, so on OSK the local
reaches save_to_folder() uninitialised.  filter writes its copy of the
message as /r0/filter.<pid> and then opens /r0/filter.<stack rubbish>:
"can't open temp file /r0/filter.26048 for reading!" -- measured
2026-09-20, written filter.3.  The source has carried the one-line fix
since then (the assignment moved above the #ifndef); this is the same
fix in the binary, which already carries two other patches and so is
patched rather than rebuilt.

  CMDS/ELM/filter  save_message(), the call `save_to_folder(foldername,
                   filter_pid)' at 0x8aa:

      old  move.l 16(a7),d1        load the uninitialised local
           move.l 28(a7),d0        foldername
           bsr.s  save_to_folder
           move.l d0,(a7)          ret = ...
           move.l (a7),d0          ... and load it straight back
      new  jsr    -28160(a6)       getpid(), the call main's own
                                   sprintf of the temp name makes
           move.l d0,d1
           move.l 28(a7),d0
           bsr.s  save_to_folder
           move.l d0,(a7)          d0 already holds ret

Fourteen bytes; the redundant reload pays for the two the call needs.
Both branches into the sequence land on its first byte, unchanged.
Module header untouched; the CRC is recomputed.  Same shape as
tools/patch_elm_linefeed.py.
"""
import os
import sys

PATCHES = {
    "CMDS/ELM/filter": [(0x8aa, bytes.fromhex("222f0010202f001c61122e802017"),
                         bytes.fromhex("4eae92002200202f001c61102e80"))],
}


def crc24(data):
    acc = 0xFFFFFF
    for b in data:
        acc ^= b << 16
        for _ in range(8):
            acc <<= 1
            if acc & 0x1000000:
                acc ^= 0x800063
        acc &= 0xFFFFFF
    return acc ^ 0xFFFFFF


def patch(path, edits, apply):
    d = bytearray(open(path, "rb").read())
    size = int.from_bytes(d[4:8], "big")
    if crc24(bytes(d[:size - 3])) != int.from_bytes(d[size - 3:size], "big"):
        return "%s: CRC already bad -- left alone" % path
    if all(d[at:at + len(new)] == new for at, old, new in edits):
        return "%s: already patched" % path
    for at, old, new in edits:
        if d[at:at + len(old)] != old:
            return ("%s: bytes at 0x%x are %s, not %s -- a different binary"
                    % (path, at, d[at:at + len(old)].hex(), old.hex()))
    if not apply:
        return "%s: would patch %s" % (path, ", ".join("0x%x" % e[0] for e in edits))
    for at, old, new in edits:
        d[at:at + len(new)] = new
    d[size - 3:size] = crc24(bytes(d[:size - 3])).to_bytes(3, "big")
    open(path, "wb").write(d)
    e = open(path, "rb").read()
    ok = crc24(e[:size - 3]) == int.from_bytes(e[size - 3:size], "big")
    return "%s: patched, CRC %s" % (path, "ok" if ok else "VERIFY FAILED")


def main(argv):
    root, apply = argv[0], "--apply" in argv
    for rel, edits in PATCHES.items():
        print(patch(os.path.join(root, rel), edits, apply))


if __name__ == "__main__":
    main(sys.argv[1:])
