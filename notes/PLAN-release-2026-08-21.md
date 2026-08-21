# PLAN — the release pass, 2026-08-21

rdoggett left for the day and asked for roughly 24 hours of unattended work
aimed at **getting the collection ready to release**. He answered four
questions before going; those answers are the standing authority for this
pass and are recorded here so nobody has to guess later.

| question | answer |
|---|---|
| commits | **Commit freely on a branch.** `release-pass-2026-08-21`. Every commit with all eight `check_disk.py` checks green. Nothing pushed. |
| network | **Read-only fetching allowed** while hunting the missing libraries and freeware gaps. Screen anything fetched before it goes near `disk/`. |
| keep/drop | **Settle the placement question myself and build it.** Blocking since 2026-08-08; no longer blocking. |
| hoard scope | **`tools/paths.py` knows it all** — pool, 68k extras, ARR, manuals, SDK. Re-sweep those, do not go wandering. |

His own words on the layout question: *"I'm still unclear whether it's better
to put the freeware on /h0 (as it is) or on /dd (where /dd/GAMES seems to want
to live)."* That is a real open question and Track D exists to answer it with
measurement rather than taste.

## Tracks

### A — the hoard re-sweep
Every previous pass through this material found things the one before missed,
so this is not busywork. Specifically:

- A1. Inventory every archive in all four trees; find the ones nobody ever
      unpacked (`vi.zip`, `unzip`, `elvis1.7.lzh` and friends are visible from
      the first `ls`), and every archive nested inside another.
- A2. Diff the pool against `disk/` by module name — what did we extract and
      then never install?
- A3. **The missing libraries.** `osklib.r`, `netdb.h`, `popen`, `strings.r`.
      Sweep locally for any `.r`/`.l`/`.h` we do not already have, then go
      looking online.
- A4. `elvis` — full docs and source on the disk, no binary, and
      `elvis1.7.lzh` is sitting in the 68k tree. Close it.

### B — runnability
- B1. Re-run the four-stage sweep and confirm 877/925 still holds after the
      relink work.
- B2. Work the 48 that do not run, in order of how many people would care.
- B3. Re-measure the two counts CLAUDE.md tells you not to trust: the `/h0`
      programs (100) and the TERMCAP-first set (74 known, 69 measured).

### C — keep/drop
Settled placement (see `notes/DECISION-placement.md` when written), `keep.c`
in Microware C, built with `cc -qm=16k -n=keep`, receipt at `/dd/SYS/kept`,
`drop` refusing on a changed CRC. `check_disk` gains a rule.

### D — /h0 versus /dd
Build both arrangements, run the same programs against each, and count what
actually breaks. Answer rdoggett's question with numbers, in
`notes/DECISION-placement.md`.

### E — release polish
The star list's 27 stale entry lines, `DOC/STATUS`, the catalog, the README,
and a version string on the disk (which `kept` wants anyway).

## Rules I am holding myself to

- Make every check fail once before believing it. This collection has produced
  a verifier that reported 20/20 having run nothing.
- Measure, never infer. Every proxy tried on this disk was wrong in both
  directions.
- Never `pkill -f os9exec`; rdoggett keeps his own shell open.
- The os9exec `consio.c` change stays uncommitted and unreverted.
- CR-only text on the disk. Never the word "bootable".
- Nothing adversarial about Microware, ever.

## Log

Running notes go in `notes/SESSION-2026-08-21.md`. Anything needing rdoggett's
decision goes in `notes/FOR-RDOGGETT.md` — one file, so there is one place to
look on return.
