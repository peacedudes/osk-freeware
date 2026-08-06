# What is on this disk

614 programs of OS-9/68K community software, gathered from the archives that kept it and made to run again. **519 of them need nothing but this disk**; the rest want Microware's `cio`, marked below with a star.

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
| [Languages](#languages) | 3 | Interpreters and language systems beyond C. |
| [Archives & compression](#archives--compression) | 20 | Pack, unpack and shrink -- lha, zip, tar, arc, zoo, and OS-9 module libraries. |
| [Encoding & conversion](#encoding--conversion) | 16 | Between text encodings, line endings, number bases, ciphers and hashes. |
| [Communications](#communications) | 20 | Kermit in several builds, terminal sessions, and networking. |
| [Graphics & images](#graphics--images) | 189 | The netpbm toolkit, JPEG, a ray tracer, and things that draw. |
| [Games](#games) | 58 | Adventures, board and card games, arcade ports, dungeon crawls and puzzles. |
| [Screen toys](#screen-toys) | 6 | Things to watch rather than play. Start one and leave it going. |
| [Amusements](#amusements) | 18 | Generators, simulators and diversions that are not quite games. |
| [System & modules](#system--modules) | 32 | OS-9 module and process tools, devices, system state and scheduling. |
| [Disk & DOS](#disk--dos) | 20 | Reading and writing MS-DOS media with the mtools set. |
| [Time & calendar](#time--calendar) | 12 | Calendars, clocks and astronomy. |
| [Maths & calculators](#maths--calculators) | 11 | Calculators, plotting, orbits and number theory. |
| [Printing](#printing) | 8 | Spoolers, page formatting and PostScript. |
| [Documentation](#documentation) | 4 | Pagers, readers and the help system. |

## Shells

*The stock OS-9 shell is thin. These give you history, job control and a command line worth living in.*

<details><summary>16 programs</summary>

**Shell helpers**

| | |
|---|---|
| `checkenv` | &#9733; check env var |
| `exist` | &#9733; test file existence |
| `fc` | &#9733; re-execute history |
| `getenv` | &#9733; print an environment variable |
| `hist` | C-shell history + commandline editing  [no military use -- EFFO-INFO] |
| `if` | conditional execution for shell scripts (varval/loaded/def) |
| `paths` | show/expand the PATH |
| `printenv` | &#9733; print the environment |
| `printf` | formatted print from the shell |
| `run` | run a program with stdio rebound to the terminal (needs PORT) |
| `xc` | execute commands from a file (needs a .xc) |

**Shells**

| | |
|---|---|
| `bash` | GNU Bourne-Again Shell; runs, but warns about getwd and a missing .bashrc |
| `gshell` | GSHELL - a shell |
| `ksh` | &#9733; Public Domain Korn Shell 4.3 (edition 11, OS-9 port) |
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
| `VI` | PVIC, public domain            -> /dd/CMDS/REBUILT (name was taken) |
| `vi` | vi/ex editor (EFFO build, has its own ex_OS9.c) |
| `vi_cio` | &#9733; PVic vi, cio build (use vi_nocio instead) |
| `vi_nocio` | PVic 1.0a -- vi-compatible editor, cio-free (the vi to use here) |
| `vis` | make non-printing characters visible |

**Binary & hex**

| | |
|---|---|
| `beav` | BEAV 1.40 -- Binary Editor And Viewer (needs TERM) |
| `chbase` | &#9733; change module base |
| `hexed` | hex editor via your text editor  [no military use -- EFFO-INFO] |
| `hexedit` | Hex file editor -- hex [-vdr] file |
| `pbyte` | patch bytes in a file at a hex offset |

**emacs family**

| | |
|---|---|
| `emacs` | &#9733; MicroEmacs 4.00 |
| `emacs.mm1` | &#9733; MicroEmacs macro module |
| `me` | MicroEmacs 3.11 -- ADDED; needs TERM.  (memacs400 `emacs` needs cio) |
| `mg` | &#9733; MicroGnuEmacs |

**Line & stream**

| | |
|---|---|
| `ed` | &#9733; GNU ed 0.2 line editor |
| `editor` | GSHELL front-end for the editor |
| `sed` | sed - stream editor (verified: s/x/y/ substitution works) |

</details>

## Text tools

*Search, sort, compare, reformat, split and spell-check.*

<details><summary>71 programs</summary>

**Transform & filter**

| | |
|---|---|
| `ape` | APE - text filter |
| `autolf` | &#9733; auto-linefeed filter |
| `casefix` | normalise letter case in a text file |
| `cut` | cut selected fields from each line |
| `cuts` | Coco Usenet Transfer Utility |
| `detab` | &#9733; tabs to spaces |
| `deton` | detab - convert tabs to spaces |
| `eo` | eo - text utility |
| `field` | &#9733; extract fields |
| `fillup` | fill a file up to a given length with a constant byte |
| `gep` | global expression parser - grep-like filter |
| `paste` | merge lines of files |
| `pep` | file 'detergent' - strip junk from files |
| `psc` | &#9733; sc's print/format filter |
| `qt` | quick text utility |
| `rot` | rot-N text transformer |
| `shuffle` | shuffle lines/cards |
| `souper` | souper - text utility |
| `tabs` | tab/space conversion filter |
| `upperdir` | Normalise case: files lowercase, dirs uppercase |
| `valspeak` | Valley-speak text filter |

**Sort, compare & merge**

| | |
|---|---|
| `cdiff` | context diff |
| `diff` | GNU diff 1.1 -- ADDED; the disk had no diff at all.  Verified on CR files |
| `ediff` | visual file compare |
| `fcomp` | compare two text files |
| `join` | GNU join -- relational join of two sorted files |
| `nsort` | numeric sort |
| `qsort9` | &#9733; sort filter |
| `sort` | GNU sort |
| `spiff` | tolerant diff - ignores formatting noise |
| `unip` | unique lines with page numbers |
| `uniq` | &#9733; drop duplicate lines |

**Count & inspect**

| | |
|---|---|
| `ascii` | ASCII character table |
| `dump` | hex dump of a file or module |
| `file` | Identify file types (warns: no /dd/SYS/magic file -- still IDs OS-9 modules) |
| `gdd` | &#9733; data dump |
| `strings` | extract printable strings |
| `strings.cio` | &#9733; archived build, needs cio; superseded by the gcc2 rebuild |
| `tail` | &#9733; last lines of a file |
| `wc` | count lines/words/chars -- REBUILT HERE with gcc2; counts CR or LF lines |
| `wc.cio` | &#9733; archived build, needs cio; superseded by the gcc2 rebuild |

**Search & match**

| | |
|---|---|
| `bm` | &#9733; bm - fast grep utility (Boyer-Moore) |
| `bmgtest` | Boyer-Moore-Gosper substring search demo |
| `bmgtest2` | Boyer-Moore-Gosper substring search demo (variant) |
| `fgrep` | &#9733; very fast grep utility |
| `grep` | GNU grep 2.0 -- pattern search |
| `soundex` | Soundex phonetic key for each word on stdin |

**Fortune & sayings**

| | |
|---|---|
| `cookhash` | build the hash file cookie(1) needs, from a sayings file |
| `cookie` | print a random fortune cookie |
| `fortune` | print a random quotation |
| `sonnet` | writes (bad) sonnets in iambic pentameter, curses-based |
| `strfile` | build fortune's index file |
| `unstr` | reverse strfile - dump a fortune index |

**Spelling & words**

| | |
|---|---|
| `buildhash` | build ispell's dictionary hash (writes LIB/ispell.hash) |
| `ispell` | interactive spelling checker |
| `jargon` | Jargon-file browser (needs its database files) |
| `makelex` | compiles sonnet's lex.data word list into a C array |
| `speech` | English-to-phoneme translation |

**Format & typeset**

| | |
|---|---|
| `lout` | Lout 2.05 document formatter (Basser Lout, Jeffrey Kingston) |
| `nroff` | nroff text formatter -- setenv TMACDIR /dd/LIB first |
| `proff` | proff - portable roff text formatter (macros in LIB/proff) |
| `roff` | roff text formatter |
| `tformat` | text formatter (SNOBOL4-in-C) |

**Banners & text art**

| | |
|---|---|
| `banner` | print large banner text |
| `cursive` | generate a horizontal cursive banner |
| `gothic` | print text as a gothic/blackletter banner |

**KWIC index**

| | |
|---|---|
| `pagefraz` | KWIC suite - phrase extractor |
| `pagekwic` | KWIC suite - split a Stylo file to one phrase per line with page no. |
| `pageline` | KWIC suite - line/page numbering |

**Split & join**

| | |
|---|---|
| `sepwords` | split a file to one word per line |
| `splitalf` | split a file alphabetically |

</details>

## Files & directories

*Listing, copying, finding, renaming, and knowing what you have.*

<details><summary>31 programs</summary>

**Copy, move, delete**

| | |
|---|---|
| `cp` | &#9733; copy files |
| `dback` | Directory backup utility (wants a /d0 device) |
| `delbak` | &#9733; delete backup files (*_bak) in a directory tree |
| `eunlink` | &#9733; extended unlink |
| `move` | &#9733; move files between directories |
| `mv` | &#9733; move/rename |
| `remove` | remove files, with confirmation |
| `rm` | &#9733; remove files |
| `undel` | undelete a file |

**List & navigate**

| | |
|---|---|
| `dir` | &#9733; directory listing |
| `dm` | &#9733; disk/dir monitor |
| `edir` | &#9733; extended directory listing |
| `l` | &#9733; brief directory listing |
| `ls` | GNU ls (fileutils 3.13) -- OUR OWN FIXED BUILD: real stat(), columns, -al |
| `tree` | Print a directory tree -- BUT fails on this disk: it opens the raw |

**Find & compare**

| | |
|---|---|
| `dfiles` | find duplicate files on disk and issue the cmp commands |
| `du` | disk usage, by directory |
| `ff` | find files by name -- ff [<opts>] <name>... |
| `find` | find 1.1.5 -- search a directory tree |
| `space` | effective disk usage  [conditions apply -- run `help space`] |

**Paths**

| | |
|---|---|
| `basename` | strip directory from a pathname -- REBUILT HERE with gcc2 |
| `basename.cio` | &#9733; archived build, needs cio; superseded by the gcc2 rebuild |
| `dirname` | strip filename from a pathname -- REBUILT HERE with gcc2 |
| `dirname.cio` | &#9733; archived build, needs cio; superseded by the gcc2 rebuild |

**Attributes & ownership**

| | |
|---|---|
| `chgrp` | &#9733; change group |
| `chown` | &#9733; change owner |
| `eset` | &#9733; set file attributes |
| `owner` | &#9733; show file owner |

**Create & rename**

| | |
|---|---|
| `mkdir` | &#9733; make directory |
| `ren` | bulk rename files |
| `rendsk` | rename a disk volume |

</details>

## Developer tools

*Version control, tags, cross-reference, formatters, a debugger and benchmarks.*

<details><summary>28 programs</summary>

**Benchmarks**

| | |
|---|---|
| `disktest` | measure disk performance  [no military use -- DOC/EFFO-INFO] |
| `fibo` | Fibonacci benchmark |
| `float` | floating-point benchmark |
| `paranoia` | &#9733; floating-point benchmark |
| `savage` | Savage floating-point accuracy benchmark |
| `sieve` | sieve of Eratosthenes benchmark |
| `time` | time a command |
| `timeio` | time I/O operations |
| `timid` | timing utility |

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
| `cb` | &#9733; C beautifier |
| `cpr` | print/pretty-list C source files |
| `ifdef` | resolve #ifdefs in C source |
| `indent` | reformat a C source program for readability |
| `patch` | Larry Wall's patch - apply a diff |
| `unifdef` | remove #ifdef sections from C source |

**Source navigation**

| | |
|---|---|
| `ctags` | generate a vi tags file from C source (BSD) |
| `cxref` | &#9733; C cross-reference lister -- numbered listing + symbol table |
| `etags` | generate an emacs TAGS file |
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
| `cccp2` |  |
| `collect` |  |
| `compiler` | GSHELL front-end for the C compiler |
| `gcc` |  |
| `gcc2` |  |
| `gcc_cc1` |  |
| `gcc_cc1plus` |  |
| `gcc_cccp` |  |
| `gcc_collect` |  |
| `gpp` |  |

**Make & generators**

| | |
|---|---|
| `assembler` | GSHELL front-end for the assembler |
| `bison` | GNU bison 1.19 parser generator -- ADDED; skeletons in /dd/LIB |
| `dmake` | &#9733; dmake 3.70 - parallel make with its own makefile dialect |
| `flex` | lexical analyzer generator -- see DOC/flex/README-FLEX FIRST |
| `gmake` | GNU make -- ADDED (the gnu.bin build of make is the broken one) |
| `m4` | m4 macro processor |
| `make` | make - maintain and regenerate groups of files (verified: -? works) |
| `makeinfo` | GNU makeinfo -- Texinfo to info |
| `rtf` | RTF/68K FORTRAN compiler proper |
| `yacc` | yacc parser generator |

**Assemblers & linkers**

| | |
|---|---|
| `as0` | 68000 assembler (xasm) |
| `as09` | &#9733; 6809 assembler |
| `as1` | 68010 assembler (xasm) |
| `as11` | 68HC11 assembler (xasm) |
| `as4` | 68040 assembler (xasm) |
| `as5` | 68050 assembler (xasm) |
| `lnk` | module linker |
| `lnk.org` | module linker (original build) |
| `my.opt` | 68k assembly peephole optimiser |

**Other languages**

| | |
|---|---|
| `for` | RTF/68K FORTRAN compiler driver |

</details>

## Languages

*Interpreters and language systems beyond C.*

<details><summary>3 programs</summary>

| | |
|---|---|
| `forth` | &#9733; Forth interpreter |
| `wam.sbprolog` | SB-Prolog 2.2 WAM engine -- see DOC/sbprolog/README-SBPROLOG |
| `xlisp` | XLISP 2.1 Lisp interpreter |

</details>

## Archives & compression

*Pack, unpack and shrink -- lha, zip, tar, arc, zoo, and OS-9 module libraries.*

<details><summary>20 programs</summary>

**Create & extract**

| | |
|---|---|
| `ar` | archive librarian (Carl Kreider) -- .ar files |
| `arc` | third-party, no terms stated   -> /dd/CMDS/REBUILT (name was taken) |
| `cat` | concatenate files -- REBUILT HERE with gcc2 (archived cat needs cio) |
| `cat.cio` | &#9733; archived build, needs cio; superseded by the gcc2 rebuild |
| `lha` | LHa 2.08 -- create/extract .lzh archives |
| `lharc` | LHarc archiver |
| `marc` | MARC archiver |
| `shar` | Shell-archive creator |
| `tar` | GNU tar 1.10 |
| `unzip` | &#9733; Info-ZIP unzip |
| `zip` | Info-ZIP zip 1.9 |
| `zipnote` | Info-ZIP zipnote -- view/edit zip comments |
| `zipsplit` | Info-ZIP zipsplit -- split a zip archive |
| `zoo` | &#9733; zoo archiver |

**Compress a file**

| | |
|---|---|
| `compr` | file compressor |
| `compress` | compress/uncompress (LZW) -- ADDED |
| `gzip` | GNU gzip |

**OS-9 module libraries**

| | |
|---|---|
| `liborder` | order the modules in an OS-9 library |
| `modbuster` | Split merged OS-9 module files |
| `unpacklib` | split an OS-9 library into its modules |

</details>

## Encoding & conversion

*Between text encodings, line endings, number bases, ciphers and hashes.*

<details><summary>16 programs</summary>

**Text encodings**

| | |
|---|---|
| `atob` | ASCII-to-binary decode |
| `btoa` | Binary-to-ASCII encode |
| `chardef` | define a character set |
| `todos` | &#9733; OS-9 to DOS line endings |
| `toos9` | &#9733; DOS to OS-9 line endings |
| `uudecode` | &#9733; uudecode |
| `uuencode` | &#9733; uuencode |
| `uuexpand` | expand uuencoded text |

**Ciphers & hashes**

| | |
|---|---|
| `checksum` | file checksum |
| `chksum` | 32-bit file checksum |
| `crypto` | cryptogram puzzle solver's assistant |
| `des` | DES file encryption |
| `md5` | MD5 checksum |
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
| `aterm` | ATerm 2.6 -- terminal emulator |
| `cls` | clear the screen (termcap) |
| `connect` | connect to a serial line |
| `fkeys` | define terminal function keys |
| `initvdu` | &#9733; init video display |
| `input` | UNAXCESS BBS - input helper |
| `sbreak` | Send/clear an SS_Break signal on a serial path |
| `screen` | Screen multiplexer (needs HOME set) |
| `setfont` | load a downloadable terminal font -- setfont <path> |
| `setterm` | &#9733; set terminal type |
| `tsmon2` | tsmon replacement - terminal monitor |
| `udate` | UNAXCESS BBS - date display |
| `uwho` | UNAXCESS BBS - who is online |
| `wysecrack` | &#9733; Wyse terminal baud detect -- needs real Wyse hardware |
| `wysetime` | Wyse terminal time utility |

**Kermit**

| | |
|---|---|
| `ckermit` | &#9733; C-Kermit (cio build) |
| `kermit` | C-Kermit 5A(188) -- serial file transfer + terminal emulation |
| `kermit2` | Kermit file transfer (variant 2) |
| `kermit3` | Kermit file transfer (variant 3) |
| `xkermit` | &#9733; Kermit variant |

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
| `pbmtext` | netpbm image tool |
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
| `pnmscale` | netpbm image tool |
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
| `pbmtoascii` | PBM (bitmap) to ASCII art |
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
| `pbmtopk` | PBM (bitmap) to packed font |
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
| `hpcdtoppm` | PhotoCD to PPM (colour) |
| `icontopbm` | Sun icon to PBM (bitmap) |
| `ilbmtoppm` | IFF/ILBM to PPM (colour) |
| `imgtoppm` | GEM IMG to PPM (colour) |
| `lispmtopgm` | Lisp machine to PGM (greyscale) |
| `macptopbm` | MacPaint to PBM (bitmap) |
| `mgrtopbm` | MGR to PBM (bitmap) |
| `mtvtoppm` | MTV ray tracer to PPM (colour) |
| `pcxtoppm` | PCX to PPM (colour) |
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
| `sgitopnm` | SGI to PNM |
| `sirtopnm` | sir to PNM |
| `sldtoppm` | AutoCAD slide to PPM (colour) |
| `spctoppm` | Atari Spectrum to PPM (colour) |
| `spottopgm` | spot to PGM (greyscale) |
| `sputoppm` | Atari Spectrum to PPM (colour) |
| `tgatoppm` | Targa to PPM (colour) |
| `xbmtopbm` | X bitmap to PBM (bitmap) |
| `ximtoppm` | xim to PPM (colour) |
| `xpmtoppm` | XPM to PPM (colour) |
| `xvminitoppm` | xvmini to PPM (colour) |
| `xwdtopnm` | X window dump to PNM |
| `ybmtopbm` | ybm to PBM (bitmap) |
| `yuvsplittoppm` | yuvsplit to PPM (colour) |
| `yuvtoppm` | Abekas YUV to PPM (colour) |
| `zeisstopnm` | Zeiss confocal to PNM |

**JPEG**

| | |
|---|---|
| `cjpeg` | JPEG encoder (IJG) -- ADDED |
| `cjpeg.070` | JPEG compressor (68070 build) |
| `djpeg` | JPEG decoder (IJG) -- ADDED |
| `djpeg.070` | JPEG decompressor (68070 build) |
| `rdjpgcom` | read the comment from a JPEG file |
| `rdjpgcom.070` | read a JPEG's comment (IJG 0.70 build) |
| `wrjpgcom` | write a comment into a JPEG file |
| `wrjpgcom.070` | write a JPEG's comment (IJG 0.70 build) |

**Drawing & display**

| | |
|---|---|
| `bush` | draw a random bush/tree |
| `draw` | character-graphics drawing program |
| `loadmem` | load memory image |
| `pdraw` | Pdraw 1.4 - 2D/3D data plotting, PostScript output |
| `savemem` | save memory image |
| `snap` | snapshot the screen to a file |

**X11**

| | |
|---|---|
| `basicwin` | X11 demo - basic window (needs an X server) |
| `X11R6shl` | X11R6 shared library loader |
| `xengine` | X11 demo - engine animation (needs an X server) |

**Ray tracing & 3D**

| | |
|---|---|
| `mtst` | spline curve fitting - test driver |
| `rayshade` | ray tracer 4.0 -- RUNS but renders wrong; see DOC/rayshade |
| `rsconvert` | convert rayshade image output between formats |

</details>

## Games

*Adventures, board and card games, arcade ports, dungeon crawls and puzzles.*

<details><summary>58 programs</summary>

**Board & card**

| | |
|---|---|
| `back` | &#9733; backgammon -- '?' gives the built-in help |
| `blackjack` | Las Vegas blackjack (M. Theys) -- BASIC09; stops at line 8 |
| `blackjak` | blackjack -- from the SNOBOL4-in-C package, see below |
| `chess` | chess - 68k port (three engine versions built) |
| `crib` | cribbage |
| `cribbage` | &#9733; cribbage -- offers instructions before it deals |
| `gnuan` | GNU Chess analyser -- annotates a saved game move by move |
| `gnuchess` | &#9733; GNU Chess |
| `gnuchessc` | GNU Chess 4.0, curses display |
| `gnuchessn` | &#9733; GNU Chess (ncurses) |
| `gnuchessr` | &#9733; GNU Chess (raw) |
| `mille` | &#9733; Mille Bornes -- the French car-racing card game |
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
| `piano` | &#9733; play notes -- piano <base note> <note duration> |
| `stone` | stone -- a game, from the SNOBOL4-in-C package |
| `tess` | tesselation puzzle |
| `tt` | typing/terminal game |
| `vtxtcn` | world - build its text tables |
| `world` | World - text adventure |
| `zot` | Zot - arcade game |

**Arcade & action**

| | |
|---|---|
| `bite` | bite - small game |
| `greed` | Greed - grid game |
| `lander` | lunar lander |
| `pacman` | Pac-Man |
| `robots` | &#9733; robots -- outrun them until they crash into each other |
| `snake` | snake arcade game |
| `sokoban` | Sokoban puzzle |
| `tet` | Tetris |
| `wanderer` | Boulderdash-style maze game (SCREEN DATA MISSING) |

**Adventure & fiction**

| | |
|---|---|
| `advcom` | ADVSYS adventure compiler |
| `advent` | Colossal Cave Adventure |
| `advint` | ADVSYS adventure interpreter |
| `infocom` | Infocom Z-machine interpreter -- plays GAMES/INFORM/*.z3 |
| `infocom.tcap` | Infocom interpreter, termcap build |

**Word & guessing**

| | |
|---|---|
| `animal` | guess-the-animal learning game |
| `bog` | Boggle word game |
| `hang` | hangman |
| `joke` | print a joke |

**Chess utilities**

| | |
|---|---|
| `bincheckr` | check a GNU Chess opening-book file |
| `checkgame` | replay a saved chess game -- game <file> [start [end]]; 2nd build |
| `game` | replay a saved chess game -- game <file> [start [end]] |
| `postprint` | print a chess position as PostScript (GNU Chess) |

**Puzzles**

| | |
|---|---|
| `maze` | maze generator |
| `mines` | minesweeper |
| `puz15` | the 15-puzzle |
| `puzzle15` | the 15-puzzle |

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
| `life` | Conway's Game of Life |
| `rain` | raindrops screen effect |
| `suicide` | animation: a stick figure walks off a rooftop |
| `suicide1` | suicide, variant |
| `suicide2` | suicide, variant |
| `worms` | worms screen effect |

</details>

## Amusements

*Generators, simulators and diversions that are not quite games.*

<details><summary>18 programs</summary>

**Generators**

| | |
|---|---|
| `name` | random name generator |
| `newsgen` | generate a fake news bulletin |
| `pwgen` | random password generator |
| `reagan` | satirical speech generator |
| `rndname` | random name generator |
| `rpoem` | random poem generator (SNOBOL4-in-C) |
| `rstory` | random story generator (SNOBOL4-in-C) |
| `rstory2` | random story generator, second version (SNOBOL4-in-C) |
| `scales` | musical scale generator |

**Simulations**

| | |
|---|---|
| `bio` | biorhythm chart (F. Kaefer 1987) -- BASIC09, needs runb |
| `england` | weather simulator - England (Gregorian/mid-Atlantic) |
| `florida` | weather simulator - Florida (Gregorian/Gulf) |
| `georgia` | weather simulator - Georgia (Gregorian/S-Atlantic) |
| `logisim` | logic circuit simulator |
| `minnesota` | weather simulator - Minnesota (Gregorian/N-Atlantic) |
| `nasa` | NASA orbital-element reader |

**Curiosities**

| | |
|---|---|
| `areacode` | look up a US telephone area code |
| `touchtype` | typing tutor |

</details>

## System & modules

*OS-9 module and process tools, devices, system state and scheduling.*

<details><summary>32 programs</summary>

**Processes & memory**

| | |
|---|---|
| `aprocs` | &#9733; process monitor |
| `dpark` | &#9733; park a process |
| `launch` | &#9733; launch background process |
| `signal` | &#9733; send a signal to a process |
| `sysmax` | show maximum system memory |
| `sysmem` | show system memory use |
| `sysmin` | show minimum system memory |
| `sysmon` | &#9733; system monitor |
| `t` | tiny test/stub binary |
| `top` | show the busiest processes |
| `who` | 'who is logged in'.  Written in MICROWARE SHELL syntax |

**OS-9 modules**

| | |
|---|---|
| `bootgen` | generate an OS-9 boot file |
| `flink` | list a module's links |
| `gen` | generate a C program/module/type source frame |
| `mexist` | &#9733; test module existence |
| `os9lib` | OS-9 support library module |
| `rtfdat` | RTF FORTRAN data module |
| `version` | show a module's version/edition |

**System state**

| | |
|---|---|
| `clock` | display a clock |
| `date` | Print date and time |
| `firq` | FIRQ utility |
| `loglist` | &#9733; log listing |
| `oskversion` | report the OS-9/OSK version |
| `setime` | Set system time (prompts YYMMDDHHMMSS) |
| `sysid` | show system identification |

**Devices & disks**

| | |
|---|---|
| `dam` | display the disk allocation map -- dam [<drive>] |
| `dinfo` | disk/device information |
| `shdev` | &#9733; show devices |
| `ssl` | show a file's segment list, sector by sector -- ssl <file> |

**Scheduling**

| | |
|---|---|
| `cron` | run commands at specified times (daemon) |
| `minute` | minute timer |

**Hardware control**

| | |
|---|---|
| `pow` | X-10 Powerhouse home control (needs /x1 hardware) |

</details>

## Disk & DOS

*Reading and writing MS-DOS media with the mtools set.*

<details><summary>20 programs</summary>

| | |
|---|---|
| `msattrib` | mtools 3.6 -- MS-DOS attrib (drive a: and b: are ready) |
| `msbadblocks` | mtools 3.6 -- MS-DOS badblocks (drive a: and b: are ready) |
| `mscd` | mtools 3.6 -- MS-DOS cd (drive a: and b: are ready) |
| `mscheck` | mtools disk verifier.  A ksh script (#!ksh), and ksh |
| `mscopy` | mtools 3.6 -- MS-DOS copy (drive a: and b: are ready) |
| `msdel` | mtools 3.6 -- MS-DOS del (drive a: and b: are ready) |
| `msdeltree` | mtools 3.6 -- MS-DOS deltree (drive a: and b: are ready) |
| `msdir` | mtools 3.6 -- MS-DOS dir (drive a: and b: are ready) |
| `msformat` | mtools 3.6 -- MS-DOS format (drive a: and b: are ready) |
| `msinfo` | mtools 3.6 -- MS-DOS info (drive a: and b: are ready) |
| `mslabel` | mtools 3.6 -- MS-DOS label (drive a: and b: are ready) |
| `msmd` | mtools 3.6 -- MS-DOS md (drive a: and b: are ready) |
| `msmove` | mtools 3.6 -- MS-DOS move (drive a: and b: are ready) |
| `msrd` | mtools 3.6 -- MS-DOS rd (drive a: and b: are ready) |
| `msread` | mtools 3.6 -- MS-DOS read (drive a: and b: are ready) |
| `msren` | mtools 3.6 -- MS-DOS ren (drive a: and b: are ready) |
| `mstoolstest` | mtools 3.6 -- MS-DOS toolstest (drive a: and b: are ready) |
| `mstype` | mtools 3.6 -- MS-DOS type (drive a: and b: are ready) |
| `mswrite` | mtools 3.6 -- MS-DOS write (drive a: and b: are ready) |
| `mtools` | MS-DOS disk suite -- front end listing its sub-commands |

</details>

## Time & calendar

*Calendars, clocks and astronomy.*

<details><summary>12 programs</summary>

**Calendars**

| | |
|---|---|
| `cal` | &#9733; calendar |
| `calen` | calendar printer (v_misc) |
| `calendar` | reminder service - reads a calendar file |
| `calender` | print a whole year's calendar (German) |
| `digclk` | digital clock with hostname |
| `easter` | compute the date of Easter |
| `japan` | weather simulator - Japan (Japanese calendar/N-Pacific) |
| `setimex` | &#9733; set time from hardware clock |
| `shire` | weather simulator - the Shire (Middle-earth calendar) |
| `today` | date, moon phase and this-day-in-history |

**Astronomy**

| | |
|---|---|
| `ephem` | &#9733; ephem - astronomical ephemeris |
| `ephem881` | &#9733; ephem, 68881 build |

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
| `sc` | sc -- spreadsheet calculator (needs TERM) |

**Plotting & charts**

| | |
|---|---|
| `lac` | commodity price chart (tc suite) |
| `main` | tc suite - main driver |
| `scope` | tc suite - scope display |
| `sin` | tc suite - sine plot |

**Astronomy & orbits**

| | |
|---|---|
| `orbit` | satellite orbit calculator |

</details>

## Printing

*Spoolers, page formatting and PostScript.*

<details><summary>8 programs</summary>

**Spooling**

| | |
|---|---|
| `lp` | line printer spooler - submit a job |
| `lpq` | show the print queue |
| `lprm` | remove a job from the print queue |
| `lpshut` | shut down the printer scheduler |
| `perr` | &#9733; print an OS-9 error message |
| `prjob` | print a job |
| `qp` | queue/print helper |

**PostScript**

| | |
|---|---|
| `gs33` | Ghostscript 3.33 (needs gs_init.ps + fonts) |

</details>

## Documentation

*Pagers, readers and the help system.*

<details><summary>4 programs</summary>

| | |
|---|---|
| `help` | help system |
| `helpindex` | build the help index |
| `less` | Pager (wants a real TERM) |
| `rdoc` | document reader |

</details>

---

&#9733; needs Microware's `cio`, which is not on the disk — `DOC/README-CIO` explains how to point at your own.

Generated by `tools/gen_catalog.py` from the disk's own documents. Do not edit by hand; it will be overwritten.
