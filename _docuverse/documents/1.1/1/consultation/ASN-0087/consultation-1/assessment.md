# Channel Assignment — ASN-0087 review-1

**Date:** 2026-05-26 11:45

## Issue 1: L1c invariant verification is hand-waved
Reason: The inc-chain construction is mechanical from ASN-0093's SubAllocatorAxiom.ChainDiscipline and the address scheme of ASN-0034/0043. All step labels and length monotonicity are derivable from foundation definitions already cited by the ASN.

## Issue 2: Missing S-invariant verifications in M-Inv
Reason: S8a, S8-depth, S8-fin, D-SEQ★, S8★ are foundation invariants from ASN-0036/0047; verification follows directly from K.μ⁺_L's positioning rule and the depth-2 link-subspace structure already documented.

## Issue 3: No concrete example
Reason: A worked scenario is an exposition exercise constructed from the ASN's own definitions and the LP12 evaluation already specified — no design intent or implementation evidence is needed.

## Issue 4: No weakest precondition analysis
Reason: wp(MAKELINK, discoverable_from) is mechanical given the effect (M-Effect) and the LP12 biconditional already cited; the computation is purely formal.

## Issue 5: v_ℓ construction not made explicit in Effect
Reason: The construction formula lives in K.μ⁺_L's foundation definition (ASN-0093/0047) and just needs to be restated at the operator-facing layer.

## Issue 6: Intermediate-state discoverability claim is imprecise
Reason: The predicate-domain correction is a logical fix — `discoverable_from` is undefined when `ℓ ∉ dom(L)`. The proper Σ_mid-vs-Σ' comparison and reflexive-vs-non-reflexive split follow from the definitions already in the ASN.

## Issue 7: MAKELINK's side effect on other links' discoverability not analyzed
Reason: The change to `ran(M(d))` by adding `ℓ` is captured by M-Effect; the consequence for prior links with endsets covering `ℓ` follows directly from LP12, which the ASN already cites.

## Issue 8: Reflexive endset case not addressed
Reason: L13 (ASN-0043) already permits link addresses as endset targets, so the foundation allows the case abstractly. The fix — either explicit treatment or scoping out — is derivable from the cited foundation and the LP12 projection function.

## Issue 9: Verification that K.μ⁺_L's first-arrangement guard is satisfied is incomplete
Reason: The S3★ + L14 derivation chain uses only foundation invariants already cited by the ASN (ASN-0036 for S3★, ASN-0043/0093 for L14). The missing step is mechanical.
