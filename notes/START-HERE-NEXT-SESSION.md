# Start here, next session

## 2026-09-12 (later): rdoggett's ten decisions, executed

**Four programs dropped**, each measured first: `dearc` (cannot read a
CRUNCHED member -- four genuine 1980s archives and one written by this
disk's own `arc' all stop at the first member; SOURCES.txt had already
recorded dearc as NOT taken, "arc covers it"), `rstory2` (forks four
`rstory_*` programs that were never distributed and cannot be rebuilt --
rstory.c's main() takes no arguments), `splitalf` (a real bug found and
fixed in SRC -- `fa[1] == NULL' tested inside the loop that opens fa[0] --
which only made the failure honest; it still dies on the second fopen, and
`MEM=64k' changed nothing), `wc.cio` (nothing unique: both read stdin the
same, `wc' also takes filenames).  Earlier the same day: `kermit_cio` and
the three gzip `_nocsl` builds.

**Four were NOT broken -- these are the better half of the finding:**
- `dedit` is BASIC09 I-code (type 2 lang 2, measured) and wants runb.
  DOC/INDEX said "Three programs are BASIC09 I-code"; there are FOUR.
- `names` is a German ADDRESS BOOK (`Adressen Verwaltung' 1.0).  INDEX
  called it "list the names of modules in a file".  It does not.
- `ff` needs a `shell' module, like m4 -- it forks one for `dir ! grep'.
- `creadoc` likewise: it forks a shell for `dir -eadu' and for `del', so
  it wants your own OS-9's utilities.  Not "one constant", which is what
  I said twice before reading the source.

**All six GNU Chess builds stay** -- no two are indistinguishable, which a
subagent established from captures and binaries.  gnuchessc was wrong in
INDEX on both halves (it is the CHESSTOOL build, boardless BY DESIGN, and
its data files ARE found).  The `nchess' RECIPE carried -DCHESSTOOL, which
deletes the search table that is nchess's whole reason to exist -- fixed,
and the rebuild now matches what ships.

**Decision 7 is finished.**  All six GNU Chess builds stay -- no two are
indistinguishable -- and INDEX now says what tells each apart, so a reader
can pick one and drop the rest.  Measured, not transcribed: `gnuchessr'
carries the book's full path (it books wherever you run it) and uses `set'
to lay out a position; `nchess' has only the bare name (books from the
current directory), uses `edit', and on the same drive script prints the
live search table that gnuchessr does not.  `nchess' LOST its "GNU Chess
4.0" label, which nothing here supports -- the string lineage actually
points the other way, but that reading is inferred, so the claim simply
goes rather than being reversed.

Two provenance gaps closed with it: gnuan, gnuchessc, gnuchessn and
gnuchessr had NO ORIGINS row at all, and the `gnuchess' row credited the
whole name to Usenet gnu.ar when only the CMDS/GAMES build comes from
there -- CMDS/gnuchess is a different port from the Microware archive.

DO NOT re-derive cio dependency from strings while working on these.  I
started to, and CLAUDE.md is right: the proxy is wrong in both directions
and the star markers were measured by running without the modules.

**fpu ships** (decision 2) with its own grant in DOC/fpu.doc, honestly
labelled: it belongs in a bootfile and an Init extension list, neither of
which this collection has, so it is there to install on your own system.

**Q2 source staged** (decision 1): SRC/gawk2.0 (28 files), SRC/bison (39),
SRC/dvips (65 top-level .c/.h plus the archive's own OS9/ port files).
All CR-only, all recorded in SOURCES.txt with their terms.  dvips's porter
had asked for exactly this in his ReadMe.OS9.

**jive stays OUT** (decision 3).  No N-word in it -- but `wet-back' and
`greaser' are in its vocabulary, which is rdoggett's stated test even
though the word he named is absent.  `valspeak', the companion filter from
the same distribution, ships and is clean.

**The card audit's headline was wrong by a factor of twenty, and the
correction is worth more than the finding.**  os9-dev-skill-fc's
CARD-AUDIT.md said 244 published `try' commands cannot be reproduced.
Re-measured from docs/screens.js: 951 programs all carry a try line, 299
name a path under `tmp/', and for 286 of those the path appears in that
card's OWN published screen -- so the reader sees the file being made
even when the creating command ran before the `clear'.  Thirteen did not,
and TWO of those thirteen only WRITE into tmp/ (djpeg, rayshade), which
is fine because tmp/ ships.  **Only a READ can fail.**  Eleven real ones.

Fixed by SHIPPING the inputs, which is what this collection already does
46 times over (DOC/xasm/sample.a0, DOC/logisim/counter.lsi,
GAMES/rayshade/boxball.ray are all try-line targets that ship).  New:
DOC/samples/{jabber.txt,titles,menu,hello.ps}.  Repointed: vi, sed,
sed_1.06, mg, pagekwic, mshell, gs403, and pnmhisteq at the
already-shipped DEMO/sphere.pgm.

Still open from that eleven: `EditLibr' and `Librarian' want a catalogue
Ascii2Libr generates -- the route is to mount a host directory as OS9H1
and `copy' the built cat.libr out of the image, then ship it, checking it
arrives byte-identical.  And `pbyte' PATCHES ITS INPUT IN PLACE, so it
must not point at shipped data: it should be the one card that visibly
stages a scratch copy, with a sentence saying why.

**`pagekwic' IS NOT BROKEN -- settled from source, do not chase it.**  I
wrote here that its output looked wrong because it rotates words ACROSS
titles.  It does, and that is the design: os9-dev-skill-fc read
`SRC/bix/pagekwic.c' and it is a PHRASE indexer, not a line one --
`#define DEFFRZ (4)', a circular `wordbuf' printing every rotation of a
sliding window, and a `get_word()' that treats CR as a word separator and
never signals end-of-line to its caller.  A phrase spanning a line break
is what it is for.  Its DOC/INDEX entry was right all along ("one phrase
per line"); the card's caption was the only thing setting a wrong
expectation, and I nearly trusted the caption over the source.

The card now demos it honestly -- `pagekwic -f=3 < DOC/samples/jabber.txt',
continuous prose instead of four unrelated titles, with a caption that
says PHRASE keyword-in-context.  `-f=<n>' sets the window, 1 to 10.

**THE CARD AUDIT IS CLOSED AT ZERO.**  Measured against docs/screens.js
after the final shoot: 951 programs, 951 try lines, 295 naming a tmp/
path, and NONE naming a path nobody creates.  The claim that started it
was 244; it went 244 -> 13 -> 11 -> 2 -> 0 as each measure was replaced
by a better one.  The measure that is actually right, and worth reusing:
a path is satisfied if it appears in the card's own screen OR is created
earlier in the SAME try line -- gs403 creates its output with
`-sOutputFile=' mid-line and reads it back, so any rule about which sigil
precedes a path gets it wrong.

**The six Home Librarian cards share a shipped catalogue now.**
Ascii2Libr, Libr2Ascii, EditLibr, Librarian, PrintCards and PrintLabels
each rebuilt the same twelve-line catalogue by hand -- eight echo lines
apiece, invisible, before the `clear'.  `DOC/samples/cat.txt' ships that
text and each card builds from it in ONE visible line, so the try line is
copyable and 48 lines of duplicated staging are gone.

**A trap of my own, one level below the usual one.**  The repoint script
dropped each stanza's staging line by matching "contains the filename and
a printf".  Every line it matched really was a staging line -- but
gs403's also carried `export GS_LIB=/dd/LIB/gs403' and its mkdir, so the
card would have shot Ghostscript with no fonts and been read as a
Ghostscript limitation.  I verified what the line WAS, not everything it
DID.  Read back what a bulk edit produced before trusting the pattern
that produced it.

**IN FLIGHT, NOT YET PROVEN -- pick this up first:** `DVIPS/tex.pro' and
six sibling prologues are staged into `disk/SYS/TEX/DVIPS' from the
PUBCMDS copy of dvips_source.lzh (the refetch copy does NOT contain them).
dvips has never rendered here for want of that file.  It is NOT verified:
the gate was red when I rebuilt, so mkimage refused and every test so far
ran against a stale image.  Run the gate, rebuild, then
`chd /dd/DOC/mg; dvips mg_doc.dvi -o /dd/tmp/mg.ps'.  The binary searches
`.:/DD/SYS/TEX/DVIPS:/DD/USR/TEX/DVIPS:/DD/TEX/DVIPS' and honours
TEXCONFIG.

**Decisions 4 and 5 -- the untestable sections.** New category "Needs
hardware", with subcategories Display (apfel, g, graphdemo, graphsave,
showpic, sine, striche, umusek) and Printers (splman, splprt, splstat,
lpsched).  Its blurb says outright that we cannot test any of them.

I did NOT follow rdoggett's item-5 list literally, and this is the
reason: he listed `for', `lnk' and `lnk.org' as needing hardware, and
they do not.  `lnk' calls l68 with Microware's /h0/LIB/sys.l and `for'
forks Microware's shell for each compiler pass -- that is the reader's
own OS-9, the same case as m4, ff and creadoc, which this collection
documents in place rather than sequestering.  Their INDEX entries
already say so, so they stayed where they are.  `splprt' and `splstat'
DID move, though he did not name them: splman's own entry says the three
go together.

I also checked the four programs left behind in `Graphics & images |
Hardware demos' and left them there ON PURPOSE.  His list encodes a real
distinction and it is abort-versus-runs: `showpic', which he named, "is
entered and aborts: it wants the display, not just the library", while
`wgen' with the graph trap resident RUNS and asks for a resolution,
`lissaj' prints its 1990 banner and prompts for X and Y frequencies, and
`lorenz3d' prompts and then emits Tektronix plotting codes.  All three
have captures showing them working.  `graph' itself is the trap library,
a type-$0B module and not a program at all.  Do not "tidy" these four in
after the others.

**xmas stays** (decision 9, which he left to me).  It is a real animated
character-art card -- a tree trimmed, lights blinking, reindeer running
-- and its "from The ghost of Robert past" is the OS-9 porter's edit of
a line the source invites you to change.  Nothing on the card names
whose it is, which is the rule, and it costs nothing to keep.

**I REPEATED THAT TRAP THE SAME EVENING, so it is worth more than one
line.**  Shipped DOC/samples/cat.txt and label.tpl, then shot six cards
against an image built BEFORE they existed.  Every capture came back
`Error #000:216 -- that path name doesn't lead to anything', which reads
exactly like a broken card and is nothing of the kind.  The first time it
was the dvips prologues and I wrote "staging and building are not
independent" in this very file; the second time I had that sentence in
front of me and still did it.

The rule with teeth: **anything you add under disk/ is invisible to the
emulator until mkimage runs.**  A card that suddenly cannot open a file
you just created is that, nine times in ten, and the check costs four
seconds -- `dir /dd/DOC/samples' before believing the capture.

**A trap I set for myself, worth not repeating:** I issued "stage the
files" and "rebuild the image and test" in the SAME parallel batch, so
mkimage ran against a tree that did not have them yet, and I read the
resulting failure as a dvips problem.  Staging and building are not
independent.


## 2026-09-12: seven programs added, 1000 total, 24 commits

Added and carded: **browse** and **uustat** (the two B5 called blocked -- the
scan that "proved" it looked only in `disk/LIB/`, and the library is
`disk/GNULIB/os9lib.l', already on the build path), **almanac**, **zc** with
its 780 KB zipcode table, **cfscores**, **rot22**, **reversi**, **gnugo**.

Fixed, each found by measurement rather than report: `ls' printed a literal
`%s' where the filename belongs (error.c defined variadic error() with fixed
parameters) and had silently blanked two cards whose whole point was showing
a file gone; `infoxpress' published os9exec's own pty announcement as its
entire panel; `xcrypt', `liborder' and `unpacklib.os9' all claimed things
their own captures contradicted; `disk/readme' endorsed leaving the reader's
OS-9 on /dd two lines after saying not to.

Settled: rdoggett's `/h1' shell load (see FOR-RDOGGETT); Q1 (non-commercial
terms) recorded as settled so nobody re-asks; the twenty-four command names
this disk shares with OS-9's own, noted in README-KEEP.

**Assessed and ready to pick up, in order:**

- **scrabble** -- DONE 2026-09-12, commit 9d6aa1e4.  It ships, reads
  GAMES/words and draws its board.  The estimate below was the right shape
  but for the wrong reason; see the next bullet.
- **napoleon** -- DONE 2026-09-12, commit 58199b30.  It ships and it plays.
  The "a day, 71 ANSI prototypes" estimate was wrong in KIND, and the
  correction is in `tools/rebuild/README.md': ansi2knr converts only a
  definition whose NAME is at the left margin, so it did 46 of scrabble's for
  nothing and 0 of napoleon's 84.  **Ask where the name sits, not how many
  prototypes there are.**  The rest of what that port cost -- 634 adjacent
  string literals, a 12,449-character GPL scroll joined at run time, no
  `#error' in Microware's cpp, difftime being a macro, the disk's own yacc
  beating host bison -- is all recorded there too, because none of it is
  about napoleon.

- **TOP's own source trees** (`Scraped/.../os9/top/src/') -- OS-9 ports of
  programs this disk ships as binaries.  Verified 2026-09-12 against
  `src_census.py' (701 of 999 programs have source here, 70%; 298 do not)
  and against ORIGINS read as entries rather than by substring:

      gawk    gawk2.0      15 .c   10,026 lines   no source here, no ORIGINS row
      bison   bison        19 .c    8,380 lines   no source here, no ORIGINS row
      emacs   emacs_3.10   23 .c   18,135 lines   no source here, no ORIGINS row

  Those three are genuine gaps.  compress, less, rcs, diff and flex are NOT:
  we already have their source, filed by ARCHIVE rather than by program
  (`SRC/hc_utils/compress.c', `SRC/less/less_332/', `SRC/rcs', `SRC/diff',
  `SRC/flex') -- checking `disk/SRC/<program>' finds nothing and is the wrong
  test, which cost me three false findings tonight.  Q2 is rdoggett's call.

  NOTE when sizing any TOP tree: its files are CR-terminated with zero LF, so
  `wc -l' reports 0 for all of them.  Count CRs.

**Left out deliberately, with reasons in PLAN-acquisitions.md:** `flicker'
(an unstoppable ANSI loop), `dumpinit' (six mod_config members this SDK's
<module.h> does not have), `adven2' (Fortran).

