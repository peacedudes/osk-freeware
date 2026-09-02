# For rdoggett

Terse on purpose. Everything before 2026-08-27 is in git history.

Branch `release-pass-2026-08-21`. Every `check_disk.py` check green -- there
are twenty now, and nineteen of them are proved able to FAIL by
`tools/check_the_checks.py`.

---

## WHAT NEEDS YOU, in order

**1. `gnuchess` — the one real decision.** Details below; measured, and my
recommendation is there.

**2. ~~`disk/SYS/loglist`~~ — SETTLED 2026-09-02: `loglist` IS GONE, program
and file both, at your word. You went looking for it because of that note,
read its catalogue entry, and the entry was the problem: it opened `A LOGIN
LOGGER, not just a listing' -- shouting a correction at a mistake only a
previous session had made, in the middle of a page a stranger reads -- and
its card ran straight on into `every -?', so the sample output under
`loglist' was another program's help. Dropped rather than patched.

**3. Two gaps in the `os9-dev` SKILL, noted not fixed.** The skill repo is
`~/Developer/os9/os9-dev-skill` and its tree is clean; say the word and I
will write these in. Both are in
`references/common/using-os9exec-repl.md`, section "The cio trap handler
divides archived binaries".

  a. **The cio SELECTOR MISMATCH is not in the skill at all.** The section
     says the failure is `**** Can't install trap handler ****' and that you
     classify a binary by searching for the module name `cio\0'. That covers
     the program which cannot FIND cio. It says nothing about the program
     that finds it and is silently broken anyway: the era's `LIB/cio.l' puts
     `_flshbuf'/`_filbuf' at trap-13 selectors $41/$42, where every `cio'
     MODULE has raw memory allocate/free, so the inline putc/getc macro
     hands the allocator a `FILE *' as a byte count. Nothing is written,
     nothing is read, a block leaks per character. On current os9exec, which
     counts refused allocations rather than printing them, the program simply
     never returns. The answer is `-qm', not `-qixm'. We have the whole
     mechanism measured in `DOC/README-CIO' and
     `notes/os9exec-bugs/CIO-SELECTOR-MISMATCH.md`.

  b. **"a usage message is a pass" is unsafe, and the same section says it.**
     Under "Batch-testing binaries": *"This tests 'loads and starts' (a usage
     message is a pass)"*. For this whole class it is exactly the wrong
     signal -- a usage line goes through `printf' inside the module and never
     crosses the broken selector, so the program prints its help perfectly
     and then does no work at all. Measured here on 2026-08-31: `unifdef',
     `ape' and `hexed' each printed their complete option list and then
     produced nothing for a real file. It is still a fine *loads-and-starts*
     test; it just needs a sentence saying that is all it is.

  c. **A RELATIVE `OS9Hx` PATH BREAKS ORDINARY FILE OPENS while module
     loading still works** -- measured here 2026-09-01, and it cost an
     hour. The skill's os9exec page warns about a leading `./' on
     `OS9DISK' in exactly those words and then says "Bare or absolute
     paths both work". For an `OS9Hx` device a BARE relative name is not
     safe either: `OS9H0=osk-freeware.dd` mounts the device, `wn' loads
     and runs from it, and the file it wants to serve cannot be opened --
     every request came back 404 and nothing said why. Absolute fixed it.
     Same symptom shape as the `./' trap, so it probably belongs in the
     same paragraph.

  d. **`F$SysDbg` HAS NOW BEEN EXERCISED LIVE**, which the skill says has
     never happened ("Neither has been exercised live for that reason").
     OS-9's own `break' utility calls it, and under os9exec it lands in the
     EMULATOR's meta-debugger with the prompt
     `# Pid=3: dbgmsk=$0001,$0000,$0000 stop=$0000 trigger='' (type
     ?<Enter> for hlp)` -- and hangs the script, exactly as predicted.
     Asserted in `tools/datatests/last2.cases`, last case in the family
     because nothing after it runs.

What the skill got RIGHT and saved time on, for the record: `break' is
documented as "halt into the ROM debugger (superuser, console)", and
`setime' as taking six separate fields `y m d h m s' rather than the packed
string `DOC/INDEX' describes. Both were about to be driven wrong.

**4. `tools/screenshots.py` now mounts `/h0` too, and I have not re-shot the
gallery on it.** The four harnesses disagreed about whether the collection
is also `/h0`; `notes/DECISION-placement.md` says it should be, and
`drive.py` always did it. I made `datatest.py` and `screenshots.py` match.
The DATATESTS are all green on that (629 cases), but the 485 gallery cards
were captured under the old arrangement and only five have been re-shot.
Nothing looks wrong — `/h0` only ADDS a device — but a full re-shoot is a
couple of hours and is the honest way to be sure. Say if you want it run.

**4a. UPDATE 2026-09-02: 115 of the 409 cards have now been shot under the
`/h0` arrangement**, not the five that stood when item 4 was written -- they
went through as their programs were corrected. Nothing in them looked
different for `/h0`'s sake. The remaining 294 are still on the old captures
and the question below is unchanged.

**5. I stopped the full gallery re-shoot part-way, deliberately.** It was
running at about 0.6 minutes a card -- five hours for 485 -- and it held the
image lock the whole time, which blocked everything else. I shot the twelve
cards I had changed instead, plus the seventy the full run got through before
I stopped it, and nothing in those seventy looked different under `/h0`. The
629 datatest cases all pass with `/h0` mounted, which is the stronger
evidence anyway. If you want the full sweep run for completeness it is
`tools/screenshots.py --all` and about five hours.

  One thing to know if you do: **`--only` skips `setup-image`**, so a card
  that reads its shared test images comes out blank. Six cards were made
  self-contained for that reason; twenty still depend on it, which
  `check_disk`'s new `cards do not depend on each other` check explicitly
  sanctions.

**5a. YOUR os9exec CHANGE REACHED US, and it was a good one.** The binary at
`~/Developer/os9/os9exec` was rebuilt at 04:20 on 2026-09-02 and now reports
**V4.10** where it reported V4.0 (`Core: report V4.10, the work since the
v4.0.0 tag`). `sysmon` compares that against what it was built for, and it
had been refusing outright -- `OS9/68k V4.0 is too old for SYSMON V6.1'. It
now STARTS: it asks about `/dd/sys/nodedef`, times out, draws its whole
Process Monitor, and takes a bus error at `F$GPrDsc`, the same gap
`devprc -a` and `top` meet at `F$GPrDBT`. Its card, its `DOC/INDEX` entry and
its datatest case all recorded the refusal and are corrected. Nothing needed
from you; you may just like knowing which program noticed.

  One thing I would not have found otherwise: `tools/ansiscreen.py` did not
  know the **DEC line-drawing character set**, so sysmon's table came out as
  forty lines of `(0x       (0x`. It does now, mapped to `+ - |` rather than
  the Unicode box characters, because nothing here may carry a byte over
  0x7f. sysmon is the only program on the disk that had ever got far enough
  to use it.

