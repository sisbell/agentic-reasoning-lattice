# Review of ASN-0043

## REVISE

### Issue 1: L9 proof's allocator chain incomplete for the empty-state case

**ASN-0043, L9 proof, L1c verification for `dom(Σ.L) = ∅`**: "When `d'` has no prior link allocations (as when `dom(Σ.L) = ∅`), the first link address is established by the child-spawning sequence from `d'`'s element-level allocator: `inc` to reach subspace `s_L` at element field depth 1, then `inc(·, 1)` to reach depth 2 — T10a-conforming by TA5a bounds (`k' = 1` with `zeros ≤ 3`)."

**Problem**: The proof presumes `d'`'s element-level allocator is already active. But in the empty-state limit (`Σ.C = Σ.M = Σ.L = ∅`), no allocator under `d'` has been spawned. The chain must include `inc(d', 2)` — the child-spawn that establishes `d'`'s element-level allocator at base `1.0.1.0.1.0.1`. This step requires its own TA5a check (`k' = 2` requires `zeros(d') ≤ 2`, satisfied since `zeros(d') = 2`). The worked example walks through this step explicitly; the L9 proof must match that rigor, especially since the proof's whole point is to construct a witness state from scratch.

**Required**: Enumerate all spawn steps from `d'` to `a` (the initial `inc(d', 2)`, the sibling sweep `inc(·, 0)` from element-field-depth-1 subspace 1 across to subspace `s_L`, and the child-spawn `inc(·, 1)` to depth 2), with TA5a discharged at each `k' > 0` step.

### Issue 2: L11b's precondition omits S0–S3 but the verification of L14a invokes S3

**ASN-0043, L11b statement**: "`(A Σ satisfying L0–L14 ∧ L-fin, a ∈ dom(Σ.L) :: (E Σ' extending Σ, a' ∈ dom(Σ'.L) :: a' ≠ a ∧ Σ'.L(a') = Σ.L(a) ∧ Σ' satisfies L0–L14 ∧ L-fin))`"

**ASN-0043, L11b proof, L14a discharge**: "L14a by S3 (arrangements unchanged, so all V-position targets remain in dom(Σ.C)) and L0 (verified above, dom(Σ.C) ∩ dom(Σ'.L) = ∅)"

**Problem**: The L11b proof uses S3 (ReferentialIntegrity) to discharge L14a in Σ', but S3 is not in L11b's precondition. By contrast, L9's precondition includes `S0–S3` explicitly. The asymmetry leaves a soundness gap: without S3 in the precondition, we cannot conclude that `ran(Σ.M(d)) ⊆ dom(Σ.C)`. An alternative discharge from L14a (in Σ) plus freshness of `a'` would need to establish `a' ∉ ran(Σ.M(d))` separately, which itself requires some bound on where arrangements may point.

**Required**: Either (a) add S0–S3 to L11b's precondition to match the proof's argument, or (b) rewrite the L14a discharge to use only invariants in the stated precondition (likely requiring `a'` freshness against `ran(Σ.M(d))`, which the proof must derive).

### Issue 3: L9 verification list does not address L11b's preservation in Σ'

**ASN-0043, L9 proof, verification of Σ'**: The verification list covers L0, L1, L1a, L1b, L1c, L3–L5, L11a, L12, L14, L-fin, S0–S3, L14a, L2, L6, L8, L10, L13, L12a.

**Problem**: L11b is in the precondition (`Σ satisfies L0–L14 ∧ L-fin ∧ S0–S3`, where "L0–L14" presumably spans L11b) and is therefore part of "Σ' is conforming". But L11b is not addressed in the verification list. The proof's "Remaining properties" sentence covers L2 (structural), L6 (vacuous), and labels L8/L10/L13 as "lemmas that do not constrain states" — but L11b is itself a meta-lemma whose preservation should be acknowledged. Likewise, L9 itself (the property under proof) should be noted as preserved in Σ' by the same construction recursively.

**Required**: Add an explicit note that L9 and L11b are model-level meta-lemmas whose preservation in Σ' follows by the same construction applied recursively to Σ', so they hold without separate verification. Or, if a stronger argument is wanted, sketch why their existential conclusions remain reachable from Σ'.

## OUT_OF_SCOPE

### Topic 1: Versioning interactions

The ASN does not address how link permanence (L12) interacts with versioning operations (e.g., what happens to a link's endsets when content at a referenced I-address is revised). The Scope explicitly excludes operations and version creation, so this is properly out of scope.

### Topic 2: Discovery and indexing semantics for the canonical span

L13 says link addresses are valid endset span targets and exhibits the canonical span `(b, δ(1, #b))`. Whether discovery operations (e.g., "find all links targeting `b`") must use this canonical form or may match looser span shapes is a property of the query interface — addressed in Open Questions as endset equivalence, properly out of scope.

VERDICT: REVISE
