# Revision Categorization — ASN-0061 review-2

**Date:** 2026-03-21 10:42

## Issue 1: D-DEL is a false postcondition
Category: INTERNAL
Reason: The ASN's own worked example and domain completeness section already contain the correct post-state characterization (dom(M'(d)) ∩ V_S = L ∪ Q₃). The fix is to restate D-DEL using material already present in the ASN.

## Issue 2: D-ORPH missing within-subspace sharing condition
Category: INTERNAL
Reason: The missing condition follows from the ASN's own definitions of within-document sharing (S5, ASN-0036) and the logic of range membership. The reviewer provides the exact formal predicate needed; no external evidence is required.

## Issue 3: D-PRE formal items incomplete
Category: INTERNAL
Reason: Both constraints (#w = #p and w₁ = 0) are already stated in the ASN's prose immediately before D-PRE and are used in subsequent proofs. The fix is mechanical: promote them to numbered items.

## Issue 4: Block classification claims five exhaustive cases but six exist
Category: INTERNAL
Reason: The ASN already acknowledges the both-cuts case in the paragraph following the enumeration and handles it correctly in D-BLK. The fix is to reconcile the enumeration with the ASN's own subsequent text.
