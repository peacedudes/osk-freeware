# Start here, next session

## DO NEXT -- 2026-09-19

**`notes/FOR-RDOGGETT.md` is FOUR items and every one of them is his**:
push/tag and the CI pin (1), real hardware (3), cancelling usenet-rewind
(7 -- the pull is finished, nothing is left to fetch), and three decisions
(21 cpp, 23 ispell when his source arrives, 24 the duplicate builds).
Read it first; there is nothing in it for you to do.

**utree 3.03b-um is ported, on the disk, and catalogued** -- his own usenet
find, and the first full-screen file manager here.  `SRC/utree/README.OSK`
is the record of every arm.  Three of them are worth carrying forward
because they are about OS-9 and not about utree:

  * **`NODIRENT` is a trap.**  It looks like the switch for a system with
    no `<dirent.h>`; it turns `opendir(n)` into `fopen(n,"r")`, and RBF
    will not open a directory as a plain file.  OS-9 has the real
    opendir/readdir/closedir in `unix.l` and its `<dir.h>` says in its
    first line that they work like BSD 4.2's.  Take the BSD arm.
  * **A full-screen program must read the keyboard with `read()`, one
    byte.**  `getc(stdin)` is buffered, and raw mode has cleared the
    end-of-record character, so the driver waits for a whole buffer and
    the program looks dead from the first keystroke.
  * **A PORT MUST NOT SHELL OUT THROUGH `system()`.**  It forks the bare
    module name `shell' and never reads `$SHELL'.  On a real OS-9 system
    that is right, and `SYS/login` loads yours off /h1 -- but with the
    collection standing by itself there is no such module, and system()
    returns 677130 having printed not one character (measured 2026-09-19,
    twice, with and without blarslib).  `DOC/README-SHELLS` has had that
    since 2026-09-11; what is new is what a PORT does instead, which is
    `os9exec(os9fork, sh, argv, environ, 0, 0)` with the shell `$SHELL`
    names -- `SRC/perl4/osk.c` did it first, `SRC/utree/osk.c` follows --
    **and the `-c` matters**: `ksh "script a b"` runs the script with NO
    arguments (whole string in `$0`, `$#` zero) where `ksh -c "script a b"`
    passes both.  A MODULE gets its arguments either way, which is why
    this went unnoticed.

**AN os9exec LIMIT, NOT AN OS-9 ONE -- and the distinction was nearly
written down the wrong way round.**  `utree /dd' stops partway through SRC
with `ualloc: memory full' while os9exec reports 30 MB free in a 32 MB
arena.  Raising the module's own MEM= from 128k to 1024k moved the free
figure by exactly that much and did not move the failure.  The os9exec
session named it within the hour: `MAXMEMBLOCKS = 512' in os9exec_nt.h is
a COUNT of F$SRqMem blocks per process, not a size, so 512 allocations of
any size exhaust it -- about 2 MB at this C library's 4 KB chunk.  **Real
OS-9 joins adjacent memory blocks and os9exec did not**, so on hardware
utree would very likely read the whole tree; a fix is in flight there.
Our documentation says "open it on a subdirectory, or give `-q'", which
is sensible advice on any machine, and does NOT call it an OS-9 limit.
The general rule this is an instance of: when os9exec is the only thing
you have measured on, say so, and ask.

**`mail' WORKS, and its card said it could not.**  It wants a scratch
device at /r0; `DOC/README-RUNNING` has said all along how to get one
(`mount -r=256k /r0`, and twenty programs want it), and nobody had applied
it.  With a RAM disk mounted, mail sends a message and reads it straight
back.  **Before writing a program off, read the disk's own documentation
for what it needs** -- this is the second time that rule has paid.

**`mailx' -- DO NOT WRITE A MECHANISM FOR IT, and this is why.**  Between
01:25 and 02:15 on 2026-09-19 the SAME command with the SAME environment
gave three different answers: "no mail waiting", then "can't change to
your mailbox directory: 'su'...error 214", then the same with error 216.
An explanation was written into its caption and a case on the strength of
the first two, and had to be withdrawn.  What moved was the os9exec
WORKING COPY beside this one, being rebuilt through the evening (sockets,
and the memory-block ceiling above).  **A verification run against a
sibling's working tree is a run against a moving target** -- note which
binary, and re-run before believing a difference is yours.

**Two more that moved the same way, and both cases were rewritten rather
than chased.**  `msntp' used to answer "unable to allocate socket for
NTP"; os9exec grew real sockets that day and it now BLOCKS instead, so it
is no longer a case (a case that hangs is worse than no case) and the
comment in `net.cases' says so.  `lfmaker' used to print "No more memory"
-- the EMULATOR's message, not the program's -- and went silent while
still answering 208, so `system2.cases' asserts the STATUS now.  **Do not
pin another project's diagnostic text in a case here.**

**Programs under no test: 15, from 22** (`tools/worklist.py --programs
--no-test`).  `tools/datatests/refusals.cases` took seven on the principle
that **a refusal is a measurement**.  Flagged cards: 24 of 965.

**One process note.**  `tools/datatests/untested.cases` was overwritten by a
`cat >` that did not check whether the file was there; git had it and it is
restored, and the new cases live in `refusals.cases`.  Look before you
write, the same way you look before you delete.

## DO NEXT -- 2026-09-18 (done; kept for what it measured)

**rdoggett read the gallery and the decisions list and sent two pages of
notes.  Working through them was this session, and eleven of the eighteen
open questions are answered and gone.**  `notes/FOR-RDOGGETT.md` is rewritten
and is short now; read it first.  What is left for him: push and the CI pin
(1), real hardware (3), cancelling usenet-rewind (7, now unblocked), the
three Kientzle transfer programs (17), the GPL binaries (20), omega and the
DECUS cpp (21), ispell when his source arrives (23), and one new one -- the
twelve remaining "second build of" duplicates (24).

**THE QUEUE HE SET IS FINISHED.**  The usenet last-ditch pull is complete
(nine groups, every count matching the site's index); the CoCo Community
Archive survey is complete (26 images, no candidates -- and note it is 26,
not the 24 first reported, and that `frames.dsk' needed its two-byte JVC
header stripped before either reader could see it); and the clamp screen
sweep is DONE.  Both halves of the sweep were run: the exact one over every
stored play-test raw found nothing, and the filter over cards flagged 96, of
which 82 changed.  `spline' went from 119 ink to 1898 and `lorenz3d' from
108 to 1856.  Three picture cards -- `djpeg', `pgmramp', `pnmtile' -- turned
out to draw WIDER THAN 80 COLUMNS, which is why the clamp had been eating
them; given windows that fit (164 and 156 columns) they show whole pictures
and touch no margin.

**WHAT IS OPEN NOW** is `notes/FOR-RDOGGETT.md` (five items, all his), and
one thread of our own: **UNIX FILE MODES ARE NOT OS-9 MODES**, below.

**UNIX FILE MODES ARE NOT OS-9 MODES -- a live defect class, seven sites
still unchecked.**  `open(name, 0)' is O_RDONLY on Unix and NO ACCESS BITS
on OS-9, so the open succeeds and every read through it is refused E$BMode.
The os9exec session traced it in `patch' (which is fixed and applies diffs
now); a scan of disk/SRC found 76 call sites across 34 trees, most of them
harmless or deliberate -- a stat() shim opens mode 0 ON PURPOSE.  `bmgtest'
and `bmgtest2' had it live and are fixed.  The seven still to check are
listed with line numbers in `disk/SRC/strsch/README.OSK`, and the test is
cheap: hand the program a NAMED file, then the same data on standard input.
If the second works and the first does not, it is this.

