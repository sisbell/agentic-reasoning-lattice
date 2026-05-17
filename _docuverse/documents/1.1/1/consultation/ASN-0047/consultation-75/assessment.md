# Channel Assignment — ASN-0047 review-75

**Date:** 2026-05-17 05:37

## Issue 1: Loose attribution in worked example
Reason: The ASN itself supplies both the correct discharge mechanism (SubAllocatorAxiom's namespace property at first emission) and the Cross-document disjointness lemma. K.α's own precondition prose ("By the axiom or by GlobalUniqueness (depending on case)") already names the case split. The fix applies the ASN's existing distinction to the worked example — no external evidence needed.

## Issue 2: Awkward presentation of K.δ zeros formula
Reason: Pure editorial cleanup. The per-case identities `zeros(e) = zeros(t)` for k ∈ {0, 1} and `zeros(e) = zeros(t) + 1` for k = 2 are already correct and primary in the ASN; removing the historical-correction commentary about a superseded formula is internal to the ASN's presentation.

## Issue 3: Redundancy between P3★ and P5★ in ExtendedTransitionInvariants
Reason: Both P3★ and P5★ are defined in the ASN itself, and the proofs of both reduce to the same P0/P1/P2/L12 chain. The choice between dropping one or annotating the equivalence is a presentational decision derivable from the ASN's own structure — parallel to the existing S9-vs-P0 traceability note. No design-intent or implementation evidence is needed.

## Issue 4: K.α freshness mechanism in worked example for first-emission case
Reason: K.α's precondition discussion in the ASN already enumerates the discharge umbrella (SubAllocatorAxiom for first emission, T10a for subsequent emissions within a frontier, Cross-document disjointness lemma for cross-document pairs). Spelling this out in the worked example or adding a footnote consumes only content already present in the ASN.
