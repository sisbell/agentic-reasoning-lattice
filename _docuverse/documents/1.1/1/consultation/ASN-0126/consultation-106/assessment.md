# Channel Assignment — ASN-0126 review-106

**Date:** 2026-06-10 13:05

## Issue 1: Retraction and sterilization are analyzed only for Binary-registered [R]; the framework leaves [R]'s registration free
Reason: Choosing between the two licensed fixes — commit [R] to Binary versus analyzing all three corners — is a design/evidence question, not internal math: the note's attribution convention is already grounded in Nelson's metalink pattern, and whether range-form or single-target retraction has precedent determines whether the Multi-R corner is real or scope-out-able. Corners (a) and (b) close internally either way.
Nelson question: Was retraction/deletion of a link intended as a mandatory, fixed-form act of the system (one attributed act withdrawing one link), or did the design admit configurations with no retraction at all, or acts that withdraw whole regions of links at once?
Gregory question: How does udanax-green remove or retract links — strictly one link per operation, or can a single operation (e.g., a vspan delete over the link subspace) excise a contiguous range of link addresses?

## Issue 2: `Nullify_Binary` has no operation contract
Reason: Internal. Every contract component the review lists (preconditions, effect, frame, the iff-P-tgt scope guarantee, the nullified-set behavior for non-P-tgt targets) is already derived in the Retraction section; the fix is assembling them into one ASN-0086-style block.

## Issue 3: The frontier-landing of raw `K.λ_sh` deposits is asserted, not derived
Reason: Internal. The review sketches the complete derivation from L-ContiguousPrefix at pre- and post-state (a one-element extension of a contiguous initial segment that stays contiguous must add the frontier slot), using only results the note already B2-transfers.

## Issue 4: Up-set clause overclaims when the frontier has not yet entered B
Reason: Internal. This is a logic-conditioning fix — restrict "every future emission" to emissions after the frontier enters B — fully determined by the corollary's own case analysis.

## Issue 5: TA5(c) applied to `ℓ_prev` without discharging T4-validity
Reason: Internal. The identical hypothesis is already discharged in Range sterilization via L0b at the `→*`-reachable projection; the fix is repeating that one citation at the earlier instance.

## Issue 6: Worked illustration never exhibits the registry; gate precondition (i) and C0 are checked only nominally
Reason: Internal. The review explicitly licenses arbitrary distinct ghost-address singletons under a vocabulary prefix, and constructing them plus walking one CoverageEqualityDecidable comparison uses only the note's own address algebra and ASN-0043/0086 definitions.

## Issue 7: Duplicated statements accumulated across sections (anti-bloat)
Reason: Internal. Pure deduplication — deciding which single statement carries each fact and deleting the recaps requires no information beyond the note's own text.
