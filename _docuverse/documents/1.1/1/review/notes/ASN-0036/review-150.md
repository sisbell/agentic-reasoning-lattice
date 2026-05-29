# Review of ASN-0036

I worked through every proof (S1, S4, S5, S7, S8, D-CTG-depth, D-SEQ) and the partition lemma in detail. The mathematics is sound: edge cases (empty arrangement, m = 2 vs. m ≥ 3, append position, cross- vs. within-subspace uniqueness) are handled, the singleton-partition uniqueness lemma is rigorous in both branches, and the foundation citations are all to ASN-0034 (a foundation), so the self-containment rule is satisfied. Concrete worked examples are present and check the key postconditions. My findings are anti-bloat, consistent with the `review-mode.anti-bloat` classifier this note carries.

## REVISE

### Issue 1: D-MIN prematurely states D-SEQ's result
**ASN-0036, D-MIN (postcondition note)**: "Combined with D-CTG and S8-fin, a document with n text elements occupies V-positions [1, 1] through [1, n] — matching Nelson's 'addresses 1 through 100.'"
**Problem**: This is exactly the content D-SEQ formally derives ("V_1(d) = {[1, ..., 1, k] : 1 ≤ k ≤ n}"). Stating the combined D-CTG + D-MIN + S8-fin conclusion inside D-MIN, before D-SEQ exists, is a duplicate-downstream-result pattern: the reader meets the theorem as an aside in the property whose job is only to fix the minimum, then meets it again as the actual claim. The same "matching Nelson's 'addresses 1 through n/100'" tag also recurs across D-CTG, D-MIN, and D-SEQ.
**Required**: Drop the "Combined with..." sentence from D-MIN (its job is `min = [1,...,1]`, full stop) and keep the combined-occupancy statement and the Nelson tag only at D-SEQ, where it is the derived conclusion.

## OUT_OF_SCOPE

None. The Open Questions correctly defer operation frame conditions, `Val` constraints, the sharing inverse, quiescent-state relaxation of S3, reachability/orphan distinction, and subspace-alignment enforcement — all genuinely new territory rather than gaps in this note. S7d's document-addressing premise is load-bearing for S7's `origin` uniqueness and reads as an addressing fact, not a lifecycle operation, so I do not flag it against the document-creation scope exclusion.

VERDICT: REVISE
