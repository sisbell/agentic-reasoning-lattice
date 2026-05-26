# Channel Assignment — ASN-0098 review-14

**Date:** 2026-05-26 01:08

## Issue 1: Weakest precondition analysis missing for a non-trivial postcondition
Reason: The fix is derivable from the ASN alone. The review explicitly identifies the building blocks (LP10's exact-difference formula and LP12's discoverability biconditional) and the target postcondition (discoverability preservation under K.μ⁻); the synthesis is a proof-engineering exercise internal to the ASN.

## Issue 2: Case numbering ambiguity in the achievability section
Reason: Pure editorial wording fix. Either add consistent numerical labels to all four cases or drop the partial numbering on descendant/ancestor — no design or implementation question is involved.

## Issue 3: "Structural form #ℓ = #s alone" understates the canonical condition
Reason: The fix is derivable from the ASN's own definitions. The ASN already defines canonical as `ℓ = δ(n, #s)` (the conjunction of `#ℓ = #s` and ordinal-displacement form); the review asks only that the prose accurately reflect this existing definition and distinguish the two grounds (infinite-F-intersection vs. definitional canonical-form requirement) already established in the surrounding paragraphs.
