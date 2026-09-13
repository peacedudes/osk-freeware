# Start here, next session

## 2026-09-13 (overnight): the sweep finished, the card queue halved

**Two things want rdoggett and nothing else does** -- both in
`notes/FOR-RDOGGETT.md`, both costing either money or a licence
judgement, neither of them a task anyone can pick up:

1. **comp.os.os9 1987-2002 HAS BEEN FOUND.**  `usenet-rewind.com` holds
   the group from May 1987 to December 2023, 17,802 messages, checked by
   reading the 1987 digests themselves.  Bodies are free; the author
   addresses and original messages need a plan, about $40 for a month,
   and their terms forbid scraping while naming an API plan as the licit
   route.  This is the hole the acquisitions plan has called the live
   question for two days.
2. **`rcsmerge` can be made to work, and the last piece is
   non-commercial-only.**  diff3 compiles from source already on the
   disk once the recipe supplies `-DDIFF_PROGRAM="/dd/CMDS/diff"`, then
   fails to link on `pipe`; the only `pipe()` in the pool carries a
   non-commercial clause narrower than the package around it.

**The PD_ALF sweep is COMPLETE: 929 of 929 stanzas, 36 clearers, and not
one damaged card.**  Its three leftover mysteries all resolved to
instrument error rather than program behaviour -- see the tally below.
Do not re-sweep for PD_ALF; the question it was opened to answer is
answered.

**The flagged-card queue went from 66 of 990 to 30 of 929**, and both
numbers moved for reasons worth knowing.  `audit_cards` had been
discounting the FIRST LINE of every capture (241 of them; two were
really command echoes) and scoring 61 captures the gallery never
publishes.  Four cards were genuinely REPAIRED -- `UnMacpack`,
`macunpack`, `finger`, `afm2tfm` -- each of which was showing a usage
line because of how it was being asked, not because the program could
not do it here.  The rest were read one at a time and either excepted
with a reason or recorded as something the DISK cannot do.

**Three traps found in the harness, all of which had fooled me first:**
`notes/playtests` is gitignored, so every "tree: 0 modified" printed
after a sweep proved nothing about captures; a gate piped into `tail`
reports `tail`'s exit status; and `!` inside double quotes triggers
history expansion in this shell, where `$!` is 0 anyway.

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

**CLAUDE.md IS GITIGNORED (.gitignore:20) AND IS NOT IN THE REPO.**  I
found this by noticing an edit of mine never appeared in `git status'.  It
matters for two reasons.  Anything corrected there is corrected only on
THIS machine -- it does not travel, and a fresh clone gets whatever the
file says wherever it came from.  And it is rdoggett's own instruction
file rather than a project document, so it is not mine to maintain.

I did edit it once tonight, on my own judgement and not at anyone's
request: line 517 said "check_disk.py has TWENTY-ONE checks now" where the
tool prints 27, and that same passage records the number having already
drifted through nine, fifteen, seventeen, eighteen and twenty.  I replaced
the count with a pointer to what the tool prints, which is what the
passage itself advises.  FLAGGED TO RDOGGETT rather than left silent, and
I have not touched anything else in it.

**NEVER CHAIN AN EDIT WITH ITS OWN VERIFICATION IN ONE SHELL COMMAND.**
This is the mechanism behind commit 719a911a, whose message claimed a
docstring edit that had failed three lines above the output I read.  The
edit asserted, printed a traceback, and the same command went on to run
the gate and the commit -- and the gate said `EXIT=0 green=27', which was
TRUE about the file as it already stood.  A silently failed edit leaves
the old content in place, so every check downstream passes and says
nothing.  Edit, then verify in a SEPARATE command, and grep the file for
the text you just wrote (`grep -c '<the new phrase>'`) before believing
it landed.  os9-dev-skill-fc named this one; it was my standing habit all
evening.

**A SWEEP WITHOUT CONTROLS PROVES NOTHING -- including a sweep checking
your own work.**  At the end of the session I verified all fifteen of the
night's claimed artifacts really exist (samples shipped, dvips prologues,
fpu and its grant, the three source trees, the two dropped programs, both
checks registered, the breaker in BREAKS, the CLI proof in the
docstring): 15 present, 0 wrong.  It is only worth reporting because
three CONTROLS were in it that had to come out FALSE -- an absent file, an
absent string, a dropped program.  Without them a sweep that matched
nothing would print the same reassuring zero.  The sibling session ran the
same idea without controls first and got MISSING for all 26 items, then
false alarms on 3 of 26, both times from bad needles rather than absent
content.

**AND THE NUMBER IN A SUMMARY IS THE ONE NOBODY MEASURES.**  I reported
sixteen commits, then twenty, then twenty-two, having measured only the
first and incremented in my head after.  Measured: 57 today, or 35 since
the scrabble port -- and the gap between those two right answers is the
point, because I had never stated WHICH set I meant, so the figure could
not be wrong against anything.  State the boundary or do not state the
number.

