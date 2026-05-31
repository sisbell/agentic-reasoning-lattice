# Review of ASN-0084

This ASN is mathematically rigorous: the pivot/swap postconditions, the bijection lemmas (R-PPERM, R-SPERM), commutation (R-COMM), the run-decomposition transform (R-BLK), and the canonicality argument (R-CANON) all check out, including the forward/backward-extension case analysis in R-CANON and the cross-subspace disjointness via T10. I found no correctness defects. The findings below concern accreted meta-prose flagged by the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: EXT-VAC leads with vacuous-satisfaction commentary the reader must skip past
**ASN-0084, "Consequences of R-PRE," Empty-exterior boundary cases (EXT-VAC)**: "R-EXT in both PivotPostcondition and SwapPostcondition quantifies over {v ∈ V_S(d) : v < c₀ or v ≥ c_{n−1}}, and either subset may be empty for boundary configurations of the cut sequence. When ord(c₀) = 1, no V-position satisfies v < c₀ ..., so the left-exterior subset is empty and R-EXT is vacuously satisfied on the left."

**Problem**: The load-bearing outputs of this paragraph are exactly two facts: (a) the left-exterior set is empty when ord(c₀)=1, and (b) `c_{n−1} ∉ V_S(d) ⟹ c_{n−1} ∉ dom(M(d))` — fact (b) is consumed in R-BLK Phase 1, fact (a) in the boundary worked example. The surrounding "either subset may be empty" / "R-EXT is vacuously satisfied on the left" framing advances no reasoning; it defends a postcondition clause against a non-issue. A reader chasing fact (b) must read past the vacuity commentary to reach it.

**Required**: Reduce EXT-VAC to the two derived emptiness facts and their citations; drop the "vacuously satisfied" defensive framing.

### Issue 2: Bidirectional pointer prose between R-BLK and R-CANON
**ASN-0084, end of R-BLK**: "B′ is therefore not necessarily maximal (see R-CANON)." **And R-CANON, Termination paragraph**: "R-CANON resolves the operational question left open by R-BLK."

**Problem**: Two adjacent lemmas point at each other to describe a division of labor ("not maximal, see X" / "X resolves what Y left open"). This is forward-reference accretion — the kind of cross-section deferral the classifier flags. The substantive termination/confluence content in R-CANON stands on its own; the "resolves the question left open by R-BLK" sentence is roadmap narration.

**Required**: Drop the mutual pointers. State R-BLK's output (a covering, disjoint, non-maximal partition) and let R-CANON state its hypothesis (a no-mergeable-pair partition) without narrating their relationship.

## OUT_OF_SCOPE

### Topic 1: Depth-2 text-subspace restriction appears unnecessary
The ASN scopes the text subspace to m₁ = 2 and builds the displacement arithmetic on the singleton-tumbler/ℕ identification. Yet R-CANON's preamble already operates the same OrdinalShift/TS2/TS5 machinery at arbitrary depth m > 2 for non-S runs. The restriction looks cosmetic — generalizing the text subspace to m₁ > 2 would reuse R-CANON's existing apparatus. Lifting it is future work, not an error here, but the asymmetry is worth recording.

### Topic 2: k-cut generalization, composition of rearrangements, and weakest-precondition characterization
The Open Questions (k > 4 cuts; whether composing rearrangements stays expressible as one; the wp of REARRANGE_K relative to R-PRE(iv) vs D-SEQ) are genuine extensions, appropriately deferred.

VERDICT: REVISE
