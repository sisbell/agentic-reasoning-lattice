# Revision Categorization — ASN-0063 review-6

**Date:** 2026-03-21 19:42



## Issue 1: K.μ~ fixedness argument has a cardinality gap
Category: INTERNAL
Reason: The fix is a missing proof step (cardinality/injection argument) that follows entirely from definitions already present in the ASN — the bijection π, the amended K.μ⁺ precondition, and S3★. No external evidence needed.

## Issue 2: CL1 proof claims "exactly one" but ASN later notes overlapping I-spans
Category: INTERNAL
Reason: The fix is changing "exactly one" to "at least one" — a wording correction derivable from the ASN's own definitions (S5 sharing, B1/B2 block coverage) and its own later observation about overlapping spans.

## Issue 3: Orphan links section claims K.μ⁻ achieves link withdrawal without noting D-CTG constraint
Category: NELSON
Reason: The formal constraint (D-CTG prevents arbitrary interior removal) is clear from existing definitions. But whether link withdrawal should be supported and what mechanism Nelson intended — complete removal, boundary-only removal, or a separate withdrawal operation — is a design intent question.
Nelson question: When a document owner withdraws a link, did you envision the link being removed from the document's arrangement (requiring a mechanism to maintain contiguous ordering), or did you intend a different withdrawal mechanism such as marking the link as inactive while preserving its arrangement position?

## Issue 4: CL4 overclaims "any one of which would suffice" for five principles
Category: INTERNAL
Reason: The fix is restating the rhetorical claim to distinguish the two formal guarantees (S0 and K.λ frame) from the three design-philosophy observations. All information needed is already in the ASN.

## Issue 5: CL11 claims "all foundation invariants" but omits P3 and P4a
Category: INTERNAL
Reason: P3 and P4a are trivially preserved (R unchanged, C unchanged, M extended monotonically) — the one-sentence justifications follow directly from the ASN's own frame conditions and the definitions in ASN-0047.
