# ASN-0099 Claim Statements

*Source: ASN-0099-findlinks-operation.md (revised 2026-05-26) — Extracted: 2026-05-27*

## Definition — Image

```
image(R, d, Σ)
  defined when  d ∈ dom(Σ.M)
  ≡             {Σ.M(d)(v) : v ∈ R ∩ dom(Σ.M(d))}
```

Variables: `R ⊆ T` (query region), `d` (document), `Σ` (system state), `T` (tumbler address space).

---

## Definition — FindLinks

```
findlinks(I, Σ) = {a ∈ dom(Σ.L) : (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)}
```

Variables: `I ⊆ T` (query I-set), `Σ` (system state), `Σ.L` (link store), `Σ.L(a).eᵢ` (i-th endset of link `a`), `coverage(·)` (set of tumbler addresses covered by an endset).

---

## Definition — FindLinksV

```
findlinks_V(R, d, Σ)
  defined when  d ∈ dom(Σ.M)
  ≡             findlinks(image(R, d, Σ), Σ).
```

---

## Definition — FindLinksFiltered

```
findlinks_filtered(C, Σ)
  = {a ∈ dom(Σ.L) : (A (i, J) ∈ C : i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅)}
```

Variables: `C` (constraint set of pairs `(i, J)` with `i ∈ ℕ⁺`, `J ⊆ T`).

Union-form characterization:
```
findlinks(I, Σ) = ⋃_{i = 1}^{N} findlinks_filtered({(i, I)}, Σ)
   where N = max{|Σ.L(a)| : a ∈ dom(Σ.L)}  when dom(Σ.L) ≠ ∅
         N = 0                              when dom(Σ.L) = ∅  (empty union = ∅)
```

---

## Definition — FindLinksScoped

Defined via F14:
```
findlinks_scoped(I, S, Σ) = findlinks(I, Σ) ∩ S
                           = {a ∈ dom(Σ.L) ∩ S : matches(a, I, Σ)}
```

Variables: `S ⊆ T` (scope set).

---

## ComprehensionInvariantUnderΣL — ComprehensionInvariantUnderSigmaL (meta-lemma, lemma)

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
   Predicates built from these — F1's existential, the filtered
   form's universal, scoped intersection — evaluate identically at
   the two states. Set extensionality closes the equality.
```

---

## PerLinkInvarianceUnderValuePreservation — PerLinkInvarianceUnderValuePreservation (sub-lemma, lemma)

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

---

## ChainIndexEqualsAllocationOrder — ChainIndexEqualsAllocationOrder (sub-lemma, lemma)

```
ChainIndexEqualsAllocationOrder — sub-lemma:
   For any document d ∈ dom(Σ.M) and any link addresses
   ℓ₁, ℓ₂ ∈ dom(Σ.L) with home(ℓ₁) = home(ℓ₂) = d:
       ℓ₁ < ℓ₂ under T1  ⟺  ℓ₁ was allocated before ℓ₂ under d.
```

---

## A1a — PublishedFramePreservation (structural lemma, lemma)

```
A1a (published-frame preservation, covering {K.σ, K.α, K.δ, K.μ~,
     K.μ⁺_L}): conclusion immediate from the substrate's published
     `L' = L` frame clause. No interpretive commitment.
```

---

## A1b — ClosedWorldPreservation (convention-grounded lemma, lemma)

```
A1b (closed-world preservation, covering {K.μ⁺, K.μ⁻, K.ρ}):
     conclusion derived from the substrate's effect-clause convention
     under the closed-world reading — components absent from both
     effect and frame are unchanged.
