# Revision Categorization — ASN-0067 review-7

**Date:** 2026-03-21 18:27



## Issue 1: C13 contradicts the ASN's own observation about D-CTG
Category: INTERNAL
Reason: The ASN already contains the correct observation about D-CTG not being an invariant of all reachable states. The fix is rewording C13(a) to be consistent with what the ASN itself already says — no external evidence needed.

## Issue 2: Worked example — maximal merging check incomplete
Category: INTERNAL
Reason: The I-adjacency check for blocks 3 and 4 is a straightforward arithmetic verification using values already present in the worked example. The conclusion is correct; only the justification text needs the missing pair checked.

## Issue 3: ContentReference "m" refers to an ambiguous subspace
Category: INTERNAL
Reason: The fix is a wording clarification to specify which subspace's depth determines m. The mathematical content is unaffected — m = #u already determines everything — and the corrected phrasing follows directly from the existing definitions.
