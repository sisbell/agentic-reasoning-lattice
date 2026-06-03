# Review of ASN-0075

I checked every proof, the worked example arithmetic, the wp derivations, and the edge-case coverage. The core results hold up under scrutiny.

**D-EXH (Three-State Exhaustion).** The impossible-row exclusion is rigorous: the chain `a ∈ dom(C)` → `a ∉ dom(L)` (L14) → `subspace(v) ≠ s_L` (S3★ link-clause contrapositive) → `subspace(v) = s_C` (S3★-aux) → `(a,d) ∈ Contains_C(Σ)` → `(a,d) ∈ R` (P4★) is fully discharged, and the composite-boundary hypothesis is correctly identified as load-bearing for the P4★ step. Mutual exclusion and exhaustion are both established from the cross-product table. No hand-waves.

**D-DISCR (Discrimination Requires Provenance).** Both witness histories are valid composites. I verified J0/J1★/J1'★ discharge at each composite boundary, the first-emission determinacy (`a = [d.0.s_C.1]` grounded in A_C(d)), and the synchronized `v_a` argument that makes the `(C,L,E,M)` agreement total. The table pins every foundation component identically while `(a,d) ∈ R_1 \ R_2`. The necessity conclusion follows soundly.

**Worked example.** The arithmetic is internally consistent, including the non-trivial K.μ~ + K.μ⁻ sequencing — moving `b` to the trailing position `[1,3]` before truncation is exactly what the "retain prefix" semantics of K.μ⁻ requires to delete `b` specifically. The four claim verifications (D-EXH, D-IDENT, D-ORIG, D-SYM) check out against the resulting state.

**wp analysis.** Q0 and Q1 are genuinely non-trivial state-level postconditions, and the supplementary R-disjointness lemma's three-group partition correctly falsifies both conjuncts in each group, with the boundary hypothesis properly invoked for the P4★-dependent steps.

**Derived guarantees.** D-IDENT's link-survival argument correctly covers both the span-boundary (`a = start(σ)`) and span-interior (`start(σ) < a < reach(σ)`) cases via `a ∈ ⟦σ⟧`, grounded in P3 (`L' = L`) and P0. Origin, symmetry, observational frame, and state-functional independence are each derived, not asserted.

Foundation usage is correct, all cross-references are to foundation ASNs (0034, 0036, 0047), and no notation is reinvented.

## OUT_OF_SCOPE

### Topic 1: Multi-document and span-presentation generalizations
**Why out of scope**: The open questions (≥3 documents, witness-structure replacement, finite span presentation, restoration semantics) are correctly deferred — they are new territory requiring span/bundle-algebra treatment, not gaps in this binary observational operation.

VERDICT: CONVERGED
