Reading the ASN against the foundation, the span algebra is mostly carefully constructed — the WF/WR/D1/D2 chain is correctly threaded, the TumblerAdd carrier-membership discharge is consistently applied, and the SC case split is genuinely exhaustive. A few cross-claim issues remain.

### S9 invokes TA-LC without a precondition that supplies its action-point bounds
**Class**: REVISE
**Foundation**: TA-LC (LeftCancellation) — preconditions `Pos(x)`, `Pos(y)`, `actionPoint(x) ≤ #a`, `actionPoint(y) ≤ #a`.
**ASN**: S9 (NormalizationUniqueness). Stated preconditions: "Σ̂₁ … and Σ̂₂ … are both normalized span sequences … each span is non-empty (start(γₖ) < reach(γₖ))." Proof step: "two spans sharing start and reach share width, since start ⊕ w₁ = reach = start ⊕ w₂ forces w₁ = w₂ by left cancellation (TA-LC, ASN-0034)."
**Issue**: TA-LC's preconditions are `Pos(width)` and `actionPoint(width) ≤ #start` for both operands. S9's stated preconditions give only "normalized" and "non-empty" (`start < reach`). Non-emptiness is strictly weaker than well-formedness — the document itself distinguishes "well-formed span" (S2) from an arbitrary `(s, ℓ)` pair. As written, the precondition chain into TA-LC is not discharged from S9's hypotheses, so the equal-start-equal-reach case is not actually ruled out from the stated assumptions. (In intended usage the spans come from S8, which emits well-formed level-uniform spans, so the gap is in the standalone contract, not the S10 call site.)
**What needs resolving**: S9 must carry well-formedness of the component spans (`Pos(width)`, `actionPoint(width) ≤ #start`) as a precondition, so that TA-LC applies — or otherwise establish `w₁ = w₂` from start/reach equality without TA-LC.

### WR lists derived facts in its precondition slot
**Class**: OBSERVE
**Foundation**: —
**ASN**: WR (WidthRecovery) formal contract. Preconditions listed: "ℓ > 0 with action point k ≤ #s (T12); s < reach(σ) (TA-strict on T12); s ⊕ ℓ = reach(σ) satisfies TA0's preconditions; divergence(s, reach(σ)) = k ≤ #s of type (i) (T1, Divergence)."
**Issue**: Every one of these is a consequence of "σ is a well-formed level-uniform span" — and indeed the proof body derives them all (the divergence-type-(i) fact in particular is derived in the second proof paragraph, not assumed). Listing derived results as preconditions, each annotated with the claim that proves it, inflates the caller's apparent obligation; a consumer reading the contract would believe it must establish `divergence(s, reach(σ)) = k ≤ #s` before calling, when the genuine input is just level-uniformity.
**What needs resolving**: n/a (OBSERVE) — the genuine precondition is "σ is a well-formed level-uniform span"; the rest belong in the proof, not the precondition slot.

### Body proofs of S1/S3/S4 cite the later sibling S11 for a proof technique
**Class**: OBSERVE
**Foundation**: TumblerAdd (carrier postcondition `a ⊕ w ∈ T`).
**ASN**: S1, S3, S4 narrative bodies: "We discharge it as S11 does: each span σ ∈ {α, β} is well-formed, so … TumblerAdd's carrier postcondition a ⊕ w ∈ T gives reach(σ) ∈ T."
**Issue**: S1, S3, S4 precede S11 in the document, yet their prose routes the reach-in-T discharge "as S11 does." The actual logical content is the direct TumblerAdd citation, which the formal contracts of S1/S3/S4 already record correctly. The "as S11 does" pointer is a navigation reference to a downstream sibling for a technique, not a dependency — a presentation wart that reads as if S11 were upstream.
**What needs resolving**: n/a (OBSERVE) — the technique is self-contained from TumblerAdd; the sibling cross-reference can be dropped without changing the argument.

### S4 precondition slot carries an essay on which operand's `p ∈ T` is whose obligation
**Class**: OBSERVE
**Foundation**: —
**ASN**: S4 (SplitPartition) formal contract preconditions: "p ∈ T — the interiority constraint below asserts s < p < reach(σ), and < compares only members of the carrier T, so p must lie in T for that assertion to be well-defined; this membership is the consumer's to supply, p being given rather than constructed, whereas the companion operands are placed within the contract — s ∈ T is subsumed by σ's well-formedness and reach(σ) ∈ T by TumblerAdd's carrier postcondition; …"
**Issue**: This is defensive justification prose occupying a precondition slot — it argues why `p ∈ T` is a legitimate precondition rather than simply stating it. The structural content reduces to "p ∈ T; p interior to σ; level_compat(s, p)."
**What needs resolving**: n/a (OBSERVE).

VERDICT: REVISE