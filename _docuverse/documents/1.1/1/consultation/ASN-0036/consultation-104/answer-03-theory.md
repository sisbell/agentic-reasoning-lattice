## Question 3 [theory]

> Is the prohibition on garbage-collecting unreferenced Istream content (even when no arrangement references it) an architectural commitment distinct from monotonic growth of the content store, or is it the same commitment stated with different emphasis — and if distinct, what specific reclamation behavior must the formal statement explicitly forbid?

**Same commitment, different framing.** Monotonic growth of the content store and the prohibition on garbage-collecting unreferenced Istream content are not separate commitments — removal *is* the negation of growth, so they coincide under my design. The append-only model is exactly what makes historical backtrack and link survivability possible:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes flow into the storage system, filed, as it were, chronologically." [LM 2/14]

**But for a formal statement, adopt the no-GC framing.** "Monotonic growth" can be read narrowly — as a property of the user-visible docuverse — while leaving room for "physical compaction that preserves logical identity." The no-GC framing closes that loophole. The commitment that matters operationally is: **the resolution function from I-address to bytes is total and time-monotonic. Once an address resolves to bytes, it always resolves to those same bytes.**

The formal statement must therefore explicitly forbid:

1. **Reference-counted reclamation** — removing Istream bytes because no current Vstream maps to them. Deleted bytes are "not currently addressable, awaiting historical backtrack functions" [LM 4/9] — note the word *awaiting*. They are dormant, not dead.

2. **Mark-and-sweep from current-version roots** — even when nothing live points to bytes in *this* document, "those bytes remain in all other documents where they have been included" [LM 4/11], and may be linked to or transcluded in the future.

3. **Mark-and-sweep from the union of all versions** — historical reconstruction must work for any past instant: "when you ask for a given part of a given version at a given time, it comes to your screen" [LM 2/15]. This requires keeping bytes that no *current* arrangement uses but some past arrangement did.

4. **Link-orphan reclamation** — even bytes that no link presently touches must be retained, because link survivability ("if anything is left at each end" [LM 4/43]) is a guarantee about *future* link-making as well as past.

5. **Cross-document orphan removal** — bytes not transcluded anywhere today must still resolve, because transclusion is a future capability of every Istream address, not a flag set at creation.

6. **Address invalidation under any name** — compaction, tombstone reaping, "logical deletion," archival migration that loses bytes, eviction on lapsed payment. Any operation whose effect is "an I-address that previously resolved now does not" violates the commitment, regardless of how it is dressed up.

The distinction worth preserving in the formal text is between *what the user observes* (their document shrinks under DELETE) and *what the store does* (nothing). DELETE is a Vstream operation that removes a mapping; it never touches Istream. The formal predicate I would want proved is something like: for all times t1 ≤ t2 and all I-addresses a, if `resolve_I(t1, a) = bytes`, then `resolve_I(t2, a) = bytes`. That single monotonicity-of-resolution property captures the commitment more cleanly than "the store grows."

One gap the curated sources flag, separate from GC: the disposition of content when storage rental lapses is not specified in *Literary Machines*. NEED_RAW: 5/11-5/13 if the formal statement needs to reconcile self-supporting services with the no-reclamation invariant.
