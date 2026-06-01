# Channel Assignment — ASN-0047 review-239

**Date:** 2026-06-01 11:24

## Issue 1: GlobalLineage part (iii) reproves by induction what a one-line argument already supplies in part (ii)
Reason: Pure internal restructuring. The one-line replacement uses only T4b's parse and L1 (`zeros(ℓ) = 3`), both already present in the ASN; the document-prefix-to-third-separator fact is identical to part (ii)'s content argument. No design intent or implementation evidence is required to delete the redundant induction.

## Issue 2: K.δ's core discharge is fragmented across the document, with ≥4 sites deferring to one downstream section
Reason: Pure editorial reorganization of existing material. Inlining the case-(ii) discharge or collapsing the cross-section deferrals reuses content already written; no new theory or implementation facts are needed.

## Issue 3: P6, P7, P8 each carry a full preservation argument twice
Reason: Pure deduplication. Choosing one canonical home for each preservation argument requires only the ASN's existing derivations; no external channel input is needed.
