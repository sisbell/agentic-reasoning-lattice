# Channel Assignment — ASN-0091 review-70

**Date:** 2026-06-04 02:35

## Issue 1: RA-adm discharge restates the full foundation invariant list verbatim
Reason: Purely editorial compression. The three-step structure (ExtendedReachableStateInvariants → Σ' reachable → RA-adm) is already present in the ASN; dropping the enumerated list and the S7/M0/C1/C2 trailing sentence requires no external evidence.

## Issue 2: RE-ran's two-case uniformity is re-derived at each downstream use site
Reason: Internal. RE-ran's uniform statement and its target/non-target provenance are already established in "Domain Stability and Range Invariance"; replacing the two parentheticals with bare citations is a self-contained edit.

## Issue 3: Empty-case "every RE-* claim holds vacuously" over-generalises its own justification
Reason: Internal. The ASN already distinguishes arrangement-indexed claims (RE-ran, RE-proj, RE-μ) from component-global claims (RE-C, RE-L, RE-R, RE-origin, RE-cov) via their RA-frame provenance in the Claims table; scoping the vacuity justification accordingly is derivable from the ASN's own content.

## Issue 4: Defensive scope-justification inside ChainDisjointAdjacency
Reason: Internal. The lemma's conclusion `x+1 ≠ y` is already complete from domain disjointness; deleting the trailing defensive sentence requires no design intent or implementation evidence.
