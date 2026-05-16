# Review of ASN-0051

## REVISE

### Issue 1: SV10 witness violates J0 (AllocationRequiresPlacement)

**ASN-0051, "Concrete witness." paragraph in SV10**: "K.α allocates the three element-level content addresses i₁, i₂, i₃ under d's prefix with fields(i_k).E₁ = s_C..." followed by a single "K.μ⁺ extends M(d) from V_{s_C}(d) = ∅ by adding v₁ ↦ i₂".

**Problem**: J0 (ASN-0047) requires every newly allocated content address to be placed in some `M(d)` at the composite's post-state — `(A Σ → Σ', a : a ∈ dom(C') \ dom(C) : (E d, v : d ∈ E'_doc ∧ v ∈ dom(M'(d)) : M'(d)(v) = a))`. The witness allocates i₁, i₂, i₃ but places only i₂; the composite from Σ₀ to Σ fails J0 for i₁ and i₃. Σ is therefore not reachable by any valid composite from Σ₀ under ValidCompositeExtended, so SV10's existential ("there exists a state Σ...") is not actually witnessed by the construction given.

**Required**: Drop K.α(i₁) and K.α(i₃) from the chain. The span (i₁, ℓ_span) is well-formed under T12 regardless of whether i₁ ∈ dom(C), and coverage(F) = ⟦(i₁, ℓ_span)⟧ contains i₁, i₂, i₃ as tumblers in T independently of allocation status. With only i₂ allocated and placed at v₁, π(F, d) = {i₂} ⊊ coverage(F) holds and A = {i₂} ⊆ dom(Σ.C) for the discovery clause.

### Issue 2: CrossDocumentDecoupling inherits SV10's J0 violation

**ASN-0051, CrossDocumentDecoupling witness**: "Extend the SV10 witness." The corollary's Step 1–3 chain adds K.δ(d₂), K.α(j), K.μ⁺(v₁ ↦ j), K.ρ on top of the SV10 base state.

**Problem**: The SV10 base state itself fails J0 (Issue 1); the corollary's additional steps place j but leave i₁ and i₃ unplaced, so the composite from Σ₀ to Σ⁺ remains J0-invalid.

**Required**: Apply Issue 1's fix to the SV10 setup that this corollary inherits.

### Issue 3: discover_s domain restriction A ⊆ dom(Σ.C) is unjustifiably narrow

**ASN-0051, "Link Discovery" definition**: "For a set of I-addresses A ⊆ dom(Σ.C) and an endset slot s ∈ {from, to, type}, define: discover_s(A) = {a ∈ dom(Σ.L) : coverage(Σ.L(a).s) ∩ A ≠ ∅}".

**Problem**: The restriction A ⊆ dom(Σ.C) excludes link-address queries from the discovery framework. L4 (EndsetGenerality, ASN-0043) and L13 (ReflexiveAddressing, ASN-0043) admit endsets that reference link addresses, and K.μ⁺_L (ASN-0047) places link addresses into ran(M(d)). The surrounding prose describes A as derived "via M(d)" without subspace constraint — "the system converts those V-positions to I-addresses via M(d)" — so A may naturally include link addresses, contradicting the formal restriction. The restriction also excludes natural use cases the rest of the system supports (reverse-link discovery, type queries against the link-typed hierarchy).

**Required**: Either (a) relax to A ⊆ T so the definition matches the prose's I-space framing, or (b) explicitly justify the content-only restriction as a scope decision and update CrossDocumentDecoupling's "A ⊆ ran(Σ.M(d₁))" to indicate A is the content-subspace slice. Option (a) is cleaner — all SV7–SV9 proofs read unchanged under it because they reference only coverage and dom(L), neither of which is constrained by A's subspace.

## OUT_OF_SCOPE

### Topic 1: Link-subspace contribution to projection

SV11's m·p decomposition explicitly handles only the text-subspace contribution π_text(e, d); the full π(e, d) may include link-subspace contributions from K.μ⁺_L mappings, and the reflexive-addressing case (L13) is acknowledged. The ASN cleanly defers this to a future Link Subspace ASN.

### Topic 2: Same-origin coverage growth at element level

The "Content Allocation and Coverage Stability" section identifies sequential overshoot and child-depth entry as mechanisms by which same-origin allocations can enter existing endset coverage but makes no formal SV claim, deferring the allocator-discipline analysis to ASN-0034. The descriptive treatment suffices to motivate SV6 and the architectural framing of coverage stability.

### Topic 3: Broader-level spans (action point k ≤ p₃)

SV6 restricts to k > p₃. The note on scope acknowledges broader-level spans as Nelson's design feature (admitting future-content discovery via prefix-level reach) and defers their formal treatment to ASN-0034's address-hierarchy machinery; the SV6 boundary at k = p₃ is structurally consequential but not nominally designated in Nelson, which the note correctly observes.

VERDICT: REVISE
