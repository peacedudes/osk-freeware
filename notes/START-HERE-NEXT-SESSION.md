# Picking this up cold

**Read `notes/PLAN.md`. It is self-contained and it is the work.**

Everything else in `notes/` is background. You do not need it, and reading it
first is how sessions have historically lost an hour before touching anything.

## The two-minute version

Branch `release-pass-2026-08-21`, never pushed. Tree clean, all fourteen
`check_disk.py` checks green, `osk-freeware.dd` current.

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
