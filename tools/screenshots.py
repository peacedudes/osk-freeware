#!/usr/bin/env python3
r"""Capture MANY programs in ONE emulator session, one screen each.

    tools/screenshots.py tools/screenshots/text.sheet [...]
    tools/screenshots.py --all [--image osk-freeware.dd]
    tools/screenshots.py --all --only gnuchess,hexedit   # just those two

Why this exists beside `tools/playtest.py'
------------------------------------------
`playtest.py' answers "does this program read the keyboard and do its job",
and it pays for that answer: a fresh emulator per program, a control pass to
compare against, and a verdict. That is the right price for `tet' and it is
the wrong price for `today', which prints four lines and stops. At ~35
seconds a program, capturing the collection that way is a day of wall
clock for pictures nobody judged.

This drives a SINGLE bash session on a pseudo-terminal and runs stanza after
stanza in it, clearing the screen between, keeping the bytes each program
wrote and rendering just those into a fresh 24x80 grid. Eight programs cost
about ninety seconds instead of five minutes.

It judges nothing. The screens are for the catalogue, and a human -- or the
model driving this -- looks at them. What it DOES guarantee is that every
screen here came out of a running program on the real disk image: the bytes
are captured off the terminal, never composed.

A card is a science-fair stand: a browser who knows nothing about the
program should see at a glance WHAT IT DOES (the caption's first line and the
catalogue's purpose), WHAT TO TYPE (`try', short, no paths), and IT RUNNING
(a before/after in the capture), and only then, folded away, the detail.
Requirements the reader must supply -- data files, a GAMES directory, runb --
come from DOC/DEPENDS and show as `Needs'; cio is not one, it ships.

Sheet format (blank lines and `#' comments ignored):

    shot    today                  start a stanza; the program's own name,
                                   because that is how the catalogue finds it
    cap     Prints the date in ...  caption for the gallery (repeatable) --
                                   describe what the reader is LOOKING AT; do
                                   not restate the command or narrate the
                                   capture, the screen is the example
    try     today -l               the command the card shows as `Try it':
                                   what a reader types at bash or ksh, the
                                   program and its real arguments, no full
                                   pathlists.  Every stanza carries one; a
                                   bare name is right only for a program
                                   that takes no arguments
    os9     today -l               the same command at Microware's shell,
                                   when it differs (chd for cd, >- to
                                   overwrite, #32k memory, no $VAR, quoting).
                                   Omit it when the `try' line is the same
                                   at both shells.  Verify it with
                                   tools/os9try.py before writing it down
    burst                          capture this stanza UNTHROTTLED -- for a
                                   program that paints its screen in one
                                   burst and never repaints (backgammon's
                                   board), where the paced pty drops most of
                                   it.  `run'/`send' lines become the shell
                                   proc and the program's standard input;
                                   answer prompts with `send'
    fold                           fold a run of identical lines into one
                                   and a count -- for a program that floods
                                   one line; off by default, because ASCII
                                   art is made of repeated lines
    frames                         publish the stanza as a FILMSTRIP: one
                                   line per frame, top to bottom -- for a
                                   program that animates by rewriting one
                                   line with bare carriage returns (zot's
                                   letters dancing in).  A screen grid keeps
                                   only the last frame of that, which is a
                                   plain line of text; the strip keeps the
                                   dance.  Sampled evenly to fit the window,
                                   the typed commands always kept
    for     sysid getsys           which CATALOGUE programs this screen shows,
                                   when the shot's own name is not the only
                                   one -- the gallery hangs it on each
    run     /dd/CMDS/today         the command line typed at the shell
    wait    4                      seconds
    send    y\r                    keys, all at once (\r \e \s \t \003 ...)
    keys    hjkl                   keys one at a time, `rate' apart
    kill                           Ctrl-E now, BEFORE the screen is taken --
                                   how to capture the FIRST page of a
                                   program that prints for pages
    send    \023                   Ctrl-S: XOFF, the terminal stops where it
                                   is; `snap' then takes a still page of a
                                   program that scrolls, and `send \021'
                                   (Ctrl-Q) lets it go on.  rdoggett's tip.
    run     clear                  a `clear' inside the stanza starts the
                                   picture over -- setup lines typed before
                                   it are left out of it
    snap                           TAKE THE PICTURE HERE.  Without it the
                                   fullest moment of the stanza is kept,
                                   which is right for a program that prints
                                   and wrong for a game: touchtype's level
                                   menu has more ink than its playing field,
                                   so the menu was published.  With one or
                                   more `snap's, only those moments compete.
    rate    0.4                    seconds between `keys' characters
    size    24 80                  window size for the stanzas that follow
    quit    \033:q!\r              keys to leave the program politely, sent
                                   AFTER the screen is taken -- an editor that
                                   is still running would otherwise eat the
                                   next stanza's command line

Every stanza ends with Ctrl-E, which os9exec delivers to the last writer and
which kills a program however it is blocked. That is what makes it safe to
put an editor and a game in the same session.
"""
import fcntl
import hashlib
import os
import pty
import re
import struct
import subprocess
import sys
import termios
import threading
import time

