# Channel Assignment — ASN-0071 review-11

**Date:** 2026-06-02 22:39

## Issue 1: Reinvented entity-predicate notation (IsNode / IsDocument)
Reason: Internal fix — the review already supplies the foundation's spelling (`Node`/`Document` from ASN-0047), and the correction is a mechanical rename within this ASN's prose; no design intent or implementation evidence is needed.

## Issue 2: `find`'s dependence on `dom(Σ.C)` mis-stated
Reason: Internal fix — the contradiction is visible from the ASN's own F-find and F-CUR definitions, which read only `E_doc` and `M`; dropping or rephrasing the parenthetical requires no external channel.
