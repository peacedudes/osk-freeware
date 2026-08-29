# Tools

    mkimage.sh          build the disk image from disk/
    mktar.py            write disk/ as a ustar archive (used by mkimage.sh)
    check_disk.py       check the disk tree's invariants
    gen_depends.py      regenerate disk/DOC/DEPENDS
    gen_catalog.py      build docs/index.html, the browsable guide
    measure_layout.py   where the programs expect their files -- /dd or /h0
    doc_census.py       how many programs have documentation
    src_census.py       how many have SOURCE here, and by which route
    screen_microware.py screen a candidate for Microware material BEFORE it
                        goes anywhere near disk/
    screened-src.txt    files under disk/SRC that screen strongly and have
                        been read and accepted, each with the reason
    categories.psv      what each program is FOR -- hand-maintained
    rebuild/            rebuild programs from source (see rebuild/README.md)
    rebuild/make_overlay.sh
                        build the clean /dd overlay those rebuilds need. It
                        was an undocumented local directory until 2026-08-21,
                        when it turned out to be gone
    gen_freeware_index.py

## Checking the tree

    tools/check_disk.py disk

Nine invariants, each of which has been made to fail on purpose:

- no text file contains LF -- OS-9 ends a line with CR alone, and an LF-ended
  file is read as one enormous line
- no UTF-8 on an 8-bit disk -- an em dash written host-side arrives as three
  garbage characters. Legacy 8-bit archive content is left alone, told apart
  by the fact that it does not decode as UTF-8
- no more than the 15 documented modules carry the SDK author stamp
- no editor or host litter (a vim swap file reached the tree once, and
  `mkimage.sh` reads `disk/` off the filesystem, so `.gitignore` cannot stop it)
- every command is named in `DOC/INDEX`
- `DOC/INDEX`'s star grid is self-consistent: it says "All N", lists N
  distinct names, and every one is a real file under `CMDS`.
  **This replaced a check on the counts quoted in `readme` and `DOC/INDEX`.**
  Those counts are gone: rdoggett's instruction, 2026-08-22, was to keep
  numbers out of the prose entirely -- *"Suppose we release the collection,
  and somebody writes sometime later offering us a new trove? It's a
  constant update nightmare, just so we can say 99 million sold."* He is
  right, and the old check was the proof: every removal cost an edit in five
  files. `DOC/CATEGORIES` and the catalogue are GENERATED and can carry
  numbers safely; hand-written prose cannot
- every program has a category in `categories.psv`
- `DOC/DEPENDS` is up to date
- no unscreened Microware source under `disk/SRC`. Added 2026-08-21, when
  `disk/SRC/msfm` turned out to be 21 files of OS-9 file-manager internals
  whose proprietary-confidential notice was a sibling of the directory
  somebody copied, and so stayed behind. Only the STRONG rules count here --
  the NAME rule alone matches 212 files under `disk/SRC`, every `makefile` and
  `string.h` in the collection, and a check that cries wolf is one nobody
  reads

CI runs this before it builds anything. Note the stamp check reads files in
Python on purpose: `grep -r` on this machine is ugrep, which skips binary
files and reports a confident zero.

## Regenerating DOC/DEPENDS

    tools/gen_depends.py disk           # rewrite it
    tools/gen_depends.py disk --check   # exit 1 if it would change

`DOC/DEPENDS` says what each program needs besides its own binary, found by
scanning every binary for `/dd` and `/h0` paths. Run it after adding or
removing anything. It had drifted badly from hand-editing — it listed 110
programs where 158 have dependencies, and attributed one `gnuchess`'s paths to
the other.

## Building the image

    OS9EXEC_DIR=/path/to/os9exec  tools/mkimage.sh disk osk-freeware.dd

Only the **os9exec binary** is needed — not its OS-9 system disk. The build
uses no Microware utility at all, so it runs on a clean machine:

1. os9exec's internal `mount -k` writes the blank image. It is a command of
   the emulator, not an OS-9 program, so it needs no disk to run.
2. `mktar.py` writes `disk/` as a ustar archive, host-side, with the finished
   disk's attributes already in the mode bits.