# One writer at a time: all three harnesses write to the image itself.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import imagelock                                    # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
from os9env import emulator_env
import ansiscreen                                        # noqa: E402

OS9EXEC = os.environ.get("OS9EXEC",
                         os.path.join(REPO, "..", "os9exec", "os9exec"))
CAPS = os.path.join(REPO, "notes", "playtests")
SHEETS = os.path.join(REPO, "tools", "screenshots")

# THE ENVIRONMENT A PERSON ARRIVES WITH. SYS/login sets these; a program that
# wants one and does not get it fails in a way that reads as its own bug --
# `sokoban' stops with "cannot get your username" without USER, and `tttt'
# with "Unknown terminal type ''" without TERM.
LOGIN = ("export TERM=xterm-256color",
         "export TERMCAP=/dd/SYS/termcap",
         "export HOME=/dd",
         "export USER=tester",
         "export LOGNAME=tester",
         "export MAIL=/dd/SPOOL/MAIL/tester",
         "export PATH=/dd/CMDS:/dd/CMDS/GAMES:/dd/CMDS/NETPBM:/dd/CMDS/UUCP",
         "export PATH=$PATH:/dd/CMDS/TEXCMDS:/dd/CMDS/ELM:/dd/CMDS/COMMS",
         "export PATH=$PATH:/dd/CMDS/NETWORK:/dd/CMDS/NEWS:/dd/CMDS/WN",
         "export PATH=$PATH:/dd/CMDS/ADL:/dd/CMDS/REBUILT",
         "export PATH=$PATH:/dd/CMDS/DEMOS:/dd/CMDS/DHRY:/dd/CMDS/GCC139:.",
         # The reader's own OS-9, as SYS/login appends it: `load' and the
         # rest of Microware's commands come from there, not from this disk.
         "export PATH=$PATH:/h1/CMDS:/h1/CMDS/GAMES",
         "export TMACDIR=/dd/LIB",
         "export HELPDIR=/dd/SYS/HELP",
         "export SIMPATH=/dd/SBPROLOG/MODLIB",
         "export PEP=/dd/SYS/PEP",
         # SHELL MUST BE ksh, and this list said bash until 2026-08-31.
         # Programs that shell out reach system(), which forks $SHELL with the
         # whole command line as ONE ARGUMENT; ksh parses that and bash reads
         # it as a script filename. The `latex' card showed
         # E$PNNF because of this one word. SYS/login is the authority and
         # check_disk.py now fails if the two disagree.
         "export SHELL=/dd/CMDS/ksh")

ESCAPES = {"\\r": "\r", "\\n": "\n", "\\e": "\033", "\\s": " ", "\\t": "\t"}


def unescape(s):
    for k, v in ESCAPES.items():
        s = s.replace(k, v)
    return re.sub(r"\\([0-7]{1,3})", lambda m: chr(int(m.group(1), 8)), s)


def parse(path):
    """A sheet is a list of stanzas. `shot' opens one; the rest fills it."""
    shots, cur, rate, size = [], None, 0.4, (24, 80)
    for raw in open(path):
        # A `#' STARTS A COMMENT ONLY AT THE START OF A LINE. Stripping it
        # anywhere ate `lda #$41' out of an as09 stanza, and the shell sat
        # in continuation mode swallowing the three stanzas that followed.
        line = "" if raw.lstrip().startswith("#") else raw.rstrip()
        if not line.strip():
            continue
        word, _, rest = line.strip().partition(" ")
        rest = rest.strip()
        if word == "shot":
            cur = {"name": rest, "cap": [], "for": [], "acts": [],
                   "try": None, "os9": None, "fold": False, "burst": False,
                   "frames": False, "fresh": False,
                   "rate": rate, "size": size, "quit": None, "sheet": path}
            shots.append(cur)
            continue
        if word == "rate":
            rate = float(rest)
            if cur:
                cur["rate"] = rate
            continue
        if word == "size":
            # INSIDE a stanza this sets that stanza's window and nothing
            # else; before any stanza it sets the default for the rest of
            # the sheet. A tall window is how a stanza whose command wraps
            # keeps the command on screen under a full-height picture, and
            # nothing else in the sheet should inherit that.
            if cur:
                cur["size"] = tuple(int(x) for x in rest.split())
            else:
                size = tuple(int(x) for x in rest.split())
            continue
        if cur is None:
            sys.exit("%s: `%s' before any `shot'" % (path, word))
        if word == "cap":
            cur["cap"].append(rest)
        elif word == "for":
            cur["for"] += rest.split()
        elif word == "try":
            cur["try"] = rest
        elif word == "os9":
            cur["os9"] = rest
        elif word == "fold":
            cur["fold"] = True
        elif word == "frames":
            cur["frames"] = True
        elif word == "fresh":
            # END THE SESSION AFTER THIS STANZA.  For a stanza that leaves
            # something RESIDENT the next one would inherit: a background
            # process, a created event, a data module.  `lpsched /nil &'
            # makes the `spoolqueue' event and data module that `edir',
            # `eset' and `eunlink' each need, and a SECOND lpsched in the
            # same session answers "can't create spoolerqueue" -- so without
            # this only one of those four stanzas could have a real card.
            # It is also the honest fix for a background player like `mw's,
            # which `$!' being 0 in this bash makes unkillable from a stanza.
            cur["fresh"] = True
        elif word == "burst":
            # Capture this stanza unthrottled (see capture_burst).  For a
            # program that paints its whole screen in one burst and never
            # repaints -- backgammon's board -- the paced pty drops most of
            # the burst through its FIFO, so only the frame survives; an
            # unthrottled run delivers the lot.
            cur["burst"] = True
        elif word == "run":
            cur["acts"].append(("run", rest))
        elif word == "kill":
            cur["acts"].append(("kill", ""))
        elif word == "snap":
            cur["acts"].append(("snap", ""))
        elif word == "wait":
            cur["acts"].append(("wait", float(rest)))
        elif word == "send":
            cur["acts"].append(("send", unescape(rest)))
        elif word == "keys":
            cur["acts"].append(("keys", unescape(rest)))
        elif word == "quit":
            cur["quit"] = unescape(rest)
        else:
            sys.exit("%s: unknown directive `%s'" % (path, word))
    return shots


