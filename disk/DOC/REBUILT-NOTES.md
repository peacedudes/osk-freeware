# Programs added from source — 2026-08-01

124 programs were built from the `/h2` archive corpus and the EFFO forum disks
and installed onto this disk. They meet the bar `DOC/INDEX` sets: **trap-free**
(`cc -qm`, never `-qixm`), so they need no `cio`, `math` or `csl` module.

Layout, matching what the disk already used:

- `CMDS/` — utilities
- `CMDS/GAMES/` — games, kept separate for discovery
- `CMDS/REBUILT/` — alternates that clash with a curated name (see below)
- `DOC/<name>/` — that program's own man page / README / help text
- `SRC/<name>/` — the C source it was built from, including its makefile
- `GAMES/<NAME>/` — per-game data files

All hardcoded `/h0/...` paths in the sources were rewritten to `/dd/...`, and
`/tmp` and `/r0` (which are OS-9 *device* names, not directories) to `/dd/tmp`.

## Four curated binaries were overwritten, and what was done

The installer's collision guard had a shell precedence bug and it replaced four
programs that were already on the disk. Recorded here because two of them could
not be put back exactly.

| program | what happened |
|---|---|
| `kermit` | **restored** — C-Kermit 5A(188), re-fetched from the Microware archive (`ckermit188.lzh`), 294542 bytes |
| `screen` | **restored** — re-fetched from the Microware archive (`screen`, MISC), 66654 bytes |
| `diff` | **NOT the original.** The disk had GNU diff 1.1; `diff.lzh` in the archive is source only, so the exact binary is gone. `CMDS/diff` is now our **GNU diff 1.4** build from the `/h2` corpus — functionally verified (correct `2c2 / < / --- / > / 3a4` output on a CR-terminated test pair). Source in `SRC/diff/`. |
| `ascii` | **NOT the original.** No provenance was recorded for it in `SOURCES.txt` or `DOC/INDEX` beyond "ASCII character table", and no archive copy was found. `CMDS/ascii` is now our build from the `misc` archive. Source in `SRC/misc/`. |

If the original `diff` 1.1 or `ascii` matter, GNU diff 1.1 source is available
as `diff.lzh` in the Microware archive (APPS, file id 3810) and can be rebuilt.

## `CMDS/REBUILT/` — alternates, not replacements

Programs whose name already exists in `CMDS/`. Left here so the curated disk
stays the author's call:

- `cpr` — "print C files"; the disk already has a `cpr`
- `kermit`, `screen` — our source builds, superseded by the restored originals

## Upgrades over `CMDS/NEEDCIO/`

These existed only as `cio`-dependent binaries and now have trap-free builds in
`CMDS/GAMES/`: **`advent`** (Colossal Cave), **`gnuchess`** (GNU Chess 4.0),
**`strings`**. The `NEEDCIO` copies are untouched.

## Known limitations

- `wanderer` — its screen data files are absent from every copy of the archive.
- `pow` — X-10 home control; opens `/x1`, which needs real hardware.
- `v_misc/xc` — wants a `.xc` control file in the working directory.
- Five SNOBOL demo programs (`blackjak` `poker` `rpoem` `rstory` `stone`) build
  but die at runtime with `Illegal instruction: 4afc` — a jump into a module
  header, i.e. a bad function pointer in their shared `pattern.c`. `rstory2`
  and `tformat` from the same archive are fine.


## wam.sbprolog -- replaced deliberately, 2026-08-01

The SB-Prolog archive shipped a prebuilt `wam.sbprolog` (71158 bytes) and we
installed that first.  It has now been replaced by our own build from the
sources beside it (72088 bytes), made with the tree's own OS-9 makefiles.

This is the one case where overwriting was the point rather than an accident.
Both binaries were run side by side, same queries, same environment, and
produced identical output down to the line breaks.  The replacement is the one
whose provenance is the source in `/dd/SRC/sbprolog`.

The prebuilt is not lost: it is still in the original archive.
