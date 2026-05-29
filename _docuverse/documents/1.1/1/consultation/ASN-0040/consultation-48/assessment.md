# Channel Assignment — ASN-0040 review-48

**Date:** 2026-05-28 21:20

## Issue 1: B8's postcondition is stronger than the proof establishes
Reason: The fix is a statement/contract scoping problem — the proof already exposes the incomparable-branch case and the remedy is to restrict the postcondition to co-reachable acts (or redefine "baptismal act"). Both the defect and the corrective language live entirely within the ASN's own model.

## Issue 2: B7 applies T10a.6 to arbitrary B6 pairs without realizing them in one conforming tree
Reason: The required alternative — a direct disjointness proof from S1 plus the foundation's prefix/ordering machinery (T1, PrefixOrderingExtension) already cited in-text — is derivable from the ASN and its declared dependencies; no design intent or implementation evidence is at issue.

## Issue 3: B6 necessity forward-references B8, which depends on B6
Reason: The fix substitutes the already-proved S2 stream identity for the circular B8 citation; S2 is stated and proved in this same ASN, so the correction is fully internal.

## Issue 4: Bop frame statement triplicated with repeated component inventory
Reason: Pure editorial de-duplication of a claim stated three times; no external information is needed to collapse it to the single Frame line.

## Issue 5: Repeated downstream deferral to the activation-discipline ASN
Reason: Editorial consolidation of three identical deferral pointers into one Open Questions entry; entirely within the author's discretion and the ASN's text.
