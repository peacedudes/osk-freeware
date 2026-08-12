# PLAN: runnability triage — a verdict for every program

Written 2026-08-11. Design agreed with rdoggett; nothing here is built yet.

Lives in `notes/` rather than `docs/` because `docs/` is the published Pages
directory and this is working material, not part of the collection.

## The problem, in rdoggett's words

> I think it's unhelpful to just dump a torrent of maybe they work, maybe you
> know how to make them work, but we don't know... onto anyone.

> I don't have a clue how to do anything with any of the programs in graphics.
> Am I missing something? Can I compile and run fortran somehow? How?

The collection is not too big. It is too **silent**. A program that starts,
prints nothing and exits is indistinguishable from one that is broken, and
today nothing on the disk tells the difference. The repo cannot be shared
until that is fixed, because sharing it in this state hands strangers the
same guessing game.

## Goal

Every program carries an honest, measured verdict, and every cluster of
programs ships something you can actually run to see it work.

The shape is a **curated verified core plus a clearly-marked archive tier** —
not "delete everything we cannot fix". Nothing gets dropped for being
obscure; things get dropped only for being genuinely redundant.

**Non-goals.** Rewriting programs. Porting anything. Making interactive
programs testable without a human. Finishing all ~25 clusters before shipping
anything — the work lands cluster by cluster.

## Verdict taxonomy

Five states. Only one of them is failure.

| verdict | meaning |
|---|---|
| **Verified** | Ran against a shipped demo file. Exact steps and real captured output recorded. |
| **Verified, part supplied** | Works once the user brings a Microware piece. We ran it *with* that piece and recorded the steps. |
| **Needs a human** | Interactive or visual. Steps written, awaiting play-test. A temporary state that drains. |
| **Preserved** | Could not be made to do anything. What was tried is written down. Stays, clearly marked. |
| **Not a program** | Data module, library, shell script, BASIC09 I-code. Named so it stops reading as broken. |

**"Verified, part supplied" is load-bearing and was nearly designed out.** An
earlier draft proposed abandoning any cluster needing software not on the
disk, which would have written off Fortran because `for` calls Microware's
`r68`. That is wrong, and it repeats a mistake `CLAUDE.md` already records
about `cc`. The rule is only that the **image build** must not need Microware.
Anyone who wants to compile Fortran on OS-9 has `r68` and `l68`, exactly as
the starred programs assume they have `cio` — `DOC/README-CIO` is already
this convention, and this verdict just generalises it to the SDK.

The 87 starred programs (see pruning, below) all **belong** in this tier, but
none is there yet. What was measured is that they trap *without* `cio` — not
that they work *with* it. Promoting one requires running it with `cio`
supplied and recording the result, the same as any other verdict.

## The unit of work is a cluster

~25 clusters, seeded from `tools/categories.psv` and split where one category
is not one job. NETPBM's 169 programs are a single cluster with a single demo
image; `forth`, `xlisp` and `wam.sbprolog` are three clusters despite sharing
the "Languages" category of three.

Current category tally, for sizing:

```
189 Graphics & images   (169 of them NETPBM)     20 Disk & DOS
 71 Text tools                                   20 Communications
 57 Games                                        20 Archives & compression
 33 Compilers & build                            19 Amusements
 32 System & modules                             18 Editors
 31 Files & directories                          16 Shells
 28 Developer tools                              16 Encoding & conversion
                                                 11 Maths & calculators
                                                 10 Time & calendar
                                                  8 Printing
                                                  6 Screen toys
                                                  4 Documentation
                                                  3 Languages
```

Each cluster produces three things:

1. **A demo file**, shipped in `/dd/DEMO/` — the PGM image, the `.f` Fortran
   source, the Prolog program, the 6805 assembly source.
2. **A recipe** — exact commands, and the real output they produced.
3. **A verdict per program** in the cluster.

## DEMO/ ships on the disk

Decided. The recipes have to work for someone who downloaded the image and
never saw GitHub, which repo-only demo files cannot do.

This is the first content **we author** into a collection that until now was
entirely gathered. It is marked as ours in `DOC/INDEX` and in the directory's
own readme, the same way the five gcc2 rebuilds are marked "REBUILT HERE".

## Recipes are executable

A recipe nobody re-runs rots exactly the way `readme`'s per-directory counts
rotted with nothing to catch it.

- `tools/recipes/<cluster>.sh` — runnable; drives os9exec against the shipped
  `DEMO/` files and diffs against recorded expected output.
- `tools/check_recipes.py` — runs them all.
- **Kept out of `tools/check_disk.py`**, which must stay fast and
  emulator-free. Separate command, separate concern.
- Every recipe is **made to fail once** before it is believed. House rule,
  and this collection has produced four checks that could not fail.

Recipes reach people through channels that already exist: `DOC/HOWTO` on the
disk, `docs/CATALOG.md`, `docs/index.html`. `tools/howto.psv` and its 20
entries are absorbed, not duplicated.

## The human queue