**6. Nothing else is waiting on you.** For the record, and needing nothing
from you: Metafont works. `SYS/TEX/MFBASES` held only its Makefile, so
`virmf` had no base and the eight bitmap-font tools had nothing to read --
which is why their gallery card was eight usage lines and why every DVI
driver warns it cannot open a font. `inimf` builds both bases the disk's own
`install.script` asks for; they now ship, and `cmr10` renders from the 117
Computer Modern sources that were here all along. 15 new cases assert it.

---

## What happened on 2026-08-31, evening, in one page

You asked for the programs to be RUN and checked, and for that to keep going
rather than stopping every two tasks. Here is where it got to.

**The tooling came first, because the bottleneck was never judgement.**
`tools/drive.py` runs forty programs with real arguments in ONE emulator
session and writes a transcript; `tools/worklist.py` says which program still
has nothing; `tools/audit_cards.py` finds the cards that show a usage
line or an error. The old card auditor flagged 2 of 407 -- its rule required
every line to be an error, and the typed command never is.

| | morning | now |
|---|---|---|
| Programs with neither a test nor a card | 421 | **97** |
| `datatest` cases | 187 | **423** |
| Cards flagged as help-only or error-only | undetectable | 31 found, 11 fixed |

**The single biggest find: `SYS/login` never set `SHELL`.** Programs that
shell out reach the C library's `system()`, which forks `$SHELL` with the
whole command line as one argument -- and of the five shells here only `ksh`
parses that. One line, and `tex`, `latex`, `eo` and `maketexpk` went from
doing nothing at all to working. `DOC/STATUS` had blamed a fork resolved
against the execution directory; that was wrong and is corrected.

**The eleven cio casualties are fixed.** The os9exec session pointed out that
every one had source and a recipe here already; rebuilt `-qm` they all work,
and they are installed, unstarred and asserted. `cvtbase` converts, `cdiff`
diffs, `xrf` prints a full cross-reference. `relink_cio.sh` now refuses to
relink a program that would come out broken, which is what produced
`kermit_cio`.

**Twelve index entries described a different program.** The one to see is
`checkfile`: the entry said "check a C source file for structural mistakes"
and it is a CHEQUE-BOOK program -- Add Records, Print Balance, Account,
Amount. `paranoia` was filed as a floating-point benchmark and is a text
adventure. Every one was found by running the program.

**And a card that lied.** `dhry-all` was captioned "ALL TWELVE run here" and
its capture showed one line: the other eleven Dhrystone builds were sitting at
a prompt waiting for a run count. It shows twelve now.

**Nothing here is waiting on a decision from you.** The loop has 97 programs
left in it and `notes/PLAN.md` says how to run it.

## ONE THING NEEDS YOU: `gnuchess`, and the measurement changed it

Everything else from the duplicate-names decision is done (2026-08-31): the
five in CMDS/REBUILT renamed file and module together, 25 more alternates
given module names that match their files, and the byte-identical second
`makeinfo` deleted. Colliding module names are down from 32 to 11, and the
eleven left are csl/csl020, math/math881, MM1/msdrv (all three deliberate --
a program links those BY NAME), the gcc passes (forked by filename, so
harmless, documented), and gnuchess.

You said "drop or rename the CMDS copy". Before doing either I ran all four,
on a pseudo-terminal, TERM=vt100, `. /dd/SYS/termcap.entry' sourced:

    CMDS/gnuchess         nothing in 20 seconds
    CMDS/gnuchessn        nothing in 20 seconds
    CMDS/gnuchessr        prompts, takes a move, answers with its own
    CMDS/GAMES/gnuchess   draws the board and plays

DOC/DEPENDS suggests why: the CMDS build opens
`/h0/usr/src/chess/gnuchess.book' by absolute path and that file is not on
this disk; the GAMES build opens its book by bare name.

So the CMDS copy may not be a duplicate worth renaming -- it may be a copy
that does not run. **Drop it, or keep it renamed as a preserved binary?** I
have not touched it, because every name I could think of was weak:
`gnuchesst' would say "termcap" and gnuchessn is termcap too; `gnuchessx'
would say "X windows" and all three carry that option. If you want it kept I
would take `gnuchess_h0', since wanting its data at /h0 is the one thing
that actually distinguishes it. The measurement is recorded in DOC/INDEX
either way.

## THE os9exec RELEASE IS NOT BLOCKED BY THIS -- root cause found overnight

I spent much of the night building a case that `F$SRqMem` was an os9exec
defect reaching shipped binaries. **The os9exec session found the actual root
cause and it is not os9exec.** Recorded in
`notes/os9exec-bugs/CIO-SELECTOR-MISMATCH.md`.

The archives were linked against a `cio.l` whose stub table has `_flshbuf` at
trap-13 selector `$41`. Every `cio` MODULE we have -- oskBoot's, ours, both
SDK builds -- has a memory routine there instead. So `putc` lands on the raw
allocator and hands it the `FILE *` as a byte count, and every character leaks
a chunk until the arena is gone. I was right that `d0` held an address; I was
wrong that os9exec put it there. The program did.

**What I got wrong and have withdrawn:** I wrote that the `CMDS/sed` swap had
retired a working binary to work around an emulator fault. It had not -- with
the `cio` module we ship, that build genuinely cannot run. The swap stands;
only the reason recorded for it needed fixing.

**One genuine os9exec item, and it is small.** `memstuff.c:782` prints
`No more memory !!!` to the console on every failed allocation, where real
OS-9 returns `E$NORAM` silently. That is the whole reason an ABI fault inside
a program reads as an emulator failure -- the emulator's voice arrives on the
program's stdout. The os9exec session is raising it with you separately. It
cost this collection a program's reputation and me a night, which is probably
the strongest argument for changing it.

**What it means for the disk: ELEVEN programs, and they are named.** 353 modules
link `cio`; 41 carry the call; all 41 have been driven. Nine are broken, in two
different ways:

    LOUD    cvtbase  logisim  unstr
            hundreds of `No more memory !!!', no work done

    SILENT  cdiff  pagekwic  pagefraz  nroff  etags  cookhash  yacc  xrf
            opens your file, reads NOT ONE BYTE, reports on it anyway

`loan` probably belongs there too. `dam`, `undel`, `snap`, `setfont` and `vis`
are UNTESTED rather than clean -- each only ever printed a usage line at me,
which proves nothing about the program. The silent ones are the
dangerous ones -- `cdiff` says "MAXLINECOUNT exceeded" on a three-line file,
`nroff` and `etags` print nothing -- and the same fault hands the C library's
allocator the FILE structure itself to free, so the heap is corrupted too. A program fails this way only if it runs a `putc`/`getc`
MACRO on a `FILE`; `printf`, `fwrite` and `read`/`write` are all fine.

