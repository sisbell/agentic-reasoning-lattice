# Revision Categorization — ASN-0043 review-2

**Date:** 2026-03-16 21:53

## Issue 1: L13 — Span `(b, [1])` analysis is wrong
Category: INTERNAL
Reason: The fix requires correcting tumbler arithmetic using TumblerAdd and T12 from ASN-0034, and redefining "references entity b" as `b ∈ coverage(e)` rather than claiming exact singleton coverage. All definitions needed are already present in ASN-0034.

## Issue 2: L10 — Derivation gap from contiguity to span expressibility
Category: INTERNAL
Reason: The three missing steps (upper bound via TA5(c), expression as `p ⊕ ℓ`, T12 verification) are all derivable from ASN-0034 definitions. This is a mechanical gap-fill in a mathematical derivation.

## Issue 3: L9 is a consequence of L4 but presented as independent
Category: INTERNAL
Reason: The relationship between L4 and L9 is a logical entailment within the ASN's own property set. The fix is one sentence deriving L9 from L4 or merging them — no external evidence needed.

## Issue 4: L7 is a design principle, not a formalizable property
Category: INTERNAL
Reason: The reformulation as a negative meta-property ("the invariants L0–L14 impose no constraint on directional significance of slots") is verifiable by inspection of the invariant set already defined in the ASN. No design intent or implementation evidence beyond what is already quoted.
