# ASN-0099 Claim Statements

*Source: ASN-0099-findlinks-operation.md (revised 2026-05-26) — Extracted: 2026-06-03*

## Definition — Image

```
image(R, d, Σ)
  defined when  d ∈ dom(Σ.M)
  ≡             {Σ.M(d)(v) : v ∈ R ∩ dom(Σ.M(d))}
```

Variables: `R ⊆ T` (query V-region), `d` document, `Σ` system state. Silent projection: V-positions in `R` absent from `dom(Σ.M(d))` contribute nothing.

## Definition — Findlinks

```
findlinks(I, Σ) = {a ∈ dom(Σ.L) : (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)}
```

Variables: `I ⊆ T` (query I-set), `Σ` system state with link store `Σ.L`.

## Definition — FindlinksV

```
findlinks_V(R, d, Σ)
  defined when  d ∈ dom(Σ.M)
  ≡             findlinks(image(R, d, Σ), Σ).
```

For `d ∉ dom(Σ.M)`, `findlinks_V(R, d, Σ)` is undefined — no silent fallback.

## Definition — FindlinksFiltered

```
findlinks_filtered(C, Σ)
  = {a ∈ dom(Σ.L) : (A (i, J) ∈ C : i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅)}
```

A *slot constraint* is a pair `(i, J)` with `i ∈ ℕ⁺`, `J ⊆ T`. `C` is a set of slot constraints.

Union form relating filtered to unfiltered:
```
findlinks(I, Σ) = ⋃_{i = 1}^{N} findlinks_filtered({(i, I)}, Σ)
   where N = max{|Σ.L(a)| : a ∈ dom(Σ.L)}  when dom(Σ.L) ≠ ∅
         N = 0                              when dom(Σ.L) = ∅  (empty union = ∅)
```

## Definition — FindlinksScoped

```
findlinks_scoped(I, S, Σ) = findlinks(I, Σ) ∩ S
                           = {a ∈ dom(Σ.L) ∩ S : matches(a, I, Σ)}
```

`S ⊆ T` is a scope set (e.g., "all links in document `d`").

## ComprehensionInvariantUnderΣL — ComprehensionInvariantUnderSigmaL (META-LEMMA, lemma)

```
If Σ.L = Σ'.L as partial functions, then for every comprehension
over dom(Σ.L) whose membership predicate consults only Σ.L and
query-data (never Σ.M, Σ.C, Σ.E, Σ.R):
    {a ∈ dom(Σ.L) : P(a, Σ)} = {a ∈ dom(Σ'.L) : P(a, Σ')}.
```

Proof chain: `Σ.L = Σ'.L` gives `dom(Σ.L) = dom(Σ'.L)` and per-link value equality `Σ.L(a) = Σ'.L(a)`. Component-wise tuple equality on Link values (L6) gives `|Σ.L(a)| = |Σ'.L(a)|` and per-slot endset equality `Σ.L(a).eᵢ = Σ'.L(a).eᵢ`. Coverage is a deterministic function of its endset argument. Set extensionality closes the equality.

## PerLinkInvarianceUnderValuePreservation — PerLinkInvarianceUnderValuePreservation (SUB-LEMMA, lemma)

```
For any link a with a ∈ dom(Σ.L) ∩ dom(Σ'.L) and Σ'.L(a) = Σ.L(a):
- matches(a, I, Σ) ⟺ matches(a, I, Σ') for every I ⊆ T.
- For every slot constraint (i, J), the per-link filter conjunct
    i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅
  evaluates identically at Σ and Σ'.
- Consequently, for every constraint set C, the filtered per-link
  universal (A (i, J) ∈ C : i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅)
  evaluates identically at Σ and Σ'.
```

## ChainIndexEqualsAllocationOrder — ChainIndexEqualsAllocationOrder (SUB-LEMMA, lemma)

```
For any document d ∈ dom(Σ.M) and any link addresses
ℓ₁, ℓ₂ ∈ dom(Σ.L) with home(ℓ₁) = home(ℓ₂) = d:
    ℓ₁ < ℓ₂ under T1  ⟺  ℓ₁ was allocated before ℓ₂ under d.
```

