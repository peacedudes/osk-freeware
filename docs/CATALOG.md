# What is on this disk

936 programs of OS-9/68K community software, gathered from the archives that kept it and made to run again. **585 of them need nothing but this disk**; the rest want Microware's `cio`, marked below with a star.

`DOC/INDEX` on the disk lists everything alphabetically. This is the same collection sorted by what each program is *for*, which is the more useful order when you do not yet know what you are looking for.

> Open a program in `docs/index.html` for its **sample output** --
> captured from that program running on the disk image.
>
> Prefer to click around? `docs/index.html` is a searchable version with per-program detail — what it needs, where it came from, on what terms. GitHub will not render it here; download the repository and open it, or enable Pages.

| Category | Programs | |
|---|--:|---|
| [Shells](#shells) | 21 | Unix shells to sit beside OS-9's own -- bash and ksh bring history, job control, and scripts that come across unchanged. |
| [Editors](#editors) | 27 | vi and emacs in several flavours, line and stream editors, and editors for binary and hex. |
| [Text tools](#text-tools) | 114 | Search, sort, compare, reformat, split and spell-check. |
| [Files & directories](#files--directories) | 32 | Listing, copying, finding, renaming, and knowing what you have. |
| [Developer tools](#developer-tools) | 46 | Version control, tags, cross-reference, formatters, a debugger and benchmarks. |
| [Compilers & build](#compilers--build) | 40 | C compilers and their passes, assemblers, linkers, make and parser generators. |
| [Languages](#languages) | 10 | Interpreters and language systems beyond C. |
| [Archives & compression](#archives--compression) | 37 | Pack, unpack and shrink -- lha, zip, tar, arc, zoo, and OS-9 module libraries. |
| [Encoding & conversion](#encoding--conversion) | 24 | Between text encodings, line endings, Macintosh formats, ciphers and hashes. |
| [Communications](#communications) | 96 | Kermit in several builds, terminal sessions, and networking. |
| [Graphics & images](#graphics--images) | 202 | The netpbm toolkit, JPEG, a ray tracer, and things that draw. |
| [Games](#games) | 67 | Adventures, board and card games, arcade ports, dungeon crawls and puzzles. |
| [Screen toys](#screen-toys) | 10 | Animations and screen effects -- they draw on the terminal rather than print to it. Some run until you stop them. |
| [Amusements](#amusements) | 19 | Generators, simulators and diversions that are not quite games. |
| [System & modules](#system--modules) | 127 | OS-9 module and process tools, devices, system state and scheduling. |
| [Disk & DOS](#disk--dos) | 20 | Reading and writing MS-DOS media with the mtools set. |
| [Time & calendar](#time--calendar) | 13 | Calendars, clocks and astronomy. |
| [Maths & calculators](#maths--calculators) | 11 | Calculators, plotting, orbits and number theory. |
| [Printing](#printing) | 15 | Spoolers, page formatting and PostScript. |
| [Documentation](#documentation) | 5 | Pagers, readers and the help system. |

## Shells

*Unix shells to sit beside OS-9's own -- bash and ksh bring history, job control, and scripts that come across unchanged.*

<details><summary>21 programs</summary>

**Shell helpers**

| | |
|---|---|
| `checkenv` | &#9733; compares an environment variable with a value for a script to branch on: `checkenv <name> , <value>', spaces round the comma.  It returns 0 whether the value matches or not, so `getenv -p <name>', which prints the value, is the one to use for a reliable branch<br>**How:** `checkenv <name> , <value>' with spaces round the comma. Meant to return an error when they differ; it returns 0 either way. |
| `exist` | &#9733; test file existence |
| `getenv` | &#9733; print or test an environment variable.  German prompts: `getenv -p TERM' prints the value with a newline, -l without one, -x exits with it, -n inverts the test.  Bare, or with a name and no option, it prints its own usage.  DESIGNA VLT, version UTIL 2.40<br>`USAGE: getenv [-n\|-p\|-l\|-x] <Environment> [<Wert>]` |
| `hist` | a command-line editor with history, in front of the shell  [no military use -- EFFO-INFO]<br>**How:** A command-line editor with history in front of the shell. On this console it prints a row of asterisks and returns at once. |
| `if` | conditional execution for a shell script: `if def <var>', `if loaded <module>' or `if varval <var> <value>', the commands, `else', `endif'.  It hands the branch to Microware's `shell' to run<br>**How:** Ask for it by path, /dd/CMDS/if -- bash has an if of its own. It hands the chosen branch to Microware's `shell' to run. |
| `printenv` | &#9733; print the environment<br>`Syntax:   printenv [<options>] [{<env var name}]` |
| `printf` | formatted print from the shell, as on Unix: widths, numbers and floating point<br>**How:** printf as on Unix: `printf "%-8s\|%5d\n" name 12'. Widths, numbers and floating point all work. |
| `qp` | &#9733; expand BACK-QUOTES in a command line, which Microware's shell does not do for itself: `qp <cmd> <args>'.  It forks a `shell' to do the expansion, so it wants Microware's on your execution path<br>**How:** Runs its expanded command through Microware's `shell'. |
| `run` | runs a program with its input and output on the terminal PORT names: `run '<program> <args>''<br>**How:** `run '<program> <args>'' with PORT naming a terminal: the program runs with its input and output on that terminal. |
| `submit` | &#9733; submit a job to the print spooler<br>`Syntax: submit [<opts>] [<submit file>] [{<parameter>)]` |
| `xc` | runs the commands marked in a file -- a line beginning `% ' -- and leaves the rest as notes.  Forks them through Microware's `shell' to run<br>**How:** `xc <file>': lines beginning `% ' are commands, the rest is notes. It forks them through Microware's `shell' to run. |

**Shell utilities**

| | |
|---|---|
| `env` | &#9733; Print or set the environment for a command (GNU)<br>`Usage: env [OPTION]... [-] [NAME=VALUE]... [COMMAND [ARG]...]` |
| `expr` | &#9733; Evaluate an expression (GNU) |
| `logname` | &#9733; Print your login name (GNU)<br>`Usage: logname [OPTION]...` |
| `su` | &#9733; Become another user (GNU) -- and it is the GNU one, so it answers `illegal option' and points at `su --help' for the `-?' every other program here takes<br>`Usage: su [OPTION]... [-] [USER [ARG]...]` |
| `whoami` | &#9733; Print who you are logged in as (GNU)<br>`Usage: whoami [OPTION]...` |

**Shells**

| | |
|---|---|
| `bash` | GNU Bourne-Again Shell 1.12 -- this disk's shell; reads .bashrc. It CANNOT serve as $SHELL for a program that shells out: it reads system()'s command line as a script filename.  `ksh' is the one that can, and SYS/login sets SHELL to it. DOC/README-SHELLS compares all five<br>`usage: fc [-e ename] [-nlr] [first] [last] or fc -s [pat=rep] [command]` |
| `gshell` | GSHELL V1.1 (Uwe Simon, 1988) -- a full-screen MENU, not a command shell: a lettered list of the directory, `+' and `-' to page, `.' to change directory, a letter to run a file. `assembler', `compiler' and `editor' are the same engine pointed at one job each.  DOC/README-SHELLS<br>**How:** A full-screen menu of the current directory: + and - page, . changes directory, a letter runs that file. Control-C leaves it. |
| `ksh` | &#9733; Korn shell.  `ksh -c '<commands>'` works completely.  Its INTERACTIVE loop depends on the EMULATOR: it reads the command line with read(fd,buf,256), and needs the emulator's I$Read to return at the end-of-record character rather than only when the full count arrives, or no typed command reaches it.  Given that, ksh is a full shell -- prompt, for loops, variables, forking.  DOC/README-KSH<br>`Syntax: 'setpr <prior>' or 'setpr <pid> [<pid>..] <prior>'` |
| `mshell` | &#9733; a menu shell: `mshell <menufile>' shows one numbered entry per `label,command' line and a number runs that command -- through Microware's `shell'<br>**How:** `mshell <menufile>': one `label,command' per line. A number picks an entry; it hands the command to Microware's `shell' to run. Control-C leaves it. |
| `sh` | Bourne shell v7.5 -- what the startup script runs.  It has a REAL `chd' where bash does not, and it cannot fork a program by absolute pathname here, which is the trade. DOC/README-SHELLS |

</details>

## Editors

*vi and emacs in several flavours, line and stream editors, and editors for binary and hex.*

<details><summary>27 programs</summary>

**Alternates**

| | |
|---|---|
| `sed_1.06` | &#9733; another build of sed -- it is the build that ships as `sed'; the earlier one did nothing but exhaust memory.<br>`Syntax   : sed [<opts>] [<file>]` |

**Binary & hex**

| | |
|---|---|
| `beav` | BEAV 1.40 -- Binary Editor And Viewer (needs TERM)<br>**How:** Full-screen binary editor: `beav <file>'. Control-C leaves it. |
| `hexed` | a hex editor made of your text editor: it writes the file out as a hex dump, opens that in the editor `-e=' names (default vi), and writes the file back when you leave. `-t=<dir>' says where the dump goes; without it, /r0 [no military use -- EFFO-INFO]<br>**How:** `hexed -t=<dir> -e=<editor> <file>': the file goes out as a hex dump into <dir>, the editor opens it, and leaving the editor writes the file back. Without -t it uses /r0. |
| `hexedit` | HEXPERT V2.4 by Dominic Alston -- `hexedit <file>'.  It reads TERMCAP as the capability string itself, not as the name of a file, so source `. /dd/SYS/termcap.entry' first and it draws its viewer; without that it prints the terminal type and exits.  gnuchess wants the same.  Its -d option is separately broken -- `file not accessible' (214) for a file that is readable.  `beav' is the binary editor that needs nothing, and `hexed' the one that would work if there were a RAM disk.<br>**How:** `hexedit <file>'. Put the termcap entry in TERMCAP first (`. /dd/SYS/termcap.entry') or it will not draw. |
| `pbyte` | &#9733; patch bytes in a file at a hex offset<br>`Syntax: pbyte <path> <hex_offset> <hex_byte> [<hex_byte>]` |

**emacs family**

| | |
|---|---|
| `em` | MicroEMACS 3.8b, a screen editor with Emacs keys<br>**How:** A screen editor. It stops with "Environment variable TERM not defined!" unless TERM is set -- SYS/login sets it, so run it from a login shell rather than bare. |
| `emacs` | &#9733; MicroEmacs 4.00<br>**How:** Full-screen editor, MicroEMACS keys. Control-X control-C quits. Its macros and help are in USR/LIB/EMACS. |
| `emacs.mm1` | &#9733; MicroEMACS 4.00 built for the MM/1 -- the same editor as `emacs'<br>**How:** The MM/1 build of `emacs'; the same keys, control-X control-C quits. |
| `me` | MicroEmacs 3.11 -- ADDED; needs TERM.  (memacs400 `emacs` needs cio)<br>**How:** Full-screen editor, MicroEMACS keys, German messages. Control-X control-C quits. |
| `mg` | &#9733; MicroGnuEmacs<br>**How:** Full-screen editor, Emacs keys. Control-X control-C quits. |
| `umacs` | &#9733; uMacs 1.0, MicroEMACS in 45K -- the same keys, no macro language<br>**How:** A small Emacs (uMacs 1.0). Full-screen: it takes the display and shows "== uMacs 1.0 == main ==" at the foot. It needs only TERM set. |

**Line & stream**

| | |
|---|---|
| `ed` | &#9733; GNU ed 0.2, the line editor.  It keeps its scratch file on /r0, a RAM disk, so mount one (`mount -r=256k /r0'); DOC/README-RUNNING has the details<br>**How:** Needs a /r0 RAM disk for its scratch file; `mount -r=256k /r0' provides one. Then `ed <file>', with ed's usual commands: 1,4p prints, s/a/b/ substitutes, w writes, q quits. |
| `editor` | a full-screen file picker that hands the file you choose to `umacs': a lettered list of the directory, `+' and `-' to page, `.' to change directory.  Run it bare; given a path on the command line it stops on an illegal instruction. `gshell' and `assembler' are the same menu in front of other programs.<br>**How:** Run it bare: a full-screen file picker for umacs. Given a file on the command line it stops on an illegal instruction. Control-C leaves the menu. |
| `sed` | &#9733; sed - stream editor: substitutes, deletes and prints with -n.  See DOC/README-CIO.<br>`Syntax   : sed [<opts>] [<file>]` |

**SEDT family**

| | |
|---|---|
| `btree` | &#9733; B-tree file handling demonstration and test |
| `new_e` | SEDT editor, generic terminal -- it picks vt100 or vt220 by TERM.  Needs the same three SYS/sedt.* files as `e' |
| `sedt` | &#9733; SEDT 2.6 screen editor, the VT100 build: a DEC-style keypad editor.  `new_e' and `e' are two more builds of it; all three read SYS/sedt.keys, sedt.ruler0 and sedt.help |

**vi clones**

| | |
|---|---|
| `elvis` | Elvis 1.7 -- the best-documented of this disk's three vi editors, and the one with the most options.  Built from the source in CMDS/archives.  Needs TERM and TERMCAP; runs with no program under its other personalities and need elvis present to run. IT ALSO NEEDS A /dd/tmp, and the path is compiled in: on a /dd without that directory it stops before drawing anything with `Can't create temp file... Does directory "/dd/tmp" exist?'.  This disk ships one, so it bites on the machine you copy elvis TO.  Either `makdir /dd/tmp' or, before starting it, `setenv EXINIT "set directory=<a dir you have>"' -- elvis reads EXINIT before creating the temp file.  `vi' has the same compiled-in /dd/tmp; the PVIC builds do not.  DOC/README-VI has the table<br>**How:** A full vi/ex clone. Needs TERM and TERMCAP set -- `SYS/login' does both. `view' opens read-only, REBUILT/vi.elvis is the same program as vi, and all of them exec CMDS/elvis, so it must be present. |
| `elvis_input` | elvis under its `input' personality -- it opens already in insert mode.  The name is load-bearing: elvis's wrapper picks its personality from the LAST LETTER of the name it was invoked by, so a name ending in another letter falls through to plain vi.  CMDS/input is a different program entirely |
| `elvprsv` | Preserve an elvis session across a crash |
| `elvrec` | recover an elvis buffer preserved when elvis died.  Run with NO ARGUMENTS it lists what is recoverable -- so its silence here means there is nothing, which is true.  It reads `/usr/preserve/Index', and OS-9 cannot have a /usr at all: a leading /name is a DEVICE, not a directory.  So on this machine it can never find anything, whatever is placed under /dd.  `expreserve' is the half that saves. DOC/elvrec/elvrec.doc.<br>**How:** Bare, it lists what elvis preserved; nothing listed means nothing was preserved. |
| `vi.elvis` | elvis 1.7 as vi.  CMDS/vi is the EFFO build and CMDS/vi_nocio is PVic -- three unrelated vi clones |
| `view` | elvis opened read-only |

**vi family**

| | |
|---|---|
| `vi` | &#9733; the real vi/ex, and it keeps the name -- its source in SRC/effo_vi is the Berkeley ex source itself, not a clone. `vi -x' is ex, `vi -d' is edit.  See DOC/README-VI.<br>**How:** One of three unrelated vi editors here, and the only one that is the genuine Berkeley ex/vi rather than a clone -- its source in SRC/effo_vi is the real ex_*.c files. `vi -x' becomes ex, `vi -d' becomes edit. DOC/README-VI compares all three. |
| `vi_1.0` | PVIC 1.0, public domain      -> /dd/CMDS/REBUILT (name was taken) and CMDS/vi_nocio are PVIC 1.0a<br>`Usage: vi [file ...]` |
| `vi_cio` | &#9733; PVic vi, cio build (use vi_nocio instead)<br>**How:** PVIC 1.0a built with cio. Put the termcap entry in TERMCAP first (`. /dd/SYS/termcap.entry'), then `vi_cio <file>'. CMDS/vi_nocio is the same editor needing no module. |
| `vi_nocio` | PVIC 1.0a -- the smallest of this disk's three vi editors, public domain.  See DOC/README-VI to choose between them<br>**How:** PVIC 1.0a, the smallest of the three vi editors on this disk, public domain, no source or docs here. DOC/README-VI compares it with vi and elvis. |

</details>

## Text tools

*Search, sort, compare, reformat, split and spell-check.*

<details><summary>114 programs</summary>

**Alternates**

| | |
|---|---|
| `diff_1.1` | another build of GNU diff 1.1<br>`Syntax   : diff [<options>] file1 file2` |

**Banners & text art**

| | |
|---|---|
| `banner` | &#9733; print large banner text |
| `cursive` | generate a horizontal cursive banner<br>`usage: cursive [-tn] [-in] message` |
| `gothic` | &#9733; print text as a gothic/blackletter banner |
| `zot` | &#9733; prints a line of text in one of fourteen decorative styles: `zot -s=3 "text"'; -d shows them all<br>**How:** `zot -s=<1-14> "text"' prints the text in that style; `zot -d "text"' shows every style in turn. |

**Count & inspect**

| | |
|---|---|
| `ascii` | &#9733; ASCII character table |
| `charcnt` | &#9733; Count characters in a file (Carl Kreider) |
| `dump` | hex dump of a file or module<br>**How:** This is the hex dump on this disk. There is no `od'. |
| `file` | Identify file types.  SYS/magic is now here, so it names real formats -- "GIF picture ver. 87a 320 x 200, interlaced, 256 colors" -- and not just OS-9 modules<br>**How:** Names real formats now that SYS/magic is here: `file /dd/DEMO/gulls.gif' reports the GIF version, size and colour count. |
| `strings` | &#9733; extract printable strings, reported as $offset: <text><br>`Usage: strings [-anpl=n] [file [file]]` |
| `sum` | Checksum and block count (GNU) |
| `tail` | &#9733; last lines of a file -- DESIGNA's, and it takes `-l=<n>', not GNU's `-n <n>', which it rejects as an unknown option.  `head' on this disk IS the GNU one and takes -n: two conventions, one disk |
| `wc` | count lines, words and characters for each file named, and print a total; it counts CR-terminated lines as well as LF. |
| `wc.cio` | &#9733; archived build of wc.  It counts on standard input -- `1 lines, 6 words, 40 chars' where `wc' says `1 6 40' -- so `wc' is the build for a file argument. |

**DVI drivers**

| | |
|---|---|
| `dvialw` | DVI to Apple LaserWriter<br>**How:** Works, and so do the other nine dvi* drivers. The disk ships the MetaFont sources, not the ready-made bitmaps, so each driver says "Font file [cmr10 [300 dpi]] could not be opened ... Proceeding with zero size characters" once per font and writes a page with the right layout and no glyphs. FONTS/PK300 and PK144 hold a Makefile each; generate the bitmaps from the MetaFont sources in SYS/TEX/MFINPUTS. Output goes to <dvifile>_alw beside the input, not to standard output. |
| `dvidjp` | DVI to HP DeskJet Plus<br>`Usage: dvidjp [opts] dvifiles` |
| `dvieps` | DVI to Epson<br>`Usage: dvieps [opts] dvifiles` |
| `dviimp` | DVI to Imagen<br>`Usage: dviimp [opts] dvifiles` |
| `dvijep` | DVI to HP LaserJet Plus<br>`Usage: dvijep [opts] dvifiles` |
| `dvijet` | DVI to HP LaserJet<br>`Usage: dvijet [opts] dvifiles` |
| `dvilj2` | DVI to HP LaserJet II<br>`Usage: dvilj2 [opts] dvifiles` |
| `dvimac` | DVI to Macintosh<br>`Usage: dvimac [opts] dvifiles` |
| `dvioki` | DVI to Okidata<br>`Usage: dvioki [opts] dvifiles` |
| `dvitos` | DVI to Toshiba<br>`Usage: dvitos [opts] dvifiles` |

**Format & typeset**

| | |
|---|---|
| `fmt` | Simple text formatter (elvis 1.7)<br>`usage: fmt [-width] [files]...` |
| `hc` | shift text to a column, or label every line.  `hc +8 f' indents f so the text starts at column 8; `hc -11 f' strips leading columns so it starts at column 11; `hc -l "> " f' puts that string in front of every line.  With no option it copies the file through.  It evaluates nothing -- for arithmetic see `bc' and `dc' |
| `lout` | Lout 2.05 document formatter (Basser Lout, Jeffrey Kingston)<br>`usage: -o<filename>` |
| `nroff` | nroff text formatter.  Built `-qm' from SRC/nroff, it formats: given a man page it sets the text and names the macros it does not know (`unrecognized command .TH'), which is a plain nroff without the man package rather than a fault. DOC/README-CIO<br>**How:** Formats a text with nroff requests: `nroff file.ms'. Its macro sets are in LIB (tmac.*). Point TMACDIR at LIB if a macro package is not found. |
| `proff` | proff - portable roff text formatter (macros in LIB/proff). Given a text file it justifies it to a measure, and takes page ranges and a statistics option.  `roff' works too; `nroff' wants a real macro package and answers `illegal switch' to -?<br>`usage: proff [+n] [-n] [-v] [-ifile] [-s] [-pon] [infile [outfile]]` |
| `roff` | roff text formatter, and it works: `roff -?' gives its syntax and page-range options.<br>`Syntax: roff {[+00] [-00] [-s] -[h] file}` |
| `tformat` | text formatter (SNOBOL4-in-C)<br>`Usage: tformat [width\|-?] [<infile] [>outfile]` |

**Fortune & sayings**

| | |
|---|---|
| `cookhash` | build the hash file cookie(1) needs, from a sayings file<br>`usage: cookhash <cookiefile >hashfile` |
| `cookie` | print a random fortune cookie<br>**How:** Bare it prints a fortune from a default file. Given arguments it wants BOTH the cookie file and the hash `strfile' built for it: `strfile mine' then `cookie mine mine.dat'. |
| `fortune` | print a random quotation<br>`usage:  fortune [ - ] [ -wsloa ] [ file ]` |
| `sonnet` | writes (bad) sonnets in iambic pentameter, curses-based<br>**How:** Full-screen: it takes over the display. **ESC quits**. (control-C also gets you out, but ESC is the program's own way.) |
| `strfile` | &#9733; build fortune's index file<br>`usage:  strfile [ - ] [ -cC ] [ -sv ] inputfile [ datafile ]` |
| `unstr` | reverse strfile - dump a fortune index.  It takes the index BASE name, appending `.dat' itself, so `unstr /dd/GAMES/FORTUNE/fortunes' is the invocation and bare it prints its own usage.  DOC/README-CIO<br>`usage: unstr datafile[.dat] [ outfile ]` |

**KWIC index**

| | |
|---|---|
| `pagefraz` | KWIC suite - phrase extractor<br>`Syntax: pagefraz <opts> [<in_path> [<out_path>]] <opts>` |
| `pagekwic` | KWIC suite - split a Stylo file to one phrase per line with page no.<br>`Syntax: pagekwic <opts> [<in_path> [<out_path>]] <opts>` |
| `pageline` | KWIC suite - line/page numbering<br>`Syntax: pageline <opts> [<in_path> [<out_path>]] <opts>` |

**Search & match**

| | |
|---|---|
| `bm` | &#9733; bm - fast grep utility (Boyer-Moore) |
| `bmgtest` | &#9733; Boyer-Moore-Gosper substring search demo<br>**How:** bmgtest [-i] [-n] <pattern> [file ...]. A demonstration of Boyer-Moore-Gosper searching. |
| `bmgtest2` | &#9733; Boyer-Moore-Gosper substring search demo (variant)<br>`usage: bmgtest [-i] [-n] pattern [file ...]` |
| `fgrep` | &#9733; very fast grep utility<br>`usage: fgrep [-[[AB] ]<num>] [-[CVchilnsvwx]] [-[ef]] <expr> [<files...>]` |
| `grep` | GNU grep 2.0 -- pattern search<br>`usage: grep [-[[AB] ]<num>] [-[CEFGVchilnqsvwx]] [-[ef]] <expr> [<files...>]` |
| `soundex` | Soundex phonetic key for each word on stdin |

**Sort, compare & merge**

| | |
|---|---|
| `cdiff` | context diff.  Built `-qm' from SRC/v_misc/cdiff.c, it produces a real context diff: `>>>> INSERT BEFORE 2'. DOC/README-CIO |
| `diff` | &#9733; GNU diff 1.1 -- handles CR text files.<br>`Usage: diff [-options] file1 file2` |
| `ediff` | put `diff' output into plain English: `diff <f1> <f2> ! ediff', or `ediff <file' for a diff you already have.  A one-line change comes out as `-------- 1 line changed at 3 from: ... to: ...'.  `diff' does the comparing; this makes the answer readable<br>`Syntax   : 'ediff <file'  or  'diff <f1> <f2> ! ediff'` |
| `fcomp` | &#9733; compare two text files<br>`Syntax: fcomp <file_1> <file_2>` |
| `join` | GNU join -- relational join of two sorted files<br>`Usage: join [-a 1\|2] [-v 1\|2] [-e empty-string] [-o field-list...] [-t char]` |
| `nsort` | sort lines from standard input -- LEXICALLY, despite the name: given 3, 22, 111 and 4 it answers 111, 22, 3, 4, the same order GNU `sort' gives with no options.  For a numeric sort use `sort -n', which gets it right<br>`Usage: nsort <unordered >sorted` |
| `qsort9` | &#9733; sort filter<br>`Syntax: qsort9 [<opts>] [<srcpath>] [<opts>]` |
| `sort` | GNU sort<br>`Usage: sort [-cmus] [-t separator] [-o output-file] [-bdfiMnr] [+POS1 [-POS2]]` |
| `spiff` | &#9733; tolerant diff - ignores formatting noise<br>**How:** Compares two files while ignoring differences that do not matter (whitespace, number formatting). Takes TWO filenames. |
| `tcmp` | &#9733; Compare two text files (Carl Kreider)<br>**How:** Compares two text files and prints each differing line, both versions one under the other with the line number in each file. Files whose lines differ only in tabs and spaces are reported as changed, which reads oddly until you dump them. |
| `unip` | unique lines with page numbers<br>`Syntax: unip [<opts>] [<srcpath>] [<opts>]` |
| `uniq` | &#9733; drop duplicate lines<br>`Usage: UNIQ [-u][-d][-c] [-n] [^n] input [>output]` |

**Spelling & words**

| | |
|---|---|
| `buildhash` | build ispell's dictionary hash.  It reads a word list called `dict.191' (the name is compiled in). /dd/LIB/ispell.hash is the built hash, 490,186 bytes, and it ships, so ispell itself reads that and works.  `chardef' reads the same word list. |
| `ispell` | interactive spelling checker<br>**How:** Interactive spelling checker. Takes a file: `ispell <file>'. `ispell -a' is the pipe interface programs use. |
| `jargon` | Jargon-file browser (needs its database files)<br>**How:** A browser for the Jargon File, which is here: VH/jargon.txt, version 3.0.0 of 27 July 1993, with its index. It will not read SYS/termcap -- do `. /dd/SYS/termcap.entry' first, then `jargon -m'. |
| `makelex` | &#9733; compiles sonnet's lex.data word list into a C array |
| `speech` | English-to-phoneme translation<br>`Usage: PHONEME [infile [outfile]]` |

**Split & join**

| | |
|---|---|
| `sepwords` | split a file to one word per line<br>`Syntax: sepwords [<in_path> [<out_path>]]` |
| `split` | Split a file into pieces (GNU)<br>`Usage: split [-lines] [-l lines] [-b bytes[km]] [-C bytes[km]] [+lines=lines]` |
| `splitalf` | &#9733; split a file into <name>_A to <name>_Z by the first letter of each line, and <name>_0 for the rest.  It opens <name>_0, then tests a file slot it has not opened yet and stops with `can't open output file(s)'.<br>**How:** It makes <name>_0 and then stops with `can't open output file(s)', whatever it is given -- it tests a file slot it has not opened yet. No argument gets round it. |

**TeX**

| | |
|---|---|
| `afm2tfm` | Adobe font metrics to TeX font metrics<br>`Usage: afm2tfm foo[.afm] [-O] [-v\|-V bar[.vpl]]` |
| `bibtex` | BibTeX -- bibliography formatter, and it WORKS.  It reads the job name from STANDARD INPUT (`Please type input file name (no extension)--' is a prompt, not silence), and the .bst styles are in SYS/TEX/INPUTS -- plain, unsrt, abbrv and alpha -- not in SYS/TEX/BIB, which holds a read.me<br>**How:** It reads the job name from STANDARD INPUT -- `Please type input file name (no extension)--' is a prompt, not silence. The .bst styles are in SYS/TEX/INPUTS (plain, unsrt, abbrv, alpha), not SYS/TEX/BIB, which holds one read.me. A BACKSLASH CANNOT BE TYPED at this shell -- bash's echo eats `\c' -- so patch one in with `pbyte <file> <hex offset> 5c'. |
| `dvips` | DVI to PostScript -- pair it with gs33<br>**How:** DVI to PostScript. It wants a header file tex.pro -- point it at one, or use `dvialw', which writes PostScript too. |
| `dvitype` | show what is inside a .dvi file, as text<br>**How:** `dvitype <file>.dvi < /nil'. It asks five questions -- output level, starting page, page count, device resolution, magnification -- and takes the default for each at end of file. Redirect its input so a script does not wait on the questions. |
| `gftopk` | MetaFont generic font to packed font<br>**How:** `gftopk cmr10.120gf /dd/tmp/cmr10.120pk'. GFFONTS must name where the input is; the OUTPUT path is never searched for, so an absolute one works with nothing set. |
| `gftype` | show what is inside a .gf file<br>**How:** `gftype -i <font>.<dpi>gf' draws the glyphs as asterisks; -m adds the opcodes. GFFONTS must NAME THE DIRECTORY -- the compiled-in FONTS paths do not begin with `.', so a file beside you is invisible. |
| `inimf` | MetaFont with no base preloaded<br>**How:** It builds a Metafont base, which SYS/TEX/MFBASES now ships. To rebuild: `echo "plain; \input modes; dump" > mf.in' then `ksh -c "cd /dd/tmp; inimf < mf.in"'. About a minute. DOC/README-METAFONT has the rest. |
| `initex` | TeX with no format preloaded, for building .fmt files<br>**How:** TeX with no format preloaded -- this is what BUILDS the .fmt files. `initex "plain \dump"'. The three formats already ship in SYS/TEX/FORMATS, built this way, so you only need this to make your own. |
| `latex` | LaTeX -- Lamport's document preparation system on top of TeX<br>**How:** See `tex'. The wrapper cannot reach the engine; run `virtex '&lplain' yourfile.tex'. That does work: SAMPLES/small.tex gives "Output written on small.dvi (1 page, 1704 bytes)". The .dvi and .log land in your DATA directory. |
| `maketexpk` | generate a .pk font at the size TeX asked for<br>**How:** It carries the RIGHT Metafont line in its own strings and then reaches for `makdir', `del' and `attr' to file the result -- three Microware utilities that are not here. Run the virmf line yourself: DOC/README-METAFONT has it, and `gftopk' is all maketexpk was going to do afterwards. |
| `pktogf` | packed font back to generic font<br>**How:** Unpacks a .pk. The result is longer than the .gf it came from -- pktogf rewrites the preamble comment -- and the bitmap is unchanged. |
| `pktype` | show what is inside a .pk file<br>**How:** `pktype <font>.<dpi>pk' prints the packed font back, glyphs included. PKFONTS must name the directory. |
| `pltotf` | property list to TeX font metric<br>`Usage: pltotf [-verbose] <property list file> <tfm file>.` |
| `slitex` | SliTeX -- LaTeX for slides<br>**How:** LaTeX for slides; its format is SYS/TEX/FORMATS/splain.fmt, already built. |
| `tangle` | WEB to Pascal -- Knuth's literate programming tool.  IT NEEDS A CHANGE FILE NAMED, always: given only a .web it answers `Error: `Can't open file.'' -- the absent CHANGE file is what it could not open.  DOC/tex ships `sample.web' and `none.ch' (an empty change file): copy both to your data directory and run `tangle sample none'.  It reads and writes there, not where you typed from.<br>**How:** Needs a CHANGE FILE named, always. `tangle yourfile.web' alone answers `Error: `Can't open file.'' and the file it cannot open is the absent change file, not your source. DOC/tex ships `sample.web' and `none.ch' (empty, changes nothing): copy both to your data directory and run `tangle sample none'. It reads and writes in the DATA directory, which bash's `cd' does not move. `weave sample none' is the other half. |
| `tex` | TeX itself -- the typesetting program (a driver; virtex does the work)<br>**How:** Run the engine, not the wrapper. `tex' is one line: it asks a shell to run `virtex "&plain" yourfile', the quoted format name is never unquoted, and the shell answers E$PNNF for the whole line (rc 221 with no $SHELL set, and silently). Type `virtex '&plain' yourfile.tex' instead. For LaTeX it is `virtex '&lplain' yourfile.tex', for SliTeX `virtex '&splain''. SYS/TEX/SAMPLES/small.tex is a LaTeX document and story.tex is plain TeX with no \end. |
| `texidx` | build an index from TeX's .idx output |
| `tftopl` | TeX font metric to property list (the readable form)<br>`Usage: tftopl [-verbose] <tfm file> [<property list file>].` |
| `vftovp` | virtual font to virtual property list<br>**How:** `vftovp s.vf s.tfm back.vpl' reads the binary pair back to text. VFFONTS and TEXFONTS must name where the .vf and .tfm are. |
| `virmf` | the real MetaFont engine -- generates fonts from .mf sources<br>**How:** Metafont. `virmf '&cmbase' '\scrollmode; \mode:=epsonlo; \input cmr10; \end'' renders all 128 characters of cmr10. THE JOB NAME COMES FROM THE COMMAND LINE: the same line fed on standard input renders the same font and calls it `mfput'. |
| `virtex` | the real TeX engine, loaded with a format<br>**How:** The real TeX engine, and the one to use -- see `tex'. It wants the format first: `virtex '&plain' file.tex' or `virtex '&lplain' file.tex'. The formats that ship are plain, lplain and splain, in SYS/TEX/FORMATS. |
| `vptovf` | virtual property list to virtual font<br>**How:** `vptovf /dd/DOC/tex/sample.vpl s.vf s.tfm'. sample.vpl is a one-character virtual font written for this, mapping `A' onto cmr10's. |
| `weave` | WEB to TeX -- the other half of literate programming, and it needs a change file for the same reason `tangle' does: `weave sample none'<br>**How:** The other half of `tangle', and it NEEDS A CHANGE FILE NAMED just as tangle does: `weave sample none', never `weave sample.web'. Given only a .web it answers `Error: `Can't open file.'' and the file it cannot open is the absent change file. DOC/tex ships sample.web and none.ch. |

**Transform & filter**

| | |
|---|---|
| `ape` | writes GIBBERISH in the style of whatever it is given -- a travesty generator. `travesty' and `newsgen' are the others of its kind here. Its options are `-b' (how much source to read) and `-l' (how many characters must match before it follows the source).<br>**How:** A travesty generator: `-b' is how much source to read and `-l' the pattern length. Feed it VARIED text -- one word repeated makes it generate without end, because every position matches every other. |
| `autolf` | &#9733; Mike Tozer's line-ending converter, 1995, and THE ONE THAT WORKS: it turns CR into CRLF or LF and back, expands tabs, and handles ^Z. Use it as a FILTER -- `autolf -c -C -L < in > out' makes DOS text out of OS-9 text. Given a FILENAME it converts in place through a temporary and then cannot rename it back -- this C library has no rename(), the same wall zip and arc hit. `-H' explains the conversions. It is what `todos' and `toos9' were supposed to be.<br>`Usage:   autolf [<opts>] {<file names> [<opts>]}` |
| `casefix` | normalise letter case -- A FILTER, and it reads STANDARD INPUT.  Given a file as an argument it says nothing at all; `casefix < file' sentence-cases it<br>**How:** It is a FILTER and reads STANDARD INPUT: `casefix < file' sentence-cases it. |
| `cut` | cut selected fields from each line |
| `detab` | &#9733; tabs to spaces<br>`Usage: detab [-tn] [infile] or [<infile]` |
| `eo` | &#9733; EXECUTE A COMMAND ON EVERY LINE OF A FILE -- an xargs. `eo <file> <command> @' runs <command> once per line with `@' replaced by the line; -p takes the lines from a pipe, -q runs quietly, -e stops on the first error. Marc Balmer, version 1.8. It shells out, so it needs SHELL set, which SYS/login does.<br>**How:** Runs a command on every line of a file, with `@' standing for the line: `eo <file> <command> @'. It shells out, so it needs SHELL set to a shell that takes a command line as one argument -- SYS/login sets `SHELL=/dd/CMDS/ksh' and that is what makes it work. Without it, `can't execute /dd/bash'. `-p' takes the lines from a pipe instead of a file. |
| `expand` | Turn tabs into spaces (GNU)<br>`Usage: expand [-tab1[,tab2[,...]]] [-t tab1[,tab2[,...]]] [-i]` |
| `field` | &#9733; select whitespace-separated fields from standard input by number, in the order asked for and tab-separated on output: `field 2 4 1' prints the second, fourth and first word of each line. `-i=c' names another input separator.<br>`Syntax  : field [<opts>] <fields...> [<opts>]` |
| `fillup` | &#9733; fill a file up to a given length with a constant byte: `fillup -n=64 -i=65 f' pads f to 64 bytes with `A' and says `24 bytes (value=65) appended'.  The length option is -n=, not -l=.  L. Zeller, 1992<br>`Syntax:   fillup [<options>] <file>` |
| `gawk` | &#9733; GNU awk 2.11 -- the pattern-and-action language.  It works, but it IGNORES A FILENAME ARGUMENT and reads standard input whatever it is given, so redirect: gawk '{...}' < file, never gawk '{...}' file.  Named a file, it sits waiting on the terminal.<br>**How:** GNU awk 2.11. IT IGNORES A FILENAME ARGUMENT and reads standard input whatever it is given, so redirect: `gawk "{print \$1}" < file', never `gawk "{print \$1}" file' -- named a file it sits waiting on the terminal. Keep the program text short: a command line wider than the window scrolls under bash and is hard to read back. Needs Microware's cio. |
| `gdd` | &#9733; GNU dd -- a block copier and converter. `gdd if=<file> bs=<n> skip= seek= count=', and `conv=ucase' converts to upper case on the way through. `of=' can only name a file that already exists, so send the output through `>' instead. Give it arguments; `dump' is the hex dump here.<br>**How:** GNU dd -- a block copier and converter. `gdd if=<file> bs=8 count=1' copies eight bytes, `conv=ucase' converts on the way through. `of=' can only name a file that already exists, so send the output through `>'. Give it arguments. It uses Microware's cio; `dump' is the hex dump here. |
| `gep` | &#9733; global expression parser -- grep-like; its `-e' takes the PATH OF A FILE holding the expressions: `gep -e=/dd/tmp/patterns <file>'. A file of patterns applied at once is what it is for and nothing else here does it. See DOC/README-GREP<br>**How:** Its expressions come from a FILE named with `-e', which its own option list marks `(required)': `gep -e=<patterns> <source>'. Handing it a pattern and a file the way you would grep earns `more than one path specified'. |
| `head` | First lines of a file -- `head -n 20 file'.  These GNU builds want -n 20, not -20<br>**How:** First lines of a file. This GNU build wants `head -n 20 file' -- the older `head -20' form is rejected as an unrecognized option. Needs cio. |
| `l` | &#9733; list a TEXT FILE with word wrap and a carriage return at the end of every line -- `l -<width> <file>', 79 columns by default.  Written for Stylo documents and other long-line files.  It takes files, not directories<br>`Usage: l [-options] [file] [file] [-options]` |
| `paste` | merge lines of files<br>**How:** Joins lines side by side, tab-separated by default: `paste f1 f2'. `-d:' picks another separator; `-s' puts one file's lines on a single line. |
| `pep` | file 'detergent' - strip junk from files<br>`Usage: pep [options] [filename ...]` |
| `psc` | &#9733; turn an ASCII table into commands for `sc', the spreadsheet: `psc -d' ' < table' answers `let A0 = 1', `let B0 = 2' and a `format' line per column.  -d sets the field delimiter, -r assembles rows first, -s names the top-left cell.  Robert Bond's, and it works<br>**How:** Feeds `sc', the spreadsheet: `psc -d' ' < table' turns rows of numbers into `let A0 = 1' commands sc can read. -r assembles rows first, -s names the top-left cell, -d sets the delimiter. |
| `rot` | turn a text file on its side -- line one becomes column one |
| `subber` | &#9733; Substitute text in a stream: a word list of `,old,new' pairs (the first character is the delimiter) and a file or standard input (Carl Kreider).  It grows its data area as it reads, so give it room -- at your OS-9 shell, `subber #1000k words file'<br>**How:** Substitutes words in a stream from a word list of `,old,new' pairs (the line's first character is the delimiter), reading a file as the second argument or standard input. It grows its data area as it reads, with F$Mem, so give it room up front: at an OS-9 (Microware) shell, `subber #1000k words file' -- bash and ksh read the `#' as a comment, so run it at your OS-9 shell or through it, `/h1/CMDS/shell "subber #1000k words file"'. Tested: `,fox,cat' turns `a fox' into `a cat'. |
| `tabs` | re-space a file, standard input to standard output: `-i8' says the input's tab stops are every 8 columns, `-o0' asks for spaces on output and `-o4' for tabs every 4.<br>`Syntax   : tabs [<opts>] [<input_redirection>] [<output_redirection>]` |
| `tac` | Print a file backwards, last line first (GNU)<br>**How:** Prints a file backwards, last line first -- cat's mirror image. Needs cio. |
| `unexpand` | Turn leading spaces back into tabs (GNU)<br>`Usage: unexpand [-tab1[,tab2[,...]]] [-t tab1[,tab2[,...]]] [-a]` |
| `unp` | &#9733; Strip unprintable characters from a stream (Carl Kreider)<br>`Usage:  unp [-?] [file]` |
| `upperdir` | Normalise case: files lowercase, dirs uppercase<br>`Usage: UpperDir [directory name]` |
| `valspeak` | Valley-speak text filter: standard input in, the rewritten text out. `I think this operating system is really good' comes back as `I think this operatin' system is like wow! really bitchin''. |

</details>

## Files & directories

*Listing, copying, finding, renaming, and knowing what you have.*

<details><summary>32 programs</summary>

**Attributes & ownership**

| | |
|---|---|
| `chgrp` | &#9733; change group<br>`Usage:  chgrp [-z] {numerical-gid \| username} [file [... file]]` |
| `chown` | &#9733; change owner<br>`Usage:  chown [-z] {numerical-uid \| username} [file [... file]]` |
| `fstat` | display a file's FILE DESCRIPTOR -- the RBF FD sector, not the attribute bits `attr' shows you.  Its own Function line says "Display file descriptor information" and it reports itself as `FStat'.  `-s' adds the segment list, and `ssl' shows the same list from the same sector<br>`Syntax: FStat [<opts>] <file1> [<opts>]` |
| `owner` | &#9733; CHANGE a file's owner -- `owner <user> <file> ...', super user only.  Run with a file it prints its usage; run as `owner <file>' it reads the filename as a user name and answers `No such user'.  `fstat' and `ls -l' are what SHOW an owner<br>`Usage: owner user file file ...` |

**Copy, move, delete**

| | |
|---|---|
| `cp` | &#9733; copy files -- `cp <from> <to>' copies the bytes across.  Run with no arguments it prints its usage and then stops on a bus error<br>`Usage: cp file1 file2` |
| `dback` | directory backup: walks a directory and issues an OS-9 `copy' for every file that has changed, so what you see is the list of copies it wants<br>`Usage: Dback [-options] <fromdir> <todir> [-options]` |
| `delbak` | &#9733; delete backup files (*_bak) in a directory tree<br>`Usage: delbak [-options] [directory] [-options]` |
| `move` | &#9733; move files between directories WITHOUT COPYING THE CONTENTS -- it relinks them, which is why it is quick and why its own help warns never to kill it mid-run.  `move <from> <to>' wants a destination NAME; -w=<dir> is the wildcard form that takes a directory.  L. Zeller, V2.1<br>`Syntax:   move [<options>] <from> [<to>] [<options>]` |
| `mv` | &#9733; GNU mv (fileutils 3.13) -- rename a file or move it into a directory; `-i' asks before overwriting, `-b' keeps a backup, `-v' names what it moved<br>`Usage: mv [-bfiuv] [-S backup-suffix] [-V {numbered,existing,simple}]` |
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
| `dfiles` | &#9733; find duplicate files under a directory and write out the `cmp' commands that would prove them identical, so the list itself is the answer |
| `du` | &#9733; disk usage, by directory<br>`Syntax: du <directory>` |
| `ff` | &#9733; find files by name -- `ff <name>'.  It builds the command `dir -ausr ! grep <name>' and hands it to Microware's `shell'. `find' does the same job |
| `find` | &#9733; find 1.1.5 -- search a directory tree, with its own syntax: `-n=<name>' matches and `-o' prints what it found. (`find <dir> -name x -print' answers `only one parameter allowed'.)  The manual in DOC/find describes a different find.<br>`Syntax: find {<opts>} [<path>]` |
| `space` | &#9733; effective disk usage  [conditions apply -- run `help space`]<br>`Syntax:   space [<opts>] {<dir/file path>} [<opts>]` |

**Home Librarian**

| | |
|---|---|
| `Ascii2Libr` | Home Librarian: build a catalogue from plain text -- `Ascii2Libr -outfile cat.libr', with the text on standard input, in the form Libr2Ascii writes<br>**How:** `-outfile cat.libr' with a space, and it reads the ASCII on standard input. The text is the form Libr2Ascii writes: a page count, then a card count and the cards, then the title, author and subject index sections. |
| `EditLibr` | Home Librarian: edit a catalogue<br>**How:** Part of the HL10 librarian set. Wants an edit file as a parameter; `EditLibr' alone prints its syntax. |
| `Libr2Ascii` | Home Librarian: dump a catalogue to plain text<br>**How:** `-infile cat.libr' with a space. It writes the catalogue to standard output as text, and a page count and four index-key counts at the end -- all zero means the catalogue is empty. |
| `Librarian` | Home Librarian: search a catalogue.  SIX PROGRAMS AND THEIR DOCS TRAVEL TOGETHER -- its licence requires it<br>**How:** One of six Home Librarian programs that must stay together -- its licence says so. Start here to search a catalogue; EditLibr edits one, Ascii2Libr builds one from text, Libr2Ascii dumps it back, PrintCards and PrintLabels print it. Manual in DOC/homelibr. |
| `PrintCards` | Home Librarian: print catalogue cards<br>`Syntax: PrintCards [opts]` |
| `PrintLabels` | Home Librarian: print labels.  ITS OPTIONS TAKE A SEPARATE ARGUMENT -- `-infile cat.libr -templatefile tpl.txt', not `-infile=...', which answers `Bad option:' and prints the syntax.  The same is true of Ascii2Libr, Libr2Ascii, PrintCards and EditLibr.  The template is a text file copied out once per card, with %title, %author, %year and the other field names replaced<br>**How:** Its options take a SEPARATE argument: `-infile cat.libr -templatefile tpl.txt', never `-infile=...', which answers `Bad option:' and prints the syntax. The same is true of Ascii2Libr, Libr2Ascii, PrintCards and EditLibr. The template is a text file copied out once per card with %title, %author, %year and the other field names replaced. |

**List & navigate**

| | |
|---|---|
| `dir` | &#9733; directory listing -- `dir [<opts>] <directory>'; `-e' adds owner, dates, attributes and size<br>`Syntax: dir [<opts>] {<dir names> [<opts>]}` |
| `dm` | &#9733; Disk Master 1.4, a full-screen two-pane disk and directory browser with a file-information panel beside the listing.  It runs the commands on its bottom line through system(), so SHELL must name a shell that can carry them out: with SHELL=/dd/CMDS/sh it runs completely.  Its help file is SYS/dm.hlp<br>**How:** Disk Master 1.4, a full-screen disk browser. It runs the commands on its bottom line through system(), so SHELL must name a shell that can carry them out; with SHELL=/dd/CMDS/sh it runs completely, listing and file-information panel and all. |
| `ls` | GNU ls (fileutils 3.13) -- a real stat(), columns, and `-al'<br>`Usage: ls [OPTION]... [FILE]...` |
| `tree` | print a directory tree, drawn with line graphics -- directories only, sorted, from the directory you name<br>`Syntax: tree [<directory>] [<opts>]` |

**Paths**

| | |
|---|---|
| `basename` | &#9733; strip directory from a pathname (M.C. Gregorie, 1994)<br>`Syntax:   basename <path> [<suffix>]` |
| `dirname` | &#9733; strip filename from a pathname (M.C. Gregorie, 1994)<br>`Syntax:   dirname <path>` |

**Split & join**

| | |
|---|---|
| `divide` | &#9733; SPLIT A FILE into pieces -- Farside Systems 1992, `divide -l=<lines> <infile> [<outfile>]' |
| `fc` | &#9733; split a big file in two, to carry it on 360k disks -- the cut is at exactly 350,000 BYTES: its own Function line says "Takes first 350,000 bytes of a file or stdin and puts in one file and puts remaining bytes" in the other<br>`Syntax:   fc [<file>]` |

</details>

## Developer tools

*Version control, tags, cross-reference, formatters, a debugger and benchmarks.*

<details><summary>46 programs</summary>

**Assembly**

| | |
|---|---|
| `tab` | Tabulate 6809 or 68000 assembly source -- opcode-aware, and works on code that will not assemble<br>`Syntax: tab [<opts>]` |
| `xlate` | &#9733; Translate 6809 assembly source to 68000<br>**How:** Translates 6809 assembly source into 68000. Pairs with as09 (the 6809 assembler on this disk) and with `tab', which tabulates either dialect. Needs cio. |

**Benchmarks**

| | |
|---|---|
| `dhry` | Microware cc<br>**How:** Dhrystone 2.0. Twelve builds of the same source sit in CMDS/DHRY -- run several and compare, which is what tells you the compiler's cost. Run under an emulator the number describes the host machine, not a 68000. |
| `dhryGcc` | &#9733; GCC 1.x |
| `dhryGcc2` | &#9733; GCC 2.x |
| `dhryGcc2in` | &#9733; GCC 2.x, inlined |
| `dhryGcc2mx` | &#9733; GCC 2.x, mixed |
| `dhryGcc2o2` | &#9733; GCC 2.x, optimised |
| `dhryGccin` | &#9733; GCC 1.x, inlined |
| `dhryGccmx` | &#9733; GCC 1.x, mixed |
| `dhryGcco2` | &#9733; GCC 1.x, optimised |
| `dhryO2` | Microware cc, optimised<br>**How:** All eleven Dhrystone builds READ A RUN COUNT FROM STANDARD INPUT before they start -- run bare they print two lines and wait. `echo 200000 \| dhryO2'. Under os9exec even 20000 runs finish inside one tick of the clock, so it answers "Measured time too small ... Please increase number of runs" rather than a rate; the comparison between builds is what they are here for, and on real hardware it works as intended. |
| `dhryshamu` | &#9733; Shamus build |
| `dhryshamu2` | &#9733; Shamus build, second variant |
| `disktest` | measure disk performance  [no military use -- DOC/EFFO-INFO]<br>`Syntax   : disktest [<opt>]` |
| `fibo` | &#9733; Fibonacci benchmark |
| `float` | &#9733; floating-point benchmark |
| `savage` | &#9733; Savage floating-point accuracy benchmark |
| `sieve` | &#9733; sieve of Eratosthenes benchmark |
| `time` | &#9733; time a command |
| `timid` | timing utility -- and it reports itself as `timit', which is the name in its own usage line.  It takes NO command to time: `timid wc -c file' answers `timid: unknown option c'. `time' is the one that times a command.<br>`Syntax: timit [<opts>]` |

**Debugging**

| | |
|---|---|
| `sdb` | SDB 2.0 - symbolic debugger |
| `trap` | &#9733; system-state trap-handler example -- it installs a trap from system state.  Ask for it by PATH: `trap' is also a bash builtin, and the builtin answers first, silently.<br>**How:** The system-state trap-handler example: it installs a trap from system state. Ask for it BY PATH -- `/dd/CMDS/trap' -- because `trap' is also a bash builtin, and the builtin answers first, silently. |

**Libraries**

| | |
|---|---|
| `libsplit` | Split a linker library into its component modules<br>`Syntax   : [<opts>] {<library>} [<opts>]` |

**Source checking**

| | |
|---|---|
| `bcheck` | &#9733; count brackets in a source file and report a mismatch.<br>`Syntax: bcheck [<opt>] [<filename>]` |
| `ccheck` | &#9733; C program checker -- matching brackets, quotes, comment brackets, and indentation that disagrees with them<br>**How:** Checks C source for mismatched brackets, quotes and comment markers, and for indentation that disagrees with the nesting. Needs cio. |

**Source formatting**

| | |
|---|---|
| `cb` | &#9733; C beautifier<br>`Usage:  cb <input.fil >output.fil` |
| `cpr` | print/pretty-list C source files -- and it expands what it is given rather than passing it through: 40 bytes of /dd/SYS/motd come out as 404, paginated.<br>`Usage: cpr [-cCnNsS] [-T title] [-t tabwidth] [-p[num]] [-r[num]] [-l pagelength] [[-f] file] ...` |
| `ifdef` | resolve #ifdefs in C source<br>`Syntax: ifdef [<opts>] [<file>] [<opts>]` |
| `indent` | reformat a C source program for readability<br>`Syntax: indent [<opts>] [<inpath> [<outpath>]] [<opts>]` |
| `patch` | Larry Wall's patch - apply a diff.  It recognises a diff, then stops with `Error reading tmp file /dd/tmp/patchi000003' and leaves the target unchanged. `diff' itself works |
| `unifdef` | remove #ifdef sections from C source.  Its option is `-d<sym>' -- lower case, no equals -- and `-u<sym>' for the other side; `-D<sym>' is refused.<br>**How:** Its option is `-d<sym>' -- lower case, no equals -- and `-u<sym>' for the other side. `-DOSK' is refused with its own help, which reads like the program working and is not. |

**Source navigation**

| | |
|---|---|
| `ctags` | generate a vi tags file from C source (BSD)<br>`usage: ctags [-BFadtuwvx] [-f tagsfile] file ...` |
| `cxref` | &#9733; C cross-reference lister -- numbered listing + symbol table<br>`Syntax:		cxref [-opts] [path]` |
| `etags` | generate an emacs TAGS file<br>`Syntax: etags { [<opts>] <path> }` |
| `rdoc` | &#9733; reverse documentation: C source in, structure chart out |
| `xrf` | C cross-reference generator -- it wants its language table, `C.XRF', in the CURRENT DATA DIRECTORY.  The disk has it as DOC/xrf/c.xrf; copy that beside your source or it stops with `Cannot open Language Table file'<br>**How:** Wants TWO files in the DATA directory, not on the command line: its language table as `C.XRF' (the disk has it as DOC/xrf/c.xrf -- copy it) and the source you name. Given both it prints a full cross-reference: every identifier with the lines it appears on. |

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
| `rcsdiff` | &#9733; RCS diff.  The RCS set here depends on the clock advancing between check-ins: two made in the same second collide and `ci' refuses the second -- `Date ... is not later than ... in existing revision 1.1'.  With only one revision there is nothing for rcsdiff to compare, and it then cannot create its own temporary either.  `ci', `co' and `rlog' work singly. |
| `rcsident` | &#9733; RCS ident |
| `rcsmerge` | &#9733; RCS merge -- same clock, same result as rcsdiff |
| `rlog` | &#9733; RCS log |

</details>

## Compilers & build

*C compilers and their passes, assemblers, linkers, make and parser generators.*

<details><summary>40 programs</summary>

**Alternates**

| | |
|---|---|
| `m4_0.5` | &#9733; another build of m4 -- it is the build that ships as `m4'; the earlier one mangled what it expanded.<br>`Usage: m4 [options] file ....` |

**Assemblers & linkers**

| | |
|---|---|
| `as0` | 6800/6802 cross-assembler (xasm).  See the note below this list.  A sample source for each of the six ships in DOC/xasm, so they can be seen doing their job rather than printing their usage line: `as0 /dd/DOC/xasm/sample.a0 - l s' lists the assembly with addresses, opcodes and a symbol table. The options come after a lone `-', and as11 is the one exception -- it takes them without it<br>**How:** Assemble the sample that ships with it: `as0 /dd/DOC/xasm/sample.a0 - l s' -- the options come after a lone `-', `l' for the listing and `s' for the symbol table. There is a sample for each of the six (sample.a0, .a1, .a4, .a5, .a09, .a11) and each is written for its own processor: as09 rejects the 6800 one, correctly. as11 is the one that takes its options without the `-'. None of these is a 68000 assembler. |
| `as09` | &#9733; 6809 assembler -- the one that targets the 6809 itself. It rejects 6800 source (`ldaa' is a 6800 mnemonic, not a 6809 one); DOC/xasm/sample.a09 is written for it<br>`Usage: as09 [files]` |
| `as1` | 6801/6803 cross-assembler (xasm).  DOC/xasm/sample.a1<br>`Usage: as1 [files]` |
| `as11` | 68HC11 cross-assembler (xasm).  DOC/xasm/sample.a11<br>`Usage: as11 [files]` |
| `as4` | 6804 cross-assembler (xasm).  DOC/xasm/sample.a4<br>`Usage: as4 [files]` |
| `as5` | 6805/68HC05 cross-assembler (xasm).  DOC/xasm/sample.a5<br>`Usage: as5 [files]` |
| `assembler` | GSHELL front-end for the assembler -- the same full-screen menu as `gshell', headed `Assembler-SHELL V1.0'.  It does not assemble anything itself; `as0' and its five siblings are the assemblers<br>**How:** Full-screen: it takes over the display. **control-C gets you out**; none of q, Q, control-D or ESC do. |
| `lnk` | RTF FORTRAN link driver; calls l68 with /h0/LIB/sys.l, which is Microware's |
| `lnk.org` | as lnk, the original build<br>**How:** `load /dd/CMDS/os9lib' first. Without it this calls F$Link for os9lib, gets E_MNF and exits printing nothing. DOC/README-RUNNING names the four programs that do this. |

**C toolchain**

| | |
|---|---|
| `cc1plus` | GCC 2.x C++ compiler pass, where it was built |
| `cc2` | GCC 2.x C compiler pass, where it was built |
| `cc2plus` | GCC 2.x C++ pass, second form |
| `cccp2` | &#9733; GCC 2.x preprocessor, where it was built<br>`Usage: cccp2 [switches] input output` |
| `collect` | GCC 2.x collect2, where it was built<br>`Syntax   : collect [<opts>] {<file>} [<opts>]` |
| `compiler` | GSHELL front-end for the C compiler<br>**How:** Full-screen: it takes over the display. **control-C gets you out**; none of q, Q, control-D or ESC do. |
| `gcc` | &#9733; the GCC driver -- GCC139's and GCC2's share this name. They are NOT the same version, and neither is 2.x: GCC139/gcc answers `gcc version 1.39' and GCC2/gcc answers `gcc version 1.42', read out of `gcc -v'<br>`Usage: gcc {options} {files} {options}` |
| `gcc2` | &#9733; the GCC 2.x driver, and the only one that is: `gcc version 2.5.6'<br>`Usage: gcc2 {options} {files} {options}` |
| `gcc_cc1` | GCC 1.39 C compiler pass |
| `gcc_cc1plus` | GCC 1.39 C++ compiler pass |
| `gcc_cc2` | GCC 2.x compiler pass, under the name gcc2 forks |
| `gcc_cccp` | GCC 1.39 preprocessor<br>`Usage: gcc_cccp [switches] input output` |
| `gcc_cccp2` | &#9733; GCC 2.x preprocessor, under the name gcc2 forks<br>`Usage: gcc_cccp2 [switches] input output` |
| `gcc_collect` | GCC 1.39 collect2<br>`Syntax   : collect [<opts>] {<file>} [<opts>]` |
| `gpp` | the C++ driver -- and it is a GCC 1.x one.  GCC2/gpp says `gpp version 1.40.3 (based on GCC 1.40)' and GCC139/gpp says 1.37.1<br>`Usage: gpp {options} {files} {options}` |
| `gpp_cc1plus` | GCC 2.x C++ pass, under the name gpp forks |
| `gpp_cccp` | &#9733; GCC 2.x preprocessor, under the name gpp forks<br>`Usage: gpp_cccp [switches] input output` |
| `gpp_collect` | GCC 2.x collect2, under the name gpp forks<br>`Syntax   : collect [<opts>] {<file>} [<opts>]` |

**Fortran**

| | |
|---|---|
| `creadoc` | extract the documentation header (C++ ... C--) from every .f file in the current directory into creadoc.txt.  It reads each file name from a fixed column of a `dir -eadu' listing. Written in 1989, it expects a two-digit year there; OS-9 prints 2026 as `126', one digit wider, so the name lands a column right and creadoc opens it with a leading space and stops.  Date the sources before 2000 and the column is right -- and it then writes nothing, so a further stop is still to be found.  DOC/rtf/biory.doc is its output for biory.f. Source: SRC/rtf/creadoc.f |
| `for` | the RTF/68K FORTRAN driver, and a bash KEYWORD -- ask for it by PATH (`/dd/CMDS/for') or bash swallows the name.  It uses Microware's `shell' on your execution path, forking one to run each compiler pass.  Call `rtf' directly and you need no shell at all -- see DOC/README-FORTRAN |
| `rtf` | RTF/68K Real-Time Fortran-77 compiler, v2.14 (CERN, 1987), AND IT COMPILES HERE.  `load /dd/CMDS/os9lib' first, then `rtf <file>.f' reads the Fortran and writes 68k ASSEMBLY beside the source: zero errors, `RTF normally completed'. Assemble and link that with Microware's r68 and l68. Call rtf directly: the `for' driver forks Microware's `shell' to run it.  Sources to try in SRC/rtf.  Manual: DOC/rtf/rtfman.txt |

**Make & generators**

| | |
|---|---|
| `bison` | GNU bison 1.19 parser generator -- ADDED; skeletons in /dd/LIB<br>`Usage: bison [-dltvyV] [-b file-prefix] [-o outfile] [-p name-prefix]` |
| `dmake` | &#9733; dmake 3.70 - parallel make with its own makefile dialect |
| `flex` | lexical analyzer generator -- see DOC/flex/README-FLEX FIRST<br>`Syntax   : flex [-bcdfinpstvFILT8 -C[efmF] -Sskeleton] [filename ...]` |
| `gmake` | GNU make -- ADDED (the gnu.bin build of make is the broken one)<br>`Usage: gmake [options] [target] ...` |
| `m4` | m4 macro processor.  It expands macros correctly, from a file or a pipe<br>`Usage: m4 [options] file ....` |
| `make` | &#9733; make -- maintains a target. Two rules catch people: a command line must begin with a TAB (which will not survive being typed at this terminal, so copy DOC/make/demo.mk rather than echoing one), and a recipe must have no shell metacharacter -- `cp a b' runs, `cat a > b' gets `That path name doesn't lead to a file'.  DOC/STATUS has both<br>**How:** It works. Copy `/dd/DOC/make/demo.mk` rather than writing a makefile at the shell -- a command line must begin with a TAB and a tab does not survive being typed at this terminal. And keep shell metacharacters out of a recipe: `cp a b` runs, `cat a > b` gets "That path name doesn't lead to a file", because make forks bash with the line as a PATHNAME rather than with -c. The default rules are in default.mk beside it, and make looks for that along your PATH. |
| `makeinfo` | GNU makeinfo -- Texinfo to info<br>`Usage: makeinfo [options] texinfo-file...` |
| `yacc` | yacc parser generator, rebuilt `-qm' from SRC/effo_yacc. It reads a grammar and writes y.tab.c into the data directory.  `bison' is the other parser generator here and reports states and conflicts<br>`Syntax   : yacc [-dltv] [-b <prefix>] filename` |

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
| `adlcomp` | compile an ADL world<br>**How:** Compiles an ADL world: `adlcomp /dd/ADL/DEMOS/tiny.adl -o /dd/tmp/tiny -i /dd/ADL'. The `-i' is where standard.adl lives and is required. |
| `adldebug` | play with the debugger attached<br>**How:** adlrun with the debugger attached. |
| `adlrun` | <world>                          play it<br>**How:** Plays a compiled ADL world: `adlrun /dd/tmp/tiny'. The tiny demo opens "You are in a small but comfortable room... There is a red pillow here." NOTE: play from an RBF disk, not a host-directory mount; reading a world off /hN under os9exec trips an assertion inside the emulator. |
| `adltouch` | refresh a compiled world<br>**How:** Refreshes a compiled world after you edit its source. |

**Interpreters**

| | |
|---|---|
| `forth` | &#9733; Forth-83, and it runs.  Type at it:<br>**How:** Type `2 3 + . cr' and it answers 5; `: squares 10 1 do i dup * . loop cr ;' then `squares' prints them; `words' lists its vocabulary; `bye' leaves. A SOURCE FILE IS A COMMAND-LINE ARGUMENT -- `forth fibonacci.tst' loads it and gives you the prompt -- because `include' is defined in the library, not the kernel. The library and the twenty-two programs it shipped with are in lib/tile and lib/tile/TST; lib/tile/readme explains the name (TILE is this Forth's own). |
| `lua` | Lua 3.0, a small scripting language -- and it RUNS, once it has a `csl' of the edition it was built against.  As it stands it stops at `**** csl traphandler mismatch ****', because the `csl' on this disk is edition 16 and lua wants a later one.  `load' the newer module first and it works:<br>**How:** It stops at `**** csl traphandler mismatch ****' because it was built against a LATER csl than the edition 16 this disk ships. `load' a later csl module first -- anyone with a Microware SDK has one -- and it runs: `lua DOC/lua/examples/hello.lua' prints `hello world, from Lua!'. `luac' needs none of that. Eight example scripts are in DOC/lua/examples. |
| `luac` | &#9733; Lua bytecode compiler -- luac -o out in.lua<br>**How:** `luac -l -o out.lc in.lua' compiles and lists the bytecode instruction by instruction. It needs no csl and works as the disk stands. DOC/lua/examples has eight scripts that came with the package. |
| `runc` | Runs a compiled Lua chunk as an OS-9 command -- and stops with the same csl mismatch as `lua'.  DOC/STATUS names all five programs that do |
| `wam.sbprolog` | SB-Prolog 2.2 WAM engine -- see DOC/sbprolog/README-SBPROLOG<br>`Usage: sim [-Ttdns] [-m s_size] [-p p_size] [-b tr_size] [-ui num] pil_file_name ...` |
| `xlisp` | XLISP 2.1 Lisp interpreter |

</details>

## Archives & compression

*Pack, unpack and shrink -- lha, zip, tar, arc, zoo, and OS-9 module libraries.*

<details><summary>37 programs</summary>

**Alternates**

| | |
|---|---|
| `arc_5.12` | ARC v5.12, third-party; /dd/CMDS/arc is 5.21.  5.12 wants its command letter with a leading dash, and cannot write an archive on this disk: the rename of its temporary file into place fails every time, with `No Children'<br>`Usage: arc -{amufdxeplvtc}[bswn][g<password>]` |
| `compress_4.0` | compress 4.0, another edition of CMDS/compress<br>`Syntax   : compress [-cdfvV] [-b maxbits] [file ...]` |
| `compress_rebuilt` | our source build of CMDS/compress, from the same hc_utils source.  Same program, and the two agree byte for byte on what they write<br>`Usage: compress [-dfvoV] [-b MaxBits] [file ...]` |
| `gtar` | another GNU tar; CMDS/tar is the one the image build uses |
| `gzip020_csl` | &#9733; gzip 1.2.4, 68020, needs csl<br>`usage: gzip020_csl [-gzip020_cslcdfhlLnNgzip020_csltvV19] [-S suffix] [file ...]` |
| `gzip020_nocsl` | gzip 1.2.4, 68020, no csl needed<br>`usage: gzip020_nocsl [-gzip020_nocslcdfhlLnNgzip020_nocsltvV19] [-S suffix] [file ...]` |
| `gzip68k_csl` | &#9733; gzip 1.2.4, 68000, needs csl<br>`usage: gzip68k_csl [-gzip68k_cslcdfhlLnNgzip68k_csltvV19] [-S suffix] [file ...]` |
| `gzip68k_nocsl` | gzip 1.2.4, 68000, no csl needed<br>`usage: gzip68k_nocsl [-gzip68k_nocslcdfhlLnNgzip68k_nocsltvV19] [-S suffix] [file ...]` |
| `gzipcpu32_nocsl` | gzip 1.2.4, CPU32, no csl needed<br>`usage: gzipcpu32_nocsl [-gzipcpu32_nocslcdfhlLnNgzipcpu32_nocsltvV19] [-S suffix] [file ...]` |
| `gzipcpu32k_csl` | &#9733; gzip 1.2.4, CPU32, needs csl<br>`usage: gzipcpu32k_csl [-gzipcpu32k_cslcdfhlLnNgzipcpu32k_csltvV19] [-S suffix] [file ...]` |
| `lharcs` | C-LHarc 1.01, older than CMDS/lha 2.08<br>`Usage: lharcs {axevlufdmctp}[qnftv] archive_file [files or directories...]` |
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
| `marc` | MARC, the archive MERGER -- `marc <target> <source> [names]' copies members from one .arc into another<br>`Usage: MARC <tgtarc> <srcarc> [<filename> . . .]` |
| `shar` | Shell-archive creator, and ONE BROKEN CHECK is all that stops it: its read-access test rejects every file that EXISTS -- `No read access for file: <name>' on its own standard output, for world-readable files that `cat' reads, absolute or relative, with -a or without.  Hand it a name that is NOT there and the check passes vacuously: it writes the whole shell-archive preamble, cut line and all, and only then fails at open.  For making an archive here, use `tar', `zoo' or `lha'. |
| `tar` | GNU tar 1.10<br>`Syntax : tar [ctx][mfv] tarfile [file(s)...]` |
| `unzip` | &#9733; Info-ZIP unzip -- reads zips made elsewhere; DOC/zip/sample.zip is one to try it on.  `zoo', `tar' and `gzip' are the archivers on this disk<br>`Usage: unzip [ -options[modifiers] ] file[.zip] [filespec...]` |
| `zip` | Info-ZIP zip 1.9.  It deflates correctly, writes a temporary file (_Z000003), then cannot rename it over the target and reports `zip error: Could not create output file', in /dd/tmp and in /dd alike.  `zoo', `tar' and `gzip' round-trip exactly. |
| `zipnote` | Info-ZIP zipnote -- view/edit zip comments<br>`Usage:  zipnote [-w] [-b path] zipfile` |
| `zipsplit` | Info-ZIP zipsplit -- split a zip archive<br>`Usage:  zipsplit [-ti] [-n size] [-b path] zipfile` |
| `zoo` | &#9733; zoo archiver<br>`Usage: zoo {acDeglLPTuUvx}[aAcCdEfInmMNoOpPqu1:/.@n] archive file` |

**OS-9 module libraries**

| | |
|---|---|
| `ar2` | &#9733; Ar V2.00 -- Carl Kreider's archiver, a later edition than the V1.2 included as `ar'.  Both are here; ar is unstarred<br>`Usage:  Ar -<cmd>[<modifier>] archive [file .. ]` |
| `liborder` | &#9733; order the modules in an OS-9 library -- give it one. On /dd/LIB/alib.l and the other libraries here it works. Handed a plain file instead it reads a length from what it takes to be a ROF header and asks for that many bytes, which floods `No more memory !!!'.<br>`Usage: liborder <options> file1.r file2.r ...` |
| `modbuster` | Split merged OS-9 module files<br>**How:** Give it a file holding SEVERAL modules and it writes one file per module in the CURRENT directory. Use ksh to put yourself somewhere writable first. `/dd/CMDS/GAMES/cyberwar' looks like a candidate but modbuster hangs on it with no output at all; a single ordinary module (`/dd/CMDS/today') shows it working. |
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
| `crypto` | &#9733; cryptogram puzzle solver's assistant<br>**How:** `crypto -h' is the real option list and `-i' the interactive commands; its bare answer is two lines naming those. As a FILTER it ends the emulator session here, so read the help rather than piping through it. |
| `des` | &#9733; DES file encryption -- it writes `<file>.n' and removes the original.  It does not restore a file run through it twice with the same key (the result checksums 00000000), so for a round trip use `xcrypt'<br>**How:** It takes FILES and has no option flags at all -- `des file ...'. `-e' and `-?' are read as filenames and earn `Can't read -e.' |
| `md5` | MD5 checksum<br>`Usage: MD%d <-opts> <filename>` |
| `xcrypt` | &#9733; file encryption/decryption |

**Macintosh**

| | |
|---|---|
| `binhex` | Encode a file as Macintosh BinHex 4.0<br>`Usage: binhex [-binhex] [files]` |
| `hexbin` | Decode BinHex back to a Macintosh file<br>**How:** Decodes Macintosh BinHex (.hqx) files, which is how Mac software travelled by mail and BBS. binhex goes the other way; unsit opens StuffIt archives and macunpack opens PackIt ones. All trap-free. DOC/macutils has the package readme. |
| `macbin` | MacBinary encode/decode<br>`Usage  :   Converts files to MacBinary format` |
| `macsave` | unpack MacBinary files FROM STANDARD INPUT, and its SILENCE IS CORRECT: its own manual page says it "reads standard input and silently writes the file(s) it contains", giving them `.bin' names in the current directory and making subdirectories for embedded folders. `macbin' is the translator that MAKES one. DOC/macsave/macsave.1.<br>**How:** Its silence is CORRECT and documented: DOC/macsave/macsave.1 says it "reads standard input and silently writes the file(s) it contains". `macbin' makes the MacBinary it wants, and the pair round-trips. |
| `macstream` | Read a MacTerminal file stream.  It measures the file before it reads it and answers `Short file <name>' for anything too small to be one<br>`Usage: macstream [-macstream] files` |
| `macunpack` | Unpack a packed Macintosh archive<br>`Usage: macunpack [-macunpack] [filename]` |
| `mcvert` | Convert between Macintosh file representations<br>`Usage: Mcvert [-rduxh] [DUpqsv] filename(s)` |
| `UnMacpack` | Unpack MacPack format.  Named for its module, which is UnMacpack rather than unmacpack<br>`Usage: macunpack [-UnMacpack] [filename]` |
| `unsit` | Unpack a StuffIt archive (V1.15f, Nigel Perry)<br>`Usage: Unsit [-rdulM] [-vqfm] filename` |

**Text encodings**

| | |
|---|---|
| `atob` | ASCII-to-binary decode<br>`Usage: atob <filein >fileout` |
| `btoa` | Binary-to-ASCII encode<br>`Usage : btoa <filein >fileout` |
| `cuts` | &#9733; Coco Usenet Transfer Utility -- encodes a binary as text that will pass through electronic mail, in a form that survives gateways between ASCII and EBCDIC machines; `-d' decodes, which is the half worth having.  The encoder (`-e') asks for billions of bytes of memory, is refused, and writes empty data lines until it is stopped.<br>**How:** Coco Usenet Transfer Utility: it encodes a binary as mail-safe text and `-d' decodes a cuts file. Use `-d' for the half worth having; the encoder (`-e') asks for gigabytes of memory and is refused. |
| `todos` | &#9733; OS-9 to DOS line endings.  Use `autolf -c -C -L', which does the job -- todos and toos9 are no-ops (see below) |
| `toos9` | &#9733; DOS to OS-9 line endings.  `autolf -l -C' converts the other way and is the one to use: todos and toos9 rewrite a file in place but leave it byte-identical to the input on CR-only OS-9 text, so they are no-ops here.  `flip' host-side or `tr' also convert. |
| `uudecode` | &#9733; uudecode<br>`USAGE: uudecode [infile]` |
| `uuencode` | &#9733; uuencode.  Give it ONE argument -- the input file -- and redirect: `uuencode myfile > myfile.uu'.  Its own usage line prints `uuencode >outfile [infile] name', which fails with two arguments.<br>**How:** ONE argument, the file: `uuencode /dd/SYS/motd > out.uu'. Its usage line reads as though it wants two and with two it prints that line and stops. `uudecode' is what undoes it. |
| `uuexpand` | make text portable across 8- and 16-bit machines, reading standard input: its own usage is `uuexpand [opts]' or `uuunexpand [opts]', with -8 and -16 choosing which.  To undo a `uuencode', that is `uudecode', which is here<br>**How:** Makes text portable across 8- and 16-bit machines, reading standard input. Its own usage is `uuexpand [opts] / or: uuunexpand [opts]' with -8 and -16 choosing which. Use `uudecode' to undo `uuencode'. |

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
| `ckermit` | &#9733; C-Kermit 5A(190) BETA.14, 24 Jul 94 -- the cio build. |
| `kermit` | OS-9 Kermit Version 1 Release 5 -- serial file transfer and terminal emulation.  `ckermit' is the C-Kermit, and REBUILT/kermit_cio is our build of this one.  Run with no cio present it starts and prints its banner; it is REBUILT/kermit_cio that wants the module<br>`Usage: kermit c[le line esc.char]   (connect mode)` |
| `kermit2` | Kermit Program Version 1 Release 6 -- the same command letters as `kermit', 5K smaller.  DOC/README-KERMIT compares all six<br>`Usage:   kermit c[le line esc.char]   (connect mode)` |
| `kermit3` | Kermit68K version 1.0.00, 01 July 1987 -- a DIFFERENT program from the other small ones: it puts up its own `Kermit68K>' prompt and reads a Kermit.ini, rather than taking command letters.<br>`Usage: kermit [-x arg [-x arg]...[-yyy]...]]` |
| `kermit_cio` | &#9733; a source build that links cio; CMDS/kermit is the archive binary and needs none<br>`Usage: kermit c[le line esc.char]   (connect mode)` |
| `xkermit` | &#9733; the same version and banner as `kermit' -- OS-9 Kermit 1.5 -- in half the space, because it links cio rather than carrying stdio.  DOC/README-KERMIT<br>`Usage: kermit c[le line esc.char]   (connect mode)` |

**Mail**

| | |
|---|---|
| `answer` | &#9733;  clears the screen and asks `Message to:' |
| `arepdaemon` | &#9733; the daemon autoreply relies on.  It reads /dd/USR/LIB/ELM/autoreply.data; without it, `Error 216 attempting fstat' -- though it still touches autoreply.log on its way there |
| `autoreply` | &#9733; send an automatic reply while you are away.  It resolves your mailbox by the session's numeric owner rather than $USER, so under this identity it reaches for a mailbox named `su' and stops there; turning autoreplying off does not need the mailbox and answers for real<br>`Usage: autoreply <filename>	to start autoreply,` |
| `checkalias` | &#9733; check an alias resolves before you rely on it. `listalias' answers the same question and prints its result<br>`Usage: checkalias alias [alias ...]` |
| `disable` | &#9733; disable a UUCP device<br>`Syntax: disable <port>` |
| `dotilde` | &#9733; the mailer's TILDE-ESCAPE handler: it reads a message from standard input and acts on the `~' commands in it, answering `Unrecognized tilde command' and `Continuing...type "." or <ESC> to end message...' |
| `elm` | &#9733; the Elm mail reader itself -- full-screen, menu-driven<br>**How:** The full-screen mail reader. It opens on the folder that ships for this account, `~/SPOOL/MAIL/tester', showing one message. `readmsg 1' prints a message without opening the reader; `messages' counts the folder. Mail lives at /dd/SPOOL/MAIL/<user>, and SYS/login points MAIL at it. |
| `enable` | &#9733; re-enable a UUCP device<br>`Syntax: enable [<opts>] <port> [<opts>]` |
| `fastmail` | &#9733; send a file as mail without opening the reader.  It needs a delivery agent to deliver it<br>`Usage: fastmail {args} [ filename \| - ] address(es)` |
| `filter` | sort incoming mail into folders by rule.  A PIPE stage: its own usage line begins `\| filter'<br>`Usage: \| filter [-nrvlq] [-f rules] [-o file]` |
| `frm` | &#9733; list who your mail is from, one line each.  On this port it answers `tester has no mail' for a folder that `messages' counts and `readmsg' prints, so use those two<br>**How:** Lists who your mail is from, one line each. Reads $MAIL, which SYS/login sets. |
| `lcasep` | &#9733; lower-case a name for mail<br>`usage: lcasep [-f file] [-o outfile]` |
| `listalias` | &#9733; list the aliases you have, once newalias has compiled them: `home  os9-freeware (This Collection)'.  Its -s and -u forms pipe through `egrep'; the plain form needs nothing extra<br>`Usage: listalias [ -s \| -u ] <optional-regular-expression>` |
| `lmail` | &#9733; local mail delivery.  Its usage line answers; giving it a real recipient does not return here -- it hangs, and only the session's own end brings it down<br>`Syntax: lmail <user name> {<user name>}` |
| `mail` | &#9733; a simple mail sender<br>`Syntax: mail [<opts>] [<user>]` |
| `mailx` | &#9733; the mail reader and sender |
| `makedb` | build smail's path-alias dbm: `makedb -o <name> <file>' writes <name>.dir and <name>.pag.  /dd/USR/LIB/SMAIL/palias is the source it defaults to |
| `messages` | &#9733; count and list what is in a folder.  Works<br>**How:** Counts what is in your mail folder: "There is 1 message in your mailbox". |
| `newalias` | &#9733; rebuild the alias database -- run it after editing aliases, and add -g for the system file.  `processed 2 aliases', `processed 6 aliases'<br>**How:** Rebuilds the Elm alias database from USR/LIB/ELM/aliases.text after you edit it. |
| `newmail` | &#9733; watch for mail arriving and say so.  -d reports the folder it is watching and its size<br>`Usage: newmail [-d] [-i interval] [-w] {folders}` |
| `nptx` | &#9733; smail's full-name permuter: it takes `<full name>' TAB `<login>', one per line, and answers with the pair reversed.  Anything else -- an address list, a bare name, the password file -- earns `format error: <the line>'<br>**How:** smail's full-name permuter, and its input format is the whole trick: one line of `<full name>' TAB `<login>' and it answers with the pair reversed. ANY other shape -- an address list, a bare name, the password file -- earns `format error: <the line>', which is how it came to be described as an alias expander. |
| `pathalias` | compute mail routes from a map<br>`usage: pathalias [-vciDfI] [-l localname] [-d deadlink] [-t tracelink] [-g edgeout] [-s treeout] [-a avoid] [files ...]` |
| `philmail` | the philmail mailer |
| `printmail` | &#9733; format a message for a printer.  It forks `readmsg' by bare name, so load it first; then it prints the message the same way `readmsg' would<br>**How:** It forks `readmsg' BY BARE NAME, and OS-9 resolves a bare-name fork against the EXECUTION directory, never against PATH -- so it is silent from everywhere except /dd/CMDS/ELM. `load /dd/CMDS/ELM/readmsg' once and it works from anywhere: a RESIDENT module is found by name with no directory search at all. |
| `pwparse` | &#9733; parse the password file for the mailer |
| `read_mail` | &#9733; a small mail reader of its own: it opens /dd/MAIL/mail_<user> and offers `[L]ist again, e[X]it & delete mail, exit & [N]ot delete'<br>**How:** Not vi's helper and not part of Elm: it has a mail directory of its own, /dd/MAIL/mail_<user>, and $USER decides which. Answer its L/X/N prompt ON STANDARD INPUT -- `echo N > f; read_mail < f'. With no input at all it re-asks without bound. |
| `readmsg` | &#9733; print selected messages from a folder, by number or by pattern.  Works<br>**How:** Prints messages from a mail folder: `readmsg 1' for the first. It reads the welcome message in /dd/SPOOL/MAIL/tester. |
| `rmail` | &#9733; deliver incoming mail (invoked by uuxqt, not by you). Given a local name it builds <mailbox>/<user>, and the mailbox here is a file, so it stops with `can't change to mailbox: /dd/SPOOL/MAIL/tester/tester'.  Given a `host!user' address for remote delivery it does not return at all<br>**How:** Local delivery builds <mailbox>/<user> and stops, because the mailbox here is a file: `rmail tester' answers plainly. `rmail "site!user"' for remote delivery does not return. |
| `smail` | &#9733; smart mail router<br>`Usage:   smail [<options>] address...` |
| `uupoll` | &#9733; poll a site for waiting work.  It works silently: `uupoll nowhere' leaves /dd/SPOOL/uucp/nowhere/C.nowhereAPOLL, and the grade letter from -g goes into the name (`-gZ' -> ...ZPOLL)<br>**How:** Polls a UUCP site for waiting work, and it does the job in SILENCE -- which is why it reads as broken. `uupoll <site>' leaves /dd/SPOOL/uucp/<site>/C.<site>APOLL; the grade letter from -g goes into the name, so `-gZ' gives ...ZPOLL. Blars uucp; wants the `uucp' user, which SYS/password has. |
| `uux` | &#9733; run a command on another UUCP site<br>**How:** Runs a command on another UUCP site. This is BLARS uucp, which reads USR/LIB/UUCP/Config -- a different configuration from UUCPbb's SYS/UUCP. Both ship. |

**News**

| | |
|---|---|
| `bdecode` | &#9733; decode a batched news article<br>`Usage: bdecode [file]` |
| `byteflip` | &#9733; byte-swap a dbz database between architectures -- hand it a dbz database<br>**How:** It is in CMDS/NEWS. Hand it a dbz database to byte-swap between architectures. |
| `c7decode` | &#9733; decode 7-bit-safe encoded news |
| `dbz` | &#9733; the news history database<br>**How:** The news history database from C News: `dbz [-a] [-x] [-c] database [file]...'. Part of a news system. |
| `expire` | &#9733; delete news articles past their expiry date |
| `newshist` | &#9733; rebuild the history file<br>`usage: newshist [-df file] msgid ...` |
| `newslock` | &#9733; the news system's lock<br>`Usage: newslock tempname lockname` |
| `postnews` | &#9733; post an article to a newsgroup<br>`Usage: postnews [options]` |
| `readnews` | &#9733; read Usenet news articles: it opens the reader and asks about each newsgroup in the active file not yet in .newsrc, then answers `**** End of newsgroups' when the news spool is empty |
| `rnews` | &#9733; unpack an incoming news batch |
| `subscribe` | &#9733; add a newsgroup to your subscription list -- for one already in /dd/.newsrc but turned off, `Newsgroup X is now subscribed.' and `X! 1' becomes `X: 1' in the file. A group not in .newsrc at all is silently left alone, which both this and unsubscribe do<br>**How:** It works, and so does `unsubscribe' -- give it a group that IS in /dd/.newsrc. A group that is not there is silently left alone. |
| `unsubscribe` | &#9733; drop one, and it does that too: `!' replaces `:'.  It has one bug of its own -- for a group that is ALREADY off it prints `Newsgroup  684700s already unsubscribed.', because the string in the binary is `Newsgroup % is already unsubscribed.' with no conversion letter after the `%'<br>`usage: unsubscribe <newsgroup> [newsgroup...]` |

**TCP/IP**

| | |
|---|---|
| `atp` | &#9733; AX.25 transport, from the KA9Q package |
| `finger` | &#9733; ask another machine who is logged in<br>**How:** Asks another machine who is logged in: `finger <userid>'. Needs a network. |
| `infoxpress` | InfoXpress client |
| `msntp` | set the clock from a network time server -- stops with a csl traphandler mismatch; see DOC/STATUS<br>**How:** Sets the clock from a network time server. |
| `net` | KA9Q net -- TCP/IP over SLIP or AX.25: telnet, ftp, smtp<br>**How:** KA9Q net, Phil Karn's TCP/IP over SLIP or AX.25 -- the stack amateur radio ran on. Needs NETHOME, NETSPOOL and TMPDIR set and a real interface; see DOC/ka9q. |
| `osknet` | OSKNET -- TCP/IP for OS-9, Telnet, FTP, Ping and SMTP<br>**How:** Charles Hedrick's TCP/IP for OS-9 -- Telnet, FTP, Ping and SMTP. It needs a network interface. Its own documentation is nine files in DOC/osknet: start with howto.doc and useguide.doc. |

**Terminal & session**

| | |
|---|---|
| `aterm` | ATerm 2.6 terminal emulator.  WORKS -- config is in SYS/ATERM; run it from a login session rather than as the machine's first process, or its terminal library bus errors.  `aterm /t1' for a real serial port.  Manual DOC/aterm, source SRC/aterm<br>`Syntax  : ATerm /serial_path` |
| `cls` | clear the screen (termcap)<br>`Syntax: cls` |
| `connect` | &#9733; connect to a serial line<br>`Usage: connect [<switches>] [<path1>] [<switches>] [<path2>]` |
| `fkeys` | define terminal function keys<br>`Syntax: fkeys [<path>]` |
| `initvdu` | &#9733; init video display<br>**How:** It sets up specific VDU hardware. On a terminal it is not defined for, it answers "is not defined for this terminal". |
| `input` | UNAXCESS BBS - input helper |
| `sbreak` | Send/clear an SS_Break signal on a serial path<br>`Syntax:   sbreak [/device]` |
| `setfont` | &#9733; load a downloadable terminal font -- setfont <path>. Given a font file it writes no byte to /term, to $PORT, or to a file $PORT names, and returns exit status 0.  With no argument it answers `usage: setfont <path>'.<br>`usage: setfont <path>` |
| `setterm` | &#9733; set the terminal type -- SetTerm 2.0, Brian C. White. `setterm' alone reports what TERM says; give it a name to change it.  When TERM names a terminal it does not know it falls back on SYS/setterm, which lists the defaults, and that file ships now -- it came in the same archive as the binary and had never been unpacked.  DOC/setterm has the manual and a termcap.extra of further entries<br>**How:** `setterm' alone reports what TERM says; give it a terminal name to change it. Run with no arguments and a terminal it wants to configure it goes FULL-SCREEN -- **ESC quits** (control-C also works, but ESC is the program's own way). SYS/setterm is the defaults file it falls back on when TERM names something it does not know, and DOC/setterm/termcap.extra has further entries you can add to SYS/termcap. |
| `tsmon2` | tsmon replacement - terminal monitor<br>`Syntax:   tsmon2 [<options>] <device name>` |
| `udate` | &#9733; UNAXCESS BBS date display -- and it gets the YEAR wrong: `Monday, August 31, 19126'.  A two-digit year (126, meaning 2026) written into a four-digit field behind a literal `19'. |
| `uwho` | &#9733; UNAXCESS BBS -- who is online.  Opens `/etc/utmp'; in OS-9 a leading /etc names a DEVICE, so it wants an /etc device presenting utmp, which the BBS would supply.  A Unix-ism from the port |
| `wysecrack` | &#9733; probe a Wyse terminal: it sends the code that asks the terminal to identify itself (`Anybody out there?' is in the binary) and reads the reply to sense its baud rate. With a Wyse terminal on the line it answers; without one it waits.  Companion to wysetime, which sets that terminal's clock |
| `wysetime` | Wyse terminal clock-setter, in BASIC09.  `runb wysetime' prints the escape sequence a Wyse terminal reads to set its own display clock; run it by bare name at an OS-9 shell. |

**Terminal & transfer**

| | |
|---|---|
| `blastem` | XModem and YModem file transfer, written for the MM/1<br>`Syntax: blastem [<opts>] {<filename> [<opts>]}` |
| `dld` | &#9733; XModem download<br>`Syntax: dld <file>` |
| `k` | Kermit transfer (Tim Kientzle) |
| `rxmod` | receive an OS-9 module over a serial line and enter it in the module directory.  Source: SRC/serload the module directory.  Source: SRC/serload<br>**How:** It stops with `can't install Vmod Trap handler' and the handler is sitting beside it: `load /dd/CMDS/COMMS/vmod_trap' first. It then gets past the install and faults inside the trap, which is a different thing and worth telling apart. |
| `sterm` | a serial terminal emulator<br>`Usage:  sterm [-df? -l'p' -e'x']` |
| `tsu` | &#9733; tterm's setup program |
| `tterm` | &#9733; Stephen Carville's terminal emulator, VT100-ish<br>`Usage:  tterm <options>` |
| `txmod` | send an OS-9 MODULE over a serial line<br>`Syntax: TXMod [<opts>] module(s) [<opts>]` |
| `uld` | &#9733; XModem upload<br>`Syntax: uld <file>` |
| `xy` | XMODEM/YMODEM transfer (Tim Kientzle).  `xy -?' prints the shared usage: send by naming files, receive by naming none; -A forces ASCII, -B binary, and -X/-Y/-K/-G/-C pick the protocol.  `z -?' lists the family's options too |
| `xydown` | XModem/YModem download, public domain.  It SENSES which the sender is using -- XModem, YModem or YModem-Batch -- and follows, and it converts line endings on the way in. Written for use inside Eddie Kuns' KBCom terminal program and stands alone.  Full source in SRC/xydown, notes in DOC/xydown<br>`Usage:  XYDOWN  [opts]  [filename]` |
| `xyt` | &#9733; X/Y/ZMODEM transfer for tterm<br>`Usage:  xyt [opts] [filename] [opts]` |
| `z` | ZMODEM transfer (Tim Kientzle).  `z -?' prints the usage for both.  $MODEM names the port; -p<port> overrides it |

**UUCP**

| | |
|---|---|
| `uucico` | &#9733; the transfer program itself -- dials, talks UUCP<br>`usage: uucico [opts] -r \| sys [sys...]  [opts]` |
| `uuclean` | &#9733; remove stale jobs from the spool.  The spool is /dd/SPOOL/uucp, and SYS/UUCP/Parameters names it.  uuclean walks every ENTRY in the spool as if it were a directory, so the README that keeps the directory in the repository trips it: `can't change to directory .../README'. Harmless, and it is why the message is not a sign of a broken spool<br>`Usage: uuclean [opts]` |
| `uucp` | &#9733; queue a file copy to or from another site |
| `uulog` | &#9733; show the transfer log<br>`Usage: uulog [-s<sysname> -u<username> -d<days>] [-f]` |
| `uuname` | &#9733; list the sites you can reach<br>`Usage:  uuname [-l]` |
| `uuxqt` | &#9733; run the jobs a remote site queued here.  It looks for a module called `procs' to see whether it is already running, so it wants a `procs' loaded (error 221 without one).<br>`Usage:  uuxqt [opts]  <sys> [<sys>...]  [opts]` |

**Web server**

| | |
|---|---|
| `authwn` | authentication helper for protected areas |
| `inetd` | &#9733; the internet daemon: it listens on a port and hands the connection to `wn'.  It opens `/socket', so it needs a TCP/IP stack presenting that device; without one it gets as far as `tcp protocol unknown'.  `inetd' alone prints its usage<br>**How:** The listener that hands incoming connections to wn. Needs a network. |
| `inetdc` | &#9733; what inetd forks for each connection.  1626 bytes with no message strings; inetd runs it, not you |
| `wn` | the web server itself, and it SERVES.  It is an inetd-style server: one HTTP request on standard input, one response on standard output, so run bare it waits.  Its document root is compiled in as /h0/c/unid/wn_1.14.3/osk -- which is on this disk, so mount the collection as /h0 as well as /dd and it answers `HTTP/1.0 200 OK' with the page. It serves the files named in that directory's index.cache; see wndex.<br>**How:** A real HTTP server (WN 1.14.3, GPL). It starts and opens its log -- the path /h0/c/unid/wn_1.14.3/osk/logs is compiled into the binary, and that directory is on this disk so it can. To serve, it needs TCP/IP under it (KA9Q or osknet, in CMDS/NET). It is an inetd-style server -- one request in on standard input, one response out -- so you can hand it a request by hand and read the reply. Its manual is 30 HTML files in DOC/wn. |
| `wn.stb` | WN's symbol table (a data module) |
| `wndex` | build the index.cache WN serves from.  It works on the CURRENT directory and IGNORES a directory given as an argument, so on this disk run it as `ksh -c "cd <dir>; /dd/CMDS/WN/wndex"' -- ksh's cd moves the OS-9 data directory where bash's does not<br>**How:** Builds the index.cache WN will not serve without. It works on the CURRENT directory and IGNORES a directory given as an argument -- on this disk that means ksh, whose `cd' is a real chdir where bash's is not: `ksh -c "cd <dir>; /dd/CMDS/WN/wndex"'. On its own it says "Can't open ./index -- skipping it", which means you are not where you think you are. The site that ships at /dd/c/unid/wn_1.14.3/osk already has its cache built; that is WN's compiled-in document root. |

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
| `graph` | the `Graph' TRAP LIBRARY itself -- a type-$0B module.  It is what g, striche, apfel, sine, showpic, graphdemo, graphsave and wgen all link.  `load' it and the trap installs; the module executes in supervisor state, so a program that calls it from the shell is entered and aborts on a supervisor-only instruction. |
| `graphdemo` | Atari GRAPH demonstration |
| `graphsave` | save an Atari GRAPH screen.  Aborts with the `graph' trap library resident, like `showpic': it wants the display |
| `lissaj` | &#9733; Tektronix demo: Lissajous figures |
| `lorenz3d` | &#9733; Tektronix demo: the Lorenz attractor in 3D |
| `showpic` | show a picture on the Atari GRAPH display.  With the `graph' trap library resident it is entered and aborts: it wants the display, not just the library. |
| `sine` | sine plot, Atari GRAPH |
| `striche` | &#9733; line drawing, Atari GRAPH.  Needs the `graph' trap library found -- see the graph entry below |
| `wgen` | Tektronix waveform generator.  With the `graph' trap library resident it runs and asks for a resolution and the intensity of each harmonic, then emits Tektronix plotting codes.  Bare, it aborts with `unintialized User Trap #5'.<br>**How:** It aborts with `unintialized User Trap #5, err=#227' until the `graph' trap library is resident: `load /dd/CMDS/GAMES/graph'. Then it asks for a resolution and the intensity of nine harmonics and draws the waveform. Give it ten numbers -- at end of input it draws for ever. `showpic' and `graphsave' need the same library AND a display, so they abort either way. |

**JPEG**

| | |
|---|---|
| `cjpeg` | JPEG encoder (IJG).  Makes a JPEG from a PNM.  It wants LF between the fields of a PNM header where the netpbm here writes CR, so patch the three separators with `pbyte' first; DOC/STATUS has the offsets both ways.<br>**How:** Makes a JPEG from a PNM -- but not straight from a netpbm PNM. cjpeg wants LF between the header fields and this disk's netpbm writes CR, so it says "Bogus data in PPM file". Patch the three separators with `pbyte` first: for `ppmmake red 8 8` they are at offsets 2, 6 and a. DOC/STATUS has the full recipe both ways. |
| `cjpeg.070` | JPEG encoder, a build for another processor.  On the 68000 its twin `cjpeg' is the one to use; the .070 files are builds for a different CPU.<br>`usage: cjpeg.070 [switches]` |
| `djpeg` | JPEG decompressor, jpeg-5a.  Decodes a JPEG to a PNM.  Its output ends each header line with LF where the netpbm here wants CR, so patch the three separators with `pbyte' to pipe it on; DOC/STATUS has the offsets.<br>**How:** Decompresses a JPEG: `djpeg -pnm image.jpg > out.ppm`. The disk has one to try, SRC/jpeglib/JPEG_5A/testimg.jpg. Its output will NOT pipe into netpbm unpatched -- djpeg writes LF at the end of a PNM header line and netpbm here wants CR. `pbyte out.ppm 2 0d` and the same at the two later separators fixes it; DOC/STATUS has the offsets. |
| `djpeg.070` | JPEG decompressor, a build for another processor.  It decodes a JPEG, including one the 68000 cjpeg wrote; its companion encoder is cjpeg.070<br>`usage: djpeg.070 [switches]` |
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
| `ppmforge` | netpbm image tool<br>**How:** `-night' takes NO ARGUMENT. Written `-night 0' the 0 swallows the parse and -width/-height are ignored. And without `-night' it builds a PLANET at its default `-mesh 256', which ends the emulator session: `ppmforge -night -width 32 -height 16'. |
| `ppmhist` | netpbm image tool |
| `ppmmake` | netpbm image tool |
| `ppmmix` | netpbm image tool |
| `ppmnorm` | netpbm image tool |
| `ppmntsc` | netpbm image tool<br>**How:** It takes a DIMFACTOR first -- 0.0 is black, 1.0 the original -- then the file. Without it you get its usage. |
| `ppmpat` | netpbm image tool |
| `ppmquant` | netpbm image tool<br>**How:** A PALETTED CONVERTER NEEDS A QUANTISED IMAGE, and this is what quantises: `ppmquant 16 in.ppm > out.ppm'. Eight netpbm writers -- ppmtoicr, ppmtosixel, ppmtouil, ppmtopuzz, ppmtopict, ppmtopi1 and two more -- write ZERO BYTES for a 24-bit PPM and correct files after it. |
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
| `imgtoppm` | AT&T Image-8 to PPM (colour)<br>**How:** Reads the Img Software Set (AT&T Image-8) format; gemtopbm reads GEM IMG. Feed it an Image-8 file. |
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
| `psidtopgm` | PostScript image to PGM (greyscale)<br>**How:** Reads the hex digits of PostScript `image' operator data: `psidtopgm <width> <height> <bits/sample>' then the hex on standard input. `echo ffffffff00000000 \| psidtopgm 4 2 8' makes a 4x2 graymap, a white row over a black one. |
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
| `pbmtopk` | PBM (bitmap) to packed font<br>**How:** A TeX font tool: it wants a pkfile, a .tfm metric file and a resolution. Point it at a .tfm. |
| `pbmtoplot` | PBM (bitmap) to plot |
| `pbmtoptx` | PBM (bitmap) to ptx |
| `pbmtox10bm` | PBM (bitmap) to X10 bitmap |
| `pbmtoxbm` | PBM (bitmap) to X bitmap |
| `pbmtoybm` | PBM (bitmap) to ybm |
| `pbmtozinc` | PBM (bitmap) to zinc |
| `pgmtofs` | PGM (greyscale) to Usenix FaceSaver |
| `pgmtolispm` | PGM (greyscale) to Lisp machine |
| `pgmtopbm` | PGM (greyscale) to PBM (bitmap)<br>**How:** WITHOUT -threshold IT IS NOT REPRODUCIBLE: its dither differs every run, so any assertion on a length or a checksum downstream of it flaps. `pgmtopbm -threshold' when you need the same answer twice. |
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
| `ppmtoyuvsplit` | PPM (colour) to yuvsplit<br>**How:** It takes a BASENAME and writes THREE files beside the DATA directory, not to standard output: <name>.Y, .U and .V. 4:2:0 subsampling, so a 32x16 image gives .Y = 512 bytes and .U = .V = 128. `yuvsplittoppm <name> <w> <h>' brings them back. |

**Plotting**

| | |
|---|---|
| `gnuplot` | &#9733; gnuplot 2.0 -- plots functions and data files.  Built-in help (SYS/gnuplot.gih); demos and sample data in DOC/gnuplot/demo<br>**How:** Type `set term' first -- it lists every output device it knows, and refuses to plot until you choose one. Its whole manual is built in: type `help'. Demos and sample data are in DOC/gnuplot/demo. Needs Microware's cio. |
| `tplot` | &#9733; Plot data to a plotter.  Asks for an interval and a range and drives the output device; written for an Atari ST<br>`Usage : hiplot <-opt1> .. <-optn> <file1> .. <filen>` |

**Ray tracing & 3D**

| | |
|---|---|
| `mtst` | &#9733; spline curve fitting - test driver |
| `rayshade` | ray tracer 4.0.  It renders, and requires Microware's `shell' on the execution path: it builds its scene through popen(), which OS-9's C library implements by forking a program of exactly that name.  It also wants `cccp' in the data directory, where the forked shell looks.  With both, it renders and reports its statistics.  DOC/rayshade has the two lines.<br>**How:** Ray tracer 4.0, and it renders. REQUIRES MICROWARE'S `shell` on your execution path -- it builds its scene through popen(), and OS-9's C library implements popen() by forking a program of exactly that name. It also wants `cccp` in the DATA directory. DOC/rayshade has the two lines. |
| `rsconvert` | convert rayshade image output between formats.  Run here it prints `/* Converted by rsconvert */' and then stops with a stack overflow, with or without a file named.<br>`usage: rsconvert [oldfile]` |

**Viewers**

| | |
|---|---|
| `mgif` | GIF inspector and viewer.  `mgif -i file.gif' reports a GIF's structure and works anywhere; DISPLAYING one needs an Atari ST, because flicker.c writes to ST graphics memory.  Source in SRC/mgif -- its GIF decoder is portable and is the part worth having<br>**How:** `mgif -i file.gif' inspects a GIF and prints its structure -- that works on any terminal. Displaying an image needs an Atari ST, because it writes straight to ST graphics memory. Try it on /dd/DEMO/gulls.gif. |

**X11**

| | |
|---|---|
| `basicwin` | X11 demo - basic window (needs an X server) |
| `X11R6shl` | X11R6 shared library loader |
| `xengine` | X11 demo - engine animation (needs an X server)<br>`Usage : xengine [Toolkit-Options][-piston piston_color][-shaft shaft_color][-cylinder cylinder_color][-roter roter_color][-back background_color][-dep depression_colore][-pre pression color][-mono][-patchlevel]` |

</details>

## Games

*Adventures, board and card games, arcade ports, dungeon crawls and puzzles.*

<details><summary>67 programs</summary>

**Adventure & fiction**

| | |
|---|---|
| `advcom` | ADVSYS adventure COMPILER -- turns .adv source into a world file (a .dat, not a .adi; the .adi is an INCLUDE).  The sample source is here, in GAMES/ADVSYS.  Copy osample.adv and objects.adi to a directory, make it the data directory (`load' advcom, then `sh -c "chd <dir>; advcom osample"') and it writes osample.dat -- bare name, because it holds a filename in 20 characters and appends `.adv'<br>**How:** The ADVSYS compiler. It opens its `@objects.adi' include by BARE NAME in the data directory and keeps a filename in 20 characters, so copy osample.adv and objects.adi from GAMES/ADVSYS to a directory of your own, `load /dd/CMDS/GAMES/advcom', then `sh -c "chd /dd/tmp/adv; advcom osample"'. It names every object it compiles and writes osample.dat. |
| `advent` | Colossal Cave Adventure, Will Crowther and Don Woods' mid-1970s original and the first text adventure -- self-contained, reads /dd/GAMES/adv/glorkz.  Needs this disk as /dd; mounted only as /h0 it cannot find its data.  Unrelated to advcom/advint.<br>**How:** Colossal Cave. Needs this disk as /dd -- it opens /dd/GAMES/adv/glorkz by absolute path, so mounted only as /h0 it cannot find its data. |
| `advint` | ADVSYS adventure INTERPRETER -- plays a world compiled by advcom, and there is one to play: build it as advcom's entry says and `advint osample' starts you in the livingroom. Both open their files by bare name in the data directory, so run them where the files are: `load' the module, then `sh -c "chd /dd/tmp/adv; advint osample"'. GAMES/ADVSYS/README has the details<br>**How:** Plays an ADVSYS world. Build one first (see advcom), then run it where the .dat is: `load /dd/CMDS/GAMES/advint', then `sh -c "chd /dd/tmp/adv; advint osample"' -- you start in the livingroom, `n' goes to the hallway, `e' to a storage room with a key. |
| `infocom` | Infocom Z-MACHINE interpreter -- a third, unrelated adventure system.  Plays the .z3 files in GAMES/INFORM (dejavu, hellow, shell -- Inform demos, not the Infocom games).<br>**How:** A Z-machine. Plays the .z3 files in /dd/GAMES/INFORM -- the Inform demos dejavu, hellow and shell. |
| `infocom.tcap` | Infocom interpreter, TERMCAP build -- and it is the one to use at a terminal.  It puts a proper status line at the top of the screen (`Y2 Rock Room     Score: 0/2') where plain `infocom' writes the cursor codes for that line as literal text down the left margin<br>**How:** The termcap build of the Z-machine, and the one to use at a terminal: `infocom.tcap /dd/GAMES/INFORM/dejavu.z3' keeps a status line (room and score) across the top. Three Inform story files ship in GAMES/INFORM: dejavu, hellow, shell. |
| `paranoia` | &#9733; the PARANOIA text adventure.  `Welcome to Paranoia!  As Philo-R-DMD you will die at times during the adventure... you will be given a new clone' -- six clones, one mission, RETURN to go on.  `float' and `savage' are the floating-point benchmarks of that name.<br>**How:** The PARANOIA text adventure. RETURN to go on, a letter to choose, `p' for your statistics, six clones. `float' and `savage' are the floating-point benchmarks on this disk. |

**Arcade & action**

| | |
|---|---|
| `greed` | Greed - grid game<br>`Usage: greed [-p] [-s]` |
| `lander` | lunar lander -- space starts a game, a digit sets the power, x or k is vertical thrust, z/j and c/l the side retros.  Its score file is GAMES/lander.hs, looked for under /h0, so mount the disk there as well<br>**How:** Full-screen. Space starts a descent, a digit sets the engine power, `x' or `k' fires the main thruster and z/j and c/l the side retros. `q' quits. |
| `pacman` | Pac-Man written for G-Windows.  At a terminal it draws nothing and returns to the shell at once.  Its maze and score file are in GAMES/PACMAN<br>**How:** Pac-Man as an ASCII maze: the keypad moves you -- 8 up, 2 down, 4 left, 6 right (the layout is in GAMES/pacman/document). The maze, score and board files are in GAMES/pacman. It draws in raw keyboard mode at an OS-9 terminal. |
| `robots` | &#9733; robots -- outrun them until they crash into each other. You are the `I', the robots are the `#' and a wreck is an `@'.  USE -m: manual mode, one robot step per move of yours; without it the game is effectively unplayable. The keys are the numeric keypad 1-9 with 5 to stand still, `t' to teleport and `s' for a last stand.<br>**How:** Play with `robots -m' -- manual mode, where the robots take one step per move you make. Keys are the numeric keypad 1-9 (5 stands still), `s' for last stand, `t' to teleport. Needs Microware's math module and a real TERM. |
| `snake` | snake arcade game.  You are the `I', the money is the `$' and the snake chases you; h/j/k/l move, `x' quits. Run it from a login session -- bare, with no TERMCAP, it bus errors instead; see DOC/README-BUSERR.  Some of its cursor moves arrive as literal text, so the board picks up stray characters as you play.  Playable, untidy<br>**How:** Full-screen. h/j/k/l move; reach the `$' before the snake reaches you. `x' quits. |
| `sokoban` | &#9733; Sokoban puzzle<br>**How:** Wants a username, so run it from a login rather than a bare shell, or it stops with "cannot get your username". |
| `tet` | Tetris -- `p' plays; s/j and f/l move a piece, d/k turns it, space drops it, q quits to the high-score table it keeps in GAMES/tet.hs.  Needs a terminal, not a pipe<br>**How:** Tetris. `p' plays from the menu; s or j moves the piece left, f or l right, d or k turns it, space drops it, ESC pauses and q quits to the high-score table, kept in GAMES/tet.hs. Give it a real terminal: it does no terminal setup of its own (the raw-mode code in SRC/tet/tet.c is inside `#ifndef OSK'), so from a pipe it draws its board and reads nothing. |
| `tt` | Tetris for terminals: , and / move, . rotates, space drops, s pauses, q quits<br>**How:** Tetris for terminals, full-screen: , and / move the piece, . rotates, space drops, s pauses, q quits. |
| `wanderer` | Boulderdash-style maze game.  Screens ARE here, in GAMES/WAND/screens; needs this disk as /dd to find them.<br>**How:** Full-screen. Dig through the earth for diamonds, forty-five on the first screen. `q' quits. Its thirty screens are in GAMES/WAND. |

**Board & card**

| | |
|---|---|
| `back` | &#9733; backgammon on a full board, points numbered 1 to 24, with the dice cup and the doubling status beside it. Single letters are the commands: R rolls, D doubles, H is the help, N starts a new game, Q quits<br>**How:** Single letters are the commands: R rolls, D doubles, H is the help, N starts a new game, Q quits. |
| `blackjack` | Las Vegas blackjack (M. Theys, 1969) in BASIC09 -- `runb blackjack' asks your name and whether you want the rules, then takes a wager and deals: RETURN draws, `s' stands, `d' doubles down, `x' splits a pair, a wager of 0 ends the game (blackjak, in GAMES, is the SNOBOL4 one)<br>**How:** BASIC09 I-code: `load /h1/CMDS/runb' then `runb blackjack' (bare module name -- a pathname gives BASIC09 error 43). It asks your name and whether you want the rules, then takes a wager and deals: RETURN draws a card, `s' stands, `d' doubles down, `x' splits a pair; a wager of 0 ends the game. runb links the `math' trap handler from the execution directory, so leave chx at CMDS -- tested, plays a full hand. |
| `blackjak` | &#9733; Las Vegas BlackJack (SNOBOL4-in-C).  Data: GAMES/SNOBOL |
| `chess` | chess against the machine on a shaded board.  It asks for your colour, your name and a long or short game, then takes a move as two squares -- `e2' then `e4', two keystrokes each with no RETURN.  68k port, three engine versions built<br>**How:** It asks for your colour, your name and a long or short game, then takes a move as two squares -- `e2' for the piece and `e4' for where it goes. Each square is two keystrokes and needs no RETURN. |
| `crib` | cribbage.  Needs TERM set, so run it from a login session -- bare it says `Unknown terminal type'<br>**How:** Full-screen cribbage, and it wants TERM -- run it from a login session. Answer the instructions question, choose a long or short game, and discard by naming a card, `7H'. Control-C gets you out. |
| `cribbage` | &#9733; cribbage -- offers instructions before it deals.  Needs TERM, so run it from a login session<br>**How:** The other cribbage, the same shape: TERM must be set, it offers the rules first, then cuts for the crib. Control-C gets you out. |
| `gnuchess` | &#9733; GNU Chess, and the build `gnuchess' runs: it is first on PATH and reads its opening book at the compiled-in path /h0/usr/src/chess/gnuchess.book, which ships here, so it answers 1.e4 with a book move.  Source `. termcap.entry' first (it reads TERMCAP as the description itself).  It shares a module name with CMDS/GAMES/gnuchess, a second port that opens its book by bare name reads TERMCAP as the description itself rather than as a filename -- and it draws the board, keeps both clocks and plays.  It opens its opening book by bare name, so it books when the book is the current directory; the CMDS build books from a fixed path and is what `gnuchess' runs<br>**How:** Full-screen chess. It reads TERMCAP as the terminal description itself rather than as a filename, so do `. /dd/SYS/termcap.entry' first; then it draws its time-control menu and plays. The build in CMDS/GAMES is the one that draws a board. |
| `gnuchessc` | GNU Chess 4.0 built for a curses display.  Its display files live at a compiled-in path; supply them there for a board.  It takes a move as `e2e4' and answers with its own<br>**How:** Its board display reads files from a compiled-in path; supply them there for a board. It still takes a move as `e2e4' and answers with its own. |
| `gnuchessn` | &#9733; GNU Chess with the 1989 display, which draws the squares as blocks of hashes so light and dark can be told apart on a terminal with no highlighting.  Source `. /dd/SYS/termcap.entry' first; moves go in as `e2e4'<br>**How:** As gnuchess: `. /dd/SYS/termcap.entry' first, then moves as `e2e4'. |
| `gnuchessr` | &#9733; GNU Chess with the plainest display -- pieces as letters, capitals for one side and lower case for the other, nothing that needs a terminal to draw.  It prompts `Enter #moves #minutes', takes a move and replies with its own<br>`Usage: gnuchess [-a] [-h] [-x xwndw]` |
| `mille` | &#9733; Mille Bornes -- the French car-racing card game<br>**How:** Full-screen Mille Bornes. `p' picks a card, `u #' plays one, `d #' discards, `s' saves the game and `q' quits. |
| `nchess` | GNU Chess 4.0 (plain display) |
| `poker` | &#9733; Cold-hand Poker (SNOBOL4-in-C).  Data: GAMES/SNOBOL |
| `tttt` | tic-tac-toe<br>**How:** Full-screen tic-tac-toe on a four-by-four board. Name a square as a column letter and a row digit, `b1'. `q' quits. |

**Chess utilities**

| | |
|---|---|
| `bincheckr` | check a GNU Chess opening-book file -- it reports booksize 0 for the 145 KB book that ships here, then aborts<br>**How:** It is in CMDS/GAMES, not CMDS. `bincheckr /dd/GAMES/gnuchess.book' prints the book's entrysize and counts and then faults at close. |
| `checkgame` | check a saved GNU Chess game for illegal moves and print the board it finishes on.  It reads the `chess.lst' that gnuchess writes when you type `list'.  A different program from `game', which makes PostScript<br>**How:** It reads the `chess.lst' that gnuchess writes when you type `list'. Play in a directory of your own -- `ksh -c "cd /dd/tmp/mine; gnuchess"' -- type `list' then `quit', and then `checkgame /dd/tmp/mine/chess.lst'. |
| `game` | draw a saved GNU Chess game board by board as PostScript, one page a move, for printing with the ChessFont file DOC/game names.  Given a game it writes the first line of the page setup and stops there<br>**How:** Same input as checkgame, a gnuchess `chess.lst', and it writes PostScript on standard output: `game chess.lst > out.ps'. Here it gets as far as the page setup and stops. |
| `gnuan` | GNU Chess analyser -- annotates a saved game move by move<br>**How:** Give it a file of moves like `e2e4 e7e5 g1f3', then a search depth and a minutes-per-move limit, and it annotates the game move by move. At the end of the file it prints the position and stops with `Bad move'. |
| `postprint` | print the positions in GNU Chess's saved hash file as PostScript, a board to a page with the best move and the search depth.  Point it at that hash file; without one it writes the first line of the page setup and stops<br>**How:** It wants gnuchess's persistent hash file -- point it at one. |

**Dungeon crawl**

| | |
|---|---|
| `hack` | hack -- the original dungeon crawl NetHack grew out of<br>**How:** RUN IT BY ITS FULL PATH: `/dd/CMDS/GAMES/hack', not `hack'. It chdirs into its playground and then stats argv[0] to date-check saved levels, so a bare name cannot resolve and it stops with "Cannot get status of hack." Invoked in full it starts: "Are you an experienced player?". Its playground -- record, bones, rumors, help -- is in GAMES/HACK/PLAYGROUND. |
| `larn` | &#9733; larn -- dungeon crawl; see the PLAYGROUND note above<br>**How:** Full-screen dungeon crawl. RETURN gets past the opening text. Control-C gets you out; its playground is GAMES/LARN/PLAYGROUND. |
| `ularn` | ULarn -- the larn variant, and its data is complete |
| `wish` | &#9733; the `hack' wish toy: run it and it prints `Wishing for: 3 potions of gain level' and `what happened to "hack"'.  The same program as CMDS/GAMES/wish.  DOC/ORIGINS lists a `wish' from EFFO disk 17 (WiSH_src.lzh, Hellmuth Michaelis, GPL) as well as one from the `toys' archive; the EFFO one is not the binary that is here, under either name |

**Other games**

| | |
|---|---|
| `ask` | the CLIENT for `wisecrack': it reads one line from /PIPE/txtpipe and prints it, and says `No Wisecracks coming' when nothing is feeding the pipe.  Start the server first -- `wisecrack &' -- and it answers.<br>**How:** Asks a yes/no question and sets the shell status, for scripts. On its own it says "No Wisecracks coming" -- it is the front half of the `wisecrack' pipe from EFFO forum 20. |
| `backgammon` | &#9733; backgammon, with a computer opponent<br>`Usage:  backgammon [-] [n r w b pr pw pb t3a]` |
| `colortest` | &#9733; G-Windows colour chart |
| `convert` | STARTS the `world' adventure. Run it and you get `WORLD. Amiga C  Version 1.02 Copyright 1987 J.D. McDonald  GOOD LUCK!', the opening paragraph and a `>' prompt.<br>**How:** It STARTS the `world' adventure -- run it and the game opens. |
| `cyberwar` | &#9733; CyberWar -- Stephen Carville's game, needs G-Windows |
| `dclock` | &#9733; a digital clock for G-Windows<br>`Usage: dclock [options]` |
| `fuddle` | chess - fuddle variant |
| `hotel` | &#9733; hotel -- two-player board game, played by coordinates<br>**How:** Full-screen: it takes over the display. **control-C gets you out**; q, Q, control-D and ESC do not. If it has a quit command of its own, its documentation in DOC/ will say. |
| `mkdict` | builds bog's dictionary from a word list in the current directory<br>**How:** Run it in /dd/GAMES/BOG, where bog's word list is; it is in CMDS/GAMES. |
| `mkindex` | builds the index bog reads its dictionary through, from the dictionary in the current directory<br>**How:** Run it in /dd/GAMES/BOG after mkdict; it is in CMDS/GAMES. |
| `nobs` | cribbage (Colonel's program)<br>**How:** Full-screen: it takes over the display. **control-C gets you out**; q, Q, control-D and ESC do not. If it has a quit command of its own, its documentation in DOC/ will say. |
| `piano` | &#9733; play notes -- piano <base note> <note duration><br>`syntax: piano <base note> <note duration>` |
| `puzzle` | &#9733; sliding-tile puzzle for G-Windows -- it draws through G-Windows, so at a terminal it gets one rule of plus signs out -- the top edge of the tile frame -- and stops.  For a 15-puzzle you can play, use puzzle15 or GAMES/puz15; both work |
| `scriptmaster` | &#9733; G-Windows scripting tool<br>`Usage: scriptmaster -t=<title> -d=<directory>.` |
| `shuffle` | a FULL-SCREEN SWITCH PUZZLE: a row of numbered switches, `LEVEL: 1', `Wich switch ?' and a move counter, where flipping one flips its neighbours.  `q' quits.  Wants TERM. For shuffling lines, `sort -r' and `tac' are the line tools<br>**How:** Full-screen: it takes over the display. **`q' quits**. |
| `stone` | &#9733; the stones game (SNOBOL4-in-C).  Data: GAMES/SNOBOL |
| `teachgammon` | &#9733; backgammon that teaches you the game as you play<br>`Usage:  backgammon [-] [n r w b pr pw pb t3a]` |
| `tess` | &#9733; tesselation puzzle |
| `vtxtcn` | world - build its text tables.  Writes .inc files; needs world's .dat files in the current directory |
| `wisecrack` | a SERVER, and `ask' is its client.  Run it in the background and every `ask' pulls one line out of it through /PIPE/txtpipe -- slogans from a German OS-9 seminar, 1992-93.  `wisecrack & ask "anything"'. |
| `world` | World - text adventure |

**Puzzles**

| | |
|---|---|
| `maze` | maze generator, small enough to have won an obfuscated-C contest.  It reads the number of rows on standard input and draws a maze that wide: `echo 11 \| maze'<br>**How:** Reads the number of rows on standard input: `echo 11 \| maze' draws a maze eleven rows deep. |
| `mines` | &#9733; minesweeper<br>**How:** Full-screen minesweeper. Name a square by its row letter and then its column letter, and answer `Mark?' with Y to flag it rather than open it. `q' quits. |
| `puz15` | the 15-puzzle -- same program as CMDS/puzzle15, built twice<br>**How:** Full-screen fifteen puzzle. Slide the tiles into the gap; `puz15 5x5' plays a bigger board. Control-C gets you out. |
| `puzzle15` | the 15-puzzle -- same program as GAMES/puz15, built twice<br>**How:** The same fifteen puzzle, in CMDS. Slide the tiles into the gap; `puzzle15 5x5' plays a bigger board. Control-C gets you out. |
| `queens` | &#9733; N-queens solver -- IOCCC entry by M. Baruch.  It reads the board size on standard input as a NUMBER and draws every arrangement it finds with no two queens attacking: `echo 6 \| queens'<br>**How:** Reads the board size on standard input as a number: `echo 6 \| queens'. |

**Word & guessing**

| | |
|---|---|
| `animal` | guess-the-animal learning game<br>**How:** The file it learns from is one you name: `animal /dd/DOC/animal/example'. Answer y or n to each question; when its final guess is wrong it asks what you were thinking of and what question tells the two apart, and writes that back into the file. Control-C leaves it. |
| `bog` | Boggle word game<br>**How:** Boggle. Space starts the three-minute round, `?' shows the rules, and you type every word you can trace through adjoining letters. Control-C leaves it. Its word list, index and help are in GAMES/BOG. |
| `hang` | &#9733; hangman<br>**How:** Hangman. Type a letter to guess it; the letters still unused are along the top. Control-C gets you out. Its word list is GAMES/dict. |

</details>

## Screen toys

*Animations and screen effects -- they draw on the terminal rather than print to it. Some run until you stop them.*

<details><summary>10 programs</summary>

| | |
|---|---|
| `bite` | a skull animation<br>**How:** Full-screen: it takes over the display. **`q' quits**. |
| `card` | Towers of Hanoi whose twelve disks are the lines of a Christmas message; VT100, wants TERMCAP |
| `life` | Conway's Game of Life<br>**How:** life [init-file]. The patterns are in /dd/GAMES/LIFE -- try `life /dd/GAMES/LIFE/glider`. It also wants more memory than the default; from the OS-9 shell that is `life #22k <file>`, and bash has no #size syntax at all. |
| `rain` | raindrops screen effect<br>**How:** Full-screen: it takes over the display. **control-C gets you out**; q, Q, control-D and ESC do not. If it has a quit command of its own, its documentation in DOC/ will say. |
| `suicide` | animation: a stick figure walks off a rooftop |
| `suicide1` | suicide, variant |
| `suicide2` | suicide, variant |
| `textb` | &#9733; Mandelbrot set drawn in ASCII on an 80x25 terminal.  Start with X -2.3, Y -2.0, range 4.0, 32 iterations<br>**How:** An ASCII Mandelbrot viewer -- it asks four questions and draws. Try X_Coord -2.3, Y_Coord -2.0, RANGE 4.0, Max Iter 32. Needs Microware's cio. |
| `ttyexp` | fireworks that clear the screen; VT100, wants TERMCAP<br>`Usage: ttyexp <parameters>` |
| `worms` | worms screen effect<br>`usage: worms [-field] [-length #] [-number #] [-trail]` |

</details>

## Amusements

*Generators, simulators and diversions that are not quite games.*

<details><summary>19 programs</summary>

**Biorhythms**

| | |
|---|---|
| `bio` | a biorhythm chart (F. Kaefer's Biorhythm V2.2e) in BASIC09 -- `runb bio' asks a Date and a Birthday as DD.MM.YYYY (RETURN at the Date prompt takes your system date), then `g' for a graph (or `v' for values) and a number of days, and plots the physical, emotional and mental cycles<br>**How:** A biorhythm chart (F. Kaefer's Biorhythm V2.2e, BASIC09) -- `runb bio' draws it. It asks a Date, then a Birthday, both as DD.MM.YYYY (dots, four-digit year, e.g. 06.09.1954; RETURN at the Date prompt takes your system date), then `g' for a graph (or `v' for values) and a number of days, and plots the physical, emotional and mental cycles. |
| `biory` | biorhythm chart, in German: asks a name (Name Vorname), a birth date as TTMMJJ and a span of years as JJ-JJ, and writes the chart -- Koerper, Seele, Geist, month by month -- to Biory.Lis in the current directory.  Needs `load /dd/CMDS/os9lib' first; RETURN at the name prompt ends it. Source: SRC/rtf/biory.f |

**Curiosities**

| | |
|---|---|
| `areacode` | &#9733; look up a US telephone area code<br>`Usage: areacode nnn nnn ...` |
| `touchtype` | TYPEFAST, a typing game: words fall down the screen and you type each one before it lands.  ESC ends the game and scores you in words per minute<br>**How:** Full-screen typing game. Answer `n' to the instructions question, pick a level 1-3 (q quits there), type each falling word followed by SPACE or RETURN. ESC ends the game and prints the words-per-minute score. |

**Generators**

| | |
|---|---|
| `name` | &#9733; invents pronounceable names, as many as you ask for<br>`Usage: name number-of-names` |
| `newsgen` | &#9733; generate a fake news bulletin |
| `pwgen` | &#9733; pronounceable passwords: `pwgen <length> [how many]'<br>**How:** pwgen <length> [count]. Give it a length and it prints that many pronounceable passwords. |
| `rndname` | &#9733; invents pronounceable names, as many as you ask for -- a second program of the same idea as `name'<br>`Usage: name number-of-names` |
| `rpoem` | &#9733; random poem generator (SNOBOL4-in-C).  Data: GAMES/SNOBOL |
| `rstory` | random story generator, roff output.  Data: GAMES/SNOBOL |
| `rstory2` | &#9733; asks your name, sex, favourite animal and colour and a setting, then hands them to a story program (rstory_W, rstory_S, rstory_C or rstory_G); supply one and it writes the story |
| `scales` | &#9733; musical scale generator -- writes `scales.lst' in the current directory<br>`Usage: scales [-h] [-d] [-a] [-m] [-c] [outname]` |
| `travesty` | rewrites its input as plausible nonsense, by Markov chains: `travesty -n400 < file' for 400 characters of it<br>`Usage: travesty [ -oord ] [ -nnum ] [ -rrand ] [ -sS ] [ -ACHUVW ]` |

**Simulated weather**

| | |
|---|---|
| `england` | &#9733; a year of random weather, day by day, for a tabletop game: the mid-Atlantic climate profile on the Gregorian calendar. `england 2' does two years.  Six builds of one program differ only in climate and calendar: england, florida (Gulf coast), georgia (south Atlantic), minnesota (north Atlantic), japan (north Pacific, Japanese calendar) and shire (mid-Atlantic, Middle-earth calendar)<br>**How:** One of six weather simulators that differ only in climate and calendar: england, florida, georgia, minnesota, japan (Japanese calendar) and shire (Middle-earth). Each prints a day's weather and stops. |
| `florida` | &#9733; the weather program on its Gulf-coast profile; see england<br>**How:** `florida < /nil'. It simulates a year of Florida weather day by day, with the calendar notes. |
| `georgia` | &#9733; the weather program on its south-Atlantic profile; see england |
| `japan` | &#9733; the weather program on its north-Pacific profile, with the months of the Japanese calendar; see england<br>**How:** A weather simulator on the Japanese calendar -- see `england'. |
| `minnesota` | &#9733; the weather program on its north-Atlantic profile; see england |
| `shire` | the weather program on its mid-Atlantic profile, with the months of Tolkien's Shire calendar; see england<br>**How:** A weather simulator using the Middle-earth calendar -- see `england'. |

</details>

## System & modules

*OS-9 module and process tools, devices, system state and scheduling.*

<details><summary>127 programs</summary>

**Devices & disks**

| | |
|---|---|
| `dam` | &#9733; display the disk allocation map -- dam [<drive>] |
| `dedit` | BASIC09 disk sector editor (Carl Kreider) -- read, edit and write raw sectors, decode a disk's identification sector.  I-CODE, not 68000 code: run it with runb and the bare module name, like bio and wysetime.  Nine modules in the one file. |
| `dinfo` | &#9733; disk/device information<br>`Syntax:   dinfo [<opts>] {<device name> [<opts>]}` |
| `dpark` | &#9733; park the DISK HEAD: `dpark [/device]' restores an RBF device's head to track 00, which is what you did before moving a drive.<br>`Syntax:   dpark [/device]` |
| `shdev` | &#9733; show devices |
| `ssl` | &#9733; show a file's segment list, sector by sector -- ssl <file> |

**Finding things**

| | |
|---|---|
| `about` | what is known about one program: what it is, what it is for, where it came from, the files it opens and whether they are here, and whether its source and documentation survived.  One card per program -- `about hack'. DOC/CATEGORIES browses; this answers. what it is for, where it came from, the files it opens and whether they are here, and whether its source and documentation survived.  One card per program -- `about hack'.  DOC/CATEGORIES browses; this answers.<br>`Usage: about <program>...` |

**Keeping and dropping**

| | |
|---|---|
| `drop` | put back exactly what keep wrote.  It refuses to remove any file whose checksum has changed, so your saves and scores are safe from it by construction.<br>`Usage: keep [-n] [-f] [-q] [-s] [-p <dir>] <program>...` |
| `keep` | take a program off this disk onto your own disk -- copies it and whatever DOC/DEPENDS says it needs, and records every file written.  `keep -n' shows what it would do without doing it.  See DOC/README-KEEP.<br>`Usage: keep [-n] [-f] [-q] [-s] [-p <dir>] <program>...` |
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
| `flink` | &#9733; list a module's links<br>**How:** DO NOT run it on a shipped module. It makes a directory entry aliasing the file's FD in the CURRENT directory, RBF has no hard links, and removing the entry leaves the file pointing at a DIRECTORY -- `cat' then answers `is a directory' for everything. |
| `gen` | generates the FRAME of a new C program -- header block, authorship and version lines and the sectioned comments a Microware example was laid out with.  It appends `.c' to whatever name you give it: `gen -p frame' leaves `frame.c'.  `-m' does a module frame, `-t' a type, `-f' a function declaration.<br>`Syntax: gen [<opt>] <pathname> [<opts>]` |
| `load` | load a module into memory, so a program that LINKS a library MODULE can find it -- `load /dd/CMDS/os9lib' and the RTF Fortran set comes alive.  A clean-room reimplementation of Microware's load, source in SRC/load, built trap-free<br>`Syntax:   load [<opts>] {<module> [<opts>]}` |
| `mexist` | &#9733; test module existence<br>`Usage: mexist [options] <Module>` |
| `os9lib` | RTF/68K FORTRAN run-time LIBRARY.  rtf, for, lnk, biory and creadoc all F$Link it, so `load' it into the module directory before running them.  See DOC/README-FORTRAN. |
| `ptxm` | Path Table eXtension Module (Nick Holgate, 1995): a KERNEL extension letting user-state processes open unlimited I/O paths.  Courtesyware, free.  It installs into the kernel and so needs supervisor state.  DOC/ptxm/ptxm.txt |
| `remove` | &#9733; REMOVE MODULES FROM MEMORY -- its own Function line says so.  `remove <module>...', -q for quiet.  `rm' removes files<br>**How:** Removes MODULES FROM MEMORY. `del', `rm' and `deldir' are the file ones. |
| `rtfdat` | RTF FORTRAN data module |
| `version` | &#9733; prints ITS OWN version and nothing else -- `Dies ist das Program 'version', Version 7' -- whatever module you name. `ident' and `modinfo' show a module's edition. |
| `vmod_trap` | the VMod_trap trap library rxmod and txmod need.  Type-$0B, and it runs in SUPERVISOR state, so it installs here and then faults.  Renamed from lowercase `vmod_trap' -- rxmod asks for `VMod_trap' and real OS-9 matches exactly and it runs in SUPERVISOR state, so it installs here and then faults.  Renamed from lowercase `vmod_trap' -- rxmod asks for `VMod_trap' and real OS-9 matches exactly |

**Processes & memory**

| | |
|---|---|
| `aprocs` | &#9733; process monitor.  It calls F$SetSys twice and is aborted (E_PRCABT) where that call is not implemented.  `procs', `top' and `sysmon' are the other process listers.<br>`Syntax: aprocs [<opts>]` |
| `edir` | &#9733; list the EVENT directory -- OS-9 events and their values<br>`Syntax: edir [<opts>]` |
| `eset` | &#9733; set an OS-9 event to a value -- eset <event> <num><br>`Syntax: eset <event> <num> [<opts>]` |
| `eunlink` | &#9733; unlink an OS-9 EVENT by name -- `eunlink <event>'.  `edir' lists the events and `eset' sets one<br>`Syntax: eunlink {<event>}` |
| `launch` | &#9733; M.C.Gregorie's login helper: reads /dd/SYS/config, sets the environment for your terminal type -- and optionally a default PATH and emacs bindings -- then starts the shell you name on its command line.  It does not put anything in the background<br>**How:** Says "nothing to launch" until it is configured -- see its documentation. |
| `signal` | &#9733; send a signal to a process<br>`Syntax: signal <process-id> <signal-code> [<seconds>]` |
| `sysmax` | &#9733; shows the system's maximum process AGE -- `system maximum age is 0' unless the kernel answers the F$SetSys call it uses. |
| `sysmin` | &#9733; shows the system's minimum process PRIORITY -- `system minimun priority is 0' here, same F$SetSys call. |
| `sysmon` | &#9733; system monitor.  It asks whether to create SYS/nodedef, times out on the keyboard and draws its Process Monitor, then takes a bus error at F$GPrDsc, the get-process- descriptor call this system does not answer -- the same gap `devprc -a' and `top' meet.  `dinfo', `map' and `space' answer the questions it would have.<br>`Syntax: sysmon [<opt>]` |
| `t` | tiny test/stub binary |
| `top` | &#9733; show the busiest processes -- prints its heading and then aborts (E_PRCABT).  `aprocs' aborts the same way<br>`Syntax: top [<opts>] [<num>]` |
| `vis` | &#9733; run a command over and over and refresh the screen with its output -- what `watch' does on other systems: `vis {opts} <command> <args>'.  Not the Unix `vis' that makes non-printing characters visible |
| `who` | 'who is logged in'.  Written in Microware shell syntax |

**Scheduling**

| | |
|---|---|
| `cron` | run commands at specified times (daemon) |
| `every` | &#9733; run a command at intervals<br>`Syntax: every <time> <progname> [<progopts>]` |
| `repeat` | repeat an OS-9 command N times -- `repeat 2 date' runs date twice.  It hands the command to $SHELL, which SYS/login sets to ksh, and ksh runs it.  date writes no trailing newline, so the repeats abut on one line.<br>`syntax: repeat [number of repetitions] [OS-9 command]` |

**System state**

| | |
|---|---|
| `clock` | display a clock |
| `oskversion` | &#9733; report the OS-9/OSK version<br>`Syntax:   OSKversion` |
| `perr` | &#9733; print an OS-9 error message<br>`Syntax: perr [<error_codes>]` |
| `setime` | Set system time.  It PROMPTS with `YYMMDDHHMMSS' and then does not set it: the clock is unchanged whether the answer comes from standard input or from six fields on the command line. |
| `sysid` | &#9733; show system identification |

**Users and login**

| | |
|---|---|
| `adduser` | &#9733; add a user to the system, for uucp logins<br>`Usage: adduser [opts] [<username> [<userid>] ]` |
| `passwd` | change your own password in /dd/SYS/password.  Matches on the user NAME, and the name must be spelt exactly as the password file has it, capitals included.  Matthias Rosenthal's, EFFO forum disk 5; source in SRC/passwd.<br>`Syntax: passwd` |

**Utilities**

| | |
|---|---|
| `add_errmsg` | &#9733; build vi's error-message file -- it wants /dd/SYS/vi_errmsg, which is here |
| `argproc_demo` | demonstration of argproc(), RICO's command-line argument parser.  Built from SRC/argproc with MEM=64k, it parses the line and prints what it made of it -- `argproc_demo readme' answers `arg=readme, b=0, c=0, sGiven=0, s=this is a test, x=32, pi=3.144500'.  A switch takes its argument with NO SPACE (`-x99', not `-x 99'), which the program says itself under -help.  The argproc library manual is here too: DOC/argproc_demo/man.argproc, from EFFO forum 7.<br>**How:** A switch takes its argument with NO SPACE: `-x99', never `-x 99'. `argproc_demo readme' prints what it made of the line. |
| `bigsetter` | Modula-2 set-operations demonstration |
| `bootlogger` | &#9733; log what happens during boot |
| `break` | send a BREAK on a serial line -- an assembler example, and it calls F$SysDbg, the system-debugger trap, on its way there.  On a machine with a debugger attached that drops you into it and waits for an answer, which in a script is a hang<br>`Syntax: break` |
| `btop` | convert characters to bit patterns -- its own Function: line, and what it does: `btop <file>' prints each character as a grid of O and space.<br>`Syntax:   BtoP [<opts>] [<path1>] [<opts>] [<path2>] [<opts>]` |
| `chardef` | define a character set -- it reads the same `dict.191' word list as `buildhash'.  Run bare it ends the os9exec session, so give it its input.<br>`Syntax: defchar [<path>]` |
| `clear` | &#9733; clear the screen<br>`Syntax:   clear` |
| `combine` | &#9733; interleave two files BYTE BY BYTE, one supplying the even bytes and the other the odd -- how a 16-bit EPROM image is put back together from two 8-bit halves.  F.R.Schmitt, 1989.<br>`Syntax: combine [<file1>] [<file2>] [<outfile>] [<opt>]` |
| `config` | report this machine's C type properties as #defines -- char, short, int, long, pointer and float all come out; it then aborts where `double' begins, because that needs a 68881 or Microware's fpu.  See DOC/README-BUSERR |
| `cpu` | &#9733; CPU speed test -- draws its bar chart and its answer (156 MHz, which is the emulator), then traps on vector $07 and takes the session down with it |
| `demerge` | split a merged file back into its parts<br>**How:** OS-9's `merge' is concatenation and there is no `merge' binary here, so `cat a b > c' makes the file demerge takes apart. There is no `od' either -- `dump' is the hex dump. |
| `demo` | egetopt option-parsing demonstration |
| `deton` | &#9733; time out an I/O read using an alarm: `deton [seconds]', an example rather than a tool.  For converting tabs, see `detab' and `expand'<br>`syntax: deton [seconds]` |
| `devprc` | show which device belongs to which process.  -h works; -a stops at F$GPrDBT (0x1f), the get-process-descriptor-block-table call, and needs a kernel that keeps one; where the call is answered without a table it is a bus error.  `top' stops in the same place, after printing its heading. |
| `dload` | &#9733; load a data file into a data module: `dload <filename>'. Nothing to do with serial downloads -- `sbreak' and `break' are the serial-line examples here<br>`Syntax: dload <filename>` |
| `e` | SEDT screen editor, the small VT220 build.  Reads SYS/sedt.keys, sedt.ruler0 and sedt.help, which ship |
| `expreserve` | &#9733; vi's crash-recovery helper: preserves an edit buffer when the editor dies.  Like ksh it reads the terminal asking for more bytes than you type (388), so it depends on the same emulator behaviour -- see DOC/README-KSH<br>**How:** Saves a vi buffer when the editor or the line dies; vi runs it for you rather than you running it. |
| `exrecover` | &#9733; recover a vi buffer that expreserve saved<br>**How:** Recovers what expreserve saved. Again, vi's helper rather than a command you start. |
| `fastcc` | &#9733; a faster front end for cc |
| `fixyear` | Y2K: correct a date the clock got wrong<br>`Usage: fixyear [-opt] <file\|dir> <dir\|file> [-opt]` |
| `fontgen` | generate a font for the Gepard display<br>**How:** Generates a character font for the Gepard display -- it prints the assembler source of an 80-column font on stdout. |
| `getsys` | &#9733; report the system's globals -- what OS-9 thinks it is running on<br>`Syntax: getsys [<opts>]` |
| `ggrep` | &#9733; GNU grep, from the sh_utils collection<br>**How:** GNU grep. `ggrep <expr> <files...>'; -E, -F, -i, -v, -w and the rest as you would expect. |
| `greg` | &#9733; converts a Julian day number to a Gregorian date: `greg 2461281' is the 29th of August 2026<br>**How:** It converts a JULIAN DAY NUMBER to a Gregorian date and is nothing to do with regular expressions: `greg 2460000' answers `2023 2 25'. |
| `hinterhalt` | &#9733; a small game (EFFO forum 7) |
| `i_am_i` | prints its own source (Pascal) |
| `isam` | &#9733; indexed-sequential file demonstration |
| `lfmaker` | make a G-Windows launch file -- and it asks the allocator for an ADDRESS as if it were a length, so the request is refused: `2470464192-byte request refused, 32682944 bytes free'.  The number MOVES with the environment, which is what identifies it as an address.  It happens only once the module is already resident: run it bare first, then with an argument. |
| `lgrep` | &#9733; list the files a pattern appears in -- its banner says "same as 'grep -l', but prints filenames without comments". `grep -l' does the same job here.  DOC/README-GREP compares the six searchers<br>`Syntax: lgrep <arg1> ... <argn>` |
| `liborder.os9` | report the order of modules in a library<br>`Usage: liborder <options> file1.r file2.r ...` |
| `makecrc` | GENERATE C SOURCE for CRC tables.  It takes no arguments: run it somewhere writable and it writes six files into the data directory -- arc.c, binhex.c, ccitt.c, ccitt32.c, kermit.c and zip.c -- each holding a crctab[256] and an updcrc() for one polynomial.  It writes them without a message, so list the directory afterwards.  For a CRC of a file, `chksum' does that<br>**How:** It GENERATES C SOURCE and takes no arguments. Run it somewhere writable (`ksh -c "cd /dd/tmp; makecrc"') and it writes six files -- arc.c, binhex.c, ccitt.c, ccitt32.c, kermit.c, zip.c -- each a crctab[256] and an updcrc(). It writes them without a message, so list the directory afterwards. |
| `map` | &#9733; show the disk blocks a file occupies, sector by sector: `map <file>', or `map -e <file>' for the extended form. For memory rather than disk, see `mfree' and `free'<br>`Syntax: map [<opts>] <file> {<file>}` |
| `modinfo` | report a module's header -- name, type, size, edition, CRC<br>`Syntax:   module [modulename]` |
| `mvolformat` | format a multi-volume set<br>`Syntax: mvolformat drive volname volcount [format options]` |
| `names` | &#9733; list the names of modules in a file.  It can hang on some inputs; `ident', `modinfo' and `module_census' answer the same question. |
| `phone` | connect two terminals<br>`Syntax: phone <communication-path>` |
| `preset` | LOAD THE TERMINAL'S FUNCTION KEYS: it writes a fixed set of definitions -- `dir', `umacs', `r68', `l68', `dsave -ieb128k' and so on -- and answers `Funktionstasten belegt!'.  German, from forum3.  It takes no arguments and ignores any given. |
| `pri` | change a process's priority: `pri <pid> <priority>'. |
| `ptob` | convert bit patterns back to characters -- the other half of `btop', and the round trip is exact.<br>`Syntax:   PtoB [<opts>] [<path1>] [<opts>] [<path2>] [<opts>]` |
| `ptxminst` | install Ptxm -- the kernel extension above |
| `rndir` | &#9733; convert directory NAMES between upper and lower case -- its own Function: line is "rename directory names in big/small characters".  `-l' for small, `-q' to work silently.<br>`Syntax: rndir [<opt>]` |
| `screen` | &#9733; Russ Smith's `screens': picks a file at random from $HOME/.SCREENS and shows it -- a login greeting.  On OS-9 it RUNS the file rather than printing it, through system(), so it wants Microware's `shell' on your execution path.  Not the terminal multiplexer of the same name.  Source in SRC/screen, man page in DOC/screen/screens.6 |
| `screen_nocio` | a trap-free source build; CMDS/screen uses cio and this one does not |
| `scsiutil` | SCSI device utility<br>`Usage: SCSIutil [/scsi_dev@] <command>` |
| `setime2` | Y2K: set the system time, four-digit year<br>`Syntax:   setime2 [<opt>] [<setime2>] [<opt>]` |
| `setyear` | Y2K: set the year directly<br>`Syntax:   setyear <YYYY>` |
| `snd_sig` | &#9733; send a signal to a process<br>`Syntax:   snd_sig [-options] pid pid1...pidn` |
| `spline` | &#9733; fit a spline through points, output PostScript |
| `sqrtx` | square-root demonstration |
| `suse` | show a program's usage line.  `-?' does the same for most programs here. |
| `suspend` | &#9733; REMOVES a process from the system -- its own usage line says so -- rather than suspending it.  F.R.Schmitt, 1989.<br>`Syntax  : suspend  [<processname>]  [<opt>]` |
| `t_trtest` | RICO trap-handler test |
| `testibc` | IEEE-488 (GPIB) bus test program, B & K Denmark, 1989. Answer its `Timeout time (1/10 Sec)?' prompt and it draws a full command menu: Ifc, Remote, Llo, Goto local, Clear, Send, Enter, Dev-clear, Time, Quit.  Each command needs an IEEE-488 bus to reach.  It reads its messages from /dd/sys/errmsg.ibc. |
| `transfer` | &#9733; copies files from GDOS DISKS to OS-9, and takes no options at all.  For general device-to-device copies, `cp', `copy' and `dsave' do that.<br>`Syntax: transfer` |
| `trunc` | &#9733; truncate a file to a given length<br>`Syntax: trunc <path> <num>` |
| `tty` | &#9733; report the terminal's name |
| `umusek` | UMusEK -- a music editor.  It needs a hardware graphics screen: point it at one and it opens.  Without a graphics screen it stops with `***DS_ScAdd Error 208.' and `Fran: Can't get screen addr, 'bye!'. |
| `unpacklib.os9` | unpack a library into its object modules<br>`Usage: unpacklib <options> file1.l file2.l ...` |
| `vc` | &#9733; a SPREADSHEET -- `Welcome to the Spreadsheet Calculator, type ? for help', with rows, columns and a formula line |
| `vecho` | System V `echo': the newline is suppressed by a trailing \c IN THE ARGUMENT, not by default.  `vecho one' writes `one' and a CR; `vecho one\c' writes `one' and stops. Several arguments are joined with a space.  SRC/less_v177 |
| `vlen` | &#9733; a VARIABLE-LENGTH RECORD demonstration: it ignores whatever you give it, creates a filesystem of its own, adds a hundred records of varying length and prints the minimum, the maximum and the mapper entries as it goes.  `isam' is the other demonstration of its kind here.  IT LEAVES ITS STORE BEHIND, in the DATA directory, as `test.mp' and `test.st' -- run it twice and the second run answers `Filesystem already exists.' and adds nothing.  Delete those two to run it again.<br>**How:** It leaves its store behind, in the DATA directory, as `test.mp' and `test.st'. Run it twice and the second run says `Filesystem already exists.' and adds nothing; delete those two to run it again. |
| `what` | inventory the expansion cards in a GEPARD -- the German 68k machine much of the EFFO material was written on.  It prints `What's where in the GEPARD:' and a table of I/O address, reference byte and card name, empty on anything else.  It ignores its arguments.<br>**How:** An inventory tool for the GEPARD, the German 68k machine: it prints "What's where in the GEPARD:" and a table of expansion cards. On other hardware the table is empty, and it ignores its arguments. |
| `xlharc` | extract LHarc archives<br>`Usage: xlharc {axevlufdmctp}[qnftv] archive_file [files or directories...]` |
| `yagi` | Yagi antenna design calculator, to DL6WU's method.  It asks FIVE questions on standard input -- frequency, element count, boom diameter, insulated from the boom Y/N, and a tubing size off its own list -- and prints element lengths and spacings.  Answer four and it loops on the fifth<br>**How:** It asks FIVE questions on standard input -- centre frequency in MHz, element count, boom diameter, whether the elements are insulated from the boom (Y/N), and a tubing size off its own list of six. Answer four and it loops on the fifth forever, because EOF on a numeric read returns the same thing every time. |
| `ynad` | &#9733; YNAD -- Yet Another Name & Address program.  A contact database. |

**Vendor demos**

| | |
|---|---|
| `ob68kdemo` | OmniBasic 1.16 -- a BASIC compiler.  Limited symbol table; otherwise the including compiler.  Run it from /dd/DOC/omnibasic, where its library and examples are. Like UniBasic it needs Microware's cc to finish a build<br>**How:** OmniBasic 1.16, same arrangement as ub68kdemo and the same SHELL trick -- see its entry. Run it from /dd/DOC/omnibasic. DEMO VERSION, capped symbol table. |
| `sddemo` | White's Speedisk 2.10 -- disk de-fragmenter.  Wants an 80x24 screen; falls back to tty mode<br>**How:** White's Speedisk 2.10 de-fragmenter, demo build. Wants an 80x24 screen and drops to tty mode without one. |
| `ub68020demo` | UniBasic 1.10 for the 68020 -- the same demonstration as `ub68kdemo' and it runs the same way, announcing `OS9/68020 Version' where the other says 68000. |
| `ub68kdemo` | UniBasic 1.10 -- a BASIC compiler, same arrangement as OmniBasic.  Run it from /dd/DOC/unibasic<br>**How:** UniBasic 1.10, and it does compile -- the trick is that it runs its build through $SHELL. With SHELL unset it hunts for `/dd/bash' and dies with "Error Exit" and error 216. Do `setenv SHELL /dd/CMDS/sh', work in a directory holding basic.h and basic.l (DOC/unibasic has them), have your C toolchain reachable with CDEF and CLIB set, and give it memory. DEMO VERSION: the symbol table is capped, nothing else is. |

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

<details><summary>13 programs</summary>

**Astronomy**

| | |
|---|---|
| `ephem` | &#9733; ephem - astronomical ephemeris<br>**How:** An astronomical ephemeris: `ephem -c /dd/SYS/ephem.cfg -d /dd/SYS/ephem.db'. RETURN passes the opening page; any key stops the loop; ? is help; control-D quits. |
| `ephem881` | &#9733; ephem, 68881 build<br>**How:** The same as ephem, built for a 68881 coprocessor. Control-D quits. |
| `lunisolar` | &#9733; lunar and solar position calculator |
| `nasa` | &#9733; NASA orbital-element reader.  Wants `nasa.dat' in the CURRENT directory: NORAD two-line element sets -- a name line, then TLE line 1 and line 2 per satellite -- and writes kepler.dat. No element set ships here; supply a current one.  The format is parsed in SRC/eff_orbit/nasa.c and is column-sensitive<br>**How:** Put NASA two-line elements in nasa.dat in the current directory and run `nasa'; it writes kepler.dat, which `orbit' reads. No element set ships; they are published for every satellite. |
| `orbit` | &#9733; the N3EMO satellite tracker, version 3.7: where a satellite is from a site, hour by hour -- azimuth, elevation, doppler, range and transponder mode.  It opens kepler.dat, mode.dat and a <site>.sit by bare name from the current directory, and DOC/orbit holds them (pgh, bern and zuerich sites), so run it from there: `chd /dd/DOC/orbit' and `orbit', or under bash `ksh -c "cd /dd/DOC/orbit; orbit"'.  `nasa' makes a kepler.dat from published two-line elements<br>**How:** It reads kepler.dat, mode.dat and a <site>.sit by bare name from the current directory, and DOC/orbit holds them: `ksh -c "cd /dd/DOC/orbit; orbit"'. Answer d for a day's table, then the site (pgh), the date, the start hour, the step and the length. |

**Calendars**

| | |
|---|---|
| `cal` | &#9733; Calendar, Bob van der Poel.  `cal -h' prints holidays with it -- SYS/holidays is here, and SYS/birthdays is an empty template for your own dates.  SYS/cal.init is a printer setup for a laser<br>**How:** `cal -m=<month> -y=<year>', with flags. -h marks the holidays in SYS/holidays and anything you add to SYS/birthdays, which it includes. |
| `calen` | calendar printer (v_misc) |
| `calender` | &#9733; print a whole year's calendar (German)<br>**How:** A whole year at once, in German. It asks `Fuer welches Jahr?' (which year); RETURN at the question ends it. |
| `qt` | &#9733; tells the time in words, the way a person would say it: `It's just gone ten past four.' |
| `setimex` | &#9733; set time from hardware clock<br>`Usage:` |
| `today` | date, moon phase and this-day-in-history |

**Clocks**

| | |
|---|---|
| `digclk` | &#9733; digital clock with hostname<br>`Usage: digclk [refresh_rate]` |
| `gcl` | &#9733; a grand digital clock: the time drawn large across the terminal and redrawn as it runs.  `-n=<seconds>' runs it for that long; -s scrolls the digits, -i inverts the video<br>**How:** A full-screen digital clock: `gcl' runs until stopped, `gcl -n=10' for ten seconds; -s scrolls the digits, -i inverts the video. |

</details>

## Maths & calculators

*Calculators, plotting, orbits and number theory.*

<details><summary>11 programs</summary>

**Calculators**

| | |
|---|---|
| `cam` | &#9733; CAMSHAFT, not camera: it asks for the rocker ratio, the lift at a crank angle and the base circle, and plots the lift curve for an intake lobe.  The plot is Tektronix vectors, so on a vt100 it arrives as characters -- the dialogue above it is the readable part. |
| `chbase` | &#9733; converts a number from one base to another: `chbase 255 10 16' prints FF, and a target base of 0 prints every base from 2 to 36<br>`Syntax   : chbase <number> [ <base A> [ <base B> ] ]` |
| `cvtbase` | converts a number between bases.  The bases are named by key -- b, d, h or x, o -- or by their value, and the number comes on standard input: `echo 255 ! cvtbase d h' answers ff<br>**How:** The BASES are the arguments and the NUMBER comes on standard input: `echo 255 ! cvtbase d h' answers ff, `cvtbase d b' answers 11111111. Bases are named b, d, h or x, o -- or by their actual digit characters. |
| `loan` | &#9733; amortisation calculator: principal, term, rate and start month in, the payment and a month-by-month schedule out |
| `rechne` | &#9733; calculator, German -- and it takes ONE expression with no spaces in it: `rechne 4095+1' answers 4096, $1000 and the binary.  Spaced out it evaluates each argument separately |
| `rpn` | &#9733; RPN calculator -- and its `+' is wrong: 12, 34, + leaves a stack of three with 0 on top instead of one with 46. `rechne' is the calculator that answers correctly |
| `sc` | sc -- spreadsheet calculator (needs TERM)<br>**How:** The spreadsheet, version 6.16. `sc' opens and says "Type '?' for help". It reads TERMCAP as SYS/login sets it, so no `. /dd/SYS/termcap.entry' is needed first. |

**Simulators**

| | |
|---|---|
| `logisim` | logic circuit simulator -- draws a pulse diagram from a circuit written as text.  Two sample circuits ship with it, DOC/logisim/flipflop.lsi and counter.lsi, and its notes are DOC/logisim/logisim.doc, in German.  It needs `PORT' set to a terminal path -- it reopens the keyboard through it, so `setenv PORT /term' first.  Past that it floods `No more memory !!!'.<br>**How:** Set PORT first: `setenv PORT /term'. Without it, `logisim: Environment variable PORT not defined' -- it reopens the keyboard through that path. Two sample circuits ship in DOC/logisim (counter.lsi, flipflop.lsi) and its notes are there too, in German. |

**Spreadsheets**

| | |
|---|---|
| `checkfile` | &#9733; a CHEQUE BOOK -- a full-screen account manager, John R. Wainwright, 1992.  Records carry Date, Type, Description, Account and Amount; the menu is A - Add Records, B - Print Balance, R - Report, F - Select File, V - View/Edit, Q - Quit, and it opens `testfile.dat' unless you pick another.  Wants TERM.  For checking C source, that is `ccheck'<br>**How:** Full-screen: it takes over the display. **`q' quits**. |
| `oleo` | GNU Oleo 1.6, a spreadsheet.  `sc' is the spreadsheet on this disk that runs; Oleo stops with an illegal instruction at 000465d2 before it draws a cell.<br>**How:** GNU Oleo, a spreadsheet. `sc' is the spreadsheet on this disk that runs; Oleo stops with an illegal instruction (0009, E_PRCABT), from a full login session as much as from a bare shell. |
| `scqref` | &#9733; Quick reference for sc, the spreadsheet on this disk |

</details>

## Printing

*Spoolers, page formatting and PostScript.*

<details><summary>15 programs</summary>

**PostScript**

| | |
|---|---|
| `gs33` | Ghostscript 3.33 -- the older one.  gs403 ships with its init files and fonts; use that<br>`Usage: gs ... -%c file.ps arg1 ... argn` |
| `gs403` | Aladdin Ghostscript 4.03, and this one is COMPLETE: its init files and fonts are in LIB/gs403.  Point GS_LIB at that directory and it interprets -- `export GS_LIB=/dd/LIB/gs403' in bash, NOT `setenv', which is the OS-9 shell's and is not a bash command.  It then reads a PostScript file and drops to its own `GS>' prompt.  Runs with no trap handler -- built with GCC 2.5.8 by its porter.<br>**How:** Aladdin Ghostscript 4.03. Point GS_LIB at its library first -- in bash that is `export GS_LIB=/dd/LIB/gs403`, NOT `setenv`, which is the OS-9 shell's command and gets "setenv: command not found" here. Then `gs403 -q -dNOPAUSE -sDEVICE=nullpage <file>.ps` reads the file and gives you its GS> prompt. Everything it needs, fonts included, is in that directory. gs403 is the complete build; gs33 is the older one. |
| `lwf` | ASCII to PostScript, like Unix enscript.  Reads its prologue from /dd/USR/LIB/lwf.prologue<br>**How:** Turns plain text into PostScript, the way Unix enscript does. It reads /dd/USR/LIB/lwf.prologue and stops without it. No PostScript printer here, so send the output to a file and take it elsewhere. |

**Printers**

| | |
|---|---|
| `alps` | &#9733; Switch an ALPS ASP-1000 printer between draft and NLQ<br>`Syntax: alps [<opts>] >/<device>` |
| `epson` | &#9733; spline output driver for an Epson printer<br>`usage: epson [<opts>]` |
| `lmargin` | &#9733; set the left margin ON AN EPSON PRINTER -- its own usage line says `epson'.  For indenting text, see `fmt', `proff' and `pep'.<br>`usage: epson [<opts>]` |

**Spooling**

| | |
|---|---|
| `lp` | &#9733; line printer spooler - submit a job<br>`Syntax: lp [<opts>] {<path>}` |
| `lpq` | &#9733; shows the spooler queue.  It looks for a DATA MODULE called `spoolqueue' in memory; with a spooler running it reports the queue, and without one answers `no spooler installed'.  Same for `prjob' and `lp'.<br>`Syntax: lpq [-p=dev] [user]` |
| `lprm` | &#9733; remove a job from the print queue<br>`Syntax: lprm [-d=dev] [-] job..` |
| `lpsched` | &#9733; the line-printer scheduler<br>`Syntax: lpsched [-r] {<devname>}` |
| `lpshut` | &#9733; shut down the printer scheduler<br>`Syntax: lpshut` |
| `prjob` | &#9733; print a job |
| `splman` | &#9733; OS-9 print spooler: the manager (Carl Kreider).  It wants a printer on an SCF device to spool to.  `splprt' is the process that drives the printer and `splstat' shows the queue; the three go together |
| `splprt` | &#9733; OS-9 print spooler: the printer process, one per printer. It wants an SCF device to write to |
| `splstat` | &#9733; OS-9 print spooler: queue status.  It reads the spooler's queue.  The other spooler on this disk speaks up when its queue is empty: `lpq: no spooler installed', `lpshut: no spooler active', `prjob: Spooler not installed'. |

</details>

## Documentation

*Pagers, readers and the help system.*

<details><summary>5 programs</summary>

| | |
|---|---|
| `help` | help system<br>`Syntax:   help [<opts>] [<topic> {<subtopic>}] [<opts>]` |
| `helpindex` | &#9733; builds the .ndx index a .hlp help file needs: `helpindex dinfo.hlp' writes dinfo.ndx beside it<br>**How:** `helpindex dinfo.hlp' writes dinfo.ndx beside it. Only names ending .hlp or .hlib are accepted unless -a is given; with no name it asks for one. |
| `less` | Pager (wants a real TERM).  Its help screen works now: SYS/less.hlp is on the disk |
| `lessecho` | &#9733; prints its arguments back quoted for a shell -- the helper less uses to hand file names on<br>`usage: lessecho [-ox] [-cx] [-pn] [-dn] [-a] file ...` |
| `lesskey` | turns a key-binding file into the binary less reads: a `#command' section, then one key and one command per line<br>`usage: lesskey [-o output] [input]` |

</details>

---

&#9733; marks a program that uses Microware's `cio`, which ships on the disk, included with Microware's permission; `DOC/README-CIO` has the details.

Generated by `tools/gen_catalog.py` from the disk's own documents. Do not edit by hand; it will be overwritten.
