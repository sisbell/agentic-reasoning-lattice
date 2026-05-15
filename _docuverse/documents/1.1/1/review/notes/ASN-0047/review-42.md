# Review of ASN-0047

## REVISE

### Issue 1: L3 conflicts with ASN-0043
**ASN-0047, Link store and extended system state**: "L3 (TripleEndsetStructure). (A a ∈ dom(Σ.L) :: Σ.L(a) = (F, G, Θ) where F, G, Θ ∈ Endset). Every link in the link store has exactly three endsets."
**Problem**: ASN-0043's L3 (NEndsetStructure) is `|Σ.L(a)| ≥ 3` — at least three endsets, not exactly three — and also requires `Σ.L(a).e₃ ≠ ∅`. ASN-0047's local Link definition `Link = {(F, G, Θ) where F, G, Θ ∈ Endset}` drops the non-empty type-endset clause, and K.λ's precondition `(F, G, Θ) ∈ Link` permits empty Θ — violating ASN-0043. The Endset definition restated in this ASN also drops the empty-set admissibility statement that ASN-0043 includes.
**Required**: Either align L3 with ASN-0043 (support N ≥ 3 with K.λ taking a tuple of length N, enforce Θ ≠ ∅) or explicitly state ASN-0047 amends L3 to triples and justify dropping the non-empty type-endset clause.

### Issue 2: D-CTG/D-MIN applied to link subspace conflicts with ASN-0036
**ASN-0047, K.μ⁺_L precondition and Per-subspace arrangement invariants**: "D-CTG (VContiguity) and D-MIN (VMinimumPosition) are quantified over *all* subspaces S."
**Problem**: ASN-0036's D-CTG and D-MIN are explicit about scope: D-CTG's Frame says "The link subspace V_2(d) is exempt — sparse with tombstones is permitted"; D-MIN's Frame says "gaps below the minimum (e.g., from tombstoning) are admissible." ASN-0047 enforces contiguity and minimum-position on the link subspace via K.μ⁺_L's preconditions, treating them as if they applied universally. This is a model tightening, not a faithful reading of the foundation.
**Required**: State explicitly that ASN-0047 amends D-CTG and D-MIN to apply per-subspace (with rationale: tombstoning reserved for the open withdrawal mechanism), or relax K.μ⁺_L to admit sparse link arrangements.

### Issue 3: Per-subspace D-SEQ used without foundation
**ASN-0047, K.μ⁻ amendment and ExtendedReachableStateInvariants proof**: "By D-SEQ at the input state (ASN-0036), V_S(d) for each non-empty subspace S is a contiguous ordinal range {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}."
**Problem**: ASN-0036's D-SEQ is stated specifically for V_1(d) (text subspace, S = 1). The per-subspace generalization to arbitrary S is invoked repeatedly — in K.μ⁻ amendment, K.μ~-FIX, the K.μ~ link-subspace fixity argument, and the ExtendedReachableStateInvariants induction — but never proven or restated generically. It cannot be derived from ASN-0036's D-CTG and D-MIN either, since those are themselves text-subspace-only (Issue 2).
**Required**: Either prove the per-subspace D-SEQ within this ASN (would follow from per-subspace D-CTG + D-MIN + S8a + S8-fin + S8-depth) or restate ASN-0036's per-subspace forms as part of the amendments.

### Issue 4: K.δ and K.λ allocator discipline weakened by "typically"
**ASN-0047, K.δ**: "For non-root entities, the address is typically allocated via inc(·, k) (TA5, ASN-0034) within the parent's ownership domain."
**Problem**: The proof relies on T10a's GlobalUniqueness to conclude e ∉ E (and ℓ ∉ dom(L) ∪ dom(C) for K.λ). GlobalUniqueness only applies to addresses produced by T10a-conforming allocation events. The word "typically" admits non-conforming allocations, breaking the GlobalUniqueness chain. K.λ has the same pattern — its forward-allocation precondition orders ℓ but doesn't pin it to the inc(·, 0) frontier.
**Required**: Replace "typically" with a structural requirement. State that K.δ produces e via inc(·, k) with k ∈ {1, 2} within parent(e)'s ownership domain (subject to T10a's zeros-count constraints), and that K.λ produces ℓ via inc(·, 0) on the link allocator's current frontier under d's link prefix.

