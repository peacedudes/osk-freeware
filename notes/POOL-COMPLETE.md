# The gathering, finished

Written 2026-08-15. `notes/POOL-NEW-HAUL.md` describes the 152 recovered
archives and the 177 programs found in them; this is what came of finishing
the job across the whole pool.

## The pool is complete: 464 files

Three passes got it there.

1. **152 archives** restored the five categories that were entirely absent --
   DRIVERS, EFFO, GWINDOWS, NETWORK, TELECOM (`tools/refetch_archive.py`).
2. **32 more** found by comparing the archive's listing to the pool **by
   name**, across all eighteen categories (`tools/fill_archive_gaps.py`).
   Counting would have missed them and lied in both directions: GCC and GNU
   hold more locally than the site lists, so a count shows a surplus where
   there is a shortfall.
3. A **verification pass** then reported "nothing missing" for all eighteen
   categories and fetched nothing. The check failed once before it passed.

## Then the extractor turned out to be the weak link

133 pool files had never been opened by any earlier pass, because extraction
dispatched on the **file extension**. That was wrong 27 times
(`notes/pool-file-kinds.tsv`, from `tools/sniff_pool.py`):

| the file says | it actually is |
|---|---|
| `rn.tar.Z`, `KA9Q9501.gz`, `ptylev.zip`, `y2kit.tgz` | LHA archives |
| `elm24.lzh`, `cnews.tar.Z` | bare OS-9 modules -- both are `wermit`, C-Kermit |
| `rtclock1287.lzh`, `netpbm_cmds.lzh` | ZIP |
| `smbfm11t.zip` | gzip |
| `pd0.lzh`, `GNU_ATP_1_40.lzh` | compress |
| twelve files named `fileNNNN` | LHA and ZIP -- no extension at all, one of them 1.2 MB |
| `dvips.lzh`, `MNews.lzh`, `rn_4_3_blars.lzh`, `osknet.tar.gz`, `msntp_1..5.zip` | plain description text |

Those last ones are **not** failed downloads. The archive serves a paragraph of
description under an archive-looking name, and `rn_4_3_blars.lzh` is in fact
WN's unpacking instructions. **Pool filenames cannot be trusted for
provenance; only content can.** `tools/extract_pool.py` now sniffs magic bytes.

### OS-9 `ar` needed the collection's own `ar`

Nothing host-side reads Carl Kreider's `+AR0.0+` format. The disk ships two
readers, and the difference matters: **`ar` V1.2 answers "unknown compression
algo"; `ar2` V2.00 reads them.** `ar2` is starred, so it wants cio. The
extractor now runs `ar2` under os9exec with the target directory mounted as
`/h6` -- in-universe, the same way the disk populates itself with its own
`tar`. All 17 `.ar` archives opened.

Two traps cost a pass each and are worth keeping:

- **Judge success by what LANDED, not by what was printed.** Matching os9exec's
  stdout reported FAILED for three archives that had extracted perfectly well;
  its output carries NULs and escape sequences.
- `mnews.t.Z` has a stray block that makes bsdtar reject the whole archive.
  `tarfile(..., ignore_zeros=True)` reads all 200 members.

## What is actually there

`tools/inventory_pool.py`, over the fully-extracted pool
(`notes/pool-complete-inventory.txt`):

| | |
|---|---|
| distinct modules in the pool | **956** |
| already on the disk | 537 |
| **not on the disk** | **419** |

Of the 419: **274 programs**, 86 subroutine modules (library members out of the
`.ar` files), 25 descriptors, 12 drivers, 10 data, 5 system, 3 file managers,
3 trap handlers.

### The three finds worth naming

**A complete TeX system**, in `APPS/TeXSystem.lzh` -- an archive of archives,
which is why it had counted as one file and been invisible. `tex`, `latex`,
`slitex`, `initex`/`virtex`, MetaFont as `inimf`/`virmf`, `tangle` and `weave`,
`bibtex`, the font tools, and **ten DVI drivers** for different printers. It
ships an installation guide, a usage guide, and a LaTeX article describing
itself. **All 30 run trap-free**, and `dvips` came in with the DRIVERS
category. Fonts are not included -- the documentation is explicit that
MetaFont generates them.

