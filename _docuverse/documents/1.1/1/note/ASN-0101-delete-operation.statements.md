# ASN-0101 Claim Statements

*Source: ASN-0101-delete-operation.md (revised 2026-05-27) — Extracted: 2026-06-03*

## D0 — DelOperation (SPEC, OPERATION)

**Parameters.** A document `d` and a level-uniform V-span `σ = (s, ℓ_σ)` of ordinal type. *Notational convention.* `ℓ_σ` is the span width of `σ`; `ℓ` is reserved for link addresses.

*Preconditions.*

- *Document membership:* `d ∈ dom(M)`.
- *Span well-formedness:* `s ∈ V_S(d)` for some subspace `S = subspace(s) ∈ {s_C, s_L}`; `Pos(ℓ_σ)`; `#ℓ_σ = #s = m_S`; the action point of `ℓ_σ` is `m_S` (equivalently `ℓ_σ = δ(n, m_S)` for some `n ≥ 1`).
- *Containment:* writing `r := s ⊕ ℓ_σ`, every depth-`m_S` position `v` with `subspace(v) = S` and `s ≤ v < r` lies in `V_S(d)`. Under D-SEQ★ this reduces to `s = [S, 1, ..., 1, p]` for some `p ∈ {1, ..., n_S}` and `p + n − 1 ≤ n_S`, equivalently `p + n ≤ n_S + 1`.

*Regions.* Let `Λ := {v ∈ V_S(d) : v < s}`, `X := {v ∈ V_S(d) : s ≤ v < r}`, `Π := {v ∈ V_S(d) : v ≥ r}`.

*Shift function.* `σ_d : Π → T` where `σ_d(v)` is the unique tumbler `u ∈ T` satisfying `shift(u, n) = v`. For each `v = [S, 1, ..., 1, k] ∈ Π` with `k ≥ p + n`, `σ_d(v) = [S, 1, ..., 1, k − n]`. `Q := {σ_d(v) : v ∈ Π} = {[S, 1, ..., 1, j] : p ≤ j ≤ n_S − n}`.

*Effect.* The post-state arrangement `M'(d)` satisfies:

- *Domain:* `V_S(M'(d)) = Λ ∪ Q`, and `V_{S'}(M'(d)) = V_{S'}(d)` for every `S' ∈ {s_C, s_L}` with `S' ≠ S`.
- *Values, left of the cut:* `(A v ∈ Λ :: M'(d)(v) = M(d)(v))`.
- *Values, shifted right of the cut:* `(A v ∈ Π :: M'(d)(σ_d(v)) = M(d)(v))`.
- *Values, other subspace:* `(A v : v ∈ V_{S'}(d) ∧ S' ≠ S :: M'(d)(v) = M(d)(v))`.

*Frame.*

- *Content store:* `C' = C` exactly — `dom(C') = dom(C)` and `(A a ∈ dom(C) :: C'(a) = C(a))`.
- *Link store:* `L' = L` exactly — `dom(L') = dom(L)` and `(A ℓ ∈ dom(L) :: L'(ℓ) = L(ℓ))`.
- *Entity set:* `E' = E` exactly.
- *Provenance:* `R' = R` exactly.
- *Document set:* `dom(M') = dom(M)`.
- *Other documents:* `(A d' ∈ dom(M) : d' ≠ d :: M'(d') = M(d'))`.

DEL is a new atomic transition kind extending the foundation's transition vocabulary `{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ, K.σ}`.

---

## D1 — GapClosure (LEMMA, lemma)

Let `Σ → Σ'` be a DEL[d, σ] transition with `σ = (s, ℓ_σ)`. The shift function `σ_d` is an order-preserving bijection from `Π` onto `Q`. Writing `n_S' := |V_S(d)| − n`: when `n_S' ≥ 1`, `V_S(M'(d)) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S'}` is contiguous with minimum `[S, 1, ..., 1]` of depth `m_S`; when `n_S' = 0`, `V_S(M'(d)) = ∅` and D-CTG★, D-MIN★, D-SEQ★ hold vacuously for subspace `S`.

