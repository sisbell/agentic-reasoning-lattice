# Channel Assignment — ASN-0036 review-187

**Date:** 2026-05-29 22:43

## Issue 1: OrdShiftHom cites a nonexistent proof part
Reason: Fully internal — OrdShiftHom has only parts (a) and (b), and the ASN's own proof shows S8a is consumed in part (b), so the corrected reference is derivable from the ASN's content alone.

## Issue 2: The shift-successor fact is restated three times before OrdShiftHom states it
Reason: Fully internal — this is prose deduplication. The OrdShiftHom lemma and its proof already contain the canonical statement, so removing the redundant lead-in passages requires no design intent or implementation evidence.