```

---

## A1 — LinkStoreInertOfNonAllocatingOperations (composite lemma, lemma)

```
A1 (LinkStoreInertOfNonAllocatingOperations):
   For every transition Σ → Σ' produced by an operation in V ∖ {K.λ}:
       dom(Σ'.L) = dom(Σ.L) ∧ (A a ∈ dom(Σ.L) :: Σ'.L(a) = Σ.L(a)).
   Equivalently, K.λ is the unique operation of V that modifies the
   link store.

   A1 is the union of:
   - A1a (published-frame preservation, covering {K.σ, K.α, K.δ, K.μ~,
     K.μ⁺_L}): conclusion immediate from the substrate's published
     `L' = L` frame clause. No interpretive commitment.
   - A1b (closed-world preservation, covering {K.μ⁺, K.μ⁻, K.ρ}):
     conclusion derived from the substrate's effect-clause convention
     under the closed-world reading — components absent from both
     effect and frame are unchanged.

   Vocabulary scope: V = {K.σ, K.α, K.λ, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L,
   K.ρ} as published in ASN-0047 and ASN-0093.
```

---

## F1 — MatchPredicate (definition, predicate)

```
F1 (MatchPredicate):
   For a ∈ dom(Σ.L), I ⊆ T, Σ ∈ 𝒮:
   matches(a, I, Σ) ≡ (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅).
```

---

## F2 — Completeness (introduced, lemma)

```
F2 (Completeness):  findlinks(I, Σ) ⊆ result(I, Σ).
```

Variables: `result : 𝒫(T) × 𝒮 → 𝒫(T)` (conforming implementation's output function).

---

## F3 — Soundness (introduced, lemma)

```
F3 (Soundness):     result(I, Σ) ⊆ findlinks(I, Σ).
```

Together F2 ∧ F3 force `result(I, Σ) = findlinks(I, Σ)`.

---

## F2-filt, F3-filt — FilteredConformance (introduced, lemma)

```
F2-filt ∧ F3-filt:  result_filtered(C, Σ) = findlinks_filtered(C, Σ).
```

F2-filt is the completeness containment `findlinks_filtered(C, Σ) ⊆ result_filtered(C, Σ)`. F3-filt is the soundness containment `result_filtered(C, Σ) ⊆ findlinks_filtered(C, Σ)`.

---

## F2-sco, F3-sco — ScopedConformance (introduced, lemma)

```
F2-sco ∧ F3-sco:    result_scoped(I, S, Σ) = findlinks_scoped(I, S, Σ).
```

---

## F2-V, F3-V — VSideConformance (introduced, lemma)

```
F2-V ∧ F3-V:        result_V(R, d, Σ) = findlinks_V(R, d, Σ),
                    for every (R, d, Σ) with d ∈ dom(Σ.M).
