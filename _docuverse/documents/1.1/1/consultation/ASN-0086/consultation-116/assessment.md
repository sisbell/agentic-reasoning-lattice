# Channel Assignment — ASN-0086 review-116

**Date:** 2026-05-31 22:26

## Issue 1: wp Case 2 regime (i) "automatic" simplification is unsound over the stated domain
Reason: The fix is internal — the ASN already establishes that R0a holds only at substrate-conforming states and that Emit_K's domain is the strictly weaker state-local-conforming sub-space (which admits the antichain-violating witness). Restricting the "automatic" claim to conforming pre-states, or retaining `NoCraftedSpanReachesD` as an irreducible conjunct, follows from definitions already present.

## Issue 2: R0a-Cor1 induction base assumes `dom(Σ_init.L) = ∅` without justification
Reason: The note needs a ground for the initial link-store state; deciding between "assume empty" and "generalize the base to whatever seed the substrate admits" requires knowing what the implementation actually initializes the link store to at boot, which is implementation evidence.
Gregory question: At system initialization (before any link allocation), does udanax-green's link store begin empty, or can it boot with a pre-populated set of link addresses — and if pre-populated, are those addresses a contiguous sibling-chain prefix per home?

## Issue 3: Anti-bloat — changelog prose, repeated defensive clauses, and redundant restatement
Reason: Purely editorial deletions specified verbatim by the review (changelog fragment, three collapsed-to-one repetitions, duplicated table contingency clause, orphan S3 sentence); no design intent or implementation evidence is involved.

## Issue 4: R6b formal statement uses prose predicates inside the quantifier
Reason: The fix is internal — the review supplies the exact formal replacement, and its content is already proved precisely in R6b's own proof; this is a notation correction derivable from the ASN.
