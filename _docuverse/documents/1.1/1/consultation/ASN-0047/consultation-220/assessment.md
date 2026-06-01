# Channel Assignment — ASN-0047 review-220

**Date:** 2026-06-01 05:58

## Issue 1: K.μ~ realisation keyed to `|dom_C(M(d))| ≥ 2`, contradicting its own sufficiency condition
Reason: The ASN's own necessity/sufficiency analysis already establishes the correct condition ("takes at least two distinct values") and explicitly proves bare cardinality insufficient; the fix is a direct restatement derivable from the ASN's existing content.

## Issue 2: P4a's trace-property status and design rationale restated across three+ locations
Reason: This is an anti-bloat deduplication entirely internal to the ASN — consolidating repeated trace-property explanation to the definition box and replacing downstream restatements with citations requires no design intent or implementation evidence.
