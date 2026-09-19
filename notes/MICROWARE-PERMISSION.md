# If we ask Microware for permission: what to cite

Assembled 2026-08-15 from the archive itself. Everything below is quoted from
files in Microware's own OS-9 Archive, with the path each came from, so a
request can point at precedent rather than argue from principle.

## What the modules are

Microware shipped two generations of C for OS-9/68000, and they have different
runtimes. That is the whole reason this set exists.

| | |
|---|---|
| **`cc` 3.2 and earlier** (K&R) | The C library lives in the **`cio`** trap module, with **`math`** for floating point. Almost every binary in this collection was built this way -- that is what the star in `DOC/INDEX` marks. |
| **Ultra C** (ANSI) | Replaced `cio` with **`csl`**, the C Shared Library. A program compiled under Ultra C will not run without it, and `cio` does not substitute. |

So `ucc_support` is the runtime a machine needs in order to **run** freeware
somebody compiled with Ultra C -- the OS-9 equivalent of a redistributable C
runtime. Its own readme says it plainly: *"If you already have Ultra C
installed on your system or are using OS9/680x0 v3.0 you do not need these
modules."*

The five 68k modules, read out of their headers:

| module | what it is | type | size |
|---|---|---|---:|
| `csl` | C Shared Library for the 68000 | trap handler | 47,192 |
| `csl020` | the same, for 68020/030/040 | trap handler | 43,794 |
| `fpu` | floating-point emulator, for a machine with no coprocessor | system module | 12,724 |
| `fpu040` | floating-point emulator for the 68040 | system module | 6,140 |
| `p2init` | installs a module as an OS9P2 kernel extension -- `fpu` has to be an extension, and this is what puts it there | program | 232 |

And two for OS-9000/386 (`ucc_support_386`): `csl` (45,714) and `fpuem`
(9,584), the x86 floating-point emulator. Those are OS-9000 modules -- their
header magic is byte-swapped from the 68k `4AFC`, which is how you can tell
them apart at a glance.

None of them replaces `cio` or `math`; the readme is explicit that 3.2-compiled
software still needs those.

## The precedent worth citing

**Microware has already permitted this exact set to be distributed publicly.**
`MISC/ucc_support_68k.uue` in their archive carries this readme:

> Ultra C support modules for for OS9/680X0 systems.
>
> The modules in this archive are copyrighted and are subject to the same
> License Agreement that appears on software distributed by Microware Systems
> Corporation. Use of these modules is restricted to running programs compiled
> under Ultra-C on OS9/680x0 systems.
>
> **Uploaded with permission of Microware Systems Corp.**

It was assembled by **Stephen Carville, High G Software**, Glendora CA -- an
author who also has five programs of his own in this pool (`cyberwar`,
`puzzle`, `tterm`, `lfmaker`, `scriptmaster`). So the precedent is: a community
member asked, and Microware said yes, for the purpose of letting people run
freeware.

**A second, stronger precedent, for `fpu` alone.** `TELECOM/xyz.lzh` carries
`fpu.doc`, whose first two lines are an outright grant:

> FPU - (C) 1995 Microware Systems Corp.
> Permission to distribute FPU is granted so long as this file is retained.

No condition beyond keeping the notice with it.

## Why this collection would ask

The disk ships 494 programs and **125 of them stop with
`**** Can't install trap handler ****`** because `cio` is not here. Every one
of those works the moment a user supplies their own. The collection is built so
that they can (`DOC/README-CIO`), and it does not ship Microware's modules.

The ask would be for permission to include, purely so the collection runs out
of the box for someone whose OS-9 licence is in a box in the basement:

1. **`cio`** and **`math`** -- what the 125 starred programs need.
2. **`csl`** / **`csl020`** -- what anything Ultra-C-compiled needs.
3. **`fpu`** / **`fpu040`** / **`p2init`** -- floating point on a machine with
   no coprocessor, and the installer that puts it in place.

Points that may help the case:

- Microware **already permitted 3 of those 6** to be uploaded publicly for this
  purpose, and granted `fpu` outright.
- The collection is non-commercial preservation and says so; it does not
  redistribute any Microware **product** -- no utilities, headers, libraries or
  compiler, and `DOC/INDEX` records that as policy.
- Every request is narrow: runtime modules only, and only so that
  community-written software from 1985-1996 still starts.
- The modules are useless without OS-9 itself, which remains Microware's to
  sell.

## Where the line is drawn today, without permission

| | |
|---|---|
| `fpu` from `xyz.lzh` | **May ship** -- explicit written grant, provided `fpu.doc` travels with it. **SHIPPED since 2026-09-12; the RIGHT COPY since 2026-09-19** -- 12,724 bytes, edition 12, md5 `3f5b0760`. What shipped in between was a 14,572-byte edition 5 out of `TELECOM/STerm68k.lzh`, which travels with no document; the commit that added it said it came from the granted archive and the hashes say otherwise. |
| `csl`, `csl020`, `fpu040`, `p2init`, `fpuem` from `ucc_support` | **`csl` and `csl020` ship since 2026-08-16 on Allan's answer, a separate route. The rest stays out** -- `fpu040` was on the disk from 2026-09-12 and came off 2026-09-19: no copy of it anywhere here travels with a grant. "Uploaded with permission" is permission for *that* upload; the modules remain under Microware's Licence Agreement by their own words. |
| `cio`, `math`, `math881` | **Stays out.** No grant found anywhere in the pool. |

One detail worth knowing before quoting sizes: the `fpu` in `ucc_support` and
the `fpu` in `xyz.lzh` are **both 12,724 bytes and are not the same file**
(md5 `ff75a069…` against `3f5b0760…`). The grant travels with its own copy.
And the loose `csl` found in `TELECOM/STerm68k.lzh` is byte-identical to
`ucc_support`'s -- the same artifact, escaped from its readme.
