# Revision Categorization — ASN-0001 review-7

**Date:** 2026-02-28 09:28

## Issue 1: TA4 verification contradicts stated property
Category: INTERNAL
Reason: The counterexample is constructed from the ASN's own constructive definitions of ⊕ and ⊖. The fix (strengthening TA4's precondition to require all components before k to be zero, or restricting to single-component displacements) is derivable from the existing definitions and the verification already written in the ASN.

## Issue 2: TA1 inconsistency between body and table
Category: INTERNAL
Reason: The body states weak (≤), the verification confirms weak is correct with equality arising in Case 1, and the table states strict (<). This is a notation error resolvable by reading the ASN's own text.

## Issue 3: TA3 stated without proof or verification
Category: INTERNAL
Reason: The constructive definition of ⊖ is fully specified in the ASN. The case-by-case verification can be constructed from that definition using the same method already applied to TA1/TA1-strict — no external evidence is needed.

## Issue 4: Partition Monotonicity proof assumes k = 0 without justification
Category: INTERNAL
Reason: The ASN already cites Gregory's implementation evidence (`rightshift=0` for element allocation, `rightshift=1` for sub-document creation) and describes the architectural pattern (siblings at the same depth, children one level deeper). The fix — constraining T10a so that sibling allocation uses k = 0 and reserving k > 0 for child-spawning — is derivable from the evidence and reasoning already present in the ASN.

## Issue 5: Global Uniqueness Case 4 depends on the flawed non-nesting argument
Category: INTERNAL
Reason: This is entirely downstream of Issue 4. Once T10a is constrained to k = 0 for siblings, the length-uniformity claim holds by TA5(c), and the length-separation argument in Case 4 follows. No external evidence is needed beyond what Issue 4's fix provides.

## Issue 6: Reverse inverse proof has a gap in the TA3 application
Category: INTERNAL
Reason: This is downstream of Issues 1 and 3. Once TA4's precondition is corrected and TA3 is verified against the constructive definition — both achievable from the ASN's own content — the proof can be reconstructed with the corrected statements.
