# Channel Assignment — ASN-0134 review-31

**Date:** 2026-06-14 07:30

## Issue 1: A1 carries §8's read-taxonomy and repeats the behavioral-read roster
Reason: Internal — the read-taxonomy, the `age`/`stale` access-count analysis (including the `findpreviousisagr` evidence already cited), and the roster all exist in the ASN; the fix only relocates the §8 machinery to V0/V2, leaves a pointer in A1, and enumerates the roster once. No new design-intent or implementation fact is required to move and deduplicate established content.

## Issue 2: The §4 both-miss duplicate and the I1a literal-vs-operative gap are derived three times
Reason: Internal — the both-miss derivation and the I1a literal-vs-operative distinction are already derived in full in §4 (M1(b) even says "derived there in full"). The fix keeps that one derivation and replaces the two restatements with citations plus the clause-8 delta, all from material already present.

## Issue 3: A6 defends its own structure rather than stating it
Reason: Internal — the load-bearing transfer enumeration (RP-a/B2/RP-b) is retained verbatim; the fix only trims the self-defending A6/W3 non-contradiction prose and the duplicate "no boundary-only class" claim, and the review even supplies the one-sentence replacement. No external fact is at stake.

## Issue 4: Overlapping summary layers and verbatim refrains
Reason: Internal — this is consolidation of four summary layers into one and collapsing two verbatim refrains ("role-dual…not scope-dual"; "cross-home by H1, same-home by clause 2's spacing") to a single canonical statement. Purely editorial; no design-intent or implementation question.

## Issue 5: This note's M1 collides with ASN-0093's M1
Reason: Internal — the label collision and the identities of both `M1`s (ASN-0093 ArrangementMonotonicity vs. this note's SafetyUnderMIC) are already established in the ASN; the fix is a mechanical rename of the local theorem applied consistently, needing nothing from either channel.
