# For rdoggett, on your return

One file, one place to look. Branch **`release-pass-2026-08-21`**, off `main`,
nothing pushed. Every commit made with the `check_disk.py` checks green.

Newest first. The 2026-08-21 pass is below the 2026-08-22 one and still
stands — nothing in it was undone.

---

# 2026-08-23 (overnight) — three programs that had never built


**Needs you: one judgement call, at the bottom. Nothing else.**

**`inform`, `djpeg` and `ed` all build now.** None of them ever had. Each was
verified by RUNNING it, not by linking it:

  - **`inform`** — Graham Nelson's Inform compiler, the thing that produced
    everything in `GAMES/INFORM`. `DOC/INDEX` has said for months that our cpp
    aborts on it. It recompiles the collection's own `hellow.inf` to a story
    file **byte-identical to the `hellow.z3` that has shipped since day one.**
  - **`djpeg`** — the JPEG decoder. Verified by round trip against `cjpeg`.
  - **`ed`** — GNU ed. The audit called it an ANSI tree; it is K&R throughout,
    and the de-ANSIfier we run was *destroying* it.

**Two compiler bugs, both measured, both with small reproductions:**

  1. **`cpp` dies on a source line of 513 characters.** That is the whole of
     the "nested macro" bug we have been carrying — nesting is just how a line
     gets long. It explains our own three-file reproduction exactly: the one
     that crashes expands to 542 characters, the two that compile to 270 and
     222. `c68` has a limit too, 1023. **And cpp does not always crash — in
     some shapes it truncates and exits silently**, which is how an earlier
     pass concluded long lines were fine.
  2. **`o68` miscompiles what `c68 -k` emits**, and only in one construct: the
     true arm of `a ? "this" : "that"` on string literals gets an address
     eight bytes wrong. `one ? "Error" : "Warning"` prints `rning`. That is
     what made inform report impossible diagnostics. Ten-case probe; nine
     cases fine.

**Also:**

  - The whole tree still builds: **277 of 280 recipes clean**, the same three
    known failures (`ls`, `pdraw`, `pep`). That is after four changes that
    touch every recipe, so it is a real check, not a formality.
  - **`build.sh` was leaving 228 files in `disk/`** while printing "the tree is
    left as it was found". It had its own stale copy of `tidy.sh`. It calls the
    real one now.
  - **The `strchr(s,0)` grep you wanted is done.** The guidance was too broad:
    `unix.l`'s `strchr` is *correct*; it is `index`, `rindex` and `strrchr`
    that fail on NUL. Only pdksh is exposed and **all six of its sites are
    already patched**. Nothing to do.
  - `mtools` is not a timeout and never was — it is a `gcc2` build like `ls`.
    Settled, off the list.

**The judgement call.** Small source fixes were made in place, each marked with
a comment saying what and why: three ANSI function definitions in `SRC/gtar`,
and one `typedef` guard in `SRC/ed/regex.h`. All four are the OSK porter's own
lines, not upstream code, and the automatic tool cannot do the job without
wrecking the files around them. I took the `jconfig.h` precedent — fix in
place, mark it. **If you would rather source edits lived as patches under
`tools/rebuild/`, say so and I will move them.**

Detail: `notes/CPP-MACRO-CRASH.md` (rewritten), `notes/SESSION-2026-08-23.md`.

---

# 2026-08-23 (evening) — the cpp bug is not what we said it was

**Needs you: one judgement call, below. Nothing else.**

  - **Microware's `cpp` dies on a line of 513 characters.** That is the whole
    bug. It is not "nested macro expansion" — nesting is just how a line gets
    long. Measured, and it explains the three-file reproduction we have been
    carrying: the crashing one expands to 542 characters, the two that compile
    to 270 and 222. `c68` has a limit too, 1023.
  - **`djpeg` builds** — the JPEG decoder, which never has here. Verified by
    decoding, not by linking: compress a test image with `cjpeg`, decompress
    it, the smooth channels come back within about 1 of 255.
  - **`gtar` does not**, but nothing about the preprocessor stands in its way
    now, and the five names still missing are written down.
  - Four headers went into `SRC/COMPAT`, all new names, none able to change
    what an existing build resolves.
  - The disk's JPEG test images are damaged — no byte above 0x7f anywhere in
    any of the three. A 7-bit transfer, long before us. Not worth fixing
    unless you want the IJG self-test to run.