**Two build rules learned the hard way:**
- `KNR' ON AN ALREADY-K&R TREE IS HARMFUL.  ansi2knr rewrites parameter
  declarations that are already K&R and c68 then reports `multiple
  definition' on plainly-correct lines.  Symptom is distinctive; the fix is
  to REMOVE the flag.  In `tools/rebuild/README.md' too.
- `build.sh' deletes its temp directory on exit, so a failed build's log is
  gone before you can read it.  Pass `OUT=' and `LOG=' in the environment --
  rebuild.sh honours them and build.sh does not override.


## 2026-09-11: two tracks running

- **Acquisitions plan**: `notes/PLAN-acquisitions.md` (committed b241bfac) --
  eleven batches of software the collection lacks, with verified URLs and
  licence terms, from two deep archive sweeps. Claim a batch by message
  before starting; one session at a time regenerates DEPENDS/CATEGORIES/
  README/docs or rebuilds the image, announced first. Two questions wait on
  rdoggett: non-commercial licences, and GPL source for shipped gcc/dvips.
- **keep is now a real installer** (`notes/keep-installer-2026-09-11.md`): it
  fetches termcap-when-missing and a program's data directories, leaves the
  system directories to your own disk, refcounts shared files, preserves
  scores on re-install (`unkeep -a` clears them), takes every build of a
  name (gcc 1.39 and 2), and unkeep now removes the directories it empties.
  Verified across 440+ programs; three bugs found and fixed in the pass.

