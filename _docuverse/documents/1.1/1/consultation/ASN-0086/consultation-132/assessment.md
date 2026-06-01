# Channel Assignment — ASN-0086 review-132

**Date:** 2026-06-01 01:12

## Issue 1: WP Case 2's "weakest precondition" is invalid over Emit_K's declared domain
Reason: The fix is a formal reconciliation already templated by Case 1's own treatment (carry PC as an explicit conjunct, or restrict the asserted domain). The required facts — Emit_K's declared domain, R0a's substrate-conformance gating, and the Case 1 pattern — are all present in the ASN; no design intent or implementation evidence is needed.

## Issue 2: Dangling "(i)–(iii)" reference in the state-transition section
Reason: Pure editorial cross-reference repair; the three step-types and their frame conditions are defined in the same section, so the label/replacement is derivable from the ASN alone.

## Issue 3: Redundant restatement of the single-fresh-home / n=1 decomposition in R7a
Reason: Deduplication of two passages stating the same decomposition fact; the surviving discharge (4)(iii) argument is internal to the proof, so the edit is fully derivable from the ASN.

## Issue 4: Repeated boilerplate clarifications across sections
Reason: Consolidating duplicated well-definedness and usage-discipline statements to their definitional homes is an internal editing task using only text already present in the ASN.
