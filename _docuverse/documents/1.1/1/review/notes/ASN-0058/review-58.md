# Review of ASN-0058

I checked the proofs for rigor and found the mathematical content solid: M-int, M12a/M12b/M12, M16a, C0, and C2 all hold under scrutiny, including the boundary cases (n=1 blocks, empty arrangement, k=0 shifts, j=u_m in C2). The remaining findings concern the anti-bloat patterns this note is flagged for — explanatory prose accreted around precondition/claim slots.

## REVISE

### Issue 1: M16a opens with a defensive justification of its own precondition
**ASN-0058, M16a (OriginInvarianceUnderShift)**: "The precondition `a + k ∈ dom(C)` is what places `a + k` in `origin`'s domain — S7 (ASN-0036) defines `origin` on `dom(C)` exactly."
**Problem**: This sentence does not advance the claim; it restates foundation-known information (origin's domain is dom(C)) to justify why a precondition is stated. It is the "why the precondition is needed rather than what it says" pattern. A precise reader already reads `a + k ∈ dom(C)` in the contract and must skip the gloss.
**Required**: Delete the sentence. The precondition stands on its own in the formal statement.

### Issue 2: M16's claim setup carries an embedded use-site applicability aside
**ASN-0058, M16 (CrossOriginMergeImpossibility)**: "Let `β₁ = (v₁, a₁, n₁)` and `β₂ = (v₂, a₂, n₂)` be blocks with `a₁, a₂ ∈ dom(C)` — **which holds, in particular, whenever both blocks belong to a decomposition of some `M(d)`, by B3 (Consistency) and S3 (ReferentialIntegrity, ASN-0036)**."
**Problem**: The em-dash clause interrupts the claim's hypothesis to inventory where the hypothesis is satisfied. This is a use-site note embedded in a claim slot — the reader following the proof setup must read past it. M16b's derivation already performs exactly this B3+S3 discharge at the point of use, so the applicability note is also redundant with its actual consumer.
**Required**: Drop the em-dash clause; let the hypothesis `a₁, a₂ ∈ dom(C)` stand. Application sites (M16b, the worked example) already establish when it holds.

### Issue 3: Worked example pre-empts a downstream obstruction with a forward pointer
**ASN-0058, Worked Example (Canonical Decomposition)**: "...the I-adjacency comparisons below operate within that common prefix **(M16's cross-origin obstruction does not arise here)**."
**Problem**: This example precedes M16 in the document; the parenthetical is a forward reference defending the single-source simplification against a complication introduced later. The single-source assumption already does the work — the reader needs no forward pointer to M16 to follow the merge/canonicality checks.
**Required**: Remove the parenthetical forward reference. The stated single-source assumption is self-sufficient for the example.

## OUT_OF_SCOPE

None — the Open Questions section already parks future territory (I-space discontinuity structure, lattice of decompositions, block-count bounds, depth relationships, multi-source reordering) without claiming it.

VERDICT: REVISE
