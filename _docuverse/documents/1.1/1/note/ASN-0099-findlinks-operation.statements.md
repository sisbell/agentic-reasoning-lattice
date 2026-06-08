# ASN-0099 Claim Statements

*Source: ASN-0099-findlinks-operation.md (revised 2026-05-26) — Extracted: 2026-06-07*

## Definition — ImageRegion

```
image(R, d, Σ)
  defined when  d ∈ dom(Σ.M)
  ≡             {Σ.M(d)(v) : v ∈ R ∩ dom(Σ.M(d))}
```

## Definition — FindLinks

```
findlinks(I, Σ) = {a ∈ dom(Σ.L) : matches(a, I, Σ)}
```

## Definition — FindLinksFiltered

```
findlinks_filtered(C, Σ)
  = {a ∈ dom(Σ.L) : (A (i, J) ∈ C : i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅)}
```

A slot constraint is a pair `(i, J)` with `i ∈ ℕ⁺`, `J ⊆ T`. A link satisfies the constraint iff its slot `i` exists and the coverage at that slot meets `J`. A filter constraint `(i, J)` is unsatisfiable at `a` when `i > |Σ.L(a)|` or `Σ.L(a).eᵢ = ∅`.

The unfiltered form is recovered as:
```
findlinks(I, Σ) = ⋃_{i = 1}^{N} findlinks_filtered({(i, I)}, Σ)
   where N = max{|Σ.L(a)| : a ∈ dom(Σ.L)}  when dom(Σ.L) ≠ ∅
         N = 0                              when dom(Σ.L) = ∅
```

## Definition — FindLinksScoped (F14 — ScopeFilter, DEF/function)

```
F14 (ScopeFilter):
   findlinks_scoped(I, S, Σ) = findlinks(I, Σ) ∩ S
                             = {a ∈ dom(Σ.L) ∩ S : matches(a, I, Σ)}
```

Natural choices for `S`: "all links in document `d`" (`{a : home(a) = d}`), "all links by user `u`", or any access-control narrowing.

## F1 — MatchPredicate (DEF/predicate)

```
F1 (MatchPredicate):
   matches(a, I, Σ) ≡ (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅).
```

For `a ∈ dom(Σ.L)`, `I ⊆ T`, `Σ ∈ 𝒮`.

## F12 — TwoPhaseFactoring (DEF/function)

```
F12 (TwoPhaseFactoring) — DEFINITION of findlinks_V:
   findlinks_V(R, d, Σ)
     defined when  d ∈ dom(Σ.M)
     ≡             findlinks(image(R, d, Σ), Σ).
```

For `d ∉ dom(Σ.M)`, `findlinks_V(R, d, Σ)` is undefined.

## ComprehensionInvariantUnderΣL — ComprehensionInvariantUnderLinkStore (LEMMA/lemma)

```
ComprehensionInvariantUnderΣL — meta-lemma:
   If Σ.L = Σ'.L as partial functions, then for every comprehension
   over dom(Σ.L) whose membership predicate consults only Σ.L and
   query-data (never Σ.M, Σ.C, Σ.E, Σ.R):
       {a ∈ dom(Σ.L) : P(a, Σ)} = {a ∈ dom(Σ'.L) : P(a, Σ')}.

   The chain: Σ.L = Σ'.L gives dom(Σ.L) = dom(Σ'.L) and per-link
   value equality Σ.L(a) = Σ'.L(a). Component-wise tuple equality on
   Link values (L6) gives |Σ.L(a)| = |Σ'.L(a)| and per-slot endset
   equality Σ.L(a).eᵢ = Σ'.L(a).eᵢ. Coverage is a deterministic
   function of its endset argument, so per-slot coverage agrees.
   Any membership predicate built from these evaluates identically
   at the two states; set extensionality closes the equality.
```

## PerLinkInvarianceUnderValuePreservation — PerLinkInvariance (LEMMA/lemma)

