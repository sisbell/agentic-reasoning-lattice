# Review of ASN-0100

## REVISE

(none)

## OUT_OF_SCOPE

(none — scope is properly bounded by §"Bounding the Scope")

The ASN is exceptionally thorough. I verified the substantive claims and found no errors warranting REVISE:

**Substrate decomposition correctness.** The four-step decomposition (n K.α + optional K.μ⁻ + K.μ⁺ + n K.ρ) is properly admissible under ValidComposite★. Each elementary's precondition is discharged at its intermediate state, and the J0/J1★/J1'★ couplings discharge at the boundary.

**Freshness argument.** Each K.α firing's freshness precondition `a_k ∉ dom(Σ_k.C) ∪ dom(Σ_k.L)` is properly discharged against the intermediate (not pre-) state via ChainEnumerationInjectivity + ChainMembershipForOrigin + SubAllocatorAxiom.Disjointness (for C-clause) and subspace separation via SC-NEQ (for L-clause).

**K.μ⁻ omission cases.** The three-case analysis (i.a forced, i.b/ii canonical-decomposition choices) correctly distinguishes intrinsic forcing from parsimony. The alternative-decomposition admissibility under ValidComposite★'s broader vocabulary is correctly argued.

**S2 functionality.** The pairwise-disjointness argument across Left/Insertion/Shifted-right regions uses TumblerAdd's piecewise rule at action point m_C correctly. Last-component ranges are disjoint: Left `< p_m`, Insertion `[p_m, p_m + n − 1]`, Shifted-right `≥ p_m + n`.

**Boundary cases.** Empty (i.a vs i.b sub-cases), append (case ii), j=0 (Left empty), n=1 — all covered. The fresh-allocator-state vs prior-emission sub-case for empty arrangement is explicitly traced.

**I3 (ASN-0082) handling.** The disclaiming of I3-V, I3-CS, I3-CX (which describe a shift-only post-state inconsistent with INSERT's) is explicit and load-bearing for the Insertion region's separate verification. The companion lemmas (I3-S2, I3-S3, etc.) cover the Left + Shifted-right + cross-subspace portion; Insertion is verified inline.

**Wp analyses.** Both wp computations (discoverability under tight/non-tight distinction; (a, d) ∈ R' via chain-structure derivation) are non-trivial.

**Worked examples.** The interior example traces projection through every intermediate via LP6/LP10/LP9/LP14, including the K.μ⁻ "temporary retraction" and K.μ⁺ "shift-cancellation" mechanics. The non-tight alternative is traced.

**Invariant coverage.** Every ASN-0047 invariant (per-state Class (a) and composite-boundary Class (b)) is addressed, with explicit S4 discharge against the changed dom(C) at each K.α intermediate.

**Atomicity distinction.** The elementary-level (SequentialTransitionAxiom) vs composite-level (precondition) split is honest and necessary.

VERDICT: CONVERGED
