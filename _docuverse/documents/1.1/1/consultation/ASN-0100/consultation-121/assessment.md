# Channel Assignment — ASN-0100 review-121

**Date:** 2026-06-08 00:17

## Issue 1: Per-address content invariants discharged twice with identical reasoning
Reason: This is a pure editorial deduplication — both paragraphs discharge the same five invariants by the same mechanism already stated in the ASN. The fix (cite the §Post-state discharge from §Atomicity, keep only the genuinely-new intermediate obligations) is fully derivable from the ASN's own text.

## Issue 2: L0 content conjunct deferral is fragmented across three sections
Reason: This is an internal cross-reference cleanup — the ASN already contains the single actual discharge (§Post-state S7 bullet); the fix is just repointing the two deferrals there and removing the redundant restatement. No design intent or implementation evidence is required.
