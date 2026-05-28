# ASN-0101 Claim Statements

*Source: ASN-0101-delete-operation.md (revised 2026-05-27) — Extracted: 2026-05-28*

---

## Definition — VSubspacePositions

For each document `d ∈ dom(M)` and each subspace `S ∈ {s_C, s_L}`:

`V_S(d) := {v ∈ dom(M(d)) : subspace(v) = S}`

By S8-depth, all V-positions in `V_S(d)` share a common depth `m_S ≥ 2`. By D-SEQ★, when non-empty `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` for some `n_S ≥ 1`.

---

## Definition — OrdinalDisplacement

`δ(n, m)` for the ordinal displacement of ASN-0034 — the tumbler `[0, ..., 0, n]` of length `m`.

---

## Definition — OrdinalShift

`shift(v, n)` for `v ⊕ δ(n, #v)`, the OrdinalShift advancing `v`'s last component by `n`.

Length-preservation postcondition: `#shift(u, n) = #u`.

OrdinalShiftBase: `shift(t, 0) = t`.

---

## Definition — DeleteRegions

Let `Σ → Σ'` be a DEL[d, σ] transition with `σ = (s, ℓ_σ)`, `r := s ⊕ ℓ_σ`, subspace `S = subspace(s)`:

- `Λ := {v ∈ V_S(d) : v < s}` (the *left region* — positions strictly before the deleted span)
- `X := {v ∈ V_S(d) : s ≤ v < r}` (positions in the deleted span)
- `Π := {v ∈ V_S(d) : v ≥ r}` (the *right region* — positions strictly after)

---

## Definition — ShiftFunction

The *shift function* `σ_d : Π → T` is defined by: `σ_d(v)` is the unique tumbler `u ∈ T` satisfying `shift(u, n) = v`.

Well-definedness: by length-preservation `#u = #v = m_S`; by TS2 (ShiftInjectivity, ASN-0034), at most one such `u` exists. For each `v = [S, 1, ..., 1, k] ∈ Π` with `k ≥ p + n`, `σ_d(v) = [S, 1, ..., 1, k − n]`.

The map `σ_d` is a bijection from `Π` onto `Q := {σ_d(v) : v ∈ Π} = {[S, 1, ..., 1, j] : p ≤ j ≤ n_S − n}`.

---

## D0 — DelOperation (SPEC, atomic_transition)

*Parameters.* A document `d` and a level-uniform V-span `σ = (s, ℓ_σ)` of ordinal type. `ℓ_σ` denotes the span width of `σ`.

*Preconditions.*

- *Document membership:* `d ∈ dom(M)`.
- *Span well-formedness:* `s ∈ V_S(d)` for some subspace `S = subspace(s) ∈ {s_C, s_L}`; `Pos(ℓ_σ)`; `#ℓ_σ = #s = m_S`; the action point of `ℓ_σ` is `m_S` (equivalently `ℓ_σ = δ(n, m_S)` for some `n ≥ 1`).
- *Containment:* writing `r := s ⊕ ℓ_σ`, every depth-`m_S` position `v` with `subspace(v) = S` and `s ≤ v < r` lies in `V_S(d)`. Under D-SEQ★ this reduces to `s = [S, 1, ..., 1, p]` for some `p ∈ {1, ..., n_S}` and `p + n − 1 ≤ n_S`, equivalently `p + n ≤ n_S + 1`.

*Effect.* Let `Λ`, `X`, `Π`, `Q`, `σ_d` be as in the definitions above. The post-state arrangement `M'(d)` satisfies:

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

DEL is a new atomic transition kind extending ASN-0047's transition vocabulary `{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ, K.σ}`.

---

## D1 — GapClosure (LEMMA, lemma)

Let `Σ → Σ'` be a DEL[d, σ] transition with `σ = (s, ℓ_σ)`. The shift function `σ_d` is an order-preserving bijection from `Π` onto `Q`. Writing `n_S' := |V_S(d)| − n`: when `n_S' ≥ 1`, `V_S(M'(d)) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S'}` is contiguous with minimum `[S, 1, ..., 1]` of depth `m_S`; when `n_S' = 0`, `V_S(M'(d)) = ∅` and D-CTG★, D-MIN★, D-SEQ★ hold vacuously for subspace `S`.

---

## D2 — ContentImmutability (INV, ensures)

For every transition `Σ → Σ'` arising from DEL[d, σ]:

`dom(C') = dom(C)  ∧  (A a ∈ dom(C) :: C'(a) = C(a))`

---

## D3 — LinkStoreImmutability (INV, ensures)

For every transition `Σ → Σ'` arising from DEL[d, σ]:

`dom(L') = dom(L)  ∧  (A ℓ ∈ dom(L) :: L'(ℓ) = L(ℓ))`

---

## D4 — DocumentIdentityPersistence (INV, ensures)

For every transition `Σ → Σ'` arising from DEL[d, σ]:

`d ∈ dom(M')  ∧  dom(M') = dom(M)`

---

