# ASN-0063 Claim Statements

*Source: ASN-0063-createlink-operation.md (revised 2026-03-22) — Extracted: 2026-03-22*

## Definition — VSpanImage

For document d with arrangement M(d) and V-span σ_v = (v_s, w_v) satisfying T12 (SpanWellDefined, ASN-0034):

`image(d, σ_v) = {M(d)(v) : v ∈ ⟦σ_v⟧ ∩ dom(M(d))}`

For a V-span-set Ψ = {σ₁, ..., σₖ} where each σᵢ satisfies T12:

`image(d, Ψ) = (∪ i : 1 ≤ i ≤ k : image(d, σᵢ))`

## Definition — Resolve

`resolve(d, Ψ) = {ρ_{β,σ} : σ ∈ Ψ, β ∈ B, V(β) ∩ ⟦σ⟧ ≠ ∅}`

where B is the canonical block decomposition of M(d) and each `ρ_{β,σ}` is the I-span produced by CL0 for block β and V-span σ.

Extended form: for endset specification S = {(d₁, Ψ₁), ..., (dₘ, Ψₘ)}, `resolve(S) = resolve(d₁, Ψ₁) ∪ ... ∪ resolve(dₘ, Ψₘ)`.

For direct I-span-set form: `resolve(E_I) = E_I`.

## Definition — ContentContainment

`Contains_C(Σ) = {(a, d) : d ∈ E_doc ∧ (E v : v ∈ dom(M(d)) ∧ subspace(v) = s_C : M(d)(v) = a)}`

## Definition — DiscoveryFunction

For I-address a and role r ∈ {from, to, type}:

`disc(a, r) = {ℓ ∈ dom(L) : a ∈ coverage(L(ℓ).r)}`

For a set of I-addresses S:

`disc(S, r) = {ℓ ∈ dom(L) : S ∩ coverage(L(ℓ).r) ≠ ∅}`

---

## CL0 — BlockProjection (LEMMA)

Let β = (v_β, a_β, n) be a mapping block and σ_v a V-span in the same subspace. Precondition: `V(β) ∩ ⟦σ_v⟧ ≠ ∅`.

The non-empty intersection of V(β) and ⟦σ_v⟧ is a contiguous sub-range of V(β) of the form `{v_β + k : c ≤ k < c'}` for some `0 ≤ c < c' ≤ n`. The I-span

`ρ = (a_β + c, δ(c' − c, #a_β))`

satisfies T12 (SpanWellDefined) and the depth-`#a_β` members of ⟦ρ⟧ are exactly `{a_β + k : c ≤ k < c'}` — the image of the overlap through β. That is, the image of `V(β) ∩ ⟦σ_v⟧` through β is representable by a single well-formed I-span whose same-depth denotation is exactly the image.

## CL1 — ResolutionExistence (LEMMA)

Precondition: M(d) satisfies S2 and S8-fin; every σ ∈ Ψ satisfies `subspace(start(σ)) = s_C ∧ width(σ)₁ = 0`.

`(E E : E ∈ Endset : image(d, Ψ) ⊆ coverage(E))`

## CL2 — ResolutionContainment (LEMMA)

Precondition: `(A σ ∈ Ψ : subspace(start(σ)) = s_C ∧ width(σ)₁ = 0)`.

`image(d, Ψ) ⊆ coverage(resolve(d, Ψ))`

---

## S3★ — GeneralizedReferentialIntegrity (INV)

`(A d, v : v ∈ dom(Σ.M(d)) : (subspace(v) = s_C ⟹ Σ.M(d)(v) ∈ dom(Σ.C)) ∧ (subspace(v) = s_L ⟹ Σ.M(d)(v) ∈ dom(Σ.L)))`

## S3★-aux — SubspaceExhaustiveness (INV)

In every reachable state:

`(A d, v : v ∈ dom(M(d)) : subspace(v) = s_C ∨ subspace(v) = s_L)`

## P4★ — ProvenanceBounds (INV)

`Contains_C(Σ) ⊆ R`

## CL-OWN — LinkSubspaceOwnership (INV)

In every reachable state:

`(A d, v : v ∈ dom(M(d)) ∧ subspace(v) = s_L : origin(M(d)(v)) = d)`

## J1★ — ExtensionRecordsProvenance (INV)

`(A Σ → Σ', d, v, a : v ∈ dom(M'(d)) \ dom(M(d)) ∧ subspace(v) = s_C ∧ M'(d)(v) = a : (a, d) ∈ R')`

