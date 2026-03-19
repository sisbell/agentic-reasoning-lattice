# Revision Categorization — ASN-0034 review-13

**Date:** 2026-03-14 00:11

## Issue 1: Off-by-one in TA5/T4 preservation analysis
Category: INTERNAL
Reason: Arithmetic counting error within the ASN's own analysis. Starting from zeros=0, three inc(·,2) steps yield three separators — the fix is changing "two" to "three," derivable from the ASN's own definitions.

## Issue 2: TA7a stated only for single-component ordinals
Category: INTERNAL
Reason: The ASN's own constructive definition of ⊕ already proves the generalization — components before the action point are copied unchanged. The ASN also already defines multi-component element fields (`E₁. ... .Eδ` with `δ ≥ 1`) and uses them in the worked example (`[1, 3]`). Generalizing TA7a follows directly from existing content.

## Issue 3: Result length of ⊕ used without statement
Category: INTERNAL
Reason: The formula `p = max(k-1, 0) + (n - k + 1)` simplifies to `n = #w` by elementary algebra on the ASN's own constructive definition. The fix is stating this as a remark and citing it where used.

## Issue 4: T9 status inconsistency
Category: INTERNAL
Reason: The body text already labels T9 as `[lemma]` and derives it from T10a + TA5(a). The table entry "introduced" contradicts the body. Fix is a label change within the ASN.
