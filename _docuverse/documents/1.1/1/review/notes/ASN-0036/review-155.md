# Review of ASN-0036

## REVISE

### Issue 1: Result/count asserted inside the ValidInsertionPosition Definition slot
**ASN-0036, Valid insertion position (non-empty Definition)**: "There are exactly `N + 1` valid insertion positions: the `N` positions coinciding with existing V-positions `v₀` through `v_{N−1}`, plus the append position `shift(min(V_1(d)), N)`."
**Problem**: This is a theorem about the cardinality of the satisfying set, stated in a Definition slot. The same claim is then re-derived in the standalone derivation paragraph ("Hence the predicate is satisfied by exactly `N + 1` distinct positions") and restated again as formal-contract postcondition (c). The count appears three times in three structural slots. A Definition should fix the defining condition only; the count is a consequence that belongs with its derivation.
**Required**: Remove the count sentence from the Definition; let the derivation establish it and postcondition (c) record it.

### Issue 2: Commentary embedded in the ValidFirstInsertionPosition Definition
**ASN-0036, Valid insertion position (empty Definition)**: "Distinct values of `m` identify distinct valid positions; the strand model fixes only the lower bound `m ≥ 2`."
**Problem**: This is meta-commentary about what the model does and does not fix, placed in a definition slot. It duplicates the Open Question ("the specific value is a one-time allocation convention... What operation-layer constraints determine the canonical choice of m"). The definition only needs `v = [1,...,1]` of depth `m`; the "strand model fixes only the lower bound" observation is essay content that does not advance the defining condition.
**Required**: Strike the commentary from the Definition; the Open Question already carries it.

### Issue 3: S1 Remark is a scope inventory that does not advance the claim
**ASN-0036, The content store (S1 Remark)**: "S1 covers addresses at which content has actually been stored, a narrower scope than T8's allocation permanence, which covers any allocated address whether or not it carries content."
**Problem**: This is a use-site/scope comparison against a foundation property. It states what S1 is *not* relative to T8 rather than advancing S1's content; a reader following the append-only-log argument must step around it. Under the `review-mode.anti-bloat` classifier this is a flaggable pattern.
**Required**: Drop the remark, or fold the single distinguishing fact (S1 is conditioned on `a ∈ dom(C)`) into S1's frame if it is load-bearing — it is not currently used downstream.

## OUT_OF_SCOPE

### Topic 1: Operation-layer preservation of D-CTG / D-MIN / S2
The question of how INSERT, DELETE, COPY, and REARRANGE preserve the contiguity invariants — including insertion that coincides with an occupied V-position and the displacement underlying it — is correctly deferred. It is named in the Open Questions and matches the declared scope exclusion for operation-specific frame/postconditions. No revision needed here; the state-level invariants stand independently.

### Topic 2: Canonical choice of V-position depth `m`
The strand model fixes only `m ≥ 2`; the canonical value (m = 2 for basic INSERT/DELETE vs. deeper subdivisions) is an operations-layer convention. Properly out of scope.

VERDICT: REVISE