class Session:
    """One os9exec + bash on a pty, with the capture growing behind it."""

    # A program asking the window's size -- `resize' -- sends the cursor to
    # row 999, column 999 and asks where it stopped.  A real terminal answers
    # with its bottom right corner, so the session answers exactly that
    # query, and only that one: a general cursor-position report needs the
    # cursor tracked, which nothing here does, and a wrong answer is worse
    # than none.
    SIZE_QUERY = b"\x1b[999;999H\x1b[6n"

    def __init__(self, image, rows=24, cols=80):
        self.buf = bytearray()
        self.size_answer = ("\x1b[%d;%dR" % (rows, cols)).encode("latin-1")
        self.size_asked = 0
        self.lock = threading.Lock()
        self.master, slave = pty.openpty()
        fcntl.ioctl(slave, termios.TIOCSWINSZ,
                    struct.pack("HHHH", rows, cols, 0, 0))
        # emulator_env, not dict(os.environ): see tools/os9env.py.
        env = emulator_env(OS9DISK=image, OS9H0=image)
        # Mount the reader's OS-9 system (locally, the SDK) as /h1 when OS9SDK
        # points at it, so the runb-only programs (bio, blackjack) capture
        # exactly as a reader with their own system runs them: `load
        # /h1/CMDS/runb; runb <name>'. Unset -- as in CI, which never
        # re-captures -- /h1 is simply absent and that load fails gracefully.
        sdk = os.environ.get("OS9SDK")
        if sdk:
            env["OS9H1"] = sdk
        self.proc = subprocess.Popen([OS9EXEC, "bash"], stdin=slave,
                                     stdout=slave, stderr=slave,
                                     env=env, close_fds=True)
        os.close(slave)
        threading.Thread(target=self._drain, daemon=True).start()
        # LET os9exec COME UP FIRST. On a pty the terminal echoes anything
        # typed before the emulator has taken the line, so an early command
        # is simply lost.
        time.sleep(3.5)
        for line in LOGIN:
            self.write(line + "\r")
            time.sleep(0.35)

    def _drain(self):
        while True:
            try:
                chunk = os.read(self.master, 65536)
            except OSError:
                break
            if not chunk:
                break
            with self.lock:
                self.buf.extend(chunk)
                asked = self.buf.count(self.SIZE_QUERY)
            while self.size_asked < asked:
                os.write(self.master, self.size_answer)
                self.size_asked += 1

    def write(self, s):
        os.write(self.master, s.encode("latin-1"))

    def mark(self):
        with self.lock:
            return len(self.buf)

    def slice(self, a, b):
        with self.lock:
            return bytes(self.buf[a:b])

    READY = "S9READY"

    def ready(self, timeout=10):
        """Is the shell actually back, or is something still holding the tty?

        Ctrl-E is aimed at the terminal's LAST WRITER and not every program
        dies of it -- SEDT survived one and then ate the next three stanzas
        of its sheet, so `vc' and `ispell' were published showing SEDT's
        buffer. Asking the shell to echo a marker is the only answer that
        cannot be inferred: either the marker comes back or the session is
        no longer a shell and has to be replaced.
        """
        # THE MARKER MUST BE SPLIT WHEN TYPED AND WHOLE WHEN PRINTED.
        # Counting occurrences did not work: `vc', the spreadsheet, survived
        # Ctrl-E and ECHOED what was typed at it -- twice, in its own error
        # line -- so the check passed and the next five stanzas were
        # captured inside a spreadsheet, complete with `Unintelligible
        # word: let r0c0 = cho'. Only a shell that RUNS the command can join
        # the halves.
        typed = 'echo %s"%s"\r' % (self.READY[:3], self.READY[3:])
        try:
            self.write("\r")
            time.sleep(0.3)
            at = self.mark()
            self.write(typed)
        except OSError:
            return False
        deadline = time.time() + timeout
        while time.time() < deadline:
            time.sleep(0.4)
            if self.READY.encode() in self.slice(at, self.mark()):
                return True
        return False

    def close(self):
        try:
            self.write("\005")               # kill whatever is still running
            time.sleep(0.4)
            self.write("\r")
            time.sleep(0.3)
            self.write("stop\r")             # os9exec's own clean shutdown
            time.sleep(0.8)
        except OSError:
            pass
        try:
            self.proc.wait(timeout=8)
        except subprocess.TimeoutExpired:
            self.proc.terminate()            # ask, then allow time
            try:
                self.proc.wait(timeout=8)
            except subprocess.TimeoutExpired:
                self.proc.kill()             # only after a polite stop failed
        os.close(self.master)


