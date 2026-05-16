# Channel Assignment — ASN-0051 review-57

**Date:** 2026-05-16 08:23

## Issue 1: SV10 prose conflates "resolution" with "projection"
Reason: The terminology distinction is already drawn explicitly in the ASN's Definitions section (resolution = locate, projection = π). The fix is a consistency edit using terms the ASN itself defines — no external evidence or design intent required.

## Issue 2: SV11 attainment witnesses do not cover p ≥ 3
Reason: The mathematical machinery needed is already in the ASN — the suffix-coalescence argument from the disjoint-extent non-attainment case can be applied per-pair, and the existing p=2 multi-block overlap witness construction generalises to p=3 by adding a third overlapping block under S5. The fix is derivable from the ASN's own structural reasoning.

## Issue 3: SV11 fragment-count analysis omits one strictness mechanism in the worked example
Reason: Purely editorial clarification of what the existing analysis says — the 4 → 2 gap is entirely mechanism (b) within-block coalescence, and the ASN already establishes that non-injective sharing inflates only the width sum. The fix restates content the ASN already contains.

## Issue 4: Sub-claim (i) proof obligation about t_j defined
Reason: Proof-presentation restructuring to make a load-bearing inference (proper-prefix → T1(ii) → t < s) explicit. The substance is already present in the ASN; only the ordering of clauses needs adjustment.