---

## D2 — ContentImmutabilityUnderDelete (LEMMA, lemma)

For every transition `Σ → Σ'` arising from DEL[d, σ]:

`dom(C') = dom(C)  ∧  (A a ∈ dom(C) :: C'(a) = C(a))`

---

## D3 — LinkStoreImmutabilityUnderDelete (LEMMA, lemma)

For every transition `Σ → Σ'` arising from DEL[d, σ]:

`dom(L') = dom(L)  ∧  (A ℓ ∈ dom(L) :: L'(ℓ) = L(ℓ))`

---

## D4 — DocumentIdentityPersistenceUnderDelete (LEMMA, lemma)

For every transition `Σ → Σ'` arising from DEL[d, σ]:

`d ∈ dom(M')  ∧  dom(M') = dom(M)`

---

## D5 — CrossDocumentArrangementIsolationUnderDelete (LEMMA, lemma)

For every transition `Σ → Σ'` arising from DEL[d, σ]:

`(A d' ∈ dom(M) : d' ≠ d :: M'(d') = M(d'))`

---

## D6 — SubspaceIsolationUnderDelete (LEMMA, lemma)

For every transition `Σ → Σ'` arising from DEL[d, σ] with `S = subspace(s)`:

`(A S' ∈ {s_C, s_L} : S' ≠ S :: V_{S'}(M'(d)) = V_{S'}(d)  ∧  (A v ∈ V_{S'}(d) :: M'(d)(v) = M(d)(v)))`

---

## D7 — AttributionSurvivalUnderDelete (LEMMA, lemma)

For every transition `Σ → Σ'` arising from DEL[d, σ] and every I-address `a` with `a ∈ ran(M(d))` at the pre-state `Σ`:

`a ∈ dom(C') ∪ dom(L')  ∧  origin(a) at Σ' = origin(a) at Σ`

Equivalently, restricted by subspace: when `subspace_I(a) = s_C`, `a ∈ dom(C')`; when `subspace_I(a) = s_L`, `a ∈ dom(L')`. By L14 (store disjointness), these are mutually exclusive.

---

## D8 — ArrangementWellFormednessPreservationUnderDelete (LEMMA, lemma)

For every transition `Σ → Σ'` arising from DEL[d, σ], the post-state satisfies every foundation invariant that the pre-state was required to satisfy. The invariants partition into three groups:

*Group (i): Arrangement invariants on the modified document `d`.* The post-state arrangement `M'(d)` satisfies:

- *Functionality (S2):* `M'(d)` is a well-defined partial function.
- *Finite domain (S8-fin):* `|dom(M'(d))| < ∞`.
- *Well-formed V-positions (S8a):* `(A v ∈ dom(M'(d)) :: zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))`.
- *Per-subspace common depth (S8-depth):* within each subspace, all V-positions share a common depth.
- *Referential integrity (S3★):* `(A v ∈ dom(M'(d)) :: (subspace(v) = s_C ⟹ M'(d)(v) ∈ dom(C')) ∧ (subspace(v) = s_L ⟹ M'(d)(v) ∈ dom(L')))`.
- *Per-subspace contiguity, minimum, sequentiality (D-CTG★, D-MIN★, D-SEQ★):* `V_S(M'(d)) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S − n}` for the affected subspace; unchanged for the other. When `n_S − n = 0`, all three predicates hold vacuously for subspace `S`.
- *Per-subspace span decomposition (S8★):* the per-subspace arrangement decomposes into finite correspondence runs.
- *Subspace exhaustiveness (S3★-aux):* every V-position lies in `s_C` or `s_L`.
- *Link-subspace ownership (CL-OWN):* every link-subspace V-position maps to a link with `origin = d`.
- *Link-subspace position uniqueness (CL-UNIQ):* the link-subspace restriction is injective.

