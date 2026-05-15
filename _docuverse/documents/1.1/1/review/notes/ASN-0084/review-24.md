# Review of ASN-0084

## REVISE

### Issue 1: D-SEQ cited for arbitrary depth-2 subspaces, but D-SEQ applies only to V_1(d)
**ASN-0084, State and Vocabulary section**: "At depth 2, D-SEQ (ASN-0036) gives V_S(d) = {[S, k] : 1 ≤ k ≤ N} for some N ≥ 0, and each ord(v) is a singleton tumbler [k] with k ∈ ℕ⁺."

**Problem**: D-SEQ (ASN-0036) is stated specifically for V_1(d), the text subspace, and follows from D-CTG which explicitly exempts V_2(d) (link) as "sparse with tombstones is permitted." For non-text depth-2 subspaces, V_S(d) need not be sequential, and the characterization {[S, k] : 1 ≤ k ≤ N} is unjustified. CS3 + CS4 admit any depth-2 subspace S, not just S = 1, so this is an actual scope mismatch. The over-broad citation recurs in: (a) "Consequences of R-PRE" empty-exterior boundary cases ("V_S(d) = {[S, 1], ..., [S, N]}" and "ord(c_{n−1}) = N + 1"); (b) canonical decomposition step (b)'s justification that [S, ord(v₁) − 1] ∈ V_S(d) ("by D-SEQ"). The worked examples both use S = 1 so the demonstrations are unaffected, but the formal claims overreach.

**Required**: Either (a) restrict the ASN's scope explicitly to S = 1 and document that, removing the over-broad D-SEQ application; or (b) re-justify each appeal to V_S(d) sequential structure using only R-PRE(iv) (local contiguity in the affected range) and S8 (within-run V-extent contiguity). For canonical decomposition step (b), the intermediate-position membership [S, ord(v₁) − 1] ∈ V_S(d) follows directly from membership in V(b₂) (since ord(v₂) ≤ ord(v₁) − 1 ≤ ord(w) and V(b₂) is contiguous by S8), without invoking D-SEQ.

### Issue 2: Canonical decomposition step (c) handles forward extension only
**ASN-0084, canonical decomposition step (c)**: "Suppose, toward contradiction, that some run b = (v_b, a_b, n_b) in the terminal partition is non-maximal. Then there exists a valid run b' = (v_b, a_b, n_b') with n_b' > n_b strictly extending b."

**Problem**: "Maximal" was defined as "runs that cannot be extended by merging with a V-adjacent, I-adjacent neighbor." Merging b with a forward neighbor d produces a strictly larger run with V-start v_b (the case treated). Merging b with a backward neighbor c (i.e., (c, b) mergeable) produces a strictly larger run with V-start v_c < v_b — this case is not addressed. The implication "non-maximal → strict forward extension with V-start v_b" is therefore unjustified for the broader definition of maximal in scope at this step.

**Required**: Add a parallel case-analysis line, or replace the existing claim with a two-branch dispatch. The backward branch is immediate: if b is backward-extendable via partition neighbor c, then (c, b) is a mergeable pair, directly contradicting the termination condition that no mergeable pair remains. Both forward and backward cases must be explicitly covered for the conclusion "every run in the terminal partition is maximal" to follow.

### Issue 3: Phase 1 "outside ⋃_k V(b_k)" case asserted but its uniqueness justification is informal
**ASN-0084, R-BLK Phase 1**: "Outside ⋃_k V(b_k): no split is performed. This occurs only for the last cut c_{n−1} when c_{n−1} > max(V_S(d))..."

**Problem**: The assertion "occurs only for the last cut c_{n−1} when c_{n−1} > max(V_S(d))" combines two claims: (a) earlier cuts c_0, ..., c_{n−2} are in V_S(d) ⊆ ⋃_k V(b_k); (b) c_{n−1} is outside V_S(d) iff c_{n−1} > max(V_S(d)). Claim (a) follows from R-PRE(iv) applied at each c_i for i < n−1 (since c_i ∈ [c_0, c_{n−1}) at depth 2 in subspace S forces c_i ∈ V_S(d)). Claim (b) implicitly assumes V_S(d) is downward-closed past max — true under D-SEQ for S = 1, but for sparse V_S(d) (e.g., S = 2), c_{n−1} could fall in a gap with ord(c_{n−1}) < max(V_S(d)) and still be outside V_S(d). This issue is dependent on Issue 1 — under the subspace-1 restriction (or a re-justification via S8 only), claim (b) needs sharpening to "c_{n−1} ∉ V_S(d)" rather than the strict bound "c_{n−1} > max(V_S(d))."

**Required**: Either justify the claim by restricting scope (Issue 1's fix) or rephrase as "c_{n−1} ∉ V_S(d)" without the maximum-position framing, and verify that the rest of Phase 1 (right-exterior handling) does not need the stronger bound.

### Issue 4: Step (b)'s a₁ = a₂ derivation references TS5 and TS4 but with mixed-zero handling that should be tightened
**ASN-0084, canonical decomposition step (b)**: "k₁ = k₂ (by TS5: if k₁ ≠ k₂ with both ≥ 1, then shift(v₁, k₁) ≠ shift(v₁, k₂), contradicting equality; when one is 0, TS4 forces the other to be 0)."

**Problem**: TS5 (ShiftAmountMonotonicity, ASN-0034) requires both shift amounts ≥ 1. The "when one is 0" case uses the identity convention and TS4 (StrictIncrease, which gives shift(v, n) > v for n ≥ 1) to conclude that if k₁ = 0 and k₂ ≥ 1, then shift(v₁, 0) = v₁ < shift(v₁, k₂), contradicting equality. The argument is correct but compresses two steps (TS4 plus T1 irreflexivity to convert > to ≠). The "both 0" sub-case is also not addressed (it gives k₁ = k₂ = 0 trivially, consistent with the conclusion, but should be noted for completeness).

**Required**: Expand the case analysis to cover all three sub-cases explicitly — both ≥ 1 (TS5), one = 0 and one ≥ 1 (TS4 + T1 irreflexivity), both = 0 (immediate equality) — and cite T1 irreflexivity (or equivalently the > vs = exclusion in the strict-total-order trichotomy) where it is implicitly used.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4
**Why out of scope**: Acknowledged in Open Questions. The ASN explicitly scopes to 3-cut and 4-cut operations via CS1; generalization is future work.

### Topic 2: Composition of multiple rearrangements
**Why out of scope**: Acknowledged in Open Questions. Properties of single rearrangements are proved here; composition belongs in a future ASN.

### Topic 3: Higher-depth V-positions (#v > 2)
**Why out of scope**: Explicit scope boundary stated in State and Vocabulary. Deeper coordinate handling requires additional notation and arguments deferred to future ASNs.

### Topic 4: Inverse rearrangements and normal forms
**Why out of scope**: The ASN defines specific operations but does not address invertibility (every pivot has an inverse pivot) or canonical-form questions for sequences of rearrangements.

### Topic 5: Run-count change bounds under rearrangement
**Why out of scope**: Acknowledged in Open Questions. The post-rearrangement canonical partition may have more or fewer runs than the original; bounds on this change are future work.

VERDICT: REVISE
