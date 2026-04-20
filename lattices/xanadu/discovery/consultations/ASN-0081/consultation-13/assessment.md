# Revision Categorization — ASN-0081 review-13

**Date:** 2026-04-09 22:21

## Issue 1: Additive compatibility identity used without derivation in D-SHIFT
Category: INTERNAL
Reason: The identity `ord(p ⊕ w) = ord(p) ⊕ w_ord` is derivable from TumblerAdd (ASN-0034) and the ord/w_ord definitions already present in this ASN. The review itself supplies the three-step depth-2 computation and notes the pieces are already scattered across D-SHIFT and D-SEP — assembly into a named lemma requires no external evidence.
