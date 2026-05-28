# Review of ASN-0101

## REVISE

### Issue 1: D11 cardinality wp derivation has an implicit step
**ASN-0101, D11 justification**: "by D9's third clause and the bijectivity of σ_d, the post-state projection cardinality on subspace S equals `|project(L(ℓ).eᵢ, d, Σ) ∩ (Λ ∪ Π)| = |project(L(ℓ).eᵢ, d, Σ) ∩ V_S(d)| − |project(L(ℓ).eᵢ, d, Σ) ∩ X|`"
**Problem**: The chain cites D9 (which gives the partition form `(project ∩ Λ) ∪ σ_d(project ∩ Π)`) and σ_d's bijectivity (which preserves cardinality on Π), but the step from `|project ∩ Λ| + |project ∩ Π|` to `|project ∩ (Λ ∪ Π)|` relies on `Λ ∩ Π = ∅`, and the further step to `|project ∩ V_S(d)| − |project ∩ X|` relies on the partition `V_S(d) = Λ ⊎ X ⊎ Π`. Neither is cited.
**Required**: State the two implicit facts: (i) `Λ ∩ Π = ∅` (from last-component ranges, already established in D8's S2 justification), (ii) `V_S(d) = Λ ⊎ X ⊎ Π` (from D0's region definitions). Then `|project ∩ (Λ ∪ Π)| = |project ∩ V_S(d)| − |project ∩ X|` follows by inclusion-exclusion on the partition.

### Issue 2: D11 discoverability wp derivation has confusing prose
**ASN-0101, D11 justification**: "Their union is non-empty iff their union is — which is the pre-state projection intersected with Λ ∪ Π ∪ V_{S'}(d) = V_S(d) \ X ∪ V_{S'}(d) = dom(M(d)) \ X."
**Problem**: The phrase "Their union is non-empty iff their union is" is a tautology and obscures the actual argument: that the post-state projection (a function of pre-state data via D9) is non-empty iff `project(L(ℓ).eᵢ, d, Σ) ∩ (Λ ∪ Π ∪ V_{S'}(d)) ≠ ∅`. The intended reduction works through `Λ ∪ Π ∪ V_{S'}(d) = (V_S(d) \ X) ∪ V_{S'}(d) = dom(M(d)) \ X` but the reader has to reconstruct the actual claim from a tautological sentence.
**Required**: Rephrase to identify the union being computed: e.g., "The post-state projection is non-empty iff at least one of its three components is non-empty, equivalently iff `project(L(ℓ).eᵢ, d, Σ) ∩ (Λ ∪ Π ∪ V_{S'}(d)) ≠ ∅`. Computing the union: `Λ ∪ Π = V_S(d) \ X`, so `Λ ∪ Π ∪ V_{S'}(d) = (V_S(d) \ X) ∪ V_{S'}(d) = dom(M(d)) \ X`."

