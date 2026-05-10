# Revision Categorization — ASN-0034 review-13

**Date:** 2026-03-19 18:00

## Issue 1: Off-by-one in TA5/T4 preservation analysis
Category: INTERNAL
Reason: The correct count (three separators from three `inc(·, 2)` steps: zeros 0→1→2→3) is derivable from the ASN's own analysis of TA5 and T4, which enumerates the steps explicitly. Pure arithmetic correction.

## Issue 2: TA7a stated only for single-component ordinals
Category: INTERNAL
Reason: The ASN's own T4 defines `δ ≥ 1` for element fields, and the constructive definition of ⊕ already shows components before the action point are copied unchanged. The generalization follows directly from existing definitions.

## Issue 3: Result length of ⊕ used without statement
Category: INTERNAL
Reason: The formula `p = max(k-1, 0) + (n - k + 1) = n` is already present in the constructive definition. The fix is extracting and naming a simplification that the ASN already contains, then citing it in the proofs that depend on it.

## Issue 4: T9 status inconsistency
Category: INTERNAL
Reason: The body text already labels T9 as `[lemma]` and derives it from T10a + TA5(a). The table entry just needs to match the body text — no external evidence required.
