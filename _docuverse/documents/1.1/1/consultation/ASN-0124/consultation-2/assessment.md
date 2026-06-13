# Channel Assignment — ASN-0124 review-2

**Date:** 2026-06-12 23:25

## Issue 1: FD-LOCAL(ii) "can add members" contradicts FD-FRAME
Reason: Internal consistency fix. The contradiction is fully diagnosed by the note's own claims — FD-FRAME proves `{K.δ, K.α, K.λ, K.ρ}` add no members and FD-STEP attributes all member-addition to K.μ⁺; the load-bearing "can never remove `d`" follows from FD-LOCAL(i). The Nelson [LM 4/60] non-impedance attribution is already settled and unaffected, so no channel is needed.

## Issue 2: FD-COMPLETE misdescribes the quantifier's range
Reason: Internal consistency fix. The correct range is fixed by the note's own definitions — `dom(Σ.M) = E_doc` with `zeros = 2`, and FD-V's `𝒫(E_doc)` codomain — against which the prose gloss listing nodes/accounts is simply wrong; the review supplies the exact corrected wording. No design-intent or implementation evidence is in question.
