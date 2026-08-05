# Freeware disk: first triage pass, and where game data should live

2026-07-31. Every OS-9 module on the freeware disk (**161** of them) was
classified two independent ways: statically, by what it references, and
dynamically, by booting it as its own program. Untracked — a working document.

**Read the caveat in "What this pass cannot tell you" before acting on the
problem list.** This run used the freeware tree as a *host-native directory*,
and we already know that medium breaks `stat()` and raw device opens by design.
Some of the failures below are the medium, not the program.

No `make` was run: a concurrent session holds CONF68K and we share one
`./os9exec`.

---

## Where game data should live — answered by measurement, not preference

I scanned all 161 modules for compiled-in absolute paths. **No game on this
disk stores a score file at a hardcoded path.** The premise turns out not to
hold here:

- `advent` opens `advent1.txt` … `advent4.txt` — **relative names, no
  directory**, so they resolve against the process's current data directory.
- `infocom` (a Z-machine interpreter, and it runs) embeds **no** file paths at
  all; the story file is a command-line argument.
- `gnuchess` wants `/h0/usr/src/chess/gnuchess.book` — read-only opening book,
  not scores.

So the OS-9 idiom already covers it: **run each game with `chd` set to its own
directory.** A game writing `scores` then writes it beside its data, and no new
convention is needed. One line in a wrapper procedure file does it.

**If you still want a fixed location, `/dd/GAMES` is the right answer and your
objection to it dissolves.** "It forces that directory onto the boot drive" is
true only if freeware is mounted alongside somebody else's system disk. We
decided freeware ships as its own bootable RBF image — booted that way, `/dd`
*is* the freeware disk, so `/dd/GAMES` lives on the freeware image and touches
nobody's system disk. `GAMES/` already exists there with `ADV/` and `INFORM/`.

**`/h0/games` would be worse.** Inside OS-9 the boot disk is `/dd` by
definition; `/h0` is a naming accident of our host setup and is not guaranteed
to exist on a recipient's machine. Several binaries here already hardcode `/h0`
paths (`/h0/CMDS/pd`, `/h0/usr/src/chess/gnuchess.book`, `/h0/lib/bison.*`) and
every one of those is a defect we inherit, not a pattern to copy.

### The dependency that actually matters is not scores — it is termcap

`/dd/SYS/termcap` (or `/dd/sys/…`, same thing — Microware's *Using Professional
OS-9*: "OS-9 does not distinguish upper case letters from lower case letters")
is referenced by roughly **20** binaries: `less`, `emacs`, `mg`, `me`, `sc`,
`screen`, `beav`, `hexedit`, `vi`, `setterm`, `initvdu`, `launch`, `jargon`,
`gnuchess`, `bash`, `sh`, `infocom.tcap` … A good termcap at that one path is
the highest-leverage file on the whole disk. One is already present in `SYS/`.

**Named but missing on the disk**, so their users will fail: `/dd/TMP`,
`/dd/tmp`, `/dd/TEMP` (`TMP` and `tmp` are the same directory; `TEMP` is a
third, distinct one), and `/h0/CMDS/pd`.

---

## Results

| group | runs | starts & waits | needs cio | problem |
|---|---|---|---|---|
| `CMDS/` (top level, 81) | **54** | 15 | 0 | 12 |
| `CMDS/NEEDCIO/` (63) | 0 | 0 | **63** | 0 |
| `CMDS/NEEDCIO/GCC/` (10) | 2 | 3 | 5 | 0 |
| `CMDS/NONFREE/` (4) | 3 | 1 | 0 | 0 |
| `GAMES/` (2) | 0 | 0 | **2** | 0 |
| root (`ed`) | 0 | 0 | 1 | 0 |

"Starts & waits" is a **success**: the program initialised and blocked for
input. `VI` paints a full screen before waiting. Only the last column is bad.

**The `NEEDCIO/` pre-sort is sound** — 63 of 63 fail exactly as filed, and *no*
top-level command does. Two independent methods agree: 73 modules reference the
`cio`/`csl` trap handler statically, 71 fail with it at runtime.

Six modules are filed wrongly and should move **into** `NEEDCIO/`:
`CMDS/file`, `CMDS/less`, `CMDS/vi_nocio_pv`, `GAMES/ADV/advent`,
`GAMES/ADV/advent0`, and `ed` at the disk root.
`vi_nocio` is a **false alarm** — its own module name ends in "cio", the exact
substring trap the skill warns about; it runs fine.

Six could be promoted **out** of `NEEDCIO/`: `vi_cio` (also misnamed) and five
GCC pieces (`cc1plus`, `cc2`, `cc2plus`, `collect`, `gpp`).

### Gems — 54 top-level commands that run unaided

`as0 as1 as11 as4 as5 aterm basename beav bison date diff dirname file gmake
grep gzip hexedit infocom infocom.tcap join lha ls makeinfo me modbuster
msattrib msbadblocks mscd mscopy msdel msdeltree msformat msinfo mslabel msmd
msmove msrd msread msren mstoolstest mstype mswrite mtools sbreak sc screen
shar tar tree vi_nocio vi_nocio_pv zip zipnote zipsplit`

