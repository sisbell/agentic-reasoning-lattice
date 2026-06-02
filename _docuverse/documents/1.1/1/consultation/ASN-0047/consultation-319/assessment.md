# Channel Assignment — ASN-0047 review-319

**Date:** 2026-06-02 02:54

## Issue 1: Freshness-discharge content stated once, then restated per sub-case
Reason: Purely an editorial deduplication choice — consolidate the per-sub-case encoding into one location (scope note or K.δ) and leave a bare pointer at the other. Nothing turns on design intent or implementation evidence; both the frontier-index (k=0) and at-most-once (k∈{1,2}) characterizations are already fully stated in the ASN.

## Issue 2: Rationale and use-site prose lodged in structural slots
Reason: Internal cleanup — the "imposed, not derived" status flag and the Nelson-motivation gloss are both already present in the ASN; the fix only decides which slot retains them and deletes the duplicate plus the "(used in the Notation)" pointer. No new design-intent or implementation fact is required to remove already-stated prose.
