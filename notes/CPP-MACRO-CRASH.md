# Microware's `cpp` takes a bus error on nested macro expansion

Found 2026-08-22 while writing a build recipe for `flex`. Minimal
reproduction and the two nearest non-crashing cases are in
`notes/cpp-macro-crash/`.

## What happens

    $ cpp crash5.c -o=out.m
    Error #000:102 (E_BUSERR) bus error TRAP 2 occurred

`cpp` is edition 37, from the SDK. The register dump is the giveaway:

    Dn=00000020 656E745F ...
    An=6D61785F ...

`$6D61785F` is ASCII `max_` and `$656E745F` is `ent_` — fragments of the
identifiers `current_max_dfa_size` and `current_...`. An address register
holding text means a pointer was overwritten with string data, which is a
fixed-size buffer being run past, not a resource running out.

## What it takes to trigger

`notes/cpp-macro-crash/crash5.c` is five levels of a macro that expands to two
copies of the level below it, with a twelve-character body:

    #define M0(x) { a = (x); }
    #define M1(x) { M0(x) M0(x) }
    ...
    #define M5(x) { M4(x) M4(x) }
    main() { M5(1) }

Neither half of that does it, which is what makes the bug awkward rather than
obvious:

| file                        | shape                          | result   |
|-----------------------------|--------------------------------|----------|
| `ok4.c`                     | same, four levels               | compiles |
| `ok5tiny.c`                 | five levels, body is `a;`       | compiles |
| `crash5.c`                  | five levels, twelve-char body   | **bus error** |
| a flat `#define` of 2000 characters      |                    | compiles |
| a `#define` continued over 8000 characters |                  | compiles |
| a chain of forty macros, each expanding to one |              | compiles |

So it is neither depth alone, nor expansion length alone, nor the number of
expansions — it is a nested expansion whose intermediate text passes some
size. Giving the process more memory (`cpp ... #512k`) changes nothing, which
rules out the stack and the heap.

## Whose bug it is

`cpp`'s. A fixed-size buffer overrun reproduces the same way on real hardware
— it would smash the same memory and take the same trap — and os9exec's part
in it is only to report it, which it does cleanly and with enough of a dump to
diagnose. Recorded here because rdoggett is exercising os9exec before
publishing, and because "the compiler died" is otherwise indistinguishable
from "the emulator died".

## What it costs this collection

`flex` is the one program known to hit it: `dfa.c` defines `STACK_STATE`,
which expands `PUT_ON_STACK` → `DO_REALLOCATION` and `MARK_STATE`, then
`CHECK_ACCEPT`, then `ADD_STATE` → `DO_REALLOCATION` again. The
`current_max_dfa_size` inside `DO_REALLOCATION` is the `max_` in the register
dump. `flex` therefore has no recipe; the shipped binary was built elsewhere.

A port could flatten those macros into functions. Nothing else in the
collection is known to need it, so nothing has been changed.
