# For rdoggett, on your return — 2026-08-21

One file, one place to look. Branch: **`release-pass-2026-08-21`**, off `main`.
Nothing pushed. Every commit made with all eight `check_disk.py` checks green.
Read `notes/PLAN-release-2026-08-21.md` for what I was asked and what I decided,
and `notes/SESSION-2026-08-21.md` for the running record.

## Read this one first

**Microware's proprietary source was on the shipping disk, and I have removed
it.** `disk/SRC/msfm` -- 21 files of OS-9 file-manager internals: path
descriptors, system globals, process descriptors.

It is byte-identical to EFFO forum disk 12's `SOFTWARE/C/MSFM/SRC`, and that
archive's `note.doc` says:

> Source of original version: Peter Dibble: OS-9 INSIGHTS ... This source code
> is the proprietary confidential property of Microware Systems Corporation,
> and is provided to licensee solely for documentation and educational
> purposes. Reproduction, publication, or distribution in any form to any
> party other than licensee is strictly prohibited.

Three things make this worth your attention beyond the removal itself:

1. **`msfm` was already on the refused list** in `notes/WORK-QUEUE.md` --
   *"Microware's, out of Dibble's OS-9 Insights"*. The MODULE was refused. The
   SOURCE came in by another route and nobody noticed.
2. **The notice was a sibling of the directory somebody copied**, one level up
   from the `SRC/` that was taken, so it stayed behind. The 21 files carry no
   header, no copyright line, nothing. Reading any one of them tells you only
   that it is a file manager.
3. **`tools/screen_microware.py` would have caught it** -- it flags 10 of the
   21 on its SYSTEM SOURCE rule. It had only ever been run on candidates
   before installing them, never over what was already on the disk.

So `check_disk.py` has a ninth check now, `no unscreened Microware source`,
which screens `disk/SRC` on the strong rules only (the NAME rule alone matches
212 files and a check that cries wolf is one nobody reads). Six pre-existing
strong flags are listed with reasons in `tools/screened-src.txt` -- **please
read those six and tell me if you disagree with any**; I judged all six to be
third-party or common-interface code, but `disk/SRC/hc_utils/sys.c` is yours
and you would know better than I do.

I proved the check fires by putting one msfm file back.

This is the item I would most want a second opinion on, and the reason I would
not ship before you have looked.

## Things that need YOUR decision

1. **`~/Developer/os9/os9exec` has FOUR modified files, not one.** The handoff
   says the uncommitted change is *"one file, `consio.c`, 25 lines"*. It is
   actually `consio.c` (+127/-13), `debug.c`, `filestuff.h`, and
   `test/Sources/OS9Tests/main.swift` (+101) — 219 insertions across four
   files. I have not touched, committed or reverted any of it, as instructed.
   But the handoff understates what is sitting there, and you should look
   before deciding.

2. **The star list and the shipped counts disagree with the disk, everywhere.**
   `DOC/INDEX`'s own header contradicts itself in three consecutive sentences
   ("228 programs are starred", "Of the 581 ... 162 are starred", "Of the 499
   ... 125 are starred"). `DOC/README-CIO` says 101 starred; the measured
   figure is 367. `DOC/README-RUNNING` says 444 programs where there are 597.
   I have fixed these by GENERATING them (see below) rather than hand-editing,
   because hand-editing is what let them rot. **Check I have not generated a
   number you disagree with.**

3. **Two headers from the recovered pdksh port were refused as Microware's.**
   `OSK/DEFS/ioctl.h` is byte-identical to the SDK's `DEFS/UNIX/ioctl.h`;
   `OSK/DEFS/termios.h` has every line in the SDK's `termio.h`. I left both
   out of `disk/`. The build uses the SDK's copies, which is normal. Say if
   you would rather ship them — I judged not, and `tools/screen_microware.py`
   agreed, but it is your call and it is reversible.

## The headline: the missing libraries were not missing

The handoff listed the pdksh rebuild as **blocked on material that does not
exist here**, naming `osklib.r`. That was wrong on every count:

  - **`osklib.r` is not a file anybody ever shipped.** It is a build product,
    `merge`d from 21 objects.
  - **Its sources were in the pool all along**, in
    `microware-archive/SHELLS/pd_ksh.e11.lzh`.
  - The import into `disk/SRC/pdksh/` had **dropped the port's entire `OSK/`
    directory** except `OSK/INCL` (renamed `OSK_INCL`). The shipped source
    tree could not be built by anybody. It is now complete.
  - **I built `osklib.r`** — 21 sections, 11 KB.
  - `popen.r` and `netdb.h`, the other two "blockers", were both sitting in
    `~/Developer/os9/play/`. `strings.r` was already known not to be needed.

So the honest summary is: nothing was missing except a directory we dropped on
the way in. Details and the full build recipe: `tools/rebuild/pdksh/README.md`.

**`ksh` itself is not finished.** It builds, links, starts, and runs `cd`,
assignments and `print` — but every command that is an *alias* (`echo`,
`true`, `pwd`) aborts on a null pointer. Four candidate causes are ruled out
by experiment and written down so nobody retests them. This only matters if
the os9exec fix is never committed; **`ksh` already works on the collection**
with that fix in place.

## Your `/h0` vs `/dd` question — answered, with numbers

**`/dd`.** Your instinct about `/dd/GAMES` was right, by about five to one.

  - **258** programs want the *collection* mounted as `/dd` (their own data).
  - **53** want data at `/h0`.
  - 98 more want only `/h0/sys/termcap`, which `TERMCAP` already settles, so
    they do not count either way.

Demonstrated live, not just counted — `fortune` prints a fortune as `/dd` and
says `can't open /dd/GAMES/FORTUNE/fortunes.dat` as `/h0`. Full reasoning and
what it means for `keep` in **`notes/DECISION-placement.md`**; the measurement
is `tools/measure_layout.py` so you can rerun it rather than trust me.

The recommendation is: ship as `/dd`, keep the `/h0` hard link (it costs one
inode and collects the 53), and steer people away from `/h0`-only, which is
the worst of the three arrangements.

## Also worth knowing

- **The `OS9CLEAN` overlay had gone missing.** `tools/rebuild/README.md` listed
  it under "Prerequisites, none of which are in this repo", so it was somebody's
  local directory and it was gone — the whole rebuild machinery was unusable
  until I worked it out again. It is now `tools/rebuild/make_overlay.sh`.
- **`elvis` is not missing.** `CLAUDE.md` and the ROADMAP say it "has full docs
  and source on the disk but no binary". It is on the disk, it is 111,944
  bytes, and it works — draws the screen, loads a file, takes `:q!`. I rebuilt
  it from source to the same size to confirm. Stale note, not a gap.