Two things I got wrong on the way, both now corrected in place, because they
are the shape of mistake this collection keeps making:

- **I published 2, then 3, and it is 9.** Every count was too low because I
  was looking for the wrong thing. `unstr` only storms on the 192 KB index it
  is really for, not on a test file. And the whole SILENT half -- six more
  programs -- makes no noise at all, so counting floods could never have found
  it. The rule is now "count opens and reads", not "watch for the flood":
  a program that opens a file, reads nothing, and reports on it anyway is a
  victim. One trace answers both halves.
- **I nearly published 5.** A sweep flagged `etags` and `sedt` too. They make
  perfectly ordinary requests -- 4 KB, 6 KB -- and simply run out of room.
  Their `No more memory` lines are REAL allocation failures. They are
  indistinguishable from the defect from outside only because os9exec
  announces every failed allocation on the console; the message carries no
  information at all. That is the argument for changing `memstuff.c:782`.

## ONE THING I SHIPPED THAT YOU MIGHT NOT WANT

**An empty `disk/SYS/loglist`, added 2026-08-31.** `CMDS/loglist` is a login
logger -- `-i` records a login, `-o` a logout, `-l` prints the table -- and it
refuses to do anything at all without that file: *"Sorry, there is no
/dd/sys/loglist"*. One empty file makes it work; the precedent is
`SYS/birthdays`, which ships as a template for `cal`. Delete it if you would
rather the disk shipped no writable log, and I will put the requirement in
`DOC/DEPENDS` prose instead.

Two faults of `loglist`'s own, both measured and **neither the emulator's**:
every `-l` line after the first loses its leading character (`OGIN +` for
`LOGIN +`) while the bytes it WROTE are correct, so the fault is in its
display loop; and the year prints as `126`, years-since-1900 unwrapped.

## Answered earlier (kept for the record)

**1. ~~Should a program called `shell` ship?~~ DECIDED 2026-08-30: NO.**
rdoggett: *"we can't call sh or ksh or bash shell. It will be too confusing.
But we can assume that people who will want to use programs that require it
will already have it, and in their path."* Done -- `rayshade`, `dm`, `for`,
`qp` and `screen` each say REQUIRES MICROWARE'S `shell` in `DOC/INDEX`, and
`DOC/STATUS` has the group. Original question: Five programs fail for want of
one, and I measured exactly what a plain `copy sh shell` buys: `dm` (Disk
Master 1.4) runs completely, `rayshade` renders, the Fortran driver `for`
gets one step further, `qp` and `screen` are unaffected. It is a new program
under a name OS-9 users associate with Microware's shell, so it is your call.
Full table further down under "measured".

**2. ~~Which `vi` should be called `vi`?~~ DECIDED 2026-08-30: it keeps
the name.** rdoggett uses it daily and it works for him; it is also the
genuine Berkeley ex source, which is why it has the name. I could not
reproduce his working case -- 24 lines and 36, TERMCAP both ways, ^L and ^R
all gave the same two lines under the harness -- so the entry and the card
now say the harness result is a fact about the harness until somebody
explains it. I am not renaming a program that works for the person using it
to satisfy a test rig. Original question: The EFFO one -- the genuine Berkeley
ex/vi source, which is why it has the name -- paints two lines of a file and
stops. `elvis`, `vi_nocio` and `REBUILT/VI` (PVIC) all work properly. I have
documented it everywhere it bites and swapped nothing, because which name
gets which program is an editorial decision, not a defect.

**3. ~~Should `orbit`'s three data files ship at the root?~~ DECIDED
2026-08-30: NO.** rdoggett: *"Don't put raw data files at root. It's just
part of the instructions that the program requires a chd before it can
run."* Done -- `chd /dd/DOC/orbit` is the recipe in `DOC/INDEX`, `howto.psv`
and `DOC/STATUS`, with the bash workaround marked as a workaround. No helper
scripts: *"we will end up with a dozen or more little scripts."* Original
question: `orbit` -- the
N3EMO satellite tracker, which was recorded as broken and is not -- opens
`kepler.dat`, `mode.dat` and a `<site>.sit` by BARE NAME in the data
directory. All three are on the disk, in `DOC/orbit`, and it finds none of
them. Copying them to `/dd` makes it work first try, and the card and the
play-test both do that in their setup. Shipping them there permanently would
put four more files in the root beside `readme` and `startup`; leaving them
where they are means the program looks broken to anyone who just types
`orbit`. I have documented the copy in `DOC/INDEX` and `tools/howto.psv` and
shipped nothing new, because root clutter is an editorial call.

**4. Duplicate names -- MY RECOMMENDATION, waiting on your yes.** You are
right that OS-9 is not geared for it, and I measured how badly:
`/dd/CMDS/REBUILT/VI` fills the screen, but after `load /dd/CMDS/vi` that
SAME PATH gives the other program's two-line behaviour. The resident module
wins and nothing warns you. Ten names exist twice; eight share a module name
too. `DOC/STATUS` has the table.

What I recommend, in order:

1. **Rename OURS, never the archive's.** The five in `CMDS/REBUILT` that
   collide -- `arc`, `compress`, `kermit`, `screen`, `VI` -- are builds we
   made. The archive binary has the historical claim to the plain name.
   This is also the convention REBUILT already half-follows: `compress_4.0`,
   `diff_1.1`, `sed_1.06`, `zoo_2.1`, `gtar` and `lharcs` all sit in that
   same directory under distinguishing names. Only these five broke it.
2. **Rename the MODULE with the file** -- `MODNAME=` in the recipe. A rename
   that leaves both modules called `screen` is worse than doing nothing,
   because the filenames would then promise a distinction that is not there.
3. **`makeinfo` is not a rename job**: `CMDS/makeinfo` and
   `CMDS/GCC139/makeinfo` are BYTE-IDENTICAL. Delete the GCC139 copy.
4. **Leave `gcc` and `gpp` alone** (GCC139 vs GCC2). Both are archive
   material, they live in directories you choose between, and their own
   README refers to them by the plain name. Document that you must not have
   both loaded -- renaming here costs more than it buys.
5. **`gnuchess`** (CMDS vs GAMES) shares a module name and is a real hazard;
   a game belongs in GAMES, so I would drop or rename the CMDS copy.
   **`wish`** does NOT collide as a module (`wish` vs `B_wish`) -- filename
   only, lowest priority.

For the five in (1) I would use the suffix that already means "the trap-free
build we made", following `vi_nocio`. `vi_nocio` is taken by PVic, so
REBUILT/VI needs a different one -- say `vi_effo`, since that is what it is.
**Say the word and I will do it**: rename, rebuild with `MODNAME=`, and fix
every reference in INDEX, CATEGORIES, howto, the sheets and the recipes.