```

F2-V is the primary obligation on `result_V`.

---

## F4 — MatchFormulaDesignJustification (introduced, lemma)

```
F4 (MatchFormulaDesignJustification):
   F1's design factors into two separable choices, anchored
   differently.

   (a) Per-endset structure (LM 4/58-anchored). Within each
   endset, satisfaction is existential over spans, and the per-span
   test is overlap (`coverage(span) ∩ I ≠ ∅`). F1's endset-level
   overlap `coverage(eᵢ) ∩ I ≠ ∅` unfolds to this per-span
   existential with an identifiable witness span `(s, ℓ) ∈ eᵢ`.
   Two compositional properties separate F1 from the natural
   alternatives. Spans-monotonicity — adding a non-witnessing
   span to an endset cannot suppress an existing satisfying state —
   is broken only by containment `coverage(eᵢ) ⊆ I`: adding a
   non-conforming span violates the per-span universal. Reverse
   containment `I ⊆ coverage(eᵢ)` and cardinality thresholds
   `|coverage(eᵢ) ∩ I| ≥ k` are themselves spans-monotone — adding
   a span enlarges `coverage(eᵢ)`, so any prior `I ⊆ coverage`-
   satisfaction survives, and `|coverage(eᵢ) ∩ I|` can only weakly
   grow, preserving any prior threshold-satisfaction. What
   distinguishes F1 from these two aggregates is therefore not
   spans-monotonicity but the per-span witness structure: F1's
   match is anchored at a single identifiable span, while reverse
   containment and cardinality fold every span's contribution into
   a global condition with no individual span identifiable as the
   reason for the match. F1 is robust to adversarial junk-span
   insertion on both counts — the witness survives addition and
   remains locatable; containment fails monotonicity outright,
   while the two aggregates preserve satisfaction but lose the
   anchor.

   (b) Across-endsets quantifier (reader-facing surface choice).
   F1 chooses OR-across-slots — the link-level slot-existential
   `(E i : …)` — producing the unfiltered query "is any slot a
   witness?". LM 4/58's literal AND-across-endsets reading is not
   F1; its direct realization is `findlinks_filtered` with per-slot
   constraints, against which F1 is the strict OR-relaxation:
   `findlinks(I, Σ) = ⋃_i findlinks_filtered({(i, I)}, Σ)`. The
   relaxation is design-justified for the unfiltered query: the
   reader's question "what connects here?" does not privilege any
   slot (L7 leaves directional significance to the link type), so a
   slot-symmetric existential is the natural surface answer for the
   unfiltered case. AND-across-slot discrimination is preserved at
   the API level through `findlinks_filtered`, not by altering F1.

   Choices (a) and (b) are independent. Layer-(a) alternatives —
   containment, reverse containment, cardinality thresholds, the
   full-empty extremes — define different operations at the F1 site
   and are surfaced by the conformance contract F2 ∧ F3: any P
   diverging from F1's overlap test produces a result(I, Σ) that
   disagrees with findlinks(I, Σ) on at least one realizable (a, I)
   pair, hence non-conformance with F2 ∧ F3 as written. Layer-(b)
   alternatives are different operations, not competing predicates
   at the F1 site — the AND form is `findlinks_filtered`, conforming
   to F2-filt ∧ F3-filt against a different specification.

   LM 4/60's across-link robustness principle ("THE QUANTITY OF
   LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE
   SEARCH ON OTHERS") is convergent with the overlap choice within
   (a) but is not its direct anchor — LM 4/60 governs the cross-link
   case (junk-link filtering across distinct links), while spans-
   monotonicity within a single endset is grounded in LM 4/58's
   per-endset existential structure itself.

   The uniqueness asserted is operational distinguishability under
   F2 ∧ F3 wired with F1 — not mathematical uniqueness derivable
   from foundation invariants. A spec that wired F2 ∧ F3 to a
   different layer-(a) predicate, or that exposed the layer-(b) AND
   form at the F1 surface, would commit to a different operation.
```

---

## F5 — IdentityNotValue (introduced, lemma)

```
F5 (IdentityNotValue):
   matches(a, I, Σ) consults dom(Σ.L), Σ.L, and coverage(·), never
   Σ.C(·). For distinct α ≠ β, matches(a, {α}, Σ) and
   matches(a, {β}, Σ) are computed independently — each decided by
   address-level membership in coverage(Σ.L(a).eᵢ), with no reference
   to content values.

   Derivation. By inspection of F1's RHS, the existential
   `(E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)` consults
   only |Σ.L(a)|, per-slot endsets Σ.L(a).eᵢ, the coverage function
   on endsets, and the I-set — Σ.C does not appear among the consulted
   components. For distinct α ≠ β, the queries matches(a, {α}, Σ) and
   matches(a, {β}, Σ) reduce per slot to the address-level set-
   membership tests `α ∈ coverage(Σ.L(a).eᵢ)` and
   `β ∈ coverage(Σ.L(a).eᵢ)`; these are independent membership
   predicates over coverage sets, with no shared content lookup.
```

---

## F6 — TransclusionTransparency (introduced, lemma)

```
F6 (TransclusionTransparency):
   For documents d₁, d₂ ∈ dom(Σ.M) and V-positions v₁ ∈ dom(Σ.M(d₁)),
   v₂ ∈ dom(Σ.M(d₂)) with Σ.M(d₁)(v₁) = Σ.M(d₂)(v₂) = α:
       findlinks_V({v₁}, d₁, Σ) = findlinks_V({v₂}, d₂, Σ).
```

---

## F7 — EndsetSymmetry (introduced, lemma)

```
F7 (EndsetSymmetry):
   (a) Slot symmetry: matches(a, I, Σ) consults all slots uniformly.
   (b) Filter conjunction: findlinks_filtered(C, Σ) intersects per-slot
       constraints — a link must satisfy every constraint to appear.
