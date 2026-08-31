# Picking this up cold

**Read `notes/PLAN.md`. It is self-contained and it is the work.**

Everything else in `notes/` is background. You do not need it, and reading it
first is how sessions have historically lost an hour before touching anything.

## The two-minute version

Branch `release-pass-2026-08-21`, never pushed. Tree clean, all sixteen
`check_disk.py` checks green, `osk-freeware.dd` current.

**What moved on 2026-08-31, and what did NOT.** Read both halves.

DONE: the maintainer's name came off the shipped disk and the published guide;
`bush` left the collection; module-name collisions went from 32 names over 76
files to 11, all deliberate or one open decision; `DOC/README-KERMIT` and
`DOC/README-GREP` joined `DOC/README-VI`; a fifteenth and sixteenth
`check_disk` invariant landed; and eleven programs were found broken by a
`cio` selector mismatch, root-caused by the os9exec session and written up in
`notes/os9exec-bugs/CIO-SELECTOR-MISMATCH.md`. Roughly a dozen `DOC/INDEX`
entries described a different program than the binary does and were corrected.

**NOT DONE, and this is the work rdoggett actually asked for.** He asked for
every program to be run with real arguments and checked for whether it WORKS;
for its `-?` to be captured and compared against the documentation; and for
screenshots that show a program working rather than its usage line. Against
935 programs, about 50 were driven and 5 cards were replaced. That pass is
barely started. Most of the night went into the `cio` investigation instead,
which was worth doing once but is now finished -- do not reopen it.

**Start with `notes/PLAN.md` item 1a and item 4.** They are the same loop:
take a program, read its entry, run it the way its own usage line says, and
fix whatever disagrees. That loop found every documentation error listed
above. It does not need cleverness and it does not need a sweep -- two
automated detectors were tried on it and both lied, which is recorded.

```sh
OS9EXEC_DIR=~/Developer/os9/os9exec tools/mkimage.sh disk osk-freeware.dd
tools/check_disk.py disk
```

`disk/` is maintained by hand; `osk-freeware.dd` is a build artefact and is
gitignored. `tools/README.md` explains every tool. `CLAUDE.md` has the rules
and is not optional reading.

## If you only remember three things

1. **OS-9 text files end lines with CR (0x0D), never LF.** An LF-terminated
   file reads as one enormous line and `check_disk.py` will catch it.
2. **Measure, do not infer.** Every proxy tried on this collection has been
   wrong in both directions, usually confidently.
3. **Make every check fail once** before you believe it. This tree has
   produced a remarkable number of checks that could not fail.

## Where the answers live

| Question | File |
|---|---|
| What should I do next? | `notes/PLAN.md` |
| What is this program, and does it work? | `disk/DOC/INDEX`, `disk/DOC/STATUS` |
| How do I actually run it? | `tools/howto.psv` |
| What does it need besides its binary? | `disk/DOC/DEPENDS` |
| Where did it come from, and on what terms? | `disk/DOC/ORIGINS`, `disk/SOURCES.txt` |
| Which of these seven similar things do I take? | `disk/DOC/README-VI` is the model |
| What did we already try that failed? | `notes/PLAN.md`, last section |
| Why is it like this? | `notes/HISTORY-2026-08.md` |
| What needs rdoggett? | `notes/FOR-RDOGGETT.md` — currently nothing |
