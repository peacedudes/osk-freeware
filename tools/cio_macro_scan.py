#!/usr/bin/env python3
"""cio_macro_scan.py -- list OS-9/68k programs that can storm F$SRqMem.

Contributed by the os9exec session, 2026-08-31, with the root cause it found.

THE DEFECT.  Every `cio` trap module we have implements trap-13 selector $41
as the raw memory ALLOCATOR and $42 as the raw free.  The LIB/cio.l these
binaries were linked against defines $41 = _flshbuf(FILE*, c) and
$42 = _filbuf(FILE*).  So the inline putc/getc MACRO slow path hands cio a
FILE POINTER where a byte count belongs.  The allocator succeeds, the FILE's
ptr/end are never advanced, the next character takes the slow path again, and
the program leaks one chunk per character until the 68k arena is exhausted.
Programs that use printf/fprintf/fwrite/read/write are unaffected: those run
inside the module and never cross the broken selectors.

WHAT COUNTS.  Presence of the $41/$42 STUB is NOT the criterion -- the linker
pulls in the whole 69-stub cio.l psect, so clean programs (autolf) carry stubs
they never call.  The criterion is a BSR/BRA from the program's own code TO
that stub.

WHY THERE IS NO REACHABILITY FILTER.  Tried and discarded: a call site inside
a function nothing calls cannot fire, but the call graph cannot be recovered
here -- cstart dispatches with an indexed PC-relative `jsr` (`4EBB 0800`), so
a BFS from M$Exec reaches nothing and reports every site dead, including
logisim's and cvtbase's, which are known to fire.  The result below is
therefore an UPPER bound: a site only storms if it is reached.  Confirm by
running the listed programs and watching for an F$SRqMem whose d0 is wildly
larger than the module's own M$Mem+M$Stack -- that request IS the FILE
pointer, and it appears on the first character, long before the arena dies.

    tools/cio_macro_scan.py disk          # 353 cio programs, 41 with a site
"""
import os
import re
import struct
import sys


def u16(d, i):
    return struct.unpack('>H', d[i:i + 2])[0]


def u32(d, i):
    return struct.unpack('>I', d[i:i + 4])[0]


def branch_target(d, i):
    w = u16(d, i)
    if w in (0x6100, 0x6000):                                  # bsr.w / bra.w
        return i + 2 + struct.unpack('>h', d[i + 2:i + 4])[0]
    if (w >> 8) in (0x61, 0x60) and (w & 0xFF) not in (0x00, 0xFF):
        return i + 2 + struct.unpack('>b', d[i + 1:i + 2])[0]   # bsr.s / bra.s
    if w == 0x4EBA:                                            # jsr d16(pc)
        return i + 2 + struct.unpack('>h', d[i + 2:i + 4])[0]
    return None


def scan(path):
    """-> (is_cio_program, sites_calling_$41, sites_calling_$42) or None."""
    try:
        d = open(path, 'rb').read()
    except OSError:
        return None
    if len(d) < 0x50 or d[0:2] != b'\x4A\xFC':                 # M$ID
        return None
    if (u16(d, 0x12) >> 8) != 0x01:                            # program module
        return None
    if b'cio traphandler mismatch' not in d:                   # cio, not csl
        return None
    size = min(u32(d, 4), len(d))
    code_end = min(u32(d, 0x40) or size, size)                 # stop at M$IData

    stub = {}
    for m in re.finditer(b'\x4E\x4D', d[:code_end]):           # TRAP #13
        i = m.start()
        if i + 4 <= code_end and u16(d, i + 2) in (0x41, 0x42):
            stub[i] = u16(d, i + 2)
    n = {0x41: 0, 0x42: 0}
    if stub:
        for i in range(0, code_end - 3, 2):
            if branch_target(d, i) in stub:
                n[stub[branch_target(d, i)]] += 1
    return (True, n[0x41], n[0x42])


def survey(roots):
    total, rows = 0, []
    for root in roots:
        for dp, _, fn in os.walk(root):
            if os.path.basename(dp) == 'archives':
                continue
            for f in sorted(fn):
                p = os.path.join(dp, f)
                r = scan(p)
                if r is None:
                    continue
                total += 1
                if r[1] or r[2]:
                    rows.append((os.path.relpath(p, root), r[1], r[2]))
    return total, rows


def main(roots):
    total, rows = survey(roots or ['.'])
    print("cio-linked program modules: %d" % total)
    print("with a putc/getc macro call site: %d" % len(rows))
    for name, a, b in sorted(rows, key=lambda x: -(x[1] + x[2])):
        print("  %-28s _flshbuf=%-3d _filbuf=%d" % (name, a, b))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
