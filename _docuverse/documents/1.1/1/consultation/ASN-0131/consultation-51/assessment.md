# Channel Assignment — ASN-0131 review-51

**Date:** 2026-06-14 03:04

## Issue 1: Vestigial double-justification of the retraction emitter's addressability
Reason: Internal fix. The substantive claim — that RE-ADDR's general "does not retract its own emitter address" clause already covers `b` arity-independently, subsuming the `wp` Case 2 path — is established within the ASN (RE-ADDR's own derivation from the unit-depth discipline and R0a) and confirmed identical-in-content by the reviewer. Deleting the redundant pre-announcement, use-site clause, and claims-table tail requires no design intent or implementation evidence.

## Issue 2: The lemma-transfer bridge is framed as a use-site inventory with forward/back cross-references
Reason: Internal fix. The reviewer explicitly confirms the bridge's soundness obligation is discharged — the only change is reframing prose to state the conclusion self-containedly once and have R-Scope and `wp` Case 2 cite it by name, dropping the "we invoke below" announcement and per-site hypothesis re-derivation. No design-intent or implementation question remains open.
