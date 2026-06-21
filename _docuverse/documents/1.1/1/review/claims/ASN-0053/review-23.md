I read the foundation set and then the ASN as a system, tracing the precondition chains from each span-algebra claim back through WF/WR into D1/D2/TA-assoc/TA-LC and the carrier-membership discharges via TumblerAdd. The endpoint-in-T plumbing (the recurring "each σ is well-formed, so reach(σ) = start(σ) ⊕ width(σ) ∈ T via TumblerAdd") is consistent across S1/S3/S4/S8/S11/S11c, and the WF↔D1 and WR↔D2 divergence-type arguments are sound. Two places where the narrative body and the appended formal-contract version of the same claim disagree, and one is an unsound grounding.

### S7 body grounds span-infinitude in T0(b), which does not supply it
**Class**: REVISE
**Foundation**: T0(b) (UnboundedLength) — postcondition is purely existential: "for every n ≥ 1 there exists t ∈ T with #t ≥ n." T0 (CarrierSetDefinition) comprehension is what populates T with each specific extension.
**ASN**: S7 body proof: "Thus every extension lies in [s, reach(s, ℓ)) = ⟦(s, ℓ)⟧, and by T0(b) there are infinitely many of them. Hence ⟦σ⟧ is infinite for every span σ."
**Issue**: T0(b) asserts only that *some* tumbler of each length exists; it says nothing about the family s.0ⁿ — neither that those particular extensions inhabit T, nor that they are pairwise distinct, nor that they are infinitely many. The infinitude actually rests on T0's comprehension axiom (placing each s.0ⁿ ∈ T) together with the injectivity n ↦ s.0ⁿ (distinct lengths #s + n). The appended formal-contract version of S7 states this correction explicitly and even disavows T0(b): "The separate UnboundedLength claim T0(b)... is not what we invoke." The body was not updated to match, so it carries an incorrect citation as a load-bearing proof step in the "why exact representation fails" argument — classic reviser drift where the contract was corrected but the narrative left stale.
**What needs resolving**: The body proof of S7 must ground the infinitude of ⟦σ⟧ in T0's comprehension (each s.0ⁿ ∈ T) plus the distinct-length injectivity argument, matching the appended version, rather than citing T0(b).

### S11c body Case 2 drops the lower guard `start(α) ≤ t` without invoking the Case 2 hypothesis
**Class**: OBSERVE
**Foundation**: T1 (LexicographicOrder) — transitivity.
**ASN**: S11c body, Case 2: "if t ≥ reach(β), then t ∉ ⟦β⟧... Therefore ⟦α⟧ \ ⟦β⟧ = {t : reach(β) ≤ t < reach(α)}."
**Issue**: The difference set is {t : start(α) ≤ t < reach(α) ∧ reach(β) ≤ t}; rewriting it as {t : reach(β) ≤ t < reach(α)} silently discards the `start(α) ≤ t` conjunct. That rewrite is sound only because Case 2's hypothesis start(α) < reach(β) forces t ≥ reach(β) ⟹ t > start(α); the body does not state this reliance. The appended version makes the ⊆/⊇ inclusions and the recovered guard explicit. Conclusion is correct; the body narrative is less rigorous than its own formal contract.
**What needs resolving**: None required for soundness; the body could note that start(α) < reach(β) (Case 2) licenses dropping the lower guard.

The remaining claims — WF, WR, S0–S6, S8 (loop invariant J, N1/N2 derivation, termination), S9 (all six cases including the empty-start-empty-reach exclusion via TA-LC), S10, S11/S11a/S11b/S11d, and the split/merge inverses S3b/S4a — discharge their cross-claim preconditions correctly, and the "level-uniform span ⟹ well-formed" convention introduced by the opening ("by TA-strict every span is non-empty") is applied consistently where the proofs assert well-formedness.

VERDICT: REVISE