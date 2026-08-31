# The plan — osk-freeware, from here to releasable

Hand this file to a fresh session. It is self-contained: you do not need the
rest of `notes/`, and you should not read it unless something here sends you
there.

---

## What this is

A curated collection of OS-9/68000 (OSK) community software, published as one
RBF disk image. `disk/` is the tree that gets maintained; `osk-freeware.dd` is
a build artefact, gitignored, never hand-edited.

The point of the collection is that someone can **take part of it onto their
own OS-9 media**. Keep that reader in mind; it decides most questions.

## Get running (two minutes)

```sh
OS9EXEC_DIR=~/Developer/os9/os9exec tools/mkimage.sh disk osk-freeware.dd
tools/check_disk.py disk          # 14 invariants, all must be green
tools/gen_catalog.py disk --check # every program catalogued and categorised
tools/gen_screens.py --check      # no card has drifted from its stanza
```

Longer, and worth running before you claim anything is finished:

```sh
tools/datatest.py --all --image osk-freeware.dd   # 175 cases, 172 pass
tools/playtest.py --all --image osk-freeware.dd   # 115 tests, 111 pass
tools/ci/run_workflow_locally.sh /tmp/scratch     # the whole GitHub workflow
```

The seven failures are deliberate and each says why in its own file. **One
harness at a time** — they all write to the image and take a lock.

## Where it stands, measured

| | |
|---|---|
| Programs | 936 catalogued |
| Demonstrated running | 871 of 922 — 94.5% (bar: it printed something) |
| Screens | 936 have one; 864 are of the program itself |
| **Tests that can fail again** | **277** — the other 659 rest on a photograph |
| Source here | 627 of 945 (66%) |
| Documented beyond one index line | 609 of 945 (64%) |

Read the second column carefully. 94.5% only means "produced output rather
than dying" — `rpn` gets its arithmetic wrong and clears that bar.

---

## The work, in order

### 1. Rename the colliding modules — decided, ready to execute

OS-9 finds a program by MODULE name once it is resident, whatever path you
type. Ten names exist in two directories; eight share a module name too.
Measured: `/dd/CMDS/REBUILT/VI` fills the screen, then `load /dd/CMDS/vi` and
that same path gives the other editor. Nothing warns you.

rdoggett decided: rename ours, never the archive's.

- `CMDS/REBUILT/{arc,compress,kermit,screen,VI}` — builds we made. The archive
  binary keeps the plain name. REBUILT already half-follows this convention:
  `compress_4.0`, `diff_1.1`, `sed_1.06`, `zoo_2.1`, `gtar`, `lharcs`.
- **Rename the module with the file** (`MODNAME=` in `tools/rebuild/recipes.psv`).
  A rename that leaves two modules called `screen` is worse than doing
  nothing — the filenames would promise a distinction that is not there.
- `makeinfo`: `CMDS/makeinfo` and `CMDS/GCC139/makeinfo` are byte-identical.
  Delete the GCC139 copy; it is not a rename job.
- Leave `gcc` and `gpp` (GCC139 vs GCC2): both archive material, in
  directories you choose between, and their own README uses the plain name.
  Document "do not load both".
- `gnuchess` (CMDS vs GAMES) shares a module name — a game belongs in GAMES,
  so drop or rename the CMDS copy. `wish` does not collide as a module
  (`wish` vs `B_wish`); filename only, lowest priority.

Done when: `tools/gen_catalog.py disk` reports no name in two directories
except the ones deliberately left, every check is green, and the affected
INDEX/CATEGORIES/howto entries and sheet stanzas name the new files.

### 2. Family chooser documents — highest value for the stated purpose

Somebody taking part of this onto their own media has to choose between
several of a thing, and should not have to install all of them to find out
how they differ. `DOC/README-VI` was rewritten as the model on 2026-08-30:
a table of hard facts, the reason you cannot keep several (module names), a
short "take this if" per candidate, and a one-line answer for someone who
wants exactly one file.

Families still needing one, roughly in order of how many people care:

- **shells** — bash, sh, ksh, gshell, mshell. Which is the one to take?
- **archivers** — arc/marc/dearc, lha/lharc/xlharc, zoo/booz/fiz, tar/gtar,
  zip/unzip, compress/compr/gzip and its four builds.
