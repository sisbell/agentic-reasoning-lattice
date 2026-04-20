# Revision Categorization — ASN-0029 review-2

**Date:** 2026-03-11 09:10

## Issue 1: D0 missing actor constraint
Category: INTERNAL
Reason: The fix (`actor(op) = a`) is directly derivable from the pattern already established by D10a and D15 within this ASN. No external evidence needed.

## Issue 2: D12 precondition incomplete — no access check, no constraint on a_req
Category: INTERNAL
Reason: The required precondition follows from D5(c) (private access restriction) and the publication status model already defined in the ASN. The review specifies the exact fix from existing properties.

## Issue 3: D2 derivation hand-wave
Category: INTERNAL
Reason: The verification sketch requires checking D2 against operations defined in this ASN (D0, D10a, D12) and ASN-0026 (INSERT, DELETE, COPY, REARRANGE) — all already referenced with their relevant frame conditions (P7). No new evidence needed.

## Issue 4: Σ.pub frame not established for ASN-0026 operations
Category: INTERNAL
Reason: Σ.pub is new state introduced in this ASN; ASN-0026 operations predate it and cannot modify state they do not define. The frame extension is a logical consequence of the state separation already present in both ASNs.
