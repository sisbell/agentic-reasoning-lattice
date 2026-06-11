# Channel Assignment — ASN-0112 review-57

**Date:** 2026-06-10 23:12

## Issue 1: Unproven existential in V3's "not least over all of T" remark; natural witness fails at the single-occupied-position boundary
Reason: The fix is internal — both repair paths use only machinery already in the ASN (T1's prefix ordering for option (a); D0/D1, TumblerSub, and S8a for option (b)'s case-split witnesses, which the review itself spells out). Neither design intent nor implementation behavior bears on whether the parenthetical is weakened to the order-theoretic fact or backed by the explicit constructions.

## Issue 2: The wp section derives a post-hoc discriminator for `Tight` but not the parallel — and equally derivable — one for `Exact`
Reason: The fix is internal — the `Exact` discriminator follows in two lines from premises already established in the ASN (S8a forcing `zpd = m_s` in the single-subspace case, V2's `zpd = 1` cross-subspace derivation, and the V5/V6 dichotomy with the wp(`Exact`) characterization). The review even supplies the derivation; no external consultation is needed.