Plus 15 that start and wait for input: `atob bash bash_new btoa cat cjpeg
compress djpeg kermit md5 setime sh sort upperdir wc`.

Note the 19 `ms*`/`mtools` entries are one package — good coverage, but it is a
single gem, not nineteen.

### Problem list — 9, and most are environment, not the binary

| | |
|---|---|
| `dback` | wants `/d0`, a device that does not exist here |
| `msdir` | wants `/pc1@` — a raw PC device open; nothing to attach |
| `gs33` | needs `gs_init.ps`; it names `/dd/etc/lib/gs33` |
| `jargon` | needs its database (`/h0/vh`) |
| `less` | needs a working termcap — see above |
| `find` | `can't open dir ''` — **suspect the medium**, retest on RBF |
| `ascii`, `t`, `wysetime` | produced nothing at all; need a real look |

---

## What this pass cannot tell you

1. **It ran on a host-native directory.** Raw device opens are refused there by
   design (`E$Unit`, commit `063f8d1`), which is the known cause of
   `stat()`-style failures — `ls: cannot open '.'` was seen from a nested copy
   during this run. **Re-run the whole triage on the RBF image** before trusting
   any single failure. That is the same trap that made CONF68K's t10 pass on one
   medium and fail on the other.
2. **"Runs" means loads, starts, and produces output** — usually a usage
   message. It does not mean the program is correct. It is a floor, not a
   verdict on quality.
3. **Nothing here judges licence or provenance.** `NONFREE/` is separated
   already; `archives/` holds seven `.lzh` sources that were not examined.

## Documentation vs. reality — the disk and its own index have drifted

`readme` and `SOURCES.txt` already contain a thorough command index, provenance
and licence audit from a July 2026 pass. That work is good and should be kept.
But the disk has moved since, and the docs now make claims that are false. A
recipient reads these files first, so shipping them as-is ships wrong
information.

**Shipping bugs, in priority order:**

1. **`startup` is never executed on this disk, so nothing sets `PATH` or
   `TERM` at all.** It is written for Microware's `shell` (`shell /dd/startup`),
   which is deliberately absent; the disk's boot shell is `sh`, and `sh` reads
   `/dd/SYS/profile` — **which does not exist**. Verified: booting
   `os9exec /dd/CMDS/sh` prints "TERM not set, using uEmacs-like defaults".
   Whatever PATH we want has to move into a file `sh` actually reads.
   - Within that dead file, `/dd/CMDS/SHARE` **does not exist** either — both
     `readme` and `SOURCES.txt` still describe `CMDS/SHARE/` as the disk's real
     command set. The commands are in `CMDS/` itself now.
   - Its trailing `/h0/CMDS` is **not** a bug, correcting an earlier reading of
     mine: it is an optional fallback to the user's own SDK disk, and it matches
     the layout decision below (freeware on `/dd`, your real disk on `/h0`). A
     PATH element that is absent simply does not match. Depending on the SDK
     would be wrong; offering it as a last resort is not.
2. **`SOURCES.txt`: "CMDS/ … EVERY ONE verified to run with no Microware module
   present at all."** No longer true — `file`, `less` and `vi_nocio_pv` sit in
   top-level `CMDS/` and die with the trap-handler message. So do
   `GAMES/ADV/advent`, `GAMES/ADV/advent0` and the root `ed`, which means the
   readme's own instruction `chd /dd/GAMES/ADV && advent` **cannot work on this
   disk.**
3. **Documented as `[REMOVED]`, still present:** `wysetime` (my run: produces
   nothing, consistent with the note that it is a Basic09 subroutine module, not
   a program) and `upperdir` (documented as an infinite loop). Either delete
   them or drop the REMOVED label — right now the disk contradicts its index.
4. **`CMDS/BROKEN/` is described but does not exist**; `gsort` and `strcmp`,
   the two entries it was for, are genuinely gone. Just stale text.
5. **`readme` places GCC at `CMDS/GCC/`**; it is at `CMDS/NEEDCIO/GCC/`.
6. **`SOURCES.txt` says gnuchess is "Not shipped"**; three gnuchess binaries are
   present under `NEEDCIO/`.

None of this is hard to fix, and the fix is mostly deletion. But it wants doing
before the image is built, not after — the image freezes whatever is there.

## Suggested next steps

0. **Fix the startup PATH first** — it names a directory that does not exist
   and a licensed SDK disk that will not be there. Nothing else on this list
   matters if the disk boots with a broken PATH.
1. Build the RBF image and re-run this pass against it — it reclassifies an
   unknown number of the 9 problems, and it is the medium we decided to ship.
2. Move the six misfiled `cio` modules; rename `vi_nocio`/`vi_cio`, whose names
   state the opposite of the truth.
3. Create `/dd/TMP` and `/dd/TEMP`, and decide about `/h0/CMDS/pd`.
4. Ship each game in its own directory and launch it via a wrapper that `chd`s
   there. No new path convention required.