`notes/PLAYTEST-QUEUE.md`, generated from everything marked *needs a human*:
a batched list with exact steps to type. rdoggett runs short sessions against
a pre-narrowed list and reports what happened. No wandering the disk.

## Findings already made, which become work items

Measured during design, not yet acted on.

- **169 NETPBM converters and zero image files.** Not one `.ppm`, `.pgm`,
  `.pbm`, `.gif` or `.jpg` anywhere in the tree. The largest category on the
  disk cannot be demonstrated at all. Plain PBM/PGM/PPM are ASCII, so the fix
  is cheap.

- **The five assemblers are mislabelled in `DOC/INDEX`.** Measured from the
  mnemonic tables in the binaries; genuine 68000 mnemonics score 2/10 in all
  five, which is noise.

  | prog | INDEX says | mnemonics found | real target |
  |---|---|---|---|
  | `as0` | 68000 | `ldaa staa sei tap` | 6800/6802 |
  | `as1` | 68010 | + `abx mul` | 6801/6803 |
  | `as4` | 68040 | `brset brclr clry ldyi`, self-names `gxas4` | 6804 |
  | `as5` | 68050 | `mul brset brclr bhcc` | 6805/68HC05 |
  | `as11` | 68HC11 | + `xgdx idiv pshy` | 68HC11 — the only correct entry |

  The tell was free: **there is no 68050.** Motorola never made one. This is
  the xasm 8-bit cross-assembler suite — a coherent and demonstrable cluster.
  `CLAUDE.md` also tells future sessions `as0`/`as1` are available for
  rebuilding modules; for 68k work that is false and must be corrected.

- **RTF/68K FORTRAN 2.14 (19-May-1987) is on the disk and undocumented.**
  `for` is the driver, `rtf` the compiler, `rtfdat` the data module (loaded
  from `/dd/cmds/rtfdat`, lowercase — worth checking against the uppercase
  `CMDS` on this disk). `for` shells out to `rtf`, then `r68`, then `del`.
  Verdict: *verified, part supplied*. There is no `DOC/rtf` directory.

- **Five `.cio` duplicates should be pruned.** `CMDS/REBUILT/` holds
  `basename.cio`, `cat.cio`, `dirname.cio`, `strings.cio`, `wc.cio` —
  archived builds needing `cio`, beside trap-free gcc2 rebuilds already in
  `CMDS`. `DOC/INDEX` line 761 calls them "superseded by the gcc2 rebuild".
  Shipping the superseded copy *and* labelling it superseded is the problem
  in miniature. Removing them takes the starred count from 92 to 87 and
  changes `DOC/INDEX`, `readme` and `check_disk.py`'s counts.

  The other five in `REBUILT` are **not** this case and are not swept up:
  `arc` and `VI` are different third-party programs that collided on a taken
  name; `compress`, `kermit` and `screen` are our source builds against the
  archive binary in `CMDS`. Genuinely two implementations, one decision each.
  Separately, `REBUILT/VI` is a third PVic build redundant with
  `CMDS/vi_nocio` — probably droppable, needs a look.

- **No Fortran-adjacent language claims survive.** There is no Lua and no
  `f77`; both appear only as words inside third-party manuals. `snobol` is a
  SNOBOL4 pattern-matcher **library for C**, already documented as such.

## First increment: NETPBM

Chosen because it is 169 programs and one demo image — the largest block of
unusable-looking software on the disk, and if the shape works there it works
anywhere.

Scope of the increment:

1. Author a small PGM demo image host-side, plus whatever second format the
   recipe needs to show a conversion round-trip.
2. Ship it in `/dd/DEMO/`.
3. Write `tools/recipes/netpbm.sh`, make it fail once, then make it pass.
4. Capture verdicts for the 169 programs.
5. Surface the recipe in `DOC/HOWTO`, `docs/CATALOG.md` and `docs/index.html`.
6. Rebuild the image; `tools/check_disk.py` green.

The increment is done when a person who has never seen the disk can read one
recipe, type it, and watch an image get converted.

## Risks

- **Demo files are new content in a collected archive.** Mitigated by marking
  them as ours wherever the disk describes itself. Worth a second look if it
  starts to feel like the archive is drifting.
- **169 verdicts from one recipe is a generalisation.** Running one converter
  does not prove the other 168. The recipe must exercise a real sample, and
  the verdict wording must not overclaim — this is exactly the failure mode
  the house rule about checks that cannot fail is guarding against.
- **`check_recipes.py` needs os9exec**, so it cannot run in CI. That is fine
  and matches how the image build already treats the emulator, but it means
  recipe rot is caught locally or not at all.

## Settled during design

- Curated core + marked archive tier, not delete-what-we-cannot-fix.
- Cluster, not per-program.
- Demo files ship on the disk.
- Effort ceiling: a cluster stops when the next step needs software that
  cannot exist, **not** merely software the user must supply.
- CI stays parked. Exercising it requires pushing, and the collection is not
  ready to be pushed.
