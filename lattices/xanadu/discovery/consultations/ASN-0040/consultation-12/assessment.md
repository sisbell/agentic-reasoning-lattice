# Revision Categorization — ASN-0040 review-12

**Date:** 2026-04-09 12:32



## Issue 1: B1 proof — B6(iii) not verified for the stream-identity sub-case
Category: INTERNAL
Reason: The missing derivation steps (sole-defect implies zeros(p) ≤ 3, zeros(p') = zeros(p) − 1, therefore B6(iii)) are all derivable from definitions and reasoning already present in the ASN. The review even spells out the exact lines to add.

## Issue 2: Properties Table — B1 dependency list omits B10
Category: INTERNAL
Reason: The omissions are mechanical — the Formal Contracts already list the correct dependencies, and the fix is copying those dependencies into the summary table rows. No external evidence needed.

## Issue 3: Post-proof B1 recap is redundant with the formal proof
Category: INTERNAL
Reason: This is an editorial restructuring — removing redundant re-argument and retaining the no-skip observation. The decision about what to keep vs. remove is fully determined by the ASN's own content and the review's specific instructions.
