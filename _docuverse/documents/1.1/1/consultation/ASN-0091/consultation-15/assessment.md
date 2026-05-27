# Channel Assignment — ASN-0091 review-15

**Date:** 2026-05-26 18:15

## Issue 1: P4a verification framing in admissibility section
Reason: Fix is internal — P4a's definition is in the ASN's dependency chain (ASN-0036), RE-R preserves R, and REARRANGE extends transition history without altering prior states. All ingredients are already present; the revision is a framing correction.

## Issue 2: Worked examples don't exercise content-subspace exterior under R-EXT
Reason: Fix is internal — R-EXT is defined in ASN-0084 (already cited), and constructing a third concrete trace with interior cuts follows the same mechanical pattern as the existing worked examples. No design intent or implementation evidence required.