Detail: `notes/CPP-MACRO-CRASH.md` (rewritten), `notes/SESSION-2026-08-23.md`
(second half).

---

# 2026-08-22/23 — the build pass

**Needs you: nothing.** `blarslib` was the one question and you answered it.

**Six lines of what changed:**

  - `ksh` works as shipped, interactively and with `-c`, on os9exec with your
    `I$Read` fix. Nothing os9exec did was wrong all pass.
  - Build recipes went 203 → 277. Last whole-tree run: 271 of 274 clean; the
    three added since are each verified alone but not in a full run.
  - Microware's `cpp` bus-errors on nested macros. **There is a way round it**
    — GNU's `cccp2`, which is in the SDK — and `flex` builds through it.
  - `world`, `patch`, `sonnet` had never compiled for want of one file each,
    and each file was still in the archive it came from.
  - `blarslib` is in, minus thirteen headers that were Microware's. It
    unlocked uucp (26 programs), smail and SB-Prolog. It did **not** unlock
    macutils, which is what I said it would when I asked — that was wrong.
  - Every build used to leave object files in `disk/`, which `mkimage.sh`
    ships. A check refuses that now, and it caught one already committed.

Detail: `notes/SESSION-2026-08-22.md`, `notes/SESSION-2026-08-23.md`.
What is left: `notes/PLAN-next.md`. A cold start:
`notes/START-HERE-NEXT-SESSION.md`.

---

# 2026-08-21 — the repair pass

Detail: `notes/SESSION-2026-08-21.md`. What I was asked and what I decided:
`notes/PLAN-release-2026-08-21.md`.

## 1. Read this first — Microware source was on the shipping disk

**`disk/SRC/msfm`, 21 files of OS-9 file-manager internals — path descriptors,
system globals, process descriptors. I have removed it.**

Byte-identical to EFFO forum disk 12's `SOFTWARE/C/MSFM/SRC`, whose `note.doc`
says:

> Source of original version: Peter Dibble: OS-9 INSIGHTS ... This source code
> is the proprietary confidential property of Microware Systems Corporation,
> and is provided to licensee solely for documentation and educational
> purposes. Reproduction, publication, or distribution in any form to any
> party other than licensee is strictly prohibited.

Three things beyond the removal:

1. **`msfm` was already on the refused list** in `notes/WORK-QUEUE.md` —
   *"Microware's, out of Dibble's OS-9 Insights"*. The MODULE was refused. The
   SOURCE came in by another route and nobody noticed.
2. **The notice was a sibling of the directory somebody copied**, one level up
   from the `SRC/` that was taken, so it stayed behind. The 21 files carry no
   header, no copyright line, nothing.
3. **`tools/screen_microware.py` would have caught it** — it flags 10 of the 21.
   It had only ever been run on candidates before installing them, never over
   what was already on the disk.