def moments(sess, shot, start, end):
    """Render the stanza at several moments and keep the fullest.

    THE LAST MOMENT IS OFTEN THE WRONG ONE.  A program that scrolls has
    pushed its heading off; one that clears on the way out leaves a bare
    screen; one that is still drawing has drawn half.  So the screen is
    rendered at every mark taken while the stanza ran, and the one with the
    most of the program's OWN ink wins -- the same rule tools/playtest.py
    settled on after `hang' published an empty screen because hangman tidies
    up when the game ends.

    A tie goes to the LATER moment, so a program that simply prints keeps
    its full output rather than an early fragment of it.
    """
    rows, cols = shot["size"]
    best, best_worth = None, -1
    fallback, fallback_worth = None, -1
    # A stanza that said WHERE to look is not asking for the fullest moment.
    snaps = shot.get("_snaps") or []
    for at in snaps or (list(shot.get("_marks", [])) + [end]):
        if at <= start:
            continue
        scr = ansiscreen.render(trim_partial(sess.slice(start, at)), rows, cols)
        n, raw = worth(scr), ink(scr)
        if n >= best_worth:
            best, best_worth = scr, n
        if raw >= fallback_worth:
            fallback, fallback_worth = scr, raw
    # A program that ONLY ever produced the dump -- `top' aborts before it
    # draws anything -- scores zero at every moment, and publishing an empty
    # screen instead of the abort would be hiding what happened.
    if best is not None and ink(best) == 0 and fallback_worth > 0:
        best = fallback
    return best if best is not None else ansiscreen.render(b"", rows, cols)


def capture(sess, shot):
    """Run one stanza and return (screen, the-emulator-died).

    A program CAN take os9exec down with it -- `cpu' does, reliably -- and
    when it does every write to the pty fails with EIO. Losing the rest of a
    sheet to that would be the harness deciding which programs get
    captured, so the death is caught, the bytes that arrived before it
    are rendered anyway (they are the most interesting part), and the caller
    starts a fresh session for the next stanza.
    """
    died = False
    shot["_start"] = sess.mark()          # in case it dies before `clear'
    try:
        died = _drive(sess, shot)
    except OSError:
        died = True
    rows, cols = shot["size"]
    end = shot.get("_end") or sess.mark()
    return moments(sess, shot, shot["_start"], end), died


