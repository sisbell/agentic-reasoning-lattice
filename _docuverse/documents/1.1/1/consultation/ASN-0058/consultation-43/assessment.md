# Channel Assignment — ASN-0058 review-43

**Date:** 2026-05-15 06:30

## Issue 1: M-int's Component-m reduction step lacks explicit T1 derivation
Reason: Fix is internal — the required derivation uses T1, T3, TA0, TumblerAdd from ASN-0034, all already cited, and the proof technique is reused verbatim from M-int's earlier paragraphs (Subspace agreement, Prefix agreement).

## Issue 2: M12a's Equal Starts argument quietly handles the k₂ = 0 case via a "skip ahead" that needs explicit verification
Reason: Fix is internal — the boundary case discharge uses only conditions 1 and 3 of maximal runs (already defined in M12) plus OrdinalShiftBase; the review itself supplies both viable proof shapes, neither requiring design intent or implementation evidence.

## Issue 3: Two sections share the heading "A Worked Example"
Reason: Fix is internal — purely a presentational disambiguation of two section headings; no semantic or implementation question arises.
