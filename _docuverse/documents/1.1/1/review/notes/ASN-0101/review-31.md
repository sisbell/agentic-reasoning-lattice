# Review of ASN-0101

I read the full specification, checked each of D0–D11's proofs, traced the worked examples (content depth-3, link depth-2, cross-document), and walked the boundary-case enumeration. The operation spec, the gap-closure argument (D1), the five preservation claims (D2–D6), the well-formedness discharge (D8), and the wp calculations (D11) are carefully done and the examples verify against the postconditions. One genuine gap remains.

## REVISE

### Issue 1: LP-family extension catalogue overstates its scope — LP16–LP21 are omitted, including the Resurrection lemma the ASN's own prose invokes

**ASN-0101, D10 (LP-family extension under DELETE)**: "The combined effect: ASN-0098's projection apparatus carries to the DEL-extended vocabulary intact, with D9 and D11 closing the only two extension points... LP-Comp's case-analysis remains exhaustive over the extended vocabulary once the present cataloguing is taken as the DEL row."

**Problem**: The catalogue explicitly covers "LP2 through LP14" (matching ASN-0098's LP-Comp note), but ASN-0098's projection apparatus also includes LP16 (TransclusionDiscoverability), LP17 (GhostProjection), LP18 (Resurrection), LP19/LP19a (TightEndsetBoundaryExclusion / TightFreshness), LP20 (RangeConfinement), and LP21 (RepresentationInvariance). None of these is addressed. The closing claim that the apparatus "carries intact" with "only two extension points" is therefore an overclaim against the demonstrated scope.

This is not a cosmetic omission. The ASN's own "Link discoverability" section asserts:

> "The orphan condition is reversible: a subsequent operation that adds a V-position in `d` mapping to an I-address in the link's coverage restores discoverability."

That sentence is exactly LP18 (Resurrection) instantiated with DEL as the *orphaning* step — yet it is stated with no derivation and no citation (standard #6: a derived guarantee stated without derivation is a REVISE item). LP18 is a multi-step lemma over `Σ →* Σ'`; admitting DEL into the vocabulary means LP18 must be confirmed to hold when DEL is the transition that produced the orphan. The dispatch is available (Store Monotonicity★ holds under DEL because `dom(C') = dom(C)` and `dom(L') = dom(L)` by D2/D3 — neither store shrinks; LP3★ extends via D3), but it is not stated.

**Required**: Either (a) add LP16–LP21 to the extension catalogue with their per-lemma dispatch — most are state-relative (LP16, LP17, LP20, LP21, like LP12) and apply directly to the post-state, while LP18, LP19, LP19a carry through the prefix via the already-established Store Monotonicity★ / LP3★ mechanisms — or (b) narrow the closing claim to the LP-Comp (LP2–LP14) portion and state separately why LP16–LP21 need no DEL-specific extension. In either case, cite LP18 at the orphan-reversibility prose so the resurrection claim is grounded rather than asserted.

## OUT_OF_SCOPE

### Topic 1: DEL-then-INSERT exact recovery
The fourth Open Question (whether DELETE followed by insertion at the same V-position recovers the pre-DELETE arrangement) is correctly deferred — INSERT mechanics are out of scope, and the question is properly logged rather than answered here.

VERDICT: REVISE
