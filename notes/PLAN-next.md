# What is left, in order — written 2026-08-22 as rdoggett went to sleep

He said: *"You seem done, yet I feel there is lots more to do."* He is right,
and this is the list. It is ordered so that whoever picks it up — me tonight,
him tomorrow — starts at the top and does not have to decide.

The four capabilities he named are the measure: **findable, live-demoable,
easy to install on a target, easy to install buildable source, documentation
accessible in universe.** Everything below serves one of them.

---

## 1. Write recipes for the 61 source trees that have none  — BIGGEST

`tools/build.sh --missing` lists them. 109 of 170 trees have a recipe, which
is what "we know this compiles" means. The other 61 have never been
established either way, so the collection cannot honestly claim its source is
good.

**Method, per tree, about five minutes each:**

    tools/try_compile.sh <tree> <program>

It makes the naive attempt and classifies the failure against the table in
`tools/rebuild/README.md`. Then either add a recipe to
`tools/rebuild/recipes.psv` or write down why it cannot have one.

**Read `DOC/ORIGINS` first for each tree** — a tree is named by ARCHIVE, not
by program. `SRC/divutils` builds `gen`, `run` and `if`; `toys` builds `wish`.
Guessing `SRC/<program>` finds nothing for most of the disk.

The failure shapes already seen, and their fixes, are in
`notes/COMPILE-VERIFY.md`. Most are: sources named in another tree (reach them
as `../unixlib/bcopy.c`), a file list that is too long (two `main`s) or too
short, a header included as `<foo.h>` when it sits beside the source, or a
function this C library never had.

## 2. Take the counts out of the two docs that still carry them

His instruction, 2026-08-22: *"avoid putting actual numbers of anything in the
docs ... It's a constant update nightmare, just so we can say 99 million
sold."* Done for `disk/readme`, `DOC/README-CIO` and `DOC/README-RUNNING`.
Still to do:

  - **`README.md`** — the GitHub page, ~31 lines carrying numbers.
  - **`DOC/STATUS`** — harder, and worth a moment's thought rather than a
    blind edit. Its numbers ARE its content: it is a dated report of a
    measurement, not a claim about the collection. The honest fix is probably
    to keep them and label the date loudly, or to generate the whole file from
    `tools/verify_combine.py`. **Ask him.**

## 3. The ksh output fault

The alias crash is fixed (`strchr(s,0)` is a bus error here — `osk.h` maps
`strchr` to `index`, and `index(s,0)` returns NULL). A second fault remains:
the FIRST command's output is lost, to a file as well as to the terminal.

Everything known is in `tools/rebuild/pdksh/README.md`, including the decisive
clue: setting `_IONBF` in `io.c` makes each write emit exactly ONE CHARACTER,
which is not a flushing problem but a `FILE` layout one. The next thing to try
is `savefd`/`restfd` around the first command in `exec.c`.

Worth doing because it is the only thing that would make `ksh` work on a
RELEASED os9exec, which is what anybody downloading this will have.

## 4. `adv`

The one tree that got away. Supplying `execv` moves the problem: `adv/main.c`
defines its own `chain`, which collides with `clibn.l`'s `process_a` psect
that `chainc` drags in, and its tree carries three files with `main()`
(`main.c`, `okplay.c`, `test.c`). Both are recipe problems, not missing
library.

## 5. A live-demo affordance

"Simple to live demo" is the one capability with no tool behind it. Today the
answer is "mount it as /dd and type a program name", which is fine but assumes
you know a name worth typing. `about` answers *tell me about X*; nothing
answers *show me something good*.

Cheapest useful thing: a short curated list on the disk — `DOC/START-HERE`, a
dozen programs that demo well with one line each and no setup (`fortune`,
`cookie`, `rain`, `worms`, `hack`, `advent`, `zot`, `bog`...). Generated is
better than hand-written if it can be, but this one is a taste judgement and
probably has to be typed.

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
