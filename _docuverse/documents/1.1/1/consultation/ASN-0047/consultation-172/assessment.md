# Channel Assignment — ASN-0047 review-172

**Date:** 2026-05-31 21:24

## Issue 1: The K.δ k=0 frontier-identification mechanism is stated three times, two of them near-verbatim
Reason: This is a pure editorial deduplication — collapsing three restatements of the FrontierEquivalence-based frontier check to two sites (lemma + discharge section) and trimming the Rationale paragraph to its one local point (`¬IsNode(t)` needed for `parent(t)`). All content involved (the lemma, the precondition pair, the T4b parent-projection partiality) is already present in the ASN; no design intent or implementation evidence is required to decide what to keep or cut.
