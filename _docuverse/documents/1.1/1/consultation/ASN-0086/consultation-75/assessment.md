# Channel Assignment — ASN-0086 review-75

**Date:** 2026-05-19 17:43

## Issue 1: R6c-Corollary's "→*-subsequence" framing isn't a valid →*-chain
Reason: Pure proof-structure fix. The reviewer has supplied the corrected approach (direct induction over the ↦*-chain splitting on step type), and every ingredient (R6a, R3, LinkStoreInvarianceUnderArrangement, Definition of A_K) is already established within the ASN.

## Issue 2: R5's claim is silent about the emission precondition
Reason: Precondition clarification fully derivable from L1a (already cited): `a ∈ A_rel^Σ` entails `home(a) ∈ dom(Σ.M)`, hence `dom(Σ.M) ≠ ∅`. The reviewer supplies the exact one-line fix.

## Issue 3: ChainMembershipForOrigin uniqueness for re-enumeration in R7a's discharge (4)(iii)
Reason: Citation addition. ChainEnumerationInjectivity is an ASN-0093 lemma already invoked elsewhere in R7a; the fix only makes its use at (4)(iii) explicit.

## Issue 4: Worked Sketch silently assumes content addresses were K.α-emitted
Reason: Grounding sentence using ASN-0093 SubAllocatorAxiom.FirstEmission and SiblingRecurrence, both already cited in the ASN. The reviewer supplies the exact text.

## Issue 5: "Properties Introduced" table conflates definitions with disciplines
Reason: Editorial labeling fix internal to the ASN — introduce COMMITMENT/DISCIPLINE label for layer-level conventions. The substrate/layer boundary is already articulated in the ASN's prose; only the table labeling needs to reflect it.

## Issue 6: R0a-Cor2's "equivalent route" remark dangles
Reason: Editorial choice — either develop the ChainPrefixExtension parallel derivation or remove the mention. The TA5(c) + TA5-SigValid route already in the proof is self-sufficient per the reviewer's note.
