#!/usr/bin/env python3
"""Which gallery cards show a program WORKING, and which do not.

    tools/audit_cards.py                # the flagged ones, worst first
    tools/audit_cards.py --all          # every card and its score
    tools/audit_cards.py --show <name>  # one card's capture, in full

WHY THIS EXISTS, and why `audit_screens.py' is not enough
--------------------------------------------------------
`audit_screens.py' flags a card whose EVERY line is an error.  On a real
capture the typed command line is one of those lines and is not an error, so
the rule almost never fires: it reported 2 of 407 on 2026-08-31.  That is a
check that cannot fail, which is this collection's oldest recurring defect.

rdoggett, 2026-08-31: *"Sample output that does nothing more than show the
help is only valuable if the help isn't shown some other way, and there is no
more interesting output from the program to show."*  And, of `hc': a card
that shows a FAILED invocation, captioned as though the program were at
fault, is worse than no card.

So this scores each card by what its lines ARE, per command run:

    USAGE     the program answered with its own usage or syntax line
    ERROR     an OS-9 error, a trap, a "not found", a "can't"
    WORK      anything else -- the program doing its job

A card is flagged when it has no WORK at all, or when errors outnumber work.
It is a PROMPT TO GO AND LOOK, not a verdict: `spiff' prints nothing because
the two files matched, which is the point of that card, and a diff tool
saying "files differ" is doing its job in words that read like an error.
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAPS = os.path.join(REPO, "notes", "playtests")

# The shell's own prompt, in every form the captures carry it.
# A BARE `$' IS ONLY A PROMPT WHEN A SPACE FOLLOWS IT.  `strings'
# prints its offsets as `$00017F: <text>', and stripping the `$' left
# `00017F: ...', which then landed in the typed-command branch -- so a
# card with fourteen lines of real output scored work=0 and was reported
# NOTHING.  Measured 2026-09-12; `strings' is the only capture affected,
# but the shape would silently hide any program whose output starts `$'.
PROMPT = re.compile(r"^(bash#|os9\$|\$(?=\s))\s?")

USAGE = re.compile(r"(?i)^\s*(usage|syntax|use\b|options?)\s*[:\-]"
                   r"|^\s*usage\s*$")
ERROR = re.compile(
    r"(?i)(error\s*#|\berror\b|can't|cannot|couldn't|unable to|not found"
    r"|no such|\*\*\*\*\s.*\s\*\*\*\*|unknown option|illegal|invalid|bad |permission"
    r"|E\$[A-Za-z]|vector=\$|not accessible|no more memory|abort)")


def sheet_commands():
    """shot name -> the set of command lines its stanza runs."""
    sys.path.insert(0, os.path.join(REPO, "tools"))
    import screenshots                                   # noqa: E402
    out = {}
    sheets = os.path.join(REPO, "tools", "screenshots")
    for f in sorted(os.listdir(sheets)):
        if not f.endswith(".sheet"):
            continue
        for shot in screenshots.parse(os.path.join(sheets, f)):
            runs = {v.strip() for k, v in shot["acts"] if k == "run"}
            out.setdefault(shot["name"], set()).update(runs)
    return out


def commands(name, sheets):
    """The exact command lines this card typed, from its own sheet stanza.

    A capture does NOT reliably prefix an echoed command with a prompt -- the
    shell's prompt is overwritten by a program that clears the screen, so the
    next command lands bare.  Scoring those bare echoes as the program's own
    output was worth several points of `work' on every card and hid exactly
    the cards this tool is for.  The sheet knows what was typed; ask it.
    """
    return sheets.get(name, set())


def classify(path, typed):
    """Score a capture's lines.  `body' comes back holding the SCORED ones.

    The command a card typed is not evidence either way, and there are two
    honest ways to know it when you see it: a prompt in front of it, or the
    sheet's own record of what was run.  There was a third until 2026-09-13
    -- discount the FIRST line of every capture, on the theory that a
    cleared screen leaves the echo bare -- and measured across 990 cards it
    discounted 241 first lines of which TWO were echoes.  The other 239 were
    the programs' own opening words: `OS-9 BACKGAMMON', `BATTLESHIPS',
    `ATerm : A terminal program for OS9/68000', `Wrote cache file
    ./index.cache'.  It cost seven cards a false NOTHING and threw away the
    most informative line of nearly every other card in the gallery.

    The two real echoes (`gs33', `wrjpgcom.070') are line-wrapped command
    text on cards scoring work elsewhere, so letting them count as one point
    hides nothing.  That is the trade: two spurious points against 239
    recovered lines.
    """
    usage = err = work = 0
    body = []
    for raw in open(path, errors="replace").read().split("\n"):
        line = raw.rstrip()
        stripped = PROMPT.sub("", line).strip()
        if not stripped:
            continue
        if PROMPT.match(line) or stripped in typed:
            continue
        body.append(stripped)
        if USAGE.search(stripped):
            usage += 1
        elif ERROR.search(stripped):
            err += 1
        else:
            work += 1
    return usage, err, work, body


def main(argv):
    show = None
    everything = False
    i = 0
    while i < len(argv):
        if argv[i] == "--all":
            everything = True
        elif argv[i] == "--show":
            i += 1
            show = argv[i]
        else:
            sys.exit(__doc__)
        i += 1

    if show:
        p = os.path.join(CAPS, "%s.shot.txt" % show)
        if not os.path.exists(p):
            sys.exit("no capture for %s" % show)
        sys.stdout.write(open(p, errors="replace").read())
        return 0

    sheets = sheet_commands()
    rows = []
    # TWO CARDS ARE FLAGGED CORRECTLY BY THE RULE AND WRONGLY BY THE POINT.
    # `perr' turns an OS-9 error number into its message, so error text IS
    # its output and a screen full of `Error #000:216' is exactly right.
    # Listing them here rather than weakening the rule: a rule that stopped
    # noticing error-only screens would stop finding the ones that matter.
    NOREADER = ("reads a format no file here is in, and no writer for it "
                "ships either -- the caption says so, and refusing a file "
                "it cannot read is the behaviour you want")
    fine = {"perr": "perr PRINTS error messages -- error text is its output",
            "perr-print": "the same program, printing a wider range",
            "csl-mismatch": "the card's SUBJECT is the csl edition skew -- "
                            "four programs that stop before they start, and "
                            "the message is the whole finding",
            "perr-alps": "perr again, beside alps and epson -- the five "
                         "`Error #000:00n' lines ARE perr's output, exactly "
                         "as on the perr card",
            "silent": "the card's SUBJECT is programs that say nothing and "
                      "why. `cannot execute binary file' for a BASIC09 "
                      "subroutine and for a trap library is the finding: "
                      "running a non-program proves nothing",
            "disktest": "measures disk performance and CANNOT here: bare "
                        "it prints nothing and `disktest /dd' ends the "
                        "emulator session outright, both measured "
                        "2026-09-01 in tools/drives/flagged1.drive. Its "
                        "option list has one option and it is -?",
            # THE NO-READER CONVERTERS.  Sixteen netpbm readers decode
            # formats no file on this disk is in -- confocal microscopes,
            # ray tracers, AutoCAD slides, Photo CD, Amiga brushes, Gould
            # scanners -- and netpbm here ships no WRITER for any of them,
            # so no round trip can be staged.  Handed something else they
            # report the bad magic number rather than guessing, and every
            # one of these cards SAYS SO in its caption.  The screen is an
            # error line; the card is correct.  Flagged by the rule,
            # wrongly by the point -- same as `perr' above.
            "brushtopbm": NOREADER, "gouldtoppm": NOREADER,
            "hipstopgm": NOREADER, "hpcdtoppm": NOREADER,
            "mtvtoppm": NOREADER, "spottopgm": NOREADER,
            "ximtoppm": NOREADER, "xvminitoppm": NOREADER,
            "edir": "the event directory IS empty, and that is the finding: "
                    "nothing on this disk CREATES an event -- OS-9's own "
                    "`event' utility is Microware's and is not here -- so "
                    "`eset' can only link to one that already exists, which "
                    "is what its `can't link to' says",
            # FOUR MORE WHOSE FAILURE IS THE POINT OF THE CARD (2026-09-13).
            # Each caption states the finding, and each was read before being
            # listed here -- the same standard `perr' and the no-reader set
            # meet.  Checked while working the flag list down from 71: all
            # four looked like defects from the flag alone and are not.
            "cjpeg.070": "the card's SUBJECT is that this is the "
                         "OTHER-PROCESSOR build.  Its 68000 twin `cjpeg' "
                         "compresses the same PNM and is published at ink "
                         "156; this one answers `Premature end of input "
                         "file'.  The failure IS the comparison the card "
                         "exists to draw",
            "pbmtobbnbg": "a WRITER, not a no-reader: given a PBM this "
                          "disk's own `pbmmake' produces, it reports `bad "
                          "magic number' while pbmtog3, pbmtogem and "
                          "pbmtoicon read the SAME FILE in the same sheet.  "
                          "The card carries its own control and documents a "
                          "defect in the program",
            "newslock": "the finding is that it leaves no trace -- no file "
                        "at either name, nothing printed.  The `ls' showing "
                        "error 216 for both lock names is the EVIDENCE for "
                        "that, captured on purpose, not a broken invocation",
            "exrecover": "recovers the buffer `expreserve' kept when vi "
                         "died.  With nothing preserved, `File not found' is "
                         "the honest answer and the caption says so",
            "remove": "a BEFORE-AND-AFTER, and the rule reads only half of "
                      "it.  The stanza loads readmsg, shows it answering by "
                      "name with its usage line, runs `remove readmsg', then "
                      "runs the SAME command again -- and `readmsg: nowhere "
                      "found' is the proof that remove did its job, which is "
                      "what the caption says.  Scored THIN-HELP because the "
                      "usage line counts as help, but that line is the BEFORE "
                      "half, not the subject",
            "flink": "makes an RBF hard link and CORRUPTS THE DISK IT LINKS "
                     "ON -- removing such an entry left `/dd/CMDS/cat' "
                     "pointing at a DIRECTORY, with every program answering "
                     "`cat: is a directory' until the image was rebuilt.  Its "
                     "usage line is the only card it can ever safely have, "
                     "and the caption says why.  See CLAUDE.md, which forbids "
                     "running it in a test at all",
            "lgrep": "its card ALREADY runs a real search -- `lgrep ksh "
                     "SYS/password', where `ksh' is genuinely in that file -- "
                     "and lgrep prints nothing and exits 0.  That silence IS "
                     "the finding, the caption says so and sends the reader "
                     "to `grep -l', and DOC/README-GREP compares the "
                     "searchers.  Scored THIN-HELP for the usage line above "
                     "the search, not for want of trying one",
            "run": "its card ALREADY does the real thing -- `export "
                   "PORT=/term; run \"whoami\"' -- and nothing comes back, "
                   "because run rebinds stdio to the terminal PORT names and "
                   "here the console IS that terminal.  The caption says "
                   "exactly that.  Nothing else is available to show",
            # THE PRINT SPOOLER IS NOT INSTALLED ON THIS DISK, and its four
            # tools can only say so.  Each was read 2026-09-13: two of them
            # already RUN for real on their cards and report the true state,
            # one runs a removal, and one hangs if pushed.  `submit' is
            # deliberately NOT here -- a .sub file could be written for it.
            "lpq": "its card already runs `lpq' for real and gets `lpq: no "
                   "spooler installed', which is the program working and "
                   "reporting the true state of this disk",
            "lprm": "its card already runs `lprm 1' for real; with no spooler "
                    "managing a queue there is nothing to link to and it says "
                    "so rather than pretending to remove a job",
            "lpsched": "starts the spooler for a printer device, and given "
                       "one -- there is no printer here -- it WAITS to open "
                       "it rather than answering, so the option list is all "
                       "that can safely be shown",
            "lpshut": "its card already runs `lpshut' for real and gets "
                      "`lpshut: no spooler active', which is the true state",
            # THE EVENT PAIR, and they follow `edir' above rather than setting
            # a precedent: NOTHING ON THIS DISK CREATES AN EVENT, because
            # OS-9's own `event' utility is Microware's and is not here.  Both
            # cards already RUN for real against a name that cannot exist.
            "eset": "sets an existing event's value, and this disk has no way "
                    "to create one -- see `edir'.  Its card already runs "
                    "`eset testevent 1' and gets the refusal that proves it",
            "eunlink": "the other end of the same pair; its card already runs "
                       "it and gets `E_EVNF Event (name) not found', which is "
                       "the whole finding",
            # TWO MORE PIECES OF ABSENT HARDWARE.  Both read 2026-09-13.
            "dpark": "restores a physical RBF drive's head to track 00 -- "
                     "something you did before moving a drive, and there is "
                     "no drive head here to park",
            "sbreak": "sends a break on a serial device; its card already "
                      "runs it bare and gets `sbreak: Must specify device!', "
                      "and there is no serial device here to name",
            # THREE TERMINAL PROGRAMS THAT NEED HARDWARE NOBODY HAS HERE, and
            # a definition file that does not ship.  Each was read 2026-09-13
            # and each caption already names the requirement.  `fontgen' is
            # NOT the missing half: it writes ASSEMBLER SOURCE for a font
            # module (`nam text80z.font', a psect, FontData) for a Gepard
            # 80-column card -- not a downloadable font any of these load.
            "setfont": "loads a downloadable terminal font from a path, and "
                       "no such font ships; the terminal here has no "
                       "downloadable font to load either",
            "chardef": "defines a character set on a VT220 from a definition "
                       "file; neither the file nor a VT220 is here",
            "fkeys": "programs a VT220's user-defined keys from a definition "
                     "file; neither the file nor a VT220 is here",
            # collect2 is a LINKER PASS, not a user-facing program: g++ runs
            # it between compiling and linking to build the global
            # constructor table.  `collect' and `gpp_collect' are the same
            # binary (md5 74b3bbf3686d) in two directories; `gcc_collect' is
            # GCC139's build of it.  With no arguments it prints its usage by
            # design -- it takes no -? -- and there is no demonstration of it
            # that is not a C++ link.
            "collect": "collect2, a g++ linker pass; with no arguments it "
                       "prints its usage by design and its real use is inside "
                       "a C++ link",
            "gcc_collect": "the same linker pass, GCC139's build of it",
            "gpp_collect": "the same linker pass, byte-identical to `collect'",
            "transfer": "copies files off a GDOS disk, and the GDOS device "
                        "DGDOS0 is not present on this disk or in os9exec -- "
                        "so `Can't load device descriptor' is the only thing "
                        "it can say here, and the caption says so.  Looked "
                        "at 2026-09-13 when the first-line fix surfaced it: "
                        "there is no other output to show",
            }
    # `texfonts-bitmap' was excepted here until 2026-09-01, on the grounds
    # that there was no .pk, .gf or .vf for its eight tools to read.  There
    # is now: `inimf' builds plain.base out of the disk's own MFINPUTS, and
    # with the base installed `virmf' renders a font that the other seven
    # read.  The exception is gone because the card is no longer a usage
    # line -- which is the outcome an exception should always be aiming at.
    for f in sorted(os.listdir(CAPS)):
        if not f.endswith(".shot.txt"):
            continue
        name = f[:-len(".shot.txt")]
        # A CAPTURE WITH NO STANZA IS NOT A GALLERY CARD.  61 of the 990
        # captures on disk belong to no stanza -- setup shots, multi-program
        # captures, leftovers -- and `gen_screens' says so plainly every run:
        # "N capture(s) belong to no stanza and are NOT published".  Scoring
        # them made this tool report on things no reader can see, and put one
        # of them (`sgi-p') in a queue of cards to go and fix.  Measured
        # 2026-09-13: 990 scored, 929 real.
        if name not in sheets:
            continue
        usage, err, work, body = classify(os.path.join(CAPS, f),
                                          commands(name, sheets))
        why = ("NOTHING" if not (usage or err or work) else
               "HELP-ONLY" if work == 0 and usage and not err else
               "ERROR-ONLY" if work == 0 and err and not usage else
               "HELP+ERROR" if work == 0 else
               "MOSTLY-ERROR" if err > work else
               "MOSTLY-HELP" if usage > work else
               # A usage line plus two or three lines of anything is still a
               # card whose subject is the help text.  rdoggett's test is
               # whether there is MORE INTERESTING OUTPUT to show, and a
               # near-empty screen carrying a syntax line says there is not.
               "THIN-HELP" if usage and work <= 3 else "")
        if name in fine:
            why = ""
        rows.append((name, why, usage, err, work, body))

    flagged = [r for r in rows if r[1]]
    order = {"NOTHING": 0, "ERROR-ONLY": 1, "HELP+ERROR": 2, "HELP-ONLY": 3,
             "MOSTLY-ERROR": 4, "MOSTLY-HELP": 5, "THIN-HELP": 6, "": 9}
    for name, why, u, e, w, body in sorted(everything and rows or flagged,
                                           key=lambda r: (order[r[1]], r[0])):
        first = next(iter(body), "")
        print("%-20s %-12s help=%-3d err=%-3d work=%-4d %s"
              % (name, why or "ok", u, e, w, first[:44]))
    print("\n%d of %d cards flagged" % (len(flagged), len(rows)))
    for name, why in sorted(fine.items()):
        print("  (not flagged, by name: %-12s %s)" % (name, why))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