## A1a — PublishedFramePreservation (LEMMA, lemma)

```
Every atomic operation in V ∖ {K.λ} — {K.α, K.δ, K.μ⁺, K.μ⁻, K.μ⁺_L, K.ρ} —
publishes L' = L in its operative frame. Consequently, for every
transition Σ → Σ' produced by any such operation:
    dom(Σ'.L) = dom(Σ.L) ∧ (A a ∈ dom(Σ.L) :: Σ'.L(a) = Σ.L(a)).

K.μ⁺ and K.μ⁻ operative definitions in this ASN's extended state
Σ = (C, L, M, E, R) are ASN-0047's amended versions — K.μ⁺ amendment
(ContentSubspaceRestriction) and K.μ⁻ per-subspace scope
(PerSubspaceContractionScope) — both of whose extended-state frames
publish L' = L explicitly.

K.μ~ is excluded from A1a: it is the non-atomic composite K.μ⁻ + K.μ⁺;
its frame clause L' = L is labelled "(derived)".
```

## A1 — LinkStoreInertOfNonAllocatingOperations (LEMMA, lemma)

```
For every transition Σ → Σ' produced by an operation in V ∖ {K.λ}:
    dom(Σ'.L) = dom(Σ.L) ∧ (A a ∈ dom(Σ.L) :: Σ'.L(a) = Σ.L(a)).
Equivalently, K.λ is the unique operation of V that modifies the
link store.

Vocabulary scope: V = {K.α, K.λ, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L, K.ρ}
(ASN-0047's extended-state vocabulary, K.μ~ the sole non-atomic member).
K.μ~ reached only through its K.μ⁻ + K.μ⁺ decomposition, each step
discharged by A1a; link-store inertness across the composite is the
transitive composition of A1a at K.μ⁻ and A1a at K.μ⁺.
```

## F1 — MatchPredicate (DEFINITION, predicate)

```
F1 (MatchPredicate):
For a ∈ dom(Σ.L), I ⊆ T, Σ ∈ 𝒮:
matches(a, I, Σ) ≡ (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅).
```

## F2 — Completeness (LEMMA, lemma)

```
F2 (Completeness):  findlinks(I, Σ) ⊆ result(I, Σ).
```

`result : 𝒫(T) × 𝒮 → 𝒫(T)` is a conforming implementation's output function.

## F3 — Soundness (LEMMA, lemma)

```
F3 (Soundness):  result(I, Σ) ⊆ findlinks(I, Σ).
```

F2 ∧ F3 together force `result(I, Σ) = findlinks(I, Σ)`.

## F2-filt, F3-filt — FilteredConformance (LEMMA, lemma)

```
F2-filt ∧ F3-filt:  result_filtered(C, Σ) = findlinks_filtered(C, Σ).
```

F2-filt: `findlinks_filtered(C, Σ) ⊆ result_filtered(C, Σ)`.
F3-filt: `result_filtered(C, Σ) ⊆ findlinks_filtered(C, Σ)`.

## F2-sco, F3-sco — ScopedConformance (LEMMA, lemma)

```
F2-sco ∧ F3-sco:  result_scoped(I, S, Σ) = findlinks_scoped(I, S, Σ).
```

F2-sco: `findlinks_scoped(I, S, Σ) ⊆ result_scoped(I, S, Σ)`.
F3-sco: `result_scoped(I, S, Σ) ⊆ findlinks_scoped(I, S, Σ)`.

## F2-V, F3-V — VSideConformance (LEMMA, lemma)

```
F2-V ∧ F3-V:  result_V(R, d, Σ) = findlinks_V(R, d, Σ),
              for every (R, d, Σ) with d ∈ dom(Σ.M).
```

F2-V: `findlinks_V(R, d, Σ) ⊆ result_V(R, d, Σ)`.
F3-V: `result_V(R, d, Σ) ⊆ findlinks_V(R, d, Σ)`.

This is the primary obligation on `result_V`. When an implementation also exposes the I-side surface satisfying F2 ∧ F3, the factoring equation `result_V(R, d, Σ) = result(image(R, d, Σ), Σ)` follows by F2 ∧ F3 + F2-V ∧ F3-V + F12.

