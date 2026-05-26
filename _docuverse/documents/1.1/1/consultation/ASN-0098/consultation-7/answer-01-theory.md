## Question 1 [theory]

> What is the intended construction discipline for endsets that "refer to specific allocated content" — was the design intent that endset spans align with the allocator frontier so future K.α/K.λ emissions necessarily fall outside the span's reach, or something else that excludes future allocations from coverage?

# On Endset Construction Discipline

The question proposes a specific discipline (align endset boundaries with the allocator frontier so future K.α/K.λ emissions fall outside). My intent, as expressed in Literary Machines, is fundamentally **the opposite orientation** — spans are designed to be **content-blind boundaries**, not allocator-aware fences. Future inclusion was a feature, not a bug to be guarded against.

## What I actually specified

Spans are defined by their endpoints alone; their contents are not enumerated and **may change over time**:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." [LM 4/25]

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." [LM 4/24]

> "A span that contains nothing today may at a later time contain a million documents." [LM 4/25]

That last sentence is the architectural commitment: span coverage is **prospective**, not retrospective. I built this in so that the 1-positions could mean "all of" a level — "all versions," "all documents on this server," "the entire docuverse" [LM 4/38]. Embracing future allocations is the whole point of that machinery.

## On the "specific allocated content" case

For the narrower case the question raises — an endset that refers to particular bytes — the construction discipline I left implicit is simply: **choose tight endpoints**. Two endpoints around the bytes you mean. But I never wrote down a rule that endset boundaries must be tied to the allocator's current frontier, and the design pushes the other way:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

Survivability rests on the link reaching the **content identities** (I-addresses) it was bound to, not on excluding the address space's growth.

## What I flagged as a limitation, not a discipline

I did acknowledge one arithmetic asymmetry:

> "Starting from a given tumbler address, it may only be possible arithmetically to get to some places in the Docuverse — those notationally after that address." [LM 4/25]

This is a property of tumbler arithmetic, not a construction rule for endsets.

## Verdict on intent

I did **not** intend that endsets "refer to specific allocated content" by being braced against the allocator frontier. The whole span design refuses to know about what's inside. Whether a particular endset should be drawn so it cannot absorb future K.α/K.λ emissions is an **implementation-layer decision** about how a particular link type wants to behave — it sits below my specification, not within it.

If your formalization needs an endset variant whose semantics exclude future allocations, that is a layer you are adding. The Literary Machines specification gives you the primitive (boundary-defined spans) and leaves the discipline to the implementor.

NEED_RAW: 4/32-4/39 (the detailed span/spec-set treatment that the curated sources cite but don't quote in depth) — to confirm I didn't articulate an allocator-frontier discipline there that the curation missed.
