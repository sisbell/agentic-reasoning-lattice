# Channel Assignment — ASN-0084 review-41

**Date:** 2026-05-15 18:27

## Issue 1: R-NS forward reference not acknowledged
Reason: This is a structural/documentary issue about the ASN's own organization. The fix (add a forward-reference note or reorder sections) is derivable from the ASN alone — the author already knows R-PPERM/R-SPERM define π's non-S branch.

## Issue 2: Operation REARRANGE_C partiality not explicit
Reason: The minimal fix (one sentence stating REARRANGE_C is undefined when R-PRE fails) follows from the ASN's existing counterexample sketches and standard Dijkstra-style conventions. The R-PRE counterexamples already demonstrate the postcondition can be unsatisfiable; declaring partiality is internal. Gregory could be consulted only if the author wants substantive runtime failure semantics beyond bare partiality.
Gregory question: When REARRANGE is invoked with arguments violating its preconditions (e.g., cut sequence extending beyond the document's V-positions), does udanax-green refuse the operation, signal an error, or exhibit some other defined failure behavior?

## Issue 3: Canonical-decomposition step (b), n₁ = n₂ derivation has gap
Reason: This is a proof-presentation gap fully internal to the ASN. The hypothesis "let b₁ and b₂ be maximal runs sharing a V-position" is label-symmetric, and the fix (one sentence noting the n₁ > n₂ case re-runs the entire (b) argument with labels swapped) requires only the ASN's existing reasoning.
