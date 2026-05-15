# Channel Assignment — ASN-0058 review-32

**Date:** 2026-05-14 23:14

## Issue 1: M7f elides the B3 case-split that distinguishes merge from split
Reason: Pure exposition fix internal to the ASN — the required case-split (M-aux + V-adjacency + I-adjacency) already exists verbatim inside C1a's verification and needs to be promoted to M7f's site. No design-intent or implementation question is in play.

## Issue 2: M16's citation of M0 for n₁ ≥ 1 is misdirected
Reason: Citation correction derivable from the ASN's own Definition (Mapping Block), which fixes `n ∈ ℕ with n ≥ 1`. M0 states a cardinality identity, not the positivity. No external channel needed.

## Issue 3: "Trivial partition corollary" mislabels a multi-step argument
Reason: Summary-table wording fix; the body's own construction (right/left-extension phases, M-aux translation, S8-fin termination) demonstrates the corollary is not trivial. Fully internal.