```
PerLinkInvarianceUnderValuePreservation — sub-lemma:
   For any link a with a ∈ dom(Σ.L) ∩ dom(Σ'.L) and
   Σ'.L(a) = Σ.L(a):
   - matches(a, I, Σ) ⟺ matches(a, I, Σ') for every I ⊆ T.
   - For every slot constraint (i, J), the per-link filter conjunct
       i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅
     evaluates identically at Σ and Σ'.
   - Consequently, for every constraint set C, the filtered per-link
     universal `(A (i, J) ∈ C : i ≤ |Σ.L(a)| ∧
     coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅)` evaluates identically at Σ and Σ'.
```

## A1a — PublishedFramePreservation (LEMMA/lemma)

```
A1a (PublishedFramePreservation):
   Every operation of V ∖ {K.λ} preserves the link store across its
   transition — single-step Σ → Σ' for the atomic operations, the
   two-step composite Σ →* Σ' for K.μ~:
       dom(Σ'.L) = dom(Σ.L) ∧ (A a ∈ dom(Σ.L) :: Σ'.L(a) = Σ.L(a)).
   The atomic operations — V_atomic ∖ {K.λ} = {K.α, K.δ, K.μ⁺, K.μ⁻,
   K.μ⁺_L, K.ρ} — publish `L' = L` in their operative frame (K.μ⁺ and
   K.μ⁻ via ASN-0047's amended extended-state versions). The composite
   K.μ~ (the non-atomic K.μ⁻ + K.μ⁺ composite) preserves Σ.L by
   transitive composition of A1a at its two atomic constituents.
```

Where `V ≡ V_atomic ∪ {K.μ~}` and `V_atomic = {K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ}`.

## F2 — Completeness (LEMMA/lemma)

```
F2 (Completeness):  findlinks(I, Σ) ⊆ result(I, Σ).
```

Where `result : 𝒫(T) × 𝒮 → 𝒫(T)` denotes a conforming implementation's output function.

## F3 — Soundness (LEMMA/lemma)

```
F3 (Soundness):     result(I, Σ) ⊆ findlinks(I, Σ).
```

Together F2 ∧ F3 force `result(I, Σ) = findlinks(I, Σ)`.

## F4 — MatchIndividuation (LEMMA/lemma)

```
F4 (MatchIndividuation):
   The witnesses below individuate F1's per-endset overlap test: each
   exhibits an (a, I) pair on which an alternative match design —
   coverage-containment in either direction, a cardinality threshold,
   or an I-independent design (match-all, or a slot test that ignores
   the query) — disagrees with F1. The witnesses are L3-admissible
   states.
