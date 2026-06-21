## Audit

**WF** is the load-bearing construction that S11, S11c, and S11a all import for their explicit span witnesses. Both of WF's postconditions — the reach identity and level-uniformity — rest on proof steps that go beyond WF's stated *Depends* (T12 and D1 alone). The dependency gap propagates upstream into S11 and S11c via their right-difference span constructions.

**SC** and **S0** are correctly stated; their proofs walk all cases and the WLOG reduction in SC is mechanically sound. **S11b**, **S11a**, and **S11d**'s reverse-containment sub-case are each clean one-step arguments. **S2**'s derivation is sound given the cited claims.

**S11**'s tightness argument is correct: the three steps (start(α) ∈ ⟦λ⟧, reach(β) ∈ ⟦ρ⟧, S0 convexity forcing t ∈ ⟦γ⟧, then t excluded from both components) close without gaps.

The cross-claim issue that no per-claim checker can fully surface: WF's broken *Depends* means the same level-length derivation is silently ungrounded in every caller that constructs a right-difference span via WF.

---

### WF — D1's precondition `divergence(s, r) ≤ #s` is unverified
**Class**: REVISE
**Foundation**: D1 (DisplacementRoundTrip) — explicit preconditions `a ∈ T, b ∈ T, a < b, divergence(a,b) ≤ #a, #a ≤ #b`
**ASN**: WF *proof* — "Since s < r and #s = #r, the divergence k is of type (i) with k ≤ #s — equal length excludes the prefix case."
**Issue**: WF applies D1 with a = s, b = r. Four of D1's five preconditions are discharged by WF's preconditions (s ∈ T, r ∈ T, s < r, #s ≤ #r from #s = #r). The fifth, `divergence(s, r) ≤ #s`, is discharged by the argument that T1's case (ii) is excluded when #s = #r, leaving case (i) with witness k ≤ #s, which the Divergence claim then identifies with divergence(s, r). Neither T1 nor Divergence appears in WF's *Depends*. Without them, the argument that divergence(s, r) = k ≤ #s is ungrounded, D1's precondition is unverified, and the step `reach(γ) = s ⊕ (r ⊖ s) = r` has no licensed foundation.
**What needs resolving**: WF must add T1 and Divergence to its *Depends* and formally discharge D1's precondition `divergence(s, r) ≤ #s` from them.

---

### WF — Level-uniformity postcondition `#width(γ) = #start(γ)` ungrounded
**Class**: REVISE
**Foundation**: D1 (DisplacementRoundTrip) — postcondition is `a ⊕ (b ⊖ a) = b` only; TumblerSub's length-pair dispatch is used inside D1's proof but is not re-exported.
**ASN**: WF *proof* — "#width(γ) = #(r ⊖ s) = max(#r, #s) = #s = #start(γ)"
**Issue**: Step 2 of this chain, `#(r ⊖ s) = max(#r, #s)`, is TumblerSub's output-length formula. TumblerSub is not in WF's *Depends*. D1's sole exported postcondition is `a ⊕ (b ⊖ a) = b`; it does not re-export TumblerSub's length formula. An alternative derivation exists — D1 gives `s ⊕ (r ⊖ s) = r`, and TumblerAdd's result-length identity `#(a ⊕ w) = #w` then gives `#(r ⊖ s) = #r = #s` — but TumblerAdd is also absent from WF's *Depends*. Without either cited claim, the level-uniformity postcondition `#width(γ) = #start(γ)` is not derivable from WF's stated dependencies and is ungrounded.
**What needs resolving**: WF must add TumblerSub or TumblerAdd to its *Depends* and cite the appropriate length property to ground the step `#(r ⊖ s) = #s`.

---

### S11 and S11c — WF precondition `#reach(β) = #reach(α)` for the right-difference span is ungrounded
**Class**: REVISE
**Foundation**: WF (WellFormedSpanFromEndpoints) — preconditions `s < r` and `#s = #r`; D1 / TumblerAdd — result-length identity `#(a ⊕ w) = #w` (not in S11's or S11c's *Depends*)
**ASN**: S11 *proof* — "Since reach(β) < reach(α) and #reach(β) = #reach(α) (level-uniformity and level-compatibility ensure all boundary tumblers share the same length), WF gives a well-formed level-uniform span with reach(ρ) = reach(α)." S11c Case 2 *proof* — "We establish #reach(β) = #reach(α): level-uniformity of α gives #reach(α) = #start(α), level-uniformity of β gives #reach(β) = #start(β), and level_compat(start(α), start(β)) gives #start(α) = #start(β)."
**Issue**: The construction of the right-difference span ρ (in S11) or γ' (in S11c Case 2) invokes WF with s = reach(β) and r = reach(α), which requires WF's precondition `#reach(β) = #reach(α)`. The proof derives this from level-uniformity via the chain: (a) `#reach(σ) = #(start(σ) ⊕ width(σ)) = #width(σ)` [by TumblerAdd's result-length identity], and (b) `#width(σ) = #start(σ)` [level-uniformity as defined in WF's postcondition], giving `#reach(σ) = #start(σ)`. Step (a) requires TumblerAdd, which is in neither S11's *Depends* (T1, S2, WF, S0) nor S11c's *Depends* (SC, WF). The parenthetical "(level-uniformity and level-compatibility ensure...)" is an informal claim, not a grounded proof step. If "level-uniform" is formally defined elsewhere to include `#reach = #start` as an axiom, that definition must be cited; if not, TumblerAdd is missing. Either way, the step is currently ungrounded in the stated *Depends*.
**What needs resolving**: S11 and S11c must either (a) cite TumblerAdd and derive `#reach = #start` from level-uniformity via TumblerAdd's result-length identity, or (b) cite the formal definition of "level-uniform" if that definition axiomatically includes `#reach = #start`. The informal parenthetical is not sufficient.

---

VERDICT: REVISE