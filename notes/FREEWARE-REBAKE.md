# REBAKE MANIFEST -- modules carrying the SDK author stamp

This is the record of a finished job, kept for the reasoning rather than the
mechanics. The driver scripts it names in passing — `build_games.sh`,
`verify3.sh`, `rebuild_recipes.sh` and the rest — were one-off scripts written
during the run and are **not in this repository**. What was kept is
`tools/rebuild/`: `rebuild.sh`, `verify.sh` and the 203 recipes in
`recipes.psv`. Read that if you want to rebuild something; read this if you
want to know why a binary is the way it is.

`tools/check_disk.py` now fails if more than the 15 documented modules carry
the stamp, so a regression cannot creep back unnoticed.

Every C program built with this SDK links `LIB/cstart.r`, which carries a
64-byte `Author` psect reading:

    >>>>>>>>>>>>>>>>from the disk of Robert Doggett <<<<<<<<<<<<<<<<

A stock Microware `cstart.r` has **no `Author` psect at all** -- verified
against the v12 SDK (`OS9/68000/LIB/cstart.r`, 1409 bytes, clean). The stamp
is an addition to this SDK copy, not a Microware default.

**Decision: rebuild, do not patch.** A patched binary would not match what
anyone else gets compiling the same source, which is the whole point of
shipping the source alongside it.

## The fix for future builds -- already in place

`cc` hardcodes `/dd/LIB/cstart.r`, so the startup module cannot be selected
per build. Instead there is a clean `/dd` overlay at `scratchpad/ddclean`:
symlinks to every entry of `h0` except `LIB`, which is a real directory of
symlinks with all five `cstart*` variants replaced by copies whose `Author`
psect is overwritten with 64 spaces -- same length, nothing relocates.
`h0` is never written to. It also provides the writable `/dd/tmp` flex needs.

    OS9DISK=<scratchpad>/ddclean ./os9exec -r shell

Verified: `hello.c` built through the overlay runs identically and carries no
stamp; against the stamped build only the 64 stamp bytes and the module CRC
differ.

The stock 1409-byte `cstart.r` CANNOT simply be substituted -- this `l68`
rejects it: *"psect 'cstart_a' ... created by assembler too new for this
linker"*. Same refusal for `ansi_cstart.r`. The v12 SDK ships no compiler or
linker to pair with it (it is the OS-9 system distribution: 178 utilities,
`cio`, `csl`), so there is no matched newer toolchain to switch to.

## Scale

| | count |
|---|---|
| modules on the disk | 427 |
| STAMPED -- need rebaking | 224 |
| clean -- arrived prebuilt from others, **do not rebuild** | 203 |
| of the stamped: source tree on the disk | 195 |
| of the stamped: source not yet located | 29 |

## STAMPED with source -- rebuild through the clean overlay (195)

