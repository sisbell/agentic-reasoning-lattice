# Channel Assignment — ASN-0100 review-78

**Date:** 2026-06-05 04:49

## Issue 1: Per-address content-invariant discharge is duplicated across two sections
Reason: The fix is purely structural deduplication — consolidate the per-address discharge into one location and cite from the other. The ASN already establishes that the post-state `dom(C)` equals the final K.α intermediate's `dom(C)` and that the final K.ρ intermediate is the boundary Σ', so the decision is internal to the document's own reasoning.

## Issue 2: "First insertion pins m_C" is stated three times
Reason: The fact and its correct home (the precondition) are both already present in the ASN; the fix is to state it once and remove restatements plus the forward reference. No design intent or implementation evidence is needed.

## Issue 3: §Background restates foundation vocabulary
Reason: The fix trims a restatement of the shared-vocabulary identity/location distinction while keeping the INSERT-specific behavioral claim, both of which are already present in the ASN and its cited shared vocabulary. Purely editorial, derivable from the ASN's own content.
