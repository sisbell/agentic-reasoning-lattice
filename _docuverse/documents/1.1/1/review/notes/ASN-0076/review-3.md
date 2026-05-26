# Review of ASN-0076

## REVISE

### Issue 1: E0 admissibility proof is hand-waved
**ASN-0076, E0 EditLinkComposite**: "These conditions are independently discharged for the successor step and the supersession step."
**Problem**: E0 enumerates K.λ's four preconditions but discharges none of them. The "EDITLINK as a valid composite" paragraph that verifies ValidComposite★ defers elementary preconditions to E0 ("as discharged in E0 below"), and E0 in turn just asserts they are discharged. The circular reference leaves the following unverified at both the successor step and the supersession step:
- `ℓ_new ∉ dom(L_i) ∪ dom(C_i)` and `ℓ_sup ∉ dom(L_{i+1}) ∪ dom(C_{i+1})` at the respective pre-states
- `zeros(·) = 3 ∧ E(·)_1 = s_L ∧ #E(·) ≥ 2 ∧ origin(·) = d_new` for both fresh addresses
- The endset sequences satisfy L3 (specifically, every span ∈ Span, i.e., T12)
**Required**: Explicit per-step verification citing SubAllocatorAxiom (Subspace, FirstEmission/Subsequent, Namespace, Disjointness) and L11a for freshness and namespace properties.

### Issue 2: T12 satisfaction for supersession spans not verified
**ASN-0076, composite definition**: "E_from = { (ℓ_old, δ(1, #ℓ_old)) }, E_to = { (ℓ_new, δ(1, #ℓ_new)) }, E_type = { (τ_sup, δ(1, #τ_sup)) }"
**Problem**: For each span to be in `Span`, T12 must hold: `Pos(ℓ)` and `actionPoint(ℓ) ≤ #s`. The ASN constructs these spans but never discharges T12 for them. For `δ(1, m)`: `Pos` follows from OrdinalDisplacement (last component = 1); `actionPoint(δ(1, m)) = m` saturates the bound `≤ #x` with equality. This needs to be shown, not assumed.
**Required**: Discharge T12 for `E_from`, `E_to`, `E_type` explicitly, citing OrdinalDisplacement's postconditions on `Pos(δ(n, m))` and `actionPoint(δ(n, m)) = m`.

### Issue 3: K.λ emission case not addressed in composite
**ASN-0076, composite definition and E0**: "K.λ(d_new, ℓ_new, (e'_1, ..., e'_N)); K.λ(d_new, ℓ_sup, (E_from, E_to, E_type))"
**Problem**: K.λ has two distinct cases — first emission (`ℓ = [d.0.s_L.1]`) and subsequent emission (`ℓ = inc(max{...}, 0)`) — with different tumbler determinations. The composite treats `ℓ_new` and `ℓ_sup` as free names, but they are determined by K.λ's allocation rule given d_new's pre-state. For `ℓ_new` this splits into two sub-cases (d_new has prior link allocations or not); the worked example covers only the first-emission sub-case. For `ℓ_sup` the case is forced (subsequent, since `ℓ_new ∈ dom(L_1)`), but this is not stated.
**Required**: Address both sub-cases of `ℓ_new`'s allocation explicitly; identify `ℓ_sup` as always a subsequent emission.

### Issue 4: Worked example covers only a subset of claims
**ASN-0076, "A Worked Example"**: Verifies E1, E2, E4, E7, E10.
**Problem**: E0 (composite admissibility), E3, E5, E6, E8, E9 are not checked against the concrete scenario. The standards require verifying key postconditions against at least one specific scenario. E0 in particular — the foundational well-definedness claim — should be visibly discharged in the example.
**Required**: Verify E0 against the example (showing each K.λ precondition holds for each step with the named tumbler values); note for the others either an explicit verification or a one-line reason (e.g., E8 reduces to E1).

### Issue 5: "Supersession link" structural identification conflates structure with semantics
**ASN-0076, E4 prose**: "A supersession link, in our construction, is a link of arity 3 whose endsets are structured as in the composite definition..."
**Problem**: E4's structural witness (specific endset references) does not pick out supersession links from arbitrary links that happen to have arity-3 references. Identification depends entirely on the τ_sup convention, which is deferred to a future ASN. The Appendix's illustrative procedure ("Filters to those whose type-endset coverage matches a designated supersession address") presupposes a designated address that this ASN does not — and explicitly cannot — fix. E4 should be reworded to acknowledge it establishes only the structural witness, not the semantic designation.
**Required**: Reword E4 to make the structure/semantics distinction explicit; the claim establishes the spans are present in the endsets and discoverable, not that the link is identifiable as a supersession without an external τ_sup convention.

### Issue 6: Invariant inheritance from K.λ not made explicit
**ASN-0076, throughout**: No claim explicitly addresses that EDITLINK preserves L0, L1, L1a, L1b, L1c, L3, L12, L14, L-fin, CL-OWN, CL-UNIQ, S-invariants, etc.
**Problem**: ValidComposite★ verification gives access to ExtendedReachableStateInvariants, so invariant preservation follows — but the reader has to infer this. An ASN introducing a composite operation should cite the inheritance.
**Required**: Add a short claim (or expand E0) noting that EDITLINK, as a ValidComposite★, inherits all per-state invariants from K.λ via ASN-0047's ExtendedReachableStateInvariants theorem.

## OUT_OF_SCOPE

### Topic 1: τ_sup convention and supersession-type registry
Pinning τ_sup to a specific address and registering supersession as a distinguishable link type belongs to a future ASN on type-endset conventions. The ASN correctly defers this.

### Topic 2: Reader-side resolution policy
Reconciling divergent successors (E5), traversing chains of supersessions, handling counter-claims — these belong to a future link-search or version-resolution ASN.

### Topic 3: Content edit semantics
Whether following an edited link should lead to the original's or successor's referenced content (raised in Open Questions) belongs to a future content/version-derivation ASN.

VERDICT: REVISE