| program | where | source |
|---|---|---|
| advcom | CMDS/GAMES | SRC/advint |
| advent | CMDS/GAMES | SRC/adv |
| advint | CMDS/GAMES | SRC/advint |
| animal | CMDS/GAMES | SRC/animal |
| ape | CMDS | SRC/hc_loose |
| areacode | CMDS | SRC/misc |
| ascii | CMDS | SRC/misc |
| assembler | CMDS | SRC/eff_gshell |
| banner | CMDS | SRC/misc |
| bite | CMDS/GAMES | SRC/v_misc |
| bmgtest | CMDS | SRC/strsch |
| bmgtest2 | CMDS | SRC/strsch |
| bog | CMDS/GAMES | SRC/bog |
| buildhash | CMDS | SRC/ispell |
| bush | CMDS | SRC/misc |
| calen | CMDS | SRC/hc_loose |
| calen | CMDS/REBUILT | SRC/hc_loose |
| calender | CMDS | SRC/calender |
| casefix | CMDS | SRC/hc_loose |
| cdiff | CMDS | SRC/v_misc |
| chksum | CMDS | SRC/chksum |
| clock | CMDS | SRC/misc |
| compiler | CMDS | SRC/eff_gshell |
| compress | CMDS/REBUILT | SRC/hc_utils |
| convert | CMDS/GAMES | SRC/world |
| cookhash | CMDS | SRC/cookie |
| cookie | CMDS | SRC/cookie |
| cpr | CMDS | SRC/cpr |
| cpr | CMDS/REBUILT | SRC/cpr |
| crib | CMDS/GAMES | SRC/crib |
| crypto | CMDS | SRC/crypto |
| cursive | CMDS | SRC/cursive |
| cut | CMDS | SRC/cutpaste |
| cuts | CMDS | SRC/cuts |
| cvtbase | CMDS | SRC/misc |
| dam | CMDS | SRC/effo_wolk |
| des | CMDS | SRC/des |
| dfiles | CMDS | SRC/dfiles |
| diff | CMDS | SRC/diff |
| diff | CMDS/REBUILT | SRC/diff |
| digclk | CMDS | SRC/digclk |
| dinfo | CMDS | SRC/eff_dinfo |
| draw | CMDS | SRC/draw |
| du | CMDS | SRC/eff_du |
| easter | CMDS | SRC/v_misc |
| ediff | CMDS | SRC/eff_ediff |
| editor | CMDS | SRC/eff_gshell |
| england | CMDS | SRC/weather |
| eo | CMDS | SRC/eff_eo |
| etags | CMDS | SRC/eff_etags |
| ff | CMDS | SRC/effo_wolk |
| fibo | CMDS | SRC/eff_bench |
| fillup | CMDS | SRC/fillup |
| find | CMDS/REBUILT | SRC/eff_effind |
| fkeys | CMDS | SRC/eff_fkeys |
| flink | CMDS | SRC/eff_flink |
| float | CMDS | SRC/eff_bench |
| florida | CMDS | SRC/weather |
| fortune | CMDS | SRC/fortune |
| gcl | CMDS | SRC/v_misc |
| gen | CMDS | SRC/divutils |
| georgia | CMDS | SRC/weather |
| gnuchess | CMDS/GAMES | SRC/gnu |
| gothic | CMDS | SRC/gothic |
| greed | CMDS/GAMES | SRC/v_misc |
| gshell | CMDS | SRC/eff_gshell |
| hang | CMDS/GAMES | SRC/hang |
| hc | CMDS | SRC/misc |
| help | CMDS | SRC/eff_help |
| helpindex | CMDS | SRC/eff_help |
| hexed | CMDS | SRC/eff_hexed |
| hist | CMDS | SRC/hist |
| if | CMDS | SRC/divutils |
| ifdef | CMDS | SRC/ifdef |
| indent | CMDS | SRC/indent |
| ispell | CMDS | SRC/ispell |
| japan | CMDS | SRC/weather |
| joke | CMDS/GAMES | SRC/toys |
| kermit | CMDS/REBUILT | SRC/kermit |
| lander | CMDS/GAMES | SRC/lander |
| life | CMDS/GAMES | SRC/life |
| loan | CMDS | SRC/misc |
| lp | CMDS | SRC/eff_lp |
| lpq | CMDS | SRC/eff_lp |
| lprm | CMDS | SRC/eff_lp |
| lpshut | CMDS | SRC/eff_lp |
| ls | CMDS | SRC/ls |
| m4 | CMDS | SRC/eff_m4b |
| make | CMDS | SRC/eff_make |
| makelex | CMDS | SRC/sonnet |
| maze | CMDS/GAMES | SRC/v_misc |
| minnesota | CMDS | SRC/weather |
| mkdict | CMDS/GAMES | SRC/bog |
| mkindex | CMDS/GAMES | SRC/bog |
| mtst | CMDS | SRC/eff_spline |
| name | CMDS | SRC/hc_loose |
| nasa | CMDS | SRC/eff_orbit |
| nchess | CMDS/GAMES | SRC/gnu |
| newsgen | CMDS/GAMES | SRC/toys |
| nobs | CMDS/GAMES | SRC/nobs |
| nroff | CMDS | SRC/nroff |
| nsort | CMDS | SRC/hc_loose |
| orbit | CMDS | SRC/eff_orbit |
| pacman | CMDS/GAMES | SRC/toys |
| paste | CMDS | SRC/cutpaste |
| patch | CMDS | SRC/patch |
| pdraw | CMDS | SRC/effo_pdraw |
| pep | CMDS | SRC/pep |
| printf | CMDS | SRC/misc |
| prjob | CMDS | SRC/eff_lp |
| puz15 | CMDS/GAMES | SRC/v_misc |
| pwgen | CMDS | SRC/misc |
| qp | CMDS | SRC/eff_qp |
| qt | CMDS | SRC/misc |
| queens | CMDS | SRC/ioccc |
| rain | CMDS/GAMES | SRC/toys |
| rdoc | CMDS | SRC/eff_rdoc |
| reagan | CMDS | SRC/reagan |
| remove | CMDS | SRC/eff_remove |
| rendsk | CMDS | SRC/eff_rendsk |
| rndname | CMDS | SRC/rndname |
| roff | CMDS | SRC/eff_roff |
| rot | CMDS | SRC/rot |
| rpn | CMDS | SRC/eff_rpn |
| run | CMDS | SRC/divutils |
| savage | CMDS | SRC/eff_bench |
| scales | CMDS | SRC/hc_loose |
| screen | CMDS/REBUILT | SRC/screen |
| sdb | CMDS | SRC/effo_sdb |
| sed | CMDS | SRC/eff_sed |
| sedt | CMDS | SRC/effo_sedt |
| setfont | CMDS | SRC/effo_wolk |
| shire | CMDS | SRC/weather |
| shuffle | CMDS | SRC/shuffle |
| sieve | CMDS | SRC/eff_bench |
| snake | CMDS/GAMES | SRC/snake |
| snap | CMDS | SRC/snap |
| sokoban | CMDS/GAMES | SRC/sokoban |
| sonnet | CMDS | SRC/sonnet |
| soundex | CMDS | SRC/soundex |
| space | CMDS | SRC/eff_space |
| speech | CMDS | SRC/speech |
| spiff | CMDS | SRC/spiff |
| ssl | CMDS | SRC/effo_wolk |
| strfile | CMDS | SRC/fortune |
| strings | CMDS | SRC/v_misc |
| tar | CMDS/REBUILT | SRC/eff_tar |
| tess | CMDS/GAMES | SRC/tess |
| tet | CMDS/GAMES | SRC/tet |
| time | CMDS | SRC/hc_utils |
| today | CMDS | SRC/today |
| top | CMDS | SRC/eff_top |
| touchtype | CMDS | SRC/touchtype |
| trap | CMDS | SRC/trap |
| tree | CMDS/REBUILT | SRC/eff_tree |
| tttt | CMDS | SRC/hc_loose |
| undel | CMDS | SRC/eff_undel |
| unifdef | CMDS | SRC/hc_utils |
| unstr | CMDS | SRC/fortune |
| uuexpand | CMDS | SRC/v_misc |
| valspeak | CMDS/GAMES | SRC/toys |
| version | CMDS | SRC/version |
| vi | CMDS | SRC/effo_vi |
| vis | CMDS | SRC/vis |
| vtxtcn | CMDS/GAMES | SRC/world |
| wam.sbprolog | CMDS | SRC/sbprolog |
| wanderer | CMDS/GAMES | SRC/wanderer |
| wish | CMDS/GAMES | SRC/toys |
| world | CMDS/GAMES | SRC/world |
| worms | CMDS/GAMES | SRC/toys |
| xc | CMDS | SRC/v_misc |
| xcrypt | CMDS | SRC/xrand |
| xlisp | CMDS | SRC/xlisp |
| xrf | CMDS | SRC/eff_xrf |
| yacc | CMDS | SRC/effo_yacc |
| zot | CMDS/GAMES | SRC/zot |

