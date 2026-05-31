# Channel Assignment — ASN-0043 review-123

**Date:** 2026-05-30 19:06

## Issue 1: L11a shared-home case asserts chain routing through `d.0.s_L` without the forcing argument
Reason: The required forcing argument is pure tumbler-algebra: descent freezes the `sig` position so the subspace component at `#d + 2` can only be advanced to `s_L` by a depth-1 sibling sweep. This follows entirely from T10a/TA5-SigValid machinery already cited in the ASN, requiring no design intent or implementation evidence.

## Issue 2: Defensive scope meta-prose and a redundant restatement accreted around the L11a shared-home rework
Reason: This is a purely editorial fix — replacing defensive parentheticals with a positive structural statement the proof already establishes, and deleting a restated conclusion. The substance is fully present in the existing *Distinct homes* and *Shared home* sub-cases; no channel input is needed.
