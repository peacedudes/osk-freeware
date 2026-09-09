# Plan: visit every card again, to a higher bar

Hand this to a fresh session. It is self-contained. Read `CLAUDE.md` for the
rules and `notes/PLAN.md` for the build/test mechanics; you do not need the
rest of `notes/` or any prior chat.

---

## What this is

A curated collection of ~900 OS-9/68000 community programs, shipped as one
RBF disk image and published as a browsable gallery in `docs/` (built from
`tools/catalog.template.html` by `tools/gen_catalog.py`, with per-program
screen captures folded in by `tools/gen_screens.py`). Every program has a
**card**: a one-line description, a **Try it** command, a **See it run**
capture, a **Needs** line, a **keep** preview, and, folded under **Details
and provenance**, its own help text and provenance.

`disk/` is the maintained tree; `osk-freeware.dd` is a build artefact.

## Why you are here

A first pass gave every card a `try` line, a fresh capture, and a reviewed
caption. It was too uniform. rdoggett spot-checked two cards and both were
wrong:

- **gothic** captured only the bottom of its output (its blackletter word is
  264 lines tall and the grid was 90). Fixed by sizing the grid to the whole
  output. The lesson stands for any program whose output is taller or wider
  than one screen: **show the whole thing**, not a scrolled tail.
- **roff** showed, as "Its own help", three lines ending at `Options:` with
  no options under it. That text is scraped from the binary by a regex
  (`usage_of()` in `gen_catalog.py`). The program's real `-?` output --

  ```
  Syntax: roff {[+00] [-00] [-s] -[h] file}
  Function: format textfiles
  Options:
       +00       start at page 00
       -00       end at page 00
       -c        print table of contents
       -s        ????
       -h        use hardtabs
  ```

  -- appears nowhere on the card.

**The scraper is the sausage factory.** Any field filled by a mechanical
rule looks uniform and is individually wrong. rdoggett: *"look at each card
individually instead of pushing them through the same sausage factory."*

## The job

**Visit every card again -- all ~900, one at a time, not a spot check.** For
each program, the card must, by your own eyes on that program:

1. **Say what it is and does** in its one-line `DOC/INDEX` description --
   what the program is, not how to ask it for help, not a bare usage line,
   not ALL CAPS, not the author's name. The first-pass captions are a good
   starting reference but are not automatically right.
2. **Show its own real, complete help.** Run it and capture the actual help
   text -- for most OS-9 programs `program -?`, but this is a per-program
   judgement, which is the whole point:
   - Many answer `-?`; some want `-h`, `help`, `--help`, a bare run, or
     nothing.
   - Games, screen toys, editors, and stdin filters do **not** take `-?` --
     it launches them, hangs, or prints nothing. For those the "help" is
     whatever they genuinely print, or their `DOC/<name>` documentation, or
     an honest "it has no help; here is what it does" carried by the demo.
   - The help shown must be the program's **whole** help, never truncated
     mid-list the way `usage_of()` truncates roff.
3. **Show it running on real input**, its own output doing its own job (the
   existing `See it run` rules in `notes/PLAN.md` still hold: a `try` line
   with no full pathlists, an `os9` line where Microware's shell differs,
   a caption that describes for a stranger, the window sized to the whole
   output).
4. **Answer the keep question**: could a stranger, from this card alone,
   tell what the program is and decide whether to take it onto their disk?

## Do this first: fix the machinery, then the cards

The mechanical help scrape must be replaced before you re-card, or you will
be fighting it on every program.

- **Retire or rewrite `usage_of()`.** Decide where real help lives -- a
  regenerated `disk/DOC/USAGE`, or a new captured-help store -- and have
  `gen_catalog.py` read the program's **captured** help, in full, for the
  card's "Its own help" section. Never truncate a help block; if it is long,
  show it all (it is under a fold).
- **Write a help-capture tool** (sibling to `tools/os9try.py`): run a program
  with its help flag, `</dev/null`, with a timeout, capture the real output,
  and record which flag was used. It must be told, per program, which flag
  (or that the program takes none) -- a table you build as you visit each
  card, not a guess applied to all.
- **Prove it can fail** (this collection's rule): a check that the help shown
  on a card is the captured `-?` output and not a truncated scrape, made to
  fail once on a truncated example.

## The order of work

Go category by category through `tools/screenshots/*.sheet` (the twenty
sheets are the twenty categories). For each program, in one sitting: its
description, its captured help, its demo, its caption. Commit per category,
`check_disk.py` green every time (`CLAUDE.md`: you commit your own work).

The four categories whose descriptions were never improved last pass, do
first, because they are the worst: **text tools, text filters,
communications, graphics** (~230 programs). Then the rest.

## Traps, learned the hard way

- **Sonnet subagents stall on long emulator commands.** They do the analysis
  and stanza-writing well, then spawn an `until`/`sleep` waiter on a slow
  shoot and stop. Have a subagent write stanzas + `.edits` + a report and let
  the dispatcher run the real `tools/screenshots.py` shoots. A batch that
  only ran `probe_sheet.py` leaves **stale** captures (it saves nothing) --
  always finish with the real saving harness and verify capture mtimes.
- **Do not declare a category done without looking at its cards rendered.**
  Every "complete" last session was premature. Render cards in a browser
  (`docs/index.html`) and read them as a stranger.
- **`gen_catalog.py`/`gen_screens.py` regenerate from all captures at once**,
  so integrate a category only when no other batch is mid-edit, or its
  half-done state rides into your commit.
- **The tooling built last pass** is in memory `os9-sweep-tooling-2026-09-09`
  and works: the `try`/`os9`/`fold`/`burst` sheet directives, `os9try.py`,
  the page's bash/OS-9 shell switch, the keep preview, opt-in line folding,
  the logisim rebuild. Reuse it; do not rebuild it.

## Acceptance

A category is done when every one of its cards, read in the browser by
someone who has never seen the program, says what the program is, shows its
real complete help, shows it doing its own job, and leaves the reader able to
decide whether to keep it -- and when rdoggett can open any card in it at
random and not wince.

## Build and gate (from `notes/PLAN.md`)

```sh
rm -f disk/.DS_Store
OS9EXEC_DIR=~/Developer/os9/os9exec tools/mkimage.sh "$PWD/disk" "$PWD/osk-freeware.dd"
tools/check_disk.py disk          # every check green before every commit
tools/gen_screens.py              # fold captures into docs/screens.js
tools/gen_catalog.py disk         # rebuild the page from INDEX/categories/howto
```

Best-forgotten candidates and the open decisions are in
`notes/FOR-RDOGGETT.md`.