**TWO HOUSE RULES BECAME GATES, and that is the durable result of this
evening rather than the text fixes.**  os9-dev-skill-fc put it better than
I could: every rule broken tonight was one with no mechanical enforcement,
and every rule with a gate behind it fired.  So:

  `text names what the reader has'  -- CLAUDE.md's rule that this
      collection never says what the disk LACKS.  Six entries broke it and
      had shipped.  Narrow on purpose: help.psv's 27 "there is no help
      flag" lines mean the PROGRAM has no flag, and hardware facts like
      "no sound device here" are not violations.

  `OS-9 paths count dots'  -- no CARD may chain `../..'.  Not because it
      is invalid OS-9 (it is not; see the 2026-09-13 correction below) but
      for PORTABILITY: the dotted form works on real OS-9 and on every
      os9exec build, where `../..' relative to a subdirectory failed on an
      RBF image until os9exec 985e0d8.  A card has to work on the system
      the reader already has.

**ONE GATE HAS A BREAKER; THE OTHER CANNOT HAVE ONE.  Do not read the
pair as equally proven.**  `text names what the reader has' is registered
in check_the_checks.py's BREAKS list and reports `fails as it should'.
`OS-9 paths count dots' has NO breaker and cannot: that harness copies the
DISK tree and runs the gate against the copy, while the dots check reads
the sheets and case files under tools/, which are never copied.  A breaker
touching root/ would change nothing it looks at and the tool would report
the check BLIND -- proof it does not have.  So the reason sits where the
breaker would have been, and the check is proven instead THROUGH THE REAL CLI:
a throwaway sheet with a chaining `run' line makes `check_disk.py disk'
EXIT 1 and name the check, and removing it returns exit 0.  Both
directions were probed in-process too (prose teaching the rule and a
correct `.../' form must pass, and do).  Running the CLI is the step that
separates a REGISTERED check from a merely defined one -- a function can
report perfectly while nothing calls it.  If it ever grows a root-relative target, give it a breaker.

**AND THE BREAKER I WROTE FIRST NEVER RAN.**  BREAKS is an explicit
registry; I defined the function without registering it, and the tool
reported "24 of 24 breaks were caught" -- true, and not an answer to the
question I was asking.  Not a check that missed a defect: a check never
invoked, inside the tool built to prove checks get invoked.  When you add
a check, grep the run's output for ITS OWN LABEL; a summary line that
sounds right is not evidence yours was among them.

**THE FIRST CHECK CAUGHT A HOLE IN ITSELF ON ITS FIRST FAILURE RUN.**  My
pattern was the literal `not on this disk'.  Against the old text it
caught two of three and missed `map's real wording -- "neither is on this
disk", which contains no "not".  Passing on the cleaned tree would never
have shown it.  This repo's "make every check fail once" rule, applied to
a check written to enforce a different rule, and it paid immediately.

**FINDINGS 17 AND 12's REMAINDER ARE CLOSED, measured.**  17 said the
`browse' and `uustat' help captures recorded an execution failure
(`shell: can't execute ... E_PNNF') and were committed ahead of their
binaries.  Both binaries ship now and both captures show real help --
"Browse through a directory, written by Peter da Silva" and "Syntax:
uustat [<opts>]".  It was mid-campaign when the audit ran, as it said.

12's remainder called `tail' a marginal second German program after
`exist'.  It is not: no German strings in the binary at all.  `exist',
`names' and `ff' are marked in language.psv; `tail' should not be.

**FINDING 2's PATH HALF IS REAL AND ALREADY HANDLED.**  SYS/login sets
seven CMDS subdirectories and neither GCC2 nor GCC139 is among them, so a
bare `gcc' reaches nothing -- which is exactly why those cards `cd' into
the directory and run `./gcc'.  The captions say so.  Its version half dissolves too, measured
from the binaries: GCC2/gcc IS 1.42 and its card says 1.42, matching its
own capture, which prints `gcc version 1.42' twice; gcc2 is 2.5.6 and
says 2.5; gpp is 1.40.3 and says 1.40.  GCC139/gcc is 1.39 and HAS NO
CARD -- the card called `gcc' is the GCC2 driver, run as `./gcc' from its
directory, as its caption states.  The audit compared two binaries, only
one of which is carded.  Nothing to fix.

**PLAN.md 1a IS THE NEXT REAL WORK, and its figure is stale: 72, not 27.**
Measured 2026-09-12 with the repo's own detector, tools/audit_cards.py,
which is the honest one (its header records two earlier versions that
lied).  It flags 95 of 990 -- but 23 of those are captures the INK FLOOR
correctly dropped, so no reader ever sees them.  The real set is the 61
that are flagged AND published:

    THIN-HELP     23        MOSTLY-HELP     4
    ERROR-ONLY    17        MOSTLY-ERROR    1
    NOTHING       16

It has moved twice in one evening: 95/72 as first measured, 92/69 once
the scorer bug was fixed, 84/61 once the eight no-reader converters were
excepted.  Re-measure before working from it.

**THE THIN-HELP AND ERROR-ONLY GROUPS ARE MOSTLY HONEST CARDS.**  Read
one by one rather than bucketed (my regex buckets called 22 of 31
"unclassified", which is a measurement of the regex):

  device or service genuinely absent -- CORRECT cards, leave them:
    blastem (/t0), disable + enable (/t1), xyt (no modem port), atp (no
    config file), msntp, uulog, mail + mailx + rmail (no mail spool),
    lnk.org.  And the spooler set -- lpq, lprm, lpshut: NO spooler is
    loaded at boot and `spoolqueue' does not exist on the disk, so a
    syntax line is all they can print here.  Same for submit, suspend,
    snd_sig, sbreak, run: each needs a live process or a serial path.

  NOT a defect after all -- brushtopbm, gouldtoppm, hipstopgm, hpcdtoppm,
    mtvtoppm, spottopgm, ximtoppm and xvminitoppm are eight of SIXTEEN
    netpbm readers for formats no file here is in, and netpbm here ships
    no WRITER for any of them, so no round trip can be staged.  Every one
    of those cards ALREADY SAYS SO in its caption -- "No file in that
    format ships here; handed a colour picture it reports the bad magic
    number rather than guessing" -- and the family stanza `noreader' makes
    the same point for all sixteen.  audit_cards flags them because the
    SCREEN is an error line; it cannot read the caption.  Excepted by name
    in its `fine' dict, which exists for exactly this (`perr' is the
    same shape).  I nearly rewrote sixteen working captions.

  AND `sldtoppm'/`psidtopgm' are NOT inconsistent siblings, which I also
    nearly "fixed": they omit the no-file-ships sentence because it does
    not apply -- sldtoppm has a real round trip through ppmtoacad, and
    psidtopgm decodes hex handed to it directly.  Neither is flagged.

**THIN-HELP IS 23 OF 23 HONEST -- no defects in that group at all.**
Every one states its situation in its own caption: `lpq' "With no spooler
started it says so", `UnMacpack' "No PackIt archive is on this disk to
open", `eset' "can only reach an event that has already been created",
`lgrep' "prints nothing even for a string that is present, so `grep -l'
is the one to reach for", `lmail' "hangs and has to be broken out of",
`run' "the console is that terminal already".  I counted 10 unexplained,
then 5, then 0 -- each time because my keyword net was reading a caption
TRUNCATED TO 56 CHARACTERS and judging the fragment.  Read the caption in
full before calling it silent.

**THE REAL DEFECT IN THIS LIST IS A GARBLED-CAPTURE CLUSTER, AND IT IS
THE HARNESS RATHER THAN THE SHEET.**  Eleven cards in graphics.sheet, but
the sheet is only where they happen to sit.  Characters eaten from the
front of lines, or overlapped:
`wrjpgcom' shows `$ reeware disk' for "OS-9 freeware disk", `X11R6shl'
shows `$ hl:', `basicwin' `$ in: cannot connect to X server',
`rdjpgcom.070' `$ 70 build', and loadmem/savemem/rsconvert/snap show
overlapping text.

RE-SHOOTING IN A BATCH DOES NOT FIX IT; SHOOTING ONE ALONE DOES.  That
is the whole diagnosis and it is measured.  All eleven re-shot
together came back BYTE-IDENTICAL (basicwin: ink 15, `in: cannot connect
to X server').  `basicwin' shot ALONE in a fresh session came back
perfect -- ink 46, `basicwin: cannot connect to X server', name intact.
Same stanza, same image, same command; only the SESSION differs.

`graph' IS THE TWELFTH MEMBER, not a separate case as this file first
said.  Its stanza is at graphics.sheet:1242, inside the cluster; its old
capture was garbled identically (`$ parity = 1cf6H000Heentrant execute in
supervisor statede M'); and a solo shoot cleaned it to a proper modinfo
listing.  It was the FIRST evidence of the cure and I misread it as a
stale capture.  Every one of the twelve shot singly comes back clean:
X11R6shl 15 -> 56, xengine 14 -> 40, loadmem 7 -> 157, savemem 7 -> 129,
rsconvert 16 -> 61, snap 4 -> 332 -- eighty-fold on that last one, same
stanza, same image.

WHAT IS REFUTED, measured 2026-09-13.  Three explanations written here
were wrong, and each died on a cheap experiment.  Do not re-derive them:

  ACCUMULATED STATE ACROSS A LONG RUN -- no.  `--only' on twelve of the
  cluster reproduces the damage exactly, with the sixty earlier stanzas
  of the sheet never run.

  POSITION IN THE SESSION -- no.  loadmem, savemem and snap shot as
  positions 1, 2 and 3 of their own session come back 157, 129 and 332,
  which are their solo values.

  `wgen' LEAVING KEYSTROKES UNCONSUMED -- no.  The batch that reproduced
  the damage did not include wgen at all.  A bisect of `graph' then
  `loadmem' is also clean (406 and 157), so graph alone does not poison
  the session either.

WHAT IS MEASURED.  In a twelve-stanza batch the loss is PROPORTIONAL and
grows with position; it is not a binary seven-of-twelve:

    pos 1    cjpeg.070                       48 of 48, 0% lost
    pos 2-4  wrjpgcom, wrjpgcom.070, rdjpgcom.070    20-26% lost
    pos 5-8  graph, loadmem, savemem, snap           95-99% lost
    pos 9-12 basicwin, xengine, X11R6shl, rsconvert  65-74% lost

  From position 5 on, every stanza yields roughly 4-21 ink whatever it
  ought to print -- about what the echoed command alone is worth.

THE READINESS GUARD ALREADY EXISTS, so "the harness resets only half of
it" is not the whole story.  run_sheet does `if died or starved or not
sess.ready()' after EVERY stanza and replaces the session when that
fails; ready() makes the shell echo a SPLIT marker, which only a shell
that runs the command can rejoin.  No session was replaced during any
run above, so the shell was answering every time.  And the interrupt in
this harness is \005 (Ctrl-E -- close() and the `kill' directive use
it), not \003.  Shooting one at a time is still a REPAIR that the next
full-sheet run will undo.

THE SEAM IS LOCATED -- start here rather than re-deriving this.  In
tools/screenshots.py, the per-stanza head does:

    sess.write("builtin cd /dd\r")     # resets the DATA DIRECTORY
    sess.write("clear\r")

and that is all it resets.  `self.buf' only ever grows (`_drain' does
`buf.extend(chunk)') and nothing clears pending input between stanzas.
Read that together with THE READINESS GUARD above, not instead of it: no
interrupt is sent AT THE STANZA HEAD, but ready() does run after every
stanza and replaces the session when the shell does not answer, and
_drive() already ends each stanza with \005.  So "a program left at a
prompt eats the next stanza's first characters" cannot be the whole
story -- such a program would eat ready()'s marker too, and the session
would have been replaced.  It never was in any run measured here.

Note also that buf never shrinking is not itself the bug: mark() returns
a POSITION in it, so a stanza's start is a read offset and clearing the
buffer would invalidate every stored offset.  A fix advances the offset;
it does not empty the buffer.

**FOUND AND FIXED, 2026-09-13 (commit 090b27a5).** It is none of the
above and no interrupt was needed. OS-9 ends a display line with a bare
CARRIAGE RETURN and SCF appends the line feed itself, gated on the path
option PD_ALF. A program wanting a clean binary stream clears PD_ALF,
and the change OUTLIVES IT AND REACHES OTHER PATHS -- so one program
clearing it leaves the shell and every later stanza writing CR with no
LF. (HOW it reaches them is unsettled and does not matter to the fix:
os9exec's pCsetopt copies the option block to every path on the device
and says real OS-9 does too, while the v2.4 manual read plainly puts the
table in the PATH descriptor, per path. PD_PATHS at $16, the "List of
Open Paths on Device", and inherited standard paths sharing a descriptor
both explain the observation without SS_Opt being device-scoped. The
rule that holds either way: never assume an option change is private to
your own path.) Each
line lands back at column 0 on top of the last, and the next prompt
overwrites the first six characters: `basicw' is six characters, and so
is "bash# ". That is the whole of the "six characters lost from the
start of the line" recorded above.

THE BYTES ALWAYS ARRIVED. A probe of the raw pty stream (scratchpad,
probe_raw.py) found loadmem sending 212 bytes and rendering as ink 7;
nine of twelve stanzas were "arrived, lost in rendering". ansiscreen is
blameless -- `if ch == chr(13): self.col = 0' is correct terminal
behaviour for a stream with no line feeds in it. So are the programs.

Measured both ways: loadmem alone gives LF=5 CR=5 ink 157; after
cjpeg.070 it gives LF=1 CR=5 ink 7. A session cannot be un-poisoned from
outside OS-9, so screenshots.py's alf_off() spots the signature in the
stanza's own slice and replaces the session, as it does for `starved'.
Validated on the twelve-stanza batch: every one now matches its solo
value, and promoting the result changed NOTHING in docs/screens -- the
guarded batch reproduces the solo captures exactly.

THE PROGRAMS WERE ALWAYS INNOCENT, and so was the capture path.  Run
straight through os9try, `basicwin' prints `basicwin: cannot connect to
X server'; its card showed `in: cannot connect to X server'.  Those six
characters were never LOST anywhere -- they were OVERWRITTEN in place by
the prompt that followed, for the reason above.  Nothing in the capture
path drops bytes, which is why every hunt for where they went failed.

THE INK FLOOR WAS MASKING IT (2026-09-13).  gen_screens drops a capture
under 30 ink, so most of the damaged ones never reached a reader and the
damage read as smaller than it was.  Ten are now repaired by solo
shoots.  FOUR WERE PUBLISHED DAMAGED: graphdemo and graphsave at 33 --
three points over the floor -- each showing a whole os9exec abort dump
collapsed into `Cons /termd/CMDSs Aborted'; wgen at 64; mgif at 55.
SIX WERE DROPPED BY THE FLOOR and so had no card at all, though each has
a stanza and a full caption: g, striche, apfel, sine, showpic, tplot.
The gallery went 893 -> 899 and audit_cards 79 -> 72.

`wgen' is BETTER, NOT FIXED: 64 -> 140 ink and it now shows its dialogue,
but the prompt lines are still torn around the echoed input (`S75',
`e20').  Solo shooting does not cure that one.

panel-exceptions.psv is UNCHANGED and correct: the recovered dumps show
graphdemo and graphsave really do abort with no G-Windows display, which
is what those entries say.  Only the card text was damaged -- an
exception can enshrine a harness artefact, so read the capture before
removing one.

**THE DETECTOR HAD A BUG THAT INVENTED EMPTY CARDS.**  `strings' prints
its offsets as `$00017F: <text>', and audit_cards' PROMPT pattern stripped
a leading bare `$', leaving `00017F: ...', which then matched the branch
that treats a line as the TYPED COMMAND.  A card with fourteen lines of
real output scored work=0 and was reported NOTHING.  Narrowed to
`\$(?=\s)' -- a bare `$' is a prompt only when a space follows it.  Only
`strings' was affected, but the shape would hide any program printing an
address or an offset.

I found it by DISBELIEVING THE VERDICT: the card looked full and the
program plainly worked, so the tool was wrong rather than the card.  The
first two cards I investigated from the flag list (`graph', `rdjpgcom')
were also not defects -- both were stale captures from before fixes
elsewhere, and re-shooting fixed both.  THREE of the first four
investigated were false alarms.  Re-shoot, then disbelieve the tool,
before diagnosing a program.

audit_cards scores from notes/playtests, not from docs/screens.js, so it
cannot tell a thin published card from a capture that was never
published.  Split them before counting: `cls', `byteflip', `bootlogger'
and 20 others have NO published card at all.

WHERE THE WORK IS, by category: Communications 27, Graphics 23, System &
modules 16 -- so this is probably two or three systemic causes (no
network, no display, no live service) rather than 72 separate defects.
The plan's own record says the fix is nearly always THE INVOCATION rather
than the program: `hc' was a text filter run as a calculator, `zoo2'
wanted a bare letter, eleven Dhrystones were waiting on stdin.

AND CHECK WHETHER THE PROGRAM CAN SHOW ANYTHING AT ALL FIRST.  `graph' is
the Graph trap library, a type-$0B module and not a program; `loadmem' and
`savemem' are super-user only.  A NOTHING card for those is correct, the
way fpu's absence from the panel ratchet is correct.

**SO THE CARD AUDIT IS FULLY WORKED.**  Of the six HIGH: 1 closed at 0
(try-line paths), 2 accounted for, 3 did not reproduce, 4 not
reproducible, 5 real but a PHRASING defect, 6 fixed.  Of the rest: 9 and
10 real and fixed AT SOURCE (a fence chosen by content; three captions
completed), 11 half real and fixed, 7 / 13 / 17 / 20 / 12's remainder all
measured clean, and 16 and 19 WRONG.  Nine of fifteen dissolved on
measurement -- which is the ratio worth remembering before acting on any
audit, including one's own.

**FINDING 20 DISSOLVES TOO -- the "error message as help" captures are
RIGHT.**  The audit said 72 help captures are option-rejection messages
presented under "its own help"; measured, it is 28, and they are not
defects.  These are GNU tools whose answer to `-?' is to reject the flag
AND PRINT THEIR USAGE:

    join: unrecognized option `-?'
    Usage: join [-a 1|2] [-v 1|2] [-e empty-string] [-o field-list...]

The rejection line is one line of honest noise above the thing the reader
wants.  Re-capturing all 28 would have replaced working help with
identical help.  Check what follows the error before calling a capture
broken.

**FINDING 7 IS CLOSED, measured 0.**  The audit said 47 cards show a
sample that never invokes the program the card is about.  Measured
2026-09-12 against docs/screens.js: EVERY card's screen or try line names
its own program -- 0 exceptions needed.  The 47 predate the `try' line and
the `panels show their own program' ratchet, which closed it.  Do not
re-derive it.

**FINDING 13 RECONCILES -- it was stale, not wrong.**  The audit said the
header arithmetic left no room for the BASIC09 four (992 vs 988).
Measured 2026-09-12: 996 gathered, 340 starred, 4 BASIC09, leaving
exactly 652 unstarred non-BASIC09 -- which is what CATALOG.md's header
claims.  It adds up; do not re-derive it.

**CARD-AUDIT FINDINGS 16 AND 19 ARE BOTH WRONG -- do not act on them.**
Measured 2026-09-12 after nearly "fixing" both.

16 said `dedit' and `who' fall through the panel ratchet.  They do not:
audit_panels.runnable() is every type-$01 module, `who' is a shell script
and `dedit' is type-$02 I-code, so both are correctly outside it.  Same
for `fpu'/`fpu040' (type-$0C descriptors) which I had just shipped.  I
gave all four panel-exceptions rows and the EXISTING gate rejected three
as "listed but is not a runnable program" -- the system telling me I had
the wrong instrument.  Reverted.

19 called four screens "orphaned in a superseded format".  They are not
orphans: gen_screens.collect() draws names from sheets | CAPTIONS |
play-tests, and all four have play-test captures (two are in CAPTIONS as
well), so it re-emits them on every run -- it rmtree's docs/screens and
rewrites it wholesale.  I deleted them twice and the generator put them
back both times.  Nothing to do.

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

**OS-9 COUNTS DOTS: `...' IS TWO LEVELS UP.**  Professional OS-9 v2.4,
"Accessing Files and Directories: The Pathlist", p. 4-9:

    "A single period (.) refers to the current directory.  Two periods
     (..) refer to the current directory's parent directory.  Add a
     period for each higher directory level.  For example, to specify a
     directory two levels above the current directory, three periods are
     required.  Four periods refer to a directory three levels above."

So `..' DOES resolve mid-path, as a real traversal -- `list ../DEFS/curses.h'
from /dd/CMDS reads the file.  Two levels up from /dd/CMDS/GCC2 is
`.../SYS/motd'.

**CHAINING IS NOT FORBIDDEN, AND AN EARLIER VERSION OF THIS ENTRY SAID IT
WAS.**  Corrected 2026-09-13.  rdoggett, who has run the real hardware,
gives the rule as: a component made only of dots climbs (dots - 1) levels
and components ADD UP, so `../..' is two one-level components reaching the
same place as `...'; his example is `../......./.././file', and he treats
`dir ../../../../../sys' failing as a BUG.  p. 4-9 teaches the dotted form
without excluding chaining, and no Microware line settling it either way
has been found.  os9exec-83 had agreed with the old reading and has
RETRACTED it; os9exec 985e0d8 (2026-09-13) makes relative `../..' climb
on RBF images.  So the measurements below are real and are PRE-985e0d8;
they record what one emulator build did, not what OS-9 forbids.

MEASURED HERE 2026-09-12, from /dd/CMDS/GCC2, with the disk's own `cat':

    cat .../SYS/motd        -> reads it.  Dot-counting works for OPENS,
                               not just for chd.
    cat ../../SYS/motd      -> E_PNNF, though /dd/SYS/motd exists
    cat ../../DEFS/curses.h -> E_PNNF, though /dd/DEFS/curses.h exists

THREE BEHAVIOURS, NOT TWO -- and the third caught me claiming a bug that
was not there.  The `for' card ran `../../CMDS/for div.f' from
/dd/tmp/CMPA for as long as it existed, and its PREVIOUSLY PUBLISHED
capture shows it working: `rtf div.f', ` STOP: compilation aborted',
identical to the corrected form.  So:

    bash forking a path   `../../CMDS/for'  -> WORKS (measured, old card)
    chd                   `chd ../..'       -> two levels (os9exec-cb)
    a program's open()    `cat ../../x'     -> FAILS, E_PNNF (measured)

The dotted form works for all three and is what the manual documents, so
prefer it everywhere.  But do NOT assume a chained path is broken because
one of these three refuses it -- I changed the `for' card believing I was
fixing a live defect, and the capture proved the spelling had never been
costing anything.  The change stands (documented-correct beats
accidentally-working); the claim did not.

NOTE A DISAGREEMENT WORTH KEEPING.  os9exec-cb measured `chd ../..' from
two levels down landing TWO levels up, and predicted from that my opens
should have succeeded.  They did not.  So `chd ../..' and
`open("../../x")' do not resolve alike, and this repo already knew the
open half -- tools/datatests/modules.cases:79 says `which' "climbed with
`../..' once, which on OS-9 opens the parent again".  Trust the dotted
form; do not model `../..' from chd's behaviour.

THE TRAP IS THAT THE WRONG SPELLING FAILS QUIETLY.  The extra components
are absorbed rather than rejected, so `../..' lands on the PARENT and the
error names the FILE you asked for, not the path that misdirected you.
Code that climbs by appending `/..' moves exactly one level and then
silently stops.

The GCC cards stage `hello.c' where they run, and that stands -- it is
more robust than reaching across the disk either way.  But the reason in
the commit is the pathlist being malformed, NOT any inability to climb.

**How I got it wrong, which is the part worth keeping.**  Five failures
shared two properties: running from a subdirectory, and using `../..'.  I
blamed the first.  My one counter-example, `gcc_cccp', differed in BOTH,
so it could not tell them apart -- and I read it as confirmation anyway.
A single failing case does not tell you which of its features caused the
failure; find the case that differs in one.

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
- **creadoc** FIXED, and both halves of the old entry here were wrong. It
  read each filename from column 53 of a `dir -eadu' listing where
  Microware's dir puts it at 54 -- measured over 666 lines in four
  directories, sector addresses two to five hex digits wide and sizes two
  to seven, both fields right-aligned, the name at 54 in every one. So 53
  was right nowhere, and it does write creadoc.txt once the column is. Not
  F$PrsNam, which follows the 68k manual and does not skip a leading space.
  Rebuilt through rtf -> r68 -> l68 with the SDK's utilities: the UNPATCHED
  rebuild differs from the shipped binary in 4 bytes (an M$Excpt vestige at
  0x37, outside the 24-word parity range, plus the 3 CRC bytes), which is
  what makes the provenance clean; the fixed one differs in 5 -- those plus
  offset 0x61D, ASCII `5' -> `6'. RTF stores the constant as text, so "one
  constant" is literally one character. CRC and parity verify on both.
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

- **The archive question is ANSWERED, 2026-09-13 -- read
  `notes/PLAN-acquisitions.md', "Archive state after the 2026-09-13
  sweep", before searching anything.**  The Internet Archive is back up
  and was swept; alt.sources is exhausted for OSK (8 subject hits in
  12,026 articles, all fetched, none shippable); colorcomputerarchive was
  fetched and IS out of scope apart from one thing -- The OSKer, an OSK
  magazine, six issues 1990-91, which carries a public-domain submissions
  clause worth citing but NO source to acquire; ftp.uni-kl.de is alive
  and is now a Debian mirror; RTSI is a CMS with no reachable tree.
  **The one live question is where a copy of comp.os.os9 1987-2002
  exists** -- what we hold starts in 2003, and it is not on IA and not in
  utzoo, which is torrent-only and stops mid-1991.
- Q2 and Microware's `fpu' are DONE (`e934210a', `7ae0a430'), and
  FOR-RDOGGETT.md no longer lists them.  What is left there is his alone:
  nothing pushed or tagged, the release not carrying the tar, and no
  real-hardware test.
- Everything in ROADMAP-freeware.md about the release -- CI never exercised,
  branch never pushed, nothing tagged -- is yours.

## A MEASUREMENT TRAP THAT COST TIME TWICE IN ONE NIGHT (2026-09-13)

**Never compare a raw capture in `notes/playtests' against a published
card in `docs/screens' without running it through `gen_screens.trim()'
first.  They are not the same text.**

`gen_screens' rewrites the shell prompt on the way to publication --
`PROMPT = re.compile(r"^bash#\s?")' becomes `$ ' -- and it also strips
the trailing prompt, the login noise and os9exec's file-table dump.  So
a raw capture says `bash# ppmpat ...' where the published card says
`$ ppmpat ...'.

Any ink measure that EXCLUDES lines containing `bash#' -- which
screenshots.py's own `ink()' does, deliberately, because the shell's
prompt is not the program's output -- therefore counts those command
lines in the PUBLISHED card and discards them in the RAW one.  The
bigger the stanza, the bigger the phantom loss.

It bit twice, in different disguises:

  1. Restoring twelve captures from backup and diffing them against the
     published cards reported `10 of 12 MISMATCH'.  The restore was
     byte-perfect.
  2. Validating the PD_ALF guard over a whole sheet reported `35 of 86
     DEGRADED', including setup-image at position 1, where no guard had
     fired and nothing could have poisoned anything.  Re-measured
     through trim(), it was 84 equivalent, 1 improved, 1 transient.

The tell is that the flagged set has MORE `run' lines than the
unflagged: 6.1 against 3.0 in the second case.  If a "degradation" tracks
command count rather than program behaviour, it is this.

    new = gen_screens.ink(gen_screens.trim(open(cap).read(), try_line))
    old = gen_screens.ink(open('docs/screens/NAME.txt').read())

## How far the PD_ALF fault reaches -- NOT confined to graphics.sheet

After the guard landed I predicted three more sheets would carry it --
`netpbm-ea' (31 stanzas), `netpbm-in' (22), `netpbm' (18) -- on the
grounds that graphics.sheet's nine firings were all netpbm programs
writing binary with a redirect, and those sheets are full of exactly
that.  **The prediction was WRONG.**  All 71 re-shot with the guard in
place:

    guard fired            0 times
    trim()-measured        70 equivalent, 0 improved, 0 degraded

So no program in those three clears PD_ALF, and there are no hidden
victims in them.

**THERE IS NO WORKING PREDICTOR FOR WHICH PROGRAMS CLEAR PD_ALF, and I
proposed two that both failed.**  First "netpbm program writing binary
through a redirect" -- predicted three sheets, which came back with ZERO
firings in 71 stanzas.  Then "terminal-takers and raw-byte writers",
which fitted the first few and does not hold either: of fifteen clearers
checked for termcap-ish strings, only SEVEN have any (wanderer 7, larn
11, mines 7, scrabble 7, sterm 8, hinterhalt 7, sddemo 7) and EIGHT have
none at all (giftopnm, pgmbentley, ppmrelief, zot, connect, txmod,
filter, casefix).  `casefix' settles it: a six-kilobyte sentence-case
filter that reads standard input from an `echo' pipe, with no terminal
handling of any kind, and it clears PD_ALF.

So do not reason about which sheets are at risk.  **Sweep them.**  That
is the only instrument that has ever been right about this, and it is
cheap to run measure-only with an unconditional restore.

**SWEEP TALLY, 2026-09-13: THE SWEEP IS COMPLETE -- 929 of 929 stanzas,
every sheet, nothing left unswept.**  Thirty-six clearers in all.

Clearers by sheet: graphics 9, games 5, comms 4, archives 3 (`lha',
`lharc', `lharcs'), system 2, printing 2 (`gs33', `gs403'), files 2
(`remove', `Ascii2Libr'), encoding 2 (`des', `macunpack'), textfilters 1
(`casefix'), editors 1 (`vi'), shells 1 (`hist'), played 1 (`sc'),
calendars 1 (`calen'), maths 1 (`checkfile'), documentation 1 (`help').

ZERO in netpbm-ea, netpbm-in, netpbm, devtools, texttools, compilers,
tex, amusements, dos, languages and toys -- eleven sheets clean.

**Every sheet swept since the guard landed came out with 0 REAL
candidates and 0 LOWER.**  That is the whole result: across 929 stanzas
the guard caught thirty-six sessions with PD_ALF cleared and not one
published card was damaged by one.  Equivalent counts where recorded:
tex 32, encoding 31, archives 30, files 36, compilers 40, devtools 43,
texttools 42, printing 14, calendars 13, maths 11, languages 10,
documentation 5, toys 3.

**Do not re-sweep anything for PD_ALF.**  The question the sweep was
opened to answer is answered.  Re-shoot a stanza when you have a reason
of its own -- a card that looks wrong, a program that changed -- not to
look for clearers again.

## The sweep's unexplained patterns, resolved 2026-09-13

Two patterns survived the sweep looking like findings.  Neither was.

**`sed' and `sed_1.06' both landing on EXACTLY 104 was batch damage, not
a shared program.**  Solo, on a rebuilt image, they read 143 and 148
against published 142 and 147 -- equivalent, both of them.  Two stanzas
arriving at an identical ink is a signature of a shared FAILURE MODE
(one wrecked session measured twice), and reads as evidence of a shared
cause only if you forget that the batch is the thing they share.  When
two numbers match exactly, suspect the instrument first.

**The uniform +40 across the `dos' family is a STALE-CARD finding, and
the re-shoots are the truthful side.**  `msdir' 130->170, `mscheck'
174->214, `mscopy' 151->190, `msmd' 141->181 -- four programs, one
number.  The cause is in the DATA they share, not in any of them: the
shipped `disk/DOS/a.img' holds a volume label and **`README.TXT', 139
bytes, with a long-filename entry** (read straight out of its FAT12 root
directory host-side -- 224 root entries at offset 9728, no OS-9 needed).
So on a FRESHLY BUILT image every listing of the DOS root carries that
line, and four published cards do not: they were shot against a `.dd'
whose `a.img' had lost it.

**I guessed a fifth and the re-shoot refuted it, which is worth more
than the four that were right.**  `msren' ends `msdir a: | grep TXT',
and I wrote that it must now match `README   TXT' too.  It does not:
mtools prints the entry with its lowercase flags honoured, as
`readme   txt', and `grep TXT' is case-sensitive.  `msren' changed for
an unrelated reason found in the same capture -- see below.

Two things worth keeping from it.  **A uniform gain across a family of
programs points at their shared INPUT, not at the programs** -- the four
differ in everything except which directory they list.  And the image is
a build artefact whose contents drift from `disk/' in ways nothing
flags: `git status' was clean on `disk/DOS/a.img' throughout, because the
file that had lost README.TXT was the built image, never the source.
`tools/mkimage.sh' takes four seconds and is the first move, not the
last.

`tools/datatests/dos.cases' is unaffected -- every case asserts a name
present or absent (`RAW      TXT', `NEW      TXT', `MOTD     TXT'), none
asserts a file COUNT, so the extra entry breaks nothing.  **That was
reasoning from reading the cases; it has since been RUN, and it holds:
dos 10 of 10 and tail 17 of 17 pass on the rebuilt image** (tail matters
too -- it asserts against `/dd/DOS/a.img' as well).

Two traps on the way to running them, both mine and both already written
down elsewhere in this file, which is the point:

  * `datatest.py' needs `gtimeout' and it lives in `/opt/local/bin'.  A
    background job whose PATH lacks it dies with `FileNotFoundError:
    gtimeout' before a single case runs.  Export the PATH.
  * and the run REPORTED SUCCESS anyway, because the script ended
    `python3 tools/datatest.py ... | tail -25' and then read `$?' --
    which is `tail's, and always 0.  I documented that trap tonight and
    walked into it within the hour.  Capture the output in a variable
    and read the status of the command itself.

**What `msren' actually caught: three dos cards were showing OTHER
STANZAS' leftovers.**  Its listing carried `MOTD     TXT', which its own
setup never creates -- `mscopy' and `msmd' had left it on the shared
image earlier in the same run -- and `mscheck' was reporting `Skipping
"DOCS", is a directory' for a directory `msmd' had made.  The sheet's
own header promises the opposite in so many words: "Every stanza puts
the image into the state it needs before its picture, so the sheet means
the same thing on every run."  Three setups now delete what they do not
want (`msmd' and `msren' remove `MOTD.TXT', `mscheck' removes `DOCS'),
which is gate twenty's rule applied to a shared DOS image rather than to
`/dd/tmp'.

## The capture directory is GITIGNORED, so "tree: 0 modified" proved nothing

Found 2026-09-13, and it applies to every sweep job in this session.

`notes/playtests/' is ignored in full (`.gitignore' line 52); 2,374
captures sit on disk and FIVE are tracked.  So the reassurance those
jobs printed after restoring -- `tree: 0 modified' -- could not have
reported capture churn under any circumstances.  It was a check that
cannot fail, which is this collection's signature defect, and I printed
it a dozen times tonight without once asking what it was measuring.

**The real instrument is `tools/gen_screens.py --check'**, which exits 1
naming captures that have drifted.  Use it, and know its limit:

  * It compares a capture against its STANZA -- caption and commands.
    Edit a sheet and it names the affected shots at once (it named
    `msmd', `msren' and `mscheck' the moment their setups changed).
  * **It cannot see a capture that was shot against the WRONG IMAGE.**
    The four stale dos cards had unedited stanzas, so they matched and
    the check was silent.  Nothing in the tree can catch that class; it
    took reading the DOS image's directory to find it.

**And do not pipe a gate into `tail'** -- `$?' is then `tail's, which is
always 0.  `gen_screens.py --check | tail -40' printed `3 stale ...
before committing' and reported exit 0 in the same breath; run unpiped
it exits 1.  The same trap applies to `check_disk.py'.  Redirect, then
read `$?'.

## Working the flagged-card queue down, 2026-09-13: 66 of 990 -> 37 of 929

Both numbers moved, and the DENOMINATOR moving is the more interesting
half.

**`audit_cards' was scoring 61 captures the gallery never publishes.**
`notes/playtests' holds 990 captures and the sheets define 929 stanzas;
the other 61 are setup shots, multi-program captures and leftovers
(`about-tar', `elm-suite', `gnuchess-builds', `cal-holidays' ...), and
`gen_screens' names them every single run -- "N capture(s) belong to no
stanza and are NOT published".  The audit read that directory straight
off disk and scored all 990, so it reported on things no reader can see
and put one of them, `sgi-p', in a queue of cards to go and fix.  It now
skips any capture with no stanza.  Nothing else consumed that number.

**Every name excepted below was READ FIRST** -- its stanza, its capture,
its `DOC/INDEX' and `howto.psv' lines, and its binary's strings where
that settled anything.  An exception is only honest when somebody has
looked, and four leads died on inspection (below), which is the reason
to keep looking rather than to stop.

The count moved in this order, so a later session can see what was a fix
and what was a judgement: 66 at the start; **59** when `classify' stopped
eating each card's first line (a BUG, not a judgement -- seven cards were
reported NOTHING while showing real output); 58, 57, 55, 48 as eleven
names were read and excepted; **39** after seven more exceptions and two
real card fixes; **37** when `afm2tfm' was fixed and `sgi-p' stopped
being counted.  Four cards were genuinely REPAIRED tonight -- `UnMacpack',
`macunpack', `finger', `afm2tfm' -- and each left the list by showing
its program working, not by being excused.

Eleven names went into `audit_cards.py's `fine' table, in families:

  the print spooler (4)   `lpq', `lprm', `lpsched', `lpshut'.  THERE IS
        NO SPOOLER ON THIS DISK.  Two of these already RUN for real on
        their cards and report the true state -- `lpq: no spooler
        installed', `lpshut: no spooler active' -- `lprm' really tries a
        removal, and `lpsched' WAITS to open a printer if given one.
  collect2 (3)            `collect', `gcc_collect', `gpp_collect'.  A
        g++ LINKER PASS, not a user-facing program.  `collect' and
        `gpp_collect' are the same binary (md5 74b3bbf3686d) in two
        directories; `gcc_collect' is GCC139's build.  It takes no `-?'
        and prints its usage with no arguments BY DESIGN.
  cards that must not run (1)  `flink' -- it corrupts the disk it links
        on; CLAUDE.md forbids running it at all.
  cards that already do the real thing (2)  `lgrep' searches
        `SYS/password' for `ksh', which IS in that file, and prints
        nothing (the silence is the finding, and the caption says so);
        `run' already does `export PORT=/term; run "whoami"'.
  no device (1)           `transfer' wants the GDOS device DGDOS0.

**Left flagged ON PURPOSE, because they are improvable:**

  `submit'   a real OS-9 `.sub' DOES ship -- `DOC/hexed/hexed.sub' -- but
             the command inside it is `cc ... -f=/d0/CMDS/hexed', which
             needs Microware's cc, `/r0' and `/d0', none of them here.
             A `.sub' whose command exists on this disk would make a real
             card.  (The other two `.sub' files in the tree are autotools
             `config.sub' scripts, not OS-9 submit files.)
  `afm2tfm'  **FIXED.** Its caption said "there being no .afm on the
             disk" and SIXTEEN ship in `LIB/gs403' plus two in
             `ETC/LIB/GS33', real ones (`StartFontMetrics 3.0', URW).
             Run on one it works: `afm2tfm n019003l.afm' answers
             `n019003l NimbusSanL-Regu' and writes a 1,268-byte .tfm.
             The card now converts a font instead of printing a usage
             line, and the caption no longer says something untrue.
  `UnMacpack' **FIXED.** Its stanza asked `-?', which the program REJECTS
             (`UnMacpack: unknown option -?') while printing a line that
             names the right flag: "Use macunpack -H for help".
             `tools/help.psv' already recorded `-H'.  The card now shows
             the whole option list -- fork modes, the Mac-to-Unix text
             translation, the listing and query modes.
  `finger'   **FIXED.** Its caption said it needs a network; it reads the
             password file THIS DISK SHIPS.  `finger tester' answers with
             the account's home directory, its shell, and the `.project'
             and `.plan' it would print if they existed.
  `lmail'    its caption says a real recipient hangs it.  Unverified --
             if that is right it belongs with `flink'; nobody has tried.

**THE REMAINING 30 ARE LEFT FLAGGED ON PURPOSE.  Do not sweep them into
exceptions.**  Every one has been read; they fall into two families and
a short tail, and the flag is the honest prompt that a better card would
be welcome if the world ever supplies one.

  15 ERROR-ONLY, all ABSENT HARDWARE OR SERVICE, each card already
     running for real and printing the refusal: `basicwin' and `xengine'
     want an X server, `blastem' and `xyt' a modem, `disable' and
     `enable' the device `/t1', `mail' the RAM disk `/r0', `mailx' and
     `rmail' a mailbox directory, `msntp' a socket, `uwho' `/etc/utmp',
     `uuxqt' a `procs' module, `uulog' a log whose own CONTENT contains
     the word ERROR, `lnk.org' a `shell' module to fork, and `rcsmerge'
     the `merge' binary this disk has no build of.
  11 NOTHING, programs that genuinely say nothing when run alone:
     `authwn', `inetdc' and `splman' are server helpers invoked per
     request; `elvprsv' runs only when elvis dies; `byteflip' and
     `wysecrack' end the session or wait on hardware; `cls' clears the
     screen, which is what it is FOR; `infoxpress' and `puzzle' want a
     serial host and G-Windows; `pgmedge' and `vtxtcn' wedge the capture
     session (both measured, both with panel-exceptions of their own).
  the tail of 4: `lmail', `loadmem', `submit' (a `.sub' ships but the
     command inside it needs Microware's cc), and `pdraw', which is a
     WORKING card scored MOSTLY-HELP only because its option echo lines
     match the usage pattern.

  (The list above was written from memory first and had `filter' and
  `macunpack' in it -- one excepted earlier tonight, one REPAIRED
  tonight -- sixteen names for fifteen slots.  It is now taken from
  `tools/audit_cards.py' output.  Do the same before quoting it.)

So the queue is now a list of things the DISK cannot do, not a list of
cards nobody has looked at.  That is the state it should be handed on
in.

**Four leads that died on inspection, recorded so they are not chased
again.**  `unsit's caption says no StuffIt archive is on the disk, and
three `.sit' files ship in `DOC/orbit' -- which looked like a caption
contradicting its own disk.  They are 119-124 BYTE TEXT FILES (`XXXX
Bern-Airport', `W3VC Pittsburgh'), orbit's ground-station data wearing
that extension, and `unsit' is not even flagged.  Judging a file by its
extension is the same proxy trap as judging a card by its size.

`fontgen' looked like the missing half of `setfont': a font generator on
a disk whose font loader has no font.  It is not.  It writes ASSEMBLER
SOURCE for a font data module -- `nam text80z.font', a psect, FontData --
for the Gepard 80-column card, and `setfont' wants a downloadable
terminal font.  Two programs about fonts are not a pipeline.  (`fontgen'
is a good card already, work=7, never flagged.)

`lnk.org' and `rcsmerge' died the same way -- see the section below.

**Those two were then tested, 2026-09-13, and the test earned its ten
minutes twice over.**

`savemem' RUNS.  The harness is the super user and hex addresses are
easy, so both of its stated requirements are met -- and `savemem 0 100
mem.out' creates `mem.out' at ZERO BYTES.  A card showing an empty
output file is worse than the syntax line, so the syntax line stays and
`savemem' is excepted with that measurement attached.  `loadmem' is the
same program backwards, writing INTO memory; it has not been tried and
should not be for the sake of a card.

**`snd_sig' took two runs, and BOTH taught something.  It is excepted:
this bash sets `$!' to ZERO.**  Backgrounding `cat > /nil &' makes the
shell announce the job on screen as `<3>' -- that is the pid, in OS-9's
own notation -- but `P=$!' then reads 0, so `echo pid is $P' prints
`pid is 0' and snd_sig answers `illegal wake parameter-0'.  A stanza
therefore cannot learn a pid to pass on; the number is on the screen and
nowhere a script can reach.  And a successful wake prints nothing
anyway, so even if the pid were available the card would show a command
and silence.  **Do not reach for `$!' in a sheet: it is 0 here.**

The FIRST run failed differently, and that lesson is the wider one:
**`!' INSIDE DOUBLE QUOTES TRIGGERS HISTORY EXPANSION.**
The stanza ran `echo "backgrounded pid $!"' and the shell answered

    ": Event not found.

so `$!' never reached `echo', and the `snd_sig $!' after it got an empty
argument and said `illegal wake parameter-0'.  Nothing was wrong with
snd_sig; the harness line was wrong.  This shell is INTERACTIVE, so
history expansion is on.  Use single quotes, assign `P=$!' unquoted, or
put `set +H' ahead of it.

**The exposure was then measured, and it is narrow.**  A `!' followed by
WHITESPACE is not an expansion, which is why the one shipped sheet line
that carries a bang in a double-quoted string -- `printf "#! rnews %s\r"'
in `comms.sheet' -- has always worked.  What bites is `!' followed by a
word character or by the closing quote, as in `$!"'.  And no published
card is damaged: **zero of 990 captures and zero of 899 published
screens carry `Event not found'**, which is the signature.  So this is a
trap for the next stanza somebody writes, not a defect in the gallery.

## Four flagged cards put to the test, 2026-09-13 (scratch sheet, then deleted)

The way to ask "could this card be better?" is a SCRATCH SHEET run
through `screenshots.py' -- a sheet path is just an argument, so a
throwaway sheet in the scratchpad works and the gallery never sees it.
**Delete the captures afterwards by explicit name.**  `audit_cards'
scores every `*.shot.txt' in `notes/playtests', so a leftover diagnostic
becomes a card in the count; and in zsh a glob that matches nothing
aborts the whole `rm', so `rm -f a[BC].raw' silently removes NOTHING
INCLUDING THE FILES THAT DID MATCH.  Ten strays were left that way.

  `pgmedge'   NOT broken.  On an 8x8 image it completes and `pnmfile'
              reads the result back: `PGM raw, 8 by 8'.  So the empty
              card is about TIME, not capability -- see the section
              below, where the older stanza is the fix.
  `vtxtcn'    wedges the session: `(session replaced)' with 25 seconds
              allowed, and the `ls' after it never ran.  Its
              `panel-exceptions' line says "the ls that follows on its
              card is the evidence" -- THERE IS NO ls ON ITS CARD, and
              cannot be while it does this.
  `byteflip'  honest, and now proven so.  The disk's own `dbz' WILL
              build the base it wants (`dbz base' wrote base.dir and a
              349 KB base.pag from three echoed lines), and `byteflip'
              on that base still ends the session.  Its caption already
              says it ends the shell outright.  No better card exists.
  `rcsmerge'  cannot ever merge here: it forks `merge', and this disk
              has no such binary.  A real two-revision attempt gets as
              far as `RCS file: note_v / retrieving revision 1.1 /
              Merging differences ... into note' and then `merge: not
              found'.  That IS more of the program working than the
              published card shows, so the card is improvable even
              though the merge can never finish.

### `merge' is one build and one small port away, from source already here

Worth someone's evening, and NOT started tonight.  Measured 2026-09-13.

`rcsmerge' is a shipped program that cannot do its job for want of one
helper.  What the helper needs is all on this disk already:

    disk/SRC/rcs/merge.sh    the merge script RCS ships, 1028 bytes
    disk/SRC/diff/diff3.c    diff3's source, in the SAME TREE the
                             shipped `diff' was built from
    ed, diff                 both in CMDS

What is missing is smaller than it looks.  The `diff' recipe builds
eleven sources from `SRC/diff' and **`diff3.c' is not one of them** --
the file is there, unbuilt, with no recipe of its own.  And `merge.sh'
is written in Microware-shell idiom: it calls `list', `del' and `test',
none of which are on this disk, where the same jobs are `cat', `rm' and
bash's own `test'.  So this is a BUILD plus a small PORT, not an install.

Nothing new is acquired by doing it -- `diff3.c' is part of the GNU diff
1.1 whose source and binary already ship -- so it completes a program
that is here rather than adding one.  If it works, `rcsmerge' stops
being a card about a missing helper and becomes a card about merging,
and `merge' itself is a useful program to have.

**It was attempted, 2026-09-13, and it stops at ONE unresolved symbol.**
Three builds, each against a fresh overlay from `make_overlay.sh':

  1. `diff3|diff|diff3.c alloca.c ../unixlib/getopt.c|||' and the same
     with `diff3.c' alone -- both FAIL, `undeclared identifier' at
     `diff3.c' line 287, `char diff_program[] = DIFF_PROGRAM;'.  That
     is a `-D' the build must supply: the program diff3 forks to do the
     two pairwise diffs.
  2. `diff3|diff|diff3.c|DIFF_PROGRAM="/dd/CMDS/diff"|||' -- **the
     define survives**, unescaped, straight through the psv field.  The
     cc line comes out as `-DDIFF_PROGRAM="/dd/CMDS/diff"' and line 287
     compiles.  Worth knowing generally: twelve recipes carry a VALUED
     define (`MEM=64k', `W_OK=2', `time_t=long') and none carries a
     quoted STRING, so this is the first evidence that one works.  The
     ESCAPED form in the extra-flags field does NOT work -- `\"' reaches
     cc literally and gives `unterminated string'.
  3. With the define right, the compile passes and the LINK fails:
     **`Symbol 'pipe' unresolved'**.  diff3 forks and pipes to run
     `diff' twice (`fork()' at line 1185, `execve (diff_program, argv,
     environ)' at 1190), and this SDK's libraries have no `pipe'.

**There IS a pipe() in the pool** -- `SRC/infoxpress/BNU/ELM_2.4/OSK/
pipe.c', thirteen lines of code: `pipe()' is `creat("/pipe")' plus
`dup()', `dup2()' is a loop over `dup()', and it needs only `<modes.h>'.
Technically it is a drop-in extra source for the recipe.

**But its licence is not the package's, and that stops this here.**  The
file's own header (Wolfgang Ocker, Ulli Dessauer, Reimer Mellin, 1988)
says it may be copied and distributed freely "for any non-commercial
purposes" and incorporated into commercial software only by written
permission.  `SOURCES.txt' records the Elm 2.4 package it sits inside
under the Elm General Public License, which is permissive; this FILE is
narrower than the package around it.  Building a new binary we SHIP
against it would carry that restriction into the collection, which is
rdoggett's call and is in `notes/FOR-RDOGGETT.md'.  The tree was left
clean: `c68' emits `.r' files beside the sources and two were removed.

## One card regressed in the gallery, and its exception argues the wrong case

`pgmedge'.  Found 2026-09-13 by reading git rather than by re-shooting.

At `1be0bed0' the card was SEVEN LINES: `pgmedge' wrote an edge greymap
and `pgmtopbm eg.pgm | pbmtoascii -2x4' drew it, so a reader saw the
gingham weave come back as the grid of its seams.  At `6b009068' -- the
pass that gave every card a `try' line and short relative names -- the
follow-up was changed to `pnmfile gg.pgm eg.pgm' and the card went to
ZERO lines.  It is the only card that commit hollowed: every other
`docs/screens/*.txt' it touched came out the same size or larger.

`tools/panel-exceptions.psv' line 124 then justified the empty card:
pgmedge "is slow enough to leave the interactive capture session
unusable before the follow-up renders".  **The history contradicts the
reason.**  The older stanza allowed the same `wait 20' and ITS follow-up
rendered fine.  What changed was the demo, not the program.

Re-shot solo 2026-09-13 it still comes back empty, with `(session
replaced -- pgmedge left it unusable)', so something about the current
form does wedge the session.

**THE OBVIOUS FIX WAS TRIED AND IT DOES NOT HOLD.  Seven runs, and
pgmedge is FLAKY rather than size-bound:**

    8x8    rendered        16x16  rendered
    24x16  WEDGED          24x24  WEDGED
    32x16  rendered, then WEDGED on the very next run of the same
           stanza with the same image and the same 45-second wait

So there is no size that can be relied on, and raising the wait does not
help -- 60 seconds wedges where 45 succeeded.  A card built on 32x16
would render about half the time and publish an empty panel the rest,
which is worse than the honest empty card it has now, because it would
look fixed.  **Do not restore the bigger picture.**  If anyone returns
to this, the question is not "what size" but why a 512-pixel edge detect
leaves the session unusable at all -- that smells like the program or
the emulator, not the card, and `notes/os9exec-bugs/' is where it would
go once somebody has a reproducer tighter than "about half the time".

What IS settled: the exception's SYMPTOM is real and its REASONING is
wrong.  It says pgmedge is too slow for the follow-up to render; the
older stanza rendered its follow-up on a LARGER image with a shorter
wait.  Slowness is not the mechanism.  The line now says what was
measured.  **Take the exception out only after a card renders twice
running** -- `audit_panels.gate()' fails on an excepted name that is not
runnable, so removing it early breaks the gate.

## A card getting SHORTER is not evidence that it broke

Measured 2026-09-13, and recorded because the measurement was nearly
reported as a finding.  Comparing every published card against its own
previous commit, 48 shrank by four lines or more.  That list is not
damage; it is mostly the release pass doing its job.

Of the 48, five are also flagged by `audit_cards' today, and all five
were read:

  `finger'  25 -> 3.  The old card showed `osknet' -- another program's
            banner and its missing-file warnings.  The trim FIXED it.
  `mailx'   14 -> 2.  The old card ran `philmail' underneath mailx, and
            published philmail's session.  The trim FIXED it.
  `blastem' 19 -> 2, `xyt' 14 -> 2, `mail' 22 -> 3.  Deliberate: each
            traded a screen of its own help for an honest attempt that
            fails for want of a modem or a RAM disk.  Arguable, not
            broken.

So: one regression in the gallery (`pgmedge', above), found by reading
the diffs rather than by size.  Two of the five biggest "losses" were
cards that had been showing the WRONG PROGRAM, which is the defect
`audit_panels' exists for -- and by size alone they look like the worst
damage on the list.

Two invocation hypotheses were also refuted the same way, before any
re-shoot: `lnk.org' ALREADY loads `os9lib' (its stop is the documented
`system()' forks a bare `shell' case), and `rcsmerge's card is a
deliberate demonstration of the missing `-r'.  Read the stanza before
believing a card has the wrong invocation.

## audit_cards was eating the first line of every card (fixed 2026-09-13)

`classify()' discounted three kinds of line as "the command that was
typed": one behind a prompt, one matching the sheet's own `run' record,
and **the first line of the capture, always**.  That third test was
measured across all 990 cards: it discounted 241 first lines, of which
TWO were echoes.  The other 239 were the programs' own opening words --
`OS-9 BACKGAMMON', `BATTLESHIPS', `Accordian Solitaire - by Eric
Lechner', `ATerm : A terminal program for OS9/68000', `Wrote cache file
./index.cache'.

It fired hardest on the cards whose stanza runs `clear' before the demo,
because then no prompt-prefixed echo survives and the program's ONLY
line is line one.  Seven cards were reported NOTHING while showing real
output: `wndex', `vis', `bootlogger', `preset', `screen', `fileserv',
`atp'.  Flagged count 66 -> 59.

**Two cautions for whoever reads the new list.**

`transfer' JOINED it, correctly -- its real first line is a second error
(`Can't load device descriptor "DGDOS0" !') which tips it to
MOSTLY-ERROR.  Looked at, and excepted by name: there is no GDOS device
here, so that message is all it can say.

`suspend' LEFT it and should not have.  Its capture is still nothing but
help, but the option lines under `Options:' (`-?  show this
explanation') score as WORK, and with the banner counted too its work
reached 4 -- one past the `work <= 3' threshold that defines THIN-HELP.
So the THIN-HELP rule is sensitive to how much help text a program
prints, which is not what it means to measure.  Worth fixing if the
queue is worked down; not worth widening the USAGE regex blind.

**How the change was justified, since a scorer is exactly the thing to
be careful with**: the replacement rule was reimplemented alongside the
original and compared card by card over all 990 -- ZERO mismatches --
before anything was edited, so the measurement of the old rule came from
something known to reproduce it.  Two earlier heuristics for "does this
first line resemble the typed command" were tried and both misfired
(they called `Twas brillig, and the slithy toves' an echo, because a
SETUP line writes that poem into the file the editors then display).
Nothing outside `audit_cards.py' calls `classify()' -- `audit_panels'
imports only the three regexes -- so the panels gate is untouched.

**The archives trio is the first FAMILY among the clearers**: `lha',
`lharc' and `lharcs' are three builds of one archiver, found together.
That is worth noticing, but it does NOT revive the profile -- see above,
both profiles failed and `casefix' (a stdin sentence-case filter) clears
PD_ALF while eight other clearers have no terminal handling at all.

`files' is worth a note: it fired TWICE and every card still came out
equivalent -- 36 of 36.  That is the guard doing its job rather than a
sheet with a problem, and it is what a clean sweep of an affected sheet
looks like now the fix is in.

`creadoc' re-read at ink 51 in the compilers sweep -- exactly what it was
published at hours earlier, on a rebuilt image.  The column fix is
stable and reproducible.

What the sweeps actually YIELDED, which is the honest measure of whether
to keep going: graphics recovered `pdraw' (96 -> 396); comms exposed
`listalias' and `newmail', both forking a helper by bare name and both
fixed; textfilters exposed `column', whose listing was missing eleven
games.  Four real card fixes out of five sheets.  Everything else that a
sweep flagged -- and it flagged a lot -- was run variance, a scroll,
error text, or a stanza that varies by design.

**A LOWER of exactly 0 means the session DIED, not that output shrank.**
`etags' came back 0 in devtools and re-shoots solo to 52 against a
published 50, with the same 565-byte TAGS file.  The log says why:
`(session replaced -- etags left it unusable)'.  Look for that line
before investigating a zero.

**AND I THEN OVER-GENERALISED THAT NEGATIVE.  An earlier version of this
heading said the fault was CONFINED to graphics.sheet; it is not.**
Sweeping `system.sheet' (100 stanzas) the guard fired TWICE, on
`hinterhalt' and `sddemo', and recovered `config' from 503 to 726 ink --
a second victim of the same shape as `pdraw', which nothing had flagged.
So clearers are spread thinly across sheets and three sheets returning
zero says nothing about a fourth.  Known at the time: graphics 9
firings, system 2, the three netpbm sheets 0, 772 stanzas unswept.
(The sweep has since FINISHED -- 929 of 929, 36 clearers.  See the
tally above; this paragraph is kept for the reasoning, not the count.)

**Re-shooting was the only way to establish this**, and that is the
point worth keeping.  A static scan cannot find these victims: `pdraw'
tripped no damage signature and was not thin enough to flag -- 96 ink, a
command and a plausible prompt line, looking like a program that simply
prints little -- and it turned out to be a casualty that recovered to
396 once the guard was in.  An absolute ink threshold is no use either;
`netpbm-in' and `netpbm' have median inks of 101 and 104, so "ink < 120"
flags half of each sheet for being typical of itself, and eight of the
names it flags are the no-reader converters that audit_cards already
excepts by name for being CORRECT.

The captures from that sweep were restored rather than promoted: all 70
were equivalent, so publishing them would have churned 70 cards for
nothing, the same call made on pgmcrater's re-dither.

## Two exception lists overlap by design, and merging them is a trap

Measured 2026-09-13 while working the card-flag list down.  `audit_cards'
has a `fine' dict of cards whose failure IS the point of the card;
`audit_panels' has `tools/panel-exceptions.psv'.  **14 of the 19 `fine'
entries are also panel-exceptions rows** -- perr, disktest, edir and the
whole no-reader set -- and that was true before tonight.  Hand-listing a
name in both is the EXISTING convention, not a slip.

I nearly "fixed" it twice in one sitting: first by reverting my own
additions as redundant, then by making audit_cards read
panel-exceptions.psv as a single source.  Both are wrong:

  - The two tools ask different questions and key on different things.
    audit_panels scores 970 RUNNABLE PROGRAMS by program name;
    audit_cards scores 990 CARDS by STANZA name.  The five fine-only
    entries -- cjpeg.070, csl-mismatch, perr-alps, perr-print, silent --
    are stanza names audit_panels never scores at all, so a merged
    source would silently drop them.
  - panel-exceptions.psv already prints its own reason inline in
    audit_panels output; the `fine' reasons are written for the card
    reader.  Same name, different audience.

The real cost of the overlap is DRIFT: the same judgement is recorded
twice in different words and nothing checks that they still agree.  If
that is ever worth fixing, the safe shape is a CHECK that the reasons
for a shared name have not diverged -- not one list feeding the other.

## What this session did (2026-09-13, overnight), all committed and gate-green

**`creadoc' is FIXED and shipped.**  rdoggett asked whether it failed for
using the wrong `dir'.  Answer: supplying Microware's `dir', `del' and
`shell' gets it past `can't execute "del"' and no further -- it is still
off by one, against Microware's OWN dir.  Measured 666 file entries in
four directories, sector addresses 2-5 hex digits and sizes 2-7: both
fields are right-aligned, so the name is at column 54 in every one and
`fnpos = 53' is right on no system.  One character.  Rebuilt through
rtf -> r68 -> l68; the UNPATCHED rebuild differs from the shipped binary
in 4 bytes (an M$Excpt vestige outside the parity range, plus the CRC),
which is what makes the provenance clean, and the fixed one differs in 5.
RTF stores the constant as text, so "one constant" is literally one
character.  `395751bc'.

**The garbled captures are ROOT-CAUSED and fixed** -- PD_ALF; see the
section above.  Five earlier explanations are refuted there.  Fifteen
cards repaired or newly published: ten in the cluster (`b93df9fc'), six
of which the INK FLOOR had been silently dropping so they had no card at
all; X11R6shl and vmod_trap now show the LIBRARY instead of a shell
refusing to run it (`aac8cc78', `75f50af4'); and `pdraw', which nothing
had flagged, recovered 96 -> 396 (`be65bb61').

**Two gates gained something.**  screenshots.py warns when OS9SDK is
unset and a stanza loads from /h1 (`77eecb39') -- that silence published
a blank card.  And alf_off() replaces a poisoned session (`090b27a5').

**Three of my own claims were WRONG and are corrected in place**, all
caught by the sibling sessions reading manuals: `../..' IS valid OS-9
(the gate stays, on portability, not validity) and SS_Opt's scope is not
established -- both in `398e3c35'.  A measurement trap that cost time
twice is written down, and so is why the two exception lists overlap.

**The archives were swept** -- `notes/PLAN-acquisitions.md' has the state
table.  IA is back up; alt.sources is exhausted for OSK; comp.os.os9
1987-2002 is NOT on IA and that is the live question.  One new source:
The OSKer, six issues 1990-91, public-domain submissions clause, no code.

**All of it is swept now -- 929 of 929.**  What this paragraph used to
say, when ~770 stanzas were outstanding, still holds as method:
prediction does not work here -- I predicted netpbm would be affected
and it was not (0 firings in 71) -- so the only way to find another
`pdraw' was to re-shoot and compare through trim(), and that is what
was done to all of it.

## Do not build a "cited commit hashes must resolve" gate

Tempting after 2026-09-13, when I wrote a hash into this file that does
not exist (`58e3c35', a fat-fingered duplicate of 398e3c35) and only
caught it by checking by hand.  The house habit is to turn that into a
mechanical check.  **It cannot be one**, and the reason is worth keeping
so nobody spends an evening on it:

  - `notes/' LEGITIMATELY CITES THE SIBLING REPO.  os9exec's `985e0d8'
    appears five times, in this file and in check_disk.py's dots-gate
    docstring, and is correct every time.  It does not resolve here and
    never will.
  - Not every 7-8 hex token is a hash at all.  A bare scan turns up
    `000465d2' and `000516c8' in SECOND-PASS.md, which are OS-9
    ADDRESSES, and `3f5b0760'/`ff75a069' in MICROWARE-PERMISSION.md,
    which are not commits either.
  - There is no mechanical way to tell ours from os9exec's from a hex
    address by SHAPE.  A gate would fail on correct text, which the dots
    gate's own docstring warns is the way to make a gate disbelieved.

And a measuring lesson underneath it.  My first scan reported "16 of 16
cited hashes resolve, 0 foreign" and I nearly recorded the gate as SAFE
on that.  The pattern only matched BACKTICK-QUOTED hashes; every foreign
one is written bare.  The needle measured its own shape, not the thing --
the third time in one night, after `digit-in-word' and after searching
subjects.tsv's AUTHOR column for OS-9 mentions.  When a scan returns a
clean result, check what it could not have seen.

## An ink GAIN can mean the screen SCROLLED, not that the card got better

2026-09-13, caught one card short of publishing a regression.  Comparing
a re-shoot against the published card, I flagged anything above 1.1x as
IMPROVED and treated that as good news.  `config' came back 503 -> 726
and was on its way into the gallery.

It had scrolled.  The PUBLISHED card starts at `$ config' and shows the
program from its first line -- char/short/int/long sizes, alignments,
pointer widths, then the float properties.  The new capture had lost the
command AND the whole opening, starting mid-way at `/* Maximum number =
3.40282e+38 */'.  It scored HIGHER because the grid kept the denser
`double' section that followed.  moments() warns about exactly this:
"a program that scrolls has pushed its heading off".

**So neither direction is safe unread.**  Low ink is not automatically
damage (see the raw-vs-published trap above) and high ink is not
automatically recovery.

**The cheap mechanical tell**: a sound capture's FIRST LINE is the
stanza's own `try' command; a scrolled one starts mid-output.  Checking
all fourteen cards promoted that night, thirteen started at their command
and one did not.

    first = open('docs/screens/NAME.txt').read().split('\n')[0]
    ok = re.sub(r'^\$\s?', '', first).strip() == stanza_try.strip()

**But a scroll is only a DEFECT when a better alternative exists.**
`config' scrolled where a non-scrolled published card already existed --
that would have been a strict regression.  `mgif' scrolled too, and was
still published, because what it replaced was garbled overlap at ink 55
and the scrolled capture carries 358 ink of the program's real output.
47% of published cards start mid-output; for anything printing more than
a screenful that is simply what a 24-line window gives you.  The fix
where it matters is the sheet's own `size' directive -- a taller window
keeps the command on screen under a full-height picture.

## gen_screens regenerates screens.js from EVERY capture -- mind what you commit

2026-09-13, and it published an inconsistent gallery for one commit.
Promoting a single card, I added explicit paths -- the sheet, that card's
`.txt', screens.js and screens.stanzas -- which looks careful and is not.
`gen_screens' had rewritten SEVENTEEN other cards from captures that had
drifted, and screens.js is generated from ALL of them.  So the committed
screens.js held `Sep 13 04:40' for `trunc' where the committed
`trunc.txt' still held `Sep 8 22:41', and carried a `$ ' prefix for
`clear' the card file did not.  **screens.js is what the page reads**, so
the half that was wrong was the authoritative half.

The 17 were re-shoot churn -- file timestamps, a prompt prefix,
pgmcrater's non-reproducible dither -- the class reverted for the 70
netpbm cards.

**Order matters in the repair.**  Restore the CAPTURES first, then
regenerate.  Reverting the card files alone leaves the drifted captures
in notes/playtests, and the next gen_screens run reproduces the churn.

    git status --short docs/     # BEFORE committing, and READ it
    # if more than the card you meant has moved, restore captures first

I printed exactly that check, labelled "mgif should be the only one",
and committed without reading it.

**Not the same thing, and do NOT try to fix it:** screens.js and a card
file legitimately differ for SEVEN cards that predate tonight, and the
reason is not the same for all of them.

SIX are ENCODING -- btop, c7decode, cuts, names, preset and ptob carry
`+' in the card and CP437 box characters in screens.js, from
ansiscreen's CP437_BOX mapping.  Measured: btop has 46 non-ASCII
characters in the js and 0 in the card, names 77 and 0, preset 12 and 0.
Same screen, two renderings, by design.

THE SEVENTH IS NOT.  `macstream' has 0 non-ASCII on both sides, so that
explanation does not cover it -- an earlier version of this paragraph
listed it with the other six and was wrong.  Its difference is
whitespace: the card file carries one more trailing character on the
`0050' dump line and one more blank line at the end, 20 lines against
19.  The current capture matches screens.js exactly, so the CARD FILE is
the stale half, by a trailing space.  Nothing a reader sees; not worth
churning a card for.

**And the lesson under both of tonight's gallery slips is not "print the
check".**  I printed `git status --short docs/' labelled "mgif should be
the only one", and committed with seventeen others showing.  I printed a
per-card verdict that said `other' for macstream, and committed a note
calling it an encoding difference.  The evidence was on screen both
times.  A check you print and do not READ is a check that did not run.

## comms.sheet swept 2026-09-13: four more clearers, and a THIRD way ink lies

**Four more PD_ALF clearers: `filter', `connect', `sterm', `txmod'.**
So three sheets are now known affected -- graphics 9 firings, comms 4,
system 2, the three netpbm sheets 0 -- and the refined profile holds:
terminal-takers and raw-byte writers (connect and sterm drive terminals,
txmod pushes a module down a serial line, filter is a pipeline filter),
NOT netpbm as a family.  674 stanzas were unswept at that point.  (The
profile did not survive the rest of the sweep -- `casefix', a stdin
filter with no terminal handling, clears PD_ALF too.  See the tally.)

**Swept MEASURE-ONLY and every capture restored afterwards**, so the
gallery could not move whatever turned up: 76 equivalent, tree 0
modified.  That shape is worth reusing -- it answers "are there victims
here?" with no promotion risk at all, and promotion can then be a
separate, deliberate step.

**A THIRD way an ink gain misleads: the gain can be ERROR TEXT** -- but
only ONE of the two cards was that, and an earlier version of this
paragraph got both wrong.  Both passed the scroll test, each starting at
its own command, and both carried a failed bare-name fork of a helper:

    $ listalias        $ newmail -d tester
    sort: nowhere found      uuname: nowhere found

`newmail' WAS purely that -- the published card plus one error line, no
content gained.  `listalias' was NOT: under its error line sat SIX MORE
ALIASES than the published card showed.  The ink was telling me something
real and I read it as noise.

**Both are now FIXED, and by the documented cure.**  Each forks a helper
by bare name, which resolves against chx and never PATH, so the helper
has to be resident: `load /dd/CMDS/sort' for listalias, `load
/dd/CMDS/UUCP/uuname' for newmail -- the printmail/readmsg case.
listalias went 83 -> 248 and its aliases now come out SORTED, which is
the pipeline's own proof it ran (`egrep "%s" | sort' is in the binary at
offset 1616); DOC/INDEX said "the plain form needs nothing extra" and is
corrected (`13a460a8').  newmail's card is unchanged by its fix -- the
error line goes and the result equals what was already published -- but
the stanza is worth having, because the card was previously correct only
by accident of ambient state.

**Do not generalise the mechanism -- MEASURED, and the answer is that
there is nothing left to fix.**  listalias carries `uuname -l' too, at
offset 19118, and shows no uuname error once sort is loaded, so that path
is not reached in the plain form.  The same held for every other
candidate: `answer' (22070) and `frm' (23356) and `fastmail' (7316) all
carry the string on paths their stanzas never reach, and `filter',
`elm' and `newalias' do not reference uuname at all.

The instrument that settled it costs nothing: **grep the published cards
for the error, not the binaries for the string.**  `sh' says `nowhere
found' and nothing else does, so one grep over docs/screens names every
card actually carrying a failed fork.  The answer was THREE: listalias
and newmail, both now fixed, and `remove' -- whose error line is
DELIBERATE.  remove's card is a before-and-after: readmsg resident and
answering, then `remove readmsg', then the same command replying
`readmsg: nowhere found', which is the proof it worked.  Excepted in
audit_cards rather than "fixed".

`frm' is unpublished and should stay so on its own merits: its capture
trims to ink 20 against the floor of 30, and the content is `$ frm' and
`tester has no mail.' -- honestly terse, not damaged, nothing to recover.

So ink alone has now misled three different ways in one night -- the
raw-vs-published artefact, a scroll, and error text -- and the scroll
test is necessary but NOT sufficient.  Read the content.

`fixtext' (170 v 169) and `uustat' (42 v 41) re-shoot to their published
values; transients.

**One thing left unexplained, as a lead not a claim.** Those forks fail
now and the PUBLISHED captures show them succeeding, and nothing in
either stanza loads a helper or moves chx.  `uuname' lives in
`CMDS/UUCP/', and a bare-name fork resolves against chx and never PATH
-- the documented printmail/readmsg case -- so failing is CORRECT for
how the stanza invokes it.  What is unexplained is how the published
capture ever showed otherwise.  One observation; do not call it a
regression without measuring it.

## Stanzas whose ink is NON-REPRODUCIBLE by design -- do not chase them

A sweep comparing a re-shoot against the published card will report these
as LOWER (or HIGHER) on roughly half of all runs, and nothing is wrong
with any of them.  CLAUDE.md already names the first; the rest were
measured 2026-09-13 while working the games sweep.

    pgmcrater   `pgmtopbm' without -threshold: the dither differs every
                run.  Same ink, different picture -- 16 of 23 lines
                changed between two runs and both were correct.
    fish        a card game that DEALS A DIFFERENT HAND each run.  The
                published card runs to 17 lines because three guesses
                landed before "GO FISH!"; a re-shoot went to GO FISH on
                the first guess and came out 11 lines, ink 232 -> 153.
                Nothing seeds the deck; the stanza sends `n' then `3'.
    zot         frames=True.  filmstrip() SAMPLES frames evenly when
                there are more frames than rows, so the ink CAN track how
                many animation frames a run produced.  It is the only
                frames=True stanza in the collection.  CAVEAT, measured
                after the fact: a solo re-shoot came back at exactly its
                published 217, so the sweep's 217 -> 173 was ordinary run
                variance like the other eight, NOT frame sampling.  The
                exclusion is still right -- a filmstrip is not comparable
                by ink in principle -- but do not cite sampling as the
                explanation for a particular number without checking.
    freeb       reports LIVE DISK STATISTICS.  Rebuilding the image
                changes them: 1081344 sectors and one fragment row
                became 1134592 sectors and seven.  Both correct.
    blackjack   THREE sources of variance at once: a persisted BANKROLL
                (the score files ship and are preserved -- CLAUDE.md),
                a clock time on the card (`This game started at
                17:13:38'), and a shuffled deck (`** Dealer Reshuffles
                **').  Measured 363 -> 409 and flagged a REAL candidate
                by a sweep, which it is not.
    hang        picks a RANDOM WORD, so the `Unused Letters' line and
                the transcript length differ while the stanza always
                sends the same `aeiort'.  Measured 118 -> 161 and
                flagged as a SCROLL, which it is not.

    cuts        FLOODS `No more memory'.  The published card carries a
                2,088,544,320-byte refusal; a re-shoot carried a
                3,993,495,104-byte one plus `100 allocation failures so
                far'.  Same encoded output either way -- it is the Coco
                Usenet Transfer Utility and `.0000.I.A...BIN."fox.txt"'
                is the program working -- but the refusal count varies,
                and it trips screenshots.py's own `starved' replacement.
    ape         a MARKOV TEXT GENERATOR (`ape -b=12k -l=5 < jargon.txt'):
                different prose every run, so 630 -> 544 means nothing.
    cookie      prints a RANDOM SAYING.  Published: "Your project will be
                late." / "A good workman is known by his tools."  A
                re-shoot: "All that glitters has a high refractive
                index." / "Annex Canada now!..."  Different sayings, not
                truncation; the ink measures how long one happened to be.
    fortune     the same.  Published: the Noelie Altito line.  A
                re-shoot: the lightbulb sequence, several stanzas long.

**A DIFFERENT class, which DOES want re-promoting when it moves:**
`column' lists a live directory (`ls CMDS/GAMES | column'), so its card
goes stale whenever a program is added -- eleven were missing from it.
Like freeb it drifts by design, but unlike freeb the newer listing is
simply more correct, so promote it rather than restoring it.

**The name-only candidate list is now EMPTY, and all three were WRONG.**
`wisecrack', `ask' and `shuffle' were listed here as likely
non-reproducible because of what they are.  Measured 2026-09-13 and none
of them is: `shuffle' re-shoots to EXACTLY its published 437 -- it is a
switch puzzle with a fixed layout, not a shuffler of anything random --
and `wisecrack' (55 v 51) and `ask' (54 v 53) sit inside the noise band.
`cookie' and `fortune' were on this list too and ARE non-reproducible,
measured above.

Two guesses right, three wrong, from the same kind of reasoning.  Names
suggest which stanzas to CHECK; they do not settle what a stanza does.

**HOW LITTLE ONE READING IS WORTH.**  In the texttools sweep `cookie'
read 66 -> 363 and `fortune' 127 -> 58.  A solo re-shoot minutes later
gave 124 and 275.  FOUR values for two cards across two runs, and the
sweep put `cookie' in the REAL-candidates bucket on the strength of one
of them.  The scroll and error-text tests cannot see randomness, so a
random-output stanza will keep clearing them.

**Two others are measured differently and cannot be compared by ink at
all**: `zot' (frames) above, and the burst stanzas `back', `backgammon'
and `teachgammon', which are captured through a separate unthrottled
path.  Only games.sheet contains any of them, so the graphics, system,
comms and netpbm sweep verdicts were never affected.

## zsh does NOT word-split an unquoted variable, and the job still says DONE

This cost time twice on 2026-09-13, in two different scripts, and both
times the job printed a completion line and a clean tree.

    N="a b c"
    for n in $N; do ... done        # bash: three iterations
                                    # ZSH:  ONE iteration, "a b c"

First it made a freshness check compare one nonexistent path --
`stat: notes/playtests/cjpeg.070 wrjpgcom ... rsconvert.shot.txt' -- and
report an md5 of nothing as a "fingerprint".  Then it made a five-stanza
re-shoot pass `"dos.sheet msdir"' to parse() as a single filename, so
every stanza died with FileNotFoundError while the job still printed
`DECISIVE RECHECK DONE' and `tree: 0 modified'.

**Use parameter expansion instead**, which does not depend on splitting:

    for pair in dos.sheet:msdir editors.sheet:sed; do
        SH="${pair%%:*}"; N="${pair##*:}"
    done

And the general form of the lesson, which is the one worth keeping: **a
job that reports DONE has not necessarily done anything.**  Four times
tonight a background job completed with exit 0 having accomplished
nothing -- twice from this, once from an image lock it never acquired,
once from a tool with no shebang.  Check for the OUTPUT you wanted, not
for the absence of an error.
