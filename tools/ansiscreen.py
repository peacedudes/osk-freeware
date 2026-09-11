#!/usr/bin/env python3
"""Render a captured OS-9 terminal stream into the screen it would have drawn.

    tools/ansiscreen.py <capture> [<rows> <cols>]

The four-stage sweep scores a program by WHAT IT PRINTS, which is why it
credited `tet' as working while `tet' ignored the keyboard and later while it
ran too fast to play. Bytes are not a screen. This turns the bytes into the
80x24 grid a vt100 would have shown, so a play-test can be judged on what a
person would actually have seen.

It also counts the one corruption that matters here: an ESC that never
arrived. SCF echoes what you type, and the echoed character lands in the
MIDDLE of the ESC [ r ; c H the program is writing -- so the terminal prints
the tail as text and the screen fills with `[8;13H'. Measured on tet,
2026-08-27: 9 such sequences while playing, 1 while idle, 0 once the program
turned echo off.

Deliberately a SUBSET of vt100: the cursor moves, erases, the two
alternate-keypad toggles this collection's curses actually emits, and the
DEC Special Graphics character set. Anything else is skipped rather than
guessed at -- a renderer that invents behaviour would hide exactly the
defects this exists to find.

The line-drawing set is mapped to ASCII (`+', `-', `|'), not to the Unicode
box characters: nothing in this repository may carry a byte over 0x7f.
"""
import re
import sys

ROWS, COLS = 24, 80

# ESC [ <params> <final>, plus the bare two-character escapes curses emits.
CSI = re.compile(rb"\x1b\[([0-9;?]*)([@-~])")
ESC2 = re.compile(rb"\x1b([=>78MDEHc])")

# ESC ( <c> and ESC ) <c> designate a character set for G0 and G1.  `0' is
# DEC Special Graphics -- the box-drawing set -- and `B' is US ASCII.
CHARSET = re.compile(rb"\x1b([()])([0-9A-B])")

# TeleVideo / ADM-3A cursor addressing: ESC = <row+32> <col+32>.  `gcl', the
# grand digital clock, is written for that terminal and nothing else, and
# without this its digits came out as a column of `!', `"', `#' -- the row
# bytes -- because ESC = was read as the VT100 keypad toggle and the two
# bytes after it as text.  A VT100 keypad toggle is followed by another
# escape or a control; two printable bytes that fit the grid are a move.
# ESC G <digit> is the TeleVideo attribute (G0 plain, G4 reverse): dropped.
TVI_CUP = re.compile(rb"\x1b=([\x20-\x7e])([\x20-\x7e])")
TVI_ATTR = re.compile(rb"\x1bG[0-9]")

# TeleVideo / ADM-3A clear-to-end-of-line.  `fuddle', a TeleVideo program,
# clears its status line with ESC T before writing "White's move:" over it;
# unhandled, the ESC was skipped and its `T' printed as text at column 0, so
# the card read "TWhite's move:".  ESC T and the TVI-925 ESC t both clear from
# the cursor to the end of the line.  (ESC Y, clear to end of screen, is left
# out: nothing here needs it, and it collides with vt52 cursor addressing.)
TVI_CLEAR = re.compile(rb"\x1b([Tt])")

# DEC Special Graphics, MAPPED TO ASCII rather than to the Unicode box
# characters, because nothing in this repository is allowed to carry a byte
# over 0x7f.  A corner is a `+', a horizontal a `-', a vertical a `|'; that
# is what a line-drawing terminal looked like to anyone without the font,
# and it reads correctly in a gallery card.
#
# WITHOUT THIS THE ESCAPE WAS SKIPPED AND THE LETTERS PRINTED AS TEXT.
# `sysmon' draws its process table with this set and its card came out as
# forty lines of `(0x       (0x       (0x' on 2026-09-02 -- which looks
# like a corrupt capture and is a renderer that stopped one branch short.
# It is the only program here that had ever got far enough to use it.
DEC_GRAPHICS = {
    "j": "+", "k": "+", "l": "+", "m": "+", "n": "+",
    "t": "+", "u": "+", "v": "+", "w": "+",
    "q": "-", "x": "|",
    "a": ":", "h": "#", "0": "#", "~": ".",
    "`": "+", "f": "o", "g": "+", "i": "+",
    "o": "-", "p": "-", "r": "-", "s": "-",
    "y": "<", "z": ">", "{": "*", "|": "!", "}": "#",
}

