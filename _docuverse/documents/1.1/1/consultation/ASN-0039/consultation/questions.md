# Sub-Questions — Tumbler Baptism

**Inquiry:** What does it mean to baptize a new position in the tumbler hierarchy? What invariants govern the set of baptized positions across all levels?

1. [nelson] Must newly baptized positions always extend beyond all previously baptized positions at the same level, or can gaps in the position space ever be filled retroactively?
2. [nelson] What is the relationship between baptizing a position at one level of the hierarchy and the existence of a baptized position at the level above it?
3. [nelson] Can a position be baptized but never used — and if so, must the system distinguish between "registered but empty" and "never registered"?
4. [nelson] Does baptizing a position at any level carry a permanent commitment about the range of positions available beneath it for future baptism?
5. [nelson] If two independent acts of baptism occur at the same level of the hierarchy, what guarantees prevent them from producing the same position?
6. [nelson] Is there a design limit on how many positions can be baptized beneath a single parent position, or must the addressing scheme support unbounded growth at every level?
7. [gregory] What constitutes "baptizing" a tumbler position — is it the first successful allocation at that level via query-and-increment, or is there a distinct registration step that precedes allocation?
8. [gregory] Must baptism at a child level (e.g., `1.1.0.2`) be preceded by baptism of the parent position (`1.1`) — is there a strict hierarchical prerequisite chain?
9. [gregory] Is the set of baptized positions at any given level always a contiguous prefix (1 through N with no gaps), or can gaps exist between baptized positions?
10. [gregory] Does the `.0.` digit separator play a structural role in baptism (e.g., marking a level boundary that baptism must respect), or is it purely a conventional interpretation of an unconstrained digit sequence?
11. [gregory] Are there different baptism invariants for different hierarchy levels — for instance, do element-level positions follow different rules than the levels above them in the tumbler tree?
12. [gregory] Can two concurrent sessions race to baptize the same position, and if so, does the single-threaded event loop serialization fully prevent duplicate baptism, or is there additional guarding?
