# Session log — the repair, documentation and archive pass

Branch `repair-and-document`, off `main` at `b37001c`. `main` is untouched.
Nothing pushed. Plan: `notes/PLAN-repair-and-document.md`.

Each entry is one commit, with what changed and how it was verified. All eight
`tools/check_disk.py` checks pass at every commit and the image rebuilds.

---

## Where the counts stand

|  |  |
|---|---:|
| program files under `CMDS` | 951 |
| not 68k programs at all | 26 |
| **actual programs** | **924** |
| demonstrated running | **874 (94.5%)** |
| did not | 51, of which 8 work under a stated condition |

Was 870 of 925 (94.1%) when this pass started.

**This is a fresh four-stage sweep, re-run 2026-08-19 against the current
binaries — not the old measurement with repairs added on.** The figure moved
very little, and for a while I was quoting 884 because I had been incrementing
the total each time I fixed something without re-measuring. That was wrong and
the sweep corrected it downward.

Eight programs run but under a condition the sweep does not create, so it
cannot credit them: the six of the Fortran-77 suite (they link `os9lib`, and
the sweep sets no module directory), `devprc` (its `-h` works; bare it aborts)
and `makecrc` (it writes files, never to the terminal). They are named in
`DOC/STATUS` rather than quietly folded into the total.

All 34 of the previously-silent programs now have a named cause.

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

**`Core: screen archives for Microware source before anything is added`**
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
`chess.ar` gave 23 files of engine source for the the chess on the disk`, filling a
`SRC/chess` tree `DOC/ORIGINS` already promised.
*A correction to my own earlier claim:* I reported `ARR/x` as holding source
for five games that included without any. Wrong — it is all in `disk/SRC/toys`,
11 of 15 files byte-identical. I had searched for directories named after each
program instead of files inside a tree named for the archive, which is the
exact mistake CLAUDE.md warns about.

**`Core: ship the cio builds of cat, basename, dirname, strings -- 52KB smaller`**
199 binaries on the disk are our trap-free `-qm` rebuilds, 4.9 MB in total, built
before it was known `cio` would be included. Four had a working cio build already on
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

**`Fix: all five SNOBOL4 games play -- they wanted a syntax file, not a repair`**
`poker`, `blackjak`, `rpoem`, `rstory`, `stone` died on `Illegal instruction:
4afc` — both the 68000 ILLEGAL opcode and the module sync word, so control had
jumped into a header. It read as a corrupt shared library and was not one.
*Method:* rebuilt from source and it failed **identically**, which proved the
bug was in the source, not the binary; then bisected with flushed `printf`
tracing to `que_init()` → `ph_init()`, which `phrase.h` defines as
`rsent_init("PHRASE.SYN")`. The open failed, the null result became a pattern
tree, and the first match jumped through a null function pointer. The syntax
files existed all along in `DOC/snobol` — not somewhere a running program
looks. Data moved to `GAMES/SNOBOL`, the five rebuilt to name it there; `chd`
alone would not have worked, since bash cannot change the OS-9 data directory
and sh cannot fork an absolute path. *Verified:* all five run in a plain login
session — `rpoem` writes poetry.
*One caught mistake:* an intermediate image build failed and I had hidden it
with `>/dev/null`, so I spent a cycle tracing a stale image.

**`Docs: A0 is undefined at entry -- the three faulters want supervisor state`**
The question the last pass could not settle. Microware's v2.4 Technical
Reference, F$Fork, lists the registers handed to a new process and says
**`(a0) = undefined`** outright — the module pointer these three appear to want
is in `(a3)`. So os9exec is not at fault. The deeper reason is in their source:
`firq`, `souper` and `sysmem` all declare `@_sysattr: equ $a001` and read the
kernel's globals through Microware's `<sysglob.h>`. They are **system-state
programs**, they cannot be rebuilt here (that header is Microware's and is
kernel internals), and they will not run under os9exec. A complete answer, not
a gap.

**`Core: ptxm from the pool, and five more silent programs explained`**
`makecrc` **works** — it generates `arc.c`, `binhex.c`, `ccitt.c`,
`ccitt32.c`, `kermit.c`, `zip.c`, CRC-table source for six polynomials, and
writes nothing to the terminal. `ptxminst` linked a module `Ptxm` that was not
here; it is now, from the pool's DRIVERS category — Nick Holgate's Path Table
eXtension Module, courtesyware. It is **not** a pseudo-tty installer, which is
what `DOC/INDEX` claimed. `pri` chains to `/r0/cmds/copy` with no arguments;
`suse` and `t` make no system call at all and are stubs.

**`Docs: G-Windows programs get their authors' documentation`**
`cyberwar`, `lfmaker`, `puzzle`, `scriptmaster` — all Stephen Carville's, all
already on the disk, none documented. Their readmes and manuals recovered from the
pool's GWINDOWS category, plus `cyberhelp.data`. **Licence flagged, not
settled:** the readmes carry a copyright line and no distribution statement
either way. Recorded in `SOURCES.txt`. I did not add `dclock` or `colortest`
from the same archive, because adding a new program on unstated terms is a
different question from documenting one already present.