## 2026-09-10: the guides, corrected twice by rdoggett, both committed

- **Real OS-9 comes first.** Every reader-facing guide (front page,
  `README.md', `disk/readme', `DOC/README-RUNNING') opens with the real
  system: a disk of its own reached as `/dd' and `/h0', the reader's own
  OS-9 on `/h1', the image written whole or `osk-freeware.tar' unpacked
  with the `tar' module beside it.  os9exec comes second, as the test-drive.
  Never a bare emulator line as the first thing a reader sees.
- **os9exec is named by its variables, never by a link.**  `OS9DISK' and
  `OS9H0' may be the SAME image -- os9exec says `# /h0: using OS9H0=...'
  and mounts it -- so the `ln osk-freeware.dd h0' every guide used to
  teach is gone, along with the claim that the emulator "will not mount
  one path as two devices".  It builds on macOS, Linux, Windows and most
  anything with a C compiler.  RBF images are the preferred format:
  permissions and record locking work as OS-9 expects on an image and not
  on a host directory; `mount -k' makes a blank one.  **The `h0' symlink in
  the repo root is NOT stale and must not be deleted** -- this file said
  "nothing reads it" and that was wrong: rdoggett's `free' alias passes
  `.../osk-freeware/h0' as BOTH OS9DISK and OS9H0, so removing it removed
  his disk and os9exec stopped with `E_MNF: bash' before emulation began.
  Deleted on a sibling session's report 2026-09-12, restored the same night.
  The evidence that would stop you is in `~/.zshrc', not in the tree.
- **One arrangement for running and keeping**: `keep' copies from `/dd'
  onto `/h1'; `unkeep' (was `drop') takes it back.  `DOC/README-KEEP'.
- **Spot-check fixes from rdoggett's own reading of the page.** `zot':
  its styles are ANIMATIONS (letters sliding, bouncing, sorting in, each
  frame a CR-rewrite of one line), invisible under `os9exec -r`, which
  drops the pacing; the card is now a filmstrip via the new sheet
  directive `frames'.  `robots': every score read "your name" because the
  OS-9 port's getlogin() stub in `SRC/rob/os9stuff.c' returned that
  literal; it now reads USER, LOGNAME, then group.user, rebuilt and
  installed, verified against an emptied list ("tester", today's date).
  The shipped 1987 score files are untouched.  Card shows the board in
  play, not the top ten.  `sonnet': the card says what `-l' takes (a poem
  sonnet wrote with `w'; sonnet.out by default).  `oleo' aborts, is
  carded as such, and is on FOR-RDOGGETT's best-forgotten list with piano
  and rstory2 -- recommendation: drop all three; his call.

## Where it stands (2026-09-09, evening): every card carries its own captured help

The second pass `notes/PLAN-recard.md' asked for is done in its mechanical
half and its reading half, category by category, in fourteen commits:

- **The scrape is gone.** `usage_of()' is out of `gen_catalog.py'.
  `tools/help.psv' says, per program, which command asks it for help (or
  `none' with a note), `tools/helpcap.py' runs that at Microware's shell and
  keeps the whole answer in `docs/help/<name>.txt', and the card shows the
  command and the text under **its own help** -- unfolded, on the card,
  not behind the details.  `tools/help-backlog.txt' is the ratchet and it
  is EMPTY: all 935 programs have a line.  The gate `cards carry real help
  text' fails on a missing, stale, hung, empty or cut-off capture, and
  `check_the_checks.py' proves it both ways.
- **The page**: help is its own section after "see it run"; "details and
  provenance" is always open (it was a fold that closed on every shell
  switch).  Both were rdoggett's asks.
