# Channel Assignment — ASN-0101 review-8

**Date:** 2026-05-27 16:14

## Issue 1: D0's reduction proof inappropriately invokes S8a
Reason: Fix is purely internal — the review specifies the exact T1-only derivation needed, using lex-order facts already invoked elsewhere in the ASN. No design intent or implementation evidence required.

## Issue 2: D9's quantification is not restricted to d'' ∈ dom(Σ.M)
Reason: Fix is purely internal — ASN-0098's project definition (already referenced in the ASN) constrains the domain, and D4 supplies the lift to dom(Σ.M) ∩ dom(Σ'.M). The correction is a statement-level restriction, not a design or implementation question.
