# Channel Assignment — ASN-0043 review-126

**Date:** 2026-05-30 19:36

## Issue 1: L11a shared-home case asserts the second child-spawn is `inc(d.0.s_L, 1)` without showing `k' = 1` is forced
Reason: The required justification is a closure argument over alternatives already present in the ASN — `k' = 2` violates TA5a given `zeros(d.0.s_L) = 3`, producing a non-T4 output barred by L0b; a further `inc(·, 0)` advances the subspace identifier off `s_L`, contradicting L0; and `#E ≥ 2` (L1b) forces a descent. Every cited fact (TA5a bound, L0b, L0, L1b) is internal, so the fix is derivable from the ASN alone.
