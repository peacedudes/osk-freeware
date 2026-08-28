# The plan to finish this disk

Written 2026-08-27, because rdoggett asked the right question: *"what the plan
is to work through all the freeware disk in my lifetime, and if there is no
plan, maybe let's make one now."*

There was no plan. There was a queue and a sweep, and the sweep was measuring
the wrong thing. This is the plan.

## The bar, set by rdoggett

**Every program is proven to DO ITS JOB.** Not "it loaded". Not "it printed
something". Real input producing checked output; interactive programs driven
with the screen read. Where that is impossible here -- no hardware, no
network, no peer -- the program is documented with the reason and with
whatever partial proof can be had.

This is the bar his own spot-checks imply: *"A very small sampling showed more
than half had issues."* Every false pass this collection has produced came
from a cheaper bar than this one.

## Why one-at-a-time cannot finish

834 catalogued programs. 76 have a play-test -- **9%**. At one hand-written
pty script per program the remaining 758 are the lifetime problem, and no
amount of working faster fixes it.

The disk is not 834 separate problems. It is a few families and a residue.

## The tiers, measured not guessed

| Tier | What proves it | Programs | Played | Now |
|------|----------------|---------:|-------:|----:|
| **A — data** | known input → checked output | 390 | 8 | 2% |
| **B — eyes** | driven on a pty, screen read | 138 | 68 | **49%** |
| **C — cannot** | needs hardware or a peer | 65 | 0 | 0% |
| **D — mixed** | argument-level check | 241 | 0 | 0% |
| | | **834** | **76** | 9% |

Tier A is Graphics & images (204, almost all netpbm), Text tools (81),
Archives (35), Files & directories (35), Encoding (26), Maths (9).
Tier B is Games (65), Editors (24), Amusements (23), Shells (20), Screen
toys (6). Tier C is Communications (51) and Printing (14). Tier D is System
& modules (127), Developer tools (46), Compilers (26), Disk & DOS (20) and
the small remainder.

**The lever is that Tier A is a handful of families, not 390 problems.** All
169 netpbm programs share one interface -- PNM in, PNM out -- so one generated
matrix covers them. Archives and encoders prove themselves by round trip:
pack then unpack, encode then decode, compare with the original. That is a
stronger proof than any screen shot, and it is free once the harness exists.

## The blocking prerequisite

**Every sweep this collection has run loaded no modules.** A program that
links a library exits early on `F$Link` and gets recorded on a condition that
cannot occur on a real system. The six RTF Fortran programs sat in the
"silent in every stage" group for weeks for exactly this reason.

So the sweep is redone with `load` first, or none of the numbers below mean
anything. Microware's `load` serves until rdoggett's freeware one lands, for
TESTING ONLY -- see the handoff, item 2. `OS9MDIR` is not a substitute and is
gone from the documentation.

## Order of work

**0. Re-sweep with `load`.** One pass, everything, modules loaded. Expect the
   "silent" group to shrink sharply. Until this is done, `DOC/STATUS` is
   overstating what is broken. *One session.*

**1. `tools/datatest.py` — the Tier A harness.** A test is a table row:
   program, input file, expected property of the output. Properties are
   things a machine can check and a person can trust -- dimensions, pixel
   values, byte-identity after a round trip, line and word counts. It runs
   many programs per emulator start, so 390 programs is minutes, not hours.
   *One session to build, two to populate.*

**2. Tier A, family by family.** netpbm (204) first: it is the largest block,
   the interface is uniform, and three of its tests already exist and pass.
   Then archives (35) and encoders (26) on round trips, then text tools (81)
   against known input, then files (35) and maths (9). *Three sessions.*

**3. Tier B, the remaining ~70.** Hand-written pty scripts, the existing
   `tools/playtest.py`, working `notes/PLAYTEST-QUEUE.md`. This is the tier
   that needs judgment and cannot be generated. 68 are done and the rate is
   roughly 10-15 a session. *Five sessions.*

**4. Tier D, the argument-level sweep.** Most of these are print-and-stop
   utilities where the honest question is "given sensible arguments, does it
   do the thing". Extend the Tier A harness with an arguments column rather
   than writing 241 play-tests. *Two sessions.*

**5. Tier C, documented.** 65 programs that need a modem, a printer, a
   network peer or a second machine. Each gets a named reason and, where
   possible, a partial proof -- a terminal program driven against a pipe
   loopback proves its protocol handling even with no modem. *One session.*

**Fifteen working sessions, give or take.** Not a lifetime. The estimate is
honest about which parts are mechanical and which are not: steps 1, 2 and 4
are the machine's work and scale; step 3 does not scale and is the real floor.

## Progress

**2026-08-27, the day the plan was written.** Step 1 is DONE and step 2 is
started.

  - `tools/datatest.py` exists and works. A family runs in ONE emulator
    start, so 43 netpbm cases take about a minute where 43 play-tests would
    take three hours. It refuses a case that asserts nothing, and it was made
    to fail four different ways before its passes were believed.
  - `tools/datatests/netpbm.cases` -- 43 cases, 42 passing. Eighteen image
    formats are proven to round-trip PIXEL FOR PIXEL, not merely to keep
    their dimensions. Dimensions were the first version's check and it passed
    all sixteen cases on the day it was written, which is exactly the shape of
    every false pass this collection has produced.

**It found real bugs on its first run, which is the point:**

  - **Nine netpbm programs died with `**** Stack Overflow ****`.** All 169
    netpbm modules ship with the same `M$Stack` of 3072 and these nine want
    more. `tools/set_stack.py` raises the field in place and recomputes the
    CRC -- `M$Stack` is past the 48-byte header so parity is untouched, and
    that is asserted either side of the edit. Five went from broken to
    working; four stopped crashing on input they cannot read and print their
    own diagnostic instead. 16k was tried first and is not enough.
  - **`pnmtosir`/`sirtopnm` do not round-trip.** The image returns the right
    SIZE with its channels rotated over the first half of the pixels -- a
    solid red 4x1 comes back green, green, red, red. Still open, kept as a
    failing case, documented in `DOC/INDEX`. This is the exact failure that
    a dimensions check cannot see, found within an hour of having a check
    that could.

## What this plan refuses to do

- **No credit for "it printed something".** That is the bar that produced
  every false pass in `START-HERE-NEXT-SESSION.md`.
- **No inferring from binaries.** Every proxy tried on this collection has
  been wrong in both directions -- the `cio` string, the module-name match,
  the source-file name. Run it.
- **No test that has never failed.** Each harness gets a deliberate failing
  case before its passes are believed. The `size` directive earned its keep
  that way and `life` at 40x12 is the demonstration.
- **No new dated notes files.** Findings go in `DOC/STATUS`, the handoff, or
  `COMPILE-AUDIT.md`. This file is the plan and gets updated, not superseded.

## How progress is reported

`DOC/STATUS` stays the authority on what works. This file carries the tier
table and it gets re-measured, never hand-edited: the counts above come from
the generated catalogue plus `tools/playtests/`, and any figure typed into
prose here is wrong the day after it is typed.
