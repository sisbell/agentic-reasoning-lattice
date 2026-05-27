# Channel Assignment — ASN-0101 review-2

**Date:** 2026-05-27 14:22

## Issue 1: σ_d formula yields the wrong result for depths m_S ≥ 3
Reason: Pure mathematical correction within TumblerSub (ASN-0034). The fix follows from the foundation's own algebra — no design intent or implementation evidence needed.

## Issue 2: Worked example computation is wrong
Reason: Consequence of Issue 1; correcting the formula corrects the computation. Internal arithmetic only.

## Issue 3: D1 "post-state characterisation" is asserted, not derived
Reason: Once the formula is fixed, the derivation is a mechanical TumblerSub computation citing the existing ASN-0034 spec. Internal.

## Issue 4: D8's D-CTG★ preservation fails under the current formula
Reason: Direct consequence of Issue 1. Once σ_d is correctly defined, D8 follows from the corrected D1. No external input needed.

## Issue 5: "What shifts" narrative repeats the computation error
Reason: Prose alignment with the corrected formula. Internal rewrite using TumblerSub's actual semantics.

## Issue 6: D-MIN★ derivation in "Deletion at the start" boundary case is unjustified
Reason: Same root cause as Issue 1; boundary case verification follows mechanically once σ_d is corrected. Internal.

## Issue 7: Worked example's "Verification of D8" mis-states V_1(M'(d))
Reason: Consequence of Issue 1. The intended verification becomes correct once σ_d produces the right post-state.

## Issue 8: Atomicity argument against K.μ⁻ ∘ K.μ~ is hand-waved
Reason: Argument rests on the formal contracts of K.μ⁻ and K.μ~ in ASN-0047, which are already cited. Reorganising the case-split and fixing the spurious "D5" cross-reference is internal. Nelson's primitive-status and Gregory's run-to-completion evidence are already woven into the paragraph.

## Issue 9: ValidComposite★ admissibility is asserted but not formally extended
Reason: Formal extension of ASN-0047's existing enumeration with a named claim. The vacuity of J0/J1★/J1'★ at a DEL step follows directly from D0's frame conditions. Internal.

## Issue 10: Recoverability section makes an unsupported claim about versioning behavior
Reason: Fix is to cite J4 (ForkComposite) from ASN-0047 — already in the foundation — or rephrase to keep versioning outside DEL's scope. Internal correction against the existing framework.
