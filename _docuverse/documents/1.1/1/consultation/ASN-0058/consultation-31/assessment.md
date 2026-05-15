# Channel Assignment — ASN-0058 review-31

**Date:** 2026-05-14 22:47

## Issue 1: OrdShiftHom citation for depth preservation in M12b
Reason: Pure citation correction — the correct source (OrdinalShift's postcondition `#shift(v, n) = #v` from ASN-0034) is already in scope and used elsewhere in this ASN. No design intent or implementation evidence is needed; the fix is mechanical citation replacement.

## Issue 2: M16a prose conflates document prefix with broader preserved segment
Reason: The mathematical argument is sound and `origin` is already defined by S7/S7b in ASN-0036 (cited in the proof). The fix is a prose disambiguation between the prefix tumbler (zeros=2) and the wider preserved segment (zeros=3) — both already characterized within the ASN's existing material. No external input required.
