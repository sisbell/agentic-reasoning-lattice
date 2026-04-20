# Revision Categorization — ASN-0051 review-17

**Date:** 2026-03-23 03:01



## Issue 1: Worked example does not verify SV6 (CrossOriginExclusion)
Category: INTERNAL
Reason: The fix is adding a concrete cross-origin scenario to the worked example. The review already provides explicit tumbler values and the verification steps; all required definitions (TumblerAdd, origin, field separators) are present in the ASN and its dependencies.

## Issue 2: SV7 formal content understates its claimed insight
Category: INTERNAL
Reason: Strengthening the formal statement from ⊆ to = for K.μ⁺/K.μ⁺_L transitions follows directly from the frame condition (L' = L) already cited in the ASN's own prose. No external evidence needed.

## Issue 3: SV6 proof — first-divergence reasoning is implicit
Category: INTERNAL
Reason: The fix is making explicit that j is the first divergence position before applying T1(i), and noting the agreement chain for the s⊕ℓ comparison. All required ordering axioms (T1) are already present in the ASN's dependencies.
