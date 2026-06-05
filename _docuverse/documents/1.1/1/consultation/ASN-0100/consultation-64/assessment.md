# Channel Assignment — ASN-0100 review-64

**Date:** 2026-06-05 02:47

## Issue 1: Post-K.μ⁺ intermediate state mislabeled as Σ'
Reason: Internal fix. The decomposition order (K.μ⁺ before the n K.ρ firings) and the fact that K.ρ frames M while extending R are both stated within the ASN; the correction follows directly from the ASN's own R-effect and frame clauses.

## Issue 2: §Formal Contract tail duplicates the atomicity/uniqueness content of §Atomicity
Reason: Internal fix. This is a pure deduplication of two passages already present in the ASN; deciding which copy to drop and reducing to a pointer requires no design intent or implementation evidence.

## Issue 3: INS.frame.dom is a redundant claim of INS.frame.E
Reason: Internal fix. The ASN itself states dom(M') = dom(M) as a specialization of E' = E; collapsing the redundant claim is derivable from the ASN's own Frame Conditions and claims table.
