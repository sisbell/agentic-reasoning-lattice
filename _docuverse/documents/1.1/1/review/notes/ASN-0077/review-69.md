# Review of ASN-0077

This note is mathematically thorough — the pointwise/lift structure is sound, the singleton-I-span analysis is genuinely rigorous, and the worked example correctly witnesses O13 and O14. My findings are confined to the anti-bloat patterns the note's classifier flags, plus one unused-machinery question.

## REVISE

### Issue 1: Use-site specialization prose in O11★★
**ASN-0077, O11★★ derivation (closing sentence)**: "The pure-K.μ⁺ and pure-K.μ⁺_L chains are the obvious specializations of O11★★ (sub-case (ii), respectively sub-case (i), never fires)."
**Problem**: This sentence advances no reasoning. The claim already covers mixed chains; that pure chains are instances is self-evident and the parenthetical "never fires" bookkeeping is the kind of exhaustiveness annotation the precise reader must skip. It reads as residue from a prior cycle that proved the pure cases separately.
**Required**: Delete the sentence. If the pure-chain corollaries are needed by a consumer, state that consumer; otherwise drop.

### Issue 2: Method-justification meta-prose in O5★
**ASN-0077, O5★ derivation**: "We do not re-run the per-step induction: ASN-0098 already abstracts it."
**Problem**: This is prose about *why this proof method was chosen* rather than the proof itself. The Closure schema (★) is then invoked directly two sentences later, which is all that is needed. The lead-in is noise.
**Required**: Remove the justification sentence; open the derivation with the four-clause conjunction and the schema application.

### Issue 3: Block-collapsed form (F3) and the (F1)≡(F3) equivalence chain are not load-bearing
**ASN-0077, "Lifting origin to a V-span"**: introduces (F3) `= { origin(aⱼ) : 1 ≤ j ≤ k }` and proves the full equivalence chain (F1)⊆(F3), (F3)⊆(F1).
**Problem**: No downstream claim's proof consults (F3) — O6, O7, O8, O11, O11′, O11★★, O12, and both wp derivations all route through (F1). The only downstream mention is a parenthetical in the SHOWORIGIN_V postcondition ("equal to (F3) by the equivalence chain derived above"), and the worked example's block narration uses O2 directly, not (F3). The equivalence chain therefore appears to be machinery with no consumer beyond decoration.
**Required**: Either cite a proof that genuinely depends on the block-collapsed reading, or remove (F3) and its equivalence chain. O2 (Block uniformity) can stand alone as the bridge to ASN-0058's block algebra for the worked example without (F3).

## OUT_OF_SCOPE

### Topic 1: Unified content+link I-span origin operation
**Why out of scope**: The first open question (a unified operation reporting both content and link origins over an I-stream range) is genuinely new territory — a different operation with its own guarantees — not a defect in the current I-span lift, whose content-only behavior is correctly settled in the cross-subspace edge case.

### Topic 2: Historical containment via Σ.R
**Why out of scope**: The note correctly distinguishes current-arrangement origin from historical containment and defers the latter to a separate operation. The coupling invariants between the two belong in that future ASN.

VERDICT: REVISE