- **kermit** — kermit, kermit2, kermit3, xkermit, ckermit.
- **editors beyond vi** — ed, em, me, emacs, umacs, mg, sedt, new_e, beav.
- **grep-likes** — grep, ggrep, fgrep, lgrep, bm, gep.

Everything you need is derivable without running them: size, whether it needs
`cio` (the star in `DOC/INDEX`), module name (collisions), source present
(`tools/src_census.py`), documentation present (`tools/doc_census.py`), and
provenance (`DOC/ORIGINS`). Run the programs only where the table cannot
answer the question.

Done when: each family has a `DOC/README-<family>` that a stranger can act on
without installing anything.

### 3. Tests that can fail again — 659 programs have none

277 of 936 have a data case or a play-test. The rest rest on a photograph
nobody re-checks: if a rebuild broke one tomorrow, only the 277 would notice.

The gap is not uniform. The netpbm set is covered densely as a family (a
round trip through `pnmarith -difference` requiring an all-zero result is a
strong assertion). The games have play-tests. **The thin part is the ordinary
utilities** — text filters, file tools, system commands — where a case costs
about four lines and would catch a real regression.

Write them into the existing families in `tools/datatests/`. Make each new
case fail once before believing it.

### 4. Documentation depth — 336 programs have only an index line

And 815 of 892 index entries carry no dated stamp, meaning nobody has run the
program and checked that the entry describes it. This is where the collection
is thinnest and where its errors have historically been.

**Do not try to bulk-check this.** It was tried on 2026-08-30 by comparing
each entry against its own card: a description and its output naturally share
no words (`cal` prints "August 2026", `banner` prints `@` signs), so the flag
fires on 208 entries and nearly all are fine. Worse, the first cut compared
against whatever card *carried* the program and produced a confident wrong
finding. Go program by program, or find a sharper signal than word overlap.

### 5. Housekeeping

- `notes/` is 7300 lines across 42 files. It was pruned once, at rdoggett's
  request, and has grown back. A finding belongs in the file it belongs to —
  the handoff, `DOC/STATUS`, `COMPILE-AUDIT.md` — not in a new dated file.
- Older prose in `DOC/STATUS` and `DOC/INDEX` still shouts in places. Fix it
  where you are editing anyway; do not do a sweep, an automated pass was
  tried and lower-cased filenames and table labels.

---

## Rules that matter

- **Commit your own work.** rdoggett does not approve commits. The gate is all
  14 `check_disk.py` checks green and the tree left clean. Group related
  changes; no mixed-bag commits. `git add -A` will sweep in unrelated work —
  stage deliberately.
- **OS-9 text files are CR-terminated (0x0D), never LF.** Write with
  `open(p,"wb").write(text.replace("\n","\r").encode("latin-1"))`, and build
  the bytes *before* opening the file — `open(p,"wb")` truncates the moment it
  is evaluated, which emptied `DOC/STATUS` once.
- **Never call the disk "bootable".** os9exec is the kernel; it runs a program
  with this disk mounted as `/dd`.
- **Measure, do not infer.** Every proxy tried here has been wrong in both
  directions. Do not derive the `cio` list from strings in a binary; do not
  derive the `shell` list either (122 modules carry the word because the C
  library links `popen()` into everything).
- **Make every check fail once** before believing it. This collection has
  produced a remarkable number that could not fail.
- **Do not shout.** Section headings in capitals are this collection's
  convention; mid-sentence capitals are not. "It works, with one flaw" — not
  "IT WORKS".
- Microware is a current vendor and this collection supports them. State
  provenance as fact; never write about them adversarially.

## Things already tried that did not work — do not repeat

- Bulk-checking index entries against their cards (see 4).
- An automated pass to lower-case shouting: it lower-cased `DOC/README-FORTRAN`,
  `/dd/SPL/SPLQ` and table labels like `SILENT`.
- Deriving the "needs a shell" or "needs cio" lists from strings in binaries.
- `sh` as a way to `chd` and then run something under os9exec: it cannot
  launch a program at all there — `today: nowhere found` bare, `file not
  found` by absolute path, with PATH set and `chx` done.

## Open with rdoggett

Nothing. The four questions on `notes/FOR-RDOGGETT.md` were answered on
2026-08-30; item 1 above is his decision, waiting only on execution.
