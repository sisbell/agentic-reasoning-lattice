# ASN-0053 Formal Statements

*Source: ASN-0053-span-algebra.md (revised 2026-03-19) — Extracted: 2026-07-02*

## S4a — SplitMergeInverse

Proves that split-then-merge is a lossless round-trip on level-uniform spans: splitting σ at any interior point and immediately merging the two resulting parts recovers σ exactly, with the same start and width. The guarantee rests on the adjacency of the produced halves and the WR axiom, which together force the merged width to equal the original.

*Formal Contract:*

- *Preconditions:* σ = (s, ℓ) is a well-formed level-uniform span; p is interior to σ, i.e. start(σ) < p < reach(σ); level_compat(s, p).
- *Postconditions:* S3(S4(σ, p)) = σ — merging the two parts produced by splitting σ at p yields γ with start(γ) = s and width(γ) = ℓ, hence γ = σ.
- *Definition:* Split S4 at interior p yields λ = (s, p ⊖ s) with reach(λ) = p and ρ = (p, reach(σ) ⊖ p) with reach(ρ) = reach(σ). Merge S3 of adjacent λ, ρ yields γ = (s_m, r_m ⊖ s_m) with s_m = min(start(λ), start(ρ)) and r_m = max(reach(λ), reach(ρ)).
- *Frame:* The level of every position is preserved; only the partitioning of σ changes and is then undone.

- *Depends:*
  - S4 (SplitPartition) — supplies the split operation and its outputs λ = (s, p ⊖ s), ρ = (p, reach(σ) ⊖ p) whose properties the proof traces through to recover σ
  - S3 (MergeEquivalence) — supplies the merge operation invoked in the proof step concluding that γ = (s_m, r_m ⊖ s_m) with s_m = s and r_m = reach(σ)
  - WR (WidthRecovery) — supplies the identity reach(σ) ⊖ start(σ) = ℓ used in the proof step equating the merged width to the original width

---

## WF — WellFormedSpanFromEndpoints

Proves that any pair of same-depth tumblers s < r can be directly packaged into a well-formed level-uniform span: the constructed span (s, r ⊖ s) satisfies the well-formedness condition T12 — its width is positive with action point within the common depth — and its reach recovers exactly r.

*Formal Contract:*

- *Preconditions:* s, r ∈ T with s < r and #s = #r.
- *Definition:* γ = (start(γ), width(γ)) = (s, r ⊖ s).
- *Postconditions:* γ is a well-formed level-uniform span satisfying T12 — its width r ⊖ s is positive with action point at most #s, and #width(γ) = #start(γ); and reach(γ) = s ⊕ (r ⊖ s) = r.

