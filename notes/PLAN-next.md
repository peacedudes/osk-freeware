# What is left, in order — written 2026-08-22 as rdoggett went to sleep

He said: *"You seem done, yet I feel there is lots more to do."* He is right,
and this is the list. It is ordered so that whoever picks it up — me tonight,
him tomorrow — starts at the top and does not have to decide.

The four capabilities he named are the measure: **findable, live-demoable,
easy to install on a target, easy to install buildable source, documentation
accessible in universe.** Everything below serves one of them.

---

## 1. Write recipes for the source trees that have none  — BIGGEST

`tools/build.sh --missing` lists them, and `tools/build.sh` builds everything
there is a recipe for. As of 2026-08-22 the failures are down to three, each
for a reason that is written down rather than guessed:

  - `flex`  — Microware's `cpp` bus-errors on its nested macros.
    `notes/CPP-MACRO-CRASH.md` has a three-file reproduction.
  - `ls`    — a gcc2 build; K&R `cc` will not take it.
  - `pdraw` — wants X11 headers, which are not here and are not coming.

and three trees that will never have one:

  - `COMPAT` is headers, `unixlib` is a LIBRARY (it has a recipe now, named
    `unix.l` — a first field ending in `.l` builds one), and `rcs` is
    genuinely incomplete: `rcssyn.c`, `rcsrev.c` and `rcsutil.c` are missing
    from the tree AND from `rcs4.lha` in the pool. It is RCS **version 4**
    (Purdue, 1987); GNU's 5.7 files are not drop-in.
  - `pep` calls `standby()` and `init_via()`, which live in the mc EPROM
    programmer's own hardware library. Its own header says it runs only on
    that board.

**What is left is the trees with no recipe at all** — `tools/build.sh
--missing`. Several are known to be out of reach (`homelibr` is C++, `graph`
and `aterm` and `serload` are 68k assembly, `lout` and `ed` are ANSI/gcc,
`deansi` needs a lex runtime, `calc` and `cgrafik` want headers -- h_grafik.h,
graf.h -- that are nowhere on the disk or in the pool). The rest are ordinary
work: read the tree's own makefile for the object list, which has been right
every time a guess was wrong.

**Method that pays:** `tools/try_compile.sh <tree> <program>` for a first
look, then the makefile. `tools/rebuild/README.md` has the failure table, and
it grew six rows on 2026-08-22 — read it before diagnosing anything.

## 2. Take the counts out of the two docs that still carry them

His instruction, 2026-08-22: *"avoid putting actual numbers of anything in the
docs ... It's a constant update nightmare, just so we can say 99 million
sold."* Done for `disk/readme`, `DOC/README-CIO` and `DOC/README-RUNNING`.
Still to do:

  - **`README.md`** — DONE 2026-08-22. Every hand-written count is out; the
    `CATEGORIES` table keeps its numbers because `tools/gen_catalog.py`
    writes them and nobody maintains them by hand.
  - **`DOC/STATUS`** — LEFT ALONE, deliberately, and here is why rather than
    an unanswered question. Its numbers are not a claim about the collection,
    they are the RESULT of a measurement: the file says MEASURED 2026-08-21
    at the top and every figure in it comes from the four stage files that
    `tools/verify_combine.py` reads. Stripping them would leave a report of a
    measurement with the measurement taken out. It does not drift the way
    `readme` and `DOC/INDEX` did, because it is not maintained — it is
    re-measured, and the date says when.

    What it should eventually be is GENERATED, so that the prose and the
    numbers cannot come apart: `verify_combine.py` already computes every
    figure in its tally block. That is a real piece of work (the file is 444
    lines and most of it is explanation) and it is not started.

## 3. The ksh output fault — much less urgent than it looked

**Measured 2026-08-22: the SHIPPED `ksh` works.** Interactively
(`os9exec -r ksh`: typed commands run, assignments and `$`-expansion work,
`exit` exits) and with `-c` (`print one; print two` prints both lines). That is
`disk/CMDS/ksh` unmodified, on os9exec carrying the `I$Read` fix — the fix
rdoggett has said is going to be released.

So the reason the rebuild existed has largely gone. `sh_lex.c.patch` reads the
command line a byte at a time as insurance against an os9exec WITHOUT that fix,
and that release is not going to happen.

What is still true: **our rebuild of ksh loses all output**, and that is a
port defect in the rebuild, not in what ships. `tools/rebuild/pdksh/README.md`
has what was tried on 2026-08-22 and ruled out — the `flushshf` guard and the
`fdopen(fd, "r+")` mode — and names the one probe that would settle the
remaining FILE-layout theory in two lines.

`tools/rebuild/pdksh/build_ksh.sh` now builds it in one command, about four
minutes, so the next attempt is a short loop rather than an afternoon.

## 4. `adv` — DONE 2026-08-22

It was a recipe problem, exactly as suspected, and the answer was where it
always is: the tree's own makefile. `RFILES = main.r init.r io.r done.r
subr.r vocab.r rand.r` — seven of the tree's files, not all of them, which is
why the all-`.c` attempt kept dragging in `okplay.c`'s and `test.c`'s `main`.
`advent` builds.

## 5. blarslib — one decision, and several programs turn on it

`notes/BLARSLIB.md`. Found in the pool, freely distributable by its author's
own words, and blocked only on eight header files in it that are byte
identical to Microware's. That is a provenance call, not a technical one.
Saying yes unlocks `macutils` (five programs), and gives the collection a real
Unix-compat library instead of `tools/rebuild/shims/`.

## 6. A live-demo affordance

"Simple to live demo" is the one capability with no tool behind it. Today the
answer is "mount it as /dd and type a program name", which is fine but assumes
you know a name worth typing. `about` answers *tell me about X*; nothing
answers *show me something good*.

**DONE 2026-08-22** — `disk/DOC/START-HERE`, and `disk/readme` points at it.
A dozen programs that run with nothing set up, grouped by what they do to the
terminal, with the quit key for each (from `notes/quit-keys-verified.txt`, so
they are measured rather than assumed). It is typed, not generated: which
programs demo well is a taste judgement.

Read it and change what you disagree with — that is the point of it being
short.

---

## Standing rules for whoever works this

  - **All ten `check_disk.py` checks green before every commit.** Read the
    output, not the exit code — I committed past a red check twice.
  - **Make every check fail once before believing it.**
  - Branch `release-pass-2026-08-21`. Nothing pushed.
  - Counts belong in generated files, never in prose.
  - `~/Developer/os9/os9exec` has uncommitted changes that are deliberate.
    Do not commit or revert them.
  - rdoggett's own Microware-era system utilities do not ship; porting is not
    authorship. The test is the `rfd` initials in the edition history, not his
    name. See `notes/FOR-RDOGGETT.md`.
