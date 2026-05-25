# Review of ASN-0070

## REVISE

### Issue 1: F-canonical Step 2 characterisation argument has a literally-false intermediate claim
**ASN-0070, "Step 2 — Per-subspace uniqueness", reverse direction of consecutivity characterisation**: "Given the conditions, any depth-`m_S(d)` subspace-`S` `t''` with `t < t'' < t'` must have divergence position `m_S(d)` on each side: at any earlier position `p < m_S(d)` where `t_p = t'_p`, the inequality `t < t''` would force `t''_p ≥ t_p = t'_p`..."

**Problem**: The claim "`t < t''` would force `t''_p ≥ t_p`" is not literally true at arbitrary `p`. Counterexample: `t = [1, 5]`, `t'' = [2, 3]` — then `t < t''` (divergence at position 1) but `t''_2 = 3 < 5 = t_2`. T1 constrains components only at and before the first divergence position. The conclusion (no `t''` between `t` and `t'`) is correct, but the argument as written does not establish it.

**Required**: Replace the prose with an explicit inductive argument on `p ∈ {1, ..., m-1}`. Inductive hypothesis: `t''_i = t_i = t'_i` for `1 ≤ i < p`. Step: under the IH, the first divergence of `(t, t'')` is at some `q ≥ p`, so T1 case (i) gives `t''_p ≥ t_p` (with equality if `q > p`, strict if `q = p`); symmetrically `t''_p ≤ t'_p` from `t'' < t'`; combined with `t_p = t'_p` yields `t''_p = t_p`. Alternative: case-split directly on the divergence positions `q` of `(t, t'')` and `q'` of `(t'', t')`, deriving contradictions in every case where either is `< m`. Either rewrite makes the load-bearing structure explicit.

### Issue 2: F-multi's subspace conditional is vacuous
**ASN-0070, F-multi (MultiplicityPreservation), Postcondition**: "Both `v₁ ∈ ⟦Σ_V^{S₁}⟧_V` (where `S₁ = subspace(v₁)`) and `v₂ ∈ ⟦Σ_V^{S₂}⟧_V` (where `S₂ = subspace(v₂)`). When `S₁ = S₂`, both belong to the same subspace component."

**Problem**: Under the F-multi precondition `M(d)(v₁) = M(d)(v₂) = a`, F-subspace forces `S₁ = subspace_I(a) = S₂` unconditionally. The "When `S₁ = S₂`" clause is always satisfied; the conditional phrasing suggests an alternative case (`S₁ ≠ S₂`) that cannot arise. A careful reader reasoning about multiplicity across subspaces may be misled into believing within-document sharing could span subspaces.

**Required**: State the consequence directly: "By F-subspace, `S₁ = S₂ = subspace_I(a)`, so both `v₁` and `v₂` belong to the same subspace component `⟦Σ_V^{S₁}⟧_V`." Drop the "When `S₁ = S₂`" hedge.

## OUT_OF_SCOPE

None — the Open Questions section appropriately collects future-work items (concurrency, partial-reach reporting, transclusion-lineage relationships, compactness obligations) without claiming them.

VERDICT: REVISE
