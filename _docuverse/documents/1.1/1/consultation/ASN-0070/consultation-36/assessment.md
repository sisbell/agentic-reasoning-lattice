# Channel Assignment — ASN-0070 review-36

**Date:** 2026-06-02 23:30

## Issue 1: Worked example states `coverage` as an exact finite set, contradicting its own definition and Configuration 1
Reason: Internal. The fix applies the note's own definitions (`coverage(e) = ⋃⟦σ⟧`, T12 half-open interval, L13/PrefixSpanCoverage) to restate Configs 2/3/5 as subtree/interval coverage with a depth-`m_a` slice — exactly the treatment Config 1 already models. No design intent or implementation evidence is needed.

## Issue 2: Open Question 4 poses a question the body has already decided
Reason: Internal. The Canonical Form section already states the decision (postcondition not committed to canonical form; callers canonicalise downstream), so removing or reframing the redundant open question is purely an editorial reconciliation within the note.