def _drive(sess, shot):
    # EVERY STANZA STARTS WITH THE LOGIN ENVIRONMENT.  A stanza that sources
    # /dd/SYS/termcap.entry -- hexedit, vi_cio -- leaves TERMCAP holding the
    # entry text for the rest of the session, and vi_1.0, which wants a
    # file name there, then published `Cannot open termcap file vt100|dec
    # vt100...'.  One joined line, typed before the clear, so it is never
    # in the picture.
    # Two lines, not one: joined, the exports run to 592 bytes and SCF
    # delivers at most 512 of a line.
    half = len(LOGIN) // 2
    for part in (LOGIN[:half], LOGIN[half:]):
        sess.write("; ".join(part) + "\r")
        time.sleep(0.6)
    # RESET THE DATA DIRECTORY TO ROOT at the head of every stanza.  Stanzas
    # in one size-group share a session, and `builtin cd' moves the OS-9 data
    # directory for the whole session, not just one command -- so a stanza
    # that does its setup with a hidden `builtin cd /dd/tmp/X' would leave the
    # next stanza looking there too.  The old sheets never hit this because
    # every cd was scoped inside a `ksh -c "cd X; ..."' subshell; a card that
    # shows a bare command instead keeps the cd out of sight up here, and this
    # line is what makes that safe.  SYS/login does the same `builtin cd
    # $ROOT', and it is a no-op for a stanza that never moved the directory.
    sess.write("builtin cd /dd\r")
    time.sleep(0.6)
    sess.write("clear\r")
    time.sleep(1.2)
    shot["_start"] = sess.mark()
    shot["_marks"] = []
    shot["_snaps"] = []
    for kind, val in shot["acts"]:
        if kind == "run" and val.strip() == "clear":
            # A `clear' IN the stanza starts the picture over: the setup
            # lines before it are not the program, and the fullest-moment
            # picker was choosing them over the program's own screen.
            sess.write("clear\r")
            time.sleep(1.2)
            shot["_start"] = sess.mark()
            shot["_marks"] = []
            shot["_snaps"] = []
        elif kind == "run":
            sess.write(val + "\r")
            time.sleep(1.0)
        elif kind == "wait":
            # Mark every couple of seconds, not just at the end of the wait:
            # a long wait is exactly where a program finishes drawing, starts
            # scrolling, or clears up after itself.
            waited = 0.0
            while waited < val:
                step = min(2.0, val - waited)
                time.sleep(step)
                waited += step
                shot["_marks"].append(sess.mark())
        elif kind == "send":
            sess.write(val)
            time.sleep(0.6)
            shot["_marks"].append(sess.mark())
        elif kind == "keys":
            for ch in val:
                sess.write(ch)
                time.sleep(shot["rate"])
        elif kind == "snap":
            shot["_snaps"].append(sess.mark())
        elif kind == "kill":
            # STOP IT WHILE ITS FIRST PAGE IS STILL ON SCREEN. `shire' prints
            # a year of weather and `calender' a year of dates; rendering the
            # whole stream leaves the grid showing December and no heading.
            sess.write("\005")
            time.sleep(0.8)
    time.sleep(0.6)
    shot["_end"] = sess.mark()
    if shot["quit"]:
        for ch in shot["quit"]:
            sess.write(ch)
            time.sleep(0.35)
        time.sleep(1.0)
    sess.write("\005")                       # Ctrl-E: kill the child, aimed
    time.sleep(0.5)                          # at the terminal's last writer
    sess.write("\r")
    time.sleep(0.4)
    return False


PARTIAL = re.compile(rb"\x1b\[?[0-9;?]*$")
ANSI = re.compile(rb"\x1b\[[0-9;?]*[A-Za-z]|\x1b[()#][0-9A-Za-z]|\x1b[=>78]")
FRAME_BREAK = re.compile(rb"\r\n?|\n")


def filmstrip(data, shot):
    """The stanza as one line per frame, for a program that animates a line.

    zot's fourteen styles slide, bounce, sort or spin the letters in, and it
    does that by writing the line again and again, each write ending in a
    bare carriage return so the next one lands on top.  Rendered into a grid
    that is the last frame only -- a plain line of text, which is what the
    card showed for a month, captioned as terminal attributes it never
    used.  Here every CR-terminated write is a line of its own, top to
    bottom, so the reader sees the dance.  Escape sequences go, blank frames
    go, and when there are more frames than rows the program's frames are
    sampled evenly while every typed command line stays.
    """
    rows, cols = shot["size"]
    text = ANSI.sub(b"", trim_partial(data))
    frames = [f for f in FRAME_BREAK.split(text) if f.strip()]
    runs = [v.encode("utf-8") for k, v in shot["acts"] if k == "run"]
    anchors = {i for i, f in enumerate(frames) if any(r in f for r in runs)}
    others = [i for i in range(len(frames)) if i not in anchors]
    room = rows - len(anchors)
    if len(others) > room and room > 1:
        keep = {others[round(k * (len(others) - 1) / (room - 1))]
                for k in range(room)}
        frames = [f for i, f in enumerate(frames) if i in anchors or i in keep]
    return ansiscreen.render(b"\r\n".join(frames) + b"\r\n", rows, cols)


def trim_partial(data):
    """Drop an escape sequence the capture window cut in half.

    A program that redraws -- `digclk' every second -- is mid-sequence when
    the screen is taken as often as not, and the renderer prints the tail as
    text: a working clock came out with `[11;3' written across it. The bytes
    are not corrupt; the window closed inside them.
    """
    return PARTIAL.sub(b"", data)


def stanza_hash(shot):
    """What this stanza DOES -- everything that decides the capture.

    THE CAPTION IS NOT IN HERE, and was until 2026-09-02.  A caption says
    what the screen means; it cannot change what the screen shows.  With it
    in the hash, fixing the wording of 151 captions marked NINETY-FOUR
    captures stale, and clearing that would have meant re-shooting them all
    to produce byte-identical screens -- hours, for nothing, which is the
    sort of chore that simply does not get done and leaves a drift report
    nobody believes.  The `for' list is out for the same reason: it credits
    a screen to more programs, it does not alter one.

    What remains is the name, the keystrokes, the quit sequence and the
    screen size -- change any of those and the capture really is out of
    date.
    """
    parts = [shot["name"], repr(shot["acts"]), str(shot["quit"]),
             str(shot["size"])]
    if shot.get("frames"):
        parts.append("frames")            # only when set: older hashes hold
    # `fresh' is deliberately NOT here: it changes what the NEXT stanza
    # starts from, never this stanza's own screen, and the rule above is
    # that only what alters the capture belongs in the fingerprint.
    return hashlib.sha1("\n".join(parts).encode("utf-8")).hexdigest()[:16]