## F4 — MatchFormulaDesignJustification (LEMMA, lemma)

```
F4 (MatchFormulaDesignJustification):
F1's design factors into two separable choices:

(a) Per-endset structure (LM 4/58-anchored).
Within each endset, satisfaction is existential over spans, and the
per-span test is overlap (coverage(span) ∩ I ≠ ∅). F1's endset-level
overlap coverage(eᵢ) ∩ I ≠ ∅ unfolds to this per-span existential
with an identifiable witness span (s, ℓ) ∈ eᵢ.

Spans-monotonicity — adding a non-witnessing span to an endset cannot
suppress an existing satisfying state — is broken only by containment
coverage(eᵢ) ⊆ I. Reverse containment I ⊆ coverage(eᵢ) and cardinality
thresholds |coverage(eᵢ) ∩ I| ≥ k are themselves spans-monotone.
F1 is distinguished from reverse containment and cardinality aggregates
by the per-span witness structure: F1's match is anchored at a single
identifiable span; the aggregates fold every span's contribution into
a global condition.

(b) Across-endsets quantifier (reader-facing surface choice).
F1 chooses OR-across-slots — the link-level slot-existential (E i : …).
F1 is the strict OR-relaxation of findlinks_filtered:
    findlinks(I, Σ) = ⋃_i findlinks_filtered({(i, I)}, Σ).

Choices (a) and (b) are independent. Any P diverging from F1's overlap
test produces result(I, Σ) disagreeing with findlinks(I, Σ) on at least
one realizable (a, I) pair, hence non-conformance with F2 ∧ F3.
The uniqueness asserted is operational distinguishability under F2 ∧ F3
wired with F1 — not mathematical uniqueness derivable from foundation
invariants.
```

## F5 — IdentityNotValue (LEMMA, lemma)

```
F5 (IdentityNotValue):
matches(a, I, Σ) consults dom(Σ.L), Σ.L, and coverage(·), never Σ.C(·).
For distinct α ≠ β, matches(a, {α}, Σ) and matches(a, {β}, Σ) are computed
independently — each decided by address-level membership in
coverage(Σ.L(a).eᵢ), with no reference to content values.

Derivation: the existential (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)
consults only |Σ.L(a)|, per-slot endsets Σ.L(a).eᵢ, the coverage function
on endsets, and the I-set — Σ.C does not appear. For distinct α ≠ β, the
queries reduce per slot to the address-level set-membership tests
α ∈ coverage(Σ.L(a).eᵢ) and β ∈ coverage(Σ.L(a).eᵢ): independent
membership predicates over coverage sets with no shared content lookup.
```

## F6 — TransclusionTransparency (LEMMA, lemma)

```
F6 (TransclusionTransparency):
For documents d₁, d₂ ∈ dom(Σ.M) and V-positions v₁ ∈ dom(Σ.M(d₁)),
v₂ ∈ dom(Σ.M(d₂)) with Σ.M(d₁)(v₁) = Σ.M(d₂)(v₂) = α:
    findlinks_V({v₁}, d₁, Σ) = findlinks_V({v₂}, d₂, Σ).
```

## F7 — EndsetSymmetry (LEMMA, lemma)

```
F7 (EndsetSymmetry):
(a) Slot symmetry: matches(a, I, Σ) consults all slots uniformly.
(b) Filter conjunction: findlinks_filtered(C, Σ) intersects per-slot
    constraints — a link must satisfy every constraint to appear.
```

Both halves follow from the quantifier structure of the definitions: existential ⇒ slot-symmetric; universal ⇒ conjunctive.

## F8 — Determinism (LEMMA, lemma)

```
F8 (Determinism):
findlinks(I, Σ) = findlinks(I, Σ')  whenever Σ.L = Σ'.L.
```

## F9 — LinkSurvivabilityUnderEdits (LEMMA, lemma)

