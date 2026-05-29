# Review of ASN-0053

## REVISE

### Issue 1: Displacement well-definedness claim omits the length condition
**ASN-0053, "The reach function"**: "the unique width w with a ⊕ w = b is the TumblerSub w = b ⊖ a (TumblerSub, ASN-0034). We call it the *displacement from a to b*. The displacement is well-defined when a < b and divergence(a, b) ≤ #a (D0, ASN-0034)."
**Problem**: This overclaims. D0 alone does not guarantee a width `w` with `a ⊕ w = b` exists — D0's own postcondition states `#a > #b → a ⊕ (b ⊖ a) ≠ b`. The existence of a `w` satisfying `a ⊕ w = b` is exactly D1, which requires `#a ≤ #b`; uniqueness is D2. As written, "the unique width w with a ⊕ w = b is b ⊖ a, well-defined when a < b and divergence(a, b) ≤ #a" is false whenever `#a > #b`. Every *use* in the ASN is level-uniform (`#a = #b`), so no downstream proof breaks — but the general statement introduced here is wrong.
**Required**: Add the `#a ≤ #b` condition and cite D1 (existence/round-trip) and D2 (uniqueness), not D0 alone. D0 governs only well-definedness of the subtraction and the failure direction.

### Issue 2: D1 precondition not fully discharged in S4(c)
**ASN-0053, S4 proof, (c)**: "Since #s = #p (level compatibility) and s < p, D1 gives s ⊕ (p ⊖ s) = p."
**Problem**: D1's preconditions are `a < b`, `divergence(a, b) ≤ #a`, *and* `#a ≤ #b`. The proof cites `s < p` and `#s = #p` but never states `divergence(s, p) ≤ #s`. It is true (equal length forces type-(i) divergence `k ≤ #s`), but it is the same step WF spells out explicitly and S4 elides. The same elision recurs in S5 ("By D1, s ⊕ d = p … since s < p and #s = #d = #p") and S11c.
**Required**: State the divergence bound once (equal length excludes the prefix case, so `divergence ≤ #s`) and reference it where D1 is invoked, matching WF's discharge convention.

### Issue 3: Essay content in structural slots (anti-bloat)
**ASN-0053, S2**: "The distinction matters: the result of intersecting two disjoint spans is the *absence* of a span, not a 'span of zero width.' These are categorically different — at our level of abstraction there are spans (non-empty, always) and the empty set (not a span, never)."
**ASN-0053, S1**: "The significance is topological: convex sets in a total order have convex intersection. The tumbler space's hierarchical structure cannot fragment an intersection — there is no configuration where two contiguous regions share a disconnected collection of positions."
**Problem**: Both paragraphs restate the just-proved claim in emphatic/essay form without advancing the argument. S2's paragraph repeats the claim body verbatim in different words; S1's "significance is topological" paragraph adds intuition but no reasoning the proof did not already establish. Per the anti-bloat classifier, this is prose the precise reader must skip past.
**Required**: Delete or compress to the operative fact (S2: the empty intersection is "no span," not a zero-width span — one clause). The proofs already carry the content.

### Issue 4: Redundant inverse-summary paragraph
**ASN-0053, after S3b**: "Together with S4a, this establishes that split and merge are exact inverses in both directions: split followed by merge recovers the original span (S4a), and merge followed by split at the original boundary recovers the original pair (S3b)."
**Problem**: This restates the two claim headers (S4a, S3b) without adding a derivation. It is a use-site summary, not a step.
**Required**: Remove; S4a and S3b already state their own conclusions.

## OUT_OF_SCOPE

### Topic 1: Span-set difference bound
The Open Question "Does the general difference bound extend to span-set difference?" is correctly deferred — `normalize(⟦Σ₁⟧ \ ⟦Σ₂⟧)` bounds belong to a future ASN.

### Topic 2: Cross-level intersection
Intersection of spans at different hierarchical levels (non-level-compatible) is explicitly excluded by the level-compatibility preconditions and flagged as an Open Question. Correctly out of scope.

VERDICT: REVISE
