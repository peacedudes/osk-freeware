# OS-9 freeware corpus — index

What the archive collection contains, what builds, and what actually runs.

**Not committed** — this describes a personal archive, like `CORPUS-AUDIT-68k.md`
and `FREEWARE-TRIAGE-68k.md` beside it.

**All binaries are trap-free** (`-qm`, never `-qixm`): they need no `cio` or
`math` trap handler, so they run on a disk without Microware's SDK. All
hardcoded `/h0` paths have been rewritten to `/dd`. Descriptions come from each
archive's own README or man page.

> **Snapshot, superseded.** This was the state during the first build-and-triage
> pass over the archive corpus. It is kept for the per-archive breakdown below,
> which is still accurate about *what each archive contains*. It is NOT current
> about totals or status:
>
> - the disk now carries **631 modules / 616 distinct programs**, not 125;
> - **`wanderer` plays.** Its screen data was recovered from the /h2 corpus and
>   it was rebuilt from `scores.c` as well as `wanderer.c`. The line below
>   saying its screens are missing is wrong;
> - the "auto-verified running" count came from a classifier that reads an
>   interactive prompt or a usage message as a failure. Do not quote it.
>
> The current picture lives in three places, all of them generated from the
> disk rather than typed: `freeware/DOC/INDEX` (what is on the disk),
> `freeware/DOC/ORIGINS` (where each program came from), and
> `FREEWARE-REBAKE.md` (what was rebuilt and what is still outstanding).

---

## Builds and runs