```

*Strengthening 1 — Containment from coverage to query (`coverage ⊆ I`).* Witness link `a`: arity 3 with slot 1 `(β, δ(1, #β))`, slot 2 `(γ, δ(1, #γ))`, slot 3 `(α, δ(1, #α))`, where β and γ are same-length siblings of `α` differing at position `#α`. Query `I = {α}`. The link-level strengthening predicate is `(E i : coverage(L(a).eᵢ) ⊆ I)`; no slot satisfies it. F1 admits via slot 3.

*Strengthening 2 — Containment from query to coverage (`I ⊆ coverage`).* Witness: link `a` with one canonical span `(α, δ(1, #α))` at slot 3, slots 1 and 2 empty. Query `I = {α, γ}` for any `γ ∈ T` with `α ⋠ γ`. The strengthening predicate is `(E i : I ⊆ coverage(eᵢ))`; no slot satisfies it. F1 admits via slot 3.

*Strengthening 3 — Cardinality threshold (`|coverage ∩ I| ≥ k` for `k > 1`).* Witness: link `a` with one canonical span `(α, δ(1, #α))` at slot 3, slots 1 and 2 empty. Query `I = {α}`. The strengthening predicate is `(E i : |coverage(eᵢ) ∩ I| ≥ k)` for `k > 1`; no slot satisfies it. F1 admits via slot 3.

*Weakening 1 — Slot-vacuous match (`P_⊤(a, I, Σ) ≡ a ∈ dom(Σ.L)`).* Witness: any `a ∈ dom(Σ.L)` with all `coverage(Σ.L(a).eᵢ)` disjoint from `I`. F1 rejects; `P_⊤` admits.

*Weakening 2 — Slot-disjunctive ignoring I (`P_∃-slot(a, I, Σ) ≡ (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ≠ ∅)`).* Witness: same `(a, I)` as Weakening 1 with non-empty slot 3. `P_∃-slot` admits regardless of `I`. F1 rejects.

## F5 — IdentityNotValue (LEMMA/lemma)

```
F5 (IdentityNotValue):
   matches(a, I, Σ) consults dom(Σ.L), Σ.L, and coverage(·), never
   Σ.C(·). For distinct α ≠ β, matches(a, {α}, Σ) and
   matches(a, {β}, Σ) are computed independently — each reducing per
   slot to the address-level membership test `α ∈ coverage(Σ.L(a).eᵢ)`
   (resp. `β ∈ coverage(Σ.L(a).eᵢ)`), an independent predicate over
   coverage sets with no reference to content values and no shared
   content lookup.
```

## F6 — TransclusionTransparency (LEMMA/lemma)

```
F6 (TransclusionTransparency):
   For documents d₁, d₂ ∈ dom(Σ.M) and V-positions v₁ ∈ dom(Σ.M(d₁)),
   v₂ ∈ dom(Σ.M(d₂)) with Σ.M(d₁)(v₁) = Σ.M(d₂)(v₂) = α:
       findlinks_V({v₁}, d₁, Σ) = findlinks_V({v₂}, d₂, Σ).
```

## F8 — Determinism (LEMMA/lemma)

```
F8 (Determinism):
   findlinks(I, Σ) = findlinks(I, Σ')  whenever Σ.L = Σ'.L.
```

## F9 — LinkStoreInertPreservation (LEMMA/lemma)

```
F9 (LinkStoreInertPreservation):
   For every transition produced by an operation in V ∖ {K.λ}, and any
   I ⊆ T:
       findlinks(I, Σ) = findlinks(I, Σ').

   A1a gives Σ.L = Σ'.L across every V ∖ {K.λ} operation. F8 via
   ComprehensionInvariantUnderΣL then forces the equality. For a
   reachable sequence Σ →* Σ' whose every atomic step lies in
   V_atomic ∖ {K.λ}, the per-step equalities chain by transitivity.
```

## F9-λ — KLambdaInducedIncrement (LEMMA/lemma)

```
F9-λ (KλInducedIncrement):
   For any single-step transition Σ → Σ' produced by K.λ allocating
   a fresh link ℓ_new with endsets (e₁, …, e_N), and any I ⊆ T:
       findlinks(I, Σ') = findlinks(I, Σ) ⊎ ({ℓ_new} if matches(ℓ_new, I, Σ') else ∅).

   The two parts are disjoint (⊎): K.λ's freshness precondition
   ℓ_new ∉ dom(Σ.L) ∪ dom(Σ.C) (ASN-0093) gives ℓ_new ∉ dom(Σ.L),
   so ℓ_new ∉ findlinks(I, Σ).

   Derivation: K.λ's effect-clause gives dom(Σ'.L) = dom(Σ.L) ∪ {ℓ_new}
   with Σ'.L(a) = Σ.L(a) for every a ∈ dom(Σ.L). The prior-key part
   contributes exactly findlinks(I, Σ) via PerLinkInvarianceUnderValuePreservation.
   The fresh-key part contributes {ℓ_new} when matches(ℓ_new, I, Σ') holds,
   and ∅ otherwise.
```

## F10 — OrderedResult (LEMMA/lemma)

```
F10 (OrderedResult):
   The result set admits a unique presentation as a sequence
   ⟨a₁, a₂, ..., aₙ⟩ with aⱼ ∈ dom(Σ.L) satisfying matches(aⱼ, I, Σ),
   and a₁ < a₂ < ... < aₙ under T1.
```

Finiteness: `findlinks(I, Σ) ⊆ dom(Σ.L)` by definition; L-fin gives `|dom(Σ.L)| < ∞`. T1 is a strict total order on `T`. The empty result (`n = 0`) is presented as `⟨⟩`. The same argument gives `findlinks_filtered(C, Σ)` and `findlinks_scoped(I, S, Σ)` each a unique strictly T1-increasing presentation.

## F11 — PersistentDiscoverabilityI (LEMMA/lemma)

```
F11 (PersistentDiscoverabilityI):
   For any reachable state sequence Σ →* Σ' and any a ∈ dom(Σ.L) with
   matches(a, I, Σ):  a ∈ dom(Σ'.L) ∧ matches(a, I, Σ').
```

## F13 — SetAdditive (LEMMA/lemma)

```
F13 (SetAdditive):
   findlinks(I₁ ∪ I₂, Σ) = findlinks(I₁, Σ) ∪ findlinks(I₂, Σ).
```

The load-bearing step: for fixed `a ∈ dom(Σ.L)` and `eᵢ = Σ.L(a).eᵢ`:
```
a ∈ findlinks(I₁ ∪ I₂, Σ)
  ⟺ (E i : coverage(eᵢ) ∩ (I₁ ∪ I₂) ≠ ∅)
  ⟺ (E i : Pᵢ ∨ Qᵢ)                       -- where Pᵢ ≡ coverage(eᵢ) ∩ I₁ ≠ ∅, Qᵢ ≡ coverage(eᵢ) ∩ I₂ ≠ ∅
  ⟺ (E i : Pᵢ) ∨ (E i : Qᵢ)               -- ∃ distributes over ∨
  ⟺ a ∈ findlinks(I₁, Σ) ∨ a ∈ findlinks(I₂, Σ)
  ⟺ a ∈ findlinks(I₁, Σ) ∪ findlinks(I₂, Σ)
```

## F15 — FilteredScopedTransfer (LEMMA/lemma)

```
F15 (FilteredScopedTransfer):
   For both F ∈ {findlinks_filtered(C, ·), findlinks_scoped(I, S, ·)}:
   (a) Determinism:    F(Σ) = F(Σ')  whenever Σ.L = Σ'.L.
   (b) Survivability:  F(Σ) = F(Σ')  across any V ∖ {K.λ} step.
   (c) Monotonicity:   F(Σ) ⊆ F(Σ')  for every reachable Σ →* Σ'.
```

## F19 — ResultSetMonotonicity (LEMMA/lemma)

```
F19 (ResultSetMonotonicity):
   findlinks(I, Σ) ⊆ findlinks(I, Σ') for every reachable Σ →* Σ'.
```

## F20 — ImageSetAdditive (LEMMA/lemma)

```
F20 (ImageSetAdditive):
   For d ∈ dom(Σ.M) and R₁, R₂ ⊆ T:
       image(R₁ ∪ R₂, d, Σ) = image(R₁, d, Σ) ∪ image(R₂, d, Σ).
```

## F20a — VSideAdditive (LEMMA/lemma)

```
F20a (VSideAdditive) — consequence of F12 + F20 + F13:
   For d ∈ dom(Σ.M) and R₁, R₂ ⊆ T:
       findlinks_V(R₁ ∪ R₂, d, Σ) = findlinks_V(R₁, d, Σ) ∪ findlinks_V(R₂, d, Σ).
```

Derivation:
```
findlinks_V(R₁ ∪ R₂, d, Σ)
  = findlinks(image(R₁ ∪ R₂, d, Σ), Σ)                            -- F12 unfold
  = findlinks(image(R₁, d, Σ) ∪ image(R₂, d, Σ), Σ)               -- F20
  = findlinks(image(R₁, d, Σ), Σ) ∪ findlinks(image(R₂, d, Σ), Σ) -- F13
  = findlinks_V(R₁, d, Σ) ∪ findlinks_V(R₂, d, Σ)                 -- F12 refold (twice)
```

## F21 — VSideContractionWP (LEMMA/lemma)

```
F21 (VSideContractionWP):
   For a query region R ⊆ T,
       wp(K.μ⁻[d, ℛ], a ∈ findlinks_V(R, d, ·))
         ≡ enabled(K.μ⁻[d, ℛ])
           ∧ (E i : 1 ≤ i ≤ |Σ.L(a)| : project(a, i, d, Σ) ∩ R ∩ ℛ ≠ ∅).
   where enabled(K.μ⁻[d, ℛ]) is K.μ⁻'s applicability predicate.
```

Where `project(a, i, d, Σ) = {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(Σ.L(a).eᵢ)}` and `ℛ = ⋃ {[S, 1, …, 1, k] : 1 ≤ k ≤ n'_S}` (per-subspace canonical initial segment).

Derivation key step: since `dom(Σ'.M(d)) = ℛ` with `Σ'.M(d)(v) = Σ.M(d)(v)` for `v ∈ ℛ` and `Σ'.L = Σ.L`:
```
image(R, d, Σ') = {Σ.M(d)(v) : v ∈ R ∩ ℛ}

a ∈ findlinks_V(R, d, Σ')
  ⟺ (E i : coverage(Σ.L(a).eᵢ) ∩ {Σ.M(d)(v) : v ∈ R ∩ ℛ} ≠ ∅)
  ⟺ (E i : project(a, i, d, Σ) ∩ R ∩ ℛ ≠ ∅)
```

## F22 — ReorderingDiscoverabilityInvariance (LEMMA/lemma)

```
F22 (ReorderingDiscoverabilityInvariance):
   For the range-preserving reordering K.μ~ on d and the full-document
   query R = T,
       wp(K.μ~[d], a ∈ findlinks_V(T, d, ·))
         ≡ enabled(K.μ~[d]) ∧ a ∈ findlinks_V(T, d, Σ).
```

Derivation: LP11 gives `ran(Σ'.M(d)) = ran(Σ.M(d))` for every admissible `π`. Write `J := ran(Σ.M(d)) = ran(Σ'.M(d))`. Then:
```
a ∈ findlinks_V(T, d, Σ')
  ⟺ matches(a, J, Σ')   -- F12; image(T, d, Σ') = J
  ⟺ matches(a, J, Σ)    -- PerLinkInvarianceUnderValuePreservation at a (Σ'.L(a) = Σ.L(a), fixed J)
  ⟺ a ∈ findlinks_V(T, d, Σ)
```

## F23 — ContractionExtensionWPWeakening (LEMMA/lemma)

```
F23 (ContractionExtensionWPWeakening):
   Let σ = K.μ⁻[d, ℛ] ; K.μ⁺[d] be the composite that first contracts
   d's arrangement to ℛ and then extends it. For the postcondition
   Q ≡ (a ∈ findlinks_V(R, d, ·)):
       wp(K.μ⁻[d, ℛ], Q) ∧ enabled(σ)  ⟹  wp(σ, Q).
```

Three-step derivation:

*(Step 1 — wp composition.)* `wp(σ, Q) = wp(K.μ⁻[d, ℛ], wp(K.μ⁺[d], Q))` by Dijkstra's sequential-composition law (demonic reading for nondeterministic K.μ⁺[d]).

*(Step 2 — extension preserves discoverability.)* For any post-contraction intermediate `Σ_m` and any post-extension successor `Σ_m'`: LP9 gives `project(a, i, d, Σ_m) ⊆ project(a, i, d, Σ_m')` for every slot `i`. Intersecting with fixed `R`: `project(a, i, d, Σ_m) ∩ R ⊆ project(a, i, d, Σ_m') ∩ R`. Therefore `Q(Σ_m) ⟹ Q(Σ_m')` for every successor, giving `[Q ⟹ wp(K.μ⁺[d], Q)]`.

*(Step 3 — wp monotonicity.)* From `[Q ⟹ wp(K.μ⁺[d], Q)]` and monotonicity rule: `wp(K.μ⁻[d, ℛ], Q) ⟹ wp(K.μ⁻[d, ℛ], wp(K.μ⁺[d], Q)) = wp(σ, Q)`.