def ink(scr):
    """The program's own ink -- the shell's prompt and echo are not it."""
    return sum(1 for line in scr.text().split("\n") if "bash#" not in line
               for ch in line if ch != " ")


# The lines of os9exec's own abort dump. It lands ON TOP of whatever the
# program had drawn, so where it overlays a picture it destroys ink it does
# not replace -- and a moment that lost ink that way loses to the one before
# it. Where the dump is ALL there is, as for the Graph library set, nothing
# was destroyed and the dump stands as the screen. That falls out of simply
# not counting these lines rather than penalising a screen for wearing them.
ABORT_DUMP = ("Process   Pid:", "Exit code: E_", "Directories: Current",
              "Execution -", "Files: 0")


def worth(scr):
    """How much a screen is WORTH LOOKING AT, which is not how full it is.

    A program that floods one line -- `No more memory !!!' twenty-four times
    -- fills the grid and says one thing, and picking the fullest moment
    picked exactly that: a screen of nothing but the flood, with the command
    that caused it scrolled away. So a line counts ONCE. An earlier moment,
    holding the command and the first line of the failure, then beats it.
    """
    seen, total = set(), 0
    for line in scr.text().split("\n"):
        if "bash#" in line or not line.strip() or line in seen:
            continue
        if any(line.lstrip().startswith(m) for m in ABORT_DUMP):
            continue                       # the emulator talking, not the program
        seen.add(line)
        total += sum(1 for ch in line if ch != " ")
    return total


def check_names(shots):
    """No two stanzas may share a name, IGNORING CASE.

    A capture is saved as notes/playtests/<name>.shot.txt, and on a
    case-insensitive filesystem -- which is what macOS ships -- `VI' and
    `vi' are ONE FILE. Shooting the second silently overwrote the first, so
    the `vi' card published PVIC's screen under the EFFO vi's caption: the
    exact lie the drift check exists to catch, arriving from the harness
    rather than from a program. Caught 2026-08-28 by that check.
    """
    seen = {}
    for shot in shots:
        key = shot["name"].lower()
        if key in seen and seen[key] != shot["name"]:
            sys.exit("%s: stanzas `%s' and `%s' differ only in case -- "
                     "their captures are one file on a case-insensitive "
                     "disk. Rename one." % (shot["sheet"], seen[key],
                                            shot["name"]))
        if key in seen:
            sys.exit("%s: two stanzas are both called `%s'"
                     % (shot["sheet"], shot["name"]))
        seen[key] = shot["name"]



def capture_burst(image, shot):
    """Capture one stanza with the emulator UNTHROTTLED, for a draw-once
    full-screen program the paced pty cannot deliver whole.

    Runs under Microware's own shell (the reader's OS-9, mounted as /h1 from
    OS9SDK) on a CR-only procedure file, with `-r' so pacing is off and the
    program's one burst of screen output arrives intact.  The stanza's `run'
    lines after the last `clear' are the commands; its `send' lines become
    the program's standard input, one per CR-terminated piece.  The raw
    terminal stream is rendered into the grid.
    """
    import tempfile
    rows, cols = shot["size"]
    sdk = os.environ.get("OS9SDK")
    if not sdk:
        # No reader-OS-9 to run the unthrottled shell: leave a blank grid
        # rather than a wrong one; the shoot log's low ink flags it.
        return ansiscreen.render(b"", rows, cols), False
    runs = [v for k, v in shot["acts"] if k == "run"]
    while "clear" in runs:
        runs = runs[runs.index("clear") + 1:]
    cmds = []
    for r in runs:
        r = r.strip()
        if not r or r == "clear":
            continue
        m = re.match(r"^(?:builtin\s+)?cd\s+(\S+)", r)
        if m:
            cmds.append("chd " + m.group(1))
        elif r.startswith("export "):
            continue                            # env is set below, Microware-style
        else:
            cmds.append(r)
    stdin = []
    for kind, val in shot["acts"]:
        if kind == "send":
            for piece in val.split("\r"):
                if piece != "" and all(ord(c) >= 32 for c in piece):
                    stdin.append(piece)
    env = ("setenv TERM vt100",
           "setenv TERMCAP /dd/SYS/termcap",
           "setenv PORT /term",
           "setenv PATH /dd/CMDS:/dd/CMDS/GAMES:/dd/CMDS/NETPBM:/dd/CMDS/UUCP:"
           "/dd/CMDS/TEXCMDS:/dd/CMDS/ELM:/dd/CMDS/COMMS:/dd/CMDS/NETWORK:"
           "/dd/CMDS/NEWS:/dd/CMDS/WN:/dd/CMDS/ADL:/dd/CMDS/REBUILT:"
           "/dd/CMDS/DEMOS:/dd/CMDS/DHRY:/dd/CMDS/GCC139:/h1/CMDS",
           "chx /dd/CMDS", "chd /dd")
    lines = ["-nx"] + list(env) + cmds + stdin
    scratch = tempfile.mkdtemp(prefix="burst.")
    proc = os.path.join(scratch, "b.proc")
    open(proc, "wb").write(("\r".join(lines) + "\r").encode("latin-1", "replace"))
    envd = emulator_env(OS9DISK=image, OS9H0=image, OS9H1=sdk,
                        OS9H6=scratch)
    try:
        out = subprocess.run([OS9EXEC, "-r", "/h1/CMDS/shell", "/h6/b.proc"],
                             stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, env=envd, timeout=90)
        raw = out.stdout
    except subprocess.TimeoutExpired as e:
        raw = e.stdout or b""
    i = raw.find(b"\x1b")
    if i > 0:
        raw = raw[i:]
    return ansiscreen.render(raw, rows, cols), False


