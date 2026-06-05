# ASN-0101 Claim Statements

*Source: ASN-0101-delete-operation.md (revised 2026-05-27) — Extracted: 2026-06-05*

## Definition — SubspaceVPositions

For each document `d ∈ dom(M)` and each subspace `S ∈ {s_C, s_L}`:

`V_S(d) := {v ∈ dom(M(d)) : subspace(v) = S}`

Overloaded to apply to an arrangement directly: for any arrangement `N : T ⇀ T`:

`V_S(N) := {v ∈ dom(N) : subspace(v) = S}`

so that `V_S(d) = V_S(M(d))` and the post-state form `V_S(M'(d))` denotes `{v ∈ dom(M'(d)) : subspace(v) = S}`.

By S8-depth, all V-positions in `V_S(d)` share a common depth `m_S ≥ 2`. By D-SEQ★, when non-empty `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` for some `n_S ≥ 1`.

---

## Definition — OrdinalDisplacement

`δ(n, m)` — the ordinal displacement of ASN-0034: the tumbler `[0, ..., 0, n]` of length `m`.

`shift(v, n)` for `v ⊕ δ(n, #v)`, the OrdinalShift advancing `v`'s last component by `n`.

---

## Definition — DeleteRegions

Let `σ = (s, ℓ_σ)` with `r := s ⊕ ℓ_σ`. For a DEL[d, σ] transition over subspace `S`:

- `Λ := {v ∈ V_S(d) : v < s}` — the *left region*, positions strictly before the deleted span
- `X := {v ∈ V_S(d) : s ≤ v < r}` — positions in the deleted span
- `Π := {v ∈ V_S(d) : v ≥ r}` — the *right region*, positions strictly after

---

## Definition — ShiftFunction

The shift function `σ_d : Π → T` decrements its argument's last component by `n` while leaving earlier components unchanged. Formally, `σ_d(v)` is the unique tumbler `u ∈ T` satisfying `shift(u, n) = v`.

Well-definedness: by the length-preservation postcondition `#shift(u, n) = #u` of OrdinalShift (ASN-0034), the equation forces `#u = #v = m_S`; by TS2 (ShiftInjectivity, ASN-0034) on length-`m_S` tumblers, at most one such `u` exists.

Existence: for each `v = [S, 1, ..., 1, k] ∈ Π` with `k ≥ p + n`, the tumbler `u := [S, 1, ..., 1, k − n]` satisfies `shift(u, n) = u ⊕ δ(n, m_S) = [S, 1, ..., 1, (k − n) + n] = [S, 1, ..., 1, k] = v`.

So `σ_d(v) = [S, 1, ..., 1, k − n]`.

`σ_d` is a bijection from `Π` onto `Q := {σ_d(v) : v ∈ Π} = {[S, 1, ..., 1, j] : p ≤ j ≤ n_S − n}`.

---

## D0 — DelOperation (DEF, def)

**Parameters.** A document `d` and a level-uniform V-span `σ = (s, ℓ_σ)` of ordinal type. From this point onward `ℓ_σ` denotes the span width of `σ` and `ℓ` is reserved for link addresses.

**Preconditions.**

- *Document membership:* `d ∈ dom(M)`.
- *Span well-formedness:* `s ∈ V_S(d)` for some subspace `S = subspace(s) ∈ {s_C, s_L}`; `Pos(ℓ_σ)`; `#ℓ_σ = #s = m_S`; the action point of `ℓ_σ` is `m_S` (equivalently `ℓ_σ = δ(n, m_S)` for some `n ≥ 1`).
- *Containment:* writing `r := s ⊕ ℓ_σ`, every depth-`m_S` position `v` with `subspace(v) = S` and `s ≤ v < r` lies in `V_S(d)`. Under D-SEQ★ this reduces to `s = [S, 1, ..., 1, p]` for some `p ∈ {1, ..., n_S}` and `p + n − 1 ≤ n_S`, equivalently `p + n ≤ n_S + 1`.

*Consequence — non-applicability to empty arrangements.* DEL is inapplicable when `V_S(d) = ∅`, an immediate consequence of the span well-formedness precondition `s ∈ V_S(d)`.

**Effect.** Let `Λ`, `X`, `Π` be the regions defined in DeleteRegions. The post-state arrangement `M'(d)` satisfies:

- *Domain:* `V_S(M'(d)) = Λ ∪ Q`, and `V_{S'}(M'(d)) = V_{S'}(d)` for every `S' ∈ {s_C, s_L}` with `S' ≠ S`.
- *Values, left of the cut:* `(A v ∈ Λ :: M'(d)(v) = M(d)(v))`.
- *Values, shifted right of the cut:* `(A v ∈ Π :: M'(d)(σ_d(v)) = M(d)(v))`.
- *Values, other subspace:* `(A v : v ∈ V_{S'}(d) ∧ S' ≠ S :: M'(d)(v) = M(d)(v))`.

**Frame.**