- **DOC/INDEX** was read entry by entry with the probe beside it: craft,
  author names and shouting out; the 169 netpbm programs now have one real
  entry each (the columnar block is gone, `from_index' no longer special-
  cases NETPBM); the ADL usage table, the duplicate rxmod/vmod_trap and
  `about' entries and the "Where a few programs live" list are cleaned up.
  `DOC/USAGE' is regenerated from the captures (`helpcap.py --disk disk').
- **Demos recut** where the help section made a `-?' demo redundant: the
  serial-transfer programs (xy, z, k, dld, uld, blastem, xydown, xyt,
  sterm, tterm, connect, uucico) now show what they do without a line.

**Not done, and honest about it:** the cards were read as text dumps, not
rendered in a browser (opening Safari on rdoggett's screen is disruptive).
Open `docs/index.html' and read a few at random -- that is the acceptance
test PLAN-recard names, and it has not been run by eye.

**Traps met today, for the next session:**
- `fix_index.fix' used to match star-grid rows (some names ARE small
  words: `in', `is', `mail') and entries at three spaces or `  *name'; both
  fixed, and it now pads a 16-letter name to two spaces (compress_rebuilt
  had dropped out of the catalogue).  Deleting the rule line after the star
  grid makes the grid parser eat the prose that follows -- keep it.
- **Gate the commit on `check_disk.py`'s EXIT STATUS**, never on `grep -v
  ok` (which succeeds when it finds failures).  One commit went in red that
  way and was fixed in the next.
- At Microware's shell under os9exec, bare `mv' runs the emulator's
  built-in `move'; `load /dd/CMDS/mv' first (help.psv does).  A `chx' away
  from CMDS loses `cio'; `load /dd/CMDS/cio' first (the GCC drivers do).
- A heredoc python patch that asserts halfway leaves NOTHING written;
  check the file after, not the "ok" you expected.

---

## The all-card sweep is DONE (2026-09-09)

Every program card (~900) was reviewed one at a time and carries a `try'
line; the try-line backlog is zero and every `check_disk.py' check is green.
All twenty gallery sheets swept, captions rewritten for a stranger, author
names and ALL-CAPS out of the reader-facing text, captures freshly shot.
The machinery built for it: line-folding is opt-in (`fold'), cards carry a
`try' line (gated) and an `os9' line where Microware's shell differs
(verified by `tools/os9try.py'), draw-once full-screen programs are captured
unthrottled (`burst'), and the web page has a bash / OS-9 shell switch, a
keep preview, more contrast and no capitals.  logisim's label bug was fixed
at its source and rebuilt.  What is left is polish, not sweep: see
`notes/FOR-RDOGGETT.md' (DOC/INDEX de-shouting for four categories whose
agents hit the session limit, and the best-forgotten candidates).

---



Branch `release-pass-2026-08-21`, never pushed. Tree clean, every
`check_disk.py` check green (read the list the tool prints, do not trust a
number), `osk-freeware.dd` current.

**`notes/PLAN.md` is the authority and the work. `CLAUDE.md` has the rules and
is not optional. This file is only the cold start; the rest of `notes/` is
background you do not need first.**

## What 2026-09-05 did (all committed, gate-green)

- **TeX renders.** The sixteen Plain TeX Computer Modern fonts are built at
  300 dpi (virmf/CanonCX) and ship as .pk in SYS/TEX/FONTS/PK300 and .gf in
  SYS/TEX/FONTS. All eleven DVI drivers now render the sample instead of
  zero-size text -- five at 300 dpi, five by nearest-neighbor scaling; only
  dvips cannot, for want of its tex.pro header. README-METAFONT and the
  driver cards are corrected.
- **gnuchess plays the book.** CMDS/gnuchess reads USR/src/chess/gnuchess.book
  (reachable as /h0/...), is first on PATH, and answers 1.e4 with the
  Sicilian. The collision with the GAMES build is accepted; the card shows
  the book move.
- **wysecrack left BROKEN** (moved to CMDS/COMMS -- it probes a Wyse
  terminal, not broken); CMDS/BROKEN is retired.
- **pacman** corrected -- a keypad ASCII maze game, not G-Windows.
- **subber** carried as an exception: it grows its data area with F$Mem, a
  6.5 KB request os9exec's arena cannot grant in place; runs on real OS-9.
- **creadoc** re-explained: a pre-Y2K column shift (2026 prints as `126'),
  not F$PrsNam, and it writes nothing even when the column is right.
- **README-RUNNING** rewritten to the settled /dd + /h0 + /h1 arrangement.
- os9exec fixes that landed and were measured here: MOVE from SR (biory
  draws its chart), F$Mem (per the manual), F$SysID (sysid reports).

## Where it stands (2026-09-05)

Per-program **cards** show each program doing its own job: 814 of 912
runnable programs score "work" or "play"; the rest are honest exceptions
in `tools/panel-exceptions.psv`, each with a reason, and
`tools/panel-backlog.txt` is empty. The gate `panels show their own program`
enforces it. The web page is the three-column layout in `docs/`.

The **tribute voice** governs every reader-facing word (cards, `DOC/INDEX`,
`tools/howto.psv`, the READMEs, the page): lead with what a program IS and how
to run it; name what it uses -- runb, cio, the shell, r68/l68 -- as the
reader's own OS-9, never by its absence ("not on this disk" is banned). The
reader HAS Microware OS-9; os9exec is only the convenience. See the memories
`os9-collection-is-a-tribute` and `os9-card-rules-2026-09-03`.

## What the last session did (2026-09-07), all committed and gate-green

- **Every gallery demo recut to the simple style rdoggett asked for**: the
  visible line is the program and its arguments, and the `cd', the `load'
  and the file staging are hidden before the `clear'.  A reader new to a
  command sees what to type, not a `ksh -c "cd X; ..."' shell-in-a-shell.
  All 55 wrapped cards were done across amusements, archives, calendars,
  documentation, editors, comms, compilers, devtools, encoding, games,
  system and tex -- five commits, each sheet-group its own.
- **screenshots.py now resets the data directory (`builtin cd /dd') at the
  head of every stanza.**  Stanzas in a size-group share a session, so a
  hidden `builtin cd' would otherwise leak into the next stanza; the reset
  is what makes the bare-command style safe.  Verified a no-op for the old
  sheets (an untouched card recaptures byte-identical).
- **Three cards keep their `ksh -c "cd"' wrapper on purpose**, noted in
  FOR-RDOGGETT: `creadoc' (known-broken, needs /h1), `vtxtcn' (leaves the
  session unusable unless run in a subshell), `mkdict' (fragile; and it no
  longer bus-errors, so its caption is stale).
- **gothic runs non-interactively now** (`gothic -h OS-9'), and the config
  for testing the Microware shell is settled: freeware on /dd and /h0, the
  SDK on /h1 (absolute path -- a tilde does not expand into OS9H1).

## What the last session did (2026-09-06), all committed and gate-green

- **Shown-command pathlists swept.** Visible `run' lines across the sheets
  now use short relative names reached by one `chd'/`cd'; captions and
  `try' lines were already clean and gated. What still shows a path in a
  panel is program output, the sanctioned single-`cd' form, or a typed path
  the caption explains (`mv'/`move'/`fc' dodge a ksh built-in; the GCC
  drivers must be pathed). See `notes/FOR-RDOGGETT.md'.
- **Four panels restored** after the sweep: `pgmedge' and `lesskey' re-shot
  in full-sheet context (a partial re-shot had skipped the stanza that
  makes their work directory); `ppmtopj' and `ppmtorgb3' write to files and
  became honest `panel-exceptions.psv' entries beside `vtxtcn', the
  following round-trip/`ls' being their evidence.

## What this session did (2026-09-04), all committed and gate-green

- The tribute voice reached the **captions** (the earlier INDEX/howto pass
  had not): no caption says "not on this disk" any more.
- **The reader's own OS-9 mounts on `/h1`.** `SYS/login` adds `/h1/CMDS` to
  PATH and does a silent `load /h1/CMDS/runb`; the collection stays `/dd`
  (+ `/h0`, the same image). The harness mounts the SDK as `/h1` when `OS9SDK` is
  set. `load` fails gracefully with no `/h1`, so standalone boot is unchanged.
- **`date` removed** -- a broken shadow of Microware's date (it decoded the
  year as 2100). The clock itself is fine: F$Time returns 2026, only that
  442-byte binary misread it. The three entries that cited its 2100 (setime,
  rcsdiff, udate) are corrected.
- **`wysetime` kept** -- it is a BASIC09 clock-setter (`runb wysetime` emits
  a Wyse terminal's clock-set escape sequence), carded. It had been wrongly
  removed as "uncallable"; a packed BASIC09 module IS a type-2 subroutine
  module, exactly like bio, and `runb <name>` runs it.
- **`bio`** kept (F. Kaefer's Biorhythm), verbatim source in `SRC/bio/bio`,
  carded via runb with a typed date. Its "Wrong input!" on RETURN is bio's
  own 1987 `.19` century hardcode, not os9exec.
- **`lua`** works now (the csl edition-25 swap); msntp, basicwin, xengine
  reach honest walls (no network, no X server); runc is the Lua runtime
  engine.
- `TERM=xterm-256color` in login (was mislabelled `vt100`, an alias of the
  same termcap entry).

## What this session did (2026-09-04, evening)

- **os9exec `852dddd` no longer traps MOVE from SR in user state.** `biory`
  draws its chart and its card shows it. `creadoc` runs on to a stop of its
  own (it reads file names from column 53 of `dir -eadu`; this dir prints
  them from 54) -- carded and documented as such.
- **`blackjack` plays** under runb; "error 56 at line 8" was chx off CMDS,
  where runb cannot find the `math` trap handler. Moved out of
  `CMDS/BROKEN` into `CMDS` beside bio and wysetime, carded.
- **The five zip readers have an archive**: `DOC/zip/sample.zip` (unzip's
  own readme and ziprules). unzip, zipinfo, zipnote, zipsplit and funzip
  are carded on it and `archives.cases` asserts the md5s.
- **F$Mem is implemented in os9exec (`7fa2899`)** as the manual describes.
  `subber` grows its data area with it 256 bytes at a time, which succeeds
  only while nothing sits directly above the area: from Microware's shell
  with cio loaded first it substitutes; under bash it is always refused,
  so its card shows the refusal, excepted with the reason. The `#256k`
  route written earlier tonight was layout luck, not the modifier.

## What needs rdoggett -- `notes/FOR-RDOGGETT.md`

- `DOC/README-RUNNING`'s three numbered arrangements still describe the
  pre-`/h1` swap model (its opening is fixed). They want rewriting to lead
  with the `/h1` arrangement -- his call how the setup is framed.
- The branch has never been pushed and nothing is tagged: a release is his.
- "Best forgotten" candidates, re-measured 2026-09-04 evening (blackjack,
  bio and the zip readers came off it), and the remaining os9exec gaps
  (the RCS same-second clock, F$GPrDBT) are listed there.

## The loop, for card and test work

```sh
tools/worklist.py --programs --no-test --no-card    # what still has nothing
tools/drive.py <sheet>                              # run a sheet, read the transcript
tools/audit_panels.py                               # panels that do not show their program

# Capture a card THROUGH THE HARNESS (it shuts down cleanly). A BASIC09 or
# runb-only program needs the SDK on /h1, so set OS9SDK:
OS9SDK=~/Developer/os9/play/oskBoot \
  tools/screenshots.py tools/screenshots/<sheet>.sheet --only <name> --image "$PWD/osk-freeware.dd"

tools/gen_screens.py        # publish captures to docs/screens.js
tools/gen_catalog.py disk   # rebuild the page from INDEX/categories/howto (also DOC/CATEGORIES, README)
```

Build and gate (gate EVERY commit on check_disk being green):

```sh
rm -f disk/.DS_Store        # macOS recreates it; packed, it fails the build
OS9EXEC_DIR=~/Developer/os9/os9exec tools/mkimage.sh disk osk-freeware.dd
tools/check_disk.py disk
```

## Gotchas that cost time this session

- **`disk/.DS_Store` recurs** (macOS) and breaks the build as an extra
  packed file. `rm -f disk/.DS_Store` right before mkimage and before every
  commit.
- **Capture through `tools/screenshots.py`, never an ad-hoc gtimeout-wrapped
  pty loop.** A gtimeout that kills a hung pty-driven os9exec leaves an
  orphan process you cannot clean (killing is gated). The harness lands
  softly; confirm `pgrep os9exec` is 0 afterwards.
- **`runb` and the reader's Microware tools are on `/h1`** (the SDK), not on
  the disk. `bio`, `wysetime` and `blackjack` are BASIC09: `load /h1/CMDS/runb`
  then `runb <name>`. Under Microware's own shell the bare name auto-runbs;
  under the collection's bash it does not (bash says "cannot execute binary
  file").

## If you remember four things

1. OS-9 text is CR-terminated (0x0D), never LF -- `check_disk` catches LF.
2. Measure, do not infer -- every proxy tried here has been wrong both ways.
3. Make every check fail once before believing it.
4. A program that looks broken usually has the wrong invocation.

## Where the answers live

| Question | File |
|---|---|
| What to do next / the whole picture | `notes/PLAN.md` |
| The rules | `CLAUDE.md` |
| What each program is / does it work | `disk/DOC/INDEX`, `disk/DOC/STATUS` |
| How to run it | `tools/howto.psv` |
| What it needs besides its binary | `disk/DOC/DEPENDS` |
| Where it came from, on what terms | `disk/DOC/ORIGINS`, `disk/SOURCES.txt` |
| Which panels are not worth showing, and why | `tools/panel-exceptions.psv` |
| What needs rdoggett | `notes/FOR-RDOGGETT.md` |
| Why it is like this | `notes/HISTORY-2026-08.md` |

## Done 2026-09-12: the twenty drifted captures (commit d842cc4b)

All re-shot.  Re-shooting them is what showed WHY they had drifted: the
stanzas had been rewritten earlier and never re-shot, which left `input'
under the ink floor, `lcasep' clearing it only on the length of an old
PATHNAME, and `filter' reaching for a /r0 that is compiled into its binary
and that this disk has no device for.  Fixed, listed in SPARSE_OK, and
listed in panel-exceptions.psv respectively.

`gen_screens --check' no longer says captures are "OLDER than the sheet":
it compares a stanza HASH, and the old wording sends you to compare mtimes,
where a sheet touched to add one stanza looks like it invalidated all of
them (836 of 900 against the true 20).

## Next

Three acquisition avenues were opened and CLOSED on 2026-09-12.  All of them
ended on TERMS or on prior coverage, not on availability -- which is worth
knowing before opening a fourth.

- **The Microware archive refetch is done**: the five categories the pool
  lost are back, 153 files, 34 MB, zero failures (`2f048f62', `d2081094').
  It yielded NO new programs.  rz/sz are commercial, five are K-Windows
  clients, `ot' states no terms at all, `fpu' is Microware's and is yours.
  What it did yield is licence data: lharc and m4 (`579f289c'), and
  provenance for k/xy/z which were shipping unrecorded (`64cf6cfb').
- **TOP's 30 source trees are triaged** (`4542b440').  Four fill real gaps:
  bison, emacs and gawk are Q2 and yours; larn is blocked on a bare 1986
  copyright with no grant anywhere in its 25 files, even though the tree is
  demonstrably the right source for the shipped binary.
- **DOC/ORIGINS is already mined** (`c1579c53').  Do not plan a sweep
  through it -- src_census.py's ARCHIVE route reads it already, so the 309
  source-less programs are precisely the residue it cannot place.

**The honest state of "find more": the cheap seams are worked out.**  Of the
309 without source, 5 are Microware runtime modules that will never have
any, 25 are large GNU packages, and the remaining 279 need per-program
archive hunting -- the same work the batches in PLAN-acquisitions represent,
at roughly one evening per handful.

Still genuinely open, in order of how much they are worth:

- **Two decisions are yours**, both in FOR-RDOGGETT.md with the material
  located: Q2 (gawk/bison/emacs source, TOP trees ready to stage) and
  Microware's `fpu' module.
- colorcomputerarchive.com is alive and unfetched, but it is CoCo -- 6809,
  where this disk is 68k.  Judge scope before spending on it.
- The Internet Archive was globally offline all night; its three Wayback
  rows and cdrom-coco are untestable rather than refused.  Retry.
- Everything in ROADMAP-freeware.md about the release -- CI never exercised,
  branch never pushed, nothing tagged -- is yours.