Everything else below is a report, not a question. Nothing in it is waiting
on you.

---

## Where you were right and I was wrong

**`hack` works — my test harness was broken, not hack.** It drove programs
through a FIFO, and a FIFO is not a terminal: programs that call `isatty()` or
reopen their own tty behave differently, and so does os9exec, which puts a
*tty* into raw mode at startup and leaves a pipe alone. Rewritten to use a
real pseudo-terminal. `hack` now plays; its inventory screen is in the gallery.

**`snake`'s startup hang is NOT something I introduced.** Archive binary:
drew 18 of 20 with keys, 17 of 20 without. It hangs about one run in eight,
emitting the keypad-init string and stopping before it draws. I earlier
blamed my own change on a six-run sample (6/6 vs 4/6) and reverted a good fix
on that basis. Twelve runs said 11/12 vs 10/12. Still open.

**`life` and terminal size: you are right and it cannot be fixed in `life`.**
os9exec implements no screen-size call at all, so a program can only learn its
size from termcap, which says 24x80. `DOC/README-RUNNING` now says in bold
that the disk needs an 80x24 terminal.

My harness no longer shares the blind spot. It can size the terminal now, and
`life` at 40x12 writes its status line straight through the middle of the
board -- `Gene@..@@@: 3`. So the warning in README-RUNNING is measured rather
than asserted, and `life`'s play-test carries the assertion that catches it.
The mechanism turned out not to be scrolling: `life` addresses line 24
absolutely and a short terminal clamps that into the picture, overwriting the
board in place. Nothing scrolls off, which is why it still looks like a board.

## Fixed and verified this session

  - **`tet`** -- three separate bugs. `tsleep(1)` sleeps NOTHING (500 calls,
    0 seconds; `tsleep(2)` really is 20ms) so the game ran at CPU speed;
    SCF echo corrupted the board; the high-score file pointed at `/usr/tmp`,
    which does not exist here. Plays properly now, ~1.5s a cell, scores kept
    in `/dd/GAMES/tet.hs`.
  - **`life`** -- died with `**** Stack Overflow ****` after one generation.
    The build driver had a hardcoded 16k. Added a `MEM=` recipe flag; `life`
    builds at 64k and now runs to "Generation: 9, cycles every 8 generations".
    That flag will fix other things.
  - **`who` and `mscheck`** -- your find. They were the only two files in
    `/dd/CMDS` shipped WITHOUT an execute bit, because `mktar.py` set it from
    the module magic number and those two are shell procedure files. Fixed at
    the source. (`who` is written in OS-9 *shell* syntax on a disk whose
    shells are bash and sh -- that is why it "partly works", and it needs a
    rewrite, not a permission.)
  - **netpbm** -- 152 of 168 build from source now, plus four libraries.
    Three genuine upstream bugs found doing it.

## 2026-08-29, later: ten corrupt files, and a number that could not fail

**Ten binaries under `disk/SRC/` were corrupt and had been all along** -- two
JPEGs, a GIF, a PPM, a `.zoo`, three compress archives and GNU Chess's data
and hash tables. Something had run an `iconv //TRANSLIT` over them: every
byte over `0x7f` replaced by `?`, a `0xB0` turned into the three letters
`deg`, every LF turned into CR. `testimg.jpg` began `???a`. **No program ever
misbehaved**, because the copies programs actually read -- `GNUCHESS4.0/MISC`
in the live tree -- were untouched and are byte-identical to the archive.
All ten restored from the archives `DOC/ORIGINS` names, still in the pool.
`check_disk.py` has a twelfth check now, and its first run reported nine
files, all nine of which were the check being wrong.

**The JPEG tools and netpbm both work; they disagree about line endings.**
`cjpeg`/`djpeg` separate PNM header fields with LF, the netpbm ports here use
CR, and each blames the other's data -- "Bogus data in PPM file" one way,
"junk in file where an integer should be" the other. Three bytes, patched
with `pbyte`. The claim that no JPEG could be made on this disk is gone, and
there is a card showing a GIF turned into a commented JPEG and read back.

**Coverage was being measured by a number that cannot fail.** "918 of 918
have sample output" is satisfied by a card's `for` line CREDITING a program,
whether or not the card ever runs it. Measured: **579** were actually run by
name. Some grouping is honest -- eleven DVI drivers do behave alike -- and
some was not: `scsiutil`'s card credited `read_mail` and `add_errmsg`.
Splitting the worst offenders has it at 627 and `gen_screens.py` prints both
numbers on every run now, so it cannot quietly go back.

**A CI step I added that morning had never once passed.** `gen_screens.py
--check` needs the captures, and `notes/playtests/` is gitignored, so on a
fresh checkout it exited 1 every time. Fixed by committing the stanza
fingerprints. Worth saying plainly: I added a check and did not run it the
way CI would.

**os9exec's pin is safe to bump, and this is now the whole check, not a
sample.** HEAD (`e8a3c81`) builds clean and still has the
`mount -k -v=<name>` the build needs, and the pin is an ancestor of it.
The full data suite was run against a fresh copy of the image under BOTH
binaries, 2026-08-30:

    os9exec HEAD   172 of 175
    os9exec pin    172 of 175

Not just the same score -- the same three failures (`zip`, `todos`,
`pnmtosir`, all deliberate), and the same four cases that take the session
down and get restarted. Ninety commits, several of them touching `F$SRqMem`,
and this collection cannot tell the two apart. `etags`, our own storm case,
behaves identically too.

**Bumping the pin is still your call** -- the workflow comment asks for that
deliberately and I have not changed it.

## And at the end of 2026-08-29: the screens were partly of the wrong programs

**47 programs in the catalogue were showing another program's screen.**
`gen_screens.py` gave each program the FIRST card that claimed it, and
"first" meant alphabetical. So `rdoc` -- which has a card of its own showing
it turn C source into a structure chart -- published the `helpindex` usage
message, because `helpindex` sorts earlier and lists rdoc in its `for` line.
`VI`, `date`, `fortune`, `keep`, `modinfo` and `pnmfile` were among the 47.
A program's own card wins now.

**`make` works**, and this is the shape of most of today: the obstacle was
real and it was not the program. A command line in a makefile must begin
with a TAB, and a tab does not survive being typed at this terminal -- so
every makefile written here by echoing at the shell was a syntax error, and
`make' was written up as doing nothing. It also will not take a shell
metacharacter in a recipe: `cp a b' runs, `cat a > b' does not, because make
forks bash with the line as a PATHNAME rather than with -c. There is a
`DOC/make/demo.mk` on the disk now, with its tabs intact, and the card shows
make building a target and then saying it is up to date.

**Coverage of the "actually run" kind went 579 -> 668 of 918**, by splitting
cards whose `for` line credited programs they never typed. Forty cards still
credit three or more; some of that is honest (eleven DVI drivers do behave
alike) and some is not.