## J1'★ — ProvenanceRequiresExtension (INV)

`(A Σ → Σ', a, d : (a, d) ∈ R' \ R : (E v : v ∈ dom(M'(d)) \ dom(M(d)) ∧ subspace(v) = s_C : M'(d)(v) = a))`

## P3★ — ArrangementMutabilityOnly (INV)

`(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ dom(L) ⊆ dom(L') ∧ E ⊆ E' ∧ R ⊆ R')`

Additionally, L admits only extension with values unchanged: `dom(L) ⊆ dom(L') ∧ (A ℓ ∈ dom(L) : L'(ℓ) = L(ℓ))`.

## P5★ — DestructionConfinement (INV)

For every state transition Σ → Σ':

  (a) `dom(C') ⊇ dom(C) ∧ (A a : a ∈ dom(C) : C'(a) = C(a))`

  (b) `dom(L') ⊇ dom(L) ∧ (A ℓ : ℓ ∈ dom(L) : L'(ℓ) = L(ℓ))`

  (c) `E' ⊇ E`

  (d) `R' ⊇ R`

---

## K.λ — LinkAllocation (TRANSITION)

*Precondition:*
- `d ∈ E_doc`
- `ℓ ∉ dom(L) ∪ dom(C)`
- `zeros(ℓ) = 3 ∧ fields(ℓ).E₁ = s_L`
- `origin(ℓ) = d`
- `(A ℓ' : ℓ' ∈ dom(L) ∧ origin(ℓ') = d : ℓ' < ℓ)`
- `(F, G, Θ) ∈ Link`

*Effect:* `L' = L ∪ {ℓ ↦ (F, G, Θ)}`

*Frame:* `C' = C; E' = E; (A d' :: M'(d') = M(d')); R' = R`

## K.α — ContentAllocationAmendment (AMENDMENT)

The allocated address must satisfy: `fields(a).E₁ = s_C`

## K.μ⁺ — ContentExtensionAmendment (AMENDMENT)

New V-positions must satisfy: `subspace(v) = s_C`

Postcondition: M'(d) satisfies D-CTG and D-MIN for each subspace.

## K.μ⁻ — ContentContractionAmendment (AMENDMENT)

Postcondition: M'(d) must satisfy D-CTG and D-MIN for each subspace.

By D-SEQ at the input state, V_S(d) for each non-empty subspace S is a contiguous ordinal range `{[S, 1, ..., 1, k] : 1 ≤ k ≤ n}`; the postcondition constrains contraction to removal from the maximum end of V_S(d) or removal of all positions in V_S(d).

## K.μ⁺_L — LinkSubspaceExtension (TRANSITION)

*Precondition:*
- `d ∈ E_doc`
- `ℓ ∈ dom(L)`
- `origin(ℓ) = d`
- `subspace(v_ℓ) = s_L`
- `m_L ≥ 2`, where m_L is the common depth of existing link-subspace V-positions if `V_{s_L}(d) ≠ ∅`, or a free parameter subject to `m_L ≥ 2` if `V_{s_L}(d) = ∅`
- If `V_{s_L}(d) = ∅`: `v_ℓ = [s_L, 1, ..., 1]` of depth m_L (D-MIN)
- If `V_{s_L}(d) ≠ ∅`: `v_ℓ = shift(max(V_{s_L}(d)), 1)` (D-CTG)
- `#v_ℓ = m_L`

*Effect:* `M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}`

*Frame:* `C' = C; L' = L; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R`

---

## CL3 — CreatelinkPostcondition (POST)

After CREATELINK(d, S_F, S_G, S_Θ) with F = resolve(S_F), G = resolve(S_G), Θ = resolve(S_Θ):

  (a) `ℓ ∈ dom(L') ∧ ℓ ∉ dom(L)`

  (b) `L'(ℓ) = (F, G, Θ)`

  (c) `home(ℓ) = origin(ℓ) = d`

  (d) `(A ℓ' : ℓ' ∈ dom(L) : L'(ℓ') = L(ℓ'))`

  (e) `C' = C`

  (f) `v_ℓ ∈ dom(M'(d)) ∧ M'(d)(v_ℓ) = ℓ`, where `v_ℓ = [s_L, 1, ..., 1]` (depth m_L) when V_{s_L}(d) was empty, or `v_ℓ = shift(max(V_{s_L}(d)), 1)` otherwise

  (g) `(A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))`

  (h) `E' = E`

  (i) `R' = R`

