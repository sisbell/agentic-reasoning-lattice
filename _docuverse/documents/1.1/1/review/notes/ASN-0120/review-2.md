# Review of ASN-0120

## REVISE

### Issue 1: `ρ(R, Σ) ⊆ dom(Σ.C)` is justified by the wrong referential-integrity invariant
**ASN-0120, "What the endset arguments name"**: "By referential integrity (S3), `ρ(R, Σ) ⊆ dom(Σ.C)`: every recovered address is real content."

**Problem**: The ASN builds explicitly on the ASN-0047 substrate (it cites `K.μ⁺_L`, `SubspaceConventionAxiom`, `s_L`/`s_C`). In that substrate a document's arrangement maps **both** content-subspace and link-subspace V-positions, and S3 (ASN-0036) is superseded by S3★ (ASN-0047): `subspace(v) = s_L ⟹ Σ.M(d)(v) ∈ dom(Σ.L)`. The spec-set definition permits `σ_j` "at the common V-position depth of its subspace" — i.e. either subspace. If a supplied V-span is a link-subspace span, `ρ` resolves to link addresses and `ρ(R, Σ) ⊄ dom(Σ.C)`. The cited S3 does not discharge the stated containment in this substrate.

**Required**: Either (a) add a precondition restricting each `σ_j` to the content subspace (`subspace(u_j) = s_C`) and then cite S3★ to land in `dom(Σ.C)`; or (b) state `ρ(R, Σ) ⊆ dom(Σ.C) ∪ dom(Σ.L)` and confine the main-body claims (ML1, ML2) to the content slice via subspace disjointness. As written the containment is asserted from an invariant that the operative substrate does not provide.

### Issue 2: Fact (a) of the ML9 derivation asserts a false universal about arrangement ranges
**ASN-0120, ML9 derivation, Fact (a)**: "Every image of an arrangement is content, `ran(Σ'.M(d')) ⊆ dom(Σ.C)` (S3), so intersecting with `coverage(eᵢ)` consults only its content part."

**Problem**: In the ASN-0047 substrate `ran(Σ'.M(d'))` contains the link-subspace images of `d'` (the link references seated by `K.μ⁺_L`), so `ran(Σ'.M(d')) ⊆ dom(Σ.C)` is simply false; the correct bound is `ran(Σ'.M(d')) ⊆ dom(Σ.C) ∪ dom(Σ.L)` (S3★). The *conclusion* `coverage(eᵢ) ∩ ran(Σ'.M(d')) = ρ(R_i, Σ) ∩ ran(Σ'.M(d'))` does survive — because content-subspace coverage cannot meet link-subspace images (`s_C ≠ s_L`) — but the stated reason is wrong, and the surviving argument needs the subspace-disjointness step that is currently omitted.

**Required**: Replace the S3 citation with S3★ and insert the explicit step: `coverage(eᵢ)` lies in `s_C` subtrees, link-subspace images lie in `s_L`, so `coverage(eᵢ) ∩ (link images) = ∅`, hence the intersection collapses to the content images. The same correction is needed for the `d' = d` boundary, where "coverage(eᵢ) … lie in content subtrees (subspace s_C)" silently assumes all three endsets (including the ghost-type endset of ML6) are content-subspace.

### Issue 3: The ML9 weakest precondition omits the operation's enabledness conjunct
**ASN-0120, ML9**: "`wp(makelink(d, R₁, R₂, R₃), discoverable_from(a, d', ·)) ≡ (E i : 1 ≤ i ≤ 3 : ρ(R_i, Σ) ∩ ran(Σ.M(d')) ≠ ∅)`."

**Problem**: `makelink` is a *partial* operation — ML6 introduces the precondition `ρ(R₃, Σ) ≠ ∅`, and ML0 requires `d ∈ dom(Σ.M)`. A weakest precondition for a postcondition over a partial operation must conjoin definedness; otherwise the formula asserts that the postcondition is reachable on inputs where no post-state exists (e.g. an empty type spec, which the operation rejects). The comparable foundation result, ASN-0098 LP12a, correctly writes `wp(...) ≡ enabled(K.μ⁻[d,R]) ∧ (…)`. This ASN drops the analogous `enabled` conjunct.

**Required**: State the wp as `enabled(makelink(d, R₁, R₂, R₃)) ∧ (E i : ρ(R_i, Σ) ∩ ran(Σ.M(d')) ≠ ∅)`, with `enabled` unfolding to at least `d ∈ dom(Σ.M) ∧ ρ(R₃, Σ) ≠ ∅` (and `d' ∈ dom(Σ.M)` for `discoverable_from` to be defined). The residence-independence conclusion is unaffected, but the analysis is incomplete without it.

## OUT_OF_SCOPE

### Topic 1: Endsets that reference link-subspace addresses (links pointing at links)
**Why out of scope**: Open Question 4 correctly defers this. Resolving the S3/S3★ tension in Issues 1–2 by restricting source spans to the content subspace would make this a clean future-ASN topic rather than a gap here.

### Topic 2: Meaning of an empty resolved from/to endset
**Why out of scope**: Open Question 2 defers the semantics of `ρ(R₁, Σ) = ∅` or `ρ(R₂, Σ) = ∅`. L3 constrains only the type slot, so empty non-type endsets are structurally admissible; their interpretation is genuinely new territory.

VERDICT: REVISE