```
F9 (LinkSurvivabilityUnderEdits):
For any single-step transition Σ → Σ' produced by an atomic
K.μ-family operation (K.μ⁺, K.μ⁻, K.μ⁺_L) and any I ⊆ T:
    findlinks(I, Σ) = findlinks(I, Σ').

K.μ~ is deliberately absent from the single-step quantifier: it is the
non-atomic composite K.μ⁻ + K.μ⁺, so an invocation is two atomic
transitions Σ → Σ_mid → Σ', not one arrow.
```

## F9~ — ReorderingSurvivability (LEMMA, lemma)

```
F9~ (ReorderingSurvivability):
For any K.μ~ invocation Σ → Σ_mid → Σ' (its K.μ⁻ + K.μ⁺ decomposition)
and any I ⊆ T:
    findlinks(I, Σ) = findlinks(I, Σ').

Proof: F9 at the K.μ⁻ step gives findlinks(I, Σ) = findlinks(I, Σ_mid);
F9 at the K.μ⁺ step gives findlinks(I, Σ_mid) = findlinks(I, Σ');
compose by transitivity.
```

## F9-cor — NonAllocatingPreservation (LEMMA, lemma)

```
F9-cor (NonAllocatingPreservation):
For every single-step transition Σ → Σ' produced by an atomic
operation in V ∖ {K.λ} — i.e. any member of V ∖ {K.λ, K.μ~} — and
any I ⊆ T:
    findlinks(I, Σ) = findlinks(I, Σ').

The lone non-atomic member K.μ~ is excluded from this single-step
quantifier and reached only through F9★ over its K.μ⁻ + K.μ⁺
decomposition (equivalently, F9~).
```

## F9★ — NonAllocatingMultiStepPreservation (LEMMA, lemma)

```
F9★ (NonAllocatingMultiStepPreservation):
For any reachable transition sequence Σ →* Σ' in which every
atomic step is in V ∖ {K.λ} and any I ⊆ T:
    findlinks(I, Σ) = findlinks(I, Σ').

The per-step F9-cor chained by transitivity of equality. A K.μ~
invocation appearing in the sequence contributes its two atomic steps
K.μ⁻ and K.μ⁺ (both in V ∖ {K.λ}), so F9★ covers it without
special-casing; F9~ is the two-step instance.
```

## F9-λ — KlambdaInducedIncrement (LEMMA, lemma)

```
F9-λ (KλInducedIncrement):
For any single-step transition Σ → Σ' produced by K.λ allocating
a fresh link ℓ_new with endsets (e₁, …, e_N), and any I ⊆ T:
    findlinks(I, Σ') = findlinks(I, Σ) ⊎ ({ℓ_new} if matches(ℓ_new, I, Σ') else ∅).

The two parts are disjoint (⊎): K.λ's freshness precondition
ℓ_new ∉ dom(Σ.L) ∪ dom(Σ.C) (ASN-0093) gives ℓ_new ∉ dom(Σ.L),
so ℓ_new ∉ findlinks(I, Σ).

Derivation: K.λ's effect-clause gives dom(Σ'.L) = dom(Σ.L) ∪ {ℓ_new}
with Σ'.L(a) = Σ.L(a) for every a ∈ dom(Σ.L). Split findlinks(I, Σ')
by domain into the prior-key contribution from dom(Σ.L) and the
fresh-key contribution from {ℓ_new}. For each a ∈ dom(Σ.L):
PerLinkInvarianceUnderValuePreservation transports matches(a, I, ·)
unchanged from Σ to Σ', so the prior-key part contributes exactly
findlinks(I, Σ). The fresh-key part contributes {ℓ_new} when
matches(ℓ_new, I, Σ') holds, and ∅ otherwise.
```

## F10 — OrderedResult (LEMMA, lemma)

```
F10 (OrderedResult):
The result set admits a unique presentation as a sequence
⟨a₁, a₂, ..., aₙ⟩ with aⱼ ∈ dom(Σ.L) satisfying matches(aⱼ, I, Σ),
and a₁ < a₂ < ... < aₙ under T1.

Finiteness: F3 gives result(I, Σ) ⊆ dom(Σ.L); L-fin gives |dom(Σ.L)| < ∞.
T1 is a strict total order on T and restricts to one on any subset.
```

## F10-filt, F10-sco — FilteredScopedOrderedPresentations (LEMMA, lemma)