3. The collection's **own** `tar` extracts it — GNU tar 1.10, unstarred, so it
   runs without `cio`. The disk populates itself.

Because the attributes ride in the archive, there is no `attr` pass. The old
build drove `chx`, `makdir`, `copy` and `attr` out of a licensed system disk;
all four are gone.

`rebuild/` still needs a full Microware SDK — rebuilding a program from source
means running their compiler. That is a separate job from assembling the image
and is not part of a CI build.

## What the build checks

`tar` is run verbosely and the count of extracted files is compared against an
independently taken `find` count. If they disagree the build fails and writes
no image. This is not ceremony: this collection has produced a builder that
reported "copied 3287/3287" while every copy failed and wrote a blank 125 MB
image. Shrink the size argument below the content size to watch the check
fire.

## Two constraints worth knowing

**A volume name cannot contain a space.** OS-9 does not group command-line
arguments with quotes, so `-v=` takes the first word and the rest become stray
arguments. `mkimage.sh` refuses a name with a space rather than let it split.
Override the default with `RBF_VOLNAME`.

**The image is not byte-reproducible, by 352 bytes.** Content is exact and
`mktar.py` output is byte-identical between runs, but RBF stamps a creation
time into LSN0 and into each of the 351 directory descriptors, and those come
from the clock. File contents and file dates are deterministic; tar sets the
latter from the archive.

## Using the result

**Mount it as `/dd`.** That is settled and measured -- 258 programs want the
collection at `/dd` because their own data is here, against 53 that want data
at `/h0`. `notes/DECISION-placement.md` has the reasoning;
`tools/measure_layout.py disk` prints the numbers rather than asking you to
believe them.

Then add `/h0` as well, to collect the 53. os9exec will not mount one host path
as two devices, so hard-link it and one inode has two names:

    ln osk-freeware.dd h0

## The catalogue

    tools/gen_catalog.py disk docs/index.html
    tools/gen_catalog.py disk --check      # exit 1 if a program has no category

`DOC/INDEX` answers "what is this program?" for someone who already knows the
name. It cannot answer "I want a better shell" or "is there anything else like
`rain`?", because it is alphabetical and 700 lines long. `docs/index.html` is
the other view: grouped by purpose, searchable, and every program clickable for
what it needs, where it came from and on what terms.

Everything in it is derived from the disk -- `DOC/INDEX`, `DOC/ORIGINS`,
`DOC/DEPENDS`, the EFFO `info_` files and the tree -- except the category
assignment, which is hand-maintained in `categories.psv`. No rule gets that
right: `stone` calls itself a SNOBOL demo and is a game, `rain` lives in
`CMDS/GAMES` and is not one, and `game` sounds like checkers but carries the
chess piece letters `PNBRQK`.

**GitHub does not render HTML from a repository** -- clicking an `.html` file
shows its source. The workflow publishes `docs/` to GitHub Pages, which needs
Pages enabled for the repo with "GitHub Actions" as the source. Until then that
step is skipped and the file is still readable locally.

## Photographing the programs

    tools/screenshots.py --all       # many programs per emulator session
    tools/playtest.py --all          # one interactive program per session, judged
    tools/gen_screens.py             # docs/screens.js and docs/screens/

`screenshots.py` drives ONE bash session on a pseudo-terminal and runs stanza
after stanza in it, clearing between and keeping the bytes each program wrote.
Eight programs cost about ninety seconds where `playtest.py` costs five
minutes -- it is the right tool when the question is "what does this look
like", and the wrong one when the question is "does it read the keyboard".
It judges nothing: the screens are for the catalogue and a person looks at
them.

