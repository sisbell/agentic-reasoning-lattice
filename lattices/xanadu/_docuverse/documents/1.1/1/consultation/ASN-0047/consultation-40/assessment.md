# Revision Categorization — ASN-0047 review-40

**Date:** 2026-03-22 15:15

## Issue 1: K.μ~ dom_C(M(d)) = ∅ argument uses S3★ and K.μ⁺ amendment before they are established
Category: INTERNAL
Reason: The fix is purely presentational — either reorder the proof or add explicit forward-reference annotations. All required results (S3★, K.μ⁺ amendment) are already present within the ASN; no external design intent or implementation evidence is needed.

## Issue 2: ReachableStateInvariants theorem statement omits invariants established by its proof
Category: INTERNAL
Reason: The permanence properties P0–P2 are already proved by the permanence lemma within the ASN, and the extended theorem already lists them. The fix is adding them to the four-component theorem statement or adding a clarifying note — all information is internal.

## Issue 3: K.μ~ consequence — dom(M'(d)) = dom(M(d)) — not derived
Category: INTERNAL
Reason: The derivation follows from D-SEQ, bijection cardinality, and subspace preservation — all established within the ASN's own definitions and proofs. No external evidence about design intent or implementation behavior is required.
