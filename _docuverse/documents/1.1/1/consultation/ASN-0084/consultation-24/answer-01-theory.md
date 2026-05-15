## Question 1 [theory]

> Were cut-point rearrangements (pivot/swap) intended to apply only to the text subspace (S=1, where D-SEQ guarantees sequential V-positions without tombstones), or to all depth-2 subspaces including the link subspace (S=2) where sparse V_S(d) with tombstones is permitted?

REARRANGE was intended for the text subspace only, not for the link subspace.

Two pieces of evidence from my specification:

**1. REARRANGE explicitly transposes text.** From the FEBE protocol on 4/67:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." [LM 4/67]

The operand is "regions of text" — not arbitrary depth-2 spans.

**2. Links have permanent order-of-arrival addresses.** On 4/31:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

This is the deeper architectural reason. Bytes and links live in different addressing regimes:

- **Bytes** (the text subspace, in your S=1 framing): their order "may be continually altered by editorial operations" [LM 4/30]. This is why INSERT shifts following V-positions and REARRANGE can swap regions — the V-stream is a rearrangeable view over Istream.
- **Links** (your S=2): assigned serially at creation, address-stable forever. Deleting link N does not renumber N+1, N+2... — hence the sparseness you describe, and hence the tombstone-like state I called out on 4/9 ("DELETED LINKS... not currently addressable, awaiting historical backtrack functions") [LM 4/9].

A cut-point pivot/swap presumes a contiguous, sequentially addressed line that can be re-knit at the cut. The link subspace has neither property — link addresses encode creation order, which is historical fact, not a current arrangement. Rearranging them would falsify the record of when links were made and break every reference of the form `D.V.0.2.N` ("the Nth link of this document"). That violates the same permanence principle that lets links survive editing in the first place.

On your implementation terminology: I did not specify "D-SEQ," "tombstones," or "S=1/S=2." Those are downstream framings. But they map cleanly to the distinction I drew between byte addressing [LM 4/30] and link addressing [LM 4/31], and the asymmetry you describe is faithful to my design.

I did leave a door open on 4/31:

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." [LM 4/31]

That is about *subdividing* a link's address space (e.g., for facets, structure under a link), not about rearranging the serial order of links themselves. The order itself is fixed.

So: cut-point rearrangements apply to text. Links keep their order of arrival.