## CL4 — ContentNonInterference (LEMMA)

`C' = C`

## CL5 — LinkPreservation (LEMMA)

`dom(L) ⊆ dom(L') ∧ (A ℓ' : ℓ' ∈ dom(L) : L'(ℓ') = L(ℓ'))`

## CL6 — ArrangementConfinement (LEMMA)

`(A d' : d' ≠ d : M'(d') = M(d'))`

Additionally, the text-subspace mappings of M(d) are invariant: `{(v, M(d)(v)) : v ∈ dom(M(d)) ∧ subspace(v) = s_C}` is unchanged.

## CL7 — DiscoveryMonotonicity (LEMMA)

For every state transition Σ → Σ':

`(A a, r :: disc_Σ(a, r) ⊆ disc_Σ'(a, r))`

## CL8 — DiscoveryCompleteness (LEMMA)

After CREATELINK producing link ℓ with value (F, G, Θ):

`(A a : a ∈ coverage(F) : ℓ ∈ disc(a, from))`

`(A a : a ∈ coverage(G) : ℓ ∈ disc(a, to))`

`(A a : a ∈ coverage(Θ) : ℓ ∈ disc(a, type))`

## CL9 — DiscoveryIndependence (LEMMA)

`(A d₁, d₂, v₁, v₂ : M(d₁)(v₁) = a ∧ M(d₂)(v₂) = a : disc(a, r) is identical)`

disc consults L, not M.

## CL10 — LatentLinks (LEMMA)

A link ℓ is latent when: `(A a ∈ coverage(F) ∪ coverage(G) ∪ coverage(Θ) : (A d :: a ∉ ran(M(d))))` where `L(ℓ) = (F, G, Θ)`.

For such ℓ: `ℓ ∈ dom(L)` and `(A a ∈ coverage(L(ℓ).r) : ℓ ∈ disc(a, r))`.

If a later operation adds `v ↦ a` to some document d' for a covered address a, the link becomes discoverable from d' without any change to L or disc.

---

## CL11 — InvariantPreservation (THEOREM)

CREATELINK preserves the full invariant set:

S0 ∧ S1 ∧ S2 ∧ S3★ ∧ S3★-aux ∧ S8a ∧ S8-fin ∧ S8-depth ∧ S8 ∧ D-CTG ∧ D-MIN ∧ P0 ∧ P1 ∧ P2 ∧ P3★ ∧ P4★ ∧ P5★ ∧ P6 ∧ P7 ∧ P7a ∧ P8 ∧ L0 ∧ L1 ∧ L1a ∧ L12 ∧ L12a ∧ L14 ∧ J1★ ∧ J1'★ ∧ CL-OWN

Specific obligations:
- S3★: text-subspace mappings unchanged (target dom(C)); new link-subspace mapping `v_ℓ ↦ ℓ` satisfies `ℓ ∈ dom(L')` with `subspace(v_ℓ) = s_L`
- P4★: `subspace(v_ℓ) = s_L ≠ s_C`, so `ℓ ∉ Contains_C(Σ')`; `Contains_C(Σ') = Contains_C(Σ) ⊆ R = R'`
- J1★: vacuous, since `subspace(v_ℓ) = s_L ≠ s_C`
- J1'★: vacuous, since `R' = R`
- L0: `fields(ℓ).E₁ = s_L`; `dom(L') ∩ dom(C') = ∅` since `ℓ ∉ dom(C)`

## ExtendedReachableStateInvariants — ExtendedReachableStateInvariants (THEOREM)

Every state reachable from Σ₀ = (C₀, L₀, E₀, M₀, R₀) with L₀ = ∅ by a finite sequence of valid composite transitions composed from K.α (amended), K.δ, K.λ, K.μ⁺ (amended), K.μ⁺_L, K.μ⁻ (amended), K.μ~, and K.ρ satisfies:

`S0 ∧ S1 ∧ S2 ∧ S3★ ∧ S3★-aux ∧ S8a ∧ S8-fin ∧ S8-depth ∧ S8 ∧ D-CTG ∧ D-MIN ∧ P0 ∧ P1 ∧ P2 ∧ P3★ ∧ P4★ ∧ P5★ ∧ P6 ∧ P7 ∧ P7a ∧ P8 ∧ L0 ∧ L1 ∧ L1a ∧ L12 ∧ L14 ∧ CL-OWN`
