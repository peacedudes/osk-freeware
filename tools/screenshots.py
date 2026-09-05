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

Sheet format (blank lines and `#' comments ignored):

    shot    today                  start a stanza; the program's own name,
                                   because that is how the catalogue finds it
    cap     Prints the date in ...  caption for the gallery (repeatable)
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

    def __init__(self, image, rows=24, cols=80):
        self.buf = bytearray()
        self.lock = threading.Lock()
        self.master, slave = pty.openpty()
        fcntl.ioctl(slave, termios.TIOCSWINSZ,
                    struct.pack("HHHH", rows, cols, 0, 0))
        env = dict(os.environ, OS9DISK=image, OS9H0=image)
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
    # One session per window size: the size is fixed when the pty is opened.
    done = 0
    for size in sorted({s["size"] for s in shots}):
        group = [s for s in shots if s["size"] == size]
        sess = Session(image, size[0], size[1])
        try:
            for shot in group:
                shot.pop("_end", None)
                scr, died = capture(sess, shot)
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
                if died or starved or not sess.ready():
                    print("      (session replaced -- %s left it unusable)"
                          % shot["name"], flush=True)
                    sess.close()
                    sess = Session(image, size[0], size[1])
        finally:
            sess.close()
    return done


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

    with imagelock.held(image, "screenshots"):
        total = sum(run_sheet(s, image, only) for s in sheets)
    print("%d screens in %s" % (total, CAPS))


if __name__ == "__main__":
    main(sys.argv[1:])