**`Docs: 23 manuals mined from the pool, and Graph explained by its own`**
`tools/doc_census.py` makes the coverage number reproducible: **598 of 950
documented (62%)**, 352 with nothing but their INDEX line.
`tools/find_pool_docs.py` searched the member inventory rather than extracting
454 archives, and found real manuals for 23 of the 352 — the honest finding is
that most of the rest never had one.
The prize was `graph.doc`, which **answers the bus error**: the library
*"laeuft mit gesetztem Supervisor-Bit"* and is explicitly not linkable into
ordinary programs. The module agrees — `M$Attr` is `$A0` and bit 5 is the
supervisor-state bit. Its assembler source and two more manuals came with it.
A. Greulich, 1988, public domain.

**`Docs: every one of the 34 silent programs now has a named cause`**
The last fifteen traced. Four want a file that is not here (`bootlogger`,
`cron`, `read_mail`, `arepdaemon` — each named); one wants an argument
(`bincheckr`); three want hardware or a network (`infoxpress` opens `/t3`,
`authwn`, `inetdc`); two are daemons that are silent by design (`splman`,
`splprt`); four want G-Windows. **One has a real bug:** `dir` calls `I$WritLn`
with a byte count of `$FFFFFF80` — minus 128 — and gets `E_BPADDR`. `ls` does
the same job and works.

**`Core: the VMod_trap library from the pool, and oleo's F$RTE diagnosed`**
`rxmod` asked `F$TLink` for `VMod_trap` and got `E_PNNF`. The library was in
the pool (EFFO forum 15, the SERLOAD utilities) — and its module name was
lowercase `vmod_trap`, **the same case mismatch as `graph`**, so it could never
have worked on real OS-9 either. Renamed, CRC recomputed, both checked good
before and after. The trap now installs; the library then bus-errors because
`M$Attr` is `$A0` — supervisor state — exactly like Graph. Assembler source in
`SRC/serload`.
`trap` turned out not to be silent at all: it prints `tlink: -1` and names the
handler it wanted. `oleo` calls **`F$RTE`**, which kills the caller unless it
is genuinely inside an intercept routine; execution then resumes at a bad
address and takes `Illegal instruction: 000b`.

**`Docs: the five never-assessed categories, assessed -- 65 absent modules`**
`AUDIT-pool.md` feared a large backlog in DRIVERS, EFFO, GWINDOWS, NETWORK and
TELECOM. Measured: **537 distinct modules, only 65 not already on the disk**,
and most of those are other people's hardware — Gepard, Atari and CT68000
descriptors and drivers — or already-refused packages (rz/sz, samba, the KWIN
shareware, msfm). Full write-up in `notes/POOL-ASSESSMENT.md`.
**One find matters: a Microware `fpu` sitting loose inside `TELECOM/STerm68k`,
14,572 bytes against the SDK's 12,848** — a different build, so neither hashing
nor line overlap would have caught it. Caught by name. The screener now carries
a named-module denylist (`fpu`, `fpu040`, `cio020`, `p2init`, `os9p1`, `rbf`,
`scf`, …) and explicitly **exempts the five Microware did permit**, so a later
pass cannot "fix" the disk by deleting `cio`, `csl`, `csl020`, `math` or
`math881`.

**`Core: relink-against-cio driver, and say 'on the disk' not 'shipped'`**
`tools/rebuild/relink_cio.sh` rebuilds the 199 trap-free programs with
`-qixm` (links cio) instead of `-qm`. It mirrors `rebuild.sh`'s proven
invocation — `-V=/h6 -V=/h7` for the tree's own headers and the COMPAT shims,
and four libraries linked unconditionally. Without `/h7`, `yacc` stops at
`can't open /dd/defs/assert.h`; without `math.l`, `wanderer` fails on
`_T$LtoD`.
*Two bugs found by making it fail:* the first run processed 2 of 198 rows
because **os9exec inside the loop was eating the loop's own stdin** — a trap
this collection's notes already record. `< /dev/null` fixes it. The second was
mine in reporting: I had been writing "shipped" throughout to mean "is on the
disk", which reads as a claim of distribution. **Nothing has been released.**
Reworded across the disk docs and notes.

