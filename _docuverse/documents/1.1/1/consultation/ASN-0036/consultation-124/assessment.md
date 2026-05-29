# Channel Assignment — ASN-0036 review-124

**Date:** 2026-05-28 22:11

## Issue 1: OrdAddS8a derives `rₖ ≥ 2` when the claim needs only `rₖ > 0`
Reason: Pure proof-simplification — replacing the over-derived chain with `rₖ = vₖ + wₖ ≥ 1 > 0` and pruning the unused citations is fully internal to the ASN's own S8a definition and NAT axioms already cited.

## Issue 2: Citation-bookkeeping meta-prose in S8 Depends
Reason: Deletion of accounting prose; no design intent or implementation evidence bears on whether the sentence advances the argument.

## Issue 3: S8's proof establishes only the trivial singleton decomposition; the motivating prose promises more
Reason: Both remedies are internal — tempering the prose is editorial, and proving that an ordinally-corresponding contiguous block satisfies conjunct (b) follows from the ASN's own run definition, S2, S3, and shift semantics; neither requires Nelson's intent nor Gregory's code.

## Issue 4: m = 1 necessity paragraph reasons about a case the predicate's precondition excludes
Reason: Compression to the positive `m ≥ 2` statement is derivable from the existing OrdinalShift/TumblerAdd action-point facts already in the ASN; no external channel.

## Issue 5: `subspace_I` defined twice
Reason: Removing the duplicate naming sentence from S7c is a purely editorial deduplication internal to the ASN.

## Issue 6: S9 carries no content beyond S0 yet is restated at length
Reason: Reducing S9 to a one-line pointer is internal — S0's own prose already contains the directional reading, and naming Nelson's phrase is retained as-is without needing to query design intent.
