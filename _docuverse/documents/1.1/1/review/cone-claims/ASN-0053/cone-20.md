The proofs of WF, S3b, and S6 hold up. The core dependencies — D1, D2, TumblerSub, ZPD — are correctly assembled and their preconditions discharged. One structural defect in WR's proof creates a cross-claim inconsistency with S3b, and two claims omit T1 from their Depends despite using its ordering properties directly.

### WR — ungrounded component appeal and formal contract mismatch
**Class**: REVISE
**Foundation**: TumblerAdd (TumblerAdd, ASN-0034) — component-level Definition: `rᵢ = aᵢ if i < k; rₖ = aₖ + wₖ; rᵢ = wᵢ if i > k`
**ASN**: WR (WidthRecovery) — divergence sub-proof: *"because reach(σ) = s ⊕ ℓ agrees with s below ℓ's action point and strictly exceeds it there, this k is the action point T12 bounds by #s"*
**Issue**: The proof uses TumblerAdd's component formulas (agreement below the action point; strict advancement at it) to identify the T1 witness k as the action point of ℓ. TumblerAdd is absent from WR's Depends. The identification is also unnecessary: the WF-style argument — T1 case (i)/(ii) analysis, equal lengths (#s = #reach(σ)) to exclude case (ii), Divergence uniqueness — delivers k ≤ #s directly without naming k as the action point, and requires only T1 and Divergence (both already in WR's Depends). The overcomplicated path both imports an uncited foundation and performs more work than the conclusion demands.

The formal contract compounds the issue by listing "divergence(s, reach(σ)) = k ≤ #s of type (i) (T1, Divergence)" as a caller-supplied precondition, while the proof body establishes it. S3b invokes WR twice with only "α (resp. β) is a well-formed level-uniform span" as the justification — correct given what the proof actually derives, but inconsistent with the formal contract. A per-claim check of S3b against WR's stated contract would flag the divergence condition as unsupplied; only reading both together exposes that WR derives it internally.
**What needs resolving**: The unnecessary action-point identification step must be removed and replaced with the WF-style argument (T1 case analysis + equal lengths + Divergence uniqueness). The divergence condition must be removed from WR's formal contract precondition list — it is an intermediate result, not a caller obligation. Once resolved, the formal contract's true minimal precondition ("σ is a well-formed level-uniform span") matches what S3b supplies, closing the cross-claim inconsistency.

---

### S3, S4 — T1 absent from Depends for direct order reasoning
**Class**: REVISE
**Foundation**: T1 (LexicographicOrder, ASN-0034) — trichotomy, irreflexivity, transitivity, and the mixed ≤-< chaining consequence
**ASN**: S4 (SplitPartition) — *"⟦λ⟧ ∪ ⟦ρ⟧ = {t : s ≤ t < p} ∪ {t : p ≤ t < reach(σ)} = {t : s ≤ t < reach(σ)} = ⟦σ⟧"* (part a); *"⟦λ⟧ ∩ ⟦ρ⟧ = {t : s ≤ t < p ∧ p ≤ t} = ∅, since t < p and t ≥ p cannot both hold"* (part b); S3 (MergeEquivalence) — *"Case 1: t < reach(α). Case 2: t ≥ reach(α)"*; *"reach(β) = start(α) ≤ start(β) < reach(β) — … i.e. reach(β) < reach(β)"*
**Issue**: S4 uses T1's trichotomy directly in part (a) (every t satisfies t < p or t ≥ p, covering [s, reach(σ))) and T1's irreflexivity and transitivity in part (b) (t < p and t ≥ p implies p < p via the ≥ definition and transitivity, contradicting irreflexivity). S3 uses T1's dichotomy in its converse case split and its mixed ≤-< chaining ("reach(β) ≤ start(β) and start(β) < reach(β)" → "reach(β) < reach(β)"), which requires T1's consequence that m ≤ n ∧ n < p → m < p. Neither S3 nor S4 lists T1 in its Depends. Both cite TA-strict or T12, from which T1 is transitively reachable, but the specific ordering properties are used as raw T1 invocations, not filtered through what those citations export.
**What needs resolving**: Add T1 (LexicographicOrder, ASN-0034) to the Depends lists of both S3 and S4.

---

### S3, S4 — dangling reference to undefined S11
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: S4 (SplitPartition) — *"We discharge it as S11 does: σ is well-formed, so …"*; S3 (MergeEquivalence) — *"We discharge it as S11 does: each span σ ∈ {α, β} is well-formed …"*
**Issue**: Both proofs borrow a proof-pattern label "S11" for the TumblerAdd carrier-placement argument (σ well-formed → start(σ), width(σ) satisfy TumblerAdd's preconditions → reach(σ) ∈ T). S11 is not defined anywhere in the shown ASN content and does not appear in either claim's Depends list. The full argument is spelled out inline in each case so no logical gap exists, but the reference is unresolved.

VERDICT: REVISE