**A complete bulletin board**, RCIS -- but read the caveat below it. 37
programs inside the file named `rn.tar.Z`: `rcis`, `rchat`, `conference`, `rcbulletin`, `msgedit`, `tsmon`,
`watchdog`, `online`, `nodeon`/`nodeoff`, the user and message tools. This is
what an OS-9 machine ran when it answered the phone.

**RCIS is mostly BASIC09, and that matters.** Of the 86 subroutine modules in
the pool that the disk does not have, **81 are RCIS and 83 of the 86 are
BASIC09 I-code** (type 0x02, language 0x02) -- `chaton`, `Doors`, `editusr`,
`bbslist`, `filexfer`, `Calcost` and the rest. So the bulletin board is not 37
programs; it is 37 programs driving 81 BASIC09 modules, and **the whole thing
needs Microware's `runb`** to do anything. That is a heavier dependency than
`cio`: `runb` is an interpreter, and it is not among the modules this
collection would ask permission for. Worth knowing before RCIS is counted as a
shippable feature.

**A Y2K kit** -- `fixyear`, `setyear`, `setime2`, from the file named
`file3988`, which had no extension and so was never opened.

Also: **GNU ATP 1.40** (news transport: `dbz`, `newshist`, `newslock`,
`bdecode`, `c7decode`, `byteflip`), two more **KA9Q net** builds, `msntp`,
`finger`, and a second C-Kermit build 272118 bytes -- the disk's `ckermit` is
`wermit` at 356040, so this one is genuinely different.

## Does it run?

Measured the same way throughout -- run bare on the freeware disk with no trap
handler present, then again with `cio`, `csl` and `math881` alongside.

| set | bare | with cio/csl/math | unsatisfiable |
|---|---:|---:|---:|
| 177 from the recovered categories | 69 | 102 | 4 |
| 53 from the newly-opened archives | 8 | 41 | 4 |
| 66 from the older categories (TeX among them) | 40 | 26 | 0 |

Nothing here is a pile of wreckage: the great majority runs, and the split
between "runs bare" and "wants cio" matches the disk's own 369/135.

## The EFFO Info form -- and the field that misleads

EFFO defined a structured metadata form, `Info_empty_form`, and shipped a blank
on every disk. 29 filled-in ones survive across the pool
(`notes/pool-effo-info-full.json`, `tools/parse_effo_info.py`).

**Two of its fields look alike and are not.** `$SOURCE-AVAILABILITY` says
whether the SOURCE can be had. `$AVAILABILITY` -- "Public, Shareware,
Commercial ?", mandatory -- is the one that speaks to redistribution, and
`$CONDITIONS` qualifies it. An earlier pass here read the first in place of the
second and concluded all 29 were unconditionally free.

They are not. On `$AVAILABILITY` all 29 do say public, freeware or public
domain -- but **seven carry a condition, and six of those are "no military
use"**:

| program | condition | on this disk |
|---|---|---|
| `space` (L. Zeller) | conditions in the help file prohibit military use | yes |
| `disktest` (St. Paschedag) | no military use | yes |
| `hist`, `hexed` (H. Hoheisel-Zimmermann) | no military use | yes |
| `rxmod`/`txmod` (W. Wittig) | no military use | no |
| `i_am_i` (C. Mahr) | no military use | no |
| **`help`** (L. Zeller) | peaceful applications only; no weapons work; **and `help.hlp` and `helpindex` HAVE TO be included when distributing** | **yes** |

`DOC/EFFO-INFO` on the disk already existed to record exactly this and had five
of the seven. `help` was missing, which mattered: it ships, and its condition 3
places a requirement on anyone who copies it onward. The disk does meet that
requirement -- `SYS/HELP/help.hlp` and `CMDS/helpindex` are both there -- and
`DOC/EFFO-INFO` now says so. Its counts went 27 to 29 and both missing entries
were added.

## Terms

