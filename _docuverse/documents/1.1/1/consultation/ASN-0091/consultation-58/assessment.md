# Channel Assignment — ASN-0091 review-58

**Date:** 2026-06-04 00:33

## Issue 1: The RA-adm "three-layer" discharge routes through an RA-adm-dependent lemma (circular), and is partly redundant
Reason: Purely a restructuring of the ASN's own discharge logic — the fix is to reorder existing internal dependencies (clause (iv) constructive route, ExtendedReachableStateInvariants) so RE-subpres is downstream of RA-adm, all of which is present in the ASN. No design intent or implementation evidence bears on the proof's internal citation structure.

## Issue 2: Ordering/routing-justification meta-prose around RA-dom's source
Reason: The fix is to delete a comparative routing justification and cite RA-dom's source in one clause — entirely an exposition edit within the ASN's existing content. Neither design intent nor implementation evidence is required.

## Issue 3: Net-effect distinction restated in two places
Reason: De-duplication of a distinction already developed in the abstract section, with the table cross-referencing it instead of re-deriving. Both passages are already in the ASN; choosing the canonical location is an internal editorial decision.
