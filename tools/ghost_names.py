#!/usr/bin/env python3
r"""Find names the shipped text points at and the disk does not have.

    tools/ghost_names.py            # candidates, with the files naming them
    tools/ghost_names.py --quotes   # show the sentence each one sits in
    tools/ghost_names.py <tree>     # a tree other than this repo's disk/

WHY THIS EXISTS.  A program leaves the collection and the sentences that
named it stay behind.  `check_disk.py' catches that in the files it knows
are LISTS -- howto.psv, DOC/USAGE, DOC/ORIGINS and the rest -- and it
cannot catch it in prose, which is where most of the naming happens.

On 2026-09-19 this sweep found four, one of them in the worst possible
place:

  SYS/login      greeted every reader with "cat and less read; vi_nocio
                 edits" -- and vi_nocio came off the disk with the
                 twenty-six that went on terms.  That is the one line a
                 person sees before their first prompt.
  README-CIO     offered `sedt' as the trap-free editor to use instead of
                 *ed and *emacs, and listed CMDS/sedt among the programs
                 carrying the putc macro.
  DOC/INDEX      ended `ape' with "`travesty' and `newsgen' are the others
                 of its kind here".

A REPORT, NOT A GATE, and it has to be: most of what it prints is right.
The shipped text names the READER'S own OS-9 utilities on purpose -- that
is house style, `dir' and `del' and `free' are theirs and we say so -- and
it quotes C identifiers, option letters, adventure verbs (`get', `drop',
`quit', `examine') and ordinary words in backticks.  SKIP holds the ones
already judged; everything else is for a person to look at.

Run it after any removal.  The three that left today were all from one
commit, 3028969e, "26 programs off the disk on terms".
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DISK = os.path.join(REPO, "disk")

# The reader's own OS-9, named positively by design, plus the runtime
# modules that ship and the toolchain a reader builds with.
SKIP = set("""
cio cio020 math math881 csl csl020 fpu p2init shell dir del rename free procs
runb l68 c68 cc make ar tar os9exec bash ksh sh mdir makdir attr unlink list
more size chd chx pwd r68 debug dump load merge setime tmode xmode iniz deiniz
link os9gen format backup verify build echo date error printenv setpr kill
tsmon login copy cmp ident mfree sleep setenv logout mount iconv qsort
""".split())

# Words that are quoted as words, options, verbs or identifiers rather than
# as programs.  Judged once; add to it rather than re-judging.
# `cccp' is the one that needs its reason written down: DOC/rayshade tells
# the reader to MAKE it, `copy /dd/CMDS/GCC139/gcc_cccp /dd/cccp', because
# rayshade forks it by that bare name out of the data directory.  Named as an
# instruction, not as a claim that it is installed.
# `create', `insert', `start' and `exit' are a PROGRAM'S OWN commands quoted
# in its entry -- sdb's create and insert, the menu commands of the thing
# CATEGORIES is describing -- and `start' is also sieve's own output and an
# ordinary English word.  None of them was ever a file here.
PROSE = set("""
always auto break bye can compile configure copying copyright couldn deg done
double drop edit else endif examine extern float geometry get goin hjkl
homogeneous image include index inventory isam ldaa main never one ospeed ouch
out print prog psect quiet quit read receive save scale screens set shade
signed silly squares stars the thuh time trade tuh watch zee charattr equalprg
fprintf fwrite getc putc noreader epsonlo mfput polaroid spoolqueue coords
face damage chesstool dsave deldir e2e4 uuunexpand terminate tester syscmd
mortgage banners channel remote readstr wabbits which6 xshar
jpeg wermit cccp
create insert start exit rindex filter_pid
inetdb kwin kzc lcsys libgcc1_c libgcc2_gc osktag sect0boot sector0 warranty
tex_readme cpp
""".split())


# Names the shipped text deliberately describes as GONE -- "it was dropped",
# "it has since left the disk", a dated record of a sweep when it was still
# here.  Each was read and judged on 2026-09-19.  A name here that starts
# being written about as though it were present again will not be caught, so
# take one OUT when the sentences naming it go.
GONE = set("""
dearc fpu040 kermit_cio new_e rstory2 sedt travesty
vi_cio vi_nocio
""".split())


def on_disk(disk):
    """Every file anywhere under disk/, plus the names DOC/INDEX gives.

    EVERYWHERE, not just the program directories: the text names data files
    too -- `atprc' under DOC/ka9q, `palias' under USR/LIB/SMAIL -- and a
    scan that only walked CMDS called both of those ghosts.
    """
    names = set()
    for _, _, files in os.walk(disk):
        names |= set(files)
    index = os.path.join(disk, "DOC", "INDEX")
    if os.path.exists(index):
        text = open(index, "rb").read().decode("latin-1").replace("\r", "\n")
        names |= set(re.findall(r"^ {1,4}\*? ?([A-Za-z0-9_.][\w.]*)\s{2,}(?=\S)",
                                text, re.M))
    src = os.path.join(disk, "SRC")
    if os.path.isdir(src):
        names |= set(os.listdir(src))
    return names


def shipped_text(disk):
    """The text THIS COLLECTION wrote, not everything under DOC.

    DOC is mostly other people's documentation -- a GNU manual, elvis's own
    Readme, the TeXbook's companion files -- and those name programs from
    their own world quite properly.  Reading all of it would bury the four
    real hits in hundreds of those.  So: the files at the root of the disk,
    the documents at the top of DOC, SYS/login and SYS/motd (the two a
    reader meets before anything else), and any README-* ANYWHERE under
    DOC, which is how this collection names the pages it wrote itself --
    DOC/rayshade/README-RAYSHADE is one, and it held a violation.
    """
    for name in ("readme", "startup", "SOURCES.txt"):
        p = os.path.join(disk, name)
        if os.path.isfile(p):
            yield p
    for name in ("login", "motd"):
        p = os.path.join(disk, "SYS", name)
        if os.path.isfile(p):
            yield p
    doc = os.path.join(disk, "DOC")
    if os.path.isdir(doc):
        for f in sorted(os.listdir(doc)):
            p = os.path.join(doc, f)
            if os.path.isfile(p):
                yield p
        for base, _, files in os.walk(doc):
            if base == doc:
                continue
            for f in sorted(files):
                # `README-NAME' with the hyphen is this collection's own
                # naming for a page it wrote; a bare `README' in a
                # subdirectory is the archive's own, like DOC/cnews/README,
                # which is Henry Spencer's and names Unix programs from its
                # own world quite properly.
                if f.startswith("README-"):
                    yield os.path.join(base, f)


def main(argv):
    # A positional argument used to be ACCEPTED AND IGNORED, so
    # `ghost_names.py /some/other/tree' answered confidently about this
    # repo's own disk/.  That is the shape this collection keeps producing
    # -- a tool that cannot be made to fail because it never looks where it
    # is told.  Honour the path, and refuse one that is not a tree.
    paths = [a for a in argv if not a.startswith("-")]
    if len(paths) > 1:
        sys.stderr.write("ghost_names: one tree at a time\n")
        return 2
    disk = os.path.abspath(paths[0]) if paths else DISK
    if not os.path.isdir(disk):
        sys.stderr.write("ghost_names: %s is not a directory\n" % disk)
        return 2

    known = on_disk(disk) | SKIP | PROSE | GONE
    hits = {}
    for p in shipped_text(disk):
        try:
            text = open(p, "rb").read().decode("latin-1").replace("\r", "\n")
        except OSError:
            continue
        for m in re.finditer(r"`([a-z][a-z0-9_]{2,15})'", text):
            name = m.group(1)
            if name in known:
                continue
            line = text[:m.start()].count("\n") + 1
            where = os.path.relpath(p, REPO)
            if where.startswith(".."):
                where = p
            hits.setdefault(name, []).append((where, line,
                                              text.split("\n")[line - 1][:74]))
    for name in sorted(hits):
        print("%-16s %s" % (name,
                            " ".join(sorted({w for w, _, _ in hits[name]}))))
        if "--quotes" in argv:
            for w, n, line in hits[name]:
                print("%18s%s:%d  %s" % ("", w, n, line.strip()))
    print("\n%d name(s) the shipped text points at and the disk has not got"
          % len(hits))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
