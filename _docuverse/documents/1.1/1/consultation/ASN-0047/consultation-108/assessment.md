# Channel Assignment — ASN-0047 review-108

**Date:** 2026-05-18 09:32

## Issue 1: K.δ k = 1 discharge fails for versions of versions
Reason: The fix is structurally forced by T10a.6 (DomainDisjointness) and TA5's increment rules — once t was emitted by A_v(t'), the parent-allocator for A_v(t) must be A_v(t'), not A_doc(parent(t)). The case-split and nesting are derivable from the ASN's existing T10a discipline; no external evidence is needed to determine the shape of the fix.

## Issue 2: ValidComposite★ clause (1) inline existence condition is imprecise
Reason: The Decomposition of K.μ~ section already states the correct necessary-and-sufficient condition `|dom_C(M(d))| ≥ 2`; the inline statement just needs to be tightened to match. Purely internal alignment between two sections of the ASN.

## Issue 3: K.μ~ subspace-preservation argument uses S3★(Σ') and S3★(Σ) without flagging dependency order
Reason: The required clarification — naming S3★(Σ) as the inductive hypothesis and noting that S3★(Σ') is independently established by the matrix's K.μ⁻ + K.μ⁺ argument — is fully derivable from the ExtendedReachableStateInvariants proof structure already in the ASN. Internal expository fix.

## Issue 4: NodeRegistryBootstrap references an unmodelled "node-allocation registry"
Reason: The ASN's own open question already takes the position that the registry is external to the docuverse layer; the fix is to revise the K.δ case (ii) k = 2 discharge for t = n₀ consistently with that position (option ii). This is a formal-modeling choice internal to the ASN and does not require new design intent or implementation evidence.

## Issue 5: D-SEQ★ base case for m = 2 is brief and the degenerate notation is handled parenthetically
Reason: Purely expository — restructuring the base case presentation to make the m = 2 form direct rather than deferred. Internal to the derivation's prose.

## Issue 6: Cross-document disjointness chain — Case A's length-bound discharge is implicit
Reason: The arithmetic `#p₁ = #e₁ + 2`, `#p₂ = #e₂ + 2`, and the chain to `#e₁ + 1 ≤ min(#p₁, #p₂)` follow directly from the prefix shape `[eᵢ.0.s]` and `e₁ ≺ e₂`. Internal derivation-detail fix.
