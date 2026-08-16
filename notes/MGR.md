# MGR for OS-9: what it was, and where it isn't

Written 2026-08-14, after rdoggett asked whether the collection has MGR.
Short answer: no, and I could not find an OSK build. What follows is the
evidence, so the next person starts further along than I did.

## What MGR is

ManaGeR, by Stephen A. Uhler at Bellcore, 1984, first for the Sun 3.
Presented at USENIX in 1987 as "MGR - a Window System for UNIX".

Its design is the opposite of X11's. Where X splits into a server, a separate
window manager and `xterm`, **MGR is all three in one program**, and clients
drive it by **writing escape sequences to a pseudo-terminal** -- no library to
link, no protocol to speak. Existing programs therefore work unmodified: if it
writes to a tty, it gets a window. Windows carry text, vector graphics and
basic bitmap graphics, plus a message-passing facility so clients can find each
other. The result had a very small memory footprint and asked little of the
graphics hardware, which is why it thrived where X11 starved.

That design is why it matters here: **the programs already on this disk would
run in MGR windows with no rebuild.**

## What we have that touches it

- `CMDS/NETPBM/pbmtomgr` and `mgrtopbm` -- converters for MGR's bitmap format,
  with man pages in `DOC/netpbm`. That is all of MGR that is on the disk.
- **os9exec has the plumbing.** `-x`, `-y`, `-z` and `-g` do not run a window
  system; they publish values into OS-9's system globals for a program inside
  to read -- `D_ScreenW1` at 0x1008, `D_ScreenH1` at 0x100C, `D_IPAddr` at
  0x1014 (`Source/OS9exec_core/fcalls.c`). `network.c` carries the note
  "Several adaptions for Carbon: MGR/telnet are running now". The emulator
  holds the door open; the program that walks through it is what is missing.
- The archive pool's `linkup` source has `kwin2mgr.h`, mapping its window layer
  onto MGR's client calls -- `m_move`, `m_standout`, `m_cleareol`, `m_addline`,
  `m_textregion`, `m_fcolor`. Text operations, because in MGR a window IS a
  terminal.

## Evidence the OS-9 port existed

- Wikipedia lists **OS-9** among MGR's platforms, beside SunOS, Macintosh,
  System V on the AT&T UNIX PC, Ultrix, MiNT on the Atari ST, Coherent, Linux,
  FreeBSD and VSTa.
- The MGR HOWTO: *"Many small, industrial, real-time systems under OS9 or Lynx
  in Europe use (another variant of) Mgr for their user interface."* Note
  **"another variant"** -- the OS-9 one was a derivative, not mainline.
- Best evidence of all, and it survives in the mainline source tree:
  `src/clients/portable/mphoon/makefile.osk` in the MGR sources. It is
  unmistakably OS-9 --

        CC     = cc
        HOME   = /dd
        CFLAGS = -ixt=$(HOME)/TMP -v=$(HOME)/MGR/DEFS -v=$(HOME)/OS9LIB/DEFS
        LDFLAGS= -l=$(HOME)/MGR/LIBS/mgrtrap.l -l=$(HOME)/LIB/os9lib.l -ix
        ODIR   = $(HOME)/MGR/CMDS
        ... chd $(RDIR); attr $(ODIR)/$@ -ape

  So the OS-9 port put headers in `/dd/MGR/DEFS`, clients in `/dd/MGR/CMDS`,
  and its client library in `/dd/MGR/LIBS/mgrtrap.l` -- **a trap module**,
  which is the OS-9-native way to share a library, exactly as `cio` does.

## Where I looked, and did not find it