Read by hand, per archive, and recorded per program in
`notes/pool-newcategories-gathered.tsv`. **111 of the 177 assessed carry no
licence statement at all** -- which is what this corpus is, not a gap in the
search. EFFO's 29 Info files all say public on `$AVAILABILITY`, but seven
attach a condition -- see above. Three things must
not ship: `rz`, `sz` (Omen Technology, $20/user) and `smbmount` (no bundling),
plus `msfm` (Microware's, out of Dibble's *OS-9 Insights*) and `csl`.

And one grant in the other direction: **Microware permits `fpu` to be
distributed**, in writing, so long as `fpu.doc` travels with it.

## Everything opened, and one more class of thing found

The four `.zoo` archives are open. Nothing host-side reads zoo either, so the
same answer served: **the disk's own `zoo`**, run under os9exec, next to `ar2`.
`tools/extract_pool.py` does both. They added **no new programs** -- and that
is now measured rather than assumed: all six modules in `hl10obin.zoo` are
byte-identical to the disk's, and the rest is C source.

Five more archives were hiding in the "plain text" bucket, found by looking
inside rather than at the magic bytes: `blackjack_68k.uue`,
`ucc_support_386.uue`, `ucc_support_68k.uue` (uuencoded), and `tar.shar` and
`mtp.shar`. The shars are read by `tools/`'s parser rather than executed --
they are shell scripts from strangers in 1990, and running one to see what is
in it is the wrong trade.

Final count: **961 modules, 422 not on the disk, 277 of them programs.**

### 176 alternates that name-matching was hiding

Asking "is this name on the disk?" quietly hides every *different build* of a
name already present. `tools/find_alternates.py` compares content, and finds
**176** (`notes/pool-alternates.txt`). Among them:

| module | on the disk | in the pool |
|---|---:|---:|
| `blackjack` | 6,524 -- BASIC09 I-code, in `CMDS/BROKEN` | 156,896 -- a 68k G-Windows game. **Not the same program at all** |
| `kermit` | 26,828 | 294,542 -- C-Kermit 188 |
| `gnuchess`, `gnuchessr`, `gnuchessn` | 97,762 / 66,152 / 101,652 | 200,116 / 174,148 / 203,136 -- the GNUCHESS 4.0 archive |
| `cc2`, `cc2plus`, `gcc2` | the disk's GCC2 | the **68060** builds |
| `hack` | 198,584 | 260,964 -- the EFFO pd6 build |
| `cp`, `tail` | 4,228 / 4,038 | 41,598 / 32,586 -- the full GNU builds |
| `sc`, `gawk`, `dmake`, `screen`, `sysmon`, `lout` | | different editions of each |

This is not a licence question and mostly not a "which is better" question --
`CMDS/REBUILT` exists precisely so an alternate can sit beside the curated
choice, and `notes/NOT-INCLUDED.md` already records that a different build is
**not** a reason to exclude. `blackjack` is the one that is not an alternate at
all but a separate program.

### Microware runtime modules, and where the line is

`ucc_support_68k.uue` holds `csl`, `csl020`, `fpu`, `fpu040` and `p2init`;
`ucc_support_386.uue` holds `csl` and `fpuem`. Its readme is explicit:

> The modules in this archive are copyrighted and are subject to the same
> License Agreement that appears on software distributed by Microware Systems
> Corporation. ... Uploaded with permission of Microware Systems Corp.

**Permission to upload there is not permission for us to redistribute**, and
the modules stay under Microware's agreement by their own words. These stay
out. That is a different thing from the `fpu.doc` in `xyz.lzh`, which grants
distribution outright -- and the two `fpu` builds are not even the same file
(same 12,724 bytes, different md5), so the grant travels with its own copy and
not with this one.

## The pass that should have come first: what is not a binary

Asked to check that the discarded really was worthless, the answer is that a
lot of it was not. Counting only OS-9 modules had quietly made everything else
"the rest".

Deduplicated by content across the whole extracted pool:

| kind | files | MB |
|---|---:|---:|
| **source** | 6,129 | 52.3 |
| OS-9 modules | 1,166 | 55.8 |
| plain text | 4,076 | 30.4 |
| documentation | 1,652 | 20.4 |
| binary/data | 1,657 | 18.1 |
| | **14,684** | **177.0** |

