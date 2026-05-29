# Channel Assignment — ASN-0036 review-173

**Date:** 2026-05-29 05:33

## Issue 1: S8a carries downstream-consumer justification and restates the domain-restriction axiom
Reason: Purely editorial. The fix strikes meta-prose and restates S8a as the per-component form of the domain-restriction axiom; the equivalence `zeros(v) = 0 ⟺ (A i : vᵢ > 0)` already rests on T0, which the ASN cites. No design-intent or implementation evidence is in play.

## Issue 2: S5 existence construction is not verified to be a well-formed strand state
Reason: Internal. Both remedies — instantiating `a` as an element-level address (`zeros = 3`, e.g. the `1.0.1.0.1.0.1.1` form already used in the worked example) and verifying S7b/S8-fin/S8a/domain-restriction, or declaring S5 a relative-consistency result over the bare S0–S3 — are fully derivable from the ASN's own definitions and existing constructions. No question of design intent or implementation behavior arises.
