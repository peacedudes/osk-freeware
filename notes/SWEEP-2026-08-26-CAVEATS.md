# Reading the 2026-08-26 sweep -- two things that are NOT defects

## 1. `travesty` reads NOSTART and is fine

`travesty  CMDS  NOSTART  ... E_PNNF (216): '/dd/CMDS/travesty'` -- path name
not found. It was installed at 04:26 and the image the sweep runs against was
built before that. **The sweep classifies programs listed from `disk/` but
RUNS them from the image**, so anything added between the last `mkimage.sh`
and the sweep reads as missing.

Rebuild the image and re-run that one row. The same trap cost a whole exchange
earlier tonight, when the documented run command opened a five-hour-old
artefact.

**Worth fixing properly**: `verify_all.sh` could refuse to start when any
program under `disk/CMDS` is newer than the image, which would make this
impossible rather than merely documented.

## 2. Most of the NOSTART set are not programs

Running everything under `CMDS` bare means running things that are not
commands. These are correct refusals, not failures:

  - `math`, `math881` -- Microware's math trap handlers
  - `os9lib`, `X11R6shl` -- libraries
  - `vmod_trap` -- a trap handler
  - `keydrv.mm1`, `snddrv`, `rb37c65`, `msdrv*`, `scsi_mm1a`, `windio.52` --
    MM1 device drivers

`E_NEMOD (234)` is the kernel saying "this module is not executable", which is
exactly right for a driver or a library. `E_NORAM` and `E_BMID` from the MM1
drivers are the same story from a different angle.

A "broken programs" figure built from this file without filtering on module
type will be wrong, and wrong in the direction that makes the collection look
worse than it is. `tools/verify_filters.sh` and `verify_combine.py` are the
stages that sort this out; the raw file is not the answer.
