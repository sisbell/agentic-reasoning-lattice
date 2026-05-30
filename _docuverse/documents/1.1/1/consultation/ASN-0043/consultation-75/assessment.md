# Channel Assignment — ASN-0043 review-75

**Date:** 2026-05-30 08:44

## Issue 1: "extending Σ" is used in two existential claims but never defined
Reason: The proofs already fix `Σ'.C = Σ.C` and `Σ'.M = Σ.M`; the fix is to lift that into an explicit state-extension definition (domains non-decreasing, agreement on shared domain) and cite it from L9/L11b. Fully derivable from the ASN's own existing proof content.

## Issue 2: The scope-lift caveat is deferred to from four sites and inventoried in Open Questions
Reason: Pure structural cleanup — keep the bare scoped fact at each site, delete the pointer prose and the citer inventory. No design intent or implementation evidence needed.

## Issue 3: L1c enumerates its downstream consumers in the contract slot
Reason: Editorial deletion of a use-site inventory clause from L1c's body and table row; downstream consumers already cite L1c locally. Internal.

## Issue 4: Defensive "what the axiom is NOT" prose around L1c and the L9 freshness arguments
Reason: Removal of defensive "not a log / no appeal / regardless of frontier" clauses that defend phrasing rather than state content. Internal editorial.

## Issue 5: L9's Case-A/B discriminator reads as a relocated correction note
Reason: The two cases (`d'` has prior link allocations vs. not) are already present in the proof; the fix is to state them directly and drop the "the correct discriminator is … not …" meta-framing. Internal.

## Issue 6: L11a argues at length why a case split is unnecessary — a case the precondition already excludes
Reason: Reduce to the one-sentence instantiation (L1c discharges T10a-conformance; GlobalUniqueness gives `a₁ ≠ a₂`) and delete the imagined-case-split rationale. Fully derivable from the existing L1c/GlobalUniqueness citation.

## Issue 7: The `.type` accessor introduces authorial-preference meta-prose
Reason: Keep the synonym definition, drop the stylistic preference sentence. Pure editorial.

## Issue 8: L2's formal statement carries no formal content beyond the definition of `home`
Reason: `home(a)` is defined as a function of `a` alone, so the substantive claim (endsets do not enter the home computation, formalizable via two states agreeing on `a` but differing in `Σ.L(a)`'s endsets) is derivable directly from that definition. The design principle it expresses is already quoted from Nelson in the ASN.
