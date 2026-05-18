## Question 16 [theory]

> When a document's content (or link) sub-allocator is first activated, is the first allocated address required by design to be the specific tumbler `[d.0.s_C.1]` (resp. `[d.0.s_L.1]`), or is the first emission deliberately non-deterministic within the subspace prefix?

# First Allocation Address: Deterministic, Not Non-Deterministic

The first allocated address IS required by design to be `.1` within the subspace prefix. The allocation is sequential and deterministic, not non-deterministic. This follows from Nelson's "permanent order of arrival" invariant.

## Evidence from Nelson

**For links** (4/31):
> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)"

> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)"

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document."

**For the forking mechanism generally** (4/20):
> "For instance, if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2."

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit."

**For V-stream byte positions** (4/11):
> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document."

## Why Determinism Is Required by Design

Three invariants Nelson establishes force the first emission to be `.1`:

1. **Order of arrival is encoded in the address.** The 755th link has address `.755`. The first link has address `.1`. If the first emission were non-deterministic, this correspondence would break — link `.500` might be older than link `.50`.

2. **Sequential forking is the only baptism mechanism.** Nelson's description on 4/20 shows new addresses are created by "successive new digits to the right" starting from `.1`. He describes no mechanism for skipping, randomizing, or reserving positions within a subspace.

3. **"Permanent order of arrival" is invariant.** Links keep their creation-order addresses permanently (no renumbering on deletion). For this to be meaningful, the first arrival must occupy `.1` — otherwise the ordering loses its reconstructable meaning.

## Conclusion

Both `d.0.s_C.1` (first content/byte) and `d.0.s_L.1` (first link) are the required first emissions. The design does not admit deliberate non-determinism within the subspace prefix — the forking/baptism mechanism (4/17, 4/20) describes only sequential allocation from `.1`.

NEED_RAW: 4/30-4/31 (raw pages 197-198) for verification of byte-subspace digit conventions (the curated sources show some apparent inconsistency between "1.x" notation and "after the one" phrasing for V-stream byte positions, which may merit direct inspection).