*Group (ii): Allocation and store invariants.* All of M0, S4, S7a, S7b, S7d, C1, C1b, C1c, C2, L0, L1, L1a, L1b, L1c, L3, L12, SD, L-fin, C-fin, NodeLineage, ActivatedEmission hold trivially at the post-state because `C' = C`, `L' = L`, `E' = E`, and `dom(M') = dom(M)` by D0's frame. Likewise the substrate-level chain-discipline lemmas — ChainElementT4Validity, ChainEnumerationInjectivity, DisjointSubAllocatorChains, ChainPrefixExtension, ChainMembershipForOrigin, StoreT4Validity, FirstEmissionFreshness, and CrossDocumentDisjointness — hold trivially.

*Group (iii): Transition and per-state invariants discharged by frame.* M1, C0, P0, P1, P2, P3, P4★, P4a, P6, P7, P7a, P8, and L12a, L12b all hold at the post-state, each preserved trivially under D0's frame because the components they predicate over — `(C, L, E, R, dom(M))` — are pointwise unchanged. P4★ specifically: `Contains_C(Σ') ⊆ Contains_C(Σ) ⊆ R = R'`.

---

## D9 — LinkProjectionUnderDelete (LEMMA, lemma)

For every link `ℓ ∈ dom(L)`, every slot `i`, every DEL[d, σ] transition `Σ → Σ'`, and every document `d'' ∈ dom(M)`:

- If `d'' ≠ d`: `project(L'(ℓ).eᵢ, d'', Σ') = project(L(ℓ).eᵢ, d'', Σ)`.
- If `d'' = d`, restricted to the unique subspace `S' ∈ {s_C, s_L}` with `S' ≠ S`: `project(L'(ℓ).eᵢ, d, Σ') ∩ V_{S'}(d) = project(L(ℓ).eᵢ, d, Σ) ∩ V_{S'}(d)`.
- If `d'' = d`, restricted to subspace `S`: `project(L'(ℓ).eᵢ, d, Σ') ∩ V_S(M'(d)) = (project(L(ℓ).eᵢ, d, Σ) ∩ Λ) ∪ {σ_d(v) : v ∈ project(L(ℓ).eᵢ, d, Σ) ∩ Π}`.

The full post-state projection at `d'' = d` is recovered as:
```
project(L'(ℓ).eᵢ, d, Σ')
  = (project(L(ℓ).eᵢ, d, Σ) ∩ V_{S'}(d))
  ∪ (project(L(ℓ).eᵢ, d, Σ) ∩ Λ) ∪ {σ_d(v) : v ∈ project(L(ℓ).eᵢ, d, Σ) ∩ Π}
```

---

## D10 — ValidCompositeExtensionUnderDelete (LEMMA, lemma)

ASN-0047's ValidComposite★ is extended to admit DEL as an elementary transition. A composite transition `Σ →* Σ'` is *valid* iff it is a finite sequence of atomic transitions

`Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ'`

drawn from the extended vocabulary `{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ, K.σ, DEL}`, satisfying:

(1) *Transition preconditions.* Each step `Σᵢ → Σᵢ₊₁` satisfies the elementary precondition of its transition kind, evaluated at `Σᵢ`. For a DEL step, this is D0's precondition.

(2) *Coupling constraints.* J0, J1★, and J1'★ (ASN-0047) hold between `Σ` and `Σ'` for the composite as a whole.

A single DEL transition viewed as a one-step composite `Σ → Σ'` satisfies J0, J1★, and J1'★ *vacuously*:

- *J0 (AllocationRequiresPlacement):* quantifies over `a ∈ dom(C') \ dom(C)`. By D2, `dom(C') = dom(C)`, so `dom(C') \ dom(C) = ∅` and the implication is vacuous.
- *J1★ (ExtensionRecordsProvenanceContentSubspace):* every post-state content-subspace V-position `v ∈ V_{s_C}(M'(d))` has a pre-state source `u ∈ dom(M(d))` with `M(d)(u) = M'(d)(v)`, so the antecedent — "no `v ∈ dom(M(d))` with subspace `s_C` mapped to `a`" — is false for every `(a, d)` pair; vacuous.
- *J1'★ (ProvenanceRequiresExtensionContentSubspace):* `R' = R` by D0's frame, so `R' \ R = ∅`; vacuous.

