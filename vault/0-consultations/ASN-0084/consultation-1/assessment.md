# Revision Categorization — ASN-0084 review-1

**Date:** 2026-04-10 08:29

## Issue 1: Pervasive cross-ASN references to non-foundation ASNs
Category: INTERNAL
Reason: The fix is structural — inline the ordinal increment convention from ASN-0034 (already a foundation dependency), drop unused state components (R, E), and either restate block definitions or defer R-BLK. All replacement definitions are derivable from existing foundation ASNs.

## Issue 2: Postconditions undefined outside the target subspace; frame conditions missing
Category: INTERNAL
Reason: The intent is unambiguous from the existing postcondition claim `dom(M'(d)) = dom(M(d))` — positions outside subspace S and other documents are unchanged. Adding explicit frame clauses is a mechanical completion of what the ASN already implies.

## Issue 3: R-SWP proof deferred to R-PIV without showing work
Category: INTERNAL
Reason: R-PIV provides the exact template — compute ordinal ranges for R-S1/R-S2/R-S3, check pairwise disjointness, show union tiles [c₀, c₃). All definitions needed are present in the ASN; the work is just writing it out.

## Issue 4: R-BLK commutativity proof — missing premise and dismissed cases
Category: INTERNAL
Reason: Phase 1 already guarantees no post-split block straddles a cut boundary, and the displacement formulas for β and μ are explicitly defined. The fix is stating the same-region premise and computing one additional case (β with negative displacement) from existing definitions.

## Issue 5: R-BLK Phase 1 — split processing order unspecified
Category: INTERNAL
Reason: CS2 (strict ordering of cuts) already guarantees that ascending-order processing is well-defined — each later cut falls in the right-hand piece of an earlier split. The fix is making this implicit ordering assumption explicit.

## Issue 6: R-BLK — reassembled block contiguity not established
Category: INTERNAL
Reason: The uniform-displacement property is already proven (commutativity argument in Phase 3), and contiguity follows directly — consecutive positions shifted by a constant remain consecutive. The fix is adding one explicit sentence connecting these existing results.
