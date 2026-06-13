# Channel Assignment — ASN-0123 review-31

**Date:** 2026-06-13 15:04

## Issue 1: V7 and VD restate the cross-owner severance/downward-limit argument twice
Reason: Pure deduplication, internal to the ASN. The severance result and its registry consequences are already proven (V9 severance, VD's `derives` biconditional and its failure direction); the fix is to make VD the single home and reduce V7 to the navigation consequence plus a pointer. No design intent or implementation fact is at issue.

## Issue 2: V-WF carries a downstream-consumer inventory of O5(i)/(ii)
Reason: Internal trim. V-WF's precondition discharge needs only `Document(v)` from the stream form, already stated in the preceding sentence; cutting the consumer-inventory to a bare forward pointer is purely editorial and consults nothing about design or implementation.

## Issue 3: The boundary/interior P4★ subtlety is developed twice, and the atomicity remark's second paragraph is a use-site inventory
Reason: Internal reorganization. The load-bearing reasoning (P4★ is a composite-boundary property that fails at interiors; the post-K.δ interior state is genuinely reachable) is already established in the ASN, and the implementation's whole-request realization is already documented in the evidence section; deduplicating onto V9w and trimming the use-site inventory needs no new design intent or implementation evidence.
