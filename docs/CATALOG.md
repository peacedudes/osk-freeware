# What is on this disk

615 programs of OS-9/68K community software, gathered from the archives that kept it and made to run again. **517 of them need nothing but this disk**; the rest want Microware's `cio`, marked below with a star.

`DOC/INDEX` on the disk lists everything alphabetically. This is the same collection sorted by what each program is *for*, which is the more useful order when you do not yet know what you are looking for.

> Prefer to click around? `docs/index.html` is a searchable version with per-program detail — what it needs, where it came from, on what terms. GitHub will not render it here; download the repository and open it, or enable Pages.

| Category | Programs | |
|---|--:|---|
| [Shells](#shells) | 16 | The stock OS-9 shell is thin. These give you history, job control and a command line worth living in. |
| [Editors](#editors) | 18 | vi and emacs in several flavours, line and stream editors, and editors for binary and hex. |
| [Text tools](#text-tools) | 71 | Search, sort, compare, reformat, split and spell-check. |
| [Files & directories](#files--directories) | 31 | Listing, copying, finding, renaming, and knowing what you have. |
| [Developer tools](#developer-tools) | 28 | Version control, tags, cross-reference, formatters, a debugger and benchmarks. |
| [Compilers & build](#compilers--build) | 33 | C compilers and their passes, assemblers, linkers, make and parser generators. |
| [Languages](#languages) | 6 | Interpreters and language systems beyond C. |
| [Archives & compression](#archives--compression) | 20 | Pack, unpack and shrink -- lha, zip, tar, arc, zoo, and OS-9 module libraries. |
| [Encoding & conversion](#encoding--conversion) | 16 | Between text encodings, line endings, number bases, ciphers and hashes. |
| [Communications](#communications) | 20 | Kermit in several builds, terminal sessions, and networking. |
| [Graphics & images](#graphics--images) | 189 | The netpbm toolkit, JPEG, a ray tracer, and things that draw. |
| [Games](#games) | 57 | Adventures, board and card games, arcade ports, dungeon crawls and puzzles. |
| [Screen toys](#screen-toys) | 6 | Things to watch rather than play. Start one and leave it going. |
| [Amusements](#amusements) | 19 | Generators, simulators and diversions that are not quite games. |
| [System & modules](#system--modules) | 32 | OS-9 module and process tools, devices, system state and scheduling. |
| [Disk & DOS](#disk--dos) | 20 | Reading and writing MS-DOS media with the mtools set. |
| [Time & calendar](#time--calendar) | 10 | Calendars, clocks and astronomy. |
| [Maths & calculators](#maths--calculators) | 11 | Calculators, plotting, orbits and number theory. |
| [Printing](#printing) | 8 | Spoolers, page formatting and PostScript. |
| [Documentation](#documentation) | 4 | Pagers, readers and the help system. |

## Shells

*The stock OS-9 shell is thin. These give you history, job control and a command line worth living in.*

<details><summary>16 programs</summary>

**Shell helpers**

| | |
|---|---|
| `checkenv` | &#9733; check env var<br>`Syntax: checkenv <eparam> , <evalue>` |
| `exist` | &#9733; test file existence |
| `fc` | &#9733; re-execute history<br>`Syntax:   fc [<file>]` |
| `getenv` | &#9733; print an environment variable<br>`USAGE: getenv [-n\|-p\|-l\|-x] <Environment> [<Wert>]` |
| `hist` | C-shell history + commandline editing  [no military use -- EFFO-INFO] |
| `if` | conditional execution for shell scripts (varval/loaded/def)<br>`Syntax: if [not] <cond> {<arg>} {<cmd1>} [else` |
| `paths` | show/expand the PATH |
| `printenv` | &#9733; print the environment<br>`Syntax:   printenv [<options>] [{<env var name}]` |
| `printf` | formatted print from the shell<br>`Usage: printf <format-string> [ arg1 . . . ]` |
| `run` | run a program with stdio rebound to the terminal (needs PORT)<br>`Syntax: run '<prgname> {<arg>}'` |
| `xc` | execute commands from a file (needs a .xc) |

**Shells**

| | |
|---|---|
| `bash` | GNU Bourne-Again Shell 1.12 -- this disk's shell; reads .bashrc<br>`usage: fc [-e ename] [-nlr] [first] [last] or fc -s [pat=rep] [command]` |
| `gshell` | GSHELL - a shell<br>`Syntax: gshell [<path>]` |
| `ksh` | &#9733; Public Domain Korn Shell 4.3 (edition 11, OS-9 port)<br>`Syntax: 'setpr <prior>' or 'setpr <pid> [<pid>..] <prior>'` |
| `sh` | Bourne shell v7.5 -- the startup script's shell; needs no Microware module |
| `wish` | WiSH - full-screen windowing shell over the OS-9 shell |

</details>

## Editors

*vi and emacs in several flavours, line and stream editors, and editors for binary and hex.*

<details><summary>18 programs</summary>

**vi family**

| | |
|---|---|
| `sedt` | SEDT screen editor |
| `VI` | PVIC, public domain            -> /dd/CMDS/REBUILT (name was taken)<br>`Usage: vi [file ...]` |
| `vi` | vi/ex editor (EFFO build, has its own ex_OS9.c) |
| `vi_cio` | &#9733; PVic vi, cio build (use vi_nocio instead)<br>`Usage: vi [file ...]` |
| `vi_nocio` | PVic 1.0a -- vi-compatible editor, cio-free (the vi to use here)<br>`Usage: vi [file ...]` |
| `vis` | make non-printing characters visible |

**Binary & hex**

| | |
|---|---|
| `beav` | BEAV 1.40 -- Binary Editor And Viewer (needs TERM)<br>`Syntax   : beav {<filename>}` |
| `chbase` | &#9733; change module base<br>`Syntax   : chbase <number> [ <base A> [ <base B> ] ]` |
| `hexed` | hex editor via your text editor  [no military use -- EFFO-INFO]<br>`Syntax: hexed [<opts>] <path> {[<opts>] \| [<path>]}` |
| `hexedit` | Hex file editor -- hex [-vdr] file<br>`Usage: hex [-vdr] 'file'` |
| `pbyte` | patch bytes in a file at a hex offset<br>`Syntax: pbyte <path> <hex_offset> <hex_byte> [<hex_byte>]` |

**emacs family**

| | |
|---|---|
| `emacs` | &#9733; MicroEmacs 4.00 |
| `emacs.mm1` | &#9733; MicroEmacs macro module |
| `me` | MicroEmacs 3.11 -- ADDED; needs TERM.  (memacs400 `emacs` needs cio)<br>`Syntax:   emacs [opts] <files>` |
| `mg` | &#9733; MicroGnuEmacs |

**Line & stream**

| | |
|---|---|
| `ed` | &#9733; GNU ed 0.2 line editor<br>`Usage: ed [OPTION]... [FILE]` |
| `editor` | GSHELL front-end for the editor<br>`Syntax: editor [<path>]` |
| `sed` | sed - stream editor (verified: s/x/y/ substitution works)<br>`Syntax: sed [<opts>] [<path>] [<opts>]` |

</details>

## Text tools

*Search, sort, compare, reformat, split and spell-check.*

<details><summary>71 programs</summary>

**Transform & filter**

| | |
|---|---|
| `ape` | APE - text filter |
| `autolf` | &#9733; auto-linefeed filter<br>`Usage:   autolf [<opts>] {<file names> [<opts>]}` |
| `casefix` | normalise letter case in a text file |
| `cut` | cut selected fields from each line |
| `cuts` | Coco Usenet Transfer Utility<br>`Usage: cuts <-d> [-o name] <file>...` |
| `detab` | &#9733; tabs to spaces<br>`Usage: detab [-tn] [infile] or [<infile]` |
| `deton` | detab - convert tabs to spaces<br>`syntax: deton [seconds]` |
| `eo` | eo - text utility |
| `field` | &#9733; extract fields<br>`Syntax  : field [<opts>] <fields...> [<opts>]` |
| `fillup` | fill a file up to a given length with a constant byte<br>`Syntax:   fillup [<options>] <file>` |
| `gep` | global expression parser - grep-like filter<br>`Syntax: gep [<opts>] [<srcpath>] [<opts>]` |
| `paste` | merge lines of files<br>`USAGE: paste [-s] [-d<list>] files` |
| `pep` | file 'detergent' - strip junk from files<br>`Usage: pep [options] [filename ...]` |
| `psc` | &#9733; sc's print/format filter<br>`Syntax: psc [-rkfLSPv?] [-s v] [-R i] [-C i] [-n i] [-d c] [<path1] [>path2]` |
| `qt` | quick text utility |
| `rot` | rot-N text transformer |
| `shuffle` | shuffle lines/cards<br>`Usage: shuffle [-] [-L level]` |
| `souper` | souper - text utility |
| `tabs` | tab/space conversion filter<br>`Syntax   : tabs [<opts>] [<input_redirection>] [<output_redirection>]` |
| `upperdir` | Normalise case: files lowercase, dirs uppercase<br>`Usage: UpperDir [directory name]` |
| `valspeak` | Valley-speak text filter |

**Sort, compare & merge**

| | |
|---|---|
| `cdiff` | context diff |
| `diff` | GNU diff 1.1 -- ADDED; the disk had no diff at all.  Verified on CR files<br>`Usage: diff [-options] file1 file2` |
| `ediff` | visual file compare<br>`Syntax   : 'ediff <file'  or  'diff <f1> <f2> ! ediff'` |
| `fcomp` | compare two text files<br>`Syntax: fcomp <file_1> <file_2>` |
| `join` | GNU join -- relational join of two sorted files<br>`Usage: join [-a 1\|2] [-v 1\|2] [-e empty-string] [-o field-list...] [-t char]` |
| `nsort` | numeric sort<br>`Usage: nsort <unordered >sorted` |
| `qsort9` | &#9733; sort filter<br>`Syntax: qsort9 [<opts>] [<srcpath>] [<opts>]` |
| `sort` | GNU sort<br>`Usage: sort [-cmus] [-t separator] [-o output-file] [-bdfiMnr] [+POS1 [-POS2]]` |
| `spiff` | tolerant diff - ignores formatting noise<br>`Syntax: spiff [-s script] [-f sfile] [-bteiqcdwm] [-abr value] -value f1 f2` |
| `unip` | unique lines with page numbers<br>`Syntax: unip [<opts>] [<srcpath>] [<opts>]` |
| `uniq` | &#9733; drop duplicate lines<br>`Usage: UNIQ [-u][-d][-c] [-n] [^n] input [>output]` |

**Count & inspect**

| | |
|---|---|
| `ascii` | ASCII character table |
| `dump` | hex dump of a file or module<br>`Syntax: dump [<opts>] <path/module> [<opts>] [<starting byte>] [<opts>]` |
| `file` | Identify file types (warns: no /dd/SYS/magic file -- still IDs OS-9 modules)<br>`Syntax:   file [<opts>] {<file>}` |
| `gdd` | &#9733; data dump<br>**How:** A data dump -- like `od', with GNU-style long options. Needs Microware's cio. |
| `strings` | extract printable strings |
| `strings.cio` | &#9733; archived build, needs cio; superseded by the gcc2 rebuild<br>`Usage: strings.cio [-anpl=n] [file [file]]` |
| `tail` | &#9733; last lines of a file |
| `wc` | count lines/words/chars -- REBUILT HERE with gcc2; counts CR or LF lines |
| `wc.cio` | &#9733; archived build, needs cio; superseded by the gcc2 rebuild |

**Search & match**

| | |
|---|---|
| `bm` | &#9733; bm - fast grep utility (Boyer-Moore) |
| `bmgtest` | Boyer-Moore-Gosper substring search demo<br>**How:** bmgtest [-i] [-n] <pattern> [file ...]. A demonstration of Boyer-Moore-Gosper searching, not a tool you would use. |
| `bmgtest2` | Boyer-Moore-Gosper substring search demo (variant)<br>`usage: bmgtest [-i] [-n] pattern [file ...]` |
| `fgrep` | &#9733; very fast grep utility<br>`usage: fgrep [-[[AB] ]<num>] [-[CVchilnsvwx]] [-[ef]] <expr> [<files...>]` |
| `grep` | GNU grep 2.0 -- pattern search<br>`usage: grep [-[[AB] ]<num>] [-[CEFGVchilnqsvwx]] [-[ef]] <expr> [<files...>]` |
| `soundex` | Soundex phonetic key for each word on stdin |

**Fortune & sayings**

| | |
|---|---|
| `cookhash` | build the hash file cookie(1) needs, from a sayings file<br>`usage: cookhash <cookiefile >hashfile` |
| `cookie` | print a random fortune cookie<br>`usage: cookie cookiefile hashfile` |
| `fortune` | print a random quotation<br>`usage:  fortune [ - ] [ -wsloa ] [ file ]` |
| `sonnet` | writes (bad) sonnets in iambic pentameter, curses-based<br>`Usage:  sonnet [-l input] [-f outfilename]` |
| `strfile` | build fortune's index file<br>`usage:  strfile [ - ] [ -cC ] [ -sv ] inputfile [ datafile ]` |
| `unstr` | reverse strfile - dump a fortune index<br>`usage: unstr datafile[.dat] [ outfile ]` |

**Spelling & words**

| | |
|---|---|
| `buildhash` | build ispell's dictionary hash (writes LIB/ispell.hash) |
| `ispell` | interactive spelling checker |
| `jargon` | Jargon-file browser (needs its database files)<br>`usage: jargon [-cigmr] [-b key] [srcname] [indexname]` |
| `makelex` | compiles sonnet's lex.data word list into a C array |
| `speech` | English-to-phoneme translation<br>`Usage: PHONEME [infile [outfile]]` |

**Format & typeset**

| | |
|---|---|
| `lout` | Lout 2.05 document formatter (Basser Lout, Jeffrey Kingston)<br>`usage: -o<filename>` |
| `nroff` | nroff text formatter -- setenv TMACDIR /dd/LIB first<br>**How:** Formats man pages. The -man macros in LIB/tmac.an were extended for this collection because the originals defined only .TH .SH .SS .PP and .I; LIB/orig.tmac.an is the untouched version. Try `nroff -man /dd/DOC/netpbm/pnmscale.1'. |
| `proff` | proff - portable roff text formatter (macros in LIB/proff)<br>`usage: proff [+n] [-n] [-v] [-ifile] [-s] [-pon] [infile [outfile]]` |
| `roff` | roff text formatter<br>`Syntax: roff {[+00] [-00] [-s] -[h] file}` |
| `tformat` | text formatter (SNOBOL4-in-C)<br>`Usage: tformat [width\|-?] [<infile] [>outfile]` |

**Banners & text art**

| | |
|---|---|
| `banner` | print large banner text |
| `cursive` | generate a horizontal cursive banner<br>`usage: cursive [-tn] [-in] message` |
| `gothic` | print text as a gothic/blackletter banner |

**KWIC index**

| | |
|---|---|
| `pagefraz` | KWIC suite - phrase extractor<br>`Syntax: pagefraz <opts> [<in_path> [<out_path>]] <opts>` |
| `pagekwic` | KWIC suite - split a Stylo file to one phrase per line with page no.<br>`Syntax: pagekwic <opts> [<in_path> [<out_path>]] <opts>` |
| `pageline` | KWIC suite - line/page numbering<br>`Syntax: pageline <opts> [<in_path> [<out_path>]] <opts>` |

**Split & join**

| | |
|---|---|
| `sepwords` | split a file to one word per line<br>`Syntax: sepwords [<in_path> [<out_path>]]` |
| `splitalf` | split a file alphabetically<br>`Syntax: splitalf <opts> [<in_path>] <opts>` |

</details>

## Files & directories

*Listing, copying, finding, renaming, and knowing what you have.*

<details><summary>31 programs</summary>

**Copy, move, delete**

| | |
|---|---|
| `cp` | &#9733; copy files<br>`Usage: cp file1 file2` |
| `dback` | Directory backup utility (wants a /d0 device)<br>`Usage: Dback [-options] <fromdir> <todir> [-options]` |
| `delbak` | &#9733; delete backup files (*_bak) in a directory tree<br>`Usage: delbak [-options] [directory] [-options]` |
| `eunlink` | &#9733; extended unlink<br>`Syntax: eunlink {<event>}` |
| `move` | &#9733; move files between directories<br>`Syntax:   move [<options>] <from> [<to>] [<options>]` |
| `mv` | &#9733; move/rename<br>`Usage: mv [-bfiuv] [-S backup-suffix] [-V {numbered,existing,simple}]` |
| `remove` | remove files, with confirmation<br>`Syntax   : remove [<opt>] [<modules>] [<opt>] [<modules>] [<opt>]` |
| `rm` | &#9733; remove files<br>`Usage: rm [-dfirvPR] [+directory] [+force] [+interactive] [+recursive]` |
| `undel` | undelete a file<br>`Usage: attr <file> -d` |

**List & navigate**

| | |
|---|---|
| `dir` | &#9733; directory listing<br>`Syntax: dir [<opts>] {<dir names> [<opts>]}` |
| `dm` | &#9733; disk/dir monitor<br>`Usage: DiskMaster [-c] [-d<dir name>]` |
| `edir` | &#9733; extended directory listing<br>`Syntax: edir [<opts>]` |
| `l` | &#9733; brief directory listing<br>`Usage: l [-options] [file] [file] [-options]` |
| `ls` | GNU ls (fileutils 3.13) -- OUR OWN FIXED BUILD: real stat(), columns, -al<br>`Usage: ls [OPTION]... [FILE]...` |
| `tree` | Print a directory tree -- BUT fails on this disk: it opens the raw<br>`Syntax: tree [<directory>] [<opts>]` |

**Find & compare**

| | |
|---|---|
| `dfiles` | find duplicate files on disk and issue the cmp commands |
| `du` | disk usage, by directory<br>`Syntax: du <directory>` |
| `ff` | find files by name -- ff [<opts>] <name>... |
| `find` | find 1.1.5 -- search a directory tree<br>`Syntax: find {<opts>} [<path>]` |
| `space` | effective disk usage  [conditions apply -- run `help space`]<br>`Syntax:   space [<opts>] {<dir/file path>} [<opts>]` |

**Paths**

| | |
|---|---|
| `basename` | strip directory from a pathname -- REBUILT HERE with gcc2<br>`usage: basename path [suffix]` |
| `basename.cio` | &#9733; archived build, needs cio; superseded by the gcc2 rebuild<br>`Syntax:   basename <path> [<suffix>]` |
| `dirname` | strip filename from a pathname -- REBUILT HERE with gcc2 |
| `dirname.cio` | &#9733; archived build, needs cio; superseded by the gcc2 rebuild<br>`Syntax:   dirname <path>` |

**Attributes & ownership**

| | |
|---|---|
| `chgrp` | &#9733; change group<br>`Usage:  chgrp [-z] {numerical-gid \| username} [file [... file]]` |
| `chown` | &#9733; change owner<br>`Usage:  chown [-z] {numerical-uid \| username} [file [... file]]` |
| `eset` | &#9733; set an OS-9 event to a value -- eset <event> <num><br>`Syntax: eset <event> <num> [<opts>]` |
| `owner` | &#9733; show file owner<br>`Usage: owner user file file ...` |

**Create & rename**

| | |
|---|---|
| `mkdir` | &#9733; make directory<br>`Usage: mkdir [-p] [-m mode] [+path] [+mode mode] dir...` |
| `ren` | bulk rename files<br>`Syntax: ren [<opts>] <pathlist> <newname>` |
| `rendsk` | rename a disk volume<br>`Syntax:   rendsk [<opts>] <disk device> <new name>` |

</details>

## Developer tools

*Version control, tags, cross-reference, formatters, a debugger and benchmarks.*

<details><summary>28 programs</summary>

**Benchmarks**

| | |
|---|---|
| `disktest` | measure disk performance  [no military use -- DOC/EFFO-INFO]<br>`Syntax   : disktest [<opt>]` |
| `fibo` | Fibonacci benchmark |
| `float` | floating-point benchmark |
| `paranoia` | &#9733; floating-point benchmark |
| `savage` | Savage floating-point accuracy benchmark |
| `sieve` | sieve of Eratosthenes benchmark |
| `time` | time a command |
| `timeio` | time I/O operations |
| `timid` | timing utility<br>`Syntax: timit [<opts>]` |

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

**Source formatting**

| | |
|---|---|
| `cb` | &#9733; C beautifier<br>`Usage:  cb <input.fil >output.fil` |
| `cpr` | print/pretty-list C source files<br>`Usage: cpr [-cCnNsS] [-T title] [-t tabwidth] [-p[num]] [-r[num]] [-l pagelength] [[-f] file] ...` |
| `ifdef` | resolve #ifdefs in C source<br>`Syntax: ifdef [<opts>] [<file>] [<opts>]` |
| `indent` | reformat a C source program for readability<br>`Syntax: indent [<opts>] [<inpath> [<outpath>]] [<opts>]` |
| `patch` | Larry Wall's patch - apply a diff |
| `unifdef` | remove #ifdef sections from C source<br>`syntax: unifdef {<opts>} [<file>]` |

**Source navigation**

| | |
|---|---|
| `ctags` | generate a vi tags file from C source (BSD)<br>`usage: ctags [-BFadtuwvx] [-f tagsfile] file ...` |
| `cxref` | &#9733; C cross-reference lister -- numbered listing + symbol table<br>`Syntax:		cxref [-opts] [path]` |
| `etags` | generate an emacs TAGS file<br>`Syntax: etags { [<opts>] <path> }` |
| `xrf` | C cross-reference generator |

**Debugging**

| | |
|---|---|
| `sdb` | SDB 2.0 - symbolic debugger |
| `trap` | &#9733; system-state trap-handler example |

</details>

## Compilers & build

*C compilers and their passes, assemblers, linkers, make and parser generators.*

<details><summary>33 programs</summary>

**C toolchain**

| | |
|---|---|
| `cc1plus` |  |
| `cc2` |  |
| `cc2plus` |  |
| `cccp2` | <br>`Usage: cccp2 [switches] input output` |
| `collect` | <br>`Syntax   : collect [<opts>] {<file>} [<opts>]` |
| `compiler` | GSHELL front-end for the C compiler<br>`Syntax: compiler [<path>]` |
| `gcc` | <br>`Usage: gcc {options} {files} {options}` |
| `gcc2` | <br>`Usage: gcc2 {options} {files} {options}` |
| `gcc_cc1` |  |
| `gcc_cc1plus` |  |
| `gcc_cccp` | <br>`Usage: gcc_cccp [switches] input output` |
| `gcc_collect` | <br>`Syntax   : collect [<opts>] {<file>} [<opts>]` |
| `gpp` | <br>`Usage: gpp {options} {files} {options}` |

**Make & generators**

| | |
|---|---|
| `assembler` | GSHELL front-end for the assembler<br>`Syntax: assembler [<path>]` |
| `bison` | GNU bison 1.19 parser generator -- ADDED; skeletons in /dd/LIB<br>`Usage: bison [-dltvyV] [-b file-prefix] [-o outfile] [-p name-prefix]` |
| `dmake` | &#9733; dmake 3.70 - parallel make with its own makefile dialect |
| `flex` | lexical analyzer generator -- see DOC/flex/README-FLEX FIRST<br>`Syntax   : flex [-bcdfinpstvFILT8 -C[efmF] -Sskeleton] [filename ...]` |
| `gmake` | GNU make -- ADDED (the gnu.bin build of make is the broken one)<br>`Usage: gmake [options] [target] ...` |
| `m4` | m4 macro processor<br>`Usage: m4 [-Dname[=val]] [-Uname]` |
| `make` | make - maintain and regenerate groups of files (verified: -? works)<br>`Syntax :	make {[-f <makefile>] [-dDinrst] [<target>] [<macro>=<value>]}` |
| `makeinfo` | GNU makeinfo -- Texinfo to info<br>`Usage: makeinfo [options] texinfo-file...` |
| `rtf` | RTF/68K FORTRAN compiler proper |
| `yacc` | yacc parser generator<br>`Syntax   : yacc [-dltv] [-b <prefix>] filename` |

**Assemblers & linkers**

| | |
|---|---|
| `as0` | 68000 assembler (xasm)<br>`Usage: as0 [files]` |
| `as09` | &#9733; 6809 assembler<br>`Usage: as09 [files]` |
| `as1` | 68010 assembler (xasm)<br>`Usage: as1 [files]` |
| `as11` | 68HC11 assembler (xasm)<br>`Usage: as11 [files]` |
| `as4` | 68040 assembler (xasm)<br>`Usage: as4 [files]` |
| `as5` | 68050 assembler (xasm)<br>`Usage: as5 [files]` |
| `lnk` | module linker |
| `lnk.org` | module linker (original build) |
| `my.opt` | 68k assembly peephole optimiser<br>`syntax: optim {opt} [infile] {opt} [outfile] {opt}` |

**Other languages**

| | |
|---|---|
| `for` | RTF/68K FORTRAN compiler driver |

</details>

## Languages

*Interpreters and language systems beyond C.*

<details><summary>6 programs</summary>

| | |
|---|---|
| `forth` | &#9733; Forth interpreter<br>`Syntax   : forth [<opts>] [<file>] [<opts>]` |
| `lua` | &#9733; Lua 3.0 -- a small scripting language.  OS-9 port with its own<br>**How:** Lua 3.0, and it needs Microware's csl -- see DOC/README-CIO. Run a script with `lua file.lua'. NOTE: 3.0 has no numeric `for' loop; that arrived in Lua 3.1, so `for i=1,10 do' is a syntax error here and `while' is the idiom. Examples in DOC/lua/examples. |
| `luac` | &#9733; Lua bytecode compiler -- luac -o out in.lua<br>**How:** Compiles a Lua script to bytecode: `luac -o out in.lua'. Needs csl. runc then runs the result as an OS-9 command. |
| `runc` | &#9733; Runs a compiled Lua chunk as an OS-9 command |
| `wam.sbprolog` | SB-Prolog 2.2 WAM engine -- see DOC/sbprolog/README-SBPROLOG<br>`Usage: sim [-Ttdns] [-m s_size] [-p p_size] [-b tr_size] [-ui num] pil_file_name ...` |
| `xlisp` | XLISP 2.1 Lisp interpreter |

</details>

## Archives & compression

*Pack, unpack and shrink -- lha, zip, tar, arc, zoo, and OS-9 module libraries.*

<details><summary>20 programs</summary>

**Create & extract**

| | |
|---|---|
| `ar` | archive librarian (Carl Kreider) -- .ar files<br>`Usage:  Ar -<cmd>[<modifier>] [file .. ]` |
| `arc` | third-party, no terms stated   -> /dd/CMDS/REBUILT (name was taken)<br>`Usage: arc -{amufdxeplvtc}[bswn][g<password>]` |
| `cat` | concatenate files -- REBUILT HERE with gcc2 (archived cat needs cio) |
| `cat.cio` | &#9733; archived build, needs cio; superseded by the gcc2 rebuild |
| `lha` | LHa 2.08 -- create/extract .lzh archives<br>`Syntax: LHa -{axelvudmcp}[qvnfodiszrgc012][w=<dir>] archive_file [file...]` |
| `lharc` | LHarc archiver<br>`Usage: lharc {axevlufdmctp}[qnftv] archive_file [files or directories...]` |
| `marc` | MARC archiver<br>`Usage: MARC <tgtarc> <srcarc> [<filename> . . .]` |
| `shar` | Shell-archive creator |
| `tar` | GNU tar 1.10<br>`Syntax : tar [ctx][mfv] tarfile [file(s)...]` |
| `unzip` | &#9733; Info-ZIP unzip<br>`Usage: unzip [ -options[modifiers] ] file[.zip] [filespec...]` |
| `zip` | Info-ZIP zip 1.9 |
| `zipnote` | Info-ZIP zipnote -- view/edit zip comments<br>`Usage:  zipnote [-w] [-b path] zipfile` |
| `zipsplit` | Info-ZIP zipsplit -- split a zip archive<br>`Usage:  zipsplit [-ti] [-n size] [-b path] zipfile` |
| `zoo` | &#9733; zoo archiver<br>`Usage: zoo {acDeglLPTuUvx}[aAcCdEfInmMNoOpPqu1:/.@n] archive file` |

**Compress a file**

| | |
|---|---|
| `compr` | file compressor<br>`Usage: compress [-dfvcV] [-b maxbits] [file ...]` |
| `compress` | compress/uncompress (LZW) -- ADDED<br>`Usage: compress [-dfvoV] [-b MaxBits] [file ...]` |
| `gzip` | GNU gzip<br>`usage: gzip [-gzipcdfhlLngziptvV19] [-S suffix] [file ...]` |

**OS-9 module libraries**

| | |
|---|---|
| `liborder` | order the modules in an OS-9 library<br>`Usage: liborder <options> file1.r file2.r ...` |
| `modbuster` | Split merged OS-9 module files<br>`Syntax: Modbuster [<opts>] <path> [<opts>]` |
| `unpacklib` | split an OS-9 library into its modules<br>`Usage: unpacklib <options> file1.l file2.l ...` |

</details>

## Encoding & conversion

*Between text encodings, line endings, number bases, ciphers and hashes.*

<details><summary>16 programs</summary>

**Text encodings**

| | |
|---|---|
| `atob` | ASCII-to-binary decode<br>`Usage: atob <filein >fileout` |
| `btoa` | Binary-to-ASCII encode<br>`Usage : btoa <filein >fileout` |
| `chardef` | define a character set<br>`Syntax: defchar [<path>]` |
| `todos` | &#9733; OS-9 to DOS line endings |
| `toos9` | &#9733; DOS to OS-9 line endings |
| `uudecode` | &#9733; uudecode<br>`USAGE: uudecode [infile]` |
| `uuencode` | &#9733; uuencode<br>`USAGE: uuencode >outfile [infile] name` |
| `uuexpand` | expand uuencoded text<br>`Usage: uuexpand [opts]` |

**Ciphers & hashes**

| | |
|---|---|
| `checksum` | file checksum<br>`Syntax:   checksum <file> [<file>...]` |
| `chksum` | 32-bit file checksum |
| `crypto` | cryptogram puzzle solver's assistant<br>`usage: crypto [-cegnru] [file(s)]` |
| `des` | DES file encryption |
| `md5` | MD5 checksum<br>`Usage: MD%d <-opts> <filename>` |
| `xcrypt` | file encryption/decryption |

**Number bases**

| | |
|---|---|
| `cvtbase` | convert a number between bases |
| `divide` | &#9733; integer divide |

</details>

## Communications

*Kermit in several builds, terminal sessions, and networking.*

<details><summary>20 programs</summary>

**Terminal & session**

| | |
|---|---|
| `aterm` | ATerm 2.6 -- terminal emulator<br>`Syntax  : ATerm /serial_path` |
| `cls` | clear the screen (termcap)<br>`Syntax: cls` |
| `connect` | connect to a serial line<br>`Usage: connect [<switches>] [<path1>] [<switches>] [<path2>]` |
| `fkeys` | define terminal function keys<br>`Syntax: fkeys [<path>]` |
| `initvdu` | &#9733; init video display<br>`Syntax  : initvdu [<opts>]` |
| `input` | UNAXCESS BBS - input helper |
| `sbreak` | Send/clear an SS_Break signal on a serial path<br>`Syntax:   sbreak [/device]` |
| `screen` | Screen multiplexer (needs HOME set) |
| `setfont` | load a downloadable terminal font -- setfont <path><br>`usage: setfont <path>` |
| `setterm` | &#9733; set terminal type<br>`Syntax:   setterm [opts] [term type]` |
| `tsmon2` | tsmon replacement - terminal monitor<br>`Syntax:   tsmon2 [<options>] <device name>` |
| `udate` | UNAXCESS BBS - date display |
| `uwho` | UNAXCESS BBS - who is online |
| `wysecrack` | &#9733; Wyse terminal baud detect -- needs real Wyse hardware |
| `wysetime` | Wyse terminal time utility |

**Kermit**

| | |
|---|---|
| `ckermit` | &#9733; C-Kermit (cio build) |
| `kermit` | C-Kermit 5A(188) -- serial file transfer + terminal emulation<br>`Usage: kermit c[le line esc.char]   (connect mode)` |
| `kermit2` | Kermit file transfer (variant 2)<br>`Usage:   kermit c[le line esc.char]   (connect mode)` |
| `kermit3` | Kermit file transfer (variant 3)<br>`Usage: kermit [-x arg [-x arg]...[-yyy]...]]` |
| `xkermit` | &#9733; Kermit variant<br>`Usage: kermit c[le line esc.char]   (connect mode)` |

</details>

## Graphics & images

*The netpbm toolkit, JPEG, a ray tracer, and things that draw.*

<details><summary>189 programs</summary>

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
| `pnmscale` | netpbm image tool<br>**How:** pnmscale <factor> <file>. Given only a filename it takes THAT as the factor and then reads empty standard input, reporting "bad magic number" -- which means you left out the factor, not that anything is broken. |
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
| `giftopnm` | GIF to PNM |
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
| `pcxtoppm` | PCX to PPM (colour)<br>**How:** Cannot read a pipe: it seeks backwards in its input and stops with "error seeking past header". Write the PCX to a file first and pass the filename. |
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

**JPEG**

| | |
|---|---|
| `cjpeg` | JPEG encoder (IJG) -- ADDED<br>`usage: cjpeg [switches]` |
| `cjpeg.070` | JPEG compressor (68070 build)<br>`usage: cjpeg.070 [switches]` |
| `djpeg` | JPEG decoder (IJG) -- ADDED<br>`usage: djpeg [switches]` |
| `djpeg.070` | JPEG decompressor (68070 build)<br>`usage: djpeg.070 [switches]` |
| `rdjpgcom` | read the comment from a JPEG file<br>`Usage: rdjpgcom [switches] [inputfile]` |
| `rdjpgcom.070` | read a JPEG's comment (IJG 0.70 build)<br>`Usage: rdjpgcom.070 [switches] [inputfile]` |
| `wrjpgcom` | write a comment into a JPEG file<br>`Usage: wrjpgcom [switches]` |
| `wrjpgcom.070` | write a JPEG's comment (IJG 0.70 build)<br>`Usage: wrjpgcom.070 [switches]` |

**Drawing & display**

| | |
|---|---|
| `bush` | draw a random bush/tree |
| `draw` | character-graphics drawing program |
| `loadmem` | load memory image<br>`Syntax   : LOADMEM <destinati address> <upper limit address> <path>` |
| `pdraw` | Pdraw 1.4 - 2D/3D data plotting, PostScript output<br>`usage: pdraw [-v vx vy vz] [-o options-file] [-Pprinter] [-s scale] [-e] [-h] [-nosort] [-noplot] [-print] [-ps] infile1 infile2 ...` |
| `savemem` | save memory image<br>`Syntax   : SAVEMEM <from address> <to address> <path>` |
| `snap` | snapshot the screen to a file |

**X11**

| | |
|---|---|
| `basicwin` | X11 demo - basic window (needs an X server) |
| `X11R6shl` | X11R6 shared library loader |
| `xengine` | X11 demo - engine animation (needs an X server)<br>`Usage : xengine [Toolkit-Options][-piston piston_color][-shaft shaft_color][-cylinder cylinder_color][-roter roter_color][-back background_color][-dep depression_colore][-pre pression color][-mono][-patchlevel]` |

**Ray tracing & 3D**

| | |
|---|---|
| `mtst` | spline curve fitting - test driver |
| `rayshade` | ray tracer 4.0 -- RUNS but renders wrong; see DOC/rayshade<br>`usage: rayshade [options] [filename]` |
| `rsconvert` | convert rayshade image output between formats<br>`usage: rsconvert [oldfile]` |

</details>

## Games

*Adventures, board and card games, arcade ports, dungeon crawls and puzzles.*

<details><summary>57 programs</summary>

**Board & card**

| | |
|---|---|
| `back` | &#9733; backgammon -- '?' gives the built-in help |
| `blackjack` | Las Vegas blackjack (M. Theys) -- BASIC09; stops at line 8 |
| `blackjak` | blackjack -- from the SNOBOL4-in-C package, see below |
| `chess` | chess - 68k port (three engine versions built)<br>`Syntax: chess [<opts>] <name> [<opts>]` |
| `crib` | cribbage |
| `cribbage` | &#9733; cribbage -- offers instructions before it deals |
| `gnuan` | GNU Chess analyser -- annotates a saved game move by move |
| `gnuchess` | &#9733; GNU Chess<br>`Usage: gnuchess [-a] [-h] [-x xwndw]` |
| `gnuchessc` | GNU Chess 4.0, curses display |
| `gnuchessn` | &#9733; GNU Chess (ncurses)<br>`Usage: gnuchess [-a] [-h] [-x xwndw]` |
| `gnuchessr` | &#9733; GNU Chess (raw)<br>`Usage: gnuchess [-a] [-h] [-x xwndw]` |
| `mille` | &#9733; Mille Bornes -- the French car-racing card game<br>`usage: milles [ restore_file ]` |
| `nchess` | GNU Chess 4.0 (plain display) |
| `poker` | poker -- from the SNOBOL4-in-C package, see below |
| `queens` | N-queens solver -- IOCCC entry by M. Baruch; reads N on stdin |
| `tttt` | tic-tac-toe |

**Other games**

| | |
|---|---|
| `convert` | world - build its data tables |
| `fuddle` | chess - fuddle variant |
| `hotel` | &#9733; hotel -- two-player board game, played by coordinates |
| `mkdict` | bog - build the dictionary |
| `mkindex` | bog - build the dictionary index |
| `nobs` | cribbage (Colonel's program) |
| `piano` | &#9733; play notes -- piano <base note> <note duration><br>`syntax: piano <base note> <note duration>` |
| `stone` | stone -- a game, from the SNOBOL4-in-C package |
| `tess` | tesselation puzzle |
| `tt` | typing/terminal game<br>`Usage: tt [ -s ] [ -b ] [ -l# ]` |
| `vtxtcn` | world - build its text tables |
| `world` | World - text adventure |
| `zot` | Zot - arcade game |

**Arcade & action**

| | |
|---|---|
| `bite` | a skull animation, not a game you play |
| `greed` | Greed - grid game<br>`Usage: greed [-p] [-s]` |
| `lander` | lunar lander -- KNOWN BROKEN: takes no input, and the |
| `pacman` | Pac-Man |
| `robots` | &#9733; robots -- outrun them until they crash into each other.<br>**How:** Use `robots -m'. Without it the game is effectively unplayable, which its usage line offers and nothing explained. |
| `snake` | snake arcade game -- KNOWN BROKEN: starts and then sits |
| `sokoban` | Sokoban puzzle<br>**How:** Wants a username, so run it from a login rather than a bare shell, or it stops with "cannot get your username". |
| `tet` | Tetris -- KNOWN BROKEN: draws its board and takes no input |
| `wanderer` | Boulderdash-style maze game.  Screens ARE here, in |

**Adventure & fiction**

| | |
|---|---|
| `advcom` | ADVSYS adventure COMPILER -- turns .adv source into a .adi<br>**How:** Compiles ADVSYS .adv source into a .adi world for advint. No .adv source ships here either -- this pair is for writing adventures, not playing them. |
| `advent` | Colossal Cave Adventure -- self-contained, reads<br>**How:** Colossal Cave. Needs this disk as /dd -- it opens /dd/GAMES/adv/glorkz by absolute path, so mounted only as /h0 it cannot find its data. |
| `advint` | ADVSYS adventure INTERPRETER -- plays a .adi world file.<br>**How:** Plays an ADVSYS .adi world file. THERE IS NO WORLD FILE ON THIS DISK, so it has nothing to do until you write one with advcom. |
| `infocom` | Infocom Z-MACHINE interpreter -- a third, unrelated adventure<br>**How:** A Z-machine. Plays the .z3 files in /dd/GAMES/INFORM, which are Inform demonstration programs (dejavu, hellow, shell), not the Infocom games. |
| `infocom.tcap` | Infocom interpreter, termcap build<br>`Usage: infocom.tcap [-aehlnoprstvx] <filename>` |

**Chess utilities**

| | |
|---|---|
| `bincheckr` | check a GNU Chess opening-book file |
| `checkgame` | replay a saved chess game -- game <file> [start [end]]; 2nd build<br>`Usage: game file [start [end] ]` |
| `game` | replay a saved chess game -- game <file> [start [end]]<br>`Usage: game file [start [end] ]` |
| `postprint` | print a chess position as PostScript (GNU Chess) |

**Puzzles**

| | |
|---|---|
| `maze` | maze generator -- KNOWN BROKEN: goes dead |
| `mines` | minesweeper |
| `puz15` | the 15-puzzle -- same program as CMDS/puzzle15, built twice<br>`usage: puz15 [<width[x<height>]] puz15` |
| `puzzle15` | the 15-puzzle -- same program as GAMES/puz15, built twice<br>`usage: puzzle15 [<width[x<height>]] puzzle15` |

**Word & guessing**

| | |
|---|---|
| `animal` | guess-the-animal learning game<br>`Usage: animal {data-file}` |
| `bog` | Boggle word game<br>`Usage: bog [-b] [-d] [-s#] [-t#] [-w#] [+[+]] [boardspec]` |
| `hang` | hangman |

**Dungeon crawl**

| | |
|---|---|
| `hack` | hack -- the original dungeon crawl NetHack grew out of |
| `larn` | &#9733; larn -- dungeon crawl; see the PLAYGROUND note above |
| `ularn` | ULarn -- the larn variant, and its data is complete |

</details>

## Screen toys

*Things to watch rather than play. Start one and leave it going.*

<details><summary>6 programs</summary>

| | |
|---|---|
| `life` | Conway's Game of Life<br>**How:** life [init-file]. The patterns are in /dd/GAMES/LIFE -- try `life /dd/GAMES/LIFE/glider`. It also wants more memory than the default; from the OS-9 shell that is `life #22k <file>`, and bash has no #size syntax at all. |
| `rain` | raindrops screen effect |
| `suicide` | animation: a stick figure walks off a rooftop |
| `suicide1` | suicide, variant |
| `suicide2` | suicide, variant |
| `worms` | worms screen effect<br>`usage: worms [-field] [-length #] [-number #] [-trail]` |

</details>

## Amusements

*Generators, simulators and diversions that are not quite games.*

<details><summary>19 programs</summary>

**Simulations**

| | |
|---|---|
| `bio` | biorhythm chart (F. Kaefer 1987) -- BASIC09, needs runb<br>**How:** BASIC09 I-code, not 68000 code. `load runb` first, then run `bio` by BARE NAME. Giving runb a pathname instead raises BASIC09 error 43, which reads like a broken program and is not. |
| `england` | weather simulator - England (Gregorian/mid-Atlantic)<br>**How:** One of six weather simulators that differ only in climate and calendar: england, florida, georgia, minnesota, japan (Japanese calendar) and shire (Middle-earth). Each prints a day's weather and stops. |
| `florida` | weather simulator - Florida (Gregorian/Gulf) |
| `georgia` | weather simulator - Georgia (Gregorian/S-Atlantic) |
| `japan` | weather simulator - Japan (Japanese calendar/N-Pacific)<br>**How:** A weather simulator, not a calendar tool -- see `england'. It uses the Japanese calendar, which is the only reason it looks like one. |
| `logisim` | logic circuit simulator<br>**How:** Simulates a logic circuit described in a file. The format is in DOC/logisim/logisim.doc; there is no example circuit on the disk. |
| `minnesota` | weather simulator - Minnesota (Gregorian/N-Atlantic) |
| `nasa` | NASA orbital-element reader<br>**How:** The program that FEEDS orbit. Give it NASA two-line elements in a file called nasa.dat in the current directory and it writes kepler.dat, which is what orbit reads. Neither file ships -- you supply nasa.dat. |
| `shire` | weather simulator - the Shire (Middle-earth calendar)<br>**How:** A weather simulator using the Middle-earth calendar -- see `england'. |

**Generators**

| | |
|---|---|
| `name` | random name generator<br>`Usage: name number-of-names` |
| `newsgen` | generate a fake news bulletin |
| `pwgen` | random password generator<br>**How:** pwgen <length> [count]. With no arguments it prints nothing and exits, which reads as a hang and is not one. |
| `rndname` | random name generator<br>`Usage: name number-of-names` |
| `rpoem` | random poem generator (SNOBOL4-in-C) |
| `rstory` | random story generator (SNOBOL4-in-C) |
| `rstory2` | random story generator, second version (SNOBOL4-in-C) |
| `scales` | musical scale generator<br>`Usage: scales [-h] [-d] [-a] [-m] [-c] [outname]` |

**Curiosities**

| | |
|---|---|
| `areacode` | look up a US telephone area code<br>`Usage: areacode nnn nnn ...` |
| `touchtype` | typing tutor |

</details>

## System & modules

*OS-9 module and process tools, devices, system state and scheduling.*

<details><summary>32 programs</summary>

**Processes & memory**

| | |
|---|---|
| `aprocs` | &#9733; process monitor<br>`Syntax: aprocs [<opts>]` |
| `dpark` | &#9733; park a process<br>`Syntax:   dpark [/device]` |
| `launch` | &#9733; launch background process<br>`Syntax  : launch <opts> <shell> [shellargs...]` |
| `signal` | &#9733; send a signal to a process<br>`Syntax: signal <process-id> <signal-code> [<seconds>]` |
| `sysmax` | show maximum system memory |
| `sysmem` | show system memory use |
| `sysmin` | show minimum system memory |
| `sysmon` | &#9733; system monitor<br>`Syntax: sysmon [<opt>]` |
| `t` | tiny test/stub binary |
| `top` | show the busiest processes<br>`Syntax: top [<opts>] [<num>]` |
| `who` | 'who is logged in'.  Written in MICROWARE SHELL syntax |

**OS-9 modules**

| | |
|---|---|
| `bootgen` | generate an OS-9 boot file<br>`Syntax:   bootgen [<opts>] <device> {<path> [<opts>] }` |
| `flink` | list a module's links<br>`usage: flink [ -? \| filename { filename } ]` |
| `gen` | generate a C program/module/type source frame<br>`Syntax: gen [<opt>] <pathname> [<opts>]` |
| `mexist` | &#9733; test module existence<br>`Usage: mexist [options] <Module>` |
| `os9lib` | OS-9 support library module |
| `rtfdat` | RTF FORTRAN data module |
| `version` | show a module's version/edition |

**System state**

| | |
|---|---|
| `clock` | display a clock |
| `date` | Print date and time |
| `firq` | FIRQ utility |
| `loglist` | &#9733; log listing<br>`Syntax   : loglist [-option(s)]` |
| `oskversion` | report the OS-9/OSK version<br>`Syntax:   OSKversion` |
| `setime` | Set system time (prompts YYMMDDHHMMSS) |
| `sysid` | show system identification |

**Devices & disks**

| | |
|---|---|
| `dam` | display the disk allocation map -- dam [<drive>] |
| `dinfo` | disk/device information<br>`Syntax:   dinfo [<opts>] {<device name> [<opts>]}` |
| `shdev` | &#9733; show devices |
| `ssl` | show a file's segment list, sector by sector -- ssl <file> |

**Scheduling**

| | |
|---|---|
| `cron` | run commands at specified times (daemon) |
| `minute` | minute timer<br>`Syntax: minute[<opts>]` |

**Hardware control**

| | |
|---|---|
| `pow` | X-10 Powerhouse home control (needs /x1 hardware)<br>`syntax: x10 {[<opt>]}` |

</details>

## Disk & DOS

*Reading and writing MS-DOS media with the mtools set.*

<details><summary>20 programs</summary>

| | |
|---|---|
| `msattrib` | mtools 3.6 -- MS-DOS attrib (drive a: and b: are ready)<br>`Usage: msattrib [-p] [-a\|+a] [-h\|+h] [-r\|+r] [-s\|+s] msdosfile [msdosfiles...]` |
| `msbadblocks` | mtools 3.6 -- MS-DOS badblocks (drive a: and b: are ready)<br>`Usage: msbadblocks [-V] device` |
| `mscd` | mtools 3.6 -- MS-DOS cd (drive a: and b: are ready)<br>`Usage: mscd: [-V] msdosdirectory` |
| `mscheck` | mtools disk verifier.  A ksh script (#!ksh), and ksh |
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

<details><summary>10 programs</summary>

**Calendars**

| | |
|---|---|
| `cal` | &#9733; calendar<br>`Usage: calendar [<opts>]` |
| `calen` | calendar printer (v_misc) |
| `calendar` | reminder service - reads a calendar file |
| `calender` | print a whole year's calendar (German)<br>**How:** Prints the year in GERMAN. Not a typo of `calendar' -- a different program by a different author. |
| `digclk` | digital clock with hostname<br>`Usage: digclk [refresh_rate]` |
| `easter` | compute the date of Easter<br>**How:** Prints Easter dates for 1988 to 2000 and nothing else. The range is compiled in. |
| `setimex` | &#9733; set time from hardware clock<br>`Usage:` |
| `today` | date, moon phase and this-day-in-history |

**Astronomy**

| | |
|---|---|
| `ephem` | &#9733; ephem - astronomical ephemeris<br>`usage: [-c <configfile>] [-d <database>] [field=value ...]` |
| `ephem881` | &#9733; ephem, 68881 build<br>`usage: [-c <configfile>] [-d <database>] [field=value ...]` |

</details>

## Maths & calculators

*Calculators, plotting, orbits and number theory.*

<details><summary>11 programs</summary>

**Calculators**

| | |
|---|---|
| `gcl` | gcl - general calculation utility |
| `hc` | hex calculator |
| `loan` | loan/amortisation calculator |
| `rechne` | &#9733; RPN calculator |
| `rpn` | RPN calculator |
| `sc` | sc -- spreadsheet calculator (needs TERM)<br>`Syntax: sc [-c] [-r] [-m] [-n]` |

**Plotting & charts**

| | |
|---|---|
| `lac` | commodity price chart (tc suite)<br>`Syntax: lac {<opts>} [<file>] {<opts>}` |
| `main` | tc suite - main driver<br>`Syntax: plot [<opts>]` |
| `scope` | tc suite - scope display<br>`Syntax: scope [<opts>]` |
| `sin` | tc suite - sine plot<br>`Syntax: sin {<opts>} [<file>] {<opts>}` |

**Astronomy & orbits**

| | |
|---|---|
| `orbit` | satellite orbit calculator<br>**How:** Reads a bare "kepler.dat" from the CURRENT directory, so run it from where that file is: `chd /dd/DOC/orbit` first. Then it lists 21 satellites and asks which. |

</details>

## Printing

*Spoolers, page formatting and PostScript.*

<details><summary>8 programs</summary>

**Spooling**

| | |
|---|---|
| `lp` | line printer spooler - submit a job<br>`Syntax: lp [<opts>] {<path>}` |
| `lpq` | show the print queue<br>`Syntax: lpq [-p=dev] [user]` |
| `lprm` | remove a job from the print queue<br>`Syntax: lprm [-d=dev] [-] job..` |
| `lpshut` | shut down the printer scheduler<br>`Syntax: lpshut` |
| `perr` | &#9733; print an OS-9 error message<br>`Syntax: perr [<error_codes>]` |
| `prjob` | print a job |
| `qp` | queue/print helper<br>`Syntax: qp <cmd> <arg1> ... <argn>` |

**PostScript**

| | |
|---|---|
| `gs33` | Ghostscript 3.33 (needs gs_init.ps + fonts)<br>`Usage: gs ... -%c file.ps arg1 ... argn` |

</details>

## Documentation

*Pagers, readers and the help system.*

<details><summary>4 programs</summary>

| | |
|---|---|
| `help` | help system<br>`Syntax:   help [<opts>] [<topic> {<subtopic>}] [<opts>]` |
| `helpindex` | build the help index<br>`Syntax:   helpindex [<opts>] {<help file>} [<opts>]` |
| `less` | Pager (wants a real TERM) |
| `rdoc` | document reader |

</details>

---

&#9733; needs Microware's `cio`, which is not on the disk — `DOC/README-CIO` explains how to point at your own.

Generated by `tools/gen_catalog.py` from the disk's own documents. Do not edit by hand; it will be overwritten.