**Result: 174 of 198 rebuilt, 4,083,098 → 1,905,744 bytes — 53.3% smaller.**
21 failed to build, 3 have no source tree.

**`Fix: makedb builds its database; the five screen programs all draw`**
`makedb` wanted `/dd/usr/lib/smail/`, which did not exist. Created, with a
starter `palias`; it now writes `palias.dir` and `palias.pag` and completes.
The five carried as "start, then fail later" all do their job when watched in
a session: **`suicide` animates its stick figure** (it was recorded as
producing no output), `draw` renders a live clock and calendar, `top` draws
the process table, `greed` and `digclk` draw their screens. They are
full-screen interactive programs that OS-9 aborts when input closes — not a
fault.
`mail` wants a scratch file on an `/r0` RAM disk. os9exec offers RAM disks
(`mount -r=<kB>`), but the mount is refused once a session is running, for
`r0` and `hX` alike, so `/r0` cannot be produced from inside.

**`Docs: digclk has no quit key by design; draw's is unconfirmed`**
`SRC/digclk/clock.c` reads the keyboard only inside `#ifdef MSDOS`; on OSK the
loop is sleep-and-redraw with no read at all, so **no key quits it** — you
interrupt it. `draw`'s own help says `<esc>`, but escape did not end it under
`try_quit.py`, so that is recorded as documented-but-unconfirmed rather than
written up as verified.

**`Core: 117 programs relinked against cio -- disk 194M to 190M`** and
**`Fix: revert six relinks that regressed to 'No more memory'`**

The big one, and the one I got partly wrong. Full write-up:
`notes/RELINK-CIO.md`.

174 of 198 rebuilt cio-linked, 53.3% smaller in total. Each was run against
the binary it would replace and the outputs compared; 117 passed and were
installed, **1.46 MB reclaimed**, disk 99M → 96M and the image 194M → 190M.

*Three separate mistakes, all mine, all caught:*

1. **`tar` must never be relinked.** `mkimage.sh` populates the image with the
   collection's own `tar`, which is why the build needs no Microware software.
   My relinked `tar` needed `cio`. The next image build failed outright —
   `tar extracted 0 files, expected 5596` — because the test image had the five
   modules deliberately removed. Reverted.
2. **Keeping a `.nocio` copy of all 117 made the tree bigger**, 2.5 MB of
   copies against 1.46 MB reclaimed, which defeats the purpose. Removed; git
   is the record.
3. **`NEW-SPEAKS` was a bad verdict.** It scored any output from the new
   binary as an improvement, and `No more memory !!!` is output — os9exec
   refusing the process its static storage, strictly worse than the silence it
   replaced. Six programs regressed that way and were reverted. Raising
   `-qixm` to 32k and 64k changed neither size nor behaviour, so the cause is
   not yet understood.

*What finally settled it:* every installed binary was **run** and checked for
`No more memory`, `E_BMID`, `E_NEMOD`, `User Trap`, `Illegal instruction` and
`BUSERR`. 111 ok, 6 NO-MEMORY, no faults. That audit should have run before
installing, not after — a size comparison cannot see any of those.

**Net: 111 programs relinked and verified by running.**

---

## Still open, in plan order

- **E3** — the remaining 195 trap-free rebuilds, ~4.9 MB. The clean-overlay
  build path is now proven, so this is mechanical but wants care per program.
- **B8** — the ten that start and then fail later, and the unknown quit keys
  for `digclk`, `draw`, `sc`, `sh`, `vi_cio`.
- **B9** — `ksh`'s interactive loop; pdksh source is at `SRC/pdksh/sh/`.
- **C2** — measured usage capture for the 352 still carrying only an INDEX
  line. The pool has no manual for them; most never had one.
- **D3** — reconciling the remaining pool modules the disk lacks; `passwd`,
  `channel`, `osktag` and `readstr` are the only untaken candidates worth a look.

## One thing for rdoggett

