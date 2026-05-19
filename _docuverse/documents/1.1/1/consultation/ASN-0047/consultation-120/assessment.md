# Channel Assignment — ASN-0047 review-120

**Date:** 2026-05-19 16:16

## Issue 1: K.δ case (ii) k = 2 sub-case A discharge is incomplete for subsequent accounts
Reason: The fix is internal to the ASN — both proposed remedies (explicit case-split into A1/A2, or direct appeal to T10a.6 DomainDisjointness) draw entirely on machinery already in scope: T10a's per-allocator-chain consistency, the K.δ k = 0 structural identity `parent(e) = parent(t_op)`, and the existing sub-case B/C discharges for the first-account case. No design-intent question and no implementation evidence is needed; this is a proof restructuring exercise.
