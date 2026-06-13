# Review of ASN-0131

This is a careful, well-structured note. The image machinery and existence/discovery taxonomy are cited from ASN-0127 rather than rebuilt; the worked example genuinely exercises RE-OVL, RE-CLIP, per-endset surfacing, and RE-UNIT; RE-CWP supplies a non-trivial weakest precondition (the per-endset vs. per-link distinction against D-CWP is the right insight and the derivation checks out); RE-SEL, RE-UDIST, and the field-agreement disjointness argument for `e₃` are all sound. Two gaps survive, both in the stability claims.

## REVISE

### Issue 1: The editing taxonomy claims to exhaust the vocabulary but never classifies K.μ⁺_L

**ASN-0131, RE-EDIT and the "Stability" section**: "This is the complete vocabulary `{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ}` (ASN-0047): the three arrangement edits on `d` move it through the image, `K.λ` (ordinary or retracting) through `Σ.L` and the addressable population, and the rest leave it fixed."

**Problem**: The classification accounts for exactly seven of the eight named operations. The "three arrangement edits on `d`" are K.μ⁺, K.μ⁻, K.μ~ (the insertion/deletion/rearrangement the section develops); "the rest" is explicitly "K.α, K.δ, K.ρ, together with edits to documents other than d." **K.μ⁺_L is named in the vocabulary set but placed in no bucket.** This is not harmless: K.μ⁺_L manifestly edits `Σ.M(d)` (`M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}`, a strict extension), so a reader following "arrangement edits to `d` move it through the image" would wrongly conclude it can move the answer. In fact, for a content region it cannot — and the reason is precisely the content-subspace restriction this note imposes: K.μ⁺_L adds a V-position `v_ℓ` with `subspace(v_ℓ) = s_L ∉ W`, so `W ∩ dom(M(d))` and hence `image(W, d, Σ)` are unchanged, and its frame leaves `Σ.L` (so `Avail`/`addressable`) fixed. That `K.μ⁺_L` leaves the content-region answer fixed is exactly the kind of fact the `W ⊆ s_C` restriction was introduced to secure ("one of the points the content-subspace restriction buys us"), yet it is the one arrangement edit the taxonomy never states a verdict on. The exhaustiveness assertion is therefore unsubstantiated.

**Required**: Add K.μ⁺_L explicitly to the "leaves the content-region answer fixed" category, with the one-line reason: it adds only an `s_L` V-position not in the content-subspace `W`, so `image(W, d, Σ)` is unchanged (F-IMG-MONO sharpened to equality under `W ⊆ s_C`), and it frames `Σ.L`. Then all eight operations are classified and "exhausts the vocabulary" is earned.

### Issue 2: Retraction "removal only" is not discharged for the emitter's type slot

**ASN-0131, RE-RET (and the "Under retraction" prose)**: "the to-set covers only the link address `ℓ` (subspace `s_L`) and its extensions, none of which is a content address — by the field-agreement argument used for `e₃` above, a content `c` with `ℓ ≼ c` would force `E(c)₁ = E(ℓ)₁ = s_L ≠ s_C`; and `R` lies in the type subspace, disjoint from content for the same reason."

**Problem**: The conclusion that the retraction emitter `b = (∅, {(ℓ, δ(1, #ℓ))}, R)` "is never surfaced and a retraction's net effect on RE is removal only" requires **all three** of `b`'s endsets to miss the content image `I`. The from-slot (`coverage(∅) = ∅`) and to-slot (covering `ℓ`'s `s_L`-subtree) are discharged rigorously — the field-agreement argument genuinely applies to `ℓ`, since `ℓ` is established element-level with `E(ℓ)₁ = s_L` (L0/L1, ASN-0093). But the *type* slot `R` is not. "For the same reason" invokes the field-agreement argument, which requires `R`'s spans to start at element-level (`zeros = 3`) addresses with subspace identifier `≠ s_C`. ASN-0086's RetractionType gives the designated retraction type no such structural property — it is "any `R ∈ T_admissible` whose coverage selects the conventional retraction address set," and by L4 (EndsetGenerality) / L9 (TypeGhostPermission) a type endset may reference arbitrary addresses, content included. So `coverage(R) ∩ dom(Σ.C) = ∅` is asserted, not derived; if some address in `coverage(R)` lands in the region image, the emitter surfaces as `(3, R)` and the effect is *not* removal only.

This note's own Open Question 6 concedes the point: type endsets "ordinarily reference classifying addresses disjoint from content" — *ordinarily*, not always. RE-RET presents as proven what RE's own open questions treat as a contingency.

**Required**: Either (a) fix a structural property of the designated retraction type `R` that places `coverage(R)` outside content (e.g., a layer convention seating retraction-type spans at a dedicated non-`s_C` element-level subspace, after which the field-agreement argument legitimately transfers), or (b) state the type-slot disjointness as an explicit assumption rather than "for the same reason," and condition RE-RET's "removal only" / sole-bearer-removal conclusion on `coverage(R) ∩ dom(Σ.C) = ∅` — consistent with the "ordinarily" hedge already in Open Question 6.

## OUT_OF_SCOPE

None. The deferred topics (link-subspace regions, intersection-distributivity, rendered V-position mode, non-co-resident link stores, multiplicity preservation, whole-vs-touching-span surfacing) are appropriately routed to the open questions rather than over-claimed here, and the informal mentions of FINDLINKSFROMTOTHREE / FINDNEXTNLINKSFROMTOTHREE are prose contrasts, not claim dependencies.

VERDICT: REVISE
