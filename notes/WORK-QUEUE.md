# Work queue -- what is left of the 275, in order

Read the top unticked item, do it, tick it, go on. Written 2026-08-16 so that
"what next" is never a reason to stop.

## Decided ALREADY -- do not revisit

- [x] TeX (30) -- CMDS/TEXCMDS, formats built and typesetting verified
- [x] UUCPbb 2.1 (18) -- CMDS/UUCP
- [x] Elm 2.4 (14) -- CMDS/ELM; `elm` itself fails on the password entry
- [x] WN (6) -- CMDS/WN; blocked by an os9exec adapt_inetdb bug, diagnosed
- [x] ADL (4) -- CMDS/ADL, compiles and plays
- [x] terminals and transfer (10) -- CMDS/COMMS
- [x] 17 utilities and games into CMDS and CMDS/GAMES
- [x] Microware runtime (5) -- by permission

## To do

- [x] **C News** (6, mislabelled GNU_ATP) -- CMDS/NEWS
- [x] ~~GNU ATP 1.40~~ (6) -- news transport: dbz, newshist, newslock, bdecode,
      c7decode, byteflip. Licence: GPL (it says GNU).
- [x] **networking** (6) -- CMDS/NETWORK: KA9Q net, osknet, atp, msntp, finger, infoxpress -- KA9Q net (3 builds), osknet, msntp, finger, atp,
      infoxpress. All want a network; preserve, do not expect to demo.
- [x] **EFFO leftovers** -- 61 + 20 more taken across CMDS, GAMES, COMMS, UUCP -- forum4/5/6/7/11/13/15/16 utilities not yet taken.
      Check each for a data file it needs before installing.
- [x] **Blars UUCP** -- taken into CMDS/UUCP with its own USR/LIB/UUCP config -- a SECOND uucp implementation; decide
      whether it belongs beside UUCPbb or in REBUILT as an alternate.
- [ ] **RCIS** (37 programs + 81 BASIC09 modules) -- needs Microware's `runb`,
      which we have no permission for. Document; probably do not ship.

## Refused, with the reason -- do not add

- pbmexec (15) -- measured as unable to read PBM as it exists here
- KWIN LinkUp/Terminal/LaTerm -- shareware, distribution never stated
- rz, sz -- Omen Technology, $20/user
- smbmount, samba, smbdrv -- "not with other software packages"
- msfm -- Microware's, out of Dibble's OS-9 Insights

## Added 2026-08-19 -- the repair, documentation and archive pass

Everything below is on branch `repair-and-document`; see `notes/SESSION-LOG.md`
for the commit-by-commit record and `notes/PLAN-repair-and-document.md` for the
plan it followed.

- [x] **Fortran-77** -- the whole RTF suite works; it wanted `os9lib` loaded.
      Manual, sources and demos recovered from the pool.  DOC/README-FORTRAN
- [x] **SNOBOL4 games (5)** -- they wanted a syntax file, not a repair
- [x] **devprc** -- rebuilt; the archived module's body was corrupt
- [x] **Graph (7)** and **VMod_trap** -- both module names were lowercase and
      could never have matched on real OS-9; renamed, CRCs recomputed
- [x] **All 34 silent programs** -- every one now has a named cause
- [x] **A0-at-entry** -- answered from the v2.4 manual: `(a0) = undefined`
- [x] **Microware screening** -- `tools/screen_microware.py`; caught an
      `oskdefs.d` I had installed, and an `fpu` loose in a freeware archive
- [x] **ARR (65 archives)** and **the five never-assessed pool categories**
- [x] **Relink against cio** -- 117 programs, 1.46 MB reclaimed.
      `notes/RELINK-CIO.md`

- [ ] **The star list in DOC/INDEX.** 117 programs became cio-dependent in the
      relink, so the measured star list is out of date. A re-measurement was
      running when this was written: build an image with the five Microware
      modules removed and run every program against it, matching
      `**** Can't install trap handler ****`. Do NOT infer it from a `cio\0`
      string in the binary -- that is a proxy, and the number in DOC/INDEX has
      always been a measurement.
- [ ] **The 21 relinks that would not build.** 4 want `/dd/LIB/strings.r`,
      which is in neither the SDK nor the pool. 7 want headers missing from
      their own source trees (`parame.inc` and `lex.i` are nowhere in the
      pool). 7 want symbols the cio-linked library set lacks -- `bcopy`,
      `getpwuid`, `xmalloc`, `standby`; `clib.l` does not supply them.
- [ ] **ksh's interactive loop.** Partly diagnosed: `isatty` works (SS_Opt
      succeeds on paths 0 and 1), the shell writes and reads, and it scans
      directories -- `FHASHALL` is set alongside `FTALKING`. It still prints
      no prompt and runs nothing after 45 seconds. pdksh source: SRC/pdksh/sh
- [ ] **draw's quit key.** Its own help says `<esc>`; escape did not end it
      under try_quit.py. Recorded as unconfirmed.
- [ ] **The four G-Windows programs' licence.** Copyright line, no
      distribution statement. Recorded in SOURCES.txt for a decision.
