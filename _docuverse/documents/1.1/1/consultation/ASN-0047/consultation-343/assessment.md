# Channel Assignment — ASN-0047 review-343

**Date:** 2026-06-02 07:18

## Issue 1: SSGU cross-node distinctness cites T10, whose precondition fails for nested baptised nodes
Reason: Fix is a proof-internal correction — the ASN already contains the correct premise (CrossNodeAccountBase's zero-separator divergence) and the nesting case it must handle; restating SSGU's cross-node clause as a case-split on prefix-comparability draws only on machinery present in the ASN.

## Issue 2: K.μ⁻ precondition carries defensive forward-deferring meta-prose
Reason: Pure prose trimming of redundant downstream deferrals and per-clause commentary; no design intent or implementation evidence is at stake.

## Issue 3: Triple-stated J1★ derivation rationale
Reason: DRY consolidation of an argument already stated three times within the ASN; cite-once-and-reference is entirely internal.
