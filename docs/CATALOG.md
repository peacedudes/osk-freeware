# What is on this disk

1117 programs of OS-9/68000 community software, by what each is for.  A star marks a program that uses Microware's `cio`, which is on the disk too.

`docs/index.html` has a card for each, with a screen of it running.  On the disk, `man <name>` reads its documents.

| Category | Programs | |
|---|--:|---|
| [Shells](#shells) | 25 | Unix shells to sit beside OS-9's own -- bash and ksh bring history, job control, and scripts that come across unchanged. |
| [Editors](#editors) | 22 | vi and emacs in several flavours, line and stream editors, and editors for binary and hex. |
| [Text tools](#text-tools) | 140 | Search, sort, compare, reformat, split and spell-check. |
| [Files & directories](#files--directories) | 38 | Listing, copying, finding, renaming, and knowing what you have. |
| [Developer tools](#developer-tools) | 39 | Version control, tags, cross-reference, formatters, a debugger and benchmarks. |
| [Compilers & build](#compilers--build) | 49 | C compilers and their passes, assemblers, linkers, make and parser generators. |
| [Languages](#languages) | 16 | Interpreters and language systems beyond C. |
| [Archives & compression](#archives--compression) | 34 | Pack, unpack and shrink -- lha, zip, tar, arc, zoo, and OS-9 module libraries. |
| [Encoding & conversion](#encoding--conversion) | 34 | Between text encodings, line endings, Macintosh formats, ciphers and hashes. |
| [Communications](#communications) | 123 | Kermit in several builds, terminal sessions, and networking. |
| [Graphics & images](#graphics--images) | 191 | The netpbm toolkit, JPEG, a ray tracer, and things that draw. |
| [Games](#games) | 117 | Adventures, board and card games, arcade ports, dungeon crawls and puzzles. |
| [Screen toys](#screen-toys) | 10 | Animations and screen effects -- they draw on the terminal rather than print to it. Some run until you stop them. |
| [Amusements](#amusements) | 39 | Generators, simulators and diversions that are not quite games. |
| [System & modules](#system--modules) | 141 | OS-9 module and process tools, devices, system state and scheduling. |
| [Disk & DOS](#disk--dos) | 20 | Reading and writing MS-DOS media with the mtools set. |
| [Time & calendar](#time--calendar) | 18 | Calendars, clocks and astronomy. |
| [Maths & calculators](#maths--calculators) | 20 | Calculators, plotting, orbits and number theory. |
| [Printing](#printing) | 11 | Spoolers, page formatting and PostScript. |
| [Documentation](#documentation) | 8 | Pagers, readers and the help system. |
| [G-Windows](#g-windows) | 6 | Programs for G-Windows, OS-9's graphical display.  There is none here, so each card shows the program saying so. |
| [Needs hardware](#needs-hardware) | 16 | Programs for hardware out of our reach: a GEPARD or MM/1 display, a printer on its own port.  Untested here; what is said of them comes from their own text and code. |

## Shells

*Unix shells to sit beside OS-9's own -- bash and ksh bring history, job control, and scripts that come across unchanged.*

<details><summary>25 programs</summary>

**Shell helpers**

| | |
|---|---|
| `checkenv` | &#9733; tests an environment variable for a script: `checkenv TERM vt100' exits 0 when TERM is vt100 and 1 when not. The comma in its usage line is not typed<br>**How:** `checkenv <name> <value>', no comma: status 0 when they match, 1 when they differ. Typed with the comma from its syntax line, it prints that line and returns 0. |
| `exist` | &#9733; test whether a file exists and answer in the exit status: 0 if it does, 1 if it does not. -n inverts the test, -d asks whether the name is a directory. German: its help is headed `Aufruf' and `Rueckgabewerte'<br>`EXIST    Version UTIL 2.40 by DESIGNA VLT 24.11.97` |
| `getenv` | &#9733; prints or tests an environment variable: `getenv -p TERM' prints with a newline, -l without, -x exits with the value, -n inverts the test. With no option it prints its usage. Messages are in German<br>`GETENV   Version UTIL 2.40 by DESIGNA VLT 24.11.97` |
| `hist` | a command-line editor with C-shell-style history in front of Microware's shell: `h' lists it, `logout' leaves.  Name a history file; the default is on the RAM disk /r0 [no military use -- EFFO-INFO]<br>**How:** A command-line editor with C-shell-style history in front of Microware's shell, which runs each command it is given; load your own OS-9's `shell' and `tmode' first. `hist <file>' keeps the history in that file (the default is /r0/history, on a RAM disk: `mount -r=256k /r0'); `h' lists it and `logout' leaves. |
| `if` | conditional execution for a shell script: `if def <var>', `if loaded <module>' or `if varval <var> <value>', the commands, `else', `endif'.  It hands the branch to Microware's `shell' to run<br>**How:** bash's own `if' is a reserved word; `command if' reaches the one on this disk. |
| `printenv` | &#9733; print the environment. Shares its name with a utility of your own -- README-NAMES<br>`**** PRINTENV Utility for use with ZSH, (c) 1989 by L.Zeller ****` |
| `printf` | formatted print from the shell, as on Unix: widths, numbers and floating point<br>**How:** printf as on Unix: `printf "%-8s\|%5d\n" name 12'. Widths, numbers and floating point all work. |
| `qp` | expands back-quotes in a command line, which Microware's shell does not do for itself: `qp <cmd> <args>'. It runs each quoted command, and then the whole line, with $SHELL -- `shell' if that is unset<br>**How:** Put the command in back-quotes where its output belongs: `qp wc -c `cat list`'. From bash or ksh, quote the back-quoted part -- '`cat list`' -- or the shell expands it before qp sees it. Each piece runs under $SHELL (ksh after SYS/login). |
| `run` | runs a program with its input and output on the terminal PORT names: `run '<program> <args>''<br>**How:** `run '<program> <args>'' with PORT naming a terminal: the program runs with its input and output on that terminal. |
| `strcmp` | &#9733; compares two strings and answers in its exit status for a shell `if': `strcmp abc eq abc' is true. Operators eq lt gt le ge ne, `ct' contains, `bw' begins with. `-c' ignores case, `-p' prints the answer. DOC/strcmp<br>`strcmp v2.1 (c) M.C.Gregorie, 1994` |
| `submit` | &#9733; runs a .sub batch file line by line, printing each line first: `submit demo' for demo.sub. Lines go to `shell', so your own OS-9 shell must be resident; SYS/login loads it from /h1<br>`Syntax: submit [<opts>] [<submit file>] [{<parameter>)]` |
| `xargs` | builds command lines out of what it reads and runs them: `ls \| xargs cat' hands the names to cat as arguments rather than as input |
| `xc` | runs the commands marked in a file -- a line beginning `% ' -- and leaves the rest as notes.  Forks them through Microware's `shell' to run<br>**How:** `xc <file>': lines beginning `% ' are commands, shown and run; `$ ' runs them quietly; the rest is notes. It forks them through Microware's `shell', which must be loaded (`load /h1/CMDS/shell'). |
| `yes` | prints `y', or the words it is given, over and over until the program reading it stops -- for answering prompts |

**Shell utilities**

| | |
|---|---|
| `env` | &#9733; GNU env: runs a command with variables added to its environment, `env FOO=bar printenv'<br>`Usage: env [OPTION]... [-] [NAME=VALUE]... [COMMAND [ARG]...]` |
| `expr` | &#9733; GNU expr: evaluates an expression for a script -- arithmetic, comparisons, string length and matching |
| `logname` | &#9733; prints the login name the password file gives for the number your process actually runs as -- which is not necessarily $USER: as the super-user it answers `root', and as tester `tester'.  GNU sh-utils' logname<br>`Usage: logname [OPTION]...` |
| `su` | &#9733; GNU su: become another user; its options are under `su --help'. Shares its name with a utility of your own -- README-NAMES<br>`Usage: su [OPTION]... [-] [USER [ARG]...]` |
| `whoami` | &#9733; prints the user you are running as, looked up from the process's owner number (unlike $USER, which is only what the environment says) -- the same answer as `logname'<br>`Usage: whoami [OPTION]...` |

**Shells**

| | |
|---|---|
| `bash` | GNU Bourne-Again Shell 1.12, this disk's shell; it reads .bashrc. It cannot be $SHELL for programs that shell out, since it reads system()'s command line as a script name; SYS/login sets SHELL to `ksh'. DOC/README-SHELLS compares the shells |
| `gshell` | GSHELL V1.1, a full-screen menu shell: a lettered directory list, `+' and `-' to page, `.' to change directory, a letter to run a file. `assembler', `compiler' and `editor' are the same menu for one job each. DOC/README-SHELLS<br>**How:** A full-screen menu of the current directory: + and - page, . changes directory, a letter runs that file. Control-C leaves it. |
| `ksh` | the Korn shell, pd-ksh: a full shell with a prompt, history, for loops, variables and functions, and `ksh -c "<commands>"' runs a line. It is the shell programs on this disk shell out through. DOC/README-KSH |
| `mshell` | &#9733; a menu shell: `mshell <menufile>' shows one numbered entry per `label\| command' line and a number runs that command -- through Microware's `shell'. Shares its name with a utility of your own -- README-NAMES<br>**How:** `mshell <menufile>': one `label\| command' per line, up to ten. A number picks an entry; it hands the command to Microware's `shell', which must be loaded, then waits for RETURN. Control-C leaves it. |
| `sh` | an sh-like shell, version 2.1, close to both Microware's shell and the Bourne shell; the startup script runs under it. It has a real `chd', but cannot fork a program by absolute pathname here. DOC/README-SHELLS<br>`Syntax: sh [<opts>] [<scriptfile>] [<arg1>] ... [<argn>]` |
| `wish` | WiSH, a full-screen windowing shell over the OS-9 shell: a file window and a command line. Labelled keys are terminal function keys; the control keys always work, Ctrl-D leaves. English at the keyboard. Unrelated to GAMES' hackwish<br>**How:** WiSH, a windowing shell over the OS-9 shell. Type a command on the top line (`ls', `dir', anything), Enter runs it through the OS-9 shell and pages the output -- press Enter again to return to the window. The labelled keys along the foot are terminal function keys a vt100 does not send; the control keys always work: Ctrl-P/N/B/F move the cursor over the file window, Tab moves right, Ctrl-A marks the file under the cursor, Ctrl-U unmarks all, Ctrl-W copies the cursor's name onto the command line, Ctrl-L redraws, Ctrl-V/Ctrl-Z page. **Ctrl-D leaves.** German program, English at the keyboard. (hackwish, in GAMES, is the unrelated hack cheat.) |

</details>

## Editors

*vi and emacs in several flavours, line and stream editors, and editors for binary and hex.*

<details><summary>22 programs</summary>

**Alternates**

| | |
|---|---|
| `sed_1.06` | &#9733; the same GNU sed 1.06 binary as sed, its module renamed to match its file name<br>`Syntax   : sed [<opts>] [<file>]` |

**Binary & hex**

| | |
|---|---|
| `beav` | BEAV 1.40 -- Binary Editor And Viewer (needs TERM)<br>**How:** Full-screen binary editor: `beav <file>'. Control-C leaves it. |
| `hexed` | a hex editor built on your text editor: it writes the file as a hex dump, opens it in the editor `-e=' names (default vi), and writes the file back when you leave. `-t=<dir>' says where the dump goes, else /r0 [no military use -- EFFO-INFO]<br>**How:** `hexed -t=<dir> -e=<editor> <file>': the file goes out as a hex dump into <dir>, the editor opens it, and leaving the editor writes the file back. Without -t it uses /r0. |
| `hexedit` | HEXPERT V2.4, a hex viewer and editor: `hexedit <file>' shows the file as hex and as text side by side; the arrow keys page, `e' edits the page, `q' leaves.  -d opens a directory for editing, for the super-user only<br>**How:** `hexedit <file>'. Put the termcap entry in TERMCAP first (`. /dd/SYS/termcap.entry') or it will not draw. |
| `pbyte` | &#9733; patches bytes in a file at a hex offset: `pbyte <file> <offset> <byte>...'<br>`Syntax: pbyte <path> <hex_offset> <hex_byte> [<hex_byte>]` |

**emacs family**

| | |
|---|---|
| `em` | MicroEMACS 3.8b, a screen editor with Emacs keys<br>**How:** A screen editor. It stops with "Environment variable TERM not defined!" unless TERM is set -- SYS/login sets it, so run it from a login shell rather than bare. |
| `emacs` | &#9733; MicroEMACS 4.00, a full-screen editor with Emacs keys and a macro language. It finds .emacsrc and emacs.hlp in your home or current directory or on PATH; the macros are in USR/LIB/EMACS and emacs.hlp in SYS, so put both on PATH for ESC ? help<br>**How:** Full-screen editor, MicroEMACS keys. Control-X control-C quits. It finds its startup and help files in your home directory, the current one or a PATH directory, not in USR/LIB/EMACS where they ship. |
| `me` | MicroEMACS 3.11, a screen editor with Emacs keys and German messages (Datei for File); needs TERM set<br>**How:** Full-screen editor, MicroEMACS keys, German messages. Control-X control-C quits. |
| `mg` | &#9733; Mg, a small MicroGnuEmacs -- Emacs keys in 79K, its documentation under DOC/mg.<br>**How:** Full-screen editor, Emacs keys. Control-X control-C quits. |
| `umacs` | &#9733; uMacs 1.0, MicroEMACS in 45K -- the same keys, keyboard macros included, with .umacsrc for its startup file. Shares its name with a utility of your own -- README-NAMES<br>**How:** A small Emacs (uMacs 1.0). Full-screen: it takes the display and shows "== uMacs 1.0 == main ==" at the foot. It needs only TERM set. |

**Line & stream**

| | |
|---|---|
| `ed` | &#9733; GNU ed 0.2, the line editor.  It keeps its scratch file on /r0, a RAM disk, so mount one (`mount -r=256k /r0'); DOC/README-RUNNING has the details<br>**How:** Needs a /r0 RAM disk for its scratch file; `mount -r=256k /r0' provides one. Then `ed <file>', with ed's usual commands: 1,4p prints, s/a/b/ substitutes, w writes, q quits. |
| `editor` | a full-screen file picker that hands the chosen file to `umacs': a lettered directory list, `+' and `-' to page, `.' to change directory, `!' to leave. A directory named on the command line is where it starts<br>**How:** Run it bare: a full-screen file picker for umacs. Given a file on the command line it stops on an illegal instruction. Control-C leaves the menu. |
| `sed` | &#9733; sed, the stream editor: substitutes, deletes and prints, with -n for no default output, -e for a script line and -f for a script file.  DOC/sed/sed.man is the manual<br>`Syntax   : sed [<opts>] [<file>]` |

**vi clones**

| | |
|---|---|
| `elvis` | Elvis 1.7, a vi and ex clone; manual in DOC/elvis. Needs TERM and TERMCAP, and a tmp directory on /dd for its scratch file (the disk has one). Also installed as view (read-only) and REBUILT/vi.elvis. DOC/README-VI compares the vi editors<br>**How:** A full vi/ex clone. Needs TERM and TERMCAP set -- `SYS/login' does both. `view' opens read-only, REBUILT/vi.elvis is the same program as vi, and all of them exec CMDS/elvis, so it must be present. |
| `elvis_input` | elvis opening straight into insert mode. Elvis picks its personality from the last letter of the name it is run by, so keep the name. CMDS/input is an unrelated program |
| `elvprsv` | preserves elvis's buffer when elvis dies, for elvrec to recover; elvis runs it itself |
| `elvrec` | recovers an elvis buffer saved when elvis died. With no arguments it lists what is recoverable; silence means nothing was saved. It reads usr/preserve on /dd, where elvprsv saves. DOC/elvrec/elvrec.doc<br>**How:** Bare, it lists what elvis preserved; nothing listed means nothing was preserved. |
| `stevie` | STEVIE, a small vi clone with vi's movement, operators and colon commands; needs only TERM. `stevie <file>' opens, `:wq' saves, `:q' leaves. Quick reference in DOC/stevie |
| `vi.elvis` | elvis 1.7, kept as vi.elvis because CMDS/vi is PVIC, an unrelated vi clone |
| `view` | elvis opened read-only |

**vi family**

| | |
|---|---|
| `vi` | PVIC 1.0a, the Portable VI Clone: a full-screen vi with ex mode, public domain.  Reads TERM and the termcap; see DOC/README-VI to choose between this and `elvis'<br>**How:** PVIC 1.0a, the Portable VI Clone and this disk's `vi', public domain. Source in SRC/pvic. Reads TERM and the termcap, so `. /dd/SYS/termcap.entry' first on a terminal it does not know. DOC/README-VI compares it with `elvis'. |
| `vi_1.0` | PVIC 1.0, the Portable VI Clone, public domain; CMDS/vi is PVIC 1.0a<br>`Usage: vi [file ...]` |

</details>

## Text tools

*Search, sort, compare, reformat, split and spell-check.*

<details><summary>140 programs</summary>

**Alternates**

| | |
|---|---|
| `diff_1.1` | GNU diff 1.1, the archive's build, with the same options; CMDS/diff is GNU diff 1.4<br>`Syntax   : diff [<options>] file1 file2` |

**Banners & text art**

| | |
|---|---|
| `banner` | &#9733; prints its argument as tall letters made of `@', for a banner or a sign |
| `banner1` | a banner program: its argument in large letters, -d doubles, -i slants, -c=<char> picks the character and -s builds each letter out of itself; -z=<file> banners a file<br>**How:** Prints its arguments as tall letters, eight rows high. `banner1 -d' doubles the size, `-i' slants them, `-c=<char>' builds them from a character of your choosing and `-s' builds each letter out of itself. `-z=<file>' banners each line of a file instead, and `-z' alone reads standard input. Its own usage text calls it `banner', which is the name it had in 1987; the disk's `banner' is a different program. |
| `cursive` | writes a message as one line of joined, sloping cursive script, the flourish people once signed mail with<br>`usage: cursive [-tn] [-in] message` |
| `gothic` | &#9733; print text as a gothic/blackletter banner |
| `zot` | &#9733; prints a line of text in one of fourteen animated styles -- the letters slide in, bounce, sort themselves or turn up one at a time: `zot -s=14 "text"'; -s names the styles, -d plays them all<br>**How:** `zot -s=<1-14> "text"' animates the text in that style -- the letters slide in, bounce, sort themselves or turn up one at a time, each frame overwriting the last with a bare CR; `zot -s' names the fourteen styles; `zot -d "text"' plays them all in turn.  Under os9exec, -r (unpaced output) makes every animation instantaneous, so you see only the finished line. |

**Count & inspect**

| | |
|---|---|
| `ascii` | &#9733; prints the ASCII character table: every code from 0 to 127 with its control name, decimal, hex and octal |
| `charcnt` | &#9733; counts how often each character occurs in the files named, control characters included, and totals the bytes read |
| `dump` | the hex dump: shows a file, or a module in memory (-m), as offsets, hex bytes and the characters beside them. Shares its name with a utility of your own -- README-NAMES<br>**How:** The hex dump: `dump <file>' prints offsets, bytes and the ASCII beside them. |
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
| `dvialw` | turns a TeX .dvi file into PostScript for an Apple LaserWriter<br>**How:** Works, and so do the other nine dvi* drivers. The disk ships the MetaFont sources, not the ready-made bitmaps, so each driver says "Font file [cmr10 [300 dpi]] could not be opened ... Proceeding with zero size characters" once per font and writes a page with the right layout and no glyphs. FONTS/PK300 and PK144 hold a Makefile each; generate the bitmaps from the MetaFont sources in SYS/TEX/MFINPUTS. Output goes to <dvifile>_alw beside the input, not to standard output. |
| `dvidjp` | turns a .dvi file into output for an HP DeskJet Plus<br>`[TeX82 DVI Translator Version 2.10]` |
| `dvieps` | turns a .dvi file into output for an Epson 9-pin dot-matrix printer<br>`[TeX82 DVI Translator Version 2.10 [experimental]]` |
| `dviimp` | turns a .dvi file into imPRESS for an Imagen laser printer<br>`[TeX82 DVI Translator Version 2.10]` |
| `dvijep` | turns a .dvi file into output for an HP LaserJet Plus<br>`[TeX82 DVI Translator Version 2.10]` |
| `dvijet` | turns a .dvi file into output for an HP 2686A LaserJet<br>`[TeX82 DVI Translator Version 2.10]` |
| `dvilj2` | turns a .dvi file into output for an HP LaserJet II<br>`[TeX82 DVI Translator Version 2.10]` |
| `dvimac` | turns a .dvi file into output for an Apple ImageWriter (144 dpi)<br>`[TeX82 DVI Translator Version 2.10]` |
| `dvioki` | turns a .dvi file into output for an Okidata 192 dot-matrix printer<br>`[TeX82 DVI Translator Version 2.10]` |
| `dvitos` | turns a .dvi file into output for a Toshiba P-1351 dot-matrix printer<br>`[TeX82 DVI Translator Version 2.10]` |

**Format & typeset**

| | |
|---|---|
| `col` | filters reverse and half-line feeds out of text, so nroff's output reads on a terminal; -b drops backspaces and keeps the last character struck in each column<br>`col: illegal option -- ?` |
| `column` | sets a list out in columns across the screen; -t lines a table up, -x fills rows before columns; $COLUMNS sets the width<br>`column: illegal option -- ?` |
| `fmt` | refills ragged text into even lines, 72 columns wide or as given by -<width>; the fmt that came with elvis<br>`usage: fmt [-width] [files]...` |
| `hc` | shifts text to a column or labels every line: `hc +8 f' indents so text starts at column 8, `hc -11 f' strips columns so it starts at 11, `hc -l "> " f' prefixes each line. With no option it copies the file<br>`hc: unrecognized option=-?` |
| `lout` | Lout 2.05 document formatter<br>`usage: lout [ -i<filename> ] files` |
| `nroff` | nroff, the text formatter: fills and justifies text under dot requests and macro packages (-man and the rest); the macro sets are in LIB, and TMACDIR points at them<br>**How:** Formats a text with nroff requests: `nroff file.ms'. Its macro sets are in LIB (tmac.*). Point TMACDIR at LIB if a macro package is not found. |
| `proff` | proff, a portable roff: formats text under dot requests -- fill, justify, centre, running page headers -- with its macros in LIB/proff; +n and -n select pages, -v prints statistics<br>`usage: proff [+n] [-n] [-v] [-ifile] [-s] [-pon] [infile [outfile]]` |
| `roff` | a text formatter in the nroff line: it reads text with dot-commands at the start of a line and fills, justifies and paginates it. DOC/roff has the full request list; nroff and proff are the same idea<br>`Syntax: roff {[+00] [-00] [-s] -[h] file}` |
| `soelim` | copies roff source to standard output with each file named by .so or .nx put in its place -- run it before nroff<br>**How:** `soelim file.r > whole.r' copies roff source with every file named on a .so or .nx line put in that line's place, so a formatter that does not follow .so gets the whole text; `-' names standard input. Paths are taken relative to the current directory. |
| `tformat` | fills text to a width: `tformat [width]' reads standard input and writes it refilled and justified, 80 columns unless told otherwise<br>`tformat - format stdin to stdout.` |
| `ul` | turns underlining made with backspaces into what the terminal shows as underline; -i puts the underline on a line of its own<br>`ul: illegal option -- ?` |
| `xfmt` | refills ragged text to 72 columns or the width -l gives; -m understands nroff -man requests, -x a little TeX, -c C source, and -u shows fonts as terminal attributes. Manual in DOC/xfmt<br>**How:** Refills ragged text into even lines: `xfmt file' fills to 72 columns and `-l 30' to any width; with no file named it reads standard input. `-m' interprets the nroff -man requests a manual page is written in, `-x' a few TeX commands, and `-c' marks up C source. `-j' justifies, `-i' keeps indentation, `-p n' shifts the text right. With `-u' the fonts become your terminal's attributes and TERM must be set; `-o' overstrikes instead. An unknown option prints the usage line. The manual is DOC/xfmt/xfmt.1, and DOC/xfmt/cmds.tex lists the commands it knows. |

**Fortune & sayings**

| | |
|---|---|
| `cookhash` | build the hash file cookie(1) needs, from a sayings file<br>`usage: cookhash <cookiefile >hashfile` |
| `cookie` | print a random fortune cookie<br>**How:** Bare it prints a fortune from a default file. Given arguments it wants both the cookie file and the hash `strfile' built for it: `strfile mine' then `cookie mine mine.dat'. |
| `fortune` | prints a random quotation. -s keeps to short ones, -l to long, -w pauses to let you read, -o uses the offensive file; a file name of your own is read instead<br>`usage:  fortune [ - ] [ -wsloa ] [ file ]` |
| `psychic` | a fortune teller: psychic messages strung together from stock phrases, three unless you give a number<br>**How:** `psychic' prints three psychic messages, `psychic 1' one; each is assembled at random from stock phrases. |
| `sonnet` | writes (bad) sonnets in iambic pentameter, full screen: mark the lines you like and recompose the rest; w appends the poem to a file and -l <file> loads one it wrote to go on working on it<br>**How:** Full-screen: it takes over the display. **ESC quits**, so does q at its prompt. Commands at the prompt: m# / u# mark and unmark a line, r recomposes the unmarked lines, w [file] appends the poem to a file (sonnet.out by default, -f <file> changes that). `sonnet -l <file>' loads a poem it wrote with w -- fourteen lines -- and refuses any other file. The vocabulary is compiled in (SRC/sonnet/lex.data through makelex), not read at run time. |
| `strfile` | &#9733; builds the .dat index that fortune reads from a file of sayings separated by %% lines, and reports what it found<br>`usage:  strfile [ - ] [ -cC ] [ -sv ] inputfile [ datafile ]` |
| `unstr` | strfile's reverse: writes the sayings back out of a fortune .dat index as plain text -- `unstr sayings.dat out'; the .dat may be left off the name<br>`usage: unstr datafile[.dat] [ outfile ]` |

**KWIC index**

| | |
|---|---|
| `pagefraz` | the KWIC index suite: breaks a Stylo-spooled text into overlapping phrases of four words, one per line with its page number<br>`Syntax: pagefraz <opts> [<in_path> [<out_path>]] <opts>` |
| `pagekwic` | the KWIC index suite: slides a window of -f words along a Stylo-spooled text and prints every rotation of each window with its page number, the first step of a keyword-in-context index<br>`Syntax: pagekwic <opts> [<in_path> [<out_path>]] <opts>` |
| `pageline` | the KWIC index suite: splits a Stylo-spooled text into one word per line with its page number<br>`Syntax: pageline <opts> [<in_path> [<out_path>]] <opts>` |

**Search & match**

| | |
|---|---|
| `agrep` | grep that forgives spelling: `agrep -2 homogenos file' finds `homogeneous', allowing two letters wrong, missing or extra. -i ignores case, -w matches whole words, -c counts, -f reads patterns from a file, -d sets the record delimiter (`-d "^From "' for a mailbox)<br>**How:** Like grep, but a number option allows mistakes: `agrep -1 recieve file' finds `receive', one substitution, insertion or deletion away. -i ignores case, -w wants whole words, -c counts matching records, -l names the files, -v inverts, -f patfile searches for every pattern in patfile, and -d sets the record delimiter, so `agrep -d "^From " word mailbox' prints whole messages. Bare, it prints its option summary. |
| `bmg` | &#9733; a fast grep by the Boyer-Moore algorithm: searches files for one or more fixed strings, with counts, file lists and character offsets on request<br>`bm: search for a given string or strings in a file or files` |
| `bmgtest` | Boyer-Moore-Gosper substring search: `bmgtest <pattern> <file>' prints the lines that match, and it reads standard input if you name no file.  -i ignores case, -n numbers the lines<br>**How:** bmgtest [-i] [-n] <pattern> [file ...]. A demonstration of Boyer-Moore-Gosper searching. |
| `bmgtest2` | Boyer-Moore-Gosper substring search, a second driver over the same routines in SRC/strsch; the same arguments as `bmgtest'<br>`usage: bmgtest [-i] [-n] pattern [file ...]` |
| `fgrep` | &#9733; searches files for fixed strings rather than patterns, with context lines, counts, line numbers and file lists on request<br>`Syntax   : fgrep [-[[AB] ]<num>] [-[CVchilnsvwx]] [-[ef]] <expr> [<files...>]` |
| `ggrep` | &#9733; GNU grep, a second build: the same options as `grep'<br>**How:** GNU grep. `ggrep <expr> <files...>'; -E, -F, -i, -v, -w and the rest as you would expect. |
| `grep` | GNU grep 2.0: prints the lines of files that match a regular expression -- -E extended, -F fixed strings, -i ignore case, -v invert, -n number, -c count. Shares its name with a utility of your own -- README-NAMES<br>`grep: illegal option -- ?` |
| `lgrep` | &#9733; list the files a pattern appears in -- its banner says "same as 'grep -l', but prints filenames without comments". It runs your own OS-9's `grep'; load that first. DOC/README-GREP compares the six searchers<br>`Syntax: lgrep <arg1> ... <argn>` |
| `look` | prints the lines of a sorted file that begin with a string: `look abs GAMES/words'; -f ignores case<br>`usage: look [-f] string file` |
| `sgrep` | grep with substitution: `sgrep pats <in' replaces each odd line of pats with the even line after it. -m only matches (-c counts, -n numbers, -v inverts), -y ignores case. Manual: DOC/sgrep.doc<br>**How:** A filter: `sgrep patfile <input'. patfile holds pairs of lines, a pattern and what to put in its place, and every match in the input is replaced. With -m the file is a plain list of patterns and matching lines are printed (-c counts them, -n numbers them, -v inverts). -y ignores case. Patterns use `:a' letters, `:d' digits, `:n' alphanumerics, `*' `+' `-' repeats, and `?1' in a replacement is the first wildcard's text. DOC/sgrep.doc is its manual. |
| `soundex` | Soundex phonetic key for each word on stdin |
| `wns` | &#9733; windowing search: grep that prints a window of lines round each match.  `wns -w=2 pattern file' shows two lines before and after, -a and -b set them apart, and windows that do not touch are divided by a dashed line<br>**How:** A grep with context: `wns -w=2 pattern file' prints two lines either side of each match, -a and -b set the after and before counts separately. Needs cio. |

**Sort, compare & merge**

| | |
|---|---|
| `cdiff` | a context diff: compares two text files and prints what changed, each difference headed by a line such as `>>>> INSERT BEFORE 2'<br>`TRY: diff oldfile newfile` |
| `comm` | compares two sorted files: the lines only in the first, only in the second, and in both, in three columns; -1, -2 and -3 leave a column out<br>`comm: illegal option -- ?` |
| `diff` | compares two text files and prints the lines that differ, in normal, context (-c) or ed-script (-e) form; reads CR-terminated text. GNU diff 1.4, built from SRC/diff -- the archive's GNU diff 1.1 is REBUILT/diff_1.1<br>`diff: illegal option -- ?` |
| `diff3` | compares three files at once and shows where each differs from the others -- GNU diff3 1.4, the tool a three-way merge is built on. `diff3 mine older theirs'. Source in SRC/gnudiff<br>`diff3: illegal option -- ?` |
| `ediff` | puts `diff' output into plain English: `diff <f1> <f2> ! ediff', or `ediff <file' for a saved diff. A change reads like `1 line changed at 3 from: ... to: ...'<br>`Syntax   : 'ediff <file'  or  'diff <f1> <f2> ! ediff'` |
| `fcomp` | &#9733; compares two text files line by line and names the lines inserted, deleted or changed between them<br>`Syntax: fcomp <file_1> <file_2>` |
| `join` | GNU join -- relational join of two sorted files<br>``join: unrecognized option `-?'`` |
| `nsort` | sorts lines from standard input, in lexical order. For a numeric sort use `sort -n'<br>`Usage: nsort <unordered >sorted` |
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
| `slice` | splits a file at each line matching a pattern, or every n lines, into files named by a format: `slice -f notes -x '^--' part#n' writes part1, part2 ... without the cut lines; -m files a mailbox by message date. DOC/slice/slice.1<br>`slice: Unknown flag -?` |
| `split` | GNU split: cuts a file into pieces of so many lines (-l) or bytes (-b), named after a prefix -- partaa, partab and so on<br>``split: unrecognized option `-?'`` |

**TeX**

| | |
|---|---|
| `afm2tfm` | turns an Adobe .afm font metric file into the .tfm TeX reads<br>`afm2tfm 7.0, Copyright 1990-92 by Radical Eye Software` |
| `bibtex` | BibTeX, the bibliography formatter. It prompts for the job name on standard input (`Please type input file name'). The .bst styles plain, unsrt, abbrv and alpha are in SYS/TEX/INPUTS<br>**How:** It reads the job name from standard input -- `Please type input file name (no extension)--' is a prompt, not silence. The .bst styles are in SYS/TEX/INPUTS (plain, unsrt, abbrv, alpha), not SYS/TEX/BIB, which holds one read.me. A backslash cannot be TYPED at this shell -- bash's echo eats `\c' -- so patch one in with `pbyte <file> <hex offset> 5c'. |
| `dvips` | DVI to PostScript, dvipsk 5.495b, the fuller of the two PostScript drivers (dvialw is the other): `dvips <file>.dvi -o <file>.ps'. A font size not yet built is left blank; `-M' stops it offering to make one. Source: SRC/dvips<br>**How:** DVI to PostScript: `dvips <file>.dvi -o <file>.ps'. Its prologues ship in SYS/TEX/DVIPS and it finds them there. A font size nobody has built is reported and left blank; `-M' stops it offering to make one. |
| `dvitype` | prints what is inside a .dvi file, as text<br>**How:** `dvitype <file>.dvi < /nil'. It asks five questions -- output level, starting page, page count, device resolution, magnification -- and takes the default for each at end of file. Redirect its input so a script does not wait on the questions. |
| `gftopk` | MetaFont generic font to packed font<br>**How:** `gftopk cmr10.120gf /dd/tmp/cmr10.120pk'. GFFONTS must name where the input is; the output path is never searched for, so an absolute one works with nothing set. |
| `gftype` | show what is inside a .gf file<br>**How:** `gftype -i <font>.<dpi>gf' draws the glyphs as asterisks; -m adds the opcodes. GFFONTS must name the directory -- the compiled-in FONTS paths do not begin with `.', so a file beside you is invisible. |
| `inimf` | MetaFont with no base preloaded<br>**How:** It builds a Metafont base, which SYS/TEX/MFBASES now ships. To rebuild: `echo "plain; \input modes; dump" > mf.in' then `ksh -c "cd /dd/tmp; inimf < mf.in"'. About a minute. DOC/README-METAFONT has the rest. |
| `initex` | TeX with no format preloaded, for building .fmt files<br>**How:** TeX with no format preloaded -- this is what builds the .fmt files. `initex "plain \dump"'. The three formats already ship in SYS/TEX/FORMATS, built this way, so you only need this to make your own. |
| `latex` | LaTeX -- Lamport's document preparation system on top of TeX<br>**How:** `latex yourfile.tex' works: the wrapper hands `virtex &lplain' to $SHELL, which SYS/login makes ksh.  With SHELL set to bash it fails (E$PNNF); `virtex '&lplain' yourfile.tex' works either way.  The .dvi and .log land in your data directory. |
| `maketexpk` | generate a .pk font at the size TeX asked for<br>**How:** It carries the RIGHT Metafont line in its own strings and then reaches for `makdir', `del' and `attr' to file the result -- three Microware utilities that are not here. Run the virmf line yourself: DOC/README-METAFONT has it, and `gftopk' is all maketexpk was going to do afterwards. |
| `pktogf` | packed font back to generic font<br>**How:** Unpacks a .pk. The result is longer than the .gf it came from -- pktogf rewrites the preamble comment -- and the bitmap is unchanged. |
| `pktype` | show what is inside a .pk file<br>**How:** `pktype <font>.<dpi>pk' prints the packed font back, glyphs included. PKFONTS must name the directory. |
| `pltotf` | property list to TeX font metric<br>`Usage: pltotf [-verbose] <property list file> <tfm file>.` |
| `slitex` | SliTeX -- LaTeX for slides<br>**How:** LaTeX for slides; its format is SYS/TEX/FORMATS/splain.fmt, already built. |
| `tangle` | WEB to Pascal -- Knuth's literate-programming tool.  Name a change file too, always: DOC/tex has none.ch, an empty one, beside sample.web -- `tangle sample none'<br>**How:** Needs a change file named, always. `tangle yourfile.web' alone answers `Error: `Can't open file.'' and the file it cannot open is the absent change file, not your source. DOC/tex ships `sample.web' and `none.ch' (empty, changes nothing): copy both to your data directory and run `tangle sample none'. It reads and writes in the data directory, which bash's `cd' does not move. `weave sample none' is the other half. |
| `tex` | TeX itself -- the typesetting program (a driver; virtex does the work)<br>**How:** `tex yourfile.tex' works: the wrapper hands `virtex &plain' to $SHELL, which SYS/login makes ksh, and TEXCMDS must be on PATH (it is).  With SHELL set to bash it fails (E$PNNF); `virtex '&plain' yourfile.tex' works either way.  SYS/TEX/SAMPLES/small.tex is a LaTeX document and story.tex is plain TeX with no \end. |
| `texidx` | sorts the \indexentry lines in a LaTeX .idx file into the index LaTeX reads back. This build stops with `virtual memory exhausted' on any input, and no source is here to rebuild it |
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
| `autolf` | &#9733; a filter that converts line endings between CR, LF and CR LF, expands tabs and handles ^Z: `autolf -c -C -L < in > out' makes DOS text of OS-9 text; `-H' explains. Use standard input: given a file name it cannot rename its result back<br>`autolf: copy stdin to stdout, converting end-of-line character sequences` |
| `casefix` | sentence-cases text: every letter to lower case except the first of each sentence. A filter that reads standard input; a file named as an argument is ignored<br>**How:** It is a filter and reads standard input: `casefix < file' sentence-cases it. |
| `choose` | prints lines picked at random from its input, in the order they stand: `choose -3 file' for three, one by default<br>**How:** `choose -3 file' prints three lines picked at random from the file, in the order they stand in it; with no number it picks one, and with no file it reads standard input. It seeds from the clock in whole seconds, so two runs in the same second pick alike. Asking for more lines than there are is refused. |
| `colrm` | removes columns from each line: `colrm 3 5' deletes the third to fifth characters |
| `cut` | picks fields (-f) or character columns (-c) out of each line, with -d naming the field separator<br>`cut: Illegal option -- ?` |
| `detab` | &#9733; replaces tabs with spaces, at stops every three columns or every n with -tn<br>`Usage: detab [-tn] [infile] or [<infile]` |
| `eo` | &#9733; runs a command once per line of a file, like xargs: `eo <file> <command> @' puts the line where `@' is. -p reads lines from a pipe, -q is quiet, -e stops at the first error. It runs commands through $SHELL, which SYS/login sets<br>**How:** Runs a command on every line of a file, with `@' standing for the line: `eo <file> <command> @'. It shells out, so it needs SHELL set to a shell that takes a command line as one argument -- SYS/login sets `SHELL=/dd/CMDS/ksh' and that is what makes it work. Without it, `can't execute /dd/bash'. `-p' takes the lines from a pipe instead of a file. |
| `expand` | GNU expand: turns tabs into spaces, at stops eight columns apart or as -t says. Shares its name with a utility of your own -- README-NAMES<br>``expand: unrecognized option `-?'`` |
| `field` | &#9733; select whitespace-separated fields from standard input by number, in the order asked for and tab-separated on output: `field 2 4 1' prints the second, fourth and first word of each line. `-i=c' names another input separator.<br>`field v1.0 (c) S.R.Bourne, M.C.Gregorie, 1994` |
| `fillup` | &#9733; fills a file up to a given length with a constant byte: `fillup -n=64 -i=46 f' pads f to 64 bytes with full stops and says how many it appended<br>`Syntax:   fillup [<options>] <file>` |
| `fold` | wraps long lines to a width, 80 columns unless -w says otherwise<br>`fold: illegal option -- ?` |
| `gawk` | &#9733; GNU awk 2.11, the pattern-and-action language: `gawk '{print $1}' file' prints the first field of every line, and named no file it reads standard input<br>**How:** GNU awk 2.11. `gawk "{print \$1}" file' prints the first field of every line; named no file, it reads standard input. Keep the program text short: a command line wider than the window scrolls under bash and is hard to read back. Needs Microware's cio. |
| `gdd` | &#9733; GNU dd, a block copier and converter: `gdd if=<file> bs=<n> skip= seek= count=', and `conv=ucase' converts on the way through. `of=' can only name a file that already exists, so send the output through `>' instead<br>**How:** GNU dd -- a block copier and converter. `gdd if=<file> bs=8 count=1' copies eight bytes, `conv=ucase' converts on the way through. `of=' can only name a file that already exists, so send the output through `>'. Give it arguments. It uses Microware's cio; `dump' is the hex dump here. |
| `gep` | &#9733; a global expression parser -- grep-like; its `-e' takes the path of a file holding the expressions, so it searches for a whole list of patterns at once: `gep -e=patterns <file>'. See DOC/README-GREP<br>**How:** Its expressions come from a file named with `-e', which its own option list marks `(required)': `gep -e=<patterns> <source>'. Handing it a pattern and a file the way you would grep earns `more than one path specified'. |
| `head` | prints the first lines of a file: `head -n 20 file', or the older `head -20 file'<br>**How:** First lines of a file: `head -n 20 file', or the older `head -20 file'. Needs cio. |
| `l` | &#9733; list a text file with word wrap and a carriage return at the end of every line -- `l -<width> <file>', 79 columns by default. Written for Stylo documents and other long-line files. It takes files, not directories<br>`Usage: l [-options] [file] [file] [-options]` |
| `paste` | joins files line by line, side by side and tab-separated: `paste f1 f2'; -d picks another separator and -s lays one file's lines along a single line<br>**How:** Joins lines side by side, tab-separated by default: `paste f1 f2'. `-d:' picks another separator; `-s' puts one file's lines on a single line. |
| `pep` | a file detergent: strips control characters and non-ASCII (-b), converts between the DEC, IBM-PC, Macintosh and WordStar character sets, expands tabs and sets the line terminator (-u)<br>`pep  ver. 2.1; Copyright (c) 1989 Gisle Hannemyr` |
| `psc` | &#9733; turns an ASCII table into commands for `sc', the spreadsheet: one `let' per cell and a `format' line per column. -d sets the field delimiter, -r assembles rows first, -s names the top-left cell<br>**How:** Feeds `sc', the spreadsheet: `psc -d' ' < table' turns rows of numbers into `let A0 = 1' commands sc can read. -r assembles rows first, -s names the top-left cell, -d sets the delimiter. |
| `rev` | reverses the characters of each line<br>`rev: illegal option -- ?` |
| `rot` | turn a text file on its side, a quarter-turn clockwise: the last line becomes the first column, read downwards, and the first line the last<br>`syntax: rot {opt} [<file>]` |
| `subber` | &#9733; substitutes words in a stream from a word list of `,old,new' lines, the first character being the delimiter. Give it memory up front: `subber #1000k words file' at an OS-9 shell<br>**How:** Substitutes words in a stream from a word list of `,old,new' pairs (the line's first character is the delimiter), reading a file as the second argument or standard input. It grows its data area as it reads, with F$Mem, so give it room up front: at an OS-9 (Microware) shell, `subber #1000k words file' -- `#1000k' is the shell's directive, not subber's, so only Microware's shell acts on it: bash hands it straight to subber, which answers `cannot open #1000k', and without it subber's own growth is refused -- `No more memory: 256-byte request refused'. Run it at your OS-9 shell or through it. Both halves measured 2026-09-19. Tested: `,fox,cat' turns `a fox' into `a cat'. |
| `tabs` | re-space a file, standard input to standard output: `-i8' says the input's tab stops are every 8 columns, `-o0' asks for spaces on output and `-o4' for tabs every 4.<br>`Unknown switch: ?` |
| `tac` | GNU tac: prints a file backwards, last line first<br>**How:** Prints a file backwards, last line first -- cat's mirror image. Needs cio. |
| `unexpand` | GNU unexpand: turns leading spaces back into tabs, or all of them with -a<br>``unexpand: unrecognized option `-?'`` |
| `unp` | &#9733; strips unprintable characters from a stream and reports each one removed, by code and line number<br>`Usage:  unp [-?] [file]` |
| `upperdir` | normalises the names in a directory: files to lower case, directories to upper, printing each as it renames it<br>`Usage: UpperDir [directory name]` |
| `valspeak` | Valley-speak text filter: standard input in, the rewritten text out. `I think this operating system is really good' comes back as `I think this operatin' system is like wow! really bitchin''. |

</details>

## Files & directories

*Listing, copying, finding, renaming, and knowing what you have.*

<details><summary>38 programs</summary>

**Attributes & ownership**

| | |
|---|---|
| `chgrp` | &#9733; sets the group half of a file's owner, by number or by name<br>`chgrp: Usage:  chgrp [-z] {numerical-gid \| username} [file [... file]]` |
| `chown` | &#9733; sets the user half of a file's owner, group.user, by number or by a name from SYS/password. Shares its name with a utility of your own -- README-NAMES<br>`chown: Usage:  chown [-z] {numerical-uid \| username} [file [... file]]` |
| `fstat` | display a file's RBF file descriptor -- owner, attributes, dates and length. `-s' adds the segment list, and `ssl' shows the same list from the same sector<br>`Syntax: FStat [<opts>] <file1> [<opts>]` |
| `owner` | &#9733; change a file's owner -- `owner <user> <file> ...', super user only; fstat and ls -l show the result<br>`owner: change ownership of files` |

**Browse & inspect**

| | |
|---|---|
| `browse` | a directory browser: an `ls -l' listing with a cursor. i and , move, SPACE enters a directory or pages a file, `x' dumps in hex, `?' is help, `qq' leaves. Wants TERM, and a shell for the keys that run programs<br>`Browse through a directory, written by Peter da Silva` |
| `cat` | &#9733; concatenates files to standard output: -n numbers the lines, -v shows control characters, -s squeezes runs of blank lines<br>`Syntax: cat [<opts>] {[-] <path> [<opts>]}` |
| `utree` | full-screen file manager: directory tree above, files below, one-letter commands to copy, move, rename, remove, edit, page, dump, print or grep, singly or on a tagged set. `!' runs a shell command. Setup, keys and help in SYS/UTREE<br>**How:** Full-screen, two panes: the directory tree above, the current directory's files below.  `>' or RETURN crosses into the file pane and RETURN or `q' comes back, while `<' goes up to the parent directory; the menu line names the commands for whichever pane you are in and a capital letter means the whole tagged set.  `H' is the help pages, `=' the variables, `!' a shell command line with a history, `Q' then `y' quits.  $HOME/.utree overrides the startup file in SYS/UTREE, so the settings and the menu commands can be yours without touching the disk.  It holds the whole tree in memory, so on a disk this size open it on a subdirectory -- `utree DOC' reads 303 directories and 1553 files -- or give `-q' at the root, which builds two levels, and `-l <n>' for any other depth.  An os9exec older than its 2026-09-19 memory-block fix stops partway with `ualloc: memory full' on a tree that large, counting allocations rather than bytes; that is the emulator's own accounting and not an OS-9 limit, and on a build carrying the fix the whole of /dd -- 1131 directories, 12377 files -- reads in about a minute and a half. |

**Copy, move, delete**

| | |
|---|---|
| `cp` | &#9733; copy files -- `cp <from> <to>' copies the bytes across<br>`Usage: cp file1 file2` |
| `dback` | directory backup: walks a directory and lists an OS-9 `copy' for every file that is new or has changed; -e runs them, with your own OS-9's `copy' loaded<br>`Usage: Dback [-options] <fromdir> <todir> [-options]` |
| `delbak` | &#9733; deletes the backup files (*_bak) in a directory tree<br>`Usage: delbak [-options] [directory] [-options]` |
| `move` | &#9733; moves files between directories by relinking, not copying -- quick, but do not interrupt it. `move <from> <to>' wants a destination name; -w=<dir> is the wildcard form that takes a directory<br>`Syntax:   move [<options>] <from> [<to>] [<options>]` |
| `mv` | &#9733; GNU mv (fileutils 3.13) -- rename a file or move it into a directory; `-i' asks before overwriting, `-b' keeps a backup, `-v' names what it moved. Shares its name with a utility of your own -- README-NAMES<br>``mv: unrecognized option `--'`` |
| `rm` | &#9733; GNU rm: removes files, whole directories with -r, asking first with -i, naming each with -v<br>``rm: unrecognized option `-?'`` |
| `undel` | &#9733; brings back a deleted file: it asks for the directory, offers each deleted name RBF still holds (the first letter overwritten), and asks twice before writing. Shares its name with a utility of your own -- README-NAMES<br>`usage: undel  [ -opt ] [ full directory name ] [ -opt ]` |

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
| `ff` | &#9733; find files by name under the current directory -- `ff <name>'.  It runs `dir -ausr ! grep <name>' through a module named shell; DOC/README-SHELLS |
| `find` | &#9733; find 1.1.5 -- search a directory tree, with its own syntax: `-n=<name>' matches and `-o' prints what it found. Its usage (-?) is its manual; the one in DOC/find describes a different find.<br>`Syntax: find {<opts>} [<path>]` |
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
| `PrintLabels` | Home Librarian: prints labels from a catalogue through a template, a text file copied once per card with %title, %author, %year and the other fields filled in. Options take a separate argument: `-infile cat.libr -templatefile tpl.txt', never `-infile=...'; the same holds for Ascii2Libr, Libr2Ascii, PrintCards and EditLibr<br>**How:** Its options take a separate argument -- `-infile cat.libr -templatefile tpl.txt', never `-infile=...', which answers `Bad option:' and prints the syntax. The same is true of Ascii2Libr, Libr2Ascii, PrintCards and EditLibr. The template is a text file copied out once per card with %title, %author, %year and the other field names replaced. |

**List & navigate**

| | |
|---|---|
| `dir` | &#9733; directory listing -- `dir [<opts>] <directory>'; `-e' adds owner, dates, attributes and size. Shares its name with a utility of your own -- README-NAMES<br>`Dir Version 1.08  (C) 1988 by Lim. (Modified by L.Z)` |
| `dm` | Disk Master 1.4, a two-pane directory browser from the MM/1; `h' shows its help, and the arrow keys or Ctrl-N and Ctrl-P move the bar.  Its commands run through system(), so SHELL must name sh (CMDS/sh)<br>**How:** Disk Master 1.4, a full-screen disk browser. It runs the commands on its bottom line through system(), so SHELL must name a shell that can carry them out; with SHELL=/dd/CMDS/sh it runs completely, listing and file-information panel and all. |
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
| `names` | &#9733; an address book in German, full screen: name, street, postcode, town, phone and two notes per record, in a file under SYS it creates on first run. Wants a terminal; its screen codes are a Datamedia 1520's whatever TERM says |
| `sdb` | SDB 2.0, a small relational database: `create' makes a relation, `insert' prompts for records, `print <fields> from <relation> ;' shows a table; also delete, update, sort, import, export and macros. `help' lists them; manual in DOC/sdb<br>**How:** Run it in a directory you can write to; it keeps one file per relation there. `create people ( name char 12 town char 12 ) 20' makes one, `insert people' prompts field by field and a blank line ends the entry, and `print * from people ;' reads it back as a table -- the semicolon is part of the syntax. `help' lists the commands, `exit' leaves. Typing something it cannot parse gives `syntax error' and, if you keep going, a stack overflow. |

**Split & join**

| | |
|---|---|
| `divide` | &#9733; splits a file into pieces of so many lines: `divide -l=<lines> <infile> [<outfile>]' writes outfile.1, outfile.2 and so on<br>`DIVIDE Version 1.1` |
| `fc` | &#9733; split a big file in two, to carry it on 360k disks: the first 350,000 bytes go in one file and the rest in <file>_1<br>`Syntax:   fc [<file>]` |

</details>

## Developer tools

*Version control, tags, cross-reference, formatters, a debugger and benchmarks.*

<details><summary>39 programs</summary>

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
| `dhryshamu` | &#9733; Dhrystone 2.0 built with GCC 1 at -O2 with inlining, strength reduction and no frame pointer; see dhry |
| `dhryshamu2` | &#9733; Dhrystone 2.0, a second shamu build; see dhry |
| `disktest` | measures disk performance: times a raw read, a write of a temporary file and a run of seeks, and prints the rates. It asks your OS-9's `free' for the sector count through a pipe, so free must be resident [no military use -- EFFO-INFO]<br>`Syntax   : disktest [<opt>]` |
| `savage` | &#9733; Savage's benchmark: a chain of functions that should cancel to an exact number, a thousand times; how far the printed value drifts measures the arithmetic's rounding |
| `sieve` | &#9733; the sieve of Eratosthenes as a benchmark: prints `start', runs a hundred passes, prints ` 100 sieves done'. Run it under your OS-9's `time' for a figure. `savage' and the Dhrystone builds in DHRY are the other benchmarks |
| `suse` | a CPU benchmark in 190 bytes of assembler: the Sieve of Eratosthenes, a thousand times over, and then it exits.  It prints nothing and ignores its arguments -- time it |
| `whetstone` | the Whetstone benchmark: floating-point work in a fixed mix, timed, and the rating printed in Whetstone instructions per second.  The Dhrystone builds in CMDS/DHRY measure integer work; this is the floating-point one |

**Debugging**

| | |
|---|---|
| `trap` | &#9733; an example trap handler -- it installs a trap from system state, so from an ordinary program it stops. Run it by path; trap is also a shell builtin.<br>**How:** The system-state trap-handler example: it installs a trap from system state. Ask for it by PATH -- `/dd/CMDS/trap' -- because `trap' is also a bash builtin, and the builtin answers first, silently. |

**Libraries**

| | |
|---|---|
| `libsplit` | splits a new-type ROF linker library into its object files; the libraries on this disk are the older type, for unpacklib<br>`Syntax   : [<opts>] {<library>} [<opts>]` |
| `mtst` | &#9733; exercises the C maths library: ceil, floor and round on a run of numbers, integer and floating side by side -- one of the small programs a port was checked with |

**Source checking**

| | |
|---|---|
| `bcheck` | &#9733; count brackets in a source file and report a mismatch<br>`Syntax: bcheck [<opt>] [<filename>]` |
| `ccheck` | &#9733; C program checker -- matching brackets, quotes, comment brackets, and indentation that disagrees with them<br>**How:** Checks C source for mismatched brackets, quotes and comment markers, and for indentation that disagrees with the nesting. Needs cio. |
| `cdecl` | explains a C declaration in English and writes one from English: `explain int *p' answers `declare p as pointer to int', and `declare x as pointer to function returning int' answers `int (*x)()'<br>`[] means optional; {} means 1 or more; <> means defined elsewhere` |

**Source formatting**

| | |
|---|---|
| `cb` | &#9733; the C beautifier: indents C source into a readable layout, standard input to standard output<br>`Usage:  cb <input.fil >output.fil` |
| `cpr` | print or pretty-list C source for paper: a title, a contents page, then the source with page and line numbers.<br>`Usage: cpr [-cCnNsS] [-T title] [-t tabwidth] [-p[num]] [-r[num]] [-l pagelength] [[-f] file] ...` |
| `ifdef` | reads C source and resolves its #ifdefs, writing what is left: -D<name> defines a name and -U<name> undefines it, so `ifdef -DOSK f.c' keeps the OS-9 arm and drops the others. -t prints the table it built<br>`Syntax: ifdef [<opts>] [<file>] [<opts>]` |
| `indent` | reformat a C source program for readability<br>`Syntax: indent [<opts>] [<inpath> [<outpath>]] [<opts>]` |
| `patch` | applies a diff to a file, the way `diff' made it: `patch <file> <diff>', or the diff on standard input.  It keeps the original beside the result as <file>.orig. |
| `scpp` | &#9733; the selective C preprocessor: expands only the macros you name and leaves the rest of the source as it was. `scpp -MWIDTH prog.c' interprets WIDTH alone; -D defines one<br>**How:** `scpp -MNAME file' copies the C source to standard output expanding only name -- its #define disappears and each use becomes the value -- and leaves every other macro, #include and #ifdef untouched. Name several with -M"A B"; -DNAME=value defines one; -C keeps comments; -I adds an include directory. |
| `unifdef` | resolve #ifdef sections in C source for one symbol: -d<sym> keeps its branch, -u<sym> the other.<br>**How:** Its option is `-d<sym>' -- lower case, no equals -- and `-u<sym>' for the other side. `-DOSK' is refused with its own help, which reads like the program working and is not. |

**Source navigation**

| | |
|---|---|
| `ctags` | generate a vi tags file from C source (BSD)<br>`ctags: illegal option -- ?` |
| `cxref` | &#9733; C cross-reference lister -- numbered listing + symbol table<br>`Syntax:		cxref [-opts] [path]` |
| `etags` | makes a tag table -- the index an editor uses to jump to where a name is defined. It reads C, LaTeX, Lisp, Scheme and Fortran, and writes `tags', the form vi wants, or with -e `TAGS' for emacs<br>`Syntax: etags { [<opts>] <path> }` |
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

<details><summary>49 programs</summary>

**Alternates**

| | |
|---|---|
| `m4_0.5` | &#9733; the same GNU m4 0.5 as CMDS/m4, kept under its version number<br>`Syntax   : m4 [<opts>] [<files>]` |

**Assemblers & linkers**

| | |
|---|---|
| `as0` | 6800/6802 cross-assembler, one of the xasm set: `as0 file - l s' assembles with a listing (l) and a symbol table (s), options after a lone `-'. None of the xasm tools assembles 68000 code; samples are in DOC/xasm<br>**How:** Assemble the sample that ships with it: `as0 /dd/DOC/xasm/sample.a0 - l s' -- the options come after a lone `-', `l' for the listing and `s' for the symbol table. There is a sample for each of the six (sample.a0, .a1, .a4, .a5, .a09, .a11) and each is written for its own processor: as09 rejects the 6800 one, correctly. as11 is the one that takes its options without the `-'. None of these is a 68000 assembler. |
| `as09` | &#9733; 6809 assembler -- the one of the six that targets the 6809 rather than the 6800 family.  DOC/xasm/sample.a09 is written for it |
| `as1` | 6801/6803 cross-assembler (xasm); see as0. Sample in DOC/xasm/sample.a1 |
| `as11` | 68HC11 cross-assembler (xasm). It lists by default and takes no `- l s'; a word after the file name is another source file. Sample in DOC/xasm/sample.a11 |
| `as4` | 6804 cross-assembler (xasm); see as0. Sample in DOC/xasm/sample.a4 |
| `as5` | 6805/68HC05 cross-assembler (xasm); see as0. Sample in DOC/xasm/sample.a5 |
| `assembler` | GSHELL front-end for the assembler -- the same full-screen menu as `gshell', headed `Assembler-SHELL V1.0'.  It does not assemble anything itself; `as0' and its five siblings are the assemblers<br>**How:** Full-screen: it takes over the display. **control-C gets you out**; none of q, Q, control-D or ESC do. |
| `lnk` | the RTF Fortran link driver: `lnk fact' calls l68 on fact.r with Microware's sys.l from LIB on /h0 |
| `lnk.org` | the original lnk, the RTF Fortran link driver: runs `l68' through `shell'. `load os9lib' first, and it needs the start-up code `fstart.r', assembled from SRC/rtf/rtfstart.a with your own r68. DOC/README-FORTRAN has the chain<br>**How:** `load /dd/CMDS/os9lib' first. Without it this calls F$Link for os9lib, gets E_MNF and exits printing nothing. DOC/README-RUNNING names the four programs that do this. |

**C compilers**

| | |
|---|---|
| `cpp` | Decus CPP, a public-domain C preprocessor. It writes the `#P' and `#5' line markers Microware's compiler pass expects; `-A' gives ordinary `#line' output. Shares its name with your OS-9's preprocessor -- README-NAMES<br>**How:** Give it a C source file: `cpp t.c'. By default it writes Microware's `#P'/`#5' line markers, because it was built to replace their preprocessor pass; `-A' gives ordinary `#line' output instead. The file must be CR-terminated like everything else on this disk -- an LF-terminated one arrives as a single enormous line. |

**C toolchain**

| | |
|---|---|
| `cc1plus` | a GCC C++ compiler pass (1.40.3) in the GCC2 directory; the driver runs it |
| `cc2` | the GCC 2.x C compiler pass, in the GCC2 directory; the driver runs it, and -version reports it |
| `cc2plus` | a second GCC C++ compiler pass (2.5.8) in the GCC2 directory |
| `cccp2` | &#9733; the GCC 2.x preprocessor, in the GCC2 directory beside its driver<br>`GNU C Compatible Compiler Preprocessor (Version 2.5.6)` |
| `collect` | collect2: builds the table of global constructors and destructors a C++ program needs before linking<br>`Syntax   : collect [<opts>] {<file>} [<opts>]` |
| `compiler` | a full-screen menu in front of the C compiler: a letter compiles that file, the lower-case letter asks for arguments first, `.' changes directory, `!' leaves the menu; control-C quits the program<br>**How:** Full-screen: it takes over the display. **control-C gets you out**; none of q, Q, control-D or ESC do. |
| `gcc` | &#9733; the GCC driver -- GCC139's and GCC2's share this name. They are not the same version, and neither is 2.x: GCC139/gcc answers `gcc version 1.39' and GCC2/gcc answers `gcc version 1.42', read out of `gcc -v'<br>`GNU C Compiler (Version 1.42)` |
| `gcc137` | &#9733; the GCC 1.37.1 driver: `gcc version 1.37.1' |
| `gcc137_cc1` | &#9733; its C compiler pass: `GNU C version 1.37.1 (OS-9/68000)' |
| `gcc137_cccp` | &#9733; GNU C 1.37.1's preprocessor |
| `gcc2` | &#9733; the GCC 2.x driver, and the only one that is: `gcc version 2.5.6'<br>`GNU C Compiler (Version 2.5.6)` |
| `gcc272` | the GNU C and C++ 2.7.2 driver: `gcc2 version 2.7.2' |
| `gcc272_cc2` | the C compiler pass: `GNU C version 2.7.2' |
| `gcc272_cc2plus` | the C++ compiler pass: `GNU C++ version 2.7.2' |
| `gcc272_cccp2` | the preprocessor, for C and C++ |
| `gcc272_collect` | &#9733; builds the table of global constructors and destructors a C++ program needs; gcc272 runs it for every link |
| `gcc_cc1` | GCC 1.39 C compiler pass |
| `gcc_cc1plus` | GCC139's C++ compiler pass: `GNU C++ version 1.37.1' |
| `gcc_cc2` | GCC 2.x compiler pass, under the name gcc2 forks |
| `gcc_cccp` | GCC 1.39 preprocessor<br>`GNU C Compatible Compiler Preprocessor (Version 1.39)` |
| `gcc_cccp2` | &#9733; GCC 2.x preprocessor, under the name the gcc2 driver forks it by<br>`GNU C Compatible Compiler Preprocessor (Version 2.5.6)` |
| `gcc_collect` | GCC 1.39 collect2<br>`Syntax   : collect [<opts>] {<file>} [<opts>]` |
| `gpp` | the C++ driver -- and it is a GCC 1.x one.  GCC2/gpp says `gpp version 1.40.3 (based on GCC 1.40)' and GCC139/gpp says 1.37.1<br>`GNU C++ Compiler (Version 1.40.3 (based on GCC 1.40))` |
| `gpp_cc1plus` | GCC2's C++ pass, 1.40.3, under the name the gpp driver forks it by |
| `gpp_cccp` | &#9733; GCC 2.x preprocessor, under the name gpp forks<br>`GNU C Compatible Compiler Preprocessor (Version 2.5.6)` |
| `gpp_collect` | GCC 2.x collect2, under the name gpp forks<br>`Syntax   : collect [<opts>] {<file>} [<opts>]` |

**Make & generators**

| | |
|---|---|
| `bison` | GNU bison 1.19, the parser generator: reads a grammar and writes the parser in C, with -v leaving a report of the states and conflicts. Its skeletons are in LIB<br>`Bison 1.19 (OSK-Version 1.2) (c) 1993 Dipl-Kfm Norbert Kuehne` |
| `dmake` | &#9733; dmake 3.70 - parallel make with its own makefile dialect<br>`Usage:` |
| `flex` | flex, the fast lexical analyser generator: turns a rules file into a C scanner, lex.yy.c. DOC/flex/README-FLEX has what to know first<br>`Syntax   : flex [-bcdfinpstvFILT8 -C[efmF] -Sskeleton] [filename ...]` |
| `gmake` | GNU make: builds targets from a makefile's rules -- -f names the file, -n prints what it would do, -k keeps going past errors<br>`Usage: gmake [options] [target] ...` |
| `ltb` | lexical table builder: turns a word list into a C hash table. `ltb proffsym.new lextab' writes the lextab.h and lextab.d proff's parser is built from; SRC/proff has both input and result |
| `m4` | m4 macro processor.  It expands macros from a file or a pipe.  Its `syscmd' needs a `shell' module: it forks one by that bare name and is silent without it, so keep your own shell loaded -- DOC/README-SHELLS<br>`Syntax   : m4 [<opts>] [<files>]` |
| `make` | &#9733; maintains targets from a makefile. Command lines must start with a TAB, which typing here expands, so copy DOC/make/demo.mk. A recipe with `>' or `\|' runs under $SHELL (ksh). Shares its name with a utility of your own -- README-NAMES<br>**How:** It works.  Copy `/dd/DOC/make/demo.mk' rather than writing a makefile at the shell -- a command line must begin with a TAB, and a tab does not survive being typed at this terminal.  A recipe with `>' or `\|' goes to $SHELL, which SYS/login makes ksh, and runs; with SHELL set to bash it fails.  The default rules are in default.mk beside it, and make looks for that along your PATH. |
| `makeinfo` | GNU makeinfo -- Texinfo to info<br>``makeinfo: unrecognized option `-?'`` |
| `v7make` | Seventh Edition Unix make, public domain: runs a makefile's commands whose targets are out of date. Commands go to `shell', so load your own OS-9's first. The module calls itself V7make |
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
| `adltouch` | re-dates an ADL save file: `adltouch <save> <n>' writes n over its first four bytes, the stamp that ties a saved game to the world it was saved from<br>**How:** `adltouch tiny 7' writes 7 into the first four bytes of the compiled world; dump the file to see it. It prints nothing. |

**Fortran**

| | |
|---|---|
| `creadoc` | extracts the documentation header (C++ ... C--) of each .f file in the current directory into creadoc.txt.  Needs your OS-9's shell, dir and del, and os9lib loaded. DOC/rtf/biory.doc is its output for biory.f. Source: SRC/rtf/creadoc.f |
| `fact` | prints the factorials 1! to 12! -- the Fortran example for this disk's RTF/68K compiler, source in SRC/rtf/fact.f. `load os9lib' first, as every RTF program needs.  Twelve is as far as a 32-bit integer goes: 13! overflows |
| `for` | the RTF/68K Fortran driver: it forks Microware's shell to run each compiler pass. At bash `for' is also the loop keyword, so use `command for' there. Calling `rtf' directly needs no shell at all; see DOC/README-FORTRAN |
| `rtf` | RTF/68K 2.14, a real-time Fortran-77 compiler. `load os9lib' from CMDS, then `rtf file.f' writes 68k assembly beside the source for your own r68 and l68. `for' is its driver. Sample sources in SRC/rtf; manual DOC/rtf/rtfman.txt |

**Interpreters**

| | |
|---|---|
| `dds` | a BASIC interpreter in 1536 characters of obfuscated C: it prompts `Ok' and takes numbered lines; RUN, LIST, NEW, OLD, SAVE and BYE act at once. Single-letter variables; FOR, GOSUB, GOTO, IF, INPUT, PRINT. Type in capitals<br>**How:** A BASIC interpreter in 1536 characters of obfuscated C -- the 1990 contest's Best Language Tool. It prompts with `Ok'. Type numbered lines to enter a program and bare commands to act: RUN, LIST, new, OLD <file>, SAVE <file>, BYE. Variables are the single letters a to z, and it understands FOR/NEXT, GOSUB/RETURN, GOTO, IF/THEN, input, PRINT and REM. All input must be uppercase. There is no error checking: a mistake ends the program rather than reporting itself. |
| `forth` | &#9733; TILE Forth, a Forth-83 interpreter. A source file named on the command line loads first; `words' lists the vocabulary, bye leaves. lib/tile holds its source library, lib/tile/TST test programs, DOC/forth the manuals<br>**How:** Type `2 3 + . cr' and it answers 5; `: squares 11 1 do i dup * . loop cr ;' then `squares' prints them; `words' lists its vocabulary; `bye' leaves. A source file is a command-line argument -- `forth fibonacci.tst' in lib/tile/TST loads it and gives you the prompt -- because `include' is defined in the library, not the kernel. The library and its twenty-two programs are in lib/tile and lib/tile/TST. |
| `lua` | Lua 3.0, a small scripting language: `lua <file>' runs a script, with none it reads standard input, -v prints the version. Examples in DOC/lua/examples. luac compiles to bytecode, or to an OS-9 module that runc starts<br>**How:** `lua cf.lua' in DOC/lua/examples prints a temperature table; `lua hello.lua' says hello. Eight example scripts are there; -v prints the version. |
| `luac` | &#9733; Lua bytecode compiler: `luac -o out.lc in.lua'; -l lists the instructions as it compiles. -m writes an OS-9 module instead of a bytecode file, and -x -o <name> puts that module in the execution directory for `runc' to start<br>**How:** `luac -l -o hello.lc hello.lua' compiles and lists the bytecode. `luac -x -o name script.lua' makes an OS-9 module in the execution directory for runc. |
| `perl` | Perl 4.036, a text-processing language: `perl script.pl' runs a script and `perl -e' a line of program. Manual in DOC/perl/perl.txt, library in LIB/perl<br>**How:** Perl 4.036. `perl -e 'print 6*7, "\n";'' prints 42; `perl script.pl' runs a file; -v prints the version. system and backticks go through $SHELL, which SYS/login sets to ksh. The library is in LIB/perl and the manual in DOC/perl/perl.txt. |
| `runc` | runs a Lua script that `luac -x' has compiled into an OS-9 module: `load greet', then `runc greet <args>'. The script reads its arguments from argv[1] onwards, with the count in argv.n<br>**How:** Compile with `luac -x -o greet greet.lua', `load greet', then `runc greet World'. The script reads argv[1] onwards; argv.n is the count. |
| `wam.sbprolog` | SB-Prolog 2.2, a full Prolog. Needs SIMPATH naming SBPROLOG/MODLIB; `wam.sbprolog SBPROLOG/MODLIB/$readloop', run from the collection's root, gives the `?-' prompt, and halt. leaves. DOC/sbprolog has the manual and README-SBPROLOG<br>**How:** Needs SIMPATH=/dd/SBPROLOG/MODLIB (login sets it). From /dd: `wam.sbprolog SBPROLOG/MODLIB/$readloop' gives the `?-' prompt; after a solution ; asks for the next and Return accepts it; halt. leaves. |
| `xlisp` | XLISP 2.1, a Lisp interpreter with objects, at a > prompt; (exit) leaves. DOC/xlisp has the manual |

</details>

## Archives & compression

*Pack, unpack and shrink -- lha, zip, tar, arc, zoo, and OS-9 module libraries.*

<details><summary>34 programs</summary>

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
| `compress` | compress and uncompress with Lempel-Ziv-Welch coding: `compress -c < file > file.Z' packs, `-dc' unpacks, and plain `compress file' replaces the file with file.Z. Pipes are safe. Shares its name with a utility of your own -- README-NAMES<br>**How:** `compress -c < file > file.Z' packs and `compress -dc < file.Z > file' unpacks; plain `compress file' replaces the file with file.Z.  Its output is safe through a pipe as well as into a file: the shipped binary is the build whose putchar double-evaluation is fixed (SRC/hc_utils/README.OSK).  `compr' and `compress_4.0' are the other two compresses here. |
| `gzip` | GNU gzip 1.2.2: compresses a file to .gz and back again with -d; -l lists, -t tests, -1 to -9 trade speed for size<br>`gzip 1.2.2 (17 Jun 93)` |
| `jaw` | zcat in 22 lines, a 1990 obfuscated-C contest entry: `jaw < file.Z' writes out what compress packed<br>**How:** `jaw < file.Z' writes out what compress packed into file.Z, as zcat does. It reads a pipe as well as a file. Run as a copy whose name begins with `a' it decodes btoa's text instead -- its authors' shark archiver pipes the one into the other. |

**Create & extract**

| | |
|---|---|
| `ar` | Ar 1.2, an archive manager: gathers files into one .ar archive and compresses them as it goes -- -u adds, -t lists, -x extracts, -p prints a member<br>`Ar V1.2 - archive file manager` |
| `ar2` | &#9733; Ar 2.00, a later edition of `ar' with delete and move as well, and each file's attributes recorded<br>`Ar V2.00 - archive file manager` |
| `arc` | ARC 5.21, the archiver that came before zip: a adds, x extracts, v lists with the compression column, t tests, p prints a member<br>`ARC - archive utility, Version 5.21, created on 04/22/87 at 15:05:21` |
| `bru` | backs up a directory tree to one archive file and restores it, keeping owners, attributes and dates: `bru -c -q -f save.bru mydir'; -t lists, -x restores here (a pattern restores part). Super-user only; -q stops it asking for a disk<br>**How:** `bru -c -q -f save.bru dir' backs up, `bru -t -q -vvv -f save.bru' lists, `bru -x -q -f save.bru' restores into the current directory. Run it as the super-user; -q stops it asking for a disk, and -f must come before the paths. |
| `lha` | LHa 2.08 -- create/extract .lzh archives<br>`LHa Vrs. 2.08 for OSK - revised Dec. 2, 1994  M.Haaland` |
| `lharc` | C-LHarc 1.00, the older sibling of lha: a adds to a .lzh archive, x extracts, l lists, t tests<br>`C-LHarc for OS-9/68k Version 1.00   (C) 1989-1990 Y.Tagawa, Kai Uwe Rommel` |
| `marc` | the arc archive merger -- `marc <target> <source> [names]' copies members from one .arc into another<br>`MARC - archive merger, Version 5.21, created on 04/22/87 at 15:05:10` |
| `shar` | wraps files as a shell archive, the form source travelled over usenet in: `shar <files> > <archive>'. `shar -u' or `unshar' unpacks one<br>`shar: illegal option -- ?` |
| `tar` | a 1989 tar (SRC/eff_tar): c creates, t lists, x extracts; v shows each file, f names the archive. GNU tar 1.10 is REBUILT/gtar. Shares its name with a utility of your own -- README-NAMES<br>`Syntax : tar [ctx][mfv] tarfile [file(s)...]` |
| `unshar` | unpacks a shell archive -- the form programs were posted to Usenet in -- with its own small interpreter, no Unix shell needed.  DOC/unshar/which6.shar is one to try it on<br>`unshar: illegal option -- ?` |
| `unzip` | &#9733; Info-ZIP unzip: extracts a .zip, including ones this disk's `zip' makes; DOC/zip/sample.zip to try. It extracts into the current directory, so chd there first: `-d <dir>' writes nothing<br>**How:** It extracts where it is standing, and `-d <dir>' writes nothing at all while reporting success, so chd to the directory you want the files in first. It reads what this disk's `zip' makes once the temporary has been renamed. |
| `zip` | Info-ZIP zip 1.9: packs files into a .zip. It leaves the archive under a temporary name _Z<number>, so finish with `mv _Z* mine.zip'. Use bare names from inside the directory: a path with a slash cannot be unzipped back<br>**How:** It deflates into a temporary of its own -- _Z<number> -- and then cannot rename that onto the name you gave, so it stops with `Could not create output file'. The temporary is the archive: `mv _Z* mine.zip' and unzip reads it back byte for byte. Stand in the directory and use bare names, both when packing and when unpacking. |
| `zipnote` | Info-ZIP zipnote -- view/edit zip comments<br>`Copyright (C) 1990-1992 Mark Adler, Richard B. Wales, Jean-loup Gailly` |
| `zipsplit` | Info-ZIP zipsplit -- split a zip archive<br>`Copyright (C) 1990-1992 Mark Adler, Richard B. Wales, Jean-loup Gailly` |
| `zoo` | &#9733; zoo 2.01: archives files with -add, -extract, -list, -test, -delete and the rest; `zoo h' prints its help<br>`Zoo archiver, Version 2.01 (1988/08/25 12:43:57)` |

**OS-9 module libraries**

| | |
|---|---|
| `liborder` | &#9733; lists relocatable (.r) objects in the order to merge them into a library, last first, as l68 wants: `liborder a.r b.r c.r'. `-modinfo' prints each object's public names. `liborder.os9' is a different program that sorts by calls<br>`liborder: Unimplemented option '-?'.` |
| `liborder.os9` | orders relocatable objects for a library by what they call: `liborder.os9 stat.r parse.r make.r' prints make.r first, since it calls into the other two.  -modinfo lists an object's public and external names<br>`liborder: Unimplemented option '-?'.` |
| `modbuster` | splits a file holding several OS-9 modules into one file per module, in the current directory or the one -w=<dir> names, each named for the module it holds<br>**How:** Give it a file holding SEVERAL modules and it writes one file per module in the current directory. Use ksh to put yourself somewhere writable first. `/dd/CMDS/GAMES/cyberwar' looks like a candidate but modbuster hangs on it with no output at all; a single ordinary module (`/dd/CMDS/today') shows it working. |
| `unpacklib` | takes an OS-9 library apart into the modules that were merged to make it, writing each as its own file; -verbose names each one and its size as it goes, -list names them and writes nothing<br>`unpacklib: Unimplemented option '-?'.` |

**zip**

| | |
|---|---|
| `funzip` | &#9733; Unzip straight from a pipe -- funzip < file.zip<br>**How:** Unzips from a pipe rather than a file: `funzip < thing.zip > thing'. For a normal archive use unzip; zipinfo lists what is inside one. |
| `zipinfo` | &#9733; Info-ZIP zipinfo -- what is inside a zip archive<br>`ZipInfo:  Zipfile Information Utility v1.0 of 21 August 92` |

**zoo**

| | |
|---|---|
| `booz` | &#9733; extracts or lists a zoo archive: `booz l' lists, `booz x' extracts, `booz t' tests<br>**How:** Lists and extracts zoo archives: `booz l file.zoo' lists with a bare letter, `booz x' extracts. fiz repairs a zoo archive that will not open. |
| `fiz` | &#9733; finds what survives in a damaged zoo archive: it prints the position of each directory entry and stored file it can find, and zoo then lists or extracts starting from one.  It changes nothing itself |

</details>

## Encoding & conversion

*Between text encodings, line endings, Macintosh formats, ciphers and hashes.*

<details><summary>34 programs</summary>

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
| `crypto` | helps you solve cryptogram puzzles: interactively, or as a filter when its output is redirected, it encodes a text with a random or rotated cipher. `crypto -h' lists the options, `-i' the interactive commands<br>**How:** `crypto -h' is the real option list and `-i' the interactive commands; its bare answer is two lines naming those. With its output redirected it is a filter: `crypto -r13 -n < file > out'. A cypher given with -c is joined to it: `-czyx...a', all 26 letters. |
| `des` | &#9733; DES file encryption -- it writes `<file>.n' and removes the original.  It does not restore a file run through it twice with the same key (the result checksums 00000000), so for a round trip use `xcrypt'<br>**How:** It takes files and has no option flags at all -- `des file ...'. `-e' and `-?' are read as filenames and earn `Can't read -e.' |
| `md5` | the MD5 digest of each file named |
| `xcrypt` | scrambles a file against a key typed at its `Key:' prompt: `xcrypt -e <input-file> <output-file>' encrypts and `-d' decrypts with the same key.  Source in SRC/xrand<br>`xcrypt [-e\|-d] <input-file> <output-file>` |

**Macintosh**

| | |
|---|---|
| `binhex` | encodes a MacBinary file as BinHex 4.0, the text form Macintosh software was posted in<br>`File input options:` |
| `hexbin` | decodes a BinHex file back into the Macintosh file it carried<br>**How:** Decodes Macintosh BinHex (.hqx) files, which is how Mac software travelled by mail and BBS. binhex goes the other way; unsit opens StuffIt archives and macunpack opens PackIt ones. All trap-free. DOC/macutils has the package readme. |
| `macbin` | wraps a file in MacBinary, the form a Macintosh file with two forks travels in; -t and -c set its type and creator, and -d unwraps<br>`MacBinary file converter version 1.1` |
| `macsave` | unpack MacBinary files from standard input into `.bin' files in the current directory, making subdirectories for embedded folders. It writes silently, as its manual page says. `macbin' is the translator that makes a MacBinary file. Its manual is DOC/macsave/macsave.1<br>**How:** Its silence is correct and documented: DOC/macsave/macsave.1 says it "reads standard input and silently writes the file(s) it contains". `macbin' makes the MacBinary it wants, and the pair round-trips. |
| `macstream` | combines one or more files into a MacBinary stream on standard output, the form a Mac terminal program expects; -d treats a plain file as data, with a placeholder type and creator<br>`File input options:` |
| `macunpack` | opens PackIt archives from a Macintosh<br>`File output options:` |
| `mcvert` | converts between MacBinary and BinHex either way: -U makes the BinHex for uploading, -D takes it back to MacBinary for downloading<br>`Mcvert V1.05 By Doug Moore` |
| `UnMacpack` | unpacks Macintosh files and archives -- PackIt, Compress It, ShrinkToFit, BinHex 5.0, MacBinary 1.0 and UMCP -- into MacBinary or separate forks.  Named for its module, which is UnMacpack rather than unmacpack<br>`File output options:` |
| `unsit` | opens StuffIt archives from a Macintosh: -l lists, -r and -d take one fork only<br>`unsit: unknown option -?` |

**Text encodings**

| | |
|---|---|
| `atob` | decodes what btoa encoded, back to the bytes<br>`Bad args to atob` |
| `bcd` | prints text as a punched card, the holes marked in each row: `bcd OS-9' |
| `btoa` | encodes a binary file as printable text, five characters for every four bytes with a checksum on the last line -- denser than uuencode; atob decodes it<br>`Bad args to btoa` |
| `compface` | compresses a 48x48 face into the short text for a mail `X-Face:' header. Input is 48 rows of `0x%04X,0x%04X,0x%04X,'; DOC/compface/face.hex is a sample. `uncompface' goes the other way |
| `cuts` | Coco Usenet Transfer Utility: encodes a binary as text that survives mail, including ASCII-EBCDIC gateways. `cuts -e -o f.cut -a file' packs a text file; `cuts -d f.cut' writes it back under its own name<br>**How:** Coco Usenet Transfer Utility: `cuts -e -o f.cut -a file' encodes a text file (-b for a binary, -9 for an OS-9 module) as mail-safe text, and `cuts -d f.cut' writes it back under its original name in the current directory. |
| `mimecode` | encode or decode base64, MIME's transfer encoding. `mimecode -e' turns a file into printable base64 and `-d' turns it back; uuencode and btoa are the older kinds, this is the one mail and the web use<br>`Usage: mimecode <options>` |
| `morse` | writes text as Morse code -- dit and daw, or dots and dashes with -s<br>`morse: illegal option -- ?` |
| `ppt` | punches text onto paper tape: a row of holes for each character, with the sprocket hole down the middle |
| `todos` | &#9733; turns CR line endings into CR LF, in place, through a temporary and your own OS-9's del and rename.  `autolf -c -C -L' does the same as a filter<br>**How:** It writes the DOS version into `todos.$$$.<n>' in the directory you are standing in and asks `rename' to put it over the file you named; the shell reads the `$$' in that name as its process number, so the rename fails. Rename the temporary yourself, or use `autolf -c -C -L < in > out', which renames nothing. |
| `toos9` | &#9733; turns CR LF line endings back into CR, in place, as todos does.  `autolf -C' does the same as a filter<br>**How:** The same the other way round: the OS-9 version is left in `toos9.$$$.<n>' for you to rename, and it appends one 0xFF byte at the end. `autolf -C' does the job as a filter. |
| `translit` | transliterates text between alphabets by a table: KOI8, KOI7, ALT and GOSTCII Russian, Library of Congress and phonetic romanization, LaTeX; `translit -t koi8-lc.rus -i in -o out'<br>**How:** Converts text from one alphabet or coding to another by a table: `translit -t koi8-lc.rus -i in -o out'. Eighteen tables for Russian are in LIB/translit -- KOI8, KOI7, ALT and GOSTCII codings, Library of Congress, GOST and Pokrovsky transliteration, phonetic spelling and LaTeX -- and a table named without -t is taken the same way. Without -i and -o it is a filter. It will not write over an existing -o file. TRANSP names another table directory and TRANSF the default table. The manual is DOC/translit/translit.txt.A and .B. The post's examples are in SRC/translit/ORIG: example.ko8.UU and example.alt.UU are uuencoded, with DOS line ends that `autolf -C' turns into OS-9 ones. |
| `uncompface` | turns an `X-Face:' line back into the 144 hex words `compface' made it from, so the picture can be looked at again |
| `uud` | decodes what uue or uuencode wrote, and when a file came in pieces -- .uaa, .uab ... -- finds them and joins them by itself: `uud file.uaa'.  -t= names the directory to write in<br>`uud: Unknown option <-?>` |
| `uudecode` | &#9733; undoes uuencode: writes the file named on the begin line back into the current directory<br>`ERROR: can't find -?` |
| `uue` | uuencodes a file into file.uue, or with -l=<lines> into pieces no longer than that, file.uaa, file.uab ..., for mail that limits a message's size: `uue -l=500 archive'. DOC/uutools/uu.doc is the manual<br>`Syntax: uue <[opts]> <file>` |
| `uuencode` | &#9733; wraps a file as printable text for mail: `uuencode file name > file.uu' records it as `name'; with the file alone it records the pathlist as given.  `uudecode' undoes it<br>**How:** The file and the name to record it by: `uuencode /dd/SYS/motd motd > out.uu'. With the file alone it records the pathlist you gave. `uudecode' is what undoes it. |
| `uuexpand` | expands a file into a run of `0' and `1' characters, one per bit, so it survives a copy between machines with different byte or character sizes; `uuexpand -u' (or `uuunexpand') reverses it. Unrelated to uuencode<br>**How:** Expands a file into a string of 0s and 1s, one character per bit; despite the name it is unrelated to uuencode or uudecode. `uuexpand -u' (or `uuunexpand') reverses it. The -8/-16/-7 options choose the assumed character width, for portability across machines. |

</details>

## Communications

*Kermit in several builds, terminal sessions, and networking.*

<details><summary>123 programs</summary>

**File transfer**

| | |
|---|---|
| `fileserv` | &#9733; the UUCP mail file server: reads a message on standard input and obeys `reply <address>', `help', `get <file>', `dir' and `quit' in its body, mailing answers back through rmail. Serves SPOOL/files; logs to LOG/FileServ |
| `fixtext` | &#9733; repair the line endings of a received text batch<br>`fixtext: A text file filter.  Removes escape sequences, expand tabs and change` |

**Kermit**

| | |
|---|---|
| `ckermit` | &#9733; C-Kermit 5A(190) BETA.14, 24 Jul 94 -- the cio build.<br>`Usage: ckermit [cmdfile] [-x arg [-x arg]...[-yyy]..] [ = text ] ]` |
| `kermit` | OS-9 Kermit 1.5: serial file transfer and terminal emulation by command letter -- connect, send, receive, host-server, get, quit. DOC/README-KERMIT compares the Kermits here. Shares its name with a utility of your own -- README-NAMES<br>`OS-9 Kermit Version 1 Release 5` |
| `kermit2` | Kermit Program Version 1 Release 6 -- the same command letters as `kermit', 5K smaller.  DOC/README-KERMIT compares all six<br>`Kermit Program   Version 1    Release 6` |
| `kermit3` | Kermit68K version 1.0.00, 01 July 1987 -- a different program from the other small ones: it puts up its own `Kermit68K>' prompt and reads a Kermit.ini, rather than taking command letters |
| `xkermit` | &#9733; the same version and banner as `kermit' -- OS-9 Kermit 1.5 -- in half the space, because it links cio rather than carrying stdio.  DOC/README-KERMIT<br>`OS-9 Kermit Version 1 Release 5` |

**Mail**

| | |
|---|---|
| `answer` | &#9733; takes telephone messages as mail: it asks `Message to:', checks the name against the alias table, takes the message and mails it. -p gives a `While You Were Out' slip |
| `arepdaemon` | &#9733; the daemon that sends autoreply's replies: once an hour it reads the table in USR/LIB/ELM/autoreply.data, answers each new letter in those mailboxes, and logs what it did to autoreply.log |
| `atp` | &#9733; ATP 1.40, an off-line reader for QWK mail packets from a bulletin board. It reads `atprc' or `.atprc' from your home directory or the directory $ATP names; a working one is in DOC/ka9q, and DOC/ka9q/atp.doc documents every setting |
| `autoreply` | &#9733; sets up an automatic reply while you are away: `autoreply <file>' names the reply, `autoreply off' stops it, and alone it says which file is in use. It finds you by your user number in the password file |
| `checkalias` | &#9733; shows what mail aliases expand to, using `elm -c'; a name that is no alias comes back as a UUCP address. `load ELM/elm' from CMDS first, or it prints nothing and returns 221<br>`Usage: checkalias alias [alias ...]` |
| `disable` | &#9733; turns the terminal monitor (MTSMon) off on a port, freeing the line for, say, a modem dialling out. `enable' turns it back on<br>`Syntax: disable <port>` |
| `dotilde` | &#9733; the tilde-escape handler mailx and postnews call for each `~' line typed into a letter: `dotilde <command> <t2flag> <uid> <quotechar> <letter> <homedir> <message>' -- ~r appends a file, ~m the message replied to, ~h lists the rest<br>`================= Tilde Help =================` |
| `elm` | &#9733; the Elm mail reader itself -- full-screen, menu-driven<br>**How:** The full-screen mail reader. It opens on the folder that ships for this account, `~/SPOOL/MAIL/tester', showing one message. `readmsg 1' prints a message without opening the reader; `messages' counts the folder. Mail lives at /dd/SPOOL/MAIL/<user>, and SYS/login points MAIL at it. |
| `enable` | &#9733; turns the terminal monitor back on for a port, the counterpart of `disable'; -p holds the prompt back until a signal arrives<br>`Syntax: enable [<opts>] <port> [<opts>]` |
| `fastmail` | &#9733; send a file as mail without opening the reader.  It needs a delivery agent to deliver it<br>`/dd/CMDS/ELM/fastmail: illegal option -- ?` |
| `filter` | sorts incoming mail into folders by rule, as a pipe stage in the mail delivery path. The rules are .elm/filter_rules in your home directory; `filter -r' lists them as it understands them<br>`/dd/CMDS/ELM/filter: illegal option -- ?` |
| `frm` | &#9733; list who your mail is from, one line each, with each letter's subject<br>**How:** Lists who your mail is from, one line each. Reads $MAIL, which SYS/login sets. |
| `lcasep` | &#9733; lower-cases the host name at the start of each line, up to the first tab, for mail routing; the rest passes unchanged. A filter for pathalias output; -f and -o name files<br>`/dd/CMDS/UUCP/lcasep: illegal option -- ?` |
| `listalias` | &#9733; lists the mail aliases you have, once newalias has compiled them: yours, then the system's<br>`/dd/CMDS/ELM/listalias: illegal option -- ?` |
| `lmail` | &#9733; local mail delivery: `lmail <user>' reads a message on standard input and appends it to that user's folder in SPOOL/MAIL, taking its lock in SYS/.LOCKS/MAIL.LOCKS<br>`Syntax: lmail <user name> {<user name>}` |
| `mail` | &#9733; reads and sends mail (UUCP set): `mail <user>' takes a message ended by a line with one dot, filed in MAIL/ under that login; `mail' alone opens what is waiting, `?' lists commands. Needs a scratch device at /r0 -- DOC/README-RUNNING |
| `mailx` | &#9733; reads and sends mail: `mailx' opens what is waiting (-r newest first), `mailx <address>' sends, -a names a file being replied to. It wants a mailbox directory of its own, not elm's mailbox file, and says so when there is none<br>`mailx v2.1 (94Sep30)  --send and receive e-mail` |
| `makedb` | build smail's path-alias dbm: `makedb -o <name> <file>' writes <name>.dir and <name>.pag. USR/LIB/SMAIL/palias is the source it defaults to<br>`/dd/CMDS/UUCP/makedb: illegal option -- ?` |
| `messages` | &#9733; counts and lists what is in a mail folder: `There is 1 message in your mailbox'<br>**How:** Counts what is in your mail folder: "There is 1 message in your mailbox". |
| `newalias` | &#9733; rebuilds the Elm alias database after you edit your aliases; -g does the system file<br>**How:** Rebuilds the Elm alias database from USR/LIB/ELM/aliases.text after you edit it. |
| `newmail` | &#9733; watch for mail arriving and say so.  -d reports the folder it is watching and its size<br>`/dd/CMDS/ELM/newmail: illegal option -- ?` |
| `nptx` | &#9733; smail's full-name permuter: it takes `<login>' TAB `<full name>', one per line, and writes the forms of the name mail may arrive under -- `Doe', `J.Doe', `John.Doe' -- each with the login<br>**How:** smail's full-name permuter, and its input format is the whole trick: one line of `<full name>' TAB `<login>' and it answers with the pair reversed. Any other shape -- an address list, a bare name, the password file -- earns `format error: <the line>', which is how it came to be described as an alias expander. |
| `pathalias` | works out how mail should be routed from a map of which site talks to which, and prints one line per destination: the site, then the bang path to reach it. -l names the site you are computing from<br>`/dd/CMDS/UUCP/pathalias: illegal option -- ?` |
| `philmail` | an off-line mail reader: it opens your mail file, steps through the messages with return and offers a reply; `q' quits<br>`/dd/CMDS/UUCP/philmail is an off-line mail reader for UNIX mail` |
| `printmail` | &#9733; format a message for a printer.  It forks `readmsg' by bare name, so load it first; then it prints the message the same way `readmsg' would<br>**How:** It forks `readmsg' by bare name, and OS-9 resolves a bare-name fork against the execution directory, never against PATH -- so it is silent from everywhere except /dd/CMDS/ELM. `load /dd/CMDS/ELM/readmsg' once and it works from anywhere: a resident module is found by name with no directory search at all. |
| `pwparse` | &#9733; reads a password file on standard input and prints the login name from each line, one to a line -- the form the mail system wants a user list in |
| `readmsg` | &#9733; prints selected messages from a mail folder, by number or by pattern: `readmsg 1' for the first<br>**How:** Prints messages from a mail folder: `readmsg 1' for the first. It reads the welcome message in /dd/SPOOL/MAIL/tester. |
| `rmail` | &#9733; delivers incoming mail into a directory per user -- uuxqt runs it, not a person. MAIL names the directory that holds the users' mailbox directories, and each letter becomes a file of its own there<br>**How:** Local delivery builds <mailbox>/<user> and stops, because the mailbox here is a file: `rmail tester' answers plainly. `rmail "site!user"' for remote delivery does not return. |
| `smail` | &#9733; routes mail: works out the path to an address from the map pathalias built and hands the message to the right mailer. -A prints the mapped address and stops, -v is verbose, -d both without delivering<br>`Usage:   /dd/CMDS/UUCP/smail [<options>] address...` |
| `uupoll` | &#9733; poll a site for waiting work. It works silently: `uupoll <site>' leaves C.<site>APOLL in the site's spool directory, and the grade letter from -g goes into the name (`-gZ' -> ...ZPOLL)<br>**How:** Polls a UUCP site for waiting work, and it does the job in SILENCE -- which is why it reads as broken. `uupoll <site>' leaves /dd/SPOOL/uucp/<site>/C.<site>APOLL; the grade letter from -g goes into the name, so `-gZ' gives ...ZPOLL. Blars uucp; wants the `uucp' user, which SYS/password has. |
| `uux` | &#9733; run a command on another UUCP site<br>**How:** Runs a command on another UUCP site. This is BLARS uucp, which reads USR/LIB/UUCP/Config -- a different configuration from UUCPbb's SYS/UUCP. Both ship. |

**News**

| | |
|---|---|
| `bdecode` | &#9733; decodes a C News batch: it skips forward to the line `Decode the following with bdecode', decodes what follows and checks the CRC at the end. Given anything else it says `Missing header'. Source in SRC/cnews/input |
| `byteflip` | &#9733; reorders the bytes of each word on standard input, so a dbz database moves between architectures: `byteflip 4 0 1 2 3 4 3 2 1 0' reverses four-byte words. Give it the numbers: with none it reads zero bytes for ever<br>**How:** It is in CMDS/NEWS, and it reads standard input rather than a file. Four things say how to swap: the word length, where each byte comes from, the word length again, and where each byte goes -- `byteflip 4 0 1 2 3 4 3 2 1 0 < in > out' turns every four-byte word end for end, so `ABCDEFGH' becomes `DCBAHGFE'. With no arguments the word length is zero and it reads zero bytes for ever. Measured 2026-09-19. |
| `c7decode` | &#9733; the inverse of C News's c7encode: it reads the seven-bit-safe form a news batch is put into to cross a link that eats the eighth bit, and writes the eight-bit original back. Source in SRC/cnews/input |
| `cvt_help` | turns nn's help files from their portable markup into the control codes nn prints them with -- what installing nn's help means.  USR/LIB/NN holds files it has already converted<br>**How:** Converts nn's help files; USR/LIB/NN already holds converted ones. |
| `dbz` | &#9733; builds and maintains C News's history index -- the .dir and .pag pair beside the history file that lets the news system find an article by message-id without reading the whole of it. `dbz database [file]...'<br>**How:** The news history database from C News: `dbz [-a] [-x] [-c] database [file]...'. Part of a news system. |
| `decode` | B News 2.11's decode, carried by MNews: turns the printable text encode made back into the original bytes<br>**How:** Reverses encode. |
| `encode` | B News 2.11's encode: turns a binary file -- a compressed news batch -- into printable text a seven-bit link can carry<br>**How:** B News's encode: a binary on standard input becomes printable text on standard output. decode reverses it. |
| `expire` | &#9733; delete news articles past their expiry date<br>`/dd/CMDS/UUCP/expire: illegal option -- ?` |
| `inews` | stores and forwards news articles.  `inews -h < article' posts one, filling in the headers it lacks; `inews -c=newgroup:<group>' creates a group, -e=<days> expires old articles and -r rebuilds the active file<br>**How:** MNews's article store: run `setup' first, then `inews -c=newgroup:<group> </nil' makes a group and `inews -h < file' posts the article in the file. Articles land in /h0/SPOOL/MNEWS, one file per article. |
| `newsetup` | writes a .newsrc for rn from the groups in the active file, each marked unsubscribed until you choose.  rn runs it for a newcomer, through your own OS-9's `shell'; run directly it needs nothing<br>**How:** Writes a .newsrc for rn from the groups in the active file, each marked unsubscribed; it needs nothing else. rn runs it for you when there is no .newsrc, and that route goes through your own OS-9's `shell'. |
| `newshist` | &#9733; looks message-ids up in the news history and reports what it finds, or that there is no entry for them: `newshist "<id@site>" ...'. -df names a history file other than the system's<br>`/dd/CMDS/NEWS/newshist: unknown option -?` |
| `newslock` | &#9733; the news system's lock: `newslock <tempname> <lockname>' links the temporary name to the lock name and returns 0; while the lock exists it fails, returning 1<br>`Usage: /dd/CMDS/NEWS/newslock tempname lockname` |
| `newsrun` | feeds the batches in SPOOL/CNEWS/in.coming to relaynews one by one, uncompressing and converting line endings, and removes each once filed; refused ones go to in.coming/bad. `-v' reports each. `load trlf' first; it uses your own OS-9's `shell'<br>**How:** Files the batches waiting in SPOOL/CNEWS/in.coming through relaynews and removes each once filed. It runs `compress -d' and `trlf' through your own OS-9's `shell', so `load /dd/CMDS/NEWS/trlf' first; relaynews it runs by its full path. `newsrun -v' names each file and what became of it. |
| `nn` | the nn newsreader, release 6.3.10: a full-screen menu of the unread articles in each group, read by subject, with threads, kill files and online help (`?').  `nn <group>' opens one group; it reads the database nnmaster keeps<br>**How:** The nn newsreader. Needs `setup' run and nn's database built (`nnmaster -I', answering OK, then `nnmaster'); then `nn <group>'. Space reads on, `?' is help, `q' quits. Its first run makes .nn in your home directory with `makdir' through your own OS-9's `shell'; with neither resident it opens but keeps no place. |
| `nnadmin` | looks inside nn's database and log, checks it, and tells a running nnmaster what to do<br>**How:** Looks inside nn's database; it needs nnmaster to have built one. |
| `nnaux` | the helper nn runs to post, follow up, reply, mail or forward: it collects the text and hands a post or follow-up to inews, and mail, a reply or a forward to cmail<br>**How:** nn's helper for posting and replying; nn runs it. |
| `nncheck` | says whether there is news you have not read: `There is 1 unread article in 1 group', or `No News (is good news)'<br>**How:** Says whether you have unread news, once nnmaster has built nn's database. |
| `nnmaster` | builds and keeps nn's database of articles: `nnmaster -I' sets it up, a plain `nnmaster' collects what has arrived since, and -r keeps it running as a daemon<br>**How:** Keeps nn's database: `nnmaster -I' once, then `nnmaster' after new articles arrive. -I asks for OK and then whether to reuse the GROUPS file, so feed it `OK' and `y' (printf 'OK\ry\r' > ok; nnmaster -I < ok). It forks your own OS-9's `shell': without one -I stops after `Initializing master data base...' and never returns. With no GROUPS file yet, -I sorts one with your own `qsort', and without that it repeats `can't execute "qsort"' for ever. |
| `Pnews` | posts an article to C News: it asks for the distribution, newsgroup and subject, or with -h <file> -s sends a file that has its header.  The post waits in SPOOL/CNEWS/in.coming for relaynews<br>**How:** Posts an article to C News: bare it asks for the distribution, newsgroup and subject and opens an editor; `Pnews -h <file> -s' posts a file that already has its header. relaynews then files it. |
| `postnews` | &#9733; post an article to a newsgroup: it asks for the header, reads the body, and hands the article to rnews, which files it in SPOOL/news. It takes the Distribution from SYS/UUCP/distributions<br>**How:** UUCPbb's poster: `postnews -n <group> -s <subject> -f <file>', then answer the prompts; Distribution must be one in SYS/UUCP/distributions. It forks `rnews' by bare name, so `load /dd/CMDS/UUCP/rnews' first or it stops with `cannot spawn process--> rnews ... (error 221)'. |
| `readnews` | &#9733; read Usenet news articles: it opens the reader and asks about each newsgroup in the active file not yet in .newsrc, then answers `**** End of newsgroups' when the news spool is empty<br>`readnews: read Usenet news articles` |
| `relaynews` | C News's relay: files an article or a batch under its newsgroup, numbers it, updates the active file and the history, and refuses a Message-ID it has seen.  `relaynews -r -n < file'; -r sends its log to USR/LIB/CNEWS<br>**How:** C News's article filer: `relaynews -r -n < article' files one article (or a batch) under its newsgroup in SPOOL/CNEWS and updates USR/LIB/CNEWS/active. Pnews leaves posts in SPOOL/CNEWS/in.coming for it. |
| `rn` | rn 4.3, the newsreader: `rn <group>'; y reads, space pages, q leaves. Needs a .newsrc (newsetup writes one) and a RAM disk at /r0 (`mount -r=256k /r0'), or it stops and leaves .newsrc renamed .oldnewsrc. Manual in DOC/rn<br>**How:** Larry Wall's newsreader, on the C News spool. Mount a RAM disk first (`mount -r=256k /r0'), then `rn <group>'; y reads, space pages, q quits. Without /r0 it stops with `Can't open /r0/rnvary.3' and leaves your .newsrc renamed to .oldnewsrc -- rename it back. A .newsrc in your home directory lists the groups; newsetup writes one. |
| `rnews` | &#9733; unpacks a batch of articles received from another site and hands each to inews -- by bare name, so `load' inews first, or it repeats `Can't execute 'inews'' for ever.  A compressed (`cunbatch') batch goes through a module named `uncompress' SPOOL/news; -n names the group to assume and -x turns on debugging<br>**How:** Two programs, one name (DOC/README-NEWS). MNews's (CMDS/MNEWS): run `setup', then `load /dd/CMDS/MNEWS/inews' first -- it forks inews by bare name and without it repeats `Can't execute 'inews'' for ever; a `#! cunbatch' batch needs a module named `uncompress'. UUCPbb's (CMDS/UUCP): `rnews <batch>' files each article under SPOOL/news. |
| `sbatch` | collects the articles waiting for a neighbouring site into batches to send it: `sbatch <system>', -c to compress.  It forks uux by bare name, so `load' UUCP's uux first<br>**How:** Batches the articles waiting for a neighbour: `sbatch <system>'. Sys in USR/LIB/NEWS names the neighbours; this disk's names none. It forks `uux' by bare name, so `load /dd/CMDS/UUCP/uux' first or it stops with `Can't fork 'uux ...' (errno = 221)'. |
| `subscribe` | &#9733; turns a newsgroup back on in the .newsrc in your home directory: `X! 1' becomes `X: 1'. A group not in .newsrc at all is left alone, by this and by unsubscribe<br>**How:** It works, and so does `unsubscribe' -- give it a group that IS in /dd/.newsrc. A group that is not there is silently left alone. |
| `tass` | a threaded newsreader for MNews "pre 2" (January 1993): your groups, then articles by thread; Return reads, q goes back, h helps, `tass -u' only updates indexes. It finds news through SysInfo's MNEWS.LIB and MNEWS.DIR, not CMDS/MNEWS's spool -- nn reads that |
| `trlf` | turns LF into CR, for newsrun: `trlf <file>' converts the file in place, `trlf -s' standard input to standard output.  A file already in OS-9's form is unchanged.  Written for this disk<br>`Syntax:   trlf -s  \|  trlf <file> ...` |
| `unsubscribe` | &#9733; turns a newsgroup off in the .newsrc in your home directory: `!' replaces `:' and the record of what was read stays. For a group already off, its message prints a number where the name belongs<br>`unsubscribe: unsubscribe from Usenet newsgroup(s)` |

**TCP/IP**

| | |
|---|---|
| `bm` | the mailer that goes with net: write a letter and it is queued for net's SMTP to send; run bare it reads your mail.  It reads NETHOME and NETSPOOL as net does.  DOC/bm/bm.doc is its manual<br>`Usage: (read) bm [-u user] [-f file]` |
| `boa` | &#9733; Boa 0.92, a small web server: `boa &' serves c/unid/boa/osk/HTML on port 8080 and runs what is under /cgi-bin/ as CGI; `boa -c <dir>' uses another root with its own CONF. Requests are logged in logs/access_log |
| `chp` | a remote login over OS-9/Net; the same as rex <node> login |
| `finger` | &#9733; shows what the system knows about a user: home directory, shell and .plan. Local accounts only, from the password file; user@host answers `No such user'<br>**How:** `finger tester' reads the password file this disk ships and prints the account's home directory, its shell, and the .project and .plan it would show if they existed -- no network needed for a local name. `finger user@host' is the form that asks another machine. |
| `msntp` | sets the system clock from an SNTP server: `msntp <server>'; with none it waits for broadcasts (DOC/msntp/msntp.1). Needs a network and Microware's `netdb' module, even for a dotted address<br>**How:** Sets the clock from a network time server. |
| `net` | KA9Q net -- TCP/IP over SLIP or AX.25: telnet, ftp, smtp. Set NETHOME (startup.net, hosts.net and the rest) and NETSPOOL (mail and its queues); Chapter 2 of DOC/net says how, and `exit' leaves it<br>**How:** KA9Q net, Phil Karn's TCP/IP over SLIP or AX.25 -- the stack amateur radio ran on. Needs NETHOME, NETSPOOL and TMPDIR set and a real interface; see DOC/net, Chapter 2. |
| `nslookup` | BIND 4.8.3 name lookup: `nslookup <host>' asks for a name's addresses; bare, it gives its own prompt. It reads resolv.conf from the root of /h0 (example in DOC/bind) and needs Microware's ISP networking<br>**How:** Looks a host name up in the domain name system: `nslookup <host>', or bare for its own prompt. It reads the server from resolv.conf at the root of /h0 -- DOC/bind/resolv.conf is an example to copy there -- and needs Microware's ISP networking. Here it reads that file, names the server it found, and stops at the socket. |
| `nsquery` | BIND 4.8.3's small resolver test: `nsquery <host> [server]' prints a host's names and addresses.  Same resolv.conf, same networking as nslookup<br>**How:** `nsquery <host> [server]' prints the host's names and addresses. Same resolv.conf and networking as nslookup; bare, it prints its usage line. |
| `osknet` | OSKNET -- TCP/IP for OS-9, Telnet, FTP, Ping and SMTP<br>**How:** Charles Hedrick's TCP/IP for OS-9 -- Telnet, FTP, Ping and SMTP. It needs a network interface. Its own documentation is nine files in DOC/osknet: start with howto.doc and useguide.doc. |
| `prexd` | the rex daemon: start it with & in the startup file of every node that takes rex requests.  Built as prexd, not rexd, so it cannot be mistaken for OS-9/Net's own<br>`Syntax: rexd` |
| `prexdc` | the server prexd starts for each request |
| `remdate` | sets the date and time from another OS-9/Net node's clock |
| `rex` | runs a command on another OS-9/Net node as you: rex /n0/<node> <command>.  Needs prexd on that node<br>`Syntax: rex </net/remote station> <command>` |
| `ttcp` | measures TCP or UDP throughput: `ttcp -r -s' on one machine, `ttcp -t -s <host>' on the other, and it times a megabyte. Needs Microware's ISP networking and its /socket device. Manual in DOC/ttcp<br>**How:** Measures network throughput: `ttcp -r -s' on one machine, then `ttcp -t -s <address>' on the other, and it times a megabyte going across. Both on one machine works too: `ttcp -r -s & ttcp -t -s 127.0.0.1'. It needs Microware's ISP networking (the /socket device) under it; give the other machine as a dotted address, as there is no host table here. |

**Terminal & session**

| | |
|---|---|
| `aterm` | ATerm 2.6, a terminal emulator for a serial line: `aterm /t1'. Its configuration is in SYS/ATERM; run it from a login session rather than as the machine's first process. Manual in DOC/aterm, source in SRC/aterm<br>`ATerm : A terminal program for OS9/68000` |
| `cls` | clears the screen, reading TERM and the termcap to find out how. `clear' beside it does the same job from a different author; either will do<br>`Syntax: cls` |
| `connect` | &#9733; joins two paths, your terminal and a remote device, passing data both ways. Both default to standard input and output; switches before each path set its echo, CR/LF and XON/XOFF. Control-E quits<br>`Usage: connect [<switches>] [<path1>] [<switches>] [<path2>]` |
| `fkeys` | loads the user-defined keys of a VT220 from a file, so the function keys send what you want. Given no file it reads the definitions from standard input; -? prints its syntax<br>`Syntax: fkeys [<path>]` |
| `infoxpress` | a client for the InfoXpress information service, reached over a serial line |
| `initvdu` | &#9733; sets the login terminal up from its termcap entry. It knows particular VDUs; on one it has no definition for it says so and changes nothing, which is the answer rather than a failure. -d shows what it would send<br>**How:** It sets up specific VDU hardware. On a terminal it is not defined for, it answers "is not defined for this terminal". |
| `input` | the Unaxcess bulletin board's input helper: it copies standard input to standard output a character at a time |
| `resize` | asks the terminal its window size and prints LINES and COLUMNS, which less and others prefer to termcap's 24 by 80. At bash, `resize' sets them -- repeat after resizing; `resize -s' prints setenv lines for your OS-9 shell<br>`usage: resize [-s]` |
| `sbreak` | Send/clear an SS_Break signal on a serial path<br>`Syntax:   sbreak [/device]` |
| `setfont` | &#9733; loads a downloadable font from a font file into a terminal that accepts one -- `setfont <path>'<br>`usage: setfont <path>` |
| `setterm` | &#9733; reports or sets the terminal type: alone it names TERM; give a name to change it. An unknown terminal falls back on SYS/setterm. DOC/setterm has the manual and extra termcap entries<br>**How:** `setterm' alone reports what TERM says; give it a terminal name to change it. Run with no arguments and a terminal it wants to configure it goes full-screen -- **ESC quits** (control-C also works, but ESC is the program's own way). SYS/setterm is the defaults file it falls back on when TERM names something it does not know, and DOC/setterm/termcap.extra has further entries you can add to SYS/termcap. |
| `tput` | prints what a terminal needs for a capability, read from termcap: `tput -Tvt100 clear' emits the clear-screen escape and `tput cols' prints 80.  The capability names are the System V ones -- clear, bold, cup, lines, cols<br>`Usage: tput [ -Ttype ] [ -e ] [ -nlines ] capname [ x y ]` |
| `tsmon2` | watches a terminal device and starts the login program when someone types RETURN on it -- the job your own `tsmon' does, with more control: -i starts login as soon as carrier appears instead of waiting for a key<br>`**** TSMON2: de-luxe version of the timesharing monitor (c) 1989 by L.Zeller` |
| `vttest` | the VT100 compatibility test: a menu of pages for cursor movement, screen features, character sets, double-size lines, the keyboard, status reports, VT52 mode and VT102 editing, each saying what a correct terminal shows.  0 leaves<br>**How:** Full-screen menu of VT100 tests. Type a test's number and RETURN; each page says what a correct terminal should show, and RETURN moves on. 0 leaves, printing `That's all, folks!'. Run it on the terminal you mean to judge: the keyboard and reports tests read what that terminal sends back. |
| `wysetime` | Wyse terminal clock-setter, in BASIC09: `runb wysetime' prints the escape sequence a Wyse terminal reads to set its own display clock |

**Terminal & transfer**

| | |
|---|---|
| `blastem` | XModem and YModem file transfer, written for the MM/1<br>`Syntax: Blastem [<opts>] {<filename> [<opts>]}` |
| `dld` | &#9733; sends a file with XMODEM -- FHL's, 1986.  In its own words it downloads FROM the file, out to the other end: `dld <file>' starts it and control-X aborts; `uld' is the other half, receiving into a file<br>`dld version 1.4   (c) 1986 FHL` |
| `k` | Kermit file transfer, short form: `k <file>...' sends, `k' alone waits to receive, guessing text or binary per file. Needs a serial line with a Kermit at the other end<br>`General Usage:` |
| `rxmod` | receives an OS-9 module over a serial line and enters it in the module directory; `txmod' sends. `load' COMMS/vmod_trap first. Source in SRC/serload<br>**How:** `load /dd/CMDS/COMMS/vmod_trap' first, or it stops with `can't install Vmod Trap handler'.  Loaded, it waits on its serial line for a module to arrive, and times out when none does. |
| `sterm` | a serial terminal emulator: -l'<port>' names the line, or the MODEM variable does; with neither it stops with `No MODEM port defined!'. ESC opens its menu; -e'<n>' sets the B+ protocol's error limit<br>`Sterm Ver. 2.0` |
| `tsu` | &#9733; makes the directories and files tterm expects before it is first used -- USR/TTERM and a dialling list named after you -- and reports each one it finds or creates |
| `tterm` | &#9733; a terminal emulator, VT100-ish: -l=<port> links it to a serial port, MODEM by default. `tsu' sets its directories up first and `xyt' does file transfer from inside it<br>`Tterm Version 2.30` |
| `txmod` | sends OS-9 modules over a serial line to `rxmod', which enters them in the module directory there: -x sends everything in the execution directory, -l names the device [no military use -- EFFO-INFO]<br>`4ETXMod - Err:  -? !` |
| `uld` | &#9733; receives a file by XMODEM into the file named (an upload, in its own terms): `uld <file>' starts it and control-X aborts; `dld' is the other half, sending one out<br>`uld version 1.4   (c) 1986 FHL` |
| `vt100` | a VT-100/VT-52 terminal program for the MM/1 under K-Windows: vt100 /t2.  Alt-/ is its menu (hang up, shell, options); no file transfer of its own -- shell out to kermit.  Untested: there is no MM/1 here |
| `xy` | XMODEM/YMODEM transfer.  `xy -?' prints the shared usage: send by naming files, receive by naming none; -A forces ASCII, -B binary, and -X/-Y/-K/-G/-C pick the protocol.  `z -?' lists the family's options too<br>`General Usage:` |
| `xydown` | XModem/YModem download: it detects XModem, YModem or YModem-Batch from the sender and converts line endings on the way in. Stands alone or runs inside KBCom. Source in SRC/xydown, notes in DOC/xydown<br>`XYDOWN ver. 1.1` |
| `xyt` | &#9733; XModem, YModem and YModem-batch transfer for tterm<br>`xyt - version 1.02` |
| `z` | ZMODEM transfer. `z -?' prints the usage it shares with xy. $MODEM names the port; -p<port> overrides it<br>`General Usage:` |

**UUCP**

| | |
|---|---|
| `uucico` | &#9733; UUCP's transfer program: calls a remote site, or answers one with -r, and moves the queued files<br>`usage: uucico [opts] -r \| sys [sys...]  [opts]` |
| `uuclean` | &#9733; removes stale jobs from the UUCP spool that SYS/UUCP/Parameters names, and rotates the log files; -x shows what it would do and touches nothing<br>`uuclean: removed old UUCP files, rotate UUCP and FileServ log files` |
| `uucp` | &#9733; queue a file copy to or from another site<br>`uucp:  unix to unix copy program` |
| `uulog` | &#9733; reads the UUCP and file-server logs and shows what was transferred: -s<site> narrows it to one remote site, -u<user> to one user, -d<days> to a day already past, and -f follows the log as it grows<br>`uulog: examine uucp or fileserver log files` |
| `uuname` | &#9733; lists the UUCP sites this machine can reach; -l prints this machine's own name instead<br>`uuname --show local machine name or those of UUCP sites we talk to` |
| `uustat` | UUCP job status and control: what is queued, for which system, by whom. `-s' limits to one system, `-u' to one user; `-k' kills a job, `-r' rejuvenates one. With an empty queue it says `uucp is possibly active'<br>`Syntax: uustat [<opts>]` |
| `uuxqt` | &#9733; runs commands a remote UUCP site queued here: name a site, or `ALL' for every system in the Systems file. It looks for a module named `procs' to check for another copy running. -xN debugs, -q is quiet |

**Web server**

| | |
|---|---|
| `authwn` | authentication helper for protected areas |
| `inetd` | &#9733; the internet daemon: listens on a port and hands each connection to `wn'. It needs Microware's ISP `inetdb' data module from your own networking; without it, `tcp protocol unknown'. Alone it prints its usage<br>**How:** The listener that hands incoming connections to wn: `inetd <port> wn'. It needs Microware's ISP `inetdb' module, which names the protocols; without it the answer is `tcp protocol unknown'. |
| `inetdc` | &#9733; the per-connection helper inetd forks; not run directly |
| `wn` | the WN web server 1.14.3, inetd-style: one HTTP request on standard input, one response out, so run bare it waits. Its document root is under /h0, so mount this disk as /h0 too. It serves what index.cache names (see wndex); manual in DOC/wn<br>**How:** A real HTTP server (WN 1.14.3, GPL). It starts and opens its log -- the path /h0/c/unid/wn_1.14.3/osk/logs is compiled into the binary, and that directory is on this disk so it can. To serve, it needs TCP/IP under it (KA9Q or osknet, in CMDS/NETWORK). It is an inetd-style server -- one request in on standard input, one response out -- so you can hand it a request by hand and read the reply. Its manual is 30 HTML files in DOC/wn. |
| `wn.stb` | WN's symbol table (a data module) |
| `wndex` | builds the index.cache WN serves a directory from. It works on the current directory and ignores a directory given as an argument, so change to the directory first (`cd', or `chd' at the OS-9 shell)<br>**How:** Builds the index.cache WN will not serve without. It works on the current directory and ignores a directory given as an argument -- on this disk that means ksh, whose `cd' is a real chdir where bash's is not: `ksh -c "cd <dir>; /dd/CMDS/WN/wndex"'. On its own it says "Can't open ./index -- skipping it", which means you are not where you think you are. The site that ships at /dd/c/unid/wn_1.14.3/osk already has its cache built; that is WN's compiled-in document root. |

</details>

## Graphics & images

*The netpbm toolkit, JPEG, a ray tracer, and things that draw.*

<details><summary>191 programs</summary>

**Drawing & display**

| | |
|---|---|
| `draw` | a character-graphics drawing program: move a cursor over a canvas laying down characters -- hjkl move, p lifts and drops the pen, backslash chooses the character, `?' shows the keys<br>`syntax: draw [<opts>] <file> [<opts>]` |
| `pdraw` | Pdraw 1.4: plots 2D and 3D data as PostScript. It reads an options file (labels, hidden lines, point marks), lists the settings, asks before plotting, and writes `dataplot.ps' beside the data<br>`Pdraw V1.4  9/4/90` |
| `snap` | &#9733; writes what is on the terminal screen to a file -- `polaroid' unless you name another -- so a display can be kept. -s and -e take a range of lines rather than the whole screen<br>`syntax: snap {opt} [<file>] {opt}` |

**Hardware demos**

| | |
|---|---|
| `graph` | the Graph trap library, a type-$0B module, not a program; g, striche, apfel, sine, showpic, graphdemo and graphsave call it. `load' it to install the trap. It runs in supervisor state, so calls from a program run at the shell abort |
| `lissaj` | &#9733; draws Lissajous figures on a Tektronix graphics terminal. It asks four things first -- the x and y angular frequencies, how long to hold the picture, and the phase -- and then plots |
| `lorenz3d` | &#9733; Tektronix demo: the Lorenz attractor in 3D |
| `wgen` | Tektronix waveform generator: asks for a resolution and the intensity of nine harmonics, then emits Tektronix plotting codes.  It needs no trap library<br>**How:** It needs no trap library now (measured 2026-09-23 on os9exec b5da6df; it used to abort with `unintialized User Trap #5, err=#227' until `graph' was loaded). It asks for a resolution and the intensity of nine harmonics and draws the waveform. Give it ten numbers -- at end of input it draws for ever. `showpic' and `graphsave' need the same library and a display, so they abort either way. |

**JPEG**

| | |
|---|---|
| `cjpeg` | JPEG encoder (IJG) for the 68020 and up: makes a JPEG from a PNM. It wants LF between PNM header fields and this netpbm writes CR, so patch them with `pbyte' first (DOC/STATUS has the offsets). cjpeg.070 runs on any 68000 and takes netpbm files as they are<br>**How:** Makes a JPEG from a PNM -- but not straight from a netpbm PNM. cjpeg wants LF between the header fields and this disk's netpbm writes CR, so it says "Bogus data in PPM file". Patch the three separators with `pbyte` first: for `ppmmake red 8 8` they are at offsets 2, 6 and a. DOC/STATUS has the full recipe both ways. |
| `cjpeg.070` | JPEG encoder, cjpeg built for the 68000, 68010 and 68070 (the unsuffixed set is for the 68020 and up).  Under os9exec it stops at `Premature end of input file' on every input<br>`usage: cjpeg.070 [switches] [inputfile]` |
| `djpeg` | JPEG decompressor, jpeg-5a.  Decodes a JPEG to a PNM.  Its output ends each header line with LF where the netpbm here wants CR, so patch the three separators with `pbyte' to pipe it on; DOC/STATUS has the offsets.<br>**How:** Decompresses a JPEG: `djpeg -pnm image.jpg > out.ppm`. The disk has one to try, SRC/jpeglib/JPEG_5A/testimg.jpg. Its output will not pipe into netpbm unpatched -- djpeg writes LF at the end of a PNM header line and netpbm here wants CR. `pbyte out.ppm 2 0d` and the same at the two later separators fixes it; DOC/STATUS has the offsets. |
| `djpeg.070` | JPEG decompressor, djpeg built for the 68000, 68010 and 68070.  It decodes a JPEG, including one cjpeg wrote<br>`usage: djpeg.070 [switches] [inputfile]` |
| `rdjpgcom` | read the comment from a JPEG file<br>`rdjpgcom displays any textual comments in a JPEG file.` |
| `rdjpgcom.070` | read a JPEG's comment -- the 68000/68010/68070 build<br>`rdjpgcom displays any textual comments in a JPEG file.` |
| `wrjpgcom` | write a comment into a JPEG file<br>`wrjpgcom inserts a textual comment in a JPEG file.` |
| `wrjpgcom.070` | write a JPEG's comment -- the 68000/68010/68070 build<br>`wrjpgcom inserts a textual comment in a JPEG file.` |

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
| `pgmedge` | finds the edges in a greymap: it writes a new greymap in which a pixel is as bright as the contrast around it, so shapes come out light against dark |
| `pgmenhance` | sharpens a greymap by edge enhancement, -1 mild to -9 strong<br>`usage:  pgmenhance [-N] [pgmfile]  ( 1 <= N <= 9, default = 9 )` |
| `pgmhist` | prints a histogram of the grey levels in a greymap |
| `pgmkernel` | makes a convolution kernel for pnmconvol, of the size given<br>`usage:  pgmkernel [-weight f] width [height]` |
| `pgmnoise` | makes white noise: every pixel an independent random grey<br>`usage:  pgmnoise width height` |
| `pgmnorm` | normalises the contrast of a greymap, stretching it to the full range<br>`usage:  pgmnorm [-bpercent N \| -bvalue N] [-wpercent N \| -wvalue N] [pgmfile]` |
| `pgmoil` | paints a greymap again as if in oils: each pixel becomes the commonest value around it<br>`usage:  pgmoil [-n <n>] [pgmfile]` |
| `pgmramp` | makes a grey ramp -- left to right, top to bottom, rectangular or elliptical<br>`usage:  pgmramp -lr\|-tb\|-rectangle\|-ellipse <width> <height>` |
| `pgmtexture` | measures the texture of a greymap the way a pattern-recognition paper does: angular second moment, contrast, correlation, entropy and the rest<br>`usage:  pgmtexture [-d <d>] [pgmfile]` |
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
| `pnmpaste` | pastes one image into another at a position, replacing, or-ing, and-ing or xor-ing the pixels<br>`usage:  pnmpaste [-replace\|-or\|-and\|-xor] frompnmfile x y [intopnmfile]` |
| `pnmrotate` | rotates an image by an angle between -90 and 90 degrees, anti-aliased<br>`usage:  pnmrotate [-noantialias] <angle> [pnmfile]` |
| `pnmscale` | scales an image by a factor, to a width or height, or into a box (-xysize)<br>**How:** Scales an image: `pnmscale 0.5 file'. Given only a filename it takes that as the scale factor and then waits on empty input, reporting "bad magic number" -- which means you left out the factor, not that your file is bad. The same trap catches pnmdepth, pnmcut, pnmrotate and others. |
| `pnmshear` | shears an image by an angle, anti-aliased<br>`usage:  pnmshear [-noantialias] <angle> [pnmfile]` |
| `pnmsmooth` | smooths an image by averaging each pixel with its neighbours, through a mean kernel of the size given (-size, 3 by 3 by default) that it hands to pnmconvol; -dump writes the kernel<br>`usage:  pnmsmooth [-size width height] [-dump dumpfile] [pnmfile]` |
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
| `ppmntsc` | dims every other row of an image by a factor from 0 to 1, the look of an interlaced video frame<br>**How:** It takes a DIMFACTOR first -- 0.0 is black, 1.0 the original -- then the file. Without it you get its usage. |
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
| `atktopbm` | reads an Andrew Toolkit raster as a PBM |
| `bioradtopgm` | Bio-Rad confocal microscope image to PGM; -image picks one of a stack<br>`usage:  bioradtopgm [-image#] [Bioradfile]` |
| `bmptoppm` | reads a Windows or OS/2 BMP as a PPM<br>`usage:  bmptoppm [bmpfile]` |
| `brushtopbm` | reads a Xerox doodle brush file as a PBM |
| `cmuwmtopbm` | reads a CMU window manager bitmap as a PBM |
| `fitstopnm` | FITS, the astronomers' image format, to PNM; -image picks a plane, -min and -max set the scaling<br>`usage:  fitstopnm [-image N] [-noraw] [-scanmax] [-printmax] [-min f] [-max f] [FITSfile]` |
| `fstopgm` | Usenix FaceSaver image to PGM |
| `g3topbm` | Group 3 fax file to PBM<br>`usage:  g3topbm [-kludge][-reversebits][-stretch] [g3file]` |
| `gemtopbm` | GEM .img (Atari and PC) to PBM<br>`usage:  gemtopbm [-debug] [gemfile]` |
| `giftopnm` | GIF to PNM; -image picks one of several in the file, -comments prints its comments<br>**How:** Reads a GIF into the PNM formats the other 168 converters work on -- try `giftopnm /dd/DEMO/gulls.gif \| pnmfile'. Important for anyone piping images out of the emulator: os9exec turns CR into CRLF on the way to the host, so a raw image containing byte 13 arrives corrupted. Keep binary inside OS-9 and convert with pnmnoraw before taking a picture anywhere else. DOC/README-NETPBM has the details. |
| `gouldtoppm` | Gould scanner file to PPM |
| `hipstopgm` | reads a HIPS image, the format of a human-vision research library, as a PGM<br>**How:** No HIPS image ships, and one is two commands: `printf "osk\rstrip\r1\rtoday\r2\r8\r8\r0\r0\r.\r" > x.hips' -- origin, name, frames, date, rows, columns, bits a pixel, packing, format, then a line holding one dot -- and `printf "0123456789abcdef" >> x.hips' for the pixels. |
| `hpcdtoppm` | Kodak Photo CD image to PPM, at one of five resolutions<br>`Error in Arguments !` |
| `icontopbm` | Sun icon to PBM |
| `ilbmtoppm` | Amiga IFF ILBM to PPM, HAM and extra-halfbrite pictures included<br>`usage:  ilbmtoppm [-verbose] [-ignore <chunkID>] [-isham\|-isehb] [-adjustcolors] [ilbmfile]` |
| `imgtoppm` | Img-whatnot, a PC paint program's format, to PPM<br>**How:** Reads the Img Software Set (AT&T Image-8) format; gemtopbm reads GEM IMG. Feed it an Image-8 file. |
| `lispmtopgm` | Lisp machine bitmap to PGM<br>**How:** Reads a Lisp Machine bitmap back into a PGM; pgmtolispm's output round-trips at any depth up to 8 bits. |
| `macptopbm` | MacPaint to PBM<br>`usage:  macptopbm [-extraskip N] [macpfile]` |
| `mgrtopbm` | MGR window-manager bitmap to PBM |
| `mtvtoppm` | MTV/PRT ray-tracer image to PPM<br>**How:** No MTV image ships, and one is two commands: `printf "4 2\r" > x.mtv' then `printf "0123456789abcdefghijklmn" >> x.mtv' -- a line of width and height, then three raw bytes a pixel. `mtvtoppm x.mtv > out.ppm' and pnmfile says PPM raw, 4 by 2. |
| `pcxtoppm` | PCX, PC Paintbrush's format, to PPM<br>**How:** Cannot read a pipe -- it seeks backwards in its input and stops with "error seeking past header". Write the PCX to a file and pass the filename. sgitopnm has the same limitation. |
| `pi1toppm` | Atari Degas .pi1 to PPM |
| `pi3topbm` | Atari Degas .pi3 to PBM<br>`usage:  pi3topbm [-debug] [pi3file]` |
| `picttoppm` | Macintosh PICT to PPM<br>`usage:  picttoppm [-verbose] [-fullres] [-noheader] [-quickdraw] [-fontdir file] [pictfile]` |
| `pjtoppm` | HP PaintJet file to PPM |
| `pktopbm` | TeX packed-font (.pk) characters to PBM, one bitmap per character.  Give it -x and -y, the bitmap size: without them it reads each character out of step and reports a bad pk file<br>`pktopbm: This is PKtoPBM, version 2.4` |
| `psidtopgm` | a PostScript image -- the hex data of an `image' operator -- to PGM, given its width, height and bits per sample<br>**How:** Reads the hex digits of PostScript `image' operator data: `psidtopgm <width> <height> <bits/sample>' then the hex on standard input. `echo ffffffff00000000 \| psidtopgm 4 2 8' makes a 4x2 graymap, a white row over a black one. |
| `qrttoppm` | QRT ray-tracer output to PPM |
| `rasttopnm` | Sun raster to PNM |
| `rawtopgm` | raw grey bytes to PGM, given the width and height; -headerskip drops a header<br>`usage:  rawtopgm [-headerskip N] [-rowskip N] [-tb\|-topbottom] [<width> <height>] [rawfile]` |
| `rawtoppm` | raw RGB bytes to PPM, given the width and height and the byte order<br>`usage:  rawtoppm [-headerskip N] [-rowskip N] [-rgb\|-rbg\|-grb\|-gbr\|-brg\|-bgr] [-interpixel\|-interrow] <width> <height> [rawfile]` |
| `rgb3toppm` | three greymaps -- red, green and blue -- combined into one PPM; ppmtorgb3 splits it<br>`usage:  rgb3toppm <red pgmfile> <green pgmfile> <blue pgmfile>` |
| `sgitopnm` | reads an SGI image as a PNM; it seeks, so give it a file, not a pipe<br>**How:** Cannot read a pipe -- same as pcxtoppm. Give it a filename or it reports "premature EOF". |
| `sirtopnm` | Solitaire image recorder file to PNM |
| `sldtoppm` | AutoCAD slide to PPM<br>`usage:  sldtoppm [-verbose] [-info] [-adjust] [-scale <s>]` |
| `spctoppm` | Atari compressed Spectrum picture to PPM |
| `spottopgm` | SPOT satellite image to PGM |
| `sputoppm` | Atari uncompressed Spectrum picture to PPM |
| `tgatoppm` | TrueVision Targa to PPM<br>`usage:  tgatoppm  [-debug] [tgafile]` |
| `xbmtopbm` | X11 or X10 bitmap, as C source, to PBM |
| `ximtoppm` | Xim image to PPM |
| `xpmtoppm` | X pixmap (XPM) to PPM |
| `xvminitoppm` | converts an XV thumbnail (.xvpics) to PPM. The format: `P7 332', a comment, the size, then one byte a pixel -- three bits red, three green, two blue<br>**How:** No XV thumbnail ships, and one is two commands: `printf "P7 332\r#END_OF_COMMENTS\r8 2 255\r" > x.xv' then `printf "0123456789abcdef" >> x.xv' -- one byte a pixel into a fixed palette of three bits of red, three of green and two of blue. |
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
| `pgmtoppm` | colours a greymap: `pgmtoppm colour' runs black to white through the colour, `pgmtoppm c1-c2' from one colour to another<br>`usage:  pgmtoppm <colorspec> [pgmfile]` |
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

**Ray tracing & 3D**

| | |
|---|---|
| `rayshade` | ray tracer 4.0.  It builds each scene through popen(), which forks a module named `shell' to run `cccp', so load your own OS-9's shell and GCC 1.39's gcc_cccp first. DOC/rayshade/README-RAYSHADE has the detail.<br>**How:** Ray tracer 4.0, and it renders. It builds its scene through popen(), which forks your own OS-9's `shell` to run `cccp`: `load /h1/CMDS/shell' and `load /dd/CMDS/GCC139/gcc_cccp' first. |
| `rsconvert` | converts a rayshade 3 scene file to rayshade 4 syntax: `rsconvert old.ray > new.ray', or standard input to standard output |

**Viewers**

| | |
|---|---|
| `mgif` | a GIF inspector and viewer. `mgif -i file.gif' reports a GIF's structure and works on any terminal; displaying one needs an Atari ST, because flicker.c writes to ST graphics memory. Source in SRC/mgif<br>**How:** `mgif -i file.gif' inspects a GIF and prints its structure -- that works on any terminal. Displaying an image needs an Atari ST, because it writes straight to ST graphics memory. Try it on /dd/DEMO/gulls.gif. |

**X11**

| | |
|---|---|
| `basicwin` | the classic X11 demonstration: it opens a window on an X display and draws into it |
| `X11R6shl` | X11R6 shared library loader |
| `xengine` | an X11 demonstration: an engine animated in a window on an X display |

</details>

## Games

*Adventures, board and card games, arcade ports, dungeon crawls and puzzles.*

<details><summary>117 programs</summary>

**Adventure & fiction**

| | |
|---|---|
| `advcom` | the ADVSYS adventure compiler: turns .adv source into the world file advint plays. It opens `objects.adi' from the current directory, so copy osample.adv and objects.adi from GAMES/ADVSYS to a directory of your own and run `advcom osample' there. File names are limited to 20 characters<br>**How:** The ADVSYS compiler. It opens its `@objects.adi' include by bare name in the data directory and keeps a filename in 20 characters, so copy osample.adv and objects.adi from GAMES/ADVSYS to a directory of your own, `load /dd/CMDS/GAMES/advcom', then `sh -c "chd /dd/tmp/adv; advcom osample"'. It names every object it compiles and writes osample.dat. |
| `advent` | Colossal Cave Adventure, the mid-1970s original and the first text adventure; its text is GAMES/adv/glorkz on this disk.  Unrelated to advcom/advint.<br>**How:** Colossal Cave. Needs this disk as /dd -- it opens /dd/GAMES/adv/glorkz by absolute path, so mounted only as /h0 it cannot find its data. |
| `advint` | the ADVSYS adventure interpreter: plays a world advcom compiled, opened by bare name in the data directory -- `advint osample' starts you in the livingroom. GAMES/ADVSYS/README has the details<br>**How:** Plays an ADVSYS world. Build one first (see advcom), then run it where the .dat is: `load /dd/CMDS/GAMES/advint', then `sh -c "chd /dd/tmp/adv; advint osample"' -- you start in the livingroom, `n' goes to the hallway, `e' to a storage room with a key. |
| `infocom` | an interpreter for Infocom's Z-machine: plays the .z3 files in GAMES/INFORM (dejavu, hellow, shell -- Inform demonstrations, not the Infocom games). It writes its status-line cursor codes as literal text; infocom.tcap is the build for a terminal<br>**How:** A Z-machine. Plays the .z3 files in /dd/GAMES/INFORM -- the Inform demos dejavu, hellow and shell. |
| `infocom.tcap` | Infocom interpreter, TERMCAP build, the one to use at a terminal: it keeps a proper status line at the top of the screen, where plain `infocom' prints that line's cursor codes as text<br>**How:** The termcap build of the Z-machine, and the one to use at a terminal: `infocom.tcap /dd/GAMES/INFORM/dejavu.z3' keeps a status line (room and score) across the top. Three Inform story files ship in GAMES/INFORM: dejavu, hellow, shell. |
| `inform` | Inform 1.0, the compiler from Inform source to Z-machine story files for infocom: `inform hellow' turns hellow.inf into hellow.z3. The GAMES/INFORM demos have source and library headers in SRC/inform; manual in DOC/inform<br>`OSK Inform 1.0 (v796/au)` |
| `napoleon` | a text adventure set in an English country house, where the Napoleons have left rather more behind them than furniture. The `(napoleon)' prompt reads whole sentences, not just verb-noun; `save' and `load' keep a game |
| `paranoia` | &#9733; the PARANOIA text adventure.  `Welcome to Paranoia!  As Philo-R-DMD you will die at times during the adventure... you will be given a new clone' -- six clones, one mission, RETURN to go on<br>**How:** The PARANOIA text adventure. RETURN to go on, a letter to choose, `p' for your statistics, six clones. `float' and `savage' are the floating-point benchmarks on this disk. |

**Arcade & action**

| | |
|---|---|
| `bks` | Brickstop: catch the falling bricks on a paddle before they pile up to it -- `,' and `.' move, q leaves the game; high scores in GAMES/BKS<br>**How:** Full-screen. p starts a game: bricks fall at the left, and `,' or `<' and `.' or `>' move the paddle to catch them before the pile reaches it. q leaves the game and shows the high scores (kept in GAMES/BKS/hiscores); m returns to the menu and q there quits. ESC, which the menu calls pause, does nothing here. |
| `bugs` | a Dr. Mario lookalike: two-letter pieces fall into a bottle of bugs, and four alike in a row clear them; h and l move, a and s turn, space drops, p pauses, q quits<br>**How:** Full-screen Dr. Mario lookalike. j and k choose the level, then the speed, each accepted with Return. Pieces of two letters fall into the bottle, where the bugs are letters in reverse video or underlined; four of the same letter in a row, across or down, are cleared. h and l move the falling piece, a and s turn it, space drops it, p pauses and q quits. |
| `lander` | lunar lander -- space starts a game, a digit sets the power, x or k is vertical thrust, z/j and c/l the side retros.  Its score file is GAMES/lander.hs, looked for under /h0, so mount the disk there as well<br>**How:** Full-screen. Space starts a descent, a digit sets the engine power, `x' or `k' fires the main thruster and z/j and c/l the side retros. `q' quits. |
| `letters` | Letter Invaders, a typing game: words fall down the screen and typing one clears it before it lands; `-l5' starts at level 5, `-h' shows the high scores, kept in GAMES/LETTERS<br>**How:** Full-screen typing game. Words fall from the top of the screen, and typing a word's letters clears it; a word that reaches the bottom costs one of your lives. Every 15 words the level rises and the words fall faster. The bottom line shows the score, level, words, lives and words per minute. `letters -l5' starts at level 5, -b rings the bell for a mistake, and `letters -h' shows the top ten scores, kept in GAMES/LETTERS. The words come from GAMES/words. |
| `mw` | &#9733; Mazewar for up to eight players at terminals on one system: `w' walks, `a' `d' turn, `s' shoots, `m' mines, `n' builds a wall, `Q' quits. Score only by killing; `mw -l=5' adds a computer player. Maze in USR/GAMES/LIB/MAZEWAR, found with this disk as /h0<br>**How:** Full-screen maze game for up to eight players on one system. `w' walks, `a'/`d' turn, `s' shoots, `m' mines, `n' walls, `Q' quits; `mw -l=5 >/nil &' first starts a computer player to play against. Needs cio; its maze is USR/GAMES/LIB/MAZEWAR. |
| `mz` | a maze of pellets and monsters: eat the pellets while one to six monsters (one per skill level) chase you. Number pad moves (7 8 9 / 4 6 / 1 2 3); control-C is the only way out<br>**How:** Full-screen. `n' then RETURN skips the instructions; a skill level 1-6 and RETURN starts. Number pad moves: 7 8 9 / 4 6 / 1 2 3. Control-C is the only way out. |
| `pacman` | Pac-Man in an ASCII maze: you are OS9, chased by ghosts CPM, MPM, RAM and ROM. Keypad moves (8 up, 2 down, 4 left, 6 right); q quits and shows scores. Data in GAMES/pacman; wants TERM<br>**How:** Answer the name and instructions prompts, then play with the keypad: 8 up, 2 down, 4 left, 6 right, q quits.  It draws with your terminal's termcap entry; its board, help and score files are in GAMES/pacman. |
| `perp` | gather every diamond on the screen, pushing boulders and opening locks with keys: hjkl move, q restarts the level, S and L save and load, ^C quits; map in GAMES/PERP<br>**How:** Full-screen. Collect every diamond on the level: h j k l move, pushing boulders -- o can be crushed, O cannot -- and walking onto a key opens its lock. q gives up the level and starts it again, S saves the game to $HOME/cod.save and L loads it, ^L redraws, ^C quits. `perp 2' starts at the second level. The map and sprites are in GAMES/PERP. |
| `robots` | &#9733; outrun the robots until they crash into each other: you are `I', robots `#', wrecks `@'. Keypad 1-9 moves, 5 stands still, `t' teleports, `s' makes a last stand; -m gives one robot step per move<br>**How:** Play with `robots -m' -- manual mode, where the robots take one step per move you make. Keys are the numeric keypad 1-9 (5 stands still), `s' for last stand, `t' to teleport. Needs Microware's math module and a real TERM. |
| `snake` | snake arcade game.  You are the `I', the money is the `$' and the snake chases you; h/j/k/l move, `x' quits. Run it from a login session -- bare, with no TERMCAP, it bus errors instead; see DOC/README-BUSERR<br>**How:** Full-screen. h/j/k/l move; reach the `$' before the snake reaches you. `x' quits. |
| `sokoban` | &#9733; Sokoban: push every packet (`$') onto a storage square (`.') without trapping one. Its fifty levels, help text and saved games are in GAMES/SOKOBAN, and it asks the system for your user name, so run it from a login<br>**How:** Wants a username, so run it from a login rather than a bare shell, or it stops with "cannot get your username". |
| `tet` | Tetris -- `p' plays; s/j and f/l move a piece, d/k turns it, space drops it, q quits to the high-score table it keeps in GAMES/tet.hs.  Needs a terminal, not a pipe<br>**How:** Tetris. `p' plays from the menu; s or j moves the piece left, f or l right, d or k turns it, space drops it, ESC pauses and q quits to the high-score table, kept in GAMES/tet.hs. Give it a real terminal: it does no terminal setup of its own (the raw-mode code in SRC/tet/tet.c is inside `#ifndef OSK'), so from a pipe it draws its board and reads nothing. |
| `thricken` | collect every diamond to load the next level: hjkl move, s and r save and restore, q leaves, ^C quits; -l <n> starts at level n, -d plays screens of your own. Screens in GAMES/THRICKEN; DOC/thricken<br>**How:** Full-screen, the sequel to perp. Collect every diamond on the level and the next one loads: h j k l move, s saves the level position and r restores it, q leaves the game and ^C quits. `-l <n>' starts at level n (0 to 6 ship here) and `-d <directory>' plays a set of screens of your own -- DOC/thricken/screens.doc says how to write them. The panel names the level, the score, the moves and what you are collecting; the screens are in GAMES/THRICKEN and the high score file is GAMES/THRICKEN/scores. |
| `torus` | robots on a torus: each move you make, the robots close in -- lead them into each other to make scrap heaps; hjklyubn move, t teleports, q quits; scores in GAMES/TORUS<br>**How:** Full-screen. You are @; + robots step toward you each turn and # robots twice. Make them collide -- each collision leaves a scrap heap * that destroys robots running into it. h j k l y u b n move, . or w waits, t teleports to a safe square (the count is bottom left), r to a random one, a is antimatter, s sits tight to the end, q quits. The field's edges join; +h and +v flip how. `torus -s' shows the scores, kept in GAMES/TORUS. |
| `tt` | Tetris for terminals: , and / move, . rotates, space drops, s pauses, q quits<br>**How:** Tetris for terminals, full-screen: , and / move the piece, . rotates, space drops, s pauses, q quits. |
| `wanderer` | a Boulderdash-style maze game: dig through the earth for diamonds. Its 49 screens are in GAMES/WAND/screens, found with this disk as /dd<br>**How:** Full-screen. Dig through the earth for diamonds, forty-five on the first screen. `q' quits. Its thirty screens are in GAMES/WAND. |
| `worm` | the growing worm: you are `@' with a body of `o's; h/j/k/l steer, H/J/K/L run. Eat a digit to grow that much; hitting the wall or yourself ends it. `worm <length>' sets the start length<br>**How:** Full-screen. h/j/k/l steer, H/J/K/L run; with no key the worm keeps going. Eat the digits to grow. Control-C gets you out. |

**Board & card**

| | |
|---|---|
| `accordian` | Accordian solitaire: the deck is dealt in a row, and a stack slides one or three places left onto a card of the same suit or rank, closing the gap; win by squeezing it to one pile |
| `back` | &#9733; backgammon on a full board, points numbered 1 to 24, with the dice cup and the doubling status beside it. Single letters are the commands: R rolls, D doubles, H is the help, N starts a new game, Q quits<br>**How:** Single letters are the commands: R rolls, D doubles, H is the help, N starts a new game, Q quits. |
| `bjack` | blackjack, a 1990 obfuscated-C contest entry: one deck, a stake of $1000 or the one you name (`bjack 500'); a wager of 0 or end of file quits<br>**How:** `bjack [stake]' -- $1000 unless you name one; the largest bet is 500. It asks `Wager?' before each hand, then offers double, hit, split and insurance as the cards allow; answer y or n. A wager of 0, a negative one, or end of file quits. |
| `blackjack` | Las Vegas blackjack in BASIC09: `runb blackjack'. RETURN draws, `s' stands, `d' doubles down, `x' splits, a wager of 0 ends the game. `blackjak' in GAMES is a different, SNOBOL4 version<br>**How:** BASIC09 I-code: `load /h1/CMDS/runb' then `runb blackjack' (bare module name -- a pathname gives BASIC09 error 43). It asks your name and whether you want the rules, then takes a wager and deals: RETURN draws a card, `s' stands, `d' doubles down, `x' splits a pair; a wager of 0 ends the game. runb links the `math' trap handler from the execution directory, so leave chx at CMDS -- tested, plays a full hand. |
| `blackjak` | &#9733; Las Vegas BlackJack (SNOBOL4-in-C).  Data: GAMES/SNOBOL |
| `bs` | Battleships against the computer on a 10x10 grid: place your fleet, then hunt the computer's ships square by square with the hjklyubn cursor keys; sink the whole fleet to win |
| `c4` | Connect Four against the computer: the columns are lettered a to g, and you drop a piece by typing a column's letter. Line up four in a row to win; `q' quits |
| `canfield` | Canfield, the casino solitaire you bet on: earn units for each card worked up to a foundation, building down in alternating colours on the tableau; name a move by its two ends (s2, tf, 13, 2f), `ht' deals, `q' quits |
| `cfscores` | reports canfield's betting record from GAMES/cfscores: hands, games, runs, thinking time and what you are worth. Before your first game of canfield it has nothing to report |
| `chess` | chess against the machine on a shaded board.  It asks for your colour, your name and a long or short game, then takes a move as two squares -- `e2' then `e4', two keystrokes each with no RETURN<br>**How:** It asks for your colour, your name and a long or short game, then takes a move as two squares -- `e2' for the piece and `e4' for where it goes. Each square is two keystrokes and needs no RETURN. |
| `craps` | casino craps at a full table: a key picks the bet (p pass line, d don't pass, f field, h hardway, o odds), then the amount and Return; r rolls, `?' lists keys, q leaves. High rollers in GAMES/CRAPS<br>**How:** Full-screen casino craps with a rack of $100. Each bet is a key, then the amount and Return: p is the pass line, d dont pass, c come, D dont come, b a place bet, f the field, h a hardway, o takes odds and l lays them; s, a, 2, 3, y and u are the one-roll proposition bets. r rolls the dice, `?' lists every key, ^L redraws and q leaves, writing the high roller list to GAMES/CRAPS/craps.list. $CRAPSNAME names you there if you set it, otherwise $USER does. |
| `crib` | cribbage.  Needs TERM set, so run it from a login session -- bare it says `Unknown terminal type'<br>**How:** Full-screen cribbage, and it wants TERM -- run it from a login session. Answer the instructions question, choose a long or short game, and discard by naming a card, `7H'. Control-C gets you out. |
| `cribbage` | &#9733; cribbage -- offers instructions before it deals.  Needs TERM, so run it from a login session<br>**How:** The other cribbage, the same shape: TERM must be set, it offers the rules first, then cuts for the crib. Control-C gets you out. |
| `drawpoker` | five-card draw poker against the computer, on a curses table: stay, drop or bet, then change up to three cards.  It offers its rules first (GAMES/LIB/poker_rules, paged with less); F quits.  Not the same game as `poker', which is cold-hand<br>**How:** Full-screen. Space leaves the title; y or n for the rules. s, d, b to Stay, Drop or Bet; r, d, c to Raise, Drop or Call; 1-5 sets the amount. To draw, type up to three card numbers and Enter. F then y quits; control-R repaints. |
| `fish` | Go Fish against the computer: ask for a rank you already hold and take any the other player has, or `GO FISH' and draw; four of a rank makes a book, and the most books wins |
| `fuddle` | chess against the computer: it asks whether you want white, draws a shaded board with the black pieces in reverse video, and takes moves as two squares, e2e4, printing `fuddling...' while it thinks |
| `gnuchess` | &#9733; GNU Chess with a full-screen board and a clock for each side; it answers 1.e4 from its opening book, which ships at the path compiled into it.  Source SYS/termcap.entry into your shell first: it reads TERMCAP as the terminal description itself. the board, keeps both clocks and plays, and opens its opening book by bare name, so it books when the book is in the current directory.  Source SYS/termcap.entry first. The CMDS build is the one `gnuchess' runs<br>**How:** Full-screen chess. It reads TERMCAP as the terminal description itself rather than as a filename, so do `. /dd/SYS/termcap.entry' first; then it draws its time-control menu and plays. The build in CMDS/GAMES is the one that draws a board. |
| `gnuchessc` | GNU Chess for the `chesstool' front end, so it prints no board, only moves: `1. ... e2e4', `My move is: g8f6'. `list' writes the game to a file checkgame can replay<br>**How:** Its board display reads files from a compiled-in path; supply them there for a board. It still takes a move as `e2e4' and answers with its own. |
| `gnuchessn` | &#9733; GNU Chess with the 1989 display, squares drawn as blocks of hashes for terminals with no highlighting; `shade', `rv', `stars', `coords' and `p' change the drawing. Moves as `e2e4'. Source SYS/termcap.entry into your shell first<br>**How:** As gnuchess: `. /dd/SYS/termcap.entry' first, then moves as `e2e4'. |
| `gnuchessr` | &#9733; GNU Chess with the plainest display: pieces as letters, capitals for one side. It prompts `Enter #moves #minutes', then trades moves. It finds its book wherever you run it; `set' lays out a position |
| `gnugo` | GNU Go 1.1: Go on a 19x19 board against the computer, with up to 17 handicap stones for black and the score counted at the end. Moves are a letter and a number, `D4'. Needs no terminal setup |
| `kalah` | Kalah, the stones-and-bins game, and Pigeon Plague against the computer: pick the game, a skill level 2 to 12 and who goes first, then type a bin number; -2 asks for advice<br>**How:** Line by line. Type k for Kalah or p for Pigeon Plague, then the computer's skill level from 2 to 12, then 1 to go first or 2 to follow. Each of you has six bins of three stones; at your turn type a bin number 1 to 6 to sow its stones, 0 to show the board again, -2 or lower to ask the computer for advice (it looks that many moves ahead), or -1 twice to abandon the game. The manual, with the rules of both games, is DOC/kalah/kalah.doc. |
| `mastrm` | Master Mind: break the computer's hidden four-peg colour code in ten guesses, reading the `b' and `w' pegs each guess earns for right colour in right or wrong place |
| `mille` | &#9733; Mille Bornes -- the French car-racing card game<br>**How:** Full-screen Mille Bornes. `p' picks a card, `u #' plays one, `d #' discards, `s' saves the game and `q' quits. |
| `monop` | Monopoly for two to nine players: `roll' to move and buy what you land on; `print' shows the board with owners and rents; `mortgage', `buy houses' and `trade' manage property. `quit' ends the game |
| `nchess` | GNU Chess with a letter board and, under it, a live table of the moves it is weighing -- depth, score, nodes, line. It opens its book from the current directory; `edit' sets up a position |
| `othello` | Othello (Reversi) against the computer: place a disk to flank a line of the opponent's between it and one of yours and they all flip; the most disks when the board fills wins |
| `poker` | &#9733; cold-hand poker against the computer, written in SNOBOL4; its data is in GAMES/SNOBOL |
| `reversi` | Othello against the computer or a second player, six strengths from Apprentice to Very Hard. Arrow keys or hjkl move, RETURN places a disk, `m' opens the menu; `-r' resumes a saved game. Unrelated to `othello' |
| `saa` | Streets and Alleys solitaire: eight stacks and a foundation per suit; move a stack's top card onto the next rank up or home to its foundation, and order every card to win |
| `scrabble` | Scrabble against the computer on the full board. hjkl move, `H' or `V' lays a word across or down, `T' trades, `A' asks the computer's choice, `S' and `R' save and restore, `Q' quits. `-n' sets players, `-m <n>' makes player n the computer. Words in GAMES/words |
| `sol` | Klondike solitaire at the terminal: t thumbs the deck three cards at a time, m moves a card or a run, h lists the commands and q quits<br>**How:** Full-screen Klondike. Type a command and RETURN at the cmd prompt: t (or just RETURN) thumbs the deck three cards at a time; m with a source and a destination moves -- 1-7 for a run, d for the deck, a for an ace pile; a turns on the auto pilot; r shows the rules, h the commands; q quits. s, p, d and w are cheats, and it remembers. |
| `solx` | a harder solitaire with no deck: every card is dealt into runs, which may be split -- `m run position destination'; h lists the commands<br>**How:** Full-screen, and harder than sol: there is no deck, every card is dealt into runs that may be split, and the layout runs sideways so runs can grow long. m takes a run, the card position to split at, and the destination run (or a for an ace pile); h lists the commands and r the rules; q quits. |
| `tttt` | tic-tac-toe on a four-by-four board, so three in a row is not enough. Name a square as a column letter and a row digit, `b1'; `q' quits<br>**How:** Full-screen tic-tac-toe on a four-by-four board. Name a square as a column letter and a row digit, `b1'. `q' quits. |
| `vcraps` | casino craps, full screen: bet with p (pass line), c, dp, f, h and more -- type the amount and Return -- then r rolls; ? lists every bet, ESC abandons an entry, X quits<br>**How:** Full-screen casino craps with $1000 to start. Space clears each message at the bottom. p bets the pass line: type the amount and Return. r rolls the dice. c is a come bet, dp don't pass, dc don't come, f the field, b6 and b8 big 6 and 8, h22 to h55 the hard ways, a7 any seven, ac any craps; a number then c, p, dc or dp bets on that number. t takes a bet down, $ totals the bets, m reviews messages, ? lists all of it, ESC abandons an entry, X quits. -b sets the bankroll and -s plays single odds. |
| `yahtzee` | Yahtzee for one or more players: say how many, space switches a player between Computer and Human (j and k move, RETURN starts); then keep or re-roll five dice and choose a box to score. Different from yahtzee2 |
| `yahtzee2` | Yahtzee 2.1 on a curses scoreboard, up to six human or computer players: space toggles human/computer, `n' names a player. In play a digit holds a die, space rerolls, `b' shows the rules, `q' quits. High scores in GAMES/YAHTZEE |

**Chess utilities**

| | |
|---|---|
| `bincheckr` | checks a GNU Chess binary opening book: entry size, book size and count, and the runs of used slots in its hash table. It reads gnuchess 4.0's book and the older layout. GAMES/gnuchess.book is a text library, not a binary book<br>**How:** Give it gnuchess 4.0's binary book: `bincheckr gnuchess.data' in /dd/GNUCHESS4.0/MISC prints the entry size, book size, count and the runs in its hash table.  GAMES/gnuchess.book is the text library, not a binary book. |
| `checkgame` | check a saved GNU Chess game for illegal moves and print the board it finishes on.  It reads the `chess.lst' that gnuchess writes when you type `list'.  A different program from `game', which makes PostScript<br>**How:** It reads the `chess.lst' that gnuchess writes when you type `list'. Play in a directory of your own -- `ksh -c "cd /dd/tmp/mine; gnuchess"' -- type `list' then `quit', and then `checkgame /dd/tmp/mine/chess.lst'. |
| `game` | draws a saved GNU Chess game board by board as PostScript, for printing with the ChessFont file in SRC/gnuchess/GNUCHESS4.0/MISC.  It reads the list gnuchessc writes when you type `list'<br>**How:** Same input as checkgame, a gnuchess `chess.lst', and it writes PostScript on standard output, a board for each move: `game chess.lst > out.ps'. |
| `gnuan` | GNU Chess analyser -- annotates a saved game move by move<br>**How:** Give it a file of moves like `e2e4 e7e5 g1f3', then a search depth and a minutes-per-move limit, and it annotates the game move by move. At the end of the file it prints the position and stops with `Bad move'. |
| `postprint` | prints the positions in GNU Chess's hash file as PostScript, each with best move, depth and score. No arguments: it reads GNUCHESS4.0/MISC on /h0, which ships empty and fills as gnuchessc plays out of its book<br>**How:** It wants gnuchess's persistent hash file -- point it at one. |

**Dungeon crawl**

| | |
|---|---|
| `castle` | The Realm of the Wizard, a first-person dungeon in character graphics. hjkl (or 4 2 8 6) turn and step, `c' casts, `i' is inventory, `<' `>' take stairs; control-E saves, `castle -r' resumes, `q' quits<br>**How:** Full-screen dungeon game seen in the first person. hjkl (or 4 2 8 6) turn left, back up, step forward and turn right, `.' turns around, `c' and a letter casts a spell (`a' tells you where you are), `i' is the inventory and ESC leaves it, `<' and `>' take the stairs. Control-E saves and leaves, `castle -r' resumes the saved game, `q' then `y' quits to the score list. Its data is GAMES/CASTLE. |
| `hack` | hack -- the original dungeon crawl NetHack grew out of<br>**How:** run it by its full path: `/dd/CMDS/GAMES/hack', not `hack'. It chdirs into its playground and then stats argv[0] to date-check saved levels, so a bare name cannot resolve and it stops with "Cannot get status of hack." Invoked in full it starts: "Are you an experienced player?". Its playground -- record, bones, rumors, help -- is in GAMES/HACK/PLAYGROUND. |
| `hackwish` | a hack cheat: replays hack until a wizard starts with a wand of wishing, wishes for what you name, and saves the game to carry on in hack |
| `larn` | &#9733; larn, a dungeon crawl: RETURN gets past the opening text. A saved game goes to Larn.sav in your home directory; the scoreboard, help, fortunes and maze are in GAMES/LARN/PLAYGROUND<br>**How:** Full-screen dungeon crawl. RETURN gets past the opening text. Control-C gets you out; its playground is GAMES/LARN/PLAYGROUND. |
| `moria` | UMoria 4.87: roll a character, shop in town, then descend after the Balrog. `?' lists commands, `^X' saves, `^K' quits. Its data is USR/GAMES/MORIADIR, found with this disk mounted as /h0<br>**How:** Full-screen dungeon crawl. SPACE past the news, then pick race, sex (m/f), ESC to keep the stats, class, and type a name; SPACE past the character sheet puts you in the town. `?' is the command list, `^X' saves and `^K' quits. It needs TERM set; its data is USR/GAMES/MORIADIR. |
| `nethack3` | NetHack 3.0f: choose a character and descend the Mazes of Menace for the Amulet of Yendor. `?' lists commands, `S' saves, `Q' quits. Its data is USR/GAMES/LIB/NETHACK3DIR, found with this disk as /h0; HACKDIR names another<br>**How:** Full-screen dungeon crawl. `y' lets it pick your character, SPACE clears each --More--, `?' is the command list, `S' saves and `Q' quits. It needs TERM set; its data is USR/GAMES/LIB/NETHACK3DIR. |
| `rogue` | a rogue 5.3 clone: explore the dungeon, fight and descend. hjkl move, `i' inventory, ESC cancels, `Q' then `y' quits to the Top Ten. Needs TERM<br>**How:** Full-screen dungeon crawl. h, j, k and l move; `i' lists the pack and SPACE puts it away; `d' drops something and ESC cancels any question; `Q' then `y' ends the game and shows the Top Ten, kept in GAMES/ROGUE/rogue.scores. It needs TERM set, as SYS/login does. |
| `ularn` | ULarn, a variant of larn: pick a class, then down into the dungeon<br>`Cmd line format: Ularn [-slicnh] [-o<optsfile>] [-##] [++]` |

**Other games**

| | |
|---|---|
| `arithmetic` | a drill in sums: it asks until the answer is right, and every twenty problems prints rights, wrongs and seconds per problem. `-o' picks operations from +-x/, `-r' the largest number; ^C stops with the score<br>**How:** Line-by-line drill in sums. It prints a problem such as `3 + 4 =' and waits; type the answer and RETURN. A wrong answer gets `What?' and the same problem again, and after every twenty it prints the score. `-o +-x/' picks the operations (+ and - by default), `-r 12' the largest operand (10). ^C or end of input stops it with the score so far. |
| `ask` | the client for `wisecrack': it reads one line from /pipe/txtpipe and prints it, and says `No Wisecracks coming' when nothing is feeding the pipe. Start the server first -- `wisecrack &' -- and it answers<br>**How:** The reader for `wisecrack': it takes the next slogan from the pipe wisecrack writes to and prints it, one a call, in German. Start the server first -- `wisecrack &' -- or ask says "No Wisecracks coming". From EFFO forum 20. |
| `atc` | Air Traffic Controller: bring each plane on the radar to its destination at the right altitude without two meeting. A plane's letter, then `a' and a digit sets altitude, `t' and a direction turns; RETURN sends, `?' prompts. `atc -l' lists airports, `-g easy' picks one; ^C quits<br>**How:** Full-screen air traffic control. `atc -l' lists the airports and `atc -g easy' picks one. Type a command to a plane by its letter: `a' and a digit sets altitude (and takes off), `t' and a direction key turns; RETURN sends it, `?' lists what may come next, ^L redraws and ^C asks to quit. Its airports are in GAMES/ATC. |
| `backgammon` | &#9733; backgammon against the computer, drawn as a board of numbered points. -n skips the instructions and -r gives you red; given a file it plays the game recorded in it<br>`Syntax: backgammon [<opts>] [<file>]` |
| `bandit` | a one-armed bandit with a payoff table and a bankroll of 100: bet 0 to 5 at the prompt, `q' walks away with the total. Source SYS/termcap.entry into your shell first; it reads TERMCAP as the description itself<br>**How:** A slot machine. Do `. /dd/SYS/termcap.entry' first -- it reads TERMCAP as the description itself. Then `n' skips the instructions, a number 0-5 is the bet, and `q' at the bet prompt ends with your total. |
| `convert` | starts the WORLD text adventure: run it and the game opens with its banner, the opening paragraph and a `>' prompt<br>**How:** It starts the `world' adventure -- run it and the game opens. |
| `corewar` | Core War: two Redcode programs fight over a circular memory. `corewar <cycles> a.e b.e' runs the battle and maps which cells each holds. Assemble warriors with cwasm; samples are in GAMES/COREWARS |
| `cwasm` | the Core War assembler: `cwasm w.rc' turns a Redcode warrior into the object file w.e that corewar loads.  Sample warriors are in GAMES/COREWARS |
| `cwdis` | the Core War disassembler: `cwdis w.e' prints a warrior object back as a numbered opcode and parameter table |
| `hotel` | &#9733; hotel -- a hotel-chain board game played against the computer: it asks how many players (2 to 7), seats you among them at random and plays the rest itself.  Each turn you play a numbered tile from your hand<br>**How:** Full-screen: it takes over the display. **control-C gets you out**; q, Q, control-D and ESC do not. If it has a quit command of its own, its documentation in DOC/ will say. |
| `mkdict` | builds bog's dictionary from a word list: `mkdict < words > dict'<br>**How:** Run it in /dd/GAMES/BOG, where bog's word list is; it is in CMDS/GAMES. |
| `mkindex` | builds the index bog reads its dictionary through: `mkindex < dict > dict.ind'<br>**How:** Run it in /dd/GAMES/BOG after mkdict; it is in CMDS/GAMES. |
| `nobs` | cribbage against the computer: it deals six cards, asks which two go to the crib, plays the hand and pegs the board above<br>**How:** Full-screen: it takes over the display. **control-C gets you out**; q, Q, control-D and ESC do not. If it has a quit command of its own, its documentation in DOC/ will say. |
| `shuffle` | a full-screen switch puzzle: a row of numbered switches, `Wich switch ?' and a move counter, where flipping one flips its neighbours; q quits. It wants TERM. For shuffling lines, `sort -r' and `tac' are the line tools<br>**How:** Full-screen: it takes over the display. **`q' quits**. |
| `ski` | Ski! -- down an endless slope a row a turn: R and L turn, J jumps, T teleports, I fires at the Snoman; Return waits<br>**How:** Line by line down an endless slope: each turn draws one row with you as the I, and the ? at the end of the line waits for a letter or Return. R and L turn you further right or left, J jumps and H hops, T teleports, I launches an ICBM at the Snoman (A) and D calls the Fire Demon. Trees Y, bare ground and ice # can hurt you, and the run ends when something bad happens. The manual is DOC/ski/ski.man. |
| `stone` | &#9733; a stones game in the Nim family against the computer, written in SNOBOL4; its data is in GAMES/SNOBOL |
| `teachgammon` | &#9733; backgammon that teaches you the game as you play<br>`Syntax: backgammon [<opts>] [<file>]` |
| `tess` | &#9733; Beyond the Tesseract, a text adventure whose puzzles draw on physics and mathematics: two-word commands, about two hundred words understood, and -f skips the title and scenario |
| `trek` | Star Trek: choose length, skill and password, then hunt Klingons before time runs out. `s' short scan, `l' long scan, `m' move, `p' phasers, `t' torpedoes, `do' dock; `help' lists all, `terminate' ends, `dump' saves to trek.dump<br>**How:** Line-by-line game at a Command: prompt. RETURN past the banner, then answer the length (s/m/l), skill (n/f/g/e/c/i) and a password. `s' is the short-range scan, `l' the long range, `help' lists the commands, `terminate' ends the game and `n' at `Another game' leaves. |
| `trek73` | Star Trek battle at a Code [1-32] prompt: give a name, a sex and how many enemies, then fight by number or in words -- `damage'; 32 lists the commands; wait too long and a turn passes<br>**How:** Line-by-line battle at a Code [1-32] prompt. Give the captain's last name, a sex and how many enemy vessels (1-9), and the log opens. Commands go by number -- 32 lists them -- or in words: `damage' gives the damage report. A command must come within the turn time, 30 seconds unless `-d 60' or TREK73OPTS=time=60 says otherwise; if it does not, ** TIME ** and the turn passes. -c, -s, -n and -r set the captain, sex, ship name and enemy race. Saving a game is not possible on OS-9. |
| `typefast` | a typing game: type each falling word, ending with SPACE or RETURN, before it lands. 1, 2 or 3 sets the pace; ten misses end it with your words per minute. Source SYS/termcap.entry into your shell first; it reads TERMCAP as the description itself<br>**How:** A typing game. Do `. /dd/SYS/termcap.entry' first -- it reads TERMCAP as the description itself. Then `n' skips the instructions and 1, 2 or 3 picks the pace; type each falling word and end it with SPACE. Ten misses end the game. |
| `vtxtcn` | builds the World adventure's text tables from vtext.dat in the current directory: q1text.dat and three .inc files |
| `wisecrack` | a server, and `ask' is its client. Run it in the background and every `ask' pulls one line out of it through /pipe/txtpipe -- slogans from a German OS-9 seminar, 1992-93. `wisecrack & ask "anything"' |
| `world` | a text adventure: a landing party stranded on an alien world; its text is in GAMES/world |
| `wump` | hunt the Wumpus through a cave: a draft means a pit next door, a smell the Wumpus. Move room to room, then shoot a crooked arrow along a path of rooms; miss and he may wake. `-h' is harder, `-r' `-t' `-a' resize the cave |
| `yidslots` | a slot machine whose three windows spin through the parts of Jewish names: type a bet, watch them stop, and see what the combination pays; 0 ends the game.  Names in GAMES/YIDSLOTS<br>**How:** Full-screen slot machine. Three windows spin through parts of names -- a first name, a name beginning and a name ending. It asks `Place your bet', you type a number and Return, and 0 ends the game. You start with 100; a combination that matches the payoff list multiplies the bet, and `Bob Glick stein' pays 1000 to 1. The windows and the payoffs come from GAMES/YIDSLOTS/yid-names, and a file named on the command line is read instead. The rules are in DOC/yidslots/README. |

**Puzzles**

| | |
|---|---|
| `hanoi` | solves the Towers of Hanoi as a list of moves: `hanoi 3' prints the seven moves for three disks; n disks take 2^n-1<br>**How:** `hanoi 3' prints the moves that shift three disks from tower 1 to tower 2, one move a line. n disks take 2^n - 1 moves, so `hanoi 20' prints over a million lines. |
| `hanoimod` | the Towers of Hanoi as the three towers after every move: `hanoimod 3'<br>**How:** `hanoimod 3' shows the same solution as hanoi as pictures: after each move, a line per tower listing the disks on it, largest first. n disks print 4 x (2^n - 1) lines. |
| `hexa` | hexagonal Sokoban: push every moneybag onto a safe square on a six-sided grid, one bag at a time and only ever forward; k/j move up and down, u/i/n/m along the diagonals.  Five screens ship, and `hexa <n>' edits one |
| `hinterhalt` | &#9733; a small maze game, in German: asked whether you need instructions (J/N) and told no, it draws the board -- walls, the player and a target |
| `knight` | the knight's tour: move a knight from square to square, never landing twice, and try to visit all 64 -- a row letter then a column digit; ESC cancels the row, Q quits<br>**How:** Full-screen. Answer the instructions question, then S to choose the first square or R for a random one. Each move is a row letter A-H and a column digit 1-8, and must be a knight's move to a square not yet visited; ESC after the row letter cancels it, Q at the row quits. The game ends when no move is left, with the count of squares visited. |
| `maze` | maze generator, small enough to have won an obfuscated-C contest.  It reads the number of rows on standard input and draws a maze that many rows tall: `echo 11 \| maze'<br>**How:** Reads the number of rows on standard input: `echo 11 \| maze' draws a maze eleven rows deep. |
| `mines` | &#9733; minesweeper on a sixteen-by-sixteen board with forty mines: name a square by its row and column letters, answer `Mark?' with Y to flag it; q quits<br>**How:** Full-screen minesweeper. Name a square by its row letter and then its column letter, and answer `Mark?' with Y to flag it rather than open it. `q' quits. |
| `queens` | &#9733; an N-queens solver, an obfuscated-C contest entry: it reads the board size on standard input as a number and draws every arrangement it finds with no two queens attacking: `echo 6 \| queens'<br>**How:** Reads the board size on standard input as a number: `echo 6 \| queens'. |
| `sod` | &#9733; Swamp of Death: cross from top left to the X at bottom right without sinking; each square shows how many neighbours are dangerous. hjkl or 4 8 6 2 move, `q' RETURN gives up. `sod -l5' picks level 1-9, `sod -s' shows scores<br>**How:** Full-screen. The swamp is a grid; you start top left (the marker) and the exit X is bottom right. hjkl or 4 8 6 2 move one square, and each square you have stood on shows how many of the eight around it would sink you. `q' asks "in fear to die?" and RETURN then gives up, printing that level's score table. `sod -l1' is the easiest level and `-l9' the deadliest; `sod -s' prints the high-score table. Its scores are in USR/GAMES/LIB/SOD, so mount this disk as /h0 too. |

**Word & guessing**

| | |
|---|---|
| `animal` | the guess-the-animal game that learns: `animal <file>' asks yes-or-no questions, and when it guesses wrong it asks what you meant and writes that into the file. DOC/animal/example is one to start from<br>**How:** The file it learns from is one you name: `animal /dd/DOC/animal/example'. Answer y or n to each question; when its final guess is wrong it asks what you were thinking of and what question tells the two apart, and writes that back into the file. Control-C leaves it. |
| `bog` | Boggle: sixteen lettered dice and three minutes to type every word you can trace through adjoining letters; its word list, index and help are in GAMES/BOG<br>**How:** Boggle. Space starts the three-minute round, `?' shows the rules, and you type every word you can trace through adjoining letters. Control-C leaves it. Its word list, index and help are in GAMES/BOG. |
| `hang` | &#9733; hangman: type a letter to guess it, and the gallows fills in as you get them wrong; its word list is GAMES/dict<br>**How:** Hangman. Type a letter to guess it; the letters still unused are along the top. Control-C gets you out. Its word list is GAMES/dict. |
| `jotto` | Jotto: you and the computer each pick a secret five-letter word of different letters and take turns guessing; a wrong guess is scored by how many of its letters are in the word |
| `jumble` | prints every ordering of the letters of a word, one to a line, to solve a newspaper word jumble: `jumble tac' lists tac, tca, atc, act, cat and cta<br>**How:** `jumble <word>' prints every ordering of its letters, one per line, and that is all it does: read down the list for the one that is a word. A word of n letters gives n! lines -- 720 for six letters -- so keep to short words or send it through grep or less. |
| `jumble2` | unscramble words against the clock: pick a level and how many words, then type each word back; `jumble2 -s' shows the high scores, kept in GAMES/JUMBLE2<br>**How:** It asks whether you want directions, a level -- (E)xpert, (H)ard, (M)oderate or (S)imple, then RETURN -- and how many words. Type each unscrambled word and RETURN before the time runs out: ? reprints the word and the time left, p passes, q forfeits. After a round RETURN plays again, c changes level, s shows the scores and q quits. Four words or more to reach the score list, kept in GAMES/JUMBLE2; `jumble2 -s' shows it. |
| `wf` | makes a word-search square from a file of words: `wf -f words -x 12 -y 12 -t Title'; without -f it reads `words' in the current directory, and DOC/wf has two word files<br>**How:** Makes a word-search square from a file with one word per line, optionally followed by a clue: `wf -f words' (a file named words in the current directory is the default). -x and -y set the size, up to 20; -t gives a title; -h, -v, -d, -b and -a choose which directions words may run; -r picks words at random; -p leaves the word list out and -c prints the clues instead. DOC/wf has two word files, words and words.2. |

</details>

## Screen toys

*Animations and screen effects -- they draw on the terminal rather than print to it. Some run until you stop them.*

<details><summary>10 programs</summary>

| | |
|---|---|
| `bite` | a skull draws itself and bites -- a screen toy; q quits<br>**How:** Full-screen: it takes over the display. **`q' quits**. |
| `card` | Towers of Hanoi whose twelve disks are the lines of a Christmas message; VT100, wants TERMCAP |
| `juggle` | animated juggling: balls fly between two hands in a site-swap pattern -- `juggle -p 3' is the cascade, `-p 441' a trick, `-r 5' a random five-throw pattern. ^C ends it<br>**How:** Full-screen animation that runs until ^C. `juggle -p 3' juggles the three-ball cascade; a pattern is site-swap digits, each the height of a throw, so `-p 51' is a shower and `-p 441' a trick, and one that cannot be juggled is refused. `-r 5' picks a random five-throw pattern, `-s 0.1' makes the steps smaller and smoother, `-h' holds 2-throws, `-n' gives it a title. |
| `life` | Conway's Game of Life on a pattern file: `life glider'; the patterns are in GAMES/LIFE<br>**How:** life [init-file]. The patterns are in /dd/GAMES/LIFE -- try `life /dd/GAMES/LIFE/glider`. It also wants more memory than the default; from the OS-9 shell that is `life #22k <file>`, and bash has no #size syntax at all. |
| `rain` | raindrops land on the screen and spread in rings -- a screen toy; control-C ends it<br>**How:** Full-screen: it takes over the display. **control-C gets you out**; q, Q, control-D and ESC do not. If it has a quit command of its own, its documentation in DOC/ will say. |
| `rot22` | software rot as a screen toy: a file's letters come loose and fall to the bottom of the screen until the text has drained away. Name a file or pipe text in |
| `textb` | &#9733; Mandelbrot set drawn in ASCII on an 80x25 terminal.  Start with X -2.3, Y -2.0, range 4.0, 32 iterations<br>**How:** An ASCII Mandelbrot viewer -- it asks four questions and draws. Try X_Coord -2.3, Y_Coord -2.0, RANGE 4.0, Max Iter 32. Needs Microware's cio. |
| `ttyexp` | character fireworks: bursts arc under gravity with trails. -s<n> bursts at once, -p<n> points each, -D<n> seconds; `ttyexp -s2 -p50' fills the screen. VT100; wants TERMCAP<br>**How:** `ttyexp -s2 -p50' fills the screen with bursts; it runs ten seconds and clears the screen when done. |
| `worms` | worms crawl about the screen at random, each leaving a trail -- a screen toy: -number how many, -length how long, -trail to leave one; control-C ends it<br>`usage: /dd/CMDS/GAMES/worms [-field] [-length #] [-number #] [-trail]` |
| `xmas` | a Christmas card in characters: a tree drawn and trimmed, lights blinking along its strings, reindeer running across the screen, and round again until control-C<br>**How:** Full-screen: a Christmas card that plays in a loop. Control-C gets you out. |

</details>

## Amusements

*Generators, simulators and diversions that are not quite games.*

<details><summary>39 programs</summary>

**Biorhythms**

| | |
|---|---|
| `bio` | a biorhythm chart in BASIC09: `runb bio' asks a date and a birthday as DD.MM.YYYY (RETURN takes today), then `g' for a graph or `v' for values and a number of days<br>**How:** A biorhythm chart in BASIC09 -- `runb bio' draws it. It asks a Date, then a Birthday, both as day.month.year with a four-digit year (RETURN at the Date prompt takes your system date), then `g' for a graph (or `v' for values) and a number of days, and plots the physical, emotional and mental cycles. |
| `biory` | biorhythm chart, in German: asks a name, a birth date as TTMMJJ and a span of years as JJ-JJ, and writes Biory.Lis in the current directory. `load os9lib' from CMDS first; RETURN at the name prompt ends it |

**Curiosities**

| | |
|---|---|
| `areacode` | &#9733; looks up North American telephone area codes, as many as you give it, from a table of the late 1980s; a code it does not know is said to be no area code |
| `globe` | show the currently-lit face of the Earth in ASCII, the globe turning through the day as the hours pass |
| `phoon` | show the phase of the moon as a little picture: `phoon' for tonight, `phoon 2025 12 25' for a date; `-l' sets the size |
| `smiley` | explains the sideways faces of net messages: `smiley ":-)"' prints what that one means; with no argument it prints one of the 589 at random, -l lists them all and -e explains $SMILEY<br>**How:** Explains the sideways faces people typed in net messages. `smiley ":-)"' prints what that face means, and a face with several meanings gets them all. With no argument it prints one of the 589 at random; -f prints just the face, -l lists the whole list, -e explains the face in $SMILEY, and -V counts it. The list is the one the post carried, uncensored, so some of it is crude. The manual is DOC/smiley/smiley.1. |
| `telenum` | turns words into the telephone number their letters dial: `telenum hello' prints 43556<br>**How:** `telenum hello world' prints the number each word dials, one a line: 43556 and 96753. Letters with no key (q and z) print as themselves. |
| `telewords` | spells a telephone number every way its keypad letters allow, one a line: `telewords 43' prints gd, ge, gf and so on to if<br>**How:** `telewords 43' prints every spelling of the number with the letters on its keys, one a line -- gd, ge ... if. 0 and 1 stand for themselves; -<digit><letters> changes what a key spells. |
| `trigraph` | prints its own C source spelled in ANSI trigraphs -- ??< for {, ??= for # -- a 1990 obfuscated-C contest entry<br>**How:** `trigraph' prints its own source with every # { } [ ] \ ^ \| ~ written as its ANSI trigraph -- ??= ??< and the rest. Microware's cpp does not read trigraphs, so SRC/ioccc/OSK holds the translated copy it was built from. |
| `westley` | picks a daisy: `westley 7' pulls seven petals, loves me, loves me not, and says how it ended. An obfuscated-C contest winner whose source reads as a letter<br>**How:** `westley <number>' picks a daisy with that many petals -- loves me, loves me not -- and says how it came out. The 1990 contest's Best Layout: its source is written to be read as English correspondence, letter by letter, and the judges' note reads the first block as "charlie, doubletime me, OXFACE! not interested, get out". Reading the source is the point of it. |
| `wysecrack` | &#9733; wisecracks for a Wyse terminal's status line: once a minute it sends ESC F and one of twelve lines, then stops. On other terminals the lines appear in the text. Nothing shows for the first minute. Companion to wysetime |

**Generators**

| | |
|---|---|
| `biff` | rewrites text as B1FF, the Usenet caricature of an over-excited newcomer: capitals, zeros for o's, `C00L!!!', `WAREZ!1!!'. `echo text \| biff'.  Mild swearing comes out stronger |
| `chef` | talk like the Swedish Chef: a filter that rewrites English into his mock accent -- the->zee, w->v, o->oo -- and barks "Bork Bork Bork!" at each sentence end.  `echo text \| chef` |
| `discord` | reads text on standard input, learns which word follows which, and writes new paragraphs by walking those chains at random, with the odd `fnord'.  Each paragraph opens with nroff's `.PP' |
| `drawl` | give text a broad Texan accent: drops the g from -ing and swaps in tuh/thuh.  `echo text \| drawl`, a stdin filter |
| `fudd` | talk like Elmer Fudd: a filter that turns r and l into w and th into d, so text comes out in his lisp.  `echo text \| fudd' |
| `ken` | turns English into Cockney, with rhyming slang for the computer words: `computer' becomes `French Tutor', `file' `Royal Mile'.  `echo text \| ken' |
| `lame` | rewrites its arguments into IRC leet-speak -- o->0, you->U, and->&, i->1 -- the way a lamer types.  `lame your text' |
| `lotto` | picks lottery numbers after a testimonial and a demand that you believe -- answer y or n; six from 1 to 49 unless -n, -b and -t say otherwise<br>**How:** `lotto' asks whether to hear testimonials, whether you believe and whether you really believe -- answer y or n -- and then draws six numbers from 1 to 49, a second apart. -n, -b and -t change how many and the range; -a sets how many testimonials. End of input quits. |
| `name` | &#9733; invents pronounceable names for the characters in a tabletop game, as many as you ask for, dealing vowels and consonants in turn with the letter frequencies of a Scrabble set |
| `newsgen` | &#9733; makes up a news bulletin at random from parts -- a top story of public figures, deeds, places and reactions, then the weather -- different every run<br>`"news" or "news lp"` |
| `ogrify` | folds text to lower case, wraps it at 40 columns and swaps words at random for words from a list -- five in a hundred, or `-50' for half.  Name the list first: the one it came with is DOC/ogrify/ogre.words<br>`Usage: ogrify [ogre.words] [-p] [-lnnn] [-nnn] [-u] [-n]` |
| `pig` | turns English into pig latin: every word of two letters or more moves its first letter to the end and adds `a'.  `echo text \| pig'<br>**How:** Pipe English through it: `echo "pig latin" \| pig' prints `igpa atinla'. Each word of two or more letters moves its first letter to the end and adds `a'; one-letter words and punctuation pass unchanged. |
| `pwgen` | &#9733; pronounceable passwords: `pwgen <length> [how many]'; the words come out one letter shorter than the length, which counts the end of the string<br>**How:** pwgen <length> [count]: length 4 to 16. It takes a few seconds over each password, so allow for that. |
| `repunsel` | a pun filter: English comes out full of plants and gardens -- `and I would root' becomes `ANT I WOOD ROOT'.  `echo text \| repunsel'<br>**How:** Pipe English through it: `echo "And I would root" \| repunsel' prints `ANT I WOOD ROOT'. Each word it has a garden pun for -- and, would, not, over, leave, care -- comes out in capitals; the rest passes through. |
| `rndname` | &#9733; invents pronounceable names, as many as you ask for -- the earlier version of `name', with every letter equally likely, so the names come out more exotic |
| `roll` | rolls dice named on its command line: `roll 3d6', six rolls with `6x3d6', the best three of four with `3,4d6', a repeat with `2@'; with nothing it rolls d100<br>**How:** Rolls dice named on its command line and prints each total. `roll 3d6' is three six-sided dice; `roll 6x3d6' rolls them six times, best first; `roll 6x3,4d6' keeps the best three of four dice each time; `roll 2@3d6' repeats the whole thing; a bare number is one die with that many sides, and with nothing it rolls d100. A die needs at least two sides. |
| `rpoem` | &#9733; writes verses at random from a grammar and a word list in GAMES/SNOBOL; a number says how many, thirty without one |
| `rstory` | a cumulative tale in the shape of The Old Woman and Her Pig, the animal, the obstacle and every helper drawn at random; `rstory \| tformat' sets it justified under a dated heading. Data: GAMES/SNOBOL |
| `scales` | &#9733; deals scales and chords into a random practice list with tick-boxes, written to `scales.lst' in the current directory or a file you name: -d diatonic, -a altered, -m modes, -c chords, each with key signature and spelling<br>**How:** Pick at least one of -d -a -m -c or it asks what you had in mind; `scales -d -c' writes 195 entries to scales.lst, and a trailing name writes elsewhere. |
| `sifi` | writes the plot of a science-fiction film -- who comes to Earth, what they want, and how it ends.  `sifi -3' writes three chapters<br>`Science Fiction plot generator` |
| `spew` | builds mock National Enquirer headlines from a grammar of phrases -- almost a yacc in reverse; `spew 5' makes five |
| `taxlaw` | writes sentences of imitation tax regulation, section and paragraph references included: `taxlaw 3' writes three<br>`usage: taxlaw [number of sentences]` |

**Simulated weather**

| | |
|---|---|
| `england` | &#9733; a year of random daily weather for a tabletop game, mid-Atlantic climate: `england 2' does two years. Siblings differ in climate and calendar: florida, georgia, minnesota, japan (Japanese calendar) and shire (Middle-earth calendar)<br>**How:** One of six weather simulators that differ only in climate and calendar: england, florida, georgia, minnesota, japan (Japanese calendar) and shire (Middle-earth). Each prints a year of weather, a line a day, with a summary at each month's end; a number says how many years. |
| `florida` | &#9733; a year of simulated Gulf-coast weather, day by day -- the weather program's Florida profile<br>**How:** Prints a year of Gulf-coast weather, a line a day; `florida \| head -n 37' shows January. See england. |
| `georgia` | &#9733; the weather program on its south-Atlantic profile; see england |
| `japan` | &#9733; the weather program on its north-Pacific profile, with the months of the Japanese calendar; see england<br>**How:** A weather simulator on the Japanese calendar -- see `england'. |
| `minnesota` | &#9733; the weather program on its north-Atlantic profile; see england |
| `shire` | the weather program on its mid-Atlantic profile, with the months of Tolkien's Shire calendar; see england<br>**How:** A weather simulator using the Middle-earth calendar -- see `england'. |

</details>

## System & modules

*OS-9 module and process tools, devices, system state and scheduling.*

<details><summary>141 programs</summary>

**Devices & disks**

| | |
|---|---|
| `dam` | &#9733; prints a disk's allocation map, one character per cluster: `dam /dd' |
| `dedit` | BASIC09 disk sector editor -- read, edit and write raw sectors, decode a disk's identification sector.  I-CODE, not 68000 code: run it with runb and the bare module name, like bio and wysetime.  Nine modules in the one file. |
| `dinfo` | &#9733; reports on an RBF disk -- volume name, creation date, capacity, how much is free and in how many blocks -- doing the job your own `free' does and saying more. -e extends the display and -f reports fragmentation<br>`Syntax:   dinfo [<opts>] {<device name> [<opts>]}` |
| `dmode` | shows and changes an RBF device descriptor: drive, step rate, density, sides, sectors and the rest. `dmode /d1' lists; `dmode /d1 stp=3 vfy=$01' changes the resident copy and re-initialises the device. Load your OS-9's descriptor first<br>**How:** `dmode /<device>' lists the parameters of that disk's descriptor; `key=n' on the same line changes them in memory and re-initialises the device (hex keys take 0x or $). It needs the descriptor resident: on os9exec, `load' one of your own OS-9's first -- the card loads the RAM disk's, r0. |
| `dpark` | &#9733; parks the disk head: `dpark [/device]' restores an RBF device's head to track 00, which is what you did before moving a drive<br>`Syntax:   dpark [/device]` |
| `freeb` | lists a disk's free space block by block: how many free blocks, each one's size and start. -t counts them by size, -a lists every one, -h omits the header, -s the total<br>`Usage:` |
| `os9dsk` | reads a CoCo OS-9 .DSK disk image: `os9dsk -dir <file>.DSK' lists it, -get copies a file out, -proc prints a procedure file that extracts the whole tree<br>`Usage:	os9dsk -dir filename.DSK DSKpath` |
| `rsdsk` | reads a CoCo RS-DOS disk image, the Disk Extended BASIC side of the same .DSK files: -dir lists it, -get copies a file out.  Between them and os9dsk, either kind of Color Computer disk can be read here<br>`Usage: rsdsk -dir filename.dsk` |
| `shdev` | &#9733; lists the system's device table: what is mounted and the driver behind each |
| `ssl` | &#9733; show a file's segment list, sector by sector -- ssl <file> |

**Drivers & file managers**

| | |
|---|---|
| `cctrap` | the trap handler cpucache calls to read and switch the caches |
| `di` | the descriptor for the disp example driver, port $FEC30000 |
| `disp` | an SCF driver written in C, the example from OS-9 International 1/93, "Writing a device driver in C": it puts the low four bits of each character on a display port.  An example to adapt |
| `h0t` | an example lfcrman descriptor: /h0t is /h0, translated |
| `lfcrman` | a file manager that shows another device with its line endings translated between LF and CR, for sharing text with a Unix machine over NFS.  From OS-9 International 2/93 |
| `pty` | the descriptor for PtyMan's server side, /pty |
| `ptydrv` | PtyMan's placeholder driver; its descriptors name it |
| `ptyman` | PtyMan 1.3, a pseudo-terminal file manager: one program opens /pty/<name>, another /tty/<name> and gets an echoing, line-editing terminal joined to it; any number of pairs. osknet's telnet server uses it. DOC/ptyman/ptyman.doc |
| `thlpct` | an example lfcrman descriptor: /thlpct is /thlpc, translated |

**Finding things**

| | |
|---|---|
| `about` | what this collection knows about a program: what it is, where it came from, the files it opens and whether they are here, and whether source and documentation survive: `about hack'. DOC/CATEGORIES is for browsing |
| `whereis` | find a program's source, command and documentation -- SRC, CMDS, DEFS, LIB and DOC, searched all the way down on every device PATH names.  `whereis gen'<br>`whereis [ -sbmu ] [ -SBM dir ... -f ] name...` |
| `which` | what a command name runs, found the way the OS-9 shell finds it, and for a module already in memory, the file it came from.  `which -a dir'<br>`Usage: which [-i] [-a] [--] [<command>]` |
| `zc` | looks up a US zip code: `zc 60115' answers `De Kalb, IL.'. With no argument it opens a form -- type codes, C clears, Q leaves. Reads SYS/zipcodes.txt |

**Keeping**

| | |
|---|---|
| `keep` | take a program off this disk onto your own disk -- copies it and whatever DOC/DEPENDS says it needs, and records every file written.  `keep -n' shows what it would do without doing it.  See DOC/README-KEEP.<br>`keep 1.0 -- OS-9 freeware collection` |
| `kept` | list what has been taken, and how much it came to<br>`keep 1.0 -- OS-9 freeware collection` |
| `unkeep` | removes the files keep installed for a program, from its receipt in SYS/kept, leaving any whose checksum has changed -- so saves and scores stay. `kept' lists what is installed<br>`keep 1.0 -- OS-9 freeware collection` |

**Microware runtime**

| | |
|---|---|
| `cio` | Microware's C library trap module -- what every starred program here needs.  Included with Microware's permission; see SOURCES.txt.  You do not run it; it loads itself. |
| `csl` | Microware's C Shared Library, for programs built with Ultra C rather than cc 3.2 (68000) |
| `csl020` | Microware's C Shared Library, the 68020/030/040 build |
| `fpu` | Microware's floating-point emulation module: on a machine with no 68881/68882 it lets Ultra C floating-point code run. It belongs in your bootfile and your Init module's extension list, not loaded by hand. Its grant, DOC/fpu.doc, must stay with it |
| `math` | Microware's floating-point trap module (software) |
| `math881` | Microware's floating-point trap module for a 68881/68882 coprocessor.  Both register as the module `math'; load whichever suits your machine. |

**MM/1 drivers**

| | |
|---|---|
| `keydrv.mm1` | the MM/1's keyboard driver |
| `msdrv.901_340` | the MM/1's mouse driver |
| `msdrv_340.901.ms` | the MM/1's mouse driver, a second build of the same edition |
| `rb37c65` | the MM/1's floppy-disk driver, for its 37C65 controller |
| `scsi_mm1a` | the low-level SCSI routines the hard disk driver links to |
| `snddrv` | the MM/1's sound driver |
| `windio.52` | the MM/1's windowing terminal driver |

**OS-9 modules**

| | |
|---|---|
| `bootgen` | &#9733; makes or extends a device's boot file from the module files you name. -a appends to the existing boot instead of writing a new one; -b sets the copy buffer<br>`Syntax:   bootgen [<opts>] <device> {<path> [<opts>] }` |
| `bsplt68` | takes an OS9Boot file apart into the modules inside it, writing each one out under its own module name. A boot file is modules end to end, so `cat a b > OS9Boot' makes one you can try it on |
| `flink` | &#9733; makes a second directory entry for a file, an RBF hard link. RBF has no real hard links, and removing the entry can leave the original pointing at the wrong place: never run it on a disk you care about<br>**How:** never run this on a disk you care about, and never on a shipped module. It makes a directory entry aliasing the file's FD in whatever directory you are standing in; RBF has no hard links; and removing that entry leaves the original file pointing at a directory, after which `cat' answers `is a directory' for everything. It corrupted /dd/CMDS/cat that way once, and only rebuilding the image put it back. |
| `gen` | generates a skeleton C file -- header block, version lines and section comments -- and appends `.c' to the name: `gen -p frame' writes `frame.c'. `-m' makes a module frame, `-t' a type, `-f' a function declaration<br>`Syntax: gen [<opt>] <pathname> [<opts>]` |
| `mexist` | &#9733; answers whether a module is in the module directory by its exit status rather than by printing: 0 if it is there, 1 if it is not. The name is case-sensitive, and it looks at up to 256 modules<br>`MEXIST   Version UTIL 2.40 by DESIGNA VLT 24.11.97` |
| `os9lib` | the RTF/68K Fortran run-time library. rtf, for, lnk, biory and creadoc all link it, so `load' it into the module directory before running them. See DOC/README-FORTRAN |
| `ptxm` | Path Table eXtension Module: a kernel extension letting user-state processes open unlimited I/O paths.  It installs into the kernel and so needs supervisor state; ptxminst installs it.  Its manual is DOC/ptxm/ptxm.txt |
| `remove` | &#9733; remove modules from memory. `remove <module>...', -q for quiet. `rm' removes files<br>**How:** Removes modules from memory. `del', `rm' and `deldir' are the file ones. |
| `rtfdat` | the RTF Fortran data module |
| `unc` | disassemble a 68000 OS-9 module back to assembler: the header as equates, then the code, tracing which bytes are instructions and which are data, naming the OS-9 syscalls.<br>`Syntax: unc {-<opts>} <file> {-<opts>}` |
| `version` | &#9733; prints its own version and nothing else -- `Dies ist das Program 'version', Version 7' -- whatever module you name. `modinfo' shows a module's edition, and your own OS-9's `ident' reports what a module was built from |
| `vmod_trap` | the VMod_trap trap handler that rxmod and txmod call, a trap module rather than a program: `load CMDS/COMMS/vmod_trap' before running them. It runs in supervisor state, which os9exec cannot give it, so it cannot be tried under the emulator |

**Processes & memory**

| | |
|---|---|
| `aprocs` | &#9733; a process monitor: prints the active processes as a tree -- id, parent, priority, CPU time, age and share of the CPU -- and -m measures their activity over a few seconds.  `procs' and `top' are the other process listers<br>`Syntax: aprocs [<opts>]` |
| `edir` | &#9733; list the event directory -- OS-9 events and their values; `-e' is the long form, with the value and the increments. The print spooler makes one to look at: `lpsched /nil &' and `spoolqueue' is in the directory<br>`Syntax: edir [<opts>]` |
| `eset` | &#9733; set an OS-9 event to a value -- eset <event> <num><br>`Syntax: eset <event> <num> [<opts>]` |
| `eunlink` | &#9733; unlink an OS-9 event by name -- `eunlink <event>'. `edir' lists the events and `eset' sets one<br>`Syntax: eunlink {<event>}` |
| `launch` | &#9733; a login helper: reads SYS/config, sets the environment for your terminal type -- and optionally a default PATH and emacs bindings -- then starts the shell you name on its command line, with PORT naming your terminal's port<br>**How:** Says "nothing to launch" until it is configured -- see its documentation. |
| `loadmem` | copies a file into memory at a given address -- destination, upper limit and path, the addresses in hex; super user only. It says nothing when it works, so read the same address back with `savemem', which is its reverse<br>`Syntax   : LOADMEM <destinati address> <upper limit address> <path>` |
| `savemem` | writes memory to a file: from and to addresses in hex, inclusive (8000 8027 is 40 bytes), then a path that must not exist yet. Super-user only. `loadmem' is the reverse<br>`Syntax   : SAVEMEM <from address> <to address> <path>` |
| `signal` | &#9733; sends a signal to a process: `signal <pid> <code> [<seconds>]' waits that long first. Code 0 ends the process; an unused id answers 228. bash prints a background job's id in angle brackets. `snd_sig' signals several processes at once<br>`Syntax: signal <process-id> <signal-code> [<seconds>]` |
| `time` | times a program: it runs the command you give it and then prints how long that took -- real, user and system time. `time wc <file>'.  EFFO submission, revision 6 |
| `top` | show processes with their share of the CPU, refreshed every few seconds: `top' lists your own, `top -a' everyone's, and `top <seconds>' sets how often.  Interrupt to leave. `aprocs' is the other process lister here<br>`Syntax: top [<opts>] [<num>]` |
| `UAC_view` | reviews what a UAC system monitor recorded: sessions, the processes each ran, exceptions and I/O, page by page. Run `UAC_view -w=DATA' in the UAC directory with PORT naming your terminal; arrow keys choose, Q leaves<br>**How:** Full-screen, and it wants PORT set to your terminal (`/term'). From the UAC directory, `UAC_view -w=DATA' opens the session directory for the fifteen recorded sessions: arrow keys choose one, S opens it, D its process pages, Q goes back and quits. |
| `vis` | run a command over and over and refresh the screen with its output -- what `watch' does on other systems: `vis {opts} <command> <args>'.  Not the Unix `vis' that makes non-printing characters visible<br>`vis: illegal option -- ?` |
| `who` | lists the terminal and user of each shell running, from procs and SYS/password.  Written in Microware shell syntax |

**Scheduling**

| | |
|---|---|
| `cron` | run commands at specified times (daemon) |
| `crontab` | &#9733; lists, installs, edits and removes a user's crontab<br>`usage:  /dd/CMDS/SYSADMIN/crontab [-u<=>user] ...` |
| `every` | &#9733; runs a program over and over, waiting the given number of seconds between runs: `every 2 oskversion' prints the version every two seconds until you stop it. The program's own options follow its name<br>`Syntax: every <time> <progname> [<progopts>]` |
| `repeat` | repeat an OS-9 command N times -- `repeat 2 today' runs today twice.  It hands the command to $SHELL, which SYS/login sets to ksh, and ksh runs it<br>`repeat ver 1.2` |
| `vcron` | &#9733; the cron daemon: runs each user's crontab.  Only members of group Cron may start it; start it from startup with & |

**System state**

| | |
|---|---|
| `clock` | a full-screen clock in banner letters.  It runs `banner' through a module called `shell' -- your own OS-9 has one; load it first, or it stops waiting on its pipe.  Source in SRC/misc/clock.c |
| `cpucache` | &#9733; shows and switches the 68020/68030/68040 on-chip caches. Its driver is not here, so of what it does only `cpucache -q on\|off' works without one of your own<br>`Syntax: cpucache [on\|off]` |
| `getinfo` | shows the SysInfo table that setup builds: `getinfo' lists its locks, `getinfo -a' every entry, and -u releases a lock a program left behind<br>**How:** Shows the SysInfo table: bare it lists the locks, -a lists everything, -u <name> releases a lock. |
| `oskversion` | &#9733; reports the system: OS-9 level, version, revision and edition, and the CPU twice over -- what the init module claims and what the system globals say the processor really is, which are not always the same machine<br>`Syntax:   OSKversion` |
| `perr` | &#9733; print an OS-9 error message<br>`Syntax: perr [<error_codes>]` |
| `setime` | sets the system time from YYMMDDHHMMSS, typed at its prompt or given on the command line. Shares its name with a utility of your own -- README-NAMES |
| `setup` | builds TOP Munich's SysInfo table -- a resident data module of named settings and locks that MNews, nn and other TOP software read -- from SYS/sysinfo, or from the file named<br>**How:** Builds TOP's SysInfo table from SYS/sysinfo (or a file you name). Run it once before MNews or nn; `getinfo -a' shows the result. |

**Users and login**

| | |
|---|---|
| `adduser` | &#9733; adds a user to the system, or removes one with -r<br>`ADDUSER: add a user to or remove a user from the system` |
| `logon` | &#9733; logs a user in: checks the password file, sets the user, the environment and the motd; -l keeps SYS/wtmp<br>`Syntax: logon [<opts>] [<user>] [<password>]` |
| `mesg` | &#9733; sets your flags in SYS/utmp: a capital letter turns one on, a small one off.  M takes messages, V lets other users see you<br>`Syntax: mesg [-]flags` |
| `mmenu` | &#9733; a menu to give users instead of a shell, as on a BBS: menus, help and jumps read from files in its menu directory, with a log of what each user ran<br>`Syntax: mmenu <opts>` |
| `mmon` | a timesharing monitor for a terminal or Hayes-modem line: answers, sets the speed and runs logon, as configured in SYS/mmon.config<br>`Syntax: mmon [<opts>] [<line>] [<opts>]` |
| `msg` | &#9733; sends a line to a user who is logged in; mmenu runs it for you.  It prints no usage |
| `newgrp` | &#9733; changes your group, as SYS/group allows, asking for the group's password if it has one<br>`Syntax: newgrp [<gid>]` |
| `passwd` | changes your own password in SYS/password.  It matches on the user name, and the name must be spelt exactly as the password file has it, capitals included.  It rewrites the file with your own OS-9's `copy', through `shell'<br>`Syntax: passwd` |
| `speak` | &#9733; a chat between two logged-in users on a split screen; Ctrl-C or Ctrl-E leaves<br>`Syntax: speak <user>` |
| `timeout` | &#9733; logon's idle timer: it ends a user's session when the time SYS/password allows runs out; logon runs it |
| `uid` | &#9733; prints your user and group ids, or another user's from SYS/password: `uid tester'.  Its refusal is in German<br>`uid {<user-name>}` |
| `watch` | &#9733; watches a modem line for RING and starts a command on an incoming call.  Super-user only |

**Utilities**

| | |
|---|---|
| `argproc_demo` | demonstrates argproc(), a command-line parser, by printing what it made of its arguments. A switch takes its value with no space: `-x99', not `-x 99'. The library manual is DOC/argproc_demo/man.argproc<br>**How:** A switch takes its argument with no SPACE: `-x99', never `-x 99'. `argproc_demo readme' prints what it made of the line. |
| `bigsetter` | a demonstration of a Modula-2 library for sets larger than the language's own: it prints each step's sets and waits for a key |
| `bootlogger` | &#9733; writes the time the machine came up into SYS/bootlog, silently. Run by hand it stamps the log with the current time; read the log to see that it worked |
| `btop` | converts characters to bit patterns: `btop <file>' prints each character as a grid of O and a middle dot (byte $B7); ptob turns the grid back into bytes<br>`Syntax:   BtoP [<opts>] [<path1>] [<opts>] [<path2>] [<opts>]` |
| `chardef` | loads a character set into a VT220 terminal from a definition file: `chardef <file>'; it calls itself defchar<br>`Syntax: defchar [<path>]` |
| `clear` | &#9733; clears the screen, reading the escape sequence to do it from the termcap. `cls' beside it does the same job from a different author; either will do<br>`Syntax:   clear` |
| `combine` | &#9733; interleaves two files byte by byte, even bytes from one and odd from the other, to rebuild a 16-bit EPROM image from two 8-bit halves. The result has no permission bits; `attr' it before reading unless you are the super-user<br>`(c.) 1989 by F.R.Schmitt MPI Kernphysik Heidelberg` |
| `config` | reports this machine's C type properties as C comments -- sizes of char through double, how arithmetic rounds, and roughly how much memory malloc can give, found by filling memory |
| `cpu` | &#9733; a CPU speed test: it draws a bar chart of its timing loop and prints the clock rate it measured, then stops on a trap |
| `demerge` | splits a file of several OS-9 modules into one file per module, each named after its module. `cat a b > c' makes such a file. `modbuster' does the same and can write to another directory<br>**How:** OS-9's `merge' is concatenation, so `cat a b > c' makes the file demerge takes apart -- your own `merge' does the same. `dump' is the hex dump here. |
| `demo` | demonstrates egetopt, printing how it parsed its command line |
| `devprc` | shows which device each process holds a path to: -a walks every process and lists its open paths and the device behind each<br>`devprc: display device(s) belonging to process(es), V.1.01` |
| `dload` | &#9733; load a data file into a data module in memory: `dload <filename>' reports its size and where it went<br>`Syntax: dload <filename>` |
| `erradm` | starts, stops, flushes and prints errlog's log<br>`Syntax: erradm <opts>` |
| `errlog` | a daemon that collects error messages into one file, SYS/errorlog on /h0<br>`Syntax: errlog [<opts>]` |
| `fastcc` | &#9733; a second front end for Microware's cc: -p pipes the preprocessor into the compiler instead of using a temporary file, -r compiles to relocatables in a directory you name, -a stops at assembler, -bp shows each command. `-?' lists all<br>`fastcc: <opts> <files> <opts>` |
| `fixyear` | adds a century to file modification years below 70, as written by an RBF without the Y2K patch. Given a directory it fixes that directory's own date, not its files. -l logs changes, -q continues past errors, -z reads names from standard input (-z=<file> from a file)<br>`Usage: fixyear [-opt] <file\|dir> <dir\|file> [-opt]` |
| `fontgen` | generate a font for the Gepard display<br>**How:** Generates a character font for the Gepard display -- it prints the assembler source of an 80-column font on stdout. |
| `getsys` | &#9733; report the system's globals -- what OS-9 thinks it is running on<br>`Syntax: getsys [<opts>]` |
| `i_am_i` | a quine in Pascal: run it and it prints its own source, the loop at the end walking the table of lines that holds the program's text [no military use -- EFFO-INFO] |
| `makecrc` | writes C source for CRC tables: with no arguments it silently writes arc.c, binhex.c, ccitt.c, ccitt32.c, kermit.c and zip.c into the current directory, each a crctab[256] and updcrc(). For a file's CRC, use `chksum'<br>**How:** It generates C SOURCE and takes no arguments. Run it somewhere writable (`ksh -c "cd /dd/tmp; makecrc"') and it writes six files -- arc.c, binhex.c, ccitt.c, ccitt32.c, kermit.c, zip.c -- each a crctab[256] and an updcrc(). It writes them without a message, so list the directory afterwards. |
| `map` | &#9733; shows where a file sits on disk: `map <file>' prints its segment list, start sector and count in hex; `map -e <file>' adds owner, attributes, dates, link count and size. Years print as years since 1900: 126 is 2026<br>`Syntax: map [<opts>] <file> {<file>}` |
| `modinfo` | report a module's header -- name, type, size, edition, CRC<br>`module: Show Module Information` |
| `mvolformat` | format a multi-volume set<br>`Syntax: mvolformat drive volname volcount [format options]` |
| `phone` | connects two terminals over a communication path so you can type to somebody on another: `phone /t1' rings until answered; control-E leaves<br>`Syntax: phone <communication-path>` |
| `preset` | loads the terminal's function keys: it writes a fixed set of definitions -- `dir', `umacs', `r68', `l68', `dsave -ieb128k' and so on -- and answers `Funktionstasten belegt!'. German. It takes no arguments and ignores any given |
| `pri` | queues files for printing by running `copy -w=/r0/list' from /r0/cmds. Needs a RAM disk at /r0 holding your own OS-9's copy in /r0/cmds; without it, error 221 |
| `ptob` | convert bit patterns back to characters -- the other half of `btop', and the round trip is exact.<br>`Syntax:   PtoB [<opts>] [<path1>] [<opts>] [<path2>] [<opts>]` |
| `ptxminst` | installs Ptxm, the path-table kernel extension; load ptxm first |
| `rndir` | &#9733; renames the subdirectories of the current directory to upper case, or lower with `-l'; `-q' works silently.  It needs your own OS-9's dir, rename and del loaded<br>`Syntax: rndir [<opt>]` |
| `screen` | `screens': runs a random file from $HOME/.screens as a login greeting, through system(), so your OS-9's `shell' must be on your execution path. Not the terminal multiplexer. Source in SRC/screen, man page DOC/screen/screens.6 |
| `scsiutil` | talks to a SCSI device: inquiry, capacity, read sectors, eject, and audio CD control -- table of contents, play, volume<br>`SCSIutil V2.02 [Jan 28 1997 : 15:59:35] - written by Gary Duncan` |
| `setime2` | Y2K: set the system time with the year counted from 1900 -- `setime2 126 9 3 14 30 0' is 3 September 2026<br>`Syntax:    setime2 [<opt>] [<yyy mm dd hh mm ss [am/pm]>] [<opt>]` |
| `setyear` | sets the system year, and only the year -- `setyear 2026' -- leaving the month, day and time alone. It takes 1970 to 2050 and prints the date it ends up with<br>`Syntax:    setyear <YYYY>` |
| `snd_sig` | &#9733; sends a signal to one process or to several at once -- `snd_sig <pid> <pid>...' -- and with no option sends the wake signal; -<n> sends signal number n instead. `signal' beside it takes one process and can delay first<br>`Syntax:   snd_sig [-options] pid pid1...pidn` |
| `spline` | &#9733; a B-spline surface demonstration: draws a fixed 5x5 mesh and the surface fitted through it in Tektronix graphics codes, reads no input, and waits for a key at the end |
| `sqrtx` | a square-root demonstration: takes the root of each integer 1 to 25, squares it back, and prints the ones that miss and by how much -- the limit of double precision |
| `suspend` | &#9733; removes a process from the system -- its own usage line says so -- rather than suspending it; -s reaches system programs too<br>`SUSPEND V1.1 (C.) 1989 by F.R.Schmitt` |
| `t_trtest` | a test driver for a library's tree functions: each line you type is looked up, added or deleted, and `.' ends |
| `testibc` | IEEE-488 (GPIB) bus test: a menu of bus commands -- Ifc, Remote, Llo, local, Clear, Send, Enter, Dev-clear, Time, Quit -- for a GESPAC IEEE-488 card, which it needs. Its message file SYS/errmsg.ibc is not here |
| `transfer` | &#9733; copies files from GDOS disks to OS-9, and takes no options at all. For general device-to-device copies, `cp', `copy' and `dsave' do that<br>`Syntax: transfer` |
| `trunc` | &#9733; truncate a file to a given length<br>`OS-9/68k supplementary command.` |
| `tty` | &#9733; report the terminal's name |
| `unpacklib.os9` | unpack a library into its object modules: the archive's other build of unpacklib, which does the same<br>`unpacklib: Unimplemented option '-?'.` |
| `vecho` | System V `echo': the newline is suppressed by a trailing \c in the argument, not by default. `vecho one' writes `one' and a CR; `vecho one\c' writes `one' and stops. Several arguments are joined with a space. SRC/less_v177 |
| `vlen` | &#9733; a variable-length record demonstration: ignores arguments, creates a store, adds a hundred records and prints sizes and mapper entries. It leaves test.mp and test.st in the current directory; delete them to run it again<br>**How:** It leaves its store behind, in the data directory, as `test.mp' and `test.st'. Run it twice and the second run says `Filesystem already exists.' and adds nothing; delete those two to run it again. |
| `xlharc` | C-LHarc 1.00 in a third build: extracts and lists .lzh archives like `lharc'<br>`C-LHarc for OSK Version 1.00   (C) 1989-1990 Y.Tagawa` |
| `yagi` | a Yagi antenna calculator, DL6WU method: answer five questions -- frequency, element count, boom diameter, insulated Y/N, tubing size from its list -- and it prints element lengths and spacings. Run at a terminal: at end of input it repeats the last question for ever<br>**How:** It asks five questions on standard input -- centre frequency in MHz, element count, boom diameter, whether the elements are insulated from the boom (Y/N), and a tubing size off its own list of six. Answer four and it loops on the fifth forever, because EOF on a numeric read returns the same thing every time. |
| `ynad` | &#9733; YNAD -- Yet Another Name & Address program.  A contact database. |

**Vendor demos**

| | |
|---|---|
| `ob68kdemo` | OmniBasic 1.16, a BASIC compiler, demo build with a limited symbol table. Run it from a copy of DOC/omnibasic, which holds its library and examples; -c stops at the C it writes, and a full build needs your own OS-9's cc<br>**How:** OmniBasic 1.16, same arrangement as ub68kdemo and the same SHELL trick -- see its entry. Run it from /dd/DOC/omnibasic. DEMO VERSION, capped symbol table. |
| `sddemo` | White's Speedisk 2.10 -- disk defragmenter.  Wants an 80x24 screen; falls back to tty mode<br>**How:** White's Speedisk 2.10 de-fragmenter, demo build. Wants an 80x24 screen and drops to tty mode without one. |
| `ub68020demo` | UniBasic 1.10 for the 68020 -- the same demonstration as `ub68kdemo' and it runs the same way, announcing `OS9/68020 Version' where the other says 68000.<br>`UniBasic Version 1.10` |
| `ub68kdemo` | UniBasic 1.10 -- a BASIC compiler, demo build.  Run it from a copy of DOC/unibasic, where its library and examples are; -c stops at the C it writes, and a full build needs your own OS-9's cc<br>**How:** UniBasic 1.10, and it does compile -- the trick is that it runs its build through $SHELL. With SHELL unset it hunts for `/dd/bash' and dies with "Error Exit" and error 216. Do `setenv SHELL /dd/CMDS/sh', work in a directory holding basic.h and basic.l (DOC/unibasic has them), have your C toolchain reachable with CDEF and CLIB set, and give it memory. DEMO VERSION: the symbol table is capped, nothing else is. |

</details>

## Disk & DOS

*Reading and writing MS-DOS media with the mtools set.*

<details><summary>20 programs</summary>

| | |
|---|---|
| `msattrib` | mtools 3.6: reads or sets a DOS file's attribute bits -- +r and -r read-only, +a archive, +h hidden, +s system<br>`msattrib: illegal option -- ?` |
| `msbadblocks` | mtools 3.6: reads every used cluster of a DOS disk and marks the ones that fail as bad, so nothing is written there again |
| `mscd` | mtools 3.6: sets the current directory on a DOS disk for the other ms commands; run bare it reports where it is |
| `mscheck` | checks that a DOS disk reads cleanly: it lists the directory and reads every file in it.  A ksh script |
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
| `msread` | mtools 3.6: copies a file off a DOS disk -- mscopy under another name<br>`msread: illegal option -- ?` |
| `msren` | mtools 3.6: renames a file on a DOS disk<br>`msren: illegal option -- ?` |
| `mstoolstest` | mtools 3.6: prints mtools' resolved configuration -- the drives it knows and the image file behind each<br>**How:** Prints mtools' resolved configuration -- the drives it knows and the image file behind each one -- not a diagnostic test of anything. |
| `mstype` | mtools 3.6: prints a file that lives on a DOS disk<br>`mstype: illegal option -- ?` |
| `mswrite` | mtools 3.6: copies a file onto a DOS disk -- mscopy under another name; -t converts text line endings<br>`mswrite: illegal option -- ?` |
| `mtools` | the mtools 3.6 suite's own front end: run bare it lists its sub-commands.  Drives a: and b: are set up in SYS/mtools.conf, backed by the disk images in DOS<br>`Supported commands:` |

</details>

## Time & calendar

*Calendars, clocks and astronomy.*

<details><summary>18 programs</summary>

**Astronomy**

| | |
|---|---|
| `almanac` | computes where the Sun, Moon and planets are at a given date and time: right ascension, declination, apparent diameter and distance in AU; with your longitude and latitude, azimuth and altitude too. Its constants are for 1990, so accuracy falls off with distance from then<br>`Syntax of command:` |
| `ephem` | &#9733; an astronomical ephemeris: a live panel of the sun, moon and planets -- right ascension, declination, azimuth, altitude and more -- for the site and star database in SYS. RETURN passes the opening page, control-D quits<br>**How:** An astronomical ephemeris: `ephem -c /dd/SYS/ephem.cfg -d /dd/SYS/ephem.db'. RETURN passes the opening page; any key stops the loop; ? is help; control-D quits. |
| `ephem881` | &#9733; ephem built for a 68881 floating-point coprocessor: the same panel, and with hardware floating point the whole table fills in at once<br>**How:** The same as ephem, built for a 68881 coprocessor. Control-D quits. |
| `lunisolar` | &#9733; the phase of the moon in one line; given a year and a time zone it writes a whole lunisolar calendar as LaTeX instead<br>`Bad args: lunisolar -?` |
| `nasa` | &#9733; NASA orbital-element reader: reads NORAD two-line element sets from `nasa.dat' in the current directory and writes kepler.dat for orbit. No element set ships; supply a current one. The format is column-sensitive<br>**How:** Put NASA two-line elements in nasa.dat in the current directory and run `nasa'; it writes kepler.dat, which `orbit' reads. No element set ships; they are published for every satellite. |
| `orbit` | &#9733; the N3EMO satellite tracker 3.7: azimuth, elevation, doppler, range and mode hour by hour from a site. It reads kepler.dat, mode.dat and <site>.sit from the current directory, so run it in DOC/orbit (sites pgh, bern, zuerich). `nasa' makes kepler.dat<br>**How:** It reads kepler.dat, mode.dat and a <site>.sit by bare name from the current directory, and DOC/orbit holds them: `ksh -c "cd /dd/DOC/orbit; orbit"'. Answer d for a day's table, then the site (pgh), the date, the start hour, the step and the length. |

**Calendars**

| | |
|---|---|
| `cal` | &#9733; prints a month or a year's calendar. `cal -h' prints holidays with it -- SYS/holidays is here, and SYS/birthdays is an empty template for your own dates. SYS/cal.init is a printer setup for a laser<br>**How:** `cal -m=<month> -y=<year>', with flags. -h marks the holidays in SYS/holidays and anything you add to SYS/birthdays, which it includes. |
| `calcdate` | adds days to a date or counts the days between two: `calcdate 051788 -o 30' prints 061688; dates are mmddyy<br>**How:** Dates are six digits, mmddyy. `calcdate 051788 -o 30' prints the date 30 days on (061688), and a negative offset goes back; `calcdate 010188 -d 123188' prints the days from the first date to the second (365). Years are two digits. |
| `calen` | prints a month as a diary page, ruled for appointments, with the neighbouring months as small calendars in the corners. It reads the month, the year and how many months from its input: `echo 9 2026 1 \| calen'<br>`Invalid flag: -?` |
| `calender` | &#9733; prints a whole year's calendar, in German, with the German public holidays under it<br>**How:** A whole year at once, in German. It asks `Fuer welches Jahr?' (which year); RETURN at the question ends it. |
| `greg` | &#9733; converts a Julian day number to a Gregorian date: `greg 2461281' answers 2026 8 29<br>**How:** It converts a Julian day number to a Gregorian date and is nothing to do with regular expressions: `greg 2460000' answers `2023 2 25'. |
| `ticktalk` | tells the time in words -- `Quarter To Two pm' -- in English, French or Afrikaans; give an hour and minute, or none for now<br>**How:** `ticktalk' prints the time now in words; `ticktalk 13 45' prints a given time, Quarter To Two pm. -french and -afrikaans change the language, -before says Twenty To One rather than Twelve Forty, -approximate rounds to five minutes and -noampm drops am and pm. |
| `today` | the date, the time and the moon's phase, spelt out in words |
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

<details><summary>20 programs</summary>

**Calculators**

| | |
|---|---|
| `bc` | an arbitrary-precision calculator: `scale' sets the decimal places, so `2^200' and `scale=40; 1/7' come out exact. -l loads the maths library: sine, cosine, arctangent, logarithm, exponential<br>`bc 1.01 (Nov 25, 1991), Copyright (C) 1991 Free Software Foundation, Inc.` |
| `cam` | &#9733; camshaft design: asks the rocker ratio, the lift at each crank angle and the base circle, and plots an intake lobe's lift curve in Tektronix vectors. On a character terminal only the dialogue is readable |
| `chbase` | &#9733; converts a number from one base to another: `chbase 255 10 16' prints FF, and a target base of 0 prints every base from 2 to 36<br>`chbase   : OS9 Utility, created by Philip Maechler` |
| `cvtbase` | converts a number between bases.  The bases are named by key -- b, d, h or x, o -- or by their value, and the number comes on standard input: `echo 255 ! cvtbase d h' answers ff<br>**How:** The bases are the arguments and the numbers come on standard input, one per line: `cvtbase d h' then 255 answers ff; Escape ends it. Bases are named b, d, h or x, o -- or by their digit characters. |
| `dc` | &#9733; an integer desk calculator laid out like the Atari ST keypad, with five memories; `dc -b=h' (or d, o, b) sets the base. Its boxes use Cumana graphic characters: on other terminals set DCGRAPHIC to `++++\|-' first<br>**How:** A full-screen integer calculator. Set DCGRAPHIC=++++\|- first unless your terminal has the Atari ST's Cumana graphics, then type digits and operators; -b=h, d, o or b picks the base. Needs cio. |
| `factor` | prints the prime factors of each number it is given, or of each it reads, one to a line: `factor 1000001' |
| `hp` | a reverse Polish calculator in floating point: `hp 2 3 +' prints 5.000; on standard input p prints the top of the stack and P the rest; x multiplies and : raises to a power<br>**How:** A reverse Polish calculator in floating point. Given an expression on the command line it prints the result: `hp 2 3 +' prints 5.000 and `hp 2 10 :' 1024.000. Read from standard input it prints only when asked: p prints the top of the stack and P the values below it. + - / and % work as usual, x (or *) multiplies, : or ^ raises to a power, d drops the top value and D empties the stack; < = > & \| and ! compare and combine, leaving 1 or 0; q quits. Dividing by zero stops it. |
| `loan` | &#9733; amortisation calculator: principal, term, rate and start month in, the payment and a month-by-month schedule out<br>**How:** Answers four prompts and prints the schedule for the whole term; pipe it through head or less. |
| `number` | writes numbers out in English words: `number 1234567'<br>`usage: number # ...` |
| `primes` | lists the primes between two numbers: `primes 1 100' |
| `rechne` | &#9733; a German command-line calculator: each answer in decimal, hex and binary<br>**How:** One expression, no spaces: `rechne 4095+1'. Operators + - x / m a o p; $ff is hex; -b lists the set bits. The other -xx switches decode status codes of the maker's own equipment. |
| `rpn` | &#9733; a reverse-Polish calculator on whole numbers: numbers push; add, sub, mul, div, mod, and bitwise and, or, xor, not combine; pr prints, pop discards. Each line shows the top and depth; ? lists words, q leaves<br>**How:** Operators are words typed on their own line: 12, 34, add. A + sign is read as the number 0 and pushed. q leaves. |
| `sc` | sc -- spreadsheet calculator (needs TERM)<br>**How:** The spreadsheet, version 6.16. `sc' opens and says "Type '?' for help". It reads TERMCAP as SYS/login sets it, so no `. /dd/SYS/termcap.entry' is needed first. |
| `theorem` | solves y'=f(x,y) by Runge-Kutta, printing x and y each step: `theorem y 0 1 0.1 1' reaches 2.718280. `theorem -r 0 0 0 0' reverses standard input instead. An obfuscated-C contest entry<br>**How:** The 1990 contest's Best of Show, and it is four programs in one source. `theorem <expr> <x1> <x2> <h> <y1>' solves the differential equation y'=f(x,y) by Runge-Kutta over the interval, printing x and y a step at a time: `theorem y 0 1 0.1 1' reaches 2.718280, which is e. The expression may use x, y, + - * / and ^, evaluated strictly left to right with no brackets. `theorem -r 0 0 0 0' instead reverses the lines of standard input. Feeding its own source through those two modes is how the other two programs are made; see DOC/ioccc. |

**Science**

| | |
|---|---|
| `chemtab` | a periodic table database from the CRC Handbook: look up one element by name, number or symbol, select elements by up to three properties, mark them on the periodic table, or graph one property against another; full screen, menu keys<br>**How:** Full-screen. Space passes the title page; answer n (or y) to extra explanations and to keeping a transcript. On the main menu 1 looks up one element -- 3, then a symbol such as Fe and Return, shows its melting and boiling points, density, radius, electronegativity and discovery year; 2 selects elements by up to three properties, 3 lists them, 4 marks them on the periodic table, 5 graphs one property against another, 6 quits. Names are typed in lower case. The data is in LIB/chemtab and the manual pages in DOC/chemtab. |

**Simulators**

| | |
|---|---|
| `logisim` | logic circuit simulator: draws a pulse diagram, a row per node and a column per step, from a text circuit. Samples: DOC/logisim/counter.lsi and flipflop.lsi; notes in German in DOC/logisim/logisim.doc. Set PORT to your terminal first (`export PORT=/term' in bash); Esc stops<br>**How:** Set PORT first: `setenv PORT /term'. Without it, `logisim: Environment variable PORT not defined' -- it reopens the keyboard through that path. Two sample circuits ship in DOC/logisim (counter.lsi, flipflop.lsi) and its notes are there too, in German. |

**Spreadsheets**

| | |
|---|---|
| `checkfile` | &#9733; cheque-book register, full screen: A adds a record (date as YY/MM/DD, cheques as negative amounts), R lists with the balance, V edits, F picks the file, Q quits. Records go in testfile.dat in the current directory. Wants TERM<br>**How:** Full screen. A adds a record through a form, C accepts it, R lists the records with the balance, Q quits. Records go in testfile.dat in the current directory; cheques are entered as negative amounts. |
| `oleo` | GNU Oleo 1.6, a spreadsheet. It opens on its copyright notice and waits for a key before drawing the grid; ^H is its help character<br>**How:** GNU Oleo, a spreadsheet: it shows its notice, then the grid of cells.  Full-screen; it needs TERM, which SYS/login sets. |
| `scqref` | &#9733; quick reference for sc, the spreadsheet: a 360-line document that prints itself, in sections A to Q -- options, cursor movement, cell entry, files, ranges and the function lists. `scqref ! less' pages it<br>**How:** `scqref ! less' pages the reference; it is 360 lines. |
| `vc` | &#9733; a spreadsheet: `Welcome to the Spreadsheet Calculator, type ? for help', with rows, columns and a formula line |

</details>

## Printing

*Spoolers, page formatting and PostScript.*

<details><summary>11 programs</summary>

**PostScript**

| | |
|---|---|
| `gs33` | Ghostscript 3.33, the earlier build; gs403 is the later one<br>`Aladdin Ghostscript 3.33 (4/10/1995)` |
| `gs403` | Aladdin Ghostscript 4.03, full build: renders PostScript to the device you choose, or gives a `GS>' prompt with no file. Set GS_LIB to LIB/gs403, where its init files and fonts are<br>**How:** Aladdin Ghostscript 4.03. Point GS_LIB at its library first -- in bash that is `export GS_LIB=/dd/LIB/gs403`, not `setenv`, which is the OS-9 shell's command and gets "setenv: command not found" here. Then `gs403 -q -dNOPAUSE -sDEVICE=nullpage <file>.ps` reads the file and gives you its GS> prompt. Everything it needs, fonts included, is in that directory. gs403 is the complete build; gs33 is the older one. |
| `lwf` | ASCII to PostScript, like Unix enscript. Reads its prologue from USR/LIB/lwf.prologue<br>**How:** Turns plain text into PostScript, the way Unix enscript does. It reads /dd/USR/LIB/lwf.prologue and stops without it. No PostScript printer here, so send the output to a file and take it elsewhere. |

**Printers**

| | |
|---|---|
| `alps` | &#9733; switch an ALPS ASP-1000 printer between draft and NLQ<br>`Syntax: alps [<opts>] >/<device>` |
| `epson` | &#9733; sets an Epson printer up and copies text to it: characters per inch, character set and a form feed, as control codes ahead of the text.  It came with a spline package, to print its plots<br>`usage: epson [<opts>]` |
| `lmargin` | &#9733; indents text by a left margin: it reads standard input and writes it out again with the margin you ask for -- `lmargin -l4 <file'. See also `fmt', `proff' and `pep'<br>`usage: epson [<opts>]` |

**Spooling**

| | |
|---|---|
| `lp` | &#9733; submits a file to the lp print spooler: -n=xx makes copies, -d=ptr picks the printer, -m mails you when it is done<br>`Syntax: lp [<opts>] {<path>}` |
| `lpq` | shows the spooler queue. It looks for a data module called `spoolqueue' in memory; with a spooler running it reports the queue, and without one answers `no spooler installed'. Same for `prjob' and `lp'.<br>`Syntax: lpq [-p=dev] [user]` |
| `lprm` | &#9733; removes a job from the printer spooler's queue by number; `-' removes every one, and -d=<dev> picks the queue of another printer<br>`Syntax: lprm [-d=dev] [-] job..` |
| `lpshut` | &#9733; shut down the printer scheduler<br>`Syntax: lpshut` |
| `prjob` | &#9733; prints a queued job from the lp spooler; with no spooler installed it says so |

</details>

## Documentation

*Pagers, readers and the help system.*

<details><summary>8 programs</summary>

| | |
|---|---|
| `help` | help system: `help <topic>' pages the topic from a .hlp file in SYS/HELP and offers subtopics; `help help' explains. In bash, `enable -n help' first, or bash's own help answers. Shares its name with a utility of your own -- README-NAMES [no military use -- EFFO-INFO]<br>**How:** `help dinfo'. At bash type `enable -n help' first, or bash's own help builtin answers instead. |
| `helpindex` | &#9733; builds the .ndx index a .hlp help file needs: `helpindex dinfo.hlp' writes dinfo.ndx beside it<br>**How:** `helpindex dinfo.hlp' writes dinfo.ndx beside it. Only names ending .hlp or .hlib are accepted unless -a is given; with no name it asks for one. |
| `less` | a pager you can move about in: space or f next screen, b back, / search, n next match, h help, q quit. Reads the terminal's size and codes from TERM and TERMCAP |
| `lessecho` | &#9733; prints its arguments back quoted for a shell -- the helper less uses to hand file names on<br>`usage: lessecho [-ox] [-cx] [-pn] [-dn] [-a] file ...` |
| `lesskey` | turns a key-binding file into the binary less reads: a `#command' section, then one key and one command per line<br>`usage: lesskey [-o output] [input]` |
| `man` | reads this disk's manual pages: `man md5' formats DOC/md5/md5.1 with nroff and pages it with less. `man -k <word>' searches names, `man -w <name>' says where a page is. Index: DOC/MANPAGES. A shell script<br>`man -- the librarian for this disk` |
| `more` | a plain pager, 24 lines a screen, Enter for the next; the 24 is fixed. It reads Enter from standard input, so fed from a pipe it never waits and loses a line at each prompt |
| `mwb` | &#9733; writes and edits manual entries in the proff format TOP's manuals use, kept under USR/DOC/.MAN on /h0<br>`Syntax: mwb {<opts>}` |

</details>

## G-Windows

*Programs for G-Windows, OS-9's graphical display.  There is none here, so each card shows the program saying so.*

<details><summary>6 programs</summary>

| | |
|---|---|
| `colortest` | &#9733; reports how G-Windows has its colour look-up table set up. At a terminal it says so and stops -- it wants the /win device, which is the G-Windows display<br>`colortest` |
| `cyberwar` | &#9733; CyberWar -- a game that needs G-Windows |
| `dclock` | &#9733; a digital clock for G-Windows<br>`dclock - digital clock for G-windows` |
| `lfmaker` | makes a G-Windows launch file.  Before anything else it asks its terminal for a G-Windows setstat, so run it on a G-Windows screen; on a terminal without one it is told E$UnkSvc and stops there in silence, with status 208 |
| `puzzle` | &#9733; sliding-tile puzzle for G-Windows -- it draws through G-Windows, so at a terminal it prints nothing and returns. It is here for a real OS-9 workstation that has G-Windows |
| `scriptmaster` | &#9733; G-Windows scripting tool |

</details>

## Needs hardware

*Programs for hardware out of our reach: a GEPARD or MM/1 display, a printer on its own port.  Untested here; what is said of them comes from their own text and code.*

<details><summary>16 programs</summary>

**<a sub-category for machine-specific tools>**

| | |
|---|---|
| `what` | lists the expansion cards in a GEPARD, a German 68k machine: I/O address, reference byte and card name. Elsewhere the table is empty; it ignores arguments. Shares its name with a utility of your own -- README-NAMES<br>**How:** An inventory tool for the GEPARD, the German 68k machine: it prints "What's where in the GEPARD:" and a table of expansion cards. On other hardware the table is empty, and it ignores its arguments. |

**Display**

| | |
|---|---|
| `apfel` | the Mandelbrot set (Apfelmaennchen) drawn on the Atari Graph display; it calls the `graph' trap library |
| `g` | &#9733; an Atari Graph demonstration, paired with striche. It calls the `graph' trap library, so load that first; it then aborts on a supervisor-only instruction, having been written to run in supervisor state |
| `graphdemo` | a demonstration of the Atari Graph display; it calls the `graph' trap library |
| `graphsave` | save an Atari Graph screen.  Aborts with the `graph' trap library resident, like `showpic': it wants the display |
| `setbgptn` | &#9733; sets the window system's background pattern from a file |
| `showpic` | show a picture on the Atari Graph display.  With the `graph' trap library resident it is entered and aborts: it wants the display, not just the library. |
| `sine` | a sine plot on the Atari Graph display; it calls the `graph' trap library |
| `striche` | &#9733; line drawing for the Atari Graph display; it calls the `graph' trap library, so load that first |
| `tplot` | &#9733; plots data with the Atari ST's A-line graphics: asks the x and y intervals and divisions, then draws. On a character terminal it aborts where drawing would begin, after the questions<br>`Usage : hiplot <-opt1> .. <-optn> <file1> .. <filen>` |
| `umusek` | UMusEK -- a music editor.  It needs a hardware graphics screen: point it at one and it opens.  Without a graphics screen it stops with `***DS_ScAdd Error 208.' and `Fran: Can't get screen addr, 'bye!'. |
| `x9eyes` | &#9733; xeyes for the personal window, resizable |

**Printers**

| | |
|---|---|
| `lpsched` | &#9733; starts the lp print spooler on a printer device; -r restarts it<br>`Syntax: lpsched [-r] {<devname>}` |
| `splman` | &#9733; OS-9 print spooler: the manager.  It wants a printer on an SCF device to spool to.  `splprt' is the process that drives the printer and `splstat' shows the queue; the three go together |
| `splprt` | &#9733; OS-9 print spooler: the printer process, one per printer. It wants an SCF device to write to |
| `splstat` | &#9733; OS-9 print spooler: reports the queue in SPL/splq as a table of jobs and a table of printers; with nothing queued it prints nothing. splman and splprt are the rest of the set |

</details>

<details>
<summary><b>Not included</b> &middot; 142</summary>

Programs that were found in the archives and left out on purpose, each with the reason and where it came from, so you can go and look for yourself.  None of them is on the disk.

| | | |
|---|---|---|
| `add_errmsg` | Builds the message file used by the forum 13 vi.<br>**Why not:** A helper of the forum 13 vi, and left out with it on the same terms. | EFFO forum disk 13, SOFTWARE/C/VI |
| `adven2` | An adventure game written in Fortran.<br>**Why not:** It needs a Fortran compiler and linker that work end to end, and the RTF Fortran here only partly does. | comp.sources.games volume 11 |
| `bawk` | An awk-like pattern language.<br>**Why not:** gawk and a2p on this disk do the job. | Microware OS-9 archive, 6809 C section |
| `bday` | Mails birthday greetings from a list kept by the administrator.<br>**Why not:** An administrator's tool that sends through sendmail from Unix system lists. | comp.sources.misc v06i099 |
| `belief` | A text filter from the silly collection.<br>**Why not:** Left out on content. | alt.sources, December 1992, silly.tar |
| `biffa` | A text filter from the silly collection.<br>**Why not:** Left out on content. | alt.sources, December 1992, silly.tar |
| `btree` | Softfocus BTREE, a B-tree file-handling demonstration and test.<br>**Why not:** The forum disk lists it as public domain, but its own btree.doc says it no longer is and is sold. | EFFO forum disk 2 |
| `calendar (Minow)` | Martin Minow's calendar reminder program.<br>**Why not:** cal, calen and calender on this disk cover it. | comp.sources.unix volume 3 |
| `cbmtopbm` | Converts a compact bitmap to PBM; one of the early pbmexec tools.<br>**Why not:** It rejects PBM files, plain and raw, that netpbm on this disk reads and writes correctly, so it works with nothing here. | Microware OS-9 archive, GRAPHICS/pbmexec.lzh |
| `cdungeon` | Dungeon, the DECUS mainframe adventure that preceded Zork, ported to C.<br>**Why not:** The game is Infocom's work, now another company's, and its notice prohibits commercial use; a question of rights this collection cannot settle. | comp.sources.games v12i068 |
| `cent` | Centipede for terminals.<br>**Why not:** The posting carries a random-number file under a bare copyright with no grant. | comp.sources.games v01i071 |
| `center` | Centres lines of text.<br>**Why not:** Its terms ask that the author be contacted for redistribution rights or inclusion in a package. | comp.sources.misc v27i070 |
| `checksoa` | Checks a domain's SOA records across its name servers.<br>**Why not:** It is example code from a published book with no grant to redistribute it. nslookup and nsquery from the same port ship. | Microware OS-9 archive, OSK_NETWORK_ISP/bind.4.8.3.lzh |
| `chop` | Cuts fields and columns out of lines.<br>**Why not:** cut, colrm and field on this disk do the job. | comp.sources.unix v25i001 |
| `ci` | RCS 4 check-in: records a new revision of a file.<br>**Why not:** The distribution's own READ_ME is a non-disclosure form forbidding distribution in any form without the author's written permission. RCS 5 and later are GNU-licensed. | Microware OS-9 archive, CMDS/rcs4.lha |
| `cmake` | Carl Kreider's crude make.<br>**Why not:** Its author describes it himself as crude and obsolete. make and gmake are on this disk. | Microware OS-9 archive, CMDS/carlutil.lzh |
| `co` | RCS 4 check-out: retrieves a revision of a file.<br>**Why not:** The distribution's own READ_ME is a non-disclosure form forbidding distribution in any form without the author's written permission. RCS 5 and later are GNU-licensed. | Microware OS-9 archive, CMDS/rcs4.lha |
| `colm` | Sets a list out in columns.<br>**Why not:** column on this disk does the job. | comp.sources.unix v16i087 |
| `CommonTeX` | Pat Monardo's CommonTeX, TeX in C, as source.<br>**Why not:** It is not the source of the TeX on this disk, and a second TeX adds nothing. | Microware OS-9 archive, osk_ctexsrc.ar |
| `dearc` | Extracts an MS-DOS .ARC archive.<br>**Why not:** It cannot read a crunched member, which nearly every real archive holds. arc on this disk reads them all. | Microware OS-9 archive, CMDS/carlutil.lzh |
| `dg` | An entry in the 1990 International Obfuscated C Code Contest.<br>**Why not:** It depends on the preprocessor expanding the name of a directive, which standard C does not do, and neither preprocessor here builds it. | EFFO forum disk 16, SOFTWARE/C/7TH_C_CONTEST |
| `dialog` | Draws dialog boxes for shell scripts.<br>**Why not:** It draws with curses line-drawing characters and colour, which no curses library here provides. | comp.sources.misc v41i109 |
| `dinkum2` | Dinkum, an Australian text adventure.<br>**Why not:** Its author's rule allows no modified versions to be released, and an OS-9 build is one. | comp.sources.games v15i036 |
| `diph` | The game of dining philosophers.<br>**Why not:** It is built on sockets, fork and select, which this C library does not have. | comp.sources.games v13i026 |
| `dots2` | A visual dots-and-crosses game.<br>**Why not:** It is built on sockets, fork and select, which this C library does not have. | comp.sources.games v02i051 |
| `dsw` | A utility from the OS-9 International magazine disk.<br>**Why not:** All rights reserved by its publisher and author, with the forum's personal-use-only condition. | OS-9 International code disk, via EFFO |
| `dumpinit` | Lists the settings of the init module.<br>**Why not:** It will not compile: six of the init module fields it prints do not exist in this SDK's header. | Microware OS-9 archive, file 2240 |
| `dynacon` | Converts CoCo Dynacalc spreadsheet files.<br>**Why not:** It came with a 6809 makefile only and is Color Computer business. | comp.os.os9, June 1989 |
| `e` | A small fixed VT100 build of the SEDT screen editor.<br>**Why not:** Its terms make it available to customers and for internal use on condition that no modifications are made, and an OS-9 build is a modified copy. | EFFO forum disk 11, SOFTWARE/C/SEDT_EDITOR |
| `errno` | Explains an error number.<br>**Why not:** perr on this disk does the job. | TOP release 2 (The OS-9 Project, Munich), top.tar.Z |
| `expreserve` | Saves the buffer of the forum 13 vi when the editor dies.<br>**Why not:** A helper of the forum 13 vi, and left out with it on the same terms. | EFFO forum disk 13, SOFTWARE/C/VI |
| `exrecover` | Restores a buffer that expreserve saved for the forum 13 vi.<br>**Why not:** A helper of the forum 13 vi, and left out with it on the same terms. | EFFO forum disk 13, SOFTWARE/C/VI |
| `ffix` | Expands tabs and turns other control characters into spaces.<br>**Why not:** detab, expand, pep and unp on this disk do the job; its in-place rewrite needs a module this disk does not have. | OS-9 Public Domain Utilities image, FFIX |
| `flicker` | An ANSI terminal teaser that inserts and deletes lines for ever.<br>**Why not:** It runs until interrupted and does not restore the terminal afterwards. | comp.sources.games v05i060 |
| `funky` | A text filter from the silly collection.<br>**Why not:** Left out on content. | alt.sources, December 1992, silly.tar |
| `gnuplot_x11` | The X11 output driver for gnuplot 3.2.<br>**Why not:** It draws only on an X11 display, and its archive holds no gnuplot binary for it to serve. | Microware OS-9 archive, GRAPHICS/gnuplot32x.tar.Z |
| `greed` | A field of digits: move to eat that many digits in a direction, until no move is left.<br>**Why not:** Its author asked that it not be redistributed. | Usenet posting, 1989; v_misc.ar on the hc disk |
| `halign` | Aligns columns of text.<br>**Why not:** column on this disk does the job. | comp.sources.unix v06i016 |
| `hd` | A hex dump.<br>**Why not:** dump, hdump and xd on this disk do the job. | TOP release 2 (The OS-9 Project, Munich), top.tar.Z |
| `hearts` | A multiplayer card game of hearts.<br>**Why not:** It is built on sockets, fork and select, which this C library does not have. | comp.sources.games v02i082 |
| `icapos9` | Support programs for the Imagewise frame grabber.<br>**Why not:** It needs the frame-grabber hardware. | comp.os.os9, May 1989 |
| `isam` | Softfocus ISAM, an indexed-sequential file demonstration.<br>**Why not:** The forum disk lists it as public domain, but its own documentation says it no longer is and is sold. | EFFO forum disk 2 |
| `jive` | A text filter that rewrites English in a comic dialect.<br>**Why not:** Left out on content. valspeak, from the same posting, ships. | comp.sources.games v01i003 |
| `jroff` | A text filter from the silly collection.<br>**Why not:** Left out on content. | alt.sources, December 1992, silly.tar |
| `kings` | Kings, a card-placing patience game for the MM/1 under K-Windows.<br>**Why not:** The only copy's binary fails its own module check, so OS-9 will not load it, and its source would need porting work to rebuild. | Microware OS-9 archive, file 2191 |
| `kraut` | A text filter from the silly collection.<br>**Why not:** Left out on content. | alt.sources, December 1992, silly.tar |
| `kutil` | Reads and writes the kernel track of CoCo floppies and Burke and Burke hard drives.<br>**Why not:** It is for Color Computer disks and hardware. | Microware OS-9 archive, 6809 C section |
| `lfcr` | Converts line endings.<br>**Why not:** autolf on this disk does the job. | TOP release 2 (The OS-9 Project, Munich), top.tar.Z |
| `link` | Makes a hard link by writing a directory entry to the raw disk.<br>**Why not:** RBF has no hard links; a program that made one this way corrupted this disk. Its author warns to use it at your own risk. | comp.os.os9, January 1989 |
| `linkup` | LinkUp, a K-Windows communications suite with ansishow, audioplay, gport and terminal.<br>**Why not:** The clients need a K-Windows display, and its installer writes over the root disk. | Microware OS-9 archive, KWIN_LinkUp_1_0.lzh |
| `ln` | Makes a hard link by writing a directory entry to the raw disk.<br>**Why not:** RBF has no hard links; a program that made one this way corrupted this disk. Its author warns to use it at your own risk. | comp.os.os9, January 1989 |
| `loglist` | A 1988 utility that lists the system's log file.<br>**Why not:** No source, no documentation and no terms anywhere. | EFFO public-domain disk 1 |
| `lpunch` | Converts punched-card deck records.<br>**Why not:** There is nothing here to use them with. | Microware OS-9 archive, 6809 C section |
| `malawi` | A two-player board game.<br>**Why not:** It is written for X11 only. | comp.sources.games v17i074 |
| `marquis` | Scrolls a message along a terminal's status line from the background.<br>**Why not:** No terminal in the disk's termcap has a status line, and it will not start without one. | comp.sources.misc v07i089 |
| `mb` | A text filter from the silly collection.<br>**Why not:** Left out on content. | alt.sources, December 1992, silly.tar |
| `mb (banner)` | Prints large banners from an external font.<br>**Why not:** The author ships no font, so it would arrive unable to print anything. | comp.sources.unix v26i141, banners collection |
| `molecule` | A simple two-dimensional particle system of animated atoms.<br>**Why not:** Its output is binary coordinates for a display program built on a frame-buffer library with no counterpart here. | comp.sources.misc v02i092 |
| `morsecode` | Converts text to Morse code.<br>**Why not:** It is written in lex and Pascal, and morse on this disk does the job. | comp.sources.unix v17i081 |
| `new_e` | A build of the SEDT screen editor that reads TERM to choose its terminal setup.<br>**Why not:** Its terms make it available to customers and for internal use on condition that no modifications are made, and an OS-9 build is a modified copy. | EFFO forum disk 11, SOFTWARE/C/SEDT_EDITOR |
| `newspeak` | A text filter from the silly collection.<br>**Why not:** Left out on content. | alt.sources, December 1992, silly.tar |
| `nist` | Sets the clock by dialling the NIST time service through a modem.<br>**Why not:** It needs a modem and the dial-up service. | Microware OS-9 archive, 6809 C section |
| `notes` | The Notesfile conferencing system (UIUC's notes) in reccoware's 1988 OS-9 port: notes, mknf, nfpipe, nfstats and a dozen more.<br>**Why not:** A multi-user conferencing system that needs its own system users and spool set up, under a copyright notice with no grant and no source. | TOP release 2 (The OS-9 Project, Munich) |
| `ntp` | NETTIME, a client for the network time protocol.<br>**Why not:** No terms anywhere in the archive, and it links a Microware networking library. msntp on this disk does the job. | Microware OS-9 archive, osk_ntp.tar.gz |
| `ocompress` | A port of compress.<br>**Why not:** compress and compr on this disk do the job. | Microware OS-9 archive |
| `omega` | Omega 0.71 beta, a large roguelike, in an OS-9 build.<br>**Why not:** Its licence does not allow distributing modified versions without the author's consent. An OS-9 build is a modified copy, and no source came with it. | TOP release 2 (The OS-9 Project, Munich), top.tar.Z |
| `os9lader` | The OS-9 loader for F68K, a Forth system.<br>**Why not:** The archive's OS-9 part is only this loader, and forth is already on this disk. | Microware OS-9 archive, LANGUAGES/f68k.tar.Z |
| `osktag` | OSKTag, a taglines tool for mail and news.<br>**Why not:** No author, copyright or grant is named anywhere in it, and it is written for K-Windows. | Microware OS-9 archive, TELECOM/OSKTag_2_01.lzh |
| `oxm` | A mail front end.<br>**Why not:** elm, mail and mailx on this disk do the same job. | TOP release 2 (The OS-9 Project, Munich), top.tar.Z |
| `pac` | A full-screen calculator built as a front end to bc.<br>**Why not:** It does its arithmetic by forking bc and talking over a two-way pipe, which this C library cannot do. bc, dc and hp are on this disk. | comp.sources.misc v14i039 |
| `pbmcatlr` | Joins PBM images left to right; one of the early pbmexec tools.<br>**Why not:** It rejects PBM files, plain and raw, that netpbm on this disk reads and writes correctly. pnmcat does the job here. | Microware OS-9 archive, GRAPHICS/pbmexec.lzh |
| `pbmcattb` | Joins PBM images top to bottom; one of the early pbmexec tools.<br>**Why not:** It rejects PBM files, plain and raw, that netpbm on this disk reads and writes correctly. pnmcat does the job here. | Microware OS-9 archive, GRAPHICS/pbmexec.lzh |
| `pbmcrop` | Crops the blank edges off a PBM image; one of the early pbmexec tools.<br>**Why not:** It rejects PBM files, plain and raw, that netpbm on this disk reads and writes correctly. pnmcrop does the job here. | Microware OS-9 archive, GRAPHICS/pbmexec.lzh |
| `pbmcut` | Cuts a rectangle out of a PBM image; one of the early pbmexec tools.<br>**Why not:** It rejects PBM files, plain and raw, that netpbm on this disk reads and writes correctly. pnmcut does the job here. | Microware OS-9 archive, GRAPHICS/pbmexec.lzh |
| `pbmenlarge` | Enlarges a PBM image; one of the early pbmexec tools.<br>**Why not:** It rejects PBM files, plain and raw, that netpbm on this disk reads and writes correctly. pnmenlarge does the job here. | Microware OS-9 archive, GRAPHICS/pbmexec.lzh |
| `pbmfliplr` | Flips a PBM image left to right; one of the early pbmexec tools.<br>**Why not:** It rejects PBM files, plain and raw, that netpbm on this disk reads and writes correctly. pnmflip does the job here. | Microware OS-9 archive, GRAPHICS/pbmexec.lzh |
| `pbmfliptb` | Flips a PBM image top to bottom; one of the early pbmexec tools.<br>**Why not:** It rejects PBM files, plain and raw, that netpbm on this disk reads and writes correctly. pnmflip does the job here. | Microware OS-9 archive, GRAPHICS/pbmexec.lzh |
| `pbminvert` | Inverts a PBM image; one of the early pbmexec tools.<br>**Why not:** It rejects PBM files, plain and raw, that netpbm on this disk reads and writes correctly. pnminvert does the job here. | Microware OS-9 archive, GRAPHICS/pbmexec.lzh |
| `pbmpaste` | Pastes one PBM image onto another; one of the early pbmexec tools.<br>**Why not:** It rejects PBM files, plain and raw, that netpbm on this disk reads and writes correctly. pnmpaste does the job here. | Microware OS-9 archive, GRAPHICS/pbmexec.lzh |
| `pbmtocbm` | Converts PBM to a compact bitmap; one of the early pbmexec tools.<br>**Why not:** It rejects PBM files, plain and raw, that netpbm on this disk reads and writes correctly, so it works with nothing here. | Microware OS-9 archive, GRAPHICS/pbmexec.lzh |
| `pbmtops` | Converts PBM to PostScript; one of the early pbmexec tools.<br>**Why not:** It rejects PBM files, plain and raw, that netpbm on this disk reads and writes correctly. pnmtops does the job here. | Microware OS-9 archive, GRAPHICS/pbmexec.lzh |
| `pc2os9` | Converts MS-DOS text files to OS-9's: line ends, tabs expanded, names lower-cased; public domain, 1992.<br>**Why not:** toos9 on this disk does the same job. | Microware OS-9 archive, OS9000 tree, pc2os9.ar |
| `peruse` | Peruse 2.0, a file browser.<br>**Why not:** It needs a CoCo driver, and its author allows personal use only. | Microware OS-9 archive, 6809 C section |
| `piped-cc` | Replaces the 6809 C compiler's first pass with pipes.<br>**Why not:** It is for the 6809 compiler only. | comp.os.os9, 1987 |
| `pjr` | An entry in the 1990 International Obfuscated C Code Contest.<br>**Why not:** The preprocessor here aborts while reading it, as the entry's own hint warns compilers may. | EFFO forum disk 16, SOFTWARE/C/7TH_C_CONTEST |
| `plasma` | The Shifty Death Effect, an ASCII plasma drawn with VT100 cursor moves.<br>**Why not:** It runs until interrupted, for the same reason as flicker; its own usage text calls it a joke. | alt.sources, February 1993 |
| `puz15` | Another build of the fifteen puzzle by the same author.<br>**Why not:** Its author allows unmodified copies only, and an OS-9 build is a modified copy. | v_misc.ar on the hc disk |
| `puzzle15` | The 15-puzzle: slide the tiles into the gap.<br>**Why not:** Its author allows unmodified copies only, and an OS-9 build is a modified copy. | EFFO forum disk 16 |
| `PwDialog` | Dialog boxes for the X68000's PW/X window system.<br>**Why not:** It needs the PW/X window device on a Sharp X68000. | Microware OS-9 archive |
| `qr.cgi` | A CGI query sample for the WN web server.<br>**Why not:** All rights reserved, and built against a library whose source and terms are not in the archive. The other WN CGI samples ship. | Microware OS-9 archive, TELECOM/wn2.zip |
| `qterm` | Asks the terminal what it is and reports the answer.<br>**Why not:** The answer comes from whatever terminal the reader uses, not from anything on this disk, and SYS/login already sets TERM and TERMCAP. | comp.sources.unix v10i072 |
| `rain (1994)` | G. L. Sicherman's rain: drops fall and pool.<br>**Why not:** This disk already ships a rain screen toy that differs only in the drop pattern. | comp.sources.unix v28i090 |
| `raypaint` | A graphics program, source only.<br>**Why not:** It is written for X11 and GL. | Microware OS-9 archive |
| `rcis` | RCIS 2.3, a multi-user dial-up BBS for OS-9/68000 K-Windows.<br>**Why not:** Its licence grants the purchaser one copy only, and it is a demonstration version that needs a registration file. | Microware OS-9 archive, TELECOM/rn.tar.Z |
| `rcs` | RCS 4's administration command: sets locks, access lists and file attributes.<br>**Why not:** The distribution's own READ_ME is a non-disclosure form forbidding distribution in any form without the author's written permission. RCS 5 and later are GNU-licensed. | Microware OS-9 archive, CMDS/rcs4.lha |
| `rcsdiff` | RCS 4: compares revisions of a file.<br>**Why not:** The distribution's own READ_ME is a non-disclosure form forbidding distribution in any form without the author's written permission. RCS 5 and later are GNU-licensed. | Microware OS-9 archive, CMDS/rcs4.lha |
| `rcsident` | RCS 4: finds the identification keywords in a file.<br>**Why not:** The distribution's own READ_ME is a non-disclosure form forbidding distribution in any form without the author's written permission. RCS 5 and later are GNU-licensed. | Microware OS-9 archive, CMDS/rcs4.lha |
| `rcsmerge` | RCS 4: merges changes between revisions.<br>**Why not:** The distribution's own READ_ME is a non-disclosure form forbidding distribution in any form without the author's written permission. RCS 5 and later are GNU-licensed. | Microware OS-9 archive, CMDS/rcs4.lha |
| `rdate` | Sets the clock from an RFC 868 time server.<br>**Why not:** Source only, and it needs the networking headers of Microware's ISP 1.x, which the SDK here lacks. | Microware OS-9 archive, network section |
| `read_mail` | Mail helper that goes with the forum 13 vi.<br>**Why not:** A helper of the forum 13 vi, and left out with it on the same terms. | EFFO forum disk 13, SOFTWARE/C/VI |
| `revcat` | Prints a file's lines in reverse order.<br>**Why not:** tac on this disk does the job. | Usenet posting |
| `revcat_db` | Prints a file backwards.<br>**Why not:** tac on this disk does the job. | comp.sources.misc v10i061 |
| `RGTool` | A program for the X68000's PW/X window system.<br>**Why not:** It needs the PW/X window device on a Sharp X68000. | Microware OS-9 archive |
| `rise_set` | Computes the rising and setting of the Sun and Moon.<br>**Why not:** It computes for one observer, fixed in the source, and needs ftime and atan2, which this C library lacks. | comp.sources.unix volume 5 |
| `rlog` | RCS 4: prints the log and history of an RCS file.<br>**Why not:** The distribution's own READ_ME is a non-disclosure form forbidding distribution in any form without the author's written permission. RCS 5 and later are GNU-licensed. | Microware OS-9 archive, CMDS/rcs4.lha |
| `robots2` | A robots game with a hall of fame, different from the robots on this disk.<br>**Why not:** It stops when it reads its terminal description: a copy loop in the program runs past the end of the string. | TOP release 2 (The OS-9 Project, Munich), top.tar.Z |
| `rock` | A spew grammar, madrock.sp, from the silly collection.<br>**Why not:** Left out on content. | alt.sources, December 1992, silly.tar |
| `rstory2` | Asks your name and favourite things and tells a story about you.<br>**Why not:** It starts four story programs that were never distributed and cannot be rebuilt. | EFFO forum disk 9, PROGRAMME/C/SNOBOL |
| `rz` | ZMODEM receive, from Omen Technology.<br>**Why not:** A commercial program: the archive carries its licence order form, priced per user. k, xy and z on this disk are free X/Y/ZMODEM. | Microware OS-9 archive, APPS/rzsz_3_36_3_OSK.lzh |
| `scamper` | A cellular automata simulator.<br>**Why not:** It is written for X11 only. | comp.sources.misc v26i024 |
| `sedt` | SEDT 2.6, Anker Berg-Sonne's DEC-style keypad screen editor, in its VT100 build.<br>**Why not:** Its terms make it available to customers and for internal use on condition that no modifications are made, and an OS-9 build is a modified copy. | EFFO forum disk 11, SOFTWARE/C/SEDT_EDITOR |
| `skewlife` | A batch Life computation on skewed squares.<br>**Why not:** It builds from a generated source file of over 700 KB and has no display of its own; this disk carries Life in several forms. | comp.sources.games v08i087 |
| `SmallTeX` | A small text formatter that writes input for a Fancy Font printer back end.<br>**Why not:** The back end, pfont, is not in any archive, so its output has nothing to print it. | Microware OS-9 archive, 6809 C section |
| `smbfm` | An SMB (Samba) client file manager: smbmount, samba and smbdrv.<br>**Why not:** Free to copy, but its terms forbid distributing any part of it with other software packages without the author's permission. | Microware OS-9 archive, NETWORK/smbfm14t.zip (and later versions) |
| `sokoban2` | The second version of sokoban.<br>**Why not:** The same author's sokoban, with the same screens, is on this disk. | TOP release 2 (The OS-9 Project, Munich), top.tar.Z |
| `sortc` | A multi-key character sort.<br>**Why not:** sort on this disk does the job. | Microware OS-9 archive, 6809 C section |
| `spiro` | Generates pretty spirograph patterns.<br>**Why not:** It draws through the Unix plot(3X) library, which OS-9 does not have. | comp.sources.misc v02i046 |
| `splitalf` | Splits a file into 26 files by the first letter of each line.<br>**Why not:** It stops on opening its second output file, even with its one real bug fixed. | EFFO forum disk 6, PROGRAMME/bix (bix.arc) |
| `stig` | Strangest Abuse of the Rules in the 1990 International Obfuscated C Code Contest.<br>**Why not:** Its C file is three bytes; the entry is a csh aliasing trick. | EFFO forum disk 16, SOFTWARE/C/7TH_C_CONTEST |
| `sysmon` | A system monitor.<br>**Why not:** Its source is marked as the proprietary confidential property of a research institute. The author offers it to anyone, but the notice is the institute's. | Microware OS-9 archive, CMDS/SYSMON.lzh |
| `sz` | ZMODEM send, from Omen Technology.<br>**Why not:** A commercial program: the archive carries its licence order form, priced per user. k, xy and z on this disk are free X/Y/ZMODEM. | Microware OS-9 archive, APPS/rzsz_3_36_3_OSK.lzh |
| `tbr` | A working shell in 550 characters, Best Utility in the 1990 International Obfuscated C Code Contest.<br>**Why not:** It is built on fork, pipe, execvp and wait, which this C library does not have. | EFFO forum disk 16, SOFTWARE/C/7TH_C_CONTEST |
| `tetrix` | A falling-blocks game.<br>**Why not:** It is the same source as tet on this disk, which is already a rebuilt copy of it. | TOP release 2 (The OS-9 Project, Munich), top.tar.Z |
| `times` | Times a command.<br>**Why not:** time on this disk does the job. | TOP release 2 (The OS-9 Project, Munich), top.tar.Z |
| `toon` | Toon 1.0, a terminal animation.<br>**Why not:** Only one of its five posted parts survives with a body, so it cannot be built. | alt.sources, May 1994 |
| `travesty` | Daniel J. Bernstein's travesty generator: rewrites its input as plausible nonsense by Markov chains.<br>**Why not:** Its grant to copy and distribute ran only until January 1, 1994. ape on this disk does the same job. | Usenet posting, 1989 |
| `tshell` | A command shell for OS-9/68000.<br>**Why not:** Its readme says it is not public domain and is free for private use, which does not cover a collection like this. | EFFO public-domain disk 4; also Microware OS-9 archive, SHELLS/tshell.zip |
| `udate` | The UNaXcess bulletin board's date display.<br>**Why not:** Its terms allow unmodified copies only, and an OS-9 build is a modified copy. | UNaXcess 1.0.2 BBS package |
| `ufo` | An object-shooting game.<br>**Why not:** Its game loop runs on millisecond alarms and ftime, which this C library lacks; a timing rewrite rather than a port. | comp.sources.games v15i004 |
| `unTC` | Extracts TC archives made on the Color Computer.<br>**Why not:** No TC archive exists anywhere in the pool to use it on. | Microware OS-9 archive, 6809 C section |
| `upatch` | Larry Wall's patch at patch level 12.<br>**Why not:** patch on this disk does the job. | TOP release 2 (The OS-9 Project, Munich), top.tar.Z |
| `uwho` | The UNaXcess bulletin board's who-is-online.<br>**Why not:** Its author allows unmodified copies only, and an OS-9 build is a modified copy. | UNaXcess 1.0.2 BBS package |
| `vi (XENIX)` | An ex/vi editor adapted for OS-9/68000 from the XENIX vi sources; a different program from the vi on this disk.<br>**Why not:** Its own first line says it originates from the XENIX sources, and nobody able to grant redistribution has done so. The vi on this disk is PVIC, which is public domain. | EFFO forum disk 13, SOFTWARE/C/VI |
| `view (4.5a)` | A picture viewer for the 6309 Color Computer.<br>**Why not:** It is for the CoCo's 6309, and its source archive is blank. | Microware OS-9 archive |
| `Vprint` | A printer-formatting utility first written for OS-9/68000 in 1991.<br>**Why not:** The only copy found is a 1997 Linux rewrite, not the OS-9 program. | community archive, bvdp/vpt |
| `wanderer2` | Wanderer 2.2.<br>**Why not:** Wanderer is on this disk. | TOP release 2 (The OS-9 Project, Munich), top.tar.Z |
| `watchdog` | A watchdog module for a real OS-9 system.<br>**Why not:** Written for a real OS-9 system; it could not be run and checked here, as the emulator used for testing loads no drivers. | OS-9 International code disk, via EFFO |
| `where` | Finds a program along PATH.<br>**Why not:** which on this disk does the job. | TOP release 2 (The OS-9 Project, Munich), top.tar.Z |
| `xtail` | A kind of tail -f for many files and directories at once.<br>**Why not:** It runs for ever by design, so it cannot be demonstrated to a finish. | comp.sources.misc v07i108 |
| `xwdtopbm` | Converts an X window dump to PBM; one of the early pbmexec tools.<br>**Why not:** It rejects PBM files, plain and raw, that netpbm on this disk reads and writes correctly. xwdtopnm does the job here. | Microware OS-9 archive, GRAPHICS/pbmexec.lzh |
| `xxxtopbm` | Converts a further bitmap format to PBM; one of the early pbmexec tools.<br>**Why not:** It rejects PBM files, plain and raw, that netpbm on this disk reads and writes correctly, so it works with nothing here. | Microware OS-9 archive, GRAPHICS/pbmexec.lzh |
| `zmodem` | A ZMODEM file transfer program.<br>**Why not:** A copyright with no grant to redistribute. k, xy and z on this disk are free X/Y/ZMODEM. | TOP release 2 (The OS-9 Project, Munich), USR/SRC/zmodem.t.Z |

</details>

---

&#9733; marks a program that uses Microware's `cio`, which ships on the disk, included with Microware's permission; `DOC/README-CIO` has the details.

Generated by `tools/gen_catalog.py` from the disk's own documents. Do not edit by hand; it will be overwritten.
