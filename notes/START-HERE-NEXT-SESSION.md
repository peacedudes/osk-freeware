# Picking this up cold

**Read `notes/PLAN.md`. It is self-contained and it is the work.**

Everything else in `notes/` is background. You do not need it, and reading it
first is how sessions have historically lost an hour before touching anything.

## The two-minute version

Branch `release-pass-2026-08-21`, never pushed. Tree clean, all seventeen
`check_disk.py` checks green, `osk-freeware.dd` current.

**2026-09-01. Third session. Read the next two sections and you are current.**

| | 2026-08-31 evening | now |
|---|---|---|
| `datatest` cases | 423 | **661** |
| `datatest` families | 24 | **48** |
| `tools/drives` sheets | 41 | **79** |
| `check_disk.py` checks | 17 | **20**, and 14 provably fail on demand |
| Star grid (programs needing `cio`) | 354 | **349** |
| Gallery cards flagged as help- or error-only | 22 | **9** |
| **Programs under no test at all** | 209 | **58** |

### The pattern that paid best: read the disk's own documentation first

Four of the five programs still on the "silent for every invocation" list on
2026-09-01 were explained by a file already on the disk, and nobody had
looked:

- `DOC/README-RUNNING` says `lnk.org`, `for`, `creadoc` and `biory` call
  `F$Link` for `os9lib`, get `E_MNF` and exit printing nothing. **`load
  /dd/CMDS/os9lib` and they work** -- `lnk.org` prints its command line and
  `biory` prompts in German.
- `DOC/macsave/macsave.1` says macsave "reads standard input and silently
  writes the file(s) it contains". Its silence is CORRECT. `macbin` makes the
  MacBinary it wants, and the pair round-trips.
- `DOC/elvrec/elvrec.doc` says a bare `elvrec` lists what is recoverable --
  so its silence means "nothing", and it reads `/usr/preserve/Index`, which
  OS-9 cannot have because a leading `/name` is a DEVICE.
- `DOC/STATUS` already recorded that `mkdict` takes a bus error on its own
  word list.

**`load` is now the answer FOUR times over** -- `readmsg` for printmail,
`vmod_trap` for rxmod, `Graph` for wgen, `os9lib` for the Fortran set.

### What to do next

**Work from `tools/worklist.py --programs --no-test`.** The 75 left are the
awkward residue and they divide into three kinds, so decide which one you
have before spending time on it:

1. **Wrong invocation** -- still the commonest, still worth trying first.
   `dev2`'s eleven "broken" programs were a work-directory collision;
   `calender` "refusing to be redirected" was a corrupted image; `uuencode`
   took four readings of its own usage line and still has none.
2. **Ends the emulator session.** `pgmcrater`, `pbmtobbnbg`, `wysecrack`,
   `cron`, `byteflip`, `top`, `devprc`, `config`, `hist`, `ephem`. A case
   whose session took an exception FAILS by the harness's own rule, and
   that rule is right -- put the finding in `DOC/INDEX` and a drive
   transcript instead.
3. **Wants hardware that is not here** -- the Atari GRAPH demos, the X11
   clients (stopped by the csl skew before they even miss a server), SCSI,
   a Gepard screen. Say which, and stop.

**THE 62 LEFT, ALREADY SORTED, so nobody re-derives it.** All were driven
on 2026-09-01; the transcripts are in `notes/drives/`.

| Why it has no case | Programs |
|---|---|
| **Ends the emulator session** — a case whose session took an exception fails by the harness's own rule, and that rule is right | `splman` `splprt` `lmargin` `pgmcrater` `pbmtobbnbg` `wysecrack` `cron` `byteflip` `top` `devprc` `config` `hist` `ephem` `ephem881` `bincheckr` `oleo` `sdb` `tplot` `yagi` `hexedit` `dfiles` |
| **Full-screen, so it belongs on a card** | `dm` `draw` `emacs.mm1` `umacs` `new_e` `vc` `shuffle` `hinterhalt` `sterm` `adlrun` `scriptmaster` |
| **Wants hardware or a peer that is not here** | `graphsave` `showpic` `aprocs` `sddemo` `rayshade` `msbadblocks` `fileserv` `mailx` `lmail` `rnews` |
| **Silent for every invocation tried** — the honest state is "nothing to assert", and each was tried at least twice | `casefix` `macsave` `mkdict` `mkindex` `vtxtcn` `creadoc` `lnk.org` `makecrc` `crypto` `elvrec` `helpindex` `PrintLabels` `uuexpand` `biory` `florida` `bibtex` |
| **Blocked by the stopped clock, not by itself** | `rcsdiff` `rcsmerge` |
| **No way to see the change** — there is no `procs` on this disk | `pri` |