A sheet (`tools/screenshots/*.sheet`) is stanzas; `shot` opens one, `run`
types a command, `send`/`keys` type keys, `kill` stops a program while its
first page is still on screen, `for` names the catalogue programs a screen
illustrates, and `cap` is the caption the gallery prints. **One stanza per
program, please** -- two definitions means two captions for one screen and
the gallery picking whichever sheet sorted last, which is how `map' came to
be captioned "the memory map" over a picture of a file's block list.

**Stanzas run top to bottom in one session, and a later one may depend on
what an earlier one left** -- `tools/screenshots/dos.sheet` formats a DOS
floppy image in its first stanza and the other five work on it. Sorting that
sheet alphabetically once put `msattrib` first, and three screens came out as
mtools asking what to do about files that were already there. Keep such a
sheet in dependency order, and make the first stanza put the world into a
known state so the sheet can be run again and mean the same thing.

Two things it survives, both learned the hard way: a program that takes the
emulator down with it (`cpu` does, every time), and a program that will not
let go of the terminal (SEDT survived a Ctrl-E and ate the next three
stanzas of its sheet). After every stanza the shell is asked to echo a
marker; if it does not come back the session is replaced.

**Then LOOK at what was captured.** `tools/audit_screens.py` reads every
capture and flags what is not worth showing -- a screen that is one line
repeated, one with almost nothing on it, one that is nothing but the command
that was typed. It is a prompt to go and look, not a verdict: a chess board
repeats its rank lines and that is fine. It exists because a card once
carried twenty-four copies of `No more memory !!!` under a caption about
converting number bases, and every check there was had passed it.

**`tools/fix_index.py` rewrites one DOC/INDEX entry safely.** The file is
CR-terminated, its entries have continuation lines indented to a fixed
column, unstarred names carry an extra leading space, and the head of the
file repeats every name in a four-column grid that matches the same regex.
Hand-editing got all four of those wrong in one session. Import `fix` and
give it the program name and the replacement lines.

**Probe a program with the environment SYS/login gives it, not just PATH.**
On 2026-08-29 a sweep over DOC/INDEX entries ran each program with PATH set
and nothing else, and produced false negatives: `mailx' said "HOME is not
defined", `mg' and `mshell' said "Unknown terminal type dumb". With HOME,
TERM, TERMCAP, USER, LOGNAME, MAIL, TMACDIR and HELPDIR exported the same
way `SYS/login' exports them, mailx prints its banner, mg opens a file and
draws its mode line, and mshell gets far enough to ask for its menu file.
Two index entries were corrected on the strength of the unfair probe and had
to be corrected again. A full-screen program still needs a pty, which is
what `tools/screenshots.py' and `tools/playtest.py' give it; the environment
is the part a plain pipe can and should still get right.

**An expectation must be something an ERROR could not produce.** On
2026-08-29 a case asserting that `motd` appeared in shar's output was passing
on the word `motd` inside `No read access for file: /dd/SYS/motd` -- shar has
never made an archive on this disk. Nine other cases had the same shape: an
`expect` string that also appears in the case's own command line, so any
message quoting the arguments would satisfy it. They now assert a column
heading, a total, or a value whose digits are not in the operands. The check
is three lines of Python over `datatest.parse` and worth re-running after
adding cases.

`gen_screens.py` also reports DRIFT: a stanza with no capture, and a capture
older than the sheet that defines it -- which is the one way this can lie
without anybody touching a program, by publishing an old screen under a new
caption. **`tools/gen_screens.py --check` makes that fatal**, and CI runs it:
printing the warning was not enough, because nothing in CI reads warnings.

**No two stanzas may have names differing only in case.** A capture is saved
as `notes/playtests/<name>.shot.txt`, and on macOS `VI` and `vi` are ONE
FILE: shooting the second silently overwrote the first, and the `vi` card
published PVIC's screen under the EFFO vi's caption. Both `screenshots.py`
and `gen_screens.py` now refuse the sheet and name the pair. The offending
stanza was renamed `pvic`.

`gen_screens.py` folds the captures into **the one catalogue** -- there is no
separate gallery page, because a second page listing the same programs is a
second catalogue to keep true. A screen lands on the program's own card in
`docs/index.html`, under `Sample output', beside the usage line the program
prints for itself.

It decides two things the capture cannot: the high half of the
character set is read as **CP437**, because that is what these programs were
written for -- `cal` rules its columns off with $C4 -- and the published
files stay **ASCII**, with the line drawing carried as numeric escapes in the
HTML and folded to `-`, `|` and `+` in the `.txt` copies.
