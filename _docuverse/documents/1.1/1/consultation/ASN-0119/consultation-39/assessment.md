# Channel Assignment — ASN-0119 review-39

**Date:** 2026-06-10 07:16

## Issue 1: P4a Case (ii) rests on ASN-0047's proof internals, not its claims
Reason: Internal. The required fix is a proof restructuring using ingredients already present in this ASN — the coupling **J1'★** (a *claim* of ASN-0047, already imported and cited here) discharges new entries, and the inductive hypothesis `U(n)` discharges pre-existing ones. The review fully specifies the claim-based path; no design intent or implementation evidence is at issue, only replacing a proof-internals appeal with a claim-level derivation.

## Issue 2: Forward-reference announcements of the worked example (anti-bloat)
Reason: Internal. Pure deletion of meta-prose clauses; no reasoning content depends on any external source.

## Issue 3: Non-circularity reassurance in the P4a induction (anti-bloat)
Reason: Internal. Pure deletion of a defensive sentence; "by induction" already carries the claim the sentence restates.

## Issue 4: R-COMM "offset's sign" conflates two distinct quantities (minor clarity)
Reason: Internal. Both quantities are already fixed by the ASN's own content — the non-negative within-region shift `k` (R-COMM / ASN-0034's positive ordinal-shift definition) and the signed net translation `π(v₀) − v₀` (read off R-PPERM/R-SPERM). The fix is a prose-precision separation requiring nothing external.
