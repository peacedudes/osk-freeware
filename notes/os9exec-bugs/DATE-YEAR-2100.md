# The current os9exec build reports the year as 2100

Found 2026-09-04.  On the shipped image under the os9exec at
~/Developer/os9/os9exec, `date' prints the correct day and time but the
wrong year:

    host:   2026-09-04 02:59
    OS-9:   September 04, 2100 02:59:52

rdoggett confirmed that an OLDER os9exec build reports the year correctly,
so this is a REGRESSION in the current build, not the disk and not OS-9.
There is no `setime' in SYS/startup or SYS/login; the disk sets no clock.

Where it is NOT: `Get_Time' in os9exec Source/OS9exec_core/utilstuff.c
computes `y = tim.tm_year + 1900' correctly (2026).  The year is mangled
downstream when the gregorian date word it returns from F$Time is packed or
decoded; not pinned to a line (left for the os9exec side).

Why it matters here: it is why `bio' rejects a RETURN-for-systemdate (it
computes an age from year 2100), and why several time programs' captures
show odd years.  These are artefacts of this emulator build, NOT the
programs, so the collection's reader-facing text must not describe a 2100
workaround as if it were inherent.  Use a good os9exec (or real OS-9) and
dates are right.
