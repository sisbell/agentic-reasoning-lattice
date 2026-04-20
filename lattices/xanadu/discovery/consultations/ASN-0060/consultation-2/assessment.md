# Revision Categorization — ASN-0060 review-2

**Date:** 2026-03-21 02:02

## Issue 1: Undefined "V-position" in OrdinalShift definition
Category: INTERNAL
Reason: The fix is derivable from the ASN's own content — the lemmas I6, I7, I8 already quantify over arbitrary tumblers of depth m, and the underlying operations (⊕, δ) from ASN-0034 are defined on arbitrary tumblers. Replacing "V-position v" with "tumbler v" resolves the inconsistency by matching the definition's domain to what the lemmas already prove.
