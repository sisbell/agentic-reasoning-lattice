# Review of ASN-0086

I checked the R0–R7a lemmas, the three operations, the wp analysis, and the worked sketch. The mathematical content is sound: R0a's cross-home zero-counting argument and same-home chain argument are both complete; R0a-Cor2's depth-2 derivation (zero-position stability via TA5(c)/TA5-SigValid + (UL)) is rigorous; R7a's K.σ/K.λ replay correctly handles the multi-fresh-home case (verified against the length-4 worked example); the wp cases give honest necessity arguments per conjunct; the worked sketch's tumbler arithmetic checks out (`a₁=1.0.1.0.1.0.2.1`, `b₁=inc(a₁,0)=...2.2`, coverage half-open interval matches PrefixSpanCoverage). I found no correctness or missing-case defects.

The findings below are anti-bloat / accretion items, which this note's `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: R0a-Cor2's "tightens L1b" consequence is stated four times
**ASN-0086, R0a-Cor2**: The statement's trailing parenthetical reads "This narrows L1b's substrate-level admission `#E ≥ 2` (ASN-0043) to the tighter `#E = 2` strictly." The sentence immediately following the proof restates it: "R0a-Cor2 tightens L1b's substrate admission `#E ≥ 2` to `#E = 2` — establishing depth-2 strictly as a structural consequence of the K.λ contract..." The same consequence then recurs in the Properties Introduced table ("tightens L1b's `#E ≥ 2` admission to depth-2 strictly") and again in Open Question 7.

**Problem**: The parenthetical and the post-proof sentence are the same claim in different words, bracketing one proof — exactly the "two paragraphs say the same thing" pattern. The post-proof restatement adds nothing the parenthetical and the proof's final line did not already establish.

**Required**: State the L1b-tightening consequence once (the statement parenthetical is the natural site), delete the post-proof restatement, and let the table entry be the index pointer. Open Question 7 may keep a single reference.

### Issue 2: "Scope." sub-paragraph under the Unit-depth retraction discipline explains enforcement-locus, not the definition
**ASN-0086, Definition — Unit-depth retraction discipline, "*Scope.*"**: "K.λ binds every emission *address* to the sibling-frontier chain but does not constrain the *shape* of a link's endsets, so the substrate does not enforce unit-depth retraction ...; a layer that adopts the discipline must do so by definitional commitment of its retraction operation."

**Problem**: This is a labeled "Scope." sub-paragraph whose function is to explain *why the discipline is a layer commitment rather than substrate-enforced* — the note's own forward-reference-accretion criteria flag "sub-paragraphs labeled 'Scope' ... that explain why rather than what." The substantive content (enforcement lives at the layer, exercised by wp Case 2 regime (ii)) is already carried where it is load-bearing: the "Definition — relational layer" paragraph ("by definitional commitment ... rather than as a separately-tracked caller obligation") and wp Case 2's regime (ii)/(iii) split.

**Required**: Fold the one load-bearing fact (substrate constrains address, not endset shape) into the discipline definition's main sentence and remove the standalone "Scope." label, or delete it as redundant with the relational-layer commitment paragraph.

## OUT_OF_SCOPE

### Topic 1: Cross-layer invariants between `L_K` and arrangements `Σ.M`
The note's first open question (predicate visibility against `Σ.M`) is genuinely new territory — under M2 arrangements are empty, so this cannot be addressed here. Correctly deferred.

### Topic 2: Higher-arity typed relations and concurrent type-address allocation
Open questions on `L_K^{(n)}` projections and colliding dynamic type addresses across layers are future-ASN scope, not defects in this standard-triple development.

VERDICT: REVISE
