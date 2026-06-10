# Channel Assignment — ASN-0127 review-21

**Date:** 2026-06-10 10:59

## Issue 1: The worked illustration's `a_θ` incomparability premise is asserted, not discharged
Reason: Internal — the review already supplies the discharge path (pin `a_θ = [d, 0, s_L, 1]`, then T7 distinctness plus the Prefix length lemma from ASN-0034), all of which is tumbler arithmetic over foundations the note already cites. No design intent or implementation evidence bears on a prefix-incomparability proof.

## Issue 2: F-INERT's quantification domain is ambiguous, and one reading falsifies the claim
Reason: Internal — a pure notational fix (parenthesize the set expression or reuse F-PRES's explicit enumeration, both already present in the note). No external knowledge needed.

## Issue 3: Dangling label "(Q3)"
Reason: Internal — editorial repair (number the open questions or replace the label with a textual pointer). Nothing to consult.

## Issue 4: The two-keystone split is narrated three times, twice with deferrals to the same downstream site
Reason: Internal — a deduplication/restructuring edit; the substantive content (F-CIL's hypothesis fails on K.λ paths, LP13 grounds the existence lane) is already correctly stated in E-INV's derivation. The fix is choosing where to say it once, not what is true.

## Issue 5: The "unrestricted union law" rationale appears three times; F-LAMBDA pre-narrates the discovery section
Reason: Internal — same accretion pattern as Issue 4: the content-sharing rationale and the D-NONMONO forward-summaries are correct but duplicated, and the review names exactly which copies to keep and cut. Pure consolidation.

## Issue 6: Dead slot-constraint apparatus, and an open question hanging off undefined machinery
Reason: Choosing between deleting the `(i, J)` bullet and introducing the filtered query — and writing the recast open question either way — requires knowing what query form the trimmed treatment was mirroring; that is implementation evidence about the real link-retrieval operation's filter semantics. The proof mechanics themselves are internal, so only Gregory is needed.
Gregory question: What filter arguments does udanax-green's link-retrieval operation (find-links-from-to-three) take, and does matching require each *specified* specset (from/to/type) to intersect its corresponding endset slot — conjunctive per-slot matching, with unspecified slots unconstrained — rather than any single slot meeting any filter?

## Issue 7: D-NONMONO's K.μ~ clause embeds Phase-1 witnesses that belong with F-IMG-SWING
Reason: Internal — the witnesses are verified correct and the finding is placement only; moving them to F-IMG-SWING and leaving citations behind is a restructuring edit fully specified by the review.
