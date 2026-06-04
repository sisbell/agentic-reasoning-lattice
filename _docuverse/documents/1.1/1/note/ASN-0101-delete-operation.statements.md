# ASN-0101 Claim Statements

*Source: ASN-0101-delete-operation.md (revised 2026-05-27) — Extracted: 2026-06-03*

## Definition — SubspaceVPositions

For each document `d ∈ dom(M)` and each subspace `S ∈ {s_C, s_L}`:

```
V_S(d) := {v ∈ dom(M(d)) : subspace(v) = S}
```

By S8-depth, all V-positions in `V_S(d)` share a common depth `m_S ≥ 2`. By D-SEQ★, when non-empty `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` for some `n_S ≥ 1`.

## Definition — OrdinalDisplacement

`δ(n, m)` denotes the tumbler `[0, ..., 0, n]` of length `m` — the ordinal displacement of ASN-0034.

`shift(v, n)` denotes `v ⊕ δ(n, #v)`, the OrdinalShift advancing `v`'s last component by `n`.

## Definition — DelRegions

Given DEL[d, σ] with `σ = (s, ℓ_σ)`, subspace `S = subspace(s)`, `r := s ⊕ ℓ_σ`, and `ℓ_σ = δ(n, m_S)`:

```
Λ := {v ∈ V_S(d) : v < s}        (left region — positions strictly before the deleted span)
X := {v ∈ V_S(d) : s ≤ v < r}   (positions in the deleted span)
Π := {v ∈ V_S(d) : v ≥ r}        (right region — positions strictly after)
```

## Definition — ShiftFunction

The shift function `σ_d : Π → T` decrements its argument's last component by `n` while leaving earlier components unchanged. Formally, `σ_d(v)` is the unique tumbler `u ∈ T` satisfying `shift(u, n) = v`.

For each `v = [S, 1, ..., 1, k] ∈ Π` with `k ≥ p + n`:

```
σ_d(v) = [S, 1, ..., 1, k − n]
```

Well-definedness: by the length-preservation postcondition `#shift(u, n) = #u` of OrdinalShift (ASN-0034), the equation forces `#u = #v = m_S`; by TS2 (ShiftInjectivity, ASN-0034) on length-`m_S` tumblers, at most one such `u` exists. Existence: for each `v = [S, 1, ..., 1, k] ∈ Π` with `k ≥ p + n`, setting `u := [S, 1, ..., 1, k − n]` satisfies `shift(u, n) = v` by TumblerAdd's componentwise definition.

`Q := {σ_d(v) : v ∈ Π} = {[S, 1, ..., 1, j] : p ≤ j ≤ n_S − n}`

`σ_d` is a bijection from `Π` onto `Q`.

## Definition — ProjectFunction

```
project(L(ℓ).eᵢ, d, Σ) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(L(ℓ).eᵢ)}
```

## Definition — DiscoverableFrom

```
discoverable_from(ℓ, d, Σ) ≡ (E i : project(L(ℓ).eᵢ, d, Σ) ≠ ∅)
```

## Definition — EnabledDel

```
enabled(DEL[d, σ]) = wp(DEL[d, σ], true)
```

The conjunction of D0's preconditions: document membership `d ∈ dom(M)`, span well-formedness, and containment.

---

## D0 — DelOperationSpec (SPEC, atomic-transition)

**Parameters.** A document `d` and a level-uniform V-span `σ = (s, ℓ_σ)` of ordinal type. `ℓ_σ` is the span width; `ℓ` is reserved for link addresses.

**Preconditions.**

- *Document membership:* `d ∈ dom(M)`.
- *Span well-formedness:* `s ∈ V_S(d)` for some subspace `S = subspace(s) ∈ {s_C, s_L}`; `Pos(ℓ_σ)`; `#ℓ_σ = #s = m_S`; the action point of `ℓ_σ` is `m_S` (equivalently `ℓ_σ = δ(n, m_S)` for some `n ≥ 1`).
- *Containment:* writing `r := s ⊕ ℓ_σ`, every depth-`m_S` position `v` with `subspace(v) = S` and `s ≤ v < r` lies in `V_S(d)`. Under D-SEQ★ this reduces to `s = [S, 1, ..., 1, p]` for some `p ∈ {1, ..., n_S}` and `p + n − 1 ≤ n_S`, equivalently `p + n ≤ n_S + 1`.

**Effect.** The post-state arrangement `M'(d)` satisfies:

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

DEL is a new atomic transition kind extending the foundation's transition vocabulary `{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ, K.σ}` (ASN-0047, ASN-0093). It is not a derived composite of `K.μ⁻` and `K.μ~`.

