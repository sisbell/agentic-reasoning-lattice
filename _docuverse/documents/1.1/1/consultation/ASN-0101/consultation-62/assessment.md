# Channel Assignment — ASN-0101 review-62

**Date:** 2026-06-04 06:58

## Issue 1: Reconstruction reasoning is split across two passages that both defer to out-of-scope versioning
Reason: The fix is internal. Both passages and the corrective fact (DEL is information-destroying w.r.t. `M(d)`; reconstruction depends on out-of-scope versioning) are already present in the ASN; consolidating to the in-scope statement requires no design intent or implementation evidence.

## Issue 2: D9 prose duplicates the LP-family extension that D10 owns
Reason: The fix is internal. D10's LP-family paragraph already discharges LP17/LP18 carry-over via D3 and LP3★; removing the duplicated assertion from D9 and leaving only its projection consequence is a pure deduplication derivable from the ASN's own structure.
