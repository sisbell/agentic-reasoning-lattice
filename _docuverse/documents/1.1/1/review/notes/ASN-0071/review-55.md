# Review of ASN-0071

This ASN is mathematically sound. PC, PC-RANGE, and the F-* family are correctly derived: the prefix-confinement closure (componentwise fact + well-ordering), the cross-depth case split at component `#u` (T1 case (i)/(ii)), F-CONTENT's store-disjointness routing, and the finiteness bound all hold under scrutiny. The worked scenario is consistent. The findings below are accretion, consistent with the `review-mode.anti-bloat` classifier — no correctness defect.

## REVISE

### Issue 1: Nomenclature-justification prose in F-CONTENT
**ASN-0071, *The operation* (F-CONTENT)**: "A document is returned because it shares *byte content*, never because it shares a *link* address. This is what justifies calling the operation content-transclusion discovery."
**Problem**: The first sentence states what the operation does (legitimate). The second justifies the operation's *name* — meta-prose that does not advance the claim `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ⊆ dom(Σ.C)`.
**Required**: Drop the nomenclature-justification sentence; keep the operational statement.

### Issue 2: "Three depth regimes" paragraph restates PC-RANGE
**ASN-0071, *Resolution*** (paragraph beginning "Three depth regimes follow"): the `#u = m_C` and `#u < m_C` regimes narrate the PC-RANGE formula already stated immediately above and then demonstrated concretely in the worked scenario (which itself tags "the width-1 instance of PC-RANGE"). The `#u > m_C` "dual boundary" regime — `iaddrs_one(d_s, σ)(Σ) = ∅` — is a genuine derived guarantee, but it floats in prose with no claim carrier and is never demonstrated.
**Problem**: Narrative restatement of a labeled formula (essay in a structural slot); the one new consequence (`#u > m_C ⟹ ∅`) is asserted without a claim label.
**Required**: Either elevate the `#u > m_C` empty-resolution result to a claim (it is the dual boundary of F-FILT and worth stating precisely), or trim the regime narration to the single line linking PC-RANGE's `r_{#u}` to S8-depth's `m_C`. Do not keep the prose-only version of both.

### Issue 3: Body-to-intro backward reference
**ASN-0071, *Resolution***: "...a shallow vspec reaches every deeper arrangement position beneath the named coarse coordinate — the coarse-coordinate reach the introduction foreshadowed."
**Problem**: The trailing clause is a pointer back to the introduction's Nelson framing; it advances no part of the PC-RANGE characterisation and couples the claim to motivational essay.
**Required**: Delete the trailing clause; the technical statement stands on its own.

## OUT_OF_SCOPE

### Topic 1: Relationship between current-containment result and provenance relation R
**Why out of scope**: Correctly deferred to Open Questions. F-CUR's "present participle" semantics are fully specified for the single-state query; the `R`-versus-current-containment guarantee is new territory.

VERDICT: REVISE
