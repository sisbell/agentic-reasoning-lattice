# Channel Assignment — ASN-0069 review-17

**Date:** 2026-05-25 17:50

## Issue 1: V8b's K.μ⁺_L argument cites V4b for a fact V4b does not supply
Reason: Citation correction internal to the ASN — F ⊆ V_{s_C}(d_src) follows trivially from F's definition as a restriction, and V5 supplies the time-invariance of V_{s_C}(d_src). Both facts are already present in the ASN; no external input needed.

## Issue 2: V12(d) contains meta-commentary about an earlier draft
Reason: Editorial fix — remove the draft-history parenthetical or restate as a positive claim. The underlying mathematical fact (V4 ⇒ ran(M'(d_new)) ⊆ ran(M(d_src))) is already established in V4; the revision is purely a presentation change.

## Issue 3: V11's premise is ambiguous about which state determines the restriction set V_{s_C}(d^{i-1}_new)
Reason: Formal precision fix — the review itself supplies the required tightening (premise must forbid both domain changes and value changes on the chain source's content-subspace across the gap). The derivation in V11 already depends on this stronger reading; making the premise explicit is internal to the ASN.
