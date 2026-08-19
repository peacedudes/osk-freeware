# Session log — the repair, documentation and archive pass

Branch `repair-and-document`, off `main` at `b37001c`. `main` is untouched.
Nothing pushed. Plan: `notes/PLAN-repair-and-document.md`.

Each entry is one commit, with what changed and how it was verified. All eight
`tools/check_disk.py` checks pass at every commit and the image rebuilds.

---

## Where the counts stand

|  |  |
|---|---:|
| program files under `CMDS` | 949 |
| not programs at all | 25 |
| **actual programs** | **924** |
| demonstrated running | **877 (95.0%)** |
| did not | 47 |

Was 870 of 925 (94.1%) when this pass started.

---

## Commits

**`Docs: measured verification of all 949 programs, four stages`**
The previous session's finished work, approved and committed unchanged.

**`Docs: plan for the repair, documentation and archive pass`**
The plan, written before touching anything.

**`Core: one place knows where the archives are, and it fails loudly`**
Eight tools hardcoded `~/mine`, which is now off limits, and would have failed
silently or found nothing. `tools/paths.py` is the single place that knows;
every accessor exits non-zero rather than returning an empty directory.
*Verified:* a bad `OSK_POOL` override exits 1 with a message naming both the
path tried and the move. Re-running `list_pool.py` against the relocated pool
produced **15,153 member rows against the 7,704 on file** — the old inventory
predated the 152 recovered archives, so `notes/pool-members.tsv` was refreshed.

**`Core: a prober for diagnosing one program at a time`**
`tools/run_in_session.sh` runs one command through `SYS/login` and shows what
came back, keeping os9exec's `#` lines and using `grep -a` throughout.
*Verified by making it fail first:* its original filter used
`grep -vF "$cmd"`, which swallowed `/dd/CMDS/no_such_program: (E$PNNF)…`
because the error line names the command — a program that could not be found
scored identically to one that ran and said nothing. Now matches the echoed
line exactly.

**`Fix: the Fortran-77 system works -- six programs wanted os9lib loaded`**
The disk carries a complete Fortran-77 compiler and nobody knew. `rtf`, `for`,
`lnk`, `lnk.org`, `biory` and `creadoc` were all in the silent-and-unexplained
list. Every one calls `F$Link` for `os9lib`, gets `E_MNF`, and exits without
printing — `for` exits with status 221, which is `E_MNF` itself.
`os9lib` is the Fortran **run-time library**, not a program; running a library
as a program is what reached its floating-point code and got it recorded as
"wants a 68881". Same misclassification as `graph`.
*Verified:* with the module reachable, `rtf` reports
`RTF/68K Version 2.14 (19-May-1987)` and **compiled `prime.f` with 0 errors**;
`biory` prompts for a name. From the pool came a **227 KB RTF/68K manual**
(`EFFO/pd1.lzh`), both examples' Fortran source, five demos, and `rtfstart.a`
— the exact file `lnk` names when it fails. `DOC/README-FORTRAN` explains the
module-directory requirement, since the disk has no `load` command.
*Honest limit:* `rtf` emits 68k **assembly**; finishing a build needs
Microware's `r68` and `l68`.

**`Docs: STATUS -- 876 of 924 running, eight silent ones explained`**
Also closed `elvprsv` (its own manual, already on the disk, says never to run
it from a command line) and `sysid` (calls `F$SysID`, which os9exec dispatches
to `OS9_F_UnImp`; its source branches straight to `F$Exit` on the error
without printing — sound program, missing emulator call).

**`Fix: drop Microware's oskdefs.d, and a screener that would have caught it`**
`disk/SRC/rtf/oskdefs.d`, installed by me an hour earlier from an EFFO
*public-domain* disk, is **Microware's file** — same header, same typo
("resrtictions"), 35 identical lines, 1424 bytes against their 1470. Removed.
`tools/screen_microware.py` screens four ways: content hash, line overlap,
ownership claim, and file kind.
*Tuned by making it fail three times:* it first indexed `play/oskBoot`'s
`SRC/`, `USR/` and `SYS/`, which are this project's own working directories,
and accused us of copying our own `ls` build and 33 freeware `.hlp` files; it
matched empty files against each other; and a bare mention of "Microware" in a
comment banner flagged 30 innocent files.
*Verified:* catches Microware system source renamed, stripped of its copyright
and with 46% of its lines deleted — at 100% line overlap.

**`Core: screen archives for Microware source before anything ships`**
Weighted toward **source**, because that is the actual concern: infrastructure
in Japan and Germany runs OS-9/68k today and published source could expose
unknown vulnerabilities. Binaries are a lesser worry, which is why permission
for `cio`/`csl`/`math` was straightforward — they expose nothing.
*Also failed first:* the system-source detector matched `/V_[A-Z]+/` and
flagged Tetris's `V_TYPE`, Phantasia's `D_BEYOND` and POSIX's `d_name`.
Replaced with named OS-9 symbols, case-sensitive, two distinct hits required.

