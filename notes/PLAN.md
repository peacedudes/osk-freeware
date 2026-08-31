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
tools/datatest.py --all --image osk-freeware.dd   # 180 cases, 177 pass
tools/playtest.py --all --image osk-freeware.dd   # 115 tests, 111 pass
tools/ci/run_workflow_locally.sh /tmp/scratch     # the whole GitHub workflow
```

The seven failures are deliberate and each says why in its own file. **One
harness at a time** — they all write to the image and take a lock.

## Where it stands, measured

| | |
|---|---|
| Programs | 935 catalogued |
| Demonstrated running | 871 of 922 — 94.5% (bar: it printed something) |
| Screens | 484 cards; 864 programs run by name on one, the rest credited |
| **Tests that can fail again** | **277** — the other 658 rest on a photograph |
| Source here | 626 (66%) |
| Documented beyond one index line | 603 (63%) |

Re-measured 2026-08-31 after `bush` left the disk. The tools are the
authority, not this table: `tools/gen_screens.py --check`,
`tools/src_census.py disk`, `tools/doc_census.py disk`.

Read the second column carefully. 94.5% only means "produced output rather
than dying" — `rpn` gets its arithmetic wrong and clears that bar.

---

## The work, in order

### 1. Module-name collisions — the five in REBUILT are done, 27 names remain

Done 2026-08-31: `CMDS/REBUILT/{arc,compress,kermit,screen,VI}` are now
`arc_5.12`, `compress_rebuilt`, `kermit_cio`, `screen_nocio` and `vi_1.0`,
file and module together, with `tools/rename_module.py`. `bush` also left the
disk (a countdown to the end of a 1989 administration). `makeinfo` and
`gnuchess` are NOT done.

**The measurement that mattered.** The plan used to say "ten names in two
directories, eight sharing a module name". Measured per FILE rather than per
name, it is **32 module names over 76 files**. The five above were the ones
the decision covered; the rest fall into three groups:

- **Must not be renamed.** `csl`/`csl020` and `math`/`math881` are Microware
  trap libraries: a program links them BY NAME, and the second of each pair
  exists to answer to that name on another CPU. `MM1/msdrv.901_340` and
  `msdrv_340.901.ms` are two editions of one driver, bound by a descriptor.
- **The gcc passes.** `gcc_cc1plus`, `gpp_cc1plus` and `GCC2/cc1plus` are all
  module `cc1plus`, and the same for `cccp2`, `collect` and `cc2`. They are
  forked by FILENAME, so a compiler run is not misdirected; it is still a
  reason not to load both compilers. Documented in `DOC/STATUS`, not changed.
- **Alternates whose filename is already distinct but whose module is not** —
  about 25 files: `compress_4.0`, `diff_1.1`, `m4_0.5`, `sed_1.06`, `zoo_2.1`,
  the six `gzip*`, `vi.elvis`, `ctags.elvis`, `input.elvis`, `wc.cio`,
  `vi_cio`, `kermit2`, the four `*.070` jpeg tools, `emacs.mm1`, `ephem881`,
  `infocom.tcap`, `lnk.org`. Making each module match the filename it already
  has takes nothing away from the archive and is the obvious next batch.

  **One hazard, found before it bit.** Elvis's wrappers pick their personality
  from the LAST LETTER of `argv[0]` — `alias.c` maps `w`→`-R` (view),
  `t`→`-i` (input), anything else→plain vi. If `argv[0]` comes from the module
  name rather than the filename, renaming `input.elvis`'s module from `input`
  to `input.elvis` ends the letter on `s` and turns it into plain vi. **Measure
  which one OS-9 passes before renaming those three.** `input.elvis` is the
  discriminating test: its file already ends in `s` and its module in `t`.

Still open from the original decision: `makeinfo` (`CMDS` and `GCC139` are
BYTE-IDENTICAL — delete the GCC139 copy) and `gnuchess` (`CMDS` and `GAMES`
are different ports; the CMDS one has siblings `gnuchessn` and `gnuchessr` and
shares their `-x xwndw` usage line, so `gnuchessx` would keep that family
together while leaving GAMES the plain name). `wish` collides by filename
only — `wish` against `B_wish` — and is lowest priority.

### 1a. Gallery cards that photograph a usage line — 40 of them

rdoggett, 2026-08-31: *"Sample output that does nothing more than show the
help is only valuable if the help isn't shown some other way, and there is no
more interesting output from the program to show."*

Measured: 40 of 483 cards are a usage or syntax message and nothing else. Five
are orphans — a card file with no stanza behind it, produced by a bare
play-test run — and 35 come from a sheet stanza that chose `-?` on purpose.

Four are fixed and `hc` is the one worth reading about (below). The remaining
~30 need asking, per program: is there data on this disk it could be run on,
and is its help already in `DOC/`? `logisim` was the pattern — two sample
circuits ship in `DOC/logisim` and the card showed the usage line.

**`hc` was wrong in three places at once**, and is the shape to look for.
`DOC/INDEX` called it a hex calculator, it was filed under Maths &
calculators, and its card ran `echo 1f * 3 + 7 | hc` and photographed the
usage line the invocation earned. It is a text filter: `hc +8 f` indents to
column 8, `hc -11 f` strips back to column 11, `hc -l "> " f` labels every
line. All three are fixed. A card that shows a program failing, captioned as
though the program were at fault, is worse than no card.

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
