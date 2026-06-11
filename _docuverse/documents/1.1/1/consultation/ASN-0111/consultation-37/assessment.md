# Channel Assignment — ASN-0111 review-37

**Date:** 2026-06-10 22:36

## Issue 1: RL4 witness construction leaves the extension step's enablement undischarged
Reason: The fix is internal — K.λ's full precondition (including the value-shape conjunct) is already cited from ASN-0093 within the note, and the worked example already exhibits an L3-conforming pattern (`(∅, G_c, Θ)`) that the abstract construction can adopt. Specifying `ℓ_c` with a non-empty type slot and splitting the precondition into state-dependent and branch-independent conjuncts requires no design intent or implementation evidence.

## Issue 2: The "exactly one attainable" claim in RL0 is supported by a fact too weak to deliver it
Reason: Internal fix — the correct support (`readlink(a, Σ) = Σ.L(a)` on the success branch, or RL0's biconditionals) is already present in the ASN one display earlier; the revision only swaps the cited justification.

## Issue 3: The cross-reference to the worked example overstates what it instantiates
Reason: Internal fix — either rewording the parenthetical or extending the worked example with the two branched states uses only the ASN's own construction (the K.λ branching argument and the worked example's addresses); no external authority is needed to settle what the example does or should verify.

## Issue 4: Forward-deferral and deduplication meta-prose around the structural screen
Reason: Internal fix — this is purely editorial deletion of document-organization commentary; the substantive screen content (conjuncts, necessity citations, `Σ₀` witness) is already present and unchanged.
