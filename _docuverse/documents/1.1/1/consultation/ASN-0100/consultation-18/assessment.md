# Channel Assignment — ASN-0100 review-18

**Date:** 2026-05-28 12:44

## Issue 1: Worked example misstates `coverage` as a finite address set
Reason: The fix is internal — the `coverage` definition (ASN-0098), the canonical span machinery, and the `project = coverage ∩ ran(M(d))` characterisation are all already present in the ASN; this is a notational correction consistent with definitions the ASN already cites.

## Issue 2: `δ(0, m_C)` invoked in the functionality disjointness arithmetic
Reason: The fix is internal — the ASN already splits `k = 0` (via OrdinalShiftBase, ASN-0058) from `k ≥ 1` in its S8a/S8-depth sections, so the functionality paragraph need only apply the same split it already uses elsewhere.
