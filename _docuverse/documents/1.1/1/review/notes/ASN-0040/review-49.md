# Review of ASN-0040

## REVISE

### Issue 1: Stale T10a claim in B8 contradicts the revised B7

**ASN-0040, §Global uniqueness (B8 prose)**: "Across namespaces, B8 is ASN-0034's GlobalUniqueness specialized to allocator domains — discharged through B7, which is itself T10a.6."

**Problem**: B7 was revised to be proved *directly* from the canonical stream form, S1, T3, and the field-segment constraint — its own Depends line states "The proof is independent of T10a.6's allocator-tree framing," and B8's Formal Contract Preconditions list only B0★, B0a, B1, B4, and B7 (no T10a.6). The prose claim that B7 "is itself T10a.6" is therefore false after the revision. It is leftover content from the pre-revision dependency structure — a paragraph relocated rather than removed.

**Required**: Strike or correct the "which is itself T10a.6" identification. If a provenance note is kept at all, it must reflect that B7's disjointness is now self-contained.

### Issue 2: Co-reachability rationale stated three times

**ASN-0040, §Global uniqueness**: the same justification appears (a) in the B8 body — "The co-reachability scope is load-bearing, not cosmetic… an unconditional 'distinct acts ⟹ distinct addresses' claim would be false… never jointly observed"; (b) in the proof opening parenthetical — "(Acts on incomparable branches are excluded by the scope of B8: they share no reachable descendant, so their outputs are never jointly observed and the question does not arise.)"; and (c) in the Postconditions — "two baptisms on incomparable branches… may compute the same address, but are never jointly observed."

**Problem**: Three paragraphs in one section say the same thing in different words. "load-bearing, not cosmetic" is defensive meta-prose explaining why the scope is needed rather than advancing the proof. This is exactly the reviser-drift accumulation the anti-bloat mode flags.

**Required**: State the co-reachability scope once (in the contract), and let the proof simply handle the comparable case. Remove the duplicate rationale.

### Issue 3: B8 provenance essay does not advance the proof

**ASN-0040, §Global uniqueness**: "The genuinely new, registry-level content is the same-namespace clause… The foundation's per-allocator forward ordering relates indices to addresses; it does not by itself assert that distinct acts occupy distinct indices."

**Problem**: This is a use-site/provenance commentary about what the foundation does and does not do, duplicating the decomposition already given in the preceding paragraph ("Within the same namespace… Across namespaces…"). Two adjacent paragraphs partition the proof the same way; the second adds no reasoning step.

**Required**: Delete the provenance paragraph; the proof's Case 1 / Case 2 split already carries the content.

### Issue 4: Prose justifying document ordering in B6 necessity

**ASN-0040, §B6 necessity, sub-case (b) d = 1**: "the argument is self-contained in S2 and B7's disjointness target, with no appeal to the later B8."

**Problem**: This justifies *where the claim sits in the document* (non-circularity relative to "the later B8") rather than advancing the necessity argument. Flagged anti-bloat pattern: prose justifying ordering / forward-pointer non-circularity.

**Required**: Remove the clause; the argument either stands on S2 and the disjointness target or it does not, independent of B8's position.

### Issue 5: B4 decentralization essay, duplicated in B8

**ASN-0040, §Atomicity (B4)**: "This is precisely what enables decentralized baptism — two agents baptizing under different parents proceed independently, and their addresses are guaranteed distinct by the partition structure of the address space (T10)."

**Problem**: Essay content about what B4 enables, not what B4 states; the same same-namespace/cross-namespace point is restated in B8. The forward gesture to T10 adds nothing the B7 citation does not already supply.

**Required**: Keep the substantive content (B4's grain is per-namespace, via B7) and drop the decentralization essay.

### Issue 6: Meta-citation sentence in Bop

**ASN-0040, §The baptism operation (Bop proof)**: "We cite B_fin (§B_fin), B10 (§B10), and B1 (§B1) as the established invariants they are, holding at the precondition state s of any reachable transition."

**Problem**: Bop and its full correctness proof are placed *before* B1, B10, and B_fin are stated, so the proof opens by announcing it will forward-cite three downstream sections. This is forward-reference accretion: multiple deferrals to the same not-yet-stated results. The sentence describes the citation act rather than the argument.

**Required**: Either reorder so the invariants precede the operation that consumes them, or drop the meta-announcement and cite each result inline at the single point of use.

## OUT_OF_SCOPE

None beyond the topics the ASN already scopes out (ownership, parent-prerequisite chain, content storage, etc.). The B3 ghost-validity forward requirement is correctly parameterized over a future `Occupied` predicate and stays abstract.

VERDICT: REVISE
