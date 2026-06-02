# Channel Assignment — ASN-0086 review-217

**Date:** 2026-06-01 17:29

## Issue 1: FreshLinkKeyDisjointness is unused machinery
Reason: The fix is internal — whether any argument in the note consumes L14/L14a is determined by reading the note's own proofs (R0 preservation, Step 1 inventory), and the reviewer already supplies the lineage fact that L14/L14a are derived standing theorems in any ASN-0093-conforming system. Verify no downstream reader exists, then delete the sub-lemma and the L14/L14a mentions, leaning on SD where disjointness is actually invoked.

## Issue 2: Convention RetractionDirectionality is re-explained at its consumption site
Reason: Purely editorial — Convention RetractionDirectionality and the `coverage(G')`-only quantifier already carry the meaning; collapsing the restatement to a bare citation is derivable from the note's own structure.

## Issue 3: WP Case 1 is presented as part of a "Weakest-Precondition Analysis" but is, by its own statement, not a wp
Reason: Purely editorial — the load-bearingness counterexamples are the substance and remain intact; dropping the meta-prose that contrasts Case 1 against a wp it never claimed to be is a structural trim derivable from the note alone.
