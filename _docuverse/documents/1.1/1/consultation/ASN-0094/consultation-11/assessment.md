# Channel Assignment — ASN-0094 review-11

**Date:** 2026-05-19 23:14

## Issue 1: Subspace identifier identification asserted without formal derivation
Reason: The reviewer specifies the exact fix: add a parallel link-side scaffolding clause `E(a).1 = s_L` symmetric to the existing content-side assumption. This converts a bridge claim into an explicit framework commitment, derivable from the ASN's existing scaffolding structure.

## Issue 2: AllocatorTreeDepth references ASN-0093 by number
Reason: Pure editorial fix — reword to route the citation through ASN-0086's SubstrateConformingLayer (which is foundation) or remove the definition. The substitute reference path is already established within the ASN.

## Issue 3: ZeroCountDepth and AllocatorTreeDepth are unused
Reason: Structural cleanup decision internal to the ASN: either delete vestigial definitions or invoke them at the SingleHomeCoverageDiscipline chain-index reasoning. No external evidence or intent needed to make this call.

## Issue 4: "Multiset-valued" wording is imprecise
Reason: Pure phrasing fix — the walkthrough already contains the correct formulation ("set-valued; may contain slot-pair-identical tuples"). Just align the catalog row to the walkthrough's wording.

## Issue 5: C-fin not in content-side scaffolding
Reason: Add a sixth content-side scaffolding clause for content-store finiteness, symmetric to ASN-0043's L-fin, then cite at the two finiteness invocation sites. Purely internal symmetric extension of the existing scaffolding enumeration.

## Issue 6: Sh-conf wp_eff derivation telescopes the NoCraftedSpanReachesD discharge
Reason: The expansion uses only properties already cited from the verified foundations (ASN-0086's R0a/ChainUniformLength/CrossDocDisjointness/FreshEmissionAddress, ASN-0034's T10a.7, the substrate-conforming layer's chain enumeration). The fix is to spell out the home/cross-home case split within the framework's own mathematical content.