- **Our own source archive does not have it.** `notes/DOWNLOADS-68k.md` indexes
  all 419 files fetched from the Microware hobbyist archive; nothing matches
  mgr, manager or window. Its `GWINDOWS` category is G-Windows applications
  (Gespac's system) -- blackjack, cyberwar, puzzle, dclock -- not MGR.
- The mainline MGR source tree (4031 files) contains exactly two OS-9 traces,
  both copies of that one `makefile.osk`. No server, no `mgrtrap.l`.
- `ftp://bellcore.com/pub/mgr`, where the pre-Linux ports were archived, is
  described in the HOWTO as already gone, and has no Wayback captures.
- RTSI's OS-9 archive (os9archive.rtsi.com) has Wayback captures only of the
  company's later web site; the file archive itself was never crawled.

## The bigger thing this turned up

**153 of the 419 downloaded archives are missing from the pool.**
`notes/DOWNLOADS-68k.md` records 17 categories fetched "2026-08-02, zero
failures"; the pool directory holds 13. Absent entirely:

    DRIVERS   13 files,  1.1 MB
    EFFO      36 files, 12.8 MB     <- the EFFO forum disks
    GWINDOWS   7 files,  0.2 MB
    NETWORK   20 files,  8.3 MB
    TELECOM   77 files, 11.2 MB

`download.log` in the pool only covers the 13 surviving categories, so these
were fetched in a different pass and not kept. **Everything in `AUDIT-pool.md`
is an audit of 281 files, not 419.** The EFFO forum disks in particular are
where European OS-9 community software lived -- which is exactly the world the
HOWTO says used MGR.

## The five categories were re-fetched, 2026-08-14 -- and MGR is not there

All 152 missing archives recovered from Microware's OS-9 Archive, zero
failures, 35 MB. The pool now holds all 432 files. `tools/refetch_archive.py`
is the fetcher; the archive runs Phoca Download behind a POST form with a
per-session token, so each file's page must be fetched before its download.
Category ids under OSK (98): drivers 105, effo 108, gwindows 122,
network 127, telecom 134.

**MGR is not in any of them.** Across all 6508 members of those 152 archives
(`notes/pool-newcategories-members.txt`) the only matches are traces of it
being *used*, never the thing itself:

| where | what |
|---|---|
| `forum23.lzh` | `f23a/HARDWARE/ATARI/CUMANA/keydef_mgr.a` -- a keyboard-definition module for **Cumana OS-9/68000 V2.1** on the Atari ST, and its whole difference from the plain `keydef.a` is that it fills in the function keys (`OC0`-`OCF`) the other leaves at zero. Somebody wanted F-keys working under MGR. |
| `forum17.lzh` | `SOFTWARE/C/BEAV/.beavrc.mgr` -- a config for the BEAV editor tuned for running in an MGR window. |
| `netpbm_*.lzh` | `mgrtopbm`, `pbmtomgr` -- the format converters we already ship. |
| `forum23.lzh` | `SOFTWARE/SCULPTOR/mgr` -- Sculptor's database *manager*, unrelated. |

So two independent programs in this archive were configured for MGR, on the
Cumana Atari port Wikipedia names -- and the window system itself was never
deposited here. It has to come from somewhere else.

Re-fetching those five categories was the obvious next move, for MGR and for
whatever else is in 34 MB nobody here has opened.

## 2026-08-16 -- why it is not here, from the archive's own paperwork

The client/server split is the right way to think about it: the server owns the
framebuffer and could never run under os9exec, while the clients are ordinary
programs writing an escape stream, which is what a freeware collection would
plausibly carry. So the search was redone against **client** signatures, at
content level, across all 17,413 files of the fully-extracted pool.

**Neither half is here.** Every MGR client-library symbol returns zero:
`m_setmode`, `m_newwin`, `m_selectwin`, `m_ttyset`, `m_clearwin`, `m_flush`,
`ckmgrterm`, `menu_load`, `get_mgrterm`, `MGRLIB`. No `mgr.l`, no `.mgrrc`, no
`mgr` binary. The one `mgr.h` in the pool is netpbm's, and its first line says
what it is: *"the following defs are taken from the MGR header file
lib/dump.h"* -- the bitmap dump format for `mgrtopbm`, not the client library.
The `.fnt` files are KWindows', not MGR's.

### The reason, in the CERN OS-9 newsletter of April 1992

`EFFO/forum22.lzh`, `FORUM22/INFO/cern_92.04`, under the heading **Commercial**:

> 'MGR', Spectralab, 92
> The window package available for OS-9, Lynx-OS, MS-DOS, UNIX which has all
> the functions you would hope for. The documentation contains a lot of
> examples.

and earlier in the same issue:

> MGR : Spectralab are offering a one day course on this software product,
> which they demonstrated at CERN. The price is 800sf and the dates are
> May 22 and June 26th.

**The OS-9 MGR was a commercial product, sold by Spectralab, with a paid
training course.** That is why a freeware archive does not have it. It is a
licence question, not a technical one. Bellcore's original MGR was
freely distributable; the OS-9 port was somebody's product.

### One named client, catalogued but never distributed

EFFO's `soft_list` -- carried on forums 16, 17, 20, 21, 22 and 23 -- has
exactly one MGR entry:

    Program name : PERF                        Class : UTILITY
    Description  : graphical performance display
    Hardware     : ATARI
    Where        : B. Stotz ETH
    > displays cpu load and free memory on a mgr window
    > !!!!runs only on the mgr window system!!!!!

Note the `Where:` field. Other entries say "EFFO Forum 6"; this one names the
author, meaning EFFO catalogued it but did not carry it. `perf` appears nowhere
in the pool, by filename or module name.

`soft_list` also names distribution channels we do not hold at all -- an
**"OS9 Pool"** appears against eight entries -- and `cern_91.2` mentions a
zterm terminal file extended to include vt320, **mgr** and cumana.

### What would actually work

**If any part of MGR turns up, keep it.** An earlier draft of this page argued
the server was useless because os9exec cannot run it. That is the same reasoning
that once excluded the MM/1 drivers, and it was wrong for the same reason: this
collection is not only for people running the emulator. Somebody with a VME
board or an Atari with the right hardware is exactly who a preserved server
would be for. Clients, server, fonts, `PERF` -- all worth having if found, on
the usual licence terms.

Nothing in this collection can exercise MGR today, because no client of any
kind survives here. The route that remains is to build MGR's clients from the
GitHub sources for OS-9 with Microware `cc`, run the X11 server on the host,
and connect an os9exec `/tN` pty to it. That is a sound test of the SCF
terminal path -- but it produces NEW software, not preserved software, and
belongs in `tools/` or a demo, not in the collection as community freeware.

