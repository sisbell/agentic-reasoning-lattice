# Review of ASN-0063

## REVISE

### Issue 1: S8 derivation chain cites wrong dependencies
**ASN-0063, ExtendedReachableStateInvariants proof (K.μ⁻, K.μ⁺, K.μ~ cases)**: "S8 follows from the now-established D-CTG, D-MIN, S8-fin, S8a, S2, S8-depth via the derivation chain in ASN-0036"
**Problem**: ASN-0036 derives S8 (SpanDecomposition) from `S8-fin, S8a, S2, S8-depth, T5, PrefixOrderingExtension, TA5(c), TA7a`. D-CTG and D-MIN are not among S8's dependencies — S8 decomposes whatever V-positions exist into correspondence runs regardless of whether those positions form a contiguous range. D-SEQ depends on D-CTG and D-MIN; S8 does not. This error appears three times in the inductive step (once each for K.μ⁻, K.μ⁺, K.μ~).
**Required**: Replace "D-CTG, D-MIN, S8-fin, S8a, S2, S8-depth" with "S8-fin, S8a, S2, S8-depth, T5, TA5(c), TA7a" in all three occurrences, matching ASN-0036's stated derivation chain.

### Issue 2: K.μ⁺_L permits foreign link placement without justification
**ASN-0063, K.μ⁺_L precondition**: "ℓ ∈ dom(L) (the target link must already exist in dom(L) — placed there by some prior K.λ)"
**Problem**: The precondition requires `ℓ ∈ dom(L)` but not `origin(ℓ) = d`. This permits placing links created by other documents into d's link subspace — a form of "link transclusion" that the ASN neither discusses nor justifies. CREATELINK is unaffected (K.λ guarantees `origin(ℓ) = d`), but K.μ⁺_L is defined as a general elementary transition available for arbitrary valid composites. K.μ⁺ (content extension) similarly lacks an origin restriction, permitting content transclusion — but content transclusion is a well-established architectural feature. Link transclusion is not discussed anywhere in the ASN, and it conflicts with the out-link ownership model quoted from Nelson: "a document consists of its contents… and its out-links, the links it contains." A document arranging a link with `origin(ℓ) ≠ d` would have an out-link it doesn't own.
**Required**: Either add `origin(ℓ) = d` to K.μ⁺_L's precondition (enforcing that documents arrange only their own links), or explicitly justify the omission — e.g., by analogy with content transclusion and a brief discussion of the architectural implications for out-link semantics. The current silence on this design decision is the problem.

### Issue 3: Contains_C definition omits domain membership
**ASN-0063, Definition — ContentContainment**: "Contains_C(Σ) = {(a, d) : d ∈ E_doc ∧ (E v : subspace(v) = s_C ∧ M(d)(v) = a)}"
**Problem**: The quantifier over v does not include `v ∈ dom(M(d))`. The condition `M(d)(v) = a` is meaningful only when `v ∈ dom(M(d))`, so the membership is implicit — but the foundation (ASN-0047) states Contains explicitly as `{(a, d) : d ∈ E_doc ∧ a ∈ ran(M(d))}`, making domain membership visible. The superseding definition should match the foundation's explicitness.
**Required**: Write `(E v : v ∈ dom(M(d)) ∧ subspace(v) = s_C : M(d)(v) = a)`.

## OUT_OF_SCOPE

### Topic 1: Link reordering mechanism
K.μ~ is proven to fix link-subspace mappings (positions and values unchanged). This is a derived consequence, not a design goal, but it means there is no mechanism to reorder links within a document's link subspace. If link ordering carries semantic weight (e.g., out-link display order), a link-specific reordering transition would be needed.
**Why out of scope**: The fixity is correctly derived within this ASN. Whether link reordering is needed is a future design question.

### Topic 2: Ownership-gated transitions
The ASN notes that "only the owner has a right to withdraw a document or change it" (Nelson, LM 2/29) but acknowledges this is "not yet formalized in the transition framework." K.α, K.μ⁺, K.λ, and K.μ⁺_L constrain structural validity but do not gate operations on ownership.
**Why out of scope**: Formalizing ownership gates is a cross-cutting concern affecting all transitions, not specific to CREATELINK.

### Topic 3: CL0 I-span level-uniformity
CL0 I-spans `(a_β + c, δ(c' − c, #a_β))` are level-uniform (`#start = #width = #a_β`) by construction. This property is not explicitly stated in CL0's conclusion but will matter when future ASNs apply span algebra operations (S1 intersection, S3 merge, S8 normalization) to resolved endsets, since those operations require level-uniform inputs.
**Why out of scope**: The property is derivable from the construction and is not needed for this ASN's conclusions.

VERDICT: REVISE
