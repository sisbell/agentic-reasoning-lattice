# Channel Assignment — ASN-0094 review-67

**Date:** 2026-05-24 12:50

## Issue 1: ASN length impacts reviewability and specification clarity
Reason: This is an editorial pruning task — identifying repetitive disclaimers, duplicated cross-references, and excessive worked examples. The substantive content is already present in the document; no design intent or implementation evidence is needed to decide what to cut.

## Issue 2: Counterfactual worked example for LinkAddressNotPrefixOfEmit Case II.B
Reason: This is a presentation issue about whether a counterfactual example clarifies or confuses the proof. The mathematical content (the lemma and its proof) is sound; only the example's framing needs revision. Derivable from the ASN's own content.

## Issue 3: Sh5(b) status downgraded to "documentation aspiration"
Reason: Sh5 is the framework's own META commitment about how it constructs its template catalog — neither a design intent question (Nelson didn't specify catalog construction discipline) nor an implementation question (udanax-green has no template catalog). The framework must decide its own enforcement level.

## Issue 4: Audit-slice multiplicity loss as a "deliberate commitment" is a semantic shift from ASN-0086
Reason: The choice of `idem = ⊤` vs `idem = ⊥` for R hinges on whether Nelson's design intended duplicate retractions to merge (set semantics) or accumulate as audit events (multiset semantics), and on what udanax-green actually does at the substrate level.
Nelson question: Did the Xanadu design intend duplicate retractions of the same target to produce one logical retraction (set semantics) or accumulate as distinct audit events (multiset semantics)?
Gregory question: When `Nullify` (or its equivalent) is called twice on the same target address in udanax-green, does the implementation produce one retraction record or two distinct records?

## Issue 5: Resolution standalone admissibility verification path depends on aspirational discipline
Reason: The standalone admissibility claim's verification path inherits Sh5(b)'s strength; once Issue 3 settles Sh5(b)'s enforcement level, the wording for "settled" can be adjusted accordingly. Internal — flows from Issue 3.

## Issue 6: Three framework-local Peano-style axioms expand the commitment surface significantly
Reason: This is a specification-structure question about whether ASN-0034 should be modified or whether ASN-0094 should carry the supplements locally. The non-derivability arguments are mathematical; the routing decision is an ASN-discipline question internal to the spec series.

## Issue 7: Sh4 Case A enumeration of transitions has unclear load-bearing status
Reason: This is an editorial clarity issue about whether the transition enumeration is load-bearing for exhaustiveness or merely illustrative. The mathematical content is sound; only the framing needs a single consistent reading. Derivable from the ASN's own content.
