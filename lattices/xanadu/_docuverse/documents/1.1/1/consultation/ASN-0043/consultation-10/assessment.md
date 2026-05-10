# Revision Categorization — ASN-0043 review-10

**Date:** 2026-03-17 01:21



## Issue 1: L11 worked example mischaracterizes non-injectivity applicability
Category: INTERNAL
Reason: This is a wording error in the worked example's verification commentary. The fix — replacing the incorrect characterization with accurate language about the existential witness — is fully derivable from L11's own formal statement.

## Issue 2: L11 combines two claims of different logical character under INV
Category: INTERNAL
Reason: This is a classification/structuring decision about how to label properties in the ASN's own table. The precedent (S5 classified as LEMMA in ASN-0036) and the logical character of both halves are already present in the ASN and its dependencies — no external evidence needed.

## Issue 3: L4 formal statement is entailed by L3 + the Endset definition
Category: INTERNAL
Reason: The issue is about the relationship between L4's formal statement and the definitions already given in this ASN. Whether to reclassify L4 as a corollary or restructure the sub-items as lemmas is an internal structural decision requiring no design-intent or implementation evidence.
