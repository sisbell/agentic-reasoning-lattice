## Audit

**S0 (Convexity).** The two non-strict composition steps — `start(σ) ≤ q` from `start(σ) ≤ p ∧ p ≤ q`, and `q < reach(σ)` from `q ≤ r ∧ r < reach(σ)` — are each derived by explicit case analysis on the T1 abbreviation `a ≤ b ≡ a < b ∨ a = b`, reducing every branch to T1(c) or equality substitution. The four-case split for the lower bound and two-case split for the upper bound both close. T1 does not export ≤-transitivity as a named postcondition, and S0 correctly avoids citing it. The precondition `q ∈ T` is required for the bracketing chain to be well-typed and is rightly listed as the consumer's obligation. Depends: T1 only. Sound.

**WF (WellFormedSpanFromEndpoints).** The core work is discharging D1's fifth precondition `divergence(s, r) ≤ #s`. The proof eliminates T1 case (ii) under `#s = #r` by observing that the case bound `k = #s + 1 ≤ #r = #s` unfolds under NAT-order's `≤`-definition into two sub-cases (`#s + 1 < #s` and `#s + 1 = #s`), each reaching `#s < #s` via NAT-addcompat's successor inequality and NAT-order's transitivity or equality substitution respectively, against NAT-order's irreflexivity. T1 case (i) then holds with k ≤ #s, and NAT-order's exactly-one disjointness converts `sₖ < rₖ` to `sₖ ≠ rₖ`, qualifying k for Divergence case (i); Divergence's uniqueness clause identifies k = divergence(s, r), giving `divergence(s, r) = k ≤ #s`. The TumblerSub application at (r, s) is licensed: Divergence symmetry carries the case (i) witness to (r, s), ZPD's Relationship-to-Divergence certifies zpd(r, s) = k defined, TumblerSub's positive-branch postconditions export Pos(r ⊖ s) and actionPoint(r ⊖ s) = k. The bound `k ≤ #s` (from Divergence case (i)) combined with TumblerSub's length postcondition `#(r ⊖ s) = #r = #s` closes actionPoint(r ⊖ s) ≤ #s for T12. D1's five preconditions are all in hand; the round-trip identity gives reach(γ) = r. Level-uniformity holds: `#(r ⊖ s) = #r = #s = #start(γ)`. Sound.

**S6 (LevelConstraint).** Under the well-formed level-uniform span preconditions — which match TumblerAdd's — the result-length identity `#(s ⊕ ℓ) = #ℓ` applies directly. Composing with `#ℓ = #s` closes the chain `#start(σ) = #width(σ) = #reach(σ) = #s`. Depends: TumblerAdd only. Sound.

**S2 (EmptyDistinction).** Directly cites T12's postcondition (b), `s ∈ span(s, ℓ)`, which instantiates to `start ∈ ⟦span⟧`. The non-emptiness inference is a one-step application of this postcondition. Sound.

**S11 (DifferenceBound).** The proof is structurally complex; each sub-argument holds.

*Reach membership:* TumblerAdd's carrier postcondition at (start(σ), width(σ)) places reach(α) ∈ T and reach(β) ∈ T before the containment derivation begins — correctly, since the reach-bound contradiction requires testing reach(α) for membership in ⟦β⟧ = {t ∈ T : …}, which requires t ∈ T.

*Boundary characterization:* `start(β) ∈ ⟦β⟧` follows from T12(b) re-exported by S2; containment then gives `start(β) ∈ ⟦α⟧`, yielding `start(α) ≤ start(β)` and (as a byproduct) `start(β) < reach(α)`. The reach bound uses this byproduct: assuming reach(β) > reach(α) puts reach(α) strictly between start(β) and reach(β), so reach(α) ∈ ⟦β⟧ ⊆ ⟦α⟧, giving reach(α) < reach(α) against T1 irreflexivity. Both bounds are valid.

*Partition:* T1's totality gives a clean binary split at start(β), then at reach(β), covering (L)/(M)/(R) exhaustively and disjointly.

*λ construction:* start(α), start(β) ∈ T directly (span starts); level_compat supplies `#start(α) = #start(β)`; WF closes. ⟦λ⟧ = (L) from reach(λ) = start(β).

*ρ construction:* reach(β), reach(α) ∈ T from TumblerAdd (established at the outset); S6 on each level-uniform span gives `#reach(σ) = #start(σ)`, and level_compat propagates to `#reach(β) = #reach(α)`; WF closes. ⟦ρ⟧ = (R) from reach(ρ) = reach(α).

*Tightness:* In case (c), start(α) ∈ ⟦λ⟧ (since start(α) < start(β) = reach(λ) and start(α) ≤ start(α)) and reach(β) ∈ ⟦ρ⟧ (since reach(β) < reach(α) and reach(β) ≤ reach(β)) — both in ⟦γ⟧. A witness t ∈ ⟦β⟧ (non-empty by S2) satisfies t ≥ start(β) and t < reach(β). The lower bound start(α) ≤ t is derived by case-splitting the abbreviation `start(β) ≤ t ≡ start(β) < t ∨ start(β) = t` and composing with start(α) < start(β) via T1(c) or equality substitution — the same technique S0 uses for its own ≤-chain. With start(α) ≤ t ≤ reach(β) and both brackets in ⟦γ⟧, S0's convexity applied to the well-formed span γ gives t ∈ ⟦γ⟧ = ⟦λ⟧ ∪ ⟦ρ⟧; but t ∉ ⟦λ⟧ (t ≥ start(β) = reach(λ)) and t ∉ ⟦ρ⟧ (t < reach(β) = start(ρ)) — contradiction. Sound.

The Depends lists are complete: S0 uses T1; WF uses T12, D1, T1, Divergence, TumblerSub, ZPD, NAT-addcompat, NAT-order; S6 uses TumblerAdd; S2 uses T12; S11 uses T1, S0, S2, S6, WF, TumblerAdd. T12 is consumed by S2 which re-exports its start-in-span postcondition for S11's use; no transitive gap.

VERDICT: CONVERGED