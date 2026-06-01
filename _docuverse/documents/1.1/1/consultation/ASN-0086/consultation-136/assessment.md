# Channel Assignment — ASN-0086 review-136

**Date:** 2026-06-01 01:50

## Issue 1: "R0a-Cor1" is a prerequisite of R0a, not a corollary — label and ordering are inverted
Reason: The fix is internal — the ASN already supplies R0a-Cor1's full proof (induction on conformance transitions using only the at-most-one-key discipline, frontier-landing, and ChainEnumerationInjectivity) and confirms it never invokes R0a, so reordering and relabeling is derivable from the present content.

## Issue 2: R5.1 citation in Nullify's definition assumes a precondition the composition's stated execution domain drops
Reason: The fix is internal — the ASN already contains the general T12 well-formedness argument (`#a ≥ 1` by T0, `actionPoint(δ(1,#a)) = #a ≤ #a`) covering the `a ∉ A_rel^Σ` case, and R5.1's `a ∈ A_rel^Σ` precondition is stated in-note; restricting the citation needs no external input.

## Issue 3: Use-site inventory / protocol rationale in the substrate-conforming-state definition
Reason: The fix is a deletion of self-referential citation bookkeeping; no design intent or implementation evidence bears on removing the sentence.

## Issue 4: Forward-reference meta-prose in Remark — NestedLinkWitness
Reason: The fix is a deletion of a forward-reference clause; the witness construction is fully present and the change requires nothing beyond the ASN.

## Issue 5: Duplicated scope prose in the Weakest-Precondition Analysis
Reason: The fix folds two redundant in-note paragraphs into one; both already appear in the ASN, so the consolidation is purely internal.
