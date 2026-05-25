# Channel Assignment — ASN-0068 review-5

**Date:** 2026-05-25 00:50

## Issue 1: Iterated predecessor notation `v − j` not formally extended
Reason: Fix is internal — extending notation from the j=1 case already in the ASN to general j ≥ 0, using ShiftInjectivity (TS2, ASN-0034), D-SEQ★ (ASN-0047), and S8a (ASN-0036) already cited in the ASN.

## Issue 2: Predecessor-arithmetic step not cited
Reason: Fix is internal — the missing citations are M-aux (ASN-0058) for shift-addition associativity and the predecessor inverse property established in Issue 1's fix. Both are already part of the ASN's citation surface.

## Issue 3: Validity of R as a correspondence run not explicitly verified
Reason: Fix is internal — adds a verification paragraph stitching together the existing left-walk and right-walk constructions from the proof itself, using shift arithmetic that becomes properly cited after Issues 1 and 2.
