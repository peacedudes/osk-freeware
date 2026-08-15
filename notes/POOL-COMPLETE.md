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

**A complete bulletin board**, RCIS -- 37 programs inside the file named
`rn.tar.Z`: `rcis`, `rchat`, `conference`, `rcbulletin`, `msgedit`, `tsmon`,
`watchdog`, `online`, `nodeon`/`nodeoff`, the user and message tools. This is
what an OS-9 machine ran when it answered the phone.

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

## What is NOT gathered

- **4 `.zoo` archives** -- `hl10obin/doc/src.zoo` and `unix.zoo`. No zoo tool
  is installed here. HL10 is also present as `.lzh`, so the loss may be nil,
  but it is unchecked.
- `nn` 6.3.10, `mnews` and `mg` are **source** distributions, not binaries.
- The pool is the Microware OS-9 Archive only. The disk's `DOC/ORIGINS` also
  credits the **hc disk** and a set of **usenet `.ar` archives**, and neither
  collection is held here in whole.
