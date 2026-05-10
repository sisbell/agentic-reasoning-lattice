# Revision Categorization — ASN-0036 review-2

**Date:** 2026-03-14 15:55

## Issue 1: Worked example I-addresses violate T4 and S7b
Category: INTERNAL
Reason: The correct address form is derivable from T4 (ASN-0034) and the ASN's own S7b. The review already provides the corrected addresses — mechanical rewrite through the example tables and invariant checks.

## Issue 2: S7 origin formula uses an incomplete identifier
Category: INTERNAL
Reason: The fix is to align S7's formula with what S7a already states — "allocated under the tumbler prefix of the document." The full prefix reconstruction from T4 fields is given in the review itself. No external evidence needed.

## Issue 3: Correspondence run definition has three technical defects
Category: INTERNAL
Reason: All three defects are notational/mathematical. The zero-displacement fix requires a base-case convention or range shift. The action-point mismatch requires defining ordinal-only reduction for I-addresses analogous to TA7a — derivable from the tumbler hierarchy (within a run, all I-addresses share document prefix and element subspace; only the ordinal varies). The representation inconsistency resolves once the reduction is stated.

## Issue 4: S5 quantifies over "reachable states" without defining reachability
Category: INTERNAL
Reason: The review provides the reformulation — state S5 as model-theoretic satisfiability (the invariants admit states with arbitrarily high sharing multiplicity) rather than operational reachability. Uses only concepts already defined in this ASN.
