# The 90-file corpus: audit and recommendation

Answers the open ROADMAP-68k item *"The old 90-file corpus is untouched and
still manifest-driven. Decide whether it gets converted, mined for claims worth
promoting into CONF68K, or left as-is."*

Written 2026-07-31 while a concurrent session held CONF68K. **Nothing in
`test/68k-conformance/` was read-modified or touched, and `ROADMAP-68k.md` was
left alone** so the two sessions cannot clobber each other. This file is
untracked on purpose — it is a decision aid, not a deliverable.

## What is actually there

`test/68k-live-verification/` holds **98 files**, not 90 — the count in the
roadmap has drifted, which is itself the trend the item exists to stop.

| | count |
|---|---|
| source programs (`.a` / `.bas` / `.c`) | **67** |
| run reports (`.md`) | 26 |
| input data (`.txt`) | 2 |
| covered by `live-verification-manifest.json` | **6** |

## The finding that decides it

**Not one of the 67 sources cites a Microware manual page.** Every one is
written against the skill's `syscall-reference.md` or another `.md` in that
repo. The skill is derived, second-hand, and says so about itself.

CONF68K's whole discipline is the opposite: `DOCS/claims.md` names the manual
page behind every claim, because the suite exists so a *real* OS-9 system can
disagree with the documentation. A claim sourced from our own derived notes
cannot do that job — if the system disagrees, the notes are the first suspect,
not the system.

So **"promote into CONF68K" is not a port.** Each promoted claim needs its
citation re-sourced to the manual and its wording restated against what the
manual actually says. That was the bulk of the work for the six F$Event tests
added today: the code was quick, finding and reading the manual passage was not.

Budget honestly at **~30–45 min per promoted claim**, not minutes.

## The corpus is five different things

### 1. `batch*-01.a` — 13 files, 50 self-reported checks ★ the promotable set

Systematic syscall probes covering roughly 40 calls: F$ID/Time/CmpNam,
Load/Link/UnLink/Fork/Exit/Wait, I$Create/Delete/MakDir/ChgDir/Dup/Seek,
Send/Icpt, SPrior/CRC/SetCRC/GetStt, SigMask/DatMod/Alarm, DFork/DExec/DExit,
ReadLn/STime/Chain, TLink, Julian/Gregor/PrsNam, SRqMem/SRtMem/SRqCMem/CpyMem,
UnLoad/SUser/Sleep, SSpd/Mem/SchBit/AllBit.

They already emit PASS/FAIL themselves — the same shape CONF68K uses — and
**12 of 13 are single-process**, so they are not blocked on the multi-process
harness. Their coverage is almost entirely disjoint from CONF68K's current 18
(file I/O plus F$Event), so this is breadth, not duplication.

**Recommend: mine these, a few claims at a time.** Not a bulk conversion — 50
claims at ~30–45 min each is 25–35 hours. Take them in priority order, newest
manual citation first.

### 2. `dogfood-*` multi-process — 24 files

EOF-lock, lost-update, record-lock, pipes, pre-emption. This is the richest
material in the corpus and it is **exactly what the concurrent CONF68K session
is building the harness for**. Anything here should be decided by that work, not
by this audit — I deliberately did not analyse them further.

**Recommend: defer, and hand this list to whoever owns the multi-process work.**

### 3. `dogfood-*` single-process — 17 files

Mixed. Some are genuine claims (`dogfood-gprdsc-overrun.a` — does F$GPrDsc bound
its copy; `dogfood-sslock.a`; `dogfood-strap-unterminated.a`). Others are
language/toolchain demos (`line-counter`, `basic09calls68k-*`) that were never
claims about OS-9 behaviour.

**Recommend: keep as exploratory dogfood, promote the three or four that state a
real claim** when their area next comes up.

### 4. `dogfood-driver-*` / `dogfood-filemgr-*` — 6 files ★ can never be tested here

Per the `os9-systems-dev` skill: os9exec has **no module dispatch for driver or
file-manager entry points**. `I$Attach` never allocates driver storage or calls
`Init`; device I/O routes through a fixed C table keyed by hardcoded path
prefixes. A correctly-assembled, CRC-valid `Drivr` module installs and is never
invoked.

So these six prove exactly one thing: that the toolchain assembles and links a
byte-correct `Drivr`/`Devic` module. That is a build-artifact claim, not a
behaviour claim, and no amount of harness work changes it.

**Recommend: reclassify explicitly as toolchain artifacts**, so nobody spends a
session trying to make them assert something. Worth a one-line header in each.

### 5. `example-*` — 2 files

`example-fileio.a` and `example-clib.c` are worked examples for the skill's
documentation. They are teaching material that happens to compile.

**Recommend: they belong with the skill repo, not in a test corpus.**

## Recommendation in one line

**Mine, don't convert.** Keep the corpus as the exploratory record it always
was; treat the 13 batch probes as a queue of 50 candidate claims to be promoted
into CONF68K a few at a time with real manual citations; mark the six
driver/file-manager modules as toolchain-only so they stop reading as untested
behaviour; move the two worked examples out.

That ends the "files accumulate faster than checkability" trend without a
25-hour conversion, because it changes what the corpus *is for*: a staging area
with a named exit, rather than an instrument that never became one.

## Cheap follow-up worth doing regardless

The roadmap says 90 files; there are 98. Whatever is decided, the count should
come from `ls`, not from prose — otherwise the next measurement drifts too.
