# Channel Assignment — ASN-0086 review-197

**Date:** 2026-06-01 14:20

## Issue 1: "Reachable case" in L-ContiguousPrefix is subsumed by the "Extension" induction
Reason: Purely structural deduplication — whether the reachable case is subsumed by the induction is decidable from the proof's own logic (K-Step Conformance Preservation, clauses (b)/(c), EmptyInitialLinkStore). No design intent or implementation evidence bears on it.

## Issue 2: R0's per-invariant enumeration is a use-site inventory the conformance lemma already discharges wholesale
Reason: The fix is internal — clause (a) of substrate-conformance already names "the full L/S/M/C invariant catalog," so the roll-call's redundancy and the lone non-redundant L3 clause are both derivable from definitions present in the ASN.

## Issue 3: "Consequence — A_K is not monotone" forward-references and pre-stages the Worked Sketch
Reason: A presentation fix — restate the non-monotonicity abstractly and drop the forward-imported Σ_i/a_i labels. Both the abstract statement and the Worked Sketch witnesses already exist in the ASN; no external channel is needed.
