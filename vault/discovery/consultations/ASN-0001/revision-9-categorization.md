# Revision Categorization — ASN-0001 review-9

**Date:** 2026-03-01 18:50

## Issue 1: TA-strict not verified against the constructive definition
Category: INTERNAL
Reason: The proof follows directly from the constructive definition of ⊕ already in the ASN — at the action point k, (a ⊕ w)_k = a_k + w_k > a_k since w_k > 0, giving a ⊕ w > a by T1 case (i). No external evidence needed.

## Issue 2: Constructive definition of ⊖ undefined for prefix-related operands of different lengths
Category: INTERNAL
Reason: The fix requires choosing a convention (zero-padding or precondition restriction) for the abstract definition. Both options are derivable from the ASN's own framework — the mathematical content and Gregory's implementation behavior are already discussed in the ASN.

## Issue 3: "Action point" used before defined
Category: INTERNAL
Reason: The definition already exists in the ASN's constructive definition section; the fix is purely a presentation reordering — moving the definition to before its first use at TA0.

## Issue 4: Global Uniqueness Case 3 — derivation compressed to assertion
Category: INTERNAL
Reason: The two-case derivation (same length implies component difference by contrapositive; different length implies inequality directly) follows from T3, which is already stated and proven in the ASN. No external evidence needed.

## Issue 5: TA7a not verified from the constructive definition
Category: INTERNAL
Reason: The derivation follows from the constructive definition's "copy from start" rule for positions before the action point, which is already fully specified in the ASN. Identifying the subspace-identifier position and confirming element-local displacements act after it requires only the address structure from T4, also already present.
