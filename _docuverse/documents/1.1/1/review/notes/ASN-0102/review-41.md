# Review of ASN-0102

## REVISE

### Issue 1: X8 calls the copied blocks "maximal contiguous I-runs of resolve_Σ(R)" — contradicting the inter-reference coalescence it then asserts

**ASN-0102, X8 (RunFragmentation)**: "The copied region is *constructed* as `B_copy = {(v + c_j, a_j, n_j) : 1 ≤ j ≤ k}` — k blocks, one per maximal contiguous I-run of resolve_Σ(R), laid at consecutive V-starts... The *canonical* (maximally-merged, M12) count of the copied region need not equal k, however".

**Problem**: These two statements cannot both be literally true. If each block were a *maximal contiguous I-run of the whole resolution* `resolve_Σ(R)`, the blocks would already be I-maximal and the canonical (maximally-merged) count would equal `k` by construction — leaving no room for the inter-reference coalescence the same claim goes on to describe ("Across an inter-reference boundary... may also be I-adjacent... and coalesces in the canonical form"). The earlier load-bearing statement is precise about this: "each `k_i` is the maximal-contiguous-I-run count of reference `r_i` **taken in isolation**." `resolve_Σ(R)` is the *concatenation* of per-reference maximal decompositions (ASN-0058 `resolve(R) = resolve(r_1) ⌢ … ⌢ resolve(r_q)`); its list elements are per-reference maximal, not globally maximal, so two consecutive elements straddling a reference boundary can be I-adjacent without having been merged. The summary table row repeats the same imprecise phrasing ("one per maximal contiguous I-run, independent of W").

**Required**: Replace "one per maximal contiguous I-run of resolve_Σ(R)" with "one per run of the resolution *list* `resolve_Σ(R)` (each run per-reference maximally merged, but not merged across reference boundaries)," in both the X8 prose and the summary table, so the construction count `k` is consistent with the subsequent "canonical count `≤ k`, equality iff no inter-reference boundary is I-adjacent."

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
