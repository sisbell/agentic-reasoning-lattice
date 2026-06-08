# Channel Assignment — ASN-0100 review-108

**Date:** 2026-06-07 22:38

## Issue 1: Prepend boundary (j=0, full-clearance) lacks a concrete worked example
Reason: Fully internal — the j=0 mechanics (forced `n'_{s_C}=0`, vacuous post-K.μ⁻ intermediate, full-run K.μ⁺, re-pinned minimum) are already specified abstractly in the Σ'-uniqueness section and the formal contract; the fix only instantiates them as a concrete example and checks INS.inv.seq / D-MIN★, both already proven generally.

## Issue 2: Reviser-drift paragraph inside a worked example that stipulated the contrary case
Reason: Fully internal — this is an editorial relocation of content (empty arrangement ≠ empty content store) that already lives in the ASN (INS.alloc keys K.α's branch on `dom(C)`); no design-intent or implementation evidence is needed to move it.
