# Channel Assignment — ASN-0130 review-23

**Date:** 2026-06-13 04:33

## Issue 1: The endorsement-withdrawal point is restated near-verbatim across PR1 and PR3
Reason: Pure prose deduplication — the fix removes a restatement from PR3 and points it to PR1, the section that already owns the permanence-division reasoning. Both passages and the cross-reference target are present in the note; no design intent or implementation evidence is in question.

## Issue 2: Non-predicate rejection is explained at length in both PR5 and PR5a (0)
Reason: Internal deduplication — PR5a (0) is the definitional home of the non-predicate check and PR5's lint caveat need only cite it. The concept and both passages already live in the note; nothing about Nelson's intent or Gregory's code is at stake.

## Issue 3: certify_pd_stable's defining check (iii) has no decidability/termination argument
Reason: The decidability clause is assembled entirely from facts already present — PR2 gives termination, PR3a gives `expand(a) ∈ PL` (finite), and PD0's rules are treated as syntax-directed/spelling-level throughout (per dependency ASN-0129). The required clause is a restatement of these established facts, not a new claim needing external grounding.

## Issue 4: "What this note commits" bullets restate the PR bodies in full rather than pointing to them
Reason: Purely structural trimming — the commit bullets are condensed to terse guarantees with mechanism left to the PR bodies. This is an editing operation over content already in the note; no channel input is needed.
