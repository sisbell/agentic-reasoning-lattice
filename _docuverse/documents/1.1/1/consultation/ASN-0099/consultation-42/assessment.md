# Channel Assignment — ASN-0099 review-42

**Date:** 2026-05-27 07:58

## Issue 1: F5 lacks explicit derivation
Reason: The fix is derivable from F1 itself — the required derivation just makes explicit which sub-expressions of F1's RHS the predicate consults. No design intent or implementation evidence needed.

## Issue 2: F4 forward-references findlinks_filtered
Reason: Purely structural fix — both `findlinks` and `findlinks_filtered` are defined within this ASN; the issue is ordering or adding a stub. No external consultation needed.

## Issue 3: F4 layered structure obscures the operational point
Reason: Editorial reorganization of material already present in the ASN. The layer taxonomy and the five witnesses are both internal; consolidating or relabeling them needs no outside input.

## Issue 4: F10a Case (ii) bookkeeping is compressed
Reason: The missing step (`d₂[#d₁] = d₁[#d₁] ≠ 0`) follows directly from ASN-0034's Prefix and T4, both already cited in F10a. The fix is internal expansion of a foundation-grounded derivation.

## Issue 5: Conformance pair variants stated only as conjunctions
Reason: Presentation choice between stating each variant as two containments or noting the conjunction explicitly. The content is fixed; only the format is at issue.
