# Regional Review — ASN-0034/TA6 (cycle 1)

*2026-04-23 01:58*

### Missing ActionPoint claim
**Class**: REVISE
**Foundation**: (none — foundation ASN)
**ASN**: TA-PosDom proof: "Since `Pos(t)`, ActionPoint applies to `t` and supplies an index `actionPoint(t)` with (i) `1 ≤ actionPoint(t) ≤ #t`; (ii) `tᵢ = 0` for all `1 ≤ i < actionPoint(t)`; (iii) `t_{actionPoint(t)} ≥ 1`." TA-PosDom's Depends slot lists "ActionPoint (ActionPoint) — supplies `actionPoint(t)` and postconditions (i)–(iii)".
**Issue**: ActionPoint is cited as an available claim with three postconditions, but no ActionPoint claim is presented anywhere in the ASN content. Since the review preamble states this is a foundation ASN with no external foundations and says "review internal consistency only", ActionPoint must be internal — yet it is absent. TA-PosDom's proof therefore rests on a non-existent claim, and TA6's Conjunct 2 (which cites TA-PosDom) inherits the gap.
**What needs resolving**: Either ActionPoint must be stated as a claim in this ASN with its own proof (establishing (i)–(iii) from prior claims plus NAT-wellorder/NAT-zero), or TA-PosDom's proof must be rewritten to construct the witnessing index inline from the existential `Pos(t)` via NAT-wellorder directly, without appealing to an undefined `actionPoint(·)` operator.

### Spurious dependencies in TA6
**Class**: REVISE
**Foundation**: NAT-zero, NAT-order, TA-Pos, TA-PosDom
**ASN**: TA6 Depends lists `T3 (CanonicalRepresentation) — component-wise tumbler equality underpinning the `Zero(t)` characterization` and `NAT-discrete (NatDiscreteness) — discreteness of ℕ supporting the `tⱼ > 0 ⟺ tⱼ ≠ 0` step`.
**Issue**: (a) T3 is never invoked in the TA6 proof — `Zero(t)` is characterized by TA-Pos via component values, not via tumbler equality, so T3's sequence-equality bridge is irrelevant here. (b) The equivalence `tⱼ > 0 ⟺ tⱼ ≠ 0` is established from NAT-zero's `0 ≤ tⱼ` and NAT-order's `≤` definition + disjointness alone; NAT-discrete's successor-bound is not used. Both dependency entries are use-site inventory that does not match the proof.
**What needs resolving**: Remove T3 and NAT-discrete from TA6's Depends, or (if the author intends them) expose the proof step that actually requires them.

### Transitivity Case `k₂ < k₁` skips sub-case analysis
**Class**: REVISE
**Foundation**: T1 (LexicographicOrder)
**ASN**: T1 transitivity, Case `k₂ < k₁`: "Since `k₂ < k₁` and `a` has components below `k₁`, `k₂ ≤ m`."
**Issue**: Getting `k₂ ≤ m` needs to distinguish how `a < b` was witnessed. If via T1(i), `k₁ ≤ m` and `k₂ < k₁` give `k₂ < m`, hence `k₂ ≤ m`. If via T1(ii), `k₁ = m + 1`, so `k₂ < m + 1`, which requires NAT-discrete to conclude `k₂ ≤ m`. The phrase "a has components below k₁" is not a reason — in the T1(ii) subcase, `k₁ = m + 1` sits *above* m, so the informal justification does not carry. The proof skips the NAT-discrete invocation that the (ii) subcase requires.
**What needs resolving**: Split the `k₂ < k₁` case into the two subcases for how `a < b` was witnessed, and cite NAT-discrete explicitly when promoting `k₂ < m + 1` to `k₂ ≤ m` in the (ii) subcase. (NAT-discrete is already in T1's Depends, so no new foundation is needed.)

### T4 Exhaustion meta-prose and uniform-mechanism gloss
**Class**: OBSERVE
**Foundation**: T4 (HierarchicalParsing)
**ASN**: T4 Exhaustion Consequence: "The mechanism for excluding the branch `zeros(t) < m` given a lower bound `m ≤ zeros(t)` is uniform: unfolding `≤` to `m < zeros(t) ∨ m = zeros(t)` shows that one of trichotomy's other two alternatives holds, and trichotomy's exactly-one clause … then forbids the third."
**Issue**: This is a meta-commentary that describes the shape of the excluded-branch argument before it is performed, then repeats the same wording four times in the iterated case analysis. A single direct invocation per step would be shorter and easier to follow. The "uniform mechanism" framing is reviser drift — explaining why the pattern works rather than performing it.

VERDICT: REVISE
