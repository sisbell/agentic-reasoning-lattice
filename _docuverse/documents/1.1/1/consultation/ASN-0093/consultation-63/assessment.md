# Channel Assignment — ASN-0093 review-63

**Date:** 2026-05-31 11:20

## Issue 1: Intro undercounts the substrate's new content-side invariants — C2 is omitted
Reason: The fix is internal — it reconciles the opening paragraph's enumeration/count with the Properties Introduced table's own Source attributions (C2 marked "Substrate; content-side analog of L1a"). Both the discrepancy and either resolution (add C2 and bump the count, or re-label C2's Source as restated from ASN-0036 S7a) are derivable from the ASN's own content.

## Issue 2: C1c/L1c subsequent-emit chain exhibition carries freshness prose that is not part of the allocator-conformance claim
Reason: The fix is internal — C1c/L1c are defined within the ASN as pure existence claims for a T10a-conforming step sequence, and the freshness obligation is already discharged by SubsequentEmissionFreshness per the ASN's own structure. Striking the misplaced freshness sentences requires only the ASN's definitions and lemma division of labor.
