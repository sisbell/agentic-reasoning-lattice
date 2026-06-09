# Channel Assignment — ASN-0121 review-20

**Date:** 2026-06-09 02:28

## Issue 1: FL-WP omits the fresh-retraction-link entry, a third result-changing case
Reason: Derivable from the ASN alone. FL-DEF and FL-WILD already commit `findlinks` to range uniformly over all of `addressable(Σ)` "of every arity N≥3"; a retraction link satisfies L3 (`e₃ = R ≠ ∅`), sits in `dom(Σ.L)`, and is thus a candidate member by the ASN's own definitions — exclusion would contradict FL-WILD, so the case must be added, not waived. Its wp is structurally FL-WP(a) with ordinariness relaxed, `L_R^{Σ'} = L_R^Σ ∪ {(b,∅,G')}` (FL-WP(b)'s extension), and the self-retraction conjunct `b ∉ coverage(G')` retained — every piece of machinery is already present in the ASN.
