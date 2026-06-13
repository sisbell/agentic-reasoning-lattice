# Channel Assignment — ASN-0122 review-2

**Date:** 2026-06-12 22:44

## Issue 1: `subspace(start) = s_C` does not entail "span confined to the content subspace," and is not the mechanism that makes the result content-only
Reason: The fix is internal — every ingredient is already present. The counterexample (`σ = ([1,5], [3])`) is worked out in the T12 span algebra the ASN already depends on; the load-bearing mechanism (the unconditional `∩ V_{s_C}(d_i)` clip) is the ASN's own region definition; X9's losslessness is the ASN's own result; and option (a)'s justification (`(s⊕ℓ)₁ = s₁ = s_C` under prefix copy, plus T5 contiguity) uses only foundation theorems already cited. The choice between strengthening the precondition (a) and pinning losslessness to the clip while demoting the predicate to operand hygiene (b) is a spec-presentation decision aligned with the ASN's already-established clip philosophy and its `(u, δ(n, m))` feet — no design intent or implementation evidence is required to settle the content-only goal, which X9 already fixes.