**What changed on the disk today, so nothing is re-derived:**

  * **Twenty-nine programs came off on his rulings**, each recorded in
    SOURCES.txt: six utilities written at Microware (time, timid, deton,
    sysid, sysmax, sysmin); greed; travesty; puzzle15, puz15, udate, uwho;
    the EFFO `vi'; sysmon; RCS's seven; SEDT's `e', `new_e' and `sedt';
    btree and isam; `break', which is Microware's own utility disassembled;
    and fibo, float, touchtype, vi_cio and compress_rebuilt as duplicates or
    broken.  Eight misfiled documentation directories went too.
  * **`vi' is PVIC now.**  The EFFO vi was XENIX-derived; `vi_nocio' took
    the name, module renamed to match, and DOC/README-VI is rewritten around
    the two editors left.
  * **Three things were FIXED rather than written off.**  `top' walked off
    the end of its own process table -- rebuilt, and it runs; `compress' is
    the build whose putchar double-evaluation is fixed; `make' links a
    utime() of the collection's own instead of a file with no grant.
  * **Two things are new.**  `man' reads the ~300 manual pages that were
    already here (DOC/MANPAGES is its generated index, with a gate check),
    and `fact' is a twenty-line Fortran example that compiles on this disk
    and runs, which is what he asked Fortran to have.
  * **DOC/README-NAMES is new**: twenty programs here carry the name of a
    utility the reader already owns, and it says what decides which one runs.
  * README-EDITORS answers "which of the six Emacsen"; README-GCC answers
    "which gcc"; card captions now show quoted keys in the accent colour.

**Tools worth knowing about**: `tools/program_refs.py <name>` finds every
reference to a program, and `tools/remove_program.py <name>` does the
mechanical removal and reports what needs a person.  Twenty-nine removals in
one day is what they exist for.

## The session before this one -- 2026-09-14 (late)

Settled this session (committed; do not re-derive):
  * **lmail never hung** -- it retries its lock in /DD/SYS/.LOCKS/MAIL.LOCKS
    every 10 s for 20 min, and that directory did not ship.  It ships now
    (`.keep' placeholders, since the disk's tar drops nested empty dirs) and
    lmail delivers; mail.cases asserts it.  uux and uupoll want the same dir.
  * **rcsdiff works under Microware's shell** with co in a directory RCS
    inside CMDS: its system() line is `%s/co ... >-%s' with /dd/cmds/rcs
    compiled in.  On this disk CMDS/rcs is the rcs PROGRAM (case-insensitive
    RBF), so that directory cannot exist beside it, and ksh cannot parse >-.
    Card and requires.psv say so.  rcsmerge carries the same string.
  * **hist** keeps its history on /r0 unless given a file and runs every
    command through a module named `shell'.  Under the SDK shell with
    `hist <file>' it works (h lists, logout leaves).
  * **sdb's quit command is `exit'**, not q; INDEX and card said q.
  * **gnugo, sdb Stack Overflow** is their own recursion at end of input
    (gnugo's getmove() calls itself per illegal move).  Not os9exec.
  * **vtxtcn works** beside SRC/world/vtext.dat (it is World's build step).
  * **monop's dice were garbage** (rolls 52400, 10315): roll.c assumes a
    15-bit rand() unless vax is defined and /dd/LIB/rand.r gives 31 bits.
    Rebuilt with `vax' (6001c4a5).  The other 25 rand.r recipes were scanned
    for 15-bit constants and are clean.
  * Cases now play gnugo, jotto, poker, blackjak, mastrm, hinterhalt, monop
    to a real ending.

Open:
  1. **os9exec: I$MakDir onto an existing DIRECTORY on an RBF image answers
     E$FNA; an existing file, or a host dir, answers E$CEF.**  Reported to
     os9exec-d9 with a repro; they will check the Technical Manual.  This is
     perl's "mkdir answers E$FNA".  FIXED in d74b174: makdir and perl's
     mkdir both give E$CEF now (measured).  perl's rmdir is a known absence
     (README-OSK); s2p is a shell script and is deliberately not built.
  1a. **os9exec F$GPrDsc bound check: FIXED in 143152b** (unpushed).  sysmon
     now stops walking at E$IPrcID and draws its monitor; its stanza runs
     `sysmon 2>/nil' so os9exec's `F$SetSys: unimplemented 08A6/08A8'
     notices stay off the screen.  Reshoot needs OS9EXEC at or past 143152b.
  1d. **os9exec RBF lost update -- image corruption: FIXED in b3145c3**
     (unpushed; misc.cases 18 of 18 on it, measured 2026-09-14).  Each path keeps its own copy of the current sector and
     writes it all back when done, so two update paths on one sector lose
     each other's bytes.  `move' links the new entry through one path and
     zeroes the old entry's first byte through the other; the zero is lost,
     and every move leaves two names on one FD (dump of /dd/tmp/MVX showed
     mv1..mv4 all on $80AEC).  Deleting either frees sectors the other
     uses.  misc.cases `move-relinks...' was blind (it matched its own rm's
     message) and now requires the old name gone: it FAILS until the fix,
     a fourth deliberate failure beside zip, todos, sir.  The release
     image is built by tar, so it is not affected.
  1b. Lead, sent to os9exec-d9, unproven: aprocs shows every process's age
     as ~2^32 s where Microware's procs -e shows 0:00; D_Julian/D_Second
     read correctly, so suspect the descriptor's start date/time.  The
     aprocs card's caption credits those globals.
  1c. cpu stops with a math-handler overflow (vector 7, D0=$7FF00000)
     straight after F$Time when run under -r; paced, the card reaches test
     11.  Probably an elapsed time of zero; not chased.
  2. **Full-screen programs** on `worklist.py --programs --no-test` -- play-
     tests (tools/playtests/*.keys) are the instrument.  First batch of 12
     written 2026-09-14 from their card stanzas: hang bog saa othello hexa
     robots worm mines tt accordian tttt greed.
  2a. **Play-tests had been deleted, not missing.**  The 2026-09-03 card
     pass (27521b0b, f7c6f94c) removed about forty tools/playtests/*.keys
     -- animal, bog, tt, advent, chess... -- while making one card per
     game, with no reason in either message.  A card captures; a play-test
     asserts, and worklist.py counts only the latter, so those programs
     reappeared as untested.  Written again 2026-09-14 from the card
     stanzas, each committed only after it passed (hang shown failing on
     a wrong expect first).  xmas expects the credit line, not HAPPY
     HOLIDAYS, which only later frames draw.  larn and ularn snap the
     opening text first: the dungeon starts dark and the ink check called
     it STARVED.  Left out on purpose: snake (11 orphans, its stray cursor
     text) and sddemo (writes at 24;80 forever and ignores E).
  2b. Also settled 2026-09-14 (late): **cron works** under Microware's
     shell -- an every-minute crontab line ran within 80 s (it reads
     /dd/usr/lib/crontab, forks `shell').  **rnews works**; it numbers
     articles from SYS/UUCP/active, so a case must save and restore it.
     **rayshade renders** in a case with sh copied to CMDS/shell and
     gcc_cccp to /dd/cccp.  kermit/kermit2/sterm/wysecrack want a line;
     mailx wants MAIL to be a directory of per-user folders; lmargin
     writes nothing to stdout (printer path); tplot rejects every answer
     to `x interval ?'; creadoc and hist need Microware's shell.
  2c. **os9exec f7b31ea (host-dir rename)**: mv and wndex pass on a host
     /dd; move still E$BMode (second update path on the same dir, entry
     at $2C0); upperdir E$Share because it holds subdir open while
     rewriting its entry.  Both traces sent to os9exec-d9.  upperdir FIXED
     in 517d4f4 (system family 15/16 on a host dir, only combine left);
     b2bee94 fixed adlrun's zero-length read.  move FIXED on host dirs in
     c360ba0 (misc 18/18 on a host dir).  No host-dir rename case is open.
     Full datatest on a fresh image with b2bee94: 796 of 800 -- zip, todos,
     sir, and tail's stale rsconvert-crash case, since rewritten (17/17).
  2d. **rsconvert works; its header asked for 11.2k.**  It converts a
     rayshade 3 scene to rayshade 4 syntax (INDEX said image formats), and
     its yacc parser overflowed that stack.  `#24k' at Microware's shell was
     enough; CMDS/rsconvert's M$Mem is now 32k (CRC recomputed with
     rename_module.py's crc24, parity untouched since $38 is outside it).
     netpbm6.cases asserts it, shown failing on the old binary.
  2e. **tplot** takes each answer as two numbers (`0 10'), then draws
     through Atari ST A-line traps ($A000) -- an ST program, not a fault.
  2f. **os9exec host-dir assert**: a zero-length I$Read with A0=0 aborts on
     `buffer!=NULL' in pFread (fileaccess.c:338).  adlrun does it; on an
     image it is fine.  Sent to os9exec-d9.  This is the whole host-dir
     games4 difference.
  2g. **disk/ is hard-linked to an unknown twin** (FOR-RDOGGETT 18).
     `ls -li' before changing a file under disk/.
  2h. **vtxtcn's card works** (it had run in GAMES/WORLD, where vtext.dat
     is absent, so it read a NULL FILE forever); panel exception retired.
     dm needs Microware's pd (`pd >/pipe/getcwdpipe' through SHELL) and
     uuxqt needs its procs -- both in requires.psv.  sysmon.keys passes
     only on os9exec 143152b or later.  rcsmerge is an audit_cards
     exception with the measured reason.  Leftover no-test list is 26:
     hardware, G-Windows, a peer, or Microware's own shell and utilities.
  2i. **Running tools/ci/run_workflow_locally.sh from the repo root fails
     at its first step, and it is the environment, not the workflow.**
     The repo root holds a gitignored `tar' -- an OS-9/68K module dated
     2026-09-13 22:05 -- and this shell's PATH contains `.', so the
     script's `git archive | tar -x' ran the OS-9 module (`cannot execute
     binary file'), exported nothing, and every later step reported on an
     empty tree (`cannot read /dd/startup').  Run it with cwd elsewhere.
     The `tar' file was left alone: it is in rdoggett's working tree.
  2j. **CI could never have built an image, found and fixed 894e158e.**
     Five captures (corewar, cwasm, cwdis, monop, yahtzee2 .shot.txt) had
     been committed into the gitignored notes/playtests, so a clean
     checkout was not capture-free: `gen_screens.py --check' took the
     regenerate path, deleted docs/screens/ and wrote a five-screen
     screens.js, and mkimage's gate then failed with 841 problems.  The
     five are untracked and --check now writes nothing.  Proved with
     tools/ci/run_workflow_locally.sh (run it with cwd outside the repo).
     After the fix the WHOLE workflow passes locally at the current pin
     261b4b6 and at b3145c3: image reads /dd/startup, runs a module,
     281M compresses to 43M.  Still never run on GitHub (Linux); the
     dot-file pin note in FOR-RDOGGETT item 1 is about exactly that.
     e99b3a54 makes the script cd out of the repo first; verified by a
     full passing run started from the repo root (11917 files exported).
  2k. games4's advcom case piped advcom into head; on a host dir head's
     exit cut advcom off mid-write (advint: `bad data file').  Output now
     goes to a file.  os9exec b2bee94 fixed adlrun's zero-length read.
  2l. **playtest.py never mounted its image as /h0** (fixed 29d879b6).  It
     passed OS9DISK only, so os9exec used the repo's `h0' link -- the WORKING
     osk-freeware.dd -- as /h0 on every play-test ever run, beside rdoggett's
     open emulator.  hack's playground is an /h0 path: a save `0tester' was
     written into his image at 22:39 (FOR-RDOGGETT 19).  Any play-test result
     for a program that reads /h0 data is from the wrong disk until rerun.
     The full --all run of 2026-09-14 night was stopped with SIGTERM for it.
     I also committed 29d879b6 with the gate red (NetHack's card was not yet
     shot) -- the rule is green before every commit.
  2m. **NetHack 3.0f (TOP) is in** (4df6cc54).  **UMoria 4.87 (TOP) is
     rebuilt from TOP's source**, game code untouched (rdoggett 2026-09-15:
     no big changes to something already ported).  TOP's binary cannot draw
     a screen here, measured with a corrected termcap too.  Mellin's ncurses
     had three faults with SYS/termcap, all fixed in SRC/moria/tcentry.c, a
     read_entry() linked ahead of ncurses.l: (1) it takes only an entry
     whose third character is `|'; (2) it decodes termcap `\n' as OS-9 C's
     '\n', a CR, so do=\n never moved down (this, not nonl(), was why
     screens drew over one line -- BUGGY_CURSES is NOT needed); (3) it
     treats am as wrap-now, and on an xn terminal cursor motion cancels the
     wrap, so map rows piled at column 80 -- the shim hides am when xn is
     present.  The SYS/termcap `vt|' alias noted here before is not needed
     and SYS/termcap is unchanged.  Also found on the way: DEFS/ncurses
     lacked terminfo.h, which its curses.h includes; the driver's long
     path did not pass -V= to per-file compiles; and a replacement for a
     LIBRARY function in the parts library is never pulled -- the new
     recipe keyword LINKFIRST= puts its object on the link line.
  2o. **Mazewar (TOP, Ulrich Dessauer) staged as TOP's binary**, unchanged:
     CMDS/GAMES/mw and USR/GAMES/LIB/MAZEWAR/maze.  No source anywhere in
     the pool (ftp/mw/y/SRC/mw.a is a Microware logo array, unrelated); no
     terms stated.  Needs cio -- measured: all five runtime modules withheld
     gives "Can't install trap handler", cio alone restored runs -- so it is
     starred and the grid is All 341.  `mw -l=5 >/nil &' starts a computer
     player that joins as player 2; the card and mw.keys use that.  It
     sends the xterm entry's ec (`ESC[%dX') unexpanded once, at quit.
     tools/helpcap.py is mode 644 in git: run it as `python3 tools/helpcap.py
     --only <name> --image <scratch>' -- it DEFAULTS to osk-freeware.dd.
     MNews is next and large: whole package as source (inews, rnews,
     sendbatch, nn 6.3); its licence forbids shipping only part of it
     (PLAN-acquisitions B9).
  2p. **atc (4.3BSD Net/2, Ed James) in progress**: disk/SRC/atc (ORIG +
     port), GAMES/ATC, CMDS/GAMES/atc built clean (70,778 b).  Built on the
     source's own SYSV path with OSK guards (README.OSK).  grammar.c/lex.c
     generated ON OS-9 by the disk's yacc -d and flex -S/dd/LIB/flex.skel,
     both exit 0 -- dogfood that worked first time.  Four build findings,
     each a general trap: (1) a 53K local array -> as68 `value out of
     range' (16-bit displacement); (2) the same array static -> l68
     `non-remote data allocation ... exceeds 64k'; malloc fixed both;
     (3) the disk's flex skeleton omits the yywrap() macro under OSK, so the
     program must supply yywrap(); (4) curses.l defines update(), so a game
     function named update clashes at link.  atan2 is only in blarslib.l;
     unix.l's alarm() sends signal 5 and DEFS/signal.h has no SIGALRM.
     **UNBLOCKED: os9exec-d9 fixed it in 40facae** (fix/scf-pd-eor, not
     pushed; built in scratchpad os9r).  Re-measure alarmtest/readtest/
     sigtest/cursestest and atc on that binary with OS9EXEC=<os9r>/os9exec --
     every harness honours OS9EXEC.  The report as filed:
     **was BLOCKED on an os9exec bug, reported to os9exec-d9 2026-09-15:** F$Alarm
     ignores bit 31 of d3 (Microware: bit 31 set = 256ths of a second), so
     unix.l's alarm() -- d3 = secs<<8 | $80000000 -- never fires and atc's
     clock never ticks.  Measured with scratchpad sigpool/alarmtest:
     `alarm=0 errno=0 caught-after-sleep=0'.  os9exec's own F$Sleep decodes
     the bit.  The radar draws; keys do nothing; a BEL flood follows (its
     getAChar gets -1 in a loop -- not yet explained, re-measure once alarms
     fire).  Microware also says an alarm during I$Read makes the read return
     an error, so the SYSV EINTR retry is right in shape; which error number
     (probably the signal code, per the error table) is unmeasured, and
     include.h's EINTR 0x40 is a placeholder until then.  Uncommitted: SRC/atc,
     GAMES/ATC, CMDS/GAMES/atc, recipe, games4 cases, catalogue rows -- the
     gate is red until INDEX and card exist.  Skills gaps (F$Alarm encoding;
     ipc.md "resume the wait" vs I$Read) sent to os9-dev-skill-fc.
     **CORRECTION, measured on 40facae:** the frozen clock was ATC'S bug, not
     os9exec's.  unix.l's signal() never calls a handler asynchronously: it
     installs intercept(sig_catch), which only stores _last_signal_, and the
     handler runs when the program calls check_signal().  Every `caught=0'
     above was that, on any emulator -- the F$Alarm bit-31 fix still stands
     on code reading and os9exec's own tests; both sessions told.  Measured:
     Microware intercept() delivery works; an alarm during read()/readln()
     returns -1 with errno = the signal code (5), as Microware specifies;
     stdio then keeps ferror(stdin) set, so getchar() fails at once until
     clearerr() -- that was the BEL flood.  Fix in graphics.c getAChar:
     on -1 with errno==SIGALRM, clearerr + check_signal() + retry.
     **atc PLAYS on 40facae** (measured 2026-09-15): the clock ticks (Time 1,
     2, 3), a plane holds at the airport, ^C reaches quit() through
     check_signal() and asks `Really quit?', no BEL.  Its getAChar retry
     takes any signal code 1-31, not only SIGALRM, because ^C (3) aborts the
     read the same way.  On quit it printed `getpwuid failed for uid 0':
     blarslib.l's getpwuid (linked for atan2) reads the password file, so
     log.c now takes the name from USER under OSK.  On d74b174 (the current
     pin) the clock does not run at all -- the card needs 40facae or later.
     Still to do: record, help, card, games4, gate, commit (chain running).
     Unexplained, not chased: scratchpad sigpool/cursestest (initscr, crmode,
     noecho, alarm, five getchar()) printed nothing at all on 40facae or
     d74b174 -- not even its endwin; its five getchar() may never return.
  2q. **trek (4.3BSD Net/2, Eric Allman) built and tested, commit pending**
     (the gate is red only while atc is uncatalogued; they commit together):
     games4 `trek-sets-up-a-game-and-scans-the-first-quadrant' passes and its
     must-fail copy fails; card shot (ink 439); trek.keys PASS (ink 431).
     Earlier status: disk/SRC/trek (ORIG + port), recipe, catalogue rows,
     tools/playtests/trek.keys.  Line-oriented, no data files.  Three OSK
     guards (README.OSK): main.c gtty; dumpgame.c creat/open modes (Unix
     0644 as an OS-9 attribute byte sets $80, the directory bit); trek.h
     Device[] extern.  Two general c68/cpp traps found on the way:
     (1) c68 rejects a header definition without extern followed by the
     same variable's initialised definition in one file (`multiple
     definition'), where ANSI C accepts it as tentative;
     (2) **Microware cpp: a comment opened on a #if/#ifdef/#else line must
     close on that line.**  A two-line comment there turned the next line
     into code, broke the #ifdef pairing, and every source reported
     `undeclared identifier' for Device.  Put the comment above the directive.
     (3) **l68 has no common symbols.**  A global defined (not extern) in a
     header is defined in every file that includes it; a Unix ld merges
     those, l68 reports `Symbol 'X' ... has already appeared' for each and
     counts every copy toward the 64K data limit (trek: 66,476 bytes).
     Fix used: an EXTERN prefix, extern on OSK, empty in the one file
     (externs.c) that defines them.  Expect this in most BSD games.
  2r. **TOP's v7make, scpp, cpp.decus -- measured 2026-09-15, not shipped.**
     v7make (public domain) and scpp (Tektronix 1985, non-commercial -- Q1)
     ship as TOP binaries; both need cio (trap-handler message with the five
     modules withheld; both run with cio alone restored).  scpp works:
     `scpp -MWIDTH s.c' expands WIDTH and leaves DEPTH.  v7make CANNOT run a
     command here: it does system("shell \"cmd\""), the disk has no `shell'
     module (`Error code 663304'), and SHELL=ksh fails too (`663312').  It
     would need a -qm rebuild that runs commands through ksh -- a change to a
     period port, so ask before doing it.  cpp.decus (Minow, PD) is source
     only, not built yet.  Test files: scratchpad top3.cases, hostwith/tmp/TOP3.
     Harness trap met on the way: `expect MADE' matched inside `NOT-MADE' --
     use tokens that cannot contain each other (BUILT=yes / BUILT=no).
  2s. **TOP's ncurses programs run UNCHANGED with SYS/termcap.entry sourced**
     (read 2026-09-15, TOP src/ncurses/SRC/lib_setup.c lines 113-118): when
     TERMCAP does not start with `/' it goes straight to interpret_buf(), so
     neither the third-character `|' rule nor the name match applies, and
     termcap.entry's do=\E[B avoids the `\n' decode fault.  Every TOP binary
     built on ncurses -- bandit, typefast, yahtzee, wanderer2, sokoban2, and
     TOP's own moria -- rejects plain SYS/termcap with `'vt100': Unknown
     terminal type'.  Reach for termcap.entry before rebuilding one.  Caveat:
     the entry declares am without xn, so a screen that writes column 80 can
     still misdraw on an xterm (moria's full-width map did).  TOP game triage
     is in PLAN-acquisitions B6: sokoban2, wanderer2 and yahtzee duplicate
     disk games; bandit and typefast are new and trap-free; tetrix, robots2
     and sod need cio.
  2t. **bandit (62a90132), wns and dc (7c43b9c0), typefast (cf359c1d)
     shipped; SYS/termcap.entry dropped `am' (509e569c).**  The entry
     declared `am' without `xn', so TOP's ncurses misdrew any full-width
     row; gnuchess, jargon and vi_cio draw identically without it.  wns and
     dc need cio; bandit and typefast are trap-free.  dc's card sets
     DCGRAPHIC=++++|- out of sight for plain boxes.
     Harness trap: playtest.py keys files treat `#' as a comment ANYWHERE, so
     a setup line holding `co#80' is silently cut -- put such a line in a file
     and source it.
  2u. **castle (The Realm of the Wizard, CSG v08i093-097) ported.**  Patch1
     (v09i031) had never been applied and is now; ORIG/patches01 keeps it.
     Worth knowing for any curses game here: **SCF turns ^C and ^E into
     signals, the signal aborts curses' read, stdio's error flag latches and
     getch() spins** -- castle hung on ^C and died unsaved on ^E, its save
     key.  **And ESC is SCF's end-of-file character: getch() returns -1 for
     it** (measured with a curses probe), so castle's inventory, which only
     ESC leaves, trapped the player.  Microware curses' crmode() never
     touches SS_Opt, so nothing clears any of these for you.  castle's tty.c
     clears kbich/kbach/eofch while the game runs and restores them (sc.c
     clears kbach the same way); restore measured with a probe after quit
     and after save.  Not every ESC key here has this bug: howto.psv records
     sonnet and setterm quitting on ESC and moria taking it at character
     creation, so those read it some other way.  Check per program.
     Also: the build links unix.l, whose
     signal() only records -- a handler never runs by itself (the skill's
     os9-clib-reference says so).  And curses.l HAS savetty()/resetty(), so
     a shim of those names clashes at l68.
  2v. **arithmetic (4.3BSD Net/2) ported; TOP's tetrix is a DUPLICATE of
     `tet'** -- same Quentin Neill source with TOP's OSK arms, and tet is
     already a trap-free rebuild with an echo fix, so tetrix was withdrawn
     unshipped.  arithmetic's only real change: unix.l's signal() only
     records, so ^C aborted fgets and it left with no score; a
     check_signal() on the failed read runs intr() as BSD did (atc's
     pattern).  Measured and parked: TOP's robots2 stops os9exec with
     `Illegal instruction' in its data area just after F$ID, with
     SYS/password open -- not yet known whether it is the program, its cio
     linkage or the emulator.  Disassembly (m68k-elf-objdump is on this
     Mac): 0x3fa8 is its intercept routine, which looks the signal up in a
     table and jsr's through the entry before F$RTE; the faulting address
     equals A0, so a signal it never registered probably sends it into the
     table.  Which signal, and who sends it, is unmeasured.  sod (TOP, needs cio) draws its maze and
     answers `q'; wants /h0/USR/GAMES/LIB/SOD and /dd/TMP lock files.
  2w. **Shipped since 2v: juggle (f7c4c48f), sod (09bee004), jumble
     (e51b6871), rot22's high-bit fix (c445effd); agrep 2.01 in its gate
     run at handoff.**  Three porting traps agrep turned up, each measured
     and each now in the os9-dev skill's references:
     - **`remote' storage lifts l68's 64K and the 32K stack displacement.**
       `remote char big[300000]' at file scope and `static remote' on a big
       local both link and read back (scratch remotepool).  agrep's megabyte
       of buffers is REMOTE/LREMOTE under OSK.
     - **`open(path, 0)' succeeds and every read fails** -- Unix O_RDONLY is 0,
       OS-9 read is 1.  Named files searched as empty while stdin worked.
     - **<stdio.h>'s putc/putchar evaluate the character twice** (the
       line-buffer test compares it with '\n'), so putchar(*p++) prints every
       other character.  fputc() is a function.
     Plan rows go stale: ten were already shipped (memory
     os9-plan-rows-go-stale).  TOP's native tools are all duplicates or
     multi-user; B11 assessed; ASCII plasma left out; Toon incomplete.
  2x. **agrep (1665fc8a), sgrep (f4a2b6f3), rogue 5.3 clone (520034e2).**  rogue's author put every system dependence in
     machdep.c; its OSK arm taught three things worth knowing:
     - **A comment can state an argument's sense backwards.**
       md_control_keybord's comment says true sets the keyboard up; its
       code, and start_window()'s call with 0, say false does.  Following
       the comment left ^C/^E/ESC set during play and cleared at exit.
     - **Two save/restore pairs that each restore a WHOLE _gs_opt copy
       clobber each other.**  The keyboard pair saved after echo was off
       and put echo back off after the echo pair had turned it on.  Restore
       only the fields you changed.  Measured with castle's optprobe.
     - **`#define getchar()' over <stdio.h>'s macro draws only a `redefined
       macro' warning, and the build read keys wrongly until `#undef getchar'
       came first.**  Evidence the first definition stays; not isolated.
     Also: rogue keys its scores by USER, so a second nickname replaces the
     entry -- two USERs are what shows fopen "r+w" keeps the file (it does).
  2y. **Three more IOCCC entries, compress's pipe bug, and a stale image
     (2026-09-15).**  bjack, jaw and trigraph (ee8962ca) build from
     SRC/ioccc/OSK; README.OSK there lists every change, and queens's
     credit is corrected from the contest's hint file.
     **Microware's putc/putchar macro evaluates its argument twice when the
     stream is line-buffered -- a pipe or a terminal -- and once into a
     file.**  `putchar(*p++)' is exact in every redirect-to-file test and
     corrupt through `| cat'.  jaw had it (fputc now); so does compress.c:
     REBUILT/compress_rebuilt is fixed (66797841), CMDS/compress keeps it
     (FOR-RDOGGETT 22).  Of the 30 SRC files passing ++/-- to putc or
     putchar, ls, m4, proff, spew and pbmtomacp were measured through a
     pipe and are clean.  **Test output through a pipe, not only a file.**
     **osk-freeware.dd had last been built 2026-09-13** (sector 0, DD.DAT at
     0x1A), so perl and everything since were missing from rdoggett's
     `free' session; its 07:41 mtime was a session writing to it, not a
     build.  Rebuilt 07:58, the old one kept as osk-freeware-2026-09-13.dd.
     Read the creation date in sector 0 before trusting an image's mtime.
     **CMDS/ispell faults at its first dictionary lookup** and its card had
     captioned the crash as working.  Not os9exec: a probe reading the hash
     in ispell's own three read() calls got every byte under both builds,
     and a host-side walk of LIB/ispell.hash with hash.c finds THE, CAT and
     HELLO with 24-byte entries.  SRC/ispell is a different edition from the
     binary; built, it works, and ships as REBUILT/ispell_rebuilt
     (1b74fb46).  FOR-RDOGGETT 23.
     **Caption sweep for the same defect:** 30 published captures carry a
     failure signature (Process Aborted, Error #, No more memory, not
     found, Unknown terminal type).  Each was read against its whole
     caption; every other one says what the screen shows.  config's card
     ends with os9exec's own `# No more memory' notices as config probes the
     heap -- true output, unexplained on the card.  A crash captioned as
     working shows up only when the caption and the capture are read
     together; tools/audit_cards scores ink, not agreement.
     **An outer timeout on datatest leaves a STALE LOCK** (<image>.lock
     naming the dead datatest pid), and every later datatest on that image
     then refuses to run -- silently, if its output went to /dev/null, so
     the probe looks like it produced nothing.  It cost two runs on
     2026-09-15 after `gtimeout 120 datatest' killed a loco probe; the
     emulator underneath kept running until datatest's own inner timeout.
     Give datatest its own timeout rather than wrapping it, and keep its
     last lines visible.
     **From the Unix posts (notes/PLAN-acquisitions, "The 135 Unix posts"):**
     choose and pig (1ac41c32); hanoi, hanoimod, telewords, telenum,
     anagram, psychic and lotto (d63c88c4).  telenum was the third program
     today with putchar's double evaluation -- `telenum hello' printed 456
     on a terminal.  A card's shown screen is the check on its caption:
     anagram's said "the words hiding in parsley" over a screen showing only
     parsley, and gen_screens scored it fine.
     Later the same night: knight, bks (488587fd), sol, solx (33739d93),
     calcdate, soelim, ticktalk (3a74512d), jumble2 (c622dbe9), weekday and
     repunsel (545b494f).  Two traps worth keeping: Microware cpp joins backslash-
     continued lines BEFORE evaluating #if, so an over-512 string in a
     skipped #else still kills it with no diagnostic -- the long text must
     be absent from the compiled file; and Microware termlib's BC and UP
     are char pointers (PC is PC_), so a program declaring them as arrays
     links cleanly and overwrites them.  robots2: the skill session later
     measured that the TOP termcap library's FILE route works once the
     entry's first field is the old two-character form (`d0|vt100:...');
     robots2 then dies later, at I$SetStt, a separate bug.
  2z. **Later on 2026-09-15: nine more ports, and the traps they found.**
     chemtab (8d537dd8), vcraps (c001e096), translit (f15d0115), trek73
     (b20bcb93), roll, ski and wf (3508b84c), hp (77989aad), bugs -- the
     dr_mario post -- (18246404); smiley is ported and parked on branch
     hold/smiley (FOR-RDOGGETT 24); letters is under way.  Every
     README.OSK lists its changes; notes/PLAN-acquisitions has the rest.
     **AT&T lex programs need five things under the disk's flex** (memory
     os9-lex-to-flex-ports): flex ignores the program's input()/unput(),
     so feed YY_INPUT; `flex -I' when the parser reads the line through a
     shared pointer (hp said "stack underflow" for 2 3 + without it);
     yyrestart() before each parse; supply yywrap(); extern any global the
     .l defines again.  Make y.tab.c and lex.yy.c ON OS-9 with the disk's
     yacc and flex, never from a posted grammar.c.
     **Static data past 64K: declare it `remote'** (wf's word lists, as jaw's
     tables) -- r68 says "value out of range", l68 "exceeds 64k".
     **A program's own setterm() collides with curses.l's**, which every
     build links (letters); rename it under OSK.
     **`};' after a function body is "identifier missing"** (wf, four times).
     **Microware cpp rejects #ident even in a skipped #if** (trek73, 33
     files); make each a comment, in the .y and .l too.
     **A value returned from main reaches the shell as 0**; exit() gives the
     real status (smiley's unknown-face count).
     **toos9's INDEX entry named `autolf -l -C', which converts nothing**
     (13ffcea2): measured, `autolf -C' makes OS-9 lines of DOS text.
     **gen_screens drops a capture under 30 characters of ink** -- hp's first
     card was 21 and simply did not publish; the gate says "no card".
     Make the card show more of the program; do not lower the floor.
     **Blunt: two translit datatests ran against osk-freeware.dd**, which
     harnesses must never use; they wrote only to a host directory, but
     datatest takes the image lock.  Every run since used a *-cb.dd.
     **Later still:** letters (1c377278; help fixed 708aaeca, sleep 08ac93a4) and
     kalah (726c8243), the first program from the 6809 archive's C; CoCo-only
     items in the c09_ tree are settled in PLAN-acquisitions.
     **os9exec returned at once from a sleep under one tick** -- letters'
     10 ms pause was 2/256 and every word fell the whole screen.  Reported
     with a probe; fixed in os9exec 263b94a (it now rounds up, as the manual
     gives for F$Alarm).  A floor I had added for it was taken out again, so
     that the game runs at its author's pace on a sleep that rounds up.
     **letters' help capture was its tty refusal ("where are you?")**, and
     the gate accepted it: a program that checks isatty(0) cannot be asked
     for help by helpcap.  Its help entry is none, with the options in the
     note.  Read a new capture, not only the gate's verdict.
     **printf prints NOTHING to an unbuffered stdout here** (measured: fputs,
     putc and write do; printf and fprintf do not).  setbuf(stdout,0) is
     common in old games -- kalah's output was rows of repeated punctuation.
     Leave stdout buffered; a terminal still shows a prompt before the read.
     **A raw write() to a terminal gets NO line feed here.**  Measured with
     one program printing both ways: write() arrives as `x\r' per line and
     every line lands on the one before it; fputs() arrives as `x\r\n'.  To a
     FILE the write() bytes are right, so a data test passes and only a
     terminal capture shows it -- smiley (0b8de539) shipped with a smeared
     card and was fixed by routing its write macros through stdio
     (bd05465d).  Look at a card, not only at the gate.
     **A function returning char, called undeclared, is garbage above the
     low byte on the 68000** -- kalah's Pigeons totals read 661522 for 18.
     Code from a 6809 compiler relied on it; declare the function.
     **smiley and yidslots ship as posted (0b8de539, 4def3472).**  rdoggett,
     2026-09-15, on smiley's uncensored face list: "If we censor any of it, we
     are positioning ourselves as moral police.  I say take it as it is, or
     reject it in whole."  That answers FOR-RDOGGETT 24, which is gone, and it
     freed yid-slots, held for the same reason.  Both were read in full first:
     what is in them is in notes/PLAN-acquisitions and the session log.
  2aa. **xfmt ported (db77304e) -- and the flex findings are general.**
     comp.sources.unix v16i071, a formatter that also sets nroff -man
     pages.  It was deferred as "needs a patched flex skeleton"; that was
     wrong.  **The post's flex.skel.diff is already in this disk's
     skeleton** -- flex.skel is version 2.16 and carries both halves,
     `static int yy_start = 0' and `if ( ! yy_start ) yy_start = 1'.
     Check the skeleton before believing a post's patch instructions.
     Three things this flex DID want, each measured with a four-line
     probe rather than guessed:
     (1) **a comment starting in column 1 of the rules section is read as
     a rule** -- "unrecognized rule"; indent it and it is fine.  A comment
     inside an action block is C and is left alone (17 of 38 were flagged).
     (2) **{name} is expanded inside parentheses**, so a definition holding
     trailing context (`wh [ \t]*/[^a-z]') is illegal when used -- write
     the trailing context out in the rule instead (15 rules).
     (3) **yyin is null until the first yylex() ON THIS SKELETON** -- 2.16
     declares `FILE *yyin = (FILE *) 0' and assigns stdin inside yylex's
     init block -- so a program that does `freopen(name, "r", yyin)' in
     main() BEFORE scanning reopens nothing, scans nothing, and prints
     nothing with no error.  Give yyin stdin first.  **This is
     version-specific**: the os9-dev session's skeleton declares
     `FILE *yyin = stdin' and the same idiom works there (they checked
     2026-09-15).  `grep -n "FILE \*yyin" <skeleton>' tells them apart.
     stdin-only use hid this completely: the bug shows only when a file is
     NAMED -- the same shape as the line-buffering traps, where the
     convenient way to drive a program under test conceals the defect.
     **Four environment traps cost time tonight, all avoidable:**
     * `~/Developer/os9/os9exec' is the REPOSITORY; the binary is
       `~/Developer/os9/os9exec/os9exec'.  `[ -x ]' is TRUE for a
       directory, so mkimage.sh passed its own check and `mount -k' wrote
       no image, reported as "created no image at .../hz".
     * **rdoggett's ~/.zshrc EXPORTS OS9H0**, so any harness run that does
       not clear it mounts osk-freeware.dd as /h0 -- the one image
       harnesses must never touch.  Clear OS9H0 (and OS9H1) explicitly;
       run_in_session.py and datatest.py set them themselves and are safe.
     * **tools/ is HOST text, LF-terminated.**  The CR-only rule is for
       disk/.  Appending CR lines to tools/rebuild/recipes.psv corrupted
       three lines; it was caught by reading the bytes back, not by any
       check.
     * **rebuild.sh writes R_<prog> and .r files into the POOL**, so a
       recipe naming `../unixlib/getopt.c' leaves a MODIFIED tracked
       `disk/SRC/unixlib/getopt.r' behind.  Restore it and remove the new
       .r files before committing.

  2ab. **thricken ported (c9d4813d), and MY SHAR EXTRACTOR HAD A BUG --
     check ORIG against the post before trusting it.**  Every file I
     unpacked with the scratch extractor gained ONE BLANK FIRST LINE: the
     slice started AT the newline ending the `sed ... << MARKER' line
     instead of after it.  In xfmt (already committed, fixed in aba3dc8f)
     it was harmless and invisible -- flex ignores a blank line before
     `%{'.  In thricken it was FATAL and looked like a port bug: the level
     file's first line is the sprite filename, so load_level() read "",
     fopen("") failed, and the game printed `No such level' for data that
     was plainly sitting there.  I checked the chdir, the permissions and
     the file contents before checking my own extraction.
     **Re-extract and diff before believing a port is broken**: compare
     ORIG byte for byte against a fresh extraction of the post; all 29
     thricken files differed by exactly one leading byte.
     **Four shar dialects so far**, and one regex does not read them all:
     `sed -e 's/^X//' > file << 'END'` (redirect first), `sed "s/^X//"
     >'file' <<'END_OF_FILE'` (quoted name), `sed 's/^X//' << 'SHAR_EOF' >
     file &&` (marker first, trailing &&), and markers CONTAINING A DOT
     (`END_OF_FILE_xtail.h`) which a `[\w]+` marker pattern silently skips
     -- five of xtail's seven files were missed that way.  Always print the
     file count and compare it with the post's own "Contents:" list.
     **ansi2knr answers fewer ANSI trees than it looks like.**  thricken is
     ANSI throughout, and `KNR' converted NOTHING: the tool rewrites a
     definition only when the function NAME is at the left margin, and every
     one of thricken's sixteen writes the return type on the same line.  It
     never touches declarations either.  Count BOTH shapes before choosing
     the flag; 32 constructs here were a scripted hand conversion.
     **curses' cbreak() only sets a flag on this system** -- it does not put
     the terminal in character mode -- so stdio's getchar() still waits for
     a whole line in a curses program.  getch() is the read that honours it
     (chemtab reached the same place by a different route).
     Also measured for thricken: no kill() in this C library (getpid() is
     there), no sleep() (tsleep() counts ticks), no SIGTSTP/SIGSTOP, and
     getpwuid() comes free from the driver's own shim, answering with $USER.

  2ac. **craps ported (b54b5a4b).  Two library findings that will bite the
     next curses port.**
     **(1) printw() BUS-ERRORS on a floating-point conversion -- and printw
     ALONE.**  craps keeps every amount as a double and drew NOTHING, which
     reads like a curses initialisation fault, not a printf bug.  The trace
     is distinctive: last syscall a write, PC in a runaway zero-padding loop
     (`MOVE.B #$30,(A3)+` / `SUB.L #1,D5`).  Measured against every
     neighbour: printw("%d") is fine, and wprintw(), mvprintw() and
     mvwprintw() all render the same float correctly -- INCLUDING to stdscr,
     which is what printw is shorthand for.  So the defect is the wrapper.
     The fix is one line where a program's calls are uniform:
         #define printw(f, a)   wprintw(stdscr, (f), (a))
     craps' twenty-seven calls all pass one argument after the format, so
     the port differs from the 1987 posting by that define instead of a
     helper function and twenty-five edited call sites.  printw is variadic
     in general, so a program with a mixed call set needs sprintf()+addstr()
     instead.  The os9-dev session reproduced the abort on its own rig down
     to the faulting instruction pair.
     **(2) A PORT'S OWN HEADER SHADOWS THE SDK'S FOR THE WHOLE CHAIN.**  The
     recipe compiles with `-V=/h6/<tree> -V=/h7`, so the program's directory
     answers every `#include <name.h>` -- including ones issued from inside
     SDK and COMPAT headers.  craps ships a types.h; final.c included
     <sys/types.h> for nothing; COMPAT's sys/types.h does `#include
     <types.h>`; that found CRAPS' types.h, which includes <curses.h>; and
     curses.h HAS NO INCLUDE GUARD, so sgstat.h arrived twice and struct
     _sgs was defined twice.  62 errors, every one reported inside
     /dd/DEFS/sgstat.h -- a file the program never mentions.  I spent four
     probes on wrong theories (signal.h, then several sources in one cc
     line) before asking WHICH FILE triggered it: `main.c final.c` failed
     and `main.c subs.c` did not, which named it in two builds.  Check a
     port's own header names against DEFS and COMPAT first: types.h, time.h,
     stat.h and string.h are the collisions to expect.
     Also confirmed here: no link() and no crypt() in either library, and
     curses.l defines update() (the fourth name after setterm, abort and
     REFRESH that a game has to rename).
     **The deferred list is nearly empty.**  What is left is hodge-c (pipes
     frames to a display monitor -- the same coprocess problem as pac),
     banners (thirteen banner programs, three of them already here), and
     skewlife (build-time tables, low value).  The 135 usenet posts are all
     triaged.  CoCo/6809 remains, and is explicitly last.

  2ad. **banner1 ported (8d58010d) -- UNCHANGED, because it came from
     here.**  banner-01 of the `banners' collection (comp.sources.unix
     v26i141) is Wolfgang Ocker's 1987 program, and its own README calls it
     "the very first banner on OS-9/68000 ... one of the few programs that
     transitioned with me from OS-9/68000 to Unix".  The #ifdef OSK arms
     were still in the source and everything they call is in clib --
     _errmsg() (five programs here already use it) and intercept().  ORIG
     verified byte for byte against the posting; the port differs from it
     by nothing at all.  The other twelve are assessed in PLAN-acquisitions
     with a reason each: banner-04 IS the disk's `banner' and banner-05
     holds its `cursive', both confirmed by licence text rather than name.
     **A HOST VARIABLE CROSSES INTO os9exec ONLY IF ITS NAME STARTS WITH
     '@'.**  Found in os9exec's prepParams by the os9-dev session, measured
     here both ways: `TERM=zzz os9exec ...' is ignored silently and the
     process sees the seeded `dumb'; `@TERM=zzz os9exec ...' arrives, and
     `@USER=probe' likewise (USER is otherwise NULL without SYS/login).
     This corrects the memory that said the host environment never crosses.
     It also means a harness can hand a program TERM and TERMCAP without a
     login session at all.
     **DO NOT PROBE AGAINST `disk/' AS A HOST MOUNT WITHOUT CLEANING UP.**
     Running `OS9DISK=$PWD/disk os9exec -r bash' lets the emulated bash
     write `.bash_history' INTO THE TREE, and `no editor or host leftovers'
     then fails the gate.  It cost a gate run tonight.  Use a scratch image,
     or delete the file afterwards.
     **And read check_disk's EXIT STATUS, not the tail of its output.**
     `tools/check_disk.py disk 2>&1 | tail -31' printed a FAILED line and
     then `exit 0' -- the 0 was the pipeline's, not the checker's.

  2ae. **Three more 1990 IOCCC entries shipped (574622f1): dds, theorem,
     westley.**  All eleven are public domain under the contest's rule 5;
     seven were left after the earlier four.  dds is a BASIC interpreter in
     1536 characters -- it prompts `Ok', takes numbered lines, and RUN and
     LIST work; theorem is Best of Show, a Runge-Kutta solver that reaches
     e and is also a reversing filter; westley is Best Layout, a daisy
     picked petal by petal from source written to read as a letter.
     **READ THE PACKAGE'S OWN MAKEFILE BEFORE CALLING A CHANGE TOO
     INVASIVE.**  I had written westley off in the plan as unshippable,
     because making it compile meant reformatting source whose PRIZE WAS
     ITS LAYOUT.  Wrong: the contest's own common.mk builds that entry
     through exactly the three sed substitutions I thought I was inventing
     (`s/signed//', `s/1s/1/g', `s/^<tab>#/#/'), and does the same for
     scjones's trigraphs.  A transformation the authors ship in their own
     build is sanctioned, not damage.
     **And its last error was mine.**  westley failed on an undeclared
     identifier which turned out to be `stdout': the file has no
     #include <stdio.h>, and I had added a putchar-through-fputc macro.  I
     read the entry's scoping for a cycle before looking at my own line.
     Two library facts worth keeping: dds's arrays come to 65,694 bytes and
     needed `remote' (l68: "non-remote data allocation ... exceeds 64k"),
     and theorem declares its globals TWICE on purpose -- that is how one
     source compiles as four programs -- so the second set is extern here.
     **The four not shipped, each measured:**
     dg relies on the preprocessor expanding the DIRECTIVE NAME (`#define d
     define', then `#d name(x) ...' sixty times), which standard C does not
     do.  Writing them out as #define gets further and still fails: cc runs
     and exits having written nothing, no diagnostic and no module -- the
     silent cpp death of notes/CPP-MACRO-CRASH.md.  Its author predicts it
     ("defines nested too deeply").  OSK/dg.c is kept with the rewrite so
     the next person starts where I stopped.
     pjr: cpp aborts (E_PRCABT) while READING it; its hint warns compilers
     run out of temporary value space on the call chain that is the entry.
     tbr: a working shell in 550 characters, built on fork(), pipe(),
     execvp() and wait() -- none of which exist in this C library.
     stig: the C file is three bytes; the entry is a csh aliasing trick,
     and the judges said that type would not be permitted again.
     **What is left unopened:** the nine CoCo Community Archive zips under
     Scraped/acquisitions-2026-09-11/os9/community/cca (Sled, Tree,
     Filters, Wildcard Commands, Bob Van der Poel's PD programs, OS-9 PD
     Utilities and three more).  The c09_ tree is assessed; the usenet
     posts are all triaged.  My earlier "~150 colorcomputerarchive zips"
     was wrong -- there are 29 zips in the whole pool and nine of them are
     that archive.

  2n. **ONE harness gap left; the first is FIXED (efe864e4, 2026-09-16).**
     tools/ansiscreen.py clamped the cursor at the last column, so every
     character written past column 80 landed on top of column 79 and the
     ones before it were destroyed.  It now does a DEFERRED wrap, the way an
     `am' terminal does.  Measured over all 274 stored play-test raws at
     each capture's own geometry: 26 render differently, 19 of them showing
     MORE (life 161 -> 1879 ink, because a full-width board was being eaten
     a row at a time), and the 7 showing less all trigger the wrap branch --
     that is the screen scrolling because the characters survive now.
     mz waited on this and is no longer blocked by it.

     **Consequence, and it is the expensive half: every published screen was
     rendered AT CAPTURE TIME with the clamp.**  screenshots.py keeps no raw
     stream, so a card can only pick the fix up by being re-shot; and the
     play-test screens cannot be re-rendered from their stored raws either,
     because the `snap' offsets are byte positions taken live during the run
     and are not persisted -- only .screen.txt and .control.txt could be
     rebuilt, and gen_screens' pick() publishes whichever label has the most
     ink, so a half-refreshed set puts fresh screens in competition with
     stale snapshots.  Both pipelines must be RE-RUN.  20 programs are
     affected and have published screens; panel-backlog.txt holds none of
     them, so the ratchet should not move.

     STILL OPEN: playtest.py's `expect' searches the RAW stream on purpose
     (orbit's scrolled header), so a program that prints the right words
     onto a garbled screen PASSES -- TOP's moria passed on `Warrior' with
     the screen in column 80.  Read the snapshots.
  3. System utilities on the same list (aprocs cpu devprc vc top sysmon):
     probe for case material.

## 2026-09-14 (night): cases for the programs that had none

Five new families and eleven cases added to utils, each asserting what the
program PRODUCED and each shown failing on a deliberately wrong expectation
first: `amusements` (e2ef11d6), `games3`, `games4`, `netpbm6`, `system6`.
Worth knowing from them: cwasm rebuilds the shipped GAMES/COREWARS/imp.e
byte for byte; advcom compiles the ADVSYS sample and advint plays it; adlrun
plays AARD to its score line; almanac's figures are floating point, so its
case also guards the X-flag fix; unc disassembles pri to 1694 lines.

**Measured after them, `--all` on an image freshly built from `disk/`:
782 of 785** -- exactly the three deliberate failures (zip, todos, sir).
The bench, news and tail families each restart once after a case that
takes the session down; the restarts re-run setup and every case passes.

`tools/worklist.py --programs --no-test` is down to 91.  What is left is
mostly NOT datatest material, and each group was probed before being set
aside:
  * full-screen programs (animal, hang, tttt, bog, crib, saa, othello,
    hexa, lander, corewar's map, ...) want a terminal; `drive.py` sheets are
    their instrument, not case files.
  * re-ask forever at end of input, so a case would hang its family for 300 s:
    poker, blackjak, jotto, mastrm, monop, hinterhalt.
  * hang with no output: lmail, hist, vtxtcn (vtxtcn wants world's .dat
    files beyond q1text.dat).
  * `**** Stack Overflow ****` on piped input: gnugo (after its banner and
    board, fed `0', `b', `pass') and sdb (after a `q' it calls a syntax
    error).  Not chased; not known to be os9exec.
  * a datatest runs with NO PATH: a bare `printf' in a `run' line is
    `command not found', and a program reading that pipe then waits
    forever.  That is what hung the first games3 run -- use /dd/CMDS/printf.
  * the disk's `tail' takes `-30', not `-n 30'.

## 2026-09-14 (evening): every card states its terms and requirements

rdoggett: *"You must note on each card it's requirements, copyrights,
whatever."*  Done for every catalogued program:

  * `tools/terms.psv` -- name|terms|where recorded, all 998 programs; the
    backlog file is empty and gate `every card states its terms` keeps it so.
  * `tools/requires.psv` -- name|requirement|where, for what no scan sees.
    Its trap-module lines were MEASURED with `tools/probe_trap_needs.sh`:
    sixteen programs ask for csl, basicwin and xengine then for X11R6shl,
    g and striche for graph, rxmod for vmod_trap -- all on the disk.  The
    program-name gate reads the file (25dcacaf only claimed that; 2a42b5a3
    did it, shown failing on a bogus name first).
  * Cards list cio for starred programs and every requires.psv line under
    Needs; a card with no terms line would say "not yet looked up".

How: package licence files; research passes over every SRC tree, DOC
directory, binary and pool archive, each line with file and line; every
flagged restriction checked against its file.  SOURCES.txt was wrong more
than once -- smallutils, the DESIGNA VLT utilities, basename/dirname and
emacs had "public domain" or "freeware" with nothing behind them -- and
those entries are corrected.

Also fixed on the way: atp is a QWK mail reader, not the KA9Q AX.25
transport; SetTerm's readme sat in DOC/mines; SOURCES.txt listed wysetime as
removed; EFFO-INFO said i_am_i is not on the disk; README-MODULES and
SOURCES.txt still called the soft-float math imprecise.

The 32 card lines whose "public domain" or "freeware" rested on SOURCES.txt
alone were re-checked: 16 held, 9 were wrong (cal is shareware, beav and
emacs.mm1 non-commercial, sh and cat only "licensed free of charge", aprocs,
hexedit, lha, dirname a bare copyright), 7 state nothing.  Cards and the
SOURCES.txt entries are corrected; screen's entry also called it a terminal
multiplexer (it is Screens).  tools/probe_trap_needs.sh was run end to end
and agrees with the manual sweep (20 needing a module); it now names Graph.

The rest of the card lines resting on SOURCES.txt alone were re-checked too:
of 76, 39 held and 32 were corrected -- ckermit's Columbia no-sale notice,
zip's "not sold for profit", larn's "Copying for Profit is Prohibited", gs33
under the Aladdin licence not the GPL, no GNU licence travelling with bash
or less 290, makeinfo under the GNU Emacs licence, fuller BSD and GPL text
elsewhere -- and kermit states nothing.  SOURCES.txt's own entries for those
eleven, and dvi2tty's "no licence text" (its source says non-commercial),
are corrected as well.

Requirements measured further: probe_trap_needs.sh takes BASE_MODULES, and
run with math and math881 withheld it found 18 programs needing Microware's
math (lunisolar and spline print the name as "A"; confirmed by running them
with math supplied).  It sees only STARTUP needs -- bm names math and starts
without it.  CLAUDE.md (local) now says csl edition 25 has shipped since
2026-09-04; csl020 is still 15.

A recipe is not proof of what ships.  `recipes.psv` builds less, lessecho
and lesskey from SRC/less/less_332 (version.c: "332"), but CMDS/less is the
binary from the initial import and answers `less --version' with "290"; it
was never replaced by the recipe's output, and the lessecho/lesskey cards
cite other archives too.  src_census counts all three as recipe-built.
Before quoting a program as "built from SRC", run it and compare.

Still open:
  * FOR-RDOGGETT 16-17: eight DOC directories hold another program's document,
    and k, xy and z ship binaries their licence ties to source.  Earlier note: DOC/bm (Bdale
    Garbee's MS-DOS mailer; bm is a Boyer-Moore grep), DOC/dump (a
    terminfo dump), DOC/join and DOC/uniq (Gregorie's programs, not the GNU
    binaries), DOC/whoami (UUCP's page; the binary is GNU's).  None of the
    documented programs is on the disk.  Their cards point at the wrong
    manual.  Nothing moved yet.
  * FOR-RDOGGETT items 8-15 are the licence and authorship questions;
    nothing was removed or rebuilt.

## 2026-09-14: perl 4.036 is in, and os9exec's floating point was wrong

**perl** (471a003c): `CMDS/perl`, `LIB/perl`, `DOC/perl` (man page as text,
words.pl for the card), `SRC/perl4` with `README-OSK` and `osk.diff`;
recipe `perl`, card in languages.sheet, `tools/datatests/perl.cases` 7/7.
perl's own t/ suite passes file by file except what wants /bin/rm, ./perl,
tr, ln, touch or fork.  Not done: rmdir (OS-9 has no call for it -- would
be clear the dir attribute and delete), mkdir on an existing name answers
E$FNA rather than E$CEF, and x2p (a2p, s2p) is not built.

**os9exec never set X after NEG or NBCD** (notes/os9exec-bugs/X-FLAG.md).
Microware's software doubles depend on it: 1.0-1.0 was -2^-20 and exp(1)
right to six places.  Fixed and reviewed on os9exec `fix/scf-pd-eor`
(209b35c, tests d819c40 + d56b1bd), not pushed.  **rdoggett: while an
os9exec Claude session is active, report emulator bugs to it with a repro
-- never edit or commit in that repo from here.**

What the bug had put into this repo, corrected: DOC/README-FLOATINGPOINT
("math.l is single precision" -- it is not); gawk "ignores a filename
argument" (it reads files; case, howto, INDEX, card); savage's result and
pnmrotate 90's size in their cases.  dbz works too, from the earlier RBF
EOF-lock fix (21d5759): flagged.cases rewritten.

**Open:**
  * The seventeen published cards with floating-point output are reshot
    (68c19815): savage, sqrtx, config and both ephems changed for real;
    almanac, lunisolar, dvitype and rayshade only by date or timing.
    config's card now ends with os9exec's own `# No more memory' lines
    from its malloc probe -- announced by design, then tallied (os9exec
    make test asserts it) -- which a reader may find odd.
  * Full datatest on a fresh image after all of the above: **748 of 751**
    -- exactly the three deliberate failures (zip, todos, sir).
  * The CI workflow pins os9exec; bump it once those commits are pushed.
    CI runs check_disk and the image build, not the datatests.

## 2026-09-13 (late): the collection as a HOST DIRECTORY -- dogfooding os9exec

rdoggett's expectation, and now a standing target: unpack the tree into an
empty host directory, name it as both `OS9DISK` and `OS9H0`, and everything
works in os9exec except what makes no sense on a host dir (`free`-like
programs).  Failures there are to be ROOT-CAUSED AS os9exec BUGS, not written
off.  He also withdrew the tar as a second download (456437fe): the image is
the one download; unpacking is a test arrangement, not a distribution.

**How to run it.**  `python3 tools/mktar.py disk <x>.tar` (mkimage no longer
leaves one), `tar -xpf <x>.tar -C <empty dir>` (the `-p` keeps the public
write bits), then `datatest.py --all --image <that dir>`.  A directory takes
several concurrent os9exec sessions safely; an image does not.

**macOS, os9exec d318661: 726 of 743 on the directory, 740 on the image.**
The fourteen directory-only failures, every one traced with `-r -d 2`:

  * SEVEN were ONE os9exec bug, FIXED in os9exec a211ea4 (fix/scf-pd-eor,
    unpushed): a mode-0 `I$Open` on a host dir has no host stream, and
    `SS_Size` did `fstat(fileno(NULL))`; segv_handler turns the host
    SIGSEGV into the guest's E$BusErr.  zip, zipinfo, unzip, zipsplit's
    zipinfo, mv, texidx (+ rm-removes, which only rode on mv).  Verified
    from outside by building a211ea4 from `git archive` and rerunning
    archives/files/tex: 68 of 71.
  * FOUR rename by WRITING A 32-BYTE ENTRY into a directory opened `$83`,
    which a host dir refuses with E$BMODE: `mv` (it reaches this once the
    SS_Size fix lets it past), `move`, `wndex` (C-library rename()) and
    `upperdir`, which then retries forever because it never checks the
    error -- that was the "4 MB of spaces" flood, NOT case-insensitivity.
    Filed on os9exec's ROADMAP-68k as translating a name-only entry write
    into a host rename.
  * `combine` creates with attribute byte 0; on a host dir that becomes
    host mode `----------`, unreadable, where RBF lets the super user read
    it.  Filed with the above.
  * THREE make no sense on a host dir: `dinfo`, `freeb`, `dam` (sector 0
    and the allocation map).  Expected, and the only ones that should stay.
  * `patch` fails on BOTH, at different points -- not directory-only.

**And one RBF-IMAGE bug the comparison exposed: `dbz`'s "store failed" is
os9exec, not dbz.**  On a host dir dbz stores fine.  On the image a read of
the just-created, empty history.pag returns E$DEADLK.  FIXED in os9exec
21d5759 (fix/scf-pd-eor, unpushed).  The mechanism, as instrumented by
os9exec-d9 -- and NOT the stale-ring theory first sent from here: an
update-mode open resolves its pathname THROUGH the path being opened, the
walk reads the directory to its end and takes the DIRECTORY's EOF lock,
and RingJoin moved the path onto the file keeping it.  So every update
path started life holding its file's end, and dbz's two update opens of
history.pag deadlocked each other ("the writer is us").  `flagged.cases`
asserts "store failed" as a dbz defect: it flips once the harness's
os9exec includes 21d5759, and the case must change in the same commit as
that move -- not before, or it fails against the os9exec in use.
Verified from here: 21d5759 built from `git archive`, `flagged.cases` on a
fresh image is 7 of 8 with exactly that case failing ("store failed"
missing, no E$DEADLK anywhere in the capture).  One thing to look at when
the case is rewritten: `dbz -c` still reports "can't find" the record it
has now stored -- the case expects that line too, so it still matches, but
a store that succeeds and a lookup that cannot find it may be a second
defect, in dbz or in os9exec.

**Linux (Ubuntu 24.04 container, os9exec d318661 built from `git archive`,
tree unpacked INSIDE the container so the host filesystem is
case-sensitive; container runs as root):**

    RBF image           737 of 743   (macOS 740)
    unpacked directory  725 of 743   (macOS 726)

  * **The three extra image failures are ONE Linux-only os9exec bug, and
    it reaches our RELEASE IMAGE.**  The Linux build runs every pathname
    through `include_2e` (utilstuff.c, `#ifdef linux`, since the 2002
    sources) -- netatalk's convention of storing a host file `.x` as
    `:2ex` -- and applied it to OS-9 pathnames on RBF images too.  So
    `/dd/.newsrc` is looked up as `:2enewsrc` (E$PNNF: ELM's newalias,
    `cat /dd/.newsrc`, UUCP unsubscribe), and a dot-file CREATED by a Linux
    build lands in the image as `:2ename`.  **Our CI builds the image on
    ubuntu-latest, and the collection's own `tar` creates `.bashrc`,
    `.newsrc` and `.ELM` while filling it** -- a CI-built image would carry
    them misnamed, and the workflow's "read the image back" step would not
    notice.  FIXED in os9exec 4d26520 (respelling kept for host file names
    only; RBF opens and chd use a new EatBackOS9).  **Before any release:
    bump the CI's os9exec pin to 4d26520 or later, and add a read-back of
    `/dd/.newsrc` to the workflow so it cannot recur silently.**  Rebuild
    any image a Linux os9exec wrote before the fix -- its dot-files are
    literal `:2ename` entries and stay that way.
    Tonight's os9exec commits, in order, all on fix/scf-pd-eor and
    unpushed: d318661 (paced /tN output held), a211ea4 (mode-0 host dir),
    21d5759 (dbz E$DEADLK), 4d26520 (Linux dot-names).
  * **Case-insensitive lookup WORKS on a Linux host directory** --
    `/dd/SYS/MOTD`, `/dd/sys/motd`, `/DD/SYS/motd` and `whereis -b GEN`
    all resolve.  rdoggett doubted there were case issues; he was right.
  * Directory failures: 16 are common to both platforms.  Linux-only:
    `last3`'s ci case is TIMING (it needs the clock not to advance between
    two check-ins; the slower container crossed a second) and
    `whereis-ignores-case-as-RBF-does`, whose capture ends at its marker
    with no `@@CASE@@end` although the command takes one second.  SOLVED:
    NOT case, NOT lost output -- the harness runs from the repo, which in
    the container is a slow read-only bind mount of the macOS directory,
    and os9exec's START DIRECTORY evidently gets touched during host-dir
    walks: the identical generated script on the identical fresh tree,
    every device named by variable, exit 0 both times, took 11 s with cwd
    on container-local disk and 407 s with cwd=/repo.  That blows the
    family's 300 s gtimeout and cuts off whichever `whereis` is running
    (three reruns failed different whereis cases).  Sent to os9exec-d9 as
    a performance lead.  FIXED in os9exec b77cc22 (every lookup was probing
    all 35 device letters beside cwd -- ~280 failed host calls a scan) and
    confirmed from here: the same family from cwd=/repo now takes 3 s and
    2 s, all three whereis cases pass, end marker present.  On an os9exec
    older than b77cc22, `cd` somewhere container-local before `datatest.py`.
    macOS-only: `combine`, and only because the container runs as root,
    which reads a mode-000 file regardless.  Run as a user, Linux would
    fail it the same way.
  * `dbz -c` reporting "can't find" a record it has stored is dbz's own
    behaviour, identical on image and host dir (os9exec-d9, checked on
    21d5759); an untested guess is that it wants tab-separated history
    fields where the case writes spaces.

`CLAUDE.md`'s rule that bash's `[ -f ]`/`[ -d ]` fail on host dirs is stale
and was corrected: both answer true on `/dd` and `/h5` as host dirs.

## THE FIRST MOVE, 2026-09-13 (end of session)

Everything below is committed and the tree is clean.  Two things want
rdoggett and are in `notes/FOR-RDOGGETT.md`.

**The tex-driver thread is CLOSED (9cdb0577), and it was image state after
all.**  The explicit 57-file list and `--all`, run side by side on two
fresh images, both gave 728 of 743 with identical failures -- so `--all`
was never the variable and nothing flapped.  Then the capture was READ:
every driver said `can't open [/dd/story.dvi]`.  `tex.cases`' setup
passed `'\\input ... \\end'` in single quotes, bash kept both backslashes,
TeX stopped at `Undefined control sequence`, and no story.dvi was ever
written.  The drivers passed whenever `text.cases` -- which sorts AFTER
`tex` -- had left one on the image from an earlier run.  Proved both ways
before the fix: tex alone on a used image, 3 drivers PASS; on a fresh
image, 3 FAIL.  Fixed, and a fresh image now gives tex 17 of 18 (only the
stale `dvips` case).  Every earlier "not image state" conclusion in the
datatest section below rests on runs against `osk-freeware.dd`, which
had carried story.dvi all along.

**The lesson, cheaper than any bisection: read the `.raw` capture in
`notes/datatests/` for a failing case before theorising.**  The answer
was printed in it the whole time.

**Measured after the fix, `--all` on a fresh image: 731 of 743** -- the
nine stale cases listed below plus the three deliberate failures.

**The nine stale cases are updated too (2ac61f27)**, each rewritten to
assert what the program does NOW, with the old failure message kept as
an `absent` so it cannot quietly come back: `lua` prints its banner and
runs hello.lua; `runc` runs a script `luac -m -o` made into a module
(`-x` would write it into /dd/CMDS, so the case does not use it);
`msntp` now stops at "unable to allocate socket for NTP"; `dvips`
writes PostScript with `<tex.pro>` in three families; `dvidrivers`
finds cmr10 at 300 dpi; `about` quotes `Usenet`; `system5` runs
`unkeep`.  Measured on fresh images: the seven families 65 of 65,
`driven` 20 of 20.  Full `--all` on a fresh image after both commits:
**740 of 743** -- exactly the three deliberate failures.  The datatest
suite has no open thread.

**Do not** pipe a harness into `tail` and read `$?` -- you get `tail`'s.
**Do not** rebuild `osk-freeware.dd` while rdoggett has an emulator open
on it; build to another name INSIDE the repo (mkimage cds to the output
directory, and outside the repo there is no `bash`).  As of 2026-09-13
it no longer leaves a `.tar` beside the image: rdoggett withdrew the tar
as a second download.

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

**The archives are otherwise DONE, and the last lead closed as a
rediscovery.**  The "lost" RTSI archive turned out to be live -- moved to
microware.com -- and then to be the SAME corpus this pool inventoried on
2026-09-11, same download ids, zero new filenames.  Wayback is closed for
all thirteen dead OS-9 hosts (front pages only, the FTP trees were never
crawled).  What came out of the night's searching that is worth keeping
is small and specific: the archive's 321 KB master index, a 597-row fetch
manifest, and the name of its maintainer.  `notes/PLAN-acquisitions.md`
has all of it.  **Do not re-search these hosts.**

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

## A gate was blind to 69 files, and the published screens are TWO things

Found 2026-09-13 because an os9exec session asked whether any card had
been built around the pre-`985e0d8` RBF behaviour.  None had -- but the
asking turned up a hole.

**`check_disk`'s dots gate read `tools/{screenshots,datatests,drives}`
and never `tools/playtests/*.keys`** -- 69 files that type commands at
the disk and whose screens are published.  Widening the directory list
alone changed NOTHING, because the gate only inspects lines matching an
executable-directive regex (`try|os9|run|send|expect`) and a playtest's
command lines begin with `keys`.  Both had to change.  It then failed
naming `netpbm.keys:15`, the only chained `../..` in any scanned file.
**When a gate is widened and stays green, suspect the line filter, not
the file list.**

**And the two published forms are NOT the same set.**  `docs/screens.js`
is the gallery `index.html` reads and is keyed BY PROGRAM: a screen only
appears if some program's card claims it.  `docs/screens/*.txt` is a
mirror of EVERY screen, keyed by screen name, rewritten wholesale
(`shutil.rmtree`) on each `gen_screens` run.  So the mirror legitimately
holds screens no card shows -- `netpbm`, `netpbm-color`,
`netpbm-convert`, `hackquit` among them -- and a string in the mirror is
NOT necessarily published to a reader.  Checked here: 0 of the 887
screens cards reference is `netpbm`, and NO published card text contains
`../..`.

**Three of my own inferences died in that half-hour, all the same way.**
I read a commit date as staleness (those files are rewritten every run --
their mtimes all match `screens.js` to the second); I tested for a
playtest capture using the SHEET naming `<name>.shot.txt` when playtests
write `<name>.screen.txt`, and called it an orphan; and I reported "does
the published screen contain it? no" from a script whose input was an
empty string because the lookup above it had found nothing.  Each looked
like evidence.  **Check what a negative result was actually computed
from.**

**Playtest screens have no drift detection at all.**  `gen_screens
--check` compares each capture against its SHEET stanza hash; playtest
screens have no stanza and no hash, so a `.keys` file can be edited and
its published screen will keep showing the old command with nothing to
notice.  That is still open and is worth closing.

## The datatest suite: 727 of 743, and the disk has OUTGROWN NINE OF ITS TESTS

> **RESOLVED 2026-09-13 (9cdb0577) -- read "THE FIRST MOVE" at the top
> first.**  The tex-driver investigation below (position, bisection,
> `--all`, accumulation) was chasing a setup line that never produced
> `/dd/story.dvi`; the drivers passed only on images where `text` had left
> one.  Its "not left-over image state" conclusions are WRONG.  The
> nine stale cases it lists are all updated as of 2ac61f27.

Run whole for the first time in a while, 2026-09-13.  **16 failures, and
so far NINE of them are cases asserting a failure that a later commit
FIXED.**  None is a regression; the collection got better and the tests
were not told.

`notes/PLAN.md` records the baseline: 420 of 423 on 2026-08-31, with
three deliberate failures.  Those three still fail and are still
deliberate -- `zip-cannot-write-its-archive`,
`todos-must-change-the-file`, `sir-round-trip-is-lossy`.  The rest
accumulated AFTER that baseline, as capabilities landed:

  **The csl three.**  `9befb924`, 2026-09-04, "Runtime: ship csl edition
  25 -- **fixes lua, runc, msntp**".  It touched **ZERO** files under
  `tools/datatests/`.  `driven`, `lua` and `net` still expect `csl
  traphandler mismatch` from exactly those three programs.  The shipped
  `disk/CMDS/csl` is now byte-for-byte the SDK's 48,366-byte copy.

  **The dvips three.**  `e934210a`, 2026-09-12, "**dvips renders**, and
  the source for gawk, bison and dvips ships".  Also touched **ZERO**
  case files.  `tex`, `dvifont` and `dvidrivers` still expect
  `Couldn't find header file tex.pro`, and `dvifont.cases` still carries
  the comment "there is no .pro on this disk" -- there are SEVEN in
  `disk/SYS/TEX/DVIPS/`.

  **One font case by date.**  `a02d284c`, 2026-09-05, shipped the
  Computer Modern fonts at 300 dpi and DID update `tex.cases` -- but not
  `dvifont.cases` (last touched 09-01) or `dvidrivers.cases` (09-02).
  `dvidrivers` still expects `Font file [cmr10 [300 dpi]] could not be
  opened`, and 17 PK300 fonts ship.

  **`about`** expects the origin phrase `from  usenet archive  fortune.ar`.
  `DOC/ORIGINS` says `Usenet` now -- the old phrasing appears ZERO times.

  **`system5`** runs `/dd/CMDS/drop`.  `drop` was RENAMED to `unkeep` on
  2026-09-09 and there is no `drop` on the disk.

**THE FOUR WERE SETTLED BY RUNNING THE SUITE TWICE, and the controlled
comparison is the whole value of it:**

    the image I had been working on   727 of 743
    a PRISTINE image, same commit     728 of 743

**Exactly one case differs: `games2 convert-starts-the-world-adventure`
fails on the worked image and PASSES on a clean one.  That one was MINE**
-- a scratch diagnostic ran `vtxtcn' with the data directory at
`/dd/GAMES/WORLD', which writes `.inc' tables beside the game's data, and
`convert' reads that directory.  Nothing was committed and the source
tree was untouched; the damage lived only in the built image, and a
rebuild clears it.

**The other three are REAL and are not mine**: `tex`'s `dvialw` and
`dvilj2` (`[1 pages]`) and `dvieps` (`nearest neighbor`) fail identically
on a pristine image.

**THEN THEY WERE RUN BY HAND, AND ALL THREE WORK.**  Against the same
`/dd/story.dvi` the harness uses, each prints the exact string its case
is looking for:

    dvialw   [PostScript [Apple LaserWriter laser printer]]
             [Output on file /dd/story.dvi_alw]   [1 pages]   [1{1}]  [OK]
    dvilj2   [Hewlett-Packard LaserJet II laser printer]
             [Output on file /dd/story.dvi_lj2]   [1 pages]   [1{1}]  [OK]
    dvieps   Font file [cmsl10 [240 dpi]] could not be opened.
             ---using nearest neighbor [...pk300/cmsl10.300pk [300 dpi]]
             instead.                              [1{1}]  [OK]

So **the programs are not broken and the cases are not wrong about what
they print** -- the strings are there.

**AND RUN ALONE, THE FAMILY PASSES: `datatest.py tex.cases` is 17 of 18,
with only the known-stale `dvips` case failing.  All three drivers
pass.**  So they fail ONLY in a full `--all` run.  It is not the
programs, not the cases, not the family's own ordering, and not
left-over image state (a pristine image fails them too).  **An earlier
FAMILY changes something they depend on.**

**The obvious candidates were tested and are NOT it.**  `dvidrivers` and
`dvifont` both sort before `tex`, both render the same `story.dvi`, and
both build `cmr10` at other resolutions on purpose -- so a driver finding
a 240dpi font where it expected 300dpi looked like exactly the right
shape.  Run together in `--all` order, `dvidrivers dvifont tex` gives
**23 of 27 and all three drivers PASS**; only the four stale
`tex.pro`/font cases fail.  `tex` alone straight afterwards is 17 of 18,
unchanged.  So it is not those two families.

**THE PROBE WAS RUN AND THE ANSWER IS POSITION.  These failures are not
about which programs they are; they are about how LATE the family runs.**

    whole suite, alphabetical   728 of 743   tex's three drivers FAIL
    whole suite, tex FIRST      728 of 743   tex's three drivers PASS
                                             -- and `last' and `misc'
                                             fail instead, having passed
                                             in every earlier run

Same total both ways.  Move `tex` to the front and its three drivers come
right, while two families that had always passed start failing.  The
failures MOVE to whatever is late.

**And they are all write failures.**  `misc` fails missing `/dd/tmp/mv1`;
`last` fails missing an elm helper's reply; `archives` fails FINDING
`Could not create output file`; and a DVI driver that cannot write its
output file prints no `[1 pages]`.  That is one symptom wearing four
names.

**THE OBVIOUS CAUSE IS WRONG.  THE DISK IS NOT FULL.**  Measured
immediately after a full 743-case run by reading the RBF allocation
bitmap out of the image host-side -- no emulator, no `free` (which this
disk does not carry):

    DD_TOT 1,134,592 sectors of 256 bytes, DD_BIT 4 sectors per bit
    allocated   149,779 clusters   146.3 MB
    FREE        133,869 clusters   130.7 MB

Nearly half the disk is empty at the end of the run.  So whatever the
late families are losing, it is not space.

**BISECTED TWICE, AND THE SIGNAL IS STABLE.  The threshold is between 41
and 53 families ahead of `tex`.**

    28 families then tex     314 of 325   all three drivers PASS
    28 families then tex     314 of 325   REPEAT, identical total
    41 families then tex     501 of 515   all three drivers PASS
    48 families then tex     582 of 596   all three drivers PASS
    50 families then tex     619 of 634   all three drivers PASS
    52 families then tex     687 of 702   all three drivers PASS
    all 57, tex FIRST        728 of 743   all three drivers PASS
    `datatest.py --all'      728 of 743   all three drivers FAIL

**THE BISECTION DID NOT CONVERGE -- IT REFUTED ITSELF, and that is the
finding.**  EVERY arrangement built from an explicit list of case files
passes, up to and including 52 families ahead of `tex` and all 57 with
`tex` first.  The only thing that fails is `--all`.  So the variable is
NOT how many families run first, and NOT which ones: an earlier draft of
this section concluded "the culprit is one of `system4`, `system5`,
`tail`" and that is WRONG -- 50 and 52 both pass, which brackets all
three of them.

**So the next move is one run, and it is not a bisection.**  Give
`datatest.py` an EXPLICIT list of all 57 case files in alphabetical
order -- the same set and order `--all` builds for itself -- and see
which way it goes:

  * if it PASSES, `--all` differs from its own file list in some way
    (how it enumerates, orders, or sets up), and the bug is in
    `datatest.py`, not in any family;
  * if it FAILS, then something about the full 57-family SET matters
    that 52 does not, and the search resumes between 52 and 57.

Either answer is worth more than another bisection step.  Matched-state
proof that this is not the image: the FIRST full run tonight was
alphabetical on the worked image and failed all three; `tex`-first on
that SAME worked image passed all three.

**One arithmetic trap to avoid repeating.**  `tex` is 52nd of the 57, so
"the first N families" and "N families before tex" agree only while
N < 52; a loop taking the first N NON-tex files in glob order starts
pulling in families that normally run AFTER `tex` (at N=52 it adds
`text`), building an ordering the real suite never has.

**One caveat, and it may undo the neatness.**  `last` FAILED in this
bisection and in the tex-first run, and PASSED in the pristine full run
-- with the identical set of families ahead of it in each case.  Same
preceding conditions, different answer, which is the signature of
NON-DETERMINISM rather than position.  Four families take a session
restart (`bench`, `maths`, `news`, `tail`) and a restart's timing is not
reproducible, so some of this may be flap.  **Before bisecting further,
run the same arrangement twice and see whether it answers the same way.**
A bisection over a flaky signal will converge on nonsense.

**The rest of what is ruled out, which is worth more than another
guess:** not the programs (all three drivers
work run by hand), not the cases (they pass when their family runs
alone), not left-over image state (a pristine image fails them too), not
a neighbouring family (`dvidrivers dvifont tex` together is 23 of 27 with
all three passing), and not disk space (above).  What is left is
something the emulator or RBF accumulates across 57 sequential sessions
-- path descriptors, module memory, directory size (`/dd/tmp` ends a run
holding 318 entries) -- and NONE of that has been measured.  Measure
before writing the next explanation into this file; three of mine were
wrong tonight.

**How to read the bitmap**, since it is the only free-space instrument
here: LSN0 holds DD_TOT at 0..2, DD_MAP (bitmap bytes) at 4..5 and
DD_BIT (sectors per bit) at 6..7; the bitmap starts at LSN 1 and a set
bit is an allocated cluster.

(`games2` fails in a tex-first run only because that run used
`osk-freeware.dd`, which still carried the `/dd/GAMES/WORLD` pollution
from my own scratch diagnostic.  On a pristine image it passes.)

**A WRONG LEAD, REMOVED:** an earlier draft of this section said
`/dd/story.dvi` is 668 bytes while a passing case is called
`the-dvi-is-1704-bytes`, "so the two are not the same file". They are not
supposed to be: that case measures `/dd/small.dvi`, from the LaTeX case
above it. Nothing there. It was written from the case NAME without
reading the case.

**The method worth keeping: run the suite against a FRESH image built to
a different filename.**  `tools/mkimage.sh disk fresh.dd` then
`datatest.py --all --image $PWD/fresh.dd`.  Two traps in that one line:
the script **cd's to the output directory** (its own header says so,
because `mount -k` creates `<CWD>/hX` and ignores `OS9Hx`), so building
outside the repo puts the emulator somewhere with no `bash` and it stops
with `E_MNF: 'bash'` before emulation starts; and it writes `<name>.tar`
beside the image, which `.gitignore` does not cover for any name but
`osk-freeware` -- delete it, or leave a 130 MB stray behind.  **Do not
rebuild `osk-freeware.dd` itself to do this:** rdoggett keeps an emulator
session open on that exact file (`lsof` showed it held open, twelve hours
in) and `osk-freeware.tar` is the name his build uses.

**The rule this pays for: a commit that fixes a program must update the
case that asserts it broken, in the same commit.**  Two commits here
named the programs they fixed in their own subject lines and changed no
test at all.  A suite that is not run whole does not notice, and this one
had not been run whole in a fortnight.

**And run it with `gtimeout` on PATH** (`/opt/local/bin`), or
`datatest.py` dies with `FileNotFoundError` before a single case runs --
and capture its status in a variable, because piping it into `tail`
reports `tail`'s 0 and the failure looks like a pass.

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

## The CoCo survey's first port was WITHDRAWN, and the bar moved (2026-09-15)

`ffix' (Bob van der Poel, 1988) was ported off the "OS-9 Public Domain
Utilities" image, built clean, measured, catalogued -- and then taken back
out again before it shipped.  rdoggett, mid-flight: *"don't just port
everything from coco that you can, make sure it's a useful addition to us
and not overly color computer related."*

He is right and the port should never have started.  `ffix' expands tabs,
which `detab' and `expand' do; it turns every other control character into
a space, which `pep' -- "a file detergent" -- and `unp' do.  What was left
was nothing a reader could not already do.  Everything about it is reverted;
`notes/PLAN-acquisitions.md' records it as not a candidate so it does not
get re-ported.

**The test for the ~20 undescended Level 2 Library images is NOT "does it
compile".**  It is: write the one sentence saying what a reader can do
afterwards that they could not do before.  If that sentence names a program
already on this disk, or only makes sense on a Color Computer, record it as
not a candidate and move on.

Two technical findings are worth keeping even though the program is gone:

**A file header is a claim, not a measurement.**  `ffix' documents four
conversions and one of them cannot happen: `filecopy()' assigns
`lastc = c' at the TOP of its loop, so the previous character is never
retained, and the branch tests `c == '\l'', which is not a C escape
sequence.  Measured, the two bytes 0D 0A come out 0D 20 -- the LF becomes a
space like any other control character, never deleted.  Catalogue text
written from that header would have been wrong in a way no check here could
catch.

**Arming out the back half of a destructive sequence leaves the front half
running.**  The in-place path copies to a scratch file, `unlink()'s the
original, then renames the scratch over it via `system("rename ...")'.
Only the rename is impossible here, so that is what got the `#ifdef OSK'
arm -- and `ffix file' then deleted the file and stopped.  The test caught
it because it dumped the file afterwards rather than reading the refusal
message and believing it.  **Put the refusal before the first irreversible
step, and assert the artefact still exists afterwards.**

## The screen-corruption sweep: how to find the rest (queued behind the downloads)

rdoggett, 2026-09-16, on the ansiscreen clamp: *"if the bug that caused the
bad renderings is fixed, great.  fix the ones you know about and if you know
how to find others that may be corrupted, put finding and fixing them on your
todo list after wading through the rest of the downloaded stuff."*

So the ORDER is: the 20 known ones first (in hand), then the remaining
downloads, then this sweep.

**How to find them, two methods, one exact and one a filter.**

EXACT, for anything with a stored raw -- the 274 play-test captures.  Render
the raw with the current renderer and compare against the published screen;
any difference is a screen the clamp altered.  That is how the 26 were found,
and it cannot be fooled.

A FILTER, for cards -- screenshots.py keeps no raw, so there is nothing to
re-render and no exact test.  Use the necessary condition: the clamp could
only alter a screen if some line actually reached the right margin, so a
published screen is a candidate if it holds a line exactly as wide as THAT
CAPTURE'S geometry.  It over-reports and cannot miss one.

**Do not use a fixed width of 80.**  A first cut did and flagged 111 of the
967 published screens -- but `gothic' renders 96 columns wide and `calen'
131, so on those the test was asking the wrong question entirely.  Take each
capture's width from its sheet `size' directive (default 24 80), the way the
renderer measurement did, then re-shoot the candidates and keep the ones that
actually change.

Cheapest order within the sweep: run the exact method over every stored raw
first, since it needs no emulator time at all; only then re-shoot the card
candidates, which do.

## The clamp screen-sweep: FINISHED 2026-09-16 (this was the pause note)

**All seven resume steps below are DONE.  Nothing here is left to pick up.**
Both pipelines were re-run against a scratch image -- nineteen cards and the
same nineteen play-tests (19 of 19 pass, no orphaned escapes) -- gen_screens
republished, and SIXTEEN screens changed plus screens.js (78b2efdf).  life's
card had been publishing a nearly empty board and now renders its whole
80-column field.  audit_panels --gate is clean at 0 problems, the ratchet did
not move, check_disk is green on all 29, and the scratch image and its lock
are removed.  osk-freeware.dd was never touched.

**What is NOT done, and is the queue in rdoggett's order:** the rest of the
downloads -- 20 CoCo images, the only body left -- and THEN the sweep for any
other clamp-corrupted screens, whose method is in the section above.

The rest of this section is kept as the record of how it stood mid-way.


**Nothing is half-committed.**  The tree was clean at d53e39ce when this
paused.  `notes/playtests/' is gitignored and gen_screens had not been run,
so `docs/' is untouched and no partial state is in git.

**What is done.**  The ansiscreen clamp is FIXED and committed (efe864e4):
it now does a deferred wrap instead of destroying every character written
past the right margin.  Nineteen cards were re-shot against `sc-cb.dd' and
their captures are in notes/playtests/*.shot.txt.  Measured against what is
still published: life 205 -> 1852 ink (its card was showing about a ninth of
the board), gnuan +416, animal +176, shire +135, torus +118, perp +100; six
came back identical, so those cards were never affected; japan -22, wish -14
and yahtzee2 -6 are the scroll effect, which is the faithful result.

**What was in flight.**  A play-test re-run over the same nineteen .keys
scripts, launched with `--image sc-cb.dd'.  It may have finished, been
killed by the pause, or still be going.  Check before anything else.

**Resume, in this order.**

1. If a play-test run is still going, LET IT FINISH.  Never kill an emulator.
2. If it was killed, `sc-cb.dd.lock' is left behind.  imagelock reports a
   stale lock and never steals one, so remove it on purpose, then re-run:

       python3 tools/playtest.py $(for n in animal draw editor england gnuan \
         hexa hexedit japan life perp shire stone sysmon thricken torus \
         touchtype wisecrack wish yahtzee2; do echo tools/playtests/$n.keys; \
         done) --image $PWD/sc-cb.dd

   Both pipelines have to be refreshed together: gen_screens' pick() publishes
   whichever label has the most ink, so a fresh card shot competing with a
   stale play-test snapshot is worse than neither.
3. `python3 tools/gen_screens.py'  -- republishes docs/screens/*.txt and
   docs/screens.js.
4. `python3 tools/audit_panels.py --gate' -- the ratchet.  panel-backlog.txt
   holds none of these twenty names, so it should not move in either
   direction; if it does, read why before editing the backlog.
5. `tools/check_disk.py disk' -- read the REAL exit status.  Not through a
   pipe, and NOT with ${PIPESTATUS[0]}: that is a bash-ism and this shell is
   zsh, which silently gave an empty status here today.
6. Commit docs/.
7. `rm sc-cb.dd sc-cb.dd.lock' after an `lsof' check.  It is a scratch image;
   osk-freeware.dd is rdoggett's and no harness may touch it.

**CLAUDE.md is GITIGNORED and has never been tracked** (.gitignore line 20).
It is rdoggett's own local instruction file, so an edit to it is local only --
`git add' refuses it and no commit can carry it.  Do not try; say what changed
instead.  It was corrected on 2026-09-16 because it told a new session that
FOR-RDOGGETT held "currently nothing" when it held eighteen open items.

**The twenty affected programs**: animal draw editor england gnuan hexa
hexedit japan life perp shire stone sysmon thricken torus touchtype
wisecrack wish yahtzee2 zot.  thricken has no card stanza and is published
from its play-test capture; puzzle's capture changed too but it publishes no
screen, so it needs nothing.

**Then the queue rdoggett set, in his order**: the rest of the downloads --
20 CoCo images, the only body left (Level 2 Library 15, Filters 2,
Rdump/RayTrace 2, Wildcard 1; the other six are assessed) -- and only THEN
the corruption sweep, whose method is in the section above.  Expect most of
the twenty to come back "not a candidate": they are 6809 Level 2 disks, and
the bar is now what a reader can do afterwards that they could not do
before, not whether the source compiles.
