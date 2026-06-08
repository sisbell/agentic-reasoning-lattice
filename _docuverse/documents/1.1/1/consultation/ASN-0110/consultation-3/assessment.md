# Channel Assignment — ASN-0110 review-3

**Date:** 2026-06-08 00:29

## Issue 1: Two incompatible region models — RE-decide demands `I = coverage(Q)`, but the worked example and RE-Vside use explicit finite I-sets
Reason: The inconsistency itself is internal (the three models provably disagree, and decidability for a finite explicit I-set is trivial), but choosing the *faithful* model requires knowing what the operation actually accepts as its region argument — a span-set or an enumerated address set — which is implementation evidence.
Gregory question: What does udanax-green's RETRIEVEENDSETS take as its content-region argument — a span/span-set (vspecset) that gets resolved to addresses, or an explicitly enumerated set of I-addresses?

## Issue 2: RE-translucent overclaims — "every endset whose coverage includes α"
Reason: Pure definitional error against RE-result, which restricts `Eᵢ` to slot-`i` values of stored links; the corrected quantifier is derivable from the ASN's own definitions.

## Issue 3: Worked-instance coverage values are stated as singletons when they are subtrees
Reason: The coverage of a unit span is the half-open tumbler interval `[s, s⊕ℓ)` (T12), a subtree, not a singleton; the correction follows directly from the ASN's own coverage and interval definitions.
