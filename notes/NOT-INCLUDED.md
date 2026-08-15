# What was left out of the collection, and why

Every exclusion in one place, for review. Written 2026-08-13 while working the
archive pool (`notes/AUDIT-pool.md`); it supersedes nothing, it just gathers
what was scattered across `SOURCES.txt` and the audit into a list you can
disagree with line by line.

**Nothing here is a permanent judgement.** Several entries changed sides
already: `lua` was excluded for two years on a rule this disk contradicts 128
times over, and the vendor demos were excluded on a policy nobody had written
a reason for.

## Held for your decision

*(empty — `auxlib` was the only entry and is now included; see SOURCES.txt)*

## Excluded on the owner's terms

| | |
|---|---|
| `tshell` | Its readme states *"NOT Public Domain, but its free for private use"* — the author's own restriction, and the clearest case on this list. |

## Excluded as duplicates of what already ships

The bar here is **byte-identical, or the same program under another name**.
A different build or an older edition is NOT a reason — those now live in
`CMDS/REBUILT`, which exists precisely so alternates can sit beside the
curated choice.

| | |
|---|---|
| `lha208.bin`, `fgrep_1.11`, `hex` | **Byte-identical** to `CMDS/lha`, `CMDS/fgrep` and `CMDS/hexedit`. Nothing to add. |
| `trminfo1.lzh` | Every one of its terminal descriptions is already in `SYS/TERM`, `coco3` included. |
| `advent0`, `colossal.lzh` | Already here: `GAMES/adv` holds advent0 and advent1-4.txt, `SRC/adv` the source. |
| `cc1`, `cccp` | gcc 1.42 passes with no rest-of-toolchain; GCC 1.39 and 2.x ship complete. |

**Reversed, and now included:** `compress_4.0`, `diff_1.1`, `gtar`, `lharcs`,
`m4_0.5`, `sed_1.06` (other editions) and the six-build `gzip` 1.2.4 set
(68000, 68020 and CPU32, with and without csl) — all in `CMDS/REBUILT`. Also
`ub68020demo` in `CMDS/DEMOS`. Calling a 68020 build a duplicate of a 68000
one was wrong: on a 68020 machine it is the build that fits.

## Excluded because they cannot work here

| | |
|---|---|
| the 15 `pbmexec` programs | **Not because netpbm replaced them.** They cannot read PBM as it exists on this disk: `pbminvert` rejects a hand-written, textbook plain P1 that netpbm's own `pnmfile` reads correctly — *"Junk in file where an integer should be!"* — and does the same with raw P4. Fourteen of the names are free and would have been genuine additions (`cbmtopbm`, `pbmtops`, `pbmcrop`, `pbmtrnspos`…); they simply do not work with anything here. |
| `umusek` | Stops with *"Can't get screen addr"*. |
| `dedit` | Will not load at all — error 205, `E_BMID`, a bad module ID. |
| `gnuplot_x11` | An X11 driver, and that archive holds no `gnuplot` binary to drive. |
| `f68k` / `os9lader` | F68K is a **Forth** system despite the name; its OS-9 part is only a loader, and `forth` is already here. |
| `regex`, `strcmp`, `testpad`, `makecrc` | Library and test fragments, not programs. |
| `tplot` | Drives an Atari ST plotter, and unlike mgif it has no mode that does anything without one. |

**Reversed, and now included:** the seven **MM/1 drivers** (`CMDS/MM1`) — a
driver is not meant to be *run*, so "fails to start" was never a reason, and
an MM/1 is a real OS-9 machine somebody still owns. And **`mgif`**, because
`mgif -i` inspects a GIF perfectly well on any terminal; only *display* needs
the ST.

## Excluded on the owner's terms -- from the 152 recovered archives

Measured 2026-08-14 while working the newly-recovered pool categories; the
whole haul is described in `notes/POOL-NEW-HAUL.md`.

| | |
|---|---|
| `rz`, `sz` (ZMODEM) | Omen Technology's, and the archive carries the order form: **$20 per user**, 1-10 users, *"payment of this license authorizes the installation and use"*. Both run trap-free and would have been a genuinely useful pair. Not ours to ship. |
| `smbmount`, `samba`, `smbdrv` | The author encourages free copying and then draws a line: *"No part of this material may be distributed with other software packages without the express permission from the author."* A curated collection is precisely that. Worth asking him. |
| `msfm` (MS-DOS file manager) | Derived from source printed in Peter Dibble's *OS-9 Insights*, and its own `note.doc` carries Microware's notice -- *"proprietary confidential property ... distribution in any form to any party other than licensee is strictly prohibited."* |
| `csl` | Microware's, found redistributed inside `STerm68k.lzh`. Finding it in a freeware archive does not make it freeware. |

**`fpu` was on this list and comes off it.** `xyz.lzh` carries `fpu.doc`, which
says in its first two lines: *"FPU - (C) 1995 Microware Systems Corp.
Permission to distribute FPU is granted so long as this file is retained."*
That is the rights holder granting it. `fpu` may ship as long as `fpu.doc`
ships beside it, and the Ultra C builds that need it are usable rather than
dead. No such grant exists for `cio` or `csl`.

## Excluded on merit

| | |
|---|---|
| `cmake` | Carl Kreider's own one-line description: *"crude make, obsolete."* `make` and `gmake` are here. |
| `dearc` | `arc` covers it. Weak, and worth revisiting. |
| `uac_view` | A viewer for one person's system data files, shipped with 79 files of that data. |
| `dhry` — **reversed** | Excluded once as "a benchmark that measures the host under emulation". That was wrong: on real hardware it measures your machine, and with a figure from real hardware it is useful under emulation too. All twelve builds now ship in `CMDS/DHRY`. |
| Vendor demos — **reversed** | Excluded once as "commercial demo versions". UniBasic's manual contains an explicit *grant*. All three now ship in `CMDS/DEMOS`. |

## Present but not built

| | |
|---|---|
| **Inform 3** | The manual, the three demos' source and the compiler source all ship. The compiler does not build: `cpp` aborts (`E_PRCABT`, wild pointer) part way through the 160 KB source, with `-qm` and without, with `-K=2`, and with 256 MB of arena. |
| **`man`** | Not the program it looks like. It expects `/dd/USR/MAN` full of **proff-format** files, not troff man pages, and falls back to OS-9 `help`. `nroff -man` already reads the 172 pages in `DOC/netpbm`. |
| `elvis` | Long-standing: full docs and source on the disk, no binary. See `ROADMAP-freeware.md`. |
| `spline` | Built for a Tektronix-graphics machine; only its test driver `mtst` ships. |

## Images deliberately not shipped

`jessica1.gif` and `school46.gif` came as test material with `mgif`. They look
like photographs of identifiable people, possibly children, and one image is
enough to make the converters demonstrable — `gulls.gif` ships instead.

## Not an exclusion, but on the same shelf

`SYS/password` listed `tester` and the anonymous account against execution and
data directories that have never existed, so only `su` could ever log in. Fixed
2026-08-13: both now point at `/dd/CMDS` and have a data directory with a
`.login` that sets PATH, TERM and TERMCAP, because a fresh OS-9 login inherits
nothing.
