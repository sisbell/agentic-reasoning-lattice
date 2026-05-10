# Review of ASN-0067

## REVISE

### Issue 1: C13 contradicts the ASN's own observation about D-CTG
**ASN-0067, C13 — SequentialCorrectness**: "V-addresses are dense and contiguous (D-CTG) in every reachable state."
**Problem**: The ASN earlier correctly observes that D-CTG is *not* an invariant of all reachable states: "D-CTG is thus not an invariant of all reachable states — it is a design constraint that complete operations are expected to preserve at their endpoints." The elementary decomposition demonstrates this concretely — after steps 1–2 (K.μ⁻ + K.μ⁺), the intermediate state has a gap at [v, v + w) and is reachable from Σ₀ via a valid composite (J0, J1, J1' hold vacuously: no content allocated, no I-address newly introduced, no provenance added). C13's claim that D-CTG holds "in every reachable state" directly contradicts this. D-CTG is absent from ASN-0047's ReachableStateInvariants theorem.
**Required**: Reword C13(a) to be consistent with the earlier observation. For example: "D-CTG is a design constraint that complete operations preserve at their endpoints. A partial shift — V-addresses shifted but content not yet placed — creates a gap, violating D-CTG at the intermediate state."

### Issue 2: Worked example — maximal merging check incomplete
**ASN-0067, Worked Example**: "The placed block γ₁ cannot merge with its neighbors: origin(1.0.2.0.1.0.4) = 1.0.2.0.1 differs from origin(1.0.1.0.1.0.1) = 1.0.1.0.1, so M16 (CrossOriginMergeImpossibility) applies at both boundaries. B' is maximally merged."
**Problem**: M16 establishes that γ₁ cannot merge with blocks 1 or 3 (cross-origin). But B' has four blocks, and maximal merging requires checking *all* V-adjacent pairs. Blocks 3 and 4 — ([1,5], 1.0.1.0.1.0.3, 1) and ([1,6], 1.0.1.0.1.0.7, 2) — share origin 1.0.1.0.1 and are V-adjacent ([1,5] + 1 = [1,6]). M16 does not apply. The I-adjacency check must be shown explicitly: I-reach of block 3 is 1.0.1.0.1.0.3 + 1 = 1.0.1.0.1.0.4, while block 4's I-start is 1.0.1.0.1.0.7. Since 1.0.1.0.1.0.4 ≠ 1.0.1.0.1.0.7, the merge condition (M7) is unsatisfied. The conclusion is correct but the justification skips this pair.
**Required**: Add the I-adjacency check for blocks 3 and 4.

### Issue 3: ContentReference "m" refers to an ambiguous subspace
**ASN-0067, Definition — ContentReference**: "m is the common V-position depth in d_s's text subspace (S8-depth, ASN-0036)"
**Problem**: S8a defines text-subspace V-positions as those with v₁ ≥ 1, admitting multiple text subspaces (v₁ = 1, v₁ = 2, etc.), each potentially at a different depth under S8-depth. The phrase "d_s's text subspace" in the singular does not identify which subspace's depth determines m. Since u has first component u₁ (the subspace identifier), the relevant depth is that of subspace u₁ in d_s. The math is unaffected — m = #u determines everything — but the definition should be unambiguous.
**Required**: Change to "m is the common V-position depth in subspace u₁ of d_s (S8-depth, ASN-0036)."

## OUT_OF_SCOPE

### Topic 1: Concurrency model for intermediate state visibility
**Why out of scope**: The ASN correctly notes that "formalizing the requirement that intermediate states are invisible to other operations requires a concurrency model not yet present in the foundation." ValidComposite defines sequential correctness only. A future ASN on concurrent access must address isolation guarantees.

### Topic 2: Authorization invariants for cross-owner COPY
**Why out of scope**: The ASN raises this in Open Questions. COPY's structural definition is independent of authorization policy. A future ASN on access control should specify when COPY from a non-owned document is permitted.

VERDICT: REVISE