The first row is the one to be careful with: several of those programs
produce GOOD OUTPUT and then die (`config` prints its whole table, `top`
its heading, `bincheckr` the book's counts). They are not broken in the way
the row title suggests, and `DOC/INDEX` says so for each.

**DO NOT QUOTE "programs with neither a test nor a card" -- IT WAS A BROKEN
MEASUREMENT.** `worklist.py`'s `carded()` read `for'-credited names out of the
wrong key and never matched one, so every program credited on a shared card
counted as uncarded. The 421/97/42 sequence was that bug shrinking, not the
work. Fixed 2026-09-01; `carded()` now means "a card runs it by name", as
`gen_screens` already did. **The backlog to work from is `--no-test`: 209.**

### What this session settled, in one screen

1. **Five more cio casualties rebuilt** -- `printf`, `valspeak`, `unifdef`,
   `ape`, `hexed`. **But the headline is the other twenty-four**: all
   twenty-nine programs the scan named were RUN with real arguments, and
   twenty-four of them were fine. Carrying the call site is not making the
   call. `setfont` looked like a sixth and is not -- a `-qm` rebuild of it
   behaves identically, which is what rules the mismatch out, so the archive
   binary was put back. **A rebuild that changes nothing is the cheap way to
   tell "broken by cio" from "does nothing".**
2. **`printf` was the expensive one.** It dropped every literal before the
   first conversion, so a format with no conversion wrote a ZERO-BYTE file --
   and `misc1`, `misc2`, `misc3` and the four `rcs` sheets all built their
   input that way. Those sheets were measuring their own setup; `nptx` was
   written off as silent on the strength of one. Re-run them.
3. **`ksh -c "cd <dir>; <prog>"` moves the OS-9 data directory.** bash's does
   not, interactively; `sh`'s `chd` does but `sh` cannot fork an absolute
   path. This unblocks the shells chooser and any program reading a bare
   filename.
4. **A bare-name fork resolves against `chx`, and `load` is the fix.**
   `printmail` forks `readmsg` by bare name and was silent everywhere except
   `/dd/CMDS/ELM`; one `load` and it works from anywhere.
5. **WN serves a page.** It is an inetd-style server -- one request in on
   stdin, one response out -- its document root is compiled in as
   `/h0/c/unid/wn_1.14.3/osk` (which is on this disk), and the one thing it
   was missing was an `index.cache`. That now ships. `HTTP/1.0 200 OK`.
6. **`subscribe` and `unsubscribe` both work** and `DOC/INDEX` said neither
   did -- the old measurement used a group that was not in `.newsrc`, which
   both silently leave alone.
7. **`/h0` is now mounted by `datatest.py` and `screenshots.py`** as well as
   `drive.py`. It is the arrangement `notes/DECISION-placement.md` settles
   on, and three of the four harnesses were not doing it.
8. **AN `OS9Hx` DEVICE PATH MUST BE ABSOLUTE.** With `--image
   osk-freeware.dd` -- a bare relative name, which is what `--all` was
   documented to take -- the device mounts, MODULE LOADING WORKS, and
   ordinary file opens on it silently fail. The whole WN family went 200 to
   404 on that difference and nothing said why. All four harnesses now
   `abspath` the image.
9. **Three more programs fixed by `load`**, all the same shape as
   `printmail`: `rxmod` wants `vmod_trap`, `wgen` wants the `Graph` user
   trap, and both modules were sitting in the same directory as the program
   all along. **Reach for `load` before believing a program cannot find its
   helper.**
10. **The RCS set is stopped by the CLOCK, not by itself.** `date -t` reads
    2100 and does not advance, so two check-ins land in the same second and
    `ci` refuses the second; `rcsdiff` then has one revision to compare with
    itself. `ci`, `co` and `rlog` work singly.
11. **Two cases asserted TODAY'S DATE** and passed for exactly one day.
    Fixed. If a case names a weekday or a month, it is broken.

**Older, still true:**

Three tools were built first, because the bottleneck was throughput and not
judgement:

| | |
|---|---|
| `tools/drive.py` | run a SHEET of 40 programs with real arguments in ONE emulator session; transcript out. It asserts nothing -- it shows you what came back. The step before a test. |
| `tools/worklist.py` | one row per program: what `DOC/INDEX` claims, the binary's own usage line, card?, test?, driven?, and what KIND of module it is. Every column derived; nothing can go stale. |
| `tools/audit_cards.py` | which gallery cards show a program WORKING and which show only its help text or an error. The old `audit_screens.py` flagged 2 of 407 because its rule could not fire. |

What moved, measured:

| | morning | now |
|---|---|---|
| Programs with neither a test nor a card | 421 | **97** |
| `datatest` cases | 187 | **423** |
| Cards flagged as help-only or error-only | undetectable | 31 found, 11 fixed |

### The three findings worth knowing before you touch anything

**1. `SYS/login` now sets `SHELL=$ROOT/CMDS/ksh`, and that one line fixed
`tex`, `latex`, `eo` and `maketexpk`.** Programs that shell out reach this C
library's `system()`, which forks `$SHELL` with the whole command line as ONE
ARGUMENT -- the way Microware's own shell is invoked. Of the five shells here
only `ksh` parses that; bash reads it as a script filename, `sh` cannot fork
an absolute pathname, `gshell` and `mshell` are menus. `DOC/README-SHELLS` is
the family chooser written out of that measurement.

**2. The eleven programs broken by the cio selector mismatch were REBUILT and
they all work.** `cvtbase`, `cdiff`, `nroff`, `etags`, `yacc`, `xrf`,
`unstr`, `cookhash`, `logisim`, `pagekwic`, `pagefraz` -- built `-qm` from the
sources and recipes already in this repository, installed over the broken
binaries, unstarred, and asserted in `tools/datatests/cio11.cases`. The star
grid went 365 to 354. `tools/rebuild/relink_cio.sh` now REFUSES to relink a
program that `cio_macro_scan.py` names, because `-qixm` links the mismatched
library and that is how `CMDS/REBUILT/kermit_cio` came to be broken.

**3. A dozen `DOC/INDEX` entries described a different program.** `checkfile`
is a cheque-book program, not a C source checker. `paranoia` is a text
adventure, not a floating-point benchmark. `remove` removes MODULES from
memory, not files. `preset` loads terminal function keys. `eo` runs a command
on every line of a file. `dotilde` is the mailer's tilde-escape handler. Each
was found the same way: run the program and read what it says.

## What to do next -- start here, no deliberation needed

**The next batch is Communications/Mail (12) and System & modules/Utilities
(11).** Nine of those twelve mail programs are ALREADY DRIVEN by
`tools/drives/mail.drive`, `mail2` and `mail3`, and eight of the eleven
utilities by `system1` and `system2` -- so re-run the sheet, read the
transcript, and write the cases. That needs no new invocations and no
thinking about what a program is for:

```sh
tools/drive.py mail mail2 mail3          # ~3 minutes, transcripts in notes/drives
tools/worklist.py --programs --no-test --no-card --sub Mail
# then write tools/datatests/mail2.cases from what the transcripts show
```

After that the ones that need real thought are Communications/News (7),
Web server (4) and TCP/IP (4) -- all of which talk to a peer that does not
exist here, so the honest assertion is what each says about its absent
device, not that it works.

`notes/PLAN.md` has the whole picture, and the loop is:

```sh
tools/worklist.py --programs --no-test --no-card   # 97 left
# write a sheet in tools/drives/, run it, read the transcript
tools/drive.py <sheet>
# turn what it settled into a case that can fail again
tools/datatest.py tools/datatests/<family>.cases
```

Then `tools/audit_cards.py` for the 20 cards still flagged.

```sh
OS9EXEC_DIR=~/Developer/os9/os9exec tools/mkimage.sh disk osk-freeware.dd
tools/check_disk.py disk
tools/datatest.py --all          # 423 cases, 3 deliberate failures
```

`disk/` is maintained by hand; `osk-freeware.dd` is a build artefact and is
gitignored. `tools/README.md` explains every tool. `CLAUDE.md` has the rules
and is not optional reading.

## If you only remember four things

1. **OS-9 text files end lines with CR (0x0D), never LF.** An LF-terminated
   file reads as one enormous line and `check_disk.py` will catch it.
2. **Measure, do not infer.** Every proxy tried on this collection has been
   wrong in both directions, usually confidently.
3. **Make every check fail once** before you believe it. This tree has
   produced a remarkable number of checks that could not fail -- including
   one this session: a `cvtbase` case whose only assertion was the absence of
   a word, satisfied by 207 MB of a program on fire.
4. **A program that looks broken usually has the wrong invocation.** Eight
   netpbm converters wrote zero bytes until they were handed a QUANTISED
   image; eleven Dhrystone builds looked mute because they were waiting for a
   run count; `tangle` could not open a `.web` because the file it could not
   open was the absent CHANGE file.

## Where the answers live

| Question | File |
|---|---|
| What should I do next? | `notes/PLAN.md` |
| What still has nothing? | `tools/worklist.py --programs --no-test --no-card` |
| What is this program, and does it work? | `disk/DOC/INDEX`, `disk/DOC/STATUS` |
| How do I actually run it? | `tools/howto.psv` |
| What does it need besides its binary? | `disk/DOC/DEPENDS` |
| Where did it come from, and on what terms? | `disk/DOC/ORIGINS`, `disk/SOURCES.txt` |
| Which of these several similar things do I take? | `DOC/README-VI`, `DOC/README-SHELLS` |
| Which cards are not worth showing? | `tools/audit_cards.py` |
| What did we already try that failed? | `notes/PLAN.md`, last section |
| Why is it like this? | `notes/HISTORY-2026-08.md` |
| What needs rdoggett? | `notes/FOR-RDOGGETT.md` |
