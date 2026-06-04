# Channel Assignment — ASN-0101 review-58

**Date:** 2026-06-04 06:29

## Issue 1: P4★/P7a at a DEL-terminated composite boundary asserted, not derived
Reason: The derivation chain uses only premises already present in the ASN — P4★/P7a holding at the prior boundary Σ, the ValidComposite★ coupling constraints J0/J1★ from D10, and D8's monotone-shrinking-of-`Contains_C` plus `R' = R` neutrality. Writing out each conjunct of P4★ (`Contains_C(Σ') ⊆ R'`) and P7a at Σ' is an internal expansion requiring no design intent or implementation evidence.

## Issue 2: Accreted attribution-policing prose in the composite-boundary section
Reason: Purely editorial — collapsing redundant paragraphs and deleting inter-paragraph attribution commentary draws only on the ASN's own content. No external channel needed.
