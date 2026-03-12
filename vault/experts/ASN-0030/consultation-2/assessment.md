# Revision Categorization — ASN-0030 review-2

**Date:** 2026-03-12 00:07

## Issue 1: INSERT and PUBLISH missing from operations analysis
Category: INTERNAL
Reason: INSERT's properties (+_ext, P9-new) and PUBLISH's frame condition (D10a) are already established in ASN-0026 and ASN-0029. The analysis follows the same pattern used for DELETE, COPY, etc.

## Issue 2: A5 not labeled as specification requirement
Category: INTERNAL
Reason: This is an epistemic labeling fix — matching A5's status to A4a's treatment. The determination that ASN-0026 doesn't establish the specific V-space postcondition is derivable from reading the foundations already cited.

## Issue 3: A4a uses set equality instead of permutation
Category: INTERNAL
Reason: Purely a formal precision issue — strengthening a mathematical predicate from set equality to permutation/multiset equality. The fix is self-contained notation.

## Issue 4: A7 wp derivation contradicts A8
Category: INTERNAL
Reason: The formal statement A7 is already correctly scoped; the prose derivation overclaims. The fix is splitting the argument into two cases (V-space-derived vs ghost endsets) using distinctions already present in the ASN.

## Issue 5: `endset(L)` used without definition
Category: INTERNAL
Reason: The ASN already describes endsets as "sets of I-address spans" and references T12 (SpanWellDefined). The fix is writing out the explicit set comprehension unfolding spans to individual addresses using machinery already cited.

## Issue 6: Transition (f) is composite, not single-step
Category: INTERNAL
Reason: The fix is clarifying the semantics of the A3 transition table — whether it classifies single-operation transitions or reachable state-pairs. The INSERT+DELETE composition is already described in the ASN's own text.

## Issue 7: Ghost permanence claim lacks justification
Category: INTERNAL
Reason: The multi-step argument uses T9 (ForwardAllocation), T10a (AllocatorDiscipline), T1 (LexicographicOrder), and `inc(·, k')` semantics — all established in ASN-0001. The reasoning about sibling increments and child prefix extensions is derivable from these existing axioms without external evidence.
