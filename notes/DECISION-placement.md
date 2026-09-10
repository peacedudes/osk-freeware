# Where the collection should live: `/dd`, not `/h0`

Written 2026-08-21, answering rdoggett's question before he left:

> *"I'm still unclear whether it's better to put the freeware on /h0 (as it
> is) or on /dd (where /dd/GAMES seems to want to live). If it stays on /h0,
> we have to 'keep' things, installing needed files to /dd."*

**Answer: `/dd`.** His instinct about `/dd/GAMES` was right, and it is right
by a factor of five. The measurement is `tools/measure_layout.py`, which
exists so nobody has to take this note's word for it.

## The numbers

`tools/measure_layout.py disk`, over the 943 programs under `CMDS`,
**re-measured 2026-08-29**:

| | programs | was, 2026-08-21 |
|---|---:|---:|
| name no `/dd` path at all | 490 | 492 |
| want **this collection** as `/dd` (its own data files) | **429** | 258 |
| want a real **OS-9 system** as `/dd` (Microware's utilities) | 142 | 304 |
| carry a `/h0` path | 139 | 139 |
| ...of which want only `/h0/sys/termcap` | 97 | 98 |
| ...want other `/h0` data of their own | **54** | 53 |

The two figures that decide it are in bold. **429 programs want the
collection at `/dd`. 54 want data at `/h0`.** Ratio 7.9 to 1.

Re-run 2026-09-01: **431 and 54**, ratio 8.0 to 1 — two more programs' data
resolved here when `SPOOL/uucp/seabass` and the WN `index.cache` were added.
The decision does not move and the shape has been stable for eleven days.
`CLAUDE.md` was still quoting 258 and 53 until that day, which is exactly the
drift this file exists to stop; it now says to run the tool.

THE SHIFT SINCE AUGUST IS THE DISK GETTING BETTER, not the tool changing.
A program counts as "wants this collection" when the `/dd` path it carries
RESOLVES here, so every data file recovered into the tree since -- the SEDT
key files, `SPL/splq`, the vi and ephem data, the cal holidays -- moves
programs out of "wants an OS-9 system" and into "wants this collection".
171 of them have moved. The conclusion is not merely unchanged; it is
stronger than when it was made.

The 98 termcap ones do not count on either side: `SYS/login` exports
`TERMCAP` and they read that first, so they are satisfied wherever the disk
is. The 304 that want a system as `/dd` do not count either -- they want
`/dd/CMDS/shell`, `/dd/CMDS/del`, `/dd/DEFS/sys`, which are Microware's and
are not ours to supply under any arrangement.

The counts split `/dd` references by whether **this disk actually carries the
file**, case-insensitively, because that is the only way to tell "wants our
data" from "wants a system". Without that split `/dd` references look like one
undifferentiated 450 and the question stays unanswerable.

## Demonstrated, not just counted

`fortune` names `/dd/GAMES/FORTUNE/fortunes.dat`.

```
collection as /dd                      collection as /h0, bare system as /dd
-----------------                      -------------------------------------
$ fortune                              $ /h0/CMDS/fortune
When the government bureau's           fortune: can't open
remedies do not match your             /dd/GAMES/FORTUNE/fortunes.dat
problem, you modify the problem...
```

That is the 429 in miniature. Nothing about `fortune` is unusual; it was
picked because its one data file is short to name.

## What this means for `keep`

It **narrows** `keep`'s job rather than removing it, and it changes who it is
for.

`keep` is NOT for running the collection. Running the collection means
mounting it as `/dd`, and then nothing needs keeping -- that is rdoggett's
"curator", use case #2 in `PLAN-keep-drop.md`, and it already works with no
new software at all.

`keep` is for the person who **already has an OS-9 system on `/dd`** and wants
some of this on it. For them the collection is a second disk and `/dd` is
theirs, so:

  - a program with no data (492 of 942) is one file copy;
  - a program wanting our data (429) needs the program **and** the files
    `DOC/DEPENDS` lists, copied to the same `/dd`-relative places;
  - a program wanting `/h0` data (53) needs either a `/h0`, or the data put
    where it looks. `keep` should say so rather than pretend.

So `keep`'s real specification is: *make a program that expects the collection
at `/dd` work on a `/dd` that is not the collection.* That is a sharper thing
to build than "install", and it is what the receipt makes safe.

## The recommendation in full

1. **Ship the collection to be mounted as `/dd`.** `OS9DISK=osk-freeware.dd`.
   This is what os9exec gives you for free -- `/dd` is the root and the home --
   and it is how all 942 programs were tested.
2. **Also mount it as `/h0`** (`OS9H0=` the same image; os9exec mounts one
   image under two names, and the hard link this once prescribed was never
   needed -- 2026-09-10). This collects the 53. It is what the current arrangement already does and it
   should stay.
3. **`/h0`-only is the one arrangement to steer people away from.** It is
   strictly the worst of the three: it strands 429 programs to satisfy 54.
4. **`keep` targets the second case**, someone else's `/dd`, and should be
   written and documented as that.

## What to fix in the shipped documentation

Every count in this area had drifted, in the same direction, because they are
hand-maintained. `DOC/README-RUNNING` says *"Of the 444 programs in CMDS and
CMDS/GAMES"* (it is 597), *"94 of them carry a hardcoded /h0 path"* (111 for
that scope, 139 overall), *"69 ... want just one file"* (84), *"20 programs
read their data from /dd"* (174 for that scope, 258 overall). `CLAUDE.md`'s
"100 / 74 / 37 / 11 / 41" are all stale too, and it already warns the reader to
recount rather than trust it.

They should be **generated**, not corrected -- correcting them just resets the
clock. `tools/measure_layout.py` prints every one.
