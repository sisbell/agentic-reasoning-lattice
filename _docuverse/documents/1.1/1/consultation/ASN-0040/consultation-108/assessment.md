# Channel Assignment — ASN-0040 review-108

**Date:** 2026-05-29 04:50

## Issue 1: "Why the axiom is needed" prose preceding B-Seq
Reason: Pure editorial cut — removing motivating meta-prose and optionally relocating the cross-branch remark to B8. No design intent or implementation evidence is at stake; the content to keep already exists in the ASN.

## Issue 2: B-Seq Justification mixes grounding with restated scope
Reason: The implementation grounding is already stated in the ASN; the fix only condenses it to one clause and removes duplicated scope qualifications. This is deduplication of existing text, derivable from the ASN alone.

## Issue 3: B8 Case 1 explains an excluded case rather than dispatching it
Reason: WLOG-relabeling cleanup — truncating a sentence at "without loss of generality." Purely internal proof hygiene with no external dependency.

## Issue 4: B6 necessity does not address (iii) at d = 1
Reason: The needed sentence follows from the ASN's own T4 definition (T4 bounds zeros ≤ 3, so (iii) at d=1 reduces to a T4 consequence). Fully derivable from existing content.
