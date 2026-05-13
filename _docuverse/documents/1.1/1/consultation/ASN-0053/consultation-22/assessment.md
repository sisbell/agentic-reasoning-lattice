# Channel Assignment — ASN-0053 review-22

**Date:** 2026-05-13 14:31

## Issue 1: S8's sort step is not "well-defined" by T1 alone
Reason: The fix is a proof-rigor clarification — either acknowledging tie-breaking irrelevance with output uniqueness inherited from S9, or extending to a total order. Both options are derivable from the ASN's existing definitions and S9.

## Issue 2: S9 Case 1 collapses an N2 + N1 chain into a single citation
Reason: Pure proof hygiene — Case 2 already demonstrates the correct N2 + N1 chaining pattern within the same proof. The fix mechanically mirrors Case 2's rigor in Case 1 and the j > n sub-case.

## Issue 3: Span-set union Σ₁ ∪ Σ₂ used in S10 without definition
Reason: Notational cleanup derivable from existing material — the ASN already defines span-sets as sequences with denotational equivalence (≡), and Nelson's quoted position ("what matters is which bytes are designated, not the order") is already in-text. Defining ∪ as either concatenation or as the span-set with the corresponding denotation is internal.
