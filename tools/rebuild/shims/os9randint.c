/* randint -- a random integer in [0 .. rng-1].
 *
 * tet's makefile links /dd/lib/rand.r for this, and that object is not on
 * this disk or in the archive pool.  The name survives only in a comment in
 * SRC/shuffle/xrand.c, whose own function is called rnd_ri.  One line of
 * shim is cheaper than hunting an object nobody kept.
 *
 * rand() comes from LIB/unix.l (SRC/unixlib/rand.c).
 */

extern int rand();

int randint(rng)
int rng;
{
    return (rng > 0) ? (rand() % rng) : 0;
}
