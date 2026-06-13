# Review of ASN-0122

I checked the derivations against the foundations and reran the worked example end to end — the mathematics is sound. corr as the kernel of `res` intersected with the operand rectangle is the right object; X1/X2 establish the address basis with the coincidence-exclusion construction correctly validated against ValidComposite★ and S4; X4c's interval-clipping argument (monotonicity via TS4/TS5, convexity via T12(c), interval ∩ interval) is correct; X11's unique succ-chain partition and lexicographic order are correct; X-T's injectivity discharge in X7(iii) (id on L, σ on R via D-BJ, non-collision via D-DP(a)) is exactly the obligation that case carries and it is met. The worked example's counts (3 relation elements, fan-out on `(d₂,[1,1])`, γ₁/γ₂, the swap's tie-break, the window clip, the six-element self-comparison, the `{b}` detector) are all forced by the definitions and check out.

The note carries the `review-mode.anti-bloat` classifier, and the findings below are forward-reference accretion, not correctness. They are mild but verifiable and compound if left.

## REVISE

### Issue 1: X9's conclusion is announced twice before it is proved

**ASN-0122, Definition (Spec-set and region)** closing sentence: "What this content-subspace restriction *costs* in correspondence information is the subject of X9 (below), and the answer there is: nothing."

**ASN-0122, "Which Positions May Participate"** opening: "We restricted regions to the content subspace. We must say exactly what the restriction discards — and the answer will be: no sharing."

**Problem**: The region definition gives away X9's result ("nothing"), and the X9 section then re-announces the same result ("no sharing") before delivering it in the proof and restating it a third time in the body ("lossless for this operation"). A reader who reached the X9 section already knows the answer from the region-definition spoiler, so the section opening is a duplicate announcement in different words. The surrounding region-definition prose also leans defensive ("This confinement is *unconditional* — it rests on the clip alone, never on a property of the operand spans"; "operand hygiene, not the guarantee").

**Required**: Drop the region-definition spoiler clause; a bare pointer ("confined to content instances — X9 shows this discards no correspondence") suffices, letting X9 carry the single announcement. Keep the `σ = ([1,5], [3])` example — it is load-bearing (it is what justifies "content-confined regions" in X4c and the precondition framing) and is a concrete example, not meta-prose. Trim the "unconditional confinement" framing to the one fact the proofs actually use: the `∩ V_{s_C}` clip confines every region to content instances regardless of operand spans.

### Issue 2: X9 forecasts an implementation deficiency from inside the theorem

**ASN-0122, "Which Positions May Participate"** (closing paragraph after X9): "We will see in the implementation observations what happens when the precondition is violated rather than enforced — not extra answers but undefined behavior, exactly as one expects of a violated precondition."

**Problem**: This is a forward pointer from a subspace-vacuity theorem to a downstream implementation section, and it previews that section's conclusion. Deficiency 2 then makes the identical point with a back-reference ("X9 says the excluded territory could never have contributed a pair, so the crash is a violated precondition, not a missing feature"). The point belongs at the implementation observation, where the evidence lives; stating it inside X9 is prose the precise reader skips past to follow the vacuity argument.

**Required**: Delete the forecasting sentence from the X9 section. Deficiency 2 already states it where it is grounded.

## OUT_OF_SCOPE

The Open Questions (n-way alignment, derived-index consistency contracts, content referenced but arranged nowhere, future subspace vocabulary) are correctly deferred; they raise new territory rather than gaps in this note. No action.

VERDICT: REVISE
