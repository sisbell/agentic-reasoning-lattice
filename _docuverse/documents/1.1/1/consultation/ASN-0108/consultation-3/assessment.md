# Channel Assignment — ASN-0108 review-3

**Date:** 2026-06-05 04:10

## Issue 1: Mis-cited foundation claims in W7
Reason: A citation correction within the spec corpus — the review already supplies the correct labels (LP13 in ASN-0098, L12 in ASN-0043), and the M-mut paragraph in this same ASN already cites it correctly. Neither design intent (Nelson) nor implementation evidence (Gregory) bears on which claim-label lives in which foundation ASN; the fix is internal consistency.

## Issue 2: W5's necessity claim ("only if") is false as stated
Reason: A purely logical correction whose counterexample is fully exhibited in the review and follows from the ASN's own definition of `After(c, Σ')` consulting only the tail above `κ(c)`. No design intent or implementation fact is at stake — the weakened necessary condition is derivable from the ASN.

## Issue 3: W2's weakest-precondition argument is asserted, not exhibited
Reason: Writing the wp predicate explicitly and adding a concrete insertion walk is a derivation from the ASN's own `After`/`Window` definitions and the offset-vs-identity distinction already stated; no external intent or evidence is required to construct the demonstration.