---

## D1 — GapClosure (LEMMA, lemma)

Let `Σ → Σ'` be a DEL[d, σ] transition with `σ = (s, ℓ_σ)`. The shift function `σ_d` is an order-preserving bijection from `Π` onto `Q`. Writing `n_S' := |V_S(d)| − n`: when `n_S' ≥ 1`, `V_S(M'(d)) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S'}` is contiguous with minimum `[S, 1, ..., 1]` of depth `m_S`; when `n_S' = 0`, `V_S(M'(d)) = ∅` and D-CTG★, D-MIN★, D-SEQ★ hold vacuously for subspace `S`.

---

## D2 — ContentImmutabilityUnderDelete (LEMMA, lemma)

For every transition `Σ → Σ'` arising from DEL[d, σ]:

```
dom(C') = dom(C)  ∧  (A a ∈ dom(C) :: C'(a) = C(a))
```

---

## D3 — LinkStoreImmutabilityUnderDelete (LEMMA, lemma)

For every transition `Σ → Σ'` arising from DEL[d, σ]:

```
dom(L') = dom(L)  ∧  (A ℓ ∈ dom(L) :: L'(ℓ) = L(ℓ))
```

---

## D4 — DocumentIdentityPersistenceUnderDelete (LEMMA, lemma)

For every transition `Σ → Σ'` arising from DEL[d, σ]:

```
d ∈ dom(M')  ∧  dom(M') = dom(M)
```

---

## D5 — CrossDocumentArrangementIsolationUnderDelete (LEMMA, lemma)

For every transition `Σ → Σ'` arising from DEL[d, σ]:

```
(A d' ∈ dom(M) : d' ≠ d :: M'(d') = M(d'))
```

---

## D6 — SubspaceIsolationUnderDelete (LEMMA, lemma)

For every transition `Σ → Σ'` arising from DEL[d, σ] with `S = subspace(s)`:

```
(A S' ∈ {s_C, s_L} : S' ≠ S :: V_{S'}(M'(d)) = V_{S'}(d)  ∧  (A v ∈ V_{S'}(d) :: M'(d)(v) = M(d)(v)))
```

---

## D7 — AttributionSurvivalUnderDelete (LEMMA, lemma)

For every transition `Σ → Σ'` arising from DEL[d, σ] and every I-address `a` with `a ∈ ran(M(d))` at the pre-state `Σ`:

```
a ∈ dom(C') ∪ dom(L')  ∧  origin(a) at Σ' = origin(a) at Σ
```

Equivalently, restricted by subspace: when `subspace_I(a) = s_C`, `a ∈ dom(C')`; when `subspace_I(a) = s_L`, `a ∈ dom(L')`. By L14 (store disjointness), these are mutually exclusive.

---

## D8 — ArrangementWellFormednessPreservation (LEMMA, lemma)

For every transition `Σ → Σ'` arising from DEL[d, σ], the post-state satisfies every foundation *per-state* invariant that the pre-state was required to satisfy, and DEL cannot break any *composite-boundary* property.

**Group (i): Arrangement invariants on the modified document `d`.** The post-state arrangement `M'(d)` satisfies:

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

**Group (ii): Allocation and store invariants.** All of M0, S4, S7a, S7b, S7d, C1, C1b, C1c, C2, L0, L1, L1a, L1b, L1c, L3, L12, SD, L-fin, C-fin, NodeLineage, ActivatedEmission and the substrate chain-discipline lemmas (ChainElementT4Validity, ChainEnumerationInjectivity, DisjointSubAllocatorChains, ChainPrefixExtension, ChainMembershipForOrigin, StoreT4Validity, FirstEmissionFreshness, CrossDocumentDisjointness) hold trivially at the post-state because `C' = C`, `L' = L`, `E' = E`, and `dom(M') = dom(M)` by D0's frame.

**Group (iii): Transition and per-state invariants discharged by frame.** M1, C0, P0, P1, P2, P3, P6, P7, P8, L12a, L12b hold trivially under D0's frame because the components they predicate over are pointwise unchanged.

**The composite-boundary properties P4★, P4a, P7a are not per-state invariants.** DEL cannot break them:

- *P4★:* `Contains_C(Σ') ⊆ Contains_C(Σ)` (content-subspace-monotone-shrinking) and `R' = R`.
- *P4a:* `R' = R` and no new witnessing obligation arises from DEL.
- *P7a:* `dom(C') = dom(C)` and `R' = R`, so neither the content-address set nor the provenance relation changes.

Their affirmative discharge at a DEL-terminated composite boundary is a composite-level obligation (D10).

