# The five never-assessed categories, assessed

Written 2026-08-19. `notes/AUDIT-pool.md` said in as many words that nothing
in DRIVERS, EFFO, GWINDOWS, NETWORK or TELECOM had been looked at, and that
this included 36 EFFO forum and public-domain disks — where European OS-9
community software actually lived. It estimated 6,508 members and feared a
large backlog.

**Measured: 537 distinct modules across those categories, and only 65 are not
already on the disk.** The backlog is far smaller than it looked, and most of
the 65 are things this collection would not want.

Tool: `tools/list_new_modules.py`, repointed at the relocated pool. It
recurses, because the EFFO forum disks are archives of archives and a single
pass finds 8 modules where there are hundreds.

## What the 65 actually are

**Hardware descriptors and drivers — about 30, and useless without the
hardware.** Gepard, Atari, CT68000 and CT68020 machines: `d0`–`d11`, `db0`,
`db1`, `dstd0`, `dstd1`, `t2`–`t10`, `msdos0`, `r0_1m`, `h0_omti`, `msD1`,
plus drivers `fdc2793`, `fdc1772`, `hdc`, `wd2797`, `herterm`, `sthd_omti`,
`mth_ser`, `mth_8ser`, `gepterm`, and the `init` and `keytable` modules that
go with them. A device descriptor is a description of somebody's disk
controller. Nothing here can use them.

**Already refused, and the refusals still stand** — see `NOT-INCLUDED.md`:

  - `rz`, `sz` — Omen Technology, $20/user
  - `smbmount`, `samba`, `smbdrv` — "not with other software packages"
  - `linkup`, `ladial`, `laterm`, `terminal`, `gport`, `ansishow`,
    `audioplay`, `confer`, `send_break` — the KWIN packages, shareware with
    distribution never stated
  - `msfm` — Microware's, out of Dibble's *OS-9 Insights*

**WN's own example CGIs** — `counter`, `envi`, `doform.cgi`, `qr.cgi`,
`sample.cgi`. WN ships on this disk but does not run (the os9exec
`adapt_inetdb` defect); its examples add nothing while the server cannot run.

**And one that must never be taken.**

## `fpu`, found loose in somebody else's archive

`TELECOM/STerm68k.lzh` contains a module called `fpu` — **Microware's
floating-point emulator**, 14,572 bytes, a *different build* from the SDK's
12,848-byte copy.

That difference is the point. It is not byte-identical to anything in the SDK,
so neither content hashing nor line overlap would have caught it; it was
caught by name. `tools/screen_microware.py` now carries a named-module
denylist for exactly this shape — `fpu`, `fpu040`, `cio020`, `p2init`,
`sysgo`, `os9p1`, `os9p2`, `rbf`, `scf`, `pipeman`, `ioman` and the rest —
and the same tool explicitly exempts the five Microware DID give permission
for, so a later pass does not "fix" the disk by deleting them.

Microware's concern is source rather than binaries, but `fpu` is a product
they sell and the permission obtained covers `cio`, `csl`, `csl020`, `math`
and `math881` — not this. It stays out.

## What was worth taking, and was taken

Everything below came out of these categories during this pass:

  - **`ptxm`** — Nick Holgate's Path Table eXtension Module, from DRIVERS.
    Courtesyware. `ptxminst` was failing `E_MNF` looking for it.
  - **`vmod_trap`** — from EFFO forum 15, the SERLOAD utilities. `rxmod`
    was failing `E_PNNF` looking for `VMod_trap`, and the module's own name
    was lowercase, so it could never have worked on real OS-9. Renamed,
    CRC recomputed. Assembler source in `SRC/serload`.
  - **The G-Windows documentation** — `cyberwar`, `lfmaker`, `puzzle` and
    `scriptmaster` all shipped undocumented; their authors' readmes and
    manuals came from GWINDOWS. Licence position recorded in `SOURCES.txt`.
  - **`graph`'s documentation and source** — from EFFO forums 4 and 6, and
    it is what finally explained the bus error the seven Atari programs take.

## Still worth a look, not yet acted on

  - **`passwd`** (EFFO forum 5, `SPRACHEN/C/PASSWD`) — a C password utility
    with a `read_me`. Nothing on this disk covers it.
  - **`channel`** (EFFO forum 7, `RICO/S_PROLOG/TRAPHANDLER`) — a trap
    handler for the S-Prolog system.
  - **`osktag`**, **`readstr`** — small subroutine modules.
  - **`font_mono`**, **`germfont`**, **`p_convert`**, **`p1_convert`** —
    fonts and printer conversion tables for Gepard and Atari hardware.

## The honest summary

The five categories were not a hidden trove. They were mostly other people's
hardware. What they did hold was **two missing trap/system modules that two
shipped programs were failing to find**, and **documentation for six shipped
programs that had none** — which is a good return, but it is a different
finding from "274 programs we never assessed".