## D5 — CrossDocumentIsolation (INV, ensures)

For every transition `Σ → Σ'` arising from DEL[d, σ]:

`(A d' ∈ dom(M) : d' ≠ d :: M'(d') = M(d'))`

---

## D6 — SubspaceIsolation (INV, ensures)

For every transition `Σ → Σ'` arising from DEL[d, σ] with `S = subspace(s)`:

`(A S' ∈ {s_C, s_L} : S' ≠ S :: V_{S'}(M'(d)) = V_{S'}(d)  ∧  (A v ∈ V_{S'}(d) :: M'(d)(v) = M(d)(v)))`

---

## D7 — AttributionSurvival (LEMMA, lemma)

For every transition `Σ → Σ'` arising from DEL[d, σ] and every I-address `a` with `a ∈ ran(M(d))` at the pre-state `Σ`:

`a ∈ dom(C') ∪ dom(L')  ∧  origin(a) at Σ' = origin(a) at Σ`

Equivalently, restricted by subspace: when `subspace_I(a) = s_C`, `a ∈ dom(C')`; when `subspace_I(a) = s_L`, `a ∈ dom(L')`. By L14 (store disjointness), these are mutually exclusive.

---

## D8 — WellFormednessPreservation (THEOREM, lemma)

For every transition `Σ → Σ'` arising from DEL[d, σ], the post-state satisfies every foundation invariant that the pre-state was required to satisfy. The invariants partition into three groups.

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

