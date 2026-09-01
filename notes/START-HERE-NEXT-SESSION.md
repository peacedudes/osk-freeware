# Picking this up cold

**Read `notes/PLAN.md`. It is self-contained and it is the work.**

Everything else in `notes/` is background. You do not need it, and reading it
first is how sessions have historically lost an hour before touching anything.

## The two-minute version

Branch `release-pass-2026-08-21`, never pushed. Tree clean, all seventeen
`check_disk.py` checks green, `osk-freeware.dd` current.

**2026-08-31, second session. The per-program pass rdoggett asked for is now
the thing that is happening, and it has a shape you can continue.**

Three tools were built first, because the bottleneck was throughput and not
judgement:

| | |
|---|---|
| `tools/drive.py` | run a SHEET of 40 programs with real arguments in ONE emulator session; transcript out. It asserts nothing -- it shows you what came back. The step before a test. |
| `tools/worklist.py` | one row per program: what `DOC/INDEX` claims, the binary's own usage line, card?, test?, driven?, and what KIND of module it is. Every column derived; nothing can go stale. |
| `tools/audit_cards.py` | which gallery cards photograph a program WORKING and which photograph its help text or an error. The old `audit_screens.py` flagged 2 of 407 because its rule could not fire. |

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
