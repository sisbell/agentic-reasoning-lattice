## Question 1 [theory]

> Does the tombstoning design require withdrawn interior links to remain at their original arrangement positions (leaving gaps), or is it satisfied by retaining the withdrawn link's permanent address while the arrangement layer is free to be gap-free?

## Answer

It is satisfied by **retaining the withdrawn link's permanent address** — and the premise that there is a separate "gap-free arrangement layer" for links to reconcile against is itself the thing to correct. Nelson's design does not give links a dense, rearrangeable arrangement layer the way it gives bytes one.

### Why the distinction matters

The question's two options come apart cleanly only for *bytes*. Bytes live in a Vstream arrangement that is dense and continually re-ordered by editing:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." (4/11)

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

Links do **not** participate in that dense, shifting arrangement. They are addressed by permanent order of arrival:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

The link address space is the 2.x subspace, ordered by creation:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" (4/31)

> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" (4/31)

Because links keep their creation-order addresses permanently, **deletion does not renumber subsequent links**. (As the curated `links` material puts it: "Deleting link `2.5` doesn't renumber `2.6` through `2.N`.") There is no compaction pass that would otherwise want to be gap-free. The "gap" left by a withdrawn interior link is inherent in the permanent address space and costs nothing to maintain — it is simply a number that is no longer currently addressable.

### What the tombstone actually is

A withdrawn link enters the explicitly-recognized state:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

That retained-but-not-currently-addressable address *is* the tombstone. It preserves:
- historical backtrack ("awaiting historical backtrack functions"),
- survivability of older versions ("may remain included in other versions"),
- the invariant that link addresses are never reused or shifted.

### Conclusion

The tombstoning requirement is met by retaining the link's permanent order-of-arrival address; it does **not** require some rearrangeable layer to hold a positional gap-marker. The reason is that links, unlike bytes, are never renumbered — so the permanent link-address space inherently carries the "position" (and the implied gap) without any gap-keeping in a Vstream-style arrangement. Conversely, the byte arrangement layer (which genuinely is dense and gap-free) carries no link tombstones at all, because withdrawn links are tracked in the permanent link address space, not in the byte Vstream.

One caveat on scope: "tombstoning" is an implementation term, not Nelson's. The above derives the answer from Nelson's stated invariants (permanent order-of-arrival link addresses at 4/31; the "DELETED LINKS … not currently addressable" state at 4/9; and the byte-only nature of Vstream renumbering at 4/11, 4/66). Nelson does not discuss interior-link withdrawal gaps in those exact terms, so the synthesis — not any single sentence — is what supports the conclusion.
