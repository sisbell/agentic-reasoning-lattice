# Channel Assignment — ASN-0087 review-16

**Date:** 2026-06-03 10:13

## Issue 1: K.μ~ reordering cannot rebind a link's V-position
Reason: Internal fix. The correction is fully determined by ASN-0047's K.μ~ admissibility clause (v) — link-subspace fixing means `π(v_ℓ) = v_ℓ`, so only K.μ⁻ can remove the binding. This is a spec-consistency repair against the cited foundation rule, requiring neither design intent nor implementation evidence.

## Issue 2: V-position depth fixed at 2 via a non-existent axiom
Reason: Internal fix. ASN-0047's `ValidFirstLinkPosition(d, v_ℓ, m)` already states the depth is a free parameter `m ≥ 2`; the fix is to align ASN-0087 with that foundation and delete the invented axiom citation. The foundation already encodes the answer, so no channel is needed.

## Issue 3: Phantom invariant citations S7c and S9
Reason: Internal fix. Whether S7c and S9/TwoStreamSeparation exist is settled by reading ASN-0036/ASN-0093; the reviewer already identifies the actual claims (S7/S7a/S7b/S7d; L14 + S0/P0 for separation). Pure spec-corpus citation correction.

## Issue 4: Per-state invariant verification omits C1b, C1c, ActivatedEmission
Reason: Internal fix. ASN-0047's ExtendedReachableStateInvariants enumerates the required per-state invariants; adding C1b, C1c (vacuous via `Σ'.C = Σ.C`) and ActivatedEmission (vacuous via `Σ'.E = Σ.E`) is mechanical completeness against the cited foundation list.

## Issue 5: Cited labels LP2★ and ChainUniformLength are not defined in the foundations
Reason: Internal fix. The replacements (LP13 / schema-★-applied-to-LP2 for value preservation; an actual ASN-0093 length result or an explicit derivation) are all available within the existing foundation ASNs the author maintains. No design or implementation evidence is required.