## 2026-08-30: `gcc` was never in the catalogue

**Eighteen programs on the disk have never appeared in the web guide** --
`gcc`, `gpp`, all the GCC 2 passes, `what`, `zipinfo`, `unpacklib.os9`, the
two CPU32 gzips and the MM/1 mouse descriptor. They were on the disk and
they were in `categories.psv`; the catalogue simply could not see them,
because it enumerates programs from `DOC/INDEX` and the GCC section was
prose with no names in it, `unpacklib.os9` had one space where the parser
wants two, and the rest appeared only in a name grid that carries no prose.

**No check could have failed on it.** `--check` said "every program has a
category" and that was true: a program it cannot see has no category to be
missing. It now reports what it could not gather, and found the eighteen on
its first run. I wrote that check after an edit of my own to `DOC/INDEX`
silently dropped three ADL programs out of the catalogue with everything
still green.

Catalogue is **936 programs now, 864 of them run by name on their own card**
-- 918 and 579 the day before.

**And 242 programs showed no provenance at all.** `DOC/ORIGINS` records
where each added program came from, and `gen_catalog` read it with a
regex that accepted four origin phrases -- matching 224 of the file's
512 entry lines. The 242 whose origin is `Microware OS-9 archive`, the
single largest source on the disk, had their `Came from` line silently
left blank. Widened to the phrases actually in the file, and the tool
now REPORTS entry-shaped lines it cannot parse rather than passing over
them; 23 remain and most are the file's own prose. Programs with no
origin: 716 before, 452 after, and that residue is programs ORIGINS
never listed rather than ones it failed to parse.

**And a caution about my own work:** I wrote `what` an index entry saying it
prints SCCS what-strings, purely from the name. The card disproved it within
the hour -- it lists GEPARD expansion cards. Both the entry and the card say
so now, including that I got it wrong, because this collection has a long
history of entries written from names.

## Look at this

`docs/index.html` -- the catalogue, with a captured screen on 936 of the
936 program cards. Every screen came from keystrokes fed to a running program
on the disk image; 864 of them are of the program named on the card, and the
rest share one with programs that behave alike (`gen_screens.py` prints both
numbers). This line named `docs/screens.html` and "16 programs" until
2026-08-29; that file has not existed for some time and the screens have been
part of the catalogue itself since.

## 2026-08-27, second session

**You were right about `OS9MDIR` and it was worse than one bad habit.**
Purged from all four shipped docs and the web catalogue. Chasing it turned up
that **every sweep this collection has ever run loaded no modules** -- so any
program linking a library was scored on a state that cannot happen on a real
machine. That is why the six Fortran programs sat in "silent" for weeks. Using
Microware's trap-free `load` for testing only, never into `disk/`, until yours
lands.

**There is a plan now** -- `notes/PLAN-verification.md`. Four tiers by what
would actually prove a program, an order, and an estimate: about fifteen
working sessions, not a lifetime. Your bar, "proven to do its job", is what it
is built on.

**Three broken programs found, nine repaired.** A new harness
(`tools/datatest.py`) checks the DATA a program wrote rather than whether it
printed anything. 63 cases, 60 pass.

  - repaired: nine netpbm programs that died of a 3072-byte stack
  - broken, documented, left failing: `zip` (cannot write its archive),
    `todos`/`toos9` (do literally nothing), `pnmtosir` (corrupts half the
    image)

`todos` is the one worth knowing about: it round-trips perfectly *because* it
does nothing, so any test that only checked "does it come back the same"
would have certified it.

**The 95.0% figure in DOC/STATUS is stale in both directions** and should not
be quoted as "works" -- `zip` and `todos` are both inside the 870.

## 2026-08-27, third session -- the screens

**You asked for pictures for the web pages. There are 478 now**, and
taking them found more broken programs than any sweep has. Every program's
own card in `docs/index.html` carries one. (There was a separate
`docs/screens.html` gallery when this was written; it is gone, and these two
lines said otherwise until 2026-08-29.) Nothing is mocked up -- keystrokes went into a running program on the
disk image and the terminal stream was rendered into the grid a vt100 would
have shown, so where a program failed, the failure is the picture.

**Twelve programs the sweep scored OK do not work.** `gawk` reads no input at
all (a BEGIN block runs; a rule or an END block prints nothing). `m4` mangles
its output. `oleo` aborts on an illegal instruction. `top`, `checkgame` and
`bincheckr` print one line and abort. `date` says the year is 2100. `cpu`
answers and then traps. `l`, `valspeak` and `pacman` do nothing. All in
`DOC/STATUS` and against the programs in `DOC/INDEX`.

**Two INDEX entries described the wrong program.** `rot` is not a rot-13
cipher -- it turns a file on its side, line one becoming column one. `edir`
is not a directory listing -- it lists OS-9 EVENTS.

**83 programs were missing from the web guide.** `gen_catalog` scanned eleven
of the eighteen program directories under `CMDS`, so TeX and LaTeX (33
programs), elm (14), the WN web server, the serial-line set, the network set
and ADL were on the disk, in `DOC/INDEX`, and invisible in the catalogue.
917 programs now, not 834. **And `SYS/login` had the same gap** -- four
directories on `PATH` -- so `tex` could not even find `virtex`. Both fixed.

**Seventeen programs want a RAM disk at /r0** and os9exec cannot make one:
its `mount` creates h0 through hz and nothing else. `ed` and `hexed` stop at
once. Nothing on this disk can fix it; `DOC/README-RUNNING` now says so.

**Five programs need a newer `csl` than the edition 16 we ship** -- `lua`,
`runc`, `msntp`, `basicwin`, `xengine`. Twenty-seven other csl-linked
programs are perfectly happy with ours, so this is a narrow fact, not the
version skew swallowing the disk.

**The JPEG pair cannot read their input**: `cjpeg` says "Bogus data in PPM
file" for a PPM netpbm reads happily. So no JPEG can be made here and `djpeg`
has nothing to decode.

## `load` is in, and OS9MDIR is out

**Your `load` ships.** CMDS/load, source in SRC/load, built here with `-qm`
so it needs no cio -- the contributed build was cio-linked at 4148 bytes,
ours is 17084 and depends on nothing. Verified four ways: `-?`, `-l`, a load
that works (`load /dd/CMDS/os9lib`, and then `for` speaks where it was
silent), and a load that fails. Its `-?` now ends with a line saying it is a
clean-room reimplementation written so the collection can stand on its own.
It is in DOC/INDEX, ORIGINS, SOURCES.txt and the gallery.

**OS9MDIR is gone from every tool.** The one that mattered was the image
build: `sh` cannot find `tar` once `chd` has moved into the new image, which
is what OS9MDIR was papering over. It now runs `load /dd/CMDS/tar` first and
the fork finds the module without a filesystem search -- 8602 of 8602 files
extracted. The other four now mount their scratch directory as a device and
run the program by its path there.

