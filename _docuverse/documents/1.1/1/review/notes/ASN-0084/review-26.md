# Review of ASN-0084

## REVISE

### Issue 1: Width-ordinal relationship is implicit but load-bearing throughout the proofs

**ASN-0084, RegionPartition definition**: "We write w_α = |α|, w_β = |β|, w_μ = |μ| for the region widths."

**Problem**: The widths are defined as set cardinalities, but the proofs use them as ordinal increments — assuming ord(c₁) = ord(c₀) + w_α, ord(c₂) = ord(c₁) + w_β (3-cut) or ord(c₁) + w_μ (4-cut), etc. Specific consumers:
- R-DISP for 3-cut β: "ord(v) = ord(c₁) + j = ord(c₀) + w_α + j" uses ord(c₁) − ord(c₀) = w_α.
- R-DISP for 4-cut β: "ord(v) = ord(c₂) + j = ord(c₀) + w_α + w_μ + j" uses ord(c₂) − ord(c₀) = w_α + w_μ.
- R-PPERM, R-SPERM, R-COMM, R-PIV, R-SWP all rely on this identity.

R-PIV proves the aggregate fact w_α + w_β = ord(c₂) − ord(c₀) inline, but the per-cut identities w_α = ord(c₁) − ord(c₀), etc., are never stated. The derivation uses R-PRE(iv) and D-SEQ (ASN-0036): [c₀, c_{n−1}) ⊆ V_S(d) and V_S(d) is sequential, so |[c₀, c₁) ∩ V_S(d)| = ord(c₁) − ord(c₀).

**Required**: Add an explicit corollary right after RegionPartition: "Under R-PRE, by R-PRE(iv) and D-SEQ (ASN-0036), w_α = ord(c₁) − ord(c₀); w_β = ord(c₂) − ord(c₁) for n = 3 and ord(c₃) − ord(c₂) for n = 4; w_μ = ord(c₂) − ord(c₁) for n = 4." Otherwise readers reconstruct this identity at every proof step.

### Issue 2: TS2 precondition #a₁ = #a₂ elided in canonical decomposition (b)

**ASN-0084, canonical decomposition (b), a₁ = a₂ sub-case**: "When k₁ ≥ 1: shift(a₁, k₁) = shift(a₂, k₁) with #a₁ = #a₂ (from equal result lengths), so TS2 gives a₁ = a₂."

**Problem**: TS2 (ShiftInjectivity, ASN-0034) requires #v₁ = #v₂ as an explicit precondition. The parenthetical "(from equal result lengths)" compresses two steps: (i) shift(a₁, k₁) = shift(a₂, k₁) = M(d)(w) is one tumbler with one length; (ii) shift preserves length via OrdinalShift's `#shift(v, n) = #v`. Neither step is named, despite being load-bearing.

**Required**: Replace "(from equal result lengths)" with the explicit two-step derivation: "since shift(a₁, k₁) = shift(a₂, k₁) is one tumbler with one length, and OrdinalShift's `#shift(v, n) = #v` (ASN-0034) gives #shift(aᵢ, k₁) = #aᵢ, we have #a₁ = #a₂."

### Issue 3: Misleading hedge in canonical decomposition (b), n_1 = n_2 sub-case

**ASN-0084, canonical decomposition (b), n_1 = n_2 sub-case**: "v_b + n_b = v_c + k_c = v_b + k_c forces n_b = k_c (TS2 in the n_b, k_c ≥ 1 sub-case, or direct identity-convention equality otherwise)"

**Problem**: Under the contradiction assumption k_c ≥ 1 established earlier in the paragraph, combined with the run property n_b ≥ 1, only the TS2 sub-case applies. The hedge "or direct identity-convention equality otherwise" has no domain. Worse, if k_c could be 0 here, the equation v_b + n_b = v_b would contradict TS4 (n_b ≥ 1 forces shift(v_b, n_b) > v_b strictly), not yield "direct identity-convention equality" of n_b and 0. The phrasing misdescribes what would happen in the impossible branch.

**Required**: Remove the hedge: "TS2 gives n_b = k_c (using n_b ≥ 1 from S8 and k_c ≥ 1 from the contradiction assumption)."

### Issue 4: "Case v₁ < v₂ is symmetric" without explicit reflection

**ASN-0084, canonical decomposition (b), v_1 = v_2 sub-case**: "Suppose v₂ < v₁ (the case v₁ < v₂ is symmetric)."

**Problem**: The symmetry is real but not surface-level — the argument backward-extends b₁, and the symmetric reflection backward-extends b₂ instead. A one-line note would close the gap without expanding the proof significantly.

**Required**: Replace "(the case v₁ < v₂ is symmetric)" with "(the case v₁ < v₂ follows by swapping b₁ and b₂: backward-extending b₂ to contradict b₂'s maximality)".

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4

**Why out of scope**: CS1 deliberately restricts to n ∈ {3, 4}. Generalizing to higher arities is listed among open questions and would form a separate ASN.

### Topic 2: Cross-subspace rearrangements

**Why out of scope**: The ASN explicitly restricts to S = 1 (text subspace, depth 2). Rearrangements that swap content between subspaces (e.g., text and link) would require different invariant handling.

### Topic 3: Composition of multiple rearrangements

**Why out of scope**: Listed as an open question. Whether the composition of two cut-point rearrangements is expressible as a single cut-point rearrangement is a future ASN topic.

### Topic 4: Bounds on change in canonical run count

**Why out of scope**: Listed as an open question. The ASN notes "the canonical (maximal) run partition of M'(d) may therefore have fewer runs than B'" but defers any quantitative bound.

### Topic 5: Constraints on cut placement relative to run boundaries

**Why out of scope**: Listed as an open question. CS1–CS4 allow arbitrary cut positions satisfying the structural conditions, without requiring alignment to run boundaries.

VERDICT: REVISE
