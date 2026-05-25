# Channel Assignment — ASN-0068 review-3

**Date:** 2026-05-25 00:11

## Issue 1: CV-IN's "equivalently" claim conflates actionPoint ≥ 2 with ordinal displacement at depth m
Reason: The fix requires choosing between two semantically distinct restriction regimes (bounded contiguous ordinal-displacement spans vs. broader in-subspace regions). The choice turns on design intent for what "restriction" means and what udanax-green's implementation actually accepts — Nelson informs the former, Gregory the latter.
Nelson question: Was the COMPAREVERSIONS restricting span-set intended to confine comparison to a bounded contiguous V-range (an ordinal-displacement window) within a subspace, or to any subspace-confined region permitted by level-uniformity and in-subspace containment?
Gregory question: Does udanax-green's COMPAREVERSIONS implementation constrain restriction span widths to ordinal displacements at the document's V-position depth (width = δ(n, m)), or does it accept widths with actionPoint ≥ 2 more generally?