```
F10-filt:  findlinks_filtered(C, Σ) admits a unique strictly T1-increasing sequence.
F10-sco:   findlinks_scoped(I, S, Σ) admits a unique strictly T1-increasing sequence.
```

## F10a — AnchorLiftingOfDocumentOrdering (LEMMA, lemma)

```
F10a (AnchorLiftingOfDocumentOrdering):
For documents d₁, d₂ ∈ dom(Σ.M) with zeros(d₁) = zeros(d₂) = 2
(M0, ASN-0093) and d₁ < d₂ under T1, the link sub-allocator anchors
satisfy b_L(d₁) < b_L(d₂) under T1 and are non-nesting under ≼.
By PrefixOrderingExtension (ASN-0034), every ℓ₁ extending b_L(d₁) is
strictly less than every ℓ₂ extending b_L(d₂).

Case (i) (component divergence on documents): The divergence position
k ≤ min(#d₁, #d₂) with d₁_k < d₂_k carries over to b_L(d₁) vs b_L(d₂)
at the same position. T1 case (i) at position k yields b_L(d₁) < b_L(d₂).
Anchors are non-nesting by strict component disagreement at k.

Case (ii) (proper prefix on documents): d₁ ≺ d₂ with #d₁ < #d₂.
Step 1 (M0): zeros(d₁) = zeros(d₂) = 2. Step 2 (T4): T4's
last-component constraint d[#d] ≠ 0 places d₁'s two zeros at positions
≤ #d₁ − 1 and forces d₁[#d₁] ≠ 0. Step 3 (Prefix): d₁ ≺ d₂ gives
componentwise agreement on positions 1..#d₁. Step 4 (M0 + T0):
zeros(d₂) = 2 total, two zeros already at positions ≤ #d₁ − 1, and
d₂_{#d₁+1} ≠ 0; T0's ℕ-discreteness sharpens to d₂_{#d₁+1} ≥ 1.
b_L(d₁) has the appended 0 separator from b_L(·) = [·.0.s_L] at
position #d₁ + 1. T1 case (i) at position #d₁ + 1 yields b_L(d₁) < b_L(d₂).
```

## F11 — PersistentDiscoverabilityI (LEMMA, lemma)

```
F11 (PersistentDiscoverabilityI):
For any reachable state sequence Σ →* Σ' and any a ∈ dom(Σ.L) with
matches(a, I, Σ):  a ∈ dom(Σ'.L) ∧ matches(a, I, Σ').

LP13 (UnconditionalLinkPersistence, ASN-0098) supplies the multi-step
per-link guarantee a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a).
PerLinkInvarianceUnderValuePreservation applied at this a then gives
matches(a, I, Σ) ⟺ matches(a, I, Σ').
```

## F12 — TwoPhaseFactoring (DEFINITION, definition)

```
F12 (TwoPhaseFactoring) — DEFINITION of findlinks_V:
findlinks_V(R, d, Σ)
  defined when  d ∈ dom(Σ.M)
  ≡             findlinks(image(R, d, Σ), Σ).

Cite F12 to invoke the unfolding identity; cite findlinks_V to invoke
the operation itself — same artifact, two labels for two citation purposes.
```

## F13 — SetAdditive (LEMMA, lemma)

```
F13 (SetAdditive):
findlinks(I₁ ∪ I₂, Σ) = findlinks(I₁, Σ) ∪ findlinks(I₂, Σ).

Proof chain (for any a ∈ dom(Σ.L), writing eᵢ = Σ.L(a).eᵢ,
Pᵢ ≡ coverage(eᵢ) ∩ I₁ ≠ ∅, Qᵢ ≡ coverage(eᵢ) ∩ I₂ ≠ ∅):

a ∈ findlinks(I₁ ∪ I₂, Σ)
  ⟺ (E i : coverage(eᵢ) ∩ (I₁ ∪ I₂) ≠ ∅)
  ⟺ (E i : Pᵢ ∨ Qᵢ)
  ⟺ (E i : Pᵢ) ∨ (E i : Qᵢ)
  ⟺ a ∈ findlinks(I₁, Σ) ∨ a ∈ findlinks(I₂, Σ)
  ⟺ a ∈ findlinks(I₁, Σ) ∪ findlinks(I₂, Σ)
```