*Group (ii): Allocation and store invariants.* All of M0, S4, S7a, S7b, S7c, S7d, C1, C1b, C1c, C2, L0, L1, L1a, L1b, L1c, L3, L12, L14, L-fin, C-fin, NodeLineage (ASN-0036, ASN-0043, ASN-0093) hold trivially at the post-state because `C' = C`, `L' = L`, `E' = E`, and `dom(M') = dom(M)` by D0's frame. Likewise the substrate chain-discipline lemmas — ChainElementT4Validity, ChainUniformLength, ChainEnumerationInjectivity, ChainUniformZeroCount, DisjointSubAllocatorChains, ChainPrefixExtension, ChainMembershipForOrigin, StoreT4Validity, FirstEmissionFreshness, and CrossDocDisjointness (ASN-0093) — hold trivially at `Σ'`.

*Group (iii): Transition and per-state invariants discharged by frame.* M1, C0, P0, P1, P2, P3, P4★, P4a, P6, P7, P7a, P8, L12a, L12b, and S9 (TwoStreamSeparation, ASN-0036) all hold at the post-state. Specifically:

- P4★ holds via the chain `Contains_C(Σ') ⊆ Contains_C(Σ) ⊆ R = R'`. For each `(a, d'') ∈ Contains_C(Σ')`: when `d'' ≠ d`, D5 gives `M'(d'') = M(d'')` so the same witness exists in `Σ`; when `d'' = d`, each `v ∈ dom(M'(d))` with `subspace(v) = s_C` falls into `Λ` (source `u = v ∈ V_{s_C}(d)`), or `Q` (source `u = σ_d^{-1}(v) ∈ Π ⊆ V_{s_C}(d)`), or `V_{s_C}(d)` when `S = s_L` (source `u = v` unchanged). In every case a pre-state witness exists.
- S9's consequent is exactly D2, so S9 holds by D2.

---

## D9 — LinkProjectionUnderDelete (LEMMA, lemma)

For every link `ℓ ∈ dom(L)`, every slot `i`, every DEL[d, σ] transition `Σ → Σ'`, and every document `d'' ∈ dom(M)`:

- If `d'' ≠ d`: `project(L'(ℓ).eᵢ, d'', Σ') = project(L(ℓ).eᵢ, d'', Σ)`.
- If `d'' = d`, restricted to the unique subspace `S' ∈ {s_C, s_L}` with `S' ≠ S`: `project(L'(ℓ).eᵢ, d, Σ') ∩ V_{S'}(d) = project(L(ℓ).eᵢ, d, Σ) ∩ V_{S'}(d)`. (By D6, `V_{S'}(M'(d)) = V_{S'}(d)` for `S' ≠ S`, so the pre-state form `V_{S'}(d)` is used on both sides.)
- If `d'' = d`, restricted to subspace `S`: `project(L'(ℓ).eᵢ, d, Σ') ∩ V_S(M'(d)) = (project(L(ℓ).eᵢ, d, Σ) ∩ Λ) ∪ {σ_d(v) : v ∈ project(L(ℓ).eᵢ, d, Σ) ∩ Π}`. Here `Λ`, `X`, `Π ⊆ V_S(d)` are the subspace-`S` regions defined in D0.

The full post-state projection at `d'' = d` is recovered as the union:
```
project(L'(ℓ).eᵢ, d, Σ')
  = (project(L(ℓ).eᵢ, d, Σ) ∩ V_{S'}(d))                                              [from S' ≠ S]
  ∪ (project(L(ℓ).eᵢ, d, Σ) ∩ Λ) ∪ {σ_d(v) : v ∈ project(L(ℓ).eᵢ, d, Σ) ∩ Π}        [from S]
```

---

## D10 — ValidCompositeExtension (DEF, composite_extension)

ASN-0047's ValidComposite★ is extended to admit DEL as an elementary transition. A composite transition `Σ →* Σ'` is *valid* iff it is a finite sequence of atomic transitions

`Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ'`

drawn from the extended vocabulary `{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ, K.σ, DEL}`, satisfying:

(1) *Transition preconditions.* Each step `Σᵢ → Σᵢ₊₁` satisfies the elementary precondition of its transition kind, evaluated at `Σᵢ`. For a DEL step, this is D0's precondition.

(2) *Coupling constraints.* J0, J1★, and J1'★ (ASN-0047) hold between `Σ` and `Σ'` for the composite as a whole.

A single DEL transition viewed as a one-step composite `Σ → Σ'` satisfies J0, J1★, and J1'★ *vacuously*:

- *J0 (AllocationRequiresPlacement):* quantifies over `a ∈ dom(C') \ dom(C)`. By D2, `dom(C') = dom(C)`, so `dom(C') \ dom(C) = ∅` and the implication is vacuous.
- *J1★ (ExtensionRecordsProvenanceContentSubspace):* quantifies over pairs `(a, d)` where `v ∈ dom(M'(d))` has `subspace(v) = s_C` and `M'(d)(v) = a` while no such `v` existed in `dom(M(d))`. By D0's source correspondence, every post-state content-subspace V-position `v` falls into `Λ` (source `u = v`), `Q` (source `u = σ_d^{-1}(v) ∈ Π`), or `V_{s_C}(d)` when `S = s_L` (source `u = v`); in every case a pre-state witness exists, so the antecedent is false for every pair. The implication is vacuous.
- *J1'★ (ProvenanceRequiresExtensionContentSubspace):* quantifies over `(a, d) ∈ R' \ R`. By D0's frame, `R' = R`, so `R' \ R = ∅` and the implication is vacuous.

LP-family extension (ASN-0098): LP2★, LP3★, LP13 extend to DEL via D3; LP4, LP5 extend via D5; LP6, LP7, LP8, LP14, LP9, LP10, LP11 are vocabulary-disjoint from DEL with D9 supplying the DEL-specific projection characterisation; LP12 applies state-relatively to the post-state; LP12a, LP12b are supplanted for DEL by D11.

---

## D11 — WeakestPreconditionsProjection (LEMMA, lemma)

Let `Σ → Σ'` be a DEL[d, σ] transition with `σ = (s, ℓ_σ)` of subspace `S`, and let `Λ`, `X`, `Π ⊆ V_S(d)` be the regions of D0. Write `Q_disc(ℓ, d)` for the post-state predicate `discoverable_from(ℓ, d, ·)`, and `Q_card(ℓ, i, d, k)` for the post-state predicate `|project(L(ℓ).eᵢ, d, ·)| = k`.

DEL is deterministic: each component of `Σ'` is uniquely determined by `Σ` and `(d, σ)`, licensing `wp(DEL[d, σ], ¬Q) ≡ ¬wp(DEL[d, σ], Q)`.

- *wp for post-DELETE discoverability from `d`:*
  ```
  wp(DEL[d, σ], Q_disc(ℓ, d)) ≡ (E i : 1 ≤ i ≤ |L(ℓ)| : project(L(ℓ).eᵢ, d, Σ) ⊄ X)
  ```
  Equivalently:
  ```
  wp(DEL[d, σ], ¬Q_disc(ℓ, d)) ≡ (A i : 1 ≤ i ≤ |L(ℓ)| : project(L(ℓ).eᵢ, d, Σ) ⊆ X)
  ```

- *wp for post-DELETE discoverability from a different document `d'' ≠ d` (with `d'' ∈ dom(M)`):*
  ```
  wp(DEL[d, σ], discoverable_from(ℓ, d'', ·)) ≡ discoverable_from(ℓ, d'', Σ)
  ```

- *wp for post-DELETE projection cardinality from `d`:*
  ```
  wp(DEL[d, σ], Q_card(ℓ, i, d, k)) ≡ |project(L(ℓ).eᵢ, d, Σ)| − |project(L(ℓ).eᵢ, d, Σ) ∩ X| = k
  ```
  Cardinality-preservation specialisation:
  ```
  wp(DEL[d, σ], |project(L(ℓ).eᵢ, d, ·)| = |project(L(ℓ).eᵢ, d, Σ)|) ≡ project(L(ℓ).eᵢ, d, Σ) ∩ X = ∅
  ```

- *wp for post-DELETE projection cardinality from a different document `d'' ≠ d` (with `d'' ∈ dom(M)`):*
  ```
  wp(DEL[d, σ], |project(L(ℓ).eᵢ, d'', ·)| = k) ≡ |project(L(ℓ).eᵢ, d'', Σ)| = k
  ```
