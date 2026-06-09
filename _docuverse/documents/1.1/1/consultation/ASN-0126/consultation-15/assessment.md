# Channel Assignment — ASN-0126 review-15

**Date:** 2026-06-08 23:59

## Issue 1: Inconsistent count of K.λ_sh's added preconditions
Reason: Purely internal bookkeeping — the note must reconcile its own statements about how many preconditions K.λ_sh carries (three: (0),(i),(ii)) and scope the wp's omission of (0) to the wp derivation. No design intent or implementation evidence bears on a self-consistency count.

## Issue 2: Scope of the "at every emit" guarantee vs the direct-link-store escape hatch
Reason: This is a framing decision about whether `→_sh` is the complete transition relation of a framework substrate or a gate that can be bypassed — a definitional choice the note must make about its own architecture, not a fact about Nelson's intent or udanax-green's behavior.

## Issue 3: P4 "falls out of the wp derivation" conflates enablement with landing
Reason: The correct enablement-based derivation of P4 is already present in "The shape-gated emit"; the fix is to restate P4's justification from K.λ_sh's enablement preconditions rather than the active-subset wp. Fully internal to the ASN's own reasoning.
