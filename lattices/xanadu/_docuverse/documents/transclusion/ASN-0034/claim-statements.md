# ASN-0034 Formal Statements

*Source: ASN-0034-tumbler-algebra.md (revised 2026-03-26) — Extracted: 2026-05-08*

## ActionPoint — ActionPoint

Defines the action point of a positive tumbler as the index of its first nonzero component. Because the tumbler is positive, at least one nonzero component exists, so the minimum is always well-defined and falls within the tumbler's length.

*Formal Contract:*
- *Preconditions:* w ∈ T, Pos(w)
- *Definition:* actionPoint(w) is the unique m ∈ S with (A n ∈ S :: m ≤ n), where S = {i ∈ ℕ : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}.
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set appearing in the comprehension `S = {i ∈ ℕ : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}` defining S, over which the bounded universal `(A i ∈ ℕ : 1 ≤ i < actionPoint(w) : wᵢ = 0)` of the *Postconditions:* ranges, and as the ambient set whose elements the bound variables `m, n` of NAT-wellorder's least-element principle `(E m ∈ S :: (A n ∈ S :: m ≤ n))` inhabit when instantiated on S (since `S ⊆ ℕ`).
  - T0 (CarrierSetDefinition) — supplies T, #w, component projection wᵢ, the commitment that the index domain `{1, …, #w}` of w is a subset of ℕ, and the commitment that the component projection delivers ℕ-valued components (i.e., `wᵢ ∈ ℕ` for each `i ∈ {1, …, #w}`), which types `w_{actionPoint(w)}` as a natural number and thereby licenses the NAT-zero and NAT-discrete instantiations at `n = w_{actionPoint(w)}`.
  - TA-Pos (PositiveTumbler) — supplies Pos(w) and the existential making S nonempty.
  - NAT-wellorder (NatWellOrdering) — least-element principle giving existence of m ∈ S with (A n ∈ S :: m ≤ n).
  - NAT-zero (NatZeroMinimum) — supplies the disjunction axiom `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` instantiated at n = w_{actionPoint(w)}, and 0 ∈ ℕ.
  - NAT-order (NatStrictTotalOrder) — definition of ≤ as `m ≤ n ⟺ m < n ∨ m = n`; irreflexivity and transitivity, used in the case analysis that secures uniqueness of the least element of S and in the derivation that wᵢ = 0 for 1 ≤ i < actionPoint(w) (unfolding actionPoint(w) ≤ #w and chaining with i < actionPoint(w) to reach i < #w, then folding to i ≤ #w).
  - NAT-discrete (NatDiscreteness) — forward direction m < n ⟹ m + 1 ≤ n.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` directly and the additive identity `(A n ∈ ℕ :: 0 + n = n)`, whose instantiation at n = 1 gives the equality 0 + 1 = 1 used to rewrite.
- *Postconditions:* 1 ≤ actionPoint(w) ≤ #w; `(A i ∈ ℕ : 1 ≤ i < actionPoint(w) : wᵢ = 0)`; 1 ≤ w_{actionPoint(w)}

---

## AllocatedSet — AllocatedSet

Defines the concrete set of allocated addresses at any reachable system state as the union of finite prefixes drawn from each activated allocator's theoretical domain. Establishes that allocation-relevant properties proved over T10a's abstract per-allocator chains transfer without modification to the realized finite prefixes seen in any actual execution state.

*Formal Contract:*
- *Definitions:*
  - *State space:* 𝒮 is the state space of the allocation system; `s ∈ 𝒮` is a pair `(Act(s), nₛ)` where `Act(s) ⊆ 𝒯` is the set of activated allocators and `nₛ` assigns each `A ∈ Act(s)` a count `nₛ(A) ≥ 0` of sibling increments performed. For `A ∉ Act(s)`, nₛ(A) is not defined.
  - *Activation predicate:* `activated(A, s) ≡ A ∈ Act(s)` — a projection of the Act component, total on 𝒯 × 𝒮 and computed from s alone (no induction over transitions).
  - *Transition vocabulary:* Σ is the system's transition vocabulary; each `op ∈ Σ` is a partial function `op : 𝒮 ⇀ 𝒮`. The predicate `op(s) defined` abbreviates `s ∈ dom(op)`; when it holds, `op(s) ∈ 𝒮` is the unique successor state.
  - *State transition:* `s → s'` is the pair `(s, op(s))` with `op ∈ Σ` and `s ∈ dom(op)`.
  - *Realized domain:* domₛ(A) = {t₀, …, t_{nₛ(A)}} where tᵢ₊₁ = inc(tᵢ, 0), when activated(A, s); domₛ(A) = ∅ when ¬activated(A, s). The second clause makes domₛ total on 𝒯 × 𝒮 and keeps the definition well-formed when nₛ(A) is undefined (outside Act(s) it is never evaluated).
  - *Allocated set:* allocated(s) = ⋃ { domₛ(A) : activated(A, s) }.
- *Axiom (admissibility of Σ):* Every `op ∈ Σ` whose application yields `s → s'` realizes exactly one of three transition shapes:
  - *(T1) Sibling increment of `A ∈ Act(s)`:* Act(s') = Act(s); nₛ'(A) = nₛ(A) + 1; nₛ'(B) = nₛ(B) for every `B ∈ Act(s) ∖ {A}`. The step applies `inc(tₙₛ(A), 0)` to A's frontier.
  - *(T2) Child spawn of `A ∉ Act(s)`:* admissible in s only when `parent(A) ∈ Act(s)` and `spawnPt(A) ∈ domₛ(parent(A))` — equivalently, `spawnPt(A) = tᵢ for some i with 0 ≤ i ≤ nₛ(parent(A))`, i.e., spawnPt(A) is an already-realized sibling of parent(A) in s, not necessarily parent's current frontier; under this precondition the step applies `inc(spawnPt(A), spawnParam(A))` with `spawnParam(A) ∈ {1, 2}`, yielding A's base address `t₀ ∈ dom(A)`; Act(s') = Act(s) ∪ {A}; nₛ'(A) = 0; nₛ'(B) = nₛ(B) for every `B ∈ Act(s)`.
  - *(T3) Non-allocating:* Act(s') = Act(s); nₛ'(B) = nₛ(B) for every `B ∈ Act(s)`; every realized domain is unchanged.
- *Postconditions:*
  - *Initial state:* Act(s₀) = {root}, nₛ₀(root) = 0, and `allocated(s₀) = {t₀}` where t₀ is the root allocator's base address.
  - *Persistence of activation:* for every admissible transition `s → s'`, `Act(s) ⊆ Act(s')`, equivalently `activated(A, s) ⟹ activated(A, s')`.
  - *No spontaneous activation:* if `A ∉ Act(s)` and `s → s'` is not a (T2) step spawning A, then `A ∉ Act(s')`.
  - *No repeat activation:* along any admissible transition sequence, no allocator's (T2) spawn step occurs twice (by T10a's at-most-once constraint on `(t, k')` pairs).
  - *Path-independence of activation:* for any two admissible transition sequences from s₀ that terminate at the same state s, the activated set Act(s) is the same along both. This is structural — activation is a projection of s, so any two paths sharing an endpoint share Act(s) by construction — not a derived consequence of α and β.
  - *Inclusion (i):* for every reachable s and every activated A, `domₛ(A) ⊆ dom(A)`.
  - *Initial-segment structure (ii):* `domₛ(A) = {tᵢ : 0 ≤ i ≤ nₛ(A)}`, and the indices i agree with T10a's enumeration of `dom(A)` — the same `tᵢ₊₁ = inc(tᵢ, 0)` chain generates both, so no index is skipped, no element is out of order, no gap appears.
  - *Reachable-state containment (iii):* `dom(A) ⊇ ⋃ { domₛ(A) : s reachable from s₀ }`. The reverse inclusion is a liveness statement not furnished by this ASN.
  - *Transfer of T9 to realized allocations:* for every reachable s, every activated A, and every pair `a, b ∈ domₛ(A)` with `a = tᵢ, b = tⱼ` and `i < j ≤ nₛ(A)`: `same_allocator(a, b)` (T10a) and `allocated_before(a, b)` (T9) hold by (i) and (ii), and T9's forward-ordering conclusion `a < b` applies to the pair.
- *Frame:* for every non-allocation-affecting (i.e., (T3)) transition `s → s'` and every `A ∈ 𝒯`, `activated(A, s) ≡ activated(A, s')` and, where activation holds, `domₛ(A) = domₛ'(A)`; thus `allocated(s) = allocated(s')`.
- *Depends:*
  - T0 (CarrierSetDefinition) — the carrier T of tumblers and the component-projection / length primitives used to index each allocator's chain.
  - T0(a) (UnboundedComponentValues) — component values are unbounded at every position, underwriting the inexhaustibility of the sibling `inc(·,0)` chain.
  - T0(b) (UnboundedLength) — tumbler length is unbounded, so allocator nesting via deep increments is not capped.
  - T9 (ForwardAllocation) — `allocated_before` ordering and per-allocator forward-ordering conclusion.
  - T10a (AllocatorDiscipline) — allocator tree 𝒯 with root, spawning triples `(parent(A), spawnPt(A), spawnParam(A))` and the `k' ∈ {1, 2}` child-spawning rule (used by admissibility shape (T2)), the per-allocator chain `dom(A) = {tₙ : n ≥ 0}`, and the at-most-once constraint on `(t, k')` pairs (forbids double spawning, so (T2) cannot fire twice for the same A).

---

## D0 — DisplacementWellDefined

Establishes that when a < b and the divergence point does not exceed a's length, the displacement b ⊖ a is a well-defined positive tumbler whose action point equals the divergence index. The round-trip a ⊕ (b ⊖ a) recovers b exactly when a is no longer than b; if a is strictly longer than b, the round-trip is guaranteed to fail.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, a < b, divergence(a, b) ≤ #a
- *Depends:*
  - Divergence (Divergence) — case structure and symmetry; case (i) gives shared-bound conjunction.
  - T1 (LexicographicOrder) — case (i) gives `aₖ < bₖ`; case (ii) gives `b < a` for the prefix sub-case.
  - TA2 (WellDefinedSubtraction) — `b ⊖ a ∈ T` from `b ≥ a`.
  - TumblerSub (TumblerSub) — component formulas, length-pair dispatch at `(#b, #a)`, and conditional postcondition (positivity, action point).
  - ZPD (ZPD) — `zpd(b, a) = divergence(b, a)` in case (i).
  - T3 (CanonicalRepresentation) — distinct lengths imply distinct tumblers.
  - TA-Pos (PositiveTumbler) — defines `Pos`.
  - ActionPoint (ActionPoint) — defines `actionPoint`.
  - TA0 (WellDefinedAddition) — `a ⊕ w ∈ T` from `Pos(w)` and `actionPoint(w) ≤ #a`.
  - TumblerAdd (TumblerAdd) — result-length identity `#(a ⊕ w) = #w`.
  - NAT-sub (NatPartialSubtraction) — conditional closure for `wₖ = bₖ − aₖ ∈ ℕ`; strict positivity for `wₖ ≥ 1`.
  - NAT-order (NatStrictTotalOrder) — trichotomy at `(#a, #a + 1)` for the sub-case (ii-a) refutation; definition of `≤` from `<` to convert `bₖ > aₖ` to `bₖ ≥ aₖ`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality `#a < #a + 1`.
- *Forward References:*
  - D1 (RoundTripRecovery) — proves the component-by-component recovery that this claim navigates to under the #a ≤ #b condition
- *Postconditions:* b ⊖ a ∈ T, Pos(b ⊖ a), actionPoint(b ⊖ a) = divergence(a, b), #(b ⊖ a) = L (per TumblerSub's length-pair dispatch at `(#b, #a)`), a ⊕ (b ⊖ a) ∈ T, #a > #b → a ⊕ (b ⊖ a) ≠ b

---

## D1 — DisplacementRoundTrip

Proves the displacement round-trip identity: when a < b, the divergence point does not exceed a's length, and a is no longer than b, then a ⊕ (b ⊖ a) = b exactly. This is the affirmative half of D0's conditional — the length constraint #a ≤ #b is the precise condition that closes the round-trip.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, a < b, divergence(a, b) ≤ #a, #a ≤ #b
- *Depends:*
  - Divergence (Divergence) — case (i) supplies aᵢ = bᵢ for 1 ≤ i < k, shared-bound k ≤ #a ∧ k ≤ #b, and aₖ ≠ bₖ; sub-case (ii-a) instantiated by a-proper-prefix-of-b rules out T1 case (ii) for (a, b) by forcing divergence(a, b) = #a + 1 against k ≤ #a; uniqueness clause for case (i) identifies T1 case (i)'s witness j with k, lifting aⱼ < bⱼ to aₖ < bₖ; symmetry bridges divergence(a, b) = divergence(b, a).
  - T1 (LexicographicOrder) — supplies a witness j for a < b in one of two cases; case (ii) is eliminated for the pair (a, b) (it would make a a proper prefix of b, instantiating Divergence sub-case (ii-a) and contradicting k ≤ #a), so case (i) holds with aⱼ < bⱼ at j ≤ #a ∧ j ≤ #b and aᵢ = bᵢ for 1 ≤ i < j — Divergence's uniqueness then identifies j = k, yielding aₖ < bₖ; discharges TumblerSub's precondition b ≥ a from a < b via the ≤ abbreviation (a ≤ b ≡ a < b ∨ a = b) and the ≥ abbreviation (b ≥ a ≡ a ≤ b).
  - ZPD (ZPD) — identifies zpd(b, a) = divergence(b, a) in case (i).
  - TumblerSub (TumblerSub) — component formulas for w = b ⊖ a, w ∈ T, length-pair dispatch, and conditional postcondition actionPoint(w) = zpd(b, a).
  - TA-Pos (PositiveTumbler) — defines Pos(w).
  - ActionPoint (ActionPoint) — minimum-formula underlying TumblerSub's action-point identification.
  - TA0 (WellDefinedAddition) — establishes a ⊕ w ∈ T from Pos(w) and actionPoint(w) ≤ #a.
  - TumblerAdd (TumblerAdd) — constructive component definition and result-length identity #(a ⊕ w) = #w.
  - T3 (CanonicalRepresentation) — concludes a ⊕ w = b from component-wise equality and matching length.
  - NAT-sub (NatPartialSubtraction) — conditional closure for wₖ ∈ ℕ; strict positivity for wₖ ≥ 1; left-inverse for aₖ + (bₖ − aₖ) = bₖ.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality #a < #a + 1 used in Divergence sub-case (ii-a) elimination and again in T1 case (ii) elimination for the pair (a, b).
  - NAT-order (NatStrictTotalOrder) — trichotomy at (#a, #a+1) for Divergence sub-case (ii-a) and for T1 case (ii) elimination at (a, b); at (#a, #b) for Divergence sub-case (ii-b) and TumblerSub sub-case (β); exactly-one trichotomy's disjointness clause ¬(aⱼ < bⱼ ∧ aⱼ = bⱼ) at (aⱼ, bⱼ) converts T1 case (i)'s aⱼ < bⱼ into aⱼ ≠ bⱼ to qualify j for Divergence case (i)'s conjunction; <-to-≤ weakening of bₖ > aₖ.
- *Postconditions:* a ⊕ (b ⊖ a) = b

---

## D2 — DisplacementUnique

Proves that the displacement carrying a to b is unique: any positive tumbler w satisfying a ⊕ w = b must equal the canonical displacement b ⊖ a. The argument applies left cancellation after D1 supplies a second witness, so no two distinct displacements can produce the same target from the same source.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, divergence(a, b) ≤ #a, #a ≤ #b, Pos(w), actionPoint(w) ≤ #a, a ⊕ w = b
- *Depends:*
  - D1 (DisplacementRoundTrip) — supplies the second witness a ⊕ (b ⊖ a) = b.
  - T1 (LexicographicOrder) — gives bₖ > aₖ at the divergence point; strict-to-weak weakening a < b ⇒ b ≥ a.
  - Divergence — case analysis eliminating case (ii); symmetry divergence(a, b) = divergence(b, a).
  - ZPD — zpd(b, a) = divergence(b, a), bridging to k.
  - TumblerSub — carrier membership b ⊖ a ∈ T, component formulas at k, action-point identification, length-pair dispatch at (#b, #a).
  - TumblerAdd — result-length identity #(a ⊕ w) = #w pinning #w = #b.
  - ActionPoint — defining minimum-formula underlying actionPoint(b ⊖ a) = k.
  - TA-Pos (PositiveTumbler) — positivity predicate Pos(·).
  - TA0 (WellDefinedAddition) — well-definedness precondition for both additions.
  - TA-LC (LeftCancellation) — cancellation rule yielding w = b ⊖ a.
  - NAT-sub (NatPartialSubtraction) — conditional closure and strict positivity for (b ⊖ a)ₖ = bₖ − aₖ.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality #a < #a + 1 for sub-case (ii-a).
  - NAT-order (NatStrictTotalOrder) — trichotomy at (#a, #a + 1), (#a, #b), and (aₖ, bₖ).
- *Forward References:*
  - D0 (DisplacementWellDefined) — named in the worked example as the precondition checkpoint; D2 re-derives its conclusions independently.
- *Postconditions:* w = b ⊖ a

---

## Divergence — Divergence

Given two distinct tumblers `a ≠ b`, `divergence(a, b)` returns the exact index where they first differ — either
the position of the first mismatched component (bounded by `k ≤ #a ∧ k ≤ #b` rather than by a primitive binary
minimum), or one past the shorter tumbler's length (`#a + 1` in sub-case (ii-a) with `#a < #b`, else `#b + 1` in
sub-case (ii-b) with `#b < #a`) when all shared components agree but lengths differ; the sub-case is selected by
NAT-order trichotomy. The function is symmetric and always defined for distinct tumblers (exhaustiveness guaranteed
by T3: if neither case applied, the tumblers would be equal).

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, a ≠ b
- *Definition:* (i) if `(∃ k : 1 ≤ k ∧ k ≤ #a ∧ k ≤ #b : aₖ ≠ bₖ)`, then `divergence(a, b)` is the least `k` satisfying `1 ≤ k ∧ k ≤ #a ∧ k ≤ #b ∧ aₖ ≠ bₖ ∧ (A i : 1 ≤ i < k : aᵢ = bᵢ)` (equivalently, the unique such `k`, the universal conjunct being the minimality condition restated); (ii) if `#a ≠ #b ∧ (A i : 1 ≤ i ≤ #a ∧ i ≤ #b : aᵢ = bᵢ)`, then `divergence(a, b) = #a + 1` when `#a < #b` (sub-case (ii-a)) and `divergence(a, b) = #b + 1` when `#b < #a` (sub-case (ii-b)).
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies `a, b ∈ T`, lengths `#a, #b`, and component projections `aₖ, bₖ, aᵢ, bᵢ` as ℕ-valued, making component (in)equalities well-formed.
  - T3 (CanonicalRepresentation) — exhaustiveness: if neither case applies, all shared components agree and `#a = #b`, so `a = b`, contradicting `a ≠ b`.
  - NAT-order (NatStrictTotalOrder) — trichotomy at length pair `(#a, #b)` splits case (ii) into sub-cases (ii-a)/(ii-b); the definition `x ≤ y ⟺ x < y ∨ x = y` and `<`-transitivity together discharge the mixed `≤`-`<` chain showing `i ≤ #a ⇒ i ≤ #b` under `#a < #b` (and the symmetric chain under `#b < #a`) by case-splitting on the unfolded `≤` and applying `<`-transitivity in the strict branch and `=`-substitution in the equality branch.
  - NAT-wellorder (NatWellOrdering) — existence of a least element in the nonempty subset `{k ∈ ℕ : 1 ≤ k ∧ k ≤ #a ∧ k ≤ #b ∧ aₖ ≠ bₖ}` grounds case (i)'s designating description, so "the least such `k`" is non-vacuous.
  - NAT-closure (NatArithmeticClosureAndIdentity) — addition closure instantiated at `(#a, 1)` and `(#b, 1)`, with `1 ∈ ℕ` from the same axiom, well-types case (ii)'s values `#a + 1` and `#b + 1` as ℕ.
- *Postconditions:* `divergence(a, b) ∈ ℕ`; exactly one of case (i) or case (ii) applies; in case (ii), `divergence(a, b) = #a + 1` in sub-case (ii-a) and `divergence(a, b) = #b + 1` in sub-case (ii-b); `divergence(a, b) = divergence(b, a)` for all `a ≠ b`.

---

## GlobalUniqueness — GlobalUniqueness

No two distinct allocation events — whether from the same allocator, sibling allocators, or allocators at different hierarchy depths — ever produce the same address. The proof proceeds by strong induction on allocator tree depth, with five cases ruling out every possible collision scenario. As a consequence, each address belongs to exactly one allocator's domain.

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` produced by distinct allocation events — root initialization or `inc(t, k)` — within a system conforming to T10a. Each address has a producing allocator assigned by the event taxonomy: root base to root; `inc(t, 0)` output to the executing allocator; `inc(t, k')` with `k' > 0` output to the newly created child. The domain prefix of a non-root allocator `A` spawned by `c₀ = inc(t, k')` is `t`; every `a ∈ dom(A)` satisfies `t ≼ a`.
- *Depends:*
  - AllocatedSet (AllocatedSet) — allocation-event taxonomy grounding distinctness.
  - T9 (ForwardAllocation) — `allocated_before(a, b) ⟹ a < b`.
  - T1 (LexicographicOrder) — irreflexivity of `<`.
  - T10 (PartitionIndependence) — distinctness from non-nesting prefixes.
  - T10a (AllocatorDiscipline) — `inc(·, 0)`-only siblings; `k' ∈ {1, 2}`; per-parent uniqueness.
  - T10a.1 (UniformSiblingLength) — every sibling shares the allocator's base length.
  - T10a.3 (LengthSeparation) — descendants at depth `d ≥ 1` have length `≥ γ + d`.
  - T10a.4 (T4Preservation) — every domain prefix is T4-valid.
  - T10a.6 (DomainDisjointness) — for distinct allocators `X ≠ Y`, `dom(X) ∩ dom(Y) = ∅`. Consumed in exhaustiveness's `p₁ = p₂` routing: from the parents' domains containing the shared value, T10a.6 forces `P₁ = P₂` without invoking the inductive hypothesis.
  - T10a.8 (UniformSiblingZeroCount) — base zero count lifts to all siblings.
  - T3 (CanonicalRepresentation) — tumbler equality requires position-wise agreement.
  - T4 (HierarchicalParsing) — clause (iv) `t_{#t} ≠ 0` on T4-valid addresses.
  - TA5 (HierarchicalIncrement) — (b) agreement on `1 ≤ i ≤ #t`; (c) `#inc(t, 0) = #t` with single-position modification; (d) `#inc(t, k') = #t + k'` and zero-separator bookkeeping.
  - TA5-SigValid (TA5-SigValid) — `sig(cₙ) = #cₙ` for T4-valid `cₙ`.
  - Prefix (PrefixRelation) — ≼ definition and `p ≺ q ⟹ #p < #q`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — left and right order compatibility.
  - NAT-cancel (NatAdditionCancellation) — right cancellation `n + m = p + m ⟹ n = p`.
  - NAT-order (NatStrictTotalOrder) — trichotomy, `≤` definition, transitivity, irreflexivity.
  - NAT-addassoc (NatAdditionAssociative) — `(m + n) + p = m + (n + p)`. Consumed in Case 5's sub-case `k'₁ > k'₂` (with `(k'₁, k'₂) = (2, 1)`): instantiated at `(m, n, p) = (#p₁, 1, 1)` to regroup `#p₁ + (1 + 1) = (#p₁ + 1) + 1`, which (combined with T4's *Numerals* definition `2 := 1 + 1`) identifies `#p₁ + 2 = (#p₁ + 1) + 1`, putting the equation `#p₁ + 2 = #p₂ + 1` into the form `(#p₁ + 1) + 1 = #p₂ + 1` so that NAT-cancel can fire on the trailing `+ 1` to yield `#p₂ = #p₁ + 1`.
- *Invariant:* For every pair of addresses `a, b` arising from distinct allocation events in any reachable system state: `a ≠ b`.
- *Postconditions:* (1) Domain Disjointness — for distinct `A₁ ≠ A₂`, `dom(A₁) ∩ dom(A₂) = ∅`. (2) Well-defined owning allocator — each address value belongs to at most one allocator's domain.
- *Proof structure:* Strong induction on allocator tree depth *d*. Claim `U(d)`: all pairs at depth ≤ *d* produce distinct outputs. Base (`d = 0`): sole root, Case 1. Step: Cases 1–5 are self-contained; the `p₁ = p₂` routing invokes T10a.6 (domain disjointness on the parent pair) to establish shared parentage, then applies T10a's per-parent uniqueness.

---

## NAT-addassoc — NatAdditionAssociative

Addition on ℕ is associative: `(m + n) + p = m + (n + p)` for every `m, n, p ∈ ℕ`.
Registered as one of the nine NAT-* axioms inside T0's enumeration (declared
exhaustive); this file states the formal content downstream proofs cite. Membership
in the enumeration is decided by demonstrated downstream consumption — associativity
enters via GlobalUniqueness Case 5's length-collision argument (which regroups
`#p₁ + (1 + 1)` as `(#p₁ + 1) + 1` in the `(k'₁, k'₂) = (2, 1)` extraction);
commutativity is held out because no proof in this ASN reorders two summands, and
its omission is what forces NAT-addcompat and NAT-cancel to state their
left/right clauses independently rather than deriving one from the other.

*Formal Contract:*
- *Axiom:* `(A m, n, p ∈ ℕ :: (m + n) + p = m + (n + p))` (associativity of addition on ℕ).
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set over which the bounded universal `(A m, n, p ∈ ℕ :: (m + n) + p = m + (n + p))` of the associativity axiom ranges.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies the binary operation `+ : ℕ × ℕ → ℕ` whose associativity is here posited, ensuring every sum `m + n`, `n + p`, `(m + n) + p`, and `m + (n + p)` appearing in the axiom is an ℕ-element.

---

## NAT-addbound — NatAdditionDominatesOperands

For every `m, n ∈ ℕ`, the sum `m + n` is bounded below by each of its
operands: `m + n ≥ n` (right dominance) and `m + n ≥ m` (left dominance).
Both sides are stated independently because commutativity of addition
is not enumerated — without `m + n = n + m`, neither form is derivable
from the other. Right dominance follows from NAT-zero (which gives
`0 ≤ m`), NAT-addcompat's right order compatibility (which lifts
`0 ≤ m` to `0 + n ≤ m + n`), and NAT-closure's left additive identity
(which rewrites `0 + n` to `n`). Left dominance follows by the parallel
route through NAT-zero's `0 ≤ n`, NAT-addcompat's left order
compatibility, and NAT-closure's right additive identity.

*Formal Contract:*
- *Consequence:* `(A m, n ∈ ℕ :: m + n ≥ n)` (the sum dominates its right operand) — derived from NAT-zero, NAT-addcompat (right order compatibility), NAT-closure (left additive identity), and NAT-order as shown in the preceding *Right dominance* prose.
- *Consequence:* `(A m, n ∈ ℕ :: m + n ≥ m)` (the sum dominates its left operand) — derived from NAT-zero, NAT-addcompat (left order compatibility), NAT-closure (right additive identity), and NAT-order as shown in the preceding *Left dominance* prose.
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set over which the bounded universals `(A m, n ∈ ℕ :: m + n ≥ n)` and `(A m, n ∈ ℕ :: m + n ≥ m)` of the two dominance Consequences range, and from which the fixed `m, n` of the right- and left-dominance derivations are drawn.
  - NAT-zero (NatZeroMinimum) — supplies the minimality clause `(A k ∈ ℕ :: 0 < k ∨ 0 = k)`, consumed by both the right-dominance and left-dominance derivations.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — supplies the right order compatibility clause `(A m', n', p ∈ ℕ : p ≤ n' : p + m' ≤ n' + m')`, consumed by the right-dominance derivation; and the left order compatibility clause `(A m', n', p ∈ ℕ : p ≤ n' : m' + p ≤ m' + n')`, consumed by the left-dominance derivation.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies the left additive identity `(A k ∈ ℕ :: 0 + k = k)`, consumed by the right-dominance derivation, and the right additive identity `(A k ∈ ℕ :: k + 0 = k)`, consumed by the left-dominance derivation; also underpins the binary operation `+` whose value `m + n` is here bounded below by each operand.
  - NAT-order (NatStrictTotalOrder) — supplies the defining equivalences `a ≤ b ⟺ a < b ∨ a = b` and `a ≥ b ⟺ b ≤ a`, consumed by both derivations.

---

## NAT-addcompat — NatAdditionOrderAndSuccessor

Addition on ℕ is non-strictly monotone with respect to order on either side:
if `p ≤ n` then `m + p ≤ m + n` (left) and `p + m ≤ n + m` (right) for all
`m`. Both forms are stated as axiom clauses so proofs that add a fixed
summand on either side need not tacitly assume commutativity — GlobalUniqueness
Case 5's sub-case `k'₁ < k'₂` uses both placements, left to lift `k'₁ ≤ k'₂` to
`#p₁ + k'₁ ≤ #p₁ + k'₂` and right to lift `#p₁ ≤ #p₂` to
`#p₁ + k'₂ ≤ #p₂ + k'₂`. The clauses deliver only non-strict `≤`; promoting
`#p₁ < #p₂` to the strict `#p₁ + k'₂ < #p₂ + k'₂` requires combining NAT-addcompat
with NAT-cancel (to rule out the equality `#p₁ + k'₂ = #p₂ + k'₂`) and NAT-order
(to weaken `<` to `≤` and to re-strengthen `≤` with non-equality back to
`<`). Additionally, every natural number is strictly less than its
successor: `n < n + 1`. The axiom body cites the non-strict `≤` defined in
NAT-order and the addition/`1`-constants supplied by NAT-closure, so both
foundations appear in the Depends slot.

*Formal Contract:*
- *Axiom:* `(A m, n, p ∈ ℕ : p ≤ n : m + p ≤ m + n)` (left order compatibility); `(A m, n, p ∈ ℕ : p ≤ n : p + m ≤ n + m)` (right order compatibility); `(A n ∈ ℕ :: n < n + 1)` (strict successor inequality).
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set over which the bounded universals `(A m, n, p ∈ ℕ : p ≤ n : m + p ≤ m + n)` and `(A m, n, p ∈ ℕ : p ≤ n : p + m ≤ n + m)` of the two compatibility clauses range, and over which the bounded universal `(A n ∈ ℕ :: n < n + 1)` of the strict successor inequality ranges.
  - NAT-order (NatStrictTotalOrder) — supplies the primitive strict order `<` (used in the strict successor inequality `n < n + 1`) and its non-strict companion `≤` (defined by `m ≤ n ⟺ m < n ∨ m = n`, used in the antecedents `p ≤ n` and the consequents `m + p ≤ m + n` and `p + m ≤ n + m` of both compatibility clauses).
  - NAT-closure (NatArithmeticClosureAndIdentity) — posits `1 ∈ ℕ` and closes ℕ under addition, so every sum `m + p`, `m + n`, `p + m`, `n + m`, and `n + 1` appearing in the axiom lies in ℕ, and the successor inequality `n < n + 1` compares two ℕ-elements.

---

## NAT-cancel — NatAdditionCancellation

Addition on ℕ is cancellative on either side: `m + n = m + p ⟹ n = p`
(left cancellation) and `n + m = p + m ⟹ n = p` (right cancellation), for
every `m, n, p ∈ ℕ`, stated as independent axiom clauses because the
NAT-* axioms of this ASN do not include commutativity of addition on ℕ,
so neither is derivable from the other. Summand absorption
`m + n = m ⟹ n = 0` is recorded as a consequence rather than an axiom:
from `m + n = m` and NAT-closure's right identity `m + 0 = m`, the
rewrite `m + n = m + 0` together with left cancellation at `p := 0`
yields `n = 0`; the mirror form `n + m = m ⟹ n = 0` is the parallel
consequence via right cancellation and NAT-closure's left identity
`0 + m = m`. Cancellation is stated axiomatically alongside the other
NAT-* facts so downstream proofs can cite it directly without appealing
to an implicit "standard properties of ℕ" clause.

*Formal Contract:*
- *Axiom:* `(A m, n, p ∈ ℕ : m + n = m + p : n = p)` (left cancellation); `(A m, n, p ∈ ℕ : n + m = p + m : n = p)` (right cancellation).
- *Consequence:* `(A m, n ∈ ℕ : m + n = m : n = 0)` (summand absorption, posited form) — derived from the left-cancellation axiom and NAT-closure's right additive identity `n + 0 = n` instantiated at `n := m`, as shown in the preceding prose; the mirror form `(A m, n ∈ ℕ : n + m = m : n = 0)` is the parallel consequence, derived from right cancellation and NAT-closure's left additive identity `0 + n = n` instantiated at `n := m`.
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set over which the bounded universals `(A m, n, p ∈ ℕ : m + n = m + p : n = p)` and `(A m, n, p ∈ ℕ : n + m = p + m : n = p)` of the two cancellation axioms range, and over which `(A m, n ∈ ℕ : m + n = m : n = 0)` (and the mirror form) of the summand-absorption Consequence ranges.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies the binary operation `+ : ℕ × ℕ → ℕ` used in all clauses; the right additive identity `(A n ∈ ℕ :: n + 0 = n)`, instantiated at `n := m`, used to rewrite the RHS of `m + n = m` to `m + 0` in the derivation of the posited absorption form from left cancellation; and the left additive identity `(A n ∈ ℕ :: 0 + n = n)`, instantiated at `n := m`, used to rewrite the RHS of `n + m = m` to `0 + m` in the parallel derivation of the mirror form from right cancellation.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` on the right-hand side of the absorption conclusion `m + n = m ⟹ n = 0`.

---

## NAT-card — NatFiniteSetCardinality

The cardinality operator |·| is postulated as a primitive total function on subsets
of every initial segment {j ∈ ℕ : 1 ≤ j ≤ n} ⊆ ℕ (n ∈ ℕ), with codomain ℕ. For such S,
|S| ∈ ℕ is the unique k for which there exists a strictly increasing function
f : {j ∈ ℕ : 1 ≤ j ≤ k} → ℕ with image S (at k = 0 the domain is empty, f is the
empty function, vacuously strictly increasing with image ∅, forcing S = ∅ and
|∅| = 0 without recourse to a convention on empty lists), and |S| ≤ n.
NAT-order's strict-total-order discipline keeps the "strictly increasing function"
predicate well-formed. NAT-card is the foundation
citation for every claim that invokes |·| — in particular the definition
zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}| in T4 and its downstream consumers T4a,
T4b, T4c.

*Formal Contract:*
- *Axiom:* `(A n ∈ ℕ, S : S ⊆ {j ∈ ℕ : 1 ≤ j ≤ n} :: |S|` is the unique `k ∈ ℕ` such that `(E f :: f : {j ∈ ℕ : 1 ≤ j ≤ k} → ℕ ∧ (A i, j : 1 ≤ i < j ≤ k : f.i < f.j) ∧ S = {f.j : 1 ≤ j ≤ k}))` — strictly-increasing-function characterisation, existence-and-uniqueness of `k` carried by "the unique"; `(A n ∈ ℕ, S : S ⊆ {j ∈ ℕ : 1 ≤ j ≤ n} :: |S| ≤ n)` — upper bound.
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set appearing in the outer membership clause `n ∈ ℕ`, in the initial-segment domain `{j ∈ ℕ : 1 ≤ j ≤ n}` whose subsets `S` ranges over, in the cardinality clause `|S| ∈ ℕ` and the inner existential over `k ∈ ℕ`, in the domain `{j ∈ ℕ : 1 ≤ j ≤ k}` and codomain ℕ of the enumerating function `f : {j ∈ ℕ : 1 ≤ j ≤ k} → ℕ`, and in the upper-bound clause `|S| ≤ n` over which `n` is the ℕ-bound.
  - NAT-order (NatStrictTotalOrder) — supplies the strict order `<` (used in the strictly-increasing condition `(A i, j : 1 ≤ i < j ≤ k : f.i < f.j)` on the enumerating function `f`) and the non-strict companion `≤` (used in the upper bound `|S| ≤ n`, in the initial-segment domain `{j ∈ ℕ : 1 ≤ j ≤ n}` bounding `S`, and in the domain `{j ∈ ℕ : 1 ≤ j ≤ k}` of `f`); the strict-total-order discipline (irreflexivity, transitivity, trichotomy `m < n ∨ m = n ∨ n < m`) makes "strictly increasing function" a well-formed predicate on ℕ-valued functions.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ`, the lower bound in the initial segment `{j ∈ ℕ : 1 ≤ j ≤ n}` and in the domain `{j ∈ ℕ : 1 ≤ j ≤ k}` of the enumerating function; combined with NAT-order's `≤` and the outer `n ∈ ℕ`, this grounds `S ⊆ {j ∈ ℕ : 1 ≤ j ≤ n}` with ℕ-typed elements. Also supplies `0 < 1`, which forces `{j ∈ ℕ : 1 ≤ j ≤ 0} = ∅` and so renders the `k = 0` and `n = 0` cases of the axiom well-formed.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` appearing in the empty-domain case `k = 0` (where `{j ∈ ℕ : 1 ≤ j ≤ 0}` is forced empty by `0 < 1`) and in the empty-set cardinality `|∅| = 0`.

---

## NAT-carrier — NatCarrierSet

Posits `ℕ` as a set, the primitive carrier on which the rest of the NAT-* claims (and T0
in turn) operate. Every Cartesian product `ℕ × ℕ`, every membership `x ∈ ℕ`, and every
set-builder `{j ∈ ℕ : ...}` appearing in NAT-order, NAT-zero, NAT-closure, NAT-discrete,
and downstream consumers presupposes this declaration. No further structure — order,
zero, addition, discreteness — is asserted here; those commitments are layered on top by
the dedicated NAT-* claims.

*Formal Contract:*
- *Axiom:* `ℕ` is a set (the carrier of natural numbers).
- *Depends:* (none).

---

## NAT-closure — NatArithmeticClosureAndIdentity

Posits the binary operation `+ : ℕ × ℕ → ℕ` directly on ℕ, asserts
`1 ∈ ℕ`, fixes `0` as a two-sided additive identity: left
(`0 + n = n`) and right (`n + 0 = n`), and asserts the
successor-positivity clause `(A n ∈ ℕ :: 0 < n + 1)` — the
Peano no-predecessor-of-zero condition for the addition-based
successor. The distinctness `0 < 1` of the two named constants
follows as a consequence — the successor-positivity instance at
`n := 0` together with the left-identity rewrite `0 + 1 = 1`. Closure
of ℕ under addition is carried by the signature's codomain commitment.

*Formal Contract:*
- *Axiom:* `+ : ℕ × ℕ → ℕ` (`+` is a binary operation on ℕ); `1 ∈ ℕ` (one is a natural number); `(A n ∈ ℕ :: 0 + n = n)` (left additive identity); `(A n ∈ ℕ :: n + 0 = n)` (right additive identity); `(A n ∈ ℕ :: 0 < n + 1)` (successor positivity — the addition-based successor is never `0`).
- *Consequence:* `0 < 1` (the named constants `0` and `1` are distinct in the strict order) — derived from the successor-positivity clause `(A n ∈ ℕ :: 0 < n + 1)` instantiated at `n := 0`, the left-identity clause `(A n ∈ ℕ :: 0 + n = n)` instantiated at `n := 1`, and substitutivity of `=`, as shown in the preceding prose.
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set appearing as the domain `ℕ × ℕ` and codomain `ℕ` of the signature `+ : ℕ × ℕ → ℕ`, in the membership clause `1 ∈ ℕ`, and over which the bounded quantifiers `(A n ∈ ℕ :: 0 + n = n)`, `(A n ∈ ℕ :: n + 0 = n)`, and `(A n ∈ ℕ :: 0 < n + 1)` of the left-identity, right-identity, and successor-positivity clauses range.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` appearing in the left-identity clause `0 + n = n`, the right-identity clause `n + 0 = n`, the successor-positivity clause `0 < n + 1`, and the *Consequence:* `0 < 1`.
  - NAT-order (NatStrictTotalOrder) — supplies the strict-order primitive `<` used in the successor-positivity clause `0 < n + 1` and in the *Consequence:* `0 < 1`.

---

## NAT-discrete — NatDiscreteness

No natural number lies strictly between `n` and `n + 1`. The axiom form is
`m < n ⟹ m + 1 ≤ n`; the familiar no-interval reformulation
`m ≤ n < m + 1 ⟹ n = m` is recorded as a Consequence rather than a second axiom,
because it is derivable from the axiom body via NAT-order's `≤`-definition,
exactly-one trichotomy, and irreflexivity. The
axiom cites the non-strict `≤` (defined in NAT-order by `m ≤ n ⟺ m < n ∨ m = n`)
and the successor term `m + 1` (grounded by NAT-closure's `1 ∈ ℕ` and
addition-closure), so both appear in the Depends slot.

*Formal Contract:*
- *Axiom:* `(A m, n ∈ ℕ :: m < n ⟹ m + 1 ≤ n)` (discreteness).
- *Consequence:* `(A m, n ∈ ℕ :: m ≤ n < m + 1 ⟹ n = m)` (no-interval form) — derived from the axiom together with NAT-order (the `≤`-definition used to split `m ≤ n`, the exactly-one-trichotomy clause `¬(a < b ∧ b < a)` instantiated at `(m + 1, n)`, and irreflexivity `¬(n < n)` after rewriting `n < m + 1` to `n < n` via `m + 1 = n`) via the forward walk in the preceding prose.
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set appearing in the carrier-side clause `m, n ∈ ℕ` of the bounded universal `(A m, n ∈ ℕ :: m < n ⟹ m + 1 ≤ n)` in the Axiom and likewise of the bounded universal `(A m, n ∈ ℕ :: m ≤ n < m + 1 ⟹ n = m)` in the no-interval Consequence, over which the bound variables `m, n` range before being further restricted by the term-side hypotheses.
  - NAT-order (NatStrictTotalOrder) — supplies the non-strict companion `≤` (defined by `m ≤ n ⟺ m < n ∨ m = n`) used in the axiom's consequent `m + 1 ≤ n` and in the Consequence derivation's case split on `m ≤ n`, the exactly-one-trichotomy clause `¬(a < b ∧ b < a)` instantiated at `(m + 1, n)` in the derivation, and irreflexivity `¬(n < n)` used to discharge the rewritten `n < n`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — posits `1 ∈ ℕ` and closes ℕ under addition, so the successor `m + 1 ∈ ℕ` and the inequalities `m + 1 ≤ n` and `n < m + 1` are comparisons of two ℕ-elements.

---

## NAT-order — NatStrictTotalOrder

The natural numbers are strictly totally ordered by `<`: no number precedes itself (irreflexivity), the order is
transitive, and any two naturals are related by at least one of `<`, `=`, `>` (at-least-one trichotomy). The
three axiom clauses together with indiscernibility of `=` export two Consequences. First, *exactly-one
trichotomy*: for any two naturals, exactly one of less-than, equality, or greater-than holds. The implicational
form `m < n ⟹ m ≠ n` is the mutual-exclusion conjunct `¬(m < n ∧ m = n)` rewritten by the classical
equivalence `¬(A ∧ B) ⟺ (A ⟹ ¬B)` — a derivable restatement of that conjunct, not a separately
exported Consequence; consumers needing the implicational form cite the exactly-one trichotomy bullet. Second,
`≤`-*transitivity*: `m ≤ n ∧ n ≤ p ⟹ m ≤ p`, derived by four-way case analysis on the defining disjunction
`x ≤ y ⟺ x < y ∨ x = y` against `<`-transitivity and indiscernibility of `=`. The non-strict companion `≤`
is defined from `<` directly, and the reverse companions `≥` and `>` are defined as the converses of `≤` and
`<`; all three defined relations inherit the strict-total-order guarantees through their unfoldings.

*Formal Contract:*
- *Axiom:* `< ⊆ ℕ × ℕ` (`<` is a binary relation on ℕ); `(A n ∈ ℕ :: ¬(n < n))` (irreflexivity); `(A m, n, p ∈ ℕ : m < n ∧ n < p : m < p)` (transitivity); `(A m, n ∈ ℕ :: m < n ∨ m = n ∨ n < m)` (at-least-one trichotomy).
- *Definition:* `(A m, n ∈ ℕ :: m ≤ n ⟺ m < n ∨ m = n)`; `(A m, n ∈ ℕ :: m ≥ n ⟺ n ≤ m)`; `(A m, n ∈ ℕ :: m > n ⟺ n < m)`.
- *Consequence:* Exactly-one trichotomy: `(A m, n ∈ ℕ :: (m < n ∨ m = n ∨ n < m) ∧ ¬(m < n ∧ n < m) ∧ ¬(m < n ∧ m = n) ∧ ¬(m = n ∧ n < m))`. The disjunction is the at-least-one axiom clause directly; `¬(m < n ∧ n < m)` follows from transitivity and irreflexivity; `¬(m < n ∧ m = n)` follows by substituting `m = n` into `m < n` via indiscernibility of `=`, rewriting to `m < m` against irreflexivity at `n := m`; `¬(m = n ∧ n < m)` follows by the same substitution applied to `n < m`.
- *Consequence:* `≤`-transitivity: `(A m, n, p ∈ ℕ : m ≤ n ∧ n ≤ p : m ≤ p)`. Unfolding each hypothesis by the definition `x ≤ y ⟺ x < y ∨ x = y` yields four cases. `m < n ∧ n < p` gives `m < p` by `<`-transitivity, hence `m ≤ p`. `m < n ∧ n = p` gives `m < p` by substituting `n = p` into `m < n` via indiscernibility of `=`, hence `m ≤ p`. `m = n ∧ n < p` gives `m < p` by substituting `m = n` into `n < p`, hence `m ≤ p`. `m = n ∧ n = p` gives `m = p` by transitivity of `=`, hence `m ≤ p`.
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set on which the strict order `<` is posited (`< ⊆ ℕ × ℕ`), over which the bounded quantifiers `(A n ∈ ℕ :: ...)`, `(A m, n ∈ ℕ :: ...)`, and `(A m, n, p ∈ ℕ : ... :: ...)` appearing in the irreflexivity, trichotomy, and transitivity clauses range, and on which the non-strict companion `≤` and the reverse companions `≥` and `>` are defined.

---

## NAT-sub — NatPartialSubtraction

Subtraction on ℕ is a partial binary operation defined when the minuend is at least
the subtrahend. The difference `m − n` is the unique natural number satisfying
`(m − n) + n = m` (equivalently `n + (m − n) = m`); right telescoping
`(m + n) − n = m` and left telescoping `(n + m) − n = m` are bundled as additional
axiom clauses — both sides stated independently because commutativity of addition
is not enumerated, so neither telescoping form is derivable from the other.
Strict monotonicity `m ≥ p ∧ n ≥ p ∧ m < n ⟹ m − p < n − p` is exported as a
Consequence rather than an axiom clause, since it derives from the right-inverse
together with NAT-addcompat's right order compatibility and NAT-order's
at-least-one trichotomy with irreflexivity; retaining it as an axiom would
launder the derivation through a non-minimal clause. Strict positivity
`m > n ⟹ m − n ≥ 1` is likewise exported as a Consequence, since lifting
`m − n ≠ 0` to `m − n ≥ 1` leans on NAT-discrete's discreteness of ℕ — a
structural commitment beyond subtraction-structure alone. The per-step citation
convention covers every subtraction step that TumblerSub, TA2, TA3, TA3-strict,
TA4, TA7a, ReverseInverse, D0, D1, and D2 invoke at a divergence point or
round-trip.

*Formal Contract:*
- *Axiom:* `− : {(m, n) ∈ ℕ × ℕ : m ≥ n} → ℕ` (signature: `−` is a partial binary operation on ℕ, single-valued on its domain of definition); `(A m, n ∈ ℕ : m ≥ n : m − n ∈ ℕ)` (conditional closure); `(A m, n ∈ ℕ : m ≥ n : (m − n) + n = m)` (right-inverse characterisation); `(A m, n ∈ ℕ : m ≥ n : n + (m − n) = m)` (left-inverse characterisation); `(A m, n ∈ ℕ :: (m + n) − n = m)` (right telescoping); `(A m, n ∈ ℕ :: (n + m) − n = m)` (left telescoping).
- *Consequence:* `(A m, n, p ∈ ℕ : m ≥ p ∧ n ≥ p ∧ m < n : m − p < n − p)` (strict monotonicity) — derived from the right-inverse clause, NAT-addcompat (right order compatibility), and NAT-order (at-least-one trichotomy, irreflexivity, the `≤`-definition, and the exactly-one-trichotomy Consequence's `¬(x < y ∧ y < x)` clause) as shown in the preceding strict-monotonicity prose.
- *Consequence:* `(A m, n ∈ ℕ : m > n : m − n ≥ 1)` (strict positivity) — derived from the right-inverse clause, NAT-closure (left additive identity and `1 ∈ ℕ`), NAT-order (the `>`/`≤`/`≥` definitions and the exactly-one-trichotomy Consequence's `¬(m < n ∧ m = n)` conjunct at `(m, n) := (n, m)`, contrapositively `n < m ⟹ n ≠ m`), NAT-zero (`(A k ∈ ℕ :: 0 < k ∨ 0 = k)`), and NAT-discrete (discreteness instantiated at `(0, m − n)`) as shown in the preceding strict-positivity prose.
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set appearing in the signature `− : {(m, n) ∈ ℕ × ℕ : m ≥ n} → ℕ` (both as the Cartesian factor `ℕ × ℕ` filtering the domain and as the codomain), in the conditional-closure clause `m − n ∈ ℕ`, and over which the bounded universals of the inverse-characterisation, telescoping, strict-monotonicity, and strict-positivity clauses range.
  - NAT-order (NatStrictTotalOrder) — supplies the strict order `<` and its companions `≤`, `≥`, `>` (defined by `m ≤ n ⟺ m < n ∨ m = n`, `m ≥ n ⟺ n ≤ m`, `m > n ⟺ n < m`), used in the signature's domain condition `{(m, n) ∈ ℕ × ℕ : m ≥ n}` and in the antecedents `m ≥ n` of the conditional-closure and inverse-characterisation clauses; supplies the at-least-one trichotomy axiom and irreflexivity axiom, together with two conjuncts of the exactly-one-trichotomy Consequence — `¬(x < y ∧ y < x)`, against which the strict-monotonicity derivation dispatches the `a = b`, `b < a`-and-`<`, and `b < a`-and-`=` subcases, and `¬(m < n ∧ m = n)` at `(m, n) := (n, m)` (contrapositively `n < m ⟹ n ≠ m`), against which the strict-positivity derivation contradicts the `m − n = 0` case.
  - NAT-closure (NatArithmeticClosureAndIdentity) — posits `1 ∈ ℕ` and closes ℕ under addition, so every sum `(m − n) + n`, `n + (m − n)`, `m + n`, `n + m` appearing in the inverse-characterisation and telescoping clauses is an ℕ-element; additionally supplies the left-identity `(A k ∈ ℕ :: 0 + k = k)`, which the strict-positivity derivation invokes twice — once to collapse `0 + n = m` to `n = m`, once to collapse `0 + 1 ≤ m − n` to `1 ≤ m − n`.
  - NAT-addbound (NatAdditionDominatesOperands) — supplies the right-dominance clause `(A m, n ∈ ℕ :: m + n ≥ n)`, which discharges the conditional-closure precondition `m + n ≥ n` implicit in the right-telescoping clause `(m + n) − n = m`; and the left-dominance clause `(A m, n ∈ ℕ :: m + n ≥ m)`, instantiated at `(m, n) := (n, m)` to yield `n + m ≥ n`, which discharges the conditional-closure precondition implicit in the left-telescoping clause `(n + m) − n = m`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — supplies right order compatibility `(A m, n, p ∈ ℕ : p ≤ n : p + m ≤ n + m)`, instantiated at antecedent `b ≤ a` in the strict-monotonicity derivation's `b < a` case to lift `b ≤ a` through right-addition by `p` to `b + p ≤ a + p`.
  - NAT-zero (NatZeroMinimum) — supplies the axiom clause `(A k ∈ ℕ :: 0 < k ∨ 0 = k)`, instantiated at `k := m − n` in the strict-positivity derivation to lift `m − n ≠ 0` to `0 < m − n` before NAT-discrete fires.
  - NAT-discrete (NatDiscreteness) — supplies `(A m, n ∈ ℕ :: m < n ⟹ m + 1 ≤ n)`, instantiated at `(m, n) := (0, m − n)` in the strict-positivity derivation to yield `0 + 1 ≤ m − n`, which NAT-closure's left-identity reduces to `m − n ≥ 1`.

---

## NAT-wellorder — NatWellOrdering

Every nonempty subset of ℕ contains a least element under `<`. This well-ordering principle is what grounds induction and termination arguments over natural numbers.

*Formal Contract:*
- *Axiom:* `(A S : S ⊆ ℕ ∧ S ≠ ∅ : (E m ∈ S :: (A n ∈ S :: m ≤ n)))` (least-element principle).
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set appearing in the carrier-side clause `S ⊆ ℕ` of the axiom and as the ambient set whose elements `S` ranges over and from which the bound variables `m, n ∈ S` of the inner quantifiers `(E m ∈ S :: ...)` and `(A n ∈ S :: ...)` draw their values (since `S ⊆ ℕ`).
  - NAT-order (NatStrictTotalOrder) — supplies the non-strict companion `≤` (defined by `m ≤ n ⟺ m < n ∨ m = n`), used in the inner quantifier `(A n ∈ S :: m ≤ n)` that characterizes `m` as a least element of `S`.

---

## NAT-zero — NatZeroMinimum

Fixes 0 as the minimum of ℕ via the pair `0 ∈ ℕ` and `(A n ∈ ℕ :: 0 < n ∨ 0 = n)`,
together with the exported *Consequence:* `(A n ∈ ℕ :: ¬(n < 0))`. The consequence
bullet is not delivered by the axiom body alone; it is lifted from the disjunction
under the hypothesis `n < 0` by NAT-order's transitivity `m < n ∧ n < p ⟹ m < p`
(reducing the `0 < n` branch to `0 < 0`) and indiscernibility of `=` (rewriting
`n < 0` under `0 = n` to the same `0 < 0`), both contradicting NAT-order's
irreflexivity `¬(n < n)`; NAT-order is declared in Depends. Supplies `0 ∈ ℕ` for
zero-padded components and literal-zero sites across the ASN, and the disjunction
`0 < n ∨ 0 = n` — combined with `n ≠ 0` to rule out the equality case — to
instantiate NAT-discrete at `m = 0` and derive the inference `n ≠ 0 ⟹ n ≥ 1`.

*Formal Contract:*
- *Axiom:* `0 ∈ ℕ` (zero is a natural number); `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` (every natural number is strictly above or equal to zero).
- *Consequence:* `(A n ∈ ℕ :: ¬(n < 0))` (no natural number is strictly below zero — the minimum reading).
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set appearing in the membership clause `0 ∈ ℕ` and over which the bounded quantifiers `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` of the axiom's second clause and `(A n ∈ ℕ :: ¬(n < 0))` of the *Consequence:* range.
  - NAT-order (NatStrictTotalOrder) — supplies `<` for the axiom's second clause and the irreflexivity `¬(n < n)` + transitivity `m < n ∧ n < p ⟹ m < p` used in the body's derivation of the *Consequence:* bullet `¬(n < 0)`.

---

## NoDeallocation — NoDeallocation

Every state transition in the system is required to leave the allocated address set at least as large as it found it — no operation may remove a previously allocated address. This formalizes the permanence guarantee: once a tumbler is allocated, it remains allocated for all time.

*Formal Contract:*
- *Axiom:* `(A op ∈ Σ, s ∈ 𝒮 :: op(s) defined ⟹ allocated(s) ⊆ allocated(op(s)))`, where Σ is the system's complete (closed) transition vocabulary of partial functions on 𝒮 and 𝒮 is the state space of the allocation system. Frame assumption: Σ is closed.
- *Depends:*
  - AllocatedSet (AllocatedSet) — supplies the transition vocabulary Σ, the state space 𝒮, and the symbol `allocated(s) = ⋃ { domₛ(A) : A activated in s }`.

---

## OrdinalDisplacement — OrdinalDisplacement

δ(n, m) is the canonical "pure depth-m shift" tumbler — a sequence of length m that is zero everywhere except at the last position, which holds n ≥ 1. It acts at depth m and serves as the unit displacement that later shift operations are built from.

*Formal Contract:*
- *Preconditions:* n ∈ ℕ, m ∈ ℕ, n ≥ 1, m ≥ 1
- *Definition:* δ(n, m) = [0, 0, …, 0, n] of length m
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier-set criterion for `δ(n, m) ∈ T`; length operator `#·: T → ℕ` for `#δ(n, m) = m`.
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set appearing in the Precondition membership clauses `n ∈ ℕ` and `m ∈ ℕ`, and as the codomain typing the components of δ(n, m) (the m-th component `n` drawn from the precondition and the leading zeros at positions 1..m−1 drawn from NAT-zero's `0 ∈ ℕ`), discharging T0's commitment that a tumbler's components be ℕ-valued.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the m − 1 leading zero components.
  - NAT-order (NatStrictTotalOrder) — `≤`/`<` unfolding, transitivity of `<`, and the `¬(m < n ∧ m = n)` conjunct of the exactly-one trichotomy, used in `n ≥ 1 ⟹ n ≠ 0`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies the *Consequence* `0 < 1` (derived from its successor-positivity and left-identity clauses) that anchors the `n ≥ 1 ⟹ n ≠ 0` promotion.
  - TA-Pos (PositiveTumbler) — positivity predicate witnessed at i = m.
  - ActionPoint (ActionPoint) — minimum-position formula evaluated against δ's component pattern.
- *Postconditions:* δ(n, m) ∈ T, #δ(n, m) = m, Pos(δ(n, m)), actionPoint(δ(n, m)) = m

---

## OrdinalShift — OrdinalShift

Shifting a tumbler v by n increments only its last component by n, leaving all earlier components unchanged, and is computed as tumbler addition v ⊕ δ(n, #v). The result has the same length and same prefix as v, with the final component strictly increased.

*Formal Contract:*
- *Preconditions:* v ∈ T, n ∈ ℕ, n ≥ 1
- *Definition:* shift(v, n) = v ⊕ δ(n, m) where m = #v
- *Depends:*
  - OrdinalDisplacement (OrdinalDisplacement) — constructs δ(n, m); supplies postconditions `δ(n, m) ∈ T`, `Pos(δ(n, m))`, `actionPoint(δ(n, m)) = m`, `#δ(n, m) = m`.
  - T0 (CarrierSetDefinition) — length operator typing `#·: T → ℕ` and length axiom `#a ≥ 1`; carrier characterisation places vₘ ∈ ℕ.
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set for the Precondition membership clause `n ∈ ℕ`, and as the codomain of T0's length operator `#·: T → ℕ` instantiated at v to type m = #v ∈ ℕ — the depth argument passed to OrdinalDisplacement.
  - TA-Pos (PositiveTumbler) — defines the predicate `Pos(·)` consumed at TA0 precondition (iii).
  - ActionPoint (ActionPoint) — defines `actionPoint(·)` consumed at TA0 precondition (iv).
  - TA0 (WellDefinedAddition) — postconditions `a ⊕ w ∈ T` and `#(a ⊕ w) = #w`.
  - TumblerAdd (TumblerAdd) — piecewise component rule: prefix copy for i < m, advance `vₘ + n` at position m.
  - NAT-zero (NatZeroMinimum) — `(∀ n ∈ ℕ :: 0 ≤ n)` supplies `0 ≤ vₘ`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — right order-compatibility lifts `0 ≤ vₘ` to `vₘ + n ≥ 0 + n`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — additive identity `0 + n = n`.
  - NAT-order (NatStrictTotalOrder) — defining clause `m ≤ n ⟺ m < n ∨ m = n` and transitivity of `<` compose `vₘ + n ≥ n` with `n ≥ 1` into `vₘ + n ≥ 1`.
- *Postconditions:* shift(v, n) ∈ T, #shift(v, n) = #v, shift(v, n)ᵢ = vᵢ for i < #v, shift(v, n)_{#v} = v_{#v} + n ≥ 1

---

## PartitionMonotonicity — PartitionMonotonicity

Within any prefix-delimited partition of the address space, all allocated addresses are totally ordered by T1 consistently with per-allocator allocation order. For sibling sub-partitions with non-nesting prefixes p₁ < p₂, every address extending p₁ precedes every address extending p₂ — the prefix hierarchy imposes a global cross-allocator ordering on top of each allocator's local order.

*Formal Contract:*
- *Preconditions:* A system conforming to T10a (allocator discipline); a partition with prefix `p ∈ T`; up to two child-spawning events from `p`, via `inc(p, k')` with `k' ∈ {1, 2}` as permitted by T10a, each establishing a child prefix whose sibling stream is produced by repeated `inc(·, 0)`.
- *Depends:*
  - T5 (ContiguousSubtrees) — `subtree(p)` is a contiguous T1-interval.
  - T10a (AllocatorDiscipline) — at most two children per `p` via `inc(p, k')` with `k' ∈ {1, 2}`; sibling streams by repeated `inc(·, 0)`.
  - T10a.1 — uniform length of siblings within a stream.
  - T10a.4 — T4-validity preservation, feeds TA5-SigValid.
  - TA5-SigValid (SigOnValidAddresses) — `sig(t) = #t` for valid addresses.
  - TA5 (HierarchicalIncrement) — (a) strict monotonicity of `inc`; (b) `inc(s, k')` with `k' > 0` preserves positions `1..#s`; (c) `inc(·, 0)` preserves length and acts at the significant position; (d) child-base characterisation for `k' ∈ {1, 2}`.
  - T1 (LexicographicOrder) — case (i) divergence-position comparison; case (ii) proper-prefix ordering.
  - T3 (CanonicalRepresentation) — equal-length componentwise agreement implies equality.
  - Prefix (PrefixRelation) — prefix definition and `p ≺ q ⟹ #p < #q`.
  - PrefixOrderingExtension — extends non-nesting prefix order to all descendants.
  - T9 (ForwardAllocation) — per-allocator allocation-order consistency.
- *Postconditions:* (1) For sibling sub-partition prefixes `tᵢ < tⱼ` (with `0 ≤ i < j`) within any single child allocator's stream, and any `a, b ∈ T` with `tᵢ ≼ a` and `tⱼ ≼ b`: `a < b`. (2) Within each sub-partition with prefix `tᵢ`, for any `a, b` allocated by the same allocator: `allocated_before(a, b) ⟹ a < b`. (3) When both param-1 and param-2 children are spawned from `p` (with `c₁ = inc(p, 1)` and `c₂ = inc(p, 2)`), let `reach(c) = ⋃_{s ∈ dom(c)} subtree(s)`. Every address in `reach(c₂)` precedes every address in `reach(c₁)`: every `a ∈ reach(c₁)` has `a_{#p+1} ≥ 1`, every `b ∈ reach(c₂)` has `b_{#p+1} = 0`, both reaches agree with `p` on positions `1..#p`, and T1 case (i) at position `#p + 1` gives `b < a`. Equivalently, for any `b` with `p ≼ b` and `b_{#p+1} = 0`, and any `a` with `p ≼ a` and `a_{#p+1} ≥ 1`: `b < a`.
- *Invariant:* For every reachable system state, the set of allocated addresses within any prefix-delimited partition is totally ordered by T1 consistently with per-allocator allocation order.

---

## Prefix — PrefixRelation

Defines the prefix relation p ≼ q: p's length does not exceed q's and every component of p matches the corresponding component of q. A proper prefix p ≺ q additionally requires p ≠ q, which forces #p < #q strictly — equal-length agreement would make the tumblers identical by T3. The non-prefix notation p ⋠ q abbreviates ¬(p ≼ q). Two derived postconditions are exported: proper-prefix length (p ≺ q ⟹ #p < #q) and reflexivity (∀t ∈ T :: t ≼ t), the latter discharged by NAT-order's ≤-at-equal-arguments step together with equality reflexivity at each index.

*Formal Contract:*
- *Definition:* `p ≼ q` iff `#p ≤ #q ∧ (∀i : 1 ≤ i ≤ #p : qᵢ = pᵢ)`. Proper prefix: `p ≺ q` iff `p ≼ q ∧ p ≠ q`. Non-prefix: `p ⋠ q` iff `¬(p ≼ q)`.
- *Depends:*
  - T0 (CarrierSetDefinition) — length `#p` and component projection `pᵢ` for `p ∈ T`.
  - NAT-order (NatStrictTotalOrder) — `≤` on ℕ for length comparison and index range; defining clause `m ≤ n ⟺ m < n ∨ m = n`.
  - T3 (CanonicalRepresentation) — equal-length tumblers agreeing on all components are equal.
- *Derived postcondition (proper-prefix length):* `p ≺ q ⟹ #p < #q`. From `p ≼ q` conclude `#p ≤ #q`. If `#p = #q`, the component condition `(∀i : 1 ≤ i ≤ #p : qᵢ = pᵢ)` covers all positions of both tumblers, so by T3 `p = q`, contradicting `p ≠ q`. Hence `#p ≠ #q`, and by NAT-order's `≤`-unfolding `#p < #q`.
- *Derived postcondition (reflexivity):* `(∀t ∈ T :: t ≼ t)`. Instantiate the Definition at `p = q = t`: `#t ≤ #t` by NAT-order's `≤`-clause at the equality disjunct; `tᵢ = tᵢ` for `1 ≤ i ≤ #t` by reflexivity of equality. Both conjuncts hold, so `t ≼ t`.

---

## PrefixOrderingExtension — PrefixOrderingExtension

If p₁ < p₂ and neither is a prefix of the other, then every tumbler extending p₁ precedes every tumbler extending p₂ under T1. The divergence position witnessing p₁ < p₂ carries through to all extensions, so the relative order of the two prefix subtrees is fully determined by the prefixes alone.

*Formal Contract:*
- *Preconditions:* `p₁, p₂ ∈ T` with `p₁ < p₂` and `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`; `a, b ∈ T` with `p₁ ≼ a` and `p₂ ≼ b`.
- *Depends:*
  - T1 (LexicographicOrder) — supplies divergence position `k` with `p₁ₖ < p₂ₖ`; re-applied to conclude `a < b`.
  - Prefix (PrefixRelation) — transfers component equality and length bounds from `p₁, p₂` onto `a, b`.
- *Postconditions:* `a < b` under T1.

---

## ReverseInverse — ReverseInverse

Under the conditions that a and w share the same length k, a ≥ w, w is positive, and a has all-zero components before w's action point, subtracting w from a and then adding w back recovers a exactly. This establishes that tumbler subtraction and addition are mutually inverse within this constrained setting.

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `a ≥ w`, `Pos(w)`, `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`, where `k` is the action point of `w`
- *Depends:*
  - TumblerSub — piecewise definition for structure of `y = a ⊖ w`; carrier-membership postcondition `a ⊖ w ∈ T`.
  - TumblerAdd — prefix-copy/advance rule for components of `y ⊕ w`; result-length identity `#(a ⊕ w) = #w`; carrier-membership postcondition `a ⊕ w ∈ T`.
  - TA-Pos (PositiveTumbler) — precondition `Pos(w)`.
  - ActionPoint — action-point function; `wᵢ = 0` for `i < actionPoint(w)`.
  - TA4 (PartialInverse) — yields `(y ⊕ w) ⊖ w = y`.
  - T1 (LexicographicOrder) — case (i) at divergence position `k`; trichotomy on `(y ⊕ w, a)`; irreflexivity.
  - T3 (CanonicalRepresentation) — yields `a = w` in the equality branch.
  - ZPD (ZeroPaddedDivergence) — case-split and minimality clauses keying TumblerSub's branches.
  - TA3-strict (OrderPreservationUnderSubtractionStrict) — applied at both trichotomy cases.
  - T0 (CarrierSetDefinition) — carrier `T`, length `#`, component projection with typing `aᵢ ∈ ℕ`.
  - NAT-sub — conditional closure and strict positivity for `aₖ - wₖ`.
  - NAT-addcompat — right order-compatibility for the strict-promotion chain.
  - NAT-closure — additive identity `0 + wₖ = wₖ`.
  - NAT-cancel — summand absorption ruling out `yₖ + wₖ = wₖ`.
  - NAT-zero — `0 ∈ ℕ` for the zero-valued components and inequalities.
  - NAT-order — trichotomy on length and component pairs; defining clause `m ≤ n ⟺ m < n ∨ m = n`; irreflexivity at `n = 0`.
- *Postconditions:* `(a ⊖ w) ⊕ w = a`

---

## Span — Span

A span is the address-set determined by a pair (start address, length), containing every tumbler from the start up to but not including the result of displacing by the length. The two validity conditions — the length must be positive and its action point must not exceed the depth of the start — are precisely what guarantee the upper bound is a legal tumbler, so any pair satisfying them yields a well-defined span.

*Formal Contract:*
- *Preconditions:* `s ∈ T`, `ℓ ∈ T`, `Pos(ℓ)`, `actionPoint(ℓ) ≤ #s`
- *Definition:* `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}`
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies the carrier `T` and length operator `#`.
  - TA-Pos (PositiveTumbler) — supplies the positivity predicate `Pos(·)`.
  - ActionPoint (ActionPoint) — supplies the action-point function `actionPoint(·)`.
  - TumblerAdd (TumblerAdd) — supplies the operator `⊕`.
  - TA0 (WellDefinedAddition) — licenses `s ⊕ ℓ ∈ T` under the four preconditions via the instantiation `(a, w) := (s, ℓ)`.
  - T1 (LexicographicOrder) — supplies the strict order `<` and the non-strict `≤` bracketing the defining set.

---

## T0(a) — UnboundedComponentValues

For every tumbler and every component position within it, no natural number bounds the values that can appear at that position — there always exists a tumbler of the same depth whose component at that position exceeds any given bound. This establishes that address space within any subtree is inexhaustible, and no finite quota limits allocation beneath any node.

*Formal Contract:*
- *Postcondition:* For every tumbler `t ∈ T` and every component position `i` with `1 ≤ i ≤ #t`, and for every bound `M ∈ ℕ`, there exists `t' ∈ T` with `#t' = #t` that agrees with `t` at all positions except `i`, where `t'.dᵢ > M`.
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier characterisation of T, length operator `#·`, component projection `·ᵢ`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — addition closure `(A m, n ∈ ℕ :: m + n ∈ ℕ)` instantiated at `(M, 1)` with `1 ∈ ℕ` from the same axiom to place `M + 1 ∈ ℕ`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality `(A n ∈ ℕ :: n < n + 1)`.

---

## T0(b) — UnboundedLength

There is no maximum tumbler length — for every natural number n, a tumbler of at least n components exists in T. Together with T0(a), this makes the address space infinite in two independent dimensions: unlimited siblings at any level, and unlimited nesting depth.

*Formal Contract:*
- *Postcondition:* For every `n ∈ ℕ` with `n ≥ 1`, there exists `t ∈ T` with `#t ≥ n`.
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier characterisation of T as finite sequences over ℕ with length ≥ 1, and the length operator `#·`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ`, required to conclude that each witness component `dᵢ = 1` lies in ℕ.
  - NAT-order (NatStrictTotalOrder) — supplies the defining clause `m ≤ n ⟺ m < n ∨ m = n` and the converse `n ≥ n ⟺ n ≤ n`, required to lift `n = n` (reflexivity of equality) to `n ≥ n` and hence discharge `#t ≥ n`.
- *Forward References:*
  - T0(a) (UnboundedComponentValues) — named as the sibling dimension (unlimited siblings at any level) to contrast with the nesting-depth unboundedness established here

T0(b) is what separates the tumbler design from fixed-width addressing. Nelson: "New items may be continually inserted in tumbler-space while the other addresses remain valid." The word "continually" carries the weight — the process of creating new addresses never terminates. Between any two sibling addresses, the forking mechanism can always create children: "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right." Each daughter can have daughters without limit.

The address space is unbounded in two dimensions: T0(a) gives unlimited siblings at any level; T0(b) gives unlimited nesting depth. Nelson calls this "finite but unlimited" — at any moment finitely many addresses exist, but there is no bound on how many can be created: "A span that contains nothing today may at a later time contain a million documents."

Gregory's implementation uses a fixed 16-digit mantissa of 32-bit unsigned integers. When `tumblerincrement` would require a 17th digit, it detects the overflow and terminates fatally; `tumbleradd` silently wraps on digit-value overflow. Both violate T0(b). The comment `NPLACES 16 /* increased from 11 to support deeper version chains */` records that the original bound of 11 was concretely hit — version chains deeper than 3–4 levels caused fatal crashes.

---

## T0 — CarrierSetDefinition

Posits the carrier set T as the set of finite sequences of natural numbers, and
introduces the length operator (#) and component projection (aᵢ) as primitives. Commits
that for each a ∈ T the component projection's index domain is `{j ∈ ℕ : 1 ≤ j ≤ #a}`,
so bounded quantifiers of the form `1 ≤ i ≤ #a` are well-formed over ℕ. Formalizes
nonemptiness as `(A a ∈ T :: 1 ≤ #a)`, drawing `1 ∈ ℕ` from NAT-closure and the
non-strict relation `≤` from NAT-order; without this clause the case
`#a = 0` would leave the index range empty and collapse Pos/Zero predicates to mutual
vacuity on the same tumbler. Posits a comprehension/constructor clause asserting that
every length `p ≥ 1` paired with a component map `r : {j ∈ ℕ : 1 ≤ j ≤ p} → ℕ` is
realised by some `t ∈ T` with `#t = p` and `tᵢ = r(i)`; this is the converse of the
projection clauses and is what discharges membership claims for tumblers constructed
component-wise (e.g., `a ⊕ w ∈ T` in TumblerAdd, and any downstream operator that
builds a tumbler from a length and a component recipe). Commits extensional equality
for T — elements with equal length and pointwise-equal components are identical —
making length-and-component agreement a sufficient condition for tumbler equality
rather than a separately postulated or separately derived property; together with
comprehension, extensionality also guarantees uniqueness of the constructed tumbler.
This is an axiom, not a derivation — it establishes the raw material from which every
other property in the system is built.

*Formal Contract:*
- *Axiom:* `T` is a set (the carrier of tumblers); `#· : T → ℕ` (length operator on T); `(A a ∈ T :: 1 ≤ #a)` (nonemptiness — each tumbler has at least one component); `(A a ∈ T :: i ↦ aᵢ : {j ∈ ℕ : 1 ≤ j ≤ #a} → ℕ)` (component projection signature — for each tumbler `a ∈ T`, the projection `i ↦ aᵢ` is a total, single-valued function from the index domain `{j ∈ ℕ : 1 ≤ j ≤ #a}` into ℕ; in particular `aᵢ ∈ ℕ` at each `i` in the index domain); `(A p ∈ ℕ : p ≥ 1 : (A r : {j ∈ ℕ : 1 ≤ j ≤ p} → ℕ :: (E t ∈ T :: #t = p ∧ (A i ∈ ℕ : 1 ≤ i ≤ p : tᵢ = r(i)))))` (comprehension — every nonempty finite sequence of naturals, presented as a length `p ≥ 1` and a component map `r` from the index domain `{j ∈ ℕ : 1 ≤ j ≤ p}` into ℕ, is represented in T by some `t` with `#t = p` and `tᵢ = r(i)`); `(A a, b ∈ T : #a = #b ∧ (A i ∈ ℕ : 1 ≤ i ≤ #a : aᵢ = bᵢ) : a = b)` (extensionality — tumblers with equal length and pointwise-equal components are identical).
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set appearing as the codomain of the length operator `#· : T → ℕ`, as the codomain of the component-projection signature `i ↦ aᵢ : {j ∈ ℕ : 1 ≤ j ≤ #a} → ℕ` and the comprehension's component map `r : {j ∈ ℕ : 1 ≤ j ≤ p} → ℕ`, in the index-domain comprehensions `{j ∈ ℕ : 1 ≤ j ≤ #a}` and `{j ∈ ℕ : 1 ≤ j ≤ p}`, over which the bounded quantifier `(A p ∈ ℕ : p ≥ 1 : ...)` of the comprehension axiom ranges, and over which the inner index variable `i` of the comprehension's `(A i ∈ ℕ : 1 ≤ i ≤ p : tᵢ = r(i))` and the extensionality axiom's `(A i ∈ ℕ : 1 ≤ i ≤ #a : aᵢ = bᵢ)` ranges before being further restricted by the term-side range.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` for the lower bound of the nonemptiness clause `1 ≤ #a` and for the lower bound `1` in the index domain `{j ∈ ℕ : 1 ≤ j ≤ #a}` of the component-projection signature.
  - NAT-order (NatStrictTotalOrder) — supplies the non-strict relation `≤` on ℕ appearing in the nonemptiness clause `1 ≤ #a` and in the index-domain bound `1 ≤ j ≤ #a` of the component-projection signature.

---

## T1 — LexicographicOrder

Defines a strict total order on T by lexicographic comparison: two tumblers are compared component-by-component left to right, with the first disagreement deciding the outcome, and a shorter tumbler preceding any proper extension of itself. The order is irreflexive, satisfies trichotomy, and is transitive — making any two tumblers comparable and giving the "tumbler line" its linear structure on which spans, link endsets, and content reference all depend.

*Formal Contract:*
- *Definition:* `a < b` iff `∃ k ∈ ℕ` with `1 ≤ k` and `(A i ∈ ℕ : 1 ≤ i < k : aᵢ = bᵢ)` and either (i) `k ≤ #a ∧ k ≤ #b ∧ aₖ < bₖ`, or (ii) `k = #a+1 ≤ #b`.
- *Abbreviations:* `a ≤ b` abbreviates `a < b ∨ a = b`; `a ≥ b` abbreviates `b ≤ a`; `a > b` abbreviates `b < a`.
- *Depends:*
  - T0 (CarrierSetDefinition) — length `#a` and component projection `aₖ` for `a ∈ T`.
  - T3 (CanonicalRepresentation, this ASN) — bridge between component-level agreement and tumbler equality; Case 1 concludes `a = b`, Cases 2 and 3 conclude `a ≠ b`.
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set over which the bound variable `k` of the existential quantifier `∃ k ∈ ℕ` and the bound variable `i` of the universal quantifier `(A i ∈ ℕ : 1 ≤ i < k : aᵢ = bᵢ)` in the *Definition* range.
  - NAT-order (NatStrictTotalOrder) — irreflexivity, trichotomy, and transitivity of `<` on ℕ; `≤`-defining clause `m ≤ n ⟺ m < n ∨ m = n` for composing strict with non-strict bounds.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` and the signature `+ : ℕ × ℕ → ℕ`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality `n < n + 1`.
  - NAT-cancel (NatAdditionCancellation) — right cancellation at `1`, used in sub-case (ii, ii) to pass from `m + 1 = n + 1` to `m = n`.
  - NAT-discrete (NatDiscreteness) — forward direction `m < n ⟹ m + 1 ≤ n`, used contrapositively in Case 1 to rule out `m < n` and `n < m` from the exhaustion-shape negations `¬(m + 1 ≤ n) ∧ ¬(n + 1 ≤ m)` and in part (c) Case `k₂ < k₁` case-(ii) branch to obtain `k₂ ≤ m` from `k₂ < m + 1`.
  - NAT-wellorder (NatWellOrdering) — least-element principle, invoked in part (b) within the branch where at least one divergence position exists, to define the first divergence position `k`.
- *Postconditions:* (a) Irreflexivity — `(A a ∈ T :: ¬(a < a))`. (b) Trichotomy — `(A a,b ∈ T :: (a < b ∨ a = b ∨ b < a) ∧ ¬(a < b ∧ a = b) ∧ ¬(a < b ∧ b < a) ∧ ¬(a = b ∧ b < a))`. (c) Transitivity — `(A a,b,c ∈ T : a < b ∧ b < c : a < c)`.

---

## T10 — PartitionIndependence

If two tumblers p₁ and p₂ are incomparable — neither is a prefix of the other — then every address beneath p₁ is distinct from every address beneath p₂, with no communication or central registry required. This is the formal basis for coordination-free allocation: the prefix hierarchy partitions address space so that independent owners of disjoint subtrees can baptize new addresses simultaneously without any risk of collision.

*Formal Contract:*
- *Preconditions:* `p₁, p₂ ∈ T` with `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`; `a, b ∈ T` with `p₁ ≼ a` and `p₂ ≼ b`.
- *Postconditions:* `a ≠ b`.
- *Depends:*
  - Prefix — definition of `≼` as componentwise agreement.
  - T0 (CarrierSetDefinition) — tumbler length `#p` and component projection `pᵢ`.
  - NAT-order (NatStrictTotalOrder) — at-least-one trichotomy (for the `m ≤ n` vs `m > n` case split), the reverse-companion definition `m > n ⟺ n < m` and `≤`-definition `n ≤ m ⟺ n < m ∨ n = m` (for deriving `n ≤ m` from `m > n` in Case 2 to satisfy the length clause of `p₂ ≼ p₁`), and the `≤`-transitivity Consequence (for chaining `k ≤ m ≤ #a` and `k ≤ n ≤ #b`).
  - NAT-wellorder (NatWellOrdering) — well-definedness of `min` on nonempty subsets of ℕ.
  - T3 (CanonicalRepresentation) — tumblers differing in any component are distinct.

Nelson: "The owner of a given item controls the allocation of the numbers under it." No central allocator is needed. No coordination protocol is needed. The address structure itself makes collision impossible.

Nelson: "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." Baptism is the mechanism by which ownership domains are established — the owner of a number creates sub-numbers beneath it, and those sub-numbers belong exclusively to the owner.

---

## T10a-N — AllocatorDisciplineNecessity

T10a's restriction of the sibling stream to inc(·, 0) is not merely sufficient but necessary. Relaxing it to admit inc(·, k) with any k > 0 produces a co-sibling pair where the first output is a strict prefix of the second, directly falsifying T10a.2 (NonNestingSiblingPrefixes); since the construction is parametric in k, every relaxation witnesses a failing pair.

*Formal Contract:*
- *Preconditions:* T10a's sibling restriction is relaxed to permit `inc(·, k)` with any `k ≥ 0` in the sibling stream. `t₀ ∈ T`; `k > 0`; the allocator emits `t₁ = inc(t₀, 0)` and `t₂ = inc(t₁, k)` as co-sibling outputs.
- *Postconditions:* `t₁ ≼ t₂` with `t₁ ≠ t₂`, falsifying T10a.2 (NonNestingSiblingPrefixes). The `k = 0` sibling restriction is therefore necessary for T10a.2.
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier `T`, length `#·`.
  - NAT-zero (NatZeroMinimum) — supplies `0 ≤ k` to instantiate NAT-discrete at `m = 0`.
  - NAT-discrete (NatDiscreteness) — no-interval form at `m = 0` with `n = k` yields `k ≥ 0 + 1`, which NAT-closure's left identity rewrites to `k ≥ 1`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` (the symbol in `k ≥ 1`) and the left-identity clause `0 + n = n` (instantiated at `n = 1`) used to rewrite NAT-discrete's conclusion `k ≥ 0 + 1` to `k ≥ 1`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — order-compatibility lifts `1 ≤ k` to `#t₁ + 1 ≤ #t₁ + k`; strict successor gives `#t₁ < #t₁ + 1`.
  - NAT-order (NatStrictTotalOrder) — chains the strict inequality and weakens `<` to `≤` for Prefix.
  - TA5 (HierarchicalIncrement) — (d) gives `#t₂ = #t₁ + k`; (b) gives agreement on positions `1..#t₁`.
  - Prefix (PrefixRelation) — converts agreement plus `#t₁ ≤ #t₂` into `t₁ ≼ t₂`.
  - T10a (AllocatorDiscipline) — the discipline whose relaxation is considered.
  - T10a.2 (NonNestingSiblingPrefixes) — the clause falsified by the constructed pair.

---

## T10a.1 — UniformSiblingLength

All siblings produced by a single allocator share the same tumbler length as the base address. Because sibling production uses only inc(·, 0), which preserves length by TA5, the entire sibling stream is length-uniform.

*Formal Contract:*
- *Precondition:* Allocator with base address `t₀`, producing siblings by `inc(·, 0)`.
- *Postcondition:* `(A n ≥ 0 : #tₙ = #t₀)`.
- *Depends:*
  - T10a (AllocatorDiscipline) — supplies base address `t₀` and sibling recurrence `tₙ₊₁ = inc(tₙ, 0)`.
  - TA5 (HierarchicalIncrement), postcondition (c) — `#inc(t, 0) = #t`, the per-step length preservation.

---

## T10a.2 — NonNestingSiblingPrefixes

Distinct outputs of a single allocator are prefix-incomparable — neither sibling is a prefix of the other. Because T10a.1 guarantees all siblings share the same length, a prefix relation between distinct siblings would require unequal lengths, yielding a contradiction; the result supplies the within-allocator non-nesting condition that T10 requires.

*Formal Contract:*
- *Precondition:* `tᵢ`, `tⱼ` are distinct siblings from the same allocator (`tᵢ ≠ tⱼ` as tumblers).
- *Postcondition:* `tᵢ ⋠ tⱼ ∧ tⱼ ⋠ tᵢ`.
- *Depends:*
  - T10a (AllocatorDiscipline) — sibling production uses only `inc(·, 0)`, fixing the "same allocator" regime.
  - T10a.1 (UniformSiblingLength) — `#tᵢ = #tⱼ`.
  - Prefix (PrefixRelation) — positional-agreement conjunct of `≼`.
  - T3 (CanonicalRepresentation) — `#a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ) ≡ a = b`.

---

## T10a.3 — LengthSeparation

Child allocator outputs are strictly longer than any output of their parent allocator, with length increasing additively at each spawning step. Along any lineage the cumulative length offset equals the sum of the spawning increments, so outputs at different nesting depths always differ in length and therefore never coincide (by T3).

*Formal Contract:*
- *Precondition:* Parent allocator with sibling length `γ`; `t` is a parent sibling (`#t = γ` by T10a.1); child spawned via `inc(t, k')` with `k' ∈ {1, 2}`.
- *Postcondition:* All child outputs have length `γ + k' > γ`; no child output equals any parent sibling. Descendant at depth `d` along a lineage with parameters `k'₁, …, k'_d` has output length `γ + k'₁ + … + k'_d ≥ γ + d`; cumulative length is strictly increasing with depth, so outputs at different depths never collide. Local monotonicity: for ancestor A at depth `d_A` and descendant B at depth `d_B > d_A` on the same lineage, `#output(B) − #output(A) = k'_{d_A+1} + … + k'_{d_B} ≥ d_B − d_A ≥ 1`.
- *Depends:*
  - T10a (AllocatorDiscipline) — restricts child-spawning to `inc(·, k')` with `k' ∈ {1, 2}`.
  - T10a.1 (UniformSiblingLength) — uniform length `γ` for parent siblings and `γ + k'₁ + … + k'_d` for depth-`d` outputs.
  - TA5 (HierarchicalIncrement) — (c) `#inc(t, 0) = #t`; (d) `#inc(t, k') = #t + k'` for `k' > 0`.
  - T0 (CarrierSetDefinition) — carrier is ℕ; types all length terms, sums, and depth differences for NAT-* instantiations.
  - NAT-order (NatStrictTotalOrder) — supplies the companion definitions `m > n ⟺ n < m` and `m ≥ n ⟺ n ≤ m` (presenting the child-length conclusion as `γ + k' > γ` in paragraph 2, and the local-monotonicity intermediates `k'_{d_A+1} + … + k'_{d_B} ≥ d_B − d_A ≥ 1` and `#output(B) − #output(A) ≥ 1` in `≥`-form); transitivity of `<` together with the mixed `<`-`≤` chain `m < n ∧ n ≤ p ⟹ m < p` (consumed at paragraph 2's chaining step to combine NAT-addcompat's `γ < γ + 1` with `γ + 1 ≤ γ + k'` into `γ < γ + k'`, and again in local monotonicity to combine `#output(A) < #output(A) + 1` with `#output(A) + 1 ≤ #output(A) + (k'_{d_A+1} + … + k'_{d_B})` into `#output(A) < #output(A) + (k'_{d_A+1} + … + k'_{d_B})`); `≤`-transitivity (consumed at the running-sum induction's inductive step to chain `i + 1 ≤ i + k'_{i+1}` with `i + k'_{i+1} ≤ k'₁ + … + k'_{i+1}` — read off via the `≥`/`≤` companion from `k'₁ + … + k'_{i+1} ≥ i + k'_{i+1}` — into `i + 1 ≤ k'₁ + … + k'_{i+1}`, i.e., `k'₁ + … + k'_{i+1} ≥ i + 1`).
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor `n < n + 1` and order-compatibility of addition.
  - NAT-addassoc (NatAdditionAssociative) — iterated regrouping of the left-associated accumulation `γ + k'₁ + … + k'_{d_B}` at the depth-`d_A` boundary identifies `(γ + k'₁ + … + k'_{d_A}) + (k'_{d_A+1} + … + k'_{d_B}) = γ + k'₁ + … + k'_{d_B}`, i.e., `#output(A) + (k'_{d_A+1} + … + k'_{d_B}) = #output(B)`; this premise is consumed at two sites in the local-monotonicity derivation — the strict-inequality step lifts NAT-addcompat's `#output(A) < #output(A) + (k'_{d_A+1} + … + k'_{d_B})` to `#output(A) < #output(B)`, and the left-telescoping step rewrites `(#output(A) + (k'_{d_A+1} + … + k'_{d_B})) − #output(A) = k'_{d_A+1} + … + k'_{d_B}` as `#output(B) − #output(A) = k'_{d_A+1} + … + k'_{d_B}`.
  - NAT-sub (NatPartialSubtraction) — conditional closure (places `d_B − d_A ∈ ℕ`), strict positivity `m > n ⟹ m − n ≥ 1` (lifts `d_B > d_A` to `d_B − d_A ≥ 1` without recourse to a `[0, 1)`-collapse), and left telescoping `(n + m) − n = m` (instantiated at `n = #output(A), m = k'_{d_A+1} + … + k'_{d_B}` to compute the exact difference; right-telescoping is avoided because the NAT-addassoc regrouping delivers the sum in the order `#output(A) + (k'_{d_A+1} + … + k'_{d_B})`, matching left-telescoping's premise without an unstated commutativity step).
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` (so NAT-discrete can be instantiated at `m = 0`) and the minimum reading `¬(n < 0)`; together with NAT-discrete, sharpens the spawning-parameter fact `k' > 0` (from `k' ∈ {1, 2}`) to `1 ≤ k'` — the form NAT-addcompat's left order-compatibility consumes at each spawning step, including the per-step `1 ≤ k'_i` reused in the lineage induction and local-monotonicity derivation.
  - NAT-discrete (NatDiscreteness) — discreteness of ℕ: `m < n ⟹ m + 1 ≤ n`; instantiated at `m = 0` to sharpen `k' > 0` to `1 ≤ k'`, feeding every NAT-addcompat left order-compatibility lift across the spawning parameters `k', k'_i` (paragraphs 2–5).
  - T3 (CanonicalRepresentation) — tumblers of different lengths are distinct.

---

## T10a.4 — T4PreservationUnderDiscipline

Every address produced anywhere in an allocator tree conforming to T10a satisfies T4 (HierarchicalParsing). The root base address satisfies T4 by the initialization constraint, and TA5a (IncrementPreservesT4) propagates the invariant through every inc(·, 0) and inc(·, k') step, so T4 compliance holds at all depths by induction.

*Formal Contract:*
- *Preconditions:* Allocator tree conforming to T10a; root base address satisfies T4.
- *Postconditions:* For every allocator `A` in the tree and every `t ∈ dom(A)`, `t` satisfies T4. In particular, every address produced at every depth satisfies T4.
- *Proof structure:* Induction on allocator tree depth with strengthened hypothesis — every `t ∈ dom(A)` is T4-valid, not only `A`'s base. Base: root's sibling chain via TA5a `k = 0`. Step: child's base `inc(t, k')` is T4-valid because the strengthened hypothesis supplies `t` T4-valid at the spawning point `t = spawnPt(A) ∈ dom(parent(A))`, TA5a gives preservation for `k' ∈ {1, 2}`, and T10a's `zeros(t) ≤ 2` guard fires at that same `t` when `k' = 2`; the child's sibling chain then propagates T4 via TA5a `k = 0`.
- *Depends:*
  - T10a (AllocatorDiscipline) — root-initialization constraint; spawning rule `spawnPt(A) ∈ dom(parent(A))` and child-base `inc(spawnPt(A), spawnParam(A))`; runtime precondition `zeros(t) ≤ 2` at `k' = 2` stated on the spawning point `t`.
  - T4 (HierarchicalParsing) — invariant preserved by induction.
  - TA5a (IncrementPreservesT4) — per-step preservation: `inc(·, 0)` and `inc(·, 1)` preserve T4 unconditionally on T4-valid inputs; `inc(·, 2)` preserves T4 under `zeros(t) ≤ 2` at the input `t`.

---

## T10a.5 — CrossAllocatorIncomparability

Any two allocators that are not in an ancestor-descendant relationship produce mutually prefix-incomparable outputs — no output of one can be a prefix of any output of the other. The argument traces to the lowest common ancestor: the two spawning paths diverge at sibling outputs of that ancestor, and length separation (T10a.3) together with T4-based component analysis (TA5-SigValid) shows the divergence is irreconcilable. This alone delivers T10's non-nesting precondition at the domain prefixes of every non-ancestor-descendant allocator pair, disjoint from T10a.2's within-allocator guarantee.

*Formal Contract:*
- *Precondition:* Allocators X and Y conforming to T10a, not in an ancestor-descendant relationship.
- *Postcondition:* For all x ∈ dom(X) and y ∈ dom(Y): x ⋠ y ∧ y ⋠ x.
- *Depends:*
  - T10a — at-most-once child-spawning constraint; k' ∈ {1, 2}.
  - T10a.1 — uniform sibling length.
  - T10a.3 — length separation across depths.
  - T10a.4 — T4 preservation (enables TA5-SigValid).
  - T4 (HierarchicalParsing) — TA5-SigValid precondition.
  - T3 — distinct same-length tumblers diverge at some position.
  - TA5 — postconditions (b), (c), (d).
  - TA5-SigValid — sig = length for T4-valid addresses.
  - T0 (CarrierSetDefinition) — fixes carrier as ℕ.
  - NAT-closure (NatArithmeticClosureAndIdentity) — addition closure with `1 ∈ ℕ` from the same axiom places `n + 1 ∈ ℕ` for the `+1` steps.
  - NAT-zero (NatZeroMinimum) — lower bound `0 ≤ n`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor `n < n + 1`, left order-compatibility `p ≤ n ⟹ m + p ≤ m + n`, and right order-compatibility `p ≤ n ⟹ p + m ≤ n + m` (the right form is consumed in the LCA-existence argument: NAT-zero's `0 ≤ d` is lifted at `m = 1` to `0 + 1 ≤ d + 1`, which NAT-closure's left-identity reduces to `1 ≤ d + 1`, supplying the `d + 1 ≥ 1` precondition of NAT-sub's strict monotonicity at `p = 1`).
  - NAT-addassoc (NatAdditionAssociative) — regroups `#s + (1 + 1) = (#s + 1) + 1`, which (combined with T4's *Numerals* definition `2 := 1 + 1`) identifies `#s + 2 = (#s + 1) + 1` so that NAT-addcompat's strict successor at `n = #s + 1` reads as `#s + 1 < #s + 2`. Consumed at three sites: (i) the *All outputs in C_Y's subtree at position #s + 1* paragraph, where the inline derivation `#s + 2 = #s + (1 + 1) = (#s + 1) + 1` produces `#s + 1 < #s + 2 = #(inc(s, 2))` and discharges positional inheritance's `p < m` precondition at `(p, m) = (#s + 1, #s + 2)` for C_Y's base; (ii) the closure paragraph's range chain `#s + 1 ≤ #s + 2 ≤ #y` that places position `#s + 1` within `#y`'s domain (the right inequality from T10a.1 on C_Y's outputs and T10a.3 on deeper descendants gives `#y ≥ #s + 2`; the left inequality lifts the same `#s + 1 < #s + 2` via NAT-order's `≤`-definition); (iii) the *Descendants of C_X at position #s + 1* paragraph's child-base length bound `#s + 1 + k'' ≥ #s + 2` for `k'' ∈ {1, 2}`, where at `k'' = 1` NAT-addassoc's `(#s + 1) + 1 = #s + 2` delivers the equality and at `k'' = 2` NAT-addcompat's left order-compatibility at `(m, p, n) = (#s + 1, 1, 2)` lifts `1 ≤ 2` to `(#s + 1) + 1 ≤ (#s + 1) + 2`, with NAT-addassoc rewriting the LHS to `#s + 2`.
  - NAT-order (NatStrictTotalOrder) — supplies the companion definitions `m > n ⟺ n < m` and `m ≥ n ⟺ n ≤ m` that present Case 2's inductive step's chain `(tₙ)_{#s+1} + 1 > (tₙ)_{#s+1} ≥ 0` (with NAT-addcompat's strict successor at `n = (tₙ)_{#s+1}` read in `>` form and NAT-zero's lower bound `0 ≤ (tₙ)_{#s+1}` read in `≥` form) and the output-value conclusion `(tₙ)_{#s+1} + 1 ≥ 1` (propagated to `x_{#s+1} ≥ 1` for outputs in C_X's subtree) in `>` / `≥` form; the mixed `≤`-`<` transitivity `m ≤ n ∧ n < p ⟹ m < p` (a consequence of `<`-transitivity together with `≤`'s defining disjunction `m ≤ n ⟺ m < n ∨ m = n` — splitting the left hypothesis, the strict branch chains via `<`-transitivity and the equality branch substitutes via indiscernibility of `=`), instantiated at `m = 0`, `n = (tₙ)_{#s+1}`, `p = (tₙ)_{#s+1} + 1`, consumes NAT-zero's lower bound `0 ≤ (tₙ)_{#s+1}` as the left arm and NAT-addcompat's strict-successor conclusion `(tₙ)_{#s+1} < (tₙ)_{#s+1} + 1` as the right arm to obtain `0 < (tₙ)_{#s+1} + 1`, the strict-positivity precondition consumed by NAT-discrete (at `m = 0`) to rule out `0 ≤ (tₙ)_{#s+1} + 1 < 1` and force `(tₙ)_{#s+1} + 1 ≥ 1`.
  - NAT-discrete (NatDiscreteness) — non-zero ⇒ ≥ 1 on ℕ; forward direction `d < δ ⟹ d + 1 ≤ δ` consumed in the LCA-existence argument to lift `d ≠ δ` (combined with `d ≤ δ`) into `d + 1 ≤ δ` for every `d ∈ D`.
  - NAT-sub (NatPartialSubtraction) — conditional closure `δ ≥ 1 ⟹ δ − 1 ∈ ℕ`, right-inverse `(δ − 1) + 1 = δ`, right-telescoping `(d + 1) − 1 = d`, and strict monotonicity at `p = 1`. Consumed in the LCA-existence argument to construct `δ − 1 ∈ ℕ`, derive `δ − 1 < δ` (right-inverse fed into NAT-addcompat's strict successor), and case-split `d + 1 ≤ δ` into `d + 1 = δ` (right-telescoping yields `d = δ − 1`) and `d + 1 < δ` (strict monotonicity yields `d < δ − 1`) — placing `δ − 1 ∈ U` and contradicting δ's minimality in U.
  - NAT-wellorder (NatWellOrdering) — least-element principle: every nonempty `S ⊆ ℕ` has a least element. Applied in the LCA-existence argument to the upper-bound set `U = {u ∈ ℕ : (A d ∈ D :: d ≤ u)}` of the depth-set `D = {depth(A) : A ∈ Anc(X) ∩ Anc(Y)}`; the resulting least element δ is placed in D itself by TA5-SIG-pattern minimality contradiction, making `δ = max(D)` and locating the LCA C as the unique element of `Anc(X) ∩ Anc(Y)` at depth δ.
  - Prefix — definition of ≼.
- *Forward References:*
  - T10 (PartitionIndependence) — consumes this claim's postcondition as its non-nesting precondition `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`.

---

## T10a.6 — DomainDisjointness

Any two distinct allocators have disjoint domains — no tumbler address can belong to more than one allocator's output stream. The proof splits into two cases: ancestor–descendant pairs are separated by strict length differences, while non-ancestor–descendant pairs are separated by prefix-incomparability combined with Prefix's reflexivity postcondition. As a corollary, whenever two addresses share an allocator, that allocator is uniquely determined by the pair.

*Formal Contract:*
- *Precondition:* `X` and `Y` are distinct allocators conforming to T10a.
- *Postcondition:* `dom(X) ∩ dom(Y) = ∅`; equivalently, for every `a` there is at most one `A ∈ 𝒯` with `a ∈ dom(A)`, so `same_allocator(a, b)` determines the witnessing `A` uniquely.
- *Depends:*
  - T10a (AllocatorDiscipline) — allocator identity criterion, tree relations, per-allocator `dom(·)`.
  - T10a.1 (UniformSiblingLength) — per-domain uniform length `γ_X`.
  - T10a.3 (LengthSeparation) — strict inequality `γ_Y > γ_X` for ancestor/descendant.
  - T10a.5 (CrossAllocatorIncomparability) — prefix-incomparability across non-lineage allocators.
  - Prefix (PrefixRelation) — reflexivity `t ≼ t`.
- *Forward References:*
  - T10a.7 (EnumerationInjectivity) — elaborates the witness-uniqueness consequence: supplies within-allocator index injectivity so that the enumeration indices `(i, j)` with `a = tᵢ, b = tⱼ` are single-valued once T10a.6 has fixed the witnessing allocator.

---

## T10a.7 — EnumerationInjectivity

Within a single allocator, the sequential enumeration of its domain is injective — distinct indices always produce distinct addresses. Because each step strictly increases under the tumbler order, the full enumeration is strictly monotone, making the index of any address a single-valued function of that address. Together with T10a.6, this makes the enumeration indices of any same-allocator pair uniquely determined, which is required for T9's allocated_before predicate to be well-defined.

*Formal Contract:*
- *Precondition:* Allocator A conforming to T10a, with domain `dom(A) = {tₙ : n ≥ 0}` where `t₀` is the base address and `tₙ₊₁ = inc(tₙ, 0)`.
- *Postcondition:* The map `n ↦ tₙ` is injective: `(A m, n ≥ 0 : m ≠ n : tₘ ≠ tₙ)`. Equivalently, `(A m, n ≥ 0 : m < n : tₘ < tₙ)`.
- *Depends:*
  - T10a (AllocatorDiscipline) — supplies the enumeration `tₙ₊₁ = inc(tₙ, 0)`, instantiated at index `m` in the base of L and at index `m + d` in the step of L.
  - TA5 (HierarchicalIncrement), postcondition (a) — strict monotonicity `inc(tₙ, 0) > tₙ` at the base and step of L.
  - T1 (LexicographicOrder), postcondition (c) — transitivity of `<` chains the IH `tₘ < t_{m+d}` with `t_{m+d} < t_{m+(d+1)}` at the inductive step of L.
  - T1 (LexicographicOrder), postcondition (a) — irreflexivity of `<` converts `tₘ < tₙ` to `tₘ ≠ tₙ` at the close of the overall argument.
  - NAT-order (NatStrictTotalOrder) — trichotomy on ℕ indices resolves `m ≠ n` into `m < n ∨ n < m`; the `≤` and `>` definitions lift `m < n` to `n ≥ m` and `n > m` respectively, discharging NAT-sub's preconditions in the closing.
  - NAT-sub (NatPartialSubtraction) — strict positivity at `(n, m)` (under `n > m`) delivers `n − m ≥ 1`; left-inverse characterisation at `(n, m)` (under `n ≥ m`) delivers `m + (n − m) = n`; together these supply the positive gap `d = n − m ≥ 1` and the index identity `m + d = n` at which lemma L is instantiated in the closing. Used once, at the boundary between the corollary and its lemma — not inside the induction.
  - NAT-addassoc (NatAdditionAssociative) — at the inductive step of L, rewrites `m + (d + 1) = (m + d) + 1` so that T10a's enumeration rule at index `m + d` (which produces `t_{(m+d)+1}`) matches the induction goal indexed at `m + (d + 1)`.
  - NAT-wellorder (NatWellOrdering) — least-element principle on ℕ, the source of the induction principle on `d ≥ 1` underwriting lemma L's proof; without it the base case (`d = 1`) and inductive step (`d → d + 1`) would not extend to `(A d ≥ 1 :: L(d))`.

---

## T10a.8 — UniformSiblingZeroCount

All siblings produced by a single allocator share the same zero count as the base address. Each inc(·, 0) step modifies
only the terminal component (TA5(b), TA5(c), TA5-SigValid, T10a.4). The pre-increment value at position sig(tₙ) = #tₙ
is strictly positive on ℕ by the per-step chain T4 (non-zero) + T0 (carrier ℕ) + NAT-zero (lower bound 0 ≤ tᵢ) +
NAT-discrete (rules out 0 ≤ tᵢ < 1 under tᵢ ≠ 0). The +1 step preserves positivity by the parallel chain
NAT-closure (addition closure instantiated at (n, 1) with 1 ∈ ℕ places n + 1 ∈ ℕ) + NAT-zero + NAT-addcompat (strict successor inequality n < n + 1), matching the per-step
citation convention TA5a's case k = 0 already follows for the structurally identical sibling step. Hence no position
enters or leaves the zero set.

*Formal Contract:*
- *Precondition:* Allocator with base address `t₀`, producing siblings by `inc(·, 0)`, conforming to T10a.
- *Postcondition:* `(A n ≥ 0 : zeros(tₙ) = zeros(t₀))`.
- *Depends:*
  - T10a (AllocatorDiscipline) — supplies `t₀` and restricts siblings to `tₙ₊₁ = inc(tₙ, 0)`.
  - T10a.4 (T4PreservationUnderDiscipline) — every sibling satisfies T4.
  - T4 (HierarchicalParsing) — field-segment constraint gives `(tₙ)_{#tₙ} ≠ 0`.
  - T0 (CarrierSetDefinition) — fixes the carrier as ℕ.
  - NAT-zero (NatZeroMinimum) — lower bound `0 ≤ (tₙ)ᵢ` on ℕ.
  - NAT-discrete (NatDiscreteness) — converts non-zero to strictly positive on ℕ.
  - NAT-closure (NatArithmeticClosureAndIdentity) — `(tₙ)_{sig(tₙ)} + 1 ∈ ℕ`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality `n < n + 1`.
  - NAT-order (NatStrictTotalOrder) — `>` companion definition `m > n ⟺ n < m` reads `0 < (tₙ)_{sig(tₙ)} + 1` as `(tₙ₊₁)_{sig(tₙ)} > 0`; transitivity chains NAT-addcompat's `(tₙ)_{sig(tₙ)} < (tₙ)_{sig(tₙ)} + 1` with NAT-zero's `0 ≤ (tₙ)_{sig(tₙ)}` to give `0 < (tₙ)_{sig(tₙ)} + 1`; irreflexivity `¬(n < n)` (equivalently, the exactly-one trichotomy clause `¬(m < n ∧ m = n)` derived from it) lifts `(tₙ₊₁)_{sig(tₙ)} > 0` to `(tₙ₊₁)_{sig(tₙ)} ≠ 0`, which excludes position `sig(tₙ)` from the primed zero-index subset in the zero-index-set equality argument.
  - TA5 (HierarchicalIncrement) — TA5(b)/(c) restrict the step to a single position with length preserved.
  - TA5-SigValid (SigOnValidAddresses) — `sig(tₙ) = #tₙ` on T4-valid addresses.

---

## T10a — AllocatorDiscipline

Allocators must produce sibling addresses exclusively by shallow increment inc(·,0), and may spawn child allocators only via a single deep increment with k'∈{1,2} subject to TA5a's zero-count bound zeros(t) ≤ 2 at k'=2 (k'=1 preserves T4 unconditionally on T4-valid t). This discipline ensures all outputs have controlled prefix relationships, prevents length collisions within and across allocators, and preserves the T4 structural invariant throughout the entire allocator tree by induction.

*Formal Contract:*
- *Definitions:*
  - *Allocator tree* `𝒯`: the set of allocators induced by T10a, consisting of a root together with every allocator reachable by finite iteration of the child-spawning rule. Each non-root `A` carries a spawning triple `(parent(A), spawnPt(A), spawnParam(A))` with `parent(A) ∈ 𝒯`, `spawnPt(A) ∈ dom(parent(A))`, `spawnParam(A) ∈ {1, 2}`; `A`'s base address is `inc(spawnPt(A), spawnParam(A))`. The root's base is the T4-valid address fixed by the initialization constraint.
  - *Identity:* `X = Y` iff both are the root, or both are non-root with identical spawning triples.
  - *Derived relations:* `child`, `depth`, `ancestor`, `descendant`, *ancestor-descendant relationship*, *param-1 child* (spawnParam = 1), *param-2 child* (spawnParam = 2), *sibling allocator* (distinct children of a common parent).
  - *Domain:* `dom(A) = {tₙ : n ≥ 0}` where `t₀` is `A`'s base and `tₙ₊₁ = inc(tₙ, 0)`. Child-spawning outputs are excluded from the parent's domain and become the initial element of the child's domain.
  - *Same allocator:* `same_allocator(a, b) ≡ ∃A ∈ 𝒯 : a ∈ dom(A) ∧ b ∈ dom(A)`.
- *Axiom:* The root's base address satisfies T4. Allocators produce sibling outputs exclusively by `inc(·, 0)`; child-spawning uses one `inc(·, k')` with `k' ∈ {1, 2}`, subject to `zeros(t) ≤ 2` when `k' = 2`. Each `(t, k')` pair yields at most one child-spawning event.
- *Depends:*
  - T4 (HierarchicalParsing) — supplies the field-segment constraint (T4-validity) and the `zeros(·)` function. T10a's axiom requires the root's base to satisfy T4 and imposes `zeros(t) ≤ 2` at child-spawning step `k' = 2`; T10a.4 establishes that every conforming allocator output satisfies T4.
  - TA5 (HierarchicalIncrement) — supplies the `inc` operator, positional agreement under `k > 0` (TA5(b)), length preservation under `k = 0` (TA5(c)), strict order `inc(t, k) > t` (TA5(a)), and length increment by `k` (TA5(d)). Threaded through every consequence and the necessity argument.
  - TA5a (IncrementPreservesT4) — supplies the T4-preservation envelope: unconditional under `inc(·, 0)` and `inc(·, 1)` on T4-valid inputs, conditional under `inc(·, 2)` when `zeros(t) ≤ 2`. Drives T10a.4's induction step.
  - Prefix (PrefixRelation) — supplies the prefix relation `≼` and its positional-agreement clause. Used in T10a.2's collapse of sibling prefix-relation to equality and in T10a.5's closure step contradicting `x ≼ y` from a divergence position.
  - T3 (CanonicalRepresentation) — collapses equal-length positional agreement to identity. Used in T10a.2 to rule out distinct equal-length siblings being prefix-related, and in T10a.5's base case to extract a divergence position from `tₓ ≠ tᵧ` at common length `m`.
  - T0 — fixes the carrier ℕ as the index domain for tumbler positions and the spawn parameter `k' ∈ {1, 2}`. Underpins ℕ-typed quantification throughout.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — supplies the strict successor `n < n + 1`, left order-compatibility on `<`, and right order-compatibility `p ≤ n ⟹ p + m ≤ n + m`. Used in T10a.3's length-separation chain (`#t < #t + 1 ≤ #t + k'`), in T10a-N's necessity argument, in T10a.8's positivity propagation, and in T10a.5's LCA-existence argument (right order-compatibility lifts NAT-zero's `0 ≤ d` at `m = 1` to `0 + 1 ≤ d + 1`, supplying NAT-sub strict monotonicity's `d + 1 ≥ 1` precondition).
  - NAT-zero (NatZeroMinimum) — supplies `0 ≤ n` for `n ∈ ℕ`. Used in T10a.3 to lift `k' > 0` to `1 ≤ k'`, in T10a.5 / T10a.8 to ground positivity in the divergence and zero-count arguments, and in T10a.5's LCA-existence to ground `0 ≤ d` for the right-order-compatibility lift to `1 ≤ d + 1`.
  - NAT-discrete (NatDiscreteness) — sharpens `n > 0` to `n ≥ 1` on ℕ; supplies the forward direction `d < δ ⟹ d + 1 ≤ δ`. Used in T10a.3 and T10a-N to obtain `1 ≤ k'` from `k' > 0`, in T10a.8 to derive `(tₙ)_{#tₙ} ≥ 1`, and in T10a.5's LCA-existence to lift `d ≠ δ` (combined with `d ≤ δ`) into `d + 1 ≤ δ` for every `d ∈ D`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies addition closure (`n + 1 ∈ ℕ`) and the literal `1 ∈ ℕ`. Used in T10a.5 and T10a.8 to keep successor-positivity arguments inside ℕ, and in T10a.5's LCA-existence to collapse `0 + 1 = 1` (left-identity) at two sites — discharging `0 + 1 ≤ δ ⟹ 1 ≤ δ` and `0 + 1 ≤ d + 1 ⟹ 1 ≤ d + 1`.
  - NAT-sub (NatPartialSubtraction) — supplies conditional closure `δ ≥ 1 ⟹ δ − 1 ∈ ℕ`, right-inverse `(δ − 1) + 1 = δ`, right-telescoping `(d + 1) − 1 = d`, and strict monotonicity at `p = 1`. Used in T10a.5's LCA-existence: closure produces `δ − 1 ∈ ℕ`; the right-inverse fed into NAT-addcompat's strict successor delivers `δ − 1 < δ`; right-telescoping handles the `d + 1 = δ` branch (`d = δ − 1`) and strict monotonicity handles the `d + 1 < δ` branch (`d < δ − 1`); together they place `δ − 1 ∈ U` and contradict δ's minimality in U.
  - NAT-wellorder (NatWellOrdering) — least-element principle: every nonempty `S ⊆ ℕ` has a least element. Used in T10a.5's LCA-existence: applied to the upper-bound set `U = {u ∈ ℕ : (A d ∈ D :: d ≤ u)}` of the depth-set `D = {depth(A) : A ∈ Anc(X) ∩ Anc(Y)}`, it delivers a least element δ; the TA5-SIG-pattern minimality contradiction places δ ∈ D, making `δ = max(D)` and locating the LCA P as the unique element of `Anc(X) ∩ Anc(Y)` at depth δ.
  - TA5-SigValid — fixes `sig(t) = #t` for T4-valid tumblers. Used in T10a.5 to identify which positions `inc(·, 0)` modifies and in T10a.8 to localize the zero-count argument to position `#tₙ`.
  - T1 (LexicographicOrder) — supplies irreflexivity (T1(a)) and transitivity (T1(c)) of `<`. Used in T10a.7 to derive injectivity of `n ↦ tₙ` from successor strict-positivity.
  - NAT-order (NatStrictTotalOrder) — supplies trichotomy on ℕ and the `≤`-defining clause `m ≤ n ⟺ m < n ∨ m = n`. Used in T10a.7 to resolve `m ≠ n` into `m < n ∨ n < m` for the injectivity argument, and in T10a.5's LCA-existence to split `d ≤ δ ∧ d ≠ δ` into `d < δ` (driving NAT-discrete's forward direction) and to split `d + 1 ≤ δ` into the `d + 1 = δ` and `d + 1 < δ` branches that NAT-sub dispatches.
- *Postconditions:*
  - T10a.1 (Uniform sibling length): For every allocator with base `b`, all sibling outputs `a` satisfy `#a = #b`.
  - T10a.2 (Non-nesting sibling prefixes): For all siblings `a, b` from the same allocator, `same_allocator(a, b) ∧ a ≠ b → a, b` prefix-incomparable.
  - T10a.3 (Length separation): For every child allocator spawned by `inc(·, k')` with `k' ∈ {1, 2}` from a parent with base length `m`, all child outputs `c` satisfy `#c = m + k'`; across `d` nesting levels the separation is `m + k'₁ + … + k'_d`. For any proper ancestor-descendant pair `(A, B)` — pairs where A is an ancestor of B with A ≠ B (whence `depth(A) < depth(B)`; the converse fails, as allocators in independent subtrees can satisfy `depth(A) < depth(B)` without any ancestor-descendant relationship) — `∀b ∈ dom(B), ∀a ∈ dom(A) : #b > #a`.
  - T10a.4 (T4 preservation): Every output of a conforming allocator satisfies T4.
  - T10a.5 (Cross-allocator prefix-incomparability): For allocators X, Y not in an ancestor-descendant relationship, for all `x ∈ dom(X)`, `y ∈ dom(Y)`, `x ⋠ y ∧ y ⋠ x`. (The ancestor-descendant case carries only a narrower nesting fact, not universal pairwise comparability between domains: at each spawning event `(tᵢ, k')` with `tᵢ ∈ dom(parent)`, `tᵢ ≺ c` for every `c` in the spawned child's domain and, transitively, for every `c` in any descendant allocator's domain whose chain of spawning events passes through `tᵢ`. Elements of `dom(parent)` other than the spawn point `tᵢ` need not be prefix-comparable to descendant domain elements.)
  - T10a.6 (Domain disjointness): For distinct X, Y, `dom(X) ∩ dom(Y) = ∅`. Ancestor-descendant case by T10a.1 + T10a.3; non-ancestor-descendant case by T10a.5 + Prefix reflexivity. Witness-uniqueness corollary: `same_allocator(a, b)` determines the witnessing A uniquely.
  - T10a.7 (Enumeration injectivity): For every allocator A, `n ↦ tₙ` is injective.
  - T10a.8 (Uniform sibling zero count): For every allocator with base `b`, all siblings `a` satisfy `zeros(a) = zeros(b)`.
  - T10a-N (Necessity of sibling restriction): Under the relaxed rule, `a₁ = inc(b, 0)` and `a₂ = inc(a₁, k')` with `k' > 0` satisfy `a₁ ≺ a₂`, falsifying T10a.2. The sibling restriction `k = 0` is necessary for T10a.2. The `k' ∈ {1, 2}` bound, at-most-once constraint, and root initialization serve T4 preservation and child-prefix uniqueness respectively.

---

## T12 — SpanWellDefinedness

For any (s, ℓ) satisfying the preconditions of Definition (Span), the set span(s, ℓ) has three
theorem-level properties: the endpoint s⊕ℓ exists in T (TA0), the set is non-empty because s is
always a member (TA-strict), and the set is order-convex under T1 — any tumbler lying between
two members is itself a member.

*Formal Contract:*
- *Preconditions:* `(s, ℓ)` satisfies the preconditions of Definition (Span) — equivalently, `s ∈ T`, `ℓ ∈ T`, `Pos(ℓ)`, and `actionPoint(ℓ) ≤ #s`.
- *Depends:*
  - Span (Span) — fixes the symbol `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}` and the preconditions on `(s, ℓ)`.
  - T0 (CarrierSetDefinition) — supplies the carrier `T` and length operator `#`.
  - T1 (LexicographicOrder) — supplies reflexivity of `≤`, transitivity of `<` via T1(c), and the `< ∨ =` decomposition.
  - TA0 (WellDefinedAddition) — supplies `s ⊕ ℓ ∈ T` from the four preconditions.
  - TA-strict (StrictIncrease) — supplies `s ⊕ ℓ > s` from the four preconditions.
- *Forward References:*
  - T5 (PrefixContiguity) — named as the downstream claim establishing contiguity for prefix-defined sets, a distinct property deferred from T12
- *Postconditions:* (a) `s ⊕ ℓ ∈ T`. (b) `s ∈ span(s, ℓ)`. (c) `span(s, ℓ)` is order-convex under T1: for all `a, c ∈ span(s, ℓ)` and `b ∈ T`, `a ≤ b ≤ c` implies `b ∈ span(s, ℓ)`.

---

## T2 — IntrinsicComparison

The tumbler order from T1 is computable from the two tumblers alone, consulting no external state — only their component
sequences and lengths. The comparison terminates after examining a number of component pairs bounded by both #a and #b,
making it both intrinsic and bounded.

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` — two well-formed tumblers (finite sequences over ℕ with `#a ≥ 1` and `#b ≥ 1`, per T0).
- *Depends:*
  - T0 (CarrierSetDefinition) — length operator `#·` and component-projection `·ᵢ`.
  - T1 (LexicographicOrder) — the order relation being shown computable; case (i) and case (ii) dispatch the two scan outcomes.
  - T3 (CanonicalRepresentation) — bridges componentwise agreement with `m = n` to `a = b` in the equality sub-case.
  - NAT-wellorder (NatWellOrdering) — least-element principle establishing that `k` is the first divergence position in Case 1.
  - NAT-order (NatStrictTotalOrder) — trichotomy at `(aₖ, bₖ)` and at `(m, n)`; transitivity in the mixed form `i ≤ p ∧ p < q ⟹ i ≤ q` for shared-range identification in Case 2.
  - NAT-discrete (NatDiscreteness) — forward direction `m < n ⟹ m + 1 ≤ n`, used in Case 2 sub-cases `m < n` and `n < m` to bridge the case hypothesis to the arithmetic witness `k = m + 1 ≤ n` (resp. `k = n + 1 ≤ m`) required by T1 case (ii); its no-interval Consequence also supplies the reverse inclusion `i < m + 1 ⟹ i ≤ m` (resp. `i < n + 1 ⟹ i ≤ n`) of the agreement-domain identification in those same sub-cases.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality `m < m + 1` (and symmetrically `n < n + 1`), used in Case 2 sub-cases `m < n` and `n < m` to identify the scan's agreement domain `{i : 1 ≤ i ≤ m}` (resp. `{i : 1 ≤ i ≤ n}`) with the `{i : 1 ≤ i < k}` domain required by T1 case (ii) at `k = m + 1` (resp. `k = n + 1`); it supplies the forward inclusion `i ≤ m ⟹ i < m + 1` (resp. `i ≤ n ⟹ i < n + 1`) via NAT-order transitivity, which NAT-discrete's forward/no-interval directions cannot produce without circularity.
- *Postconditions:* (a) The ordering among `a` and `b` under T1 is determined. (b) The number of component pairs examined is at most `#a` and at most `#b`. (c) The only values consulted are `{aᵢ : 1 ≤ i ≤ #a}`, `{bᵢ : 1 ≤ i ≤ #b}`, `#a`, and `#b`.
- *Frame:* No external data structure is read or modified — the comparison is a pure function of the two tumblers.

---

## T3 — CanonicalRepresentation

Tumbler equality is exactly component-wise sequence equality — two tumblers are equal if and only if they have the same length and identical values at every position. No normalization, quotient, or external identification is imposed; the raw component sequences must be literally identical.

*Formal Contract:*
- *Postcondition:* Tumbler equality is sequence equality: `a = b ⟺ #a = #b ∧ (A i ∈ ℕ : 1 ≤ i ≤ #a : aᵢ = bᵢ)`.
- *Depends:*
  - T0 (CarrierSetDefinition) — the extensionality clause `(A a, b ∈ T : #a = #b ∧ (A i ∈ ℕ : 1 ≤ i ≤ #a : aᵢ = bᵢ) : a = b)` supplies the forward direction; length `#·` and component projection `·ᵢ` supply the reverse direction via Leibniz's law.

---

## T4 — HierarchicalParsing

Valid address tumblers encode a four-level containment hierarchy (node, user, document,
element). T4 is purely definitional: its Definition slot fixes the
*zero-count* `zeros(t)`, names a position `i` a *field separator* iff `tᵢ = 0`, names the
*field segments* of `t` as the maximal contiguous sub-sequences of field-component positions
delimited by the separators, and defines the *T4-valid* predicate as the conjunction
`zeros(t) ≤ 3 ∧ no two zeros adjacent ∧ t₁ ≠ 0 ∧ t_{#t} ≠ 0` (the last three collectively
the *field-segment constraint*). T4 does not assert which `t ∈ T` satisfy the predicate,
nor how many field segments arise for a given `t` — downstream consumers (T4a's
segment-non-emptiness equivalence, T4b's projection domains, T4c's level subdomain) carry
T4-validity as an explicit precondition and derive the segment structure from it. T4a proves the field-segment constraint equivalent to every
field segment of `t` being non-empty under the bound `zeros(t) ≤ 3`. NAT-closure grounds the numerals `2 := 1 + 1` and `3 := 2 + 1`
in ℕ so that `zeros(t) ≤ 3` compares two ℕ-elements. NAT-card axiomatizes the cardinality
operator `|·|` on subsets of every initial segment `{1, …, n} ⊆ ℕ` with codomain ℕ,
grounding the definition `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|` so that `zeros(t) ∈ ℕ`;
T4's body — where both `|·|` and T0's tumbler-length `#·` are in use — carries the
disambiguation that `|·|` acts on sets while `#·` acts on sequences. As a Consequence,
`(A t ∈ T : zeros(t) ≤ 3 : zeros(t) ∈ {0, 1, 2, 3})` —
universally quantified by the bound alone, since the field-segment constraint of full
T4-validity plays no role in the derivation (which uses only the bound, NAT-zero's
`0 ≤ zeros(t)`, NAT-order's trichotomy, NAT-discrete, and NAT-closure's left additive
identity). Every T4-valid tumbler discharges the hypothesis a fortiori via the first
conjunct of T4-valid, so the four-case split `zeros(t) ∈ {0, 1, 2, 3}` collectively covers
every T4-valid tumbler; downstream consumers with hypothesis `zeros(t) ≤ 3` only (T4a
directly; T4b transitively) cite the Consequence at their use-site without a meta-argument
about which derivation steps are needed.

*Formal Contract:*
- *Definition:*
  - *Zero-count.* `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|`; the index set `{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}` is a subset of `{1, …, #t} ⊆ ℕ` (T0's index domain), so NAT-card applies at `n = #t` and yields `zeros(t) ∈ ℕ`.
  - *Field separator.* A position `i` of `t` is a *field separator* iff `tᵢ = 0`; the remaining positions are *field components*.
  - *Field segment.* The *field segments* of `t` are the maximal contiguous sub-sequences of field-component positions, delimited by the field separators. The terminology names what a segment *is*; the equivalence between every-segment-non-empty and the field-segment constraint is proved in T4a, not stipulated here.
  - *Numerals.* `2 := 1 + 1` and `3 := 2 + 1`; closure of ℕ under addition (NAT-closure), applied successively to `1 ∈ ℕ`, gives `2 ∈ ℕ` and then `3 ∈ ℕ`.
  - *T4-valid predicate.* `t ∈ T` is *T4-valid* iff `zeros(t) ≤ 3 ∧ (A i : 1 ≤ i < #t : ¬(tᵢ = 0 ∧ tᵢ₊₁ = 0)) ∧ t₁ ≠ 0 ∧ t_{#t} ≠ 0`; the last three conjuncts are collectively the *field-segment constraint*.
- *Consequence:* `(A t ∈ T : zeros(t) ≤ 3 : zeros(t) ∈ {0, 1, 2, 3})` — for every `t ∈ T` with `zeros(t) ≤ 3`, `zeros(t) ∈ {0, 1, 2, 3}` (equivalently `zeros(t) = 0 ∨ zeros(t) = 1 ∨ zeros(t) = 2 ∨ zeros(t) = 3`). Derived in the *Exhaustion* paragraph above.
- *Preconditions:* `t ∈ T`.
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies the tumbler carrier T (so the precondition `t ∈ T` and the body's component accesses `tᵢ`, `tᵢ₊₁` are meaningful), the tumbler length `#·`, the component-projection signature, and the index domain `{1, …, #t}`.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` appearing in the zero-count definition's filter `tᵢ = 0` (within `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|`), in the T4-valid predicate's clauses `tᵢ = 0`, `tᵢ₊₁ = 0`, `t₁ ≠ 0`, and `t_{#t} ≠ 0`, and in the Consequence's enumeration `zeros(t) ∈ {0, 1, 2, 3}`; also supplies the disjunction `(A n ∈ ℕ :: 0 < n ∨ 0 = n)`, instantiated at `n := zeros(t)` in the *Exhaustion* paragraph and combined with NAT-order's exactly-one trichotomy to forbid `zeros(t) < 0`.
  - NAT-discrete (NatDiscreteness) — supplies the strict-to-`+1` promotion `m < n ⟹ m + 1 ≤ n`, instantiated at `(i, #t)` for the upper bound `i + 1 ≤ #t` of the `tᵢ₊₁` well-definedness, at `(0, i + 1)` for the conversion `0 < i + 1 ⟹ 0 + 1 ≤ i + 1` in that same derivation, and at `(0, zeros(t))`, `(1, zeros(t))`, `(2, zeros(t))` in the *Exhaustion* induction.
  - NAT-order (NatStrictTotalOrder) — supplies `<` on ℕ with its companion `≤` (`m ≤ n ⟺ m < n ∨ m = n`) and the exactly-one trichotomy Consequence.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ`, closure of ℕ under addition (grounding the numerals `2 := 1 + 1` and `3 := 2 + 1`), the left additive identity `(A n ∈ ℕ :: 0 + n = n)`, and the successor-positivity axiom `(A n ∈ ℕ :: 0 < n + 1)` consumed at `n := i` to discharge the lower bound `1 ≤ i + 1` of the `tᵢ₊₁` well-definedness derivation.
  - NAT-card (NatFiniteSetCardinality) — axiomatizes `|·|` on subsets of every initial segment `{1, …, n} ⊆ ℕ` with codomain ℕ.
- *Forward References:*
  - T4a (SyntacticEquivalence) — proves downstream the equivalence between the field-segment constraint and every-segment-non-empty; T4 defers to it rather than stipulating the biconditional here.
  - T4c (LevelDetermination) — the single definitional site for the address-kind labels (node/user/document/element) that T4's zero-count levels admit.

---

## T4a — SyntacticEquivalence

The three positional conditions from T4 (no adjacent zeros, nonzero first and last
components) are logically equivalent to the condition that every field segment of
the tumbler is non-empty. This records the bridge between T4's positional form and
the semantic reading that every present field contributes at least one component.
NAT-closure grounds the numerals `2 := 1 + 1` and `3 := 2 + 1` in ℕ, and the sums
`s_i + 1`, `s_i + 2`, `#t + 1` appearing in the proof's sentinel and inequality
manipulations. NAT-sub's right-telescoping `(m + n) − n = m`, at `m = #t, n = 1`,
reduces the last-segment upper bound `s_{k+1} − 1 = (#t + 1) − 1` to `#t`, so the
last segment is the ℕ-interval `[s_k + 1, #t]` and its non-emptiness is the `+1`
form `s_k + 1 ≤ #t` — the form NAT-discrete outputs directly from
`s_k < #t ⟹ s_k + 1 ≤ #t`, avoiding a subtractive detour. T4a cites T0's
Axiom's nonemptiness clause `(A a ∈ T :: 1 ≤ #a)` at `a := t` directly for
`#t ≥ 1`, underwriting the `k = 0` branches. NAT-card's enumeration characterisation of `|·|` identifies the length
`k` of the strictly increasing enumeration `s₁ < s₂ < … < s_k` of the zero-index
subset with `zeros(t)`. T4's Exhaustion Consequence — universally quantified by the bound alone as
`(A t ∈ T : zeros(t) ≤ 3 : zeros(t) ∈ {0, 1, 2, 3})`, with hypothesis matching
T4a's precondition pointwise — instantiates at the local `t` to pin
`k ∈ {0, 1, 2, 3}` in the setup's enumeration directly, closing the citation
chain for the four-case presentation that follows.

*Formal Contract:*
- *Consequence:* The three positional conditions (i) `(A i : 1 ≤ i < #t : ¬(tᵢ = 0 ∧ tᵢ₊₁ = 0))`, (ii) `t₁ ≠ 0`, (iii) `t_{#t} ≠ 0` hold if and only if every field segment of `t` is non-empty (SyntacticEquivalence) — derived from T4's field-segment clauses, T0's non-degeneracy of `t ∈ T`, NAT-order's strict total order (specifically `<`-transitivity), `≤`-definition, and `≤`-transitivity Consequence, NAT-discrete's strict-to-`+1` promotion and no-interval Consequence, NAT-addcompat's strict successor inequality `n < n + 1`, NAT-addassoc's regrouping `(m + n) + p = m + (n + p)`, NAT-zero's first Axiom clause `0 ∈ ℕ`, NAT-closure's numerals and closure under addition, NAT-sub's right-telescoping clause, and NAT-card's enumeration characterisation of `|·|`, as shown in the preceding Forward and Reverse derivations; recorded as a Consequence rather than an Axiom because the biconditional is proved from T4's axioms and the foundation dependencies, not posited.
- *Preconditions:* `t ∈ T` with `zeros(t) ≤ 3`.
- *Depends:*
  - T0 (CarrierSetDefinition) — fixes the carrier as ℕ and supplies the Axiom's nonemptiness clause `(A a ∈ T :: 1 ≤ #a)`.
  - NAT-discrete (NatDiscreteness) — supplies the strict-to-`+1` promotion `m < n ⟹ m + 1 ≤ n` and the no-interval Consequence `m ≤ n < m + 1 ⟹ n = m`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — supplies the strict successor inequality `(A n ∈ ℕ :: n < n + 1)`.
  - NAT-addassoc (NatAdditionAssociative) — supplies `(A m, n, p ∈ ℕ :: (m + n) + p = m + (n + p))`, instantiated at `(m, n, p) := (s_i, 1, 1)` in the Reverse interior-segment derivation to rewrite the NAT-discrete output `(s_i + 1) + 1` as `s_i + (1 + 1) = s_i + 2` (with `2 := 1 + 1` from NAT-closure), discharging the equational step that would otherwise conflate the two parenthesisations.
  - NAT-order (NatStrictTotalOrder) — supplies `<` on ℕ with its companion `≤` (`m ≤ n ⟺ m < n ∨ m = n`), the `<`-transitivity Axiom clause `(A m, n, p ∈ ℕ : m < n ∧ n < p : m < p)` consumed in the Reverse interior-segment derivation at `(m, n, p) := (s_i, s_i + 1, #t)` to chain `s_i < s_i + 1 < #t` into `s_i < #t`, and the `≤`-transitivity Consequence `(A m, n, p ∈ ℕ : m ≤ n ∧ n ≤ p : m ≤ p)` consumed in the same derivation at `(m, n, p) := (s_i + 1, s_{i+1}, #t)` to chain `s_i + 1 ≤ s_{i+1} ≤ #t` into `s_i + 1 ≤ #t`.
  - NAT-zero (NatZeroMinimum) — supplies the first Axiom clause `0 ∈ ℕ`, which grounds the sentinel value `s₀ = 0` and the literal `0` appearing in the `k = 0` case branches of Forward Conditions (ii) and (iii) and the Reverse first-segment derivation.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` and closure of ℕ under addition (grounding the numerals `2 := 1 + 1`, `3 := 2 + 1` and the sums `s_i + 1`, `s_i + 2`, `#t + 1`).
  - NAT-sub (NatPartialSubtraction) — supplies the right-telescoping clause `(m + n) − n = m`.
  - NAT-card (NatFiniteSetCardinality) — supplies the enumeration characterisation of `|·|`.
  - T4 (HierarchicalParsing) — supplies the positional conditions (i)–(iii), the field-segment terminology, and the zero-count bound `zeros(t) ≤ 3` (carried as a precondition; the proof's two-case split `k = 0` versus `k ≥ 1` is exhaustive over `ℕ` without consuming the upper bound).

---

## T4b — UniqueParse

Four partial functions N, U, D, E : T ⇀ T extract the node, user, document, and
element sub-sequences of a T4-valid tumbler and are well-defined and uniquely
determined by t. Each projection's image lies in the subset of T whose every
component is in ℕ⁺ — a nonempty finite sequence over ℕ (by T0)
with every component strictly positive by NAT-zero (the disjunction
0 < n ∨ 0 = n at n := tᵢ excludes the equality branch via the
non-separator distinction tᵢ ≠ 0).
Field absence is encoded by partiality of the corresponding projection — X is
absent in t iff t ∉ dom(X) — so no external absence marker is required. The
four domains are fixed by zeros(t): dom(N) is the T4-valid subset of T (N is
never absent); dom(U) restricts dom(N) to zeros(t) ≥ 1; dom(D) to zeros(t) ≥ 2;
dom(E) to zeros(t) = 3. Presence pattern, made exhaustive over dom(N) by T4's
Exhaustion Consequence (A t ∈ T : zeros(t) ≤ 3 : zeros(t) ∈ {0, 1, 2, 3}) —
universally quantified by the bound alone, instantiated at every T4-valid t
(zeros(t) ≤ 3 by the first conjunct of T4-valid) — for each k ∈ ℕ with
0 ≤ k ≤ 3 at which zeros(t) = k: k = 0 → only N defined;
k = 1 → N, U defined; k = 2 → N, U, D defined; k = 3 → all four defined.
The four cases collectively cover every T4-valid t, so the four projections are
well-defined on their stated domains.
The component-access notation t.X₁ := (X(t))₁ is grounded in T0's subscript:
ℕ⁺ ⊆ ℕ embeds every nonempty all-ℕ⁺-component sequence into T, so T0's projection
applies to X(t) whenever X is defined at t. Hence t.X₁ is defined iff X is
defined at t — in particular t.E₁ requires zeros(t) = 3. T4a's reverse direction
supplies, from T4's field-segment constraint, the conclusion that every field
segment is non-empty; T4b locally re-expresses this as the segment-length
inequalities (s₁ ≥ 2, s_k + 1 ≤ #t, s_{j+1} ≥ s_j + 2) that discharge
non-emptiness of every listed sub-sequence, consuming the native forms T4a's
Reverse direction outputs without a subtractive rewrite (the last-segment
inequality is kept in NAT-discrete's native +1 form rather than converted to
s_k ≤ #t − 1). NAT-closure grounds the numeral 2 := 1 + 1 in ℕ and the sums
s_i + 1, s_i + 2 appearing in the case construction; T4b cites T0's
Axiom's nonemptiness clause (A a ∈ T :: 1 ≤ #a) at a := t directly for
#t ≥ 1, for the k = 0 branch where the sole segment equals t itself, and NAT-sub's conditional-closure clause at s_i ≥ 1 (T0's index domain)
gives s_i − 1 in ℕ for the sub-sequence upper indices. NAT-card's enumeration
characterisation of |·|
identifies the length k of the strictly increasing enumeration s₁ < s₂ < … < s_k
of the zero-index subset with zeros(t), so k = zeros(t) in the case analysis
on k. Well-definedness follows because T4's role-assignment makes zeros exactly
the field separators and T0 identifies each tᵢ as a function of t, so the scan
result is determined by t. Outside the T4-valid subdomain (zeros(t) ≥ 4, or
zeros(t) ≤ 3 with a violated field-segment constraint) none of the projections
is assigned a value; consumers must discharge T4-validity as a precondition.

*Formal Contract:*
- *Definition:* The four partial functions `N, U, D, E : T ⇀ T` are characterised as follows. `dom(N)` is the T4-valid subset of `T`; `dom(U) = {t ∈ dom(N) : zeros(t) ≥ 1}`; `dom(D) = {t ∈ dom(N) : zeros(t) ≥ 2}`; `dom(E) = {t ∈ dom(N) : zeros(t) = 3}`. Let `s₁ < s₂ < ... < s_k` enumerate the zero positions of `t`, with `k = zeros(t)` bounded by `0 ≤ k ≤ 3` (T4 supplies `zeros(t) ≤ 3`; NAT-zero supplies `0 ≤ zeros(t)`). T4's Exhaustion Consequence gives `zeros(t) ∈ {0, 1, 2, 3}` at the T4-valid `t` here, so the four cases `k ∈ {0, 1, 2, 3}` collectively cover `dom(N)`; the values are fixed per-`k` — for each `k ∈ ℕ` with `0 ≤ k ≤ 3` at which `zeros(t) = k`: for `k = 0`, `N(t) = (t₁, ..., t_{#t})`; for `k = 1`, `N(t) = (t₁, ..., t_{s₁ - 1})` and `U(t) = (t_{s₁ + 1}, ..., t_{#t})`; for `k = 2`, `N(t) = (t₁, ..., t_{s₁ - 1})`, `U(t) = (t_{s₁ + 1}, ..., t_{s₂ - 1})`, `D(t) = (t_{s₂ + 1}, ..., t_{#t})`; for `k = 3`, `N(t) = (t₁, ..., t_{s₁ - 1})`, `U(t) = (t_{s₁ + 1}, ..., t_{s₂ - 1})`, `D(t) = (t_{s₂ + 1}, ..., t_{s₃ - 1})`, `E(t) = (t_{s₃ + 1}, ..., t_{#t})`. Outside the stated domains, the respective projections are not assigned values.
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies ℕ as the carrier, `T` as the set of nonempty finite sequences over ℕ, the Axiom's nonemptiness clause `(A a ∈ T :: 1 ≤ #a)`, the index domain `{1, …, #t}`, the component projection `tᵢ`, and the Axiom's comprehension clause `(A p ∈ ℕ : p ≥ 1 : (A r : {j ∈ ℕ : 1 ≤ j ≤ p} → ℕ :: (E t ∈ T :: #t = p ∧ (A i ∈ ℕ : 1 ≤ i ≤ p : tᵢ = r(i)))))` — licensing T-membership of each extracted sub-sequence: nonempty (by T4a) with components in ℕ (by the component projection), so the comprehension clause places it in `T`.
  - NAT-zero (NatZeroMinimum) — supplies `(A n ∈ ℕ :: 0 < n ∨ 0 = n)`.
  - NAT-order (NatStrictTotalOrder) — supplies `<` on ℕ with its companion `≤`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` and closure of ℕ under addition (grounding the numeral `2 := 1 + 1` and the sums `s_i + 1`, `s_i + 2`).
  - NAT-sub (NatPartialSubtraction) — supplies the conditional-closure clause `s_i ≥ 1, 1 ∈ ℕ ⟹ s_i − 1 ∈ ℕ`.
  - NAT-card (NatFiniteSetCardinality) — supplies the enumeration characterisation of `|·|`.
  - T4 (HierarchicalParsing) — supplies `zeros(t) ≤ 3`, the field-segment clauses, the separator role of zero-valued positions, the field-segment identification, and the Exhaustion Consequence.
  - T4a (SyntacticEquivalence) — supplies, via its Reverse direction, the conclusion that every field segment of `t` is non-empty.
  - NAT-discrete (NatDiscreteness) — supplies `m < n ⟹ m + 1 ≤ n`, licensing the last-segment non-emptiness inequality `s_k + 1 ≤ #t` in its native `+1` form (from T4a's Reverse direction) without subtractive conversion.
- *Postconditions:* `N, U, D, E : T ⇀ T` are partial functions. `dom(N)` is the T4-valid subset of `T`; `dom(U) ⊆ dom(N)` picks out `zeros(t) ≥ 1`; `dom(D) ⊆ dom(N)` picks out `zeros(t) ≥ 2`; `dom(E) ⊆ dom(N)` picks out `zeros(t) = 3`. On its domain each projection is well-defined, uniquely determined by `t`, and returns a nonempty finite sequence over `ℕ⁺` — an element of `T` whose every component is strictly positive. Field *absence* is encoded by partiality: `X` is *absent in `t`* iff `t ∉ dom(X)`. Presence pattern, exhausted over `dom(N)` by T4's Exhaustion Consequence instantiated at every T4-valid `t` — for each `k ∈ ℕ` with `0 ≤ k ≤ 3` at which `zeros(t) = k`: `k = 0` → only `N` defined; `k = 1` → `N, U` defined; `k = 2` → `N, U, D` defined; `k = 3` → all four defined. The four cases collectively cover every T4-valid `t`. The component-access notation `t.X₁ := (X(t))₁` — T0's component projection at index 1 applied to `X(t)`, which belongs to `T` whenever `X` is defined at `t` because `ℕ⁺ ⊆ ℕ` — is defined iff `X` is defined at `t`: `t.N₁` always on the T4-valid subset; `t.U₁` iff `zeros(t) ≥ 1`; `t.D₁` iff `zeros(t) ≥ 2`; `t.E₁` iff `zeros(t) = 3`. Outside the T4-valid subdomain, none of the projections is assigned a value; consumers must carry T4-validity as a precondition.

---

## T4c — LevelDetermination

On the T4-valid subset of T (tumblers satisfying zeros(t) ≤ 3, no two zeros adjacent,
t₁ ≠ 0, t_{#t} ≠ 0), T4c defines the four hierarchical level labels — node address,
user address, document address, element address — by zero count: zeros(t) = 0 ↔
node address, zeros(t) = 1 ↔ user address, zeros(t) = 2 ↔ document address,
zeros(t) = 3 ↔ element address. The biconditionals are definitional — they assign
labels to zero-count values rather than bridging two independently characterised
notions. NAT-card axiomatizes the cardinality operator |·| on subsets of every
initial segment {1, …, n} ⊆ ℕ with codomain ℕ, grounding zeros(t) ∈ ℕ for the
definition zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}| (the zero-index subset lies in
{1, …, #t}). Exhaustion on the T4-valid subdomain is supplied directly by T4's
Exhaustion Consequence zeros(t) ∈ {0, 1, 2, 3}, which T4c cites rather than
re-derives — every T4-valid tumbler receives a label. The four labels are
pairwise distinct because the zero counts 0, 1, 2, 3 are pairwise distinct in
ℕ — NAT-addcompat's strict successor inequality n < n + 1 (at n = 0, 1, 2)
supplies 0 < 1, 1 < 2, 2 < 3, NAT-order transitivity chains these to
0 < 1 < 2 < 3, and NAT-order's exactly-one trichotomy Consequence conjunct
¬(m < n ∧ m = n) — equivalently m < n ⟹ m ≠ n — excludes equality within the
chain directly from the strict inequalities — and zeros(t) is single-valued.
NAT-zero's first Axiom clause 0 ∈ ℕ licenses the n = 0 instantiation of
NAT-addcompat's n < n + 1 to obtain the base link 0 < 1, and grounds the
literal 0 used in the label-defining biconditional zeros(t) = 0 ↔ t is a
node address. NAT-closure posits 1 ∈ ℕ and closes ℕ under addition, grounding
the numerals 2 := 1 + 1 ∈ ℕ and 3 := 2 + 1 ∈ ℕ used in injectivity's chain
0 < 1 < 2 < 3.
T4c does not claim realisation — existence of a T4-valid tumbler at each zero
count is not asserted, so T4c stands as a pure definition on whatever T4-valid
tumblers exist. The claim is universally quantified over the T4-valid subdomain
and assigns no level outside it. No dependency on T4b is required because the
labels are defined by T4c directly in terms of zero count, not in terms of
T4b's fields(t) decomposition; a downstream reading that characterises levels
by the presence or absence of particular field segments would require T4b and
is not the content of T4c.

*Formal Contract:*
- *Preconditions:* `t` satisfies the T4 constraints (`zeros(t) ≤ 3`, no two zeros adjacent, `t₁ ≠ 0`, `t_{#t} ≠ 0`).
- *Definition:* `(A t ∈ T : t is T4-valid :: (zeros(t) = 0 ↔ t is a node address) ∧ (zeros(t) = 1 ↔ t is a user address) ∧ (zeros(t) = 2 ↔ t is a document address) ∧ (zeros(t) = 3 ↔ t is an element address))`.
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies the index domain `{1, …, #t} ⊆ ℕ` that contains the zero-index subset, so NAT-card applies at `n = #t`.
  - NAT-zero (NatZeroMinimum) — supplies the first Axiom clause `0 ∈ ℕ`, which grounds the literal `0` in the label-defining biconditional `zeros(t) = 0 ↔ t is a node address`, where `zeros(t) ∈ ℕ` is compared against the ℕ-element `0`.
  - NAT-card (NatFiniteSetCardinality) — axiomatizes `|·|` on subsets of every initial segment `{1, …, n} ⊆ ℕ` with codomain ℕ, grounding the type `zeros(t) ∈ ℕ` for `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|`.
  - NAT-order (NatStrictTotalOrder) — supplies transitivity to chain `0 < 1 < 2 < 3` and the exactly-one trichotomy Consequence's conjunct `¬(m < n ∧ m = n)` — equivalently `m < n ⟹ m ≠ n` — to exclude equality within that chain directly from the strict inequalities, so that `0, 1, 2, 3` are pairwise distinct for injectivity.
  - NAT-closure (NatArithmeticClosureAndIdentity) — posits `1 ∈ ℕ` and closes ℕ under addition, grounding the numerals `2 := 1 + 1 ∈ ℕ` and `3 := 2 + 1 ∈ ℕ` used in injectivity's chain `0 < 1 < 2 < 3`; additionally supplies the distinctness *Consequence* `0 < 1` — derived in NAT-closure's prose from successor-positivity at `n := 0` and left-identity at `n := 1` — cited directly in injectivity as the base link of the chain.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — supplies the strict successor inequality `n < n + 1`, instantiated at `n ∈ {1, 2}` to obtain the links `1 < 2` and `2 < 3` in injectivity's chain.
  - T4 (HierarchicalParsing) — supplies the T4-valid subdomain constraints (`zeros(t) ≤ 3`, no two zeros adjacent, `t₁ ≠ 0`, `t_{#t} ≠ 0`) that delimit T4c's subdomain, and the Exhaustion Consequence `zeros(t) ∈ {0, 1, 2, 3}` cited directly for the exhaustion step.
- *Postconditions:* The label assignment supplied by the *Definition* slot is well-defined on the T4-valid subdomain — every T4-valid tumbler receives exactly one of the four labels. This factors into two clauses, each established by the proof above. *Exhaustion:* `(A t ∈ T : t is T4-valid :: zeros(t) ∈ {0, 1, 2, 3})`, established by the Exhaustion paragraph above. *Pairwise extensional disjointness:* the four label predicates `t is a node address`, `t is a user address`, `t is a document address`, `t is an element address` have pairwise disjoint extensions on the T4-valid subdomain, established by the Injectivity paragraph above.

---

## T5 — ContiguousSubtrees

If two tumblers a and c share a common prefix p, then every tumbler b between them in the lexicographic order also shares that prefix. This means every prefix-defined subtree occupies a contiguous interval on the tumbler line — no address from an unrelated subtree can appear between two addresses in the same subtree.

*Formal Contract:*
- *Preconditions:* `a, b, c ∈ T`; `p` is a tumbler prefix with `#p ≥ 1`; `p ≼ a`; `p ≼ c`; `a ≤ b ≤ c` under T1.
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies the length operator `#·` on `b` for the Case 1 hypothesis `#b ≥ #p` and the Case 2 hypothesis `#b < #p`, and the component projection `i ↦ bᵢ` used in Case 1 to construct the divergence-index set `{k ∈ {1, ..., #p} : bₖ ≠ pₖ}`. Neither operator is supplied for arbitrary `b ∈ T` by Prefix (which only unfolds prefix relations on `a`, `c`) or T3 (which speaks to equality from component agreement, not the projection itself).
  - Prefix (PrefixRelation) — unfolds `p ≼ a`, `p ≼ c` into length and component-wise equalities; re-folds component-wise agreement into `p ≼ b`.
  - T1 (LexicographicOrder), case (i) — derives contradictions `b < a` and `c < b` from divergence-position witnesses.
  - T1 (LexicographicOrder), case (ii) — supplies `k = #a + 1 ≤ #b` in Case 2; combined with NAT-addcompat's `#a < #a + 1` this yields `#a < #b`, which contradicts `#a > #b` and excludes case (ii).
  - T1 (LexicographicOrder), postcondition (a) irreflexivity — closes the `a = b` disjunct of `a ≤ b` (Subcase 1a) and the `b = c` disjunct of `b ≤ c` (Subcase 1b and Case 2) by substituting the derived `b < a` / `c < b` into `a < a` / `b < b`.
  - T1 (LexicographicOrder), postcondition (b) trichotomy — closes the `a < b` disjunct of `a ≤ b` (Subcase 1a) and the `b < c` disjunct of `b ≤ c` (Subcase 1b and Case 2) via the clause `¬(a < b ∧ b < a)` at `(a, b)` and `(b, c)` respectively.
  - T3 (CanonicalRepresentation) — distinct lengths imply distinct tumblers, giving `a ≠ b` in Case 2.
  - NAT-order (NatStrictTotalOrder) — trichotomy at `(bₖ, pₖ)` in Case 1 dichotomizes `bₖ ≠ pₖ` into `bₖ < pₖ ∨ bₖ > pₖ`; the `≤`/`<` clauses on ℕ underwrite the length reasoning throughout (`#a ≥ #p`, `#c ≥ #p`, `#b < #p`, `k ≤ #p ≤ min(#a, #b)`); the exclusion of T1(ii) in Case 2 unfolds `#a + 1 ≤ #b` by NAT-order's definition of `≤` and applies either `<`-transitivity (on `#a < #a + 1 < #b`) or equality substitution (on `#a + 1 = #b`) to reach `#a < #b`, then closes via exactly-one trichotomy's `¬(m < n ∧ n < m)` clause at `(#a, #b)` against `#a > #b`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — supplies the strict successor inequality `#a < #a + 1`, used in Case 2 to promote T1(ii)'s `#a + 1 ≤ #b` to `#a < #b` and derive the contradiction with `#a > #b`.
  - NAT-wellorder (NatWellOrdering) — least-element principle in Case 1, invoked on the nonempty set of indices `k ∈ {1, ..., #p}` with `bₖ ≠ pₖ` to select the first divergence index.
- *Postconditions:* `p ≼ b` — `b` extends `p` and belongs to the same subtree as `a` and `c`.

Nelson: "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." A span between two endpoints under the same prefix captures exactly the addresses under that prefix between those endpoints — no addresses from unrelated subtrees can interleave.

Because the hierarchy is projected onto a flat line (T1), containment in the tree corresponds to contiguity on the line. Nelson: "A span may be visualized as a zone hanging down from the tumbler line — what is called in computer parlance a depth-first spanning tree." Every subtree maps to a contiguous range, and every contiguous range within a subtree stays within the subtree.

---

## T6 — DecidableContainment

Containment queries (same server? same account? same document? one address a prefix of
another?) can be decided by extracting and comparing the relevant field sequences from the
two tumbler representations alone, with no external index or registry. The decidability is
a corollary of the T4-family (T4, T4a, T4b) rather than of T4 alone; it is stated
separately because it is load-bearing for decentralized operation.

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` are T4-valid (i.e., `a, b ∈ dom(N)` in the sense of T4b).
- *Depends:*
  - T0 (CarrierSetDefinition) — fixes carrier ℕ.
  - NAT-order (NatStrictTotalOrder) — trichotomy for decidable equality on ℕ; strict order for length comparisons.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` as the constant tested in `tᵢ = 0` within `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|` (Ingredient 2), and underlying T4's no-adjacent-zeros and boundary constraints recapitulated in Ingredient 1.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` and closure of ℕ under addition, grounding the presence-pattern numerals `1, 2, 3 ∈ ℕ` (`2 := 1 + 1 ∈ ℕ`, `3 := 2 + 1 ∈ ℕ`) used in Ingredient 2 and in the Postconditions as the thresholds `zeros(t) ≥ 1`, `zeros(t) ≥ 2`, `zeros(t) = 3`; the numeral `1` in the componentwise-equality index range `(A k : 1 ≤ k ≤ #D(b) : ...)` of case (d) and postcondition (d); and the successor `m + 1 ∈ ℕ` in Ingredient 3's termination-bound exposition via the signature clause `+ : ℕ × ℕ → ℕ` instantiated at `(m, 1)`.
  - NAT-card (NatFiniteSetCardinality) — axiomatizes `|·|` as a total operator on subsets of every initial segment `{1, …, n} ⊆ ℕ` with codomain ℕ, so `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|` introduced in Ingredient 2 is well-typed and places `zeros(t) ∈ ℕ`; this typing is what turns the threshold comparisons `zeros(t) ≥ 1`, `zeros(t) ≥ 2`, `zeros(t) = 3` in Ingredient 2 and in postconditions (b)–(d) into comparisons between two elements of ℕ once NAT-closure has placed the right-hand numerals in ℕ. Also fixes `|·|` as distinct from T0's tumbler-length `#·`.
  - T3 (CanonicalRepresentation, this ASN) — supplies the componentwise-equality characterisation of sequence equality on `T`: `a = b ≡ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. This is the equivalence Ingredient 3 appeals to when it reduces sequence equality to length agreement together with position-by-position comparison, and it is what licences the projection equalities `N(a) = N(b)` in case (a), `N(a) = N(b) ∧ U(a) = U(b)` in case (b), and `N(a) = N(b) ∧ U(a) = U(b) ∧ D(a) = D(b)` in case (c) as finitely many ℕ-equality checks on the extracted field sequences; the same reduction underwrites the `N(a) = N(b)` and `U(a) = U(b)` portions of case (d)'s document-family prerequisites. Uniqueness of the four projections themselves is not T3's role — that is established by T4b directly from T4 + T4a.
  - T4 (HierarchicalParsing) — zero-count bound, no-adjacent-zeros, boundary constraints, role-assignment of zeros as separators.
  - T4a (SyntacticEquivalence) — present field segments non-empty, so partiality of a projection unambiguously indicates field absence.
  - T4b (UniqueParse) — partial projections `N, U, D, E : T ⇀ T`; presence-pattern postcondition tying each projection's domain to `zeros(t)`.
- *Forward References:*
  - T1 (LexicographicOrder) — named as the ordering companion to T6; the claim frames itself as the containment-decision counterpart to T1's sort order, but T6's proof does not consume T1's ordering relation.
- *Postconditions:*
  - (a) Terminates, returns YES iff `N(a) = N(b)`.
  - (b) Terminates, returns YES iff `zeros(a) ≥ 1 ∧ zeros(b) ≥ 1 ∧ N(a) = N(b) ∧ U(a) = U(b)`; NO under asymmetric or symmetric absence.
  - (c) Terminates, returns YES iff `zeros(a) ≥ 2 ∧ zeros(b) ≥ 2 ∧ N(a) = N(b) ∧ U(a) = U(b) ∧ D(a) = D(b)`; NO under asymmetric or symmetric absence.
  - (d) Terminates, returns YES iff `zeros(a) ≥ 2 ∧ zeros(b) ≥ 2 ∧ N(a) = N(b) ∧ U(a) = U(b) ∧ #D(b) ≤ #D(a) ∧ (A k : 1 ≤ k ≤ #D(b) : D(a)ₖ = D(b)ₖ)`; NO under D-absence or when `N(a) ≠ N(b)` or `U(a) ≠ U(b)`.
  - All decisions use only the four projections at `a` and `b` and componentwise comparison on finite ℕ-sequences.

T6 captures allocation hierarchy, not derivation history. Version `5.3` was allocated under `5`, but this alone does not record which version's content was copied. Nelson: "the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." Formal version-derivation requires the version graph.

Shared prefix means shared containing scope: "The owner of a given item controls the allocation of the numbers under it." But: "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." Shared prefix guarantees containment and ownership, never semantic categorization.

Gregory's `tumblercmp` (total order) and `tumbleraccounteq` (prefix match with zero-as-wildcard, truncating candidate to parent length) realize the distinction between ordering and containment; `tumbleraccounteq` is the operational form of T6.

---

## T7 — FirstElementFieldDistinction

For two T4-valid element-level addresses (tumblers satisfying the T4 constraints with exactly
three zero delimiters), differing in the first element-field component forces the tumblers
themselves to be distinct — a Leibniz-level claim discharged through T3 (canonical
representation) restricted to T4-valid element-level addresses. T4-validity is required so that
T4b licenses the component-access notation `a.E₁`, `b.E₁` used in the statement; without it the
predicate is ill-formed. T7 does not itself establish region-level disjointness of the
Nelson-convention subspaces `{1, 2}` — the stronger claim that the set of T4-valid element-level
tumblers with `E₁ = 1` (text) is a typed region disjoint from the set with `E₁ = 2` (links),
treating the subspace identifier as a distinguished typed concept, is relocated to a downstream
property in a later ASN. T7 supplies the structural prerequisite on which that relocation rests:
arithmetic that changes the first element-field component cannot leave the tumbler unchanged.

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` satisfy the T4 constraints — at most three zero-valued components, no two zeros adjacent, `a₁ ≠ 0`, `a_{#a} ≠ 0` (and likewise for `b`) — and have `zeros(a) = zeros(b) = 3`.
- *Depends:*
  - T0 (CarrierSetDefinition) — components lie in ℕ; supplies the index domain and component projection on which T4's positivity clauses and T3's positional comparison are stated.
  - T3 (CanonicalRepresentation) — tumblers are equal iff same length and agree at every position; converts positional/length disagreement to tumbler inequality.
  - T4 (HierarchicalParsing) — constrains the bound variables; supplies the role-assignment under which zeros are separators and the *field separator* definition that makes a non-separator position one with `tᵢ ≠ 0`, the antecedent the local strict-positivity derivation feeds into NAT-zero's disjunction.
  - T4a (SyntacticEquivalence) — converts T4's positional clauses to segment non-emptiness, fixing `α, β, γ, δ ≥ 1`.
  - T4b (UniqueParse) — licenses the well-definedness of `t.E₁` on T4-valid inputs with `zeros(t) = 3`.
  - NAT-zero (NatZeroMinimum) — supplies the disjunction `(A n ∈ ℕ :: 0 < n ∨ 0 = n)`, instantiated at `n := tᵢ` (licensed by `tᵢ ∈ ℕ` from T0) and combined with T4's non-separator distinction `tᵢ ≠ 0` to yield strict positivity `0 < tᵢ` at every non-separator position.
  - NAT-order (NatStrictTotalOrder) — supplies `<`/`≤` on ℕ for the zero-count bound (inherited from T4 via the precondition `zeros(a) = zeros(b) = 3`), the `≥ 1` field-length inequalities `α, β, γ, δ ≥ 1` (and the primed counterparts for `b`) locally unpacked from T4a's conclusion, and three further roles in the strict-ordering derivation that drives sub-case 2b: (i) the `≤`-definition `a ≤ b ⟺ a < b ∨ a = b`, used to split `α + 1 ≤ α + β + 1` and `α + β + 2 ≤ α + β + γ + 2` into strict-and-equality branches that then chain into strict inequalities; (ii) transitivity `m < n ∧ n < p ⟹ m < p`, instantiated at `(α + 1, α + β + 1, α + β + 2)` and `(α + β + 2, α + β + γ + 2, α + β + γ + 3)` in the strict branches of those splits; and (iii) the `≥`-definition `a ≥ b ⟺ b ≤ a`, used at `(β + 1, 1)` and `(γ + 2, 2)` to convert NAT-addbound's outputs `β + 1 ≥ 1` and `γ + 2 ≥ 2` into the antecedent forms `1 ≤ β + 1` and `2 ≤ γ + 2` required by NAT-addcompat. Once the strict orderings `α + 1 < α + β + 2 < α + β + γ + 3` and the primed counterpart are established, NAT-order's strict total order pins down the canonical sorted enumeration of each three-element set as exactly the listed sequence (no element can occupy two positions under irreflexive `<`, and a three-element strictly ordered set admits no other ascending enumeration), so the set-equality forces element-by-element matching at corresponding positions.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` and closure of ℕ under addition, grounding the numerals `2 := 1 + 1 ∈ ℕ`, `3 := 2 + 1 ∈ ℕ`, `4 := 3 + 1 ∈ ℕ` and the sums `α + 1`, `α + β + 2`, `α + β + γ + 3`, `α + β + γ + 4` (and the primed counterparts for `b`) so that the separator-position expressions and the first element-field position are typed within ℕ; the same `1 ∈ ℕ` underwrites the field-length inequalities `α, β, γ, δ ≥ 1` and `α', β', γ', δ' ≥ 1` locally re-expressed from T4a's segment non-emptiness conclusion.
  - NAT-cancel (NatAdditionCancellation) — right/left cancellation discharges the three pairwise-matching extractions `α = α'`, `β = β'`, `γ = γ'`.
  - NAT-addassoc (NatAdditionAssociative) — regroups `α + β + 2` and `α + β + γ + 3` so NAT-cancel applies at `m = 2` and `m = 3`; additionally regroups inside the strict-ordering derivation of sub-case 2b at `(m, n, p) := (α, β, 1)`, `(α + β, 1, 1)`, `(α + β, γ, 2)`, and `(α + β + γ, 2, 1)` so that NAT-addcompat's left order compatibility and strict successor outputs `α + (β + 1)`, `(α + β + 1) + 1`, `(α + β) + (γ + 2)`, and `(α + β + γ + 2) + 1` are rewritten into the canonical left-associated forms `α + β + 1`, `α + β + 2`, `α + β + γ + 2`, and `α + β + γ + 3` respectively.
  - NAT-addbound (NatAdditionDominatesOperands) — supplies the right-dominance clause `m + n ≥ n` instantiated at `(m, n) := (β, 1)` to deliver `β + 1 ≥ 1` (used to discharge the antecedent `1 ≤ β + 1` of NAT-addcompat's left order compatibility in the first strict inequality) and at `(m, n) := (γ, 2)` to deliver `γ + 2 ≥ 2` (used to discharge the antecedent `2 ≤ γ + 2` of NAT-addcompat's left order compatibility in the second strict inequality), once NAT-order's `≥`-definition rewrites the outputs into the `≤`-form NAT-addcompat consumes.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — supplies (i) the left order compatibility clause `(A m', n', p ∈ ℕ : p ≤ n' : m' + p ≤ m' + n')`, instantiated at `(m', n', p) := (α, β + 1, 1)` and `(α + β, γ + 2, 2)` to lift the antecedents `1 ≤ β + 1` and `2 ≤ γ + 2` (supplied by NAT-addbound) into `α + 1 ≤ α + (β + 1)` and `(α + β) + 2 ≤ (α + β) + (γ + 2)`; and (ii) the strict successor inequality `(A k ∈ ℕ :: k < k + 1)`, instantiated at `k := α + β + 1` and `k := α + β + γ + 2` to deliver `α + β + 1 < α + β + 2` and `α + β + γ + 2 < α + β + γ + 3`. The `≤` and `<` outputs are then chained by NAT-order's `≤`-split and transitivity into the strict orderings `α + 1 < α + β + 2` and `α + β + 2 < α + β + γ + 3` that license the sorted pairwise matching.
- *Forward References:*
  - T1 (LexicographicOrder) — the ordering T1 induces places all text addresses (subspace 1) before all link addresses (subspace 2) within the same document, as a consequence of `1 < 2` at the subspace position under lexicographic order.
- *Postconditions:* `a.E₁ ≠ b.E₁ ⟹ a ≠ b`.

The ordering T1 places all text addresses (subspace 1) before all link addresses (subspace 2) within the same document, because `1 < 2` at the subspace position — a consequence of the lexicographic order, not an assumption.

---

## T8 — AllocationPermanence

The set of allocated addresses grows monotonically across every state transition: once an address enters the allocated set it is never removed. This follows directly from the absence of any removal operation in the transition vocabulary, so the guarantee covers all present and future operations.

*Formal Contract:*
- *Invariant:* For every state transition s → s', `allocated(s) ⊆ allocated(s')`.
- *Postcondition:* For every admissible transition sequence s₀ → s₁ → ··· → sₙ, `allocated(sᵢ) ⊆ allocated(sⱼ)` whenever `0 ≤ i ≤ j ≤ n`; equivalently, once `a ∈ allocated(sᵢ)`, `a ∈ allocated(sⱼ)` for all `j ≥ i`.
- *Depends:*
  - AllocatedSet (AllocatedSet) — defines `allocated(s)`, state, and state transition.
  - NoDeallocation (NoDeallocation) — no operation in Σ removes an allocated address.

---

## T9 — ForwardAllocation

When two addresses are produced by the same allocator and one is allocated before the other, the earlier-allocated
address is strictly smaller under the tumbler total order. Domain disjointness (T10a.6) fixes the witnessing allocator
uniquely from the pair; enumeration injectivity (T10a.7), in its strict-order form `i < j ⟹ tᵢ < tⱼ`, delivers the
strict inequality in one step — replacing a prior induction on the index gap.

*Formal Contract:*
- *Definitions:*
  - `allocated_before(a, b)` ≡ `a = tᵢ ∧ b = tⱼ ∧ i < j` in T10a's enumeration of `dom(A)`, well-defined on pairs satisfying `same_allocator(a, b)` by T10a.6 and T10a.7.
- *Depends:*
  - T10a (AllocatorDiscipline) — defines `dom(A)`, `same_allocator`, and the enumeration `tₙ₊₁ = inc(tₙ, 0)` that indexes the allocation sequence.
  - T10a.6 (DomainDisjointness) — under `same_allocator(a, b)`, the witnessing allocator `A` is uniquely determined, so the enumeration context in which `i < j` holds is unambiguous.
  - T10a.7 (EnumerationInjectivity) — used in two roles: (i) index uniqueness, so the `i, j ≥ 0` with `a = tᵢ, b = tⱼ` are determined by `(a, b)` and `allocated_before`'s `i < j` is unambiguous; (ii) strict-order postcondition `(A m, n ≥ 0 : m < n : tₘ < tₙ)`, instantiated at `(i, j)`, delivers `tᵢ < tⱼ` in one step and replaces the prior induction on `d = j − i`.
  - T1 (LexicographicOrder) — supplies the total order `<` in which T10a.7's strict-order form and T9's conclusion `a < b` are both phrased.
- *Preconditions:* `a, b ∈ T` with `same_allocator(a, b) ∧ allocated_before(a, b)`.
- *Postconditions:* `a < b` under the tumbler order T1.

---

## TA-LC — LeftCancellation

TumblerAdd is left-cancellative: if a ⊕ x = a ⊕ y with both additions well-defined, then x = y. Differing action points between x and y lead to immediate contradiction via TumblerAdd's prefix-copy rule; once a shared action point is established, component-wise equality at every position and equal lengths force x = y by canonical representation.

*Formal Contract:*
- *Preconditions:* a, x, y ∈ T; Pos(x); Pos(y); actionPoint(x) ≤ #a; actionPoint(y) ≤ #a; a ⊕ x = a ⊕ y
- *Depends:*
  - TumblerAdd (TumblerAdd) — prefix-copy, advance, tail-copy rules and result-length identity.
  - TA0 (WellDefinedAddition) — well-definedness of `a ⊕ x` and `a ⊕ y`.
  - TA-Pos (PositiveTumbler) — supplies `Pos(x)` and `Pos(y)` for action-point existence.
  - ActionPoint (ActionPoint) — action point as first nonzero component.
  - NAT-cancel (NatAdditionCancellation) — summand absorption and left cancellation on ℕ.
  - NAT-order (NatStrictTotalOrder) — trichotomy collapsing ruled-out orderings to equality.
  - T3 (CanonicalRepresentation) — component-wise and length agreement imply tumbler equality.
- *Postconditions:* x = y

---

## TA-MTO — ManyToOne

Two tumblers a and b yield the same result under displacement w if and only if they agree on every component from position 1 through w's action point. This is TumblerAdd's many-to-one property made precise: components of the starting position beyond the action point are overwritten by the displacement's tail and cannot influence or be recovered from the result.

*Formal Contract:*
- *Preconditions:* w ∈ T, Pos(w), a ∈ T, b ∈ T, #a ≥ actionPoint(w), #b ≥ actionPoint(w)
- *Depends:*
  - TumblerAdd (TumblerAdd) — three-region constructive definition and result-length identity.
  - TA0 (WellDefinedAddition) — well-definedness of `a ⊕ w` and `b ⊕ w`.
  - TA-Pos (PositiveTumbler) — discharges `Pos(w)` for TA0 and ActionPoint.
  - ActionPoint (ActionPoint) — names `k` and licenses the three-region split.
  - T3 (CanonicalRepresentation) — position-wise-and-length characterisation of tumbler equality.
  - NAT-cancel (NatAdditionCancellation) — right cancellation on ℕ at position `k`.
- *Postconditions:* a ⊕ w = b ⊕ w ⟺ (A i : 1 ≤ i ≤ actionPoint(w) : aᵢ = bᵢ)

---

## TA-Pos — PositiveTumbler

Defines positivity for tumblers via two predicate symbols: `Pos(t)` (positive) iff at least one component is
nonzero, and `Zero(t)` (zero tumbler) iff every component is zero. The `Pos` matrix is written as the
classical negation `¬(tᵢ = 0)` rather than `tᵢ ≠ 0`, so no inequality symbol beyond `=` is required on ℕ.
Commits one clause beyond the defining ones: the complementarity `(A t ∈ T :: Pos(t) ⟺ ¬Zero(t))`,
which follows from the defining clauses by the DeMorgan duality of bounded quantifiers and holds whether
or not the index range is empty. The partition-content consequence — that T0's `(A a ∈ T :: 1 ≤ #a)`
forces the index range `1 ≤ i ≤ #t` to be nonempty for every `t ∈ T`, so `Pos(t)` exhibits a nonzero
component and `Zero(t)` makes every component equal to `0` — is a derived consequence stated in prose
rather than a separate contract clause, since it restates T0's nonemptiness axiom applied to the Pos/Zero
quantifier ranges. Additionally introduces the set-form `Z = {t ∈ T : Zero(t)}`, consumed by TA7a's
subspace-closure postcondition `o ⊖ w ∈ S ∪ Z` where the union with `S` requires set-valued notation.
The ordering consequence — every positive tumbler is strictly greater under T1 than every zero tumbler of
any length — is established separately by a downstream ordering theorem that consumes ActionPoint.

*Formal Contract:*
- *Definition:* `(A t ∈ T :: Pos(t) ⟺ (E i ∈ ℕ : 1 ≤ i ≤ #t : ¬(tᵢ = 0)))`; `(A t ∈ T :: Zero(t) ⟺ (A i ∈ ℕ : 1 ≤ i ≤ #t : tᵢ = 0))`; **Z** = {t ∈ T : Zero(t)}.
- *Consequence:* `(A t ∈ T :: Pos(t) ⟺ ¬Zero(t))`.
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier `T`, length `#t`, component projection `tᵢ`, and the nonemptiness clause `(A a ∈ T :: 1 ≤ #a)` cited in prose to unpack the Definition's quantifier ranges.
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set appearing in the bounded existential `(E i ∈ ℕ : 1 ≤ i ≤ #t : ¬(tᵢ = 0))` of the `Pos` clause and the bounded universal `(A i ∈ ℕ : 1 ≤ i ≤ #t : tᵢ = 0)` of the `Zero` clause, over which the index variable `i` ranges before being further restricted by the carrier-side clause `i ∈ ℕ` and the term-side range `1 ≤ i ≤ #t`.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal appearing in `tᵢ = 0`.
  - NAT-order (NatStrictTotalOrder) — supplies `≤` on ℕ for the bounded-quantifier range `1 ≤ i ≤ #t`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` for the numeral bounding that range.

---

## TA-PosDom — PositiveDominatesZero

Every positive tumbler is strictly greater under T1 than every zero tumbler of any length. Established by
constructing the first nonzero index `k` of the positive tumbler inline via NAT-wellorder on the set of nonzero
positions, then performing a case analysis on whether the zero tumbler's length reaches `k`: when it does, T1
case (i) separates them at `k`; when it does not, T1 case (ii) separates them by the prefix rule.

*Formal Contract:*
- *Preconditions:* `t ∈ T`, `Pos(t)`; `z ∈ T`, `Zero(z)`.
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier `T`, length `#·`, component projection; commitment that the index domain `{1, …, #t}` is a subset of ℕ (used to place `S ⊆ ℕ`) and that each `tᵢ ∈ ℕ`.
  - TA-Pos (PositiveTumbler) — `Pos` and `Zero` predicate definitions; unpacks `Pos(t)` to the existential whose witnesses populate `S`.
  - NAT-wellorder (NatWellOrdering) — least-element principle applied to `S` to supply the minimal index `k`.
  - NAT-zero (NatZeroMinimum) — disjunction axiom `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` instantiated at `n = tₖ` to derive `0 < tₖ` from `tₖ ≠ 0`.
  - NAT-discrete (NatDiscreteness) — forward form `m < n ⟹ m + 1 ≤ n`, used at `m = #z, n = #t` to obtain `#z + 1 ≤ #t`, and at `m = #z, n = i` in Case `#z < k` to exclude the `#z < i` branch of trichotomy when discharging T1(ii)'s agreement obligation.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality `#z < #z + 1`, used with NAT-order's `<`/`≤` composition to discharge T1's top-level schema bound `1 ≤ #z + 1` for the witness `#z + 1` in Case `#z < k`.
  - NAT-order (NatStrictTotalOrder) — `<`/`≤` transitivity and irreflexivity used both in the least-element witness and in the case analyses, trichotomy at `(i, #z)` used in Case `#z < k` to reduce a generic `i` with `1 ≤ i < #z + 1` to `i ≤ #z` so that T1(ii)'s agreement schema can be discharged on its native range, and the `≤`-defining clause `m ≤ n ⟺ m < n ∨ m = n` used to compose strict with non-strict bounds (including the discharge of `1 ≤ #z + 1` and the assembly of `i ≤ #z` from the surviving trichotomy disjuncts).
  - T1 (LexicographicOrder) — case (i) in `#z ≥ k`, case (ii) in `#z < k`.
- *Postconditions:* `(A t ∈ T, z ∈ T : Pos(t) ∧ Zero(z) :: z < t)`.

---

## TA-RC — RightCancellationFailure

TumblerAdd is not right-cancellative: distinct tumblers a ≠ b can satisfy a ⊕ w = b ⊕ w for the same positive displacement w. The mechanism is tail replacement — any two starting positions that agree up to the action point but differ beyond it are mapped to the same result, so the starting position cannot be recovered from the result alone.

*Formal Contract:*
- *Depends:*
  - T0 (CarrierSetDefinition) — comprehension clause, instantiated at length `p = 3` with the component maps for `a = [1,3,5]`, `b = [1,3,7]`, and `w = [0,2,4]` respectively, establishes `a, b, w ∈ T` — the carrier-set membership presupposed by every condition cited below.
  - T3 (CanonicalRepresentation) — inequality from a single component disagreement.
  - TA0 (WellDefinedAddition) — action-point bound for well-definedness.
  - TA-Pos (PositiveTumbler) — positivity of `w` licensing the action point.
  - ActionPoint (ActionPoint) — minimum-position formula fixing `k = 2`.
  - TumblerAdd (TumblerAdd) — three-region rule computing each side.
- *Postconditions:* ∃ a, b, w ∈ T : Pos(w) ∧ actionPoint(w) ≤ #a ∧ actionPoint(w) ≤ #b ∧ a ≠ b ∧ a ⊕ w = b ⊕ w

---

## TA-assoc — AdditionAssociative

Tumbler addition is associative: (a ⊕ b) ⊕ c = a ⊕ (b ⊕ c) whenever action points are properly ordered (k_b ≤ #a and k_c ≤ #b). The result length always equals the length of the rightmost operand, and the effective action point of a composed displacement b ⊕ c equals k_b when k_b ≤ k_c and equals k_c when k_c ≤ k_b (NAT-order trichotomy).

*Formal Contract:*
- *Preconditions:* `a, b, c ∈ T`, `Pos(b)`, `Pos(c)`, `k_b ≤ #a`, `k_c ≤ #b` (where `k_b = actionPoint(b)`, `k_c = actionPoint(c)`).
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier `T` and length `#·` on finite ℕ-sequences.
  - TumblerAdd (TumblerAdd) — piecewise prefix-copy / advance / tail-copy definition of `⊕`.
  - TA0 (WellDefinedAddition) — preconditions `Pos(w)`, `actionPoint(w) ≤ #x`; result-length `#(x ⊕ w) = #w`.
  - TA-Pos (PositiveTumbler) — existential definition of `Pos(·)`; consumed to establish `Pos(b ⊕ c)`.
  - ActionPoint (ActionPoint) — definition `actionPoint(w) = min{i : wᵢ ≠ 0}`; bounds `1 ≤ actionPoint(w) ≤ #w`; zeros-below; minimum-nonzero `w_{actionPoint(w)} ≥ 1`.
  - T1 (LexicographicOrder) — supplies the `<` and `≥` on tumblers under which TumblerAdd's strict-advancement and dominance postconditions (`a ⊕ w > a`, `a ⊕ w ≥ w`) are stated; TumblerAdd's contract, consumed by this proof, is interpretable only with T1 in scope.
  - T3 (CanonicalRepresentation) — component-wise equality plus equal length implies tumbler equality.
  - NAT-addassoc (NatAdditionAssociative) — `(m + n) + p = m + (n + p)` on ℕ; used in Case 2.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — left order-compatibility and strict successor `n < n + 1`; used in sub-case `k_b = k_c`.
  - NAT-cancel (NatAdditionCancellation) — symmetric summand absorption `n + m = m ⟹ n = 0`, on which TumblerAdd's dominance sub-case `aₖ > 0` rests; required in scope for the consumed TumblerAdd contract.
  - NAT-closure (NatArithmeticClosureAndIdentity) — additive identity `0 + n = n` and closure under `+`.
  - NAT-discrete (NatDiscreteness) — forward direction `m < n ⟹ m + 1 ≤ n`, on which ActionPoint's minimum-nonzero clause `1 ≤ w_{actionPoint(w)}` rests; this proof invokes that clause directly when lifting `b_{k_b} ≥ 1` and `c_{k_c} ≥ 1`.
  - NAT-order (NatStrictTotalOrder) — trichotomy, transitivity, `m ≤ n ⟺ m < n ∨ m = n`.
  - NAT-sub (NatPartialSubtraction) — conditional closure of `k − 1` and `n − k` and the inverse collapses on which TumblerAdd's result-length identity `#(a ⊕ w) = #w` rests; that identity, exported through TA0, supplies the right-side length `#(a ⊕ s) = #c` here.
  - NAT-wellorder (NatWellOrdering) — least-element principle on which ActionPoint's existence-and-uniqueness construction of `actionPoint(w)` rests; this proof invokes ActionPoint's definition and bounds directly when computing `actionPoint(s)` for `s = b ⊕ c` per sub-case of NAT-order trichotomy on `(k_b, k_c)`.
  - NAT-zero (NatZeroMinimum) — lower bound `0 ≤ n`; used in `≥ 1 → > 0` lifts.
- *Postconditions:* `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)`; `#((a ⊕ b) ⊕ c) = #(a ⊕ (b ⊕ c)) = #c`; `Pos(b ⊕ c)`; `k_b ≤ k_c ⟹ actionPoint(b ⊕ c) = k_b`; `k_c ≤ k_b ⟹ actionPoint(b ⊕ c) = k_c` (jointly characterizing `actionPoint(b ⊕ c)` by NAT-order trichotomy on `(k_b, k_c)`).

**Addition is not commutative.** The operands play asymmetric roles: the first is a *position*, the second a *displacement*. Gregory's `absadd` takes the prefix from the first argument and the suffix from the second.

**There is no multiplication or division.** Gregory's codebase analysis confirms: no `tumblermult`, no `tumblerdiv`. The arithmetic repertoire is add, subtract, increment, compare. Tumblers are addresses, not quantities.

**Tumbler differences are not counts.** Nelson: "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained." The difference between two addresses specifies boundaries, not cardinality. Between sibling addresses 3 and 7, document 5 may have arbitrarily many descendants; their count is unknowable from the addresses alone.

---

## TA-dom — DisplacementDominance

A named corollary exporting TumblerAdd's dominance-guarantee postcondition a ⊕ w ≥ w as a single labelled fact for
downstream use. Under the preconditions a ∈ T, w ∈ T, Pos(w), actionPoint(w) ≤ #a, TA-dom restates TumblerAdd's
fourth postcondition unchanged, so the per-step NAT-* sourcing (NAT-zero, NAT-order, NAT-addcompat, NAT-closure,
NAT-cancel, NAT-wellorder) for the case-split discharge of r ≥ w — the divergence sub-case routing through T1
case (i) at the least index j with aⱼ > 0, and the equality sub-case routing through T3 at the inner aₖ = 0
branch via NAT-closure's additive identity — lives inside TumblerAdd and is transitively sourced here. The chief
downstream consumer is TA4 (ReverseCancellation), whose Step 2 cites the dominance fact to discharge TumblerSub's
r ≥ w precondition. Dominance is carried by TumblerAdd's construction itself (the tail-copy rule forcing
rᵢ = wᵢ above the action point, and the action-point and prefix-copy regions together either matching or
exceeding w's components below and at k), so TA-dom is a theorem derived from TumblerAdd — not an independent
axiom excluding a below-displacement model.

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `Pos(w)`, `k ≤ #a` where `k` is the action point of `w`
- *Depends:*
  - TumblerAdd — sole arithmetic source; exports `a ⊕ w ≥ w (T1, T3)` as its fourth postcondition.
  - TA-Pos (PositiveTumbler) — licenses `Pos(w)` precondition and the existence of the action point.
  - ActionPoint — licenses `actionPoint(w) ≤ #a` precondition.
  - TA0 (WellDefinedAddition) — supplies `a ⊕ w ∈ T` (so T1's ordering applies on the left) and `#(a ⊕ w) = #w` (consumed by T3 in the equality case).
  - T1 (LexicographicOrder) — meaning of `≥` via `a ≥ b ⟺ b ≤ a` and `a ≤ b ⟺ a < b ∨ a = b`.
  - T3 (CanonicalRepresentation) — equality-from-component-agreement-and-equal-length, used when `aᵢ = 0` for all `i ≤ k`.
- *Postconditions:* `a ⊕ w ≥ w`

---

## TA-strict — StrictIncrease

A named corollary exporting TumblerAdd's ordering-guarantee postcondition a ⊕ w > a as a single labelled fact for
downstream use. Under the preconditions a ∈ T, Pos(w), actionPoint(w) ≤ #a, TA-strict restates TumblerAdd's third
postcondition unchanged, so the per-step NAT-* sourcing (NAT-addcompat, NAT-order, NAT-zero, NAT-closure) for the
rₖ > aₖ step lives inside TumblerAdd and is transitively sourced here. The chief downstream consumer is T12 span
well-definedness, whose non-emptiness branch cites TA-strict to establish s ∈ span(s, ℓ). Non-degeneracy of tumbler
addition is carried by TumblerAdd's definition itself (ActionPoint's wₖ ≥ 1 and the advance clause rₖ = aₖ + wₖ),
so TA-strict is a theorem derived from TumblerAdd — not an independent axiom excluding a no-op model.

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `Pos(w)`, `actionPoint(w) ≤ #a`
- *Depends:*
  - TumblerAdd (TumblerAdd) — ordering-guarantee postcondition `a ⊕ w > a (T1)` re-exported unchanged.
  - T0 (CarrierSetDefinition) — carrier `T` and length operator `#` in the quantifier range and precondition.
  - TA-Pos (PositiveTumbler) — precondition `Pos(w)`.
  - ActionPoint (ActionPoint) — precondition `actionPoint(w) ≤ #a`.
  - TA0 (WellDefinedAddition) — membership `a ⊕ w ∈ T` so T1's ordering applies to the left-hand side.
  - T1 (LexicographicOrder) — meaning of the strict ordering `>`.
- *Forward References:*
  - T12 (SpanWellDefinedness) — downstream user of this corollary; cites TA-strict for span well-definedness rather than TumblerAdd's full postcondition list.
- *Postconditions:* `a ⊕ w > a`

---

## TA0 — WellDefinedAddition

A named corollary exporting TumblerAdd's first two postconditions a ⊕ w ∈ T and #(a ⊕ w) = #w as a single labelled
well-definedness fact for downstream use. Under the preconditions a ∈ T, w ∈ T, Pos(w), actionPoint(w) ≤ #a, TA0
restates these two postconditions unchanged, so the per-step axioms TumblerAdd cites (T0 for the membership reassembly,
NAT-closure for closure of ℕ under addition at the action point, NAT-sub for the result-length-identity collapse, and
T0's length axiom for #w ≥ 1) live inside TumblerAdd and are transitively sourced here. The chief downstream consumers
are TA1, TA1-strict, TA-LC, TA-RC, TA-MTO, TA-assoc, TA4, TA7a, OrdinalShift, D0, D1, D2, Span, T12, and TS3 — every
property that needs "a ⊕ w is a tumbler of length #w" without the ordering or dominance guarantees and would otherwise
cherry-pick from TumblerAdd's four-postcondition list. The motivation for the precondition actionPoint(w) ≤ #a
belongs to TumblerAdd's construction; TA0's content is the labelled handle, not the construction-side argument.

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, Pos(w), actionPoint(w) ≤ #a
- *Depends:*
  - TumblerAdd (TumblerAdd, this ASN) — supplies `a ⊕ w ∈ T` and `#(a ⊕ w) = #w` as postconditions.
  - T0 (CarrierSetDefinition, this ASN) — supplies carrier `T` and length operator `#`.
  - TA-Pos (PositiveTumbler, this ASN) — precondition `Pos(w)` ensures the action point exists.
  - ActionPoint (ActionPoint, this ASN) — defines `actionPoint(w)` used in the bound `actionPoint(w) ≤ #a`.
  - NAT-order (NatStrictTotalOrder) — supplies the non-strict relation `≤` on ℕ appearing in the precondition `actionPoint(w) ≤ #a`.
- *Postconditions:* a ⊕ w ∈ T, #(a ⊕ w) = #w

---

## TA1-strict — StrictOrderPreservation

When the action point of the displacement lands at or after the divergence point of two strictly ordered positions, addition preserves strict order — the original ordering relationship survives intact. If the action point falls before the divergence, the two results collapse to equality; order degrades but never reverses.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, Pos(w), actionPoint(w) ≤ #a, actionPoint(w) ≤ #b, actionPoint(w) ≥ divergence(a, b)
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier `T`, length operator `#·`, component projection `·ᵢ` with components in ℕ.
  - T1 (LexicographicOrder) — irreflexivity; case (i) witness and agreement; case (ii) structure.
  - T3 (CanonicalRepresentation) — backs Divergence's exhaustiveness at the case-(ii) rule-out.
  - Divergence — supplies `j`, case (i) agreement and disagreement, case (ii) sub-case length structure.
  - TA-Pos (PositiveTumbler) — `Pos(w)` consumed by ActionPoint and TA0.
  - ActionPoint — fixes `k`; supplies `1 ≤ k ≤ #w`.
  - TA0 (WellDefinedAddition) — `a ⊕ w, b ⊕ w ∈ T`; length identity `#(a ⊕ w) = #w`.
  - TumblerAdd — constructive component-wise definition.
  - NAT-order (NatStrictTotalOrder) — trichotomy; defining clause `m ≤ n ⟺ m < n ∨ m = n`; transitivity of `<`; irreflexivity.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor `n < n + 1`; right order-compatibility `p ≤ n ⟹ p + m ≤ n + m`.
  - NAT-cancel (NatAdditionCancellation) — right cancellation `n + m = p + m ⟹ n = p`.
- *Postconditions:* a ⊕ w < b ⊕ w

---

## TA1 — OrderPreservationUnderAddition

Adding the same positive displacement to two ordered positions preserves their relative order weakly: a < b implies a ⊕ w ≤ b ⊕ w. This holds universally — regardless of where the action point falls relative to the divergence — so no ordering relationship can be reversed by a common advancement.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, Pos(w), actionPoint(w) ≤ #a, actionPoint(w) ≤ #b
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier `T`, length `#·`, component projection `·ᵢ`.
  - T1 (LexicographicOrder) — case analysis on `a < b`; case (i) concludes strict ordering of results.
  - T3 (CanonicalRepresentation) — component-wise agreement with equal length yields equality.
  - TA0 (WellDefinedAddition) — `a ⊕ w`, `b ⊕ w ∈ T` with length `#w`.
  - TumblerAdd (TumblerAdd) — three-region piecewise structure of `⊕`.
  - TA-Pos (PositiveTumbler, this ASN) — supplies `Pos(w)`.
  - ActionPoint (ActionPoint, this ASN) — defines `actionPoint(·)` and yields `1 ≤ k ≤ #w`.
  - NAT-order (NatStrictTotalOrder) — weakening `<` to `≤`, irreflexivity, and reconstructing strict `<` from `≤` plus non-equality.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — right order-compatibility lifts `aₖ ≤ bₖ` to `aₖ + wₖ ≤ bₖ + wₖ`.
  - NAT-cancel (NatAdditionCancellation) — right cancellation rules out `aₖ + wₖ = bₖ + wₖ`.
- *Postconditions:* a ⊕ w ≤ b ⊕ w

Strict order preservation holds under a tighter condition. We first need a precise notion of where two tumblers first differ.

---

## TA2 — WellDefinedSubtraction

Tumbler subtraction a ⊖ w is well-defined whenever a ≥ w, producing a valid tumbler whose length is L — the longer of
`#a` and `#w`, named by NAT-order trichotomy on `(#a, #w)` per TumblerSub's Definition rather than by a primitive
binary-maximum operator on ℕ. The result lies in T and correctly represents the displacement needed to reach a from w.

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, a ≥ w
- *Depends:*
  - TumblerSub (TumblerSub) — piecewise construction of `a ⊖ w`: zero-padding, divergence-based case split, componentwise definition, and result length `L`.
  - T0 (CarrierSetDefinition) — minimum-length `≥ 1`, component-typing in ℕ, and carrier-set membership criterion.
  - T1 (LexicographicOrder) — derives `a > w` from `a ≥ w ∧ a ≠ w`; supplies component-divergence and prefix cases at the divergence point.
  - T3 (CanonicalRepresentation) — `a = w` iff same length and components; used in a reductio at the divergence point: assuming `a = w` propagates equal lengths and native component equality, which under NAT-order's equality case on `(#a, #w)` extends via ZPD's padded-projection definition to padded equality on `[1, L]`, contradicting Case 2's padded divergence at `k`.
  - ZPD (ZeroPaddedDivergence) — minimality property identifying `k = zpd(a, w)` in both sub-cases.
  - NAT-sub (NatPartialSubtraction) — conditional-closure clause discharging `rₖ ∈ ℕ` once `âₖ ≥ ŵₖ` (instantiated on ZPD's padded projections so the operands are well-defined when `k > #w`).
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for literal zeros (pre-divergence components, ZPD's padded extension of `a` past `#a`, ZPD's padded extension of `w` past `#w`, and the zero tumbler of Case 1); lower bound `0 ≤ âₖ` for the `≠ 0 ⟹ > 0` step.
  - NAT-order (NatStrictTotalOrder) — trichotomy on `(#a, #w)` naming `L`; defining clause `m ≤ n ⟺ m < n ∨ m = n` used to convert strict inequalities into weak form for NAT-sub and to unfold `0 ≤ âₖ` in sub-case (ii).
- *Postconditions:* a ⊖ w ∈ T, #(a ⊖ w) = L where `L = #a` if `#a ≥ #w`, else `L = #w`.

---

## TA3-strict — OrderPreservationUnderSubtractionStrict

Subtracting a common lower bound from two equal-length ordered positions preserves strict order: if a < b and both dominate w with equal lengths, then a ⊖ w < b ⊖ w. The equal-length precondition is load-bearing — without it the piecewise subtraction could shift the divergence point in a way that collapses or reverses the ordering.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w, #a = #b
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier-set membership `a, b, w ∈ T`; length operator `#·`; native-domain component projection `·ᵢ ∈ ℕ` on `{1, ..., #·}`.
  - T1 (LexicographicOrder) — definition of `<`; ruling out case (ii) under `#a = #b`; first-divergence witness `j` with prefix agreement `aᵢ = bᵢ` for `i < j` and strict component inequality `aⱼ < bⱼ`; trichotomy disjointness clause `¬(a < b ∧ b < a)` discharging the contradiction in Setup that rules out `b` zero-padded-equal to `w`; case (i) producing `a ⊖ w < b ⊖ w` from each branch's first-disagreement witness.
  - TumblerSub (TumblerSub) — Definition of `x ⊖ w` on ZPD's padded projections (zero-padding, divergence discovery, three-region rule `r_i = 0` for `i < k`, `r_k = x̂_k − ŵ_k`, `r_i = x̂_i` for `i > k`); length postcondition `#(x ⊖ w) = L_{x,w}`; exported divergence-point inequality `x̂_{zpd(x,w)} > ŵ_{zpd(x,w)}` under `x ≥ w` — invoked in Case A applied to `(b, w)` after `j = zpd(b, w)` is identified, in Setup applied to `(a, w)` and `(b, w)` to supply `â_{d_a} > ŵ_{d_a}` and `b̂_{d_b} > ŵ_{d_b}` (well-typed regardless of whether the zpd index lies in either operand's native domain), in Case 1 Subcase `j = d` to discharge NAT-sub's `≥ ŵ_d` precondition for both operands via NAT-order, in Case 2 to contradict the lifted `â_{d_a} < ŵ_{d_a}`, and in Case 3 to supply NAT-sub's strict-positivity input `b̂_{d_b} > ŵ_{d_b}`.
  - ZPD (ZeroPaddedDivergence) — existence biconditional (`zpd(x, w)` defined iff `x` is not zero-padded-equal to `w`), establishing `d_a` and `d_b` defined; codomain `1 ≤ zpd ≤ L`; padded-projection equalities `âᵢ = aᵢ` for `1 ≤ i ≤ #a` and `b̂ᵢ = bᵢ` for `1 ≤ i ≤ #b` (symmetric clause `ŵᵢ = wᵢ` for `1 ≤ i ≤ #w`) lifting padded statements to native at indices in the native domain; padding clause `âᵢ = 0` for `#a < i ≤ L` (symmetric `b̂ᵢ = 0` clause) used in Setup to derive `d_a ≤ #a` and `d_b ≤ #b` directly: the supposition `d_a > #a` (resp. `d_b > #b`) with the codomain bound forces the padding-zone value `â_{d_a} = 0` (resp. `b̂_{d_b} = 0`), substituting into TumblerSub's `â_{d_a} > ŵ_{d_a}` (resp. `b̂_{d_b} > ŵ_{d_b}`) yields `ŵ < 0`, contradicting NAT-zero's lower bound; first-disagreement clause `âₖ ≠ ŵₖ` at `k = zpd(a, w)` (symmetric for `(b, w)`) supplying the divergence position's disagreement in Cases 2 and 3; pre-divergence agreement `âᵢ = ŵᵢ` for `1 ≤ i < zpd(a, w)` (symmetric for `(b, w)`) chained through `ŵ` to derive `aᵢ = bᵢ` on the pre-divergence range; minimality used in Case A to identify `j = zpd(b, w)` from the established `b̂ᵢ = ŵᵢ` for `i < j` and `b̂ⱼ ≠ ŵⱼ`.
  - TA2 (WellDefinedSubtraction) — `a ⊖ w, b ⊖ w ∈ T`.
  - NAT-sub (NatPartialSubtraction) — conditional closure of `â_d − ŵ_d`, `b̂_d − ŵ_d` in ℕ under `â_d, b̂_d ≥ ŵ_d` (Case 1 subcase `j = d`); strict monotonicity at `(â_d, b̂_d, ŵ_d)` deriving `â_d − ŵ_d < b̂_d − ŵ_d` from `â_d < b̂_d` with both `≥ ŵ_d` (Case 1 subcase `j = d`); strict positivity yielding `b̂_j − ŵ_j ≥ 1` from `b̂_j > ŵ_j` (Case A) and `b̂_{d_b} − ŵ_{d_b} ≥ 1` from `b̂_{d_b} > ŵ_{d_b}` (Case 3) — the residual `≥ 1`-to-`> 0` step is closed downstream by NAT-closure's Consequence `0 < 1` together with NAT-order's `≤`-definition and `<`-transitivity, not by NAT-sub itself. All NAT-sub invocations are stated on ZPD's padded projections so the operands lie in ℕ even when the divergence index exceeds either native domain.
  - NAT-zero (NatZeroMinimum) — `0 ∈ ℕ` for literal-zero result components and the zero-tumbler branch (Case A); padded operand values `âᵢ = 0` and `b̂ᵢ = 0` in the padding-zone derivations of Setup; lower bound `0 ≤ ŵ_{d_a}` (resp. `0 ≤ ŵ_{d_b}`) refuting `ŵ_{d_a} < 0` (resp. `ŵ_{d_b} < 0`) obtained by substituting the padding-zone `â_{d_a} = 0` (resp. `b̂_{d_b} = 0`) into TumblerSub's exported postcondition under the supposition `d_a > #a` (resp. `d_b > #b`).
  - NAT-order (NatStrictTotalOrder) — trichotomy at length pairs `(#a, #w)` and `(#b, #w)` selecting the same sub-case under `#a = #b`, hence naming `L = L_{a,w} = L_{b,w}`; trichotomy at index pair `(d_a, d_b)` for the three-way case split; trichotomy at `(d_a, #a)` and `(d_b, #b)` together with the defining clause `m ≤ n ⟺ m < n ∨ m = n` closing the `d_a ≤ #a` and `d_b ≤ #b` arguments after their `>` branches are refuted; trichotomy at `(#a, #a + 1)` together with the `≤`-defining clause refuting `#a + 1 ≤ #a` in *The form of `a < b`* — both branches `#a + 1 < #a` and `#a + 1 = #a` are excluded by trichotomy given NAT-addcompat's `#a < #a + 1`; `>` definition `m > n ⟺ n < m` unfolding `0 > ŵ_{d_a}` (resp. `0 > ŵ_{d_b}`) to `ŵ_{d_a} < 0` (resp. `ŵ_{d_b} < 0`) in Setup, unfolding TumblerSub's `â_{d_a} > ŵ_{d_a}` to `ŵ_{d_a} < â_{d_a}` in Case 2, and folding `0 < b̂_j − ŵ_j` to `b̂_j − ŵ_j > 0` (resp. `0 < b̂_{d_b} − ŵ_{d_b}` to `b̂_{d_b} − ŵ_{d_b} > 0`) at the conclusion of the `≥ 1`-to-`> 0` bridges in Cases A and 3; defining clause `≤ ⟺ < ∨ =` converting TumblerSub's strict `>` to NAT-sub's `≥` precondition (Case 1 subcase `j = d`), and splitting NAT-sub's strict-positivity output `1 ≤ b̂_j − ŵ_j` (Case A) and `1 ≤ b̂_{d_b} − ŵ_{d_b}` (Case 3) into a `<` branch and an `=` branch for the bridge to `> 0`; `<`-transitivity at `(0, 1, b̂_j − ŵ_j)` (Case A) and `(0, 1, b̂_{d_b} − ŵ_{d_b})` (Case 3) chaining NAT-closure's `0 < 1` with the `<` branch of the split to deliver `0 < b̂_j − ŵ_j` (resp. `0 < b̂_{d_b} − ŵ_{d_b}`); disjointness-of-`<`-and-`=` at `(ŵⱼ, b̂ⱼ)` (Case A, converting `ŵⱼ < b̂ⱼ` to `b̂ⱼ ≠ ŵⱼ` on ZPD's padded projections) and at `(aⱼ, bⱼ)` (Case 1, converting `aⱼ < bⱼ` to `aⱼ ≠ bⱼ` to refute `j < d`); exactly-one-trichotomy clause `¬(x < y ∧ y < x)` at `(â_{d_a}, ŵ_{d_a})` (Case 2) ruling out the conjunction of `â_{d_a} < ŵ_{d_a}` and `ŵ_{d_a} < â_{d_a}`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies the Consequence `0 < 1`, used in Cases A and 3 to bridge from NAT-sub's strict-positivity output `b̂_j − ŵ_j ≥ 1` (resp. `b̂_{d_b} − ŵ_{d_b} ≥ 1`) to the strict-positive form `b̂_j − ŵ_j > 0` (resp. `b̂_{d_b} − ŵ_{d_b} > 0`) required to apply T1 case (i): the bridge `0 < 1 ≤ b̂_j − ŵ_j ⟹ 0 < b̂_j − ŵ_j` combines NAT-closure's `0 < 1` with NAT-order's mixed `< ≤` transitivity (the `≤`-definition splits `1 ≤ b̂_j − ŵ_j` into `1 < b̂_j − ŵ_j ∨ 1 = b̂_j − ŵ_j`, the `<` branch closes by NAT-order's `<`-transitivity chained with `0 < 1`, the `=` branch closes by indiscernibility of `=` substituting into `0 < 1`), and analogously for `(0, 1, b̂_{d_b} − ŵ_{d_b})`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality `n < n + 1` at `n := #a`, used in *The form of `a < b`* to rule out T1 case (ii) under `#a = #b`: T1(ii)'s clause `k = #a + 1 ≤ #b` substitutes via `#a = #b` to `#a + 1 ≤ #a`, whose `≤`-expansion `#a + 1 < #a ∨ #a + 1 = #a` is excluded in both branches by NAT-order's trichotomy at `(#a, #a + 1)` given NAT-addcompat's `#a < #a + 1`, so case (ii) is impossible.
- *Postconditions:* a ⊖ w < b ⊖ w

---

## TA3 — OrderPreservationUnderSubtractionWeak

Tumbler subtraction preserves weak order: if a < b and both addresses are at least as large as the subtrahend w, then subtracting w from a yields a result no greater than subtracting w from b. The guarantee is weak (≤ rather than strict <) because equal results are possible when a and b diverge only below the subtraction point.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w
- *Depends:*
  - TA2 (WellDefinedSubtraction) — `a ⊖ w, b ⊖ w ∈ T`; result components in ℕ.
  - TumblerSub (TumblerSub) — component-wise subtraction definition: zero-padding, three-phase formula, length-pair dispatch naming `L_{x,w}`; exported postcondition that when `zpd(x, w)` is defined, `x̂_{zpd(x,w)} > ŵ_{zpd(x,w)}` holds on ZPD's padded projections — invoked in Sub-case A2 applied to `(a, w)` and `(b, w)` to supply `â_d > ŵ_d` and `b̂_d > ŵ_d` (well-typed regardless of whether `d` exceeds `#w` in the prefix-divergence sub-case) for NAT-sub's `≥ ŵ_d` precondition via NAT-order, in the preamble to Sub-cases B2–B4 to supply `â_{dₐ} > ŵ_{dₐ}`, in Sub-case B2 (the `j = d` branch) to discharge NAT-sub's `≥ ŵ_d` precondition for both operands via NAT-order, in Sub-case B3 to contradict `â_{dₐ} < ŵ_{dₐ}`, and in Sub-case B4 applied to `(b, w)` for the strict divergence-point inequality `b̂_{d_b} > ŵ_{d_b}`; conditional postcondition `Pos(x ⊖ w)` when `zpd(x, w)` is defined — used in Sub-cases A1, A3, and B1 to conclude `b ⊖ w` is positive from the existence of zero-padded divergence.
  - ZPD (ZeroPaddedDivergence) — existence biconditional, first-position characterisation, pre-zpd agreement; codomain `zpd(a, w) ∈ {1, ..., L}` and padding clause `âᵢ = 0` for `#a < i ≤ L` (with the symmetric `b̂` clause for the `(b, w)` case) used in Sub-case A2 and Case B's preamble to derive `dₐ ≤ #a` (resp. `d_b ≤ #b`) directly: the supposition `dₐ > #a` (resp. `d_b > #b`) with the codomain bound forces the padding-zone value `â_{dₐ} = 0` (resp. `b̂_{d_b} = 0`), substituting into TumblerSub's `â_{dₐ} > ŵ_{dₐ}` (resp. `b̂_{d_b} > ŵ_{d_b}`) yields `ŵ < 0`, contradicting NAT-zero's lower bound.
  - T1 (LexicographicOrder) — strict ordering `<` and derived `≤`; case (i) shared-position bound in conjunction form, supplying Case B's witness `j ≤ #a ∧ j ≤ #b ∧ aⱼ < bⱼ` and used in Case B's preamble sub-case (i) of the `(b, w)` not-zero-padded-equal proof to introduce `a < w` from witness `j` against `a ≥ w`; case (ii) prefix characterisation framing Case A and supplying the successor witness for the `a ⊖ w < b ⊖ w` length-comparisons in Sub-cases A1 and A3; trichotomy clause `¬(a < b ∧ b ≤ a)` discharges the `a < w ∧ a ≥ w` contradiction in Case B's preamble sub-case (i).
  - T3 (CanonicalRepresentation) — equality from component-wise agreement at equal length in Sub-case A2's `L_{a,w} = L_{b,w}` branch.
  - TA-Pos (PositiveTumbler) — `Pos(t)` and `Zero(t)` predicates for framing zero-tumbler and positive results of subtractions in Sub-cases A1, A3, B1.
  - TA-PosDom (PositiveDominatesZero) — a zero tumbler is strictly less than any positive tumbler; used in Sub-cases A1, A3, B1.
  - NAT-sub (NatPartialSubtraction) — conditional closure, strict monotonicity (B2's `j = d` branch), strict positivity (B4).
  - NAT-zero (NatZeroMinimum) — `0 ∈ ℕ` for padded components and literal-zero result components; lower bound at `(b ⊖ w)_p` in Sub-case A2's `≠ 0 ⟹ > 0` step; lower bound `0 ≤ aⱼ` in Case B's preamble sub-case (ii) to refute `aⱼ < 0`; lower bound `0 ≤ ŵ_{dₐ}` (resp. `0 ≤ ŵ_{d_b}`) in Sub-case A2 and Case B's preamble to refute `ŵ_{dₐ} < 0` (resp. `ŵ_{d_b} < 0`) obtained by substituting the padding-zone `â_{dₐ} = 0` (resp. `b̂_{d_b} = 0`) into TumblerSub's exported postcondition under the supposition `dₐ > #a` (resp. `d_b > #b`).
  - NAT-order (NatStrictTotalOrder) — trichotomy at `(#a, #w)`, `(#b, #w)`, `(L_{a,w}, L_{b,w})`, `(dₐ, d_b)`, `(j, #w)`, `(dₐ, #a)`, `(d_b, #b)` (the latter two close out the `dₐ ≤ #a` and `d_b ≤ #b` derivations in Sub-case A2 and Case B's preamble after `¬(dₐ > #a)` and `¬(d_b > #b)` are established); defining clause `m ≤ n ⟺ m < n ∨ m = n` for ≥/> conversions and the `≠ 0 ⟹ > 0` step; `>` definition `m > n ⟺ n < m` unfolding `0 > ŵ_{dₐ}` (resp. `0 > ŵ_{d_b}`) to `ŵ_{dₐ} < 0` (resp. `ŵ_{d_b} < 0`) in Sub-case A2 and Case B's preamble; disjointness-of-`<`-and-`=` at `(wⱼ, bⱼ)` and `(0, bⱼ)` in Sub-case B1; trichotomy disjointness composing the derived `ŵ < 0` against NAT-zero's `0 ≤ ŵ` to close out the `dₐ ≤ #a` and `d_b ≤ #b` arguments; transitivity composing length and divergence-position bounds.
  - NAT-discrete (NatDiscreteness) — forward direction `m < n ⟹ m + 1 ≤ n` supplying T1 case (ii)'s successor witness at `(#a, #b)` in A1 and A3, and at `(L_{a,w}, L_{b,w})` in A2.
  - NAT-closure (NatArithmeticClosureAndIdentity) — addition closure instantiated at `(n, 1)` with `1 ∈ ℕ` from the same axiom places `n + 1 ∈ ℕ` for the T1 case (ii) witnesses formed in A1, A2, A3.
- *Postconditions:* a ⊖ w ≤ b ⊖ w

---

## TA4 — PartialInverse

Tumbler addition and subtraction are partial inverses only under tight structural conditions: (a ⊕ w) ⊖ w = a holds exactly when the action point of w coincides with the last position of a and all components of a before that position are zero. The restriction is necessary because addition discards the trailing structure of its first argument below the action point, making recovery impossible in the general case.

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `Pos(w)`, `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`, where `k` is the action point of `w`
- *Depends:*
  - TA-Pos (PositiveTumbler) — guarantees action point exists from `Pos(w)`
  - ActionPoint (ActionPoint) — defines `k` as least position with `wᵢ > 0`; `wᵢ = 0` for `i < k`
  - TumblerAdd (TumblerAdd) — three-region construction of `a ⊕ w`; dominance postcondition `r ≥ w`
  - TA0 (WellDefinedAddition) — applicability precondition `k ≤ #a`; result-length identity `#r = #w`
  - TumblerSub (TumblerSub) — three-region construction of `r ⊖ w`; no-divergence zero-tumbler branch
  - T0 (CarrierSetDefinition) — carrier `T`, length `#`, component typing `aᵢ ∈ ℕ`
  - T1 (LexicographicOrder) — `≥` comparison for TumblerSub's precondition
  - T3 (CanonicalRepresentation) — componentwise and length equality imply tumbler equality
  - ZPD (ZPD) — case-split (undefined when padded projections agree); minimality at first disagreement
  - NAT-closure (NatArithmeticClosureAndIdentity) — additive identity `0 + n = n`
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — right order-compatibility `p ≤ n ⟹ p + m ≤ n + m`
  - NAT-cancel (NatAdditionCancellation) — symmetric summand absorption `n + m = m ⟹ n = 0`
  - NAT-zero (NatZeroMinimum) — lower bound `0 ≤ n` for `n ∈ ℕ`
  - NAT-order (NatStrictTotalOrder) — trichotomy on length pair; defining clause `≤ ⟺ < ∨ =`; irreflexivity
  - NAT-sub (NatPartialSubtraction) — right-telescoping `(m + n) − n = m`
- *Postconditions:* `(a ⊕ w) ⊖ w = a`

---

## TA5-SIG — LastSignificantPosition

Defines sig(t) as the index of the rightmost nonzero component of tumbler t; for an all-zero tumbler, sig(t) = #t by convention. The result always satisfies 1 ≤ sig(t) ≤ #t, giving a well-defined handle on where a tumbler's significant content ends.

*Formal Contract:*
- *Preconditions:* `t ∈ T` (any tumbler with `#t ≥ 1`).
- *Definition:* `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})` when `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`; `sig(t) = #t` when `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies `t ∈ T` as finite ℕ-sequences with `#t ≥ 1`, component projection `tᵢ`, and the length `#t`.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` appearing in the set-comprehension condition `tᵢ ≠ 0` of the nonzero-case definition `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})` and in the all-zero condition `(A i : 1 ≤ i ≤ #t : tᵢ = 0)` of the all-zero-case definition.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` and closure of ℕ under addition.
  - NAT-wellorder (NatWellOrdering) — supplies the least-element principle.
  - NAT-order (NatStrictTotalOrder) — supplies the `≤`-defining clause `p ≤ q ⟺ p < q ∨ p = q`, transitivity of `<`, and the exactly-one trichotomy mutual-exclusion clauses `¬(m < n ∧ n < m)`, `¬(m < n ∧ m = n)`, `¬(m = n ∧ n < m)` — used to derive antisymmetry of `≤` from `m ≤ m' ∧ m' ≤ m`, hence uniqueness of the least element of `U`.
  - NAT-discrete (NatDiscreteness) — supplies the forward direction `i < m ⟹ i + 1 ≤ m`.
  - NAT-sub (NatPartialSubtraction) — supplies conditional closure `m ≥ 1 ⟹ m − 1 ∈ ℕ`, the right-inverse `(m − 1) + 1 = m`, the right-telescoping clause `(i + 1) − 1 = i`, and strict monotonicity at `p = 1`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — supplies the strict successor inequality `(A n ∈ ℕ :: n < n + 1)`.
- *Postconditions:* `1 ≤ sig(t) ≤ #t`.

---

## TA5-SigValid — SigOnValidAddresses

For any valid address satisfying T4, the signature function sig(t) equals the length of the tumbler — that is, the last component is always the rightmost nonzero position. This follows directly from T4's field-segment constraint, which forbids a zero final component.

*Formal Contract:*
- *Preconditions:* `t` satisfies T4.
- *Depends:*
  - T4 (HierarchicalParsing) — supplies `t_{#t} ≠ 0`.
  - T0 (CarrierSetDefinition) — fixes carrier as ℕ, giving `t_{#t} ∈ ℕ`, and supplies `#t ≥ 1` for every `t ∈ T`.
  - NAT-zero (NatZeroMinimum) — supplies the disjunction `0 < t_{#t} ∨ 0 = t_{#t}`; T4's `t_{#t} ≠ 0` eliminates the equality branch, yielding `0 < t_{#t}`.
  - NAT-order (NatStrictTotalOrder) — supplies the `≤`-defining clause `m ≤ n ⟺ m < n ∨ m = n`, used (a) to interpret TA5-SIG's range predicate `1 ≤ i ≤ #t` and the postcondition `sig(t) ≤ #t`, (b) to witness `1 ≤ #t ≤ #t` (hence `#t ∈ S`); supplies antisymmetry of `≤` — derived from the exactly-one trichotomy clauses `¬(m < n ∧ n < m)`, `¬(m < n ∧ m = n)`, `¬(m = n ∧ n < m)` — to combine `sig(t) ≥ #t` and `sig(t) ≤ #t` into `sig(t) = #t`.
  - TA5-SIG (LastSignificantPosition) — unfolds `sig(t)` as the maximum-position formula when `t_{#t} > 0` and supplies the range postcondition `sig(t) ≤ #t`.
- *Postconditions:* `sig(t) = #t`.

---

## TA5 — HierarchicalIncrement

The increment operation inc(t, k) produces a new address strictly greater than t under lexicographic order: k = 0 advances the rightmost nonzero component to yield the next peer at the same depth, while k > 0 appends k new components to yield a child address at depth k below t. For valid addresses, inc(t, 0) produces the next sibling; inc(t, k) for k > 0 produces a descendant, with t's zero-extension subtree lying strictly between t and the result.

*Formal Contract:*
- *Preconditions:* `t ∈ T`, `k ≥ 0`.
- *Definition:* `inc(t, k)`: when `k = 0`, modify position `sig(t)` (TA5-SIG) to `t_{sig(t)} + 1`; when `k > 0`, extend by `k` positions with `k - 1` zeros and final `1`.
- *Depends:*
  - T0 (CarrierSetDefinition) — characterisation of `T` as finite ℕ-sequences of length ≥ 1; discharges `t' ∈ T`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — addition closure instantiated at `(t_{sig(t)}, 1)` gives `t_{sig(t)} + 1 ∈ ℕ`, and at `(0, 1)` gives `0 + 1 ∈ ℕ`, with `1 ∈ ℕ` from the same axiom; the left-identity clause `0 + n = n` instantiated at `n = 1` rewrites NAT-discrete's consequent `0 + 1 ≤ k` to `1 ≤ k` in Case `k > 0`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality `n < n + 1` for Case `k = 0`; left order-compatibility `1 ≤ k ⟹ #t + 1 ≤ #t + k` for Case `k > 0`.
  - NAT-zero (NatZeroMinimum) — `0 ∈ ℕ` supplies both the literal value of the `k − 1` field separators and the legal `m`-value for instantiating NAT-discrete at `m = 0`.
  - NAT-discrete (NatDiscreteness) — instantiated at `m = 0`, `n = k`; the strict antecedent `0 < k` is the case hypothesis itself, so the axiom yields `0 + 1 ≤ k`, which NAT-closure's left identity rewrites to `1 ≤ k`.
  - T1 (LexicographicOrder) — case (i) at divergence position `sig(t)` for `k = 0`; case (ii) with proper-prefix `#t + 1 ≤ #t'` for `k > 0`.
  - TA5-SIG (LastSignificantPosition) — resolves `sig(t)` in the definition and postconditions (b), (c).
- *Forward References:*
  - TA5-SigValid (SigOnValidAddresses) — refines TA5 to T4-valid inputs, establishing `sig(t) = #t`; TA5 names it to explain the valid-address consequence of `inc(t, 0)`.
  - TA5a (IncrementPreservesT4) — elaborates TA5 by establishing the precise T4-preservation conditions for `inc(t, k)`; TA5 names it as the downstream analysis site.
  - T4 (HierarchicalParsing) — named in the prose as the validity predicate that TA5-SigValid requires and TA5a analyzes; TA5's own proof does not invoke T4.
- *Postconditions:* `t' ∈ T`. (a) `t' > t` under T1. (b) When `k = 0`: `(A i : 1 ≤ i ≤ #t ∧ i ≠ sig(t) : t'ᵢ = tᵢ)`. When `k > 0`: `(A i : 1 ≤ i ≤ #t : t'ᵢ = tᵢ)`. (c) When `k = 0`: `#t' = #t`, `t'_{sig(t)} = t_{sig(t)} + 1`. (d) When `k > 0`: `#t' = #t + k`, positions `#t + 1 ... #t + k - 1` are `0`, position `#t + k` is `1`.

`inc(t, 0)` does not produce the immediate successor of `t` in the total order. It produces the smallest same-length tumbler that agrees with `t` on positions `1, ..., sig(t) − 1` and has a strictly larger component at position `sig(t)`. When `sig(t) = #t` (which holds for valid addresses by TA5-SigValid), this is the next peer at the same hierarchical depth. When `sig(t) < #t`, same-length tumblers lie between `t` and `inc(t, 0)` — for example, `(2, 0, 1)` lies between `(2, 0, 0)` and `inc((2, 0, 0), 0) = (3, 0, 0)`. The gap between `t` and `inc(t, 0)` contains the entire subtree of `t`: all tumblers `t.x₁. ... .xₘ`. The true immediate successor in the total order is `t.0` by T1 case (ii).

For `k > 0`, `inc(t, k)` likewise does not produce the immediate successor: for `k = 1` the result is `t.1`; for `k = 2` the result is `t.0.1`. In both cases `t.0` lies strictly between `t` and the result. For address allocation this is harmless: allocation advances the counter past all existing addresses.

The conditions under which `inc` preserves T4 are established in TA5a: `inc(t, k)` preserves T4 iff `k ∈ {0, 1}`, or `k = 2` with `zeros(t) ≤ 2`; for `k ≥ 3`, `inc(t, k)` violates T4 by introducing adjacent zero separators.

| Label | Statement | Status |
|-------|-----------|--------|
| TA5 | `inc(t, k)` produces `t' > t` with same-length structure for `k = 0` (sibling) and extended structure for `k > 0` (child) | proved (this property) |
| TA5-SIG | `sig(t)` is the rightmost nonzero component position of `t`, or `#t` when all components are zero | definition (separate property) |
| TA5-SigValid | For every valid address satisfying T4, `sig(t) = #t` | proved (separate property) |
| TA5a | `inc(t, k)` preserves T4 iff `k ∈ {0, 1}`, or `k = 2 ∧ zeros(t) ≤ 2`; violated for `k ≥ 3` | proved (separate property) |

---

## TA5a — IncrementPreservesT4

The increment operation inc(t, k) produces a valid address (satisfying T4) if and only if k ∈ {0, 1}, or k = 2 with at most two existing zero components; for k ≥ 3 the result always violates T4 because the appended separator zeros create an adjacent-zero or empty-field violation. The k = 1 branch carries no extra zero-count side condition beyond T4-validity of t, since inc(·, 1) is zero-separator-neutral. This gives the precise depth limit for child allocation from any given valid address.

*Formal Contract:*
- *Precondition:* `t` satisfies T4; `k ≥ 0`.
- *Depends:*
  - T4 (HierarchicalParsing) — the four positional clauses being checked; cardinality bound `zeros(·) ≤ 3` (i) used on `t` (`zeros(t) ≤ 3`) and lifted to `t'` (`zeros(t') ≤ 3`) via the established `zeros(t') = zeros(t)` at cases `k = 0` and `k = 1`, and (at case `k = 2`) used to read off the iff threshold from `zeros(t') = zeros(t) + 1 ≤ 3`, i.e., `zeros(t) ≤ 2`; boundary clause `t_{#t} ≠ 0` (iv) used at case `k = 0` (via TA5-SigValid's `sig(t) = #t`) to give `t_{sig(t)} ≠ 0`, which excludes position `sig(t)` from the original zero-index set in the zero-index-set equality argument (the primed exclusion at the same position is supplied independently by TA5(c)'s `t'_{sig(t)} = t_{sig(t)} + 1` and the NAT chain `t_{sig(t)} + 1 ≠ 0`), and at cases `k = 1` and `k = 2` to falsify the left conjunct of T4(ii) on `t'` at the boundary index `i = #t`; left-boundary clause `t₁ ≠ 0` (iii) on `t` transferred to `t'₁ ≠ 0` in cases `k = 1, 2` (via TA5(b) at position `1`) and in the `sig(t) ≠ 1` sub-case of `k = 0` (same route), with the `sig(t) = 1` sub-case of `k = 0` deriving `t'₁ ≠ 0` from the NAT chain at position `1`; the no-adjacent-zeros clause T4(ii) on `t`, instantiated at index `i` with `1 ≤ i < #t`, is transferred to `t'` in the `sig(t) ∉ {i, i + 1}` sub-case of `k = 0` and in the interior branch `1 ≤ i < #t` of cases `k = 1` and `k = 2`, via TA5(b) agreement at `i` and `i + 1`; the same clause T4(ii), instantiated at `i = #t + 1` on `t'`, is the directly violated clause at `k ≥ 3`.
  - T0 (CarrierSetDefinition) — fixes carrier ℕ so every `tᵢ ∈ ℕ`; supplies `1 ≤ #t` (each tumbler has at least one component), used at four sites: in the `sig(t) ≠ 1` sub-case of case `k = 0` and in cases `k = 1` and `k = 2`, to discharge the legality of the `i = 1` instantiation of TA5(b)'s original-position agreement `(A i : 1 ≤ i ≤ #t : t'ᵢ = tᵢ)` for the T4(iii) transfer `t'₁ = t₁`; and at case `k ≥ 3`, to discharge the lower bound `1 ≤ #t + 1` for the T4(ii) instantiation index.
  - NAT-zero (NatZeroMinimum) — lower bound `0 ≤ n` on ℕ.
  - NAT-closure (NatArithmeticClosureAndIdentity) — addition closure instantiated at `(t_{sig(t)}, 1)` with `1 ∈ ℕ` from the same axiom places `t_{sig(t)} + 1 ∈ ℕ` at case `k = 0`. At case `k ≥ 3`, closure is consumed at the manipulated sums so the cited NAT-addcompat strict-successor and left-order-compatibility instantiations and the NAT-addassoc identification stay within signature: closure at `(#t, 1)` places `#t + 1 ∈ ℕ`, typing NAT-addcompat's strict-successor conclusion at `n = #t` (`#t < #t + 1`) as a comparison between ℕ-elements, supporting T0's `1 ≤ #t` chained via NAT-order's transitivity with that successor to give `1 ≤ #t + 1` between ℕ-elements, and admitting NAT-addcompat's strict-successor instantiation at `n = #t + 1`; closure at `(#t, 2)` places `#t + 2 ∈ ℕ`, typing the strict-successor inequality `#t + 1 < #t + 2` and NAT-addcompat's left-order-compatibility conclusion `#t + 2 ≤ #t + k` as comparisons between ℕ-elements; closure at `(#t, k)` places `#t + k ∈ ℕ`, matching TA5(d)'s `#t' = #t + k` so the chain `#t + 1 < #t + 2 ≤ #t + k = #t'` stays within ℕ; closure at `(#t + 1, 1)` places `(#t + 1) + 1 ∈ ℕ` and closure at `(1, 1)` places `1 + 1 ∈ ℕ`, so NAT-addassoc's identification `(#t + 1) + 1 = #t + (1 + 1) = #t + 2` chains through ℕ-elements at every term.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality `n < n + 1` at case `k = 0`; at case `k ≥ 3`, strict successor at `n = #t` lifts T0's `1 ≤ #t` to `1 ≤ #t + 1`, strict successor at `n = #t + 1` and `n = 2` participate in the chain `#t + 1 < #t + 2` (via NAT-addassoc) and `2 < 3 ≤ k` respectively, and left order compatibility `(A m, n, p ∈ ℕ : p ≤ n : m + p ≤ m + n)` at `(m, p, n) = (#t, 2, k)` lifts `2 ≤ k` to `#t + 2 ≤ #t + k`.
  - NAT-addassoc (NatAdditionAssociative) — at case `k ≥ 3`, identifies `(#t + 1) + 1 = #t + (1 + 1) = #t + 2` so that NAT-addcompat's strict successor inequality at `n = #t + 1` reads as `#t + 1 < #t + 2`; the same identification supplies the successor index `(#t + 1) + 1 = #t + 2` for the T4(ii) instantiation at `i = #t + 1`, against which `t'_{#t+2} = 0` is matched.
  - NAT-order (NatStrictTotalOrder) — at case `k = 0`, transitivity chains NAT-addcompat's strict successor inequality `t_{sig(t)} + 1 > t_{sig(t)}` with NAT-zero's lower bound `t_{sig(t)} ≥ 0` to give `t_{sig(t)} + 1 > 0`, and irreflexivity (equivalently, the exactly-one trichotomy clause `¬(m < n ∧ m = n)` derived from irreflexivity, which routes `> 0` to `≠ 0`) lifts `t_{sig(t)} + 1 > 0` to `t_{sig(t)} + 1 ≠ 0`; the resulting `≠ 0` conclusion is consumed at four sites within the case — the zero-index set equality's primed exclusion at position `sig(t)` (combining with TA5(c)'s `t'_{sig(t)} = t_{sig(t)} + 1` to give `t'_{sig(t)} ≠ 0`), T4(ii)'s `i + 1 = sig(t) = #t` sub-branch (combining with TA5(c)'s `t'_{sig(t)} = t_{sig(t)} + 1` at position `i + 1` to falsify `t'ᵢ₊₁ = 0`), T4(iv)'s discharge (combining with TA5(c)'s `t'_{sig(t)} = t_{sig(t)} + 1` and TA5-SigValid's `sig(t) = #t` to give `t'_{#t'} ≠ 0`), and T4(iii)'s `sig(t) = 1` sub-case (where reusing the chain at position `1` gives `t'₁ ≠ 0`). At case `k ≥ 3`, at-least-one trichotomy (via the `≤` definition unfolding `3 ≤ k` to `3 < k ∨ 3 = k`) splits `k ≥ 3` into the sub-branches `k = 3` and `3 < k`; the same `≤` definition lifts `2 < k − 1` to `2 ≤ k − 1` (i.e., `k − 1 ≥ 2`) in the `3 < k` sub-branch, and lifts `2 < 3` to `2 ≤ 3` (chained with `3 ≤ k` via transitivity to give `2 ≤ k`); transitivity additionally chains `1 ≤ #t < #t + 1` (giving `1 ≤ #t + 1`) and `#t + 1 < #t + 2 ≤ #t + k = #t'` (giving `#t + 1 < #t'`).
  - NAT-sub (NatPartialSubtraction) — conditional closure at `k ≥ 1` places `k − 1 ∈ ℕ`; right telescoping at `(m, n) = (2, 1)` gives `3 − 1 = 2` (used directly in sub-branch `k = 3` and to rewrite the left side of the strict-monotonicity conclusion in sub-branch `3 < k`); strict monotonicity at `(m, n, p) = (3, k, 1)` gives `3 − 1 < k − 1` in sub-branch `3 < k`; together these derive `k − 1 ≥ 2` at case `k ≥ 3`.
  - NAT-card (NatFiniteSetCardinality) — well-definedness of `|·|` as a total function on subsets of every initial segment `{1, …, n} ⊆ ℕ` lifts set-equality of zero-index subsets to cardinality equality at cases `k = 0` (subsets of `{1, …, #t}`) and `k = 1` (subsets of `{1, …, #t + 1}`); the enumeration characterisation, applied at `n = #t + 2`, lifts the disjoint extension `S' = S ∪ {#t + 1}` (with `#t + 1` strictly greater than every element of `S`) to `|S'| = |S| + 1` at case `k = 2`.
  - TA5 (HierarchicalIncrement) — TA5(b) agreement clauses; TA5(c) for `k = 0`; TA5(d) for `k ≥ 1`.
  - TA5-SigValid (SigOnValidAddresses) — `sig(t) = #t` on T4-valid `t` at case `k = 0`.
- *Guarantee:* `inc(t, k)` satisfies T4 iff `k ∈ {0, 1}`, or `k = 2 ∧ zeros(t) ≤ 2`.
- *Failure:* The Guarantee's iff yields two failure regions on the precondition domain (`t` satisfies T4, so `zeros(t) ∈ {0, 1, 2, 3}` by T4(i); `k ∈ ℕ`): (a) `k ≥ 3`, and (b) `k = 2 ∧ zeros(t) = 3`. In mode (a), T4(ii) on `t'` is the directly violated conjunct: by TA5(d) and the established `k − 1 ≥ 2`, the appended separator zeros at positions `#t + 1` and `#t + 2` are adjacent indices of `t'` carrying zero, so T4(ii) instantiated at `i = #t + 1` fails on `t'`. In mode (b), T4(i) on `t'` is the directly violated conjunct: by Case `k = 2` of the proof, `zeros(t') = zeros(t) + 1`, so the precondition `zeros(t) = 3` (admitted by T4(i) on `t`) yields `zeros(t') = 4`, exceeding the bound `zeros(·) ≤ 3` required by T4(i).

---

## TA6 — ZeroTumblers

No tumbler with `Zero(t)` is a valid address — every zero tumbler is excluded by the boundary rule T4 enforces on
first components. The companion ordering fact (every zero tumbler is strictly below every positive tumbler under T1)
is stated and proved once at TA-PosDom; this claim cites TA-Pos only to fix the `Zero` predicate's meaning.

*Formal Contract:*
- *Depends:*
  - T0 (CarrierSetDefinition) — `#t ≥ 1` and components in ℕ.
  - T4 (HierarchicalParsing) — boundary clause `t₁ ≠ 0`.
  - TA-Pos (PositiveTumbler) — definition of `Zero(t)`.
- *Forward References:*
  - TA-PosDom (PositiveDominatesZero) — uses zero tumblers as the dominated class in its ordering result; TA6 sentinels are the context for that pairing.
- *Postcondition:* `(A t ∈ T : Zero(t) ⟹ t is not a valid address)`.

Zero tumblers thus exist in `T` but lie outside the address-valid subset; paired with TA-PosDom's ordering result they act as sentinels — uninitialized markers, unbounded span endpoints, and lower bounds.

---

## TA7a.1 — SubspaceLengthResidue

Characterises the length-overflow residue of `⊖`: when `#w > #o` under the
other preconditions of TA7a's subtraction conjunct, the result lies in
`T \ S` because zero-padding of the minuend places `r_{#w} = 0`, violating
the universal positivity clause of **S**.

*Formal Contract:*
- *Preconditions:* `o ∈ S`, `w ∈ T`, `Pos(w)`, `o ≥ w`, `#w > #o`.
- *Depends:*
  - TA7a (SubspaceClosure) — parent claim defining **S** and establishing the complementary in-S branch whose precondition `#w ≤ #o` this sub-claim negates.
  - T0 (CarrierSetDefinition) — carrier `T`, length `#`, ℕ-typed components.
  - T1 (LexicographicOrder) — prefix-relationship case (ii) rules out `d > #o` and also the padded-sequences-agree-everywhere case, both by deriving `o < w` against `o ≥ w`.
  - T3 (CanonicalRepresentation) — length clause `#o ≠ #w ⟹ o ≠ w` supports the disagreement argument.
  - TA-Pos (PositiveTumbler) — `Pos(w)` precondition; **S** complement referenced in the postcondition.
  - TA2 (WellDefinedSubtraction) — delivers `o ⊖ w ∈ T`.
  - TumblerSub (TumblerSub) — zero-padding under NAT-order trichotomy, ZPD-based dispatch, and componentwise formula — in particular `rᵢ = oᵢ` (zero-padded) for `i > d` which places `r_{#w} = 0`.
  - ZPD (ZeroPaddedDivergence) — minimality of `zpd(o, w)`.
  - NAT-order (NatStrictTotalOrder) — trichotomy on `(#o, #w)` selects sub-case (β) with `L = #w`.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the padding positions `#o < i ≤ #w`.
- *Postcondition:* `o ⊖ w ∈ T \ S`, with `r_{#w} = 0` witnessing the escape from **S**.

---

## TA7a.2 — SubspaceDivergenceResidue

Characterises the interior-divergence residue of `⊖`: when the action point
of `w` is 1 and `o₁ = w₁` with `o ≠ w`, the first padded disagreement lies
at some `d > 1`, and TumblerSub's pre-divergence-zero clause forces
`r₁ = 0`, placing the result in `T \ S`.

*Formal Contract:*
- *Preconditions:* `o ∈ S`, `w ∈ T`, `Pos(w)`, `o ≥ w`, `#w ≤ #o`, `actionPoint(w) = 1`, `o₁ = w₁`, `o ≠ w`.
- *Depends:*
  - TA7a (SubspaceClosure) — parent claim defining **S** and establishing the complementary in-S branch whose precondition `o₁ > w₁` this sub-claim negates under `o ≠ w`.
  - T0 (CarrierSetDefinition) — carrier `T`, length `#`, `#r ≥ 1`.
  - TA-Pos (PositiveTumbler) — `Pos(w)` precondition; **S** definition whose universal positivity clause is violated at index 1.
  - ActionPoint (ActionPoint) — defines `k = actionPoint(w)`; the precondition `k = 1` is consumed only to characterise the scenario, not inside the proof (the divergence location `d > 1` follows from `o₁ = w₁ ∧ o ≠ w` without invoking `k`).
  - TA2 (WellDefinedSubtraction) — delivers `o ⊖ w ∈ T`.
  - T3 (CanonicalRepresentation) — forward direction `(#a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)) ⟹ a = b` instantiated at `(o, w)` in sub-case (α): the contradiction `o = w` against the precondition `o ≠ w` is what forces `zpd(o, w)` defined when the lengths agree.
  - TumblerSub (TumblerSub) — zero-padding under NAT-order trichotomy, ZPD-based dispatch, and the pre-divergence-zero clause `rᵢ = 0` for `i < d` which places `r₁ = 0`.
  - ZPD (ZeroPaddedDivergence) — partiality clause used both ways: in sub-case (α), the universal-agreement antecedent contradicts T3 plus `o ≠ w`; in sub-case (γ), the padding clause `ŵᵢ = 0` for `#w < i ≤ L` against `ôᵢ = oᵢ > 0` (from `o ∈ S`) breaks universal agreement at `i = #o`. Together these establish `zpd(o, w)` defined; minimality then places `d > 1` given agreement at position 1.
  - NAT-order (NatStrictTotalOrder) — trichotomy on `(#o, #w)` with `#w ≤ #o` places `L = #o`.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for `r₁ = 0`.
- *Postcondition:* `o ⊖ w ∈ T \ S`, with `r₁ = 0` witnessing the escape from **S**.

---

## TA7a.3 — SubspaceZeroResidue

Characterises the self-subtraction residue: for `o ∈ S`, the no-divergence
branch of TumblerSub produces `o ⊖ o = [0, ..., 0]`, the zero tumbler of
length `#o`, placing it in **Z**.

*Formal Contract:*
- *Preconditions:* `o ∈ S`.
- *Depends:*
  - TA7a (SubspaceClosure) — parent claim defining **S** and establishing the complementary in-S branch whose precondition `o₁ > w₁` this sub-claim negates via `o = w` (which forces `o₁ = w₁`).
  - T0 (CarrierSetDefinition) — carrier `T` and length `#`.
  - T1 (LexicographicOrder) — reflexivity of `≥` delivering `o ≥ o`.
  - TA-Pos (PositiveTumbler) — `Zero` predicate and **Z** definition.
  - TA2 (WellDefinedSubtraction) — delivers `o ⊖ o ∈ T`.
  - TumblerSub (TumblerSub) — no-divergence branch producing the zero tumbler of length `L`.
  - TA6 (ZeroTumblers) — invalidity of zero tumblers as addresses.
  - TA-PosDom (PositiveDominatesZero) — lower-bound status of the zero-tumbler residue relative to every positive tumbler.
  - NAT-order (NatStrictTotalOrder) — trichotomy on `(#o, #o)` names `L = #o`.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for every component of the zero tumbler.
- *Postcondition:* `o ⊖ o ∈ Z`, with every component zero.

---

## TA7a — SubspaceClosure

Defines the subspace **S** as the set of tumblers with all positive
components and establishes strict S-closure for ⊕ and ⊖ under tight
preconditions. For ⊕: `o ∈ S ∧ Pos(w) ∧ k ≤ #o ∧ (tail-positivity of w)`
gives `o ⊕ w ∈ S`. For ⊖: `o ∈ S ∧ Pos(w) ∧ o ≥ w ∧ #w ≤ #o ∧ o₁ > w₁`
gives `o ⊖ w ∈ S`. The T-only residues — length overflow, interior
divergence, self-subtraction to **Z** — are relocated to sub-claims
TA7a.1, TA7a.2, TA7a.3 on the complementary precondition fragments.

*Formal Contract:*
- *Preconditions:* For `⊕`: `o ∈ S`, `w ∈ T`, `Pos(w)`, `actionPoint(w) ≤ #o`, `(A i : actionPoint(w) ≤ i ≤ #w : wᵢ > 0)`. For `⊖`: `o ∈ S`, `w ∈ T`, `Pos(w)`, `o ≥ w`, `actionPoint(w) ≤ #o`, `#w ≤ #o`, `o₁ > w₁`.
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies carrier `T`, length operator `#`, ℕ-typed components, and the length-minimum `#t ≥ 1` underlying `#r ≥ 1` in both conjuncts; grounds the **S** definition.
  - T1 (LexicographicOrder) — defines the ordering relation `≥` used in the `⊖`-precondition and consumed by TA2.
  - TA-Pos (PositiveTumbler) — the precondition `Pos(w)` licenses action-point existence; supplies the **Z** definition referenced in the narrative and in the sub-claim TA7a.3.
  - ActionPoint (ActionPoint) — defines `k = actionPoint(w)` as the least non-zero position of `w` and supplies the minimum-value clause `w_k ≥ 1` used in the Conjunct 1 action-point positivity chain; the prefix-zero characterisation justifies the narrative remark that `k ≥ 2 ⟹ w₁ = 0`.
  - TumblerAdd (TumblerAdd) — three-region componentwise construction of `r = o ⊕ w` used in Conjunct 1 (pre-action copy from `o`, action-point sum `oₖ + wₖ`, tail copy from `w`).
  - TumblerSub (TumblerSub) — zero-padding under NAT-order trichotomy, ZPD-based divergence dispatch, and componentwise formula used in Conjunct 2; the divergence-at-1 branch is the one selected by `o₁ > w₁`.
  - ZPD (ZeroPaddedDivergence) — minimality clause `zpd(a, w) = min {k : 1 ≤ k ≤ L ∧ âₖ ≠ ŵₖ}` fixes `zpd(o, w) = 1` in Conjunct 2 from the position-1 disagreement `o₁ ≠ w₁` (itself supplied by `o₁ > w₁`); this divergence index is the dispatch key consumed by TumblerSub's componentwise formula at the divergence point.
  - TA0 (WellDefinedAddition) — delivers `o ⊕ w ∈ T` and `#(o ⊕ w) = #w` from the `⊕`-preconditions; the S-strengthening in Conjunct 1 rests on this T-closure.
  - TA2 (WellDefinedSubtraction) — delivers `o ⊖ w ∈ T` from the `⊖`-preconditions; the S-strengthening in Conjunct 2 rests on this T-closure.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — left order-compatibility and strict successor jointly establishing `oₖ + wₖ > oₖ` at the action point of `⊕`.
  - NAT-order (NatStrictTotalOrder) — trichotomy on `(#o, #w)` names `L` in the TumblerSub dispatch; the `≤` defining clause and transitivity of `<` compose the strict-through-addition chain in Conjunct 1.
  - NAT-sub (NatPartialSubtraction) — strict-positivity clause `m > n ⟹ m − n ≥ 1` discharges `r₁ > 0` at the divergence point of Conjunct 2.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` for the numerals in quantifier bounds and in `wₖ ≥ 1`; additive identity required in scope for the consumed contracts of TumblerAdd, TumblerSub, TA-Pos, and ActionPoint.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` in the **S** positivity clause `oᵢ > 0` and for the zero-padding semantics of TumblerSub consumed in Conjunct 2.
- *Forward References:*
  - TA7a.1 (SubspaceLengthResidue) — handles the complementary length-overflow residue case (`#w > #o`) relocated from TA7a's precondition lattice
  - TA7a.2 (SubspaceDivergenceResidue) — handles the complementary leading-zero residue case (`o₁ = w₁`) relocated from TA7a's precondition lattice
  - TA7a.3 (SubspaceZeroResidue) — handles the complementary self-subtraction residue case (collapse to Z) relocated from TA7a's precondition lattice
- *Postconditions:* `o ⊕ w ∈ S` with `#(o ⊕ w) = #w`; `o ⊖ w ∈ S` with `#(o ⊖ w) = #o`.
- *Frame:* The subspace identifier `N` is not an operand and is never modified.
- *Definition:* **S** = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)}.

---

## TS1 — ShiftOrderPreservation

Shift is order-preserving on equal-length tumblers: if v₁ < v₂ and both have length m, shifting both by the same positive amount n yields shift(v₁, n) < shift(v₂, n). The relative ordering of same-length tumblers is invariant under shift.

*Formal Contract:*
- *Preconditions:* v₁ ∈ T, v₂ ∈ T, n ∈ ℕ, n ≥ 1, #v₁ = #v₂, v₁ < v₂
- *Depends:*
  - OrdinalShift (OrdinalShift) — unfolds shift(v, n) = v ⊕ δ(n, #v).
  - OrdinalDisplacement (OrdinalDisplacement) — supplies δ(n, m) ∈ T, Pos(δ(n, m)), and actionPoint(δ(n, m)) = m.
  - Divergence (Divergence) — case (i) supplies the index k with 1 ≤ k ≤ #v₁, k ≤ #v₂, and divergence(v₁, v₂) = k; case (ii) is excluded by #v₁ = #v₂.
  - T3 (CanonicalRepresentation) — underwrites Divergence's exhaustiveness (used to rule out the residual configuration at the case-(ii)-exclusion step).
  - TA1-strict (StrictOrderPreservation) — load-bearing lemma: a < b with the eight preconditions yields a ⊕ w < b ⊕ w.
  - T0 (CarrierSetDefinition) — carrier T, length operator #·, component projection ·ᵢ.
  - T1 (LexicographicOrder) — the relation < on T, and irreflexivity used to derive v₁ ≠ v₂ from v₁ < v₂.
  - TA-Pos (PositiveTumbler) — definition of Pos(·).
  - ActionPoint (ActionPoint) — definition of actionPoint(·).
  - NAT-order (NatStrictTotalOrder) — ≤ on ℕ used in the length-bound and divergence-bound comparisons.
  - NAT-wellorder (NatWellOrdering) — least-element principle underwriting Divergence case (i)'s well-defined index k.
- *Postconditions:* shift(v₁, n) < shift(v₂, n)

---

## TS2 — ShiftInjectivity

Shift is injective over same-length tumblers: if shifting v₁ and v₂ by the same positive amount n yields identical results, then v₁ and v₂ must have been equal. This rules out any collisions introduced by the shift operation.

*Formal Contract:*
- *Preconditions:* v₁ ∈ T, v₂ ∈ T, n ∈ ℕ, n ≥ 1, #v₁ = #v₂
- *Depends:*
  - T0 (CarrierSetDefinition) — length typing `#·: T → ℕ` and length axiom `#a ≥ 1 for a ∈ T`.
  - OrdinalShift (OrdinalShift) — rewrites `shift(v, n) = v ⊕ δ(n, m)`.
  - OrdinalDisplacement (OrdinalDisplacement) — exports `δ(n, m) ∈ T`, `Pos(δ(n, m))`, `actionPoint(δ(n, m)) = m`.
  - TA-Pos (PositiveTumbler) — defines the predicate `Pos(·)`.
  - ActionPoint (ActionPoint) — defines the operator `actionPoint(·)`.
  - TA-MTO (ManyToOne) — load-bearing lemma; converse yields component-wise agreement.
  - T3 (CanonicalRepresentation) — component-wise plus length agreement implies equality.
- *Postconditions:* shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂

---

## TS3 — ShiftComposition

Two successive shifts compose into a single shift: applying shift by n₁ and then by n₂ is identical to a single shift by n₁ + n₂. Shift preserves tumbler length throughout.

*Formal Contract:*
- *Preconditions:* v ∈ T, n₁ ∈ ℕ, n₂ ∈ ℕ, n₁ ≥ 1, n₂ ≥ 1, #v = m
- *Depends:*
  - OrdinalShift (OrdinalShift) — unfolds `shift(·, n) = · ⊕ δ(n, m)` at each of three shift sites.
  - OrdinalDisplacement (OrdinalDisplacement) — fixes `δ(n, m) = [0, ..., 0, n]` with `actionPoint = m`, and exports `Pos(δ(n, m))` and `δ(n, m) ∈ T`.
  - T0 (CarrierSetDefinition) — length operator typing `#·: T → ℕ` and length axiom `#a ≥ 1` supply `m ∈ ℕ` and `m ≥ 1`; carrier characterisation places `vₘ ∈ ℕ`.
  - TA-Pos (PositiveTumbler) — defines `Pos(·)` consumed at TA0's third precondition.
  - ActionPoint (ActionPoint) — defines `actionPoint(·)` consumed at TA0's fourth precondition.
  - NAT-closure (NatArithmeticClosureAndIdentity) — addition-closure supplies `n₁ + n₂ ∈ ℕ`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — left/right order compatibility and strict successor inequality supply the chain `n₁ + n₂ ≥ 1 + n₂ ≥ 1 + 1 ≥ 1`.
  - NAT-order (NatStrictTotalOrder) — defining clause `m ≤ n ⟺ m < n ∨ m = n` and transitivity of `<` compose the chain into `n₁ + n₂ ≥ 1`.
  - TA0 (WellDefinedAddition) — discharges each `⊕`'s action-point precondition, supplies result-length `#(a ⊕ w) = #w`, and supplies `u ∈ T` for the second shift.
  - TumblerAdd (TumblerAdd) — three-region rule producing `uᵢ`, `Lᵢ`, `Rᵢ`.
  - NAT-addassoc (NatAdditionAssociative) — `(vₘ + n₁) + n₂ = vₘ + (n₁ + n₂)` at the comparison step.
  - T3 (CanonicalRepresentation) — component-wise and length agreement implies tumbler equality.
- *Postconditions:* shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂)
- *Frame:* #shift(shift(v, n₁), n₂) = #v = m

---

## TS4 — ShiftStrictIncrease

Shifting a tumbler by any positive amount strictly increases it — the shifted result is always greater than the original under the lexicographic order. This makes shift a strict advance with no fixed points.

*Formal Contract:*
- *Preconditions:* v ∈ T, n ∈ ℕ, n ≥ 1, #v = m
- *Depends:*
  - OrdinalShift (OrdinalShift) — unfolds `shift(v, n) = v ⊕ δ(n, m)`. Preconditions `v ∈ T`, `n ∈ ℕ`, `n ≥ 1` discharged from TS4's own preconditions under identity substitution.
  - OrdinalDisplacement (OrdinalDisplacement) — supplies exported postconditions `δ(n, m) ∈ T`, `Pos(δ(n, m))`, and `actionPoint(δ(n, m)) = m` at TA-strict's membership, positivity, and action-point precondition checks respectively.
  - TA-strict (StrictIncrease) — the load-bearing lemma: converts `Pos(w)` and `actionPoint(w) ≤ #a` into `a ⊕ w > a`.
  - T0 (CarrierSetDefinition) — length operator typing `#·: T → ℕ` supplies `m ∈ ℕ`; length axiom `#a ≥ 1 for all a ∈ T` supplies `m ≥ 1`. Both feed OrdinalDisplacement's `m ∈ ℕ` and `m ≥ 1` preconditions.
  - TA-Pos (PositiveTumbler) — defines the predicate `Pos(t) ⟺ (E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)` consumed at TA-strict's first precondition.
  - ActionPoint (ActionPoint) — defines `actionPoint(w) = min({i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0})` consumed at TA-strict's second precondition.
- *Postconditions:* shift(v, n) > v

---

## TS5 — ShiftAmountMonotonicity

Larger shift amounts produce strictly larger results on the same tumbler: if n₂ > n₁ ≥ 1, then shift(v, n₂) > shift(v, n₁). The output of shift is strictly monotone in the shift amount.

*Formal Contract:*
- *Preconditions:* v ∈ T, n₁ ∈ ℕ, n₂ ∈ ℕ, n₁ ≥ 1, n₂ > n₁, #v = m
- *Depends:*
  - TS3 (ShiftComposition) — rewrites shift(v, n₂) as shift(shift(v, n₁), d).
  - TS4 (ShiftStrictIncrease) — yields shift(u, d) > u for u = shift(v, n₁).
  - OrdinalShift — supplies u ∈ T and #u = m for u = shift(v, n₁).
  - NAT-sub (NatPartialSubtraction) — conditional closure, strict positivity, and left-inverse characterisation applied to d = n₂ − n₁.
  - NAT-order (NatStrictTotalOrder) — converts n₂ > n₁ to n₂ ≥ n₁ for NAT-sub's weak-order preconditions.
  - T0 (CarrierSetDefinition) — length operator typing #·: T → ℕ and length axiom #a ≥ 1, licensing m = #v ∈ ℕ with m ≥ 1.
  - T1 (LexicographicOrder) — establishes the strict total order `<` on T and grounds the companion relation `>` as its converse (`a > b ⟺ b < a`), licensing the rewrite from `shift(v, n₂) > shift(v, n₁)` to `shift(v, n₁) < shift(v, n₂)` at the proof's conclusion and the comparison `[2, 3, 11] < [2, 3, 14]` in the worked example.
- *Postconditions:* shift(v, n₁) < shift(v, n₂)

---

## TumblerAdd — TumblerAdd

Defines tumbler addition (⊕) as a hierarchical position-advance operation: below the action point components are copied from the base address, at the action point the components are summed, and above the action point components are taken from the displacement. The result always strictly exceeds the base address and is at least as large as the displacement itself.

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, Pos(w), actionPoint(w) ≤ #a
- *Definition:* k = actionPoint(w); rᵢ = aᵢ if i < k; rₖ = aₖ + wₖ; rᵢ = wᵢ if i > k
- *Depends:*
  - T0 (CarrierSetDefinition) — comprehension clause, instantiated at result-length `p ≥ 1` and the component map `i ↦ rᵢ` valued in ℕ, discharges `a ⊕ w ∈ T`; component projection supplies `aⱼ, aₖ ∈ ℕ` for dichotomy sites.
  - NAT-closure (NatArithmeticClosureAndIdentity) — closure of ℕ under addition at `rₖ = aₖ + wₖ`; additive identity `0 + wₖ = wₖ` in the dominance proof.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — left order-compatibility and strict successor inequality for strict advancement; right order-compatibility for dominance sub-case `aₖ > 0`.
  - NAT-cancel (NatAdditionCancellation) — summand absorption symmetric form `n + m = m ⟹ n = 0`, instantiated at `n = aₖ, m = wₖ`, rules out `aₖ + wₖ = wₖ` in the dominance sub-case `aₖ > 0`.
  - NAT-zero (NatZeroMinimum) — lower bound `0 ≤ n` at dichotomy sites.
  - NAT-order (NatStrictTotalOrder) — defining clause unfolds `≤` at dichotomy and strict-promotion sites; transitivity composes bounds.
  - NAT-wellorder (NatWellOrdering) — least element of `{j : 1 ≤ j < k ∧ aⱼ > 0}` in the divergence sub-case.
  - NAT-sub (NatPartialSubtraction) — conditional closure of `k - 1` and `n - k`; right-inverse `(m − n) + n = m` at `(k − 1) + 1 = k` and left-inverse `n + (m − n) = m` at `k + (n − k) = n` collapse the result-length identity.
  - ActionPoint (ActionPoint) — bounds `1 ≤ k ≤ #w`, zeros-below-action-point `wᵢ = 0` for `i < k`, and `wₖ ≥ 1`.
  - TA-Pos (PositiveTumbler) — the predicate `Pos(w)` in the precondition.
  - T1 (LexicographicOrder) — case (i) at the divergence position for the strict-advancement postcondition and for the strict branches of dominance; `≥` abbreviation (`a ≥ b ≡ b < a ∨ b = a`) merges the dominance proof's strict and equality branches to deliver `a ⊕ w ≥ w`.
  - T3 (CanonicalRepresentation, this ASN) — equality sub-case of dominance concludes `r = w` from component-wise agreement and equal length.
- *Forward References:*
  - TumblerSub (TumblerSub) — the inverse operation, constructed below in this ASN; TumblerAdd's correctness does not depend on it.
- *Postconditions:* a ⊕ w ∈ T, #(a ⊕ w) = #w, a ⊕ w > a (T1), a ⊕ w ≥ w (T1, T3)

---

## TumblerSub — TumblerSub

Defines component-wise tumbler subtraction `a ⊖ w`, producing a result whose nonzero components begin at the first
zero-padded divergence point and whose length is `L` — the longer of `#a` and `#w`, named by NAT-order trichotomy on
`(#a, #w)` (sub-case (α): `#a = #w`, `L = #a`; (β): `#a < #w`, `L = #w`; (γ): `#w < #a`, `L = #a`) rather than by a
primitive binary-maximum operator on ℕ, reproducing ZPD's analogous length-pair dispatch for the same operand pair.

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, a ≥ w (T1).
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier membership `a ⊖ w ∈ T` and per-operand length bounds `#a ≥ 1`, `#w ≥ 1`.
  - T1 (LexicographicOrder) — precondition ordering `a ≥ w`; trichotomy derives `w < a`; T1 case (ii) is eliminated in Divergence case (i) (its prefix-agreement range `1 ≤ i ≤ #w` instantiated at `i := k` would force `wₖ = aₖ`, contradicting `wₖ ≠ aₖ`) and in Divergence case (ii) sub-case (ii-b) (it yields `a < w`, contradicting `w < a`); in Divergence case (i), T1 case (i)'s witness `j` satisfies `wⱼ < aⱼ` and, once identified with `k` via Divergence's uniqueness, supplies `wₖ < aₖ`.
  - T3 (CanonicalRepresentation) — contrapositive `a ≠ b ⟺ #a ≠ #b ∨ (∃ j : 1 ≤ j ≤ #a : aⱼ ≠ bⱼ)` instantiated at `(a, w)` discharges `a ≠ w` from the not-zero-padded-equal hypothesis by case analysis on the padded-disagreement index `i`: case (A) (`i ≤ #a ∧ i ≤ #w`) fires the existential disjunct via ZPD's padded-projection equality (`âᵢ = aᵢ`, `ŵᵢ = wᵢ` lift `âᵢ ≠ ŵᵢ` to `aᵢ ≠ wᵢ`); case (B) (`i` in a padding zone) fires the length disjunct via NAT-order's trichotomy forcing `#a ≠ #w`.
  - Divergence — case analysis on the pair `(w, a)`; uniqueness clause for case (i) identifies T1 case (i)'s witness position `j` with the divergence index `k`.
  - ZPD — defines `zpd(a, w)`; padded-projection equality clauses `âᵢ = aᵢ` (for `1 ≤ i ≤ #a`) and `ŵᵢ = wᵢ` (for `1 ≤ i ≤ #w`) used in case (A) of the precondition's `a ≠ w` derivation to lift padded disagreement to native; padding clauses `âᵢ = 0` (for `#a < i ≤ L`) and `ŵᵢ = 0` (for `#w < i ≤ L`) used in case (B) to force the disagreement index into the longer operand's native domain; Relationship-to-Divergence identifies `zpd = divergence` under case (i); case-split and minimality under case (ii).
  - TA-Pos (PositiveTumbler) — defines `Pos` and `Zero` for the two conditional postconditions; the `Zero(a ⊖ w)` derivation in the no-divergence branch instantiates `Zero`'s Definition `(A i ∈ ℕ : 1 ≤ i ≤ #t : tᵢ = 0)` at `t := a ⊖ w`, discharging the universal from the per-component zeros `rᵢ = 0` supplied by the Definition's `a ⊖ w = [0, …, 0]` clause; complementarity `Pos(t) ⟺ ¬Zero(t)` then rules out `Pos(a ⊖ w)` in this branch, vacating ActionPoint's `Pos(w)` precondition.
  - ActionPoint — characterises `actionPoint(a ⊖ w)` as the unique least element of `S := {i : 1 ≤ i ≤ #(a ⊖ w) ∧ rᵢ ≠ 0}`; membership `k ∈ S` (from `1 ≤ k ≤ #(a ⊖ w)` and `rₖ ≠ 0`) and the least-element clause `(A n ∈ S :: k ≤ n)` (from the Definition's `rᵢ = 0` for `i < k`) jointly identify this minimum with `k`, yielding `actionPoint(a ⊖ w) = zpd(a, w)`.
  - NAT-sub (NatPartialSubtraction) — conditional closure `âₖ − ŵₖ ∈ ℕ` under `âₖ ≥ ŵₖ`; right-inverse characterisation `(âₖ − ŵₖ) + ŵₖ = âₖ` under `âₖ ≥ ŵₖ`, supplying the sum rewritten in the Pos derivation (instantiated on ZPD's padded projections so the operands are well-defined when `k` exceeds either native domain).
  - NAT-zero (NatZeroMinimum) — `0 ∈ ℕ` for ZPD's padded-projection clauses, `rᵢ = 0` components, and the zero-tumbler branch; lower bound `0 ≤ âₖ`.
  - NAT-order (NatStrictTotalOrder) — trichotomy on `(#a, #w)` naming `L`, reused in case (B) of the precondition's `a ≠ w` derivation where `L ∈ {#a, #w}` together with a padding-zone disagreement index (`i > #a` forcing `L = #w` and `#a < #w`, or `i > #w` forcing `L = #a` and `#w < #a`) witnesses `#a ≠ #w`; defining clause `≤ ⟺ < ∨ =` at `(0, âₖ)`; conversion `>` to `≥` at `(âₖ, ŵₖ)` for NAT-sub; disjointness-of-`<`-and-`=` at `(wⱼ, aⱼ)` in Divergence case (i) (native indices `j ≤ #w ∧ j ≤ #a`) converts T1 case (i)'s `wⱼ < aⱼ` into `wⱼ ≠ aⱼ`, qualifying the witness `j` for Divergence case (i)'s conjunction (whose uniqueness then identifies `j` with `k`); the `>` definition `m > n ⟺ n < m` at `(âₖ, ŵₖ)` and disjointness-of-`<`-and-`=` at `(ŵₖ, âₖ)` jointly discharge the Pos-derivation contradiction `ŵₖ ≠ âₖ` from `âₖ > ŵₖ`; at-least-one trichotomy at `(k, n)` together with the defining clause `≤ ⟺ < ∨ =` at `(k, n)` discharges the least-element clause `(A n ∈ S :: k ≤ n)` from `¬(n < k)`, identifying `k` as `actionPoint(a ⊖ w)` within ActionPoint's uniqueness.
  - NAT-closure (NatArithmeticClosureAndIdentity) — posits `1 ∈ ℕ` and closes ℕ under `+`, and fixes `0 + n = n`. The left-identity clause is instantiated at `n := ŵₖ` to rewrite `0 + ŵₖ = ŵₖ` in the Pos derivation, bridging the supposition `rₖ = 0` to the contradiction `ŵₖ = âₖ`.
  - NAT-discrete (NatDiscreteness) — forward direction `m < n ⟹ m + 1 ≤ n` instantiated at `(m, n) := (#a, #w)`, used in Divergence case (ii) sub-case (ii-b) to bridge the sub-case's hypothesis `#a < #w` to the T1 case (ii) condition `#a + 1 ≤ #w`, completing the exhibition of the T1(ii) witness `k = #a + 1` that yields `a < w` (which then contradicts `w < a` via T1's trichotomy disjointness clause and eliminates the sub-case).
- *Definition:* NAT-order's trichotomy on `(#a, #w)` selects exactly one of: (α) `#a = #w`, `L = #a`; (β) `#a < #w`, `L = #w`; (γ) `#w < #a`, `L = #a`. a ⊖ w is computed by case analysis on k = zpd(a, w) (ZPD) using ZPD's padded projections `â`, `ŵ` on `{1, ..., L}` for every component reference at indices that may exceed the native domain: rᵢ = 0 for i < k, rₖ = âₖ − ŵₖ, rᵢ = âᵢ for i > k; when zpd(a, w) is undefined, a ⊖ w = [0, …, 0]; #(a ⊖ w) = L.
- *Postconditions:* a ⊖ w ∈ T, #(a ⊖ w) = L (the longer of `#a` and `#w`, named by NAT-order trichotomy per the Definition); when zpd(a, w) is defined: â_{zpd(a,w)} > ŵ_{zpd(a,w)} (the divergence-point inequality on ZPD's padded projections, well-typed regardless of whether zpd(a, w) lies in either operand's native domain), Pos(a ⊖ w) (TA-Pos), actionPoint(a ⊖ w) = zpd(a, w) (ActionPoint); when zpd(a, w) is undefined: Zero(a ⊖ w) (TA-Pos).

---

## ZPD — ZeroPaddedDivergence

Defines the zero-padded divergence `zpd(a, w)` as the first position at which two tumblers disagree after both are
extended to a common length `L` by appending zeros, where `L` — the longer of `#a` and `#w` — is selected by NAT-order
trichotomy on `(#a, #w)` (sub-case (α): `#a = #w`, `L = #a`, no padding; (β): `#a < #w`, `L = #w`, `a` padded; (γ):
`#w < #a`, `L = #a`, `w` padded) rather than by a primitive binary-maximum operator on ℕ. The function is partial: it
is undefined when the padded sequences agree everywhere, which occurs when one operand is a prefix of the other with
all trailing components zero — a case where Divergence fires but zpd does not. When defined, zpd is symmetric and
equals the ordinary divergence index whenever the disagreement falls at a shared position `k` with `k ≤ #a ∧ k ≤ #w`
(the conjunction replacing `k ≤ min(#a, #w)`); in the prefix sub-cases (β) and (γ) the Divergence boundary is `#a + 1`
or `#w + 1` respectively (replacing `min(#a, #w) + 1`).

*Formal Contract:*
- *Domain:* a ∈ T, w ∈ T
- *Definition:* NAT-order trichotomy on `(#a, #w)` selects (α) `#a = #w`, `L = #a`; (β) `#a < #w`, `L = #w`; (γ) `#w < #a`, `L = #a`. Padded projections `â`, `ŵ` on `{1, ..., L}`: `âᵢ = aᵢ` for `1 ≤ i ≤ #a`, `âᵢ = 0` for `#a < i ≤ L`; `ŵᵢ = wᵢ` for `1 ≤ i ≤ #w`, `ŵᵢ = 0` for `#w < i ≤ L`. If `(A i : 1 ≤ i ≤ L : âᵢ = ŵᵢ)`, `zpd(a, w)` is undefined. Otherwise, `zpd(a, w) = min {k : 1 ≤ k ≤ L ∧ âₖ ≠ ŵₖ}`.
- *Depends:*
  - T0 (CarrierSetDefinition) — `a, w ∈ T`, lengths `#a`, `#w`, native-domain component projections `aᵢ`, `wᵢ`, ℕ-valuation of native components.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the padding clauses `âᵢ = 0`, `ŵᵢ = 0`.
  - NAT-order (NatStrictTotalOrder) — trichotomy on `(#a, #w)` selects `L` and dispatches the shared-position bound `k ≤ #a ∧ k ≤ #w` and sub-case boundaries `#a + 1`, `#w + 1`.
  - NAT-wellorder (NatWellOrdering) — least-element principle for `min {k : 1 ≤ k ≤ L ∧ âₖ ≠ ŵₖ}`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — addition closure instantiated at `(#a, 1)` and `(#w, 1)`, with `1 ∈ ℕ` from the same axiom, places `#a + 1` and `#w + 1` in ℕ in the postcondition.
  - NAT-discrete (NatDiscreteness) — forward direction `m < n ⟹ m + 1 ≤ n`, instantiated at `(#a, k)` in sub-case (β) and at `(#w, k)` in sub-case (γ), bridges the construction's strict bound `#a < k` (resp. `#w < k`) on the least disagreement position to the postcondition's `#a + 1 ≤ k` (resp. `#w + 1 ≤ k`), grounding `zpd(a, w) ≥ divergence(a, w)` against the NAT-* axioms.
  - Divergence (Divergence) — two-case structure (component divergence; prefix divergence) and domain restriction `a ≠ b` consumed by the Relationship-to-Divergence postcondition.
- *Codomain:* When defined, `zpd(a, w) ∈ {1, ..., L}`, with `L = #a` in sub-cases (α), (γ) and `L = #w` in sub-case (β).
- *Partiality:* `zpd(a, w)` is undefined iff `a` and `w` are zero-padded-equal.
- *Postconditions (Symmetry):* `zpd(a, w)` is defined iff `zpd(w, a)` is defined, and when defined, `zpd(a, w) = zpd(w, a)`. Sub-case (α) is self-symmetric; sub-cases (β) and (γ) swap under exchange, yielding the same `L`; the disagreement predicate is symmetric.
- *Postconditions (Relationship to Divergence):* For `a ≠ w`: in Divergence case (i) with divergence at `k` satisfying `k ≤ #a ∧ k ≤ #w`, `zpd(a, w) = divergence(a, w)`. In Divergence case (ii), under sub-case (β) or (γ): if the longer operand has a nonzero component beyond the shorter's last position, `zpd(a, w)` is defined and `zpd(a, w) ≥ divergence(a, w)`; if all such components are zero, `zpd(a, w)` is undefined.

---

