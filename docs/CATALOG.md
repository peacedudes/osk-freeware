# What is on this disk

939 programs of OS-9/68K community software, gathered from the archives that kept it and made to run again. **570 of them need nothing but this disk**; the rest want Microware's `cio`, marked below with a star.

`DOC/INDEX` on the disk lists everything alphabetically. This is the same collection sorted by what each program is *for*, which is the more useful order when you do not yet know what you are looking for.

> Open a program in `docs/index.html` for its **sample output** --
> photographed from that program running on the disk image.
>
> Prefer to click around? `docs/index.html` is a searchable version with per-program detail — what it needs, where it came from, on what terms. GitHub will not render it here; download the repository and open it, or enable Pages.

| Category | Programs | |
|---|--:|---|
| [Shells](#shells) | 20 | Unix shells to sit beside OS-9's own -- bash and ksh bring history, job control, and scripts that come across unchanged. |
| [Editors](#editors) | 22 | vi and emacs in several flavours, line and stream editors, and editors for binary and hex. |
| [Text tools](#text-tools) | 113 | Search, sort, compare, reformat, split and spell-check. |
| [Files & directories](#files--directories) | 37 | Listing, copying, finding, renaming, and knowing what you have. |
| [Developer tools](#developer-tools) | 48 | Version control, tags, cross-reference, formatters, a debugger and benchmarks. |
| [Compilers & build](#compilers--build) | 39 | C compilers and their passes, assemblers, linkers, make and parser generators. |
| [Languages](#languages) | 10 | Interpreters and language systems beyond C. |
| [Archives & compression](#archives--compression) | 40 | Pack, unpack and shrink -- lha, zip, tar, arc, zoo, and OS-9 module libraries. |
| [Encoding & conversion](#encoding--conversion) | 24 | Between text encodings, line endings, Macintosh formats, ciphers and hashes. |
| [Communications](#communications) | 96 | Kermit in several builds, terminal sessions, and networking. |
| [Graphics & images](#graphics--images) | 202 | The netpbm toolkit, JPEG, a ray tracer, and things that draw. |
| [Games](#games) | 66 | Adventures, board and card games, arcade ports, dungeon crawls and puzzles. |
| [Screen toys](#screen-toys) | 9 | Animations and screen effects -- they draw on the terminal rather than print to it. Some run until you stop them. |
| [Amusements](#amusements) | 20 | Generators, simulators and diversions that are not quite games. |
| [System & modules](#system--modules) | 131 | OS-9 module and process tools, devices, system state and scheduling. |
| [Disk & DOS](#disk--dos) | 20 | Reading and writing MS-DOS media with the mtools set. |
| [Time & calendar](#time--calendar) | 14 | Calendars, clocks and astronomy. |
| [Maths & calculators](#maths--calculators) | 9 | Calculators, plotting, orbits and number theory. |
| [Printing](#printing) | 14 | Spoolers, page formatting and PostScript. |
| [Documentation](#documentation) | 5 | Pagers, readers and the help system. |

## Shells

*Unix shells to sit beside OS-9's own -- bash and ksh bring history, job control, and scripts that come across unchanged.*

<details><summary>20 programs</summary>

**Shell helpers**

| | |
|---|---|
| `checkenv` | &#9733; check env var<br>`Syntax: checkenv <eparam> , <evalue>` |
| `exist` | &#9733; test file existence |
| `getenv` | &#9733; print an environment variable<br>`USAGE: getenv [-n\|-p\|-l\|-x] <Environment> [<Wert>]` |
| `hist` | C-shell history + commandline editing  [no military use -- EFFO-INFO] |
| `if` | conditional execution for shell scripts (varval/loaded/def)<br>`Syntax: if [not] <cond> {<arg>} {<cmd1>} [else` |
| `printenv` | &#9733; print the environment<br>`Syntax:   printenv [<options>] [{<env var name}]` |
| `printf` | &#9733; formatted print from the shell.  IT WORKS, with one flaw: the literal text BEFORE THE FIRST CONVERSION is dropped. Everything between and after conversions is right -- `printf "%d %s %d\n" 4 "is bigger than " 3' prints `4 is bigger than  3', and `"a%db%dc\n" 1 2' prints `1b2c', losing only the leading `a'.  So begin the format with a conversion and nothing is lost.  The degenerate case of the same flaw: a format with NO conversion is entirely `before the first conversion', so it prints nothing. Measured 2026-08-29; the earlier note here said it floods `No more memory !!!', and it does not<br>`Usage: printf <format-string> [ arg1 . . . ]` |
| `qp` | &#9733; NOT a print helper: `qp <cmd> <args>' processes BACK-QUOTES for command expansion, which Microware's shell has no way to do. requires Microware's `shell' on your execution path -- it does the expansion by forking one, and produces nothing without it. Reworded 2026-08-30<br>`Syntax: qp <cmd> <arg1> ... <argn>` |
| `run` | run a program with stdio rebound to the terminal (needs PORT)<br>`Syntax: run '<prgname> {<arg>}'` |
| `xc` | execute commands from a file (needs a .xc) |

**Shell utilities**

| | |
|---|---|
| `env` | &#9733; Print or set the environment for a command (GNU)<br>`Usage: env [OPTION]... [-] [NAME=VALUE]... [COMMAND [ARG]...]` |
| `expr` | &#9733; Evaluate an expression (GNU) |
| `logname` | &#9733; Print your login name (GNU)<br>`Usage: logname [OPTION]...` |
| `su` | &#9733; Become another user (GNU)<br>`Usage: su [OPTION]... [-] [USER [ARG]...]` |
| `whoami` | &#9733; Print who you are logged in as (GNU)<br>`Usage: whoami [OPTION]...` |

**Shells**

| | |
|---|---|
| `bash` | GNU Bourne-Again Shell 1.12 -- this disk's shell; reads .bashrc<br>`usage: fc [-e ename] [-nlr] [first] [last] or fc -s [pat=rep] [command]` |
| `gshell` | GSHELL - a shell<br>**How:** Full-screen: it takes over the display. **control-C gets you out** -- tested, and none of q, Q, control-D or ESC did. If it has a quit command of its own, its documentation in DOC/ will say. |
| `ksh` | &#9733; Korn shell.  `ksh -c '<commands>'` works completely.  Its INTERACTIVE loop depends on the EMULATOR: it reads the command line with read(fd,buf,256), and os9exec's I$Read returned only when the full count arrived rather than at the end-of-record character, so no typed command ever reached it.  With that corrected, ksh is a full shell -- prompt, for loops, variables, forking.  DOC/README-KSH<br>`Syntax: 'setpr <prior>' or 'setpr <pid> [<pid>..] <prior>'` |
| `sh` | Bourne shell v7.5 -- what the startup script runs |
| `wish` | &#9733; WiSH - full-screen windowing shell over the OS-9 shell |

</details>

## Editors

*vi and emacs in several flavours, line and stream editors, and editors for binary and hex.*

<details><summary>22 programs</summary>

**Binary & hex**

| | |
|---|---|
| `beav` | BEAV 1.40 -- Binary Editor And Viewer (needs TERM)<br>**How:** Full-screen: it takes over the display. **control-C gets you out** -- tested, and none of q, Q, control-D or ESC did. If it has a quit command of its own, its documentation in DOC/ will say. |
| `hexed` | &#9733; hex editor via your text editor -- it writes its work file to /r0 and stops when it cannot.  See DOC/README-RUNNING  [no military use -- EFFO-INFO]<br>`Syntax: hexed [<opts>] <path> {[<opts>] \| [<path>]}` |
| `hexedit` | HEXPERT V2.4 by Dominic Alston -- `hexedit <file>'.  It reads TERMCAP as the capability string itself, not as the name of a file, so source `. /dd/SYS/termcap.entry' first and it draws its viewer; without that it prints the terminal type and exits.  gnuchess wants the same.  Its -d option is separately broken -- `file not accessible' (214) for a file that is readable.  `beav' is the binary editor that needs nothing, and `hexed' the one that would work if there were a RAM disk.  Corrected 2026-08-29<br>**How:** A hex editor -- Hexpert v2.4 by Dominic Alston. Takes a file: `hexedit <file>'. Needs `. /dd/SYS/termcap.entry' first or it will not draw. |
| `pbyte` | &#9733; patch bytes in a file at a hex offset<br>`Syntax: pbyte <path> <hex_offset> <hex_byte> [<hex_byte>]` |

**emacs family**

| | |
|---|---|
| `emacs` | &#9733; MicroEmacs 4.00<br>**How:** Full-screen editor, MicroEMACS key bindings. **control-X control-C quits** (exit-emacs) -- tested. Its macros and online help are in USR/LIB/EMACS. |
| `emacs.mm1` | &#9733; MicroEmacs macro module<br>**How:** Full-screen editor, MicroEMACS key bindings. **control-X control-C quits** (exit-emacs) -- tested. Its macros and online help are in USR/LIB/EMACS. |
| `me` | MicroEmacs 3.11 -- ADDED; needs TERM.  (memacs400 `emacs` needs cio)<br>**How:** Full-screen editor, MicroEMACS key bindings. **control-X control-C quits** (exit-emacs) -- tested. Its macros and online help are in USR/LIB/EMACS. |
| `mg` | &#9733; MicroGnuEmacs<br>**How:** Full-screen editor, MicroEMACS key bindings. **control-X control-C quits** (exit-emacs) -- tested. Its macros and online help are in USR/LIB/EMACS. |

**Line & stream**

| | |
|---|---|
| `ed` | &#9733; GNU ed 0.2 line editor -- it makes its temporary file at /r0, which os9exec cannot provide, and stops at once with `module not found'.  DOC/README-RUNNING lists the seventeen programs that reach for /r0<br>`Usage: ed [OPTION]... [FILE]` |
| `editor` | GSHELL front-end for the editor<br>**How:** Full-screen: it takes over the display. **control-C gets you out** -- tested, and none of q, Q, control-D or ESC did. If it has a quit command of its own, its documentation in DOC/ will say. |
| `sed` | &#9733; sed - stream editor.  SWAPPED 2026-08-28: what ships here is now the CMDS/REBUILT/sed_1.06 build, because the one that used to be here answered every script -- from a file or a pipe, on a four-line input -- with `No more memory !!!' and `Couldn't re-allocate memory'.  The one here now substitutes, deletes and prints with -n<br>`Syntax   : sed [<opts>] [<file>]` |

**vi clones**

| | |
|---|---|
| `elvis` | Elvis 1.7 -- the best-documented of this disk's three vi editors, and the one with the most options.  BUILT HERE from the source in CMDS/archives.  Needs TERM and TERMCAP; runs with no program under its other personalities and need elvis present to run. IT ALSO NEEDS A /dd/tmp, and the path is compiled in: on a /dd without that directory it stops before drawing anything with `Can't create temp file... Does directory "/dd/tmp" exist?'.  This disk ships one, so it bites on the machine you copy elvis TO.  Either `makdir /dd/tmp' or, before starting it, `setenv EXINIT "set directory=<a dir you have>"' -- elvis reads EXINIT before creating the temp file.  `vi' has the same compiled-in /dd/tmp; the PVIC builds do not.  Measured 2026-08-31; DOC/README-VI has the table<br>**How:** A full vi/ex clone, built here from the archive that was always on this disk. Needs TERM and TERMCAP set -- `SYS/login' does both. `view' opens read-only, REBUILT/vi.elvis is the same program as vi, and all of them need CMDS/elvis present because they exec it. |
| `elvis_input` | elvis under its `input' personality -- it opens already in insert mode.  RENAMED from `input.elvis' 2026-08-31, and the name is load-bearing: elvis's wrapper picks its personality from the LAST LETTER of the name it was invoked by, so under `input.elvis' it fell through to plain vi and the personality never happened.  Measured both ways with the same bytes. CMDS/input is a different program entirely |
| `elvprsv` | Preserve an elvis session across a crash |
| `elvrec` | Recover a preserved elvis session<br>`usage: elvrec [preserved_file [recovery_file]]` |
| `vi.elvis` | elvis 1.7 as vi.  CMDS/vi is the EFFO build and CMDS/vi_nocio is PVic -- three unrelated vi clones |
| `view` | elvis opened read-only |

**vi family**

| | |
|---|---|
| `sedt` | &#9733; SEDT screen editor -- the third build of the same editor, and it needs SYS/sedt.keys like the other two.  All three run now |
| `vi` | &#9733; the real vi/ex, and it keeps the name -- its source in SRC/effo_vi is the Berkeley ex source itself, not a clone. `vi -x' is ex, `vi -d' is edit.  See DOC/README-VI.<br>**How:** One of three unrelated vi editors here, and the only one that is the genuine Berkeley ex/vi rather than a clone -- its source in SRC/effo_vi is the real ex_*.c files. `vi -x' becomes ex, `vi -d' becomes edit. DOC/README-VI compares all three. |
| `vi_1.0` | PVIC 1.0, public domain      -> /dd/CMDS/REBUILT (name was taken) and CMDS/vi_nocio are PVIC 1.0a<br>`Usage: vi [file ...]` |
| `vi_cio` | &#9733; PVic vi, cio build (use vi_nocio instead)<br>**How:** PVic vi, the cio build. Needs `. /dd/SYS/termcap.entry' first, then it opens on an empty buffer. CMDS/vi_nocio is the same editor needing no module; DOC/README-VI compares all three vi editors here. |
| `vi_nocio` | PVIC 1.0a -- the smallest of this disk's three vi editors, public domain.  See DOC/README-VI to choose between them<br>**How:** PVIC 1.0a, the smallest of the three vi editors on this disk, public domain, no source or docs here. DOC/README-VI compares it with vi and elvis. |

</details>

## Text tools

*Search, sort, compare, reformat, split and spell-check.*

<details><summary>113 programs</summary>

**Banners & text art**

| | |
|---|---|
| `banner` | &#9733; print large banner text |
| `cursive` | generate a horizontal cursive banner<br>`usage: cursive [-tn] [-in] message` |
| `gothic` | &#9733; print text as a gothic/blackletter banner |

**Count & inspect**

| | |
|---|---|
| `ascii` | &#9733; ASCII character table |
| `dump` | hex dump of a file or module<br>`Syntax: dump [<opts>] <path/module> [<opts>] [<starting byte>] [<opts>]` |
| `file` | Identify file types.  SYS/magic is now here, so it names real formats -- "GIF picture ver. 87a 320 x 200, interlaced, 256 colors" -- and not just OS-9 modules<br>**How:** Names real formats now that SYS/magic is here: `file /dd/DEMO/gulls.gif' reports the GIF version, size and colour count. Before the magic file arrived it could only recognise OS-9 modules. |
| `gdd` | &#9733; GNU dd -- `gdd if=<file> of=<file> bs=<n> skip= seek= count=' -- a block copier and converter, not a dump.  `dump' and `od' are the dumps here.  Corrected 2026-08-29<br>**How:** A data dump -- like `od', with GNU-style long options. Needs Microware's cio. |
| `strings` | &#9733; extract printable strings, reported as $offset: <text><br>`Usage: strings [-anpl=n] [file [file]]` |
| `tail` | &#9733; last lines of a file -- DESIGNA's, and it takes `-l=<n>', not GNU's `-n <n>', which it rejects as an unknown option.  `head' on this disk IS the GNU one and takes -n: two conventions, one disk |
| `wc` | count lines/words/chars; counts CR or LF lines.  Where this build came from is NOT established -- it was long listed as ours, built with gcc2, and the evidence is against that: it is starred, and a gcc2 build here links clibn and needs no cio.  The three commands listed beside it turned out to be archive binaries.  No source and no second copy has been found in this repo or the archive pool |
| `wc.cio` | &#9733; archived build.  It COUNTS CORRECTLY -- `1 lines, 6 words, 40 chars' where `wc' says `1 6 40' -- but only on standard input: it prints nothing for a file argument, which is why `wc' is still the gcc2 build.  Refined 2026-08-29 |

**DVI drivers**

| | |
|---|---|
| `dvialw` | DVI to Apple LaserWriter<br>`Usage: dvialw [opts] dvifiles` |
| `dvidjp` | DVI to HP DeskJet Plus<br>`Usage: dvidjp [opts] dvifiles` |
| `dvieps` | DVI to Epson<br>`Usage: dvieps [opts] dvifiles` |
| `dviimp` | DVI to Imagen<br>`Usage: dviimp [opts] dvifiles` |
| `dvijep` | DVI to HP LaserJet Plus<br>`Usage: dvijep [opts] dvifiles` |
| `dvijet` | DVI to HP LaserJet<br>`Usage: dvijet [opts] dvifiles` |
| `dvilj2` | DVI to HP LaserJet II<br>`Usage: dvilj2 [opts] dvifiles` |
| `dvimac` | DVI to Macintosh<br>`Usage: dvimac [opts] dvifiles` |
| `dvioki` | DVI to Okidata<br>`Usage: dvioki [opts] dvifiles` |
| `dvitos` | DVI to Toshiba<br>`Usage: dvitos [opts] dvifiles` |

**Filters**

| | |
|---|---|
| `charcnt` | &#9733; Count characters in a file (Carl Kreider) |
| `expand` | Turn tabs into spaces (GNU)<br>`Usage: expand [-tab1[,tab2[,...]]] [-t tab1[,tab2[,...]]] [-i]` |
| `head` | First lines of a file -- `head -n 20 file'.  These GNU builds want -n 20, not -20<br>**How:** First lines of a file. This GNU build wants `head -n 20 file' -- the older `head -20' form is rejected as an unrecognized option. Needs cio. |
| `split` | Split a file into pieces (GNU)<br>`Usage: split [-lines] [-l lines] [-b bytes[km]] [-C bytes[km]] [+lines=lines]` |
| `subber` | &#9733; Substitute text in a stream, ,old,new style (Carl Kreider)<br>`Usage : subber <opts> wordlist <filename>` |
| `sum` | Checksum and block count (GNU) |
| `tac` | Print a file backwards, last line first (GNU)<br>**How:** Prints a file backwards, last line first -- cat's mirror image. Needs cio. |
| `tcmp` | &#9733; Compare two text files (Carl Kreider)<br>`Usage:  tcmp [options] file1 file2` |
| `unexpand` | Turn leading spaces back into tabs (GNU)<br>`Usage: unexpand [-tab1[,tab2[,...]]] [-t tab1[,tab2[,...]]] [-a]` |
| `unp` | &#9733; Strip unprintable characters from a stream (Carl Kreider)<br>`Usage:  unp [-?] [file]` |

**Format & typeset**

| | |
|---|---|
| `fmt` | Simple text formatter (elvis 1.7)<br>`usage: fmt [-width] [files]...` |
| `hc` | NOT a calculator, whatever the index said until 2026-08-31: it shifts text to a column, or labels every line.  `hc +8 f' indents f so the text starts at column 8, `hc -11 f' strips the leading columns so it starts at column 11, and `hc -l "> " f' puts that string in front of every line.  With no option it copies the file through.  Measured 2026-08-31; it evaluates nothing |
| `lout` | Lout 2.05 document formatter (Basser Lout, Jeffrey Kingston)<br>`usage: -o<filename>` |
| `nroff` | &#9733; nroff text formatter -- and it PRINTS NOTHING here, from a file or from standard input, with or without -man and with TMACDIR set.  Worse than that: given a file it does not come back at all, and the session has to be stopped. `roff' and `proff' beside it DO work -- the claim here that they fail the same way was wrong and is corrected 2026-08-29.  Use one of those<br>**How:** Formats man pages -- but it NEVER RETURNS on this disk, and prints nothing first. Measured 2026-08-29 both ways, `nroff -man /dd/DOC/netpbm/pnmscale.1' and the same file on stdin; each hung the session. The -man macros in LIB/tmac.an were extended for this collection because the originals defined only .TH .SH .SS .PP and .I, and LIB/orig.tmac.an is the untouched version -- neither has been shown to matter while the program will not finish. `roff' is the formatter that works. |
| `proff` | proff - portable roff text formatter (macros in LIB/proff). IT WORKS: given a text file it justifies it to a measure, and takes page ranges and a statistics option.  The note here that said it prints nothing was wrong; corrected 2026-08-29.  `roff' works too; `nroff' wants a real macro package and answers `illegal switch' to -?<br>`usage: proff [+n] [-n] [-v] [-ifile] [-s] [-pon] [infile [outfile]]` |
| `roff` | roff text formatter, and it works: `roff -?' gives its syntax and page-range options.  Corrected 2026-08-29<br>`Syntax: roff {[+00] [-00] [-s] -[h] file}` |
| `tformat` | text formatter (SNOBOL4-in-C)<br>`Usage: tformat [width\|-?] [<infile] [>outfile]` |

**Fortune & sayings**

| | |
|---|---|
| `cookhash` | &#9733; build the hash file cookie(1) needs, from a sayings file<br>`usage: cookhash <cookiefile >hashfile` |
| `cookie` | print a random fortune cookie<br>`usage: cookie cookiefile hashfile` |
| `fortune` | print a random quotation<br>`usage:  fortune [ - ] [ -wsloa ] [ file ]` |
| `sonnet` | writes (bad) sonnets in iambic pentameter, curses-based<br>**How:** Full-screen: it takes over the display. **ESC quits** -- tested. (control-C also gets you out, but ESC is the program's own way.) |
| `strfile` | &#9733; build fortune's index file<br>`usage:  strfile [ - ] [ -cC ] [ -sv ] inputfile [ datafile ]` |
| `unstr` | &#9733; reverse strfile - dump a fortune index.  It FLOODS `No more memory !!!' and dumps nothing<br>`usage: unstr datafile[.dat] [ outfile ]` |

**KWIC index**

| | |
|---|---|
| `pagefraz` | &#9733; KWIC suite - phrase extractor<br>`Syntax: pagefraz <opts> [<in_path> [<out_path>]] <opts>` |
| `pagekwic` | &#9733; KWIC suite - split a Stylo file to one phrase per line with page no.<br>`Syntax: pagekwic <opts> [<in_path> [<out_path>]] <opts>` |
| `pageline` | KWIC suite - line/page numbering<br>`Syntax: pageline <opts> [<in_path> [<out_path>]] <opts>` |

**Search & match**

| | |
|---|---|
| `bm` | &#9733; bm - fast grep utility (Boyer-Moore) |
| `bmgtest` | &#9733; Boyer-Moore-Gosper substring search demo<br>**How:** bmgtest [-i] [-n] <pattern> [file ...]. A demonstration of Boyer-Moore-Gosper searching, not a tool you would use. |
| `bmgtest2` | &#9733; Boyer-Moore-Gosper substring search demo (variant)<br>`usage: bmgtest [-i] [-n] pattern [file ...]` |
| `fgrep` | &#9733; very fast grep utility<br>`usage: fgrep [-[[AB] ]<num>] [-[CVchilnsvwx]] [-[ef]] <expr> [<files...>]` |
| `grep` | GNU grep 2.0 -- pattern search<br>`usage: grep [-[[AB] ]<num>] [-[CEFGVchilnqsvwx]] [-[ef]] <expr> [<files...>]` |
| `soundex` | Soundex phonetic key for each word on stdin |

**Sort, compare & merge**

| | |
|---|---|
| `cdiff` | &#9733; context diff |
| `diff` | &#9733; GNU diff 1.1 -- ADDED; the disk had no diff at all.  Verified on CR files<br>`Usage: diff [-options] file1 file2` |
| `ediff` | visual file compare<br>`Syntax   : 'ediff <file'  or  'diff <f1> <f2> ! ediff'` |
| `fcomp` | &#9733; compare two text files<br>`Syntax: fcomp <file_1> <file_2>` |
| `join` | GNU join -- relational join of two sorted files<br>`Usage: join [-a 1\|2] [-v 1\|2] [-e empty-string] [-o field-list...] [-t char]` |
| `nsort` | NOT a numeric sort, whatever the name says: given 3, 22, 111 and 4 it answers 111, 22, 3, 4 -- the same lexical order GNU `sort' gives with no options.  `sort -n' is the numeric sort here and gets it right.  It reads standard input only.  Corrected 2026-08-29<br>`Usage: nsort <unordered >sorted` |
| `qsort9` | &#9733; sort filter<br>`Syntax: qsort9 [<opts>] [<srcpath>] [<opts>]` |
| `sort` | GNU sort<br>`Usage: sort [-cmus] [-t separator] [-o output-file] [-bdfiMnr] [+POS1 [-POS2]]` |
| `spiff` | &#9733; tolerant diff - ignores formatting noise<br>**How:** Compares two files while ignoring differences that do not matter (whitespace, number formatting). Takes TWO filenames. |
| `unip` | unique lines with page numbers<br>`Syntax: unip [<opts>] [<srcpath>] [<opts>]` |
| `uniq` | &#9733; drop duplicate lines<br>`Usage: UNIQ [-u][-d][-c] [-n] [^n] input [>output]` |

**Spelling & words**

| | |
|---|---|
| `buildhash` | build ispell's dictionary hash (writes LIB/ispell.hash) |
| `ispell` | interactive spelling checker<br>**How:** Interactive spelling checker. Takes a file: `ispell <file>'. `ispell -a' is the pipe interface programs use. |
| `jargon` | Jargon-file browser (needs its database files)<br>**How:** A browser for the Jargon File, which is here: VH/jargon.txt, version 3.0.0 of 27 July 1993, with its index. It will not read SYS/termcap -- do `. /dd/SYS/termcap.entry' first, then `jargon -m'. Tested. |
| `makelex` | &#9733; compiles sonnet's lex.data word list into a C array |
| `speech` | English-to-phoneme translation<br>`Usage: PHONEME [infile [outfile]]` |

**Split & join**

| | |
|---|---|
| `sepwords` | split a file to one word per line<br>`Syntax: sepwords [<in_path> [<out_path>]]` |
| `splitalf` | &#9733; split a file alphabetically<br>`Syntax: splitalf <opts> [<in_path>] <opts>` |

**TeX**

| | |
|---|---|
| `afm2tfm` | Adobe font metrics to TeX font metrics<br>`Usage: afm2tfm foo[.afm] [-O] [-v\|-V bar[.vpl]]` |
| `bibtex` | BibTeX -- bibliography formatter |
| `dvips` | DVI to PostScript -- pair it with gs33<br>**How:** DVI to PostScript. `dvips <file>.dvi'. Pair it with gs33 (ETC/LIB/GS33) to see the result without a printer. |
| `dvitype` | show what is inside a .dvi file, as text<br>**How:** Shows what is inside a .dvi file as readable text. `dvitype <file>.dvi', then it asks for an output level -- 4 is a complete listing, 0 errors only. |
| `gftopk` | MetaFont generic font to packed font<br>`Usage: gftopk [-v] <gf file> [pk file].` |
| `gftype` | show what is inside a .gf file<br>`Usage: gftype [-m] [-i] <gf file>.` |
| `inimf` | MetaFont with no base preloaded |
| `initex` | TeX with no format preloaded, for building .fmt files<br>**How:** TeX with no format preloaded -- this is what BUILDS the .fmt files. `initex "plain \dump"'. The three formats already ship in SYS/TEX/FORMATS, built this way, so you only need this to make your own. |
| `latex` | LaTeX -- Lamport's document preparation system on top of TeX<br>**How:** LaTeX. Its format is SYS/TEX/FORMATS/lplain.fmt, already built: `virtex "&/dd/SYS/TEX/FORMATS/lplain <file>.tex"'. |
| `maketexpk` | generate a .pk font at the size TeX asked for |
| `pktogf` | packed font back to generic font<br>`Usage: pktogf [-v] <pk file> [gf file].` |
| `pktype` | show what is inside a .pk file<br>`Usage: pktype <pk file>.` |
| `pltotf` | property list to TeX font metric<br>`Usage: pltotf [-verbose] <property list file> <tfm file>.` |
| `slitex` | SliTeX -- LaTeX for slides<br>**How:** LaTeX for slides; its format is SYS/TEX/FORMATS/splain.fmt, already built. |
| `tangle` | WEB to Pascal -- Knuth's literate programming tool<br>`Usage: tangle webfile[.web] [changefile[.ch]].` |
| `tex` | TeX itself -- the typesetting program (a driver; virtex does the work) |
| `texidx` | build an index from TeX's .idx output |
| `tftopl` | TeX font metric to property list (the readable form)<br>`Usage: tftopl [-verbose] <tfm file> [<property list file>].` |
| `vftovp` | virtual font to virtual property list<br>`Usage: <vfm file> <tfm file> <vpl file>.` |
| `virmf` | the real MetaFont engine -- generates fonts from .mf sources |
| `virtex` | the real TeX engine, loaded with a format<br>**How:** The real TeX engine. It needs a FORMAT: `virtex "&/dd/SYS/TEX/FORMATS/plain <file>.tex"'. Tested end to end -- it typesets and reports "Output written on <file>.dvi". `tex' is a small driver in front of it. |
| `vptovf` | virtual property list to virtual font<br>`Usage: vptovf <vpl file> <vfm file> <tfm file>.` |
| `weave` | WEB to TeX -- the other half of literate programming<br>`Usage: weave webfile[.web] [changefile[.ch]] [-x].` |

**Transform & filter**

| | |
|---|---|
| `ape` | &#9733; writes GIBBERISH in the style of whatever it is given -- a travesty generator, not a text filter.  `travesty' and `newsgen' are the others of its kind here.  Clarified 2026-08-29 |
| `autolf` | &#9733; Mike Tozer's line-ending converter, 1995, and THE ONE THAT WORKS: it turns CR into CRLF or LF and back, expands tabs, and handles ^Z.  Use it as a FILTER -- `autolf -c -C -L < in > out' makes DOS text out of OS-9 text, 40 bytes in and 41 out with 0D 0A at the end.  Given a FILENAME it converts in place through a temporary and then cannot rename it back -- this C library has no rename(), the same wall zip and arc hit.  `-H' explains the conversions.  It is what `todos' and `toos9' were supposed to be.  Measured 2026-08-29<br>`Usage:   autolf [<opts>] {<file names> [<opts>]}` |
| `casefix` | normalise letter case in a text file |
| `cut` | cut selected fields from each line |
| `cuts` | &#9733; Coco Usenet Transfer Utility<br>`Usage: cuts <-d> [-o name] <file>...` |
| `detab` | &#9733; tabs to spaces<br>`Usage: detab [-tn] [infile] or [<infile]` |
| `eo` | &#9733; eo - text utility |
| `field` | &#9733; extract fields<br>`Syntax  : field [<opts>] <fields...> [<opts>]` |
| `fillup` | &#9733; fill a file up to a given length with a constant byte<br>`Syntax:   fillup [<options>] <file>` |
| `gawk` | &#9733; GNU awk 2.11 -- the pattern-and-action language.  It works, but it IGNORES A FILENAME ARGUMENT and reads standard input whatever it is given, so redirect: gawk '{...}' < file, never gawk '{...}' file.  Named a file, it sits waiting on the terminal, which is what the 2026-08-27 note here called "prints nothing at all".  Corrected 2026-08-28.<br>**How:** GNU awk 2.11, the first awk this disk has ever carried. Needs Microware's cio. `gawk "{print \$1}" file' -- and mind that the OS-9 shell, not gawk, is what mangles quoting. |
| `gep` | &#9733; global expression parser - grep-like filter<br>`Syntax: gep [<opts>] [<srcpath>] [<opts>]` |
| `paste` | merge lines of files<br>`USAGE: paste [-s] [-d<list>] files` |
| `pep` | file 'detergent' - strip junk from files<br>`Usage: pep [options] [filename ...]` |
| `psc` | &#9733; sc's print/format filter<br>`Syntax: psc [-rkfLSPv?] [-s v] [-R i] [-C i] [-n i] [-d c] [<path1] [>path2]` |
| `rot` | turn a text file on its side -- line one becomes column one.  NOT a rot-13 cipher, whatever the name suggests |
| `shuffle` | shuffle lines/cards<br>**How:** Full-screen: it takes over the display. **`q' quits** -- tested. |
| `tabs` | tab/space conversion filter<br>`Syntax   : tabs [<opts>] [<input_redirection>] [<output_redirection>]` |
| `upperdir` | Normalise case: files lowercase, dirs uppercase<br>`Usage: UpperDir [directory name]` |
| `valspeak` | &#9733; Valley-speak text filter -- prints nothing, from a file or from a pipe |

</details>

## Files & directories

*Listing, copying, finding, renaming, and knowing what you have.*

<details><summary>37 programs</summary>

**Attributes**

| | |
|---|---|
| `fstat` | Report a file's status and attributes<br>`Syntax: FStat [<opts>] <file1> [<opts>]` |

**Attributes & ownership**

| | |
|---|---|
| `chgrp` | &#9733; change group<br>`Usage:  chgrp [-z] {numerical-gid \| username} [file [... file]]` |
| `chown` | &#9733; change owner<br>`Usage:  chown [-z] {numerical-uid \| username} [file [... file]]` |
| `eset` | &#9733; set an OS-9 event to a value -- eset <event> <num><br>`Syntax: eset <event> <num> [<opts>]` |
| `owner` | &#9733; CHANGE a file's owner, not show it -- `owner <user> <file> ...', super user only.  Run with a file it prints its usage; run as `owner <file>' it reads the filename as a user name and answers `No such user'.  `fstat' and `ls -l' are what SHOW an owner.  Corrected 2026-08-29<br>`Usage: owner user file file ...` |

**Copy, move, delete**

| | |
|---|---|
| `cp` | &#9733; copy files -- and it WORKS: the bytes come back byte for byte.  Run with NO arguments it prints its usage and then takes a bus error inside I$Open, which is how it comes to sit in DOC/STATUS's crash list<br>`Usage: cp file1 file2` |
| `dback` | Directory backup utility (wants a /d0 device)<br>`Usage: Dback [-options] <fromdir> <todir> [-options]` |
| `delbak` | &#9733; delete backup files (*_bak) in a directory tree<br>`Usage: delbak [-options] [directory] [-options]` |
| `divide` | &#9733; SPLIT A FILE into pieces -- Farside Systems 1992, `divide -l=<lines> <infile> [<outfile>]'.  Not integer division, whatever the name suggests |
| `eunlink` | &#9733; extended unlink<br>`Syntax: eunlink {<event>}` |
| `fc` | &#9733; split a big file in two, to carry it on 360k disks<br>`Syntax:   fc [<file>]` |
| `move` | &#9733; move files between directories<br>`Syntax:   move [<options>] <from> [<to>] [<options>]` |
| `mv` | &#9733; move/rename<br>`Usage: mv [-bfiuv] [-S backup-suffix] [-V {numbered,existing,simple}]` |
| `remove` | &#9733; remove files, with confirmation<br>`Syntax   : remove [<opt>] [<modules>] [<opt>] [<modules>] [<opt>]` |
| `rm` | &#9733; remove files<br>`Usage: rm [-dfirvPR] [+directory] [+force] [+interactive] [+recursive]` |
| `undel` | &#9733; undelete a file<br>`Usage: attr <file> -d` |

**Create & rename**

| | |
|---|---|
| `mkdir` | &#9733; make directory<br>`Usage: mkdir [-p] [-m mode] [+path] [+mode mode] dir...` |
| `rendsk` | &#9733; rename a disk volume<br>`Syntax:   rendsk [<opts>] <disk device> <new name>` |

**Find & compare**

| | |
|---|---|
| `dfiles` | &#9733; find duplicate files on disk and issue the cmp commands |
| `du` | &#9733; disk usage, by directory<br>`Syntax: du <directory>` |
| `ff` | &#9733; find files by name -- ff [<opts>] <name>... |
| `find` | &#9733; find 1.1.5 -- search a directory tree, and NOT with the Unix syntax: `-n=<name>' matches, `-o' prints what it found, and `find <dir> -name x -print' answers `only one parameter allowed'<br>`Syntax: find {<opts>} [<path>]` |
| `space` | &#9733; effective disk usage  [conditions apply -- run `help space`]<br>`Syntax:   space [<opts>] {<dir/file path>} [<opts>]` |

**Home Librarian**

| | |
|---|---|
| `Ascii2Libr` | Home Librarian: rebuild a catalogue from a plain-text file<br>`Syntax: Ascii2Libr [opts]` |
| `EditLibr` | Home Librarian: edit a catalogue<br>**How:** Part of the HL10 librarian set. Wants an edit file as a parameter; `EditLibr' alone prints its syntax. |
| `Libr2Ascii` | Home Librarian: dump a catalogue to plain text<br>`Syntax: Libr2Ascii [opts]` |
| `Librarian` | Home Librarian: search a catalogue.  SIX PROGRAMS AND THEIR DOCS TRAVEL TOGETHER -- its licence requires it<br>**How:** One of six Home Librarian programs that must stay together -- its licence says so. Start here to search a catalogue; EditLibr edits one, Ascii2Libr builds one from text, Libr2Ascii dumps it back, PrintCards and PrintLabels print it. Manual in DOC/homelibr. |
| `PrintCards` | Home Librarian: print catalogue cards<br>`Syntax: PrintCards [opts]` |
| `PrintLabels` | Home Librarian: print labels<br>`Syntax: PrintLabels [opts]` |

**List & navigate**

| | |
|---|---|
| `dir` | &#9733; directory listing.  PATCHED HERE: its moveq #128 was sign-extended to -128; see DOC/STATUS<br>`Syntax: dir [<opts>] {<dir names> [<opts>]}` |
| `dm` | &#9733; Disk Master 1.4, a full-screen disk and directory browser. requires Microware's `shell' on your execution path: it runs the commands it offers through system(), which forks a program of that name.  With one present it runs completely -- measured 2026-08-28.  Reworded 2026-08-30<br>**How:** Disk Master 1.4, a full-screen disk browser. REQUIRES MICROWARE'S `shell` on your execution path -- it runs the commands it offers through system(). With one present it runs completely. |
| `edir` | &#9733; list the EVENT directory -- OS-9 events and their values. Nothing to do with `dir'<br>`Syntax: edir [<opts>]` |
| `l` | &#9733; brief directory listing -- but it answers `not accessable, error: 214' for every directory tried here<br>`Usage: l [-options] [file] [file] [-options]` |
| `ls` | GNU ls (fileutils 3.13) -- OUR OWN FIXED BUILD: real stat(), columns, -al<br>`Usage: ls [OPTION]... [FILE]...` |
| `tree` | Print a directory tree -- BUT fails on this disk: it opens the raw device (/dd@), which a host-native disk has no equivalent for<br>`Syntax: tree [<directory>] [<opts>]` |

**Paths**

| | |
|---|---|
| `basename` | &#9733; strip directory from a pathname (M.C. Gregorie, 1994)<br>`Syntax:   basename <path> [<suffix>]` |
| `dirname` | &#9733; strip filename from a pathname (M.C. Gregorie, 1994)<br>`Syntax:   dirname <path>` |

</details>

## Developer tools

*Version control, tags, cross-reference, formatters, a debugger and benchmarks.*

<details><summary>48 programs</summary>

**Assembly**

| | |
|---|---|
| `tab` | Tabulate 6809 or 68000 assembly source -- opcode-aware, and works on code that will not assemble<br>`Syntax: tab [<opts>]` |
| `xlate` | &#9733; Translate 6809 assembly source to 68000<br>**How:** Translates 6809 assembly source into 68000. Pairs with as09 (the 6809 assembler on this disk) and with `tab', which tabulates either dialect. Needs cio. |

**Benchmarks**

| | |
|---|---|
| `dhry` | Microware cc<br>**How:** Dhrystone 2.0. Twelve builds of the same source sit in CMDS/DHRY -- run several and compare, which is what tells you the compiler's cost. Under os9exec the number describes the host machine, not a 68000. |
| `dhryGcc` | &#9733; GCC 1.x |
| `dhryGcc2` | &#9733; GCC 2.x |
| `dhryGcc2in` | &#9733; GCC 2.x, inlined |
| `dhryGcc2mx` | &#9733; GCC 2.x, mixed |
| `dhryGcc2o2` | &#9733; GCC 2.x, optimised |
| `dhryGccin` | &#9733; GCC 1.x, inlined |
| `dhryGccmx` | &#9733; GCC 1.x, mixed |
| `dhryGcco2` | &#9733; GCC 1.x, optimised |
| `dhryO2` | Microware cc, optimised |
| `dhryshamu` | &#9733; Shamus build |
| `dhryshamu2` | &#9733; Shamus build, second variant |
| `disktest` | measure disk performance  [no military use -- DOC/EFFO-INFO]<br>`Syntax   : disktest [<opt>]` |
| `fibo` | &#9733; Fibonacci benchmark |
| `float` | &#9733; floating-point benchmark |
| `paranoia` | &#9733; floating-point benchmark |
| `savage` | &#9733; Savage floating-point accuracy benchmark |
| `sieve` | &#9733; sieve of Eratosthenes benchmark |
| `time` | &#9733; time a command |
| `timid` | timing utility<br>`Syntax: timit [<opts>]` |

**Debugging**

| | |
|---|---|
| `sdb` | SDB 2.0 - symbolic debugger |
| `trap` | &#9733; system-state trap-handler example -- it cannot install one from user state, and loading `math' does not change that. Ask for it by PATH: `trap' is a bash builtin too, and the builtin answers first and silently.  Measured 2026-08-29<br>**How:** The trap-handler example, and it does NOT work: it wants system state and says "Can't install trap handler" from user state, with or without `math' loaded. Ask for it BY PATH -- `/dd/CMDS/trap' -- because `trap' is also a bash builtin, and the builtin answers first, silently, which looks exactly like success. Measured 2026-08-29. |

**Libraries**

| | |
|---|---|
| `libsplit` | Split a linker library into its component modules<br>`Syntax   : [<opts>] {<library>} [<opts>]` |

**Source checking**

| | |
|---|---|
| `bcheck` | &#9733; count brackets in a source file and report a mismatch -- it is not a boot-file checker.  Corrected 2026-08-28<br>`Syntax: bcheck [<opt>] [<filename>]` |
| `ccheck` | &#9733; C program checker -- matching brackets, quotes, comment brackets, and indentation that disagrees with them<br>**How:** Checks C source for mismatched brackets, quotes and comment markers, and for indentation that disagrees with the nesting. Needs cio. |
| `checkfile` | &#9733; Check a C source file for structural mistakes.  Wants TERM<br>**How:** Full-screen: it takes over the display. **`q' quits** -- tested. |

**Source formatting**

| | |
|---|---|
| `cb` | &#9733; C beautifier<br>`Usage:  cb <input.fil >output.fil` |
| `cpr` | print/pretty-list C source files<br>`Usage: cpr [-cCnNsS] [-T title] [-t tabwidth] [-p[num]] [-r[num]] [-l pagelength] [[-f] file] ...` |
| `ifdef` | resolve #ifdefs in C source<br>`Syntax: ifdef [<opts>] [<file>] [<opts>]` |
| `indent` | reformat a C source program for readability<br>`Syntax: indent [<opts>] [<inpath> [<outpath>]] [<opts>]` |
| `patch` | Larry Wall's patch - apply a diff -- it recognises a diff and then CANNOT FINISH: `Error reading tmp file /dd/tmp/patchi000003'.  The file it was patching is left alone.  `diff' itself works |
| `unifdef` | &#9733; remove #ifdef sections from C source<br>`syntax: unifdef {<opts>} [<file>]` |

**Source navigation**

| | |
|---|---|
| `ctags` | generate a vi tags file from C source (BSD)<br>`usage: ctags [-BFadtuwvx] [-f tagsfile] file ...` |
| `cxref` | &#9733; C cross-reference lister -- numbered listing + symbol table<br>`Syntax:		cxref [-opts] [path]` |
| `etags` | &#9733; generate an emacs TAGS file<br>`Syntax: etags { [<opts>] <path> }` |
| `rdoc` | &#9733; reverse documentation: C source in, structure chart out |
| `xrf` | &#9733; C cross-reference generator -- it wants its language table, `C.XRF', in the CURRENT DATA DIRECTORY.  The disk has it as DOC/xrf/c.xrf; copy that beside your source or it stops with `Cannot open Language Table file' |

**Tags**

| | |
|---|---|
| `ctags.elvis` | elvis 1.7's ctags; CMDS/ctags is the BSD one<br>`usage: ctags [flags] filenames...` |
| `ref` | Look up a C function's declaration from a tags file<br>`usage: ref [-t] [-c class] [-f file] tag` |

**Version control**

| | |
|---|---|
| `ci` | &#9733; RCS check in |
| `co` | &#9733; RCS check out |
| `rcs` | &#9733; RCS |
| `rcsdiff` | &#9733; RCS diff |
| `rcsident` | &#9733; RCS ident |
| `rcsmerge` | &#9733; RCS merge |
| `rlog` | &#9733; RCS log |

</details>

## Compilers & build

*C compilers and their passes, assemblers, linkers, make and parser generators.*

<details><summary>39 programs</summary>

**Assemblers & linkers**

| | |
|---|---|
| `as0` | 6800/6802 cross-assembler (xasm).  NOT a 68000 assembler -- see the note below this list<br>**How:** A 6800 cross-assembler, not a 68000 one -- as1 is 6801, as4 is 6804, as5 is 6805, as11 is 68HC11 and as09 is 6809. DOC/xasm/asm.doc is their manual; source for all of them is in SRC/xasm. |
| `as09` | &#9733; 6809 assembler<br>`Usage: as09 [files]` |
| `as1` | 6801/6803 cross-assembler (xasm)<br>`Usage: as1 [files]` |
| `as11` | 68HC11 cross-assembler (xasm)<br>`Usage: as11 [files]` |
| `as4` | 6804 cross-assembler (xasm)<br>`Usage: as4 [files]` |
| `as5` | 6805/68HC05 cross-assembler (xasm)<br>`Usage: as5 [files]` |
| `lnk` | RTF FORTRAN link driver; calls l68 with /h0/LIB/sys.l, which is Microware's and not here |
| `lnk.org` | as lnk, the original build |

**C toolchain**

| | |
|---|---|
| `cc1plus` | GCC 2.x C++ compiler pass, where it was built |
| `cc2` | GCC 2.x C compiler pass, where it was built |
| `cc2plus` | GCC 2.x C++ pass, second form |
| `cccp2` | &#9733; GCC 2.x preprocessor, where it was built<br>`Usage: cccp2 [switches] input output` |
| `collect` | GCC 2.x collect2, where it was built<br>`Syntax   : collect [<opts>] {<file>} [<opts>]` |
| `compiler` | GSHELL front-end for the C compiler<br>**How:** Full-screen: it takes over the display. **control-C gets you out** -- tested, and none of q, Q, control-D or ESC did. If it has a quit command of its own, its documentation in DOC/ will say. |
| `gcc` | &#9733; the GCC driver -- GCC139's and GCC2's share this name<br>`Usage: gcc {options} {files} {options}` |
| `gcc2` | &#9733; the GCC 2.x driver<br>`Usage: gcc2 {options} {files} {options}` |
| `gcc_cc1` | GCC 1.39 C compiler pass |
| `gcc_cc1plus` | GCC 1.39 C++ compiler pass |
| `gcc_cc2` | GCC 2.x compiler pass, under the name gcc2 forks |
| `gcc_cccp` | GCC 1.39 preprocessor<br>`Usage: gcc_cccp [switches] input output` |
| `gcc_cccp2` | &#9733; GCC 2.x preprocessor, under the name gcc2 forks<br>`Usage: gcc_cccp2 [switches] input output` |
| `gcc_collect` | GCC 1.39 collect2<br>`Syntax   : collect [<opts>] {<file>} [<opts>]` |
| `gpp` | the C++ driver<br>`Usage: gpp {options} {files} {options}` |
| `gpp_cc1plus` | GCC 2.x C++ pass, under the name gpp forks |
| `gpp_cccp` | &#9733; GCC 2.x preprocessor, under the name gpp forks<br>`Usage: gpp_cccp [switches] input output` |
| `gpp_collect` | GCC 2.x collect2, under the name gpp forks<br>`Syntax   : collect [<opts>] {<file>} [<opts>]` |

**Fortran**

| | |
|---|---|
| `creadoc` | extract documentation comments from FORTRAN source.  IT ABORTS HERE -- E_PRCABT with os9lib loaded, with a source file or without, absolute path or relative.  It is the one piece of the RTF set that does not run; `rtf' itself compiles and `biory' runs.  DOC/rtf/biory.doc is the output it produced for biory.f on the machine it came from.  Measured 2026-08-29 |
| `for` | the RTF/68K FORTRAN driver, and a bash KEYWORD -- ask for it by PATH (`/dd/CMDS/for') or bash swallows the name.  It requires Microware's `shell' on your execution path: it forks one to run each compiler pass.  Without it the driver prints the command and stops.  Call `rtf' directly instead and you need no shell at all -- see DOC/README-FORTRAN.  Reworded 2026-08-30 |
| `rtf` | RTF/68K Real-Time Fortran-77 compiler, v2.14 (CERN, 1987), AND IT COMPILES HERE.  `load /dd/CMDS/os9lib' first -- without its runtime library the whole set prints nothing -- then `rtf <file>.f' reads the Fortran and writes 68k ASSEMBLY beside the source: zero errors, `RTF normally completed'.  Assembling and linking that needs Microware's r68 and l68, which are not here.  CALL IT DIRECTLY: the `for' driver forks a program called `shell' to run rtf, and this disk has none, so it prints the command and stops.  Sources to try in SRC/rtf.  Manual: DOC/rtf/rtfman.txt.  Measured 2026-08-29 |

**Make & generators**

| | |
|---|---|
| `assembler` | GSHELL front-end for the assembler<br>**How:** Full-screen: it takes over the display. **control-C gets you out** -- tested, and none of q, Q, control-D or ESC did. If it has a quit command of its own, its documentation in DOC/ will say. |
| `bison` | GNU bison 1.19 parser generator -- ADDED; skeletons in /dd/LIB<br>`Usage: bison [-dltvyV] [-b file-prefix] [-o outfile] [-p name-prefix]` |
| `dmake` | &#9733; dmake 3.70 - parallel make with its own makefile dialect |
| `flex` | lexical analyzer generator -- see DOC/flex/README-FLEX FIRST<br>`Syntax   : flex [-bcdfinpstvFILT8 -C[efmF] -Sskeleton] [filename ...]` |
| `gmake` | GNU make -- ADDED (the gnu.bin build of make is the broken one)<br>`Usage: gmake [options] [target] ...` |
| `m4` | m4 macro processor.  SWAPPED 2026-08-28: what ships is now the CMDS/REBUILT/m4_0.5 build, because the one that used to be here MANGLED its output -- a one-line definition expanded to `i hr ' instead of `hi there'.  The one here now expands correctly, from a file or a pipe<br>`Usage: m4 [options] file ....` |
| `make` | &#9733; make -- and it DOES maintain a target, corrected 2026-08-29. Two rules catch people: a command line must begin with a TAB (which will not survive being typed at this terminal, so copy DOC/make/demo.mk rather than echoing one), and a recipe must have no shell metacharacter -- `cp a b' runs, `cat a > b' gets `That path name doesn't lead to a file'.  DOC/STATUS has both<br>**How:** It works. Copy `/dd/DOC/make/demo.mk` rather than writing a makefile at the shell -- a command line must begin with a TAB and a tab does not survive being typed at this terminal. And keep shell metacharacters out of a recipe: `cp a b` runs, `cat a > b` gets "That path name doesn't lead to a file", because make forks bash with the line as a PATHNAME rather than with -c. The default rules are in default.mk beside it, and make looks for that along your PATH. Measured 2026-08-29. |
| `makeinfo` | GNU makeinfo -- Texinfo to info.  GCC139 shipped a byte-identical second copy until 2026-08-31; this is the only one now<br>`Usage: makeinfo [options] texinfo-file...` |
| `yacc` | &#9733; yacc parser generator -- it HANGS on a two-rule grammar here: no output, no files written, and the run has to be killed.  `bison' reads the same grammar and reports its states and its conflicts<br>`Syntax   : yacc [-dltv] [-b <prefix>] filename` |

**Translators**

| | |
|---|---|
| `p2c` | Pascal to C translator (GPL).  Reads LIB/p2c/p2crc; programs it emits link against LIB/libp2c.l<br>**How:** Translates Pascal to C. It reads LIB/p2c/p2crc at startup and stops with "file not found" if that is missing; programs it emits must be linked against LIB/libp2c.l. |

</details>

## Languages

*Interpreters and language systems beyond C.*

<details><summary>10 programs</summary>

**Adventure authoring**

| | |
|---|---|
| `adlcomp` | compile an ADL world<br>**How:** Compiles an ADL world: `adlcomp /dd/ADL/DEMOS/tiny.adl -o /dd/tmp/tiny -i /dd/ADL'. The `-i' is where standard.adl lives and is required. Tested. |
| `adldebug` | play with the debugger attached<br>**How:** adlrun with the debugger attached. |
| `adlrun` | <world>                          play it<br>**How:** Plays a compiled ADL world: `adlrun /dd/tmp/tiny'. Tested -- the tiny demo opens "You are in a small but comfortable room... There is a red pillow here." NOTE: play from an RBF disk, not a host-directory mount; reading a world off /hN under os9exec trips an assertion inside the emulator. |
| `adltouch` | refresh a compiled world<br>**How:** Refreshes a compiled world after you edit its source. |

**Interpreters**

| | |
|---|---|
| `forth` | &#9733; Forth interpreter<br>`Syntax   : forth [<opts>] [<file>] [<opts>]` |
| `lua` | Lua 3.0 -- a small scripting language.  It was built against a LATER csl than the edition 16 that ships here and stops with `**** csl traphandler mismatch ****'.  `luac', the compiler, is fine.  See DOC/lua and DOC/README-LUA<br>**How:** Lua 3.0, and it needs Microware's csl -- see DOC/README-CIO. Run a script with `lua file.lua'. NOTE: 3.0 has no numeric `for' loop; that arrived in Lua 3.1, so `for i=1,10 do' is a syntax error here and `while' is the idiom. Examples in DOC/lua/examples. |
| `luac` | &#9733; Lua bytecode compiler -- luac -o out in.lua<br>**How:** Compiles a Lua script to bytecode: `luac -o out in.lua'. Needs csl. runc then runs the result as an OS-9 command. |
| `runc` | Runs a compiled Lua chunk as an OS-9 command -- and stops with the same csl mismatch as `lua'.  DOC/STATUS names all five programs that do |
| `wam.sbprolog` | SB-Prolog 2.2 WAM engine -- see DOC/sbprolog/README-SBPROLOG<br>`Usage: sim [-Ttdns] [-m s_size] [-p p_size] [-b tr_size] [-ui num] pil_file_name ...` |
| `xlisp` | XLISP 2.1 Lisp interpreter |

</details>

## Archives & compression

*Pack, unpack and shrink -- lha, zip, tar, arc, zoo, and OS-9 module libraries.*

<details><summary>40 programs</summary>

**Alternates**

| | |
|---|---|
| `arc_5.12` | ARC v5.12, third-party; /dd/CMDS/arc is 5.21.  5.12 wants its command letter with a leading dash<br>`Usage: arc -{amufdxeplvtc}[bswn][g<password>]` |
| `compress_4.0` | compress 4.0, another edition of CMDS/compress<br>`Syntax   : compress [-cdfvV] [-b maxbits] [file ...]` |
| `compress_rebuilt` | our source build of CMDS/compress, from the same hc_utils source.  Same program, and the two agree byte for byte on what they write<br>`Usage: compress [-dfvoV] [-b MaxBits] [file ...]` |
| `diff_1.1` | another build of GNU diff 1.1<br>`Syntax   : diff [<options>] file1 file2` |
| `gtar` | another GNU tar; CMDS/tar is the one the image build uses |
| `gzip020_csl` | &#9733; gzip 1.2.4, 68020, needs csl<br>`usage: gzip020_csl [-gzip020_cslcdfhlLnNgzip020_csltvV19] [-S suffix] [file ...]` |
| `gzip020_nocsl` | gzip 1.2.4, 68020, no csl needed<br>`usage: gzip020_nocsl [-gzip020_nocslcdfhlLnNgzip020_nocsltvV19] [-S suffix] [file ...]` |
| `gzip68k_csl` | &#9733; gzip 1.2.4, 68000, needs csl<br>`usage: gzip68k_csl [-gzip68k_cslcdfhlLnNgzip68k_csltvV19] [-S suffix] [file ...]` |
| `gzip68k_nocsl` | gzip 1.2.4, 68000, no csl needed<br>`usage: gzip68k_nocsl [-gzip68k_nocslcdfhlLnNgzip68k_nocsltvV19] [-S suffix] [file ...]` |
| `gzipcpu32_nocsl` | gzip 1.2.4, CPU32, no csl needed<br>`usage: gzipcpu32_nocsl [-gzipcpu32_nocslcdfhlLnNgzipcpu32_nocsltvV19] [-S suffix] [file ...]` |
| `gzipcpu32k_csl` | &#9733; gzip 1.2.4, CPU32, needs csl<br>`usage: gzipcpu32k_csl [-gzipcpu32k_cslcdfhlLnNgzipcpu32k_csltvV19] [-S suffix] [file ...]` |
| `lharcs` | C-LHarc 1.01, older than CMDS/lha 2.08<br>`Usage: lharcs {axevlufdmctp}[qnftv] archive_file [files or directories...]` |
| `m4_0.5` | &#9733; another build of m4 -- and since 2026-08-28 it IS the build that ships as `m4', the earlier one having turned out to mangle what it expanded<br>`Usage: m4 [options] file ....` |
| `sed_1.06` | &#9733; another build of sed -- and since 2026-08-28 it IS the build that ships as `sed', the earlier one having turned out to do nothing but exhaust memory<br>`Syntax   : sed [<opts>] [<file>]` |
| `zoo_2.1` | zoo 2.1 (1991), newer than the 2.01 in CMDS.  Same OSK porters as pd-ksh.  Reads what 2.01 writes; CMDS/zoo is left in place because the pool tools here call it.<br>`Usage: zoo {acDeglLPTuUvx}[aAcCdEfInmMNoOpPqu1:/.@n] archive file` |

**Compress a file**

| | |
|---|---|
| `compr` | file compressor<br>`Usage: compress [-dfvcV] [-b maxbits] [file ...]` |
| `compress` | compress/uncompress (LZW) -- ADDED<br>`Usage: compress [-dfvoV] [-b MaxBits] [file ...]` |
| `gzip` | GNU gzip<br>`usage: gzip [-gzipcdfhlLngziptvV19] [-S suffix] [file ...]` |

**Create & extract**

| | |
|---|---|
| `ar` | archive librarian (Carl Kreider) -- .ar files<br>`Usage:  Ar -<cmd>[<modifier>] [file .. ]` |
| `arc` | ARC 5.21 archive utility<br>`Usage: arc {amufdxerplvtc}[biswnoq][g<password>]` |
| `cat` | &#9733; concatenate files (S.M. Ryger, 1987) |
| `dearc` | &#9733; Extract an MS-DOS .ARC archive (Carl Kreider).  arc and marc handle the OS-9 side<br>`Usage: dearc [p] filename` |
| `lha` | LHa 2.08 -- create/extract .lzh archives<br>`Syntax: LHa -{axelvudmcp}[qvnfodiszrgc012][w=<dir>] archive_file [file...]` |
| `lharc` | LHarc archiver<br>`Usage: lharc {axevlufdmctp}[qnftv] archive_file [files or directories...]` |
| `marc` | MARC, the archive MERGER -- `marc <target> <source> [names]' copies members from one .arc into another.  It is not an archiver and does not make one<br>`Usage: MARC <tgtarc> <srcarc> [<filename> . . .]` |
| `shar` | Shell-archive creator, and ONE BROKEN CHECK is all that stops it: its read-access test rejects every file that EXISTS -- `No read access for file: <name>' on its own standard output, for world-readable files that `cat' reads, absolute or relative, with -a or without.  Hand it a name that is NOT there and the check passes vacuously: it writes the whole shell-archive preamble, cut line and all, and only then fails at open.  So the archiver works and the gatekeeper does not.  Use tar, zoo or lha.  Measured 2026-08-29 |
| `tar` | GNU tar 1.10<br>`Syntax : tar [ctx][mfv] tarfile [file(s)...]` |
| `unzip` | &#9733; Info-ZIP unzip.  Nothing here can MAKE a zip for it to read -- see the `zip' entry -- so it is untested against a fresh archive.  It reads zips made elsewhere<br>`Usage: unzip [ -options[modifiers] ] file[.zip] [filespec...]` |
| `zip` | Info-ZIP zip 1.9 DOES NOT WORK, measured 2026-08-27.  It deflates correctly and then cannot put the result anywhere: it writes a temporary (_Z000003), fails to rename it over the target, and reports `zip error: Could not create output file'.  Reproduced writing into /dd/tmp and into /dd, so it is not one bad directory. Use zoo, tar or gzip instead; all three round-trip exactly. tools/datatests/archives.cases keeps the failing case. |
| `zipnote` | Info-ZIP zipnote -- view/edit zip comments<br>`Usage:  zipnote [-w] [-b path] zipfile` |
| `zipsplit` | Info-ZIP zipsplit -- split a zip archive<br>`Usage:  zipsplit [-ti] [-n size] [-b path] zipfile` |
| `zoo` | &#9733; zoo archiver<br>`Usage: zoo {acDeglLPTuUvx}[aAcCdEfInmMNoOpPqu1:/.@n] archive file` |

**OS-9 module libraries**

| | |
|---|---|
| `ar2` | &#9733; Ar V2.00 -- Carl Kreider's archiver, a later edition than the V1.2 included as `ar'.  Both are here; ar is unstarred<br>`Usage:  Ar -<cmd>[<modifier>] archive [file .. ]` |
| `liborder` | &#9733; order the modules in an OS-9 library<br>`Usage: liborder <options> file1.r file2.r ...` |
| `modbuster` | Split merged OS-9 module files<br>`Syntax: Modbuster [<opts>] <path> [<opts>]` |
| `unpacklib` | &#9733; split an OS-9 library into its modules<br>`Usage: unpacklib <options> file1.l file2.l ...` |

**zip**

| | |
|---|---|
| `funzip` | &#9733; Unzip straight from a pipe -- funzip < file.zip<br>**How:** Unzips from a pipe rather than a file: `funzip < thing.zip > thing'. For a normal archive use unzip; zipinfo lists what is inside one. |
| `zipinfo` | &#9733; Info-ZIP zipinfo -- what is inside a zip archive<br>`Usage:  zipinfo [-1smlvht] file[.zip] [filespec...]` |

**zoo**

| | |
|---|---|
| `booz` | &#9733; Extract or list a zoo archive.  Public domain, Rahul Dhesi<br>**How:** Extracts and lists zoo archives. `booz -l file.zoo' to look, `booz -x' to extract. fiz repairs a zoo archive that will not open. |
| `fiz` | &#9733; Repair a damaged zoo archive.  Public domain<br>`Usage:  fiz archive[.zoo]  ("fiz -h" for help)` |

</details>

## Encoding & conversion

*Between text encodings, line endings, Macintosh formats, ciphers and hashes.*

<details><summary>24 programs</summary>

**Audio**

| | |
|---|---|
| `sox` | &#9733; Sound eXchange -- audio format converter.  Sample .iff sounds are in DOC/sox<br>**How:** Converts between audio formats. There is no sound device here, so it converts files rather than plays them. Sample .iff sounds are in DOC/sox. Needs Microware's cio. |

**Ciphers & hashes**

| | |
|---|---|
| `checksum` | &#9733; file checksum<br>`Syntax:   checksum <file> [<file>...]` |
| `chksum` | &#9733; 32-bit file checksum |
| `crypto` | &#9733; cryptogram puzzle solver's assistant<br>**How:** File encryption. Takes files: `crypto [-cegnru] <file>...'; `crypto -h' is the help. |
| `des` | &#9733; DES file encryption -- it writes `<file>.n', removes the original, and does NOT decrypt: run over its own output with the same key it produces a file that checksums 00000000.  `xcrypt' round-trips |
| `md5` | MD5 checksum<br>`Usage: MD%d <-opts> <filename>` |
| `xcrypt` | &#9733; file encryption/decryption |

**Macintosh**

| | |
|---|---|
| `binhex` | Encode a file as Macintosh BinHex 4.0<br>`Usage: binhex [-binhex] [files]` |
| `hexbin` | Decode BinHex back to a Macintosh file<br>**How:** Decodes Macintosh BinHex (.hqx) files, which is how Mac software travelled by mail and BBS. binhex goes the other way; unsit opens StuffIt archives and macunpack opens PackIt ones. All trap-free. DOC/macutils has the package readme. |
| `macbin` | MacBinary encode/decode<br>`Usage  :   Converts files to MacBinary format` |
| `macsave` | Save a Macintosh file with its resource fork intact |
| `macstream` | Read a MacTerminal file stream<br>`Usage: macstream [-macstream] files` |
| `macunpack` | Unpack a packed Macintosh archive<br>`Usage: macunpack [-macunpack] [filename]` |
| `mcvert` | Convert between Macintosh file representations<br>`Usage: Mcvert [-rduxh] [DUpqsv] filename(s)` |
| `UnMacpack` | Unpack MacPack format.  Named for its module, which is UnMacpack rather than unmacpack<br>`Usage: macunpack [-UnMacpack] [filename]` |
| `unsit` | Unpack a StuffIt archive (V1.15f, Nigel Perry)<br>`Usage: Unsit [-rdulM] [-vqfm] filename` |

**Text encodings**

| | |
|---|---|
| `atob` | ASCII-to-binary decode<br>`Usage: atob <filein >fileout` |
| `btoa` | Binary-to-ASCII encode<br>`Usage : btoa <filein >fileout` |
| `chardef` | define a character set<br>`Syntax: defchar [<path>]` |
| `todos` | &#9733; OS-9 to DOS line endings -- BUT SEE BELOW, it does nothing. `autolf -c -C -L' does the job and is on this disk |
| `toos9` | &#9733; DOS to OS-9 line endings -- the same, and the same answer: `autolf -l -C' converts the other way DO NOT RELY ON THESE TWO.  Measured 2026-08-27: both are NO-OPS.  Each takes a FILENAME (not a pipe) and rewrites it in place through a `todos.$$$.N' temporary, and the file that comes out is byte-identical to the one that went in -- same length, same md5 -- on CR-only OS-9 text, which is exactly what todos says it converts.  A real DOS conversion must ADD a linefeed per line and cannot leave the length alone.  Tested on /dd/SYS/termcap (963 bytes) and DOC/README-CIO (3886); neither moved. Use `flip' host-side, or `tr', until this is understood. tools/datatests/encoding.cases keeps the failing case. |
| `uudecode` | &#9733; uudecode<br>`USAGE: uudecode [infile]` |
| `uuencode` | &#9733; uuencode.  ITS OWN USAGE LINE IS WRONG: it prints `uuencode >outfile [infile] name' and then fails with two arguments.  Give it ONE -- the input file -- and redirect: `uuencode myfile > myfile.uu'.  Measured 2026-08-27<br>`USAGE: uuencode >outfile [infile] name` |
| `uuexpand` | expand uuencoded text<br>`Usage: uuexpand [opts]` |

</details>

## Communications

*Kermit in several builds, terminal sessions, and networking.*

<details><summary>96 programs</summary>

**File transfer**

| | |
|---|---|
| `fileserv` | &#9733; serve files to remote sites on request |
| `fixtext` | &#9733; repair the line endings of a received text batch<br>`Usage:  fixtext [infile] [outfile]` |

**Kermit**

| | |
|---|---|
| `ckermit` | &#9733; C-Kermit 5A(190) BETA.14, 24 Jul 94 -- the cio build.  The version is the binary's own banner, read 2026-08-30 |
| `kermit` | OS-9 Kermit Version 1 Release 5 -- serial file transfer and terminal emulation.  `ckermit' is the C-Kermit, and REBUILT/kermit_cio is our build of this one.  Corrected 2026-08-30: this entry said C-Kermit 5A(188) and starred the program; run with no cio present it starts and prints its banner, and the star belonged to the REBUILT build<br>`Usage: kermit c[le line esc.char]   (connect mode)` |
| `kermit2` | Kermit Program Version 1 Release 6 -- the same command letters as `kermit', 5K smaller.  DOC/README-KERMIT compares all six<br>`Usage:   kermit c[le line esc.char]   (connect mode)` |
| `kermit3` | Kermit68K version 1.0.00, 01 July 1987 -- a DIFFERENT program from the other small ones: it puts up its own `Kermit68K>' prompt and reads a Kermit.ini, rather than taking command letters.  Banner read 2026-08-31<br>`Usage: kermit [-x arg [-x arg]...[-yyy]...]]` |
| `kermit_cio` | &#9733; our source build; CMDS/kermit is the archive binary and needs no cio, where this one does<br>`Usage: kermit c[le line esc.char]   (connect mode)` |
| `xkermit` | &#9733; the same version and banner as `kermit' -- OS-9 Kermit 1.5 -- in half the space, because it links cio rather than carrying stdio.  DOC/README-KERMIT<br>`Usage: kermit c[le line esc.char]   (connect mode)` |

**Mail**

| | |
|---|---|
| `answer` | &#9733; reply to messages in a folder in turn |
| `arepdaemon` | &#9733; the daemon autoreply relies on |
| `autoreply` | &#9733; send an automatic reply while you are away<br>`Usage: autoreply <filename>	to start autoreply,` |
| `checkalias` | &#9733; check an alias resolves before you rely on it<br>`Usage: checkalias alias [alias ...]` |
| `disable` | &#9733; disable a UUCP device<br>`Syntax: disable <port>` |
| `dotilde` | &#9733; expand ~user in a path, as the mailer does |
| `elm` | &#9733; the Elm mail reader itself -- full-screen, menu-driven<br>**How:** The full-screen mail reader. On first run it offers to create a .elm directory in your home for its elmrc and aliases -- say y. Mail lives at /dd/SPOOL/MAIL/<user> and SYS/login points MAIL there; `readmsg 1' prints a message without opening the reader. |
| `enable` | &#9733; re-enable a UUCP device<br>`Syntax: enable [<opts>] <port> [<opts>]` |
| `fastmail` | &#9733; send a file as mail without opening the reader<br>`Usage: fastmail {args} [ filename \| - ] address(es)` |
| `filter` | sort incoming mail into folders by rule<br>`Usage: \| filter [-nrvlq] [-f rules] [-o file]` |
| `frm` | &#9733; list who your mail is from, one line each<br>**How:** Lists who your mail is from, one line each. Reads $MAIL, which SYS/login sets. |
| `lcasep` | &#9733; lower-case a name for mail<br>`usage: lcasep [-f file] [-o outfile]` |
| `listalias` | &#9733; list the aliases you have<br>`Usage: listalias [ -s \| -u ] <optional-regular-expression>` |
| `lmail` | &#9733; local mail delivery<br>`Syntax: lmail <user name> {<user name>}` |
| `mail` | &#9733; a simple mail sender<br>`Syntax: mail [<opts>] [<user>]` |
| `mailx` | &#9733; the mail reader and sender |
| `makedb` | build the alias database |
| `messages` | &#9733; count and list what is in a folder<br>**How:** Counts what is in your mail folder. Tested: "There is 1 message in your mailbox". |
| `newalias` | &#9733; rebuild the alias database -- run it after editing aliases<br>**How:** Rebuilds the Elm alias database from USR/LIB/ELM/aliases.text after you edit it. |
| `newmail` | &#9733; watch for mail arriving and say so<br>`Usage: newmail [-d] [-i interval] [-w] {folders}` |
| `nptx` | &#9733; expand a mail alias list |
| `pathalias` | compute mail routes from a map<br>`usage: pathalias [-vciDfI] [-l localname] [-d deadlink] [-t tracelink] [-g edgeout] [-s treeout] [-a avoid] [files ...]` |
| `philmail` | the philmail mailer |
| `printmail` | &#9733; format a message for a printer<br>`Usage: printmail [-p] [-r filename] <message list>` |
| `pwparse` | &#9733; parse the password file for the mailer |
| `read_mail` | &#9733; a small mail reader of its own, not vi's helper: it opens /dd/MAIL/mail_<user> and offers `[L]ist again, e[X]it & delete mail, exit & [N]ot delete'.  Corrected 2026-08-29 |
| `readmsg` | &#9733; print selected messages from a folder<br>**How:** Prints messages from a mail folder: `readmsg 1' for the first. Tested -- it reads the welcome message in /dd/SPOOL/MAIL/tester. |
| `rmail` | &#9733; deliver incoming mail (invoked by uuxqt, not by you)<br>`usage: rmail [file] "site!user[@site]"` |
| `smail` | &#9733; smart mail router<br>`Usage:   smail [<options>] address...` |
| `uupoll` | &#9733; poll a site for waiting work<br>**How:** Polls a UUCP site for waiting work. Blars uucp; wants the `uucp' user, which SYS/password now has. |
| `uux` | &#9733; run a command on another UUCP site<br>**How:** Runs a command on another UUCP site. This is BLARS uucp, which reads USR/LIB/UUCP/Config -- a different configuration from UUCPbb's SYS/UUCP. Both ship. |

**News**

| | |
|---|---|
| `bdecode` | &#9733; decode a batched news article<br>`Usage: bdecode [file]` |
| `byteflip` | &#9733; byte-swap a dbz database between architectures -- silent, and correctly so, unless handed a dbz database |
| `c7decode` | &#9733; decode 7-bit-safe encoded news |
| `dbz` | &#9733; the news history database<br>**How:** The news history database from C News: `dbz [-a] [-x] [-c] database [file]...'. Part of a news system, not useful alone. |
| `expire` | &#9733; delete news articles past their expiry date |
| `newshist` | &#9733; rebuild the history file<br>`usage: newshist [-df file] msgid ...` |
| `newslock` | &#9733; the news system's lock<br>`Usage: newslock tempname lockname` |
| `postnews` | &#9733; post an article to a newsgroup<br>`Usage: postnews [options]` |
| `readnews` | &#9733; read Usenet news articles -- and it RUNS: it opens the reader and answers `**** End of newsgroups', which is the truth on a disk with no news spool.  Every sweep scored it mute because it asks its question and waits. Corrected 2026-08-29 |
| `rnews` | &#9733; unpack an incoming news batch |
| `subscribe` | &#9733; add a newsgroup to your subscription list<br>`usage: subscribe <newsgroup> [newsgroup...]` |
| `unsubscribe` | &#9733; drop one<br>`usage: unsubscribe <newsgroup> [newsgroup...]` |

**TCP/IP**

| | |
|---|---|
| `atp` | &#9733; AX.25 transport, from the KA9Q package |
| `finger` | &#9733; ask another machine who is logged in<br>**How:** Asks another machine who is logged in: `finger <userid>'. Needs a network. |
| `infoxpress` | InfoXpress client |
| `msntp` | set the clock from a network time server -- stops with a csl traphandler mismatch; see DOC/STATUS<br>**How:** Sets the clock from a network time server. |
| `net` | KA9Q net -- TCP/IP over SLIP or AX.25: telnet, ftp, smtp<br>**How:** KA9Q net, Phil Karn's TCP/IP over SLIP or AX.25 -- the stack amateur radio ran on. Needs NETHOME, NETSPOOL and TMPDIR set and a real interface; see DOC/ka9q. |
| `osknet` | OSKNET -- TCP/IP for OS-9, Telnet, FTP, Ping and SMTP<br>**How:** Charles Hedrick's TCP/IP for OS-9 -- Telnet, FTP, Ping and SMTP. It needs a network interface, which os9exec does not present, so it starts and does nothing here. Its own documentation is nine files in DOC/osknet: start with howto.doc and useguide.doc. |

**Terminal & session**

| | |
|---|---|
| `aterm` | ATerm 2.6 terminal emulator.  WORKS -- config is in SYS/ATERM; run it from a login session, not as os9exec's first process, or its terminal library bus errors.  `aterm /t1' for a real serial port.  Manual DOC/aterm, source SRC/aterm<br>`Syntax  : ATerm /serial_path` |
| `cls` | clear the screen (termcap)<br>`Syntax: cls` |
| `connect` | &#9733; connect to a serial line<br>`Usage: connect [<switches>] [<path1>] [<switches>] [<path2>]` |
| `fkeys` | define terminal function keys<br>`Syntax: fkeys [<path>]` |
| `initvdu` | &#9733; init video display<br>**How:** Answers "is not defined for this terminal": it sets up specific VDU hardware, not a general terminal. |
| `input` | UNAXCESS BBS - input helper |
| `sbreak` | Send/clear an SS_Break signal on a serial path<br>`Syntax:   sbreak [/device]` |
| `setfont` | &#9733; load a downloadable terminal font -- setfont <path><br>`usage: setfont <path>` |
| `setterm` | &#9733; set terminal type<br>**How:** Full-screen: it takes over the display. **ESC quits** -- tested. (control-C also gets you out, but ESC is the program's own way.) |
| `tsmon2` | tsmon replacement - terminal monitor<br>`Syntax:   tsmon2 [<options>] <device name>` |
| `udate` | &#9733; UNAXCESS BBS - date display |
| `uwho` | &#9733; UNAXCESS BBS -- who is online.  Opens `/etc/utmp', and in OS-9 a leading /etc names a DEVICE, not a directory, so this cannot work here whatever is placed under /dd.  A Unix-ism left in the port; the BBS itself would have to supply an /etc device |
| `wysecrack` | &#9733; Wyse terminal baud detect -- it writes `Anybody out there?' to the terminal and waits for a Wyse to answer, which nothing here is.  That one line is all it ever prints.  Measured 2026-08-29 |
| `wysetime` | Wyse terminal time utility |

**Terminal & transfer**

| | |
|---|---|
| `blastem` | XModem and YModem file transfer, written for the MM/1<br>`Syntax: blastem [<opts>] {<filename> [<opts>]}` |
| `dld` | &#9733; XModem download<br>`Syntax: dld <file>` |
| `k` | Kermit transfer (Tim Kientzle) |
| `rxmod` | receive an OS-9 module over a serial line and enter it in the module directory.  Source: SRC/serload the module directory.  Source: SRC/serload<br>`Syntax: rxmod [<opts> [module(s)]]` |
| `sterm` | a serial terminal emulator<br>`Usage:  sterm [-df? -l'p' -e'x']` |
| `tsu` | &#9733; tterm's setup program |
| `tterm` | &#9733; Stephen Carville's terminal emulator, VT100-ish<br>`Usage:  tterm <options>` |
| `txmod` | send an OS-9 MODULE over a serial line<br>`Syntax: TXMod [<opts>] module(s) [<opts>]` |
| `uld` | &#9733; XModem upload<br>`Syntax: uld <file>` |
| `xy` | XMODEM/YMODEM transfer (Tim Kientzle) |
| `xydown` | XModem/YModem download, public domain<br>`Usage:  XYDOWN  [opts]  [filename]` |
| `xyt` | &#9733; X/Y/ZMODEM transfer for tterm<br>`Usage:  xyt [opts] [filename] [opts]` |
| `z` | ZMODEM transfer (Tim Kientzle) |

**UUCP**

| | |
|---|---|
| `uucico` | &#9733; the transfer program itself -- dials, talks UUCP<br>`usage: uucico [opts] -r \| sys [sys...]  [opts]` |
| `uuclean` | &#9733; remove stale jobs from the spool<br>`Usage: uuclean [opts]` |
| `uucp` | &#9733; queue a file copy to or from another site |
| `uulog` | &#9733; show the transfer log<br>`Usage: uulog [-s<sysname> -u<username> -d<days>] [-f]` |
| `uuname` | &#9733; list the sites you can reach<br>`Usage:  uuname [-l]` |
| `uuxqt` | &#9733; run the jobs a remote site queued here -- and it cannot start: it looks for a module called `procs' to see whether it is already running, and `procs' is not on this disk (error 221).  Measured 2026-08-29<br>`Usage:  uuxqt [opts]  <sys> [<sys>...]  [opts]` |

**Web server**

| | |
|---|---|
| `authwn` | authentication helper for protected areas |
| `inetd` | &#9733; the internet daemon that listens and hands connections to wn<br>**How:** The listener that hands incoming connections to wn. Needs a network. |
| `inetdc` | &#9733; control program for inetd |
| `wn` | the web server itself -- serves files over HTTP<br>**How:** A real HTTP server (WN 1.14.3, GPL). It starts and opens its log -- the path /h0/c/unid/wn_1.14.3/osk/logs is compiled into the binary, and that directory is on this disk so it can. What it cannot do here is serve: os9exec has no network. On a machine with TCP/IP it is the real thing. Its manual is 30 HTML files in DOC/wn. |
| `wn.stb` | WN's symbol table (a data module, not a program) |
| `wndex` | build the index WN serves from; run it in each directory you publish<br>**How:** Builds the index WN serves from. Run it in a directory you want published; on its own it says "Can't open ./index -- skipping it", which means there is nothing there to index yet. |

</details>

## Graphics & images

*The netpbm toolkit, JPEG, a ray tracer, and things that draw.*

<details><summary>202 programs</summary>

**Drawing & display**

| | |
|---|---|
| `draw` | character-graphics drawing program |
| `loadmem` | load memory image<br>`Syntax   : LOADMEM <destinati address> <upper limit address> <path>` |
| `pdraw` | Pdraw 1.4 - 2D/3D data plotting, PostScript output<br>`usage: pdraw [-v vx vy vz] [-o options-file] [-Pprinter] [-s scale] [-e] [-h] [-nosort] [-noplot] [-print] [-ps] infile1 infile2 ...` |
| `savemem` | save memory image<br>`Syntax   : SAVEMEM <from address> <to address> <path>` |
| `snap` | &#9733; snapshot the screen to a file |

**Hardware demos**

| | |
|---|---|
| `apfel` | Mandelbrot (Apfelmaennchen) -- Atari GRAPH display |
| `g` | &#9733; an Atari GRAPH demo, paired with striche.  Needs the `graph' |
| `graph` | the `Graph' TRAP LIBRARY itself, not a program -- a type-$0B module.  It is what g, striche, apfel, sine, showpic, graphdemo and graphsave all link.  `load' it and the trap installs; the library is then entered and stops on a privilege violation at its own `RTE', a supervisor-only instruction -- it was written to run in supervisor state.  Note its module name is lowercase `graph' while the programs ask for `Graph', and real OS-9 matches module names exactly |
| `graphdemo` | Atari GRAPH demonstration |
| `graphsave` | save an Atari GRAPH screen |
| `lissaj` | &#9733; Tektronix demo: Lissajous figures |
| `lorenz3d` | &#9733; Tektronix demo: the Lorenz attractor in 3D |
| `showpic` | show a picture on the Atari GRAPH display |
| `sine` | sine plot, Atari GRAPH |
| `striche` | &#9733; line drawing, Atari GRAPH.  Needs the `graph' trap library found -- see the graph entry below |
| `wgen` | Tektronix waveform generator |

**JPEG**

| | |
|---|---|
| `cjpeg` | JPEG encoder (IJG).  It reads a PNM whose header fields are separated by LF; the netpbm ports here separate them with CR, so cjpeg answers `Bogus data in PPM file' for a file netpbm wrote and netpbm answers `junk in file where an integer should be' for a file cjpeg's djpeg wrote.  Three bytes either way, and `pbyte' patches them in place -- DOC/STATUS has the offsets, and a full round trip is in the data tests.  The entry here said until 2026-08-29 that no JPEG could be made on this disk; one can.  Corrected 2026-08-29<br>**How:** Makes a JPEG from a PNM -- but not straight from a netpbm PNM. cjpeg wants LF between the header fields and this disk's netpbm writes CR, so it says "Bogus data in PPM file". Patch the three separators with `pbyte` first: for `ppmmake red 8 8` they are at offsets 2, 6 and a. DOC/STATUS has the full recipe both ways. Measured 2026-08-29. |
| `cjpeg.070` | JPEG compressor (68070 build)<br>`usage: cjpeg.070 [switches]` |
| `djpeg` | JPEG decompressor, jpeg-5a.  It works, and its output does NOT pipe into netpbm as it stands: djpeg ends a PNM header line with LF and every netpbm tool here wants CR, so ppmtopgm answers `junk in file where an integer should be'.  Patch the three separators with `pbyte' -- DOC/STATUS has the recipe -- and the pipeline runs.  Measured 2026-08-29<br>**How:** Decompresses a JPEG: `djpeg -pnm image.jpg > out.ppm`. The disk has one to try, SRC/jpeglib/JPEG_5A/testimg.jpg. Its output will NOT pipe into netpbm unpatched -- djpeg writes LF at the end of a PNM header line and netpbm here wants CR. `pbyte out.ppm 2 0d` and the same at the two later separators fixes it; DOC/STATUS has the offsets. Measured 2026-08-29. |
| `djpeg.070` | JPEG decompressor (68070 build)<br>`usage: djpeg.070 [switches]` |
| `rdjpgcom` | read the comment from a JPEG file<br>`Usage: rdjpgcom [switches] [inputfile]` |
| `rdjpgcom.070` | read a JPEG's comment (IJG 0.70 build)<br>`Usage: rdjpgcom.070 [switches] [inputfile]` |
| `wrjpgcom` | write a comment into a JPEG file<br>`Usage: wrjpgcom [switches]` |
| `wrjpgcom.070` | write a JPEG's comment (IJG 0.70 build)<br>`Usage: wrjpgcom.070 [switches]` |

**NETPBM: edit & analyse**

| | |
|---|---|
| `pbmclean` | netpbm image tool |
| `pbmlife` | netpbm image tool |
| `pbmmake` | netpbm image tool |
| `pbmmask` | netpbm image tool |
| `pbmpscale` | netpbm image tool |
| `pbmreduce` | netpbm image tool |
| `pbmtext` | netpbm image tool<br>**How:** pbmtext <word> draws it as an image. `pbmtext os9 \| pbmtoascii' prints it on the terminal and needs no file at all -- the shortest demonstration of the 169 NETPBM programs. See DOC/README-NETPBM. |
| `pbmupc` | netpbm image tool |
| `pgmbentley` | netpbm image tool |
| `pgmcrater` | netpbm image tool |
| `pgmedge` | netpbm image tool |
| `pgmenhance` | netpbm image tool |
| `pgmhist` | netpbm image tool |
| `pgmkernel` | netpbm image tool |
| `pgmnoise` | netpbm image tool |
| `pgmnorm` | netpbm image tool |
| `pgmoil` | netpbm image tool |
| `pgmramp` | netpbm image tool |
| `pgmtexture` | netpbm image tool |
| `pnmalias` | netpbm image tool |
| `pnmarith` | netpbm image tool |
| `pnmcat` | netpbm image tool |
| `pnmcomp` | netpbm image tool |
| `pnmconvol` | netpbm image tool |
| `pnmcrop` | netpbm image tool |
| `pnmcut` | netpbm image tool |
| `pnmdepth` | netpbm image tool |
| `pnmenlarge` | netpbm image tool |
| `pnmfile` | netpbm image tool |
| `pnmflip` | netpbm image tool |
| `pnmgamma` | netpbm image tool |
| `pnmhisteq` | netpbm image tool |
| `pnmhistmap` | netpbm image tool |
| `pnminvert` | netpbm image tool |
| `pnmnlfilt` | netpbm image tool |
| `pnmnoraw` | netpbm image tool |
| `pnmpad` | netpbm image tool |
| `pnmpaste` | netpbm image tool |
| `pnmrotate` | netpbm image tool |
| `pnmscale` | netpbm image tool<br>**How:** Scales an image: `pnmscale 0.5 file'. Given only a filename it takes THAT as the scale factor and then waits on empty input, reporting "bad magic number" -- which means you left out the factor, not that your file is bad. The same trap catches pnmdepth, pnmcut, pnmrotate and others. |
| `pnmshear` | netpbm image tool |
| `pnmsmooth` | netpbm image tool |
| `pnmtile` | netpbm image tool |
| `ppm3d` | netpbm image tool |
| `ppmbrighten` | netpbm image tool |
| `ppmchange` | netpbm image tool |
| `ppmdim` | netpbm image tool |
| `ppmdist` | netpbm image tool |
| `ppmdither` | netpbm image tool |
| `ppmflash` | netpbm image tool |
| `ppmforge` | netpbm image tool |
| `ppmhist` | netpbm image tool |
| `ppmmake` | netpbm image tool |
| `ppmmix` | netpbm image tool |
| `ppmnorm` | netpbm image tool |
| `ppmntsc` | netpbm image tool |
| `ppmpat` | netpbm image tool |
| `ppmquant` | netpbm image tool |
| `ppmqvga` | netpbm image tool |
| `ppmrelief` | netpbm image tool |
| `ppmshift` | netpbm image tool |
| `ppmspread` | netpbm image tool |

**NETPBM: into PNM**

| | |
|---|---|
| `asciitopgm` | ASCII art to PGM (greyscale) |
| `atktopbm` | Andrew toolkit to PBM (bitmap) |
| `bioradtopgm` | Bio-Rad confocal to PGM (greyscale) |
| `bmptoppm` | BMP to PPM (colour) |
| `brushtopbm` | Xerox brush to PBM (bitmap) |
| `cmuwmtopbm` | CMU window manager to PBM (bitmap) |
| `fitstopnm` | FITS to PNM |
| `fstopgm` | Usenix FaceSaver to PGM (greyscale) |
| `g3topbm` | Group 3 fax to PBM (bitmap) |
| `gemtopbm` | GEM to PBM (bitmap) |
| `giftopnm` | GIF to PNM<br>**How:** Reads a GIF into the PNM formats the other 168 converters work on -- try `giftopnm /dd/DEMO/gulls.gif \| pnmfile'. IMPORTANT for anyone piping images out of the emulator: os9exec turns CR into CRLF on the way to the host, so a raw image containing byte 13 arrives corrupted. Keep binary inside OS-9 and convert with pnmnoraw before taking a picture anywhere else. DOC/README-NETPBM has the details. |
| `gouldtoppm` | Gould scanner to PPM (colour) |
| `hipstopgm` | HIPS to PGM (greyscale) |
| `hpcdtoppm` | PhotoCD to PPM (colour)<br>`Usage: hpcdtoppm [options] pcd-file [ppm-file]` |
| `icontopbm` | Sun icon to PBM (bitmap) |
| `ilbmtoppm` | IFF/ILBM to PPM (colour) |
| `imgtoppm` | GEM IMG to PPM (colour) |
| `lispmtopgm` | Lisp machine to PGM (greyscale)<br>**How:** This build handles at most 16 grey levels and says "depth is too large" otherwise. Run the image through `pnmdepth 15' before pgmtolispm. |
| `macptopbm` | MacPaint to PBM (bitmap) |
| `mgrtopbm` | MGR to PBM (bitmap) |
| `mtvtoppm` | MTV ray tracer to PPM (colour) |
| `pcxtoppm` | PCX to PPM (colour)<br>**How:** Cannot read a pipe -- it seeks backwards in its input and stops with "error seeking past header". Write the PCX to a file and pass the filename. sgitopnm has the same limitation. |
| `pi1toppm` | Atari PI1 to PPM (colour) |
| `pi3topbm` | Atari PI3 to PBM (bitmap) |
| `picttoppm` | PICT to PPM (colour) |
| `pjtoppm` | HP PaintJet to PPM (colour) |
| `pktopbm` | packed font to PBM (bitmap) |
| `psidtopgm` | psid to PGM (greyscale) |
| `qrttoppm` | QRT ray tracer to PPM (colour) |
| `rasttopnm` | Sun raster to PNM |
| `rawtopgm` | raw bytes to PGM (greyscale) |
| `rawtoppm` | raw bytes to PPM (colour) |
| `rgb3toppm` | rgb3 to PPM (colour) |
| `sgitopnm` | SGI to PNM<br>**How:** Cannot read a pipe -- same as pcxtoppm. Give it a filename or it reports "premature EOF". |
| `sirtopnm` | sir to PNM |
| `sldtoppm` | AutoCAD slide to PPM (colour) |
| `spctoppm` | Atari Spectrum to PPM (colour) |
| `spottopgm` | spot to PGM (greyscale)<br>`Usage: spottopgm [-1\|2\|3] [Firstcol Firstline Lastcol Lastline] input_file` |
| `sputoppm` | Atari Spectrum to PPM (colour) |
| `tgatoppm` | Targa to PPM (colour) |
| `xbmtopbm` | X bitmap to PBM (bitmap) |
| `ximtoppm` | xim to PPM (colour) |
| `xpmtoppm` | XPM to PPM (colour) |
| `xvminitoppm` | xvmini to PPM (colour) |
| `xwdtopnm` | X window dump to PNM |
| `ybmtopbm` | ybm to PBM (bitmap) |
| `yuvsplittoppm` | yuvsplit to PPM (colour) |
| `yuvtoppm` | Abekas YUV to PPM (colour)<br>**How:** yuvtoppm <width> <height>. The dimensions are not stored in a YUV file, so you must supply the ones ppmtoyuv started from. |
| `zeisstopnm` | Zeiss confocal to PNM |

**NETPBM: out of PNM**

| | |
|---|---|
| `pbmto10x` | PBM (bitmap) to 10x |
| `pbmto4425` | PBM (bitmap) to 4425 |
| `pbmtoascii` | PBM (bitmap) to ASCII art<br>**How:** Prints an image as characters, so NETPBM can be seen on an ordinary terminal with no graphics. Try `pnminvert /dd/DEMO/sphere.pgm \| pgmtopbm -threshold -value 0.5 \| pbmtoascii'. |
| `pbmtoatk` | PBM (bitmap) to Andrew toolkit |
| `pbmtobbnbg` | PBM (bitmap) to bbnbg |
| `pbmtocmuwm` | PBM (bitmap) to CMU window manager |
| `pbmtoepsi` | PBM (bitmap) to epsi |
| `pbmtoepson` | PBM (bitmap) to epson |
| `pbmtog3` | PBM (bitmap) to Group 3 fax |
| `pbmtogem` | PBM (bitmap) to GEM |
| `pbmtogo` | PBM (bitmap) to go |
| `pbmtoicon` | PBM (bitmap) to Sun icon |
| `pbmtolj` | PBM (bitmap) to lj |
| `pbmtoln03` | PBM (bitmap) to ln03 |
| `pbmtolps` | PBM (bitmap) to lps |
| `pbmtomacp` | PBM (bitmap) to MacPaint |
| `pbmtomgr` | PBM (bitmap) to MGR |
| `pbmtopgm` | PBM (bitmap) to PGM (greyscale) |
| `pbmtopi3` | PBM (bitmap) to Atari PI3 |
| `pbmtopk` | PBM (bitmap) to packed font<br>**How:** A TeX font tool, not an image converter: it wants a pkfile, a .tfm metric file and a resolution. No .tfm ships on this disk. |
| `pbmtoplot` | PBM (bitmap) to plot |
| `pbmtoptx` | PBM (bitmap) to ptx |
| `pbmtox10bm` | PBM (bitmap) to X10 bitmap |
| `pbmtoxbm` | PBM (bitmap) to X bitmap |
| `pbmtoybm` | PBM (bitmap) to ybm |
| `pbmtozinc` | PBM (bitmap) to zinc |
| `pgmtofs` | PGM (greyscale) to Usenix FaceSaver |
| `pgmtolispm` | PGM (greyscale) to Lisp machine |
| `pgmtopbm` | PGM (greyscale) to PBM (bitmap) |
| `pgmtoppm` | PGM (greyscale) to PPM (colour) |
| `pnmtoddif` | PNM to ddif |
| `pnmtofits` | PNM to FITS |
| `pnmtops` | PNM to PostScript |
| `pnmtorast` | PNM to Sun raster |
| `pnmtosgi` | PNM to SGI |
| `pnmtosir` | PNM to sir |
| `pnmtoxwd` | PNM to X window dump |
| `ppmtoacad` | PPM (colour) to acad |
| `ppmtobmp` | PPM (colour) to BMP |
| `ppmtogif` | PPM (colour) to GIF |
| `ppmtoicr` | PPM (colour) to icr |
| `ppmtoilbm` | PPM (colour) to IFF/ILBM |
| `ppmtomap` | PPM (colour) to map |
| `ppmtomitsu` | PPM (colour) to mitsu |
| `ppmtopcx` | PPM (colour) to PCX |
| `ppmtopgm` | PPM (colour) to PGM (greyscale) |
| `ppmtopi1` | PPM (colour) to Atari PI1 |
| `ppmtopict` | PPM (colour) to PICT |
| `ppmtopj` | PPM (colour) to HP PaintJet |
| `ppmtopjxl` | PPM (colour) to pjxl |
| `ppmtopuzz` | PPM (colour) to puzz |
| `ppmtorgb3` | PPM (colour) to rgb3 |
| `ppmtosixel` | PPM (colour) to sixel |
| `ppmtotga` | PPM (colour) to Targa |
| `ppmtouil` | PPM (colour) to uil |
| `ppmtoxpm` | PPM (colour) to XPM |
| `ppmtoyuv` | PPM (colour) to Abekas YUV |
| `ppmtoyuvsplit` | PPM (colour) to yuvsplit |

**Plotting**

| | |
|---|---|
| `gnuplot` | &#9733; gnuplot 2.0 -- plots functions and data files.  Built-in help (SYS/gnuplot.gih); demos and sample data in DOC/gnuplot/demo<br>**How:** Type `set term' first -- it lists every output device it knows, and refuses to plot until you choose one. Its whole manual is built in: type `help'. Demos and sample data are in DOC/gnuplot/demo. Needs Microware's cio. |
| `tplot` | &#9733; Plot data to a plotter.  Asks for an interval and a range and drives the output device; written for an Atari ST<br>`Usage : hiplot <-opt1> .. <-optn> <file1> .. <filen>` |

**Ray tracing & 3D**

| | |
|---|---|
| `mtst` | &#9733; spline curve fitting - test driver |
| `rayshade` | ray tracer 4.0.  It renders, and requires Microware's `shell' on your execution path: it builds its scene through popen(), and OS-9's C library implements popen() by forking a program of exactly that name.  It also wants `cccp' in the DATA directory, which is where the forked shell looks.  With both, it renders and reports its statistics -- measured 2026-08-28. No `shell' ships here; anyone who runs OS-9 has one. DOC/rayshade has the two lines.  Reworded 2026-08-30<br>**How:** Ray tracer 4.0, and it renders. REQUIRES MICROWARE'S `shell` on your execution path -- it builds its scene through popen(), and OS-9's C library implements popen() by forking a program of exactly that name. It also wants `cccp` in the DATA directory. DOC/rayshade has the two lines. |
| `rsconvert` | convert rayshade image output between formats<br>`usage: rsconvert [oldfile]` |

**Viewers**

| | |
|---|---|
| `mgif` | GIF inspector and viewer.  `mgif -i file.gif' reports a GIF's structure and works anywhere; DISPLAYING one needs an Atari ST, because flicker.c writes to ST graphics memory.  Source in SRC/mgif -- its GIF decoder is portable and is the part worth having<br>**How:** `mgif -i file.gif' inspects a GIF and prints its structure -- that works on any terminal. Displaying an image does not: it writes straight to Atari ST graphics memory. Try it on /dd/DEMO/gulls.gif. |

**X11**

| | |
|---|---|
| `basicwin` | X11 demo - basic window (needs an X server) |
| `X11R6shl` | X11R6 shared library loader |
| `xengine` | X11 demo - engine animation (needs an X server)<br>`Usage : xengine [Toolkit-Options][-piston piston_color][-shaft shaft_color][-cylinder cylinder_color][-roter roter_color][-back background_color][-dep depression_colore][-pre pression color][-mono][-patchlevel]` |

</details>

## Games

*Adventures, board and card games, arcade ports, dungeon crawls and puzzles.*

<details><summary>66 programs</summary>

**Adventure & fiction**

| | |
|---|---|
| `advcom` | ADVSYS adventure COMPILER -- turns .adv source into a world file (a .dat, not a .adi; the .adi is an INCLUDE).  The sample source IS here, in GAMES/ADVSYS, and this entry said it was not. Bring osample.adv and objects.adi to the data directory and `advcom osample' builds it -- bare name, because it holds a filename in 20 characters and appends `.adv'.  Corrected 2026-08-29<br>**How:** The ADVSYS compiler. It opens its `@objects.adi` include by BARE NAME in the data directory and holds a filename in 20 characters, so bring both files to where you are and use the short name: `cat /dd/GAMES/ADVSYS/osample.adv > /dd/osample.adv`, the same for objects.adi, then `advcom osample`. Writes osample.dat. Measured 2026-08-29. |
| `advent` | Colossal Cave Adventure -- self-contained, reads /dd/GAMES/adv/glorkz.  Needs this disk as /dd; mounted only as /h0 it cannot find its data.  Unrelated to advcom/advint.<br>**How:** Colossal Cave. Needs this disk as /dd -- it opens /dd/GAMES/adv/glorkz by absolute path, so mounted only as /h0 it cannot find its data. |
| `advint` | ADVSYS adventure INTERPRETER -- plays a world compiled by advcom, and there is one to play: build it as advcom's entry says and `advint osample' starts you in the livingroom.  This said until 2026-08-29 that building it needed a real chd; it does not, and bash on this disk can do the whole thing. GAMES/ADVSYS/README has the four lines<br>**How:** Plays an ADVSYS world. Build one first (see advcom), then `advint osample` -- you start in the livingroom, `n` goes to the hallway. Measured 2026-08-29. |
| `infocom` | Infocom Z-MACHINE interpreter -- a third, unrelated adventure system.  Plays the .z3 files in GAMES/INFORM (dejavu, hellow, shell -- Inform demos, not the Infocom games).<br>**How:** A Z-machine. Plays the .z3 files in /dd/GAMES/INFORM, which are Inform demonstration programs (dejavu, hellow, shell), not the Infocom games. |
| `infocom.tcap` | Infocom interpreter, TERMCAP build -- and it is the one to use here.  It puts a proper status line at the top of the screen (`Y2 Rock Room     Score: 0/2') where plain `infocom' fills the screen with brackets trying to. Measured 2026-08-28<br>**How:** Plays Infocom adventure game files -- it needs the game's data file as an argument, which this disk does not carry. |

**Arcade & action**

| | |
|---|---|
| `bite` | a skull animation, not a game you play<br>**How:** Full-screen: it takes over the display. **`q' quits** -- tested. |
| `greed` | Greed - grid game<br>`Usage: greed [-p] [-s]` |
| `lander` | lunar lander -- KNOWN BROKEN: takes no input, and the post-crash screen is corrupt.  Wants SysV curses line drawing that vt100 termcap does not give it.<br>**How:** Full-screen: it takes over the display. **`q' quits** -- tested. |
| `pacman` | Pac-Man -- it draws nothing and exits at once, keyed or not |
| `robots` | &#9733; robots -- outrun them until they crash into each other. REBUILT HERE from source, in SRC/rob.  The archive binary drew cursor-up as a bare ^K, which a terminal reads as index -- DOWN -- so the screen scrolled and the board was left with characters that were not really there. USE -m: without it the game is effectively unplayable.<br>**How:** Play with `robots -m' -- manual mode, where the robots take one step per move you make. Keys are the numeric keypad 1-9 (5 stands still), `s' for last stand, `t' to teleport. Needs Microware's math module and a real TERM. |
| `snake` | snake arcade game.  Draws its board and takes h/j/k/l in a login session; run bare, with no TERMCAP, it bus errors instead -- see DOC/README-BUSERR.  IT SCATTERS TEXT ACROSS THE BOARD as you play: 17 cursor moves in a played game arrive as literal `[13;49H' rather than as motion, one in an untouched one.  Playable, untidy.  Measured 2026-08-28<br>**How:** Full-screen: it takes over the display. **`x' quits** -- tested. (control-C also gets you out, but `x' is the program's own way.) |
| `sokoban` | &#9733; Sokoban puzzle<br>**How:** Wants a username, so run it from a login rather than a bare shell, or it stops with "cannot get your username". |
| `tet` | Tetris -- KNOWN BROKEN: draws its board and takes no input<br>**How:** Draws the board and ignores the keyboard, and the reason is in its source: tet.c puts the terminal in raw mode inside `#ifndef OSK', so the OS-9 build has no terminal setup at all. Set the mode from outside before starting it (Microware's tmode), or rebuild with an OSK branch using _ss_opt -- LIB/alib.l provides both that and ioctl. Source in SRC/tet. |
| `wanderer` | Boulderdash-style maze game.  Screens ARE here, in GAMES/WAND/screens; needs this disk as /dd to find them.<br>**How:** Full-screen: it takes over the display. **`q' quits** -- tested. |

**Board & card**

| | |
|---|---|
| `back` | &#9733; backgammon -- '?' gives the built-in help |
| `blackjack` | Las Vegas blackjack (M. Theys) -- BASIC09; stops at line 8 with error 56, 'Parameter error'.  See the BASIC09 note below -- this one is a real fault, not the invocation. |
| `blackjak` | &#9733; Las Vegas BlackJack (SNOBOL4-in-C).  Data: GAMES/SNOBOL |
| `chess` | chess - 68k port (three engine versions built)<br>`Syntax: chess [<opts>] <name> [<opts>]` |
| `crib` | cribbage.  Needs TERM set, so run it from a login session -- bare it says `Unknown terminal type'<br>**How:** Full-screen: it takes over the display. **control-C gets you out** -- tested, and none of q, Q, control-D or ESC did. If it has a quit command of its own, its documentation in DOC/ will say. |
| `cribbage` | &#9733; cribbage -- offers instructions before it deals.  Needs TERM, so run it from a login session<br>**How:** Full-screen: it takes over the display. **control-C gets you out** -- tested, and none of q, Q, control-D or ESC did. If it has a quit command of its own, its documentation in DOC/ will say. |
| `gnuan` | GNU Chess analyser -- annotates a saved game move by move |
| `gnuchess` | &#9733; GNU Chess.  ITS MODULE NAME COLLIDES with CMDS/GAMES/gnuchess, which is a different port, so whichever loads first answers for both.  Re-measured 2026-08-31 on a pseudo-terminal with TERM=vt100 and `. /dd/SYS/termcap.entry' sourced: this one and gnuchessn printed NOTHING in twenty seconds, where gnuchessr and GAMES/gnuchess both played.  DOC/DEPENDS has the likely reason -- this build opens /h0/usr/src/chess/gnuchess.book by absolute path and that file is not here, where the GAMES build opens its book by bare name.  Take GAMES/gnuchess it draws the board and plays.  Measured 2026-08-29<br>**How:** Full-screen chess. It will not read SYS/termcap -- it wants the entry in the variable itself. Do `. /dd/SYS/termcap.entry' first and it draws its time-control menu and plays. Tested. |
| `gnuchessc` | GNU Chess 4.0, curses display |
| `gnuchessn` | &#9733; GNU Chess (ncurses) -- termcap.entry first too; printed nothing in the same test<br>**How:** As gnuchess: `. /dd/SYS/termcap.entry' first. Tested. |
| `gnuchessr` | &#9733; GNU Chess (raw) -- and the one of the three in CMDS that answered: it prompts `Enter #moves #minutes', takes a move and replies with its own<br>`Usage: gnuchess [-a] [-h] [-x xwndw]` |
| `mille` | &#9733; Mille Bornes -- the French car-racing card game<br>**How:** Full-screen: it takes over the display. **control-C gets you out** -- tested, and none of q, Q, control-D or ESC did. If it has a quit command of its own, its documentation in DOC/ will say. |
| `nchess` | GNU Chess 4.0 (plain display) |
| `poker` | &#9733; Cold-hand Poker (SNOBOL4-in-C).  Data: GAMES/SNOBOL |
| `queens` | &#9733; N-queens solver -- IOCCC entry by M. Baruch.  It reads the board size on stdin as a NUMBER: `echo 5 \| queens' draws its boards.  Every sweep here fed it prose and scored it silent |
| `tttt` | tic-tac-toe<br>**How:** Full-screen: it takes over the display. **`q' quits** -- tested. |

**Chess utilities**

| | |
|---|---|
| `bincheckr` | check a GNU Chess opening-book file -- it reports booksize 0 for the 145 KB book that ships here, then aborts |
| `checkgame` | replay a saved chess game -- prints two lines of PostScript and then aborts (E_PRCABT).  2nd build; `game' is the same<br>`Usage: game file [start [end] ]` |
| `game` | replay a saved chess game -- prints two lines of PostScript and then aborts (E_PRCABT)<br>`Usage: game file [start [end] ]` |
| `postprint` | print a chess position as PostScript (GNU Chess) |

**Dungeon crawl**

| | |
|---|---|
| `hack` | hack -- the original dungeon crawl NetHack grew out of<br>**How:** RUN IT BY ITS FULL PATH: `/dd/CMDS/GAMES/hack', not `hack'. It chdirs into its playground and then stats argv[0] to date-check saved levels, so a bare name cannot resolve and it stops with "Cannot get status of hack." Invoked in full it starts: "Are you an experienced player?". Its playground -- record, bones, rumors, help -- is in GAMES/HACK/PLAYGROUND. |
| `larn` | &#9733; larn -- dungeon crawl; see the PLAYGROUND note above<br>**How:** Full-screen: it takes over the display. **control-C gets you out** -- tested, and none of q, Q, control-D or ESC did. If it has a quit command of its own, its documentation in DOC/ will say. |
| `ularn` | ULarn -- the larn variant, and its data is complete |

**Other games**

| | |
|---|---|
| `ask` | the CLIENT for `wisecrack': it reads one line from /PIPE/txtpipe and prints it, and says `No Wisecracks coming' when nothing is feeding the pipe.  Start the server first -- `wisecrack &' -- and it answers.  Not the shell-script prompt the name suggests.  Corrected 2026-08-29<br>**How:** Asks a yes/no question and sets the shell status, for scripts. On its own it says "No Wisecracks coming" -- it is the front half of the `wisecrack' pipe from EFFO forum 20. |
| `backgammon` | &#9733; backgammon, with a computer opponent<br>`Usage:  backgammon [-] [n r w b pr pw pb t3a]` |
| `colortest` | &#9733; G-Windows colour chart |
| `convert` | world - build its data tables |
| `cyberwar` | &#9733; CyberWar -- Stephen Carville's game, needs G-Windows |
| `dclock` | &#9733; a digital clock for G-Windows<br>`Usage: dclock [options]` |
| `fuddle` | chess - fuddle variant |
| `hotel` | &#9733; hotel -- two-player board game, played by coordinates<br>**How:** Full-screen: it takes over the display. **control-C gets you out** -- tested, and none of q, Q, control-D or ESC did. If it has a quit command of its own, its documentation in DOC/ will say. |
| `mkdict` | bog - build the dictionary |
| `mkindex` | bog - build the dictionary index |
| `nobs` | cribbage (Colonel's program)<br>**How:** Full-screen: it takes over the display. **control-C gets you out** -- tested, and none of q, Q, control-D or ESC did. If it has a quit command of its own, its documentation in DOC/ will say. |
| `piano` | &#9733; play notes -- piano <base note> <note duration><br>`syntax: piano <base note> <note duration>` |
| `puzzle` | &#9733; sliding-tile puzzle for G-Windows -- it draws through a windowing system that is not here, so at a terminal it gets one rule of plus signs out, the top edge of the tile frame, and stops.  For a 15-puzzle you can play, use puzzle15 or GAMES/puz15; both work |
| `scriptmaster` | &#9733; G-Windows scripting tool<br>`Usage: scriptmaster -t=<title> -d=<directory>.` |
| `stone` | &#9733; the stones game (SNOBOL4-in-C).  Data: GAMES/SNOBOL |
| `teachgammon` | &#9733; backgammon that teaches you the game as you play<br>`Usage:  backgammon [-] [n r w b pr pw pb t3a]` |
| `tess` | &#9733; tesselation puzzle |
| `tt` | typing/terminal game<br>**How:** Full-screen: it takes over the display. **`q' quits** -- tested. |
| `vtxtcn` | world - build its text tables.  Writes .inc files and prints nothing; needs world's .dat files in the current directory |
| `wisecrack` | a SERVER, and `ask' is its client.  Run it in the background and every `ask' pulls one line out of it through /PIPE/txtpipe -- slogans from a German OS-9 seminar, 1992-93.  Alone it prints nothing at all, which is why every sweep here called both programs mute.  `wisecrack & ask "anything"'.  Measured 2026-08-29 |
| `world` | World - text adventure |
| `zot` | &#9733; Zot - arcade game |

**Puzzles**

| | |
|---|---|
| `maze` | maze generator -- KNOWN BROKEN: goes dead |
| `mines` | &#9733; minesweeper<br>**How:** Full-screen: it takes over the display. **`q' quits** -- tested. |
| `puz15` | the 15-puzzle -- same program as CMDS/puzzle15, built twice<br>**How:** Full-screen: it takes over the display. **control-C gets you out** -- tested, and none of q, Q, control-D or ESC did. If it has a quit command of its own, its documentation in DOC/ will say. |
| `puzzle15` | the 15-puzzle -- same program as GAMES/puz15, built twice<br>**How:** Full-screen: it takes over the display. **control-C gets you out** -- tested, and none of q, Q, control-D or ESC did. If it has a quit command of its own, its documentation in DOC/ will say. |

**Word & guessing**

| | |
|---|---|
| `animal` | guess-the-animal learning game<br>**How:** Full-screen: it takes over the display. **control-C gets you out** -- tested, and none of q, Q, control-D or ESC did. If it has a quit command of its own, its documentation in DOC/ will say. |
| `bog` | Boggle word game<br>**How:** Full-screen: it takes over the display. **control-C gets you out** -- tested, and none of q, Q, control-D or ESC did. If it has a quit command of its own, its documentation in DOC/ will say. |
| `hang` | &#9733; hangman<br>**How:** Full-screen: it takes over the display. **control-C gets you out** -- tested, and none of q, Q, control-D or ESC did. If it has a quit command of its own, its documentation in DOC/ will say. |

</details>

## Screen toys

*Animations and screen effects -- they draw on the terminal rather than print to it. Some run until you stop them.*

<details><summary>9 programs</summary>

| | |
|---|---|
| `card` | Towers of Hanoi whose twelve disks are the lines of a Christmas message; VT100, wants TERMCAP |
| `life` | Conway's Game of Life<br>**How:** life [init-file]. The patterns are in /dd/GAMES/LIFE -- try `life /dd/GAMES/LIFE/glider`. It also wants more memory than the default; from the OS-9 shell that is `life #22k <file>`, and bash has no #size syntax at all. |
| `rain` | raindrops screen effect<br>**How:** Full-screen: it takes over the display. **control-C gets you out** -- tested, and none of q, Q, control-D or ESC did. If it has a quit command of its own, its documentation in DOC/ will say. |
| `suicide` | animation: a stick figure walks off a rooftop |
| `suicide1` | suicide, variant |
| `suicide2` | suicide, variant |
| `textb` | &#9733; Mandelbrot set drawn in ASCII on an 80x25 terminal.  Start with X -2.3, Y -2.0, range 4.0, 32 iterations<br>**How:** An ASCII Mandelbrot viewer -- it asks four questions and draws. Try X_Coord -2.3, Y_Coord -2.0, RANGE 4.0, Max Iter 32. Needs Microware's cio. |
| `ttyexp` | fireworks that clear the screen; VT100, wants TERMCAP<br>`Usage: ttyexp <parameters>` |
| `worms` | worms screen effect<br>`usage: worms [-field] [-length #] [-number #] [-trail]` |

</details>

## Amusements

*Generators, simulators and diversions that are not quite games.*

<details><summary>20 programs</summary>

**Curiosities**

| | |
|---|---|
| `areacode` | &#9733; look up a US telephone area code<br>`Usage: areacode nnn nnn ...` |
| `touchtype` | typing tutor<br>**How:** Full-screen: it takes over the display. **control-C gets you out** -- tested, and none of q, Q, control-D or ESC did. If it has a quit command of its own, its documentation in DOC/ will say. |

**Generators**

| | |
|---|---|
| `name` | &#9733; random name generator<br>`Usage: name number-of-names` |
| `newsgen` | &#9733; generate a fake news bulletin |
| `pwgen` | &#9733; random password generator<br>**How:** pwgen <length> [count]. With no arguments it prints nothing and exits, which reads as a hang and is not one. |
| `rndname` | &#9733; random name generator<br>`Usage: name number-of-names` |
| `rpoem` | &#9733; random poem generator (SNOBOL4-in-C).  Data: GAMES/SNOBOL |
| `rstory` | random story generator, roff output.  Data: GAMES/SNOBOL |
| `rstory2` | &#9733; random story generator, second version (SNOBOL4-in-C) |
| `scales` | &#9733; musical scale generator -- writes `scales.lst' in the current directory and prints nothing to the screen<br>`Usage: scales [-h] [-d] [-a] [-m] [-c] [outname]` |
| `travesty` | make a travesty of the input -- Markov chains, DJB<br>`Usage: travesty [ -oord ] [ -nnum ] [ -rrand ] [ -sS ] [ -ACHUVW ]` |

**Simulations**

| | |
|---|---|
| `bio` | biorhythm chart (F. Kaefer 1987) -- BASIC09, needs runb<br>**How:** BASIC09 I-code, not 68000 code. `load runb` first, then run `bio` by BARE NAME. Giving runb a pathname instead raises BASIC09 error 43, which reads like a broken program and is not. |
| `biory` | FORTRAN example: Biorhythm.  Runs and prompts (in German) once os9lib is loaded.  Source: SRC/rtf/biory.f |
| `england` | &#9733; weather simulator - England (Gregorian/mid-Atlantic)<br>**How:** One of six weather simulators that differ only in climate and calendar: england, florida, georgia, minnesota, japan (Japanese calendar) and shire (Middle-earth). Each prints a day's weather and stops. |
| `florida` | &#9733; weather simulator - Florida (Gregorian/Gulf) |
| `georgia` | &#9733; weather simulator - Georgia (Gregorian/S-Atlantic) |
| `japan` | &#9733; weather simulator - Japan (Japanese calendar/N-Pacific)<br>**How:** A weather simulator, not a calendar tool -- see `england'. It uses the Japanese calendar, which is the only reason it looks like one. |
| `logisim` | &#9733; logic circuit simulator -- draws a pulse diagram from a circuit written as text.  Two sample circuits ship with it, DOC/logisim/flipflop.lsi and counter.lsi, and its notes are DOC/logisim/logisim.doc, in German.  IT NEEDS `PORT' SET to a terminal path -- it reopens the keyboard through it -- and nothing on this disk sets it: `setenv PORT /term' first, or it stops with `Environment variable PORT not defined'.  Past that check it floods `No more memory !!!' under this collection's capture harness and has not been seen to draw.  Measured 2026-08-31<br>**How:** Simulates a logic circuit described in a file. The format is in DOC/logisim/logisim.doc; there is no example circuit on the disk. |
| `minnesota` | &#9733; weather simulator - Minnesota (Gregorian/N-Atlantic) |
| `shire` | weather simulator - the Shire (Middle-earth calendar)<br>**How:** A weather simulator using the Middle-earth calendar -- see `england'. |

</details>

## System & modules

*OS-9 module and process tools, devices, system state and scheduling.*

<details><summary>131 programs</summary>

**Devices & disks**

| | |
|---|---|
| `dam` | &#9733; display the disk allocation map -- dam [<drive>] |
| `dedit` | BASIC09 disk sector editor (Carl Kreider) -- read, edit and write raw sectors, decode a disk's identification sector.  I-CODE, not 68000 code: run it with runb and the bare module name, like bio and wysetime.  Nine modules in the one file. |
| `dinfo` | &#9733; disk/device information<br>`Syntax:   dinfo [<opts>] {<device name> [<opts>]}` |
| `dpark` | &#9733; park the DISK HEAD, not a process: `dpark [/device]' restores an RBF device's head to track 00, which is what you did before moving a drive.  Corrected 2026-08-29<br>`Syntax:   dpark [/device]` |
| `shdev` | &#9733; show devices |
| `ssl` | &#9733; show a file's segment list, sector by sector -- ssl <file> |

**Keeping and dropping**

| | |
|---|---|
| `drop` | put back exactly what keep wrote.  It refuses to remove any file whose checksum has changed, so your saves and scores are safe from it by construction.<br>`Usage: keep [-n] [-f] [-q] [-s] [-p <dir>] <program>...` |
| `keep` | take a program off this collection onto your own disk -- copies it and whatever DOC/DEPENDS says it needs, and records every file written.  `keep -n' shows what it would do without doing it.  See DOC/README-KEEP.<br>`Usage: keep [-n] [-f] [-q] [-s] [-p <dir>] <program>...` |
| `kept` | list what has been taken, and how much it came to<br>`Usage: keep [-n] [-f] [-q] [-s] [-p <dir>] <program>...` |

**Microware runtime**

| | |
|---|---|
| `cio` | Microware's C library trap module -- what every starred program here needs.  Included with Microware's permission; see SOURCES.txt.  You do not run it, it loads itself. |
| `csl` | Microware's C Shared Library, for programs built with Ultra C rather than cc 3.2 (68000) |
| `csl020` | the same, for 68020/030/040 |
| `math` | Microware's floating-point trap module (software) |
| `math881` | the same, using a 68881/68882 coprocessor.  Both register as the module `math'; load whichever suits your machine. |

**MM/1 drivers**

| | |
|---|---|
| `keydrv.mm1` | keyboard driver |
| `msdrv.901_340` | mouse driver |
| `msdrv_340.901.ms` | the mouse driver's device descriptor |
| `rb37c65` | floppy driver (37C65 controller) |
| `scsi_mm1a` | SCSI driver |
| `snddrv` | sound driver |
| `windio.52` | windowing terminal driver |

**OS-9 modules**

| | |
|---|---|
| `bootgen` | &#9733; generate an OS-9 boot file<br>`Syntax:   bootgen [<opts>] <device> {<path> [<opts>] }` |
| `bsplt68` | Split a boot file into its component modules (Carl Kreider) |
| `flink` | &#9733; list a module's links<br>`usage: flink [ -? \| filename { filename } ]` |
| `gen` | generates the FRAME of a new C program -- header block, authorship and version lines and the sectioned comments a Microware example was laid out with.  IT APPENDS `.c' to whatever name you give it, which is why it looks as though it wrote nothing: `gen -p frame' leaves `frame.c'.  `-m' does a module frame, `-t' a type, `-f' a function declaration.  Clarified 2026-08-29<br>`Syntax: gen [<opt>] <pathname> [<opts>]` |
| `load` | load a module into memory, so a program that LINKS a library MODULE can find it -- `load /dd/CMDS/os9lib' and the RTF Fortran set comes alive, where before it printed nothing.  A clean-room reimplementation of Microware's load, written from the published manuals and contributed by the os9exec project; maintained here now, source in SRC/load, built trap-free so it needs no cio<br>`Syntax:   load [<opts>] {<module> [<opts>]}` |
| `mexist` | &#9733; test module existence<br>`Usage: mexist [options] <Module>` |
| `os9lib` | RTF/68K FORTRAN run-time LIBRARY.  Not a program: rtf, for, lnk, biory and creadoc all F$Link it, and every one of them fails E_MNF until it is in the module directory.  See DOC/README-FORTRAN.  Running it AS a program executes its floating-point code and stops -- that is not a fault. |
| `ptxm` | Path Table eXtension Module (Nick Holgate, 1995): a KERNEL extension letting user-state processes open unlimited I/O paths.  Courtesyware, free.  Needs supervisor state, so it cannot install under os9exec.  DOC/ptxm/ptxm.txt |
| `rtfdat` | RTF FORTRAN data module |
| `version` | &#9733; prints ITS OWN version and nothing else -- `Dies ist das Program 'version', Version 7' -- whatever module you name. `ident' and `modinfo' show a module's edition.  Corrected 2026-08-29 |
| `vmod_trap` | the VMod_trap trap library rxmod and txmod need.  Type-$0B, and it runs in SUPERVISOR state, so it installs here and then faults.  Renamed from lowercase `vmod_trap' -- rxmod asks for `VMod_trap' and real OS-9 matches exactly and it runs in SUPERVISOR state, so it installs here and then faults.  Renamed from lowercase `vmod_trap' -- rxmod asks for `VMod_trap' and real OS-9 matches exactly |

**Processes & memory**

| | |
|---|---|
| `aprocs` | &#9733; process monitor -- and it does NOT run under os9exec: it calls F$SetSys twice, which the emulator does not implement, and is then aborted (E_PRCABT).  DOC/STATUS has had this since 2026-08; the entry here did not say it.  `procs', `top' and `sysmon' are the other process listers.  Added 2026-08-30<br>`Syntax: aprocs [<opts>]` |
| `launch` | &#9733; NOT a background launcher.  M.C.Gregorie's login helper: sets the environment for the terminal type, optionally a default PATH and emacs bindings, from /dd/SYS/config, then starts the shell named on its command line.  Corrected 2026-08-28<br>**How:** Says "nothing to launch" until it is configured -- see its documentation. |
| `signal` | &#9733; send a signal to a process<br>`Syntax: signal <process-id> <signal-code> [<seconds>]` |
| `sysmax` | &#9733; shows the system's maximum process AGE, not its memory -- `system maximum age is 0' here, because os9exec does not implement the F$SetSys call it uses.  Corrected 2026-08-29 |
| `sysmin` | &#9733; shows the system's minimum process PRIORITY, not its memory -- `system minimun priority is 0' here, same unimplemented F$SetSys.  Corrected 2026-08-29 |
| `sysmon` | &#9733; system monitor -- refuses to start: `OS9/68k V4.0 is too old for SYSMON V6.1'<br>`Syntax: sysmon [<opt>]` |
| `t` | tiny test/stub binary |
| `top` | &#9733; show the busiest processes -- prints its heading and then aborts (E_PRCABT).  `aprocs' aborts the same way<br>`Syntax: top [<opts>] [<num>]` |
| `vis` | &#9733; NOT the Unix `vis': it repeatedly runs a command and refreshes the screen with the output, which is what `watch' does elsewhere -- `vis {opts} <command> <args>'.  Corrected 2026-08-29 |
| `who` | 'who is logged in'.  Written in MICROWARE SHELL syntax ('!' pipes, `( )&' groups, `*' comments), not sh or bash, so no shell here can run it.  It wants `procs', `sleep', `qsort' and `tr', none of which are on this disk -- but `field' and `join', which it also uses, ARE here, and `qsort9' is that sort under another name.  Corrected 2026-08-29: field was listed among the missing and is not. |

**Scheduling**

| | |
|---|---|
| `cron` | run commands at specified times (daemon) |
| `every` | &#9733; run a command at intervals<br>`Syntax: every <time> <progname> [<progopts>]` |
| `repeat` | repeat an OS-9 command N times -- `repeat 3 <command>' -- and it cannot here.  It hands the command to whatever $SHELL names, in the form Microware's shell takes: `sh' answers `file not found' because it cannot fork an absolute pathname and `bash' answers `cannot execute binary file' because it treats the module as a script. It also prints `free() called with bad address' on the way out.  Measured 2026-08-29<br>`syntax: repeat [number of repetitions] [OS-9 command]` |

**System state**

| | |
|---|---|
| `clock` | display a clock |
| `date` | Print date and time -- it prints the YEAR AS 2100.  `today' gets it right; setime2, setyear and fixyear are the Y2K repairs beside it |
| `loglist` | &#9733; log listing<br>`Syntax   : loglist [-option(s)]` |
| `oskversion` | &#9733; report the OS-9/OSK version<br>`Syntax:   OSKversion` |
| `setime` | Set system time (prompts YYMMDDHHMMSS) |
| `sysid` | &#9733; show system identification |

**Users and login**

| | |
|---|---|
| `adduser` | &#9733; add a user to the system, for uucp logins<br>`Usage: adduser [opts] [<username> [<userid>] ]` |
| `passwd` | change your own password in /dd/SYS/password.  Matches on the user NAME, and the name must be spelt exactly as the password file has it, capitals included.  Matthias Rosenthal's, EFFO forum disk 5; source in SRC/passwd.<br>`Syntax: passwd` |

**Utilities**

| | |
|---|---|
| `about` | what this collection knows about one program: what it is, what it is for, where it came from, the files it opens and whether they are here, and whether its source survived. Reads DOC/INDEX, CATEGORIES, ORIGINS and DEPENDS for you. what it is for, where it came from, the files it opens and whether they are here, and whether its source and documentation survived.  One card per program -- `about hack'.  DOC/CATEGORIES browses; this answers.<br>`Usage: about <program>...` |
| `add_errmsg` | &#9733; build vi's error-message file -- it wants /dd/SYS/vi_errmsg, which is here |
| `argproc_demo` | demonstration of argproc(), RICO's command-line argument parser.  STOPS WITH `**** Stack Overflow ****' whatever it is given -- its M\$Stack is 3072, the same as programs that work, so the fault is its own.  Source and the argproc library manual are now here: SRC/argproc and DOC/argproc_demo/man.argproc, from EFFO forum 7 |
| `bigsetter` | Modula-2 set-operations demonstration |
| `bootlogger` | &#9733; log what happens during boot |
| `break` | send a BREAK on a serial line (assembler example) -- and under os9exec it reaches F$SysDbg and stops the EMULATOR in its own debugger, waiting for an answer.  In a script that is a hang<br>`Syntax: break` |
| `btop` | bitmap to Gepard fat-font<br>`Syntax:   BtoP [<opts>] [<path1>] [<opts>] [<path2>] [<opts>]` |
| `btree` | &#9733; B-tree file handling demonstration and test |
| `clear` | &#9733; clear the screen<br>`Syntax:   clear` |
| `combine` | &#9733; interleave two files BYTE BY BYTE, one supplying the even bytes and the other the odd -- how a 16-bit EPROM image is put back together from two 8-bit halves.  F.R.Schmitt, 1989.  Clarified 2026-08-29<br>`Syntax: combine [<file1>] [<file2>] [<outfile>] [<opt>]` |
| `config` | report this machine's C type properties as #defines -- char, short, int, long, pointer and float all come out; it then aborts where `double' begins, because that needs a 68881 or Microware's fpu.  See DOC/README-BUSERR |
| `cpu` | &#9733; CPU speed test -- draws its bar chart and its answer (156 MHz, which is the emulator), then traps on vector $07 and takes the session down with it |
| `demerge` | split a merged file back into its parts<br>`Syntax:   demerge <path>` |
| `demo` | egetopt option-parsing demonstration |
| `deton` | &#9733; NOT a detab: `deton [seconds]' demonstrates using an alarm to TIME OUT an I/O read.  `detab' and `expand' are what convert tabs.  Corrected 2026-08-29<br>`syntax: deton [seconds]` |
| `devprc` | show which device belongs to which process.  REBUILT HERE: the archived module has a bad CRC and a corrupt initialised- data descriptor, and does not load.  -h works; -a needs the kernel process table, which os9exec answers without real data |
| `dload` | &#9733; NOT a serial download: `dload <filename>' LOADS A DATA FILE INTO A DATA MODULE, which is its own usage line. `sbreak' and `break' are the serial-line examples here. Corrected 2026-08-29<br>`Syntax: dload <filename>` |
| `e` | SEDT editor, VT220 keys.  FIXED 2026-08-28: it wants sys/sedt.keys, sys/sedt.ruler0 and sys/sedt.help, none of which were here -- it stopped with `Could not open key definition file'.  All three are in SYS now, recovered from the EFFO forum 11 archive it came from |
| `em` | a screen editor (EFFO forum 3)<br>**How:** A screen editor. It stops with "Environment variable TERM not defined!" unless TERM is set -- SYS/login sets it, so run it from a login shell rather than bare. |
| `epson` | &#9733; spline output driver for an Epson printer<br>`usage: epson [<opts>]` |
| `expreserve` | &#9733; vi's crash-recovery helper: preserves an edit buffer when the editor dies.  Like ksh it reads the terminal asking for more bytes than you type (388), so it depends on the same emulator behaviour -- see DOC/README-KSH<br>**How:** Saves a vi buffer when the editor or the line dies; vi runs it for you rather than you running it. |
| `exrecover` | &#9733; recover a vi buffer that expreserve saved<br>**How:** Recovers what expreserve saved. Again, vi's helper rather than a command you start. |
| `fastcc` | &#9733; a faster front end for cc |
| `fixyear` | Y2K: correct a date the clock got wrong<br>`Usage: fixyear [-opt] <file\|dir> <dir\|file> [-opt]` |
| `fontgen` | generate a font for the Gepard display<br>**How:** Generates a character font for the Gepard display -- it prints the assembler source of an 80-column font on stdout. |
| `getsys` | &#9733; report the system's globals -- what OS-9 thinks it is running on<br>`Syntax: getsys [<opts>]` |
| `ggrep` | &#9733; GNU grep, from the sh_utils collection<br>**How:** GNU grep. `ggrep <expr> <files...>'; -E, -F, -i, -v, -w and the rest as you would expect. |
| `greg` | &#9733; NOT a regular-expression anything: it converts a JULIAN DAY NUMBER to a Gregorian date.  `greg 2461281' answers `2026 8 29'.  Corrected 2026-08-29 |
| `hinterhalt` | &#9733; a small game (EFFO forum 7) |
| `i_am_i` | prints its own source (Pascal) |
| `isam` | &#9733; indexed-sequential file demonstration |
| `lfmaker` | make a G-Windows launch file -- and it FLOODS `No more memory !!!' as soon as it is given an argument, which is the F$SRqMem storm DOC/STATUS lists.  Measured 2026-08-29 |
| `lgrep` | &#9733; line grep<br>`Syntax: lgrep <arg1> ... <argn>` |
| `liborder.os9` | report the order of modules in a library<br>`Usage: liborder <options> file1.r file2.r ...` |
| `lpsched` | &#9733; the line-printer scheduler<br>`Syntax: lpsched [-r] {<devname>}` |
| `makecrc` | compute a CRC |
| `map` | &#9733; NOT a memory map: `map <file>' shows the disk BLOCKS a file occupies, sector by sector.  `mfree' and `free' are the memory ones.  Corrected 2026-08-29<br>`Syntax: map [<opts>] <file> {<file>}` |
| `modinfo` | report a module's header -- name, type, size, edition, CRC<br>`Syntax:   module [modulename]` |
| `mshell` | &#9733; a MENU shell: it takes a menu file as its argument and says `Could not open <name> (menufile)' without one.  It also needs TERM set, as every full-screen program here does.  Corrected 2026-08-29; an earlier note said only that it wanted a terminal, which was an artefact of probing it with no TERM in the environment |
| `mvolformat` | format a multi-volume set<br>`Syntax: mvolformat drive volname volcount [format options]` |
| `names` | &#9733; list the names of modules in a file -- and it DOES NOT COME BACK: given a module it prints nothing and never returns, with a file on its standard input or without. `ident', `modinfo' and `module_census' all answer the same question.  Measured 2026-08-29 |
| `new_e` | SEDT editor, generic terminal -- it picks vt100 or vt220 by TERM.  Needs the same three SYS/sedt.* files as `e' |
| `phone` | connect two terminals -- NOT an address book<br>`Syntax: phone <communication-path>` |
| `preset` | preset memory to a pattern |
| `pri` | change a process's priority |
| `ptob` | Gepard fat-font back to bitmap<br>`Syntax:   PtoB [<opts>] [<path1>] [<opts>] [<path2>] [<opts>]` |
| `ptxminst` | install Ptxm.  NOT a pseudo-tty installer -- that is what this entry said until 2026-08-19 and it was wrong |
| `rndir` | &#9733; rename a directory<br>`Syntax: rndir [<opt>]` |
| `screen` | &#9733; NOT the terminal multiplexer.  Russ Smith's `screens': picks a file at random from $HOME/.SCREENS and shows it. On OS-9 it runs the file rather than printing it, through system(), so it requires Microware's `shell' on your execution path.  Source in SRC/screen, man page in DOC/screen/screens.6.  Reworded 2026-08-30 |
| `screen_nocio` | our source build, and the trap-free one: CMDS/screen stops without cio and this does not |
| `scsiutil` | SCSI device utility<br>`Usage: SCSIutil [/scsi_dev@] <command>` |
| `setime2` | Y2K: set the system time, four-digit year<br>`Syntax:   setime2 [<opt>] [<setime2>] [<opt>]` |
| `setyear` | Y2K: set the year directly<br>`Syntax:   setyear <YYYY>` |
| `snd_sig` | &#9733; send a signal to a process<br>`Syntax:   snd_sig [-options] pid pid1...pidn` |
| `spline` | &#9733; fit a spline through points, output PostScript |
| `sqrtx` | square-root demonstration |
| `submit` | &#9733; submit a job to the print spooler<br>`Syntax: submit [<opts>] [<submit file>] [{<parameter>)]` |
| `suse` | show a program's usage line -- it prints nothing, for any module tried, by name or by path, and nothing for -? either. Re-measured 2026-08-29 and still true |
| `suspend` | &#9733; REMOVES a process from the system -- its own usage line says so -- rather than suspending it.  F.R.Schmitt, 1989.  Clarified 2026-08-29<br>`Syntax  : suspend  [<processname>]  [<opt>]` |
| `t_trtest` | RICO trap-handler test |
| `testibc` | IEEE binary-coded test (Pascal) |
| `transfer` | &#9733; copies files from GDOS DISKS to OS-9, and takes no options at all -- not a general device-to-device copier.  `cp', `copy' and `dsave' are those. Corrected 2026-08-29<br>`Syntax: transfer` |
| `trunc` | &#9733; truncate a file to a given length<br>`Syntax: trunc <path> <num>` |
| `tty` | &#9733; report the terminal's name |
| `umacs` | &#9733; MicroEMACS -- a small Emacs, EFFO forum 1<br>**How:** A small Emacs (uMacs 1.0). Full-screen: it takes the display and shows "== uMacs 1.0 == main ==" at the foot. This line said it needs `. /dd/SYS/termcap.entry' sourced first; measured 2026-08-29, it does not. |
| `umusek` | UMusEK -- a music editor; wants a screen address |
| `unpacklib.os9` | unpack a library into its object modules<br>`Usage: unpacklib <options> file1.l file2.l ...` |
| `vc` | &#9733; a SPREADSHEET -- `Welcome to the Spreadsheet Calculator, type ? for help', with rows, columns and a formula line.  Not a visual compare, which is what this entry said until 2026-08-28 |
| `vecho` | echo without a newline (from less) |
| `vlen` | &#9733; a VARIABLE-LENGTH RECORD demonstration, not a reporting tool: it ignores whatever you give it, creates a filesystem of its own, adds a hundred records of varying length and prints the minimum, the maximum and the mapper entries as it goes.  `isam' is the other demonstration of its kind here.  Corrected 2026-08-29 |
| `what` | Not the SCCS `what' -- it does not read a binary at all.  It prints `What's where in the GEPARD:' and a table of I/O address, reference byte and card name: an inventory of the expansion cards in a GEPARD, the German 68k machine much of the EFFO material was written on.  The table is empty here, there being no GEPARD.  It ignores its arguments.  Added to this index 2026-08-30, having never been in it; the first entry written for it guessed SCCS from the name and was wrong within the hour<br>**How:** NOT the SCCS `what`. It prints "What's where in the GEPARD:" and a table of expansion cards -- an inventory tool for the GEPARD, the German 68k machine. Empty here, there being no GEPARD, and it ignores its arguments. Measured 2026-08-30. |
| `xlharc` | extract LHarc archives<br>`Usage: xlharc {axevlufdmctp}[qnftv] archive_file [files or directories...]` |
| `yagi` | Yagi antenna design calculator |
| `ynad` | &#9733; YNAD -- Yet Another Name & Address program.  A contact database, not a yes/no dialogue.  Corrected 2026-08-28 |

**Vendor demos**

| | |
|---|---|
| `ob68kdemo` | OmniBasic 1.16 -- a BASIC compiler.  Limited symbol table; otherwise the including compiler.  Run it from /dd/DOC/omnibasic, where its library and examples are. Like UniBasic it needs Microware's cc to finish a build<br>**How:** OmniBasic 1.16, same arrangement as ub68kdemo and the same SHELL trick -- see its entry. Run it from /dd/DOC/omnibasic. DEMO VERSION, capped symbol table. |
| `sddemo` | White's Speedisk 2.10 -- disk de-fragmenter.  Wants an 80x24 screen; falls back to tty mode<br>**How:** White's Speedisk 2.10 de-fragmenter, demo build. Wants an 80x24 screen and drops to tty mode without one. |
| `ub68020demo` | UniBasic 1.10 for the 68020 -- the same demonstration as `ub68kdemo' and it runs the same way, announcing `OS9/68020 Version' where the other says 68000.  It was filed as silent until 2026-08-29 and never was |
| `ub68kdemo` | UniBasic 1.10 -- a BASIC compiler, same arrangement as OmniBasic.  Run it from /dd/DOC/unibasic<br>**How:** UniBasic 1.10, and it does compile -- the trick is that it runs its build through $SHELL. With SHELL unset it hunts for `/dd/bash' and dies with "Error Exit" and error 216. Do `setenv SHELL /dd/CMDS/sh', work in a directory holding basic.h and basic.l (DOC/unibasic has them), have your C toolchain reachable with CDEF and CLIB set, and give it memory. Verified end to end. DEMO VERSION: the symbol table is capped, nothing else is. |

</details>

## Disk & DOS

*Reading and writing MS-DOS media with the mtools set.*

<details><summary>20 programs</summary>

| | |
|---|---|
| `msattrib` | mtools 3.6 -- MS-DOS attrib (drive a: and b: are ready)<br>`Usage: msattrib [-p] [-a\|+a] [-h\|+h] [-r\|+r] [-s\|+s] msdosfile [msdosfiles...]` |
| `msbadblocks` | mtools 3.6 -- MS-DOS badblocks (drive a: and b: are ready)<br>`Usage: msbadblocks [-V] device` |
| `mscd` | mtools 3.6 -- MS-DOS cd (drive a: and b: are ready)<br>`Usage: mscd: [-V] msdosdirectory` |
| `mscheck` | mtools disk verifier.  A ksh script (#!ksh), and ksh is starred, so this one wants cio too.  Drives a: and b: are ready. |
| `mscopy` | mtools 3.6 -- MS-DOS copy (drive a: and b: are ready)<br>`Usage: mscopy [-tnmvV] sourcefile targetfile` |
| `msdel` | mtools 3.6 -- MS-DOS del (drive a: and b: are ready)<br>`Usage: msdel [-v] msdosfile [msdosfiles...]` |
| `msdeltree` | mtools 3.6 -- MS-DOS deltree (drive a: and b: are ready)<br>`Usage: msdeltree [-v] msdosfile [msdosfiles...]` |
| `msdir` | mtools 3.6 -- MS-DOS dir (drive a: and b: are ready)<br>`Usage: msdir: [-V] [-w] [-a] msdosdirectory` |
| `msformat` | mtools 3.6 -- MS-DOS format (drive a: and b: are ready)<br>`Usage: msformat [-V] [-t tracks] [-h heads] [-s sectors] [-l label] [-n serialnumber] [-S hardsectorsize] [-M softsectorsize] [-1][-2 track0sectors] [-0 rate0] [-A rateany] [-a]device` |
| `msinfo` | mtools 3.6 -- MS-DOS info (drive a: and b: are ready)<br>`Usage: msinfo [-v] drive` |
| `mslabel` | mtools 3.6 -- MS-DOS label (drive a: and b: are ready)<br>`Usage: mslabel [-vscV] drive:` |
| `msmd` | mtools 3.6 -- MS-DOS md (drive a: and b: are ready)<br>`Usage: msmd [-itnmvV] file targetfile` |
| `msmove` | mtools 3.6 -- MS-DOS move (drive a: and b: are ready)<br>`Usage: msmove [-itnmvV] file targetfile` |
| `msrd` | mtools 3.6 -- MS-DOS rd (drive a: and b: are ready)<br>`Usage: msrd [-v] msdosfile [msdosfiles...]` |
| `msread` | mtools 3.6 -- MS-DOS read (drive a: and b: are ready)<br>`Usage: msread [-tnmvV] sourcefile targetfile` |
| `msren` | mtools 3.6 -- MS-DOS ren (drive a: and b: are ready)<br>`Usage: msren [-itnmvV] file targetfile` |
| `mstoolstest` | mtools 3.6 -- MS-DOS toolstest (drive a: and b: are ready)<br>`Usage: export COUNTRY=countrycode[,[codepage][,filename]]` |
| `mstype` | mtools 3.6 -- MS-DOS type (drive a: and b: are ready)<br>`Usage: mstype [-tnmvV] sourcefile targetfile` |
| `mswrite` | mtools 3.6 -- MS-DOS write (drive a: and b: are ready)<br>`Usage: mswrite [-tnmvV] sourcefile targetfile` |
| `mtools` | MS-DOS disk suite -- front end listing its sub-commands<br>`Usage: mtools [-p] [-a\|+a] [-h\|+h] [-r\|+r] [-s\|+s] msdosfile [msdosfiles...]` |

</details>

## Time & calendar

*Calendars, clocks and astronomy.*

<details><summary>14 programs</summary>

**Astronomy**

| | |
|---|---|
| `ephem` | &#9733; ephem - astronomical ephemeris<br>**How:** An astronomical ephemeris: it shows where the Sun, Moon and planets are, for a place and a moment. It starts LOOPING -- press any key to stop and enter command mode. CONTROL-D QUITS; `?' is help; control-L redraws. In command mode the arrow keys (or h/j/k/l) move between fields: RETURN opens the one under the cursor, type a value, RETURN accepts. `d' jumps to the date, `z' to the step size. The point of the program is that last pair: set StpSz to a day and NStep to 30, press `q', and it runs time forward and you watch the planets move. |
| `ephem881` | &#9733; ephem, 68881 build<br>**How:** The same program built for a 68881 coprocessor -- see the note for `ephem'. CONTROL-D quits. |
| `lunisolar` | &#9733; lunar and solar position calculator |
| `nasa` | &#9733; NASA orbital-element reader.  Wants `nasa.dat' in the CURRENT directory: NORAD two-line element sets -- a name line, then TLE line 1 and line 2 per satellite -- and writes kepler.dat. No element set ships here; supply a current one.  The format is parsed in SRC/eff_orbit/nasa.c and is column-sensitive<br>**How:** The program that FEEDS orbit. Give it NASA two-line elements in a file called nasa.dat in the current directory and it writes kepler.dat, which is what orbit reads. Neither file ships -- you supply nasa.dat. |
| `orbit` | &#9733; N3EMO satellite orbit simulator v3.7, and it RUNS.  It needs its data directory set to where its files are -- it opens them by bare name, and they are in DOC/orbit: kepler.dat (the satellite database), <site>.sit (the observing station -- pgh, bern and zuerich all ship) and mode.dat (the transponder schedule).<br>**How:** The N3EMO satellite tracker, and it works. It opens kepler.dat, mode.dat and a <site>.sit BY BARE NAME in the DATA DIRECTORY, and they live in DOC/orbit -- so on your own OS-9 system it is `chd /dd/DOC/orbit` then `orbit`. Under os9exec neither shell will do that for you (bash's cd does not move the data directory; sh cannot launch a program here at all), so bring the three files to the directory you are in: `cat /dd/DOC/orbit/kepler.dat > kepler.dat` and so on. Then answer: satellite letter, site name without the .sit, month day year, hour, days, minutes per sample, RETURN for the terminal. Measured 2026-08-30. |

**Calendars**

| | |
|---|---|
| `cal` | &#9733; Calendar, Bob van der Poel.  `cal -h' prints holidays with it -- SYS/holidays is here, and SYS/birthdays is an empty template for your own dates.  SYS/cal.init is a printer setup for a laser<br>**How:** `cal -h' prints holidays alongside the calendar -- SYS/holidays is on the disk now, and SYS/birthdays is an empty template the holidays file INCLUDEs, so anything you add there shows up too. Add `-g' if the rule under the day names comes out as garbage on your terminal. |
| `calen` | calendar printer (v_misc) |
| `calender` | &#9733; print a whole year's calendar (German)<br>**How:** Prints the year in GERMAN. Not a typo of `calendar' -- a different program by a different author. |
| `digclk` | &#9733; digital clock with hostname<br>`Usage: digclk [refresh_rate]` |
| `easter` | &#9733; compute the date of Easter<br>**How:** Prints Easter dates for 1988 to 2000 and nothing else. The range is compiled in. |
| `gcl` | &#9733; displays a GRAND DIGITAL CLOCK, not a calculator: `gcl {opts} [bkgnd]'.  `digclk' is the other clock of its kind here.  Corrected 2026-08-29 |
| `qt` | &#9733; tells the time IN WORDS, the way a person would say it: `It's just gone ten past four.'  Not a text utility. `today' is the other one of its kind here.  Corrected 2026-08-29 |
| `setimex` | &#9733; set time from hardware clock<br>`Usage:` |
| `today` | date, moon phase and this-day-in-history |

</details>

## Maths & calculators

*Calculators, plotting, orbits and number theory.*

<details><summary>9 programs</summary>

**Calculators**

| | |
|---|---|
| `cam` | &#9733; CAMSHAFT, not camera: it asks for the rocker ratio, the lift at a crank angle and the base circle, and plots the lift curve for an intake lobe.  The plot is Tektronix vectors, so on a vt100 it arrives as characters -- the dialogue above it is the readable part.  Corrected 2026-08-29 |
| `chbase` | &#9733; converts a NUMBER from one base to another -- Philip Maechler's, and nothing to do with a module's base address.  `cvtbase' is the other one, and floods. Corrected 2026-08-29<br>`Syntax   : chbase <number> [ <base A> [ <base B> ] ]` |
| `cvtbase` | &#9733; convert a number between bases -- names them by KEY (b, d, h or x, o), and then FLOODS `No more memory !!!' without converting anything.  Its usage line prints fine, which is why it looked healthy |
| `loan` | &#9733; loan/amortisation calculator |
| `rechne` | &#9733; calculator, German -- and it takes ONE expression with no spaces in it: `rechne 4095+1' answers 4096, $1000 and the binary.  Spaced out it evaluates each argument separately |
| `rpn` | &#9733; RPN calculator -- and its `+' is wrong: 12, 34, + leaves a stack of three with 0 on top instead of one with 46. `rechne' is the calculator that answers correctly |
| `sc` | sc -- spreadsheet calculator (needs TERM)<br>**How:** The spreadsheet, version 6.16. `sc' opens and says "Type '?' for help". This line said it will not read SYS/termcap and needs `. /dd/SYS/termcap.entry' first; measured 2026-08-29, it does not -- it opens with TERMCAP as SYS/login sets it. |

**Spreadsheets**

| | |
|---|---|
| `oleo` | GNU Oleo 1.6 -- a spreadsheet, and it DOES NOT RUN: illegal instruction at 000465d2, process aborted.  `sc' is the spreadsheet that works<br>**How:** GNU Oleo, a spreadsheet, and it DOES NOT RUN whatever you do: `Illegal instruction: 0009' and E_PRCABT, from a full login session with TERM set as much as from a bare shell. This line said the login was the answer until 2026-08-29; it was measured that day and it is not. Use `sc', the other spreadsheet here, which is an unrelated program and works. |
| `scqref` | &#9733; Quick reference for sc, the spreadsheet on this disk |

</details>

## Printing

*Spoolers, page formatting and PostScript.*

<details><summary>14 programs</summary>

**PostScript**

| | |
|---|---|
| `gs33` | Ghostscript 3.33 -- the older one, and it has never had the gs_init.ps and fonts it needs.  Use gs403 instead<br>`Usage: gs ... -%c file.ps arg1 ... argn` |
| `gs403` | Aladdin Ghostscript 4.03, and this one is COMPLETE: its init files and fonts are in LIB/gs403.  Point GS_LIB at that directory and it interprets -- `export GS_LIB=/dd/LIB/gs403' in bash, NOT `setenv', which is the OS-9 shell's and is not a bash command.  It then reads a PostScript file and drops to its own `GS>' prompt.  This entry said it does not render, on a measurement made with GS_LIB unset by a `setenv' that had failed.  Runs with no trap handler -- built with GCC 2.5.8 by its porter.  Corrected 2026-08-30<br>**How:** Aladdin Ghostscript 4.03. Point GS_LIB at its library first -- in bash that is `export GS_LIB=/dd/LIB/gs403`, NOT `setenv`, which is the OS-9 shell's command and gets "setenv: command not found" here; this line said setenv until 2026-08-30. Then `gs403 -q -dNOPAUSE -sDEVICE=nullpage <file>.ps` reads the file and gives you its GS> prompt. Everything it needs, fonts included, is in that directory. The older gs33 on this disk has never had its support files. |
| `lwf` | ASCII to PostScript, like Unix enscript.  Reads its prologue from /dd/USR/LIB/lwf.prologue<br>**How:** Turns plain text into PostScript, the way Unix enscript does. It reads /dd/USR/LIB/lwf.prologue and stops without it. No PostScript printer here, so send the output to a file and take it elsewhere. |

**Printers**

| | |
|---|---|
| `alps` | &#9733; Switch an ALPS ASP-1000 printer between draft and NLQ<br>`Syntax: alps [<opts>] >/<device>` |

**Spooler**

| | |
|---|---|
| `splman` | &#9733; OS-9 print spooler: manager (Carl Kreider) |
| `splprt` | &#9733; OS-9 print spooler: printer process |
| `splstat` | &#9733; OS-9 print spooler: queue status.  Needs a queue to look at |

**Spooling**

| | |
|---|---|
| `lmargin` | &#9733; set the left margin ON AN EPSON PRINTER -- its own usage line says `epson'.  It is a printer control, not a text filter; `fmt', `proff' and `pep' are what indent text.  Clarified 2026-08-29<br>`usage: epson [<opts>]` |
| `lp` | &#9733; line printer spooler - submit a job<br>`Syntax: lp [<opts>] {<path>}` |
| `lpq` | &#9733; shows the spooler queue -- and answers `no spooler installed' here.  It looks for a DATA MODULE called `spoolqueue' in memory, not for SPL/splq; starting `splman' does not create it and nothing on this disk does.  Same for `prjob' and `lp'.  Measured 2026-08-29<br>`Syntax: lpq [-p=dev] [user]` |
| `lprm` | &#9733; remove a job from the print queue<br>`Syntax: lprm [-d=dev] [-] job..` |
| `lpshut` | &#9733; shut down the printer scheduler<br>`Syntax: lpshut` |
| `perr` | &#9733; print an OS-9 error message<br>`Syntax: perr [<error_codes>]` |
| `prjob` | &#9733; print a job |

</details>

## Documentation

*Pagers, readers and the help system.*

<details><summary>5 programs</summary>

**Pagers**

| | |
|---|---|
| `lessecho` | &#9733; Helper for less<br>`usage: lessecho [-ox] [-cx] [-pn] [-dn] [-a] file ...` |
| `lesskey` | Compile a key-binding file for less<br>`usage: lesskey [-o output] [input]` |

**Readers & pagers**

| | |
|---|---|
| `help` | help system<br>`Syntax:   help [<opts>] [<topic> {<subtopic>}] [<opts>]` |
| `helpindex` | &#9733; build the help index<br>`Syntax:   helpindex [<opts>] {<help file>} [<opts>]` |
| `less` | Pager (wants a real TERM).  Its help screen works now: SYS/less.hlp is on the disk |

</details>

---

&#9733; needs Microware's `cio`, which is not on the disk — `DOC/README-CIO` explains how to point at your own.

Generated by `tools/gen_catalog.py` from the disk's own documents. Do not edit by hand; it will be overwritten.