15 modules on the disk carry `>>>from the disk of Robert Doggett<<<` in their
`cstart` author psect — `wc`, `ls`, `pep`, `pdraw`, `queens`, `ularn`, `hotel`,
`suicide`, `tt` and the `.nocio` builds among them. It is documented in
`notes/FREEWARE-REBAKE.md` as accepted (they cannot be rebuilt), and
`check_disk.py` asserts the count stays at 15. Flagging it only because this
collection is headed for public release with your name inside those binaries.
Now that the clean-overlay build path works, several could be rebuilt without
it if you would rather they were not there.

---

## 2026-08-20

**`Fix: cron, bootlogger, read_mail and arepdaemon get the files they open`**
Four of the long-silent programs each opened one file, failed, and exited
without a word. The files now exist and are **empty**, which is the correct
state for all four: `cron` reads its crontab to end-of-file and schedules
nothing, `bootlogger` opens the log to read and to append, `read_mail` reads
the mailbox and quotes it for a reply, `arepdaemon` takes its lock and gets it.
*Caught while doing it:* my first `mail_` contained prose explaining why the
file existed — and `read_mail` dutifully quoted that prose as if it were mail.
The data files are empty; the explanations moved to READMEs beside them.

**`Fix: dir lists directories -- moveq #128 sign-extended to -128`**
A genuine 68000 bug, in `SRC/bix/dir.c` line 1066:

    wr_line1  moveq.l   #128,d1
              os9       I$WritLn

MOVEQ sign-extends an 8-bit immediate, so 128 becomes −128 and `I$WritLn` got
a byte count of `$FFFFFF80` and returned `E_BPADDR`. MOVEQ's range is
−128..+127; 128 is one past it. There is no rebuild recipe for `dir`, so the
module was patched in place: `72 80` → `72 7F` at `$1A38`, the only occurrence
in the module and immediately followed by the trap. Same two bytes, CRC
recomputed, CRC and parity checked good before as well as after. The only
behavioural difference is a 127-character maximum line. **`dir` lists a
directory now.**

**`Fix: the print spooler gets its queue; bincheckr reads a chess book`**
`splstat`, `splman` and `splprt` all open `/DD/SPL/splq`; the directory did not
exist, so each stopped at error 216. Created and empty. `splstat` now opens
the queue and exits 0. `bincheckr` works when given the opening book that was
on the disk all along: `bincheckr /dd/GAMES/gnuchess.book`.

**`Docs: ksh is dead because os9exec's I$Read waits for the full count`**
The big one. Full write-up: `notes/OS9EXEC-IREAD.md`.
Measured on a pty, in one program: `read(0,buf,1)` returns on the first
keypress; **`read(0,buf,256)` never returns**, however much is typed. Line-mode
reads (`fgets`, `I$ReadLn`) are unaffected — which is the entire difference
between `bash`/`sh`, which are interactive here, and `ksh`, which is not.
pdksh reads its command line with `read(ttyfd, line, LINE)` and `LINE` is 256.
The trace matches exactly: `I$Read D1.l=$100`, no return.
*Two things ruled out by measurement:* `isatty` works, and the line editor is
not to blame — setting `ENV` to a file with `set +o emacs` makes the **prompt
appear**, proving ksh reads and runs its ENV file, and the command read still
hangs.
*Checked:* no other program on the disk is affected. All 43 failures were
traced for a large `I$Read`; two do one, both from a file rather than a
terminal, and both now work anyway.
*Blocked:* a one-function patch to `lex.c` is written, but pdksh cannot be
rebuilt here — `osklib.r` exists nowhere at all, and the `std/` header tree
wants `/usr/include` symlinked in. **This is where I stopped.**

**`Docs: DOC/USAGE -- 179 undocumented programs describe themselves`**
352 programs have nothing but their `DOC/INDEX` line, and the pool has manuals
for only 23. So each was asked `-?` and what it said was kept: **179 answered
with a real usage or syntax line**, 114 printed something else, 9 faulted, 50
said nothing. Every line in `DOC/USAGE` came out of a program; none of it was
composed. `-?` is a convention and not a rule — TeX prompts with `**` and
reads stdin, which is correct — so silence there is not evidence of a fault.

**`Docs: argproc library source and manual, from EFFO forum 7`**
`argproc_demo` stops with `**** Stack Overflow ****` whatever it is given. Its
`M$Stack` is 3072, the same as programs that work, so the fault is its own.
The complete ARGPROC package — library source, the demo's own source, and a
manual for `argproc()` — was in the pool and is now at `SRC/argproc` and
`DOC/argproc_demo`. Rebuilding the demo needs `vsprintf` and `bcopy`, which
the cio-linked library set lacks — the same wall the relink hit.