## Reading the screens found more than taking them did

You were right that they have to be READ. Doing that, one card at a time:

  - **`vc` is a spreadsheet**, not the "visual compare" DOC/INDEX called it --
    and it survived Ctrl-E and ate the next five screens, which is how it was
    found. The harness's readiness check had been fooled by vc echoing the
    marker back; it is split when typed and whole when printed now.
  - **`m4` was mangling its output** -- `i hr ` for `hi there`. The build in
    CMDS/REBUILT is correct and now ships. That is the second swap after
    `sed`; nineteen REBUILT pairs are still untested and worth an hour.
  - **`rayshade` RENDERS.** It needed two things nobody had found: a program
    called `shell`, because OS-9's popen() forks one by that name and this
    disk has bash and sh and no `shell`; and `cccp` in the DATA directory,
    because the forked shell looks there. `copy sh shell` and `copy
    GCC139/gcc_cccp /dd/cccp`, and it traces the scene. **That popen finding
    is bigger than rayshade** -- every program here that uses popen() or
    system() fails the same way.
  - **`des` does not decrypt**: it encrypts to `<file>.n`, removes the
    original, and run over its own output produces 00000000.
  - **`patch` cannot finish**: it recognises a diff and then cannot read its
    own temporary file. `diff` itself is fine.
  - **Ghostscript does not render** -- banner, then no file and no message.
  - `divide` is a file splitter, `find` wants `-n=`, `tail` wants `-l=`,
    `xrf` wants its language table in the data directory, and `for` is a bash
    keyword so the Fortran driver needs its path.

## Reading them again, 2026-08-28: sixteen more wrong labels

Every one of these was a card whose caption said one thing and whose screen
said another. DOC/INDEX is corrected in each case and the card re-shot.

  - **Seven programs bash will not let you reach**: `break`, `enable`, `fc`,
    `for`, `help`, `if` and `trap` are all in CMDS and all bash builtins or
    keywords. Typing the name never reaches the program and never says it
    did -- `help` gave you bash's builtin list, not the .hlp system. Give
    the path and each runs. DOC/STATUS names them; README-RUNNING warns.
  - **`gawk` works.** The old note -- "prints nothing at all" -- was gawk
    sitting on the terminal, because this build IGNORES a filename argument
    and reads standard input whatever it is given. `gawk '{...}' < file`.
  - `fc` splits a big file in two to fit a 360k floppy; it is not "re-execute
    history". `rdoc` is Rueckdokumentation from c't 1988 -- C source in, a
    control-structure skeleton out; not a document reader. `screen` is Russ
    Smith's random screen displayer, not the terminal multiplexer. `bcheck`
    counts brackets in source, not a boot file. `launch` is a login helper.
    `ask` is a client for a `wisecracker' server on /PIPE/txtpipe. `ynad` is
    Yet Another Name & Address program.
  - **`vi` paints two lines** of a file and no more, whatever you do.
    `elvis` fills the screen properly and now has its own card.
  - **`arc` and `ar` need RELATIVE paths.** arc builds its archive under a
    temporary name and then moves it; the move fails on an absolute target
    because this C library has no rename(). Both work perfectly from the
    data directory.
  - `pgmedge` hangs on a photograph -- a 64x36 gradient goes through in a
    second, the same-sized sphere never returns. `etags` cannot build a TAGS
    file at all: the F$SRqMem storm, on any input. `cdiff` cannot finish a
    diff of three lines. `lgrep` prints nothing whatever it is given.
    `sysmon` refused os9exec's V4.0 as too old -- NO LONGER, see item 5a;
    it now starts and dies at `F$GPrDsc`. `ssl` gets an empty segment
    list because os9exec's RBF does not hand back the file descriptor.
  - **Dhrystone had to be asked properly**: at the default run count every
    build finishes before the clock ticks. Two million runs apiece, and GCC
    2 at -O2 comes out about 16% ahead of the Microware build.

The harness learned two things as well: it no longer publishes os9exec's
abort dump printed on top of a program's picture, and a command longer than
the terminal is split so the card does not open mid-word.

## The REBUILT pairs, asked at last

`tools/datatests/rebuilt.cases` is new and holds the answers, so nobody has
to re-open the question:

  - **`vi` should probably not be the EFFO one.** It paints two lines and
    stops. `elvis`, `vi_nocio` and `REBUILT/VI` (PVIC) all paint a full
    screen and edit properly -- I checked PVIC by typing a line into a file
    and writing it out. I did NOT swap: `vi` is the genuine Berkeley ex
    source and the other three are clones, so which name gets which program
    is your call, not a defect I should quietly fix. DOC/INDEX now says
    plainly that `vi` does not paint and names the three that do.
  - `wc` vs `wc.cio`: same counts, different wording, and `wc.cio` cannot
    take a filename. The shipped one is better.
  - `ctags` vs `ctags.elvis`: the shipped one finds the statics; elvis's
    finds `main` and nothing else.
  - `diff` vs `diff_1.1`: identical output, and diff_1.1 is twice the size.
  - `arc` vs `REBUILT/arc`: the shipped one is 5.21 and takes a bare command
    letter; the alternate is 5.12 and wants a leading dash.
  - `lharc` 1.00 vs `lharcs` 1.01: newer, no difference found, each reads
    the other's archives.
  - `screen` vs `REBUILT/screen`: same program, same stop.
  - `kermit` cannot be compared from a script -- both builds sit waiting on
    the terminal whatever you redirect.

## Two loose ends closed, and one that is yours

  - **No module on the disk reports an `R_` name any more.**
    `REBUILT/compress` and `REBUILT/screen` were the last two, both from a
    rebuild pass that forgot `-n=`. Rebuilt with the current driver; the new
    compress makes the same 631-byte archive as the shipped one and each
    reads the other's. `tools/datatests/rebuilt.cases` holds the proof.
  - **`infocom.tcap` is the better Infocom build** and the card shows it
    now: it puts a real status line across the top -- room name and score --
    where plain `infocom` fills the screen with brackets trying to.
  - **snake plays, and scatters text over its own board.** 17 of its 46
    cursor moves in a played game arrive as literal `[13;49H' rather than
    as motion. I rebuilt it from the fixed source to check: identical. So
    the echo fix in `SRC/snake/move.c` is not the cure, and I have corrected
    that comment rather than leaving it claiming to be. The byte stream
    shows one ESC arriving late and one doubled. I have NOT filed anything
    against os9exec: two wrong reports came out of that kind of inference
    before, and this is one program out of 108.

## A third reading, 2026-08-29: one bug found three more

**`printf' works, with one flaw: the literal text BEFORE the first conversion
is dropped.** Everything between and after conversions is right --
`printf "%d %s %d\n" 4 "is bigger than " 3' prints `4 is bigger than  3'
exactly, and `"a%db%dc\n" 1 2' prints `1b2c', losing only the leading `a'.
Begin the format with a conversion and nothing is lost. The degenerate case
of the same flaw is a format with NO conversion: all of it is "before the
first conversion", so it prints nothing. DOC/INDEX said it floods `No more
memory !!!'; it does not, and that entry is corrected. (My first write-up
led with the failure and read as though printf were simply broken -- rdoggett
pointed out that it works most of the time, which is fair and is now what
both the entry and the card say.) Then the same defect turned up
underneath three cards that had been quietly empty for weeks -- `nsort',
`yacc' and `expand' all built their input with `printf "10\n9\n..."', which
wrote nothing at all. All three are rebuilt with echo and all three now show
something.

Reading those three found three more:

  - **`nsort' is not a numeric sort.** Given 3, 22, 111, 4 it answers 111,
    22, 3, 4 -- exactly what GNU `sort' answers with no options. `sort -n'
    is the numeric sort here. Its card now shows all three side by side.
  - **`yacc' hangs** on a three-line grammar, as DOC/INDEX already said;
    its card now shows the grammar and the silence. `bison' reads the same
    grammar in a second.
  - `unexpand' needs `-a' for tabs that are not at the start of a line,
    which is standard and was worth saying: with it the tab round trip
    closes byte for byte.

