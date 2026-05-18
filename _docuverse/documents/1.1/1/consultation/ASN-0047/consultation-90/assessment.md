# Channel Assignment — ASN-0047 review-90

**Date:** 2026-05-17 20:58

## Issue 1: Path 2 freshness discharge undermines S4's universal claim
Reason: The fix is a framing decision internal to the ASN — either elevate single-event sequential semantics to a meta-axiom and remove the Open Question, or qualify ExtendedReachableStateInvariants explicitly with the deferred-discipline caveat. Neither requires external evidence.

## Issue 2: L1c chain construction silently depends on s_L = s_C + 1
Reason: The dependency on `s_L = s_C + 1` is a property of SubspaceConventionAxiom and tumbler-algebra inc-step semantics, both already present in the ASN. The fix — either making the convention dependency explicit or constructing an alternative chain — is derivable from existing machinery.

## Issue 3: SubAllocatorAxiom "namespace property" attribution conflates two distinct freshness sources
Reason: The fix is to correctly attribute freshness to the right axiom clauses (FirstEmission vs T10a GlobalUniqueness) — entirely an internal correctness-of-citation question. No external evidence is required.

## Issue 4: S8 for link subspace is claimed via D-SEQ★ but D-SEQ★ does not give correspondence runs
Reason: Establishing or disclaiming S8-style correspondence-run decomposition for the link subspace is a technical exercise over the ASN's own K.λ + K.μ⁺_L allocation pattern — derivable from the per-state shape D-SEQ★ already supplies.

## Issue 5: Empty F/G "type-only marker" admitted beyond consultation evidence
Reason: The ASN explicitly admits a design case the consultation did not address. Both channels are needed to either restrict L3 or substantiate the extension — Nelson to confirm design intent, Gregory to clarify whether implementation acceptance reflects intent or oversight.
Nelson question: Did the Xanadu design explicitly consider links with both F and G empty (referencing only a type via Θ), and if so, was such a "type-only marker" link intended, excluded, or left unspecified?
Gregory question: Does udanax-green ever actually allocate a link with both F and G empty (only Θ populated), or is the absence of a runtime guard in `acceptablevsa`/`docreatelink` simply unreachable in practice?

## Issue 6: Forward reference to undefined `endpoints(·)` accessor
Reason: Determining whether ASN-0043's L4 actually defines an `endpoints(·)` accessor is a check against another ASN already in the foundation stack — no external evidence needed.

## Issue 7: Structural sufficiency boundary is informally bounded
Reason: The fix the review demands — defining precisely what design enumeration the elementary set covers, by enumerating admissible state-change modes per component — is achievable from this ASN's own state model (C, L, E, M, R) and their admissible directions of change. Internal.

## Issue 8: K.α attributed to ASN-0036 in Properties Introduced table
Reason: This is a factual question about what ASN-0036 actually defines. Resolvable by inspecting ASN-0036's text.

## Issue 9: Redundant deferred-to-version-contract notes
Reason: Pure prose consolidation across three sites within this ASN. Internal.

## Issue 10: "Frame extension (existing transitions)" paragraph duplicates per-transition frame content
Reason: Pure prose cleanup — removing or shortening a meta-paragraph that restates what per-transition definitions already say. Internal.
