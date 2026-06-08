## Question 10 [theory]

> After an insertion, must the document remain a single coherent sequence with no gaps or overlaps in its positions, such that reading it end to end yields exactly the original content with the new material interleaved at the chosen point?

Yes. This is precisely the semantics Nelson specifies for INSERT, and it follows directly from the nature of the Vstream (the document's current arrangement).

## The INSERT Operation

Nelson defines INSERT so that inserted material lands at a chosen point and everything after it shifts to make room:

> "This inserts <text set> in document <doc id> at <doc vsa>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

The phrase "any following characters... are increased by the length of the inserted text" is the key. Nothing is overwritten, nothing is dropped, and the tail is pushed forward by exactly the insertion length. Reading end to end therefore yields the original content with the new material interleaved at the chosen position.

## Why No Gaps or Overlaps

The Vstream is, by construction, a **dense contiguous sequence**. V-addresses (virtual-stream addresses) describe the byte positions "in the current ordering of bytes":

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." (4/30)

Because each following character's address is increased by *exactly* the inserted length, the positions remain a single unbroken run — no two bytes share a position (no overlap) and no position is skipped (no gap). The "increase by the length" rule is what guarantees the arrangement stays coherent: it opens space of exactly the right size and slides the remainder over to fill the sequence perfectly.

## What Is and Isn't Preserved

It's worth distinguishing the two address spaces here, because the coherence holds for *positions* (Vstream) while *identity* (Istream) is untouched:

- **Vstream positions shift.** "Note that this order may be continually altered by editorial operations" (4/30). The same byte gets a new V-address after an insertion before it.
- **Istream content is unchanged.** Insertion adds new bytes to permanent storage but does not disturb existing content; "the front-end application is unaware of this" changing arrangement (4/11).

This is exactly why links survive an insertion: they attach to bytes (via permanent I-addresses), not to V-positions, so shifting the positions leaves them intact:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

## Summary

After an insertion the document must remain a single coherent Vstream — a gapless, non-overlapping sequence — and reading it end to end yields the original content with the new material interleaved at the insertion point. Nelson guarantees this through the rule that all following characters' V-addresses increase by exactly the inserted length (4/66), operating over a Vstream that is by definition the contiguous "current ordering of bytes" (4/30).

A note on scope: the curated sources establish the per-operation behavior of INSERT and the dense, contiguous nature of the Vstream, which together entail the "coherent sequence" property you describe. Nelson does not state this as a named global invariant in the curated material — it is an entailment of the INSERT definition plus the Vstream model, not a separately quoted axiom.
