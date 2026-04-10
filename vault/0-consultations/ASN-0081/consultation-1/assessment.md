# Revision Categorization — ASN-0081 review-1

**Date:** 2026-04-09 18:15

## Issue 1: D-X contradicts D-SHIFT — postconditions are internally inconsistent
Category: INTERNAL
Reason: The contradiction is provable from the ASN's own definitions and the concrete counterexample uses only stated operations. Both fix options (weakening D-X or replacing it with a closed-world postcondition) are derivable from D-SHIFT, D-SEP, and the three-region partition already in the ASN.

## Issue 2: Missing contiguity precondition for V_S(d)
Category: GREGORY
Reason: Whether V-positions within a subspace are contiguously allocated (no gaps) depends on how the allocator works in practice. The ASN references "sequential allocation" informally but needs implementation evidence to justify a contiguity axiom.
Gregory question: Within a single subspace of a document's V-stream, does the green allocator guarantee that allocated V-positions are contiguous — i.e., if positions at ordinals k and k+2 exist, must ordinal k+1 also be allocated?

## Issue 3: D-DP proof cites D-X where D-X is contradicted
Category: INTERNAL
Reason: The correct gap-closure argument is given in the review itself: at depth 2, max(L) has ordinal p₂−1, min(Q₃) has ordinal p₂, these are consecutive integers, so the claim is immediate without citing D-X.

## Issue 4: Missing closed-world postcondition
Category: INTERNAL
Reason: The ASN describes contraction as removing X and shifting R, which fully determines the post-state domain. The closed-world postcondition `dom(M'(d)) ∩ V_S(d) = L ∪ Q₃` is the direct formalization of the ASN's own narrative description of the operation.

## Issue 5: No concrete example
Category: INTERNAL
Reason: Constructing a worked example is a mechanical exercise applying the ASN's own definitions. The review provides the specific scenario; computing the three regions, shift function, and post-state uses only operations already defined in the ASN.
