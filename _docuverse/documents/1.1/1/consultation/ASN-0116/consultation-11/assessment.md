# Channel Assignment — ASN-0116 review-11

**Date:** 2026-06-08 23:23

## Issue 1: INSERT allocates content into an arrangement but records no provenance — the post-state violates ASN-0047's P7a, and the composite violates J1★
Reason: The formal obligation (J1★/P7a) is fixed by ASN-0047, but choosing between fix (a) — fold K.ρ provenance steps into the composite — and fix (b) — scope provenance out and prove P7a holds anyway — requires knowing whether the design intends insertion to establish provenance atomically (Nelson) and whether the implementation actually records a provenance/origin relation on the insert path (Gregory).
Nelson question: Is the binding of newly inserted content to its inserting document meant to be established as part of the insertion itself, or is provenance a separately-maintained relation distinct from the act of placing content?
Gregory question: Does the udanax-green insert path write any provenance/origin record (beyond the I-address origin stamp from findpreviousisagr) coupling each freshly allocated content address to the document it was inserted into?