- *Depends:*
  - T12 (SpanWellDefinedness, ASN-0034) — supplies the well-formedness predicate (Pos(ℓ) and actionPoint(ℓ) ≤ #s) that the proof verifies and the claim's conclusion targets
  - D1 (DisplacementRoundTrip, ASN-0034) — supplies the identity a ⊕ (b ⊖ a) = b used in the proof step reach(γ) = s ⊕ (r ⊖ s) = r; its precondition divergence(s, r) ≤ #s is discharged in the proof from T1 and Divergence
  - T1 (LexicographicOrder, ASN-0034) — its definition of s < r supplies the witness k (with sᵢ = rᵢ for 1 ≤ i < k) in case (i) `k ≤ #s ∧ k ≤ #r ∧ sₖ < rₖ` or case (ii) `k = #s + 1 ≤ #r`; #s = #r excludes case (ii), leaving k ≤ #s and sₖ ≠ rₖ; its trichotomy disjointness `¬(s < r ∧ s = r)` yields s ≠ r, well-defining divergence(s, r); and its ≤/≥ abbreviations turn s < r into r ≥ s, discharging TumblerSub's precondition
  - Divergence (Divergence, ASN-0034) — its case-(i) uniqueness clause identifies the T1 witness k with divergence(s, r), so k ≤ #s discharges D1's precondition divergence(s, r) ≤ #s; and its symmetry divergence(r, s) = divergence(s, r), with the case-(i) qualifier invariant under operand swap, carries that case-(i) witness to the pair (r, s) for ZPD's Relationship-to-Divergence
  - TumblerSub (TumblerSub, ASN-0034) — supplies the width r ⊖ s and the well-formedness facts D1 leaves internal: carrier membership r ⊖ s ∈ T; the positive-branch postcondition Pos(r ⊖ s), exported whenever zpd(r, s) is defined; the action-point identification actionPoint(r ⊖ s) = zpd(r, s) = k, which as a component index satisfies k ≤ #(r ⊖ s); and the length #(r ⊖ s) = max(#r, #s) = #s, which bounds actionPoint(r ⊖ s) ≤ #s and supplies level-uniformity. Its precondition r ≥ s follows from s < r (T1); zpd(r, s) is defined via the Divergence case-(i) witness through ZPD's Relationship-to-Divergence (below)
  - ZPD (ZeroPaddedDivergence, ASN-0034) — its Relationship-to-Divergence postcondition equates zpd(r, s) = divergence(r, s) in Divergence's case (i); fed the case-(i) witness k = divergence(s, r) ≤ #s (carried from the pair (s, r) to (r, s) by Divergence's symmetry, with k ≤ #r since #s = #r), it certifies that zpd(r, s) = k is defined — the guard that licenses TumblerSub's positive branch and its Pos(r ⊖ s) postcondition
  - NAT-addcompat (NatAdditionOrderAndSuccessor, ASN-0034) — supplies the strict successor inequality #s < #s + 1 used to eliminate T1 case (ii): with #s = #r the case bound k = #s + 1 ≤ #r forces #s + 1 ≤ #s, which #s < #s + 1 contradicts
  - NAT-order (NatStrictTotalOrder, ASN-0034) — its `≤` definition `m ≤ n ⟺ m < n ∨ m = n` unfolds the case-(ii) bound #s + 1 ≤ #s into the sub-cases #s + 1 < #s and #s + 1 = #s; its transitivity axiom chains the strict sub-case #s + 1 < #s with #s < #s + 1 to #s < #s, while indiscernibility of `=` rewrites #s < #s + 1 to #s < #s in the equality sub-case #s + 1 = #s; its irreflexivity `¬(#s < #s)` refutes #s < #s in both, completing the T1 case (ii) elimination; and its exactly-one trichotomy disjointness clause `¬(sₖ < rₖ ∧ sₖ = rₖ)` converts T1 case (i)'s sₖ < rₖ into sₖ ≠ rₖ to qualify k for Divergence case (i)

---

## S3 — MergeEquivalence

Proves that two overlapping or adjacent level-uniform spans can always be merged into a single well-formed span whose denotation is exactly the union of the originals. The merged span is constructed from the minimum start and maximum reach of the two inputs, and its denotation depends only on those endpoints — not on the derivation history — so any two representations covering the same address range are equivalent.

*Formal Contract:*

- *Preconditions:* α and β are well-formed level-uniform spans; level_compat(start(α), start(β)); the spans overlap or are adjacent — equivalently, taking start(α) ≤ start(β) without loss of generality, reach(α) ≥ start(β).
- *Definition:* The merged span is γ = (s, r ⊖ s) with s = min(start(α), start(β)) and r = max(reach(α), reach(β)).
- *Postconditions:* γ is a well-formed level-uniform span (by S6, #s = #r; s < r by TA-strict, reach(α) = start(α) ⊕ width(α) > start(α) = s with r ≥ reach(α); and both WF endpoints in T — s = min(start(α), start(β)) is a span start, while r = max(reach(α), reach(β)) is placed in T by TumblerAdd's carrier postcondition a ⊕ w ∈ T instantiated at (start(σ), width(σ)) under each well-formed σ ∈ {α, β}, since r is one of reach(α), reach(β)); start(γ) = s, reach(γ) = r; and ⟦γ⟧ = ⟦α⟧ ∪ ⟦β⟧. Moreover γ is identical to any span specified directly with endpoints s and r.
- *Frame:* The denotation of γ depends only on its endpoints s and r, not on the derivation history of α and β; representations {[s, m], [m, r]} and {[s, r]} of the same range are equivalent.

- *Depends:*
  - S6 (LevelConstraint) — supplies the level-uniformity property (#s = #r for all boundary tumblers) invoked in the proof to satisfy the equal-length precondition passed to WF
  - WF (WellFormedSpanFromEndpoints) — supplies the well-formedness construction invoked in the proof step concluding that γ = (s, r ⊖ s) is a valid level-uniform span with reach(γ) = r
  - TumblerAdd (TumblerAdd, ASN-0034) — supplies the carrier postcondition a ⊕ w ∈ T, instantiated at (a, w) = (start(σ), width(σ)) under each well-formed σ ∈ {α, β}, to place reach(α), reach(β) ∈ T; the reach endpoint r = max(reach(α), reach(β)) is one of these, so r ∈ T, discharging WF's carrier precondition for the reach endpoint (the start endpoint s = min(start(α), start(β)) being a span start, already in T)
  - TA-strict (StrictIncrease, ASN-0034) — supplies the strict-advance postcondition a ⊕ w > a, instantiated at (a, w) = (start(σ), width(σ)) under each well-formed span σ: at α it gives reach(α) = start(α) ⊕ width(α) > start(α) = s, whence (with r = max(reach(α), reach(β)) ≥ reach(α)) s < r, discharging WF's strict-inequality precondition; at β it gives start(β) < reach(β), the inequality that renders the disjunct reach(β) = start(α) vacuous under the WLOG ordering. Its preconditions — Pos(width(σ)) and actionPoint(width(σ)) ≤ #start(σ) — are the same ones each σ's well-formedness supplies for the TumblerAdd citation above
  - T1 (LexicographicOrder, ASN-0034) — supplies the total-order properties on T that the merge argument invokes directly. Its dichotomy (trichotomy read at a fixed t) drives the converse case split — Case 1 (t < reach(α)) versus Case 2 (t ≥ reach(α)) — which exhausts every t ∈ [s, r) in establishing [s, r) ⊆ ⟦α⟧ ∪ ⟦β⟧. Its mixed ≤-< chaining consequence (m ≤ n ∧ n < p ⇒ m < p, a corollary of transitivity) collapses reach(β) = start(α) ≤ start(β) < reach(β) to reach(β) < reach(β), which irreflexivity forbids — this is what renders the adjacency disjunct reach(β) = start(α) vacuous under the WLOG ordering start(α) ≤ start(β)
- *Forward References:*
  - S1 (IntersectionClosure) — its concrete spans α and β are reused in the example; S1 is downstream context, not a dependency of this claim's proof

---

## WR — WidthRecovery

Proves that for any level-uniform span, subtracting its start from its reach exactly recovers its width — the displacement round-trips without distortion. This holds precisely because level-uniformity forces start and reach to share the same address length, satisfying the preconditions of DisplacementUnique (D2); the worked counter-example shows the guarantee fails when address lengths differ.

*Formal Contract:*

- *Preconditions:* σ = (s, ℓ) is a well-formed level-uniform span — by Span validity, ℓ > 0 with action point ≤ #s, and #ℓ = #s by level-uniformity. This is the caller's only obligation; D2's preconditions for (a, b, w) = (s, reach(σ), ℓ) — s < reach(σ), s ⊕ ℓ = reach(σ), #s ≤ #reach(σ), and divergence(s, reach(σ)) ≤ #s — are intermediate results the proof discharges from well-formedness, not caller obligations.
- *Postconditions:* reach(σ) ⊖ start(σ) = width(σ).
- *Definition:* start(σ) = s; width(σ) = ℓ; reach(σ) = s ⊕ ℓ.

- *Depends:*
  - D2 (DisplacementUnique, ASN-0034) — supplies the displacement uniqueness result `reach(σ) ⊖ start(σ) = ℓ` that is the claim's conclusion, once its preconditions are discharged for (a, b, w) = (s, reach(σ), ℓ)
  - Span (Span, ASN-0034) — defines span validity as Pos(ℓ) ∧ actionPoint(ℓ) ≤ #s; σ being a well-formed span by hypothesis, this validity (not a T12 postcondition — T12 *consumes* it as a precondition) supplies the Pos(ℓ) and action-point bound that qualify σ and discharge TA-strict and D2's preconditions on ℓ
  - TA-strict (StrictIncrease, ASN-0034) — supplies `a ⊕ w > a` instantiated as s < reach(σ), discharging D2's precondition a < b
  - TA0 (WellDefinedAddition, ASN-0034) — supplies the result-length identity `#(s ⊕ ℓ) = #ℓ = #s` used to pin #reach(σ) = #s and to confirm TA0's own preconditions for the s ⊕ ℓ = reach(σ) step
  - T1 (LexicographicOrder, ASN-0034) — its definition of s < reach(σ) supplies the witness k (with sᵢ = reach(σ)ᵢ for 1 ≤ i < k) in case (i) `k ≤ #s ∧ k ≤ #reach(σ) ∧ sₖ < reach(σ)ₖ` or case (ii) `k = #s + 1 ≤ #reach(σ)`; the equal length #s = #reach(σ) excludes case (ii) (which would force #s + 1 ≤ #s), leaving case (i) with k ≤ #s and sₖ ≠ reach(σ)ₖ; and its trichotomy disjointness `¬(s < reach(σ) ∧ s = reach(σ))` yields s ≠ reach(σ), well-defining divergence(s, reach(σ))
  - Divergence (Divergence, ASN-0034) — its case-(i) uniqueness clause identifies the T1 witness k with divergence(s, reach(σ)), so k ≤ #s discharges D2's precondition divergence(s, reach(σ)) ≤ #s
  - NAT-addcompat (NatAdditionOrderAndSuccessor, ASN-0034) — supplies the strict successor inequality #s < #s + 1 that excludes T1 case (ii): with #s = #reach(σ) the case bound k = #s + 1 ≤ #reach(σ) forces #s + 1 ≤ #s, which #s < #s + 1 contradicts
  - NAT-order (NatStrictTotalOrder, ASN-0034) — its exactly-one trichotomy disjointness clause `¬(sₖ < reach(σ)ₖ ∧ sₖ = reach(σ)ₖ)` converts T1 case (i)'s strict component disagreement sₖ < reach(σ)ₖ into the inequation sₖ ≠ reach(σ)ₖ that qualifies k for Divergence's case-(i) qualifier
- *Forward References:*
  - WF (WellFormedSpanFromEndpoints) — sibling claim whose proof contains the equal-length/divergence-type argument reproduced inline here; cited as a navigation pointer

---

## S11b — DifferenceEqual

Proves that when two level-uniform spans are equal — sharing both start and reach — their set difference is empty. Because a span's denotation is determined entirely by its endpoints, equal spans have identical denotations, and any set minus itself is empty.

*Formal Contract:*

- *Preconditions:* α and β are well-formed level-uniform spans; level_compat(start(α), start(β)) holds; SC case (v) (equal) holds, i.e. start(α) = start(β) and reach(α) = reach(β).
- *Postconditions:* ⟦α⟧ \ ⟦β⟧ = ∅, a span-set of 0 spans.
- *Definition:* ⟦α⟧ \ ⟦β⟧ denotes the set difference of the two span denotations; under the equal case it computes to ∅ because ⟦α⟧ = ⟦β⟧.
- *Axiom:* A span's denotation is determined by its start and reach, so equal endpoints yield equal denotations; the set difference of a set with itself is empty (X \ X = ∅).

- *Depends:*
  - SC (SpanClassification) — supplies the case (v) (equal) definition whose endpoint-equality conditions form S11b's precondition and whose denotation convention (⟦γ⟧ = { p : start(γ) ≤ p < reach(γ) }) grounds the axiom that equal endpoints yield equal denotations

---

## S3a — MergeCommutativity

Proves that span merge is order-independent: merging α with β yields the same point set as merging β with α. The result is a direct instance of set-union commutativity, requiring no properties of spans beyond their point sets.

*Formal Contract:*

- *Preconditions:* α and β are spans with point sets ⟦α⟧ and ⟦β⟧.
- *Postconditions:* ⟦α⟧ ∪ ⟦β⟧ = ⟦β⟧ ∪ ⟦α⟧.
- *Definition:* The merge of two spans is the span whose point set is the union of their point sets: ⟦merge(α, β)⟧ = ⟦α⟧ ∪ ⟦β⟧.
- *Axiom:* Set union is commutative: A ∪ B = B ∪ A, inherited from the commutativity of logical disjunction.

---

## S8 — NormalizationExistence

Proves that any level-uniform, mutually level-compatible span-set has a normalized equivalent with identical denotation: a greedy interval-merge algorithm sorts spans by start position, fuses overlapping or adjacent intervals, and emits disjoint spans whenever a gap is encountered, guaranteeing the result satisfies N1 (strictly increasing starts) and N2 (separated reaches). The key insight is that strict ordering between emitted spans arises not from the sort alone — ties in start position are permitted — but from the emit condition, which forces each new interval to open strictly beyond the previous interval's reach.

*Formal Contract:*

- *Preconditions:* Σ is a span-set whose component spans are well-formed level-uniform spans and mutually level-compatible.
- *Postconditions:* there exists a normalized span-set Σ̂ with ⟦Σ̂⟧ = ⟦Σ⟧ (so Σ̂ ≡ Σ) whose emitted spans satisfy N1 (strictly increasing starts) and N2 (separated reaches); for n = 0, Σ̂ = ⟨⟩ and vacuously satisfies N1 and N2.
- *Invariant:* after processing σ₁..σᵢ, with emitted set E and current interval [s, r), J holds: ⟦E⟧ ∪ [s, r) = ⟦σ₁⟧ ∪ ... ∪ ⟦σᵢ⟧; and the current interval is non-empty (s < r), so every emitted pair (s, r ⊖ s) is a well-formed level-uniform span by WF.
- *Frame:* the input span-set Σ and its denotation ⟦Σ⟧ are unchanged; only the auxiliary state (E, [s, r)) advances.
- *Definition:* sort component spans into non-decreasing start order (ties broken arbitrarily); seed [s, r) = [start(σ₁), reach(σ₁)), E = ∅; for each subsequent σᵢ, if start(σᵢ) ≤ r extend r to max(r, reach(σᵢ)), else emit (s, r ⊖ s) and restart [s, r) = [start(σᵢ), reach(σᵢ)); after the scan emit the final (s, r ⊖ s).
- *Axiom:* T1 totally orders tumblers (used to sort starts); WF characterizes well-formed level-uniform spans; S6 gives #s = #r under level-uniformity; TumblerAdd's carrier postcondition a ⊕ w ∈ T, at (start(σ), width(σ)) under each component's well-formedness, places every component reach in T, so each emitted interval's reach endpoint r (a running maximum of component reaches) lies in T while its start endpoint s (a component start) lies in T directly — discharging WF's carrier preconditions.

- *Depends:*
  - T1 (LexicographicOrder, ASN-0034) — supplies the strict total order on tumblers used to sort span starts in the construction; listed in the Axiom as a direct dependency
  - S6 (LevelConstraint) — supplies #s = #r under level-uniformity, the equal-length precondition that WF requires before the emitted pair (s, r ⊖ s) can be certified as well-formed; listed in the Axiom
  - WF (WellFormedSpanFromEndpoints) — supplies the certificate that any emitted pair (s, r ⊖ s) with s < r and #s = #r is a well-formed level-uniform span with reach r; invoked at every emit step and in the loop invariant; listed in the Axiom
  - TumblerAdd (TumblerAdd, ASN-0034) — supplies the carrier postcondition a ⊕ w ∈ T, instantiated at (a, w) = (start(σ), width(σ)) under each component span's well-formedness, to place every component reach reach(σ) = start(σ) ⊕ width(σ) ∈ T; each emitted pair (s, r ⊖ s) takes its reach endpoint r as a running maximum of these component reaches (hence in T) and its start endpoint s as a component start (in T directly), discharging WF's carrier preconditions s, r ∈ T at every emit; listed in the Axiom
  - T12 (SpanWellDefinedness, ASN-0034) — supplies the well-formedness predicate (Pos(ℓ) and actionPoint(ℓ) ≤ #s) that the concrete example verification explicitly checks for each emitted span
- *Forward References:*
  - SC (SpanClassification) — named as the source of cases (iv) and (v) explaining why distinct spans may share a start; cited as informational context, not invoked in the construction or loop-invariant proof

---

## S11c — DifferenceOverlap

Proves that when two level-uniform, level-compatible spans overlap properly — each extending past the other's boundary on one side — their set difference is always expressible as exactly one span. In Case 1 (α starts first), the witness span runs from start(α) to start(β); in Case 2 (β starts first), it runs from reach(β) to reach(α). The witness is constructed explicitly in each sub-case, confirming the difference collapses to a single contiguous interval rather than requiring two.

*Formal Contract:*

- *Preconditions:* α and β are well-formed level-uniform spans; level_compat(start(α), start(β)) holds; the pair lies in SC case (iii) (proper overlap), i.e. either start(α) < start(β) < reach(α) < reach(β) (Case 1) or start(β) < start(α) < reach(β) < reach(α) (Case 2).
- *Postconditions:* ⟦α⟧ \ ⟦β⟧ is expressible as a span-set of exactly 1 span. In Case 1 that span is γ with ⟦γ⟧ = {t : start(α) ≤ t < start(β)}; in Case 2 it is γ' with ⟦γ'⟧ = {t : reach(β) ≤ t < reach(α)}.
- *Definition:* The witness span is constructed per sub-case. Case 1: γ = (start(α), start(β) ⊖ start(α)), with reach(γ) = start(β). Case 2: γ' = (reach(β), reach(α) ⊖ reach(β)), with reach(γ') = reach(α).
- *Axiom:* For any span σ, ⟦σ⟧ = {t : start(σ) ≤ t < reach(σ)} — reach(σ) is the exclusive upper bound of σ's denotation. This half-open convention is the external fact the witness constructions take as given: it is what lets us read ⟦γ⟧ = {t : start(α) ≤ t < start(β)} and ⟦γ'⟧ = {t : reach(β) ≤ t < reach(α)} directly off the constructed endpoints and match each to ⟦α⟧ \ ⟦β⟧. (The discharge of WF's carrier and length preconditions for these witnesses is derived, not stipulated, and is carried out in the Case 2 proof body.)
- *Frame:* α and β are unchanged; the construction produces a new span and does not mutate either operand.

- *Depends:*
  - SC (SpanClassification) — supplies the case taxonomy (case iii = proper overlap) that defines S11c's precondition and whose sub-case split structures the entire proof
  - T1 (LexicographicOrder, ASN-0034) — supplies the strict total order whose transitivity underwrites the element-chasing in both sub-cases. In Case 1 the chains start(α) ≤ t < start(β) < reach(α) (yielding t ∈ ⟦α⟧) and start(β) ≤ t < reach(α) < reach(β) (yielding t ∈ ⟦β⟧) compose strict inequalities transitively; in Case 2 the same transitivity orders a fresh t ∈ ⟦α⟧ against reach(β), via start(β) < start(α) ≤ t and reach(β) < reach(α), to split ⟦α⟧ at reach(β): the ⊆ membership branch derives the lower bound start(β) ≤ t from start(β) < start(α) ≤ t by case-splitting the ≤ — T1(c) on the strict branch start(β) < start(α) < t, substitution of equals on start(α) = t — to reach start(β) < t, and in that split's ⊇ direction it recovers the lower guard start(α) ≤ t from the Case 2 hypothesis start(α) < reach(β) and reach(β) ≤ t by the same case-split on the ≤ — T1(c) on the strict branch start(α) < reach(β) < t, substitution of equals on reach(β) = t — to reach start(α) < t. SC supplies only the ordering of the four boundary points; the step-by-step transitivity applied to the fresh variable t drawn from ⟦α⟧ is T1's
  - WF (WellFormedSpanFromEndpoints) — supplies the well-formedness guarantee invoked in both Case 1 and Case 2 to licence the constructed witness spans γ and γ' as well-formed level-uniform spans
  - S6 (LevelConstraint) — supplies the level-uniformity consequence #reach(σ) = #start(σ), which the Case 2 proof body combines with level_compat(start(α), start(β)) to discharge WF's length precondition #reach(β) = #reach(α) for the witness γ', whose endpoints are reaches. Case 1's witness γ has primitive span starts as endpoints, so its length precondition #start(α) = #start(β) is level_compat directly and does not call on S6's reach-length consequence
  - TumblerAdd (TumblerAdd, ASN-0034) — supplies the carrier postcondition a ⊕ w ∈ T that the Case 2 proof body invokes to place the reach-valued endpoints reach(β), reach(α) of the witness γ' into T, discharging WF's carrier preconditions (Case 1's endpoints are primitive span starts, already in T)

---

## S0 — Convexity

Proves that a span's address set is convex under the total order on T1 addresses: any address lying between two members of a span is itself a member. Consequently, spans cannot have gaps — sub-addresses like [1, 3, 0, 5] that fall numerically between [1, 3] and [1, 7] are genuine interior points, because the lexicographic tumbler comparison treats no separator values as boundaries.

*Formal Contract:*

- *Preconditions:* `p ∈ ⟦σ⟧ ∧ r ∈ ⟦σ⟧ ∧ q ∈ T ∧ p ≤ q ≤ r`. The carrier membership q ∈ T is stated explicitly: q is the given midpoint, and T1's `≤` relates only members of T, so the bracketing chain `p ≤ q ≤ r` is well-typed only when q ∈ T — this membership is the consumer's to supply, q being given rather than constructed, whereas p ∈ T and r ∈ T are subsumed by p ∈ ⟦σ⟧ and r ∈ ⟦σ⟧ through the Definition's carrier clause.
- *Postconditions:* `q ∈ ⟦σ⟧`
- *Definition:* span membership is the half-open interval over T1 addresses — `x ∈ ⟦σ⟧ ⟺ x ∈ T ∧ start(σ) ≤ x < reach(σ)`; the carrier clause x ∈ T matches T12's Span definition `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}`, so membership records both carrier residence and the half-open bound. And `≤` abbreviates T1's strict order, `a ≤ b ≡ a < b ∨ a = b`.
- *Axiom:* T1 exports the strict order `<` with its transitivity postcondition (c), `(A a, b, c ∈ T : a < b ∧ b < c : a < c)`. The non-strict compositions the proof needs — `start(σ) ≤ q` from `start(σ) ≤ p` and `p ≤ q`, and `q < reach(σ)` from `q ≤ r` and `r < reach(σ)` — are *not* T1 exports; each is derived in the proof by case analysis on the abbreviation, every case reducing to (c) or to substitution of equals.
- *Frame:* σ is fixed; the claim asserts closure of ⟦σ⟧ under betweenness with no state transition.

- *Depends:*
  - T1 (LexicographicOrder, ASN-0034) — supplies the carrier T of tumbler addresses together with the strict order `<` on it, its transitivity postcondition (c), and the abbreviation `a ≤ b ≡ a < b ∨ a = b`. The carrier T grounds the Definition's membership clause x ∈ T and the precondition q ∈ T, T1's `<` and `≤` being relations on T × T. The proof composes the bracketing hypotheses into start(σ) ≤ q < reach(σ) by case analysis on the abbreviation, reducing each non-strict step to (c) or to substitution of equals; it does not cite a ≤-transitivity, which T1 does not export

---

## S9 — NormalizationUniqueness

Proves that the normalization of a span sequence is unique: any two normalized sequences that cover the same set of positions must be identical — same length and the same span at every index. The argument proceeds by contradiction, showing that any divergence at the first mismatched position would place a point inside one sequence's coverage but outside the other's, violating the assumption that both represent the same set.

*Formal Contract:*

- *Preconditions:* Σ̂₁ = ⟨α₁, ..., αₘ⟩ and Σ̂₂ = ⟨β₁, ..., βₙ⟩ are both normalized span sequences — each satisfies N1 (strictly increasing starts: start(γₖ) < start(γₖ₊₁)) and N2 (strict separation: reach(γₖ) < start(γₖ₊₁)). Each component span γₖ = (start(γₖ), width(γₖ)) is well-formed: start(γₖ), width(γₖ) ∈ T, the width is positive Pos(width(γₖ)), and its action point lies within the start's depth, actionPoint(width(γₖ)) ≤ #start(γₖ). Well-formedness is strictly stronger than the non-emptiness the case analysis invokes and subsumes it: a positive width strictly advances the start, so start(γₖ) < reach(γₖ). The two sequences are span-equivalent: ⟦Σ̂₁⟧ = ⟦Σ̂₂⟧ = S.
- *Postconditions:* Σ̂₁ = Σ̂₂ as sequences — equal length (m = n) and αₖ = βₖ for every index k.
- *Definition:* ⟦⟨γ₁, ..., γₖ⟩⟧ = ⋃ₗ ⟦γₗ⟧, where each span denotes the half-open interval ⟦γₗ⟧ = [start(γₗ), reach(γₗ)) and reach(γₗ) = start(γₗ) ⊕ width(γₗ); a span is identified by its start and width, so start and reach together determine it.
- *Axiom:* Left cancellation on the position monoid (TA-LC, ASN-0034): for a common start s and widths w₁, w₂ with s, w₁, w₂ ∈ T, Pos(w₁), Pos(w₂), actionPoint(w₁) ≤ #s, and actionPoint(w₂) ≤ #s, s ⊕ w₁ = s ⊕ w₂ ⟹ w₁ = w₂. These four operand preconditions are exactly the well-formedness of the two spans sharing start s, furnished by the well-formedness precondition above.

- *Depends:*
  - TA-LC (ASN-0034) — supplies the left-cancellation axiom (s ⊕ w₁ = s ⊕ w₂ ⟹ w₁ = w₂) used to rule out the equal-start-equal-reach divergence case; its operand preconditions Pos(w₁), Pos(w₂), actionPoint(w₁) ≤ #s, actionPoint(w₂) ≤ #s (at the shared start s) are discharged by S9's well-formedness precondition on the component spans
  - T1 (LexicographicOrder, ASN-0034) — supplies the total order on positions T against which the entire case analysis runs: the strict `<` with its transitivity postcondition (c), `(A a, b, c ∈ T : a < b ∧ b < c : a < c)`, and the abbreviation `a ≤ b ≡ a < b ∨ a = b`. Each case composes an N2 step (`<` on reaches) with a repeated N1 step (`≤` on starts) into a fresh strict inequality — reach(βⱼ) < start(αᵢ) in Cases 1a/1b and its mirror reach(αⱼ) = reach(βⱼ) < start(βᵢ) in Cases 3a/3b — and drives the strict runs start(αᵢ) < reach(αᵢ) = p < reach(βᵢ) of Case 2a and its Case 2b counterpart; the mixed `<`/`≤` composition is itself a consequence of (c) and the abbreviation, derived by case analysis rather than a separate T1 export, exactly as S0 and S11d treat their analogous steps. T1's order also fixes the half-open membership ⟦σ⟧ = [start(σ), reach(σ)) that every ∈/∉ test in the proof reads
  - TA-strict (StrictIncrease, ASN-0034) — supplies the strict-advance postcondition a ⊕ w > a at (a, w) = (start(σ), width(σ)) for each well-formed component span σ, yielding the per-span non-emptiness start(σ) < start(σ) ⊕ width(σ) = reach(σ) that Cases 2a and 2b rely on (the step start(αᵢ) < reach(αᵢ) placing p = reach(αᵢ) strictly inside ⟦βᵢ⟧, and its Case 2b mirror). Its preconditions Pos(width(σ)) and actionPoint(width(σ)) ≤ #start(σ) are exactly the well-formedness S9 already assumes of each component span

---

## SC — SpanClassification

Proves that any two non-degenerate spans stand in exactly one of five mutually exclusive relationships — separated, adjacent, proper overlap, containment, or equal — determined solely by comparing their four boundary points under the total order on positions. The case split is exhaustive and aligns precisely with intersection emptiness: the disjoint cases (separated, adjacent) correspond to ⟦α⟧ ∩ ⟦β⟧ = ∅, and the overlapping cases (proper overlap, containment, equal) correspond to ⟦α⟧ ∩ ⟦β⟧ ≠ ∅, where span denotations use the half-open convention that makes adjacency boundary-touching but position-disjoint.

*Formal Contract:*

- *Preconditions:* α and β are spans in the sense of the Span definition (ASN-0034) — each a pair (start, width) meeting Span's preconditions — so that, by T12, their starts and reaches lie in T, the domain of the total order T1, and each is non-degenerate: start(α) < reach(α) and start(β) < reach(β).
- *Postconditions:* Exactly one of the five cases (i)–(v) holds. Moreover the case determines intersection emptiness: ⟦α⟧ ∩ ⟦β⟧ = ∅ iff the case is (i) or (ii), and ⟦α⟧ ∩ ⟦β⟧ ≠ ∅ iff the case is (iii), (iv), or (v).
- *Definition:* The denotation of a span γ is ⟦γ⟧ = span(start(γ), width(γ)) = { p : start(γ) ≤ p < reach(γ) } (reach exclusive) — the Span set (ASN-0034) named in boundary-point form via the projections start(γ), width(γ) and the displaced endpoint reach(γ) = start(γ) ⊕ width(γ); this is the convention under which adjacency (reach(α) = start(β)) shares no position.
- *Axiom:* T1 — positions are totally ordered, so any two of the four boundary points {start(α), reach(α), start(β), reach(β)} are comparable, which is what makes the case split exhaustive and the cases mutually exclusive. The case-(iv) containment argument uses T1 further: its strict transitivity postcondition (c), `(A a, b, c ∈ T : a < b ∧ b < c : a < c)`, and the abbreviation `a ≤ b ≡ a < b ∨ a = b` compose the non-strict `start(α) ≤ q` (from `start(α) ≤ start(β)` and `start(β) ≤ q`) and the mixed `q < reach(α)` (from `q < reach(β)` and `reach(β) ≤ reach(α)`). Neither composition is a T1 export; each is derived in the proof by case analysis on the abbreviation, every case reducing to (c) or to substitution of equals.
- *Frame:* Classification reads only the four boundary points start(α), reach(α), start(β), reach(β); it neither modifies α, β, nor their denotations.

- *Depends:*
  - Span (Span, ASN-0034) — fixes the span type as a pair (s, ℓ), its projections start(σ) = s and width(σ) = ℓ, the displaced endpoint reach(σ) = s ⊕ ℓ, and the denotation span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ} that ⟦σ⟧ abbreviates.
  - T12 (SpanWellDefinedness, ASN-0034) — discharges reach(σ) = s ⊕ ℓ ∈ T (postcondition a), making each reach a position T1 can compare, and s ∈ span(s, ℓ), i.e. start(σ) < reach(σ) (postcondition b), grounding the non-degeneracy of well-formed spans.
  - T1 (LexicographicOrder, ASN-0034) — supplies the total order on positions whose comparability of any two boundary points makes the five-case split exhaustive and mutually exclusive; it also supplies the strict transitivity postcondition (c), `(A a, b, c ∈ T : a < b ∧ b < c : a < c)`, and the abbreviation `a ≤ b ≡ a < b ∨ a = b` from which the case-(iv) containment derives `start(α) ≤ q` and `q < reach(α)` by case analysis. These non-strict and mixed compositions are not T1 exports — T1 exports no ≤-transitivity and no mixed ≤-< transitivity — but consequences derived in the proof, each case reducing to (c) or to substitution of equals

---

## S11d — GeneralDifferenceBound

Proves that for any two level-uniform, level-compatible spans, their set difference is always expressible as a span-set of at most 2 spans. The bound is achievable rather than universal: within the containment case ⟦β⟧ ⊂ ⟦α⟧, the difference is 2 spans exactly when neither boundary coincides and 1 span when one coincides, so no single span suffices in general; all other span-comparison cases yield 0 or 1. This confirms that Nelson's span-set representation is sufficient to close the span algebra under difference.

*Formal Contract:*

- *Preconditions:* α and β are well-formed level-uniform spans; level_compat(start(α), start(β)) holds.
- *Postconditions:* ⟦α⟧ \ ⟦β⟧ is expressible as a span-set of at most 2 spans. The bound 2 is achievable — and hence cannot be reduced globally to 1 — because S11's sub-case (c) exhibits a proper-containment instance (⟦β⟧ ⊂ ⟦α⟧ with neither boundary coinciding) in which no single span represents the difference. Achievability is not universality, however: the count is exactly 2 precisely when ⟦β⟧ ⊂ ⟦α⟧ *and* neither boundary coincides — equivalently start(α) < start(β) and reach(β) < reach(α), S11 sub-case (c) — whereas proper containment with exactly one boundary coinciding (S11 sub-case b) yields 1 span, not 2. Hence ⟦β⟧ ⊂ ⟦α⟧ (SC case iv) does not by itself force the count to 2. Every other SC case yields at most 1 span, and SC cases (iv reverse) and (v) yield 0.
- *Definition:* The difference span-set is determined by the SC case of (α, β): SC(i)/(ii) → {α}; SC(iii) → the single residual span from S11c; SC(iv) with ⟦β⟧ ⊂ ⟦α⟧ → the at-most-2 residual spans from S11; SC(iv) with ⟦α⟧ ⊆ ⟦β⟧ → ∅; SC(v) → ∅.

- *Depends:*
  - SC (SpanClassification) — supplies the exhaustive five-case split invoked by "By SC" that structures the entire proof of S11d
  - T1 (LexicographicOrder, ASN-0034) — supplies the building blocks of the SC(iv)-reverse inline derivation of ⟦α⟧ ⊆ ⟦β⟧: the carrier T together with the strict order `<` on it, its transitivity postcondition (c), `(A a, b, c ∈ T : a < b ∧ b < c : a < c)`, and the abbreviation `a ≤ b ≡ a < b ∨ a = b`. The carrier T grounds the membership t ∈ ⟦α⟧ from which the derivation draws its fresh t, T1's `<` and `≤` being relations on T. The two compositions the derivation performs — the non-strict start(β) ≤ t from start(β) ≤ start(α) and start(α) ≤ t, and the mixed t < reach(β) from t < reach(α) and reach(α) ≤ reach(β) — are *not* T1 exports; each is derived inline by case analysis on the abbreviation, every case reducing to (c) or to substitution of equals, just as S0 derives its own non-strict bounds. T1 exports no ≤-transitivity and no mixed ≤-< transitivity for these steps to cite. SC supplies the boundary ordering start(β) ≤ start(α) and reach(α) ≤ reach(β) that the case analysis consumes; T1 supplies only the carrier and the strict (c) from which it composes start(β) ≤ t < reach(β), placing t ∈ ⟦β⟧
  - S11a (DifferenceSeparated) — supplies the result ⟦α⟧ \ ⟦β⟧ = ⟦α⟧ (1 span) used for SC cases (i) and (ii) in the table
  - S11c (DifferenceOverlap) — supplies the 1-span residual result used for SC case (iii) in the table
  - S11 (DifferenceBound) — supplies the at-most-2-span result for SC case (iv) (⟦β⟧ ⊂ ⟦α⟧) and establishes that the bound 2 is tight
  - S11b (DifferenceEqual) — supplies the result ⟦α⟧ \ ⟦β⟧ = ∅ (0 spans) used for SC case (v) in the table

---

## S3b — MergeSplitInverse

Proves that merge followed by split is a lossless round-trip: merging two adjacent, level-uniform spans and then splitting the result at their shared boundary exactly recovers the original pair. The left/right assignment of the output is not arbitrary — it tracks the adjacency direction, with the left-to-right ordering of the inputs preserved.

*Formal Contract:*

- *Preconditions:* α and β are well-formed level-uniform spans (in particular non-empty: width(α) > 0 and width(β) > 0); level_compat(start(α), start(β)) holds; α and β are adjacent, i.e. reach(α) = start(β) ∨ reach(β) = start(α).
- *Postconditions:* Let γ = merge(α, β) (S3) and let p be the shared boundary (p = start(β) in Case A, p = start(α) in Case B); then split(γ, p) (S4) yields ⟨λ, ρ⟩ with {λ, ρ} = {α, β}. In Case A (reach(α) = start(β)): λ = α and ρ = β. In Case B (reach(β) = start(α)): λ = β and ρ = α.
- *Frame:* No spans other than α, β are read or produced; γ, λ, ρ are the only constructed values.
- *Definition:* The shared boundary p is the interior point of γ at which the original adjacency met (start(β) in Case A, start(α) in Case B); interiority start(γ) < p < reach(γ) is what makes p an admissible split point for S4.

- *Depends:*
  - S3 (MergeEquivalence) — supplies the merge operation and the endpoint formula γ = (s, r ⊖ s) with s = min(start(α), start(β)) and r = max(reach(α), reach(β)), used in both cases
  - S4 (SplitPartition) — supplies the split operation; the proof invokes split(γ, p) and reads off λ and ρ from S4's output structure
  - WR (WidthRecovery) — supplies reach(σ) ⊖ start(σ) = width(σ), used twice in each case to identify the split parts as α and β
  - TA-strict (StrictIncrease, ASN-0034) — supplies the strict-advance postcondition a ⊕ w > a at (a, w) = (start(σ), width(σ)) for each well-formed σ ∈ {α, β}, yielding the two non-emptiness facts start(α) < reach(α) and start(β) < reach(β) (cited as (†) in the proof); these ground every interiority step start(γ) < p < reach(γ) in both Case A and Case B, and the min/max determination of γ's endpoints from the adjacency hypothesis

---

## S10 — UnionOrderIndependence

Proves that span-set union is commutative and associative under normalization: whenever the participating spans are level-uniform and mutually level-compatible, the normalized union is the same regardless of operand order or grouping. The result follows because span-sets carry set-theoretic denotations — what matters is which bytes are designated, not how the contributing sets are arranged — so equal denotations force equal normalized forms by the uniqueness guarantee of S9.

*Formal Contract:*

- *Preconditions:* For commutativity, the component spans of Σ₁ and Σ₂ are well-formed level-uniform spans and mutually level-compatible across both sets. For associativity, the component spans of Σ₁, Σ₂, and Σ₃ are well-formed level-uniform spans and mutually level-compatible across all three sets. S8 (existence of a normalized equivalent) and S9 (uniqueness of the normalized form for a given denotation) hold.
- *Postconditions:* normalize(Σ₁ ∪ Σ₂) = normalize(Σ₂ ∪ Σ₁); and normalize((Σ₁ ∪ Σ₂) ∪ Σ₃) = normalize(Σ₁ ∪ (Σ₂ ∪ Σ₃)).
- *Axiom:* The denotation of a span-set union is the union of the operand denotations: ⟦Σᵢ ∪ Σⱼ⟧ = ⟦Σᵢ⟧ ∪ ⟦Σⱼ⟧. This holds by the set-theoretic semantics of span-sets (Nelson, Q8): a span-set designates a byte collection, so a combined set designates exactly the bytes designated by either operand, with no dependence on order or multiplicity.
- *Frame:* Forming a union introduces no new spans; the well-formedness, level-uniformity, and mutual level-compatibility hypotheses are therefore preserved under union, and each union span-set remains within S8's domain.

- *Depends:*
  - S8 (NormalizationExistence) — supplies existence of a normalized equivalent for each union span-set; invoked in both the commutativity and associativity sub-proofs to assert that A and B are normalized equivalents with ⟦A⟧ = ⟦B⟧
  - S9 (NormalizationUniqueness) — supplies uniqueness of the normalized form; the proof concludes A = B in both sub-proofs by applying S9 to two normalized span-sets with equal denotation

---

## S7 — CoveringExistence

Proves that any finite set of positions can be covered by a matching-cardinality span-set, but establishes that exact representation is structurally impossible: every non-empty span denotes an infinite set (because every tumbler has infinitely many proper deeper extensions), so the covering guarantee ⟦Σ⟧ ⊇ P is the strongest finite result available and no span-set can achieve ⟦Σ⟧ = P for finite P.

*Formal Contract:*

- *Preconditions:* P ⊂ T is a finite set of positions.
- *Postconditions:* there exists a span-set Σ with |Σ| = |P| and ⟦Σ⟧ ⊇ P; moreover, when P is non-empty and finite no span-set Σ satisfies ⟦Σ⟧ = P, since ⟦Σ⟧ is infinite for every non-empty Σ.
- *Definition:* The covering construction. Enumerate the finite set P as t₁, ..., tₘ with m = |P|. For each position tᵢ set ℓᵢ = [0, ..., 0, 1] with #ℓᵢ = #tᵢ (zero in every component except the last, which is 1), and take the span (tᵢ, ℓᵢ). The witness span-set is the sequence Σ = ⟨(t₁, ℓ₁), ..., (tₘ, ℓₘ)⟩, whose length is |Σ| = m = |P|.
- *Axiom:* T0's comprehension axiom — T is the set of all finite sequences over ℕ of length ≥ 1 — supplies the membership s.0ⁿ ∈ T of each trailing-zero extension of s; together with the infinitude of ℕ (the extensions s.0ⁿ have pairwise distinct lengths #s + n, so they are infinitely many) this makes ⟦σ⟧ infinite and forces the finite-vs-infinite mismatch.

- *Depends:*
  - T12 (SpanWellDefinedness, ASN-0034) — supplies the span well-formedness predicate (Pos(ℓ) and actionPoint(ℓ) ≤ #t) that certifies the constructed span (t, ℓ) is valid, invoked in the covering construction and again in the exact-representation argument
  - TA-strict (StrictIncrease, ASN-0034) — supplies t ⊕ ℓ > t, establishing t ∈ [t, t ⊕ ℓ) and confirming each covering span contains its target position
  - TumblerAdd (TumblerAdd, ASN-0034) — supplies the component-level definition reach(s, ℓ)ₖ = sₖ + ℓₖ used to show rₖ > sₖ when establishing that every proper deeper extension lies strictly below reach(s, ℓ)
  - T1 (LexicographicOrder, ASN-0034) — supplies case (ii) (prefix convention) to place every deeper extension e strictly above s, and case (i) (component divergence) to place e strictly below reach(s, ℓ), together confirming e ∈ ⟦(s, ℓ)⟧
  - T0 (CarrierSetDefinition, ASN-0034) — its comprehension axiom populates T with every finite sequence over ℕ of length ≥ 1, so each trailing-zero extension s.0ⁿ is a member of T; together with the infinitude of ℕ (the extensions have pairwise distinct lengths #s + n) this grounds the infinite-span argument that forces the finite-vs-infinite mismatch

---

## S6 — LevelConstraint

Defines level-compatibility as the requirement that two tumblers share the same length, and establishes that a span is level-uniform when its start and width tumblers satisfy this condition. For a well-formed level-uniform span — one whose width is a positive displacement acting within the start's depth, so its reach is defined — start, width, and reach all inhabit the same tumbler length, and a single depth governs the entire span. Gregory's implementation enforces this invariant at the split operation, aborting when the cut and width differ in tumbler length.

*Formal Contract:*

- *Preconditions:* σ = (s, ℓ) is a well-formed level-uniform span: s ∈ T, ℓ ∈ T, level_compat(s, ℓ) (i.e. #s = #ℓ), Pos(ℓ), and actionPoint(ℓ) ≤ #s. The last two — TumblerAdd's preconditions instantiated at (a, w) = (s, ℓ) — are what make reach(σ) = s ⊕ ℓ defined with s ⊕ ℓ ∈ T, so TumblerAdd's result-length postcondition applies. They are not implied by level-uniformity: a level-uniform pair with Pos(ℓ) failing has reach(σ) undefined, and the length identity below does not hold of it.
- *Postconditions:* start, width, and reach inhabit a single tumbler length: #start(σ) = #width(σ) = #reach(σ) = #s. The reach equality, #reach(σ) = #(s ⊕ ℓ) = #ℓ, is read directly off TumblerAdd's result-length identity — whose preconditions the Preconditions discharge; level-uniformity (#ℓ = #s) then closes the chain to #s.
- *Depends:*
  - TumblerAdd (TumblerAdd, ASN-0034) — supplies the result-length identity #(a ⊕ w) = #w, an exported postcondition of ⊕, together with the preconditions a ∈ T, w ∈ T, Pos(w), actionPoint(w) ≤ #a that it is earned under. Instantiated at the start s and width ℓ of the well-formed level-uniform span — where Pos(ℓ) and actionPoint(ℓ) ≤ #s hold, so s ⊕ ℓ is defined and s ⊕ ℓ ∈ T — it gives #reach(σ) = #(s ⊕ ℓ) = #ℓ; the level-uniform hypothesis #ℓ = #s then closes #reach(σ) = #s. This is the sole source of the addition result-length: the in-scope foundations supply only the subtraction length (TumblerSub: #(a ⊖ w) = L) and the round-trip identity (D1: a ⊕ (b ⊖ a) = b), neither of which yields #(s ⊕ ℓ) = #ℓ for a general width ℓ.

---

## InteriorPoint — InteriorPoint

Defines a strict-interior predicate for a span: position p is interior to σ when it falls strictly between the start and the reach, excluding both endpoints. Because the denotation ⟦σ⟧ uses a closed-open interval [start, reach), every interior point is automatically a member of the span's point set.

---

## S11 — DifferenceBound

Proves that when a level-uniform span β is contained within a level-uniform span α, their set difference decomposes into at most two spans: a left span covering the gap before β's start and a right span covering the gap after β's reach, with empty components omitted. The two-span bound is tight — when neither boundary coincides, no single span can represent the disconnected remainder, as convexity (S0) would force the excluded middle region into any purported single-span cover.

*Formal Contract:*

- *Preconditions:* α and β are well-formed level-uniform spans; level_compat(start(α), start(β)); ⟦β⟧ ⊆ ⟦α⟧.
- *Postconditions:* ⟦α⟧ \ ⟦β⟧ = ⟦λ⟧ ∪ ⟦ρ⟧ is expressible as a span-set of at most two spans, where the empty-interval components are omitted; its cardinality is 0 when α = β, 1 when exactly one boundary coincides, and 2 when neither coincides; in the two-span case the bound is tight — no single span γ satisfies ⟦γ⟧ = ⟦λ⟧ ∪ ⟦ρ⟧.
- *Definition:* When start(α) < start(β), the left difference span is λ = (start(α), start(β) ⊖ start(α)), well-formed and level-uniform by WF with reach(λ) = start(β). When reach(β) < reach(α), the right difference span is ρ = (reach(β), reach(α) ⊖ reach(β)), well-formed and level-uniform by WF with reach(ρ) = reach(α).
- *Axiom:* TumblerAdd's carrier postcondition a ⊕ w ∈ T, instantiated at (start(σ), width(σ)) under each span σ ∈ {α, β}'s well-formedness, places reach(α), reach(β) ∈ T at the outset. The boundary characterization start(α) ≤ start(β) and reach(β) ≤ reach(α) follows from ⟦β⟧ ⊆ ⟦α⟧ together with the totality of T1 — its reach half relying on reach(α) ∈ T to test reach(α) for membership in ⟦β⟧ = {t ∈ T : start(β) ≤ t < reach(β)}; non-emptiness of β (start(β) < reach(β)) holds by S2; a witness t ∈ ⟦β⟧ is bracketed between the two members start(α), reach(β) ∈ ⟦γ⟧ by discharging S0's precondition start(α) ≤ t ≤ reach(β) — t ≤ reach(β) by weakening t < reach(β) (left disjunct of a ≤ b ≡ a < b ∨ a = b), and start(α) ≤ t by composing the strict start(α) < start(β) with the non-strict start(β) ≤ t through a case-split on the abbreviation (postcondition (c) of T1 when start(β) < t, substitution of equals when start(β) = t), mirroring S0's own ≤-composition technique since T1 does not export this mixed step — after which S0 (convexity) forces the bracketed t ∈ ⟦γ⟧. WF's carrier preconditions s, r ∈ T are immediate for λ — start(α) and start(β) are span starts, hence in T — while for ρ, whose endpoints are the sums reach(σ) = start(σ) ⊕ width(σ), they are exactly the reach(α), reach(β) ∈ T already placed from TumblerAdd. WF's length preconditions are discharged from S6: level-uniformity gives #reach(σ) = #start(σ) for each span (start, width, and reach share one tumbler length via TumblerAdd's result-length identity), so level_compat(start(α), start(β)) propagates to #start(α) = #start(β) for λ and #reach(β) = #reach(α) for ρ.

- *Depends:*
  - T1 (LexicographicOrder, ASN-0034) — supplies the strict total order whose totality partitions ⟦α⟧ into the three sub-ranges (L)/(M)/(R) and underwrites the containment boundary derivation
  - S2 (EmptyDistinction) — supplies non-emptiness of β (start(β) < reach(β)), used in the tightness argument to obtain a witness t ∈ ⟦β⟧ lying between the two members of ⟦γ⟧
  - WF (WellFormedSpanFromEndpoints) — supplies the construction that turns endpoint pairs into well-formed level-uniform spans; applied twice, once each for λ and ρ, to guarantee the difference spans are valid
  - S6 (LevelConstraint) — supplies the level-uniformity consequence that a span's start, width, and reach share one tumbler length, i.e. #reach(σ) = #start(σ) via TumblerAdd's result-length identity #(start(σ) ⊕ width(σ)) = #width(σ); applied to α and β and combined with level_compat, it discharges WF's length precondition #reach(β) = #reach(α) for ρ (the dual #start(α) = #start(β) for λ being level_compat directly)
  - TumblerAdd (TumblerAdd, ASN-0034) — supplies two exported postconditions of ⊕, both instantiated at (a, w) = (start(σ), width(σ)) under σ's well-formedness, where reach(σ) = start(σ) ⊕ width(σ). First, the carrier postcondition a ⊕ w ∈ T, applied to both α and β at the outset, gives reach(α) ∈ T and reach(β) ∈ T; this membership is consumed twice. It is needed already in the boundary characterization, whose reach half places reach(α) in ⟦β⟧ = {t ∈ T : start(β) ≤ t < reach(β)} — a membership that requires reach(α) ∈ T over and above the two order conditions start(β) ≤ reach(α) < reach(β) — and again in the ρ-construction, where reach(α), reach(β) ∈ T discharge WF's carrier preconditions s, r ∈ T (ρ's endpoints are computed sums, not primitive start tumblers, so without this step they would not be known to lie in T and WF could not be applied). Second, the result-length identity #(a ⊕ w) = #w, read as #(start(σ) ⊕ width(σ)) = #width(σ) and composed with the defining #width(σ) = #start(σ) to give #reach(σ) = #start(σ), discharges WF's length precondition #reach(β) = #reach(α).
  - S0 (Convexity) — supplies the convexity property invoked in the tightness contradiction: a point t ∈ ⟦β⟧ lying between two members of ⟦γ⟧ must belong to ⟦γ⟧, yielding the contradiction t ∉ ⟦λ⟧ ∪ ⟦ρ⟧

---

## NormalizedSpanSet — NormalizedSpanSet

Defines the canonical two-part form a span-set must satisfy to be considered fully reduced: its spans must appear in strictly increasing order of start position, and each span must end strictly before the next one begins. Together these conditions rule out both overlap and adjacency, ensuring no two spans could be merged — the normalized form is the unique irreducible representation of a covered region.

---

## S4 — SplitPartition

Proves that splitting a level-uniform span σ at any interior, level-compatible point p yields exactly two adjacent sub-spans λ and ρ whose content-sets partition ⟦σ⟧ without overlap or omission. The split is unique and forced by the total order on tumblers: elements before p fall into the left span, elements from p onward into the right, with the two spans meeting exactly at p.

*Formal Contract:*

- *Preconditions:* σ = (s, ℓ) is a well-formed level-uniform span; p ∈ T — the interiority constraint below asserts s < p < reach(σ), and < compares only members of the carrier T, so p must lie in T for that assertion to be well-defined; this membership is the consumer's to supply, p being given rather than constructed, whereas the companion operands are placed within the contract — s ∈ T is subsumed by σ's well-formedness and reach(σ) ∈ T by TumblerAdd's carrier postcondition; p is an interior point of σ, i.e. s < p < reach(σ); level_compat(s, p) holds, i.e. #p = #s.
- *Definition:* d = p ⊖ s and d' = reach(σ) ⊖ p; the left span is λ = (s, d) and the right span is ρ = (p, d').
- *Postconditions:* λ and ρ are well-formed level-uniform spans (by T12) with #d = #s = #d'; their WF endpoints lie in T — λ's are the span start s and the given interior point p, while ρ's reach endpoint reach(σ) = start(σ) ⊕ width(σ) is placed in T by TumblerAdd's carrier postcondition a ⊕ w ∈ T instantiated at (start(σ), width(σ)) under σ's well-formedness; reach(λ) = p and reach(ρ) = reach(σ); ⟦λ⟧ ∪ ⟦ρ⟧ = ⟦σ⟧ (a); ⟦λ⟧ ∩ ⟦ρ⟧ = ∅ (b); reach(λ) = start(ρ) = p (c).
- *Frame:* σ = (s, ℓ) is unchanged; the split produces λ and ρ without modifying the original span.

- *Depends:*
  - T12 (SpanWellDefinedness, ASN-0034) — supplies the well-formedness predicate (Pos(ℓ) and actionPoint ≤ #s) that the proof verifies for both λ and ρ, and the Formal Contract's postcondition targets
  - WF (WellFormedSpanFromEndpoints) — supplies the construction invoked twice in the proof to conclude that λ = (s, d) and ρ = (p, d') are well-formed level-uniform spans with the stated reaches; its postcondition reach(λ) = s ⊕ (p ⊖ s) = p is read directly in part (c) to establish reach(λ) = p = start(ρ)
  - TumblerAdd (TumblerAdd, ASN-0034) — supplies the carrier postcondition a ⊕ w ∈ T, instantiated at (a, w) = (start(σ), width(σ)) under σ's well-formedness, to place reach(σ) = start(σ) ⊕ width(σ) ∈ T; this discharges WF's carrier precondition for ρ's reach endpoint (ρ = (p, reach(σ) ⊖ p) supplies reach(σ) as WF's r), the start endpoint p being the given interior point, already in T
  - T1 (LexicographicOrder, ASN-0034) — supplies the total-order properties on T that the partition argument invokes directly. Trichotomy underwrites part (a): every t with s ≤ t < reach(σ) satisfies t < p or p ≤ t, so {t : s ≤ t < p} ∪ {t : p ≤ t < reach(σ)} = {t : s ≤ t < reach(σ)} with no element left uncovered at the split point p. Irreflexivity and transitivity underwrite part (b): a t meeting both t < p and p ≤ t would chain (transitivity, via the definition of ≥) to p < p, which irreflexivity forbids — hence ⟦λ⟧ ∩ ⟦ρ⟧ = ∅

---

## S11a — DifferenceSeparated

Proves that when two level-uniform spans are separated or adjacent — the two disjoint cases under SC's classification — subtracting one from the other leaves the minuend unchanged: ⟦α⟧ \ ⟦β⟧ = ⟦α⟧. Because disjointness means the spans share no positions, the subtraction removes nothing and the result is a single-span span-set equal to α itself.

*Formal Contract:*

- *Preconditions:* α and β are well-formed level-uniform spans; level_compat(start(α), start(β)) holds; SC classifies the pair (α, β) as case (i) (separated) or case (ii) (adjacent).
- *Postconditions:* ⟦α⟧ \ ⟦β⟧ = ⟦α⟧, a span-set of exactly 1 span.
- *Axiom:* SC classifies cases (i) and (ii) as the disjoint cases — i.e. ⟦α⟧ ∩ ⟦β⟧ = ∅ holds by SC's classification of separated and adjacent pairs.
- *Frame:* α is preserved unchanged; β contributes no positions to the result.

- *Depends:*
  - SC (SpanClassification) — supplies the disjoint-case result ⟦α⟧ ∩ ⟦β⟧ = ∅ for cases (i) and (ii), which is the axiom on which the proof that ⟦α⟧ \ ⟦β⟧ = ⟦α⟧ rests

---

## MutuallyLevelCompatible — MutuallyLevelCompatible

Defines what it means for a collection of spans to be mutually level-compatible: all start tumblers share the same address length L. When each span is also level-uniform, this single length constraint propagates to every boundary tumbler in every span, so any two endpoints drawn from anywhere in the collection are directly comparable without consulting an external index.

---

## S1 — IntersectionClosure

Proves that the intersection of two level-uniform, level-compatible spans is always either empty or a single contiguous span — never a fragmented set. The candidate interval [max(start(α), start(β)), min(reach(α), reach(β))) is computed from the boundary tumblers directly, and level-uniformity guarantees that when this interval is non-empty, it constitutes a well-formed level-uniform span γ.

*Formal Contract:*

- *Preconditions:* α and β are well-formed level-uniform spans; level_compat(start(α), start(β)) holds.
- *Postconditions:* Either ⟦α⟧ ∩ ⟦β⟧ = ∅, or there exists a span γ with ⟦γ⟧ = ⟦α⟧ ∩ ⟦β⟧. In the non-empty case γ = (s', r' ⊖ s') is well-formed and level-uniform with start(γ) = s' and reach(γ) = r'.
- *Definition:* s' = max(start(α), start(β)) and r' = min(reach(α), reach(β)); the candidate span is γ = (s', r' ⊖ s'). The intersection is non-empty iff r' > s'.
- *Invariant:* ⟦α⟧ ∩ ⟦β⟧ ⊆ {t : s' ≤ t < r'} holds unconditionally, independent of the case split.
- *Axiom:* By S6, level-uniformity of α and β forces all four boundary tumblers start(α), reach(α), start(β), reach(β) to share a common length, so #s' = #r'. WF's endpoint-carrier preconditions are met as well: s' = max(start(α), start(β)) is a span start, hence in T directly, while r' = min(reach(α), reach(β)) is placed in T by TumblerAdd's carrier postcondition a ⊕ w ∈ T instantiated at (start(σ), width(σ)) under each well-formed σ ∈ {α, β}, since r' is one of reach(α), reach(β). With s', r' ∈ T, #s' = #r', and s' < r', WF yields well-formedness of γ.

- *Depends:*
  - S6 (LevelConstraint) — supplies the level-uniformity consequence that all four boundary tumblers share a common length, giving #s' = #r', which is the precondition fed to WF in the proof's final step
  - WF (WellFormedSpanFromEndpoints) — supplies the well-formedness construction invoked to produce γ = (s', r' ⊖ s') from s' < r' and #s' = #r', establishing that γ is a well-formed level-uniform span with reach(γ) = r'
  - TumblerAdd (TumblerAdd, ASN-0034) — supplies the carrier postcondition a ⊕ w ∈ T, instantiated at (a, w) = (start(σ), width(σ)) under each well-formed σ ∈ {α, β}, to place reach(α), reach(β) ∈ T; the reach endpoint r' = min(reach(α), reach(β)) is one of these, so r' ∈ T, discharging WF's carrier precondition for the reach endpoint (the start endpoint s' = max(start(α), start(β)) being a span start, already in T)
  - T1 (LexicographicOrder, ASN-0034) — supplies the total order on T that drives the forward inclusion: the ≤/< comparisons and the max/min over the boundary tumblers that bracket every t ∈ ⟦α⟧ ∩ ⟦β⟧ into the interval [s', r'), and the order underlying the case split r' against s' and the membership s' < r'

---

## S5 — SplitWidthComposition

Proves that when a span σ is split at an interior point, the two part-widths compose back to the original span width: d ⊕ d' = ℓ. The result follows by chaining the two displacement equations from S4 through the associativity law TA-assoc and then canceling the common base address via TA-LC.

*Formal Contract:*

- *Preconditions:*
  - The conditions of S4 hold, with p the split point satisfying s < p < reach(σ).
  - Equal lengths: #s = #d = #p and #p = #d' = #reach, with equal length excluding the prefix case so that divergence(s, p) ≤ #s and divergence(p, reach(σ)) ≤ #p (D1 applicable to both s ⊕ d = p and p ⊕ d' = reach(σ)).
  - reach(σ) = s ⊕ ℓ (ℓ is the width of σ measured from s).
  - Pos(d), Pos(d'), Pos(ℓ) (Span validity of λ, ρ from S4's construction; of σ by hypothesis).
  - k_d ≤ #s and k_{d'} ≤ #p = #s (Span validity of λ, ρ from S4), with level-uniformity of λ giving #d = #s so that k_{d'} ≤ #d.
  - actionPoint(ℓ) ≤ #s (Span validity of σ, by hypothesis).
- *Postconditions:*
  - d ⊕ d' = ℓ.
  - As established by TA-assoc en route: Pos(d ⊕ d') and actionPoint(d ⊕ d') = min(k_d, k_{d'}).

- *Depends:*
  - S4 (SplitPartition) — supplies the split setup (interior point p, spans λ and ρ, displacements d = p ⊖ s and d' = reach(σ) ⊖ p) that S5's conditions and proof chain inherit, and constructs λ, ρ as well-formed spans, so their Span validity (Pos(d), Pos(d'), action-point bounds k_d, k_{d'}) discharges the TA-assoc/TA-LC preconditions
  - D1 (DisplacementRoundTrip, ASN-0034) — supplies the round-trip identity used in the two proof steps 'By D1, s ⊕ d = p' and 'By D1 again, p ⊕ d' = reach(σ)' that anchor the displacement chain
  - TA-assoc (ASN-0034) — supplies associativity of ⊕ together with the side conclusions Pos(d ⊕ d') and actionPoint(d ⊕ d') = min(k_d, k_{d'}) that the proof discharges into TA-LC
  - Span (Span, ASN-0034) — defines span validity as Pos(ℓ) ∧ actionPoint(ℓ) ≤ #s; this predicate (not a T12 postcondition — T12 *consumes* it as a precondition) supplies Pos and the action-point bounds for σ (well-formed by hypothesis) and for λ, ρ (well-formed by S4's construction) that discharge TA-assoc and TA-LC
  - TA-LC (ASN-0034) — supplies the left-cancellation principle applied with a := s, x := d ⊕ d', y := ℓ to yield the claim's conclusion d ⊕ d' = ℓ
  - T1 (LexicographicOrder, ASN-0034) — supplies the case structure of s < p (case (i) `k ≤ #s` vs case (ii) `k = #s + 1 ≤ #p`) used to discharge D1's precondition divergence(s, p) ≤ #s; the equal-length hypothesis excludes case (ii), leaving the case-(i) witness k ≤ #s. Applied identically to the pair (p, reach(σ)) for the second D1 invocation
  - Divergence (Divergence, ASN-0034) — its case-(i) uniqueness clause identifies the T1 case-(i) witness k with divergence(s, p) (resp. divergence(p, reach(σ))), so k ≤ #s (resp. ≤ #p) discharges D1's remaining precondition
  - NAT-addcompat (NatAdditionOrderAndSuccessor, ASN-0034) — supplies the successor inequality #s < #s + 1 (resp. #p < #p + 1) that, with equal length, refutes T1 case (ii)'s bound #s + 1 ≤ #s, excluding the prefix case
  - NAT-order (NatStrictTotalOrder, ASN-0034) — its irreflexivity `¬(#s < #s)` completes the case-(ii) elimination once NAT-addcompat reduces the case bound to #s < #s

---

## S2 — EmptyDistinction

Proves that the denotation map on well-formed spans never produces the empty set: every well-formed span contains at least its start position, because TA-strict's strict-advancement postcondition — given the well-formedness precondition that the length is strictly positive — forces the end offset strictly past the start. As a consequence, the empty set lies entirely outside the image of denotation — the empty intersection of two disjoint spans is not a zero-width span but a set with no preimage, a distinction that prevents zero-length spans from contaminating downstream interval arithmetic.

*Formal Contract:*

- *Definition:* A well-formed span (s, ℓ) denotes the half-open interval ⟦s, ℓ⟧ = [s, s ⊕ ℓ) = { p : s ≤ p < s ⊕ ℓ }, where s ⊕ ℓ is its (exclusive) end offset.
- *Preconditions:* The span is well-formed — the preconditions of Definition (Span), equivalently the preconditions of T12: s ∈ T, ℓ ∈ T, Pos(ℓ) (i.e. ℓ > 0), and actionPoint(ℓ) ≤ #s. The last is a comparison of natural numbers (actionPoint(ℓ) ∈ ℕ), not the type-incoherent comparison of the tumbler s ⊕ ℓ against #s.
- *Postconditions:* ⟦s, ℓ⟧ ≠ ∅; concretely s ∈ ⟦s, ℓ⟧ — exactly T12's postcondition (b), s ∈ span(s, ℓ), read through the set equality ⟦s, ℓ⟧ = span(s, ℓ) — so the denotation has at least one position. Consequently ∅ is not in the image of the denotation map.

- *Depends:*
  - T12 (SpanWellDefinedness, ASN-0034) — supplies its postcondition (b), s ∈ span(s, ℓ). Since span(s, ℓ) = { t : s ≤ t < s ⊕ ℓ } is, by Definition (Span), the denotation ⟦s, ℓ⟧, this postcondition is exactly S2's conclusion: the denotation contains its start position and so is non-empty. T12 does not supply S2's preconditions — s ∈ T, ℓ ∈ T, Pos(ℓ) (i.e. ℓ > 0), and actionPoint(ℓ) ≤ #s are S2's own hypotheses, the preconditions of Definition (Span) that T12 likewise assumes and from which T12 in turn derives (b) (via s ≤ s and the strict advancement s < s ⊕ ℓ a positive length forces).

---

