# Channel Assignment — ASN-0070 review-18

**Date:** 2026-06-02 15:29

## Issue 1: "Single-valued both directions ⟹ partition into chains" is not valid without acyclicity
Reason: The fix is purely internal — the required acyclicity follows from T1's irreflexivity and transitivity (already invoked elsewhere in the ASN), since consecutivity implies strict `<`-increase and so cannot cycle. No design intent or implementation evidence is involved; this is a self-contained mathematical gap closed by citing T1(a)/(c).
