# Channel Assignment — ASN-0111 review-2

**Date:** 2026-06-07 22:57

## Issue 1: Worked example mislabels coverage (intervals) as finite I-address sets
Reason: The fix is internal — it aligns the example's prose with the `coverage` definition the ASN already quotes, applying the half-open-interval/subtree semantics of spans (ASN-0034, cited) and the arrangement/discoverability distinction already developed in RL8. No design intent or implementation evidence is required to restate coverage as an interval set and separate it from the content-hosting I-addresses arranged within it.

## Issue 2: RL2's "three-way grouping" prose assumes arity 3, but the model and RL-ARITY admit N > 3
Reason: The formal model (L3: `N ≥ 3`) admits N>3, but deciding whether to generalize the prose (and what slots 4+ *mean*) versus restrict to the standard triple turns on design intent — and constructing a faithful N>3 worked instance requires knowing whether such links actually arise. Nelson settles intended role of extra endsets; Gregory confirms whether the implementation ever produces them.
Nelson question: Does the design intend links to carry more than the standard from/to/type triple, and if so what role, if any, do endsets in slots beyond the third bear?
Gregory question: Does udanax-green ever construct or store link values with more than three endsets, and does it assign any meaning to slots past the third?