- *Content store:* `C' = C` exactly — `dom(C') = dom(C)` and `(A a ∈ dom(C) :: C'(a) = C(a))`.
- *Link store:* `L' = L` exactly — `dom(L') = dom(L)` and `(A ℓ ∈ dom(L) :: L'(ℓ) = L(ℓ))`.
- *Entity set:* `E' = E` exactly.
- *Provenance:* `R' = R` exactly.
- *Document set:* `dom(M') = dom(M)`.
- *Other documents:* `(A d' ∈ dom(M) : d' ≠ d :: M'(d') = M(d'))`.

DEL is a new atomic transition kind extending the foundation's transition vocabulary `{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ, K.σ}` (ASN-0047, ASN-0093).

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

For every transition `Σ → Σ'` arising from DEL[d, σ], the post-state satisfies every foundation per-state invariant the pre-state was required to satisfy, and the transition satisfies every foundation transition invariant the pre-state transition discipline imposes. These invariants fall into three groups:

**Group (i) — arrangement per-state invariants** (S2, S8-fin, S8a, S8-depth, S3★, D-CTG★, D-MIN★, D-SEQ★, S8★, S3★-aux, CL-OWN, CL-UNIQ).

The post-state arrangement `M'(d)` satisfies:

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

**Group (ii) — allocation and store per-state invariants:** M0, S4, S7a, S7b, S7d, C1, C1b, C1c, C2, L0, L1, L1a, L1b, L1c, L3, L12, SD, L-fin, C-fin, NodeLineage, ActivatedEmission. All preserved by D0's frame (`C' = C`, `L' = L`, `E' = E`, `R' = R`, `dom(M') = dom(M)`).

**Group (iii) — transition and per-state invariants:** M1, C0, P0, P1, P2, P3, P6, P7, P8, L12a, L12b. All preserved by D0's frame.

The composite-boundary properties of ASN-0047 (P4★, P4a, P7a) are neither per-state nor transition invariants and lie outside D8's scope.

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

where `Λ`, `X`, `Π ⊆ V_S(d)` are the subspace-`S` regions defined in D0, and the two contributions cover disjoint V-position sets.

*Frame note.* The outer quantification ranges over `d'' ∈ dom(M)` because `project(e, d, Σ)` is defined only when `d ∈ dom(Σ.M)`; D4 supplies `dom(M') = dom(M)`, so `project(L'(ℓ).eᵢ, d'', Σ')` is well-defined on the post-state side of every clause.

---

## D10 — WeakestPreconditionsProjectionPostconditions (LEMMA, lemma)

Let `Σ → Σ'` be a DEL[d, σ] transition with `σ = (s, ℓ_σ)` of subspace `S`, and let `Λ`, `X`, `Π ⊆ V_S(d)` be the regions of D0. Write `Q_disc(ℓ, d)` for the post-state predicate `discoverable_from(ℓ, d, ·)`, and `Q_card(ℓ, i, d, k)` for the post-state predicate `|project(L(ℓ).eᵢ, d, ·)| = k`. Write `enabled(DEL[d, σ])` for DEL's applicability predicate — the conjunction of D0's preconditions — which is exactly `wp(DEL[d, σ], true)`.

*DEL is deterministic:* each component of `Σ'` is uniquely determined by `Σ` and the parameters `(d, σ)`, licensing the negation equivalence `wp(DEL[d, σ], ¬Q) ≡ enabled(DEL[d, σ]) ∧ ¬wp(DEL[d, σ], Q)`.

Four weakest preconditions:

**(a) wp for post-DELETE discoverability from `d`:**
```
wp(DEL[d, σ], Q_disc(ℓ, d)) ≡ enabled(DEL[d, σ]) ∧ (E i : 1 ≤ i ≤ |L(ℓ)| : project(L(ℓ).eᵢ, d, Σ) ⊄ X)
```
Equivalently by determinism:
```
wp(DEL[d, σ], ¬Q_disc(ℓ, d)) ≡ enabled(DEL[d, σ]) ∧ (A i : 1 ≤ i ≤ |L(ℓ)| : project(L(ℓ).eᵢ, d, Σ) ⊆ X)
```

**(b) wp for post-DELETE projection cardinality from `d`:**
```
wp(DEL[d, σ], Q_card(ℓ, i, d, k)) ≡ enabled(DEL[d, σ]) ∧ |project(L(ℓ).eᵢ, d, Σ)| − |project(L(ℓ).eᵢ, d, Σ) ∩ X| = k
```
Specialisation — cardinality preserved iff DEL is enabled and no pre-state projection element lies in the deleted region:
```
wp(DEL[d, σ], |project(L(ℓ).eᵢ, d, ·)| = |project(L(ℓ).eᵢ, d, Σ)|) ≡ enabled(DEL[d, σ]) ∧ project(L(ℓ).eᵢ, d, Σ) ∩ X = ∅
```

**(c) Cross-document discoverability wp (`d'' ≠ d`):** by D9's first clause the projection is bytewise-invariant, so both wps reduce to:
```
wp(DEL[d, σ], Q_disc(ℓ, d'')) ≡ enabled(DEL[d, σ]) ∧ discoverable_from(ℓ, d'', Σ)
```

**(d) Cross-document cardinality wp (`d'' ≠ d`):**
```
wp(DEL[d, σ], |project(L(ℓ).eᵢ, d'', ·)| = k) ≡ enabled(DEL[d, σ]) ∧ |project(L(ℓ).eᵢ, d'', Σ)| = k
```

---

## D11 — ValidCompositeExtensionUnderDelete (LEMMA, lemma)

ASN-0047's ValidComposite★ is extended to admit DEL as an elementary transition. A composite transition `Σ →* Σ'` is *valid* iff it is a finite sequence of atomic transitions

`Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ'`

drawn from the extended vocabulary `{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ, K.σ, DEL}`, satisfying:

**(1) Transition preconditions.** Each step `Σᵢ → Σᵢ₊₁` satisfies the elementary precondition of its transition kind, evaluated at `Σᵢ`. For a DEL step, this is D0's precondition.

**(2) Coupling constraints and composite-boundary obligations.** J0, J1★, and J1'★ (ASN-0047) hold between the composite's initial state `Σ` and final state `Σ'`; and `Σ'` additionally satisfies ASN-0047's composite-boundary properties P4★, P4a, and P7a.

A single DEL transition viewed as a one-step composite `Σ → Σ'` satisfies J0, J1★, and J1'★ *vacuously*:

- *J0* quantifies over `a ∈ dom(C') \ dom(C)`. By D2, `dom(C') = dom(C)`, so `dom(C') \ dom(C) = ∅` and the implication is vacuous.
- *J1★* quantifies over pairs `(a, d)` for which some post-state content-subspace V-position maps to `a` while no such pre-state V-position did. By D0's effect, every post-state content-subspace V-position `v ∈ V_{s_C}(M'(d))` has `M'(d)(v) = M(d)(u)` for some pre-state V-position `u ∈ dom(M(d))` with `subspace(u) = s_C`. The antecedent is therefore always false. The implication is vacuous.
- *J1'★* quantifies over `(a, d) ∈ R' \ R`. By D0's frame, `R' = R`, so `R' \ R = ∅` and the implication is vacuous.

**Boundary derivation (P4★, P4a, P7a by induction).** For every DEL-extended trace `Σ₀ →* B₁ →* B₂ →* ... →* B_N` with each `B_j →* B_{j+1}` a valid composite:

- *Base case (`Σ₀`):* P4★ holds since `Contains_C(Σ₀) = ∅ ⊆ R₀`; P4a and P7a hold vacuously since `R₀ = ∅` and `dom(C₀) = ∅`.
- *Inductive step:* Fix boundary `B_j` satisfying P4★, P4a, P7a (induction hypothesis), and let `Σ := B_j`, `Σ' := B_{j+1}`. Then:
  - *P4★ at `Σ'`:* `Contains_C(Σ') ⊆ R'`. For `(a, d) ∈ Contains_C(Σ')`: if range-new (no content-subspace `v' ∈ dom(M(d))` mapped to `a`), J1★ gives `(a, d) ∈ R'`; if not range-new, P4★ at `Σ` gives `(a, d) ∈ R` and `R ⊆ R'` (P2) gives `(a, d) ∈ R'`.
  - *P7a at `Σ'`:* every `a ∈ dom(C')` carries a record. If `a ∈ dom(C)`: P7a at `Σ` and `R ⊆ R'` supply the record. If `a ∈ dom(C') \ dom(C)`: J0 supplies a content-subspace placement `M'(d)(v) = a`, so `(a, d) ∈ Contains_C(Σ')`, and the P4★ conclusion gives `(a, d) ∈ R'`.
  - *P4a at `Σ'`:* every `(a, d) ∈ R'` is witnessed at some boundary. If `(a, d) ∈ R`: P4a at `Σ` witnesses it at some `Σ_k ∈ \{Σ₀, ..., B_j\}`. If `(a, d) ∈ R' \ R`: J1'★ supplies a surviving content-subspace witness at the endpoint `Σ' = B_{j+1}`, which is itself a composite boundary.

**LP-family extension.** ASN-0098's projection lemmas close over the DEL-extended vocabulary because DEL fixes both stores (D2, D3), frames every non-`d` arrangement and the unaffected subspace of `d` (D5, D6), and D9 and D10 supply the only DEL-specific projection facts. No new LP-family lemma is required.

**Composite-level J0 warning.** DEL can break composite-level J0: a three-step composite `K.α` (emit `a`) then `K.μ⁺` (place `v ↦ a`) then `DEL[d, σ]` (with `v ∈ X`) satisfies each step's elementary precondition but fails composite-level J0, since `a ∈ dom(C_3) \ dom(C_0)` yet no content-subspace `v' ∈ dom(M_3(d))` satisfies `M_3(d)(v') = a`.