**`shar' is one broken check away from working.** Its read-access test
rejects every file that EXISTS -- `No read access for file:' for a
world-readable file that `cat' reads. Hand it a name that is NOT there and
the check passes vacuously and out comes the whole shell-archive preamble,
cut line and all. So the archiver is fine and the gatekeeper is not; both
halves are on the card and asserted in the tests. Worse,
**the data-test case for it was a false pass**: it asserted `motd' appeared
in the output, and `motd' appears in the error message. That in turn found a
real bug in `datatest.py': it stripped `#' ANYWHERE in a line, so
`absent  #!/bin/sh' became a bare `absent' matching the empty string. The
screenshot sheet parser had the identical bug and was fixed months ago; the
test harness had it still. Both are fixed, and an empty pattern is now
refused at parse time.

Also corrected: **`roff' and `proff' work** (the index said they failed like
nroff -- they do not; `nroff' hangs, they do not), `hexedit' prints the value
of TERM and exits, `devprc' crashes bare and works with `-h' exactly as `cp'
does, and `cjpeg' refuses every PNM tried -- raw, plain, PGM, 8x8, from a
file and from stdin.

## The disk already had the converter todos was supposed to be

**`autolf' works.** Mike Tozer's, 1995, sitting in CMDS under a DOC/INDEX
entry that said `auto-linefeed filter' and had evidently never been run. As a
FILTER it does exactly what `todos' and `toos9' fail to do: `autolf -c -C -L
< in > out' turns OS-9 text into DOS text -- 40 bytes in, 41 out, the trailing
0D now 0D 0A. It also does LF, tab expansion and ^Z, and `-H' explains the
conversions.

And it explains the others. Given a FILENAME rather than a pipe, autolf
converts through a temporary and reports `couldn't rename'. **That is the
same missing rename() that stops zip and arc** -- and `todos' now says so on
its own card: it converts into `todos.$$$.3' and cannot rename it back, which
is why the file comes back byte-identical and the program looked inert. One
missing library function, four programs. `DOC/STATUS' has them together now.

Found by re-testing DOC/INDEX entries that were short, unstamped and looked
inferred from the program's NAME rather than from running it. About a hundred and eighty were tried and **twenty-eight** were wrong:

| entry said | it actually is |
|---|---|
| `greg` regular-expression search demo | converts a JULIAN DAY NUMBER to a date |
| `qt` quick text utility | tells the time in words -- "just gone ten past four" |
| `vis` make non-printing characters visible | runs a command over and over, like `watch` |
| `dpark` park a process | parks a DISK HEAD at track 00 |
| `gdd` data dump | GNU `dd` |
| `vlen` report a file's record length | a variable-length-record DEMO that builds its own filesystem |
| `owner` show file owner | CHANGES an owner; `fstat` shows one |
| `bush` draw a random bush/tree | a countdown, and it was DOC/START-HERE's welcome example |
| `read_mail` vi's mail-reading helper | its own mail reader, on /dd/MAIL/mail_&lt;user&gt; |
| `lmargin` set a left margin on text | sets it on an EPSON PRINTER |
| `names` list module names in a file | never returns |
| `qp` queue/print helper | expands BACK-QUOTES for the shell |
| `cam` Tektronix demo: camera | a CAMSHAFT lift-curve calculator |
| `version` show a module's version | prints its OWN version, whatever you name |
| `sysmax` show maximum system memory | maximum process AGE |
| `sysmin` show minimum system memory | minimum process PRIORITY |
| `dload` download a file over a serial line | loads a data file into a data MODULE |
| `map` memory map display | the disk BLOCKS a file occupies |
| `transfer` transfer a file between devices | copies from GDOS disks only, no options |
| `suspend` suspend a process | REMOVES it from the system |
| `chbase` change module base | converts a NUMBER between bases |
| `deton` detab -- convert tabs to spaces | an alarm/timeout demonstration |
| `gcl` general calculation utility | a grand digital CLOCK |
| `mshell` a small shell | a MENU shell; wants a menu file |
| `repeat` run a command over and over, with a delay | repeats N times, no delay -- and cannot fork the command |
| `ask` yes/no question for a script | the CLIENT half of `wisecrack` |
| `wisecrack` prints a wisecrack | a SERVER; prints nothing itself |

