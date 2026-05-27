# Channel Assignment — ASN-0099 review-45

**Date:** 2026-05-27 08:47

## Issue 1: F4's spans-monotonicity prose conflates two distinct failure modes
Reason: The fix is purely a precision issue in characterizing predicate properties — the ASN already contains the definitions of spans-monotonicity, F1's existential structure, and the alternative predicates. The corrected characterization (containment alone breaks monotonicity; reverse containment and cardinality preserve witnesses but lack per-span witness structure) is derivable by direct inspection of the predicates defined in the ASN.

## Issue 2: Strengthening 3's witness construction is underspecified
Reason: The fix is explicit in the review (pin slots 1 and 2 empty, witness at slot 3) and follows the same construction pattern already used by Strengthenings 1 and 2 in the ASN. No external evidence is needed — L3's permission for empty non-type slots and the cardinality-on-empty-slots argument are already established in the ASN.

## Issue 3: F4 marks F12 as both definition and citation handle without clearly distinguishing the dual role
Reason: This is an editorial/labeling issue internal to the ASN's own presentation. The two remediation options (split labels vs. annotate the table) are authoring choices resolvable from the ASN's structure alone, with no design-intent or implementation-evidence question at stake.

## Issue 4: Coverage definition restated rather than imported
Reason: This is a citation-convention issue about how to reference ASN-0043's coverage definition. The fix (cite by reference or mark as convenience reproduction) is an editorial decision within this ASN's scope and does not require new evidence from Nelson or Gregory.
