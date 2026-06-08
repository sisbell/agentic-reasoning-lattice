# Channel Assignment — ASN-0102 review-109

**Date:** 2026-06-08 05:52

## Issue 1: X14 calls copied positions "fresh," contradicting X17's own domain-delta accounting
Reason: Purely internal wording defect — the fix is to drop the overloaded term "fresh" and restate the conclusion (`A ⊆ ran_{s_C}(Σ'.M(d))`), which the ASN already derives from the COPY effect clause and X17's own S8-fin domain-delta accounting. No design intent or implementation evidence is in question.
