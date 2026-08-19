# Handoff — 2026-08-17

Written before a reboot. Read this, then `notes/SECOND-PASS.md`.

## Where things stand

Everything below is **finished, built and verified**. All eight
`tools/check_disk.py` checks pass, the image rebuilds (192 MB), and the new
docs were read back off the mounted image to confirm they are there.

**The work is staged in git and NOT committed.** That is deliberate — commits
wait for rdoggett's approval. `git status` shows 26 files: 5 modified, 21
added. Nothing is half-done; if the tree looks dirty, that is why.

Proposed commit message (one line, needs approval before use):

    Docs: measured verification of all 949 programs, four stages

HEAD is `b37001c Docs: tick the work queue` on `main`.

## What this session did

Ran **every** program file under `disk/CMDS` and classified the result. The
number that came out is **870 of 925 actual programs running — 94.1%**.

An earlier sweep in this same session claimed **98.2% and was wrong twice**;
both mistakes are written up in `notes/SECOND-PASS.md` under "Read this before
trusting any sweep of this disk". Short version:

1. Filtering out os9exec's `#` lines to isolate program output throws away
   `E_BMID`, `E_NEMOD` and `unintialized User Trap` — the blank remainder then
   scores as OK. **91 programs that do not load were reported working.**
2. Running bare gives a program no TERM and no TERMCAP. `aterm` and `snake`
   take **bus errors** without it and work fine in a login session. A bus error
   is not proof a program is broken.

The four-stage harness that gets it right, run in this order:

    tools/verify_all.sh          -> notes/verify-bare.tsv      (949 rows)
    tools/verify_filters.sh      -> notes/verify-filters.tsv   (281 rows)
    tools/verify_in_session.sh   -> notes/verify-session.tsv   (116 rows)
    tools/verify_usage.sh        -> notes/verify-usage.tsv      (80 rows)

Combined verdicts are in `notes/verify-final.tsv`. Each script's header
comment carries the trap that caught me — do not "tidy" the `#`-line handling,
the `head -c`, or the read-from-a-file loop. `head -c` is what keeps the sweep
at one hour instead of seven.

`tools/module_census.py` is new and answers a question that had never been
asked: **24 of the 949 files in CMDS are not programs.** Running those as
programs proves nothing either way.

## The count, when asked

  - **55 wouldn't run** — measured, grouped by cause in `notes/SECOND-PASS.md`
  - **10 couldn't build**, but only **8 genuinely absent**: `hack`'s binary
    ships and `m4` is on the disk (its other source copy built)
  - **63 total**, two of which are on the disk anyway
  - **Separate list, ~10 items**: `top`, `digclk`, `draw`, `greed`, `suicide`,
    `mail`, `makedb`, `adlrun`, `wn`, `inetd` all score OK in this sweep
    because they start and speak. They fail *later*. **This sweep tests that a
    program starts, not that it finishes.** Nothing here supersedes them.

## Pick up here

In rough order of value:

1. **`ksh`'s interactive loop.** `ksh -c '<commands>'` works completely — for
   loops, variables, `$PWD`. Interactively it prints no prompt and runs
   nothing, on a pty as well as a pipe, with CR, LF or CRLF. A shell you
   cannot type at is the biggest single gap on the disk. `disk/SYS/profile.ksh`
   exists and may never be read; `ENV` is not set by `SYS/login`.

2. **The 28 still-silent programs** listed in `notes/SECOND-PASS.md`. They ran
   without complaint and printed nothing in all four stages. `sysid` is the
   odd one — `sysmax` and `sysmin` from the same suite both print a value.

3. **`devprc`** — bad module CRC (stored `6CF320`, computed `9F16E0`; header
   parity is fine). The EFFO forum-16 copy is byte-identical and equally bad,
   so it shipped that way. Source is now on the disk at `SRC/devprc` and a
   recipe is in `tools/rebuild/recipes.psv`, marked UNTESTED — its makefile
   also wants `getsys.a`, which is 68k assembly.

4. **The five SNOBOL4 games** (`poker`, `blackjak`, `rpoem`, `rstory`,
   `stone`) fail identically: `Illegal instruction: 4afc`, which is control
   jumping into a module header. `rstory2` and `tformat` from the same archive
   both run. One fix, five programs. Source: `SRC/effo_snobol`.

5. **The `fpu` question.** `os9lib` and `config` both execute 68881
   instructions with no coprocessor. That is what Microware's `fpu` is for, and
   the permission obtained covers only cio, math, math881, csl, csl020. The
   earlier decision was "if we don't need them we don't ask" — this is what
   needing them looks like. rdoggett's call, not mine.

6. **`graph` module-name case.** `CMDS/GAMES/graph` is the `Graph' trap
   library. Its module name is lowercase `graph` while the seven programs ask
   for `Graph`; os9exec only found it via a case-insensitive host filename
   lookup, and **real OS-9 matches module names exactly**. Renaming it (M$Name
   string, then CRC and header parity) is doable host-side but unverifiable
   from here.

## Standing constraints, unchanged

  - Commits need rdoggett's approval. Show the checks first.
  - Never `pkill -f os9exec` — other sessions match that pattern.
  - OS-9 text files are CR-only. Never call any of this "bootable".
  - Do not write about Microware adversarially.
  - os9exec's `-m`/`-M` options do not parse in this build (`-m 64k`, `-m64k`
    and `-M64M` all fail with `Error in decimal number` naming the *program*).
    Memory-pressure theories are untested territory as a result.
