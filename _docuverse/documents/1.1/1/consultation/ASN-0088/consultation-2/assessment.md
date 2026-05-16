# Revision Categorization — ASN-0079 review-2

**Date:** 2026-03-23 01:16

## Issue 1: Worked example span excludes a₃ (off-by-one)
Category: INTERNAL
Reason: The span algebra definitions (half-open denotation, reach, displacement) are fully established in the ASN and its dependencies. The fix is mechanical: adjust the width to δ(3, m) and propagate through the projection verification.

## Issue 2: Empty-endset boundary case unverified
Category: INTERNAL
Reason: The behavior follows directly from existing definitions — coverage(∅) = ∅ and ∅ ∩ P = ∅ — all within the ASN's own formalism. Adding the explicit statement requires no external evidence.

## Issue 3: F1a states unnecessary disjointness precondition
Category: INTERNAL
Reason: The proof uses standard set distribution and "non-empty union iff some component non-empty," neither of which requires disjointness. The fix is removing one word from the precondition.

## Issue 4: F19 scaling requirement internally inconsistent
Category: BOTH
Reason: Nelson's phrase "does not in principle impede" could mean O(1) independence or merely sublinear growth — this is a design-intent question. The spanfilade's actual complexity characteristics determine which formalization the implementation supports.
Nelson question: When you wrote that the quantity of non-satisfying links must not "in principle impede" search, did you mean cost must be strictly independent of total link count, or that it must not grow linearly (admitting logarithmic overhead from tree-based indexing)?
Gregory question: What is the actual complexity of a spanfilade lookup in udanax-green as a function of total link count — is it O(log n) from tree traversal, O(1) from hashing, or something else?