**5,034 unique source files -- 44.5 MB -- are not on the disk**, against the
1,834 files (16 MB) it carries in `SRC/`. Nearly three times again as much.
Where it lives, largest first: `osknet` (367 files), the X11R6 library (240),
**oleo 1.6** (217 -- the GNU spreadsheet), Elm 2.4 (272 across two archives),
GNU ATP (155), `OS9lib` (240 across two), macutils (113), stg v4 (112), `mg`
(110), `nn` (103), UUCPbb source (102), `mtp` (100), MicroEMACS 4.00 (96),
zoo 2.1 (77), libg++ (72), jpeglib 5a (72).

### And the "plain text" bucket was not filler

A sample of the largest, which is where the interesting things were hiding:

- **518 KB of `comp.os.os9`** on EFFO forum 22 -- Usenet articles 1078 to 1875,
  1990 to 1992, with a curated `hilites` index. Article 1078 is somebody asking
  whether TeX exists for OS-9/68000, which is the very package this pass found
  in `APPS/TeXSystem.lzh`. The newsgroup and the software arrived together.
- **`f_disks`** -- EFFO's own bilingual index of every forum disk it ever
  issued, in four editions as it grew.
- **376 `.mf` files** -- MetaFont sources, which is exactly what the TeX system
  needs and does not ship.
- 96 `.afm` font metrics, 46 LaTeX `.sty` files, gnuplot terminal drivers.
- `cookies` and `stquotes` -- fortune databases, 240 KB and 440 KB.
- `teapot.ray` -- the Utah teapot, for rayshade.

### The bucket labelled "binary/data" was two useful things

18 MB I had never characterised. It is mostly not opaque data:

- **831 `.r` files -- OS-9 relocatable objects.** The disk carries 18. These
  are link-ready compiled objects, the input to `l68`, and a module inventory
  cannot see them because they are not modules. 420 are `GCC/gclib.lzh` (the
  GCC library), then oleo (92), macutils (60), lout (40), JPEG (38), gdbm
  (28), less and gnutar (21 each). For anything that needs rebuilding, these
  save the compile.
- **TeX font material**, which corrects what this page said earlier. Not
  "fonts are not included": the pool holds **390 `.tfm`** metrics, **94 `.vf`**
  virtual fonts, **378 `.mf`** MetaFont sources and **16 `.pfb`** Type 1
  outlines. What is missing is the `.pk`/`.gf` bitmaps -- exactly the
  device-specific files the TeX documentation says MetaFont generates for your
  printer. The system is far more complete than "no fonts" implied.

The rest of that bucket is what it sounds like: `.gif`s, `.dat` files, a
rayshade scene, two PDFs.

### One more extractor gap, and two more programs

Nested `.tar` files had been left as empty `.x` directories: the first pass
dispatched on extension and its untar had no `ignore_zeros`. Re-running the
content-sniffing extractor over the staged tree opened **13 more archives** --
including a zoo nested in a forum disk and an `.ar` nested inside an `.ar` --
and turned up two more programs, `ltb` and `msterm`.

That is the third time widening a check has found something. It is the reason
to keep widening them.

### On splitting the disk

The numbers make the split you suggested straightforward rather than a guess:

| | |
|---|---|
| the disk today | 77 MB |
| all pool modules + documentation | ~76 MB |
| all pool source | ~52 MB |

So a **binaries-and-documentation** disk and a **source** disk are each
comfortably within the size the build already produces, and neither would need
to be trimmed to fit. Source and binary are also naturally separable audiences:
one wants to run the collection, the other wants to build or study it.

## What is NOT gathered

- Nothing, of the pool itself. Every one of the 464 files has been opened or
  identified: archives unpacked, modules read, text read, and two PDFs and a
  DVI that are what they look like.
- `nn` 6.3.10, `mnews` and `mg` are **source** distributions, not binaries.
- The pool is the Microware OS-9 Archive only. The disk's `DOC/ORIGINS` also
  credits the **hc disk** and a set of **usenet `.ar` archives**, and neither
  collection is held here in whole.
