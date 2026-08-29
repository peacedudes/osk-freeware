# For rdoggett

Terse on purpose. Everything before 2026-08-27 is in git history.

Branch `release-pass-2026-08-21`. All eleven `check_disk.py` checks green.

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

## Look at this

`docs/screens.html` -- 16 programs photographed while running, linked from the
catalogue. Every screen came from keystrokes fed to a running program.

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

**You asked for pictures for the web pages. There are 400-odd now**, and
taking them found more broken programs than any sweep has. `docs/screens.html`
is the gallery; every program's own card in `docs/index.html` carries its
screen. Nothing is mocked up -- keystrokes went into a running program on the
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
    `sysmon` refuses os9exec's V4.0 as too old. `ssl` gets an empty segment
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

## Nothing needs you

