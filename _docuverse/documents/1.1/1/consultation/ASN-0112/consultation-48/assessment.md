# Channel Assignment — ASN-0112 review-48

**Date:** 2026-06-08 12:42

## Issue 1: V-ReachTight's "common depth" gloss contradicts its own iff
Reason: The fix is internal — the iff `reach(σ_d) = reach_d ⟺ #origin_d ≤ #reach_d` is already established in the ASN's V2 covering cases and reused correctly in `wp(…, Tight)`; the correction merely replaces the false `=` ("common depth") gloss with the weaker `≤` condition already proven present. No design intent or implementation evidence is required.
