# Channel Assignment — ASN-0086 review-64

**Date:** 2026-05-19 14:14

## Issue 1: R5's from-set case not explicitly demonstrated
Reason: The fix is purely expository — the generalization paragraph already licenses any L3-conforming triple, so adding an explicit slot-1 instantiation (or parallel concrete emission) follows directly from material already in the proof. No design intent or implementation evidence is required.

## Issue 2: Relational layer's "Nullify-is-sole-producer" discipline not explicit in Definition
Reason: The ASN already takes the position that the unit-depth retraction discipline is a layer convention (Implementation Notes) and acknowledges callers could bypass via direct K.λ. The fix is choosing among three formal expressions of an already-committed stance — internal hygiene between the Definition and WP Case 2's claim.

## Issue 3: WP Case 2's `NoCraftedSpanReachesD` lacks a formal definition
Reason: The fix introduces an auxiliary function `a_K(Σ, d)` from ASN-0093 K.λ's first/subsequent emission rule (already cited throughout) and writes the predicate as a universal over `L_R^Σ`. Both ingredients are present in the ASN's own content.

## Issue 4: R6c base case verification too compressed
Reason: The fix expands "immediate" into one sentence using the Definition of `A_K` and the precondition — both already in the ASN. Pure proof-clarity, no external input needed.
