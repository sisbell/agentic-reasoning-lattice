# Revision Categorization — ASN-0084 review-6

**Date:** 2026-04-10 10:04



## Issue 1: Commutativity mislabeled as associativity
Category: INTERNAL
Reason: The fix is a terminology correction — replacing "associativity" with "commutativity" — derivable entirely from the mathematical content already present in the ASN.

## Issue 2: R-BLK Phase 1 description overstates what CS2 guarantees
Category: INTERNAL
Reason: The correction narrows an overstatement about what CS2 guarantees, using only the definitions and worked example already in the ASN. The revised wording describes standard properties of sequential splitting on ordered cut points.

## Issue 3: No explicit bridge from postconditions to ArrangementRearrangement
Category: INTERNAL
Reason: All three components (domain preservation from postcondition, C preservation from frame condition, bijection from R-PPERM/R-SPERM) are already proven in the ASN. The fix is adding an explicit concluding statement that assembles them.