`check_disk.py` now has a ninth check, `no unscreened Microware source`, over
`disk/SRC` on the strong rules only. I proved it fires by putting one msfm file
back. Accepted exceptions are in **`tools/screened-src.txt`**, each with a
reason — **please read those and tell me if you disagree**. Most are common
interface headers (`stat.h`, `pwd.h`, the FSF's `getopt.h`), but
`disk/SRC/hc_utils/sys.c` is yours and you would know better than I do.

This is what I would most want a second opinion on before you ship.

---

## 2. Your `/h0` vs `/dd` question — answered

**`/dd`.** Your instinct about `/dd/GAMES` was right, by about five to one.

- **258** programs want the *collection* mounted as `/dd` — their own data is
  here.
- **53** want data at `/h0`.
- 98 more want only `/h0/sys/termcap`, which `TERMCAP` already settles, so they
  do not count either way.

Demonstrated, not just counted: `fortune` prints a fortune as `/dd`, and says
`can't open /dd/GAMES/FORTUNE/fortunes.dat` as `/h0`.

Recommendation: ship as `/dd`, keep the `/h0` hard link (one inode, collects
the 53), steer people away from `/h0`-only — it is the worst of the three and
strands 258 programs. `DOC/README-RUNNING` now says so; arrangement 2 is
marked recommended and arrangement 1's cost is stated honestly (it said "20
programs", it is 174).

Reasoning: **`notes/DECISION-placement.md`**. Measurement:
**`tools/measure_layout.py`**, so you can rerun it rather than trust me.

---

## 3. The missing libraries were not missing

The handoff listed the pdksh rebuild as *blocked on material that does not
exist here*. Every part of that was wrong:

- **`osklib.r` is not a file anybody shipped.** It is a build product,
  `merge`d from 21 objects.
- **Its sources were in the pool all along**, in `SHELLS/pd_ksh.e11.lzh`.
- The import into `disk/SRC/pdksh/` had **dropped the port's entire `OSK/`
  directory** except `OSK/INCL` (renamed `OSK_INCL`). The shipped source could
  not be built by anybody. It is complete now.
- **I built `osklib.r`** — 21 sections, 11 KB.
- **`popen.r` and `netdb.h`** were both in `~/Developer/os9/play/`.
- `strings.r` was already known not to be needed.

**The `ksh` alias crash is FOUND AND FIXED**, and the cause is worth knowing
because it is a trap for anything else built here:

> **`strchr` on this system does not match the terminating NUL.**
> `OSK/DEFS/osk.h` has `#define strchr index`, and `index("print", 0)` returns
> **NULL** — measured with a five-line program, not assumed. `lex.c`'s alias
> path reads the last character of an alias value with
> `strchr(s->str, 0)[-1]`, which is the ANSI idiom for "the end". Here that is
> `NULL[-1]`: a byte read at `$FFFFFFFF`, a bus error, on **every alias
> expansion**. Hence `echo`, `true` and `pwd` dying while `print` and `cd`
> were fine — those three are exactly the aliases `main.c` installs.

With the fix, `ksh -c "x=5; echo x is $x; true; echo status $?"` prints
`x is 5` and `status 0`. **Any `strchr(s, 0)` anywhere in this collection is a
latent bus error** — that is worth a grep some day.

**`ksh` is still not finished**: a SECOND and separate fault loses some stdout
(`print`/`echo` write with `putc` to `shf[1]`; error output goes a different
way and appears). Characterised, with the next thing to try, in
`tools/rebuild/pdksh/README.md`. This only matters if the os9exec fix is never
committed; **ksh works on the collection today**.

Everything in `tools/rebuild/pdksh/README.md`, including a warning worth
having: the port's `fork()` emulation has the child read the parent's address
space through SSM, so a rebuilt ksh may start and still not fork on os9exec.

---

## 4. Things that need YOUR decision

1. **`~/Developer/os9/os9exec` has FOUR modified files, not one.** The handoff
   says *"one file, `consio.c`, 25 lines"*. It is `consio.c` (+127/−13),
   `debug.c`, `filestuff.h`, and `test/Sources/OS9Tests/main.swift` (+101) —
   219 insertions. I have not touched, committed or reverted any of it. But
   the handoff understates what is sitting there.

2. **I replaced your three `keep`/`drop`/`kept` bash scripts with compiled
   modules.** I overwrote them before checking they existed, which was
   careless; I restored them from HEAD and then decided on evidence. The
   evidence: run against a `/dd` that is not the collection — the only case
   `keep` is for — the script version needs `bash` and `/dd/tmp` ON THE
   DESTINATION, has neither, copies nothing, and says almost nothing about
   why. Its own header assumes the collection lives on `/h0`, the premise the
   measurement overturned. Originals kept as `SRC/keep/*.sh`. Reversible.

3. ~~Two headers from the pdksh port were refused as Microware's.~~
   **Reversed, same day, and the reversal is the interesting part.** I refused
   `OSK/DEFS/ioctl.h` and `OSK/DEFS/termios.h` because the screener said they
   matched the SDK. They matched a file under `play/oskBoot` — your WORKING
   BUILD OVERLAY, not a pristine SDK. Neither `ioctl.h` nor `termio.h` exists
   in the pristine tree at all, and no copy of either carries a Microware
   copyright: they are the standard System V definitions, and any two
   expressions of that interface overlap.

   `screen_microware.py` now says **which** SDK a match came from. That one
   change also removes most of the noise from running it over `disk/LIB`,
   where it flagged 113 files, nearly all of them our own `ncurses.l`,
   `libgcc.l` and friends sitting in the overlay. A screen that cries wolf is
   one people stop reading, and this one was close to it.

4. **`CLAUDE.md` is gitignored, and I edited it.** Stale star counts, stale
   `/h0` figures, the `elvis` claim, the missing overlay, the nine checks, and
   the keep/drop section. Those edits live only in the working copy, so they
   are not in the branch you are about to review.

---

## 5. What else changed

**Removed:** `msfm` (above).

**Added — programs:** `passwd` (Matthias Rosenthal's, EFFO forum 5, with
source and his read_me); `dedit` (a reversal decided 2026-08-15 and never
carried out — it is BASIC09 I-code, and its header bytes match `bio` and
`wysetime` exactly); `zoo_2.1` as a REBUILT alternate; `keep`, `drop`, `kept`.

**Added — source, 17 trees, taking coverage from 354 to 406 of 939 (43%):**
`uucpbb` (which `DOC/ORIGINS` had promised for 18 programs since they were
added — there was no such tree), `pdksh/OSK`, `zoo`, `jpeglib`, `macutils`,
`gnuchess`, `ed`, `rcs`, `beav`, `lout`, `gtar`, `pvic`, `smail`, `dm`,
`cnews`, `infoxpress`, `uucp_blars`, `less`.

**Added — documentation:** the `sox` manual (its DOC directory held four audio
samples and no text at all, so the census counted it as documented), the
`msntp` manual, and the full MicroGnuEmacs manual in PostScript and DVI — the
disk ships ghostscript and TeX, so both are readable on it.

**Fixed — tooling:** `tools/rebuild/make_overlay.sh` (the clean `/dd` overlay
had gone missing entirely, and the rebuild machinery was unusable);
`tools/extract_pool.py`, which **silently dropped 16 pool files** and had done
since it was written — `untar` with `ignore_zeros=True` returns zero members
instead of raising, so the not-a-tar fallback never fired. That bug is why the
sox and mg manuals were never found.

**Fixed — documentation.** Every count I could find had drifted. `DOC/INDEX`'s
header contradicted itself in three consecutive sentences. `DOC/README-CIO`
still told people to go and fetch `cio`, months after the five modules started
shipping by Microware's permission — I rewrote it. The readme claimed the
collection ships "with their source"; it is 43%, and it now says so.

---

## 6. Open, in the order I would take them

1. **Read `tools/screened-src.txt`** — six pre-existing strong flags I accepted.
2. ~~`DOC/STATUS` is stale.~~ **DONE.** The full four-stage sweep was re-run
   from scratch: **877 of 926 actual programs, 94.7%**, against the previous
   pass's 877 of 925. The same collection measured again, not a different one.

   `tools/verify_combine.py` is new and produces that number from the four
   stage files — it was hand-work before, so the figure the collection
   advertises most loudly could not be recomputed. It reproduces the previous
   pass's committed result exactly (626 / 211 / 71 / 26 / 17) from the
   previous pass's stage files, which is how I know it is right. It also
   **refuses a stage file left over from an earlier sweep**, and that guard
   earned its place within the hour: stage 4 was killed mid-run and its file
   reverted to the previous pass's, which would have silently produced a
   number that was part one measurement and part another.

   `passwd` is counted separately and said so in `DOC/STATUS`: it went on the
   disk after the sweep began, so it was verified by hand instead.
3. **The ksh alias bug**, if you want the collection self-sufficient on a
   released os9exec.
4. **`APPS/oleo1.6.tar.gz`** is the biggest source gap left — 217 files for
   `oleo` — but it arrives wrapped in a `DEFS/` of 59 files, 27 of which
   overlap the SDK's heavily (`dma68450.h` 100%, `rbf.h` 96%). The sources are
   fine; separating them from the tree is a careful job.
5. **`fpu`** — `NOT-INCLUDED.md` says a grant puts it back in,
   `POOL-ASSESSMENT.md` says it stays out. Two notes disagree. Your call.
6. The four G-Windows programs' licence, still unanswered.
7. **The CI pin is 51 commits behind.** `.github/workflows/build-image.yml`
   pins os9exec to `261b4b69`; `~/Developer/os9/os9exec` HEAD is 51 commits
   past it. The comment says to bump it deliberately, so I have not. Worth
   knowing what it implies: whatever CI builds against is what a person
   downloading a release will effectively be running, and **no released
   os9exec has the `I$Read` fix** — so on a release today, `ksh` is not usable
   interactively. That is the argument for finishing the ksh source rebuild,
   and it is the only thing that would make the collection self-sufficient.

I checked the workflow itself as far as I can without running it:
`tools/gen_catalog.py disk docs/index.html` (the two-argument form CI uses)
works, and `check_disk.py disk` passes. I did not exercise the workflow.