def alf_off(raw):
    """Has something turned the console's AUTOMATIC LINE FEED off?

    OS-9 ends a display line with a bare CARRIAGE RETURN and SCF appends the
    line feed itself, gated on the path option PD_ALF ("If PD_ALF is not
    zero, carriage returns are automatically followed by line-feeds" -- v2.4
    Technical I/O Manual).  A program that wants a clean binary stream turns
    PD_ALF off, and THE CHANGE OUTLIVES IT AND REACHES OTHER PATHS: the
    shell, and every later stanza in the session, then writes CR with no LF
    -- every line lands back at column 0 on top of the last one, and the
    next prompt overwrites the first six characters of whatever is there.

    HOW it reaches them is not settled, and the difference does not matter
    to this check.  os9exec's pCsetopt copies the block to every open path
    on the device and its comment says real OS-9 does the same; the v2.4
    manual, read plainly, puts the option table IN THE PATH DESCRIPTOR,
    copied per path at open, which is per-path storage.  Two mechanisms
    would give what is measured here without SS_Opt being device-scoped:
    PD_PATHS at $16 is the "List of Open Paths on Device", so a file
    manager has the means to apply a change across all of them; and
    inherited standard paths share a descriptor outright, so a child
    clearing PD_ALF on its stdout writes the one its parent holds.  Treat
    the scope as unsettled and never assume an option change is private to
    your own path.

    That is what published `$ in: cannot connect to X server' for basicwin
    (`basicw' = six characters = len("bash# ")) and collapsed loadmem's four
    lines of syntax into one.  Measured 2026-09-13: the same stanza shot
    alone gives LF=5 CR=5 and ink 157; shot after cjpeg.070 it gives LF=1
    CR=5 and ink 7 -- the BYTES ARRIVE either way, so nothing is lost in the
    emulator or the program.  The session cannot be un-poisoned from out
    here, so the only cure is a fresh one.
    """
    crs = raw.count(b"\r")
    return crs >= 2 and raw.count(b"\n") < crs


def run_sheet(path, image, only=None):
    shots = parse(path)
    # check_names guards the WHOLE sheet, not just the subset -- a case
    # collision between a kept stanza and a skipped one is still a collision.
    check_names(shots)
    if only:
        shots = [s for s in shots if s["name"] in only]
        if not shots:
            return 0
    os.makedirs(CAPS, exist_ok=True)
    print("== %s: %d shots" % (os.path.basename(path), len(shots)),
          flush=True)
    done = 0

    def save(shot, scr, died):
        out = os.path.join(CAPS, "%s.shot.txt" % shot["name"])
        open(out, "w").write(scr.text() + "\n")
        open(out[:-4] + ".hash", "w").write(stanza_hash(shot))
        print("   %-16s ink=%-5d %s"
              % (shot["name"], ink(scr),
                 "TOOK THE EMULATOR DOWN WITH IT" if died
                 else "" if ink(scr) >= 20 else "<-- LOOK AT THIS ONE"),
              flush=True)

    # Draw-once full-screen stanzas, unthrottled and each on its own emulator.
    burst = [s for s in shots if s.get("burst")]
    for shot in burst:
        scr, died = capture_burst(image, shot)
        save(shot, scr, died)
        done += 1

    # Everything else: one paced pty session per window size.
    for size in sorted({s["size"] for s in shots if not s.get("burst")}):
        group = [s for s in shots if s["size"] == size and not s.get("burst")]
        sess = Session(image, size[0], size[1])
        try:
            for shot in group:
                shot.pop("_end", None)
                scr, died = capture(sess, shot)
                if shot.get("frames"):
                    scr = filmstrip(sess.slice(shot["_start"],
                                               shot.get("_end") or sess.mark()),
                                    shot)
                poisoned = alf_off(sess.slice(
                    shot["_start"], shot.get("_end") or sess.mark()))
                out = os.path.join(CAPS, "%s.shot.txt" % shot["name"])
                open(out, "w").write(scr.text() + "\n")
                # A FINGERPRINT OF THE STANZA THAT TOOK IT, so gen_screens can
                # say which captures are older than what they claim to show.
                # A sheet's mtime cannot: editing one stanza makes every
                # other stanza in the file look stale, and sixty false
                # alarms are the same as none.
                open(out[:-4] + ".hash", "w").write(stanza_hash(shot))
                print("   %-16s ink=%-5d %s"
                      % (shot["name"], ink(scr),
                         "TOOK THE EMULATOR DOWN WITH IT" if died
                         else "" if ink(scr) >= 20 else "<-- LOOK AT THIS ONE"),
                      flush=True)
                done += 1
                # A PROGRAM THAT FLOODS `No more memory !!!' HAS EATEN THE
                # ARENA, and the next stanza in the same session pays for it:
                # `sed' and `diff' both failed for want of memory three
                # stanzas after one that stormed, and the screens read as
                # two more broken programs.  The shell is still answering,
                # so the readiness check cannot see this -- the flood is the
                # signal.
                starved = scr.text().count("No more memory") >= 2
                if starved:
                    print("      (session replaced -- %s exhausted the arena)"
                          % shot["name"], flush=True)
                if poisoned:
                    print("      (session replaced -- %s left the console "
                          "with no automatic line feed)" % shot["name"],
                          flush=True)
                if shot.get("fresh"):
                    print("      (session replaced -- %s asked for a fresh "
                          "one)" % shot["name"], flush=True)
                if died or starved or poisoned or shot.get("fresh") \
                        or not sess.ready():
                    # ONE replacement, one line: `starved' and `poisoned' have
                    # already said WHY, and a second generic line under them
                    # reads as a second replacement to anyone counting them.
                    if not (starved or poisoned or shot.get("fresh")):
                        print("      (session replaced -- %s left it unusable)"
                              % shot["name"], flush=True)
                    sess.close()
                    sess = Session(image, size[0], size[1])
        finally:
            sess.close()
    return done