## STAMPED, source not located (29)

Mostly the disk owner's own earlier builds. Each needs its source found
before it can be rebaked -- or it stays as-is and keeps the stamp.

| program | where | origin |
|---|---|---|
| basename | CMDS | on-original-disk |
| blackjak | CMDS/GAMES | added-by-us |
| cat | CMDS | on-original-disk |
| chardef | CMDS | added-by-us |
| checksum | CMDS | added-by-us |
| chess | CMDS/GAMES | added-by-us |
| dirname | CMDS | on-original-disk |
| hotel | CMDS/GAMES | added-by-us |
| input | CMDS | added-by-us |
| liborder | CMDS | added-by-us |
| logisim | CMDS | added-by-us |
| oskversion | CMDS | added-by-us |
| poker | CMDS/GAMES | added-by-us |
| puzzle15 | CMDS | added-by-us |
| rpoem | CMDS/GAMES | added-by-us |
| rstory | CMDS/GAMES | added-by-us |
| rstory2 | CMDS/GAMES | added-by-us |
| stone | CMDS/GAMES | added-by-us |
| suicide | CMDS/GAMES | added-by-us |
| suicide1 | CMDS/GAMES | added-by-us |
| suicide2 | CMDS/GAMES | added-by-us |
| tformat | CMDS/GAMES | added-by-us |
| tsmon2 | CMDS | added-by-us |
| tt | CMDS/GAMES | added-by-us |
| udate | CMDS | added-by-us |
| ularn | CMDS/GAMES | added-by-us |
| unpacklib | CMDS | added-by-us |
| uwho | CMDS | added-by-us |
| wc | CMDS | on-original-disk |

