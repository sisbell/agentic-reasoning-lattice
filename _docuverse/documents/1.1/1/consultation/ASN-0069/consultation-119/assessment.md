# Channel Assignment — ASN-0069 review-119

**Date:** 2026-06-03 03:48

## Issue 1: V10(b) invokes V5a without discharging its `d* ∈ Σ.E_doc` hypothesis
Reason: Neither channel is needed. The fix restricts the preservation claims to sequences beginning at or after Σ² and discharges V5a's membership hypothesis via P1 — exactly the pattern V5/V5a already use elsewhere in the ASN, so it is internal.

## Issue 2: Worked example re-explains the `d_new²` / `d²_new` notation already fixed in the notation block
Reason: Neither channel is needed. This is a pure anti-bloat deletion of duplicated notation already fixed in the §"Independence Among Forks" block; no design intent or implementation evidence bears on it.

## Issue 3: Essay flourish in §"Composability" restates V8c
Reason: Neither channel is needed. This is anti-bloat compression of rhetorical content that merely restates the already-cited V8c; the fix is internal to the ASN's own property set.
