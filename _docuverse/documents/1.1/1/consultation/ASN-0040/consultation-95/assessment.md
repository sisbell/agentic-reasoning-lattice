# Channel Assignment — ASN-0040 review-95

**Date:** 2026-05-29 03:18

## Issue 1: `s.B` and the foundation's `allocated(s)` are never reconciled in the body
Reason: Derivable from the ASN itself. The body already carries Gregory's two-phase anatomy (query vs. write, with "the write — not the query — is the moment of baptism") and the foundation's `allocated(s)`/T8 are available from ASN-0034; the required fix only asks to state that `s.B` is the committed-write registry while `allocated(s)` is the allocator's realized domain, with alignment left to the existing open question. No new design intent or implementation evidence is needed.

## Issue 2: Inconsistent contract labeling of foundation dependencies
Reason: Purely an internal editorial consistency fix — relabel foundation references (TA5, T1, NAT-closure) from "Axiom:" to "Depends:", reserving "Axiom:" for genuine design requirements. Fully derivable from the ASN's own conventions.
