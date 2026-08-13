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

| | |
|---|---|
| **`auxlib`** — `alib.l`, `alib020.l` and nine headers, a personal extension to Microware's C library | The author's own read.me says *"I don't have any sort of docs. That is perhaps the main reason I don't distribute this."* That is a habit rather than a term, and the archive was published to the hobbyist archive regardless. Useful to anyone compiling C here. Extracted and ready; left out only because the author's sentence deserves your eye, not mine. `[LIB/auxlib.ar]` |

## Excluded on the owner's terms

| | |
|---|---|
| `tshell` | Its readme states *"NOT Public Domain, but its free for private use"* — the author's own restriction, and the clearest case on this list. |

## Excluded as duplicates of what already ships

| | |
|---|---|
| `lha208.bin`, `fgrep_1.11` | **Byte-identical** to `CMDS/lha` and `CMDS/fgrep`. |
| `diff_1.1`, `compress_4.0`, `m4_0.5`, `sed_1.06`, `gtar` | Different builds of programs already here and working. `tar` in particular is load-bearing — `mkimage.sh` populates the disk with it. |
| `hex` | The disk's `hexedit` is the same program under its other name. |
| `lharcs` | C-LHarc 1.01; the disk has lha 2.08 and lharc. |
| `cc1`, `cccp` | gcc 1.42 passes; GCC 1.39 and 2.x ship complete. |
| `trminfo1.lzh` | 28 of its 30 terminal descriptions are already in `SYS/TERM`. Only `coco` is missing — worth taking on its own. |
| `gziposk124` | `CMDS/gzip` is the same 1.2.2 build; the rest are 68020/CPU32 variants. |
| `advent0`, `colossal.lzh` | Already here: `GAMES/adv` holds advent0 and advent1-4.txt, `SRC/adv` the source. |
| `ubdemo` (68020) | The 68000 sibling is in `CMDS/DEMOS`. |
| PBMPLUS, the 15 `pbmexec` programs, `pbmdoc.ar` | The 1991 suite and its documentation that netpbm replaced. netpbm is newer, needs no trap handler, and now ships its own manual. |

## Excluded because they cannot work here

| | |
|---|---|
| `mgif`, `tplot` | Write straight to Atari ST graphics memory. `mgif`'s own port note: *"it runs on ST's only, if you don't change the source."* |
| `updates.lzh` — `windio`, `scsi_mm1a`, `rb37c65`, `snddrv`, `keydrv`, two `msdrv` | MM/1 hardware drivers. |
| `umusek` | Stops with *"Can't get screen addr"*. |
| `alps` | Switches an ALPS ASP-1000 printer between draft and NLQ. One printer, 1988. |
| `dedit` | Will not load at all — error 205, `E_BMID`, a bad module ID. |
| `gnuplot_x11` | An X11 driver, and that archive holds no `gnuplot` binary. gnuplot 2.0 ships instead. |
| `f68k` / `os9lader` | F68K is a **Forth** system despite the name; its OS-9 part is only a loader, and `forth` is already here. |
| `regex`, `strcmp`, `testpad`, `makecrc` | Library and test fragments, not programs. |

## Excluded on merit

| | |
|---|---|
| `cmake` | Carl Kreider's own one-line description: *"crude make, obsolete."* `make` and `gmake` are here. |
| `dearc` | `arc` covers it. |
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
