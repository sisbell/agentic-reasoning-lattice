# Review of ASN-0058

## REVISE

### Issue 1: Unused "span algebra applies" applicability claim in the ContentReference definition
**ASN-0058, Definition (ContentReference)**: "The level-uniformity requirement ensures reach(σ) has depth m (S6, ASN-0053), so the position range is well-bounded and the span algebra (S1–S11, ASN-0053) applies."
**Problem**: The clause "the span algebra (S1–S11, ASN-0053) applies" is a forward inventory of machinery that is never invoked. The content-reference and resolution sections use the span *denotation* (σ.denotation, S6 for depth), T5, T1, T3, TumblerAdd, and M11/M12 — none of the span-algebra results S1–S11 (intersection, merge, split, difference, normalization) appear in any subsequent derivation. The reader must check whether S1–S11 are load-bearing and finds they are not. This is the use-site-inventory pattern the anti-bloat classifier targets: an applicability assertion that does not advance the definition's meaning.
**Required**: Drop "and the span algebra (S1–S11, ASN-0053) applies." Keeping the S6 citation (which establishes `#reach(σ) = m`, genuinely used) suffices.

### Issue 2: Redundant notational reading-note for D(Σ)
**ASN-0058, Resolution preamble (Content References intro)**: "As with the abbreviation `M(d)` for `M(Σ, d)`, we write `D` for `D(Σ)` when the ambient state is clear from context; downstream usage `d_s ∈ D` should be read as `d_s ∈ D(Σ)` against the same Σ that underlies `M(d_s)`."
**Problem**: The first clause ("we write `D` for `D(Σ)` when the ambient state is clear") already establishes the abbreviation. The trailing clause re-explains how to read later use sites of the same abbreviation — meta-prose about reading downstream usage rather than content that advances the definition. It restates the abbreviation it just introduced.
**Required**: Keep "we write `D` for `D(Σ)` when the ambient state is clear from context." Delete the "downstream usage `d_s ∈ D` should be read as …" continuation.

## OUT_OF_SCOPE

None. The Open Questions (I-space discontinuity structure, lattice of decompositions, block-count bounds, depth relationships, multi-source reordering) are correctly deferred and do not intrude on the present claims.

VERDICT: REVISE