`combine' turned out to interleave two files byte by byte for EPROM images
rather than merely "combine files", `ape' writes gibberish in the style of
its input, and `mshell' and `mg' both need a real terminal. `bush' is
replaced in DOC/START-HERE by `today', which prints the date in words and
the phase of the moon and is a better first thing to type.

## CLAUDE.md's own bash rules, re-measured -- three were wrong

CLAUDE.md is gitignored, so this is the tracked copy of what was found. All
of it measured 2026-08-29 against the current image.

**WRONG, and corrected in CLAUDE.md:**

  - **`mkdir` DOES have `-p`.** `mkdir -p /dd/tmp/pp/a/b/c` builds the whole
    chain from nothing and mkdir's own usage line lists it. A script written
    around the false rule has to build directories one at a time in the right
    order for no reason. `tools/datatests/files.cases` now asserts it.
  - **Command substitution DOES inherit PATH.** `$(head -n 1 file)` finds
    `head` whether PATH is exported or not. The rule said it reverts to a
    Unix default and that every command inside `$( )` needs an absolute
    path; neither is so.

**RIGHT, but narrower than it was written:**

  - **Shell functions really are invisible inside command substitution** --
    `myfunc` works, `$(myfunc)` is `command not found`. That one fact
    explains the whole symptom the rule was written for.
  - **`-f` and `-d` fail ON A HOST-DIRECTORY MOUNT only.** With `OS9H5=` a
    real directory, `[ -f /h5/README ]` is false for a file `ls` lists and
    `cat` reads. On an RBF image -- `/dd`, or `/h0` when it is the image
    hard-linked -- both work normally. The rule said they are simply not
    usable, which sends you round a detour on the image you actually use.
  - There is no `/dev/null`; `/nil` is the bit bucket. Still true.

## The Fortran compiler works, and nobody had got that far

**RTF/68K 2.14 compiles.** `load /dd/CMDS/os9lib` first -- without its runtime
library the whole Fortran set prints nothing, which is all anyone had ever
recorded -- and then `rtf /dd/SRC/rtf/div.f` answers *"Total Errors 0
Warnings 0, RTF normally completed"* and leaves 1008 bytes of 68k assembly
beside the source. `SRC/rtf` has seven programs to try. The ceiling is real
-- assembling that output needs Microware's r68 and l68, which are not here
-- but it is a long way above "prints nothing".

**Call `rtf` directly.** The `for` driver forks a program called `shell` to
run it and this disk has none, so it prints the command and stops. I proved
that rather than inferring it: built a test image WITH a shell, and the fork
then reaches it and the shell answers `rtf: nowhere found` because it has no
PATH of its own. That is the fourth thing the missing `shell` stops, after
rayshade, `screen` and `qp`.

This came out of asking whether the programs I had called broken were really
broken -- your printf point, applied to everything else I had written that
day. It found three descriptions that were too harsh (printf, shar, hexedit)
and one that was hiding a working compiler.

**A question, not a change I have made -- now measured.** I built a test
image with `sh` copied to `shell` and ran every program that fails for want
of one. Exactly what `copy sh shell` buys:

| program | with no shell | with `sh` as `shell` |
|---|---|---|
| `dm` (Disk Master 1.4) | `ERROR 216: Can't open /pipe/getcwdpipe` | **works fully** -- two-pane browser, directory list, file-information panel |
| `rayshade` | cannot render | **renders** (also needs `cccp` in the data directory) |
| `for` (Fortran driver) | prints the command, stops | reaches the shell, which then says `rtf: nowhere found` -- sh has no PATH of its own |
| `qp` | silent | still silent |
| `screen` | wants `$HOME/.SCREENS` | unchanged -- that is a different problem |

So a plain copy fixes **two** programs outright and gets a third one step
further. A `shell` that also set PATH would probably finish `for` as well.
It is still a new program shipping under a name OS-9 users associate with
Microware's, so it is your call. What I have done instead is document it
everywhere it bites and tell people to call the real program directly --
`rtf` rather than `for`, and so on.

## The front door was telling everyone to type full paths

`disk/readme` -- the first file anybody opens -- said *"bash's PATH search
does not work against this filesystem"* and gave three examples all written
as `/dd/CMDS/...`. **That is the unpacked directory's behaviour, not the
image's.** Run the image the way the disk ships and a bare `cookie` works,
`soundex </dd/SYS/motd` works, PATH is set across every program directory by
SYS/login, and `.bashrc` reads. Point OS9DISK at an unpacked tree instead and
you get `command not found` and `.bashrc: (E$Unit)`. Both measured
2026-08-29, side by side.

That is where the `/dd/CMDS/` noise you objected to came from -- the disk's
own front door taught it. The readme now says "type commands by name" and
gives the directory case as the one exception.

Two doors down, the same file said **the image must be named `dd`** and that
`freeware.rbf` "will not mount". It mounts perfectly when OS9DISK gives its
full path; the filename only matters when os9exec has to find the image for
itself. Also corrected.

And in `DOC/README-RUNNING`: **`ksh` can be the first shell now.** The note
saying it could not -- that it wanted cio loaded and so needed a shell first
-- was true before the five Microware modules shipped here. `os9exec -r
/dd/CMDS/ksh` starts it and it forks external commands normally.

## DOC/DEPENDS was answering for a third of the disk

`gen_depends.py` scanned `CMDS` and `CMDS/GAMES` and nothing else, so **354
programs had no entry at all** in the file whose first line promises "what
each program needs besides its own binary" -- the whole of NETPBM, UUCP, ELM,
TEXCMDS, COMMS, NETWORK, NEWS, WN, ADL, REBUILT, DEMOS, DHRY, GCC139 and MM1.
It now scans all eighteen program directories, the same list `gen_catalog.py`
uses, and DEPENDS went from about 250 programs to **477, with 1333 paths**.

That gap had been found and fixed twice in `gen_catalog.py` and never looked
for here. If a program directory is ever added, both lists need it.

**`/r0` stays out of DEPENDS on purpose** -- the tool's own docstring argues
that listing a device this disk should not provide would imply it should --
so the twenty programs that want a RAM disk are listed in `DOC/STATUS`
instead. That list said seventeen; re-measured 2026-08-29 it is twenty, with
`UUCP/expire`, `UUCP/rnews` and `UUCP/uucico` missed because the earlier
search required a trailing slash and some binaries stop at `/r0`.

## Three figures re-measured, all of them stale in the same direction

Not corrections to prose so much as a reminder that this collection's numbers
move under you. All 2026-08-29, all from the tools that exist to derive them:

  - **Source coverage is 627 of 945, 66%** -- `tools/src_census.py`.
    `CLAUDE.md` said 389 of 937 (41%), measured five days earlier and already
    two improvements to the tool out of date. The recipe count is **484**,
    where it said 203.
  - **429 programs want the collection at `/dd`, 54 want data at `/h0`** --
    `tools/measure_layout.py`. `notes/DECISION-placement.md` said 258 and 53.
    The shift is the disk improving: every recovered data file makes another
    program's `/dd` path resolve.
  - **Twenty programs want a RAM disk at `/r0`**, not seventeen.

Every one of these had a note beside it saying "run the tool, do not quote a
figure", and every one had a quoted figure anyway. `CLAUDE.md` is updated;
it is gitignored, so this is the tracked copy.

## Seventeen programs were filed under what they were mistaken for

Correcting a DOC/INDEX entry is only half of it: `tools/categories.psv`
assigns the browsing category, and it had been filled in from the same wrong
descriptions. `qt` was a text tool because the index called it one, `gcl` a
calculator, `vis` a vi, `chbase' a binary editor, `bush` a drawing, `divide`
a number-base converter, `screen` a terminal multiplexer, `cam` a Tektronix
demo. Seventeen moved on 2026-08-29 and nothing is uncategorised.

**When an entry is corrected, check `tools/categories.psv` too.** The
catalogue groups by category and that is where people actually go looking --
a camshaft calculator filed under Hardware demos is as good as missing.

## Nothing below here needs you

(kept for the record; the two open questions are at the top of this file)

