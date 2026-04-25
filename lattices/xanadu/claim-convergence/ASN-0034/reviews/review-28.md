# Cone Review — ASN-0034/OrdinalShift (cycle 2)

*2026-04-13 22:44*

I've read the full ASN carefully against the previous findings. Here is one new finding.

### OrdinalDisplacement formal contract omits postconditions that callers must re-derive

**Foundation**: T0 (CarrierSetDefinition), PositiveTumbler
**ASN**: OrdinalDisplacement formal contract: "*Preconditions:* n ≥ 1, m ≥ 1 / *Definition:* δ(n, m) = [0, 0, …, 0, n] of length m with action point m"
**Issue**: OrdinalDisplacement's formal contract has no postconditions. OrdinalShift must then re-derive two load-bearing facts inline before it can invoke TA0: (1) `δ(n, m) ∈ T` (from the definition + T0, since the result is a finite sequence of length m ≥ 1 over ℕ), and (2) `δ(n, m) > 0` (from the definition + PositiveTumbler, since the m-th component is n ≥ 1). These are immediate consequences of the definition combined with properties already in the ASN, yet they are not exported. Any future property that composes OrdinalDisplacement with TumblerAdd/TA0 will face the same re-derivation burden, and the gap between what the contract advertises (a construction) and what callers need (membership and positivity guarantees) invites errors at each call site.
**What needs resolving**: OrdinalDisplacement's formal contract must export `δ(n, m) ∈ T` and `δ(n, m) > 0` as postconditions, citing T0 and PositiveTumbler respectively.

## Result

Cone converged after 3 cycles.

*Elapsed: 2412s*