---

## D9 — LinkProjectionUnderDelete (LEMMA, lemma)

For every link `ℓ ∈ dom(L)`, every slot `i`, every DEL[d, σ] transition `Σ → Σ'` with subspace `S` and regions `Λ`, `X`, `Π`, and every document `d'' ∈ dom(M)`:

- If `d'' ≠ d`:
  ```
  project(L'(ℓ).eᵢ, d'', Σ') = project(L(ℓ).eᵢ, d'', Σ)
  ```

- If `d'' = d`, restricted to the unique subspace `S' ∈ {s_C, s_L}` with `S' ≠ S`:
  ```
  project(L'(ℓ).eᵢ, d, Σ') ∩ V_{S'}(d) = project(L(ℓ).eᵢ, d, Σ) ∩ V_{S'}(d)
  ```
  (By D6, `V_{S'}(M'(d)) = V_{S'}(d)` for `S' ≠ S`, so the pre-state form `V_{S'}(d)` is used on both sides.)

- If `d'' = d`, restricted to subspace `S`:
  ```
  project(L'(ℓ).eᵢ, d, Σ') ∩ V_S(M'(d))
    = (project(L(ℓ).eᵢ, d, Σ) ∩ Λ) ∪ {σ_d(v) : v ∈ project(L(ℓ).eᵢ, d, Σ) ∩ Π}
  ```

Full post-state projection recovery at `d'' = d`:

```
project(L'(ℓ).eᵢ, d, Σ')
  = (project(L(ℓ).eᵢ, d, Σ) ∩ V_{S'}(d))
  ∪ (project(L(ℓ).eᵢ, d, Σ) ∩ Λ) ∪ {σ_d(v) : v ∈ project(L(ℓ).eᵢ, d, Σ) ∩ Π}
```

---

## D10 — ValidCompositeExtensionUnderDelete (LEMMA, lemma)

