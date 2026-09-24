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
| `umusek` — **reversed** | Ships: it opens on a machine with a graphics screen and says why it stops without one. |
| `gnuplot_x11` | An X11 driver, and that archive holds no `gnuplot` binary to drive. |
| `f68k` / `os9lader` | F68K is a **Forth** system despite the name; its OS-9 part is only a loader, and `forth` is already here. |
| `regex`, `testpad`, `makecrc` | Library and test fragments, not programs. (`strcmp` was listed here; Gregorie's `strcmp` from sh 7.5 is a real program and ships.) |
| `tplot` — **reversed** | Ships: it asks its three questions on any terminal, and draws with A-line calls on an Atari ST. |

**Reversed 2026-08-15: `dedit`.** It was excluded as *"will not load at all --
error 205, `E_BMID`, a bad module ID"*. That error is real and reproduces
exactly -- but it is what OS-9 says when you try to **fork a BASIC09 module as
a 68k program**. `dedit` is type 0x02, language 0x02: I-code, the same kind of
module as `bio`, `blackjack` and `wysetime`, which this disk already ships and
already documents. Run it the documented way -- `runb` with the bare module
name -- and it loads and runs. This is the identical mistake the collection
caught once before, on `bio`, and did not think to look for again.

**Reversed, and now included:** the seven **MM/1 drivers** (`CMDS/MM1`) — a
driver is not meant to be *run*, so "fails to start" was never a reason, and
an MM/1 is a real OS-9 machine somebody still owns. And **`mgif`**, because
`mgif -i` inspects a GIF perfectly well on any terminal; only *display* needs
the ST.

## Excluded on the owner's terms -- from the 152 recovered archives

Measured 2026-08-14 while working the newly-recovered pool categories; the
whole haul was described in `POOL-NEW-HAUL.md`, (deleted in the 2026-08-27 notes prune; `git log --diff-filter=D --name-only -- notes/` finds it).

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
| `dearc` | `arc` covers it. Re-run 2026-09-23 on os9exec d992145: still *"File not packed with correct number of bits"* on a crunched member, so it stays out on function as well as merit. |
| `uac_view` — **reversed** | rdoggett, 2026-09-23 (FOR-RDOGGETT 37): ship it. `CMDS/UAC_view`. |
| `dhry` — **reversed** | Excluded once as "a benchmark that measures the host under emulation". That was wrong: on real hardware it measures your machine, and with a figure from real hardware it is useful under emulation too. All twelve builds now ship in `CMDS/DHRY`. |
| Vendor demos — **reversed** | Excluded once as "commercial demo versions". UniBasic's manual contains an explicit *grant*. All three now ship in `CMDS/DEMOS`. |

## Present but not built

| | |
|---|---|
| **Inform 3** | The manual, the three demos' source and the compiler source all ship. The compiler does not build: `cpp` aborts (`E_PRCABT`, wild pointer) part way through the 160 KB source, with `-qm` and without, with `-K=2`, and with 256 MB of arena. |
| **`man`** | Not the program it looks like. It expects `/dd/USR/MAN` full of **proff-format** files, not troff man pages, and falls back to OS-9 `help`. `nroff -man` already reads the 172 pages in `DOC/netpbm`. |
| `elvis` — **built** | Ships, built here from its source. |
| `spline` — **shipped** | `CMDS/spline` ships beside `mtst`; its output is Tektronix graphics. |

## Re-verified 2026-09-23 (os9exec d992145), all standing

Run again, fresh image each: `splitalf` (fails on its second output file),
`dearc`, `pbminvert` and the pbmexec set (*"Junk in file"* on netpbm's own PBM),
`robots2` (E_PRCABT), `gnuchess` 4.0's main build (no longer bus-errors, but
takes no keys -- its three sibling builds ship), the IOCCC `dg` and `pjr`
(DECUS cpp rejects their `#d` abbreviations), PtyMan/PtyDrv and the OS-9
International `disp`/`lfcrman`/`watchdog` (os9exec has no guest file manager
or driver support -- confirmed with its session). The silly collection's
`newspeak`, `rock`/`madrock.sp`, `belief`, `funky`, `jroff` and `biffa` stay
out on content (named real people mocked, slurs); six others shipped.

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

## msfm -- removed from the disk 2026-08-21

`msfm` was on the "Refused, with the reason -- do not add" list, as
*"Microware's, out of Dibble's OS-9 Insights"*. The MODULE was never added.
**The SOURCE was**, as `disk/SRC/msfm`, 21 files, and sat there until a sweep
of the pool found it.

How it got in is the useful part: the licence notice is in a SIBLING file,
`note.doc`, one directory up from `SRC/` in `EFFO/forum12.lzh`. Whoever took
the source took the `SRC/` directory and the notice stayed behind. The files
themselves carry no header, no copyright line, nothing -- reading any one of
them tells you only that it is a file manager.

`tools/screen_microware.py` flags 10 of the 21 on its SYSTEM SOURCE rule
(`PD_BUF`, `PD_CPR`, `PD_DEV`, `V_BUSY`, `V_STAT`, `V_NDRV`), which is exactly
what that rule is for. It was never run over `disk/SRC/`.

**The lesson worth keeping: when taking a source tree out of an archive, read
what is in the directory ABOVE it.** A licence that applies to a subtree is
routinely stored at the top of it.
