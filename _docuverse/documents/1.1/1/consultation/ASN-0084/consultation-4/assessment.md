# Revision Categorization — ASN-0084 review-4

**Date:** 2026-04-10 09:29



## Issue 1: Foundation misreference for multi-step ordinal shift
Category: INTERNAL
Reason: The correct foundation properties (OrdinalShift, TS3) are already identified in the review finding itself, and both are defined in ASN-0034 which this ASN already cites. The fix is a straightforward citation correction.

## Issue 2: Properties table omits all definitions
Category: INTERNAL
Reason: All definitions are already present in the ASN body with complete formal content. The fix is mechanical: extract each definition's label, type (DEF), and a one-line summary into the existing properties table.

## Issue 3: Invariant preservation not systematically stated
Category: INTERNAL
Reason: The review finding already identifies the argument (`dom(M'(d)) = dom(M(d))`) and lists the specific invariants (D-CTG, D-MIN, S8-fin, S8a, S8-depth). The preservation follows trivially from domain identity, which is already established in the ASN. The fix is adding an explicit note collecting what is already derivable from the ASN's own content.
