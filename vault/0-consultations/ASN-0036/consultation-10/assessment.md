# Revision Categorization — ASN-0036 review-10

**Date:** 2026-03-14 18:35

## Issue 1: S8 stated for all of dom(M(d)) but proven only for text subspace
Category: INTERNAL
Reason: The ASN already acknowledges the link-subspace gap (remark after S8a) and the fix is aligning the scope of S8's claim with what's actually proven — either restricting the quantifier or adding an explicit premise. No external evidence needed.

## Issue 2: S8 correspondence run depth uniformity cites T9 but needs T10a
Category: INTERNAL
Reason: T10a (AllocatorDiscipline) is already defined in ASN-0034 and available as a dependency. The fix is correcting the citation chain from T9 to T10a and updating the dependency list — a matter of internal cross-reference accuracy.

## Issue 3: S8-depth lacks formal statement
Category: INTERNAL
Reason: The prose content and design justification for S8-depth are already present in the ASN, including Gregory's evidence about the `s.x` form. The fix is encoding the existing prose as a quantified statement, following the pattern of every other named property.
