# Channel Assignment — ASN-0107 review-15

**Date:** 2026-06-08 11:00

## Issue 1: P1's deduplication paragraph specifies backend mechanics, not a system guarantee
Reason: Purely editorial trim — the load-bearing guarantee (set cardinality, contribution ∈ {0,1}) is already fully stated in P1's first sentences, and the required restatement as a one-clause faithfulness obligation is derivable from the ASN's own definitions. No design intent or implementation evidence is in question.

## Issue 2: The "returning the links is a separate, out-of-scope operation" remark is stated twice
Reason: Pure deduplication of a scope note already present at two sites; consolidating to W1 needs nothing beyond the ASN's own text.

## Issue 3: R5's existence-count half is E4 restated
Reason: The note already labels R5's affirmative half `= E4` explicitly; folding it to a citation and keeping only the novel discovery-count failure is internal restructuring with both pieces already present in the ASN.
