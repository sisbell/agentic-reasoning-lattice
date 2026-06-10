# Channel Assignment — ASN-0126 review-97

**Date:** 2026-06-10 08:27

## Issue 1: The from-fill `r` silently converts ASN-0086's *unattributed* retraction into a whole-document attribution
Reason: The acknowledgment facts (unattributed retraction becomes inexpressible; `r` covers the whole document subtree and is observable via `Observe_R`) are derivable from ASN-0086's RetractionDirectionality convention and ASN-0043's PrefixSpanCoverage. But choosing among the reviewer's resolutions — justifying whole-document attribution versus flagging `r` as a deferred placeholder — turns on whether unattributed retraction is a load-bearing design feature, which is design intent.
Nelson question: Was retraction designed as an unattributed (anonymous) act, as ASN-0086's empty-from Nullify allows, or is it meant to carry attribution to the agent performing it — and if attributed, is attributing it to the whole retracting document acceptable?

## Issue 2: Design-rationale reassurance in Shape-conformance (anti-bloat)
Reason: Purely editorial deletion derivable from the ASN alone — drop the "deliberately combines… the two are independent" framing and the non-mutual-unsatisfiability reassurance, keep the substantive selection clause and the two examples. The retained examples already establish span-count/coverage independence; no later proof cites the reassurance.

## Issue 3: The `|F| ≥ 2` exclusion is treated asymmetrically, and OQ6 mislabels it as "arity"
Reason: Both parts are internal. The note already establishes that a single span covers only a contiguous range (Single-source, via ASN-0043's PrefixSpanCoverage), so the `|F| ≥ 2` disjoint-source exclusion and its deferral to OQ6 follow from existing content; the OQ6 wording fix is a terminology correction (from-span-count `|F|` vs. arity `N`) the note already distinguishes throughout.
