# Channel Assignment — ASN-0112 review-4

**Date:** 2026-06-05 00:24

## Issue 1: V14 quantifies over covered positions, but the supporting invariant is about occupied positions
Reason: Purely internal logical fix — S3 ranges over `O(d)` and V6 already establishes `O(d) ⊊ ⟦σ_d⟧`; restricting V14's quantifier to occupied positions resolves the contradiction using definitions already present.

## Issue 2: Precondition 2 introduces an access notion with no referent in the abstract state
Reason: Internal scoping decision — the strand state `Σ = (C, L, E, M, R)` carries no entitlement component, the ASN already records the BERT gate as Gregory's evidence and notes it "does not change the value reported," so dropping/annotating it as a deployment-level concern needs nothing new.

## Issue 3: Result type silently unions a span with a span-set
Reason: Internal type-design choice — ASN-0053's span-set machinery (`⟨⟩`, singleton `⟨σ_d⟩`) is already cited; selecting uniform span-set typing vs. a tagged union is derivable from the note's own content.