## F14 — ScopeFilter (DEFINITION, definition)

```
F14 (ScopeFilter):
findlinks_scoped(I, S, Σ) = findlinks(I, Σ) ∩ S
                           = {a ∈ dom(Σ.L) ∩ S : matches(a, I, Σ)}
```

## F15, F16 — FilteredScopedDeterminism (LEMMA, lemma)

```
F15 (FilteredDeterminism):
findlinks_filtered(C, Σ) = findlinks_filtered(C, Σ')  when Σ.L = Σ'.L.

F16 (ScopedDeterminism):
findlinks_scoped(I, S, Σ) = findlinks_scoped(I, S, Σ')  when Σ.L = Σ'.L.
```

F15 follows from ComprehensionInvariantUnderΣL applied to the filtered universal. F16 follows from F8 + intersection-preservation with the query-supplied `S`.

## F17, F18 — FilteredScopedSurvivability (LEMMA, lemma)

```
F17 (FilteredSurvivability):
findlinks_filtered(C, Σ) = findlinks_filtered(C, Σ')  across an atomic K.μ-family step.

F18 (ScopedSurvivability):
findlinks_scoped(I, S, Σ) = findlinks_scoped(I, S, Σ')  across an atomic K.μ-family step.
```

F17 follows from F9 + F15. F18 follows from F9 + intersection-preservation. Across a K.μ~ invocation, F17 and F18 compose over its K.μ⁻ + K.μ⁺ decomposition.

## F19 — ResultSetMonotonicity (LEMMA, lemma)

```
F19 (ResultSetMonotonicity):
findlinks(I, Σ) ⊆ findlinks(I, Σ')  for every reachable Σ →* Σ'.
```

## F19-filt, F19-sco — FilteredScopedMonotonicity (LEMMA, lemma)

```
F19-filt: findlinks_filtered(C, Σ) ⊆ findlinks_filtered(C, Σ').
F19-sco:  findlinks_scoped(I, S, Σ) ⊆ findlinks_scoped(I, S, Σ').

For F19-filt: for every a ∈ findlinks_filtered(C, Σ), LP13 gives
a ∈ dom(Σ'.L) and Σ'.L(a) = Σ.L(a), and PerLinkInvarianceUnderValuePreservation
transports the filtered per-link universal unchanged to Σ', so
a ∈ findlinks_filtered(C, Σ').
F19-sco follows from F19 + intersection-preservation with the query-supplied S.
```

## F20 — ImageSetAdditive (LEMMA, lemma)

```
F20 (ImageSetAdditive):
For d ∈ dom(Σ.M) and R₁, R₂ ⊆ T:
    image(R₁ ∪ R₂, d, Σ) = image(R₁, d, Σ) ∪ image(R₂, d, Σ).

Proof: image(R, d, Σ) = {Σ.M(d)(v) : v ∈ R ∩ dom(Σ.M(d))}, and
(R₁ ∪ R₂) ∩ dom(Σ.M(d)) = (R₁ ∩ dom(Σ.M(d))) ∪ (R₂ ∩ dom(Σ.M(d))).
```

## F20a — VSideAdditive (LEMMA, lemma)

```
F20a (VSideAdditive):
For d ∈ dom(Σ.M) and R₁, R₂ ⊆ T:
    findlinks_V(R₁ ∪ R₂, d, Σ) = findlinks_V(R₁, d, Σ) ∪ findlinks_V(R₂, d, Σ).

Derivation:
findlinks_V(R₁ ∪ R₂, d, Σ)
  = findlinks(image(R₁ ∪ R₂, d, Σ), Σ)                            -- F12 unfold
  = findlinks(image(R₁, d, Σ) ∪ image(R₂, d, Σ), Σ)               -- F20 image-of-union
  = findlinks(image(R₁, d, Σ), Σ) ∪ findlinks(image(R₂, d, Σ), Σ) -- F13 set-additive
  = findlinks_V(R₁, d, Σ) ∪ findlinks_V(R₂, d, Σ)                 -- F12 refold (twice)
```
