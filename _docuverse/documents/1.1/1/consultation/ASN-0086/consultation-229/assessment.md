# Channel Assignment — ASN-0086 review-229

**Date:** 2026-06-01 19:30

## Issue 1: CoverageEqualityDecidable dismisses empty gaps without establishing indicator/set agreement
Reason: Pure proof repair internal to the ASN — the fix rests entirely on the note's own machinery (T1/T2 comparisons, TumblerAdd, span coverage, the empty-gap fact about tumbler space). Neither design intent nor implementation evidence bears on whether the endpoint-based indicator coincides with set-membership.

## Issue 2: "Scope — retractors are standard-triple links only" re-derives an exclusion already forced by the carrier
Reason: Editorial cut — the `|Σ.L(a)| = 3` conjunct in *Definition — TypedRelation* already excludes higher-arity links, so the redundant paragraph is removable using only the ASN's own definitions.

## Issue 3: The self-nullification boundary in WP Case 2 is stated three times before the worked example
Reason: Editorial deduplication — collapsing the redundant prose restatements depends only on what the derivation and worked Step 4 already prove within the note. No external channel needed.
