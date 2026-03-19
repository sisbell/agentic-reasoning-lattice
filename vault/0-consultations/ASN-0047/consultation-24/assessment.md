# Revision Categorization — ASN-0047 review-24

**Date:** 2026-03-17 12:17



## Issue 1: Missing derived invariant — every I-address has provenance
Category: INTERNAL
Reason: The derivation is fully supplied from existing machinery (J0, J1, P2). This is a matter of stating and numbering an invariant that already follows from definitions in the ASN.

## Issue 2: P4 proof case (i) — misleading dash clause
Category: INTERNAL
Reason: This is a prose clarity fix — the logical content is correct, only the phrasing obscures the exclusion structure. The replacement wording is provided.

## Issue 3: K.δ frame condition diverges from the pattern used by other transitions
Category: INTERNAL
Reason: M is defined as total in the ASN itself, so M(e) = ∅ for e ∉ E_doc already covers the pre-state value. The frame rewrite and footnote correction follow directly from the ASN's own definition of M's totality — no external evidence needed.