```

Both halves follow from the quantifier structure of the definitions: existential ⇒ slot-symmetric; universal ⇒ conjunctive.

---

## F8 — Determinism (introduced, lemma)

```
F8 (Determinism):
   findlinks(I, Σ) = findlinks(I, Σ')  whenever Σ.L = Σ'.L.
```

---

## F9 — LinkSurvivabilityUnderEdits (introduced, lemma)

```
F9 (LinkSurvivabilityUnderEdits):
   For any single-step transition Σ → Σ' produced by a K.μ-family
   operation (K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L) and any I ⊆ T:
       findlinks(I, Σ) = findlinks(I, Σ').

   F9 follows from F8 via ComprehensionInvariantUnderΣL once
   Σ.L = Σ'.L is discharged: by A1a at K.μ~ and K.μ⁺_L, by A1b at
   K.μ⁺ and K.μ⁻. F9 inherits A1b's commitment at the latter two
   sub-cases.
```

---

## F9-cor — NonAllocatingPreservation (introduced, lemma)

```
F9-cor (NonAllocatingPreservation):
   For every single-step transition Σ → Σ' produced by an operation
   in V ∖ {K.λ} and any I ⊆ T:
       findlinks(I, Σ) = findlinks(I, Σ').

   F9-cor inherits A1b's commitment at the K.μ⁺, K.μ⁻, K.ρ sub-cases;
   the other five operations discharge from A1a. K.δ has three
   sub-cases; the IsDocument sub-case modifies M(d_new) but K.δ's
   published frame includes L' = L uniformly, so F9-cor's I-side
   conclusion holds for all three.
```

---

## F9★ — NonAllocatingMultiStepPreservation (introduced, lemma)

```
F9★ (NonAllocatingMultiStepPreservation):
   For any reachable transition sequence Σ →* Σ' in which every step
   is in V ∖ {K.λ} and any I ⊆ T:
       findlinks(I, Σ) = findlinks(I, Σ').

   The per-step F9-cor chained by transitivity of equality.
```

---

## F9-λ — KLambdaInducedIncrement (introduced, lemma)

```
F9-λ (KλInducedIncrement):
   For any single-step transition Σ → Σ' produced by K.λ allocating
   a fresh link ℓ_new with endsets (e₁, …, e_N), and any I ⊆ T:
       findlinks(I, Σ') = findlinks(I, Σ) ⊎ ({ℓ_new} if matches(ℓ_new, I, Σ') else ∅).

   The two parts are disjoint (⊎): K.λ's freshness precondition
   ℓ_new ∉ dom(Σ.L) ∪ dom(Σ.C) (ASN-0093) gives ℓ_new ∉ dom(Σ.L),
   so ℓ_new ∉ findlinks(I, Σ).

   Derivation. K.λ's effect-clause gives dom(Σ'.L) = dom(Σ.L) ∪
   {ℓ_new} with Σ'.L(a) = Σ.L(a) for every a ∈ dom(Σ.L) (L12
   supplies value preservation on prior keys; K.λ's effect-clause
   adds only the fresh mapping). Split findlinks(I, Σ') by domain
   into the prior-key contribution from dom(Σ.L) and the fresh-key
   contribution from {ℓ_new}. For each a ∈ dom(Σ.L):
   PerLinkInvarianceUnderValuePreservation at this a transports
   matches(a, I, ·) unchanged from Σ to Σ', so the prior-key part
   contributes exactly findlinks(I, Σ). The fresh-key part
   contributes the singleton {ℓ_new} when matches(ℓ_new, I, Σ')
   holds, and ∅ otherwise. ComprehensionInvariantUnderΣL is not
   applicable here (dom(Σ'.L) ⊋ dom(Σ.L)); the per-link primitive
   is the load-bearing step.
```

---

## F10 — OrderedResult (introduced, lemma)

```
F10 (OrderedResult):
   The result set admits a unique presentation as a sequence
   ⟨a₁, a₂, ..., aₙ⟩ with aⱼ ∈ dom(Σ.L) satisfying matches(aⱼ, I, Σ),
   and a₁ < a₂ < ... < aₙ under T1.
```

Finiteness: F3 gives `result(I, Σ) ⊆ dom(Σ.L)`; L-fin gives `|dom(Σ.L)| < ∞`. T1 is a strict total order on `T` restricting to any subset.

---

## F10-filt, F10-sco — FilteredScopedOrderedPresentations (introduced, lemma)

```
F10-filt:  findlinks_filtered(C, Σ) admits a unique strictly T1-increasing sequence.
F10-sco:   findlinks_scoped(I, S, Σ) admits a unique strictly T1-increasing sequence.
```

---

## F10a — AnchorLiftingOfDocumentOrdering (introduced, lemma)

```
F10a (AnchorLiftingOfDocumentOrdering):
   For documents d₁, d₂ ∈ dom(Σ.M) with zeros(d₁) = zeros(d₂) = 2
   (M0, ASN-0093) and d₁ < d₂ under T1, the link sub-allocator
   anchors satisfy b_L(d₁) < b_L(d₂) under T1 and are non-nesting
   under ≼. By PrefixOrderingExtension (ASN-0034), every ℓ₁
   extending b_L(d₁) is strictly less than every ℓ₂ extending b_L(d₂).

   Case (i) (component divergence on documents). The divergence
   position k ≤ min(#d₁, #d₂) with d₁_k < d₂_k carries over to
   b_L(d₁) vs b_L(d₂) at the same position. T1 case (i) at position k
   yields b_L(d₁) < b_L(d₂). Anchors are non-nesting by strict
   component disagreement at k.

   Case (ii) (proper prefix on documents). d₁ ≺ d₂ with
   #d₁ < #d₂. We unfold the conclusion `d₂_{#d₁+1} ≥ 1` in four
   foundation steps. Step 1 (M0, ASN-0093): zeros(d₁) = zeros(d₂) = 2
   at the document level. Step 2 (T4, ASN-0034): T4's last-component
   constraint d[#d] ≠ 0 places d₁'s two zeros at positions strictly
   less than #d₁ (i.e., at positions ≤ #d₁ − 1), and forces
   d₁[#d₁] ≠ 0. Step 3 (Prefix, ASN-0034): d₁ ≺ d₂ unfolds to
   componentwise agreement on positions 1..#d₁, so d₂ inherits
   exactly those two zeros at the same positions ≤ #d₁ − 1, and the
   non-zero terminal d₂[#d₁] = d₁[#d₁] ≠ 0 transports unchanged —
   position #d₁ contributes no zero to d₂'s count. d₂'s remaining
   positions (#d₁+1..#d₂) contribute the balance of the zero count.
   Step 4 (M0 + T0, ASN-0034 + ASN-0093): zeros(d₂) = 2 total, two
   zeros already accounted for at positions ≤ #d₁ − 1, and position
   #d₁ contributing no zero (Step 3), force no additional zeros at
   positions #d₁+1..#d₂; in particular d₂_{#d₁+1} ≠ 0, and T0's
   ℕ-discreteness (no m ∈ ℕ with 0 < m < 1) sharpens this to
   d₂_{#d₁+1} ≥ 1. b_L(d₁) has the appended 0 separator from
   b_L(·) = [·.0.s_L] at position #d₁ + 1. T1 case (i) at position
   #d₁ + 1 yields b_L(d₁) < b_L(d₂). Anchors non-nest at #d₁ + 1.
```

---

## F11 — PersistentDiscoverabilityI (introduced, lemma)

```
F11 (PersistentDiscoverabilityI):
   For any reachable state sequence Σ →* Σ' and any a ∈ dom(Σ.L) with
   matches(a, I, Σ):  a ∈ dom(Σ'.L) ∧ matches(a, I, Σ').
```

LP13 (UnconditionalLinkPersistence, ASN-0098) supplies `a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)`. PerLinkInvarianceUnderValuePreservation then gives `matches(a, I, Σ) ⟺ matches(a, I, Σ')`.

---

## F12 — TwoPhaseFactoring (definition, function)

```
F12 (TwoPhaseFactoring) — DEFINITION of findlinks_V:
   findlinks_V(R, d, Σ)
     defined when  d ∈ dom(Σ.M)
     ≡             findlinks(image(R, d, Σ), Σ).
```

F12 is the citation handle for the unfolding identity. Cite F12 to invoke the unfolding identity; cite `findlinks_V` to invoke the operation itself — same artifact, two labels for two citation purposes.

---

## F13 — SetAdditive (introduced, lemma)

```
F13 (SetAdditive):
   findlinks(I₁ ∪ I₂, Σ) = findlinks(I₁, Σ) ∪ findlinks(I₂, Σ).
```

By distributivity of intersection over union: `coverage(e) ∩ (I₁ ∪ I₂) = (coverage(e) ∩ I₁) ∪ (coverage(e) ∩ I₂)`, non-empty iff at least one disjunct is non-empty.

---

## F14 — ScopeFilter (introduced, lemma)

```
F14 (ScopeFilter):
   findlinks_scoped(I, S, Σ) = findlinks(I, Σ) ∩ S
                             = {a ∈ dom(Σ.L) ∩ S : matches(a, I, Σ)}
```

---

## F15 — FilteredDeterminism (introduced, lemma)

```
F15 (FilteredDeterminism):  findlinks_filtered(C, Σ) = findlinks_filtered(C, Σ') when Σ.L = Σ'.L.
```

Follows from ComprehensionInvariantUnderΣL applied to the filtered universal.

---

## F16 — ScopedDeterminism (introduced, lemma)

```
F16 (ScopedDeterminism):    findlinks_scoped(I, S, Σ) = findlinks_scoped(I, S, Σ') when Σ.L = Σ'.L.
```

Follows from F8 + intersection-preservation with the query-supplied `S`.

---

## F17 — FilteredSurvivability (introduced, lemma)

```
F17 (FilteredSurvivability): findlinks_filtered(C, Σ) = findlinks_filtered(C, Σ') across a K.μ-family step.
```

Follows from F9 (K.μ-family preserves Σ.L) + F15. Inherits A1b's commitment at K.μ⁺ and K.μ⁻ sub-cases.

---

## F18 — ScopedSurvivability (introduced, lemma)

```
F18 (ScopedSurvivability):   findlinks_scoped(I, S, Σ) = findlinks_scoped(I, S, Σ') across a K.μ-family step.
```

Follows from F9 + intersection-preservation. Inherits A1b's commitment at K.μ⁺ and K.μ⁻ sub-cases.

---

## F19 — ResultSetMonotonicity (introduced, lemma)

```
F19 (ResultSetMonotonicity):
   findlinks(I, Σ) ⊆ findlinks(I, Σ') for every reachable Σ →* Σ'.
```

Direct from F11 + the definition of `findlinks`.

---

## F19-filt, F19-sco — FilteredScopedMonotonicity (introduced, lemma)

```
F19-filt: findlinks_filtered(C, Σ) ⊆ findlinks_filtered(C, Σ').
F19-sco:  findlinks_scoped(I, S, Σ) ⊆ findlinks_scoped(I, S, Σ').
```

F19-filt follows from LP13 + PerLinkInvarianceUnderValuePreservation applied per link: for every `a ∈ findlinks_filtered(C, Σ)`, LP13 gives `a ∈ dom(Σ'.L)` and `Σ'.L(a) = Σ.L(a)`, and PerLinkInvarianceUnderValuePreservation transports the filtered per-link universal unchanged to `Σ'`. F19-sco follows from F19 + intersection-preservation with the query-supplied `S`.

---

## F20 — ImageSetAdditive (introduced, lemma)

```
F20 (ImageSetAdditive):
   For d ∈ dom(Σ.M) and R₁, R₂ ⊆ T:
       image(R₁ ∪ R₂, d, Σ) = image(R₁, d, Σ) ∪ image(R₂, d, Σ).
```

The standard image-of-union identity for the partial function `Σ.M(d)`.