## Recipe recovery (2026-08-02)

Rebaking is not "re-run the build sweep": the generic builders do not
reproduce the original builds. A pilot over six archives produced 3 modules
out of ~12 expected, the rest failing on unresolved symbols — the originals
used specific file groupings from bespoke scripts (`build_special.sh`,
`build_multi*.sh`, `build_progs.sh`, `build_games.sh`, `build_big.sh`).

**Which builder made which program is recoverable from the build-log NAMES**
in `scratchpad/logs/`, whose prefixes encode the script:

| prefix | script | stamped programs it covers |
|---|---|---|
| `prog_` | build_progs.sh | 66 |
| `single_` | build_singles.sh | 27 |
| `each_` | build_each.sh | 20 |
| `sp_` | build_special.sh | 11 |
| `solo_` | build_solo.sh | 9 |
| `multi_` | build_multi.sh | 9 |
| `game_` | build_games.sh | 9 |

**125 of 224** stamped programs have a log naming them. The other **99 do
not** — their recipe has to be reconstructed from the archive itself before
they can be rebaked.

All 13 build scripts now run through the `ddclean` overlay, so anything they
produce from here on is unstamped.

**Trap:** `timeout` does not exist on macOS; it is `gtimeout`. A sweep using
`timeout` runs to completion in seconds and builds nothing, reporting no error
of its own — every invocation fails with "command not found" into the log.

## Rebake run 2026-08-02 — 83 done, 141 remain

The sweep rebuilt 99 modules through `ddclean`, **all 99 unstamped**. 86 of
them matched a stamped binary on the disk; all 86 were run once before being
trusted, all 86 executed, and **83 replaced their stamped counterpart** (3
were duplicate entries).

    modules on the disk : 631
    still stamped       : 141
    clean               : 490

Two harness bugs worth remembering, both of which produced confident wrong
answers rather than errors:

- `timeout` does not exist on macOS (`gtimeout`). A sweep using it finishes in
  seconds having built nothing.
- `IFS=$"\t"` is bash's locale-translation syntax, NOT a tab — the read loop
  silently never splits, and every lookup misses. Use `IFS=$'\t'`.
- Verifying a rebuilt module by handing os9exec a HOST path reports
  "can't execute" for every single one. all/ has to be mounted (`/h6`) and the
  path translated.

### Still stamped (141)

| program | where |
|---|---|
| assembler | CMDS |
| basename | CMDS |
| bmgtest | CMDS |
| bmgtest2 | CMDS |
| buildhash | CMDS |
| calender | CMDS |
| cat | CMDS |
| cdiff | CMDS |
| chardef | CMDS |
| checksum | CMDS |
| chksum | CMDS |
| clock | CMDS |
| compiler | CMDS |
| crypto | CMDS |
| cursive | CMDS |
| cut | CMDS |
| cuts | CMDS |
| dfiles | CMDS |
| diff | CMDS |
| digclk | CMDS |
| dirname | CMDS |
| draw | CMDS |
| easter | CMDS |
| editor | CMDS |
| england | CMDS |
| fillup | CMDS |
| florida | CMDS |
| fortune | CMDS |
| gcl | CMDS |
| gen | CMDS |
| georgia | CMDS |
| gothic | CMDS |
| gshell | CMDS |
| hist | CMDS |
| if | CMDS |
| ifdef | CMDS |
| indent | CMDS |
| input | CMDS |
| ispell | CMDS |
| japan | CMDS |
| liborder | CMDS |
| logisim | CMDS |
| lp | CMDS |
| lpq | CMDS |
| ls | CMDS |
| m4 | CMDS |
| make | CMDS |
| minnesota | CMDS |
| nroff | CMDS |
| orbit | CMDS |
| oskversion | CMDS |
| paste | CMDS |
| patch | CMDS |
| pdraw | CMDS |
| pep | CMDS |
| puzzle15 | CMDS |
| _…81 more_ | |

