# For rdoggett

Terse on purpose. Rewritten 2026-08-27; everything before it is in git
(`git log --diff-filter=M -- notes/FOR-RDOGGETT.md`).

Branch `release-pass-2026-08-21`, 184 commits ahead of `main`, nothing pushed.
All eleven `check_disk.py` checks green. 870 of 916 programs run (95.0%).

## Nothing needs you right now

Both open questions were answered on 2026-08-27 and are done. All eleven
checks green, uncommitted.

## Closed

**`-qm` vs `-qixm`** — you were right that it is dictated, not a preference.
Measured: same source, `-qixm` writes **0** of 4000 characters and floods
"No more memory !!!"; `-qm` writes all 4000. `-qm` is the driver default now.
One correction to my own earlier note: it is NOT our version skew — it fails
with the SDK's own matched `csl` too. Whose bug it is stays unsettled and the
decision does not depend on it.

**gcc packaging** — the five files are installed in `disk/CMDS`
(`gcc_cccp2 gcc_cc2 gpp_cccp gpp_cc1plus gpp_collect`, 1.9 MB, byte copies of
what is already in `CMDS/GCC2`). `DOC/INDEX`, `DOC/README-GCC` and the star
grid updated. GCC139 deliberately not installed — its `gcc_cc1plus` would
collide with GCC2's.

**`wc`** — you said you do not have it. No copy to compare, no thread left.
Recorded in `DOC/INDEX` as unsettled and dropped.

## Not asking, just telling

- `~/Developer/os9/os9exec` has four modified files, uncommitted and deliberate.
  Untouched.
- `keep`/`drop`/`kept` are compiled modules now; your three bash scripts are
  kept at `SRC/keep/*.sh`. Reversible.
- `CLAUDE.md` is gitignored and I have edited it, so those edits are not in the
  branch you would review.
