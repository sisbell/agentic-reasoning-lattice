# Review of ASN-0053

The mathematics here is sound. I checked every proof — WR, WF, S0–S11d, the SC exhaustiveness split, the S8 loop invariant, and the S9 six-case uniqueness argument — and each discharges its foundation preconditions correctly, covers its boundary cases, and supplies a concrete worked instance. Foundation citations (D0/D1/D2, TA-LC, TA-assoc, T12) are used legitimately, and no non-foundation ASN is referenced. The findings below are confined to the `review-mode.anti-bloat` mandate: prose that restates rather than advances.

## REVISE

### Issue 1: Redundant summary paragraph after the WR proof
**ASN-0053, "The reach function" (immediately after WR's ∎)**: "The width is recoverable from the endpoints. Conversely, start(σ) ⊕ width(σ) = reach(σ) by definition. So start ⊕ width determines reach (by definition of ⊕), and start and reach determine width (by D2, via reach ⊖ start)."
**Problem**: All three sentences restate facts already on the page. "start and reach determine width (by D2, via reach ⊖ start)" is WR verbatim — the property just proved one line above. "start ⊕ width determines reach by definition" merely re-cites the definition of `reach`. The reader must skip past this to reach the next claim; it advances no reasoning.
**Required**: Delete the paragraph. WR's statement and the reach definition already carry this content.

### Issue 2: Foundation lemma restated in a forward-reference preamble before S5
**ASN-0053, just before S5**: "The composition property below depends on left cancellation of TumblerAdd: if a ⊕ x = a ⊕ y with both sides well-defined, then x = y (TA-LC, ASN-0034)."
**Problem**: This restates TA-LC's full statement in prose ahead of its use, and S5's own proof then re-cites and re-discharges TA-LC ("We discharge TA-LC's preconditions… with a := s…"). The preamble is a forward pointer that duplicates a foundation lemma the proof will state anyway — exactly the forward-reference accretion the anti-bloat classifier targets.
**Required**: Remove the sentence. S5 invokes and discharges TA-LC at the point of use, which is sufficient.

## OUT_OF_SCOPE

None to add — the author's own Open Questions already park span-set difference bounds, cross-level intersection, allocation-stability of normalized forms, and width-by-representation vs. width-by-denotation as future work, which is the correct disposition.

VERDICT: REVISE