ASN-0047's ValidComposite★ is extended to admit DEL as an elementary transition. A composite transition `Σ →* Σ'` is *valid* iff it is a finite sequence of atomic transitions

```
Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ'
```

drawn from the extended vocabulary `{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ, K.σ, DEL}`, satisfying:

(1) *Transition preconditions.* Each step `Σᵢ → Σᵢ₊₁` satisfies the elementary precondition of its transition kind, evaluated at `Σᵢ`. For a DEL step, this is D0's precondition.

(2) *Coupling constraints and composite-boundary obligations.* J0, J1★, and J1'★ (ASN-0047) hold between the composite's initial state `Σ` and final state `Σ'`; and `Σ'` additionally satisfies P4★, P4a, and P7a.

**A single DEL transition viewed as a one-step composite satisfies J0, J1★, and J1'★ vacuously:**

- *J0 (AllocationRequiresPlacement):* quantifies over `a ∈ dom(C') \ dom(C)`. By D2, `dom(C') = dom(C)`, so `dom(C') \ dom(C) = ∅` and the implication is vacuous.
- *J1★ (ExtensionRecordsProvenanceContentSubspace):* every post-state content-subspace V-position `v ∈ V_{s_C}(M'(d))` falls into one of three exhaustive cases — `v ∈ Λ` (pre-state witness `v` itself), `v ∈ Q` with `v = σ_d(u)` for `u ∈ Π` (pre-state witness `u`), or `S = s_L` so `v ∈ V_{s_C}(d)` unchanged by D6 (pre-state witness `v` itself) — so the J1★ antecedent "no `v ∈ dom(M(d))` with subspace `s_C` mapped to `a`" is false for every `(a, d)` pair, and the implication is vacuous.
- *J1'★ (ProvenanceRequiresExtensionContentSubspace):* quantifies over `(a, d) ∈ R' \ R`. By D0's frame, `R' = R`, so `R' \ R = ∅` and the implication is vacuous.

**Composite-boundary obligations.** DEL is neutral-to-helpful for P4★, P4a, and P7a:
- P4★: `Contains_C(Σ') ⊆ Contains_C(Σ)` and `R' = R`, so DEL cannot introduce a new violation.
- P4a: `R' = R` and DEL records no new provenance pair, raising no new witnessing obligation.
- P7a: `dom(C') = dom(C)` and `R' = R`, so DEL neither creates an unrecorded content address nor removes a provenance record.

The boundary properties are established by the composite's non-DEL steps and preserved by every DEL step; the boundary obligation itself is discharged at the composite level.

**Multi-step composites.** DEL does not itself introduce coupling obligations, but its presence in a composite does not automatically discharge composite-level J0/J1★/J1'★. Composites combining DEL with allocation-and-placement steps must be checked at their endpoints. Example: the three-step composite (i) K.α emitting `a`, (ii) K.μ⁺ placing `v ↦ a`, (iii) DEL[d, σ] with `v ∈ X` satisfies each step's elementary precondition but fails composite-level J0: `a ∈ dom(C_3) \ dom(C_0)` yet no `v' ∈ dom(M_3(d))` satisfies `M_3(d)(v') = a`.

**LP-family extension.** ASN-0098's projection apparatus extends to the DEL-augmented vocabulary via the following dispatch:
- LP2★, LP3★, LP13: extend to DEL via D3 (`L' = L` exactly).
- LP4, LP5: extend to DEL on unaffected documents via D5; D9 supplies the DEL-specific projection characterisation on the affected document.
- LP6, LP7, LP8, LP14, LP9, LP10, LP11: vocabulary-disjoint from DEL; original universals stand with D9 as the DEL-specific per-step characterisation.
- LP12: state-relative, applies to the post-state of any DEL transition by direct evaluation at `Σ'`.
- LP12a, LP12b: supplanted for DEL by D11.
- LP16, LP17, LP20, LP21: state-relative, apply to the post-state directly.
- LP18: extends via Store Monotonicity★ (`dom(C') = dom(C)`, `dom(L') = dom(L)`) and LP3★ across DEL-containing sequences.
- LP19, LP19a: extend via Store Monotonicity★ for the prefix; DEL is never the allocation or extension step these lemmas quantify over.
- LP-Sub: state-relative, `dom(C') = dom(C)` (D2) and `dom(L') = dom(L)` (D3) discharge it at the post-state.
- LP-Fin, LP-Fin Corollary: purely tumbler-structural and state-independent; hold without extension.

---

## D11 — WeakestPreconditionsForProjectionPostconditions (LEMMA, lemma)

Let `Σ → Σ'` be a DEL[d, σ] transition with `σ = (s, ℓ_σ)` of subspace `S`, and let `Λ`, `X`, `Π ⊆ V_S(d)` be the regions of D0. Write `Q_disc(ℓ, d)` for the post-state predicate `discoverable_from(ℓ, d, ·)`, and `Q_card(ℓ, i, d, k)` for the post-state predicate `|project(L(ℓ).eᵢ, d, ·)| = k`.

DEL is deterministic: each component of `Σ'` is uniquely determined by `Σ` and the parameters `(d, σ)`, licensing the negation equivalence `wp(DEL[d, σ], ¬Q) ≡ enabled(DEL[d, σ]) ∧ ¬wp(DEL[d, σ], Q)` for every postcondition `Q`.

**(a) wp for post-DELETE discoverability from `d`:**

```
wp(DEL[d, σ], Q_disc(ℓ, d)) ≡ enabled(DEL[d, σ]) ∧ (E i : 1 ≤ i ≤ |L(ℓ)| : project(L(ℓ).eᵢ, d, Σ) ⊄ X)
```

Equivalently, by the determinism negation equivalence:

```
wp(DEL[d, σ], ¬Q_disc(ℓ, d)) ≡ enabled(DEL[d, σ]) ∧ (A i : 1 ≤ i ≤ |L(ℓ)| : project(L(ℓ).eᵢ, d, Σ) ⊆ X)
```

**(b) wp for post-DELETE discoverability from `d'' ≠ d` (with `d'' ∈ dom(M)`):**

```
wp(DEL[d, σ], discoverable_from(ℓ, d'', ·)) ≡ enabled(DEL[d, σ]) ∧ discoverable_from(ℓ, d'', Σ)
```

**(c) wp for post-DELETE projection cardinality from `d`:**

```
wp(DEL[d, σ], Q_card(ℓ, i, d, k)) ≡ enabled(DEL[d, σ]) ∧ |project(L(ℓ).eᵢ, d, Σ)| − |project(L(ℓ).eᵢ, d, Σ) ∩ X| = k
```

Cardinality-preservation specialisation:

```
wp(DEL[d, σ], |project(·)| = |project(L(ℓ).eᵢ, d, Σ)|) ≡ enabled(DEL[d, σ]) ∧ project(L(ℓ).eᵢ, d, Σ) ∩ X = ∅
```

**(d) wp for post-DELETE projection cardinality from `d'' ≠ d` (with `d'' ∈ dom(M)`):**

```
wp(DEL[d, σ], |project(L(ℓ).eᵢ, d'', ·)| = k) ≡ enabled(DEL[d, σ]) ∧ |project(L(ℓ).eᵢ, d'', Σ)| = k
```
