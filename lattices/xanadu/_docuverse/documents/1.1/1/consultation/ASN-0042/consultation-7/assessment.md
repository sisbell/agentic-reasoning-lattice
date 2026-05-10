# Revision Categorization — ASN-0042 review-7

**Date:** 2026-03-15 22:16

## Issue 1: O6 embedding derivation — step 3 compresses a two-case argument into one clause
Category: INTERNAL
Reason: The two-case zero-alignment argument is already present in the ASN's O9 proof; the fix is expanding step 3 to parallel that existing structure using definitions already in the document.

## Issue 2: O14 prose claims singular bootstrap principal; formalization permits multiple
Category: INTERNAL
Reason: The ASN itself already acknowledges "A multi-node system would have multiple initial principals." The fix is aligning the prose with the existing formalization — the information to resolve the singular/plural mismatch is already present in the document.

## Issue 3: Worked example does not verify O10 (DenialAsFork)
Category: INTERNAL
Reason: O10 is fully defined in the ASN and the review provides concrete tumblers. The fork scenario can be constructed entirely from existing definitions, the established principals, and the address space already set up in the worked example.