### Issue 3: Worked examples do not explicitly verify D11's cross-document wps
**ASN-0101, "A worked example" through "A cross-document transclusion example"**: The cross-document example verifies pre- and post-state projections from `d'` are bytewise equal, and that discoverability from `d'` is preserved. But D11 introduces four wp bullets, and only the from-`d` bullets (1 and 3) are numerically traced in the examples.
**Problem**: D11's bullets 2 (cross-document discoverability wp) and 4 (cross-document cardinality wp) are stated and justified in the body but never instantiated against a concrete state. The cross-document example would be the natural place to verify both — given the pre-state values computed there (`discoverable_from(ℓ_0, d', Σ) = true`, `|project(L(ℓ_0).e_1, d', Σ)| = 2`), one would expect the wp instantiations `wp(DEL[d, σ], discoverable_from(ℓ_0, d', ·)) = true` and `wp(DEL[d, σ], |project(L(ℓ_0).e_1, d', ·)| = 2) = true` to be checked numerically.
**Required**: Extend the cross-document example with two lines verifying the cross-document wps: compute the wp by D11's bullets 2 and 4, compare against the pre-state predicate, and show that the post-state confirms it.

### Issue 4: D8 Group (ii) wholesale argument elides specific invariants
**ASN-0101, D8 Group (ii) justification**: "All of M0, S4, S7a, S7b, S7c, S7d, C1, C1b, C1c, C2, L0, L1, L1a, L1b, L1c, L3, L12, L14, L-fin, C-fin, NodeLineage … hold trivially at the post-state because C' = C, L' = L, E' = E, and dom(M') = dom(M) by D0's frame — every clause of every invariant in this group is a predicate over one or more of these components..."
**Problem**: The argument names ~20 invariants but discharges most with a uniform "predicate over preserved components" appeal, with explicit reasoning only for S4 and the chain-discipline lemmas. For invariants like C1c (LinkAllocatorConformance — every link address has a structural inc-chain to its home document) and L1c, the predicate involves the existence of an inc-chain, which depends on dom(L), dom(C), and structural inc-step admissibility. The wholesale claim is correct but the reader must verify for each invariant that its predicate truly depends only on (C, L, E, R, dom(M)).
**Required**: For each invariant in the bulk list, at minimum identify the components it predicates over. Even one line per invariant ("M0 predicates over `dom(M)`, preserved by `dom(M') = dom(M)`"; "C1c predicates over `dom(C)` and structural inc-chains, both preserved by `dom(C') = dom(C)` and tumbler determinism") would discharge the obligation explicitly.

### Issue 5: D0 "Justification of the reduction" — derivation depends on m_S ≥ 2 boundary
**ASN-0101, D0 justification**: "At `m_S = 2` (the depth fixed for the link subspace by LinkVPositionDepthAxiom, and the depth that suffices for content as well) the range `2 ≤ j ≤ 1` is empty, so the claim holds vacuously; the argument then proceeds directly to the position-`m_S` case below."
**Problem**: The derivation establishes `v_j = 1` for middle positions `2 ≤ j ≤ m_S − 1` and then shows the order constraint reduces to `p ≤ v_{m_S} < p + n` at the final position. At `m_S = 2` the "middle positions" range is empty and the proof "proceeds directly to the position-m_S case", but the position-2 case (where `v = [S, v_2]`) hasn't been shown to give the same reduction. The reader must reconstruct that when `m_S = 2`, the tumbler is just `[S, v_2]`, the divergence position must be 2 (position 1 agrees), and the order constraint `s ≤ v < r` with `s = [S, p]` and `r = [S, p+n]` reduces to `p ≤ v_2 < p+n` directly by T1 case (i).
**Required**: Add one sentence handling the m_S = 2 case explicitly: "At `m_S = 2`, the tumbler is `[S, v_2]`; both `s = [S, p]` and `r = [S, p+n]` agree with `v` at position 1, so `s ≤ v < r` reduces by T1 case (i) at position 2 to `p ≤ v_2 < p + n`."

### Issue 6: D8 Group (i) S3★ source-correspondence argument elides re-mapping case
**ASN-0101, D8 Group (i) justification**: "S3★ holds via source correspondence: pre-state S3★ on u gives M(d)(u) ∈ dom(C) when subspace(u) = s_C and M(d)(u) ∈ dom(L) when subspace(u) = s_L; D2 and D3 give dom(C') = dom(C) and dom(L') = dom(L); so M'(d)(v) = M(d)(u) lies in the correct post-state store."
**Problem**: The argument is correct but the "post-state store" claim requires that `subspace(v) = subspace(u)` (since S3★ pairs subspace of v with store of M'(d)(v)). The ASN does note "subspace(v) = subspace(u): the shift σ_d modifies only the last component (by D1's structural form), preserving the first" — but this fact is invoked in passing before the S3★ derivation and could be more tightly tied to the S3★ argument itself, since S3★'s biconditional structure (`subspace(v) = s_C ⟹ ... ∧ subspace(v) = s_L ⟹ ...`) requires matching subspace of source and image.
**Required**: After establishing `subspace(v) = subspace(u)`, state the routing explicitly: "since `subspace(v) = subspace(u)`, S3★'s biconditional at `u` on the pre-state transfers to `v` on the post-state with the same subspace classification; combined with `dom(C') = dom(C)` (D2) and `dom(L') = dom(L)` (D3), the post-state store membership follows."

## OUT_OF_SCOPE

### Topic 1: Recoverability of pre-DELETE arrangement state
**Why out of scope**: The ASN's note on recoverability correctly identifies that full historical reconstruction requires a versioning mechanism (the J4 ForkComposite) outside DEL's scope. DEL contributes only the non-destruction substrate (D2 + D5). Full versioning semantics belong in a separate ASN.

### Topic 2: Maximally-merged decomposition preservation across DELETE
**Why out of scope**: The ASN notes that S8★ is satisfied by the trivial singleton decomposition, and that ASN-0058's M11 (canonical maximally-merged decomposition) may or may not be preserved across DELETE depending on whether the implementation performs a reconciliation pass. A specification of when/how reconciliation should occur is a downstream concern for the bundle algebra, not for DELETE itself.

### Topic 3: Orphan enumeration / I-address discovery after DELETE
**Why out of scope**: The ASN observes that D2 leaves orphaned I-addresses in `dom(C')` with no enumeration operation provided. Adding such an operation would be a new transition kind, distinct from DEL.

VERDICT: REVISE
