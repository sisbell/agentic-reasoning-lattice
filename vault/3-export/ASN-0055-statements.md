# ASN-0055 Formal Statements

*Source: ASN-0055-tumbler-algebra-0.md (revised 2026-03-19) — Extracted: 2026-03-19*

## TA-LC — LeftCancellation (LEMMA, lemma)

If a ⊕ x = a ⊕ y with both sides well-defined (TA0 satisfied for both), then x = y.

## TA-RC — RightCancellationFailure (LEMMA, lemma)

There exist tumblers a, b, w with a ≠ b and a ⊕ w = b ⊕ w (both sides well-defined).

## TA-MTO — ManyToOne (LEMMA, lemma)

For any displacement w with action point k and any tumblers a, b with #a ≥ k and #b ≥ k: a ⊕ w = b ⊕ w if and only if a_i = b_i for all 1 ≤ i ≤ k.

Sub-properties:

(a) (forward) If a_i = b_i for all 1 ≤ i ≤ k, then a ⊕ w = b ⊕ w.

(b) (converse) If a ⊕ w = b ⊕ w, then a_i = b_i for all 1 ≤ i ≤ k, where:
- For i < k: (a ⊕ w)_i = a_i and (b ⊕ w)_i = b_i (copy from start region)
- At i = k: (a ⊕ w)_k = a_k + w_k and (b ⊕ w)_k = b_k + w_k, so a_k = b_k
- For i > k: (a ⊕ w)_i = w_i = (b ⊕ w)_i (components of a, b unconstrained)
