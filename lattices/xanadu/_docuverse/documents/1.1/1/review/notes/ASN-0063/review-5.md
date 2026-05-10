# Review of ASN-0063

## REVISE

### Issue 1: K.μ~ preservation of S3★ is asserted without proof
**ASN-0063, CL11 — InvariantPreservation, S3★ paragraph**: "K.μ~ reorders within a fixed multiset of I-addresses, preserving both target stores."
**Problem**: K.μ~ is defined (ASN-0047) as a distinguished composite K.μ⁻ + K.μ⁺. With K.μ⁺ amended to content-subspace only, K.μ~ can remove link-subspace V-positions (via K.μ⁻) but cannot recreate them (K.μ⁺ rejects `subspace(v) = s_L`). The bijection requirement `π : dom(M(d)) → dom(M'(d))` then forces link-subspace mappings to remain fixed — if K.μ⁻ removed a link-subspace position, the bijection would need to place its I-address (in dom(L)) under a content-subspace V-position, violating S3★. This argument is sound but unstated. The ASN treats it as self-evident in one clause.
**Required**: State the argument: (1) K.μ⁺ (amended) cannot produce link-subspace V-positions; (2) therefore K.μ⁻ cannot remove them without breaking the bijection; (3) therefore K.μ~ fixes all link-subspace mappings; (4) content-subspace mappings are reordered within dom(C), preserving S3★'s content clause. Three sentences suffice.

### Issue 2: CL3 postcondition omits the arrangement change
**ASN-0063, CREATELINK composite, CL3**: "(a) ℓ ∈ dom(L')... (b) L'(ℓ) = (F, G, Θ)... (c) home(ℓ) = d... (d) existing links unchanged... (e) C' = C"
**Problem**: The postcondition describes what happened to L and C but not to M(d). Step 2 (K.μ⁺_L) creates a specific V-position v_ℓ in d's link subspace with M'(d)(v_ℓ) = ℓ. This is the out-link placement — architecturally central — yet it is absent from the formal postcondition. CL6 (ArrangementConfinement) says other documents are unchanged, but neither CL3 nor CL6 positively states the new mapping or characterizes v_ℓ.
**Required**: Add to CL3: `(f) v_ℓ ∈ dom(M'(d)) ∧ M'(d)(v_ℓ) = ℓ`, where v_ℓ is [s_L, 1, ..., 1] (depth m_L) when V_{s_L}(d) was empty, or shift(max(V_{s_L}(d)), 1) otherwise. Also add `(g) (A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))` — the existing arrangement of d is unchanged.

### Issue 3: K.μ⁺_L precondition uses post-state notation
**ASN-0063, K.μ⁺_L definition, Precondition**: "ℓ ∈ dom(L')  (the target link must already exist — K.λ must precede this step)"
**Problem**: ASN-0047's convention is that elementary-transition preconditions reference the pre-state using unprimed variables. K.μ⁺_L's own frame says `L' = L` (it does not modify L), so `dom(L') = dom(L)`. The precondition should reference the pre-state L — which, in the composite context, is the state after K.λ has already added ℓ. Writing `dom(L')` suggests the post-state of K.μ⁺_L itself, creating ambiguity. Compare K.μ⁺ (ASN-0047): "for every new mapping M'(d)(v) = a, `a ∈ dom(C)`" — unprimed C, referencing the pre-state.
**Required**: Change to `ℓ ∈ dom(L)`. The parenthetical explaining K.λ ordering is fine.

### Issue 4: CL2 claimed for the direct I-span form where it does not apply
**ASN-0063, Endset Resolution, resolve extension**: "CL2 (ResolutionContainment) holds trivially for the direct form: coverage(E_I) ⊆ coverage(resolve(E_I)) = coverage(E_I). CL1 likewise: the endset itself witnesses existence."
**Problem**: CL2 is stated as `image(d, Ψ) ⊆ coverage(resolve(d, Ψ))` — it requires a document d and V-span-set Ψ. The direct I-span form has neither; it bypasses V-space resolution entirely. The tautology `coverage(E_I) ⊆ coverage(E_I)` does not instantiate CL2; it is a different (trivial) statement. The ASN's goal — showing both input forms produce valid endsets without case-splitting in the postconditions — is correct, but the claim that CL2 "holds" for the direct form is a category error.
**Required**: Either (a) generalize CL2 to cover both forms (e.g., define a uniform notion of "intended coverage" for both V-space and direct specifications, then state containment), or (b) state explicitly that CL2 applies only to the V-space form and that the direct form needs no resolution guarantee because the user provides the endset directly.

## OUT_OF_SCOPE

### Topic 1: Fork composite behavior with amended K.μ⁺
**Why out of scope**: ASN-0063 amends K.μ⁺ with a content-subspace restriction, which affects Fork (J4, ASN-0047) since Fork uses K.μ⁺ to populate the new document. The question — whether forking a document should copy its link-subspace mappings — is a design decision for the Fork/version-creation ASN, not an error in CREATELINK. K.μ⁺'s existing "a ∈ dom(C)" precondition already prevented Fork from mapping to link addresses, so the amendment is consistent with pre-existing behavior.

### Topic 2: Link subspace reordering
**Why out of scope**: The question of whether K.μ~ should be able to reorder link-subspace V-positions (e.g., to maintain some ordering invariant on out-links) is a design question for a future ASN. REVISE issue 1 requires stating that K.μ~ *cannot* reorder them given the current amendment; whether it *should* be able to is separate.

VERDICT: REVISE
