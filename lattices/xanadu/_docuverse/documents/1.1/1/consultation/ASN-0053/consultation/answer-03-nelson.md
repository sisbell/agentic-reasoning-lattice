## Question 3 [nelson]

> If two adjacent regions share a boundary, must the system guarantee they can be merged into a single contiguous region, and must that merged region be identical to one that was specified directly?

Yes. This follows from two properties Nelson explicitly specifies, though he never states the merge guarantee in those exact words.

## The Total Order Guarantee

The tumbler line is a total order — a depth-first linearization of the docuverse tree. A span is defined by two endpoints on this line, and its content is fully determined by those endpoints:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. **There is no choice as to what lies between; this is implicit in the choice of first and last point.**"
> — [LM 4/25]

This means a span [a, c] always designates the same content regardless of how you arrived at the endpoints a and c. The content is a function of the boundary, nothing else.

## The Normalization Guarantee

On page 4/37, Nelson explicitly addresses span-set reduction:

> "A spanset may be presented to the back end **with any degree of overlap** among the spans. This is because the system in effect performs a **boolean OR** to create a **normalized specset**, i.e. a **non-overlapping coverage of the same portion of tumbler-space**. Any overlapping specset can be reduced to a normalized specset."
> — [LM 4/37]

Two adjacent spans sharing a boundary point overlap at that single point. The boolean OR produces a single span covering the union. The normalization guarantee means the system treats {[a,b], [b,c]} and {[a,c]} as equivalent — they are the same "portion of tumbler-space."

## Why the Merge Is Identical to Direct Specification

Combining these two properties:

1. Two adjacent spans [a, b] and [b, c] share boundary b
2. Their boolean OR covers everything from a to c on the tumbler line
3. A single span [a, c] covers everything from a to c on the tumbler line
4. "There is no choice as to what lies between" — so both designate exactly the same content
5. The system normalizes them into the same non-overlapping coverage

The merged region **must** be identical to one specified directly, because spans are defined purely by their endpoints on a total order, and the content between any two endpoints is uniquely determined by the tree structure.

## A Subtlety: Future Content

Nelson notes that "a span that contains nothing today may at a later time contain a million documents" [LM 4/25]. This matters for the merge guarantee: the merged span [a, c] and the union of [a, b] ∪ [b, c] must remain identical even as new content is created between a and c. They do, because both are defined by the same endpoints on the same total order, and both include whatever the tree contains between those points at any moment.

## What Nelson Does NOT Address

Nelson does not discuss:
- Whether the **difference tumbler** representation of a merged span is always computable from the component difference tumblers (the arithmetic limitation on 4/39 — "there is no positive difference tumbler that will allow us to get BACK" — suggests some representations may require recalculation)
- Whether the normalization is performed eagerly or lazily
- The computational cost of normalization for large span-sets

The guarantee is semantic (the system treats them as equivalent) rather than a statement about representation efficiency.
