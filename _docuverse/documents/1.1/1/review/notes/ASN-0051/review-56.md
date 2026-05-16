# Review of ASN-0051

## REVISE

### Issue 1: Misleading foundation citation in Notation section
**ASN-0051, Notation block (after editorial note)**: "the symbol `+` between a tumbler and a nonnegative integer denotes the OrdinalShiftBase numeric shift from ASN-0058 (M-auxiliary)"
**Problem**: The parenthetical "(M-auxiliary)" reads as a sub-reference identifying OrdinalShiftBase with M-aux. In ASN-0058, these are distinct: OrdinalShiftBase is the CONVENTION defining `a + k = shift(a, k)`; M-aux is the OrdinalIncrementAssociativity LEMMA stating `(v + c) + j = v + (c + j)`. The definitional equality `a + k = shift(a, k)` cited inline comes from OrdinalShiftBase alone — M-aux is not consumed by the notation definition.
**Required**: Remove "(M-auxiliary)" or clarify the relationship — e.g., "the OrdinalShiftBase convention from ASN-0058, with M-aux supplying associativity for chained shifts."

### Issue 2: K.μ~ composite structure of Worked Example understates elementary chain
**ASN-0051, Worked Example, "After removing a₃"**: presents the composite as "Step 1 — K.μ~ … Step 2 — K.μ⁻", but K.μ~ is itself the *distinguished composite* K.μ⁻ + K.μ⁺ per ASN-0047 (since `dom_C(M(d)) ≠ ∅` here).
**Problem**: The full elementary chain is K.μ⁻ + K.μ⁺ + K.μ⁻, not two steps. Readers checking D-SEQ admissibility per elementary K.μ⁻ in the K.μ~ stage will not find the per-stage admissibility documented (which positions are tail-removed, in what order). The same prose pattern recurs in the SV14(d) witness and its discussion of "post-K.μ~" being the Σ_int for the elementary K.μ⁻.
**Required**: Either annotate the Worked Example with the K.μ~ → (K.μ⁻ + K.μ⁺) expansion and exhibit D-SEQ admissibility at the intermediate K.μ⁻ step, or note inline that the prose treats K.μ~ as opaque at the composite level (consistent with SV5's existing composite-scope note, which should then be cross-referenced here).

### Issue 3: Implicit V-position arithmetic in SV11 multi-block witness
**ASN-0051, SV11 multi-block (m≥2, p≥2) attainment witness**: writes "v₁ < v₂ < ... < v₁₅" and asserts β₁ = (v₁, a₁, 10), β₂ = (v₁₁, a₆, 5) with V-adjacency `v₁₁ = v₁₀ + 1`.
**Problem**: The block representation `(v, a, n)` per ASN-0058 requires `M(d)(v + k) = a + k` for `0 ≤ k < n` — i.e., the V-positions inside a block are *sequential* under OrdinalShiftBase. The witness writes `v_{10+i} ↦ a_{5+i}` for `1 ≤ i ≤ 5` (so `v₁₁ ↦ a₆, ..., v₁₅ ↦ a₁₀`), which only forms the block (v₁₁, a₆, 5) if `v_{k+1} = v_k + 1` and `a_{k+1} = a_k + 1` for each k. The sibling assumption for I-addresses is stated; the V-side equivalent is not.
**Required**: State explicitly that v₁..v₁₅ are sequential V-positions in subspace s_C (e.g., `v_k = [s_C, k]` at the common depth m_C = 2), so that `v_{k+1} = v_k + 1` is the OrdinalShiftBase relationship M11 expects. Without this, the block decomposition's well-formedness rests on unstated arithmetic.

### Issue 4: SV6 proof's T4-validity argument for t — boundary case clarity
**ASN-0051, SV6 proof, "T4-validity of t" bullet — no-adjacent-zeros sub-case**: "Among the three cases k − 1 ∈ {p₁, p₂, p₃}, only k − 1 = p₃ is possible, since k > p₃ > p₂ > p₁ forces k − 1 ≥ p₃; the live boundary case is therefore the single one in which position k − 1 is the third field separator and position k is the first component of the element field."
**Problem**: This reasoning is correct but conflates two assertions: (a) only the (k-1, k) boundary is the new boundary to check (the inner pairs of positions in [1, k-1] inherit T4 from s, and pairs in [k, #t] are non-zero pairs), and (b) the (k-1, k) boundary fails to be doubly-zero. The proof says the boundary is "the single one in which … k is the first component of the element field" — but k ≥ p₃ + 1 with strict `k > p₃` gives `k ≥ p₃ + 1`, leaving k = p₃ + 1 as the *only* case where k − 1 = p₃ holds; for `k > p₃ + 1`, position k − 1 lies in the element field, not at p₃. The cases are not enumerated, and the reader has to reconstruct which subcase the conclusion applies to.
**Required**: Make the case split explicit: (i) `k = p₃ + 1` (the boundary case where position k − 1 is the third separator and position k is the first element-field component); (ii) `k > p₃ + 1` (position k − 1 lies inside the element field, so t_{k-1} is nonzero by the element-field-zero-confinement argument, hence the (k − 1, k) pair is automatically not doubly zero). The current prose only addresses case (i).

## OUT_OF_SCOPE

### Topic 1: Same-origin coverage growth under sequential allocation
**Why out of scope**: ASN explicitly defers formal characterization to ASN-0034 ("the precise allocator-discipline conditions … are deferred to the allocator-discipline treatment in ASN-0034"). The descriptive discussion appropriately motivates SV6 without overreaching.

### Topic 2: Broader-level span behavior (k ≤ p₃)
**Why out of scope**: ASN explicitly limits SV6 to element-level action points and notes that broader-level span treatment requires ASN-0034's allocator and address-hierarchy machinery.

### Topic 3: Link-subspace projection contribution
**Why out of scope**: SV11 deliberately works with π_text(e, d) and defers link-subspace contribution (including reflexive addressing under L13) to a future "Link Subspace ASN."

META: not applicable — the ASN remains squarely within the abstract specification of arrangement-state-driven projection and discovery invariants, which is the right level for a survivability ASN.

VERDICT: REVISE
