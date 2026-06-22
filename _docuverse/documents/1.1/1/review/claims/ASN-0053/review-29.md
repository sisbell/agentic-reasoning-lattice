The foundation statements — TumblerAdd, T1, T12, TumblerSub, D1, and Divergence — are all in scope. I read each ASN claim against them in turn.

**S0 (Convexity).** The one-line proof is sound. Both transitivity steps (≤ followed by ≤, then ≤ followed by <) unfold directly from T1's strict transitivity and the definition of ≤ as `< ∨ =`. T1 is the only dependency needed, and it is cited.

**S6 (LevelConstraint).** TumblerAdd's result-length postcondition `#(a ⊕ w) = #w`, instantiated at `(s, ℓ)` under the stated preconditions, gives `#reach(σ) = #ℓ = #s`. The dependency chain is complete and TumblerAdd is the sole citation needed.

**S2 (EmptyDistinction).** Follows immediately from T12's postcondition (b), `s ∈ span(s, ℓ)`, under the same preconditions T12 assumes. T12 is cited; no other foundation is required.

**S11 (DifferenceBound).** The proof is structurally sound. Reach membership (`reach(α), reach(β) ∈ T`) is placed via TumblerAdd at the outset, before either is tested for span membership — the ordering matters and the proof gets it right. The containment boundary derivation (start(α) ≤ start(β) and reach(β) ≤ reach(α)) is correctly element-chased using S2 for start(β) ∈ ⟦β⟧ and T1 irreflexivity for the reach contradiction. The (L)/(M)/(R) partition is exhaustive and pairwise disjoint by T1's totality. WF's preconditions are fully discharged for both λ (start tumblers are in T directly; level_compat supplies #start(α) = #start(β)) and ρ (reaches are in T from TumblerAdd; S6 propagates level-uniformity to give #reach(β) = #reach(α)). The tightness argument is valid: S2 supplies a witness t ∈ ⟦β⟧, S0 convexity forces t ∈ ⟦γ⟧, and the interval structure gives t ∉ ⟦λ⟧ ∪ ⟦ρ⟧. All cited dependencies — T1, S2, WF, S6, TumblerAdd, S0 — are actually used.

**WF (WellFormedSpanFromEndpoints).** Two gaps, both in the proof of WF itself.

---

### WF: NAT-addcompat and NAT-order absent from Depends for T1-case-elimination arithmetic

**Class**: REVISE
**Foundation**: NAT-addcompat (NatAdditionOrderAndSuccessor), NAT-order (NatStrictTotalOrder)
**ASN**: WF (WellFormedSpanFromEndpoints) — proof body and Depends section
**Issue**: The proof performs two arithmetic steps whose grounding is absent from WF's Depends.

(a) Eliminating T1 case (ii): "it would force #s + 1 ≤ #s, impossible since #s < #s + 1." The strict successor inequality `n < n + 1` is NAT-addcompat's postcondition. Closing the contradiction — `#s < #s + 1 ≤ #s ⟹ #s < #s` — requires NAT-order's transitivity and irreflexivity of `<` on ℕ. D1's Depends lists both for this identical step ("strict successor inequality #a < #a + 1 used in … T1 case (ii) elimination").

(b) Converting the T1 case-(i) witness: "sₖ < rₖ, whence sₖ ≠ rₖ." This uses NAT-order's disjointness-of-`<`-and-`=` clause `¬(sₖ < rₖ ∧ sₖ = rₖ)`. D1's Depends lists NAT-order for the identical step ("exactly-one trichotomy's disjointness clause … converts T1 case (i)'s aⱼ < bⱼ into aⱼ ≠ bⱼ").

WF's Depends lists T1, Divergence, D1, TumblerSub, and T12. Neither NAT-addcompat nor NAT-order appears. Neither can be drawn transitively through any listed dependency: T1's exported postconditions are tumbler order properties only; D1 exports only the round-trip identity `a ⊕ (b ⊖ a) = b`.

**What needs resolving**: NAT-addcompat and NAT-order must be added to WF's Depends, with per-step citations identifying the strict-successor contradiction and the `<`-to-`≠` conversion.

---

### WF: Pos(r ⊖ s) derived via ungrounded ZPD padding conversion; TumblerSub exports Pos directly

**Class**: REVISE
**Foundation**: TumblerSub (TumblerSub), ZPD
**ASN**: WF (WellFormedSpanFromEndpoints) — Pos derivation
**Issue**: The proof writes: "(r ⊖ s)ⱼ = rⱼ − sⱼ — TumblerSub's padded projections coincide with the native components since #r = #s leaves no padding zone — is strictly positive by TumblerSub's divergence-point inequality rⱼ > sⱼ, so Pos(r ⊖ s) holds."

TumblerSub's exported divergence-point postcondition is "â_{zpd} > ŵ_{zpd}" on ZPD's *padded* projections, not "rⱼ > sⱼ" in native components. The conversion relies on ZPD's padded-projection equality clause (âᵢ = aᵢ for 1 ≤ i ≤ #a), which states that padded equals native inside the operand's native domain. That clause belongs to ZPD, which does not appear in WF's Depends and is not re-exported by TumblerSub.

The component detour is also unnecessary: TumblerSub directly exports Pos(a ⊖ w) as a postcondition when zpd(a, w) is defined. WF already cites TumblerSub. Since s ≠ r (from s < r via T1's trichotomy disjointness) and #r = #s rule out Divergence case (ii) — the same case-elimination already done for the divergence-bound step — Divergence case (i) applies and zpd(r, s) is defined, so TumblerSub's Pos postcondition applies directly.

**What needs resolving**: Either add ZPD to WF's Depends and ground the padded-to-native conversion explicitly, or drop the component argument and cite TumblerSub's Pos postcondition directly (noting that zpd(r, s) is defined by the Divergence case-(i) witness already established in the proof).

---

VERDICT: REVISE