| archive | what it is | programs | runs |
|---|---|---|---|
| `adv` | Colossal Cave Adventure | advent | 1/1 |
| `advint` | ADVSYS — adventure-writing system + compiler | advcom advint | 2/2 |
| `animal` | "guess the animal" learning game (curses) | animal | 1/1 |
| `bog` | Boggle word game + dictionary builders | bog mkdict mkindex | 3/3 |
| `chess` | chess — three versions on one disk | CH3 CH4 CH5 fuddle | 4/4 |
| `chksum` | 32-bit file checksum | chksum | 1/1 |
| `cookie` | fortune-cookie printer + hash builder | cookie cookhash | 2/2 |
| `cpr` | print/pretty-list C source | cpr | 1/1 |
| `crib` | cribbage | crib | 1/1 |
| `crypto` | cryptogram puzzle assistant | crypto | 1/1 |
| `cursive` | horizontal cursive banner generator | cursive | 1/1 |
| `cutpaste` | `cut` and `paste` field tools | cut paste | 2/2 |
| `cuts` | Coco Usenet Transfer Utility | cuts | 1/1 |
| `digclk` | digital clock display with hostname | digclk | 1/1 |
| `des` | DES file encryption | des | 1/1 |
| `diff` | GNU diff 1.4 | diff | **1/1, output verified** |
| `draw` | character-graphics drawing program | draw | 1/1 |
| `fortune` | random quotations + database tools | fortune strfile unstr | 3/3 |
| `gnu` | GNU Chess 4.0 (curses + plain) | gnuchess nchess | 2/2 |
| `gothic` | gothic/blackletter banner text | gothic | 1/1 |
| `hang` | hangman | hang | 1/1 |
| `ispell` | interactive spelling checker + dict builder | ispell buildhash | 2/2 |
| `kermit` | Kermit file transfer (Columbia) | kermit xkermit | 2/2 |
| `lander` | lunar-lander arcade game | lander | 1/1 |
| `life` | Conway's Game of Life (curses) | life | 1/1 (draws grid) |
| `my.opt` | 68k assembly peephole optimiser | my.opt | 1/1 |
| `misc` | **11 small utilities** (see below) | 11 programs | 11/11 |
| `nobs` | cribbage (the Colonel's Cribbage Program) | nobs | 1/1 |
| `nroff` | nroff text formatter | nroff | 1/1 |
| `patch` | Larry Wall's `patch` | patch | 1/1 |
| `pow` | X-10 Powerhouse home control | pow | needs `/x1` hardware |
| `pep` | file "detergent" — strips junk from files | pep | 1/1 |
| `reagan` | satirical speech generator | reagan | 1/1 |
| `rndname` | random name generator | rndname | 1/1 |
| `rot` | rot-N text transformer | rot | 1/1 |
| `screen` | screen/terminal utility | screen | 1/1 |
| `shuffle` | card/list shuffler | shuffle | 1/1 |
| `snake` | snake arcade game | snake | 1/1 |
| `snap` | screen snapshot to file | snap | 1/1 |
| `sokoban` | Sokoban puzzle game | sokoban | 1/1 |
| `speech` | English-to-phoneme translation | speech | 1/1 |
| `spiff` | tolerant diff (ignores formatting noise) | spiff | 1/1 |
| `strsch` | Boyer-Moore-Gosper substring search + drivers | bmgtest bmgtest2 | 2/2 (usage msg) |
| `tc` | commodity/futures charting suite | lac main scope sin | 4/4 |
| `toys` | **7 small games/toys** (see below) | 7 programs | 7/7 |
| `tess` | tesselation puzzle | tess | 1/1 |
| `tet` | Tetris | tet | 1/1 |
| `today` | date, moon phase, this-day-in-history | today | 2/2 |
| `touchtype` | typing tutor | touchtype | 1/1 |
| `trap` | system-state trap-handler example | trap | 1/1 |
| `v_misc` | **13 small utilities and games** (see below) | 13 programs | 12/13 |
| `weather` | weather simulator — **6 climates** | england florida georgia japan minnesota shire | 6/6 |
| `vis` | make non-printing characters visible | vis | 1/1 |
| `wanderer` | Boulderdash-style maze game | wanderer | 1/1 — screens recovered from /h2 |
| `world` | "World" text adventure + 2 data generators | world convert vtxtcn | 2/3 (convert is silent by design) |
| `xlisp` | XLISP 2.1 Lisp interpreter | xlisp | 1/1 |
| `xrand` | file encryption (`xcrypt`) | xcrypt | 1/1 |
| `zot` | arcade game (author's own port, 1988) | zot | 1/1 |
| **EFFO** `yacc` | parser generator | yacc | 1/1 |
| **EFFO** `sdb` | symbolic debugger v2.0 | sdb | 1/1 |
| **EFFO** `snobol` | 7 SNOBOL-style demos in C | rstory2 tformat + 5 that crash | 2/7 |
| **EFFO** `vi` | full vi/ex editor (has its own `ex_OS9.c` port file) | vi | 1/1 |
| **EFFO** `sedt` | SEDT screen editor | sedt | 1/1 |
| **EFFO** `pdraw` | 2D/3D data plotting with PostScript output | pdraw | 1/1 |

**`misc` contents** — `areacode` `ascii` `banner` `bush` `clock` `cvtbase`
`hc` (hex calculator) `loan` `printf` `pwgen` `qt`.
**`toys` contents** — `joke` `newsgen` `pacman` `rain` `valspeak` `wish` `worms`.
**`weather`** builds one program per climate/calendar combination.

**`v_misc` contents** — `bite` `calen` (calendar) `cdiff` (context diff) `cpr`
`easter` (Easter date) `gcl` `greed` (game) `maze` `puz15` (15-puzzle)
`strings` `uuexpand` `vis` `xc` (run commands from file).
`greed` and `puz15` existed only as 1990 binaries until now.

## Has source, does not build

| archive | what it is | blocker |
|---|---|---|
| `cdecl` | explain/compose C declarations | **ANSI C** source (`stdlib.h`, `#line`); Microware C is K&R |
| `curses` | Microware screen package | it is a **library** + test drivers |
| `gammon` | backgammon | BSD `sgtty.h` — no OS-9 equivalent |
| `sonnet` | sonnet generator | needs `lex` output `lex.i` |
| `tet2` | Tetris variant | BSD `sgtty.h` |
| `unix.lib` | **source to `LIB/unix.l`** | library build, not a program |
| `x10`, `x10.bk` | X-10 home automation | needs `sys/filsys.h` |
| `fft` | Cooley-Tukey FFT | a **library** — has no `main` |
| `snake`(busy.c) | system-load probe | reads Unix `/dev/kmem` via `a.out.h` |

## Cannot be helped

| archive | why |
|---|---|
| `phan` | **18 corrupt bytes** (all 0xDE) across every source file; substitution is not self-consistent, so it cannot be reconstructed without inventing text |
| `hack` | **damaged in all three copies** — `hack.potion.c` absent, `hack.shknam.c` truncated mid-function |
| `tc` (chart, tc) | `julian()` called but defined nowhere — source incomplete |
| `sc` | source incomplete in every copy (archive copy is binaries+docs only) |
| `curses.vax` | VAX-specific; superseded by `LIB/curses.l` |
| `uq.rom` | **OS-9/68000 boot ROM source** — system-level, removed |
| `atomic` | "Outlaw Labs" bomb-making text — not software |
| `dr.who` | Doctor Who fan text — not software |
| `pcomm`, `indent` | unported Unix shar postings, parts never assembled |
| `dates` | "this day in history" text data (feeds `today`) |
| `srt` | BASIC09 sort routines — OS-9 native, no C build |
| `de` | `deansi` ANSI-escape stripper; test harness only |

## Legacy binaries — `/h2/CMDS/GAMES` (41, dated 1990)

Run, but **require `cio`** and hardcode `/h0/games/...`. 31 still have no
surviving source: `back` `bio` `blackjack` `cribbage` `hack` `hotel` `larn`
`mille` `newsgen` `piano` `poker` `rain` `robots` `suicide{,1,2}` `tt` `ularn`
`valspeak` `worms` and others. Verified working: `rain` `worms` `puz15` `tt`
(Tetris) `newsgen` `piano`.

## Not yet sifted — EFFO, 3094 files

From the Microware OS-9 archive (`microware.com`, category 98/OSK — 419 files
fully inventoried). The EFFO half was untouched before now:

- **10 PD disks, 633 files** — `forth`, `ephem` (astronomy), `sc`+`psc`,
  `xlisp`, a complete `hack` install, FORTRAN kit, **SB-Prolog 2.2**
- **21 forum disks, 2461 files, 459 unique `.c`** — **SDB** symbolic debugger,
  full **C-Kermit** source, a CALC spreadsheet, `tar.c`, `XRF` cross-referencer

Its copies are often better ported than ours: the EFFO `alloca.c` is already
OS-9-adapted (`#ifdef OSK`) and is what made `diff` link.

**Built from EFFO so far:** `yacc` (67396), `SDB` symbolic debugger (59914),
and 7 SNOBOL-style demo programs — of which `rstory2` and `tformat` run while
`blackjak` `poker` `rpoem` `rstory` `stone` build but die at runtime with
`Illegal instruction: 4afc` (a jump into a module header — a bad function
pointer in the shared `pattern.c`, reproducible with and without `-K=2L`).

**Attempted and blocked:** `m4` — Microware's `cpp` aborts (E_PRCABT) on
`input.c` and `macro.c` specifically, while `eval.c` with the same headers is
fine; a preprocessor limit, not a source defect. `zoo`/`fiz` — the header
defining `struct item` is absent and `portable.c` redefines `memset`; we
already ship `lha`, `ar` and `zip`. `CALC` — needs `h_grafik.h`, which exists
nowhere.

**Also built from EFFO:** **`vi`** (148442 — the real vi/ex, ships its own
`ex_OS9.c`), **`sedt`** editor (102954), **`pdraw`** plotting (83120).
`pdraw` needed one source change: `char word[100][MAXCHAR]` as a *local* is a
100 KB stack frame, past the 16-bit frame offset — made `static`.

**Still unexamined in EFFO:** ncurses (44 `.c`), UNAXCESS BBS (16),
7TH_C_CONTEST (11), WOLK (7), and the ~400 remaining loose `.c` files.
`MSFM` is missing its `fmmain.c` and cannot be built.

## Shims written (all in the corpus, none in the emulator)

| shim | why |
|---|---|
| `os9times.c` | `times(2)` — gnuchess times its moves; no CPU accounting in OS-9 C |
| `os9rand48.c` | `rand`/`srand`/`srand48`/`drand48` — `clib` has none, and both `rand.r` and `unix.l` collide with nobs's own `randint` |
| `os9link.c` | `link(2)` as a copy — RBF has no hard links; patch only needs the backup |
| `COMPAT/` | BSD headers OS-9 lacks: `sys/{types,param,file,stat,time,times,wait}.h`, `assert.h`, `pwd.h`, `utmp.h` |
