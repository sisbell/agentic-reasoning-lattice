## Question 1 [theory]

> Should ASN-0047's frame clauses for K.μ⁺, K.μ⁻, and K.ρ be amended to explicitly state `L' = L`, thereby promoting A1 to a derived substrate consequence — or is there a design-intent reason these three frames should remain silent on L?

Keep the frames silent on L. Link preservation under content editing is a **substrate property**, not an operational invariant — promoting A1 to a derived consequence is exactly right.

The architectural elegance I designed into Xanadu rests on a clean separation: bytes live in the 1.x subspace of a document, links live in the 2.x subspace. Content operations modify byte arrangements; they have no mechanism to reach into the link subspace. That separation is what makes survivability possible at all.

I made this explicit:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

And in the survivability diagram:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

The crucial passage is on tumbler addressing:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address... Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

Read that carefully: *"since the links are to the bytes themselves."* Link stability is not promised by the operations — it follows from where links point. Links target I-addresses; K.μ⁺, K.μ⁻, and K.ρ rearrange V→I mappings. The operations literally cannot mutate L because L lives in a disjoint address subspace and references content by identity, not arrangement.

Adding `L' = L` to the three frames would misrepresent the architecture. It would imply that link preservation is something the operations *choose* to do — that some other formulation of INSERT or DELETE might legitimately violate it. That isn't true. Any operation that mutated L while purporting to be content editing would be operating outside the substrate. The substrate makes it structurally impossible.

A1 should derive from two facts already in the substrate:
1. K.μ⁺, K.μ⁻, K.ρ act on V→I mappings in the byte subspace
2. Link records reside in a disjoint subspace and reference I-addresses

From those two, `L' = L` is theorem, not axiom.

The design intent is to let the addressing scheme carry the guarantee. That's why I built it this way — so that you don't need careful operational design to preserve links. The substrate does the work.