**`Core: chess source, and the 1989 usenet collection triaged`**
All 65 `ar` archives in `play/h4/ARR` opened, 1,192 members screened.
Full write-up: `notes/ARR-TRIAGE.md`. **`curses.ar` excluded** — its
`curses.h` is 82% line-identical to the SDK's, with a `.l` library and full C
source. It was never on the disk, so the screen caught it as a candidate.
`chess.ar` gave 23 files of engine source for the shipped `chess`, filling a
`SRC/chess` tree `DOC/ORIGINS` already promised.
*A correction to my own earlier claim:* I reported `ARR/x` as holding source
for five games that shipped without any. Wrong — it is all in `disk/SRC/toys`,
11 of 15 files byte-identical. I had searched for directories named after each
program instead of files inside a tree named for the archive, which is the
exact mistake CLAUDE.md warns about.

**`Core: ship the cio builds of cat, basename, dirname, strings -- 52KB smaller`**
199 shipped binaries are our trap-free `-qm` rebuilds, 4.9 MB in total, built
before it was known `cio` would ship. Four had a working cio build already on
the disk. *Verified one at a time, and that mattered:* `cat.cio` produces
**byte-identical output**, `basename`/`dirname` match and have real usage
banners; **`wc.cio` is broken** — nothing at all for a file argument where ours
correctly reports `81 455 3157` — so `wc` keeps our build. Ours are kept as
`REBUILT/*.nocio`, so reversing is one move.

**`Fix: devprc rebuilt from source -- the archived module was corrupt`**
The only outright "will not load" on the disk. Patching its CRC turned
`E_BMCRC` into `E_BMID`, which **proved the body was damaged and not just the
checksum**: its initialised-data descriptor reads `dest=0x2C734330
count=0x24402FFA` where a working module's reads `dest=0x604 count=0x110`.
Rebuilt from `SRC/devprc` with `r68` and `cc`; `perror` came from the
collection's own `SRC/unixlib`. *Verified:* CRC good, parity good, module name
right, and `devprc -h` prints its usage. `-a` asks `F$GPrDBT` for the kernel
process table, which os9exec answers without real data.
*Built against a clean overlay:* the first build carried the SDK's 64-byte
author psect. A copy of the SDK with `cstart*`'s psect blanked (same length,
so no offset moves) produces a byte-identical binary with **zero stamps**.
This also unblocks rebuilding the other 199.

**`Fix: the Graph trap library is named Graph, as real OS-9 requires`**
The module's own name was lowercase `graph` while all seven programs ask for
`Graph`; os9exec only found it through a case-insensitive **host filename**
lookup, so on real hardware none of them could ever have worked. One byte,
then the CRC recomputed — CRC and parity checked good before the patch as well
as after. All seven now **start**, both `F$TLink` calls succeed, and the
library takes a bus error (vector `$08`) on its own first instruction, at the
entry address `F$TLink` just returned. It drives Atari hardware directly.

---

## Still open, in plan order

- **E3** — the remaining 195 trap-free rebuilds, ~4.9 MB. The clean-overlay
  build path is now proven, so this is mechanical but wants care per program.
- **B2** — the five SNOBOL4 games, one shared code path.
- **B5** — `firq`/`souper`/`sysmem`: whether OS-9/68k specifies `A0` at entry.
  Answerable from the v2.4 Technical Reference, now available in `txtResources`.
- **B6/B7/B8** — `oleo`, `rxmod`, `trap`; the remaining 20 silent programs;
  the ten that start and then fail.
- **B9** — `ksh`'s interactive loop; pdksh source is at `SRC/pdksh/sh/`.
- **C1/C2** — the documentation sweep: ~383 programs whose only entry is one
  line in `DOC/INDEX`.
- **D1/D3** — the 6,508 members of the 152 recovered archives, never assessed;
  and reconciling the 419 pool modules the disk lacks.

## One thing for rdoggett

15 shipped modules carry `>>>from the disk of Robert Doggett<<<` in their
`cstart` author psect — `wc`, `ls`, `pep`, `pdraw`, `queens`, `ularn`, `hotel`,
`suicide`, `tt` and the `.nocio` builds among them. It is documented in
`notes/FREEWARE-REBAKE.md` as accepted (they cannot be rebuilt), and
`check_disk.py` asserts the count stays at 15. Flagging it only because this
collection is headed for public release with your name inside those binaries.
Now that the clean-overlay build path works, several could be rebuilt without
it if you would rather they were not there.
