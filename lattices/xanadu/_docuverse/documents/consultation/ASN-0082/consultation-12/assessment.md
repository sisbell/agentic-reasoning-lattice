# Revision Categorization — ASN-0082 review-12

**Date:** 2026-04-09 18:52

## Issue 1: Local axioms VD and VP reinvent foundation properties from ASN-0036
Category: INTERNAL
Reason: The review identifies the exact ASN-0036 statements (S8-depth, S8a) that subsume VD and VP, and the replacement proof structure is derivable from those cited definitions. No design intent or implementation evidence needed.

## Issue 2: Statement registry misattributes foundation definitions as locally introduced
Category: INTERNAL
Reason: Purely a registry correction — changing attribution from "introduced (local)" to "cited (ASN-0036)" for definitions already identified in the review.

## Issue 3: Missing content-store frame condition; S3 and S9 preservation unverified
Category: INTERNAL
Reason: The ASN already describes the shift as operating solely on arrangements, and the review identifies S9 (ASN-0036) as the foundation guarantee. The frame condition and S3 preservation proof are derivable from stated postconditions and cited dependencies.

## Issue 4: I3-CS and I3-CX labeled "frame" in registry but function as domain closure postconditions
Category: INTERNAL
Reason: The body text already correctly calls them "domain closure clauses" — the fix is aligning the registry Type field with the function described in the ASN's own prose.
