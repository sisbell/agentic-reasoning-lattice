# Review of ASN-0086

## REVISE

### Issue 1: Misnamed reference to S7c

**ASN-0086, "Shared depth-1 element-field allocator commitment"**: "(iii) S7c (DocumentArrangementSlot, ASN-0036), together with S7d's zero-count constraint, fixes the structure of allocations directly under a document"

**Problem**: Per the foundation vocabulary, S7c is "ElementFieldDepth" (the axiom `#E(a) ≥ 2`), not "DocumentArrangementSlot". The name "DocumentArrangementSlot" does not appear among ASN-0036's S-invariants. The actual ASN-0036 axiom that says element-field depth ≥ 2 cannot, by itself, "fix the structure of allocations directly under a document" or specify that the depth-1 slot is for subspace identifiers — that claim derives from L0 (subspace_I = a.E₁) plus the address structure, not from S7c.

**Required**: Correct the citation. If the intended structural claim is "the slot enumerated at element-field depth 1 is for subspace identifiers," attribute it to L0 (which actually routes addresses by their first element-field component). If a different S-invariant is meant, name it. This same error appears in the "Reconciliation with Nelson's design" paragraph and the dependency tracing.

### Issue 2: R7 Step 3 conflates the substrate primitive with Emit_K

**ASN-0086, R7 Step 3 (closure)**: "every relational-layer state-affecting transition is a class-(iii) `→`-step, and every class-(iii) `→`-step is by definition an `Emit_K` call (the Definition of Emit_K above, which fixes the construction at R0 Step 2's sibling-frontier address). No additional operation exists."

**Problem**: Class-(iii) and Emit_K are not equivalent. The substrate emission primitive (defined in Setup) admits class-(iii) transitions at *any* L1c-conforming fresh address — including strict prefix-extensions of existing link addresses (e.g., `a' = a₁.1`), as the note itself acknowledges in "Breadth of the primitive vs. the discipline R0a names." Emit_K's Definition is a *restriction* of this primitive to R0 Step 2's sibling-frontier construction. Identifying them ("every class-(iii) `→`-step is by definition an `Emit_K` call") is incorrect: a class-(iii) step initiated by direct invocation of the substrate primitive at a strict prefix-extension is *not* an `Emit_K` call. The argument is question-begging — Step 3 needs to assume "the relational layer only initiates class-(iii) transitions through Emit_K" to conclude what it claims.

**Required**: Scope the closure conclusion to relational-layer-initiated transitions. Replace with: "every class-(iii) `→`-step initiated at the relational layer is, by definition of the relational-layer operation set, an `Emit_K` call (or `Nullify`, which reduces to `Emit_R`); the substrate primitive's broader range of admissible class-(iii) addresses is not exposed at the relational layer." This makes the scope explicit and aligns with the careful tracking of discipline-conditionality elsewhere in the note.

### Issue 3: Forcing argument for the shared allocator commitment hand-waves

**ASN-0086, "Shared depth-1 element-field allocator commitment"**: "This commitment is *forced* by the conjunction of three foundation properties; no alternative is admissible."

**Problem**: The argument lists three points but does not fully derive the shared-allocator structure from them. Specifically: (a) the alternative refuted ("each per-subspace allocator's enumeration would have to start at a different prefix of `d`, but `d` has only one immediate child position") relies on T10a's at-most-once for `(d, 2)`, but does not explicitly rule out the case where a single `(d, 2)` spawn opens multiple sub-allocators; (b) point (iii)'s citation to S7c is misnamed (per Issue 1), and the structural claim "the slot enumerated at element-field depth 1 is for subspace identifiers" is informal — the actual mechanism is L0's routing convention; (c) the argument shows the shared structure is *consistent with* the cited invariants but does not formally exclude alternatives. "Forced... no alternative is admissible" is stronger than what the three-bullet argument delivers.

**Required**: Either tighten the derivation with explicit case-elimination of structural alternatives, or relax the claim to "consistent with the foundation invariants and adopted as a model commitment." The current treatment overstates the necessity.

### Issue 4: No concrete tumbler-level failure example in "Failure modes"

**ASN-0086, "Failure modes — necessity of the discipline"**: "Suppose Σ → Σ' is a class-(iii) transition that invokes the substrate emission primitive at a strict prefix-extension of some `a₁ ∈ dom(Σ.L)` — concretely, at `a' = a₁.1`..."

**Problem**: The failure modes are argued abstractly without exhibiting specific tumbler values. The worked sketch shows R0a holding for the discipline-compliant case (a₁ = 1.0.1.0.1.0.2.1, b₁ = 1.0.1.0.1.0.2.2, a₂ = 1.0.1.0.1.0.2.3); a parallel concrete example showing R0a breaking under a hypothetical non-disciplinary emission would strengthen the necessity claim. The worked sketch establishes precedent for tumbler-level invariant verification, and the failure-modes section drops to abstract argument without similar specificity.

**Required**: Add a concrete tumbler-level failure example. E.g., from Σ_1 with `dom(Σ_1.L) = {a₁, b₁}` as in the worked sketch, exhibit a non-disciplinary class-(iii) step emitting at `a' = 1.0.1.0.1.0.2.1.1` (a strict prefix-extension of a₁, satisfying L1c via the same depth-2 allocator extended by `inc(a₁, 1)`). Verify directly that `a₁ ≼ a'` and `a₁ ≠ a'`, breaking R0a at Σ', and that subsequent disciplinary emissions cannot repair the bad pair. This concretizes both the failure mechanism and its irreversibility.

### Issue 5: R0a's antichain corollary's "second zero coincides" phrasing is underspecified

**ASN-0086, R0a, Case 2 sub-argument**: "the first three zeros of `a'` all sit at positions within `a`; in particular `a'`'s second zero coincides with `a`'s second zero, so `home(a') = home(a) = d`"

**Problem**: home(a) = N(a).0.U(a).0.D(a), whose length extends to position z₃ − 1 (where z₃ is the third zero). Coincidence of just the second zero is insufficient to conclude home equality; we need the entire prefix up through position z₃ − 1 to coincide. The argument *does* deliver this (via the prefix-agreement clause `a' = a · w`), but the textual presentation singles out "second zero" without making the full-prefix-coincidence step explicit.

**Required**: Clarify to: "the first three zeros of `a'` all sit at positions within `a`, and `a'` agrees with `a` on positions 1..#a; therefore the prefix of `a'` up through position z₃(a) − 1 equals the prefix of `a` up through z₃(a) − 1, giving home(a') = home(a) = d."

## OUT_OF_SCOPE

### Topic 1: Elevating the sibling-frontier discipline to a substrate-level guarantee

**Why out of scope**: Listed as an open question. The note properly tracks R0a's discipline-conditional nature throughout and notes that elevating the discipline (via tightening Emit_K's specification or the substrate primitive) would discharge the conditionality. This is acknowledged future work.

### Topic 2: Multi-arity link extensions and A_K^{(n)}

**Why out of scope**: The note explicitly restricts to standard-triple links and flags higher-arity extensions in the open questions.

### Topic 3: L14's native scoped form without the Setup hypothesis

**Why out of scope**: The note carefully tags Setup-required claims and the final open question enumerates the reformulation work needed if the Setup hypothesis is relaxed. This is deliberate scoping.

### Topic 4: Concurrency and Observe atomicity

**Why out of scope**: Listed as an open question. The note's operations are state-to-state functions, not concurrent transitions, which is a reasonable abstraction level.

VERDICT: REVISE