def needs_sdk(sheets, only=None):
    """Stanza names that cannot be shot without OS9SDK.

    This exists because an unset OS9SDK does not fail, it goes quiet: /h1 is
    never mounted, the stanza's `load /h1/...' does nothing, the program it
    wanted is not resident, and the capture is an empty screen.  That put a
    blank creadoc card in front of me on 2026-09-13 and read as a program
    broken by the fix I had just made to it.

    TWO KINDS QUALIFY, and for a while only the first was listed.  A stanza
    that NAMES /h1 is the obvious one.  A `burst' stanza is the other, and
    it is not obvious at all: capture_burst runs the whole stanza under
    MICROWARE'S shell mounted from OS9SDK, so with the variable unset it
    returns a blank grid by design -- see its own comment.  On 2026-09-20
    `back' came back with ink=0 while the warning named only `blackjack',
    and the backgammon board read as a program that had stopped working.
    It had not: with OS9SDK set the same stanza draws the whole board.
    """
    names = []
    for path in sheets:
        for s in parse(path):
            if only and s["name"] not in only:
                continue
            text = [a for _, a in s["acts"] if isinstance(a, str)]
            text += [x for x in (s["try"], s["os9"]) if x]
            if s["burst"] or any("/h1/" in t for t in text):
                names.append(s["name"])
    return sorted(names)


def main(argv):
    image = os.path.join(REPO, "osk-freeware.dd")
    sheets, only, i = [], None, 0
    while i < len(argv):
        if argv[i] == "--image":
            i += 1
            image = argv[i]
        elif argv[i] == "--only":
            # Recapture named stanzas and leave the rest of the sheet alone.
            # Without this, correcting one card meant rerunning a sheet of
            # sixty and waiting ten minutes for the fifty-nine that were fine.
            i += 1
            only = set(argv[i].split(","))
        elif argv[i] == "--all":
            sheets += sorted(os.path.join(SHEETS, f)
                             for f in os.listdir(SHEETS)
                             if f.endswith(".sheet"))
        else:
            sheets.append(argv[i])
        i += 1
    if not sheets:
        sys.exit(__doc__)
    if not os.path.exists(image):
        sys.exit("no image at %s -- run tools/mkimage.sh first" % image)
    # AN OS9Hx/OS9DISK PATH MUST BE ABSOLUTE -- see the same line in
    # datatest.py. A bare relative name mounts the device and lets module
    # loading work while ordinary file opens on it silently fail.
    image = os.path.abspath(image)

    blind = needs_sdk(sheets, only)
    if blind and not os.environ.get("OS9SDK"):
        print("WARNING: OS9SDK is unset, so /h1 is absent.  These stanzas load\n"
              "         from it and will capture a BLANK screen, not a broken\n"
              "         program: %s\n"
              "         Set OS9SDK to an OS-9 system to re-shoot them."
              % ", ".join(blind), file=sys.stderr)

    with imagelock.held(image, "screenshots"):
        total = sum(run_sheet(s, image, only) for s in sheets)
    print("%d screens in %s" % (total, CAPS))


if __name__ == "__main__":
    main(sys.argv[1:])
