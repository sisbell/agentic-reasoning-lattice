# Review of ASN-0098

I checked every projection claim (LP2–LP21, LP-Sub, LP-Fin) against its proof and traced the operation coverage against the ASN-0047 transition vocabulary. The mathematics is sound and unusually complete: every transition kind (K.α, K.δ in all three cases, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ) is accounted for, the boundary cases (empty endset, empty arrangement, R = ∅, equality/interior/above/below in LP-Fin sub-case B) are handled explicitly, and the LP-Fin cross-document/cross-subspace exclusion argument is rigorous. My findings concern accreted meta-prose, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Redundant restatement closing the arrangement-fixing-transitions paragraph
**ASN-0098, "Frame Conditions" (Projection invariance under arrangement-fixing transitions)**: "Hence none of content allocation, link allocation, provenance recording, or node/account creation can displace any projection; in particular, creating a new link cannot retroactively affect the projection of any other link, and provenance bookkeeping displaces nothing."
**Problem**: The clause after "in particular" re-asserts in different words exactly what the preceding clause already states (link allocation and provenance recording displace nothing). It adds no case the general statement does not already cover — a reader has to recognize it as a restatement and skip it.
**Required**: Delete the "in particular…" tail; the general sentence is complete.

### Issue 2: Anthropomorphizing essay content in LP18's structural slot
**ASN-0098, LP18 (Resurrection), closing prose**: "The link does not 'know' that the content has been removed and re-introduced; it does not need to."
**Problem**: This is essay content occupying a claim's slot. The substantive point — stored state is permanent (L12, LP3★) while projection is recomputed live — is already made in the preceding sentence. The "does not know / does not need to" sentence advances no reasoning.
**Required**: Remove the sentence; the L12/LP3★ observation carries the architectural point.

### Issue 3: LP2 second sentence restates the first
**ASN-0098, LP2 (SlotInvariance), explanatory prose**: "In particular, the slot-position assignment fixed at link creation — from-set at slot 1, to-set at slot 2, type-set at slot 3, and any additional slots — is structurally preserved. No editing operation can swap, relabel, or alter which slot carries which endset."
**Problem**: The second sentence ("No editing operation can swap, relabel, or alter…") is the negative paraphrase of the first ("the slot-position assignment … is structurally preserved"). Two sentences saying the same thing.
**Required**: Keep one. The first sentence (which names the slot semantics) is the more informative; drop the second.

## OUT_OF_SCOPE

### Topic 1: Reverse-discovery, V-order/I-order correspondence, link-to-link induced discovery
**Why out of scope**: These are correctly deferred to the Open Questions section as future ASNs. They are new territory (reverse-discovery primitive invariants, V-order reflection under K.μ~), not gaps in this ASN's projection-displacement scope.

META: not triggered — the ASN defines a derived state quantity (projection) and proves abstractly how it displaces under each operation, which is squarely state-and-operation territory, not implementation mechanics.

VERDICT: REVISE
