# Channel Assignment — ASN-0111 review-33

**Date:** 2026-06-08 13:16

## Issue 1: RL4 is not a guarantee of the operation being specified
Reason: Internal. The fix is a restructuring decision — RL4 is L2 restated, recoverable from the key without performing the read, as the claim's own text concedes. Cutting or demoting it requires only the ASN's own content and the L2 citation it already makes.

## Issue 2: Foundation invariants relabeled as introduced claims, each with a motivating essay
Reason: Internal. RL1 already establishes `readlink(a, Σ) = Σ.L(a)`, so collapsing RL3/RL-WF/RL-ARITY into corollaries of that equality and dropping the motivating essays is a pure editorial consolidation derivable from the ASN's own claim structure.

## Issue 3: RL6 restates address-fidelity three times
Reason: Internal. Deduplicating the single fidelity guarantee and cutting the "reader's affair"/"does not silently recurse" restatements is prose pruning that needs nothing beyond the existing text.
