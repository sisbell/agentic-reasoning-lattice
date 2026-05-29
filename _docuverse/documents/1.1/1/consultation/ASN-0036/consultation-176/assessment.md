# Channel Assignment — ASN-0036 review-176

**Date:** 2026-05-29 05:53

## Issue 1: S5's proof forward-depends on the entire downstream invariant set
Reason: Purely a document-ordering/scoping fix — the relevant invariants (S7*, S8*, D-*) are all defined within this same ASN, so relocating S5 or rescoping its witness obligation requires no external design intent or implementation evidence.

## Issue 2: Use-site inventory and citation-convention prose in structural slots
Reason: Editorial reduction of meta-prose; the content being trimmed is justification/convention internal to the ASN, derivable from material already present.

## Issue 3: S8-depth postcondition asserts existence of a common depth without guarding emptiness
Reason: The fix adds a `V_s(d) ≠ ∅` guard matching the pattern already used by D-CTG/D-MIN/D-SEQ in this ASN — wholly internal logical correction.
