# Handoff — 2026-08-21 (morning)

> **SUPERSEDED by `notes/FOR-RDOGGETT.md`, written later the same day.**
> Most of this still stands. Three claims in it do not, and they are the ones
> a reader is most likely to act on:
>
> - **"Blocked on material that does not exist here — `osklib.r` ... not on the
>   disk, in the SDK, or in the pool."** Wrong on every count. `osklib.r` is a
>   BUILD PRODUCT, `merge`d from 21 objects, and its sources were in the pool
>   the whole time (`SHELLS/pd_ksh.e11.lzh`). The import into
>   `disk/SRC/pdksh/` had dropped the port's entire `OSK/` directory. It is
>   built now. `popen.r` and `netdb.h` were both in `~/Developer/os9/play/`.
> - **"one file, `consio.c`, 25 lines"** understates the uncommitted os9exec
>   change: it is four files and 219 insertions.
> - **`elvis` "has full docs and source on the disk but no binary"** — it has a
>   binary, 111,944 bytes, and it works.
>
> Read `notes/FOR-RDOGGETT.md` first, then `notes/SESSION-2026-08-21.md`.


Read this, then `notes/SESSION-LOG.md` for the commit-by-commit record and
`notes/WORK-QUEUE.md` for what is left. This supersedes the 2026-08-17
handoff; every item on its "pick up here" list is done.

## The one thing that is not committed, and why

**`~/Developer/os9/os9exec` has an uncommitted change** — one file,
`Source/OS9exec_core/consio.c`, 25 lines. That is deliberate.

rdoggett had just released os9exec after weeks of work when this defect turned
up, and asked to hold the commit until the repo has been **fully exercised**,
in case anything else embarrassing is lurking. So: do not commit it, and do
not revert it. If asked to carry on, keep exercising and report; the decision
is his.

What it does — `pConsIn` passed a literal `0` where the path's end-of-record
character belongs:

    return ConsRead( pid,spP, maxlenP,buffer,false, ot->_sgs_eorch );   /* was 0 */

`I$Read`'s `d1.l` is a MAXIMUM, and the v2.4 Technical Reference says the read
ends when "an end-of-record occurs (SCF only)". Without that, a terminal read
waited for the full count, so `ksh` — which asks for 256 bytes per command
line — never saw a single typed command. It repairs `ksh` and `expreserve`,
and nothing else: every program on the disk that reads a terminal was
enumerated (60), and all but three ask for one byte at a time.

Reproduction in 68000 assembly with no library in the way:
`notes/os9exec-iread/ireadt.a`. Full write-up: `notes/OS9EXEC-IREAD.md`.

**Exercised so far, all against that change:**

    make warnings          0 warnings
    make test              195 passed, 0 failed
    make test-notick       ok
    make conformance       44/44, "no unexplained divergence"
    make hammer            4 runs, 4 passed
    CONF68K host + RBF     ok       live-verify corpus   ok
    self-contained disk    ok
    make verify            9 passed, 1 failed, 2 skipped

The single `verify` failure is the **warning sweep's Linux leg, which needs
docker**, and docker is not running here. Proven not to be the change:
stashing it and re-running gives an identical failure. Three of four
toolchains report 0 warnings, 0 errors.

## What this pass did to the disk

`main` is at the merge of 66 commits. All eight `check_disk.py` checks pass,
the image builds at 190M.

**877 of 925 programs run — 94.8%**, from re-running the whole four-stage
sweep, not from adding repairs to an older figure. Thirteen more work but
print nothing or need a condition the sweep cannot create; they are named
individually in `DOC/STATUS` rather than folded into the total. All 48 that do
not run have a documented cause.

Repaired: the whole **RTF Fortran-77 system** (six programs — they wanted
`os9lib` in the module directory), all five **SNOBOL4 games** (they wanted a
syntax file that was on the disk in the wrong place), **devprc** (rebuilt; the
archived module's body was corrupt, not just its CRC), **dir** (a real 68000
bug — `moveq #128` sign-extends to −128), plus `makecrc`, `makedb`,
`bincheckr`, `cron`, `bootlogger`, `read_mail`, `arepdaemon` and the three
spooler programs.

**rdoggett's name is out of every binary** — four removed, one rebuilt, eleven
blanked with `tools/blank_author.py`. `check_disk.py`'s threshold is now ZERO,
not fifteen. Four files still credit him and should: `SRC/misc/qt.c`,
`SRC/zot/zot.c`, `SRC/hc_utils/me.c`, `DOC/zot/zot.1` — that is authorship of
his own 1988–89 work, not an SDK stamp.

## Things you will otherwise rediscover the hard way

- **Never derive the cio star list by searching binaries for `cio`.** It is a
  proxy and it is wrong in both directions: `vi_nocio` contains the string and
  does not need it; `cyberwar`, `gnuchess` and `g` lack it and do need a trap
  handler. Measure by RUNNING every program against an image with the five
  Microware modules removed. The current 367 was measured that way.
