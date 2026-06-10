# Channel Assignment — ASN-0127 review-22

**Date:** 2026-06-10 11:24

## Issue 1: False slot enumeration in the cardinality-changing swing variant
Reason: Internal fix. The correct enumeration uses facts the illustration already establishes — `subtree(a_θ) ∩ {a_1} = ∅` is proven in the coverage-shorthand paragraph — so the sentence just needs to check both non-empty slots instead of erasing one; no design intent or implementation evidence is involved.

## Issue 2: Five informal ASN-0098 analogy invocations, zero formal bridge to `discoverable_from`
Reason: Internal fix. The required lemma is a formal derivation from F-IMG, F-V, and LP12 — all corpus-internal material in the ASN's dependency cone — and the review already sketches the one-line proof; neither Nelson's intent nor udanax-green behavior bears on it.

## Issue 3: Undischarged standing conditions — `d ∈ dom(Σ'.M)` persistence and image finiteness
Reason: Internal fix. Both missing discharges are citations of existing corpus claims the review names exactly (M1, ASN-0047 for post-state definedness; S8-fin, ASN-0036 for image finiteness), following the precedent LP4 already models.

## Issue 4: The K.λ-residual narrative is told three times, and names an induction that does not exist
Reason: Internal fix. This is prose deduplication plus correcting the role description to match what the note actually proves (single-step F-LAMBDA with LP13/per-step chaining, no induction through F-CIL-perlink); everything needed is in the ASN's own derivations.

## Issue 5: Residual meta-prose and precision slips
Reason: Internal fix. All sites are editorial — a type slip, a citation pointed at the right claim (F-IMG-CONTR), deletion of meta-sentences, and restating F-INERT's closure step as the two-line path-length induction the note's own per-step equality already supports.
