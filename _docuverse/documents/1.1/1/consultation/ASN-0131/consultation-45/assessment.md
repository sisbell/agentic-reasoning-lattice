# Channel Assignment — ASN-0131 review-45

**Date:** 2026-06-14 00:57

## Issue 1: Intersection-composability left wholly open when the `⊆` half is immediately derivable
Reason: Fully internal. The image `⊆` law for intersection is already stated in the note, and `touch_W`, `Avail(Σ)` (region-independent), and the factoring proof pattern are all present from RE-UDIST; the `⊆` direction follows in one step (`touch_{W₁∩W₂}(e) ⟹ touch_{W₁}(e) ∧ touch_{W₂}(e)` for any `(i,e) ∈ Avail`) with no appeal to design intent or implementation behavior.

## Issue 2: The OQ1 / whole-endset provisionality is stated three times
Reason: Fully internal/editorial. Consolidating the provisional-status statement to one location (Extent + RE-WHOLE) and trimming the RE-DEF entry to a pointer is a restructuring of the note's own prose, requiring neither design intent nor implementation evidence.