## Second and third passes (2026-08-02)

**141 -> 121 stamped.** The three bespoke builders (`build_special.sh`,
`build_games.sh`, `build_multi.sh`) carry their recipes internally rather than
taking an archive argument, so they were missed by the first sweep. Running
them produced 28 builds, 0 failures; 20 matched a stamped binary and all 20
replaced it after verifying they fork.

`lander` rebuilt but came out STILL STAMPED — worth a look; every other build
through `ddclean` came out clean.

### Why the generic sweep failed, by cluster

    76  Symbol 'main' unresolved     a support file built on its own
    55  Symbol 'wrefresh'            curses not linked
    18  Symbol 'tputs'               termlib not linked
    16  missing include
    ..  the rest are archive-specific

`build_each.sh` and `build_solo.sh` linked only `unix.l` and `math.l` —
no `curses.l`/`termlib.l`, though `build_progs.sh` had them all along. Adding
them addresses 73 of the failures in one change.

### A vacuous check, caught

The first verification pass reported **20/20 OK having run nothing**: `tr`
fell out of `PATH` inside the loop, so the captured output was always empty and
the "can't execute" test could never match. `verify3.sh` now uses absolute tool
paths and treats empty output as its own outcome (`NOOUTPUT`) rather than
silently passing. Worth remembering: a verifier whose failure mode is silence
will always agree with you.

## Where the rebake stands: 224 -> 15 (97.6% of the disk is clean)

    modules on the disk   631
    still stamped          15
    clean                 616

The 85-individual-problems estimate above was right about the shape and wrong
about the cost: worked one at a time they were mostly small, and the same few
causes kept recurring. What actually got them:

| cause | fix | examples |
|---|---|---|
| makefile rule lists only the sources *that rule* needs | link every non-`main` `.c` in the tree | sonnet (`compose.c`), wanderer (`scores.c`), kermit (4 of 9), cuts, blackjak, rpoem |
| the archive holds several programs, and a full-source link collides | link `<prog>.c` plus only the non-`main` files | vi (was dragging in `read_mail.c`), poker, stone, if |
| a compat source duplicates something the C library already has | drop it | make (`mktime.c`), xcrypt (`xrand.c`), rndname |
| conditional-compilation defines set wrongly | read the `#ifdef` maze | make (`-DOS9` -- `union wait` is in the `#ifndef OS9` arm), soundex (`-DTESTPROG` supplies `main`), rndname (`-DOSK` *and* `-DSYSV` takes the SYSV arm and then skips the `#ifndef OSK` fallback, so `rnd` gets defined by neither) |
| sources live in a subdirectory | point the build at it | hist (`SRC/`), indent (`eff_indent/SRC`), chess (`CH5`, the only complete variant) |
| a function OS-9's K&R library never had | a small documented shim in `SRC/COMPAT/` or beside the source | patch (`popen`), uwho (`getpwuid` + `geteuid` -- it needs **two**), m4/vis/xc/uuexpand (`egetopt.r`) |
| a header OS-9 does not ship | shim it next to the source, not system-wide | patch (`S_IFREG`: RBF has only files and directories, so "regular" is "not a directory") |

### The 15 that remain, and why

| program | reason |
|---|---|
| `ls` | GNU fileutils, needs `gcc2` rather than `cc`. **CONFIRMED BY MEASUREMENT 2026-08-23**: it compiles with the GCC flag and is WORSE -- fabricated modes, no mtime, and a bus error on `-l`. **`SRC/ls` is the pre-fix tree** -- its `stat()` still fabricates permissions and never sets `st_mtime`, and `isgraph`/`mode_string` are missing entirely. Rebuilding from what ships would regress a program that currently works. |
| `pep` | EPROM programmer; `init_via`, `pgm_byte` and `standby` are in no shipped file. |
| `pdraw` | needs X11 client headers (`X/Xlib.h`); no archive here has them. |
| `basename` `cat` `dirname` `wc` `queens` `wam.sbprolog` `hotel` `suicide` `suicide1` `suicide2` `tt` `ularn` | no source on the disk or in the archive pool. Searched by name and by strings lifted out of the binaries; for `ularn` only its data files survive. |

