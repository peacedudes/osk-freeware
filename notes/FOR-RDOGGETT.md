# For rdoggett

Open questions only, two sentences each. Ask and I will explain any of them;
the detail of items before 45 lives in `notes/HISTORY-2026-09.md` under
the same number; 45-50 each have a staged tool that says what it does.
Updated 2026-09-24 (afternoon).

## Needs you

**1. Push os9exec, then pin `e2c7f7b'.**
It was `d992145'; `e2c7f7b' (2026-09-24) adds the two fixes boa and
whetstone need -- SS_Ready on a listening socket, and clock() counting a
process's own ticks -- and the os9exec session gated it.  The full suite
on it, as tester, is the last step before this collection's commit.

**45. Patch elm's user check (one instruction)?**  As any user but the
super-user, elm answers "You have no password entry!": it compares the
password file's user number with getuid(), which on OS-9 is the whole
group.user word, so the two never match.  tools/patch_elm_uid.py makes it
compare the whole word (6 bytes at 0x18738, CRC recomputed; it refuses any
other elm); tester's home files for it are staged.  Recommend: yes.

**46. Patch bash so a command it runs inherits paths 0-2 only (one byte)?**
The disk's bash hands every child all its open paths -- its own script,
its saved terminal copies, and a pipe a second time -- so the writer in
`cat file | head -n 1' never sees its reader go and waits for ever (the
os9exec session traced it; Microware's shell forks with three paths and
ends cleanly).  tools/patch_bash_forkpaths.py changes `moveq #31,d2' to
`moveq #2,d2' at $2B477 and re-seals the CRC; measured as tester, the
blocked writer is gone and 119 of 120 cases pass either way.  The one
thing it changes is a child reading a redirection of path 3 and up
(`5>file'), which already broke bash's own script.  Recommend: yes.

**47. Two more one-instruction patches of the same kind as 45: logname
and ELM's filter?**  Both mask getuid() to the user number and then ask a
getpwuid that compares the whole group.user word, so for anyone outside
group 0 logname says "no login name" and filter exits silently.
tools/patch_uid_mask.py fixes both (report-only unless told; checks the
bytes, recomputes the CRC); cases staged in Scraped/.../staged/uidmask.
ELM's fastmail and newmail have the same masked call but cannot be shown
failing here.  Recommend: yes, with 45.

**48. Give mw's module owner 0.0 (header only)?**  mw looks for a `games'
user, falls back to 90.90, and asks F$SUser for it; the kernel allows
that only to the super-user or to the module's own owner, and mw's header
says 30.95 -- left from the machine it was linked on.  So everyone but the
super-user gets "Can't setuid, please check File/Moduleowner!", and the
published card shows exactly that.  tools/patch_mw_owner.py sets the owner
to 0.0 and re-seals parity and CRC; no code changes.  Recommend: yes.

**49. Patch ELM's frm and newmail so they see a header end (one byte
each)?**  frm says "You have no mail." over a folder that elm, messages
and readmsg all read one letter from: it counts a message at the blank
line after its header, tested against LINE_FEED, which the port's own
defs.h makes a real LF under OSK -- an OS-9 blank line is a CR (the ELM
source is on the disk, SRC/infoxpress); tools/patch_elm_linefeed.py changes `cmpi.b #$0A'
to `#$0D' in both, and on a scratch image frm then lists the welcome
letter.  Recommend: yes.

**50. Patch smail so mail from a user outside group 0 is signed with their
name (one instruction)?**  smail signs every letter from anyone but the
super-user `From nobody': it stores the password file's user number
alone and compares it with getuid()'s whole group.user word -- 45's bug in
another program.  tools/patch_smail_uid.py loads the port's own whole-word
field instead (6 bytes at 0x2ca0, CRC recomputed); on a scratch image
tester's letter then says `From: tester@milkyway' and the super-user's is
unchanged.  Recommend: yes.

## No action, just so you know

**GitHub:** https://github.com/peacedudes/osk-freeware -- PRIVATE, created
2026-09-24.  The working branch is pushed and is the default there; `main'
is not, because a push to main starts CI, which needs os9exec's branch
published first.  History was rewritten before the push: the utilities
from your own archives and the oversized test transcripts are gone from
every commit and every message.  A pre-rewrite mirror is at
~/Developer/os9/Scraped/osk-freeware-git-backup-2026-09-24 -- delete it
when you are satisfied.


**Answered 2026-09-24:** 38 (harnesses run as tester -- done); 39 (both
gccs ship with source); 40 (k37 net replaces k35c, built from its own
source; K5JB's mailer is `bm', the Boyer-Moore grep is `bmg'); 41 (tass
ships, for a pre-2 MNews system; MNews pre-2 ships whole in SRC); 42
(the fonts were made with the disk's own METAFONT and ship; Vprint and
pc2os9 stay out); 44 (Notesfiles stays out).  Also: cards for the
programs left out; notes on every card we changed; programs useful on a
real system but untestable here now ship, marked untested; the utilities
from your own archives are gone from disk, docs, tools and notes, and
will be gone from history before the private GitHub push.


**3.** Nobody has tried this on real hardware, and the guides say so.

**43.** This Mac's data volume was at 99% (1 GB free) tonight; I cleared
20 GB of my own scratch images, but the drive itself is nearly full.

**7.** usenet-rewind is cancelled; access and the key last until 2026-10-14,
and nothing is lost either way.

**19.** The stray `GAMES/HACK/PLAYGROUND/save/0tester` stays, per your
"don't overdo it".

**Done 2026-09-23:** 36 settled (WebAssembly build committed in docs/try, disk.gz built by CI); 28 done (five READMEs reworded, gate widened).

**Answered 2026-09-23 (37):** ship `UAC_view`, leave `checksoa` out, ship
`ttcp`/`nslookup`/`nsquery` with the ISP static link recorded.
Earlier: 29-35.
