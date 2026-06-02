# Channel Assignment — ASN-0086 review-224

**Date:** 2026-06-01 18:43

## Issue 1: WP Case 1 presents a sufficient — not weakest — precondition, silently omitting the self-emit branch
Reason: The fix is internal — both repair paths (compute the true weakest precondition including the `a = a_emit(Σ, d_retr)` branch, or relabel Case 1 as deliberately sufficient-only) rest entirely on machinery already in the ASN: `a_emit`'s freshness, R0a's antichain at Σ', and the self-emit configuration the document itself constructs in Worked Sketch Step 4. No design intent or implementation evidence is required.