### Two checks that could not fail

Both were caught because a result looked too good, not because anything errored.

`rebuild_recipes.sh` decides a build succeeded by testing for `R_<prog>` in the
source pool. When the pool moved from the archive tree to the shipped `SRC/`
trees, that test kept pointing at the old path and reported **38 failures out
of 38** while all 38 binaries sat on disk. The mirror image happened in
`verify3.sh`, which maps a host path to an OS-9 one by stripping the pool
prefix: with the prefix wrong it built a nonsense path, every program was
"can't execute", and it reported 23/23 FAIL on 23 good modules. A check that
cannot pass is as useless as one that cannot fail, and neither announces itself.

Also fixed: the shim-retry logic reused the variable `extra`, which by then was
also the recipe's extra-flags field, so the retry passed a host path where a
filename belonged.


## The last fifteen stamps are gone — 2026-08-20

rdoggett asked for his name out of the binaries. All fifteen are clear and
`check_disk.py`'s threshold is now **zero**, not fifteen.

**Four were removed outright** — `basename.nocio`, `cat.nocio`, `dirname.nocio`
and `strings.nocio` were my own trap-free builds, kept in `CMDS/REBUILT` as an
alternative for someone who strips the Microware runtime modules out. Git holds
them at `326dbd7^` if they are ever wanted.

**One was rebuilt** — `queens`, from `SRC/ioccc/baruch.c` against the clean
overlay. 16,932 bytes down to 2,234, same behaviour.

**Eleven were edited in place**, with `tools/blank_author.py`. The Author psect
is DATA, not code, and the replacement is spaces of the SAME LENGTH, so no
offset, relocation or entry point moved; only the CRC changed, and it was
recomputed. CRC and header parity are verified good BEFORE the edit as well as
after, and a module whose CRC was already wrong would have been left alone
rather than have a detectable fault turned into a silent one. `wc` was checked
byte-for-byte against its original output.

    pep  pdraw  wc  wam.sbprolog  ls
    hotel  suicide  suicide1  suicide2  ularn  tt

**Why they could not simply be rebuilt**, which is what the stamp exists to
record:

  - **No source anywhere** — `hotel`, `suicide`, `suicide1`, `suicide2`, `tt`,
    `ularn`, `wc`. Not on the disk, not in the pool, not in the `play` trees.
    CLAUDE.md says `wc`'s source is "on the h0 workshop disk"; `play/h1`,
    `h2` and `he` are image FILES, not directories, so it is not reachable.
  - **`ls`** is a gcc2 build — its `.r` objects carry gcc's `dead face` magic,
    which Microware's `l68` will not link, and `argmatch.c` will not compile
    with the K&R `cc` ("pointer required").
  - **`pdraw`** wants `popen`; the cio-linked library set has no such symbol.
    (Its `plotX.c` also wants X11 headers, but `plotNOX.c` exists for that.)
  - **`wam.sbprolog`** wants `netdb.h`.
  - **`pep`** calls `standby()` and `init_via()` — the EPROM programmer's
    hardware driver, which is not on this disk.

## What was deliberately LEFT

Four files still name him, and should:

    SRC/misc/qt.c        "Robert Doggett, converted to OSK and major rewrite"
    SRC/zot/zot.c        "Heavily mucked with for OSK by Robert Doggett, 1988"
    DOC/zot/zot.1

Those are **authorship credits for his own 1988-89 work**, not an SDK stamp.
Removing them would be stripping attribution, which is the opposite of what
was asked.

Two binaries contain the string "Doggett" by pure coincidence and were not
touched: `CMDS/draw` has it in a name table beside Pig Latin weekdays, and
`GAMES/hack` has it among Irish place names — Skibbereen, Kanturk, Lahinch —
in its random name generator. Doggett is an Irish townland.
