# Channel Assignment — ASN-0058 review-19

**Date:** 2026-05-13 19:44

## Issue 1: M16 omits T4-validity verification of `a₁ + n₁`
Reason: Fix is internal — verifying T4 conjuncts under TumblerAdd uses only ASN-0034's T4 definition and the existing proof's setup (n₁ ≥ 1, (a₁)_{#a₁} ≥ 1). No design intent or implementation evidence required.

## Issue 2: M7 overlap exclusion conflates depth bounds
Reason: Fix is internal — restructuring the proof to derive `#v₂ = m` from S8-depth before invoking full prefix agreement is a logical reordering using already-cited dependencies (ASN-0034 T1, ASN-0036 S8-depth, S8a).

## Issue 3: First worked example does not state the same-origin assumption
Reason: Fix is internal — adding a clarifying sentence about same-origin assumption only requires referencing M16, which is already established in this ASN. Pure presentational clarification.
