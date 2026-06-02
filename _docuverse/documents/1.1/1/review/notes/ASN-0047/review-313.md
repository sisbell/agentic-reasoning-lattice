# Review of ASN-0047

This is a carefully constructed and, on the mathematical substance, a rigorous note: the state model, the seven elementary transitions, the per-subspace strengthenings (D-CTG★/D-MIN★/D-SEQ★, S3★, S8★), the K.μ~ admissibility analysis, and the allocator-hierarchy/cross-document disjointness lemmas all hold up under checking, and the five worked examples ground the key postconditions on concrete tumblers. I found no correctness defect in the proofs. The note carries the `review-mode.anti-bloat` classifier, and the findings below are the duplication / restatement patterns that pass review otherwise.

## REVISE

### Issue 1: P3 is proved twice by the same seven-transition case analysis
**ASN-0047, *Destruction confinement* and *Extended reachable-state invariants* (Per-transition invariant)**: The *Destruction confinement* proof of P3 reads "By case analysis on the seven elementary transitions. K.α extends dom(C)… K.δ extends E… K.λ extends dom(L)… Each preserves every conjunct." The later *Per-transition invariant* block re-runs the identical analysis: "P0. K.α extends dom(C) at `a ∉ dom(C)`… P1. K.δ extends E… P2. K.ρ extends R… L12. K.λ extends dom(L)…".

**Problem**: The two passages discharge the same four conjuncts of P3 over the same seven transitions with the same arguments. The second is pure restatement — exactly the "two paragraphs say the same thing" pattern the anti-bloat classifier flags.

**Required**: Reduce the *Per-transition invariant* block to a citation ("P3 is proved in *Destruction confinement*; transitivity of ⊆/= over a finite composite lifts it to the boundary") and delete the duplicated conjunct-by-conjunct walk.

### Issue 2: ValidComposite★ clause (2) restates its own exclusion
**ASN-0047, ValidComposite★ clause (2)**: "a composite that satisfies clause (1) but violates clause (2) — for instance, K.α alone without an accompanying K.μ⁺ and K.ρ, every elementary precondition holding at each intermediate state — is not a valid composite. This K.α-alone elementary sequence does exist; clause (2) is precisely what excludes it from the *valid* composites."

**Problem**: The second sentence asserts nothing the first did not already state. "K.α alone … is not a valid composite" and "clause (2) is precisely what excludes it" are the same claim twice.

**Required**: Drop the second sentence; the first (with its discriminating example) carries the point.

### Issue 3: "discharged analogously" glosses the one conjunct that differs
**ASN-0047, *Worked example: prior-provenance and first-time-transcluded replacements* (three-step variant)**: "*Post-state invariants:* S2, S3★, P4★ (now restored), D-CTG★/D-MIN★/D-SEQ★ — all discharged analogously to the two-step variant."

**Problem**: P4★ is precisely the conjunct that is *not* analogous between the two variants. In the two-step form `(aₓ, d) ∈ R` pre-exists, so P4★ holds at every intermediate state; in the three-step form P4★ *transiently fails* after K.μ⁺ and is restored only by the trailing K.ρ. The note itself flags this difference one paragraph earlier ("the notable difference at the historical layer"), yet the invariant line lumps P4★ under "analogous," contradicting that distinction.

**Required**: Exclude P4★ from the "analogous" list and state its discharge explicitly (transient failure at `Σ_post-K.μ⁺`, restoration at K.ρ), or reword to "S2, S3★, D-CTG★/D-MIN★/D-SEQ★ discharged analogously; P4★ differs — see the transient-failure note above."

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link withdrawal
**Why out of scope**: K.μ⁻ models link-subspace contraction by suffix removal only, faithful to the gap-free POOM for suffix deletions but not to the implementation's compact-and-renumber `DELETEVSPAN`. This is already correctly listed as an Open Question and belongs to a future contraction-operation ASN, not to this one — the operation-level mechanics (DELETEVSPAN) are explicitly out of scope here.

META: not applicable — the ASN defines abstract state, primitive transitions, and their invariants at the level an alternative implementation would also have to satisfy; the allocator-hierarchy detail serves uniqueness/structure guarantees, not implementation mechanics.

VERDICT: REVISE
