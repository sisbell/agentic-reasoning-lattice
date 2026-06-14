# Channel Assignment — ASN-0134 review-1

**Date:** 2026-06-13 17:34

## Issue 1: `𝔼` ranges over an undefined state combining two incompatible substrate stacks
Reason: Neither channel — the fix is a structural commitment to one already-defined foundation stack. Which stack is forced by what this note's dependents build on (the 0093→0086→0126→0128 line per its own dependency set), and the recast of A6/A5/H0 follows mechanically from the chosen stack's step vocabulary and state signature. This is project-internal layering, not Xanadu design intent or udanax-green evidence.

## Issue 2: M1(b) "no duplicated effect" is false for `idem = ⊥`, and commit-before-acknowledge does not deliver it
Reason: Neither channel — the correct scoping is read straight off the note's own cited foundations. ASN-0128 I5 and ASN-0086 R2 already establish that `idem = ⊥` produces distinct addresses with duplicated content by design, and A7 only orders the acknowledgment. The fix (scope (b) to single-op uniqueness + `idem = ⊤` collapse; delete the clause-3 dedup claim) is internal correction against existing dependencies.

## Issue 3: §2/A6 — "the precise and only sense of incomplete" omits the coupling-complete-but-transient case
Reason: Neither channel — the transient intermediate follows from ASN-0047's own `K.μ~ = K.μ⁻ + K.μ⁺` composite and the P0/P2/P4★ framing already in the dependency set; the fix is to retract the overclaim and add the shrink-then-grow case. (Also partly mooted by the Issue 1 stack choice: dropping `K.μ` removes the composite entirely.) Derivable from foundation content.

## Issue 4: G1 is vacuous in the note's single-total-order model
Reason: Neither channel — this is a pure formal-modeling decision. Restating G1 as the commutativity fact H1 already proves, or building a partial-order execution model and proving every per-home linearization preserves invariants, is entirely internal to the note's own apparatus. Nelson's per-home/owned-numbers intent is already established and cited; the defect is formal honesty, not intent.

## Issue 5: H2's proof skips the first-emission boundary
Reason: Neither channel — the `P_S(d, Σ_pre) = ∅` case is covered by ASN-0093's `FirstEmission`/`FirstEmissionFreshness`, already in the dependency list. Adding the boundary case (two concurrent first emissions both land at the determinate first slot) is derivable directly from that foundation.

## Issue 6: no concrete worked example
Reason: Neither channel — the scenario instantiates the note's own claims (H1 commutation, H2 collision, W4 fragmentation, M1(c)) over the ASN-0093 tumbler algebra, and the reviewer already specifies the concrete addresses. This is an internal construction from existing claims, not new design intent or implementation evidence.

## Issue 7: self-containedness — load-bearing references to non-foundation ASNs
Reason: Neither channel — this is a pure presentation/abstraction fix. Restating the W4/V0/V1 motivations as abstract layer requirements ("a layer requiring a contiguous content run," "a layer recognizing quiescence while writers remain active") and stripping the 0129/0130/0133 numbers and `Q0` label is derivable from the note itself.
