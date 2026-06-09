# Channel Assignment — ASN-0116 review-3

**Date:** 2026-06-08 20:38

## Issue 1: P4's "superset" claim is false under the shift relabeling
Reason: Pure logical/set-theoretic error; the counterexample and correct relation (bijection ⇒ count non-decreasing, content monotone) are fully derivable from the ASN's own definitions of `project` and the shift map. No external channel needed.

## Issue 2: P6 computes a *sufficient* precondition, not the *weakest*
Reason: Internal correctness of a wp computation; the true weakest condition (`Added ⊆ D(d,Σ)`) versus the stronger `Added = ∅` is derivable from LP12 and the Effect clauses already cited in the ASN. No external channel needed.

## Issue 3: I3-S3 cited under a content frame INSERT overrides
Reason: The fix is to re-derive referential integrity for the left/shifted regions directly from S3 plus append-only monotonicity (P2), using facts already stated in the ASN. The dependency of I3-S3 on the content-fixed frame I3-C is a citation-hygiene matter resolvable internally. No external channel needed.

## Issue 4: Worked example does not exercise the link claims (P4, P5, P6)
Reason: Constructing a concrete link scenario (shifted-suffix witness plus ghost address minted into `A_new`) only instantiates claims already established in the ASN. No external channel needed.

## Issue 5: "resurrection (LP18)" mislabels the general new-witness case
Reason: The distinction between the general new-block witness gain (any `coverage(e) ∩ A_new ≠ ∅`) and the orphaned-link special case is settled by LP18's own stated scope, which the ASN already references; restricting the LP18 citation to the orphaned sub-case is derivable from the foundation definitions in hand. No external channel needed.
