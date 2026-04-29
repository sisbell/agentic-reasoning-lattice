# Revision Categorization — ASN-0036 review-19

**Date:** 2026-03-22 17:03

## Issue 1: Phantom foundation references — GlobalUniqueness
Category: INTERNAL
Reason: The fix is replacing a non-existent label with the correct ASN-0034 labels (T9, T10) that already exist in the formal export. The derivation logic is already spelled out in the issue itself.

## Issue 2: Phantom foundation reference — PrefixOrderingExtension
Category: INTERNAL
Reason: Same pattern as Issue 1 — replacing a phantom label with the actual ASN-0034 properties (T5, T10). The correct derivation is already described in the issue text.

## Issue 3: Worked example does not verify D-CTG, D-MIN, or D-SEQ
Category: INTERNAL
Reason: The V-position sets at each state are already explicit in the worked example, and D-CTG/D-MIN/D-SEQ are defined earlier in the same ASN. The checks are mechanical — e.g., {[1,k] : 1 ≤ k ≤ 5} satisfies D-SEQ with n=5.