# `dm' (Disk Master) draws its panels with raw CODE PAGE 437 box-drawing
# BYTES -- no escape sequence switches to them and none switches back, it
# just assumes an IBM-compatible screen.  Read as latin-1 those bytes are
# printable Western-European letters (0xC9 is `\xc9', printed as `É'
# and encoded as two UTF-8 bytes), which is how a two-pane browser's frame
# turned into `\xc9\xcd\xcd...' -- a repository file carrying bytes over
# 0x7f.  Same ASCII convention as DEC_GRAPHICS: corner or tee is `+',
# double horizontal `-', double vertical `|'.
CP437_BOX = {
    "\xba": "|", "\xb9": "+", "\xbb": "+", "\xbc": "+",
    "\xc8": "+", "\xc9": "+", "\xca": "+", "\xcb": "+",
    "\xcc": "+", "\xcd": "-", "\xce": "+",
    "\xb3": "|", "\xb4": "+", "\xbf": "+",
    "\xc0": "+", "\xc1": "+", "\xc2": "+", "\xc3": "+",
    "\xc4": "-", "\xc5": "+", "\xd9": "+", "\xda": "+",
}


class Screen:
    """An 80x24 character grid with a cursor, fed a byte stream."""

    def __init__(self, rows=ROWS, cols=COLS):
        self.rows, self.cols = rows, cols
        self.grid = [[" "] * cols for _ in range(rows)]
        self.row = self.col = 0
        self.orphans = []          # escape sequences that arrived without ESC
        self.unknown = set()       # finals we chose not to implement
        # A vt100 keeps TWO designated sets, G0 and G1, and SO/SI (0x0E/0x0F)
        # pick which one is active -- `tree' designates G1 as DEC Special
        # Graphics with ESC )0 and wraps each line-drawing character in
        # SO...SI, never touching G0 at all.  Without tracking G1 and the
        # shift its `q', `t', `m', `w' came through as the literal letters.
        self.g0_graphics = False
        self.g1_graphics = False
        self.shifted = False       # SO active: G1 is the set in use
        # REVERSE VIDEO IS INK.  gcl draws its digits as blanks in reverse
        # video, so a grid of characters alone showed nothing at all: a
        # space put down while reverse is on is shown as `#', the way the
        # DEC graphics blocks are.
        self.reverse = False

    # -- cursor -----------------------------------------------------------
    def _clamp(self):
        self.row = max(0, min(self.rows - 1, self.row))
        self.col = max(0, min(self.cols - 1, self.col))

    def put(self, ch):
        active = self.g1_graphics if self.shifted else self.g0_graphics
        if active and ch >= " " and ch in DEC_GRAPHICS:
            ch = DEC_GRAPHICS[ch]
        elif ch in CP437_BOX:
            ch = CP437_BOX[ch]
        if self.reverse and ch == " ":
            ch = "#"
        if ch == "\r":
            self.col = 0
        elif ch == "\n":
            self.row += 1
            if self.row >= self.rows:      # scroll
                self.grid.pop(0)
                self.grid.append([" "] * self.cols)
                self.row = self.rows - 1
        elif ch == "\b":
            self.col -= 1
        elif ch == "\t":
            self.col = min(self.cols - 1, (self.col // 8 + 1) * 8)
        elif ch == "\x07":
            pass                            # bell
        elif ch >= " ":
            self._clamp()
            self.grid[self.row][self.col] = ch
            self.col += 1
            if self.col >= self.cols:
                self.col = self.cols - 1
        self._clamp()

    def erase_display(self, mode):
        if mode in (2, 3):
            self.grid = [[" "] * self.cols for _ in range(self.rows)]
            self.row = self.col = 0
        elif mode == 0:
            for c in range(self.col, self.cols):
                self.grid[self.row][c] = " "
            for r in range(self.row + 1, self.rows):
                self.grid[r] = [" "] * self.cols

    def erase_line(self, mode):
        if mode == 0:
            for c in range(self.col, self.cols):
                self.grid[self.row][c] = " "
        elif mode == 1:
            for c in range(0, self.col + 1):
                self.grid[self.row][c] = " "
        elif mode == 2:
            self.grid[self.row] = [" "] * self.cols

    # -- the stream -------------------------------------------------------
    def feed(self, data):
        i, n = 0, len(data)
        while i < n:
            b = data[i:i + 1]
            if b == b"\x0e":                  # SO: shift to G1
                self.shifted = True
                i += 1
                continue
            if b == b"\x0f":                  # SI: shift to G0
                self.shifted = False
                i += 1
                continue
            if b == b"\x1b":
                m = CSI.match(data, i)
                if m:
                    self._csi(m.group(1), m.group(2))
                    i = m.end()
                    continue
                m = CHARSET.match(data, i)
                if m:
                    if m.group(1) == b"(":
                        self.g0_graphics = m.group(2) == b"0"
                    else:                       # b")": designates G1
                        self.g1_graphics = m.group(2) == b"0"
                    i = m.end()
                    continue
                m = TVI_CUP.match(data, i)
                if m and (m.group(1)[0] - 0x20) < self.rows \
                        and (m.group(2)[0] - 0x20) < self.cols:
                    self.row, self.col = m.group(1)[0] - 0x20, m.group(2)[0] - 0x20
                    i = m.end()
                    continue
                m = TVI_ATTR.match(data, i)
                if m:
                    self.reverse = m.group(0)[-1:] == b"4"
                    i = m.end()
                    continue
                m = TVI_CLEAR.match(data, i)
                if m:
                    self.erase_line(0)           # clear cursor -> end of line
                    i = m.end()
                    continue
                m = ESC2.match(data, i)
                if m:
                    i = m.end()               # keypad toggles: ignore
                    continue
                i += 1
                continue
            # An ESC-less "[12;34H" is the corruption signature, not text.
            # REQUIRE DIGITS. Without them this flagged ordinary prose: the
            # "[file]" in sonnet's usage line was counted as six corrupted
            # escapes and failed a program that was working perfectly. A real
            # cursor move always carries numeric parameters.
            if b == b"[":
                m = re.match(rb"\[([0-9]+(?:;[0-9]+)*)([A-Za-z])", data[i:])
                if m and m.group(2) in b"HfABCDJKm":
                    self.orphans.append(m.group(0).decode("latin-1"))
                    for ch in m.group(0).decode("latin-1"):
                        self.put(ch)          # a real terminal prints it
                    i += m.end()
                    continue
            self.put(b.decode("latin-1"))
            i += 1

    def _csi(self, params, final):
        ps = [int(x) if x.isdigit() else 0
              for x in params.decode("latin-1").replace("?", "").split(";")]
        f = final.decode("latin-1")
        one = ps[0] if ps else 0
        if f in "Hf":
            self.row = (ps[0] - 1) if len(ps) > 0 and ps[0] else 0
            self.col = (ps[1] - 1) if len(ps) > 1 and ps[1] else 0
        elif f == "A":
            self.row -= max(1, one)
        elif f == "B":
            self.row += max(1, one)
        elif f == "C":
            self.col += max(1, one)
        elif f == "D":
            self.col -= max(1, one)
        elif f == "J":
            self.erase_display(one)
        elif f == "K":
            self.erase_line(one)
        elif f == "m":
            if 7 in ps:
                self.reverse = True
            if 0 in ps or 27 in ps or not ps:
                self.reverse = False
        elif f in "hlrsu":
            pass                              # modes: not rendered
        else:
            self.unknown.add(f)
        self._clamp()

    # -- output -----------------------------------------------------------
    def text(self):
        return "\n".join("".join(r).rstrip() for r in self.grid)

    def ink(self):
        """How many cells hold something other than a space."""
        return sum(1 for r in self.grid for c in r if c != " ")


def render(data, rows=ROWS, cols=COLS):
    s = Screen(rows, cols)
    s.feed(data)
    return s


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    rows = int(argv[2]) if len(argv) > 2 else ROWS
    cols = int(argv[3]) if len(argv) > 3 else COLS
    s = render(open(argv[1], "rb").read(), rows, cols)
    print(s.text())
    print("-" * cols)
    print("ink=%d cells   orphaned-escapes=%d   unimplemented-finals=%s"
          % (s.ink(), len(s.orphans), "".join(sorted(s.unknown)) or "none"))


if __name__ == "__main__":
    main(sys.argv)
