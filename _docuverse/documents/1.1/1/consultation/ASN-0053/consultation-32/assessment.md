# Channel Assignment — ASN-0053 review-32

**Date:** 2026-05-28 19:48

## Issue 1: Self-citation by the ASN's own number
Reason: Pure citation-convention fix — SC, S11, S11a–c are all defined in this document, so dropping the "ASN-0053" tag requires no external input. Internal.

## Issue 2: Repeated boilerplate well-formedness verification (anti-bloat)
Reason: Hoisting a single WF lemma from reasoning already proven seven times in the ASN is an internal restructuring; the content and preconditions are entirely present. Internal.

## Issue 3: S11 asserts the containment boundary characterization without derivation
Reason: The missing derivation (reach(β) ≤ reach(α) from ⟦β⟧ ⊆ ⟦α⟧ via non-emptiness) uses only T1 and span non-emptiness (S2), both already established in the ASN — and S11d gives the mirror argument. Internal.

## Issue 4: Implementation-mechanic citations inside abstract claims
Reason: The existing citations (Q10, Q14, Q15) are already Gregory-sourced; demoting them to brief evidentiary notes or removing them is an editorial presentation choice that needs no new implementation evidence. Internal.