Multi-step composites containing DEL are *not* automatically valid: DEL can remove the V-position witness required to discharge an earlier step's allocation obligation under J0.

LP-family extension catalogue (ASN-0098): LP2★, LP3★, LP13 extend to DEL via D3; LP4, LP5 via D5; LP6, LP7, LP8, LP14, LP9, LP10, LP11 are vocabulary-disjoint from DEL with D9 supplying the DEL-specific projection characterisation; LP12 applies state-relatively to the post-state; LP12a, LP12b are supplanted for DEL by D11; LP16, LP17, LP20, LP21 apply state-relatively to the post-state directly; LP18 extends through DEL via Store Monotonicity★ and LP3★; LP19, LP19a are unaffected with DEL absorbed via Store Monotonicity★ on prefix sequences.

---

## D11 — WeakestPreconditionsForProjectionPostconditions (LEMMA, lemma)

Let `Σ → Σ'` be a DEL[d, σ] transition with `σ = (s, ℓ_σ)` of subspace `S`, and let `Λ`, `X`, `Π ⊆ V_S(d)` be the regions of D0. Write `Q_disc(ℓ, d)` for the post-state predicate `discoverable_from(ℓ, d, ·)`, and `Q_card(ℓ, i, d, k)` for the post-state predicate `|project(L(ℓ).eᵢ, d, ·)| = k`. Write `enabled(DEL[d, σ])` for DEL's applicability predicate (the conjunction of D0's preconditions) which is exactly `wp(DEL[d, σ], true)`.

- *wp for post-DELETE discoverability from `d`:*
  ```
  wp(DEL[d, σ], Q_disc(ℓ, d)) ≡ enabled(DEL[d, σ]) ∧ (E i : 1 ≤ i ≤ |L(ℓ)| : project(L(ℓ).eᵢ, d, Σ) ⊄ X)
  ```
  Negation:
  ```
  wp(DEL[d, σ], ¬Q_disc(ℓ, d)) ≡ enabled(DEL[d, σ]) ∧ (A i : 1 ≤ i ≤ |L(ℓ)| : project(L(ℓ).eᵢ, d, Σ) ⊆ X)
  ```

- *wp for post-DELETE discoverability from a different document `d'' ≠ d` (with `d'' ∈ dom(M)`):*
  ```
  wp(DEL[d, σ], discoverable_from(ℓ, d'', ·)) ≡ enabled(DEL[d, σ]) ∧ discoverable_from(ℓ, d'', Σ)
  ```

- *wp for post-DELETE projection cardinality from `d`:*
  ```
  wp(DEL[d, σ], Q_card(ℓ, i, d, k)) ≡ enabled(DEL[d, σ]) ∧ |project(L(ℓ).eᵢ, d, Σ)| − |project(L(ℓ).eᵢ, d, Σ) ∩ X| = k
  ```
  Cardinality preservation specialisation:
  ```
  wp(DEL[d, σ], |project(L(ℓ).eᵢ, d, ·)| = |project(L(ℓ).eᵢ, d, Σ)|) ≡ enabled(DEL[d, σ]) ∧ project(L(ℓ).eᵢ, d, Σ) ∩ X = ∅
  ```

- *wp for post-DELETE projection cardinality from a different document `d'' ≠ d` (with `d'' ∈ dom(M)`):*
  ```
  wp(DEL[d, σ], |project(L(ℓ).eᵢ, d'', ·)| = k) ≡ enabled(DEL[d, σ]) ∧ |project(L(ℓ).eᵢ, d'', Σ)| = k
  ```
