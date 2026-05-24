# Channel Assignment — ASN-0094 review-35

**Date:** 2026-05-23 19:31

## Issue 1: NAT-card and NAT-sub cited as foundation but not in provided foundation vocabulary
Reason: This is a foundation-vocabulary consistency question — either NAT-card/NAT-sub exist in ASN-0034 (check the source) or they need inline derivation from the available NAT axioms (NAT-wellorder, NAT-closure, NAT-discrete). Neither design intent nor implementation evidence informs the choice; it's an internal foundation-extraction question.

## Issue 2: Cross-ASN references to non-foundation ASNs (ASN-0036, ASN-0093)
Reason: This is a structural question about whether ASN-0036/0093 belong to the foundation set or whether the holdout references (SharedDepthOneAllocator, AllocatorTreeDepth) should be rewritten through the scaffolding interface. The ASN already demonstrates the scaffolding pattern works for most uses; the fix is internal reorganization.

## Issue 3: SharedDepthOneAllocator is introduced but never consumed
Reason: A lemma with no downstream consumer is either dead weight or has a missing citation. This is purely an internal consistency question about the ASN's own structure — either find/add the consumption site or remove the lemma.

## Issue 4: Sub-case II.A's home(a) derivation is one sentence covering two distinct cases
Reason: The unpacking requires TA5(c) (in foundation ASN-0034) plus the scaffolding's chain enumeration property (already cited elsewhere in the ASN). All inputs are already available; the fix is to write out the argument explicitly.

## Issue 5: AllocatedAddressAntichain "Element-level character of A^Σ" reasoning leans on a layer-commitment that conditions the lemma
Reason: The conditioning is already documented in the scaffolding's *Layer-commitment status* paragraph within this ASN. The fix is to surface the qualifier at the lemma statement — purely internal rewording from existing material.

## Issue 6: ShapeWellFormedness "Behavior at c_F = 0|1" walkthrough has subtle reading hazard
Reason: This is a clarity rewording — the logic is correct, only the framing direction needs adjustment. No external input needed.

## Issue 7: NullifyActiveSubsetCompatibility Case A's "by ASN-0086's substrate-level argument under R0a and R6a" is too brief
Reason: R0a (FlatLinkDomain) and R6a (RetractionStability) are both ASN-0086 foundation primitives already available. The fix is to unpack the discharge of (i) and (ii) at Σ' with the same explicitness as Case B — internal proof expansion from foundation citations.
