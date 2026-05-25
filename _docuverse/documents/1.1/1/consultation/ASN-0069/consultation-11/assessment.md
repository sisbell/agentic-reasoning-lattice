# Channel Assignment — ASN-0069 review-11

**Date:** 2026-05-25 16:04

## Issue 1: V10 framing restricts to consecutive sibling forks
Reason: Fix is internal — generalizing the framing relies only on V1's subsequent-fork sub-case and T10a.7, both already cited in the ASN. No design intent or implementation evidence question is involved.

## Issue 2: K.μ⁺ precondition verification cites V5 at intermediate state
Reason: Fix is internal — replacing the V5 citation with K.δ's frame condition (already invoked in the same verification) is a purely structural correction to the proof. No new external evidence needed.

## Issue 3: V11's premise wording understates what is actually required
Reason: Fix is internal — V4's content-subspace selectivity (already established in the ASN) and the K.μ⁺_L transition (defined in ASN-0047 and already referenced) supply everything needed to either tighten the premise or add the explanatory remark.
