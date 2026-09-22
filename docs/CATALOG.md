# What is on this disk

1028 programs of OS-9/68K community software, gathered from the archives that kept it and made to run again. **709 of them need nothing but this disk**; the rest want Microware's `cio`, marked below with a star.

`DOC/INDEX` on the disk lists everything alphabetically. This is the same collection sorted by what each program is *for*, which is the more useful order when you do not yet know what you are looking for.

> Open a program in `docs/index.html` for its **sample output** --
> captured from that program running on the disk image.
>
> Prefer to click around? `docs/index.html` is a searchable version with per-program detail — what it needs, where it came from, on what terms. GitHub will not render it here; download the repository and open it, or enable Pages.

| Category | Programs | |
|---|--:|---|
| [Shells](#shells) | 24 | Unix shells to sit beside OS-9's own -- bash and ksh bring history, job control, and scripts that come across unchanged. |
| [Editors](#editors) | 21 | vi and emacs in several flavours, line and stream editors, and editors for binary and hex. |
| [Text tools](#text-tools) | 137 | Search, sort, compare, reformat, split and spell-check. |
| [Files & directories](#files--directories) | 37 | Listing, copying, finding, renaming, and knowing what you have. |
| [Developer tools](#developer-tools) | 36 | Version control, tags, cross-reference, formatters, a debugger and benchmarks. |
| [Compilers & build](#compilers--build) | 39 | C compilers and their passes, assemblers, linkers, make and parser generators. |
| [Languages](#languages) | 16 | Interpreters and language systems beyond C. |
| [Archives & compression](#archives--compression) | 33 | Pack, unpack and shrink -- lha, zip, tar, arc, zoo, and OS-9 module libraries. |
| [Encoding & conversion](#encoding--conversion) | 30 | Between text encodings, line endings, Macintosh formats, ciphers and hashes. |
| [Communications](#communications) | 96 | Kermit in several builds, terminal sessions, and networking. |
| [Graphics & images](#graphics--images) | 195 | The netpbm toolkit, JPEG, a ray tracer, and things that draw. |
| [Games](#games) | 112 | Adventures, board and card games, arcade ports, dungeon crawls and puzzles. |
| [Screen toys](#screen-toys) | 10 | Animations and screen effects -- they draw on the terminal rather than print to it. Some run until you stop them. |
| [Amusements](#amusements) | 32 | Generators, simulators and diversions that are not quite games. |
| [System & modules](#system--modules) | 118 | OS-9 module and process tools, devices, system state and scheduling. |
| [Disk & DOS](#disk--dos) | 20 | Reading and writing MS-DOS media with the mtools set. |
| [Time & calendar](#time--calendar) | 18 | Calendars, clocks and astronomy. |
| [Maths & calculators](#maths--calculators) | 19 | Calculators, plotting, orbits and number theory. |
| [Printing](#printing) | 11 | Spoolers, page formatting and PostScript. |
| [Documentation](#documentation) | 6 | Pagers, readers and the help system. |
| [G-Windows](#g-windows) | 6 | Programs for G-Windows, OS-9's graphical display.  There is no G-Windows here, so what their cards show is each one declining in its own words -- `Unable to access "/win" device', `dclock only runs under G-Windows', a status of 208 or 221.  None of them can be exercised without the display; they are listed for a real OS-9 workstation that has it. |
| [Needs hardware](#needs-hardware) | 12 | Programs that drive hardware this collection has no way to reach -- a graphics display of the kind a GEPARD or an MM/1 carries, or a printer on its own SCF device.  WE CANNOT TEST ANY OF THESE, at all: what is written about them comes from their own text and their code, not from watching them work.  They are here for a real machine that has the hardware. |

## Shells

*Unix shells to sit beside OS-9's own -- bash and ksh bring history, job control, and scripts that come across unchanged.*

<details><summary>24 programs</summary>

**Shell helpers**

| | |
|---|---|
| `checkenv` | &#9733; compares an environment variable with a value for a script to branch on: `checkenv <name> , <value>', spaces round the comma.  It returns 0 whether the value matches or not, so `getenv -p <name>', which prints the value, is the one to use for a reliable branch<br>**How:** `checkenv <name> , <value>' with spaces round the comma. Meant to return an error when they differ; it returns 0 either way. |
| `exist` | &#9733; test whether a file exists and answer in the exit status: 0 if it does, 1 if it does not, which is what a script wants.  -n inverts the test, -d asks whether the name is a directory.  German: its help is headed `Aufruf' and `Rueckgabewerte'.  DESIGNA VLT, version UTIL 2.40<br>`EXIST    Version UTIL 2.40 by DESIGNA VLT 24.11.97` |
| `getenv` | &#9733; print or test an environment variable.  German prompts: `getenv -p TERM' prints the value with a newline, -l without one, -x exits with it, -n inverts the test.  Bare, or with a name and no option, it prints its own usage.  DESIGNA VLT, version UTIL 2.40<br>`GETENV   Version UTIL 2.40 by DESIGNA VLT 24.11.97` |
| `hist` | a command-line editor with C-shell-style history in front of Microware's shell: `h' lists it, `logout' leaves.  Name a history file; the default is on the RAM disk /r0 [no military use -- EFFO-INFO]<br>**How:** A command-line editor with C-shell-style history in front of Microware's shell, which runs each command it is given; load your own OS-9's `shell' and `tmode' first. `hist <file>' keeps the history in that file (the default is /r0/history, on a RAM disk: `mount -r=256k /r0'); `h' lists it and `logout' leaves. |
| `if` | conditional execution for a shell script: `if def <var>', `if loaded <module>' or `if varval <var> <value>', the commands, `else', `endif'.  It hands the branch to Microware's `shell' to run<br>**How:** bash's own `if' is a reserved word; `command if' reaches the one on this disk. |
| `printenv` | &#9733; print the environment Shares its name with a utility of your own -- README-NAMES<br>`**** PRINTENV Utility for use with ZSH, (c) 1989 by L.Zeller ****` |
| `printf` | formatted print from the shell, as on Unix: widths, numbers and floating point<br>**How:** printf as on Unix: `printf "%-8s\|%5d\n" name 12'. Widths, numbers and floating point all work. |
| `qp` | &#9733; expands back-quotes in a command line, which Microware's shell does not do for itself: `qp <cmd> <args>'. It forks a `shell' to run the result, so it wants Microware's on your execution path<br>**How:** Hands its expanded command to $SHELL with the options `-ny -nl', which belong to the EFFO shell it was written for; no shell here takes them, your own OS-9's included, so here it expands nothing. |
| `run` | runs a program with its input and output on the terminal PORT names: `run '<program> <args>''<br>**How:** `run '<program> <args>'' with PORT naming a terminal: the program runs with its input and output on that terminal. |
| `submit` | &#9733; runs the commands in a .sub file one after another, printing each line before it runs it -- a batch job. The file is named without its suffix, `submit demo' for demo.sub. Every line goes to `shell', so your own OS-9's shell has to be resident; SYS/login loads it from /h1<br>`Syntax: submit [<opts>] [<submit file>] [{<parameter>)]` |
| `xargs` | builds command lines out of what it reads and runs them: `ls \| xargs cat' hands the names to cat as arguments rather than as input |
| `xc` | runs the commands marked in a file -- a line beginning `% ' -- and leaves the rest as notes.  Forks them through Microware's `shell' to run<br>**How:** `xc <file>': lines beginning `% ' are commands, shown and run; `$ ' runs them quietly; the rest is notes. It forks them through Microware's `shell', which must be loaded (`load /h1/CMDS/shell'). |
| `yes` | prints `y', or the words it is given, over and over until the program reading it stops -- for answering prompts |

**Shell utilities**

| | |
|---|---|
| `env` | &#9733; GNU env: runs a command with variables added to its environment, `env FOO=bar printenv'<br>`Usage: env [OPTION]... [-] [NAME=VALUE]... [COMMAND [ARG]...]` |
| `expr` | &#9733; GNU expr: evaluates an expression for a script -- arithmetic, comparisons, string length and matching |
| `logname` | &#9733; prints the login name the password file gives for the number your process actually runs as -- which is not necessarily $USER: logged in here it answers `su' where $USER says `tester'. GNU's<br>`Usage: logname [OPTION]...` |
| `su` | &#9733; GNU su: become another user; its options are under `su --help' Shares its name with a utility of your own -- README-NAMES<br>`Usage: su [OPTION]... [-] [USER [ARG]...]` |
| `whoami` | &#9733; prints who you are running as, the same answer `logname' gives and for the same reason: it reads the process's owner number and looks it up, where $USER is only what the environment was told. GNU's, and the same as `id -un'<br>`Usage: whoami [OPTION]...` |

**Shells**

| | |
|---|---|
| `bash` | GNU Bourne-Again Shell 1.12 -- this disk's shell; it reads .bashrc. It cannot serve as $SHELL for a program that shells out, because it reads system()'s command line as a script file name; `ksh' can, and SYS/login sets SHELL to it. DOC/README-SHELLS compares all five |
| `gshell` | GSHELL V1.1 -- a full-screen menu, not a command shell: a lettered list of the directory, `+' and `-' to page, `.' to change directory, a letter to run a file. `assembler', `compiler' and `editor' are the same engine pointed at one job each. DOC/README-SHELLS<br>**How:** A full-screen menu of the current directory: + and - page, . changes directory, a letter runs that file. Control-C leaves it. |
| `ksh` | &#9733; the Korn shell, pd-ksh: a full shell with a prompt, history, for loops, variables and functions, and `ksh -c '<commands>'' runs a line. It is the shell programs on this disk shell out through. DOC/README-KSH |
| `mshell` | &#9733; a menu shell: `mshell <menufile>' shows one numbered entry per `label\| command' line and a number runs that command -- through Microware's `shell' Shares its name with a utility of your own -- README-NAMES<br>**How:** `mshell <menufile>': one `label\| command' per line, up to ten. A number picks an entry; it hands the command to Microware's `shell', which must be loaded, then waits for RETURN. Control-C leaves it. |
| `sh` | Bourne shell v7.5 -- what the startup script runs. It has a real `chd' where bash does not, and it cannot fork a program by absolute pathname here, which is the trade.  See DOC/README-SHELLS<br>`Syntax: sh [<opts>] [<scriptfile>] [<arg1>] ... [<argn>]` |
| `wish` | WiSH, a full-screen windowing shell over the OS-9 shell: a file window to move about in and a command line at the top. The labelled keys are terminal function keys; the control keys always work, Ctrl-D to leave.  German-made, English at the keyboard.  Not the hack toy of the same name in GAMES<br>**How:** WiSH, a windowing shell over the OS-9 shell. Type a command on the top line (`ls', `dir', anything), Enter runs it through the OS-9 shell and pages the output -- press Enter again to return to the window. The labelled keys along the foot are terminal function keys a vt100 does not send; the control keys always work: Ctrl-P/N/B/F move the cursor over the file window, Tab moves right, Ctrl-A marks the file under the cursor, Ctrl-U unmarks all, Ctrl-W copies the cursor's name onto the command line, Ctrl-L redraws, Ctrl-V/Ctrl-Z page. **Ctrl-D leaves.** German program, English at the keyboard. (hackwish, in GAMES, is the unrelated hack cheat.) |

</details>

## Editors

*vi and emacs in several flavours, line and stream editors, and editors for binary and hex.*

<details><summary>21 programs</summary>

**Alternates**

| | |
|---|---|
| `sed_1.06` | &#9733; a second build of sed, kept under its version number; the same substitutions<br>`Syntax   : sed [<opts>] [<file>]` |

**Binary & hex**

| | |
|---|---|
| `beav` | BEAV 1.40 -- Binary Editor And Viewer (needs TERM)<br>**How:** Full-screen binary editor: `beav <file>'. Control-C leaves it. |
| `hexed` | a hex editor made of your text editor: it writes the file out as a hex dump, opens that in the editor `-e=' names (default vi), and writes the file back when you leave. `-t=<dir>' says where the dump goes; without it, /r0 [no military use -- EFFO-INFO]<br>**How:** `hexed -t=<dir> -e=<editor> <file>': the file goes out as a hex dump into <dir>, the editor opens it, and leaving the editor writes the file back. Without -t it uses /r0. |
| `hexedit` | HEXPERT V2.4, a hex viewer and editor: `hexedit <file>'. It reads TERMCAP as the capability string itself, not as the name of a file, so source `. /dd/SYS/termcap.entry' first and it draws its viewer; without that it prints the terminal type and exits. Its -d option reports `file not accessible' for a file that is readable<br>**How:** `hexedit <file>'. Put the termcap entry in TERMCAP first (`. /dd/SYS/termcap.entry') or it will not draw. |
| `pbyte` | &#9733; patch bytes in a file at a hex offset<br>`Syntax: pbyte <path> <hex_offset> <hex_byte> [<hex_byte>]` |

**emacs family**

| | |
|---|---|
| `em` | MicroEMACS 3.8b, a screen editor with Emacs keys<br>**How:** A screen editor. It stops with "Environment variable TERM not defined!" unless TERM is set -- SYS/login sets it, so run it from a login shell rather than bare. |
| `emacs` | &#9733; MicroEMACS 4.00, a full-screen editor with Emacs keys and a macro language; its macros and help are in USR/LIB/EMACS.<br>**How:** Full-screen editor, MicroEMACS keys. Control-X control-C quits. Its macros and help are in USR/LIB/EMACS. |
| `me` | MicroEMACS 3.11, a screen editor with Emacs keys and German messages (Datei for File); needs TERM set<br>**How:** Full-screen editor, MicroEMACS keys, German messages. Control-X control-C quits. |
| `mg` | &#9733; Mg, a small MicroGnuEmacs -- Emacs keys in 79K, its documentation under DOC/mg.<br>**How:** Full-screen editor, Emacs keys. Control-X control-C quits. |
| `umacs` | &#9733; uMacs 1.0, MicroEMACS in 45K -- the same keys, no macro language Shares its name with a utility of your own -- README-NAMES<br>**How:** A small Emacs (uMacs 1.0). Full-screen: it takes the display and shows "== uMacs 1.0 == main ==" at the foot. It needs only TERM set. |

**Line & stream**

| | |
|---|---|
| `ed` | &#9733; GNU ed 0.2, the line editor.  It keeps its scratch file on /r0, a RAM disk, so mount one (`mount -r=256k /r0'); DOC/README-RUNNING has the details<br>**How:** Needs a /r0 RAM disk for its scratch file; `mount -r=256k /r0' provides one. Then `ed <file>', with ed's usual commands: 1,4p prints, s/a/b/ substitutes, w writes, q quits. |
| `editor` | a full-screen file picker that hands the file you choose to `umacs': a lettered list of the directory, `+' and `-' to page, `.' to change directory.  Run it bare; given a path on the command line it stops on an illegal instruction. `gshell' and `assembler' are the same menu in front of other programs.<br>**How:** Run it bare: a full-screen file picker for umacs. Given a file on the command line it stops on an illegal instruction. Control-C leaves the menu. |
| `sed` | &#9733; sed, the stream editor: substitutes, deletes and prints, with -n for no default output, -e for a script line and -f for a script file<br>`Syntax   : sed [<opts>] [<file>]` |

**vi clones**

| | |
|---|---|
| `elvis` | Elvis 1.7, a full vi and ex clone -- the best-documented of this disk's three vi editors and the one with the most options, its source in CMDS/archives and its manual under DOC/elvis. Needs TERM and TERMCAP. It also appears as view (read-only) and as REBUILT/vi.elvis, both of which run elvis. It wants a /dd/tmp for its scratch file, a path compiled in: without that directory it stops before drawing, with `Can't create temp file...'. This disk ships one, so it bites only on a /dd you copy it to; `makdir /dd/tmp', or `setenv EXINIT "set directory=<a dir you have>"' before starting it, cures that. DOC/README-VI compares the three.<br>**How:** A full vi/ex clone. Needs TERM and TERMCAP set -- `SYS/login' does both. `view' opens read-only, REBUILT/vi.elvis is the same program as vi, and all of them exec CMDS/elvis, so it must be present. |
| `elvis_input` | elvis under its `input' personality -- it opens already in insert mode. The name is load-bearing: elvis's wrapper picks its personality from the last letter of the name it was invoked by, so a name ending in another letter falls through to plain vi. CMDS/input is a different program entirely |
| `elvprsv` | preserves elvis's buffer when elvis dies, for elvrec to recover; elvis runs it itself |
| `elvrec` | Recover an elvis buffer preserved when elvis died. Run with no arguments it lists what is recoverable, so silence means nothing was preserved. It reads /usr/preserve/Index, and OS-9 has no /usr -- a leading /name is a device, not a directory -- so it finds nothing here whatever is placed under /dd. expreserve is the half that saves. DOC/elvrec/elvrec.doc.<br>**How:** Bare, it lists what elvis preserved; nothing listed means nothing was preserved. |
| `vi.elvis` | elvis 1.7 under the name `vi'.  CMDS/vi is PVIC, so these are two unrelated vi clones |
| `view` | elvis opened read-only |

**vi family**

| | |
|---|---|
| `vi` | PVIC 1.0a, the Portable VI Clone: a full-screen vi with ex mode, public domain.  Reads TERM and the termcap; see DOC/README-VI to choose between this and `elvis'<br>**How:** PVIC 1.0a, the Portable VI Clone and this disk's `vi', public domain. Source in SRC/pvic. Reads TERM and the termcap, so `. /dd/SYS/termcap.entry' first on a terminal it does not know. DOC/README-VI compares it with `elvis'. |
| `vi_1.0` | PVIC 1.0, the Portable VI Clone, public domain; CMDS/vi is PVIC 1.0a<br>`Usage: vi [file ...]` |

</details>

## Text tools

*Search, sort, compare, reformat, split and spell-check.*

<details><summary>137 programs</summary>

**Alternates**

| | |
|---|---|
| `diff_1.1` | a second build of GNU diff 1.1 with the same options; see `diff'<br>`Syntax   : diff [<options>] file1 file2` |

**Banners & text art**

| | |
|---|---|
| `banner` | &#9733; prints its argument as tall letters made of `@', for a banner or a sign |
| `banner1` | the first banner program written on OS-9, back from Unix with its OS-9 arms intact: eight rows tall, -d doubles, -i slants, -c=<char> picks the character and -s builds each letter out of itself; -z=<file> banners a file<br>**How:** Prints its arguments as tall letters, eight rows high. `banner1 -d' doubles the size, `-i' slants them, `-c=<char>' builds them from a character of your choosing and `-s' builds each letter out of itself. `-z=<file>' banners each line of a file instead, and `-z' alone reads standard input. Its own usage text calls it `banner', which is the name it had in 1987; the disk's `banner' is a different program. |
| `cursive` | writes a message as one line of joined, sloping cursive script, the flourish people once signed mail with<br>`usage: cursive [-tn] [-in] message` |
| `gothic` | &#9733; print text as a gothic/blackletter banner |
| `zot` | &#9733; prints a line of text in one of fourteen animated styles -- the letters slide in, bounce, sort themselves or turn up one at a time: `zot -s=14 "text"'; -s names the styles, -d plays them all<br>**How:** `zot -s=<1-14> "text"' animates the text in that style -- the letters slide in, bounce, sort themselves or turn up one at a time, each frame overwriting the last with a bare CR; `zot -s' names the fourteen styles; `zot -d "text"' plays them all in turn.  Under os9exec, -r (unpaced output) makes every animation instantaneous, so you see only the finished line. |

**Count & inspect**

| | |
|---|---|
| `ascii` | &#9733; prints the ASCII character table: every code from 0 to 127 with its control name, decimal, hex and octal |
| `charcnt` | &#9733; counts how often each character occurs in the files named, control characters included, and totals the bytes read |
| `dump` | the hex dump: shows a file, or a module in memory (-m), as offsets, hex bytes and the characters beside them Shares its name with a utility of your own -- README-NAMES<br>**How:** The hex dump: `dump <file>' prints offsets, bytes and the ASCII beside them. |
| `file` | identifies file types from the magic table in SYS/magic -- OS-9 modules, text, images with their size and colours, archives -- one line per file named<br>**How:** Names real formats now that SYS/magic is here: `file /dd/DEMO/gulls.gif' reports the GIF version, size and colour count. |
| `hdump` | a hex dump with the characters beside the bytes: -h for hexadecimal, -o octal, -d decimal, -b binary, and -z to read standard input instead of a file<br>`Syntax: hdump [<opts>] [<path>] [<opts>]` |
| `strings` | &#9733; finds the runs of printable text inside a binary and prints each with its offset, `$offset: text'; -l=n sets the shortest run reported<br>`Usage: strings [-anpl=n] [file [file]]` |
| `sum` | GNU sum: prints a checksum and a block count for each file named |
| `tail` | &#9733; prints the last lines of a text file: `tail -l=3 file' the last three, twenty by default<br>`TAIL     Version UTIL 2.70 by DESIGNA VLT 27.05.98` |
| `undump` | rebuilds a binary file from a hex dump that hdump wrote. Dump a file, edit the hex with any text editor, undump it back: between them they make a text editor into a binary editor<br>`Syntax: undump [<opts>] outfile [<opts>] <infile` |
| `wc` | count lines, words and characters for each file named, and print a total; it counts CR-terminated lines as well as LF. |
| `xd` | hex dump with hexadecimal addresses: -c shows the characters beside the bytes, -d writes them as a C array, and -l reads a dump back to rebuild the binary<br>`XD  --  Hex dump.  Call` |

**DVI drivers**

| | |
|---|---|
| `disdvi` | dumps a .DVI file's structure -- the preamble, the fonts, and every command in it, one to a line.  For understanding what TeX produced, or why a driver dislikes it |
| `dvi2tty` | prints a TeX .DVI file as text, so a typeset document can be read on a terminal.  The disk's other DVI programs drive printers; this one is for the screen.  -e narrows or widens the spacing between words<br>`Usage: dvi2tty [ options ] dvifile[.dvi]` |
| `dvialw` | DVI to Apple LaserWriter<br>**How:** Works, and so do the other nine dvi* drivers. The disk ships the MetaFont sources, not the ready-made bitmaps, so each driver says "Font file [cmr10 [300 dpi]] could not be opened ... Proceeding with zero size characters" once per font and writes a page with the right layout and no glyphs. FONTS/PK300 and PK144 hold a Makefile each; generate the bitmaps from the MetaFont sources in SYS/TEX/MFINPUTS. Output goes to <dvifile>_alw beside the input, not to standard output. |
| `dvidjp` | DVI to HP DeskJet Plus<br>`[TeX82 DVI Translator Version 2.10]` |
| `dvieps` | DVI to Epson<br>`[TeX82 DVI Translator Version 2.10 [experimental]]` |
| `dviimp` | DVI to Imagen<br>`[TeX82 DVI Translator Version 2.10]` |
| `dvijep` | DVI to HP LaserJet Plus<br>`[TeX82 DVI Translator Version 2.10]` |
| `dvijet` | DVI to HP LaserJet<br>`[TeX82 DVI Translator Version 2.10]` |
| `dvilj2` | DVI to HP LaserJet II<br>`[TeX82 DVI Translator Version 2.10]` |
| `dvimac` | DVI to Macintosh<br>`[TeX82 DVI Translator Version 2.10]` |
| `dvioki` | DVI to Okidata<br>`[TeX82 DVI Translator Version 2.10]` |
| `dvitos` | DVI to Toshiba<br>`[TeX82 DVI Translator Version 2.10]` |

**Format & typeset**

| | |
|---|---|
| `col` | filters reverse and half-line feeds out of text, so nroff's output reads on a terminal; -b drops backspaces and keeps the last character struck in each column<br>`col: illegal option -- ?` |
| `column` | sets a list out in columns across the screen; -t lines a table up, -x fills rows before columns; $COLUMNS sets the width<br>`column: illegal option -- ?` |
| `fmt` | refills ragged text into even lines, 72 columns wide or as given by -<width>; the fmt that came with elvis<br>`usage: fmt [-width] [files]...` |
| `hc` | shift text to a column, or label every line. `hc +8 f' indents f so the text starts at column 8; `hc -11 f' strips leading columns so it starts at column 11; `hc -l "> " f' puts that string in front of every line. With no option it copies the file through<br>`hc: unrecognized option=-?` |
| `lout` | Lout 2.05 document formatter<br>`usage: lout [ -i<filename> ] files` |
| `nroff` | nroff, the text formatter: fills and justifies text under dot requests and macro packages (-man and the rest); the macro sets are in LIB, and TMACDIR points at them<br>**How:** Formats a text with nroff requests: `nroff file.ms'. Its macro sets are in LIB (tmac.*). Point TMACDIR at LIB if a macro package is not found. |
| `proff` | proff, a portable roff: formats text under dot requests -- fill, justify, centre, running page headers -- with its macros in LIB/proff; +n and -n select pages, -v prints statistics<br>`usage: proff [+n] [-n] [-v] [-ifile] [-s] [-pon] [infile [outfile]]` |
| `roff` | a text formatter in the nroff line: it reads text with dot-commands at the start of a line and fills, justifies and paginates it.  `.ce' centres, `.sp' spaces, `.fi'/ `.nf' turn filling on and off, `.ad'/`.na' the right justify, `.in'/`.ti'/`.ll' set the margins and measure, `.he'/`.fo' add a running header and footer with the page number, `.sh' numbers headings.  nroff and proff are the same idea; DOC/roff has the full request list.<br>`Syntax: roff {[+00] [-00] [-s] -[h] file}` |
| `soelim` | copies roff source to standard output with each file named by .so or .nx put in its place -- run it before nroff<br>**How:** `soelim file.r > whole.r' copies roff source with every file named on a .so or .nx line put in that line's place, so a formatter that does not follow .so gets the whole text; `-' names standard input. Paths are taken relative to the current directory. |
| `tformat` | fills text to a width: `tformat [width]' reads standard input and writes it refilled and justified, 80 columns unless told otherwise<br>`tformat - format stdin to stdout.` |
| `ul` | turns underlining made with backspaces into what the terminal shows as underline; -i puts the underline on a line of its own<br>`ul: illegal option -- ?` |
| `xfmt` | refills ragged text to 72 columns, or the width -l gives; -m also reads the nroff -man requests a manual page is written in, -x a little TeX and -c C source, showing the fonts as your terminal's attributes with -u.  DOC/xfmt has the manual<br>**How:** Refills ragged text into even lines: `xfmt file' fills to 72 columns and `-l 30' to any width; with no file named it reads standard input. `-m' interprets the nroff -man requests a manual page is written in, `-x' a few TeX commands, and `-c' marks up C source. `-j' justifies, `-i' keeps indentation, `-p n' shifts the text right. With `-u' the fonts become your terminal's attributes and TERM must be set; `-o' overstrikes instead. An unknown option prints the usage line. The manual is DOC/xfmt/xfmt.1, and DOC/xfmt/cmds.tex lists the commands it knows. |

**Fortune & sayings**

| | |
|---|---|
| `cookhash` | build the hash file cookie(1) needs, from a sayings file<br>`usage: cookhash <cookiefile >hashfile` |
| `cookie` | print a random fortune cookie<br>**How:** Bare it prints a fortune from a default file. Given arguments it wants both the cookie file and the hash `strfile' built for it: `strfile mine' then `cookie mine mine.dat'. |
| `fortune` | prints a quotation at random. -s keeps to the short ones and -l to the long, -w waits long enough to read what it printed, -o takes them from the offensive file, and a filename of your own is read instead<br>`usage:  fortune [ - ] [ -wsloa ] [ file ]` |
| `psychic` | a fortune teller: psychic messages strung together from stock phrases, three unless you give a number<br>**How:** `psychic' prints three psychic messages, `psychic 1' one; each is assembled at random from stock phrases. |
| `sonnet` | writes (bad) sonnets in iambic pentameter, full screen: mark the lines you like and recompose the rest; w appends the poem to a file and -l <file> loads one it wrote to go on working on it<br>**How:** Full-screen: it takes over the display. **ESC quits**, so does q at its prompt. Commands at the prompt: m# / u# mark and unmark a line, r recomposes the unmarked lines, w [file] appends the poem to a file (sonnet.out by default, -f <file> changes that). `sonnet -l <file>' loads a poem it wrote with w -- fourteen lines -- and refuses any other file. The vocabulary is compiled in (SRC/sonnet/lex.data through makelex), not read at run time. |
| `strfile` | &#9733; builds the .dat index that fortune reads from a file of sayings separated by %% lines, and reports what it found<br>`usage:  strfile [ - ] [ -cC ] [ -sv ] inputfile [ datafile ]` |
| `unstr` | strfile's reverse: writes the sayings back out of a fortune .dat index as plain text -- `unstr sayings.dat out'; the .dat may be left off the name<br>`usage: unstr datafile[.dat] [ outfile ]` |

**KWIC index**

| | |
|---|---|
| `pagefraz` | the KWIC index suite: extracts the phrases of a Stylo- spooled text, one per line with its page number<br>`Syntax: pagefraz <opts> [<in_path> [<out_path>]] <opts>` |
| `pagekwic` | the KWIC index suite: splits a Stylo-spooled text into one phrase per line with its page number, the first step of a keyword-in-context index<br>`Syntax: pagekwic <opts> [<in_path> [<out_path>]] <opts>` |
| `pageline` | the KWIC index suite: splits a Stylo-spooled text into one word per line with its page number<br>`Syntax: pageline <opts> [<in_path> [<out_path>]] <opts>` |

**Search & match**

| | |
|---|---|
| `agrep` | grep that forgives spelling: `agrep -2 homogenos file' finds `homogeneous', allowing up to two letters wrong, missing or extra.  -i ignores case, -w matches whole words, -c counts, -f takes many patterns from a file, and -d splits the text into records (`-d "^From "' for a mailbox)<br>**How:** Like grep, but a number option allows mistakes: `agrep -1 recieve file' finds `receive', one substitution, insertion or deletion away. -i ignores case, -w wants whole words, -c counts matching records, -l names the files, -v inverts, -f patfile searches for every pattern in patfile, and -d sets the record delimiter, so `agrep -d "^From " word mailbox' prints whole messages. Bare, it prints its option summary. |
| `bm` | &#9733; a fast grep by the Boyer-Moore algorithm: searches files for one or more fixed strings, with counts, file lists and character offsets on request<br>`bm: search for a given string or strings in a file or files` |
| `bmgtest` | Boyer-Moore-Gosper substring search: `bmgtest <pattern> <file>' prints the lines that match, and it reads standard input if you name no file.  -i ignores case, -n numbers the lines<br>**How:** bmgtest [-i] [-n] <pattern> [file ...]. A demonstration of Boyer-Moore-Gosper searching. |
| `bmgtest2` | Boyer-Moore-Gosper substring search, a second driver over the same routines in SRC/strsch; the same arguments as `bmgtest'<br>`usage: bmgtest [-i] [-n] pattern [file ...]` |
| `fgrep` | &#9733; searches files for fixed strings rather than patterns, with context lines, counts, line numbers and file lists on request<br>`Syntax   : fgrep [-[[AB] ]<num>] [-[CVchilnsvwx]] [-[ef]] <expr> [<files...>]` |
| `ggrep` | &#9733; GNU grep, a second build: the same options as `grep'<br>**How:** GNU grep. `ggrep <expr> <files...>'; -E, -F, -i, -v, -w and the rest as you would expect. |
| `grep` | GNU grep 2.0: prints the lines of files that match a regular expression -- -E extended, -F fixed strings, -i ignore case, -v invert, -n number, -c count Shares its name with a utility of your own -- README-NAMES<br>`grep: illegal option -- ?` |
| `look` | prints the lines of a sorted file that begin with a string: `look abs GAMES/words'; -f ignores case<br>`usage: look [-f] string file` |
| `sgrep` | grep with substitution, reading patterns from a file and text on standard input: `sgrep pats <in' replaces each odd line of pats with the even line after it; -m only matches (-c counts, -n numbers, -v inverts), -y ignores case. Its manual is DOC/sgrep.doc<br>**How:** A filter: `sgrep patfile <input'. patfile holds pairs of lines, a pattern and what to put in its place, and every match in the input is replaced. With -m the file is a plain list of patterns and matching lines are printed (-c counts them, -n numbers them, -v inverts). -y ignores case. Patterns use `:a' letters, `:d' digits, `:n' alphanumerics, `*' `+' `-' repeats, and `?1' in a replacement is the first wildcard's text. DOC/sgrep.doc is its manual. |
| `soundex` | Soundex phonetic key for each word on stdin |
| `wns` | &#9733; windowing search: grep that prints a window of lines round each match.  `wns -w=2 pattern file' shows two lines before and after, -a and -b set them apart, and windows that do not touch are divided by a dashed line<br>**How:** A grep with context: `wns -w=2 pattern file' prints two lines either side of each match, -a and -b set the after and before counts separately. Needs cio. |

**Sort, compare & merge**

| | |
|---|---|
| `cdiff` | a context diff: compares two text files and prints what changed, each difference headed by a line such as `>>>> INSERT BEFORE 2'<br>`TRY: diff oldfile newfile` |
| `comm` | compares two sorted files: the lines only in the first, only in the second, and in both, in three columns; -1, -2 and -3 leave a column out<br>`comm: illegal option -- ?` |
| `diff` | &#9733; GNU diff 1.1: compares two text files and prints the lines that differ, in normal, context (-c) or ed-script (-e) form; reads CR-terminated text<br>`diff: illegal option -- diff: requires two file names.  Usage: diff [-options] file1 file2` |
| `ediff` | put `diff' output into plain English: `diff <f1> <f2> ! ediff', or `ediff <file' for a diff you already have.  A one-line change comes out as `-------- 1 line changed at 3 from: ... to: ...'.  `diff' does the comparing; this makes the answer readable<br>`Syntax   : 'ediff <file'  or  'diff <f1> <f2> ! ediff'` |
| `fcomp` | &#9733; compares two text files line by line and names the lines inserted, deleted or changed between them<br>`Syntax: fcomp <file_1> <file_2>` |
| `join` | GNU join -- relational join of two sorted files<br>``join: unrecognized option `-?'`` |
| `nsort` | sorts lines from standard input -- lexically, despite the name: given 3, 22, 111 and 4 it answers 111, 22, 3, 4, the same order GNU `sort' gives with no options. For a numeric sort use `sort -n'<br>`Usage: nsort <unordered >sorted` |
| `qsort9` | &#9733; an in-memory quicksort filter: sorts lines by a chosen field (-f) and separator (-c), in dictionary order, reversed or unique<br>`Syntax: qsort9 [<opts>] [<srcpath>] [<opts>]` |
| `sort` | GNU sort: sorts lines of text -- by field (+POS or -k), numerically (-n), reversed (-r), folding case (-f), unique (-u) -- and merges already-sorted files (-m)<br>``sort: unrecognized option `-?'`` |
| `spiff` | &#9733; a tolerant diff: compares two files while ignoring differences that do not matter -- white space, number formatting, case if asked -- and knows C, shell, Fortran, Modula-2 and Lisp source<br>**How:** Compares two files while ignoring differences that do not matter (whitespace, number formatting). Takes two filenames. |
| `tcmp` | &#9733; compares two text files and prints each differing line, both versions one under the other with the line number in each; -s sets how far ahead it looks to resynchronise<br>**How:** Compares two text files and prints each differing line, both versions one under the other with the line number in each file. Files whose lines differ only in tabs and spaces are reported as changed, which reads oddly until you dump them. |
| `tsort` | sorts pairs topologically: each pair says the first must come before the second, and out comes one order that keeps them all<br>`usage: tsort [ inputfile ]` |
| `unip` | unique lines with page numbers<br>`Syntax: unip [<opts>] [<srcpath>] [<opts>]` |
| `uniq` | &#9733; drops repeated adjacent lines: -u keeps only the unrepeated, -d only the repeated, -c counts each; sort first<br>`Usage: UNIQ [-u][-d][-c] [-n] [^n] input [>output]` |

**Spelling & words**

| | |
|---|---|
| `ag` | finds every phrase the letters of a word or phrase make in a word list: `ag "dirty room"' gives dormitory and dirty moor; -w lists the words it could use<br>**How:** `ag "dirty room"' prints every phrase made from exactly those letters out of GAMES/words, one a line. -d names another word list (- for standard input), -s 3 drops words shorter than three letters, -a counts a and i as words, -w also lists the usable words and -W only those, -o writes to a file. Long phrases give very many answers. |
| `anagram` | finds the anagrams of a word in the word list GAMES/words: `anagram listen' prints enlist, listen, silent and tinsel; -l also lists near misses with their leftover letters<br>**How:** `anagram listen' lists every word in GAMES/words spelled with exactly those letters. -l adds words that use some of them, with the leftovers in brackets; -m sets the shortest word counted (2); -d names another word list. |
| `buildhash` | build ispell's dictionary hash.  It reads a word list called `dict.191' (the name is compiled in). LIB/ispell.hash is the built hash, 329,748 bytes, and it ships, so ispell itself reads that and works.  `chardef' reads the same word list. |
| `ispell` | interactive spelling checker.  `ispell <file>' walks the unknown words and offers corrections; `ispell -l <file>' just lists them.  Its table is LIB/ispell.hash, 17,632 words, which `buildhash' makes from SRC/ispell/dict.191 -- so you can add words and rebuild it.<br>**How:** Interactive spelling checker. `ispell <file>' walks the unknown words and offers corrections; `ispell -l <file>' just lists them. Its table is LIB/ispell.hash, which `buildhash' builds from SRC/ispell/dict.191 -- 17,632 words -- so adding words means editing that file and running buildhash from the directory holding it. It was written up as broken until 2026-09-20: it was being given a hash table made for a different edition of ispell, which is what the bus error at the first lookup was. |
| `jargon` | a browser for the Jargon File, the hackers' dictionary: `jargon -b word' opens at an entry; it reads jargon.txt and jargon.idx from VH on its own<br>**How:** A browser for the Jargon File, which is here: VH/jargon.txt, version 3.0.0 of 27 July 1993, with its index. It will not read SYS/termcap -- do `. /dd/SYS/termcap.entry' first, then `jargon -m'. |
| `makelex` | &#9733; compiles sonnet's lex.data word list into a C array |
| `speech` | translates English text into phonemes, the front half of a speech synthesiser: run bare it reads a line and prints its transcription; `speech in out' does a whole file<br>`Error: Cannot open input file.` |

**Split & join**

| | |
|---|---|
| `sepwords` | splits text into one word per line -- the first step towards a word list or an index<br>`Syntax: sepwords [<in_path> [<out_path>]]` |
| `split` | GNU split: cuts a file into pieces of so many lines (-l) or bytes (-b), named after a prefix -- partaa, partab and so on<br>``split: unrecognized option `-?'`` |

**TeX**

| | |
|---|---|
| `afm2tfm` | Adobe font metrics to TeX font metrics<br>`afm2tfm 7.0, Copyright 1990-92 by Radical Eye Software` |
| `bibtex` | BibTeX, the bibliography formatter. It reads the job name from standard input -- `Please type input file name (no extension)--' is a prompt, not silence -- and the .bst styles are in SYS/TEX/INPUTS (plain, unsrt, abbrv and alpha), not in SYS/TEX/BIB, which holds a read.me<br>**How:** It reads the job name from standard input -- `Please type input file name (no extension)--' is a prompt, not silence. The .bst styles are in SYS/TEX/INPUTS (plain, unsrt, abbrv, alpha), not SYS/TEX/BIB, which holds one read.me. A backslash cannot be TYPED at this shell -- bash's echo eats `\c' -- so patch one in with `pbyte <file> <hex offset> 5c'. |
| `dvips` | DVI to PostScript, dvipsk 5.495b -- the fuller of the two PostScript drivers, beside dvialw.  Its seven prologues ship in SYS/TEX/DVIPS and it finds them there, so it writes pages: `dvips <file>.dvi -o <file>.ps'.  A font size that has not been built is reported and left blank; `-M' stops it offering to make one.  Source: SRC/dvips<br>**How:** DVI to PostScript: `dvips <file>.dvi -o <file>.ps'. Its prologues ship in SYS/TEX/DVIPS and it finds them there. A font size nobody has built is reported and left blank; `-M' stops it offering to make one. |
| `dvitype` | show what is inside a .dvi file, as text<br>**How:** `dvitype <file>.dvi < /nil'. It asks five questions -- output level, starting page, page count, device resolution, magnification -- and takes the default for each at end of file. Redirect its input so a script does not wait on the questions. |
| `gftopk` | MetaFont generic font to packed font<br>**How:** `gftopk cmr10.120gf /dd/tmp/cmr10.120pk'. GFFONTS must name where the input is; the output path is never searched for, so an absolute one works with nothing set. |
| `gftype` | show what is inside a .gf file<br>**How:** `gftype -i <font>.<dpi>gf' draws the glyphs as asterisks; -m adds the opcodes. GFFONTS must name the directory -- the compiled-in FONTS paths do not begin with `.', so a file beside you is invisible. |
| `inimf` | MetaFont with no base preloaded<br>**How:** It builds a Metafont base, which SYS/TEX/MFBASES now ships. To rebuild: `echo "plain; \input modes; dump" > mf.in' then `ksh -c "cd /dd/tmp; inimf < mf.in"'. About a minute. DOC/README-METAFONT has the rest. |
| `initex` | TeX with no format preloaded, for building .fmt files<br>**How:** TeX with no format preloaded -- this is what builds the .fmt files. `initex "plain \dump"'. The three formats already ship in SYS/TEX/FORMATS, built this way, so you only need this to make your own. |
| `latex` | LaTeX -- Lamport's document preparation system on top of TeX<br>**How:** See `tex'. The wrapper cannot reach the engine; run `virtex '&lplain' yourfile.tex'. That does work: SAMPLES/small.tex gives "Output written on small.dvi (1 page, 1704 bytes)". The .dvi and .log land in your data directory. |
| `maketexpk` | generate a .pk font at the size TeX asked for<br>**How:** It carries the RIGHT Metafont line in its own strings and then reaches for `makdir', `del' and `attr' to file the result -- three Microware utilities that are not here. Run the virmf line yourself: DOC/README-METAFONT has it, and `gftopk' is all maketexpk was going to do afterwards. |
| `pktogf` | packed font back to generic font<br>**How:** Unpacks a .pk. The result is longer than the .gf it came from -- pktogf rewrites the preamble comment -- and the bitmap is unchanged. |
| `pktype` | show what is inside a .pk file<br>**How:** `pktype <font>.<dpi>pk' prints the packed font back, glyphs included. PKFONTS must name the directory. |
| `pltotf` | property list to TeX font metric<br>`Usage: pltotf [-verbose] <property list file> <tfm file>.` |
| `slitex` | SliTeX -- LaTeX for slides<br>**How:** LaTeX for slides; its format is SYS/TEX/FORMATS/splain.fmt, already built. |
| `tangle` | WEB to Pascal -- Knuth's literate programming tool. It needs a change file named, always: given only a .web it answers `Error: `Can't open file.'' and the absent change file is what it could not open. DOC/tex ships `sample.web' and `none.ch' (an empty change file): copy both to your data directory and run `tangle sample none'. It reads and writes there, not where you typed from<br>**How:** Needs a change file named, always. `tangle yourfile.web' alone answers `Error: `Can't open file.'' and the file it cannot open is the absent change file, not your source. DOC/tex ships `sample.web' and `none.ch' (empty, changes nothing): copy both to your data directory and run `tangle sample none'. It reads and writes in the data directory, which bash's `cd' does not move. `weave sample none' is the other half. |
| `tex` | TeX itself -- the typesetting program (a driver; virtex does the work)<br>**How:** Run the engine, not the wrapper. `tex' is one line: it asks a shell to run `virtex "&plain" yourfile', the quoted format name is never unquoted, and the shell answers E$PNNF for the whole line (rc 221 with no $SHELL set, and silently). Type `virtex '&plain' yourfile.tex' instead. For LaTeX it is `virtex '&lplain' yourfile.tex', for SliTeX `virtex '&splain''. SYS/TEX/SAMPLES/small.tex is a LaTeX document and story.tex is plain TeX with no \end. |
| `texidx` | sorts the \indexentry lines a LaTeX \makeindex run leaves in a .idx file into the alphabetised index LaTeX reads back.  It opens its input with no access mode at all, which OS-9 refuses to read, and its loop reads that refusal as `buffer too small' and quadruples the buffer until the request passes what the machine has -- so it always ends at `virtual memory exhausted'.  No source for it is here to fix |
| `tftopl` | TeX font metric to property list (the readable form) |
| `vftovp` | virtual font to virtual property list<br>**How:** `vftovp s.vf s.tfm back.vpl' reads the binary pair back to text. VFFONTS and TEXFONTS must name where the .vf and .tfm are. |
| `virmf` | the real MetaFont engine -- generates fonts from .mf sources<br>**How:** Metafont. `virmf '&cmbase' '\scrollmode; \mode:=epsonlo; \input cmr10; \end'' renders all 128 characters of cmr10. the job name comes from the command line: the same line fed on standard input renders the same font and calls it `mfput'. |
| `virtex` | the real TeX engine, loaded with a format<br>**How:** The real TeX engine, and the one to use -- see `tex'. It wants the format first: `virtex '&plain' file.tex' or `virtex '&lplain' file.tex'. The formats that ship are plain, lplain and splain, in SYS/TEX/FORMATS. |
| `vptovf` | virtual property list to virtual font<br>**How:** `vptovf /dd/DOC/tex/sample.vpl s.vf s.tfm'. sample.vpl is a one-character virtual font written for this, mapping `A' onto cmr10's. |
| `weave` | WEB to TeX -- the other half of literate programming, and it needs a change file for the same reason `tangle' does: `weave sample none'<br>**How:** The other half of `tangle', and it needs a change file named just as tangle does: `weave sample none', never `weave sample.web'. Given only a .web it answers `Error: `Can't open file.'' and the file it cannot open is the absent change file. DOC/tex ships sample.web and none.ch. |

**Transform & filter**

| | |
|---|---|
| `ape` | writes gibberish in the style of whatever it reads -- a travesty generator; `-b' is how much source to read and `-l' how many characters must match before it follows the source. `newsgen' is the other of its kind here<br>**How:** A travesty generator: `-b' is how much source to read and `-l' the pattern length. Feed it varied text -- one word repeated makes it generate without end, because every position matches every other. |
| `autolf` | &#9733; converts line endings between CR, LF and CR LF, expands tabs and handles ^Z, as a filter: `autolf -c -C -L < in > out' makes DOS text of OS-9 text, and `-H' explains the conversions. Given a file name it converts through a temporary it then cannot rename back, so feed it standard input<br>`autolf: copy stdin to stdout, converting end-of-line character sequences` |
| `casefix` | sentence-cases text: every letter to lower case except the first of each sentence. A filter that reads standard input; a file named as an argument is ignored<br>**How:** It is a filter and reads standard input: `casefix < file' sentence-cases it. |
| `choose` | prints lines picked at random from its input, in the order they stand: `choose -3 file' for three, one by default<br>**How:** `choose -3 file' prints three lines picked at random from the file, in the order they stand in it; with no number it picks one, and with no file it reads standard input. It seeds from the clock in whole seconds, so two runs in the same second pick alike. Asking for more lines than there are is refused. |
| `colrm` | removes columns from each line: `colrm 3 5' deletes the third to fifth characters |
| `cut` | picks fields (-f) or character columns (-c) out of each line, with -d naming the field separator<br>`cut: Illegal option -- ?` |
| `detab` | &#9733; replaces tabs with spaces, at stops every three columns or every n with -tn<br>`Usage: detab [-tn] [infile] or [<infile]` |
| `eo` | &#9733; runs a command on every line of a file -- an xargs: `eo <file> <command> @' runs the command once per line with `@' replaced by the line; -p takes the lines from a pipe, -q runs quietly, -e stops at the first error. It shells out through SHELL, which SYS/login sets<br>**How:** Runs a command on every line of a file, with `@' standing for the line: `eo <file> <command> @'. It shells out, so it needs SHELL set to a shell that takes a command line as one argument -- SYS/login sets `SHELL=/dd/CMDS/ksh' and that is what makes it work. Without it, `can't execute /dd/bash'. `-p' takes the lines from a pipe instead of a file. |
| `expand` | GNU expand: turns tabs into spaces, at stops eight columns apart or as -t says Shares its name with a utility of your own -- README-NAMES<br>``expand: unrecognized option `-?'`` |
| `field` | &#9733; select whitespace-separated fields from standard input by number, in the order asked for and tab-separated on output: `field 2 4 1' prints the second, fourth and first word of each line. `-i=c' names another input separator.<br>`field v1.0 (c) S.R.Bourne, M.C.Gregorie, 1994` |
| `fillup` | &#9733; fills a file up to a given length with a constant byte: `fillup -n=64 -i=65 f' pads f to 64 bytes with `A' and says `24 bytes (value=65) appended'. The length option is -n=, not -l=<br>`Syntax:   fillup [<options>] <file>` |
| `fold` | wraps long lines to a width, 80 columns unless -w says otherwise<br>`fold: illegal option -- ?` |
| `gawk` | &#9733; GNU awk 2.11, the pattern-and-action language: `gawk "{print $1}" file' prints the first field of every line, and named no file it reads standard input<br>**How:** GNU awk 2.11. `gawk "{print \$1}" file' prints the first field of every line; named no file, it reads standard input. Keep the program text short: a command line wider than the window scrolls under bash and is hard to read back. Needs Microware's cio. |
| `gdd` | &#9733; GNU dd, a block copier and converter: `gdd if=<file> bs=<n> skip= seek= count=', and `conv=ucase' converts on the way through. `of=' can only name a file that already exists, so send the output through `>' instead<br>**How:** GNU dd -- a block copier and converter. `gdd if=<file> bs=8 count=1' copies eight bytes, `conv=ucase' converts on the way through. `of=' can only name a file that already exists, so send the output through `>'. Give it arguments. It uses Microware's cio; `dump' is the hex dump here. |
| `gep` | &#9733; a global expression parser -- grep-like; its `-e' takes the path of a file holding the expressions: `gep -e=/dd/tmp/patterns <file>'. A file of patterns applied at once is what it is for and nothing else here does it. See DOC/README-GREP<br>**How:** Its expressions come from a file named with `-e', which its own option list marks `(required)': `gep -e=<patterns> <source>'. Handing it a pattern and a file the way you would grep earns `more than one path specified'. |
| `head` | prints the first lines of a file: `head -n 20 file', or the older `head -20 file'<br>**How:** First lines of a file: `head -n 20 file', or the older `head -20 file'. Needs cio. |
| `l` | &#9733; list a text file with word wrap and a carriage return at the end of every line -- `l -<width> <file>', 79 columns by default. Written for Stylo documents and other long-line files. It takes files, not directories<br>`Usage: l [-options] [file] [file] [-options]` |
| `paste` | joins files line by line, side by side and tab-separated: `paste f1 f2'; -d picks another separator and -s lays one file's lines along a single line<br>**How:** Joins lines side by side, tab-separated by default: `paste f1 f2'. `-d:' picks another separator; `-s' puts one file's lines on a single line. |
| `pep` | a file detergent: strips control characters and non-ASCII (-b), converts between the DEC, IBM-PC, Macintosh and WordStar character sets, expands tabs and sets the line terminator (-u)<br>`pep  ver. 2.1; Copyright (c) 1989 Gisle Hannemyr` |
| `psc` | &#9733; turns an ASCII table into commands for `sc', the spreadsheet: `psc -d' ' < table' answers `let A0 = 1', `let B0 = 2' and a `format' line per column. -d sets the field delimiter, -r assembles rows first, -s names the top-left cell<br>**How:** Feeds `sc', the spreadsheet: `psc -d' ' < table' turns rows of numbers into `let A0 = 1' commands sc can read. -r assembles rows first, -s names the top-left cell, -d sets the delimiter. |
| `rev` | reverses the characters of each line<br>`rev: illegal option -- ?` |
| `rot` | turn a text file on its side -- line one becomes column one<br>`syntax: rot {opt} [<file>]` |
| `subber` | &#9733; substitutes words in a stream from a `,old,new' word list, one pair a line, the first character being the delimiter. It grows its memory as it reads, so give it plenty up front: `subber #1000k words file' at an OS-9 shell<br>**How:** Substitutes words in a stream from a word list of `,old,new' pairs (the line's first character is the delimiter), reading a file as the second argument or standard input. It grows its data area as it reads, with F$Mem, so give it room up front: at an OS-9 (Microware) shell, `subber #1000k words file' -- `#1000k' is the shell's directive, not subber's, so only Microware's shell acts on it: bash hands it straight to subber, which answers `cannot open #1000k', and without it subber's own growth is refused -- `No more memory: 256-byte request refused'. Run it at your OS-9 shell or through it. Both halves measured 2026-09-19. Tested: `,fox,cat' turns `a fox' into `a cat'. |
| `tabs` | re-space a file, standard input to standard output: `-i8' says the input's tab stops are every 8 columns, `-o0' asks for spaces on output and `-o4' for tabs every 4.<br>`Unknown switch: ?` |
| `tac` | GNU tac: prints a file backwards, last line first<br>**How:** Prints a file backwards, last line first -- cat's mirror image. Needs cio. |
| `unexpand` | GNU unexpand: turns leading spaces back into tabs, or all of them with -a<br>``unexpand: unrecognized option `-?'`` |
| `unp` | &#9733; strips unprintable characters from a stream and reports each one removed, by code and line number<br>`Usage:  unp [-?] [file]` |
| `upperdir` | normalises the names in a directory: files to lower case, directories to upper, printing each as it renames it<br>`Usage: UpperDir [directory name]` |
| `valspeak` | Valley-speak text filter: standard input in, the rewritten text out. `I think this operating system is really good' comes back as `I think this operatin' system is like wow! really bitchin''. |

</details>

## Files & directories

*Listing, copying, finding, renaming, and knowing what you have.*

<details><summary>37 programs</summary>

**Attributes & ownership**

| | |
|---|---|
| `chgrp` | &#9733; sets the group half of a file's owner, by number or by name<br>`chgrp: Usage:  chgrp [-z] {numerical-gid \| username} [file [... file]]` |
| `chown` | &#9733; sets the user half of a file's owner, group.user, by number or by a name from SYS/password Shares its name with a utility of your own -- README-NAMES<br>`chown: Usage:  chown [-z] {numerical-uid \| username} [file [... file]]` |
| `fstat` | display a file's file descriptor -- the RBF file-descriptor sector, not the attribute bits `attr' shows you. Its own Function line says `Display file descriptor information' and it reports itself as `FStat'. `-s' adds the segment list, and `ssl' shows the same list from the same sector<br>`Syntax: FStat [<opts>] <file1> [<opts>]` |
| `owner` | &#9733; change a file's owner -- `owner <user> <file> ...', super user only. Run with a file it prints its usage; run as `owner <file>' it reads the filename as a user name and answers `No such user'. `fstat' and `ls -l' are what show an owner<br>`owner: change ownership of files` |

**Browse & inspect**

| | |
|---|---|
| `browse` | a screen-oriented directory browser: it shows an `ls -l' listing you move around the way you would move around a file in `vi', and acts on the entry under the cursor -- SPACE enters a directory or pages a file, `x' dumps it in hex, `?' shows the help.  Wants TERM, and a shell for the keys that run a program<br>`Browse through a directory, written by Peter da Silva` |
| `utree` | full-screen file manager: the directory tree in the top pane, the files of the current directory below, and a menu of one-letter commands for whichever pane you are in -- copy, move, rename, remove, edit, page, dump, print, grep, tag a set of files and act on all of them at once.  `!' escapes to a shell and keeps a history of what you ran. Its startup file, key bindings and help pages are in SYS/UTREE<br>**How:** Full-screen, two panes: the directory tree above, the current directory's files below.  `>' or RETURN crosses into the file pane and RETURN or `q' comes back, while `<' goes up to the parent directory; the menu line names the commands for whichever pane you are in and a capital letter means the whole tagged set.  `H' is the help pages, `=' the variables, `!' a shell command line with a history, `Q' then `y' quits.  $HOME/.utree overrides the startup file in SYS/UTREE, so the settings and the menu commands can be yours without touching the disk.  It holds the whole tree in memory, so on a disk this size open it on a subdirectory -- `utree DOC' reads 303 directories and 1553 files -- or give `-q' at the root, which builds two levels, and `-l <n>' for any other depth.  An os9exec older than its 2026-09-19 memory-block fix stops partway with `ualloc: memory full' on a tree that large, counting allocations rather than bytes; that is the emulator's own accounting and not an OS-9 limit, and on a build carrying the fix the whole of /dd -- 1131 directories, 12377 files -- reads in about a minute and a half. |

**Copy, move, delete**

| | |
|---|---|
| `cp` | &#9733; copy files -- `cp <from> <to>' copies the bytes across.  Run with no arguments it prints its usage and then stops on a bus error<br>`Usage: cp file1 file2` |
| `dback` | directory backup: walks a directory and lists an OS-9 `copy' for every file that is new or has changed; -e runs them, with your own OS-9's `copy' loaded<br>`Usage: Dback [-options] <fromdir> <todir> [-options]` |
| `delbak` | &#9733; delete backup files (*_bak) in a directory tree<br>`Usage: delbak [-options] [directory] [-options]` |
| `move` | &#9733; move files between directories without copying the contents -- it relinks them, which is why it is quick and why its own help warns never to kill it mid-run. `move <from> <to>' wants a destination name; -w=<dir> is the wildcard form that takes a directory.<br>`Syntax:   move [<options>] <from> [<to>] [<options>]` |
| `mv` | &#9733; GNU mv (fileutils 3.13) -- rename a file or move it into a directory; `-i' asks before overwriting, `-b' keeps a backup, `-v' names what it moved Shares its name with a utility of your own -- README-NAMES<br>``mv: unrecognized option `--'`` |
| `rm` | &#9733; GNU rm: removes files, whole directories with -r, asking first with -i, naming each with -v<br>``rm: unrecognized option `-?'`` |
| `undel` | &#9733; brings back a deleted file: it asks for the directory, offers each deleted name RBF still holds (the first letter overwritten), and asks twice before writing Shares its name with a utility of your own -- README-NAMES<br>`usage: undel  [ -opt ] [ full directory name ] [ -opt ]` |

**Create & rename**

| | |
|---|---|
| `mkdir` | &#9733; makes a directory; -p makes every directory on the way to it, -m sets its mode<br>``mkdir: unrecognized option `-?'`` |
| `rendsk` | &#9733; changes the volume name of a disk -- the name in its identification sector, not any file on it; super user only<br>`Syntax:   rendsk [<opts>] <disk device> <new name>` |

**Find & compare**

| | |
|---|---|
| `dfiles` | &#9733; find duplicate files under a directory and write out the `cmp' commands that would prove them identical, so the list itself is the answer<br>`dfiles 0.7` |
| `du` | &#9733; adds up what a directory tree holds -- bytes, kilobytes, sectors and the number of files -- one line per directory, with a total<br>`Syntax: du <directory>` |
| `ff` | &#9733; find files by name -- `ff <name>'.  It needs a `shell' module: it builds the command `dir -ausr ! grep <name>' and forks a shell by that bare name to run it, so it is silent without one -- keep your own loaded, and see DOC/README-SHELLS.  `find' does the same job with no shell at all.  Its one message, when you give it nothing to look for, is in German |
| `find` | &#9733; find 1.1.5 -- search a directory tree, with its own syntax: `-n=<name>' matches and `-o' prints what it found. (`find <dir> -name x -print' answers `only one parameter allowed'.)  The manual in DOC/find describes a different find.<br>`Syntax: find {<opts>} [<path>]` |
| `howfrag` | report how fragmented a file is: how many disk pieces it is stored in, out of a file descriptor's 48.  A high count on a file that grows a lot is when to re-copy it.<br>`Syntax:   howfrag <filename> [<filenames> ... ]` |
| `space` | &#9733; effective disk usage: what a tree costs on the disk, descriptors, directories and part-used clusters included, rather than what it contains. Conditions apply; `help space' has them<br>`Syntax:   space [<opts>] {<dir/file path>} [<opts>]` |

**Home Librarian**

| | |
|---|---|
| `Ascii2Libr` | Home Librarian: build a catalogue from plain text -- `Ascii2Libr -outfile cat.libr', with the text on standard input, in the form Libr2Ascii writes<br>**How:** `-outfile cat.libr' with a space, and it reads the ASCII on standard input. The text is the form Libr2Ascii writes: a page count, then a card count and the cards, then the title, author and subject index sections. |
| `EditLibr` | Home Librarian: builds and maintains a catalogue -- add, edit and delete cards -- `EditLibr -editfile cat.libr'<br>**How:** Part of the HL10 librarian set. Wants an edit file as a parameter; `EditLibr' alone prints its syntax. |
| `Libr2Ascii` | Home Librarian: dumps a catalogue to plain text on standard output, `Libr2Ascii -infile cat.libr', in the form Ascii2Libr reads back<br>**How:** `-infile cat.libr' with a space. It writes the catalogue to standard output as text, and a page count and four index-key counts at the end -- all zero means the catalogue is empty. |
| `Librarian` | Home Librarian: search a catalogue. Six programs and their docs travel together -- its licence requires it<br>**How:** One of six Home Librarian programs that must stay together -- its licence says so. Start here to search a catalogue; EditLibr edits one, Ascii2Libr builds one from text, Libr2Ascii dumps it back, PrintCards and PrintLabels print it. Manual in DOC/homelibr. |
| `PrintCards` | Home Librarian: prints a catalogue as index cards, the shelf list by default or the title, author or subject reference cards with -by<br>`Syntax: PrintCards [opts]` |
| `PrintLabels` | Home Librarian: print labels. Its options each take a separate argument -- `-infile cat.libr -templatefile tpl.txt', not `-infile=...', which answers `Bad option:' and prints the syntax. The same is true of Ascii2Libr, Libr2Ascii, PrintCards and EditLibr. The template is a text file copied out once per card, with %title, %author, %year and the other field names replaced<br>**How:** Its options take a separate argument -- `-infile cat.libr -templatefile tpl.txt', never `-infile=...', which answers `Bad option:' and prints the syntax. The same is true of Ascii2Libr, Libr2Ascii, PrintCards and EditLibr. The template is a text file copied out once per card with %title, %author, %year and the other field names replaced. |

**List & navigate**

| | |
|---|---|
| `dir` | &#9733; directory listing -- `dir [<opts>] <directory>'; `-e' adds owner, dates, attributes and size Shares its name with a utility of your own -- README-NAMES<br>`Dir Version 1.08  (C) 1988 by Lim. (Modified by L.Z)` |
| `dm` | &#9733; Disk Master 1.4, a full-screen two-pane disk and directory browser with a file-information panel beside the listing.  It runs the commands on its bottom line through system(), so SHELL must name a shell that can carry them out: with SHELL=/dd/CMDS/sh it runs completely.  Its help file is SYS/dm.hlp, reached with `h'. The command letters are typed in LOWER case, though the line along the foot prints them capitalised: `H' does nothing at all<br>**How:** Disk Master 1.4, a full-screen disk browser. It runs the commands on its bottom line through system(), so SHELL must name a shell that can carry them out; with SHELL=/dd/CMDS/sh it runs completely, listing and file-information panel and all. |
| `ls` | GNU ls (fileutils 3.13) -- a real stat(), columns, and `-al'<br>`Usage: ls [OPTION]... [FILE]...` |
| `tree` | print a directory tree, drawn with line graphics -- directories only, sorted, from the directory you name<br>`tree, v1.21 - 28.04.90 - updated 17.06.90` |

**Paths**

| | |
|---|---|
| `basename` | &#9733; prints the last part of a path -- the file name with every directory dropped -- and drops a suffix too if one is given as a second argument<br>`basename v1.0 (c) M.C.Gregorie, 1994` |
| `dirname` | &#9733; prints the directory part of a path: everything up to the last slash<br>`dirname v1.0 (c) M.C.Gregorie, 1994` |

**Records & catalogues**

| | |
|---|---|
| `names` | &#9733; an address book, in German: `Adressen Verwaltung', version 1.0.  Anrede, Nachname, Vorname, Strasse, PLZ, Stadt, Telefon and two Bemerkung lines per record, kept in a file of its own under SYS which it creates on first run.  Full screen and interactive -- it wants a terminal, and at end of input it re-prompts for ever.  It does not list module names; `modinfo' is what does that |
| `sdb` | SDB 2.0, "a Simple Database System" by David Betz: a small relational database.  A relation is a file, a tuple a record, an attribute a field. `create' makes a relation and names its fields, `insert' prompts for one record at a time, `print <fields> from <relation> ;' reads them back as a table, and there are delete, update, sort, import, export and macros besides.  `help' lists them and DOC/sdb holds the manual<br>**How:** Run it in a directory you can write to; it keeps one file per relation there. `create people ( name char 12 town char 12 ) 20' makes one, `insert people' prompts field by field and a blank line ends the entry, and `print * from people ;' reads it back as a table -- the semicolon is part of the syntax. `help' lists the commands, `exit' leaves. Typing something it cannot parse gives `syntax error' and, if you keep going, a stack overflow. |

**Split & join**

| | |
|---|---|
| `divide` | &#9733; splits a file into pieces of so many lines: `divide -l=<lines> <infile> [<outfile>]' writes outfile.1, outfile.2 and so on<br>`DIVIDE Version 1.1` |
| `fc` | &#9733; split a big file in two, to carry it on 360k disks -- the cut is at exactly 350,000 bytes: its own Function line says "Takes first 350,000 bytes of a file or stdin and puts in one file and puts remaining bytes" in the other<br>`Syntax:   fc [<file>]` |

</details>

## Developer tools

*Version control, tags, cross-reference, formatters, a debugger and benchmarks.*

<details><summary>36 programs</summary>

**Assembly**

| | |
|---|---|
| `tab` | Tabulate 6809 or 68000 assembly source -- opcode-aware, and works on code that will not assemble<br>`Syntax: tab [<opts>]` |
| `xlate` | &#9733; Translate 6809 assembly source to 68000<br>**How:** Translates 6809 assembly source into 68000. Pairs with as09 (the 6809 assembler on this disk) and with `tab', which tabulates either dialect. Needs cio. |

**Benchmarks**

| | |
|---|---|
| `dhry` | Dhrystone 2.0 built with Microware's cc. It reads the number of runs from standard input: `echo 500000 \| dhry'. Twelve builds of the same source sit in CMDS/DHRY, so the compilers can be compared<br>**How:** Dhrystone 2.0. Twelve builds of the same source sit in CMDS/DHRY -- run several and compare, which is what tells you the compiler's cost. Run under an emulator the number describes the host machine, not a 68000. |
| `dhryGcc` | &#9733; Dhrystone 2.0 built with GCC 1; see dhry |
| `dhryGcc2` | &#9733; Dhrystone 2.0 built with GCC 2; see dhry |
| `dhryGcc2in` | &#9733; Dhrystone 2.0 built with GCC 2 with inlining; see dhry |
| `dhryGcc2mx` | &#9733; Dhrystone 2.0 built with GCC 2, mixed options; see dhry |
| `dhryGcc2o2` | &#9733; Dhrystone 2.0 built with GCC 2 at -O2; see dhry |
| `dhryGccin` | &#9733; Dhrystone 2.0 built with GCC 1 with inlining; see dhry |
| `dhryGccmx` | &#9733; Dhrystone 2.0 built with GCC 1, mixed options; see dhry |
| `dhryGcco2` | &#9733; Dhrystone 2.0 built with GCC 1 at -O2; see dhry |
| `dhryO2` | Dhrystone 2.0 built with Microware's cc at -O2; see dhry<br>**How:** All eleven Dhrystone builds read A run count from standard input before they start -- run bare they print two lines and wait. `echo 200000 \| dhryO2'. Under os9exec even 20000 runs finish inside one tick of the clock, so it answers "Measured time too small ... Please increase number of runs" rather than a rate; the comparison between builds is what they are here for, and on real hardware it works as intended. |
| `dhryshamu` | &#9733; Dhrystone 2.0, the shamu build; see dhry |
| `dhryshamu2` | &#9733; Dhrystone 2.0, a second shamu build; see dhry |
| `disktest` | measures disk performance: it times a read of the raw device, a write of a temporary it then removes, and a run of seeks, and prints the rates.  It asks OS-9's own `free' for the sector count first, through a pipe, and waits on that pipe until the answer comes -- so on a system where `free' is to hand it runs through, and here, where it is not, it waits.  [no military use -- DOC/EFFO-INFO]<br>`Syntax   : disktest [<opt>]` |
| `savage` | &#9733; Savage's benchmark: a chain of functions that should cancel to an exact number, a thousand times; how far the printed value drifts measures the arithmetic's rounding |
| `sieve` | &#9733; the sieve of Eratosthenes as a speed test: it runs the pass a hundred times over and prints `start' and then ` 100 sieves done'.  What it measures is the gap between those two lines, so run it under your own OS-9's `time' to get a figure.  `savage' and the twelve Dhrystone builds are the other benchmarks, and Dhrystone reports its own rate |

**Debugging**

| | |
|---|---|
| `trap` | &#9733; an example trap handler -- it installs a trap from system state, so from an ordinary program it stops. Run it by path; trap is also a shell builtin.<br>**How:** The system-state trap-handler example: it installs a trap from system state. Ask for it by PATH -- `/dd/CMDS/trap' -- because `trap' is also a bash builtin, and the builtin answers first, silently. |

**Libraries**

| | |
|---|---|
| `libsplit` | Split a linker library into its component modules<br>`Syntax   : [<opts>] {<library>} [<opts>]` |

**Source checking**

| | |
|---|---|
| `bcheck` | &#9733; count brackets in a source file and report a mismatch.<br>`Syntax: bcheck [<opt>] [<filename>]` |
| `ccheck` | &#9733; C program checker -- matching brackets, quotes, comment brackets, and indentation that disagrees with them<br>**How:** Checks C source for mismatched brackets, quotes and comment markers, and for indentation that disagrees with the nesting. Needs cio. |
| `cdecl` | explains a C declaration in English and writes one from English: `explain int *p' answers `declare p as pointer to int', and `declare x as pointer to function returning int' answers `int (*x)()'<br>`[] means optional; {} means 1 or more; <> means defined elsewhere` |

**Source formatting**

| | |
|---|---|
| `cb` | &#9733; the C beautifier: indents C source into a readable layout, standard input to standard output<br>`Usage:  cb <input.fil >output.fil` |
| `cpr` | print or pretty-list C source for paper: a title, a contents page, then the source with page and line numbers.<br>`Usage: cpr [-cCnNsS] [-T title] [-t tabwidth] [-p[num]] [-r[num]] [-l pagelength] [[-f] file] ...` |
| `ifdef` | reads C source and resolves its #ifdefs, writing what is left: -D<name> defines a name and -U<name> undefines it, so `ifdef -DOSK f.c' keeps the OS-9 arm and drops the others. -t prints the table it built<br>`Syntax: ifdef [<opts>] [<file>] [<opts>]` |
| `indent` | reformat a C source program for readability<br>`Syntax: indent [<opts>] [<inpath> [<outpath>]] [<opts>]` |
| `patch` | applies a diff to a file, the way `diff' made it: `patch <file> <diff>', or the diff on standard input.  It keeps the original beside the result as <file>.orig.  It could not finish until 2026-09-18 -- its port opened files with Unix modes, where OS-9 reads mode 0 as no access at all |
| `scpp` | &#9733; the selective C preprocessor: expands only the macros you name and leaves the rest of the source as it was. `scpp -MWIDTH prog.c' interprets WIDTH alone; -D defines one<br>**How:** `scpp -MNAME file' copies the C source to standard output expanding only name -- its #define disappears and each use becomes the value -- and leaves every other macro, #include and #ifdef untouched. Name several with -M"A B"; -DNAME=value defines one; -C keeps comments; -I adds an include directory. |
| `unifdef` | resolve #ifdef sections in C source for one symbol: -d<sym> keeps its branch, -u<sym> the other.<br>**How:** Its option is `-d<sym>' -- lower case, no equals -- and `-u<sym>' for the other side. `-DOSK' is refused with its own help, which reads like the program working and is not. |

**Source navigation**

| | |
|---|---|
| `ctags` | generate a vi tags file from C source (BSD)<br>`ctags: illegal option -- ?` |
| `cxref` | &#9733; C cross-reference lister -- numbered listing + symbol table<br>`Syntax:		cxref [-opts] [path]` |
| `etags` | makes a tag table -- the index an editor uses to jump to where a name is defined. It reads C, LaTeX, Lisp, Scheme, Pascal, Fortran and more, and writes TAGS for emacs or, with -e set the other way, the form vi wants<br>`Syntax: etags { [<opts>] <path> }` |
| `rdoc` | &#9733; reverse documentation: C source in, structure chart out |
| `xrf` | C cross-reference generator -- it reads its language table C.XRF from the current data directory; the disk ships one in DOC/xrf.<br>**How:** Wants two files in the data directory, not on the command line: its language table as `C.XRF' (the disk has it as DOC/xrf/c.xrf -- copy it) and the source you name. Given both it prints a full cross-reference: every identifier with the lines it appears on. |

**Tags**

| | |
|---|---|
| `ctags.elvis` | elvis 1.7's ctags; CMDS/ctags is the BSD one<br>`usage: ctags [flags] filenames...` |
| `ref` | Look up a C function's declaration from a tags file<br>`usage: ref [-t] [-c class] [-f file] tag` |

</details>

## Compilers & build

*C compilers and their passes, assemblers, linkers, make and parser generators.*

<details><summary>39 programs</summary>

**Alternates**

| | |
|---|---|
| `m4_0.5` | &#9733; a second build of the m4 macro processor, kept under its version number<br>`Syntax   : m4 [<opts>] [<files>]` |

**Assemblers & linkers**

| | |
|---|---|
| `as0` | 6800/6802 cross-assembler, one of the six xasm tools: `as0 file - l s' assembles with a listing (l) and a symbol table (s), the options after a lone `-'. A sample source for each of the six ships in DOC/xasm. None of the six assembles 68000 code<br>**How:** Assemble the sample that ships with it: `as0 /dd/DOC/xasm/sample.a0 - l s' -- the options come after a lone `-', `l' for the listing and `s' for the symbol table. There is a sample for each of the six (sample.a0, .a1, .a4, .a5, .a09, .a11) and each is written for its own processor: as09 rejects the 6800 one, correctly. as11 is the one that takes its options without the `-'. None of these is a 68000 assembler. |
| `as09` | &#9733; 6809 assembler -- the one that targets the 6809 itself. It rejects 6800 source (`ldaa' is a 6800 mnemonic, not a 6809 one); DOC/xasm/sample.a09 is written for it |
| `as1` | 6801/6803 cross-assembler (xasm); see as0. Sample in DOC/xasm/sample.a1 |
| `as11` | 68HC11 cross-assembler (xasm). It lists by default and takes no `- l s'; a word after the file name is another source file. Sample in DOC/xasm/sample.a11 |
| `as4` | 6804 cross-assembler (xasm); see as0. Sample in DOC/xasm/sample.a4 |
| `as5` | 6805/68HC05 cross-assembler (xasm); see as0. Sample in DOC/xasm/sample.a5 |
| `assembler` | GSHELL front-end for the assembler -- the same full-screen menu as `gshell', headed `Assembler-SHELL V1.0'.  It does not assemble anything itself; `as0' and its five siblings are the assemblers<br>**How:** Full-screen: it takes over the display. **control-C gets you out**; none of q, Q, control-D or ESC do. |
| `lnk` | the RTF Fortran link driver; it calls l68 with /h0/LIB/sys.l, which is Microware's |
| `lnk.org` | as `lnk', the original build: the RTF Fortran linker driver. It wants `os9lib' resident, hands its line to `shell' and calls `l68' to link, and then wants the Fortran start-up code `fstart.r' -- whose source is SRC/rtf/rtfstart.a, assembled with your own r68. DOC/README-FORTRAN has the chain<br>**How:** `load /dd/CMDS/os9lib' first. Without it this calls F$Link for os9lib, gets E_MNF and exits printing nothing. DOC/README-RUNNING names the four programs that do this. |

**C compilers**

| | |
|---|---|
| `cpp` | Decus CPP, the public-domain C preprocessor: macros with arguments, `#if' arithmetic, `#include' and the rest.  It was built to stand in for Microware's own preprocessor pass and writes that pass's `#P' and `#5' line markers; `-A' turns those off and gives ordinary `#line' output.  Shares its name with the preprocessor your own OS-9 carries -- README-NAMES<br>**How:** Give it a C source file: `cpp t.c'. By default it writes Microware's `#P'/`#5' line markers, because it was built to replace their preprocessor pass; `-A' gives ordinary `#line' output instead. The file must be CR-terminated like everything else on this disk -- an LF-terminated one arrives as a single enormous line. |

**C toolchain**

| | |
|---|---|
| `cc1plus` | a GCC C++ compiler pass (1.40.3) in the GCC2 directory; the driver runs it |
| `cc2` | the GCC 2.x C compiler pass, in the GCC2 directory; the driver runs it, and -version reports it |
| `cc2plus` | a second GCC C++ compiler pass (2.5.8) in the GCC2 directory |
| `cccp2` | &#9733; the GCC 2.x preprocessor, in the GCC2 directory beside its driver<br>`GNU C Compatible Compiler Preprocessor (Version 2.5.6)` |
| `collect` | collect2: builds the table of global constructors and destructors a C++ program needs before linking<br>`Syntax   : collect [<opts>] {<file>} [<opts>]` |
| `compiler` | a full-screen menu in front of the C compiler -- CC-SHELL 1.0, 1988. It lists the directory a page at a time, a letter picks the file to compile and the same letter in lower case asks for arguments first; `.' changes directory and `!' leaves the menu. Control-C is what gets you out of the program<br>**How:** Full-screen: it takes over the display. **control-C gets you out**; none of q, Q, control-D or ESC do. |
| `gcc` | &#9733; the GCC driver -- GCC139's and GCC2's share this name. They are not the same version, and neither is 2.x: GCC139/gcc answers `gcc version 1.39' and GCC2/gcc answers `gcc version 1.42', read out of `gcc -v'<br>`GNU C Compiler (Version 1.42)` |
| `gcc2` | &#9733; the GCC 2.x driver, and the only one that is: `gcc version 2.5.6'<br>`GNU C Compiler (Version 2.5.6)` |
| `gcc_cc1` | GCC 1.39 C compiler pass |
| `gcc_cc1plus` | GCC 1.39 C++ compiler pass |
| `gcc_cc2` | GCC 2.x compiler pass, under the name gcc2 forks |
| `gcc_cccp` | GCC 1.39 preprocessor<br>`GNU C Compatible Compiler Preprocessor (Version 1.39)` |
| `gcc_cccp2` | &#9733; GCC 2.x preprocessor, under the name gcc2 forks<br>`GNU C Compatible Compiler Preprocessor (Version 2.5.6)` |
| `gcc_collect` | GCC 1.39 collect2<br>`Syntax   : collect [<opts>] {<file>} [<opts>]` |
| `gpp` | the C++ driver -- and it is a GCC 1.x one.  GCC2/gpp says `gpp version 1.40.3 (based on GCC 1.40)' and GCC139/gpp says 1.37.1<br>`GNU C++ Compiler (Version 1.40.3 (based on GCC 1.40))` |
| `gpp_cc1plus` | GCC 2.x C++ pass, under the name gpp forks |
| `gpp_cccp` | &#9733; GCC 2.x preprocessor, under the name gpp forks<br>`GNU C Compatible Compiler Preprocessor (Version 2.5.6)` |
| `gpp_collect` | GCC 2.x collect2, under the name gpp forks<br>`Syntax   : collect [<opts>] {<file>} [<opts>]` |

**Make & generators**

| | |
|---|---|
| `bison` | GNU bison 1.19, the parser generator: reads a grammar and writes the parser in C, with -v leaving a report of the states and conflicts. Its skeletons are in LIB<br>`Bison 1.19 (OSK-Version 1.2) (c) 1993 Dipl-Kfm Norbert Kuehne` |
| `dmake` | &#9733; dmake 3.70 - parallel make with its own makefile dialect<br>`Usage:` |
| `flex` | flex, the fast lexical analyser generator: turns a rules file into a C scanner, lex.yy.c. DOC/flex/README-FLEX has what to know first<br>`Syntax   : flex [-bcdfinpstvFILT8 -C[efmF] -Sskeleton] [filename ...]` |
| `gmake` | GNU make: builds targets from a makefile's rules -- -f names the file, -n prints what it would do, -k keeps going past errors<br>`Usage: gmake [options] [target] ...` |
| `m4` | m4 macro processor.  It expands macros correctly, from a file or a pipe.  Its `syscmd' needs a `shell' module: it forks one by that bare name and is silent without it, so keep your own shell loaded -- DOC/README-SHELLS<br>`Syntax   : m4 [<opts>] [<files>]` |
| `make` | &#9733; make -- maintains a target. Two rules catch people: a command line must begin with a TAB (which will not survive being typed at this terminal, so copy DOC/make/demo.mk rather than echoing one), and a recipe must have no shell metacharacter -- `cp a b' runs, `cat a > b' gets `That path name doesn't lead to a file'.  DOC/STATUS has both Shares its name with a utility of your own -- README-NAMES<br>**How:** It works. Copy `/dd/DOC/make/demo.mk` rather than writing a makefile at the shell -- a command line must begin with a TAB and a tab does not survive being typed at this terminal. And keep shell metacharacters out of a recipe: `cp a b` runs, `cat a > b` gets "That path name doesn't lead to a file", because make forks bash with the line as a pathname rather than with -c. The default rules are in default.mk beside it, and make looks for that along your PATH. |
| `makeinfo` | GNU makeinfo -- Texinfo to info<br>``makeinfo: unrecognized option `-?'`` |
| `yacc` | yacc parser generator, rebuilt `-qm' from SRC/effo_yacc. It reads a grammar and writes y.tab.c into the data directory.  `bison' is the other parser generator here and reports states and conflicts<br>`Syntax   : yacc [-dltv] [-b <prefix>] filename` |

**Translators**

| | |
|---|---|
| `a2p` | translates an awk program into a perl script: `a2p prog.awk > prog.pl', then `perl prog.pl file'. With no file it reads the awk program from standard input. Manual in DOC/perl/a2p.txt<br>**How:** `a2p prog.awk > prog.pl' writes the perl version of an awk program; run it with `perl prog.pl file'. The translation sets $[ to 1 so fields count from 1 as in awk. The manual is DOC/perl/a2p.txt. |
| `p2c` | Pascal to C translator (GPL).  Reads LIB/p2c/p2crc; programs it emits link against LIB/libp2c.l<br>**How:** Translates Pascal to C. It reads LIB/p2c/p2crc at startup and stops with "file not found" if that is missing; programs it emits must be linked against LIB/libp2c.l. |

</details>

## Languages

*Interpreters and language systems beyond C.*

<details><summary>16 programs</summary>

**Adventure authoring**

| | |
|---|---|
| `adlcomp` | compile an ADL world<br>**How:** From ADL/DEMOS: `adlcomp tiny.adl -o tiny -i..'. -i names the directory holding standard.adl and is required for any world that includes it. |
| `adldebug` | the ADL debugger: loads a compiled world with its symbol table and dumps its tables -- objects, nouns, verbs, routines, strings -- over a range of numbers. ? lists the commands, q leaves<br>**How:** `adldebug tiny' on a compiled world; ? lists its commands, `o 0-4' dumps the first objects, q leaves. |
| `adlrun` | plays a compiled ADL world at a > prompt -- look, take, inventory, a direction; save and restore keep a game, quit leaves. AARD is ready to run in ADL/AARD: `adlrun aard'<br>**How:** `adlrun aard' in ADL/AARD plays the museum adventure at a > prompt; save and restore keep a game, quit leaves. |
| `adltouch` | stamps a compiled ADL world with a number: `adltouch <world> <n>' writes n into the first four bytes of the file, where the compiler left a #! line. Prints nothing<br>**How:** `adltouch tiny 7' writes 7 into the first four bytes of the compiled world; dump the file to see it. It prints nothing. |

**Fortran**

| | |
|---|---|
| `creadoc` | extract the documentation header (C++ ... C--) from every .f file in the current directory into creadoc.txt -- an early Fortran documentation generator.  It works through your own OS-9: it forks a shell twice, once for `dir -eadu *.f' to list the files and once per `del' to clear its temporary, so it wants a `shell' module and Microware's `dir' and `del' the way m4 wants a shell.  It reads each file name from column 54 of that listing, which is where Microware's dir puts it.  DOC/rtf/biory.doc is its output for biory.f. Source: SRC/rtf/creadoc.f |
| `fact` | prints the factorials 1! to 12! -- the Fortran example for this disk's RTF/68K compiler, source in SRC/rtf/fact.f. `load os9lib' first, as every RTF program needs.  Twelve is as far as a 32-bit integer goes: 13! overflows |
| `for` | the RTF/68K Fortran driver: it forks Microware's shell to run each compiler pass. At bash `for' is also the loop keyword, so ask for it by path there. Calling `rtf' directly needs no shell at all; see DOC/README-FORTRAN |
| `rtf` | RTF/68K, the Real-Time Fortran-77 compiler, v2.14 (CERN, 1987). `load /dd/CMDS/os9lib' first; then `rtf file.f' reads the Fortran and writes 68k assembly beside the source, and r68 and l68 from your OS-9 assemble and link it. `for' is its driver, which forks Microware's shell for each pass. Sources to try in SRC/rtf; the manual is DOC/rtf/rtfman.txt |

**Interpreters**

| | |
|---|---|
| `dds` | a BASIC interpreter in 1536 characters of obfuscated C: it prompts `Ok', takes numbered lines, and RUN, LIST, NEW, OLD, SAVE and BYE act at once.  Variables are a to z; FOR, GOSUB, GOTO, IF, INPUT and PRINT work.  Type in capitals<br>**How:** A BASIC interpreter in 1536 characters of obfuscated C -- the 1990 contest's Best Language Tool. It prompts with `Ok'. Type numbered lines to enter a program and bare commands to act: RUN, LIST, new, OLD <file>, SAVE <file>, BYE. Variables are the single letters a to z, and it understands FOR/NEXT, GOSUB/RETURN, GOTO, IF/THEN, input, PRINT and REM. All input must be uppercase. There is no error checking: a mistake ends the program rather than reporting itself. |
| `forth` | &#9733; TILE Forth, a Forth-83 in C. A source file named on the command line is loaded first -- `forth fibonacci.tst' in lib/tile/TST -- and then it prompts silently: `2 3 + . cr' prints 5, a colon definition makes a new word, words lists the vocabulary, bye leaves. lib/tile holds its source library and TST twenty-two test programs; sixteen manuals in DOC/forth<br>**How:** Type `2 3 + . cr' and it answers 5; `: squares 11 1 do i dup * . loop cr ;' then `squares' prints them; `words' lists its vocabulary; `bye' leaves. A source file is a command-line argument -- `forth fibonacci.tst' in lib/tile/TST loads it and gives you the prompt -- because `include' is defined in the library, not the kernel. The library and its twenty-two programs are in lib/tile and lib/tile/TST. |
| `lua` | Lua 3.0, a small scripting language. `lua <file>' runs a script -- `lua hello.lua' in DOC/lua/examples prints hello world -- and with no file it reads one from standard input; -v prints the version. Eight example scripts are in DOC/lua/examples. luac compiles a script to bytecode, and to an OS-9 module that runc starts<br>**How:** `lua cf.lua' in DOC/lua/examples prints a temperature table; `lua hello.lua' says hello. Eight example scripts are there; -v prints the version. |
| `luac` | &#9733; Lua bytecode compiler: `luac -o out.lc in.lua'; -l lists the instructions as it compiles.  -m writes an OS-9 module instead of a bytecode file -- into `luac.out' unless -o names it -- and -x puts that module in the execution directory for `runc' to start.  -x needs a name: `luac -x prog.lua' writes nothing and reports success, where `luac -x -o prog prog.lua' installs it<br>**How:** `luac -l -o hello.lc hello.lua' compiles and lists the bytecode. `luac -x -o name script.lua' makes an OS-9 module in the execution directory for runc. |
| `perl` | Perl 4.036, a text-processing language. `perl script.pl' runs a script, `perl -e' runs a line of program, and with neither it reads the script from standard input; -v prints the version. system, backticks and piped opens go through $SHELL; fork is not supported. Library in LIB/perl, manual in DOC/perl/perl.txt, source and port notes in SRC/perl4<br>**How:** Perl 4.036. `perl -e 'print 6*7, "\n";'' prints 42; `perl script.pl' runs a file; -v prints the version. system and backticks go through $SHELL, which SYS/login sets to ksh. The library is in LIB/perl and the manual in DOC/perl/perl.txt. |
| `runc` | runs a Lua script that `luac -x' has compiled into an OS-9 module: `load greet', then `runc greet <args>'. The script reads its arguments from argv[1] onwards, with the count in argv.n<br>**How:** Compile with `luac -x -o greet greet.lua', `load greet', then `runc greet World'. The script reads argv[1] onwards; argv.n is the count. |
| `wam.sbprolog` | SB-Prolog 2.2, a full Prolog. Needs SIMPATH=/dd/SBPROLOG/MODLIB; `wam.sbprolog SBPROLOG/MODLIB/$readloop' from /dd gives the `?-' prompt, and halt. leaves. DOC/sbprolog has the manual and README- SBPROLOG<br>**How:** Needs SIMPATH=/dd/SBPROLOG/MODLIB (login sets it). From /dd: `wam.sbprolog SBPROLOG/MODLIB/$readloop' gives the `?-' prompt; after a solution ; asks for the next and Return accepts it; halt. leaves. |
| `xlisp` | XLISP 2.1, a Lisp interpreter with objects, at a > prompt; (exit) leaves. DOC/xlisp has the manual |

</details>

## Archives & compression

*Pack, unpack and shrink -- lha, zip, tar, arc, zoo, and OS-9 module libraries.*

<details><summary>33 programs</summary>

**Alternates**

| | |
|---|---|
| `compress_4.0` | compress 4.0, another edition of CMDS/compress<br>`Syntax   : compress [-cdfvV] [-b maxbits] [file ...]` |
| `gtar` | another build of GNU tar, taking the long +option spellings as well: `gtar +help' lists them<br>`This is GNU tar, the tape archiving program.` |
| `gzip020_csl` | &#9733; gzip 1.2.4, 68020, needs csl<br>`gzip020_csl 1.2.4 (18 Aug 93)` |
| `gzip68k_csl` | &#9733; gzip 1.2.4, 68000, needs csl<br>`gzip68k_csl 1.2.4 (18 Aug 93)` |
| `gzipcpu32k_csl` | &#9733; gzip 1.2.4, CPU32, needs csl<br>`gzipcpu32k_csl 1.2.4 (18 Aug 93)` |
| `lharcs` | C-LHarc 1.01, older than CMDS/lha 2.08<br>`C-LHarc for OS-9/68k Version 1.01   (C) 1989-1991 Y.Tagawa, Kai Uwe Rommel,` |
| `zoo_2.1` | zoo 2.1 (1991), newer than the 2.01 in CMDS; it reads what 2.01 writes and has an extended help under `zoo_2.1 H'<br>`Zoo archiver, zoo 2.1 $Date: 91/07/09 02:10:34$  (OSK port 91/07/22 reto/hcz)` |

**Compress a file**

| | |
|---|---|
| `compr` | a Lempel-Ziv-Welch file compressor, another edition of `compress': -v reports the saving, -d decompresses, and the .Z file replaces the original<br>`Unknown flag: '?'; Usage: compress [-dfvcV] [-b maxbits] [file ...]` |
| `compress` | compress and uncompress with Lempel-Ziv-Welch coding: `compress -c < file > file.Z' packs, `-dc' unpacks, and plain `compress file' replaces the file with file.Z.  Pipes are safe -- the shipped binary is the build with stdio's putchar double-evaluation fixed, 2026-09-18 Shares its name with a utility of your own -- README-NAMES<br>**How:** `compress -c < file > file.Z' packs and `compress -dc < file.Z > file' unpacks; plain `compress file' replaces the file with file.Z.  Its output is safe through a pipe as well as into a file: the shipped binary is the build whose putchar double-evaluation is fixed (SRC/hc_utils/README.OSK).  `compr' and `compress_4.0' are the other two compresses here. |
| `gzip` | GNU gzip 1.2.2: compresses a file to .gz and back again with -d; -l lists, -t tests, -1 to -9 trade speed for size<br>`gzip 1.2.2 (17 Jun 93)` |
| `jaw` | zcat in 22 lines, a 1990 obfuscated-C contest entry: `jaw < file.Z' writes out what compress packed<br>**How:** `jaw < file.Z' writes out what compress packed into file.Z, as zcat does. It reads a pipe as well as a file. Run as a copy whose name begins with `a' it decodes btoa's text instead -- its authors' shark archiver pipes the one into the other. |

**Create & extract**

| | |
|---|---|
| `ar` | Ar 1.2, an archive manager: gathers files into one .ar archive and compresses them as it goes -- -u adds, -t lists, -x extracts, -p prints a member<br>`Ar V1.2 - archive file manager` |
| `ar2` | &#9733; Ar 2.00, a later edition of `ar' with delete and move as well, and each file's attributes recorded<br>`Ar V2.00 - archive file manager` |
| `arc` | ARC 5.21, the archiver that came before zip: a adds, x extracts, v lists with the compression column, t tests, p prints a member<br>`ARC - archive utility, Version 5.21, created on 04/22/87 at 15:05:21` |
| `cat` | &#9733; concatenates files to standard output: -n numbers the lines, -v shows control characters, -s squeezes runs of blank lines<br>`Syntax: cat [<opts>] {[-] <path> [<opts>]}` |
| `lha` | LHa 2.08 -- create/extract .lzh archives<br>`LHa Vrs. 2.08 for OSK - revised Dec. 2, 1994  M.Haaland` |
| `lharc` | C-LHarc 1.00, the older sibling of lha: a adds to a .lzh archive, x extracts, l lists, t tests<br>`C-LHarc for OS-9/68k Version 1.00   (C) 1989-1990 Y.Tagawa, Kai Uwe Rommel` |
| `marc` | the arc archive merger -- `marc <target> <source> [names]' copies members from one .arc into another<br>`MARC - archive merger, Version 5.21, created on 04/22/87 at 15:05:10` |
| `shar` | Shell-archive creator, and one faulty check is all that stops it: its read-access test rejects every file that exists -- `No read access for file: <name>' on its own standard output, for world-readable files that `cat' reads, absolute or relative, with -a or without. Hand it a name that is not there and the check passes vacuously: it writes the whole shell-archive preamble, cut line and all, and only then fails at open. For making an archive here, use `tar', `zoo' or `lha'.<br>`shar: illegal option -- ?` |
| `tar` | GNU tar 1.10: c creates a Unix tape archive, t lists it, x extracts; v shows each file, f names the archive Shares its name with a utility of your own -- README-NAMES<br>`Syntax : tar [ctx][mfv] tarfile [file(s)...]` |
| `unshar` | unpacks a shell archive -- the form programs were posted to Usenet in -- with its own small interpreter, no Unix shell needed.  DOC/unshar/which6.shar is one to try it on<br>`unshar: illegal option -- ?` |
| `unzip` | &#9733; Info-ZIP unzip: opens a .zip and writes its files back, whether the archive came from elsewhere or from this disk's own `zip'. DOC/zip/sample.zip is one to try it on.  It extracts where it is standing -- `-d <dir>' writes nothing at all and still reports success, so chd to the directory you want the files in.  `zoo', `tar' and `gzip' are the other archivers here<br>**How:** It extracts where it is standing, and `-d <dir>' writes nothing at all while reporting success, so chd to the directory you want the files in first. It reads what this disk's `zip' makes once the temporary has been renamed. |
| `zip` | Info-ZIP zip 1.9: packs files into a .zip archive, deflating as it goes. The archive it builds is sound and `unzip' reads it back byte for byte -- but zip assembles it under a temporary name (_Z000003) and the rename onto the name you asked for fails, so `mv _Z* mine.zip' is the last step. Stand in the directory and use bare names at both ends: a pathname with a slash loses its leading one and cannot be unzipped back where it came from<br>**How:** It deflates into a temporary of its own -- _Z000003 -- and then cannot rename that onto the name you gave, so it stops with `Could not create output file'. The temporary is the archive: `mv _Z* mine.zip' and unzip reads it back byte for byte. Stand in the directory and use bare names, both when packing and when unpacking. |
| `zipnote` | Info-ZIP zipnote -- view/edit zip comments<br>`Copyright (C) 1990-1992 Mark Adler, Richard B. Wales, Jean-loup Gailly` |
| `zipsplit` | Info-ZIP zipsplit -- split a zip archive<br>`Copyright (C) 1990-1992 Mark Adler, Richard B. Wales, Jean-loup Gailly` |
| `zoo` | &#9733; zoo 2.01: archives files with -add, -extract, -list, -test, -delete and the rest; `zoo h' prints its help<br>`Zoo archiver, Version 2.01 (1988/08/25 12:43:57)` |

**OS-9 module libraries**

| | |
|---|---|
| `liborder` | &#9733; lists relocatable objects in the order you would merge them into a library -- `liborder a.r b.r c.r' prints them last first, which is the order l68 wants.  Measured: it reverses whatever it is given, and does not read a .l at all.  Handed a library or a plain file it takes the first bytes for an object header, reads a length from them and asks for that many, which floods `No more memory !!!'. `-modinfo' prints each object's public names. `liborder.os9' is the same program, a second build.<br>`liborder: Unimplemented option '-?'.` |
| `modbuster` | splits a file holding several OS-9 modules into one file per module, in the current directory or the one -w=<dir> names, each named for the module it holds.  It leaves an empty file called `?' behind as well -- what it makes of whatever follows the last module it recognises<br>**How:** Give it a file holding SEVERAL modules and it writes one file per module in the current directory. Use ksh to put yourself somewhere writable first. `/dd/CMDS/GAMES/cyberwar' looks like a candidate but modbuster hangs on it with no output at all; a single ordinary module (`/dd/CMDS/today') shows it working. |
| `unpacklib` | &#9733; takes an OS-9 library apart into the modules that were merged to make it, writing each as its own file; -verbose names each one and its size as it goes<br>`unpacklib: Unimplemented option '-?'.` |

**zip**

| | |
|---|---|
| `funzip` | &#9733; Unzip straight from a pipe -- funzip < file.zip<br>**How:** Unzips from a pipe rather than a file: `funzip < thing.zip > thing'. For a normal archive use unzip; zipinfo lists what is inside one. |
| `zipinfo` | &#9733; Info-ZIP zipinfo -- what is inside a zip archive<br>`ZipInfo:  Zipfile Information Utility v1.0 of 21 August 92` |

**zoo**

| | |
|---|---|
| `booz` | &#9733; extracts or lists a zoo archive: `booz l' lists, `booz x' extracts, `booz t' tests<br>**How:** Lists and extracts zoo archives: `booz l file.zoo' lists with a bare letter, `booz x' extracts. fiz repairs a zoo archive that will not open. |
| `fiz` | &#9733; repairs a damaged zoo archive by walking its directory entries |

</details>

## Encoding & conversion

*Between text encodings, line endings, Macintosh formats, ciphers and hashes.*

<details><summary>30 programs</summary>

**Audio**

| | |
|---|---|
| `sox` | &#9733; Sound eXchange -- audio format converter.  Sample .iff sounds are in DOC/sox<br>**How:** Converts between audio formats. There is no sound device here, so it converts files rather than plays them. Sample .iff sounds are in DOC/sox. Needs Microware's cio. |

**Ciphers & hashes**

| | |
|---|---|
| `caesar` | breaks a Caesar cipher, guessing the shift from how often English uses each letter; `caesar 13' applies a shift of its own, which makes it rot13 |
| `checksum` | &#9733; a 16-bit checksum of a file, or of part of one with -s for the offset and -n for the length<br>`Syntax:   checksum <file> [<file>...]` |
| `chksum` | &#9733; a 32-bit checksum of each file named, with -c to count bytes as well and -t for a total only<br>`syntax: chksum [-cehtv]	{file\|--\|-}...` |
| `crypto` | &#9733; cryptogram puzzle solver's assistant<br>**How:** `crypto -h' is the real option list and `-i' the interactive commands; its bare answer is two lines naming those. As a filter it ends the emulator session here, so read the help rather than piping through it. |
| `des` | &#9733; DES file encryption -- it writes `<file>.n' and removes the original.  It does not restore a file run through it twice with the same key (the result checksums 00000000), so for a round trip use `xcrypt'<br>**How:** It takes files and has no option flags at all -- `des file ...'. `-e' and `-?' are read as filenames and earn `Can't read -e.' |
| `md5` | the MD5 digest of each file named |
| `xcrypt` | &#9733; a file cipher that cannot be driven here.  It prints `en/decrypt <input-file> <output-file>' and stops, whatever it is given -- two filenames, a `-k' key, or nothing.  The binary carries a `Key:' prompt and a `your key is rather short' warning, so the key was meant to be typed, but nothing reaches it.  No source came with it.<br>`en/decrypt <input-file> <output-file>` |

**Macintosh**

| | |
|---|---|
| `binhex` | encodes a MacBinary file as BinHex 4.0, the text form Macintosh software was posted in<br>`File input options:` |
| `hexbin` | decodes a BinHex file back into the Macintosh file it carried<br>**How:** Decodes Macintosh BinHex (.hqx) files, which is how Mac software travelled by mail and BBS. binhex goes the other way; unsit opens StuffIt archives and macunpack opens PackIt ones. All trap-free. DOC/macutils has the package readme. |
| `macbin` | wraps a file in MacBinary, the form a Macintosh file with two forks travels in; -t and -c set its type and creator, and -d unwraps<br>`MacBinary file converter version 1.1` |
| `macsave` | unpack MacBinary files from standard input into `.bin' files in the current directory, making subdirectories for embedded folders.  It writes silently, as its manual page says.  `macbin' is the translator that makes a MacBinary file.  DOC/macsave/macsave.1.<br>**How:** Its silence is correct and documented: DOC/macsave/macsave.1 says it "reads standard input and silently writes the file(s) it contains". `macbin' makes the MacBinary it wants, and the pair round-trips. |
| `macstream` | Read a MacTerminal file stream.  It measures the file before it reads it and answers `Short file <name>' for anything too small to be one<br>`File input options:` |
| `macunpack` | opens PackIt archives from a Macintosh<br>`File output options:` |
| `mcvert` | converts between MacBinary and BinHex either way: -U makes the BinHex for uploading, -D takes it back to MacBinary for downloading<br>`Mcvert V1.05 By Doug Moore` |
| `UnMacpack` | Unpack MacPack format.  Named for its module, which is UnMacpack rather than unmacpack<br>`File output options:` |
| `unsit` | opens StuffIt archives from a Macintosh: -l lists, -r and -d take one fork only<br>`unsit: unknown option -?` |

**Text encodings**

| | |
|---|---|
| `atob` | decodes what btoa encoded, back to the bytes<br>`Bad args to atob` |
| `bcd` | prints text as an 80-column punched card, the holes marked in each row: `bcd OS-9' |
| `btoa` | encodes a binary file as printable text, five characters for every four bytes with a checksum on the last line -- denser than uuencode; atob decodes it<br>`Bad args to btoa` |
| `cuts` | &#9733; Coco Usenet Transfer Utility -- encodes a binary as text that will pass through electronic mail, in a form that survives gateways between ASCII and EBCDIC machines; `-d' decodes, which is the half worth having.  The encoder (`-e') asks for billions of bytes of memory, is refused, and writes empty data lines until it is stopped.<br>**How:** Coco Usenet Transfer Utility: it encodes a binary as mail-safe text and `-d' decodes a cuts file. Use `-d' for the half worth having; the encoder (`-e') asks for gigabytes of memory and is refused. |
| `mimecode` | encode or decode base64, MIME's transfer encoding. `mimecode -e' turns a file into printable base64 and `-d' turns it back; uuencode and btoa are the older kinds, this is the one mail and the web use.  Tim Kientzle's, from DDJ.<br>`Usage: mimecode <options>` |
| `morse` | writes text as Morse code -- dit and daw, or dots and dashes with -s<br>`morse: illegal option -- ?` |
| `ppt` | punches text onto paper tape: a row of holes for each character, with the sprocket hole down the middle |
| `todos` | &#9733; turns OS-9 line endings into DOS ones -- every CR becomes CR LF, and one stray LF lands at the end of the file.  It writes the converted text into todos.$$$.<n> in the data directory, not beside the file you named, and then forks OS-9's own `del' and `rename' to move it over the original.  Those come with your system; on this disk alone the move does not happen, and OS-9's rename wants a name rather than a pathname in any case.  Stand in the directory, give a bare name, and rename the result yourself -- or use `autolf -c -C -L' as a filter, which renames nothing<br>**How:** It writes the DOS version into `todos.$$$.<n>' in the directory you are standing in, not over the file you named -- it forks OS-9's own `del' and `rename' to finish and stops there. Rename the temporary yourself, or use `autolf -c -C -L < in > out', which renames nothing. |
| `toos9` | &#9733; turns DOS line endings into OS-9 ones -- CR LF back to CR -- and appends one 0xFF byte at the end. Like todos it leaves the converted text in toos9.$$$.<n> in the data directory, because it cannot rename that over the original; rename it yourself. `autolf -C' does the job as a filter<br>**How:** The same the other way round: the OS-9 version is left in `toos9.$$$.<n>' for you to rename, and it appends one 0xFF byte at the end. `autolf -C' does the job as a filter. |
| `translit` | transliterates text between alphabets by a table: KOI8, KOI7, ALT and GOSTCII Russian, Library of Congress and phonetic romanization, LaTeX; `translit -t koi8-lc.rus -i in -o out'<br>**How:** Converts text from one alphabet or coding to another by a table: `translit -t koi8-lc.rus -i in -o out'. Eighteen tables for Russian are in LIB/translit -- KOI8, KOI7, ALT and GOSTCII codings, Library of Congress, GOST and Pokrovsky transliteration, phonetic spelling and LaTeX -- and a table named without -t is taken the same way. Without -i and -o it is a filter. It will not write over an existing -o file. TRANSP names another table directory and TRANSF the default table. The manual is DOC/translit/translit.txt.A and .B. The post's examples are in SRC/translit/ORIG: example.ko8.UU and example.alt.UU are uuencoded, with DOS line ends that `autolf -C' turns into OS-9 ones. |
| `uudecode` | &#9733; undoes uuencode: writes the file named on the begin line back into the current directory<br>`ERROR: can't find -?` |
| `uuencode` | &#9733; uuencode. Give it one argument -- the input file -- and redirect: `uuencode myfile > myfile.uu'. Its own usage line prints `uuencode >outfile [infile] name', which fails with two arguments.<br>**How:** One argument, the file: `uuencode /dd/SYS/motd > out.uu'. Its usage line reads as though it wants two and with two it prints that line and stops. `uudecode' is what undoes it. |
| `uuexpand` | expands a file into a run of `0' and `1' characters, one per bit -- despite the shared prefix, unrelated to uuencode -- so it survives a copy between machines with different byte or character sizes; `uuexpand -u' (or `uuunexpand') reverses it<br>**How:** Expands a file into a string of 0s and 1s, one character per bit; despite the name it is unrelated to uuencode or uudecode. `uuexpand -u' (or `uuunexpand') reverses it. The -8/-16/-7 options choose the assumed character width, for portability across machines. |

</details>

## Communications

*Kermit in several builds, terminal sessions, and networking.*

<details><summary>96 programs</summary>

**File transfer**

| | |
|---|---|
| `fileserv` | &#9733; the UUCP file server, and it needs no remote site to try: it reads a mail message from standard input and obeys the commands in the body -- `reply <address>', `help', `get <file>', `dir' and `quit'. The help it answers from is SYS/UUCP/FileServ.help. It forks `rmail' BY BARE NAME to deliver each reply, so `load' rmail out of CMDS/UUCP first or it answers `cannot spawn process' -- a bare-name fork looks where chx points, not along PATH. It keeps its own log in LOG/FileServ |
| `fixtext` | &#9733; repair the line endings of a received text batch<br>`fixtext: A text file filter.  Removes escape sequences, expand tabs and change` |

**Kermit**

| | |
|---|---|
| `ckermit` | &#9733; C-Kermit 5A(190) BETA.14, 24 Jul 94 -- the cio build.<br>`Usage: ckermit [cmdfile] [-x arg [-x arg]...[-yyy]..] [ = text ] ]` |
| `kermit` | OS-9 Kermit Version 1 Release 5: serial file transfer and terminal emulation by command letter -- connect, send, receive, host-server, get, quit. `ckermit' is the C-Kermit with a command language; DOC/README-KERMIT compares the six Kermits here Shares its name with a utility of your own -- README-NAMES<br>`OS-9 Kermit Version 1 Release 5` |
| `kermit2` | Kermit Program Version 1 Release 6 -- the same command letters as `kermit', 5K smaller.  DOC/README-KERMIT compares all six<br>`Kermit Program   Version 1    Release 6` |
| `kermit3` | Kermit68K version 1.0.00, 01 July 1987 -- a different program from the other small ones: it puts up its own `Kermit68K>' prompt and reads a Kermit.ini, rather than taking command letters |
| `xkermit` | &#9733; the same version and banner as `kermit' -- OS-9 Kermit 1.5 -- in half the space, because it links cio rather than carrying stdio.  DOC/README-KERMIT<br>`OS-9 Kermit Version 1 Release 5` |

**Mail**

| | |
|---|---|
| `answer` | &#9733; replies to the messages in a folder one at a time: it clears the screen and asks `Message to:' for a recipient, checked against the alias table |
| `arepdaemon` | &#9733; the daemon autoreply relies on.  It reads /dd/USR/LIB/ELM/autoreply.data; without it, `Error 216 attempting fstat' -- though it still touches autoreply.log on its way there |
| `atp` | &#9733; ATP 1.40, an off-line reader for QWK mail packets -- the bundles a bulletin board packed a caller's messages into, so they can be read and replied to without staying connected. It reads `atprc' or `.atprc' from your home directory, or from the directory $ATP names; a working one for this disk is in DOC/ka9q, and DOC/ka9q/atp.doc documents every setting |
| `autoreply` | &#9733; send an automatic reply while you are away.  It resolves your mailbox by the session's numeric owner rather than $USER, so under this identity it reaches for a mailbox named `su' and stops there; turning autoreplying off does not need the mailbox and answers for real |
| `checkalias` | &#9733; check an alias resolves before you rely on it. `listalias' answers the same question and prints its result<br>`Usage: checkalias alias [alias ...]` |
| `disable` | &#9733; turns the terminal monitor off on a port, in its own words `Turn OFF MTSMon on <port>', which frees the line for something else to use -- a modem dialling out being why it sits with the UUCP set. `enable' turns it back on<br>`Syntax: disable <port>` |
| `dotilde` | &#9733; the mailer's tilde-escape handler: it reads a message from standard input and acts on the `~' commands in it, answering `Unrecognized tilde command' and `Continuing...type "." or <ESC> to end message...'<br>`================= Tilde Help =================` |
| `elm` | &#9733; the Elm mail reader itself -- full-screen, menu-driven<br>**How:** The full-screen mail reader. It opens on the folder that ships for this account, `~/SPOOL/MAIL/tester', showing one message. `readmsg 1' prints a message without opening the reader; `messages' counts the folder. Mail lives at /dd/SPOOL/MAIL/<user>, and SYS/login points MAIL at it. |
| `enable` | &#9733; turns the terminal monitor back on for a port, the counterpart of `disable'; -p holds the prompt back until a signal arrives<br>`Syntax: enable [<opts>] <port> [<opts>]` |
| `fastmail` | &#9733; send a file as mail without opening the reader.  It needs a delivery agent to deliver it<br>`/dd/CMDS/ELM/fastmail: illegal option -- ?` |
| `filter` | sorts incoming mail into folders by rule, as a pipe stage -- its own usage line begins with the pipe. The rules live at SYS/.elm/filter_rules; with none it says so and mails the message through. It wants a scratch device at /r0, and it leaves the terminal without its automatic line feed<br>`/dd/CMDS/ELM/filter: illegal option -- ?` |
| `frm` | &#9733; list who your mail is from, one line each.  On this port it answers `tester has no mail' for a folder that `messages' counts and `readmsg' prints, so use those two<br>**How:** Lists who your mail is from, one line each. Reads $MAIL, which SYS/login sets. |
| `lcasep` | &#9733; lower-cases everything it reads, standard input to standard output, or -f and -o for files. Mail addresses are matched in lower case, which is what it is for<br>`/dd/CMDS/UUCP/lcasep: illegal option -- ?` |
| `listalias` | &#9733; list the aliases you have, once newalias has compiled them: `home  os9-freeware (This Collection)'.  It builds an `egrep ... \| sort' pipeline and hands it to a shell, so `load' sort first or the fork misses it and you get the list unsorted with a `sort: nowhere found' line above it<br>`/dd/CMDS/ELM/listalias: illegal option -- ?` |
| `lmail` | &#9733; local mail delivery: `lmail <user>' reads a message on standard input and appends it to that user's folder in SPOOL/MAIL, taking its lock in SYS/.LOCKS/MAIL.LOCKS<br>`Syntax: lmail <user name> {<user name>}` |
| `mail` | &#9733; a mail reader and sender in one, from the UUCP set. `mail <user>' takes a message from the keyboard, a line holding one dot ending it, and files it in MAIL/ under that login name; `mail' on its own opens what is waiting and prompts, `?' listing the commands. It wants a scratch device at /r0 -- DOC/README-RUNNING says how |
| `mailx` | &#9733; reads and sends mail: `mailx' opens what is waiting, -r takes it newest first, and `mailx <address>' sends. -a names a file being replied to. It looks for a mailbox directory of its own rather than the mailbox file elm and frm use, and says so when it cannot find one<br>`mailx v2.1 (94Sep30)  --send and receive e-mail` |
| `makedb` | build smail's path-alias dbm: `makedb -o <name> <file>' writes <name>.dir and <name>.pag.  /dd/USR/LIB/SMAIL/palias is the source it defaults to<br>`/dd/CMDS/UUCP/makedb: illegal option -- ?` |
| `messages` | &#9733; counts and lists what is in a mail folder: `There is 1 message in your mailbox'<br>**How:** Counts what is in your mail folder: "There is 1 message in your mailbox". |
| `newalias` | &#9733; rebuild the alias database -- run it after editing aliases, and add -g for the system file.  `processed 2 aliases', `processed 6 aliases'<br>**How:** Rebuilds the Elm alias database from USR/LIB/ELM/aliases.text after you edit it. |
| `newmail` | &#9733; watch for mail arriving and say so.  -d reports the folder it is watching and its size<br>`/dd/CMDS/ELM/newmail: illegal option -- ?` |
| `nptx` | &#9733; smail's full-name permuter: it takes `<full name>' TAB `<login>', one per line, and answers with the pair reversed.  Anything else -- an address list, a bare name, the password file -- earns `format error: <the line>'<br>**How:** smail's full-name permuter, and its input format is the whole trick: one line of `<full name>' TAB `<login>' and it answers with the pair reversed. Any other shape -- an address list, a bare name, the password file -- earns `format error: <the line>', which is how it came to be described as an alias expander. |
| `pathalias` | works out how mail should be routed from a map of which site talks to which, and prints one line per destination: the site, then the bang path to reach it. -l names the site you are computing from<br>`/dd/CMDS/UUCP/pathalias: illegal option -- ?` |
| `philmail` | an off-line mail reader: it opens your mail file, steps through the messages with return and offers a reply; `q' quits<br>`/dd/CMDS/UUCP/philmail is an off-line mail reader for UNIX mail` |
| `printmail` | &#9733; format a message for a printer.  It forks `readmsg' by bare name, so load it first; then it prints the message the same way `readmsg' would<br>**How:** It forks `readmsg' by bare name, and OS-9 resolves a bare-name fork against the execution directory, never against PATH -- so it is silent from everywhere except /dd/CMDS/ELM. `load /dd/CMDS/ELM/readmsg' once and it works from anywhere: a resident module is found by name with no directory search at all. |
| `pwparse` | &#9733; reads a password file on standard input and prints the login name from each line, one to a line -- the form the mail system wants a user list in |
| `readmsg` | &#9733; prints selected messages from a mail folder, by number or by pattern: `readmsg 1' for the first<br>**How:** Prints messages from a mail folder: `readmsg 1' for the first. It reads the welcome message in /dd/SPOOL/MAIL/tester. |
| `rmail` | &#9733; deliver incoming mail (invoked by uuxqt, not by you). Given a local name it builds <mailbox>/<user>, and the mailbox here is a file, so it stops with `can't change to mailbox: /dd/SPOOL/MAIL/tester/tester'.  Given a `host!user' address for remote delivery it does not return at all<br>**How:** Local delivery builds <mailbox>/<user> and stops, because the mailbox here is a file: `rmail tester' answers plainly. `rmail "site!user"' for remote delivery does not return. |
| `smail` | &#9733; takes a mail address, works out the route to it from the map `pathalias' built, and hands the message to the mailer that carries it. -A prints the address it would map to and stops, -v says what it is doing and -d does both without delivering anything<br>`Usage:   /dd/CMDS/UUCP/smail [<options>] address...` |
| `uupoll` | &#9733; poll a site for waiting work.  It works silently: `uupoll nowhere' leaves /dd/SPOOL/uucp/nowhere/C.nowhereAPOLL, and the grade letter from -g goes into the name (`-gZ' -> ...ZPOLL)<br>**How:** Polls a UUCP site for waiting work, and it does the job in SILENCE -- which is why it reads as broken. `uupoll <site>' leaves /dd/SPOOL/uucp/<site>/C.<site>APOLL; the grade letter from -g goes into the name, so `-gZ' gives ...ZPOLL. Blars uucp; wants the `uucp' user, which SYS/password has. |
| `uux` | &#9733; run a command on another UUCP site<br>**How:** Runs a command on another UUCP site. This is BLARS uucp, which reads USR/LIB/UUCP/Config -- a different configuration from UUCPbb's SYS/UUCP. Both ship. |

**News**

| | |
|---|---|
| `bdecode` | &#9733; decodes a C News batch: it skips forward to the line `Decode the following with bdecode', decodes what follows and checks the CRC at the end. Given anything else it says `Missing header'. Source in SRC/cnews/input |
| `byteflip` | &#9733; reorders the bytes of every word it reads on standard input, so a dbz database written on one architecture can be read on another.  Four things say how: the word length, where each byte comes from, the word length again, and where each byte goes -- `byteflip 4 0 1 2 3 4 3 2 1 0' turns every four-byte word end for end.  Give it those numbers: with none the word length is zero and it reads zero bytes for ever<br>**How:** It is in CMDS/NEWS, and it reads standard input rather than a file. Four things say how to swap: the word length, where each byte comes from, the word length again, and where each byte goes -- `byteflip 4 0 1 2 3 4 3 2 1 0 < in > out' turns every four-byte word end for end, so `ABCDEFGH' becomes `DCBAHGFE'. With no arguments the word length is zero and it reads zero bytes for ever. Measured 2026-09-19. |
| `c7decode` | &#9733; the inverse of C News's c7encode: it reads the seven-bit-safe form a news batch is put into to cross a link that eats the eighth bit, and writes the eight-bit original back. Source in SRC/cnews/input |
| `dbz` | &#9733; builds and maintains C News's history index -- the .dir and .pag pair beside the history file that lets the news system find an article by message-id without reading the whole of it. `dbz database [file]...'<br>**How:** The news history database from C News: `dbz [-a] [-x] [-c] database [file]...'. Part of a news system. |
| `expire` | &#9733; delete news articles past their expiry date<br>`/dd/CMDS/UUCP/expire: illegal option -- ?` |
| `newshist` | &#9733; looks message-ids up in the news history and reports what it finds, or that there is no entry for them: `newshist "<id@site>" ...'. -df names a history file other than the system's<br>`/dd/CMDS/NEWS/newshist: unknown option -?` |
| `newslock` | &#9733; the news system's lock: `newslock <tempname> <lockname>' makes the lock by linking one name to the other, which is how a lock is made atomic on a Unix filesystem.  This C library has no link(), so it returns 1 and leaves nothing behind -- the same gap that stops zip, arc and todos finishing.  SRC/cnews/misc/newslock.c is four lines and says so<br>`Usage: /dd/CMDS/NEWS/newslock tempname lockname` |
| `postnews` | &#9733; post an article to a newsgroup<br>`/dd/CMDS/UUCP/postnews: illegal option -- ?` |
| `readnews` | &#9733; read Usenet news articles: it opens the reader and asks about each newsgroup in the active file not yet in .newsrc, then answers `**** End of newsgroups' when the news spool is empty<br>`readnews: read Usenet news articles` |
| `rnews` | &#9733; takes an incoming news batch apart and files each article under SPOOL/news. A batch is articles behind a `#! rnews <length>' line, which is what says where one ends and the next begins; -n names the group to assume and -x turns on debugging<br>`rnews [-x debug_level] [-n inital_newsgroup] [-z] newsfile` |
| `subscribe` | &#9733; add a newsgroup to your subscription list -- for one already in /dd/.newsrc but turned off, `Newsgroup X is now subscribed.' and `X! 1' becomes `X: 1' in the file. A group not in .newsrc at all is silently left alone, which both this and unsubscribe do<br>**How:** It works, and so does `unsubscribe' -- give it a group that IS in /dd/.newsrc. A group that is not there is silently left alone. |
| `unsubscribe` | &#9733; drops a newsgroup from your subscription list: `!' replaces `:' in /dd/.newsrc. For a group that is already off it prints `Newsgroup 684700s already unsubscribed.', because the string in the binary is `Newsgroup % is already unsubscribed.' with no conversion letter after the `%'<br>`unsubscribe: unsubscribe from Usenet newsgroup(s)` |

**TCP/IP**

| | |
|---|---|
| `finger` | &#9733; show what the system knows about a user: the home directory, the shell, and the .plan it would print; given user@host it asks that machine instead<br>**How:** `finger tester' reads the password file this disk ships and prints the account's home directory, its shell, and the .project and .plan it would show if they existed -- no network needed for a local name. `finger user@host' is the form that asks another machine. |
| `infoxpress` | a client for the InfoXpress information service, reached over a serial line |
| `msntp` | sets the system clock from a network time server, by SNTP: name the server and it asks one.  With no server named it listens for broadcasts instead and waits for one, which its own manual (DOC/msntp/msntp.1) describes and recommends against -- polling a server is the reliable way.  Either way it needs a network to reach<br>**How:** Sets the clock from a network time server. |
| `net` | KA9Q net -- TCP/IP over SLIP or AX.25: telnet, ftp, smtp<br>**How:** KA9Q net, Phil Karn's TCP/IP over SLIP or AX.25 -- the stack amateur radio ran on. Needs NETHOME, NETSPOOL and TMPDIR set and a real interface; see DOC/ka9q. |
| `osknet` | OSKNET -- TCP/IP for OS-9, Telnet, FTP, Ping and SMTP<br>**How:** Charles Hedrick's TCP/IP for OS-9 -- Telnet, FTP, Ping and SMTP. It needs a network interface. Its own documentation is nine files in DOC/osknet: start with howto.doc and useguide.doc. |

**Terminal & session**

| | |
|---|---|
| `aterm` | ATerm 2.6, a terminal emulator for a serial line: `aterm /t1'. Its configuration is in SYS/ATERM; run it from a login session rather than as the machine's first process. Manual in DOC/aterm, source in SRC/aterm<br>`ATerm : A terminal program for OS9/68000` |
| `cls` | clears the screen, reading TERM and the termcap to find out how. `clear' beside it does the same job from a different author; either will do<br>`Syntax: cls` |
| `connect` | &#9733; joins two paths -- your terminal and a remote device -- so what you type reaches one and what it sends comes back on the other. Both default to standard input and output, the switches before each path set echo, CR/LF and XON/XOFF for that path alone, and control-E quits<br>`Usage: connect [<switches>] [<path1>] [<switches>] [<path2>]` |
| `fkeys` | loads the user-defined keys of a VT220 from a file, so the function keys send what you want. Given no file it prints its syntax<br>`Syntax: fkeys [<path>]` |
| `initvdu` | &#9733; sets the login terminal up from its termcap entry. It knows particular VDUs; on one it has no definition for it says so and changes nothing, which is the answer rather than a failure. -d shows what it would send<br>**How:** It sets up specific VDU hardware. On a terminal it is not defined for, it answers "is not defined for this terminal". |
| `input` | the Unaxcess bulletin board's input helper: it copies standard input to standard output a line at a time |
| `resize` | ask the terminal how big its window is and print LINES and COLUMNS, which less and others read before the termcap's 24 by 80.  At the login bash, `resize' sets them -- type it again after dragging the window; `resize -s' prints setenv lines for your own OS-9's shell<br>`usage: resize [-s]` |
| `sbreak` | Send/clear an SS_Break signal on a serial path<br>`Syntax:   sbreak [/device]` |
| `setfont` | &#9733; load a downloadable terminal font -- setfont <path>. Given a font file it writes no byte to /term, to $PORT, or to a file $PORT names, and returns exit status 0.  With no argument it answers `usage: setfont <path>'.<br>`usage: setfont <path>` |
| `setterm` | &#9733; reports or sets the terminal type: `setterm' alone says what TERM names; give it a name to change it. When TERM names a terminal it does not know it falls back on SYS/setterm, the defaults file. DOC/setterm has the manual and a termcap.extra of further entries<br>**How:** `setterm' alone reports what TERM says; give it a terminal name to change it. Run with no arguments and a terminal it wants to configure it goes full-screen -- **ESC quits** (control-C also works, but ESC is the program's own way). SYS/setterm is the defaults file it falls back on when TERM names something it does not know, and DOC/setterm/termcap.extra has further entries you can add to SYS/termcap. |
| `tput` | prints what a terminal needs for a capability, read from termcap: `tput -Tvt100 clear' emits the clear-screen escape and `tput cols' prints 80.  The capability names are the System V ones -- clear, bold, cup, lines, cols<br>`Usage: tput [ -Ttype ] [ -e ] [ -nlines ] capname [ x y ]` |
| `tsmon2` | watches a terminal device and starts the login program when someone types RETURN on it -- the job your own `tsmon' does, with more control: -i starts login as soon as carrier appears instead of waiting for a key. Zeller, 1989<br>`**** TSMON2: de-luxe version of the timesharing monitor (c) 1989 by L.Zeller` |
| `vttest` | the VT100 compatibility test: a menu of pages for cursor movement, screen features, character sets, double-size lines, the keyboard, status reports, VT52 mode and VT102 editing, each saying what a correct terminal shows.  0 leaves<br>**How:** Full-screen menu of VT100 tests. Type a test's number and RETURN; each page says what a correct terminal should show, and RETURN moves on. 0 leaves, printing `That's all, folks!'. Run it on the terminal you mean to judge: the keyboard and reports tests read what that terminal sends back. |
| `wysecrack` | &#9733; probe a Wyse terminal: it sends the code that asks the terminal to identify itself (`Anybody out there?' is in the binary) and reads the reply to sense its baud rate. With a Wyse terminal on the line it answers; without one it waits.  Companion to wysetime, which sets that terminal's clock |
| `wysetime` | Wyse terminal clock-setter, in BASIC09.  `runb wysetime' prints the escape sequence a Wyse terminal reads to set its own display clock; run it by bare name at an OS-9 shell. |

**Terminal & transfer**

| | |
|---|---|
| `blastem` | XModem and YModem file transfer, written for the MM/1<br>`Syntax: Blastem [<opts>] {<filename> [<opts>]}` |
| `dld` | &#9733; receives a file with XMODEM -- FHL's, 1986. `dld <file>' starts it and control-X aborts; `uld' is the other half, sending one out<br>`dld version 1.4   (c) 1986 FHL` |
| `k` | Kermit file transfer, the short form: `k <file>...' sends the files named and `k' on its own waits to receive. It guesses text or binary per file unless told, and wants a serial line with a Kermit at the other end<br>`General Usage:` |
| `rxmod` | receives an OS-9 module over a serial line and enters it in the module directory -- the receiving half of `txmod'. It calls the VMod_trap handler that ships beside it in COMMS, so `load' that first. Source in SRC/serload [no military use -- EFFO-INFO]<br>**How:** It stops with `can't install Vmod Trap handler' and the handler is sitting beside it: `load /dd/CMDS/COMMS/vmod_trap' first. It then gets past the install and faults inside the trap, which is a different thing and worth telling apart. |
| `sterm` | a serial terminal emulator: -l'<port>' says which line to talk on and -e'<char>' sets the escape character that gets you back. Told of no port it says so and stops<br>`Sterm Ver. 2.0` |
| `tsu` | &#9733; makes the directories and files tterm expects before it is first used -- USR/TTERM and a dialling list named after you -- and reports each one it finds or creates |
| `tterm` | &#9733; a terminal emulator, VT100-ish: -l=<port> links it to a serial port, MODEM by default. `tsu' sets its directories up first and `xyt' does file transfer from inside it<br>`Tterm Version 2.30` |
| `txmod` | sends OS-9 modules out over a serial line to `rxmod' at the other end, which links them into the module directory there: -x sends everything in the execution directory and -l names the device to send on [no military use -- EFFO-INFO]<br>`4ETXMod - Err:  -? !` |
| `uld` | &#9733; sends a file out with XMODEM -- FHL's, 1986. `uld <file>' starts it and control-X aborts; `dld' is the other half, receiving into a file<br>`uld version 1.4   (c) 1986 FHL` |
| `xy` | XMODEM/YMODEM transfer.  `xy -?' prints the shared usage: send by naming files, receive by naming none; -A forces ASCII, -B binary, and -X/-Y/-K/-G/-C pick the protocol.  `z -?' lists the family's options too<br>`General Usage:` |
| `xydown` | XModem/YModem download, public domain.  It senses which the sender is using -- XModem, YModem or YModem-Batch -- and follows, and it converts line endings on the way in. Written for use inside Eddie Kuns' KBCom terminal program and stands alone.  Full source in SRC/xydown, notes in DOC/xydown<br>`XYDOWN ver. 1.1` |
| `xyt` | &#9733; X/Y/ZMODEM transfer for tterm<br>`xyt - version 1.02` |
| `z` | ZMODEM transfer.  `z -?' prints the usage for both.  $MODEM names the port; -p<port> overrides it<br>`General Usage:` |

**UUCP**

| | |
|---|---|
| `uucico` | &#9733; the transfer program itself -- dials, talks UUCP<br>`usage: uucico [opts] -r \| sys [sys...]  [opts]` |
| `uuclean` | &#9733; removes stale jobs from the UUCP spool, /dd/SPOOL/uucp, which SYS/UUCP/Parameters names, and rotates the log files. It walks every entry in the spool as if it were a directory, so a plain file there earns `can't change to directory'; harmless<br>`uuclean: removed old UUCP files, rotate UUCP and FileServ log files` |
| `uucp` | &#9733; queue a file copy to or from another site<br>`uucp:  unix to unix copy program` |
| `uulog` | &#9733; reads the UUCP and file-server logs and shows what was transferred: -s<site> narrows it to one remote site, -u<user> to one user, -d<days> to a day already past, and -f follows the log as it grows<br>`uulog: examine uucp or fileserver log files` |
| `uuname` | &#9733; lists the UUCP sites this machine can reach; -l prints this machine's own name instead<br>`uuname --show local machine name or those of UUCP sites we talk to` |
| `uustat` | UUCP job status and control: what is queued, for which system and by whom.  `-s' limits it to one system, `-u' to one user, `-k' kills a job and `-r' rejuvenates one.  With no queue to report on it says `uucp is possibly active' and stops<br>`Syntax: uustat [<opts>]` |
| `uuxqt` | &#9733; runs the commands a remote UUCP site queued here. It first looks for a module called `procs' to see whether another copy is already going, then wants a site named, or `ALL' for every system in the Systems file; -xN turns on debugging and -q keeps it quiet |

**Web server**

| | |
|---|---|
| `authwn` | authentication helper for protected areas |
| `inetd` | &#9733; the internet daemon: it listens on a port and hands the connection to `wn'.  It opens `/socket', so it needs a TCP/IP stack presenting that device; without one it gets as far as `tcp protocol unknown'.  `inetd' alone prints its usage<br>**How:** The listener that hands incoming connections to wn. Needs a network. |
| `inetdc` | &#9733; what inetd forks for each connection.  1626 bytes with no message strings; inetd runs it, not you |
| `wn` | the WN web server, version 1.14.3. It is an inetd-style server: one HTTP request on standard input, one response on standard output, so run bare it waits. Its document root is compiled in as /h0/c/unid/wn_1.14.3/osk, which is on this disk, so mount the collection as /h0 as well as /dd and it answers `HTTP/1.0 200 OK' with the page. It serves the files named in that directory's index.cache; see wndex. Its manual is 30 HTML files in DOC/wn<br>**How:** A real HTTP server (WN 1.14.3, GPL). It starts and opens its log -- the path /h0/c/unid/wn_1.14.3/osk/logs is compiled into the binary, and that directory is on this disk so it can. To serve, it needs TCP/IP under it (KA9Q or osknet, in CMDS/NETWORK). It is an inetd-style server -- one request in on standard input, one response out -- so you can hand it a request by hand and read the reply. Its manual is 30 HTML files in DOC/wn. |
| `wn.stb` | WN's symbol table (a data module) |
| `wndex` | builds the index.cache WN serves a directory from. It works on the current data directory and ignores a directory given as an argument, so move there first (ksh's `cd' or the OS-9 shell's `chd') and run it by name. `Can't open ./index -- skipping it' means you are not where you think you are<br>**How:** Builds the index.cache WN will not serve without. It works on the current directory and ignores a directory given as an argument -- on this disk that means ksh, whose `cd' is a real chdir where bash's is not: `ksh -c "cd <dir>; /dd/CMDS/WN/wndex"'. On its own it says "Can't open ./index -- skipping it", which means you are not where you think you are. The site that ships at /dd/c/unid/wn_1.14.3/osk already has its cache built; that is WN's compiled-in document root. |

</details>

## Graphics & images

*The netpbm toolkit, JPEG, a ray tracer, and things that draw.*

<details><summary>195 programs</summary>

**Drawing & display**

| | |
|---|---|
| `draw` | a character-graphics drawing program: it rules a canvas across the terminal and you move a cursor over it laying down characters -- hjkl to move, p to lift and drop the pen, backslash to choose the character; `?' shows the keys<br>`syntax: draw [<opts>] <file> [<opts>]` |
| `loadmem` | copies a file into memory at a given address -- destination, upper limit and path, the addresses in hex; super user only. It says nothing when it works, so read the same address back with `savemem', which is its reverse<br>`Syntax   : LOADMEM <destinati address> <upper limit address> <path>` |
| `pdraw` | Pdraw 1.4: plots 2D and 3D data as PostScript. It reads an options file -- labels, whether to hide lines, whether to mark points -- prints every setting it took from it, then asks before sending the plot on. Answer and it writes `dataplot.ps' beside the data<br>`Pdraw V1.4  9/4/90` |
| `savemem` | writes a block of memory to a file -- from address, to address and path, the addresses in hex and the range inclusive, so 8000 8027 is 40 bytes. Super user only, and the file must not already exist: handed one that does it prints its syntax rather than overwriting. `loadmem' is its reverse<br>`Syntax   : SAVEMEM <from address> <to address> <path>` |
| `snap` | &#9733; writes what is on the terminal screen to a file -- `polaroid' unless you name another -- so a display can be kept. -s and -e take a range of lines rather than the whole screen<br>`syntax: snap {opt} [<file>] {opt}` |

**Hardware demos**

| | |
|---|---|
| `graph` | the Graph trap library itself -- a type-$0B module, not a program. It is what g, striche, apfel, sine, showpic, graphdemo, graphsave and wgen all call: `load' it and the trap installs. The module executes in supervisor state, so a program that calls it from the shell is entered and aborts on a supervisor-only instruction |
| `lissaj` | &#9733; draws Lissajous figures on a Tektronix graphics terminal. It asks four things first -- the x and y angular frequencies, how long to hold the picture, and the phase -- and then plots |
| `lorenz3d` | &#9733; Tektronix demo: the Lorenz attractor in 3D |
| `wgen` | Tektronix waveform generator.  With the `graph' trap library resident it runs and asks for a resolution and the intensity of each harmonic, then emits Tektronix plotting codes.  Bare, it aborts with `unintialized User Trap #5'.<br>**How:** It aborts with `unintialized User Trap #5, err=#227' until the `graph' trap library is resident: `load /dd/CMDS/GAMES/graph'. Then it asks for a resolution and the intensity of nine harmonics and draws the waveform. Give it ten numbers -- at end of input it draws for ever. `showpic' and `graphsave' need the same library and a display, so they abort either way. |

**JPEG**

| | |
|---|---|
| `cjpeg` | JPEG encoder (IJG).  Makes a JPEG from a PNM.  It wants LF between the fields of a PNM header where the netpbm here writes CR, so patch the three separators with `pbyte' first; DOC/STATUS has the offsets both ways.<br>**How:** Makes a JPEG from a PNM -- but not straight from a netpbm PNM. cjpeg wants LF between the header fields and this disk's netpbm writes CR, so it says "Bogus data in PPM file". Patch the three separators with `pbyte` first: for `ppmmake red 8 8` they are at offsets 2, 6 and a. DOC/STATUS has the full recipe both ways. |
| `cjpeg.070` | JPEG encoder, a build for another processor.  On the 68000 its twin `cjpeg' is the one to use; the .070 files are builds for a different CPU.<br>`usage: cjpeg.070 [switches] [inputfile]` |
| `djpeg` | JPEG decompressor, jpeg-5a.  Decodes a JPEG to a PNM.  Its output ends each header line with LF where the netpbm here wants CR, so patch the three separators with `pbyte' to pipe it on; DOC/STATUS has the offsets.<br>**How:** Decompresses a JPEG: `djpeg -pnm image.jpg > out.ppm`. The disk has one to try, SRC/jpeglib/JPEG_5A/testimg.jpg. Its output will not pipe into netpbm unpatched -- djpeg writes LF at the end of a PNM header line and netpbm here wants CR. `pbyte out.ppm 2 0d` and the same at the two later separators fixes it; DOC/STATUS has the offsets. |
| `djpeg.070` | JPEG decompressor, a build for another processor.  It decodes a JPEG, including one the 68000 cjpeg wrote; its companion encoder is cjpeg.070<br>`usage: djpeg.070 [switches] [inputfile]` |
| `rdjpgcom` | read the comment from a JPEG file<br>`rdjpgcom displays any textual comments in a JPEG file.` |
| `rdjpgcom.070` | read a JPEG's comment (IJG 0.70 build)<br>`rdjpgcom displays any textual comments in a JPEG file.` |
| `wrjpgcom` | write a comment into a JPEG file<br>`wrjpgcom inserts a textual comment in a JPEG file.` |
| `wrjpgcom.070` | write a JPEG's comment (IJG 0.70 build)<br>`wrjpgcom inserts a textual comment in a JPEG file.` |

**NETPBM: edit & analyse**

| | |
|---|---|
| `pbmclean` | removes lone pixels from a bitmap -- the speckle of a scan |
| `pbmlife` | one generation of Conway's Life on a bitmap |
| `pbmmake` | makes a plain bitmap of the size given: white, black or grey (a checkerboard)<br>`usage:  pbmmake [-white\|-black\|-gray] <width> <height>` |
| `pbmmask` | makes a mask from a bitmap: the background, found from the corners, white and everything else black<br>`usage:  pbmmask [-expand] [pbmfile]` |
| `pbmpscale` | enlarges a bitmap by an integer factor, smoothing the edges rather than making stairs<br>`usage:  pbmpscale scale [pbmfile]` |
| `pbmreduce` | shrinks a bitmap by an integer factor, dithering the averaged pixels<br>`usage:  pbmreduce [-floyd\|-fs \| -threshold] [-value <val>] N [pbmfile]` |
| `pbmtext` | sets a line of text as a bitmap, in its built-in font or one from a file<br>**How:** pbmtext <word> draws it as an image. `pbmtext os9 \| pbmtoascii' prints it on the terminal and needs no file at all -- the shortest demonstration of the 169 NETPBM programs. See DOC/README-NETPBM. |
| `pbmupc` | draws a UPC-A bar code as a bitmap from the three number groups that make one up -- product type, manufacturer and product -- with -s1 or -s2 for the two sizes<br>`usage:  pbmupc [-s1\|-s2] <type> <manufac> <product>` |
| `pgmbentley` | the Bentley effect: an image smeared as if painted, brightness shifting the pixels |
| `pgmcrater` | makes a cratered landscape -- a moon -- from a random number generator<br>`usage:  pgmcrater [-number <n>] [-width\|-xsize <w>]` |
| `pgmedge` | finds the edges in a greymap: it writes a new greymap in which a pixel is as bright as the contrast around it, so shapes come out light against dark. `pgmenhance' and `pgmnorm' are the other two that work on contrast |
| `pgmenhance` | sharpens a greymap by edge enhancement, -1 mild to -9 strong<br>`usage:  pgmenhance [-N] [pgmfile]  ( 1 <= N <= 9, default = 9 )` |
| `pgmhist` | prints a histogram of the grey levels in a greymap |
| `pgmkernel` | makes a convolution kernel for pnmconvol, of the size given<br>`usage:  pgmkernel [-weight f] width [height]` |
| `pgmnoise` | makes white noise: every pixel an independent random grey<br>`usage:  pgmnoise width height` |
| `pgmnorm` | normalises the contrast of a greymap, stretching it to the full range<br>`usage:  pgmnorm [-bpercent N \| -bvalue N] [-wpercent N \| -wvalue N] [pgmfile]` |
| `pgmoil` | paints a greymap again as if in oils: each pixel becomes the commonest value around it<br>`usage:  pgmoil [-n <n>] [pgmfile]` |
| `pgmramp` | makes a grey ramp -- left to right, top to bottom, rectangular or elliptical<br>`usage:  pgmramp -lr\|-tb\|-rectangle\|-ellipse <width> <height>` |
| `pgmtexture` | measures the texture of a greymap the way a pattern- recognition paper does: angular second moment, contrast, correlation, entropy and the rest<br>`usage:  pgmtexture [-d <d>] [pgmfile]` |
| `pnmalias` | anti-aliases an image, smoothing the edge between a foreground and a background colour<br>`usage:  pnmalias [-bgcolor <color>] [-fgcolor <color>] [-bonly] [-fonly] [-balias] [-falias] [-weight <w>] [pnmfile]` |
| `pnmarith` | adds, subtracts, multiplies or differences two images of the same size, pixel by pixel<br>`usage:  pnmarith -add\|-subtract\|-multiply\|-difference\|-minimum\|-maximum pnmfile1 pnmfile2` |
| `pnmcat` | puts images side by side (-lr) or one above another (-tb)<br>`usage:  pnmcat [-white\|-black] -leftright\|-lr [-jtop\|-jbottom] pnmfile ...` |
| `pnmcomp` | composites one image over another at an offset, through an alpha mask if one is given<br>`usage:  pnmcomp [-invert] [-xoff N] [-yoff N] [-alpha file] overlay [image] [output]` |
| `pnmconvol` | convolves an image with a kernel given as a PGM; pgmkernel makes one<br>`usage:  pnmconvol <convolutionfile> [pnmfile]` |
| `pnmcrop` | crops the white (or black) border off an image<br>`usage:  pnmcrop [-white\|-black] [-left] [-right] [-top] [-bottom] [pnmfile]` |
| `pnmcut` | cuts a rectangle out of an image: x, y, width, height<br>`usage:  pnmcut x y width height [pnmfile]` |
| `pnmdepth` | changes the maximum value -- the depth -- of an image<br>`usage:  pnmdepth newmaxval [pnmfile]` |
| `pnmenlarge` | enlarges an image by an integer factor, pixel for pixel<br>`usage:  pnmenlarge N [pnmfile]` |
| `pnmfile` | says what an image is: format, width, height, depth, raw or plain |
| `pnmflip` | flips an image left to right or top to bottom, transposes it, or turns it a quarter turn<br>`usage:  pnmflip [-leftright\|-lr] [-topbottom\|-tb] [-transpose\|-xy]` |
| `pnmgamma` | gamma-corrects an image, by one value or one per colour<br>`usage:  pnmgamma <value> [pnmfile]` |
| `pnmhisteq` | equalises the histogram of an image, spreading its grey levels evenly<br>`usage:  pnmhisteq [-gray] [-verbose] [-rmap pgmfile] [-wmap pgmfile] [pnmfile]` |
| `pnmhistmap` | draws the histogram of an image as an image<br>`usage:  pnmhistmap [-white] [-black] [-max maxvalue] [-verbose] [pnmfile]` |
| `pnminvert` | inverts an image -- a negative |
| `pnmnlfilt` | a non-linear filter -- alpha-trimmed mean, optimal estimation or edge enhancement -- chosen by the two numbers given<br>`usage:  pnmnlfilt alpha radius pnmfile` |
| `pnmnoraw` | writes an image in the plain form, its pixels spelled out as numbers you can read or edit |
| `pnmpad` | pads an image with a border of the widths given, white or black<br>`usage:  pnmpad [-white\|-black] [-l#] [-r#] [-t#] [-b#] [pnmfile]` |
| `pnmpaste` | pastes one image into another at a position, replacing, or- ing, and-ing or xor-ing the pixels<br>`usage:  pnmpaste [-replace\|-or\|-and\|-xor] frompnmfile x y [intopnmfile]` |
| `pnmrotate` | rotates an image by an angle up to ninety degrees, anti- aliased<br>`usage:  pnmrotate [-noantialias] <angle> [pnmfile]` |
| `pnmscale` | scales an image by a factor, to a width or height, or into a box (-xysize)<br>**How:** Scales an image: `pnmscale 0.5 file'. Given only a filename it takes that as the scale factor and then waits on empty input, reporting "bad magic number" -- which means you left out the factor, not that your file is bad. The same trap catches pnmdepth, pnmcut, pnmrotate and others. |
| `pnmshear` | shears an image by an angle, anti-aliased<br>`usage:  pnmshear [-noantialias] <angle> [pnmfile]` |
| `pnmsmooth` | smooths an image by convolving it with a mean kernel of the size given<br>`usage:  pnmsmooth [-size width height] [-dump dumpfile] [pnmfile]` |
| `pnmtile` | repeats an image to fill a width and height<br>`usage:  pnmtile width height [pnmfile]` |
| `ppm3d` | makes a red-blue stereo anaglyph from a left and a right image<br>`usage:  ppm3d leftppmfile rightppmfile horizontal offset` |
| `ppmbrighten` | changes the brightness and saturation of an image, or normalises it<br>`usage:  ppmbrighten [-saturation <+-s>] [-value <+-v>] [-normalize] [<ppmfile>]` |
| `ppmchange` | changes one colour in an image to another |
| `ppmdim` | dims an image by a factor, 0.0 black to 1.0 unchanged<br>`usage:  ppmdim dimfactor [ppmfile]` |
| `ppmdist` | turns a colour image into a greymap for monochrome printing, spreading the colours over the grey scale by frequency or by intensity<br>`usage:  ppmdist [-frequency\|-intensity] [ppmfile]` |
| `ppmdither` | dithers a colour image down to a fixed palette of red, green and blue levels<br>`usage:  ppmdither [-dim <num>] [-red <num>] [-green <num>] [-blue <num>] [pbmfile]` |
| `ppmflash` | brightens an image towards white by a factor, as a flash would<br>`usage:  ppmflash flashfactor [ppmfile]` |
| `ppmforge` | forges a planet, clouds or a starry sky from fractal noise<br>**How:** `-night' takes no argument. Written `-night 0' the 0 swallows the parse and -width/-height are ignored. And without `-night' it builds a PLANET at its default `-mesh 256', which ends the emulator session: `ppmforge -night -width 32 -height 16'. |
| `ppmhist` | prints a histogram of the colours in an image, commonest first<br>`usage:  ppmhist [-map] [ppmfile]` |
| `ppmmake` | makes a plain image of one colour and the size given<br>`usage:  ppmmake <color> <width> <height>` |
| `ppmmix` | mixes two images by a fade factor, 0.0 all the first to 1.0 all the second<br>`usage:  ppmmix fadefactor ppmfile1 ppmfile2` |
| `ppmnorm` | normalises the contrast of a colour image |
| `ppmntsc` | clamps an image's colours to the range NTSC television can carry, dimming by a factor<br>**How:** It takes a DIMFACTOR first -- 0.0 is black, 1.0 the original -- then the file. Without it you get its usage. |
| `ppmpat` | weaves a pattern -- gingham, madras, tartan, poles, squiggles, camouflage -- of the size given<br>`usage:  ppmpat -gingham\|-g2\|-gingham3\|-g3\|-madras\|-tartan\|-poles\|-squig\|-camo\|-anticamo <width> <height>` |
| `ppmquant` | reduces an image to a number of colours, or to the colours of a map image, with Floyd-Steinberg dithering if asked<br>**How:** A paletted converter needs a quantised image, and this is what quantises: `ppmquant 16 in.ppm > out.ppm'. Eight netpbm writers -- ppmtoicr, ppmtosixel, ppmtouil, ppmtopuzz, ppmtopict, ppmtopi1 and two more -- write ZERO bytes for a 24-bit PPM and correct files after it. |
| `ppmqvga` | quantises an image to a 256-colour VGA palette<br>`usage:  ppmqvga [-dither] [-verbose] [ppmfile]` |
| `ppmrelief` | embosses an image, lighting it from the side by arithmetic |
| `ppmshift` | shifts each line of an image sideways by a random amount up to the number given<br>`usage:  ppmshift shift [ppmfile]` |
| `ppmspread` | displaces each pixel by a random amount up to the number given -- a frosted-glass effect<br>`usage:  ppmspread amount [ppmfile]` |

**NETPBM: into PNM**

| | |
|---|---|
| `asciitopgm` | reads a text picture -- ASCII art -- as a greymap, each character's darkness a grey level<br>`usage:  asciitopgm [-d <val>] height width [asciifile]` |
| `atktopbm` | Andrew Toolkit raster to PBM |
| `bioradtopgm` | Bio-Rad confocal microscope image to PGM; -image picks one of a stack<br>`usage:  bioradtopgm [-image#] [Bioradfile]` |
| `bmptoppm` | Windows or OS/2 BMP to PPM<br>`usage:  bmptoppm [bmpfile]` |
| `brushtopbm` | Xerox doodle brush to PBM |
| `cmuwmtopbm` | CMU window manager bitmap to PBM |
| `fitstopnm` | FITS, the astronomers' image format, to PNM; -image picks a plane, -min and -max set the scaling<br>`usage:  fitstopnm [-image N] [-noraw] [-scanmax] [-printmax] [-min f] [-max f] [FITSfile]` |
| `fstopgm` | Usenix FaceSaver image to PGM |
| `g3topbm` | Group 3 fax file to PBM<br>`usage:  g3topbm [-kludge][-reversebits][-stretch] [g3file]` |
| `gemtopbm` | GEM .img (Atari and PC) to PBM<br>`usage:  gemtopbm [-debug] [gemfile]` |
| `giftopnm` | GIF to PNM; -image picks one of several in the file, -comments prints its comments<br>**How:** Reads a GIF into the PNM formats the other 168 converters work on -- try `giftopnm /dd/DEMO/gulls.gif \| pnmfile'. Important for anyone piping images out of the emulator: os9exec turns CR into CRLF on the way to the host, so a raw image containing byte 13 arrives corrupted. Keep binary inside OS-9 and convert with pnmnoraw before taking a picture anywhere else. DOC/README-NETPBM has the details. |
| `gouldtoppm` | Gould scanner file to PPM |
| `hipstopgm` | HIPS image to PGM.  The header is nine lines of text -- origin, name, frames, date, rows, columns, bits a pixel, packing, pixel format -- then history lines up to one holding a single dot, then one byte a pixel, so `printf' can make one<br>**How:** No HIPS image ships, and one is two commands: `printf "osk\rstrip\r1\rtoday\r2\r8\r8\r0\r0\r.\r" > x.hips' -- origin, name, frames, date, rows, columns, bits a pixel, packing, format, then a line holding one dot -- and `printf "0123456789abcdef" >> x.hips' for the pixels. |
| `hpcdtoppm` | Kodak Photo CD image to PPM, at one of five resolutions<br>`Error in Arguments !` |
| `icontopbm` | Sun icon to PBM |
| `ilbmtoppm` | Amiga IFF ILBM to PPM, HAM and extra-halfbrite pictures included<br>`usage:  ilbmtoppm [-verbose] [-ignore <chunkID>] [-isham\|-isehb] [-adjustcolors] [ilbmfile]` |
| `imgtoppm` | Img-whatnot, a PC paint program's format, to PPM<br>**How:** Reads the Img Software Set (AT&T Image-8) format; gemtopbm reads GEM IMG. Feed it an Image-8 file. |
| `lispmtopgm` | Lisp machine bitmap to PGM<br>**How:** This build handles at most 16 grey levels and says "depth is too large" otherwise. Run the image through `pnmdepth 15' before pgmtolispm. |
| `macptopbm` | MacPaint to PBM<br>`usage:  macptopbm [-extraskip N] [macpfile]` |
| `mgrtopbm` | MGR window-manager bitmap to PBM |
| `mtvtoppm` | MTV/PRT ray-tracer image to PPM.  The format is one line of width and height and then three raw bytes a pixel, so `printf' can make one<br>**How:** No MTV image ships, and one is two commands: `printf "4 2\r" > x.mtv' then `printf "0123456789abcdefghijklmn" >> x.mtv' -- a line of width and height, then three raw bytes a pixel. `mtvtoppm x.mtv > out.ppm' and pnmfile says PPM raw, 4 by 2. |
| `pcxtoppm` | PCX, PC Paintbrush's format, to PPM<br>**How:** Cannot read a pipe -- it seeks backwards in its input and stops with "error seeking past header". Write the PCX to a file and pass the filename. sgitopnm has the same limitation. |
| `pi1toppm` | Atari Degas .pi1 to PPM |
| `pi3topbm` | Atari Degas .pi3 to PBM<br>`usage:  pi3topbm [-debug] [pi3file]` |
| `picttoppm` | Macintosh PICT to PPM<br>`usage:  picttoppm [-verbose] [-fullres] [-noheader] [-quickdraw] [-fontdir file] [pictfile]` |
| `pjtoppm` | HP PaintJet file to PPM |
| `pktopbm` | TeX packed-font (.pk) characters to PBM, one bitmap per character<br>`pktopbm: This is PKtoPBM, version 2.4` |
| `psidtopgm` | a PostScript image -- the hex data of an `image' operator -- to PGM, given its width, height and bits per sample<br>**How:** Reads the hex digits of PostScript `image' operator data: `psidtopgm <width> <height> <bits/sample>' then the hex on standard input. `echo ffffffff00000000 \| psidtopgm 4 2 8' makes a 4x2 graymap, a white row over a black one. |
| `qrttoppm` | QRT ray-tracer output to PPM |
| `rasttopnm` | Sun raster to PNM |
| `rawtopgm` | raw grey bytes to PGM, given the width and height; -headerskip drops a header<br>`usage:  rawtopgm [-headerskip N] [-rowskip N] [-tb\|-topbottom] [<width> <height>] [rawfile]` |
| `rawtoppm` | raw RGB bytes to PPM, given the width and height and the byte order<br>`usage:  rawtoppm [-headerskip N] [-rowskip N] [-rgb\|-rbg\|-grb\|-gbr\|-brg\|-bgr] [-interpixel\|-interrow] <width> <height> [rawfile]` |
| `rgb3toppm` | three greymaps -- red, green and blue -- combined into one PPM; ppmtorgb3 splits it<br>`usage:  rgb3toppm <red pgmfile> <green pgmfile> <blue pgmfile>` |
| `sgitopnm` | SGI image to PNM<br>**How:** Cannot read a pipe -- same as pcxtoppm. Give it a filename or it reports "premature EOF". |
| `sirtopnm` | Solitaire image recorder file to PNM |
| `sldtoppm` | AutoCAD slide to PPM<br>`usage:  sldtoppm [-verbose] [-info] [-adjust] [-scale <s>]` |
| `spctoppm` | Atari compressed Spectrum picture to PPM |
| `spottopgm` | SPOT satellite image to PGM |
| `sputoppm` | Atari uncompressed Spectrum picture to PPM |
| `tgatoppm` | TrueVision Targa to PPM<br>`usage:  tgatoppm  [-debug] [tgafile]` |
| `xbmtopbm` | X11 or X10 bitmap, as C source, to PBM |
| `ximtoppm` | Xim image to PPM |
| `xpmtoppm` | X pixmap (XPM) to PPM |
| `xvminitoppm` | XV thumbnail (.xvpics) to PPM.  The format is `P7 332', a comment line, the size, then one byte a pixel indexing a fixed palette -- three bits of red, three of green, two of blue -- so `printf' can make one<br>**How:** No XV thumbnail ships, and one is two commands: `printf "P7 332\r#END_OF_COMMENTS\r8 2 255\r" > x.xv' then `printf "0123456789abcdef" >> x.xv' -- one byte a pixel into a fixed palette of three bits of red, three of green and two of blue. |
| `xwdtopnm` | X window dump (xwd) to PNM |
| `ybmtopbm` | Bennet Yee `face' bitmap to PBM |
| `yuvsplittoppm` | three YUV planes -- basename.Y, .U and .V, 4:2:0 -- to PPM, given the width and height<br>`usage:  yuvsplittoppm <basename> <width> <height> [-ccir601]` |
| `yuvtoppm` | Abekas YUV bytes to PPM, given the width and height<br>**How:** yuvtoppm <width> <height>. The dimensions are not stored in a YUV file, so you must supply the ones ppmtoyuv started from. |
| `zeisstopnm` | Zeiss confocal microscope image to PNM<br>`usage:  zeisstopnm [-pgm\|-ppm] [Zeissfile]` |

**NETPBM: out of PNM**

| | |
|---|---|
| `pbmto10x` | PBM to Gemini 10X printer graphics |
| `pbmto4425` | PBM to AT&T 4425 terminal graphics<br>`usage:  pbmto4425 [pbmfile]` |
| `pbmtoascii` | PBM to ASCII art, one character per 1x2 or 2x4 block of pixels -- how to see an image on a terminal<br>**How:** Prints an image as characters, so NETPBM can be seen on an ordinary terminal with no graphics. Try `pnminvert /dd/DEMO/sphere.pgm \| pgmtopbm -threshold -value 0.5 \| pbmtoascii'. |
| `pbmtoatk` | PBM to Andrew Toolkit raster |
| `pbmtobbnbg` | PBM to BBN BitGraph terminal graphics |
| `pbmtocmuwm` | PBM to CMU window manager bitmap |
| `pbmtoepsi` | PBM to an encapsulated PostScript preview bitmap (EPSI)<br>`usage:  pbmtoepsi [-bbonly] [pbmfile]` |
| `pbmtoepson` | PBM to Epson printer graphics |
| `pbmtog3` | PBM to Group 3 fax file<br>`usage:  pbmtog3  [-reversebits] [pbmfile]` |
| `pbmtogem` | PBM to GEM .img |
| `pbmtogo` | PBM to GraphOn terminal graphics |
| `pbmtoicon` | PBM to Sun icon |
| `pbmtolj` | PBM to HP LaserJet graphics, at 75 to 300 dots per inch<br>`usage:  pbmtolj [-noreset\|-float\|-resolution N] [pbmfile]` |
| `pbmtoln03` | PBM to DEC LN03 printer graphics<br>`usage:  pbmtoln03 [-left <nn>] [-right <nn>] [-top <nn>] [-bottom <nn>] [-formlength <nn>] [pbmfile]` |
| `pbmtolps` | PBM to PostScript for a DEC LPS printer, as line drawing |
| `pbmtomacp` | PBM to MacPaint<br>`usage:  pbmtomacp [-l left] [-r right] [-b bottom] [-t top] [pbmfile]` |
| `pbmtomgr` | PBM to MGR window-manager bitmap |
| `pbmtopgm` | blurs a bitmap into a greymap by averaging over a window w pixels by h<br>`usage:  pbmtopgm <w> <h> [pbmfile]` |
| `pbmtopi3` | PBM to Atari Degas .pi3 |
| `pbmtopk` | PBM character bitmaps to a TeX packed font (.pk) and its .tfm metrics<br>**How:** A TeX font tool: it wants a pkfile, a .tfm metric file and a resolution. Point it at a .tfm. |
| `pbmtoplot` | PBM to a Unix plot(5) file |
| `pbmtoptx` | PBM to Printronix printer graphics |
| `pbmtox10bm` | PBM to X10 bitmap, as C source |
| `pbmtoxbm` | PBM to X11 bitmap, as C source |
| `pbmtoybm` | PBM to Bennet Yee `face' bitmap |
| `pbmtozinc` | PBM to Zinc Interface Library bitmap, as C source |
| `pgmtofs` | PGM to Usenix FaceSaver image |
| `pgmtolispm` | PGM to Lisp machine bitmap |
| `pgmtopbm` | greymap to bitmap by dithering -- Floyd-Steinberg, ordered or clustered -- or by a plain threshold (-threshold -value)<br>**How:** without -threshold it is not reproducible: its dither differs every run, so any assertion on a length or a checksum downstream of it flaps. `pgmtopbm -threshold' when you need the same answer twice. |
| `pgmtoppm` | colours a greymap: `pgmtoppm colour' runs black to white through the colour, `pgmtoppm c1,c2' from one colour to another<br>`usage:  pgmtoppm <colorspec> [pgmfile]` |
| `pnmtoddif` | PNM to DEC DDIF image<br>`usage:  pnmtoddif [-resolution x y] [pnmfile [ddiffile]]` |
| `pnmtofits` | PNM to FITS<br>`usage:  pnmtofits [-max f] [-min f] [pnmfile]` |
| `pnmtops` | PNM to PostScript, scaled and centred on the page; -rle compresses<br>`usage:  pnmtops [-scale <x>] [-dpi <n>] [-width <n>] [-height <n>] [-rle\|-runlength] [-center\|-nocenter] [-turn\|-noturn] [pnmfile]` |
| `pnmtorast` | PNM to Sun raster<br>`usage:  pnmtorast [-standard\|-rle] [pnmfile]` |
| `pnmtosgi` | PNM to SGI image<br>`usage:  pnmtosgi [-verbatim\|-rle] [-imagename <name>] [pnmfile]` |
| `pnmtosir` | PNM to Solitaire image recorder file |
| `pnmtoxwd` | PNM to X window dump<br>`usage:  pnmtoxwd [-pseudodepth n] [-directcolor] [pnmfile]` |
| `ppmtoacad` | PPM to AutoCAD slide or DXB file<br>`usage:  ppmtoacad [-poly] [-dxb] [-white] [-background <col>]` |
| `ppmtobmp` | PPM to Windows or OS/2 BMP<br>`usage:  ppmtobmp [-windows] [-os2] [ppmfile]` |
| `ppmtogif` | PPM to GIF; -interlace, and -transparent names a colour<br>`usage:  ppmtogif [-interlace] [-sort] [-map mapfile] [-transparent color] [ppmfile]` |
| `ppmtoicr` | PPM to NCSA ICR (Telnet) graphics<br>`usage:  ppmtoicr [-windowname windowname] [-expand expand] [-display display] [-rle] [ppmfile]` |
| `ppmtoilbm` | PPM to Amiga IFF ILBM, HAM included<br>`usage:  ppmtoilbm [-ecs\|-aga] [-ham6\|-ham8] [-maxplanes\|-mp n] [-fixplanes\|-fp n] [-normal\|-hamif\|-hamforce\|-24if\|-24force\|-dcif\|-dcforce\|-cmaponly] [-hambits\|-hamplanes n] [-dcbits\|-dcplanes r g b] [-hires] [-lace] [-floyd\|-fs] [-compress\|-nocompress] [-cmethod none\|byterun1] [-map ppmfile] [-savemem] [ppmfile]` |
| `ppmtomap` | lists the colours in a PPM as a colour-map image, one pixel per colour<br>`usage:  ppmtomap [-sort] [-square] [ppmfile]` |
| `ppmtomitsu` | PPM to Mitsubishi S340-10 dye-sublimation printer graphics<br>`usage:  ppmtomitsu [-sharpness <1-4>] [-enlarge <1-3>] [-media <a,a4,as,a4s>] [-copy <1-9>] [-tiny] [-dpi300] [ppmfile]` |
| `ppmtopcx` | PPM to PCX<br>`usage:  ppmtopcx [-24bit] [-packed] [ppmfile]` |
| `ppmtopgm` | colour to greymap, by luminance |
| `ppmtopi1` | PPM to Atari Degas .pi1, sixteen colours |
| `ppmtopict` | PPM to Macintosh PICT |
| `ppmtopj` | PPM to HP PaintJet graphics<br>`usage:  ppmtopj [-center] [-xpos <pos>] [-ypos <pos>] [-gamma <val>] [-back <dark\|lite>] [-rle] [-render <none\|snap\|bw\|dither\|diffuse\|monodither\|monodiffuse\|clusterdither\|monoclusterdither>] [ppmfile]` |
| `ppmtopjxl` | PPM to HP PaintJet XL graphics (PCL)<br>`usage:  ppmtopjxl [-nopack] [-gamma <n>] [-presentation] [-dark]` |
| `ppmtopuzz` | PPM to the X11 puzzle game's file |
| `ppmtorgb3` | splits a PPM into three greymaps, .red, .grn and .blu, written beside the input |
| `ppmtosixel` | PPM to DEC sixel graphics<br>`usage:  ppmtosixel [-raw] [-margin] [ppmfile]` |
| `ppmtotga` | PPM to TrueVision Targa<br>`usage:  ppmtotga [-name <tganame>] [-mono\|-cmap\|-rgb] [-norle] [ppmfile]` |
| `ppmtouil` | PPM to Motif UIL icon source<br>`usage:  ppmtouil [-name <uilname>] [ppmfile]` |
| `ppmtoxpm` | PPM to X pixmap (XPM)<br>`usage:  ppmtoxpm [-name <xpm-name>] [-rgb <rgb-textfile>] [ppmfile]` |
| `ppmtoyuv` | PPM to Abekas YUV bytes |
| `ppmtoyuvsplit` | PPM to three YUV planes -- basename.Y, .U and .V, 4:2:0 -- written in the data directory<br>**How:** It takes a BASENAME and writes three files beside the data directory, not to standard output: <name>.Y, .U and .V. 4:2:0 subsampling, so a 32x16 image gives .Y = 512 bytes and .U = .V = 128. `yuvsplittoppm <name> <w> <h>' brings them back. |

**Plotting**

| | |
|---|---|
| `gnuplot` | &#9733; gnuplot 2.0 -- plots functions and data files.  Built-in help (SYS/gnuplot.gih); demos and sample data in DOC/gnuplot/demo<br>**How:** Type `set term' first -- it lists every output device it knows, and refuses to plot until you choose one. Its whole manual is built in: type `help'. Demos and sample data are in DOC/gnuplot/demo. Needs Microware's cio. |
| `tplot` | &#9733; plot data from files or standard input: it asks for the x and y intervals as two numbers each and the x, y divisions, then draws with the Atari ST's A-line graphics calls.  Answer the three questions here and it aborts where the drawing would start, so the dialogue is as far as it gets on a character terminal.  Measured 2026-09-19<br>`Usage : hiplot <-opt1> .. <-optn> <file1> .. <filen>` |

**Ray tracing & 3D**

| | |
|---|---|
| `mtst` | &#9733; exercises the C maths library: ceil, floor and round on a run of numbers, integer and floating side by side -- one of the small programs a port was checked with |
| `rayshade` | ray tracer 4.0.  It renders, and wants your own OS-9's `shell' resident: it builds its scene through popen(), which forks a module of exactly that name to run `cccp'. Load both -- `load /h1/CMDS/shell' and `load /dd/CMDS/GCC139/gcc_cccp' -- and it renders and reports its statistics.  DOC/rayshade/README-RAYSHADE has the detail.<br>**How:** Ray tracer 4.0, and it renders. It builds its scene through popen(), which forks your own OS-9's `shell` to run `cccp`: `load /h1/CMDS/shell' and `load /dd/CMDS/GCC139/gcc_cccp' first. |
| `rsconvert` | converts a rayshade 3 scene file to rayshade 4 syntax: `rsconvert old.ray > new.ray', or standard input to standard output |

**Viewers**

| | |
|---|---|
| `mgif` | a GIF inspector and viewer. `mgif -i file.gif' reports a GIF's structure and works on any terminal; displaying one needs an Atari ST, because flicker.c writes to ST graphics memory. Source in SRC/mgif; its GIF decoder is portable and is the part worth having<br>**How:** `mgif -i file.gif' inspects a GIF and prints its structure -- that works on any terminal. Displaying an image needs an Atari ST, because it writes straight to ST graphics memory. Try it on /dd/DEMO/gulls.gif. |

**X11**

| | |
|---|---|
| `basicwin` | the classic X11 demonstration: it opens a window on an X display and draws into it |
| `X11R6shl` | X11R6 shared library loader |
| `xengine` | an X11 demonstration: an engine animated in a window on an X display |

</details>

## Games

*Adventures, board and card games, arcade ports, dungeon crawls and puzzles.*

<details><summary>112 programs</summary>

**Adventure & fiction**

| | |
|---|---|
| `advcom` | the ADVSYS adventure compiler: turns .adv source into the world file advint plays. It opens its `@objects.adi' include by bare name in the data directory and keeps a file name in 20 characters, so copy osample.adv and objects.adi from GAMES/ADVSYS to a directory of your own and run it there: `advcom osample'<br>**How:** The ADVSYS compiler. It opens its `@objects.adi' include by bare name in the data directory and keeps a filename in 20 characters, so copy osample.adv and objects.adi from GAMES/ADVSYS to a directory of your own, `load /dd/CMDS/GAMES/advcom', then `sh -c "chd /dd/tmp/adv; advcom osample"'. It names every object it compiles and writes osample.dat. |
| `advent` | Colossal Cave Adventure, Will Crowther and Don Woods' mid-1970s original and the first text adventure -- self-contained, reads /dd/GAMES/adv/glorkz.  Needs this disk as /dd; mounted only as /h0 it cannot find its data.  Unrelated to advcom/advint.<br>**How:** Colossal Cave. Needs this disk as /dd -- it opens /dd/GAMES/adv/glorkz by absolute path, so mounted only as /h0 it cannot find its data. |
| `advint` | the ADVSYS adventure interpreter: plays a world advcom compiled, opened by bare name in the data directory -- `advint osample' starts you in the livingroom. GAMES/ADVSYS/README has the details<br>**How:** Plays an ADVSYS world. Build one first (see advcom), then run it where the .dat is: `load /dd/CMDS/GAMES/advint', then `sh -c "chd /dd/tmp/adv; advint osample"' -- you start in the livingroom, `n' goes to the hallway, `e' to a storage room with a key. |
| `infocom` | an interpreter for Infocom's Z-machine, a third and unrelated adventure system: plays the .z3 files in GAMES/INFORM (dejavu, hellow, shell -- Inform demonstrations, not the Infocom games). It writes its status-line cursor codes as literal text; infocom.tcap is the build for a terminal<br>**How:** A Z-machine. Plays the .z3 files in /dd/GAMES/INFORM -- the Inform demos dejavu, hellow and shell. |
| `infocom.tcap` | Infocom interpreter, TERMCAP build -- and it is the one to use at a terminal.  It puts a proper status line at the top of the screen (`Y2 Rock Room     Score: 0/2') where plain `infocom' writes the cursor codes for that line as literal text down the left margin<br>**How:** The termcap build of the Z-machine, and the one to use at a terminal: `infocom.tcap /dd/GAMES/INFORM/dejavu.z3' keeps a status line (room and score) across the top. Three Inform story files ship in GAMES/INFORM: dejavu, hellow, shell. |
| `napoleon` | a text adventure set in an English country house, where the Napoleons have left rather more behind them than furniture. The prompt is `(napoleon)' and it reads whole sentences, not just verb-noun: compass directions move you, `look' redraws the room, `inventory' lists what you carry, `get', `drop', `examine' and `read' handle things, `score' rates you, and `save' and `load' keep a game.  `quit' offers to restart. The scroll on the desk where you begin carries the licence. |
| `paranoia` | &#9733; the PARANOIA text adventure.  `Welcome to Paranoia!  As Philo-R-DMD you will die at times during the adventure... you will be given a new clone' -- six clones, one mission, RETURN to go on.  `float' and `savage' are the floating-point benchmarks of that name.<br>**How:** The PARANOIA text adventure. RETURN to go on, a letter to choose, `p' for your statistics, six clones. `float' and `savage' are the floating-point benchmarks on this disk. |

**Arcade & action**

| | |
|---|---|
| `bks` | Brickstop: catch the falling bricks on a paddle before they pile up to it -- `,' and `.' move, q leaves the game; high scores in GAMES/BKS<br>**How:** Full-screen. p starts a game: bricks fall at the left, and `,' or `<' and `.' or `>' move the paddle to catch them before the pile reaches it. q leaves the game and shows the high scores (kept in GAMES/BKS/hiscores); m returns to the menu and q there quits. ESC, which the menu calls pause, does nothing here. |
| `bugs` | a Dr. Mario lookalike: two-letter pieces fall into a bottle of bugs, and four alike in a row clear them; h and l move, a and s turn, space drops, p pauses, q quits<br>**How:** Full-screen Dr. Mario lookalike. j and k choose the level, then the speed, each accepted with Return. Pieces of two letters fall into the bottle, where the bugs are letters in reverse video or underlined; four of the same letter in a row, across or down, are cleared. h and l move the falling piece, a and s turn it, space drops it, p pauses and q quits. |
| `lander` | lunar lander -- space starts a game, a digit sets the power, x or k is vertical thrust, z/j and c/l the side retros.  Its score file is GAMES/lander.hs, looked for under /h0, so mount the disk there as well<br>**How:** Full-screen. Space starts a descent, a digit sets the engine power, `x' or `k' fires the main thruster and z/j and c/l the side retros. `q' quits. |
| `letters` | Letter Invaders, a typing game: words fall down the screen and typing one clears it before it lands; `-l5' starts at level 5, `-h' shows the high scores, kept in GAMES/LETTERS<br>**How:** Full-screen typing game. Words fall from the top of the screen, and typing a word's letters clears it; a word that reaches the bottom costs one of your lives. Every 15 words the level rises and the words fall faster. The bottom line shows the score, level, words, lives and words per minute. `letters -l5' starts at level 5, -b rings the bell for a mistake, and `letters -h' shows the top ten scores, kept in GAMES/LETTERS. The words come from GAMES/words. |
| `mw` | &#9733; Mazewar for up to eight players, each at a terminal of the same system, in one maze seen from above: `w' walks, `a' and `d' turn, `s' shoots, `m' drops a mine, `n' builds a wall and `Q' quits.  You score only by killing another player, and `mw -l=5' starts a computer player to hunt.  Its maze is USR/GAMES/LIB/MAZEWAR, found with this disk as /h0<br>**How:** Full-screen maze game for up to eight players on one system. `w' walks, `a'/`d' turn, `s' shoots, `m' mines, `n' walls, `Q' quits; `mw -l=5 >/nil &' first starts a computer player to play against. Needs cio; its maze is USR/GAMES/LIB/MAZEWAR. |
| `pacman` | Pac-Man in an ASCII maze.  It reads its board, help and score files from GAMES/pacman, asks your name and whether you want instructions, and then forks OS-9's own `tmode' to set the terminal `nopause noecho' before it draws -- tmode comes with your system, and with it to hand the maze lays out: you are OS9, chased by four ghosts named for old operating systems, and the keypad moves you (8 up, 2 down, 4 left, 6 right).  It positions with the ADM-3A sequence, ESC = row+32 col+32, so the board wants a terminal that reads that.  Without tmode it puts out one row of `+' and ends<br>**How:** Answer the name and instructions prompts, then play with the keypad: 8 up, 2 down, 4 left, 6 right, q quits. It draws with TeleVideo cursor codes (ESC = row col), so the maze paints only on a terminal that understands them; its board, help and score files are in GAMES/pacman. |
| `perp` | gather every diamond on the screen, pushing boulders and opening locks with keys: hjkl move, q restarts the level, S and L save and load, ^C quits; map in GAMES/PERP<br>**How:** Full-screen. Collect every diamond on the level: h j k l move, pushing boulders -- o can be crushed, O cannot -- and walking onto a key opens its lock. q gives up the level and starts it again, S saves the game to $HOME/cod.save and L loads it, ^L redraws, ^C quits. `perp 2' starts at the second level. The map and sprites are in GAMES/PERP. |
| `robots` | &#9733; robots: outrun them until they crash into each other. You are the `I', the robots are the `#' and a wreck is an `@'. Use -m, manual mode, one robot step per move of yours; without it the game is effectively unplayable. The keys are the numeric keypad 1-9 with 5 to stand still, `t' to teleport and `s' for a last stand<br>**How:** Play with `robots -m' -- manual mode, where the robots take one step per move you make. Keys are the numeric keypad 1-9 (5 stands still), `s' for last stand, `t' to teleport. Needs Microware's math module and a real TERM. |
| `snake` | snake arcade game.  You are the `I', the money is the `$' and the snake chases you; h/j/k/l move, `x' quits. Run it from a login session -- bare, with no TERMCAP, it bus errors instead; see DOC/README-BUSERR.  Some of its cursor moves arrive as literal text, so the board picks up stray characters as you play.  Playable, untidy<br>**How:** Full-screen. h/j/k/l move; reach the `$' before the snake reaches you. `x' quits. |
| `sokoban` | &#9733; Sokoban: push every packet (`$') onto a storage square (`.') without trapping one. Its fifty levels, help text and saved games are in GAMES/SOKOBAN, and it asks the system for your user name, so run it from a login<br>**How:** Wants a username, so run it from a login rather than a bare shell, or it stops with "cannot get your username". |
| `tet` | Tetris -- `p' plays; s/j and f/l move a piece, d/k turns it, space drops it, q quits to the high-score table it keeps in GAMES/tet.hs.  Needs a terminal, not a pipe<br>**How:** Tetris. `p' plays from the menu; s or j moves the piece left, f or l right, d or k turns it, space drops it, ESC pauses and q quits to the high-score table, kept in GAMES/tet.hs. Give it a real terminal: it does no terminal setup of its own (the raw-mode code in SRC/tet/tet.c is inside `#ifndef OSK'), so from a pipe it draws its board and reads nothing. |
| `thricken` | collect every diamond on the screen and the next level loads: hjkl move, s and r save and restore the level, q leaves and ^C quits; -l <n> starts at level n and -d plays a set of screens of your own.  Screens in GAMES/THRICKEN; DOC/thricken<br>**How:** Full-screen, the sequel to perp. Collect every diamond on the level and the next one loads: h j k l move, s saves the level position and r restores it, q leaves the game and ^C quits. `-l <n>' starts at level n (0 to 6 ship here) and `-d <directory>' plays a set of screens of your own -- DOC/thricken/screens.doc says how to write them. The panel names the level, the score, the moves and what you are collecting; the screens are in GAMES/THRICKEN and the high score file is GAMES/THRICKEN/scores. |
| `torus` | robots on a torus: each move you make, the robots close in -- lead them into each other to make scrap heaps; hjklyubn move, t teleports, q quits; scores in GAMES/TORUS<br>**How:** Full-screen. You are @; + robots step toward you each turn and # robots twice. Make them collide -- each collision leaves a scrap heap * that destroys robots running into it. h j k l y u b n move, . or w waits, t teleports to a safe square (the count is bottom left), r to a random one, a is antimatter, s sits tight to the end, q quits. The field's edges join; +h and +v flip how. `torus -s' shows the scores, kept in GAMES/TORUS. |
| `tt` | Tetris for terminals: , and / move, . rotates, space drops, s pauses, q quits<br>**How:** Tetris for terminals, full-screen: , and / move the piece, . rotates, space drops, s pauses, q quits. |
| `wanderer` | a Boulderdash-style maze game: dig through the earth for diamonds. Its thirty screens are in GAMES/WAND/screens, found with this disk as /dd<br>**How:** Full-screen. Dig through the earth for diamonds, forty-five on the first screen. `q' quits. Its thirty screens are in GAMES/WAND. |
| `worm` | the growing worm: you are the `@' and your body the `o's; h/j/k/l steer, H/J/K/L run, and with no key the worm keeps going.  Eat a digit to grow that much; the wall or your own body ends it.  `worm <length>' sets how long it starts<br>**How:** Full-screen. h/j/k/l steer, H/J/K/L run; with no key the worm keeps going. Eat the digits to grow. Control-C gets you out. |

**Board & card**

| | |
|---|---|
| `accordian` | Accordian solitaire: the deck is dealt in a row, and a stack slides one or three places left onto a card of the same suit or rank, closing the gap; win by squeezing it to one pile |
| `back` | &#9733; backgammon on a full board, points numbered 1 to 24, with the dice cup and the doubling status beside it. Single letters are the commands: R rolls, D doubles, H is the help, N starts a new game, Q quits<br>**How:** Single letters are the commands: R rolls, D doubles, H is the help, N starts a new game, Q quits. |
| `bjack` | blackjack, a 1990 obfuscated-C contest entry: one deck, a stake of $1000 or the one you name (`bjack 500'); a wager of 0 or end of file quits<br>**How:** `bjack [stake]' -- $1000 unless you name one; the largest bet is 500. It asks `Wager?' before each hand, then offers double, hit, split and insurance as the cards allow; answer y or n. A wager of 0, a negative one, or end of file quits. |
| `blackjack` | Las Vegas blackjack in BASIC09 -- `runb blackjack' asks your name and whether you want the rules, then takes a wager and deals: RETURN draws, `s' stands, `d' doubles down, `x' splits a pair, a wager of 0 ends the game (blackjak, in GAMES, is the SNOBOL4 one)<br>**How:** BASIC09 I-code: `load /h1/CMDS/runb' then `runb blackjack' (bare module name -- a pathname gives BASIC09 error 43). It asks your name and whether you want the rules, then takes a wager and deals: RETURN draws a card, `s' stands, `d' doubles down, `x' splits a pair; a wager of 0 ends the game. runb links the `math' trap handler from the execution directory, so leave chx at CMDS -- tested, plays a full hand. |
| `blackjak` | &#9733; Las Vegas BlackJack (SNOBOL4-in-C).  Data: GAMES/SNOBOL |
| `bs` | Battleships against the computer on a 10x10 grid: place your fleet, then hunt the computer's ships square by square with the hjklyubn cursor keys; sink the whole fleet to win |
| `c4` | Connect Four against the computer: the columns are lettered a to g, and you drop a piece by typing a column's letter. Line up four in a row to win; `q' quits.  Hard to beat |
| `canfield` | Canfield, the casino solitaire you bet on: earn units for each card worked up to a foundation, building down in alternating colours on the tableau; name a move by its two ends (s2, tf, 13, 2f), `ht' deals, `q' quits |
| `cfscores` | reports what canfield's betting has cost you and won you -- hands, inspections, games, runs, information, thinking time, and what you are worth after it all.  It reads the same GAMES/cfscores canfield writes; before your first game it says so and stops |
| `chess` | chess against the machine on a shaded board.  It asks for your colour, your name and a long or short game, then takes a move as two squares -- `e2' then `e4', two keystrokes each with no RETURN.  68k port, three engine versions built<br>**How:** It asks for your colour, your name and a long or short game, then takes a move as two squares -- `e2' for the piece and `e4' for where it goes. Each square is two keystrokes and needs no RETURN. |
| `craps` | casino craps at a full table: each bet is a key, then the amount and Return -- p pass line, d dont pass, f the field, h a hardway, o takes odds; r rolls, `?' lists every key and q leaves.  High roller list in GAMES/CRAPS<br>**How:** Full-screen casino craps with a rack of $100. Each bet is a key, then the amount and Return: p is the pass line, d dont pass, c come, D dont come, b a place bet, f the field, h a hardway, o takes odds and l lays them; s, a, 2, 3, y and u are the one-roll proposition bets. r rolls the dice, `?' lists every key, ^L redraws and q leaves, writing the high roller list to GAMES/CRAPS/craps.list. $CRAPSNAME names you there if you set it, otherwise $USER does. |
| `crib` | cribbage.  Needs TERM set, so run it from a login session -- bare it says `Unknown terminal type'<br>**How:** Full-screen cribbage, and it wants TERM -- run it from a login session. Answer the instructions question, choose a long or short game, and discard by naming a card, `7H'. Control-C gets you out. |
| `cribbage` | &#9733; cribbage -- offers instructions before it deals.  Needs TERM, so run it from a login session<br>**How:** The other cribbage, the same shape: TERM must be set, it offers the rules first, then cuts for the crib. Control-C gets you out. |
| `fish` | Go Fish against the computer: ask for a rank you already hold and take any the other player has, or `GO FISH' and draw; four of a rank makes a book, and the most books wins |
| `fuddle` | A chess variant that shuffles -- "fuddles" -- the pieces into fresh places and then plays a game from there. It asks whether you want white, draws a shaded board with the pieces listed above it, and takes moves as two squares, e2e4. |
| `gnuchess` | &#9733; GNU Chess, the build `gnuchess' runs: first on PATH, it reads its opening book at the compiled-in path /h0/usr/src/chess/gnuchess.book, which ships here, so it answers 1.e4 with a book move. Source `. termcap.entry' first, since it reads TERMCAP as the description itself. CMDS/GAMES/gnuchess, a second port under the same name, opens its book by bare name and draws the board reads TERMCAP as the description itself rather than as a filename -- and it draws the board, keeps both clocks and plays.  It opens its opening book by bare name, so it books when the book is the current directory; the CMDS build books from a fixed path and is what `gnuchess' runs<br>**How:** Full-screen chess. It reads TERMCAP as the terminal description itself rather than as a filename, so do `. /dd/SYS/termcap.entry' first; then it draws its time-control menu and plays. The build in CMDS/GAMES is the one that draws a board. |
| `gnuchessc` | GNU Chess built to be driven by `chesstool', a front end that draws the board itself -- so this one prints no board, by design and not for want of a file.  It says `Chess' and then announces moves: `1. ... e2e4', `My move is: c7c5'.  Its data, hash and language files ship at the path compiled into it and are found -- the `Chess' it prints is an entry in that language file, and a build that could not open one says `NO LANGFILE' instead.  Take it for the engine, not to watch a game<br>**How:** Its board display reads files from a compiled-in path; supply them there for a board. It still takes a move as `e2e4' and answers with its own. |
| `gnuchessn` | &#9733; GNU Chess with the 1989 display, which draws the squares as blocks of hashes so light and dark can be told apart on a terminal with no highlighting.  It is the only build here whose board answers to commands of its own -- `shade', `rv', `stars', `coords' and `p' change how it is drawn.  Source `. /dd/SYS/termcap.entry' first; moves go in as `e2e4'<br>**How:** As gnuchess: `. /dd/SYS/termcap.entry' first, then moves as `e2e4'. |
| `gnuchessr` | &#9733; GNU Chess with the plainest display -- pieces as letters, capitals for one side and lower case for the other, nothing that needs a terminal to draw.  It prompts `Enter #moves #minutes', takes a move and replies with its own.  It carries the book's full path, so unlike `nchess' it books wherever you run it, and `set' is how you lay a position out.  It prints no search table |
| `gnugo` | GNU Go 1.1, the Free Software Foundation's Go program: it plays Wei-Chi on a 19x19 board, gives black up to 17 handicap stones if you ask, and counts the score at the end.  Moves are a letter and a number, `D4'.  It needs no terminal setup |
| `kalah` | Kalah, the stones-and-bins game, and Pigeon Plague against the computer: pick the game, a skill level 2 to 12 and who goes first, then type a bin number; -2 asks for advice<br>**How:** Line by line. Type k for Kalah or p for Pigeon Plague, then the computer's skill level from 2 to 12, then 1 to go first or 2 to follow. Each of you has six bins of three stones; at your turn type a bin number 1 to 6 to sow its stones, 0 to show the board again, -2 or lower to ask the computer for advice (it looks that many moves ahead), or -1 twice to abandon the game. The manual, with the rules of both games, is DOC/kalah/kalah.doc. |
| `mastrm` | Master Mind: break the computer's hidden four-peg colour code in ten guesses, reading the `b' and `w' pegs each guess earns for right colour in right or wrong place |
| `mille` | &#9733; Mille Bornes -- the French car-racing card game<br>**How:** Full-screen Mille Bornes. `p' picks a card, `u #' plays one, `d #' discards, `s' saves the game and `q' quits. |
| `monop` | Monopoly for two to nine players: the Parker Brothers board game at the keyboard.  Each turn `roll' to move and buy the property you land on; `print' shows the whole board with owners, prices and rents, and `mortgage', `buy houses' and `trade' manage it.  Money and rent are tracked for you. `quit' ends the game |
| `nchess` | the build that shows its thinking: the same letter board as `gnuchessr', and under it a live table of the moves it is considering -- depth, score, node count and the line it is looking at -- redrawn as it searches.  Shot side by side with gnuchessr on the same script, this one prints the table and that one does not.  It opens its book by bare name, so it books when the book is in the current directory, and `edit' sets a position up.  The one to keep if you want to watch the engine rather than just play it |
| `othello` | Othello (Reversi) against the computer: place a disk to flank a line of the opponent's between it and one of yours and they all flip; the most disks when the board fills wins |
| `poker` | &#9733; Cold-hand Poker (SNOBOL4-in-C).  Data: GAMES/SNOBOL |
| `reversi` | Othello against the computer or another player at the same keyboard, with six strengths from Apprentice to Very Hard. It opens on a menu; the arrow keys or hjkl move the cursor, RETURN places a disk and `m' reopens the menu.  `-r' resumes a saved game.  A different author's program from `othello' |
| `saa` | Streets and Alleys solitaire: eight stacks and a foundation per suit; move a stack's top card onto the next rank up or home to its foundation, and order every card to win |
| `scrabble` | Scrabble against the computer on the full fifteen-by-fifteen board: the premium squares, the hundred-letter pool and the fifty-point bonus for laying down all seven letters at once. `hjkl' move the cursor, `H' or `V' enters a word across or down from there, `T' trades letters back into the pool, `A' asks the computer what it would play, `S' and `R' save and restore a game, and `Q' quits.  Its word list is GAMES/words. `-n' sets the number of players and `-m <n>' makes player n the computer. |
| `sol` | Klondike solitaire at the terminal: t thumbs the deck three cards at a time, m moves a card or a run, h lists the commands and q quits<br>**How:** Full-screen Klondike. Type a command and RETURN at the cmd prompt: t (or just RETURN) thumbs the deck three cards at a time; m with a source and a destination moves -- 1-7 for a run, d for the deck, a for an ace pile; a turns on the auto pilot; r shows the rules, h the commands; q quits. s, p, d and w are cheats, and it remembers. |
| `solx` | a harder solitaire with no deck: every card is dealt into runs, which may be split -- `m run position destination'; h lists the commands<br>**How:** Full-screen, and harder than sol: there is no deck, every card is dealt into runs that may be split, and the layout runs sideways so runs can grow long. m takes a run, the card position to split at, and the destination run (or a for an ace pile); h lists the commands and r the rules; q quits. |
| `tttt` | tic-tac-toe on a four-by-four board, so three in a row is not enough. Name a square as a column letter and a row digit, `b1'; `q' quits<br>**How:** Full-screen tic-tac-toe on a four-by-four board. Name a square as a column letter and a row digit, `b1'. `q' quits. |
| `vcraps` | casino craps, full screen: bet with p (pass line), c, dp, f, h and more -- type the amount and Return -- then r rolls; ? lists every bet, ESC abandons an entry, X quits<br>**How:** Full-screen casino craps with $1000 to start. Space clears each message at the bottom. p bets the pass line: type the amount and Return. r rolls the dice. c is a come bet, dp don't pass, dc don't come, f the field, b6 and b8 big 6 and 8, h22 to h55 the hard ways, a7 any seven, ac any craps; a number then c, p, dc or dp bets on that number. t takes a bet down, $ totals the bets, m reviews messages, ? lists all of it, ESC abandons an entry, X quits. -b sets the bankroll and -s plays single odds. |
| `yahtzee2` | Yahtzee 2.1: the poker-dice game on a curses scoreboard. Up to six players, human or computer, roll five dice up to three times a turn and bank each roll in one of thirteen categories.  Enter the player count; for each player, space toggles human or computer and `n' names them.  In play a digit holds a die, space rerolls, `b' shows the rules and `q' quits. High scores are kept in GAMES/YAHTZEE |

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
| `castle` | The Realm of the Wizard, a dungeon seen in the first person: the corridor ahead is drawn in character graphics beside your stats.  hjkl (or 4 2 8 6) turn, back up and step, `c' casts a spell, `i' opens the inventory, `<' and `>' take the stairs; control-E saves and `castle -r' resumes, `q' quits to the score list<br>**How:** Full-screen dungeon game seen in the first person. hjkl (or 4 2 8 6) turn left, back up, step forward and turn right, `.' turns around, `c' and a letter casts a spell (`a' tells you where you are), `i' is the inventory and ESC leaves it, `<' and `>' take the stairs. Control-E saves and leaves, `castle -r' resumes the saved game, `q' then `y' quits to the score list. Its data is GAMES/CASTLE. |
| `hack` | hack -- the original dungeon crawl NetHack grew out of<br>**How:** run it by its full path: `/dd/CMDS/GAMES/hack', not `hack'. It chdirs into its playground and then stats argv[0] to date-check saved levels, so a bare name cannot resolve and it stops with "Cannot get status of hack." Invoked in full it starts: "Are you an experienced player?". Its playground -- record, bones, rumors, help -- is in GAMES/HACK/PLAYGROUND. |
| `hackwish` | a hack cheat: replays hack until a wizard starts with a wand of wishing, wishes for what you name, and saves the game to carry on in hack |
| `larn` | &#9733; larn, a dungeon crawl: RETURN gets past the opening text; its saved games and score file are in GAMES/LARN/PLAYGROUND<br>**How:** Full-screen dungeon crawl. RETURN gets past the opening text. Control-C gets you out; its playground is GAMES/LARN/PLAYGROUND. |
| `moria` | UMoria 4.87, the dungeon crawl: roll up a character by race, sex and class, buy what you can afford in the town's shops, then take the stairs down after the Balrog.  `?' lists the commands, `^X' saves and `^K' quits.  Its data is USR/GAMES/MORIADIR, found with this disk as /h0<br>**How:** Full-screen dungeon crawl. SPACE past the news, then pick race, sex (m/f), ESC to keep the stats, class, and type a name; SPACE past the character sheet puts you in the town. `?' is the command list, `^X' saves and `^K' quits. It needs TERM set; its data is USR/GAMES/MORIADIR. |
| `nethack3` | NetHack 3.0f, the dungeon crawl grown out of hack: pick or build a character, then go down through the Mazes of Menace for the Amulet of Yendor.  `?' lists the commands, `S' saves and `Q' quits.  Its data is USR/GAMES/LIB/NETHACK3DIR, found with this disk as /h0; HACKDIR names another<br>**How:** Full-screen dungeon crawl. `y' lets it pick your character, SPACE clears each --More--, `?' is the command list, `S' saves and `Q' quits. It needs TERM set; its data is USR/GAMES/LIB/NETHACK3DIR. |
| `rogue` | the rogue 5.3 clone: explore a dungeon drawn as you go, fight what you meet and take the stairs down.  hjkl move, `i' is the inventory, ESC cancels a question, `Q' then `y' quits to the Top Ten.  Needs TERM set<br>**How:** Full-screen dungeon crawl. h, j, k and l move; `i' lists the pack and SPACE puts it away; `d' drops something and ESC cancels any question; `Q' then `y' ends the game and shows the Top Ten, kept in GAMES/ROGUE/rogue.scores. It needs TERM set, as SYS/login does. |
| `ularn` | ULarn -- the larn variant, and its data is complete<br>`Cmd line format: Ularn [-slicnh] [-o<optsfile>] [-##] [++]` |

**Other games**

| | |
|---|---|
| `arithmetic` | a drill in sums at the terminal: it asks a problem and keeps asking until the answer is right, and after every twenty prints the rights, wrongs and seconds per problem.  `-o' picks the operations from +-x/, `-r' the largest number; ^C stops it with the score<br>**How:** Line-by-line drill in sums. It prints a problem such as `3 + 4 =' and waits; type the answer and RETURN. A wrong answer gets `What?' and the same problem again, and after every twenty it prints the score. `-o +-x/' picks the operations (+ and - by default), `-r 12' the largest operand (10). ^C or end of input stops it with the score so far. |
| `ask` | the client for `wisecrack': it reads one line from /pipe/txtpipe and prints it, and says `No Wisecracks coming' when nothing is feeding the pipe. Start the server first -- `wisecrack &' -- and it answers<br>**How:** The reader for `wisecrack': it takes the next slogan from the pipe wisecrack writes to and prints it, one a call, in German. Start the server first -- `wisecrack &' -- or ask says "No Wisecracks coming". From EFFO forum 20. |
| `atc` | Air Traffic Controller: guide the planes on the radar from airport or entry point to the destination each one shows, at the right altitude, without letting two meet.  Talk to a plane by its letter -- `a' and a digit sets altitude and takes off, `t' and a direction key turns -- RETURN sends it and `?' shows what may come next.  `atc -l' lists the airports, `-g easy' picks one; ^C quits.  GAMES/ATC holds the airports and the score list<br>**How:** Full-screen air traffic control. `atc -l' lists the airports and `atc -g easy' picks one. Type a command to a plane by its letter: `a' and a digit sets altitude (and takes off), `t' and a direction key turns; RETURN sends it, `?' lists what may come next, ^L redraws and ^C asks to quit. Its airports are in GAMES/ATC. |
| `backgammon` | &#9733; backgammon against the computer, drawn as a board of numbered points. -n skips the instructions and -r gives you red; given a file it plays the game recorded in it<br>`Syntax: backgammon [<opts>] [<file>]` |
| `bandit` | a one-armed bandit: three reels, a payoff table beside them, and a bankroll of 100.  Answer the bet prompt with 0 to 5, watch the reels, and `q' at the prompt walks away with the total.  Source `. /dd/SYS/termcap.entry' first -- it reads TERMCAP as the description itself<br>**How:** A slot machine. Do `. /dd/SYS/termcap.entry' first -- it reads TERMCAP as the description itself. Then `n' skips the instructions, a number 0-5 is the bet, and `q' at the bet prompt ends with your total. |
| `convert` | starts the WORLD text adventure: run it and the game opens with its banner, the opening paragraph and a `>' prompt<br>**How:** It starts the `world' adventure -- run it and the game opens. |
| `corewar` | Core War: two Redcode battle programs fight for control of a circular memory.  `corewar <cycles> a.e b.e' runs the fight and maps the core -- a 1 or a 2 marks the cells each program holds -- as the cycles count down.  Assemble warriors with cwasm; twelve samples are in GAMES/COREWARS |
| `cwasm` | the Core War assembler: `cwasm w.rc' turns a Redcode warrior into the object file w.e that corewar loads.  Sample warriors are in GAMES/COREWARS |
| `cwdis` | the Core War disassembler: `cwdis w.e' prints a warrior object back as a numbered opcode and parameter table |
| `hotel` | &#9733; hotel -- two-player board game, played by coordinates<br>**How:** Full-screen: it takes over the display. **control-C gets you out**; q, Q, control-D and ESC do not. If it has a quit command of its own, its documentation in DOC/ will say. |
| `mkdict` | builds bog's dictionary from a word list in the current directory<br>**How:** Run it in /dd/GAMES/BOG, where bog's word list is; it is in CMDS/GAMES. |
| `mkindex` | builds the index bog reads its dictionary through, from the dictionary in the current directory<br>**How:** Run it in /dd/GAMES/BOG after mkdict; it is in CMDS/GAMES. |
| `nobs` | cribbage against the computer, a third one: it deals six cards, asks which two go to the crib, plays the hand and pegs the board above<br>**How:** Full-screen: it takes over the display. **control-C gets you out**; q, Q, control-D and ESC do not. If it has a quit command of its own, its documentation in DOC/ will say. |
| `shuffle` | a full-screen switch puzzle: a row of numbered switches, `Wich switch ?' and a move counter, where flipping one flips its neighbours; q quits. It wants TERM. For shuffling lines, `sort -r' and `tac' are the line tools<br>**How:** Full-screen: it takes over the display. **`q' quits**. |
| `ski` | Ski! -- down an endless slope a row a turn: R and L turn, J jumps, T teleports, I fires at the Snoman; Return waits<br>**How:** Line by line down an endless slope: each turn draws one row with you as the I, and the ? at the end of the line waits for a letter or Return. R and L turn you further right or left, J jumps and H hops, T teleports, I launches an ICBM at the Snoman (A) and D calls the Fire Demon. Trees Y, bare ground and ice # can hurt you, and the run ends when something bad happens. The manual is DOC/ski/ski.man. |
| `stone` | &#9733; the stones game (SNOBOL4-in-C).  Data: GAMES/SNOBOL |
| `teachgammon` | &#9733; backgammon that teaches you the game as you play<br>`Syntax: backgammon [<opts>] [<file>]` |
| `tess` | &#9733; Beyond the Tesseract, a text adventure whose puzzles draw on physics and mathematics: two-word commands, about two hundred words understood, and -f skips the title and scenario |
| `trek` | Star Trek at the Command: prompt -- choose a length, a skill and a password, then hunt the Klingons across the galaxy before time runs out.  `s' is the short-range scan, `l' the long range, `m' moves, `p' phasers, `t' torpedoes, `do' docks at a starbase; `help' lists every command and `terminate' ends the game.  `dump' saves it to trek.dump<br>**How:** Line-by-line game at a Command: prompt. RETURN past the banner, then answer the length (s/m/l), skill (n/f/g/e/c/i) and a password. `s' is the short-range scan, `l' the long range, `help' lists the commands, `terminate' ends the game and `n' at `Another game' leaves. |
| `trek73` | Star Trek battle at a Code [1-32] prompt: give a name, a sex and how many enemies, then fight by number or in words -- `damage'; 32 lists the commands; wait too long and a turn passes<br>**How:** Line-by-line battle at a Code [1-32] prompt. Give the captain's last name, a sex and how many enemy vessels (1-9), and the log opens. Commands go by number -- 32 lists them -- or in words: `damage' gives the damage report. A command must come within the turn time, 30 seconds unless `-d 60' or TREK73OPTS=time=60 says otherwise; if it does not, ** TIME ** and the turn passes. -c, -s, -n and -r set the captain, sex, ship name and enemy race. Saving a game is not possible on OS-9. |
| `typefast` | a typing game: words fall down the screen and each must be typed, ended with SPACE or RETURN, before it reaches the bottom.  Pick 1, 2 or 3 for the pace; ten missed words end the game with your words per minute.  Source `. /dd/SYS/termcap.entry' first -- it reads TERMCAP as the description itself<br>**How:** A typing game. Do `. /dd/SYS/termcap.entry' first -- it reads TERMCAP as the description itself. Then `n' skips the instructions and 1, 2 or 3 picks the pace; type each falling word and end it with SPACE. Ten misses end the game. |
| `vtxtcn` | world - build its text tables.  Writes .inc files; needs world's .dat files in the current directory |
| `wisecrack` | a server, and `ask' is its client. Run it in the background and every `ask' pulls one line out of it through /pipe/txtpipe -- slogans from a German OS-9 seminar, 1992-93. `wisecrack & ask "anything"' |
| `world` | World - text adventure |
| `wump` | hunt the Wumpus through a cave of tunnels by the hazards you sense: a draft means a pit is next door, a smell the Wumpus himself.  Move room to room, then loose a crooked arrow along a path of rooms to kill him -- but miss and he may wake and eat you.  `-h' for a harder cave; `-r'/`-t'/`-a' resize it |
| `yidslots` | a slot machine whose three windows spin through the parts of Jewish names: type a bet, watch them stop, and see what the combination pays; 0 ends the game.  Names in GAMES/YIDSLOTS<br>**How:** Full-screen slot machine. Three windows spin through parts of names -- a first name, a name beginning and a name ending. It asks `Place your bet', you type a number and Return, and 0 ends the game. You start with 100; a combination that matches the payoff list multiplies the bet, and `Bob Glick stein' pays 1000 to 1. The windows and the payoffs come from GAMES/YIDSLOTS/yid-names, and a file named on the command line is read instead. The rules are in DOC/yidslots/README. |

**Puzzles**

| | |
|---|---|
| `hanoi` | solves the Towers of Hanoi as a list of moves: `hanoi 3' prints the seven moves for three disks; n disks take 2^n-1<br>**How:** `hanoi 3' prints the moves that shift three disks from tower 1 to tower 2, one move a line. n disks take 2^n - 1 moves, so `hanoi 20' prints over a million lines. |
| `hanoimod` | the Towers of Hanoi as the three towers after every move: `hanoimod 3'<br>**How:** `hanoimod 3' shows the same solution as hanoi as pictures: after each move, a line per tower listing the disks on it, largest first. n disks print 4 x (2^n - 1) lines. |
| `hexa` | hexagonal Sokoban: push every moneybag onto a safe square on a six-sided grid, one bag at a time and only ever forward; k/j move up and down, u/i/n/m along the diagonals.  Five screens ship, and `hexa <n>' edits one |
| `knight` | the knight's tour: move a knight from square to square, never landing twice, and try to visit all 64 -- a row letter then a column digit; ESC cancels the row, Q quits<br>**How:** Full-screen. Answer the instructions question, then S to choose the first square or R for a random one. Each move is a row letter A-H and a column digit 1-8, and must be a knight's move to a square not yet visited; ESC after the row letter cancels it, Q at the row quits. The game ends when no move is left, with the count of squares visited. |
| `maze` | maze generator, small enough to have won an obfuscated-C contest.  It reads the number of rows on standard input and draws a maze that wide: `echo 11 \| maze'<br>**How:** Reads the number of rows on standard input: `echo 11 \| maze' draws a maze eleven rows deep. |
| `mines` | &#9733; minesweeper on a sixteen-by-sixteen board with forty mines: name a square by its row and column letters, answer `Mark?' with Y to flag it; q quits<br>**How:** Full-screen minesweeper. Name a square by its row letter and then its column letter, and answer `Mark?' with Y to flag it rather than open it. `q' quits. |
| `queens` | &#9733; an N-queens solver, an obfuscated-C contest entry: it reads the board size on standard input as a number and draws every arrangement it finds with no two queens attacking: `echo 6 \| queens'<br>**How:** Reads the board size on standard input as a number: `echo 6 \| queens'. |
| `sod` | &#9733; Swamp of Death: cross a swamp from the top left to the X at the bottom right without stepping where you would sink. Each square you stand on shows how many of its neighbours are dangerous.  hjkl or 4 8 6 2 move; `q' and RETURN give up.  `sod -l5' picks a level from 1 to 9, `sod -s' shows the high scores<br>**How:** Full-screen. The swamp is a grid; you start top left (the marker) and the exit X is bottom right. hjkl or 4 8 6 2 move one square, and each square you have stood on shows how many of the eight around it would sink you. `q' asks "in fear to die?" and RETURN then gives up, printing that level's score table. `sod -l1' is the easiest level and `-l9' the deadliest; `sod -s' prints the high-score table. Its scores are in USR/GAMES/LIB/SOD, so mount this disk as /h0 too. |

**Word & guessing**

| | |
|---|---|
| `animal` | the guess-the-animal game that learns: `animal <file>' asks yes-or-no questions down a tree of what it knows, and when its guess is wrong asks what you were thinking of and writes it back into the file. DOC/animal/example is one to start from<br>**How:** The file it learns from is one you name: `animal /dd/DOC/animal/example'. Answer y or n to each question; when its final guess is wrong it asks what you were thinking of and what question tells the two apart, and writes that back into the file. Control-C leaves it. |
| `bog` | Boggle: sixteen lettered dice and three minutes to type every word you can trace through adjoining letters; its word list, index and help are in GAMES/BOG<br>**How:** Boggle. Space starts the three-minute round, `?' shows the rules, and you type every word you can trace through adjoining letters. Control-C leaves it. Its word list, index and help are in GAMES/BOG. |
| `hang` | &#9733; hangman: type a letter to guess it, and the gallows fills in as you get them wrong; its word list is GAMES/dict<br>**How:** Hangman. Type a letter to guess it; the letters still unused are along the top. Control-C gets you out. Its word list is GAMES/dict. |
| `jotto` | Jotto: you and the computer each pick a secret five-letter word of different letters and take turns guessing; a wrong guess is scored by how many of its letters are in the word |
| `jumble` | prints every ordering of the letters of a word, one to a line, to solve a newspaper word jumble: `jumble tac' lists tac, tca, atc, act, cat and cta<br>**How:** `jumble <word>' prints every ordering of its letters, one per line, and that is all it does: read down the list for the one that is a word. A word of n letters gives n! lines -- 720 for six letters -- so keep to short words or send it through grep or less. |
| `jumble2` | unscramble words against the clock: pick a level and how many words, then type each word back; `jumble2 -s' shows the high scores, kept in GAMES/JUMBLE2<br>**How:** It asks whether you want directions, a level -- (E)xpert, (H)ard, (M)oderate or (S)imple, then RETURN -- and how many words. Type each unscrambled word and RETURN before the time runs out: ? reprints the word and the time left, p passes, q forfeits. After a round RETURN plays again, c changes level, s shows the scores and q quits. Four words or more to reach the score list, kept in GAMES/JUMBLE2; `jumble2 -s' shows it. |
| `wf` | makes a word-search square from a file of words: `wf -f words -x 12 -y 12 -t Title'; DOC/wf has two word files<br>**How:** Makes a word-search square from a file with one word per line, optionally followed by a clue: `wf -f words' (a file named words in the current directory is the default). -x and -y set the size, up to 20; -t gives a title; -h, -v, -d, -b and -a choose which directions words may run; -r picks words at random; -p leaves the word list out and -c prints the clues instead. DOC/wf has two word files, words and words.2. |

</details>

## Screen toys

*Animations and screen effects -- they draw on the terminal rather than print to it. Some run until you stop them.*

<details><summary>10 programs</summary>

| | |
|---|---|
| `bite` | a skull draws itself and bites -- a screen toy; q quits<br>**How:** Full-screen: it takes over the display. **`q' quits**. |
| `card` | Towers of Hanoi whose twelve disks are the lines of a Christmas message; VT100, wants TERMCAP |
| `juggle` | animated juggling: balls numbered (1) (2) (3) fly between two hands in the pattern you give in site-swap digits -- `juggle -p 3' is the cascade, `-p 441' a trick, `-r 5' a random pattern of five throws.  ^C ends it<br>**How:** Full-screen animation that runs until ^C. `juggle -p 3' juggles the three-ball cascade; a pattern is site-swap digits, each the height of a throw, so `-p 51' is a shower and `-p 441' a trick, and one that cannot be juggled is refused. `-r 5' picks a random five-throw pattern, `-s 0.1' makes the steps smaller and smoother, `-h' holds 2-throws, `-n' gives it a title. |
| `life` | Conway's Game of Life<br>**How:** life [init-file]. The patterns are in /dd/GAMES/LIFE -- try `life /dd/GAMES/LIFE/glider`. It also wants more memory than the default; from the OS-9 shell that is `life #22k <file>`, and bash has no #size syntax at all. |
| `rain` | raindrops land on the screen and spread in rings -- a screen toy; control-C ends it<br>**How:** Full-screen: it takes over the display. **control-C gets you out**; q, Q, control-D and ESC do not. If it has a quit command of its own, its documentation in DOC/ will say. |
| `rot22` | software rot as a screen toy: the letters of a file come loose a few at a time and fall to the bottom of the screen, piling up until the text has drained out of the top.  Name a file or pipe text in.  Not `rot', which turns a file on its side |
| `textb` | &#9733; Mandelbrot set drawn in ASCII on an 80x25 terminal.  Start with X -2.3, Y -2.0, range 4.0, 32 iterations<br>**How:** An ASCII Mandelbrot viewer -- it asks four questions and draws. Try X_Coord -2.3, Y_Coord -2.0, RANGE 4.0, Max Iter 32. Needs Microware's cio. |
| `ttyexp` | fireworks drawn in characters: bursts thrown out from a point, arcing under gravity with trails. -s<n> bursts at once, -p<n> points in each, -D<n> seconds to run; `ttyexp -s2 -p50' fills the screen. Clears the screen when done; VT100, wants TERMCAP<br>**How:** `ttyexp -s2 -p50' fills the screen with bursts; it runs ten seconds and clears the screen when done. |
| `worms` | worms crawl about the screen at random, each leaving a trail -- a screen toy: -number how many, -length how long, -trail to leave one; control-C ends it<br>`usage: /dd/CMDS/GAMES/worms [-field] [-length #] [-number #] [-trail]` |
| `xmas` | a Christmas card in characters: a tree drawn and trimmed, lights blinking along its strings, reindeer running across the screen, and round again until control-C<br>**How:** Full-screen: a Christmas card that plays in a loop. Control-C gets you out. |

</details>

## Amusements

*Generators, simulators and diversions that are not quite games.*

<details><summary>32 programs</summary>

**Biorhythms**

| | |
|---|---|
| `bio` | a biorhythm chart in BASIC09 -- `runb bio' asks a Date and a Birthday as DD.MM.YYYY (RETURN at the Date prompt takes your system date), then `g' for a graph (or `v' for values) and a number of days, and plots the physical, emotional and mental cycles<br>**How:** A biorhythm chart in BASIC09 -- `runb bio' draws it. It asks a Date, then a Birthday, both as day.month.year with a four-digit year (RETURN at the Date prompt takes your system date), then `g' for a graph (or `v' for values) and a number of days, and plots the physical, emotional and mental cycles. |
| `biory` | biorhythm chart, in German: asks a name (Name Vorname), a birth date as TTMMJJ and a span of years as JJ-JJ, and writes the chart -- Koerper, Seele, Geist, month by month -- to Biory.Lis in the current directory.  Needs `load /dd/CMDS/os9lib' first; RETURN at the name prompt ends it. Source: SRC/rtf/biory.f |

**Curiosities**

| | |
|---|---|
| `areacode` | &#9733; looks up North American telephone area codes, as many as you give it, from a table of the late 1980s; a code it does not know is said to be no area code |
| `globe` | show the currently-lit face of the Earth in ASCII, the globe turning through the day as the hours pass |
| `phoon` | show the phase of the moon as a little picture: `phoon' for tonight, `phoon 2025 12 25' for a date; `-l' sets the size |
| `smiley` | explains the sideways faces of net messages: `smiley ":-)"' prints what that one means; with no argument it prints one of the 589 at random, -l lists them all and -e explains $SMILEY<br>**How:** Explains the sideways faces people typed in net messages. `smiley ":-)"' prints what that face means, and a face with several meanings gets them all. With no argument it prints one of the 589 at random; -f prints just the face, -l lists the whole list, -e explains the face in $SMILEY, and -V counts it. The list is the one the post carried, uncensored, so some of it is crude. The manual is DOC/smiley/smiley.1. |
| `telenum` | turns words into the telephone number their letters dial: `telenum hello' prints 43556<br>**How:** `telenum hello world' prints the number each word dials, one a line: 43556 and 96753. Letters with no key (q and z) print as themselves. |
| `telewords` | spells a telephone number every way its keypad letters allow, one a line: `telewords 43' prints gd ge gf ... if<br>**How:** `telewords 43' prints every spelling of the number with the letters on its keys, one a line -- gd, ge ... if. 0 and 1 stand for themselves; -<digit><letters> changes what a key spells. |
| `trigraph` | prints its own C source spelled in ANSI trigraphs -- ??< for {, ??= for # -- a 1990 obfuscated-C contest entry<br>**How:** `trigraph' prints its own source with every # { } [ ] \ ^ \| ~ written as its ANSI trigraph -- ??= ??< and the rest. Microware's cpp does not read trigraphs, so SRC/ioccc/OSK holds the translated copy it was built from. |
| `westley` | picks a daisy: `westley 7' pulls seven petals, loves me, loves me not, and says how it came out.  A 1990 obfuscated-C contest entry, and the one that won Best Layout -- its source is written to be read as a letter<br>**How:** `westley <number>' picks a daisy with that many petals -- loves me, loves me not -- and says how it came out. The 1990 contest's Best Layout: its source is written to be read as English correspondence, letter by letter, and the judges' note reads the first block as "charlie, doubletime me, OXFACE! not interested, get out". Reading the source is the point of it. |

**Generators**

| | |
|---|---|
| `chef` | talk like the Swedish Chef: a filter that rewrites English into his mock accent -- the->zee, w->v, o->oo -- and barks "Bork Bork Bork!" at each sentence end.  `echo text \| chef` |
| `drawl` | give text a broad Texan accent: drops the g from -ing and swaps in tuh/thuh.  `echo text \| drawl`, a stdin filter |
| `fudd` | talk like Elmer Fudd: a filter that turns r and l into w and th into d, so text comes out in his lisp.  `echo text \| fudd` |
| `lame` | rewrites its arguments into IRC leet-speak -- o->0, you->U, and->&, i->1 -- the way a lamer types.  `lame your text` |
| `lotto` | picks lottery numbers after a testimonial and a demand that you believe -- answer y or n; six from 1 to 49 unless -n, -b and -t say otherwise<br>**How:** `lotto' asks whether to hear testimonials, whether you believe and whether you really believe -- answer y or n -- and then draws six numbers from 1 to 49, a second apart. -n, -b and -t change how many and the range; -a sets how many testimonials. End of input quits. |
| `name` | &#9733; invents pronounceable names for the characters in a tabletop game, as many as you ask for, dealing vowels and consonants in turn with the letter frequencies of a Scrabble set |
| `newsgen` | &#9733; makes up a news bulletin at random from parts -- a top story of public figures, deeds, places and reactions, then the weather -- different every run<br>`"news" or "news lp"` |
| `pig` | turns English into pig latin: every word of two letters or more moves its first letter to the end and adds `a'.  `echo text \| pig'<br>**How:** Pipe English through it: `echo "pig latin" \| pig' prints `igpa atinla'. Each word of two or more letters moves its first letter to the end and adds `a'; one-letter words and punctuation pass unchanged. |
| `pwgen` | &#9733; pronounceable passwords: `pwgen <length> [how many]'<br>**How:** pwgen <length> [count]: length 4 to 16. It takes a few seconds over each password, so allow for that. |
| `repunsel` | a pun filter: English comes out full of plants and gardens -- `and I would root' becomes `ANT I WOOD ROOT'.  `echo text \| repunsel'<br>**How:** Pipe English through it: `echo "And I would root" \| repunsel' prints `ANT I WOOD ROOT'. Each word it has a garden pun for -- and, would, not, over, leave, care -- comes out in capitals; the rest passes through. |
| `rndname` | &#9733; invents pronounceable names, as many as you ask for -- the earlier version of `name', with every letter equally likely, so the names come out more exotic |
| `roll` | rolls dice named on its command line: `roll 3d6', six rolls with `6x3d6', the best three of four with `3,4d6', a repeat with `2@'; with nothing it rolls d100<br>**How:** Rolls dice named on its command line and prints each total. `roll 3d6' is three six-sided dice; `roll 6x3d6' rolls them six times, best first; `roll 6x3,4d6' keeps the best three of four dice each time; `roll 2@3d6' repeats the whole thing; a bare number is one die with that many sides, and with nothing it rolls d100. A die needs at least two sides. |
| `rpoem` | &#9733; writes verses at random from a grammar and a word list in GAMES/SNOBOL; a number says how many, thirty without one |
| `rstory` | a cumulative tale in the shape of The Old Woman and Her Pig, the animal, the obstacle and every helper drawn at random; `rstory \| tformat' sets it justified under a dated heading. Data: GAMES/SNOBOL |
| `scales` | &#9733; deals scales and chords into a random practice order, a tick-box each, in `scales.lst' in the current directory (or a file you name): -d diatonic scales, -a altered scales, -m modes, -c chords; each entry gives the key signature and the spelling<br>**How:** Pick at least one of -d -a -m -c or it asks what you had in mind; `scales -d -c' writes 195 entries to scales.lst, and a trailing name writes elsewhere. |
| `spew` | builds mock National Enquirer headlines from a grammar of phrases -- almost a yacc in reverse; `spew 5' makes five |

**Simulated weather**

| | |
|---|---|
| `england` | &#9733; a year of random weather, day by day, for a tabletop game: the mid-Atlantic climate profile on the Gregorian calendar. `england 2' does two years.  Six builds of one program differ only in climate and calendar: england, florida (Gulf coast), georgia (south Atlantic), minnesota (north Atlantic), japan (north Pacific, Japanese calendar) and shire (mid-Atlantic, Middle-earth calendar)<br>**How:** One of six weather simulators that differ only in climate and calendar: england, florida, georgia, minnesota, japan (Japanese calendar) and shire (Middle-earth). Each prints a year of weather, a line a day, with a summary at each month's end; a number says how many years. |
| `florida` | &#9733; the weather program on its Gulf-coast profile; see england<br>**How:** Prints a year of Gulf-coast weather, a line a day; `florida \| head -n 37' shows January. See england. |
| `georgia` | &#9733; the weather program on its south-Atlantic profile; see england |
| `japan` | &#9733; the weather program on its north-Pacific profile, with the months of the Japanese calendar; see england<br>**How:** A weather simulator on the Japanese calendar -- see `england'. |
| `minnesota` | &#9733; the weather program on its north-Atlantic profile; see england |
| `shire` | the weather program on its mid-Atlantic profile, with the months of Tolkien's Shire calendar; see england<br>**How:** A weather simulator using the Middle-earth calendar -- see `england'. |

</details>

## System & modules

*OS-9 module and process tools, devices, system state and scheduling.*

<details><summary>118 programs</summary>

**Devices & disks**

| | |
|---|---|
| `dam` | &#9733; display the disk allocation map -- dam [<drive>] |
| `dedit` | BASIC09 disk sector editor -- read, edit and write raw sectors, decode a disk's identification sector.  I-CODE, not 68000 code: run it with runb and the bare module name, like bio and wysetime.  Nine modules in the one file. |
| `dinfo` | &#9733; reports on an RBF disk -- volume name, creation date, capacity, how much is free and in how many blocks -- doing the job your own `free' does and saying more. -e extends the display and -f reports fragmentation<br>`Syntax:   dinfo [<opts>] {<device name> [<opts>]}` |
| `dpark` | &#9733; parks the disk head: `dpark [/device]' restores an RBF device's head to track 00, which is what you did before moving a drive<br>`Syntax:   dpark [/device]` |
| `freeb` | lists the free space on a disk block by block -- how many free blocks there are, how big each one is and where it starts.  -t counts them by size, -a lists every one, -h leaves the header out and -s the total<br>`Usage:` |
| `os9dsk` | reads a CoCo OS-9 disk image -- the .DSK files a Color Computer emulator uses.  `os9dsk -dir <file>.DSK' lists it, -get copies a file out, -proc shows the file descriptor.  A 1985 disk reads as easily as a new one<br>`Usage:	os9dsk -dir filename.DSK DSKpath` |
| `rsdsk` | reads a CoCo RS-DOS disk image, the Disk Extended BASIC side of the same .DSK files: -dir lists it, -get copies a file out.  Between them and os9dsk, either kind of Color Computer disk can be read here<br>`Usage: rsdsk -dir filename.dsk` |
| `shdev` | &#9733; lists the system's device table: what is mounted and the driver behind each |
| `ssl` | &#9733; show a file's segment list, sector by sector -- ssl <file> |

**Finding things**

| | |
|---|---|
| `about` | what this collection knows about a program: what it is, what it is for, where it came from, the files it opens and whether they are here, and whether its source and documentation survived.  One card per program -- `about hack'.  DOC/CATEGORIES browses; this answers. |
| `whereis` | find a program's source, command and documentation -- SRC, CMDS, DEFS, LIB and DOC, searched all the way down on every device PATH names.  `whereis gen'<br>`whereis [ -sbmu ] [ -SBM dir ... -f ] name...` |
| `which` | what a command name runs, found the way the OS-9 shell finds it, and for a module already in memory, the file it came from.  `which -a dir'<br>`Usage: which [-i] [-a] [--] [<command>]` |
| `zc` | looks up a US postal zip code and names the city and state -- `zc 60115' answers `De Kalb, IL.'.  With no argument it opens a form you type codes into until you quit, C clearing the field and Q leaving.  It reads SYS/zipcodes.txt, which ships |

**Keeping**

| | |
|---|---|
| `keep` | take a program off this disk onto your own disk -- copies it and whatever DOC/DEPENDS says it needs, and records every file written.  `keep -n' shows what it would do without doing it.  See DOC/README-KEEP.<br>`keep 1.0 -- OS-9 freeware collection` |
| `kept` | list what has been taken, and how much it came to<br>`keep 1.0 -- OS-9 freeware collection` |
| `unkeep` | removes the files keep wrote for a program -- it reads the receipt in SYS/kept -- and leaves any whose checksum has changed since, so your saves and scores are safe from it by construction.  `kept' lists what it would take<br>`keep 1.0 -- OS-9 freeware collection` |

**Microware runtime**

| | |
|---|---|
| `cio` | Microware's C library trap module -- what every starred program here needs.  Included with Microware's permission; see SOURCES.txt.  You do not run it, it loads itself. |
| `csl` | Microware's C Shared Library, for programs built with Ultra C rather than cc 3.2 (68000) |
| `csl020` | the same, for 68020/030/040 |
| `fpu` | Microware's floating-point EMULATION module: where there is no 68881/68882 coprocessor it makes the machine behave as though there were, so Ultra C's floating-point code runs. Carries its own distribution grant -- DOC/fpu.doc, which the grant requires be kept with it.  Not a program and not loadable by hand: it belongs in your bootfile and in your Init module's extension list, so it is here for you to install on your own system rather than to run from here |
| `math` | Microware's floating-point trap module (software) |
| `math881` | the same, using a 68881/68882 coprocessor.  Both register as the module `math'; load whichever suits your machine. |

**MM/1 drivers**

| | |
|---|---|
| `keydrv.mm1` | keyboard driver |
| `msdrv.901_340` | mouse driver |
| `msdrv_340.901.ms` | the mouse driver, a second build of the same edition |
| `rb37c65` | floppy driver (37C65 controller) |
| `scsi_mm1a` | the low-level SCSI routines the hard disk driver links to |
| `snddrv` | sound driver |
| `windio.52` | windowing terminal driver |

**OS-9 modules**

| | |
|---|---|
| `bootgen` | &#9733; makes or extends the boot file on a device from the module files you name -- the file a system reads its modules out of at startup. -a appends to the boot already there instead of writing a new one, and -b sets the copy buffer<br>`Syntax:   bootgen [<opts>] <device> {<path> [<opts>] }` |
| `bsplt68` | takes an OS9Boot file apart into the modules inside it, writing each one out under its own module name. A boot file is modules end to end, so `cat a b > OS9Boot' makes one you can try it on |
| `flink` | &#9733; makes a second directory entry for a file under a name you give -- an RBF hard link. RBF has no true hard links, and removing such an entry can leave the original pointing at the wrong place, so do not run it on a disk you care about<br>**How:** never run this on a disk you care about, and never on a shipped module. It makes a directory entry aliasing the file's FD in whatever directory you are standing in; RBF has no hard links; and removing that entry leaves the original file pointing at a directory, after which `cat' answers `is a directory' for everything. It corrupted /dd/CMDS/cat that way once, and only rebuilding the image put it back. |
| `gen` | generates the frame of a new C program -- header block, authorship and version lines and the sectioned comments a Microware example was laid out with. It appends `.c' to whatever name you give it: `gen -p frame' leaves `frame.c'. `-m' does a module frame, `-t' a type, `-f' a function declaration<br>`Syntax: gen [<opt>] <pathname> [<opts>]` |
| `load` | loads a module into memory, so a program that links a library module can find it -- `load /dd/CMDS/os9lib' and the RTF Fortran set comes alive. A clean-room reimplementation of Microware's load, source in SRC/load, built trap-free Shares its name with a utility of your own -- README-NAMES<br>`Syntax:   load [<opts>] {<module> [<opts>]}` |
| `mexist` | &#9733; answers whether a module is in the module directory by its exit status rather than by printing: 0 if it is there, 1 if it is not. The name is case-sensitive, and it looks at up to 256 modules<br>`MEXIST   Version UTIL 2.40 by DESIGNA VLT 24.11.97` |
| `os9lib` | the RTF/68K Fortran run-time library. rtf, for, lnk, biory and creadoc all link it, so `load' it into the module directory before running them. See DOC/README-FORTRAN |
| `ptxm` | Path Table eXtension Module: a kernel extension letting user-state processes open unlimited I/O paths. Courtesyware, free. It installs into the kernel and so needs supervisor state. DOC/ptxm/ptxm.txt |
| `remove` | &#9733; remove modules from memory -- its own Function line says so. `remove <module>...', -q for quiet. `rm' removes files<br>**How:** Removes modules from memory. `del', `rm' and `deldir' are the file ones. |
| `rtfdat` | the RTF Fortran data module |
| `unc` | disassemble a 68000 OS-9 module back to assembler: the header as equates, then the code, tracing which bytes are instructions and which are data, naming the OS-9 syscalls.<br>`Syntax: unc {-<opts>} <file> {-<opts>}` |
| `version` | &#9733; prints its own version and nothing else -- `Dies ist das Program 'version', Version 7' -- whatever module you name. `modinfo' shows a module's edition, and your own OS-9's `ident' reports what a module was built from |
| `vmod_trap` | the VMod_trap trap handler that rxmod and txmod call. A type-$0B trap module, not a program: `load /dd/CMDS/COMMS/vmod_trap' before running them. It runs in supervisor state, so once installed it faults on this kernel |

**Processes & memory**

| | |
|---|---|
| `aprocs` | &#9733; a process monitor: prints the active processes as a tree -- id, parent, priority, CPU time, age and share of the CPU -- and -m measures their activity over a few seconds. `procs', `top' is the other process lister<br>`Syntax: aprocs [<opts>]` |
| `edir` | &#9733; list the event directory -- OS-9 events and their values; `-e' is the long form, with the value and the increments. The print spooler makes one to look at: `lpsched /nil &' and `spoolqueue' is in the directory<br>`Syntax: edir [<opts>]` |
| `eset` | &#9733; set an OS-9 event to a value -- eset <event> <num><br>`Syntax: eset <event> <num> [<opts>]` |
| `eunlink` | &#9733; unlink an OS-9 event by name -- `eunlink <event>'. `edir' lists the events and `eset' sets one<br>`Syntax: eunlink {<event>}` |
| `launch` | &#9733; a login helper: reads SYS/config, sets the environment for your terminal type -- and optionally a default PATH and emacs bindings -- then starts the shell you name on its command line. It does not put anything in the background<br>**How:** Says "nothing to launch" until it is configured -- see its documentation. |
| `signal` | &#9733; sends a signal to a process by number, and can wait first: `signal <pid> <code> [<seconds>]' delays that many seconds and then sends it. Code 0 ends the process; sent to an id nothing holds it answers 228. Run a program with `&' and bash prints the id it got in angle brackets. `snd_sig' beside it takes several processes at once and defaults to the wake signal<br>`Syntax: signal <process-id> <signal-code> [<seconds>]` |
| `top` | show the busiest processes by their share of the CPU, refreshed every few seconds: `top' lists only those that have used any, `top -a' lists them all, and `top <seconds>' sets how often.  Interrupt to leave. `aprocs' is the other process lister here<br>`Syntax: top [<opts>] [<num>]` |
| `vis` | &#9733; run a command over and over and refresh the screen with its output -- what `watch' does on other systems: `vis {opts} <command> <args>'.  Not the Unix `vis' that makes non-printing characters visible<br>`vis: illegal option -- ?` |
| `who` | 'who is logged in'.  Written in Microware shell syntax |

**Scheduling**

| | |
|---|---|
| `cron` | run commands at specified times (daemon) |
| `every` | &#9733; runs a program over and over, waiting the given number of seconds between runs: `every 2 oskversion' prints the version every two seconds until you stop it. The program's own options follow its name<br>`Syntax: every <time> <progname> [<progopts>]` |
| `repeat` | repeat an OS-9 command N times -- `repeat 2 date' runs date twice.  It hands the command to $SHELL, which SYS/login sets to ksh, and ksh runs it.  date writes no trailing newline, so the repeats abut on one line.<br>`repeat ver 1.2` |

**System state**

| | |
|---|---|
| `clock` | a full-screen clock, the digits drawn with `banner'.  For each one it runs banner into a named pipe through system() and reads the pipe back, and this C library's system() forks a module called `shell' -- your own OS-9 has one; load it first.  With none resident nothing writes the pipe and it stops on the open.  Source in SRC/misc/clock.c |
| `oskversion` | &#9733; reports the system: OS-9 level, version, revision and edition, and the CPU twice over -- what the init module claims and what the system globals say the processor really is, which are not always the same machine<br>`Syntax:   OSKversion` |
| `perr` | &#9733; print an OS-9 error message<br>`Syntax: perr [<error_codes>]` |
| `setime` | sets the system time. It prompts with `YYMMDDHHMMSS' and then does not set it: the clock is unchanged whether the answer comes from standard input or from six fields on the command line Shares its name with a utility of your own -- README-NAMES |

**Users and login**

| | |
|---|---|
| `adduser` | &#9733; add a user to the system, for uucp logins<br>`ADDUSER: add a user to or remove a user from the system` |
| `passwd` | changes your own password in /dd/SYS/password. It matches on the user name, and the name must be spelt exactly as the password file has it, capitals included. Source in SRC/passwd<br>`Syntax: passwd` |

**Utilities**

| | |
|---|---|
| `argproc_demo` | a demonstration of argproc(), a command-line argument parser: it parses the line and prints what it made of it -- `argproc_demo readme' answers `arg=readme, b=0, c=0, sGiven=0, s=this is a test, x=32, pi=3.144500'. A switch takes its argument with no space (`-x99', not `-x 99'), which the program says itself under -help. The argproc library manual is in DOC/argproc_demo/man.argproc<br>**How:** A switch takes its argument with no SPACE: `-x99', never `-x 99'. `argproc_demo readme' prints what it made of the line. |
| `bigsetter` | Modula-2 set-operations demonstration |
| `bootlogger` | &#9733; writes the time the machine came up into SYS/bootlog and says nothing at all.  It returns silently however it is run, so the log is the only way to see that it did anything -- and run by hand it stamps the log with the time you ran it rather than with a boot |
| `btop` | convert characters to bit patterns -- its own Function: line, and what it does: `btop <file>' prints each character as a grid of O and space.<br>`Syntax:   BtoP [<opts>] [<path1>] [<opts>] [<path2>] [<opts>]` |
| `chardef` | loads a character set into a VT220 terminal from a definition file: `chardef <file>'; it calls itself defchar<br>`Syntax: defchar [<path>]` |
| `clear` | &#9733; clears the screen, reading the escape sequence to do it from the termcap. `cls' beside it does the same job from a different author; either will do<br>`Syntax:   clear` |
| `combine` | &#9733; interleaves two files byte by byte, one supplying the even bytes and the other the odd -- how a 16-bit EPROM image is put back together from two 8-bit halves<br>`(c.) 1989 by F.R.Schmitt MPI Kernphysik Heidelberg` |
| `config` | report this machine's C type properties as #defines -- char, short, int, long, pointer, float and double -- then how the arithmetic rounds and how big a block malloc can still give you.  The `No more memory' lines near the end are it halving its request until one succeeds, which is the measurement, not a failure |
| `cpu` | &#9733; a CPU speed test: it draws a bar chart of its timing loop and prints the clock rate it measured, then stops on a trap |
| `demerge` | splits a file holding several OS-9 modules into one file per module, each named after the module it holds. OS-9's `merge' is concatenation, so `cat a b > c' makes the file it takes apart. `modbuster' does the same job and can be pointed at another directory<br>**How:** OS-9's `merge' is concatenation, so `cat a b > c' makes the file demerge takes apart -- your own `merge' does the same. `dump' is the hex dump here. |
| `demo` | egetopt option-parsing demonstration |
| `devprc` | shows which device each process holds a path to: -a walks every process and lists its open paths and the device behind each<br>`devprc: display device(s) belonging to process(es), V.1.01` |
| `dload` | &#9733; load a data file into a data module: `dload <filename>'. Nothing to do with serial downloads -- `sbreak' and `break' are the serial-line examples here<br>`Syntax: dload <filename>` |
| `fastcc` | &#9733; a second front end for Microware's cc, with its own options: -p pipes the preprocessor's output straight into the compiler instead of through a temporary file, -r compiles to relocatable files in a directory you name, -a stops at assembler, -bp shows each command before it runs. `-?' lists them all<br>`fastcc: <opts> <files> <opts>` |
| `fixyear` | repairs file dates, not the clock: given a file or a directory it corrects any modification year earlier than 1970, which is what a machine whose clock was wrong when the file was written leaves behind. -l logs what it changed and -q carries on past an error<br>`Usage: fixyear [-opt] <file\|dir> <dir\|file> [-opt]` |
| `fontgen` | generate a font for the Gepard display<br>**How:** Generates a character font for the Gepard display -- it prints the assembler source of an 80-column font on stdout. |
| `getsys` | &#9733; report the system's globals -- what OS-9 thinks it is running on<br>`Syntax: getsys [<opts>]` |
| `hinterhalt` | &#9733; a small maze game, in German: asked whether you need instructions (J/N) and told no, it draws the board -- walls, the player and a target |
| `i_am_i` | a quine in Pascal: run it and it prints its own source, the loop at the end walking the table of lines that holds the program's text [no military use -- EFFO-INFO] |
| `lgrep` | &#9733; list the files a pattern appears in -- its banner says "same as 'grep -l', but prints filenames without comments". It runs your own OS-9's `grep'; load that first. DOC/README-GREP compares the six searchers<br>`Syntax: lgrep <arg1> ... <argn>` |
| `liborder.os9` | the same program as liborder, a second build<br>`liborder: Unimplemented option '-?'.` |
| `makecrc` | generates C source for CRC tables. It takes no arguments: run it somewhere writable and it writes six files into the data directory -- arc.c, binhex.c, ccitt.c, ccitt32.c, kermit.c and zip.c -- each holding a crctab[256] and an updcrc() for one polynomial. It writes them without a message, so list the directory afterwards. For a CRC of a file, `chksum' does that<br>**How:** It generates C SOURCE and takes no arguments. Run it somewhere writable (`ksh -c "cd /dd/tmp; makecrc"') and it writes six files -- arc.c, binhex.c, ccitt.c, ccitt32.c, kermit.c, zip.c -- each a crctab[256] and an updcrc(). It writes them without a message, so list the directory afterwards. |
| `map` | &#9733; show the disk blocks a file occupies, sector by sector: `map <file>', or `map -e <file>' for the extended form. For memory rather than disk, `mfree' and `free' would be the equivalents, and your own OS-9 has them<br>`Syntax: map [<opts>] <file> {<file>}` |
| `modinfo` | report a module's header -- name, type, size, edition, CRC<br>`module: Show Module Information` |
| `mvolformat` | format a multi-volume set<br>`Syntax: mvolformat drive volname volcount [format options]` |
| `phone` | connects two terminals over a communication path so you can type to somebody on another: `phone /t1' rings until answered; control-E leaves<br>`Syntax: phone <communication-path>` |
| `preset` | loads the terminal's function keys: it writes a fixed set of definitions -- `dir', `umacs', `r68', `l68', `dsave -ieb128k' and so on -- and answers `Funktionstasten belegt!'. German. It takes no arguments and ignores any given |
| `pri` | change a process's priority: `pri <pid> <priority>'.  It prints nothing whatever happens, and on this disk it answers 221 -- module not found -- for every invocation tried, a live process and no arguments alike.  What it is looking for has not been established; no source for it is here |
| `ptob` | convert bit patterns back to characters -- the other half of `btop', and the round trip is exact.<br>`Syntax:   PtoB [<opts>] [<path1>] [<opts>] [<path2>] [<opts>]` |
| `ptxminst` | install Ptxm -- the kernel extension above |
| `rndir` | &#9733; converts directory names between upper and lower case -- its own Function line is "rename directory names in big/small characters". `-l' for small, `-q' to work silently<br>`Syntax: rndir [<opt>]` |
| `screen` | &#9733; `screens': picks a file at random from $HOME/.screens and shows it -- a login greeting. On OS-9 it runs the file rather than printing it, through system(), so it wants Microware's `shell' on your execution path. Not the terminal multiplexer of the same name.  Under os9exec it stops with a bus error at the first file it accepts from that directory, and so does REBUILT/screen_nocio.  Source in SRC/screen, man page in DOC/screen/screens.6 |
| `screen_nocio` | a trap-free source build; CMDS/screen uses cio and this one does not |
| `scsiutil` | talks to a SCSI device: inquiry, capacity, read sectors, eject, and audio CD control -- table of contents, play, volume<br>`SCSIutil V2.02 [Jan 28 1997 : 15:59:35] - written by Gary Duncan` |
| `setime2` | Y2K: set the system time, four-digit year<br>`Syntax:    setime2 [<opt>] [<yyy mm dd hh mm ss [am/pm]>] [<opt>]` |
| `setyear` | sets the system year, and only the year -- `setyear 2026' -- leaving the month, day and time alone. It takes 1970 to 2050 and prints the date it ends up with<br>`Syntax:    setyear <YYYY>` |
| `snd_sig` | &#9733; sends a signal to one process or to several at once -- `snd_sig <pid> <pid>...' -- and with no option sends the wake signal; -<n> sends signal number n instead. `signal' beside it takes one process and can delay first<br>`Syntax:   snd_sig [-options] pid pid1...pidn` |
| `spline` | &#9733; fit a spline through points, output PostScript |
| `sqrtx` | a square-root demonstration: for each of the first primes it prints the root, the root squared back, and how far that lands from the number -- a few parts in ten thousand million million, which is what double precision is worth |
| `suse` | show a program's usage line.  `-?' does the same for most programs here. |
| `suspend` | &#9733; removes a process from the system -- its own usage line says so -- rather than suspending it; -s reaches system programs too<br>`SUSPEND V1.1 (C.) 1989 by F.R.Schmitt` |
| `t_trtest` | RICO trap-handler test |
| `testibc` | IEEE-488 (GPIB) bus test program, B & K Denmark, 1989. Answer its `Timeout time (1/10 Sec)?' prompt and it draws its command menu -- Ifc, Remote, Llo, Goto local, Clear, Send, Enter, Dev-clear, Time, Quit -- and then stops with `Process Aborted', because every one of those commands wants an IEEE-488 bus and there is none.  It looks for its messages in /dd/sys/errmsg.ibc; supply one there and it reads them and was in none of the archives, so each failure prints as a bare `Error #000:007' instead of a sentence.  Kept as the instrument software it is, not as something to run. |
| `transfer` | &#9733; copies files from GDOS disks to OS-9, and takes no options at all. For general device-to-device copies, `cp', `copy' and `dsave' do that<br>`Syntax: transfer` |
| `trunc` | &#9733; truncate a file to a given length<br>`OS-9/68k supplementary command.` |
| `tty` | &#9733; report the terminal's name |
| `unpacklib.os9` | unpack a library into its object modules<br>`unpacklib: Unimplemented option '-?'.` |
| `vc` | &#9733; a spreadsheet: `Welcome to the Spreadsheet Calculator, type ? for help', with rows, columns and a formula line |
| `vecho` | System V `echo': the newline is suppressed by a trailing \c in the argument, not by default. `vecho one' writes `one' and a CR; `vecho one\c' writes `one' and stops. Several arguments are joined with a space. SRC/less_v177 |
| `vlen` | &#9733; a variable-length record demonstration: it ignores whatever you give it, creates a filesystem of its own, adds a hundred records of varying length and prints the minimum, the maximum and the mapper entries as it goes. `isam' is the other demonstration of its kind here. It leaves its store behind in the data directory as `test.mp' and `test.st' -- run it twice and the second run answers `Filesystem already exists.' and adds nothing. Delete those two to run it again<br>**How:** It leaves its store behind, in the data directory, as `test.mp' and `test.st'. Run it twice and the second run says `Filesystem already exists.' and adds nothing; delete those two to run it again. |
| `what` | inventory the expansion cards in a GEPARD -- the German 68k machine much of the EFFO material was written on.  It prints `What's where in the GEPARD:' and a table of I/O address, reference byte and card name, empty on anything else.  It ignores its arguments. Shares its name with a utility of your own -- README-NAMES<br>**How:** An inventory tool for the GEPARD, the German 68k machine: it prints "What's where in the GEPARD:" and a table of expansion cards. On other hardware the table is empty, and it ignores its arguments. |
| `xlharc` | C-LHarc 1.00 in a third build: extracts and lists .lzh archives like `lharc'<br>`C-LHarc for OSK Version 1.00   (C) 1989-1990 Y.Tagawa` |
| `yagi` | a Yagi antenna design calculator, to DL6WU's method. It asks five questions on standard input -- frequency, element count, boom diameter, insulated from the boom Y/N, and a tubing size off its own list -- and prints element lengths and spacings. Answer four and it loops on the fifth<br>**How:** It asks five questions on standard input -- centre frequency in MHz, element count, boom diameter, whether the elements are insulated from the boom (Y/N), and a tubing size off its own list of six. Answer four and it loops on the fifth forever, because EOF on a numeric read returns the same thing every time. |
| `ynad` | &#9733; YNAD -- Yet Another Name & Address program.  A contact database. |

**Vendor demos**

| | |
|---|---|
| `ob68kdemo` | OmniBasic 1.16 -- a BASIC compiler.  Limited symbol table; otherwise the including compiler.  Run it from /dd/DOC/omnibasic, where its library and examples are. Like UniBasic it needs Microware's cc to finish a build<br>**How:** OmniBasic 1.16, same arrangement as ub68kdemo and the same SHELL trick -- see its entry. Run it from /dd/DOC/omnibasic. DEMO VERSION, capped symbol table. |
| `sddemo` | White's Speedisk 2.10 -- disk de-fragmenter.  Wants an 80x24 screen; falls back to tty mode<br>**How:** White's Speedisk 2.10 de-fragmenter, demo build. Wants an 80x24 screen and drops to tty mode without one. |
| `ub68020demo` | UniBasic 1.10 for the 68020 -- the same demonstration as `ub68kdemo' and it runs the same way, announcing `OS9/68020 Version' where the other says 68000.<br>`UniBasic Version 1.10` |
| `ub68kdemo` | UniBasic 1.10 -- a BASIC compiler, same arrangement as OmniBasic.  Run it from /dd/DOC/unibasic<br>**How:** UniBasic 1.10, and it does compile -- the trick is that it runs its build through $SHELL. With SHELL unset it hunts for `/dd/bash' and dies with "Error Exit" and error 216. Do `setenv SHELL /dd/CMDS/sh', work in a directory holding basic.h and basic.l (DOC/unibasic has them), have your C toolchain reachable with CDEF and CLIB set, and give it memory. DEMO VERSION: the symbol table is capped, nothing else is. |

</details>

## Disk & DOS

*Reading and writing MS-DOS media with the mtools set.*

<details><summary>20 programs</summary>

| | |
|---|---|
| `msattrib` | mtools 3.6: reads or sets a DOS file's attribute bits -- +r and -r read-only, +a archive, +h hidden, +s system<br>`msattrib: illegal option -- ?` |
| `msbadblocks` | mtools 3.6: reads every used cluster of a DOS disk and marks the ones that fail as bad, so nothing is written there again |
| `mscd` | mtools 3.6: sets the current directory on a DOS disk for the other ms commands; run bare it reports where it is |
| `mscheck` | mtools disk verifier.  A ksh script (#!ksh), and ksh is starred, so this one wants cio too.  Drives a: and b: are ready. |
| `mscopy` | mtools 3.6: copies files between OS-9 and a DOS disk, `mscopy file a:NAME.TXT' or the other way round; -t converts text line endings<br>`mscopy: illegal option -- ?` |
| `msdel` | mtools 3.6: deletes files on a DOS disk<br>`msdel: illegal option -- ?` |
| `msdeltree` | mtools 3.6: removes a directory on a DOS disk and everything inside it<br>`msdeltree: illegal option -- ?` |
| `msdir` | mtools 3.6: lists a DOS directory in DOS's own form -- 8.3 names, dates and the free space left<br>`msdir: illegal option -- ?` |
| `msformat` | mtools 3.6: writes a fresh MS-DOS filesystem onto a floppy; it wants removable media and refuses a plain disk image<br>**How:** Refuses this disk image outright because it is not removable media; even given the image's own geometry it does not complete. A real floppy drive is what it wants. |
| `msinfo` | mtools 3.6: reads a DOS disk's boot sector and reports its geometry, sector size and label, with the msformat line that would recreate it<br>`msinfo: illegal option -- ?` |
| `mslabel` | mtools 3.6: reads or writes a DOS disk's volume label<br>`mslabel: illegal option -- ?` |
| `msmd` | mtools 3.6: makes a directory on a DOS disk<br>`msmd: illegal option -- ?` |
| `msmove` | mtools 3.6: moves files between directories on a DOS disk<br>`msmove: illegal option -- ?` |
| `msrd` | mtools 3.6: removes an empty directory from a DOS disk<br>`msrd: illegal option -- ?` |
| `msread` | mtools 3.6: reads a file off a DOS disk byte for byte into an OS-9 file<br>`msread: illegal option -- ?` |
| `msren` | mtools 3.6: renames a file on a DOS disk<br>`msren: illegal option -- ?` |
| `mstoolstest` | mtools 3.6: prints mtools' resolved configuration -- the drives it knows and the image file behind each -- rather than testing anything<br>**How:** Prints mtools' resolved configuration -- the drives it knows and the image file behind each one -- not a diagnostic test of anything. |
| `mstype` | mtools 3.6: prints a file that lives on a DOS disk<br>`mstype: illegal option -- ?` |
| `mswrite` | mtools 3.6: writes a file onto a DOS disk byte for byte, with none of the name rules or text conversion mscopy applies; msread is its reverse<br>`mswrite: illegal option -- ?` |
| `mtools` | the mtools 3.6 suite's own front end: run bare it lists every sub-command, each of which is also its own program here. Drives a: and b: are set up in SYS/mtools.conf, backed by the disk images in DOS<br>`Supported commands:` |

</details>

## Time & calendar

*Calendars, clocks and astronomy.*

<details><summary>18 programs</summary>

**Astronomy**

| | |
|---|---|
| `almanac` | computes where the Sun, Moon and the eight planets are for a given date and time: right ascension, declination, apparent diameter and distance in AU.  Add your longitude and latitude and it also gives azimuth and altitude.  Its constants were taken from The Astronomical Almanac 1990, so accuracy softens the further you go from then<br>`Syntax of command:` |
| `ephem` | &#9733; an astronomical ephemeris: a live panel of the sun, moon and planets -- right ascension, declination, azimuth, altitude and more -- for a site and time, from the configuration and star database in SYS. RETURN passes the opening page, control-D quits<br>**How:** An astronomical ephemeris: `ephem -c /dd/SYS/ephem.cfg -d /dd/SYS/ephem.db'. RETURN passes the opening page; any key stops the loop; ? is help; control-D quits. |
| `ephem881` | &#9733; ephem built for a 68881 floating-point coprocessor: the same panel, and with hardware floating point the whole table fills in at once<br>**How:** The same as ephem, built for a 68881 coprocessor. Control-D quits. |
| `lunisolar` | &#9733; the phase of the moon in one line; given a year and a time zone it writes a whole lunisolar calendar as LaTeX instead<br>`Bad args: lunisolar -?` |
| `nasa` | &#9733; NASA orbital-element reader. Wants `nasa.dat' in the current directory: NORAD two-line element sets -- a name line, then TLE line 1 and line 2 per satellite -- and writes kepler.dat. No element set ships here; supply a current one. The format is parsed in SRC/eff_orbit/nasa.c and is column- sensitive<br>**How:** Put NASA two-line elements in nasa.dat in the current directory and run `nasa'; it writes kepler.dat, which `orbit' reads. No element set ships; they are published for every satellite. |
| `orbit` | &#9733; the N3EMO satellite tracker, version 3.7: where a satellite is from a site, hour by hour -- azimuth, elevation, doppler, range and transponder mode.  It opens kepler.dat, mode.dat and a <site>.sit by bare name from the current directory, and DOC/orbit holds them (pgh, bern and zuerich sites), so run it from there: `chd /dd/DOC/orbit' and `orbit', or under bash `ksh -c "cd /dd/DOC/orbit; orbit"'.  `nasa' makes a kepler.dat from published two-line elements<br>**How:** It reads kepler.dat, mode.dat and a <site>.sit by bare name from the current directory, and DOC/orbit holds them: `ksh -c "cd /dd/DOC/orbit; orbit"'. Answer d for a day's table, then the site (pgh), the date, the start hour, the step and the length. |

**Calendars**

| | |
|---|---|
| `cal` | &#9733; Calendar. `cal -h' prints holidays with it -- SYS/holidays is here, and SYS/birthdays is an empty template for your own dates. SYS/cal.init is a printer setup for a laser<br>**How:** `cal -m=<month> -y=<year>', with flags. -h marks the holidays in SYS/holidays and anything you add to SYS/birthdays, which it includes. |
| `calcdate` | adds days to a date or counts the days between two: `calcdate 051788 -o 30' prints 061688; dates are mmddyy<br>**How:** Dates are six digits, mmddyy. `calcdate 051788 -o 30' prints the date 30 days on (061688), and a negative offset goes back; `calcdate 010188 -d 123188' prints the days from the first date to the second (365). Years are two digits. |
| `calen` | prints a month as a diary page, ruled for appointments, with the neighbouring months as small calendars in the corners. It reads the month, the year and how many months from its input: `echo 9 2026 1 \| calen'<br>`Invalid flag: -?` |
| `calender` | &#9733; print a whole year's calendar (German)<br>**How:** A whole year at once, in German. It asks `Fuer welches Jahr?' (which year); RETURN at the question ends it. |
| `greg` | &#9733; converts a Julian day number to a Gregorian date: `greg 2461281' is the 29th of August 2026<br>**How:** It converts a Julian day number to a Gregorian date and is nothing to do with regular expressions: `greg 2460000' answers `2023 2 25'. |
| `ticktalk` | tells the time in words -- `Quarter To Two pm' -- in English, French or Afrikaans; give an hour and minute, or none for now<br>**How:** `ticktalk' prints the time now in words; `ticktalk 13 45' prints a given time, Quarter To Two pm. -french and -afrikaans change the language, -before says Twenty To One rather than Twelve Forty, -approximate rounds to five minutes and -noampm drops am and pm. |
| `today` | date, moon phase and this-day-in-history |
| `weekday` | the day of the week, julian day and week number of a date: `weekday 10/30/89' says Monday, day 303, week 44<br>**How:** `weekday 10/30/89' prints the day of the week, the julian day and the week number; with no date it uses today. Dates are mm/dd/yy, dd-mm-yy, yyyy-mm-dd or yy.ddd, and two-digit years are 19yy. -d -D -m -M -y -w -j -n print single parts, -v drops the words between them, -s shortens names. |

**Clocks**

| | |
|---|---|
| `digclk` | &#9733; a clock in block digits with the machine's name above it and the date below, redrawn once a minute, or every so many seconds as given<br>`Usage: digclk [refresh_rate]` |
| `gcl` | &#9733; a grand digital clock: the time drawn large across the terminal and redrawn as it runs.  `-n=<seconds>' runs it for that long; -s scrolls the digits, -i inverts the video<br>**How:** A full-screen digital clock: `gcl' runs until stopped, `gcl -n=10' for ten seconds; -s scrolls the digits, -i inverts the video. |
| `qt` | &#9733; tells the time in words, the way a person would say it: `It's just gone ten past four.' |
| `setimex` | &#9733; checks the system clock against a hardware time source and sets it: -s=<date> sets a date outright, -t tests, and -x or -e make the exit status say whether the time was right<br>`SETIMEX  Version UTIL 2.80 by DESIGNA VLT 03.08.98` |

</details>

## Maths & calculators

*Calculators, plotting, orbits and number theory.*

<details><summary>19 programs</summary>

**Calculators**

| | |
|---|---|
| `bc` | an arbitrary-precision calculator: the numbers are as long as they need to be, and `scale' says how many decimal places to keep.  `2^200' and `scale=40; 1/7' are both answered exactly; -l loads the maths library -- sine, cosine, arctangent, logarithm, exponential<br>`bc 1.01 (Nov 25, 1991), Copyright (C) 1991 Free Software Foundation, Inc.` |
| `cam` | &#9733; camshaft design, not a camera: it asks for the rocker ratio, the lift at each crank angle and the base circle, and plots the lift curve for an intake lobe. The plot is Tektronix vectors, so on a vt100 it arrives as characters -- the dialogue above it is the readable part |
| `chbase` | &#9733; converts a number from one base to another: `chbase 255 10 16' prints FF, and a target base of 0 prints every base from 2 to 36<br>`chbase   : OS9 Utility, created by Philip Maechler` |
| `cvtbase` | converts a number between bases.  The bases are named by key -- b, d, h or x, o -- or by their value, and the number comes on standard input: `echo 255 ! cvtbase d h' answers ff<br>**How:** The bases are the arguments and the numbers come on standard input, one per line: `cvtbase d h' then 255 answers ff; Escape ends it. Bases are named b, d, h or x, o -- or by their digit characters. |
| `dc` | &#9733; an integer desk calculator on the screen, laid out like the Atari ST keypad: type digits and operators, five memory slots down the left, and `dc -b=h' (or d, o, b) sets the base.  Its boxes are Cumana graphic characters; set DCGRAPHIC to six plain ones first, `++++\|-', on any other terminal<br>**How:** A full-screen integer calculator. Set DCGRAPHIC=++++\|- first unless your terminal has the Atari ST's Cumana graphics, then type digits and operators; -b=h, d, o or b picks the base. Needs cio. |
| `factor` | prints the prime factors of each number it is given, or of each it reads, one to a line: `factor 1000001' |
| `hp` | a reverse Polish calculator in floating point: `hp 2 3 +' prints 5.000; on standard input p prints the top of the stack and P the rest; x multiplies and : raises to a power<br>**How:** A reverse Polish calculator in floating point. Given an expression on the command line it prints the result: `hp 2 3 +' prints 5.000 and `hp 2 10 :' 1024.000. Read from standard input it prints only when asked: p prints the top of the stack and P the values below it. + - / and % work as usual, x (or *) multiplies, : or ^ raises to a power, d drops the top value and D empties the stack; < = > & \| and ! compare and combine, leaving 1 or 0; q quits. Dividing by zero stops it. |
| `loan` | &#9733; amortisation calculator: principal, term, rate and start month in, the payment and a month-by-month schedule out<br>**How:** Answers four prompts and prints the schedule for the whole term; pipe it through head or less. |
| `number` | writes numbers out in English words: `number 1234567'<br>`usage: number # ...` |
| `primes` | lists the primes between two numbers: `primes 1 100' |
| `rechne` | &#9733; German command-line calculator: every answer in decimal, hex and binary at once. The expression is one argument with no spaces -- `rechne 4095+1' -- with operators + - x / m (modulo) a o p (and, or, xor) and $ for hex; -b lists the bits set<br>**How:** One expression, no spaces: `rechne 4095+1'. Operators + - x / m a o p; $ff is hex; -b lists the set bits. The other -xx switches decode status codes of the maker's own equipment. |
| `rpn` | &#9733; reverse-Polish calculator on whole numbers. A number typed is pushed; the words add, sub, mul, div and mod combine the top two, and, or, xor and not work bitwise, pr prints an entry, pop discards one. After each line it shows the stack top and depth; ? lists the words, q leaves<br>**How:** Operators are words typed on their own line: 12, 34, add. A + sign is read as the number 0 and pushed. q leaves. |
| `sc` | sc -- spreadsheet calculator (needs TERM)<br>**How:** The spreadsheet, version 6.16. `sc' opens and says "Type '?' for help". It reads TERMCAP as SYS/login sets it, so no `. /dd/SYS/termcap.entry' is needed first. |
| `theorem` | solves y'=f(x,y) by Runge-Kutta and prints x and y a step at a time: `theorem y 0 1 0.1 1' reaches 2.718280, which is e.  `theorem -r 0 0 0 0' reverses standard input instead -- one source, four programs, a 1990 obfuscated-C contest entry<br>**How:** The 1990 contest's Best of Show, and it is four programs in one source. `theorem <expr> <x1> <x2> <h> <y1>' solves the differential equation y'=f(x,y) by Runge-Kutta over the interval, printing x and y a step at a time: `theorem y 0 1 0.1 1' reaches 2.718280, which is e. The expression may use x, y, + - * / and ^, evaluated strictly left to right with no brackets. `theorem -r 0 0 0 0' instead reverses the lines of standard input. Feeding its own source through those two modes is how the other two programs are made; see DOC/ioccc. |

**Science**

| | |
|---|---|
| `chemtab` | a periodic table database from the CRC Handbook: look up one element by name, number or symbol, select elements by up to three properties, mark them on the periodic table, or graph one property against another; full screen, menu keys<br>**How:** Full-screen. Space passes the title page; answer n (or y) to extra explanations and to keeping a transcript. On the main menu 1 looks up one element -- 3, then a symbol such as Fe and Return, shows its melting and boiling points, density, radius, electronegativity and discovery year; 2 selects elements by up to three properties, 3 lists them, 4 marks them on the periodic table, 5 graphs one property against another, 6 quits. Names are typed in lower case. The data is in LIB/chemtab and the manual pages in DOC/chemtab. |

**Simulators**

| | |
|---|---|
| `logisim` | logic circuit simulator -- draws a pulse diagram, a row per node and a column per step, from a circuit written as text. Two sample circuits ship with it, DOC/logisim/counter.lsi and flipflop.lsi, and its notes are DOC/logisim/logisim.doc, in German. It needs `PORT' set to a terminal path, `setenv PORT /term', because it reopens the keyboard through it; Esc stops the run<br>**How:** Set PORT first: `setenv PORT /term'. Without it, `logisim: Environment variable PORT not defined' -- it reopens the keyboard through that path. Two sample circuits ship in DOC/logisim (counter.lsi, flipflop.lsi) and its notes are there too, in German. |

**Spreadsheets**

| | |
|---|---|
| `checkfile` | &#9733; cheque-book register, full screen. A adds a record through a form (item, date as YY/MM/DD, type, description, account, amount -- cheques as negative amounts), R lists the records with the balance, V edits, F picks the data file, Q quits. Records go in testfile.dat in the current directory. Wants TERM<br>**How:** Full screen. A adds a record through a form, C accepts it, R lists the records with the balance, Q quits. Records go in testfile.dat in the current directory; cheques are entered as negative amounts. |
| `oleo` | GNU Oleo 1.6, a spreadsheet. It stops with an illegal instruction before it draws a cell; sc is the spreadsheet that runs<br>**How:** GNU Oleo. It stops with an illegal instruction before drawing a cell; sc is the spreadsheet that runs. |
| `scqref` | &#9733; quick reference for sc, the spreadsheet: a 360-line document that prints itself, in sections A to Q -- options, cursor movement, cell entry, files, ranges and the function lists. `scqref ! less' pages it<br>**How:** `scqref ! less' pages the reference; it is 360 lines. |

</details>

## Printing

*Spoolers, page formatting and PostScript.*

<details><summary>11 programs</summary>

**PostScript**

| | |
|---|---|
| `gs33` | Ghostscript 3.33 -- the older one.  gs403 ships with its init files and fonts; use that<br>`Aladdin Ghostscript 3.33 (4/10/1995)` |
| `gs403` | Aladdin Ghostscript 4.03, the complete build: its init files and fonts are in LIB/gs403. Point GS_LIB at that directory and it interprets -- `export GS_LIB=/dd/LIB/gs403' in bash, not `setenv', which is the OS-9 shell's and is not a bash command. It then reads a PostScript file and drops to its own `GS>' prompt. Runs with no trap handler -- built with GCC 2.5.8 by its porter.<br>**How:** Aladdin Ghostscript 4.03. Point GS_LIB at its library first -- in bash that is `export GS_LIB=/dd/LIB/gs403`, not `setenv`, which is the OS-9 shell's command and gets "setenv: command not found" here. Then `gs403 -q -dNOPAUSE -sDEVICE=nullpage <file>.ps` reads the file and gives you its GS> prompt. Everything it needs, fonts included, is in that directory. gs403 is the complete build; gs33 is the older one. |
| `lwf` | ASCII to PostScript, like Unix enscript.  Reads its prologue from /dd/USR/LIB/lwf.prologue<br>**How:** Turns plain text into PostScript, the way Unix enscript does. It reads /dd/USR/LIB/lwf.prologue and stops without it. No PostScript printer here, so send the output to a file and take it elsewhere. |

**Printers**

| | |
|---|---|
| `alps` | &#9733; Switch an ALPS ASP-1000 printer between draft and NLQ<br>`Syntax: alps [<opts>] >/<device>` |
| `epson` | &#9733; spline output driver for an Epson printer<br>`usage: epson [<opts>]` |
| `lmargin` | &#9733; indent text: it reads standard input and writes it out again with a left margin of the width you ask for -- `lmargin -l4 <file'. Its usage line says `epson' and its help talks about a printer; both came with it from a sibling program, and no byte of its output goes anywhere but standard output. See also `fmt', `proff' and `pep'<br>`usage: epson [<opts>]` |

**Spooling**

| | |
|---|---|
| `lp` | &#9733; submits a file to the lp print spooler: -n=xx makes copies, -d=ptr picks the printer, -m mails you when it is done<br>`Syntax: lp [<opts>] {<path>}` |
| `lpq` | &#9733; shows the spooler queue. It looks for a data module called `spoolqueue' in memory; with a spooler running it reports the queue, and without one answers `no spooler installed'. Same for `prjob' and `lp'.<br>`Syntax: lpq [-p=dev] [user]` |
| `lprm` | &#9733; removes a job from the printer spooler's queue by number; `-' removes every one, and -d=<dev> picks the queue of another printer<br>`Syntax: lprm [-d=dev] [-] job..` |
| `lpshut` | &#9733; shut down the printer scheduler<br>`Syntax: lpshut` |
| `prjob` | &#9733; prints a queued job from the lp spooler; with no spooler installed it says so |

</details>

## Documentation

*Pagers, readers and the help system.*

<details><summary>6 programs</summary>

| | |
|---|---|
| `help` | help system: `help <topic>' pages the topic's article from a .hlp file in SYS/HELP and then offers its subtopics; `help help' explains the format. bash has a help builtin of its own that answers first, so `enable -n help' there Shares its name with a utility of your own -- README-NAMES [no military use -- EFFO-INFO]<br>**How:** `help dinfo'. At bash type `enable -n help' first, or bash's own help builtin answers instead. |
| `helpindex` | &#9733; builds the .ndx index a .hlp help file needs: `helpindex dinfo.hlp' writes dinfo.ndx beside it<br>**How:** `helpindex dinfo.hlp' writes dinfo.ndx beside it. Only names ending .hlp or .hlib are accepted unless -a is given; with no name it asks for one. |
| `less` | shows a file a screenful at a time so it does not scroll past you, and lets you move about in it: space or f for the next screen, b for the one before, / to search forward, n for the next match, h for its help screen (SYS/less.hlp), q to leave.  Reads the terminal's size and codes from TERM and TERMCAP |
| `lessecho` | &#9733; prints its arguments back quoted for a shell -- the helper less uses to hand file names on<br>`usage: lessecho [-ox] [-cx] [-pn] [-dn] [-a] file ...` |
| `lesskey` | turns a key-binding file into the binary less reads: a `#command' section, then one key and one command per line<br>`usage: lesskey [-o output] [input]` |
| `man` | reads one of this disk's own manual pages: `man md5' formats DOC/md5/md5.1 with nroff and pages it with less. `man -k <word>' lists the pages whose name contains the word and `man -w <name>' says where one is.  Every page is indexed in DOC/MANPAGES.  A shell script, so you can read it |

</details>

## G-Windows

*Programs for G-Windows, OS-9's graphical display.  There is no G-Windows here, so what their cards show is each one declining in its own words -- `Unable to access "/win" device', `dclock only runs under G-Windows', a status of 208 or 221.  None of them can be exercised without the display; they are listed for a real OS-9 workstation that has it.*

<details><summary>6 programs</summary>

| | |
|---|---|
| `colortest` | &#9733; reports how G-Windows has its colour look-up table set up. At a terminal it says so and stops -- it wants the /win device, which is the G-Windows display<br>`colortest` |
| `cyberwar` | &#9733; CyberWar -- a game that needs G-Windows |
| `dclock` | &#9733; a digital clock for G-Windows<br>`dclock - digital clock for G-windows` |
| `lfmaker` | makes a G-Windows launch file. It asks the allocator for an address as if it were a length, so the request is refused: `2470464192-byte request refused, 32682944 bytes free'. The number moves with the environment, which is what identifies it as an address. It happens only once the module is already resident: run it bare first, then with an argument |
| `puzzle` | &#9733; sliding-tile puzzle for G-Windows -- it draws through G-Windows, so at a terminal it gets one rule of plus signs out -- the top edge of the tile frame -- and stops.  It is here for a real OS-9 workstation that has G-Windows |
| `scriptmaster` | &#9733; G-Windows scripting tool |

</details>

## Needs hardware

*Programs that drive hardware this collection has no way to reach -- a graphics display of the kind a GEPARD or an MM/1 carries, or a printer on its own SCF device.  WE CANNOT TEST ANY OF THESE, at all: what is written about them comes from their own text and their code, not from watching them work.  They are here for a real machine that has the hardware.*

<details><summary>12 programs</summary>

**Display**

| | |
|---|---|
| `apfel` | the Mandelbrot set (Apfelmaennchen) drawn on the Atari Graph display; it calls the `graph' trap library |
| `g` | &#9733; an Atari Graph demonstration, paired with striche. It calls the `graph' trap library, so load that first; it then aborts on a supervisor-only instruction, having been written to run in supervisor state |
| `graphdemo` | a demonstration of the Atari Graph display; it calls the `graph' trap library |
| `graphsave` | save an Atari GRAPH screen.  Aborts with the `graph' trap library resident, like `showpic': it wants the display |
| `showpic` | show a picture on the Atari GRAPH display.  With the `graph' trap library resident it is entered and aborts: it wants the display, not just the library. |
| `sine` | a sine plot on the Atari Graph display; it calls the `graph' trap library |
| `striche` | &#9733; line drawing for the Atari Graph display; it calls the `graph' trap library, so load that first |
| `umusek` | UMusEK -- a music editor.  It needs a hardware graphics screen: point it at one and it opens.  Without a graphics screen it stops with `***DS_ScAdd Error 208.' and `Fran: Can't get screen addr, 'bye!'. |

**Printers**

| | |
|---|---|
| `lpsched` | &#9733; starts the lp print spooler on a printer device; -r restarts it<br>`Syntax: lpsched [-r] {<devname>}` |
| `splman` | &#9733; OS-9 print spooler: the manager.  It wants a printer on an SCF device to spool to.  `splprt' is the process that drives the printer and `splstat' shows the queue; the three go together |
| `splprt` | &#9733; OS-9 print spooler: the printer process, one per printer. It wants an SCF device to write to |
| `splstat` | &#9733; OS-9 print spooler: queue status.  It reads the spooler's queue.  The other spooler on this disk speaks up when its queue is empty: `lpq: no spooler installed', `lpshut: no spooler active', `prjob: Spooler not installed'. |

</details>

---

&#9733; marks a program that uses Microware's `cio`, which ships on the disk, included with Microware's permission; `DOC/README-CIO` has the details.

Generated by `tools/gen_catalog.py` from the disk's own documents. Do not edit by hand; it will be overwritten.