- **`DOC/INDEX` holds the star list twice** — a per-program entry line and the
  "All 367" grid — and `check_disk` validates only the grid. Roughly 27 entry
  lines lack a star their program deserves. Fixing it is cosmetic and
  DANGEROUS: a regex over "lines starting with two spaces" also matches lines
  INSIDE the grid, silently creating a program called `*arepdaemon`. I did
  exactly that; check_disk caught it. Exclude the grid region explicitly.
- **A missing path in `DOC/DEPENDS` is usually a compiled-in fallback, not a
  fault.** Nineteen mtools programs list `/dd/sys/mtools` as absent and every
  one works, reading `mtools.conf`. Same for `/dd/SYS/errmsg.short`,
  `/dd/SYS/utmp`, `/dd/TEMP`. The header now says so.
- **A long-running `os9exec` here is probably rdoggett's own open shell.** He
  keeps one. Never kill one you did not start; identify yours by its
  arguments, never by the binary name.
- **Do not hide build output.** `mkimage.sh` refuses to build from a tree that
  fails its checks; `>/dev/null` turns that refusal into a silently stale
  image. It cost this pass a cycle tracing a binary that was never in the
  image.
- **os9exec inside a `while read` loop eats the loop's stdin.** Give it
  `< /dev/null`, or the loop does two rows and then treats data as filenames.
- **os9exec's `-m`/`-M` DO parse.** The old handoff said otherwise; the number
  is simply a SEPARATE argument (`-m 64k prog`, never `-m=64k`).

## Not done, and worth not forgetting

**Blocked on material that does not exist here** — rdoggett confirmed he does
not have any of it:

  - **`osklib.r`** — the only thing stopping a proper **pdksh rebuild**. Its
    `dmakefile` links it; not on the disk, in the SDK, or in the pool.
    `SRC/pdksh/OSK_INCL/` holds what look like its sources. A `lex.c` patch
    that would fix ksh without touching the emulator at all is written up in
    `notes/OS9EXEC-IREAD.md` and cannot currently be built.
  - **`netdb.h`** — blocks relinking `wam.sbprolog`.
  - **`popen`** — blocks relinking `pdraw`; not in the cio-linked library set.
  - `strings.r` — named by four recipes, which turned out not to need it. Now
    only a curiosity.

**Deliberately not fixed, with the reasoning:**

  - **`I$ReadLn` ignores `PD_EOR` too.** The same manual line governs both
    calls and `pConsInLn` passes a hardcoded `CR`. Proved with
    `notes/os9exec-iread/eortest.a`. NOT fixed: it has no victim on this disk
    (everything uses the default CR) and a real downside — `I$ReadLn` is what
    bash, sh and every line-mode read go through, and matching the spec would
    import the manual's own documented hang when `PD_EOR` is zero. os9exec is
    wrong here, but wrong in the safe direction.
  - **The four G-Windows programs** — `cyberwar`, `lfmaker`, `puzzle`,
    `scriptmaster`, Stephen Carville's, copyright line and no distribution
    statement either way. rdoggett has no knowledge of them and said he would
    be guessing. Recorded in `SOURCES.txt`. The question applies to the
    binaries, which predate this pass; their documentation came from the same
    public archive.
  - **`nasa`** wants a NORAD two-line element set. The format is documented in
    `DOC/INDEX` from its own source; no orbital data was invented for it.

**Genuinely impossible here:** seven programs have no source anywhere
(`hotel`, `suicide`, `suicide1`, `suicide2`, `tt`, `ularn`, `wc`); `ls` is a
gcc2 build whose objects Microware's `l68` will not link; `pep` calls an EPROM
programmer's hardware driver; and the nine `Graph`/`VMod` programs need
supervisor state, which os9exec does not implement at all — its module
attribute word is read and returned but never tested for bit 5.

## Where everything lives

`~/mine` is OFF LIMITS entirely. Everything needed moved to `~/Developer/os9/`
on 2026-08-18 — pool, manuals, SDK. `tools/paths.py` is the single place that
knows, and every accessor fails loudly rather than returning an empty
directory. `~/Developer/os9/play` is rdoggett's own play area; tread lightly.

## Standing constraints

  - Commits: rdoggett delegated repo management. Commit per finished unit with
    all eight checks green. **Nothing is pushed to GitHub** — this repo has
    never been uploaded and is not for sharing until he says so.
  - Never `pkill -f os9exec`.
  - OS-9 text files are CR-only. Never call any of this "bootable".
  - Do not write about Microware adversarially. Their concern is SOURCE, not
    binaries: infrastructure in Japan and Germany runs OS-9/68k today and they
    do not want vulnerabilities exposed. That is why permission for the five
    runtime modules was straightforward. `tools/screen_microware.py` screens
    for it and is weighted accordingly.