### Issue 5: P3★ formal statement weaker than verbal claim
**ASN-0047, P3★**: Verbal: "No other component — specifically C, L, E, R — admits contraction or reordering." Formal: `(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ dom(L) ⊆ dom(L') ∧ E ⊆ E' ∧ R ⊆ R')`
**Problem**: The formal statement captures only domain monotonicity. It permits C'(a) ≠ C(a) and L'(ℓ) ≠ L(ℓ) for existing addresses — value rewriting at the same address would satisfy the formal P3★ but violate the verbal "no reordering" of C/L. P5★'s formal statement has both monotonicity and value preservation; P3★ should match. P3★ as written is strictly weaker than P0 and L12 combined, despite the verbal claim being equivalent.
**Required**: Strengthen P3★'s formal statement: `... ∧ (A a ∈ dom(C) :: C'(a) = C(a)) ∧ (A ℓ ∈ dom(L) :: L'(ℓ) = L(ℓ))`.

### Issue 6: K.μ⁻ valid-contractions constraint stated as postcondition, not precondition
**ASN-0047, K.μ⁻ amendment**: "By D-SEQ at the input state (ASN-0036), V_S(d) for each non-empty subspace S is a contiguous ordinal range {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}; valid contractions are constrained to removal from the maximum end of V_S(d) or removal of all positions in V_S(d)."
**Problem**: The structural constraint (suffix removal per subspace) is presented as a consequence of the D-CTG/D-MIN postcondition. K.μ⁺_L states its analogous positional constraint as an explicit precondition (`v_ℓ = shift(max(V_{s_L}(d)), 1)` etc.). K.μ⁻ should be similarly explicit — an operator should not have to back-derive admissible inputs from required outputs. The asymmetry between K.μ⁺_L (explicit precondition) and K.μ⁻ (implicit precondition) makes the framework harder to read and verify.
**Required**: Add a precondition stating which removals are admissible (per-subspace suffix or full subspace clearance), with D-CTG/D-MIN as consequences rather than constraints.

### Issue 7: Π = id case in K.μ~ — "vacuous round-trip" wording unclear
**ASN-0047, K.μ~ definition section**: "When dom_C(M(d)) ≠ ∅, this decomposes into a vacuous K.μ⁻ + K.μ⁺ round-trip"
**Problem**: For π = id with non-empty content subspace, "vacuous" is ambiguous: K.μ⁻ has strict-contraction precondition (`dom(M'(d)) ⊂ dom(M(d))`), so an actually-vacuous K.μ⁻ step is invalid. The intended decomposition is presumably the n' = 0 path used in the ExtendedReachableStateInvariants proof — remove all content-subspace positions, then re-add identically — but this is non-vacuous at the elementary level. A reader trying to verify the decomposition steps cannot tell whether "vacuous" means zero steps or non-trivial steps netting to identity.
**Required**: State the π = id decomposition explicitly: either "expands into zero elementary steps" (treating K.μ~ as identity-permitted regardless of dom_C) or "remove all content-subspace positions then re-add them at identical positions with identical values" (the n' = 0 elementary path).

## OUT_OF_SCOPE

### Topic 1: Link withdrawal semantics
**Why out of scope**: The ASN flags withdrawal invariants as an open question and defers the precise mechanism (active/inactive status vs M(d) removal) to a future ASN. Resolving this would also resolve the link-subspace tombstoning question that Issue 2 surfaces.

### Topic 2: Concurrency and serialization of K.λ within a document
**Why out of scope**: Sequential allocator discipline assumes single-writer semantics. Concurrent allocation under the same document requires an atomicity protocol — already noted in the Scope section.

VERDICT: REVISE
