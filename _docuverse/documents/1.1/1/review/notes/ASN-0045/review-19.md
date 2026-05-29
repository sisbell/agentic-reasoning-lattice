# Review of ASN-0045

## REVISE

### Issue 1: Misattributed discreteness step in at-least-one
**ASN-0045, Well-Definedness (at-least-one)**: "`n > 2` with the upper bound `n ≤ 3` and NAT-discrete at `m = 2` (using `n < 3` from `n ≤ 3 ∧ n ≠ 3`, the residual case being `n = 3`) forces `n = 3`."
**Problem**: This is internally contradictory. NAT-discrete at `m = 2` states `2 ≤ n < 3 ⟹ n = 2` — applied to the cited `n < 3`, it forces `n = 2`, not `n = 3`. The branch hypothesis is `n > 2`, so the sub-case `n < 3` is *empty* in ℕ (no natural strictly between 2 and 3). Discreteness here serves to *rule out* the `n < 3` sub-branch as vacuous, after which trichotomy's residual `n = 3` (combined with `n ≤ 3`) closes the case. The text instead presents discreteness-at-m=2 as the direct producer of `n = 3`, which it is not.
**Required**: Restate as: under `n > 2`, trichotomy on `(n, 3)` gives `n < 3 ∨ n = 3 ∨ n > 3`; `n > 3` is excluded by `n ≤ 3`; `n < 3` with `n > 2` is excluded because NAT-discrete at `m = 2` would force `n = 2`, contradicting `n > 2`; hence `n = 3`.

### Issue 2: "Already covered" mislabels vacuous sub-branches
**ASN-0045, Well-Definedness (at-least-one)**: "the branch `n < 2` with `n ≥ 1` (from `n > 1`) and NAT-discrete at `m = 1` forces `n = 1` — already covered."
**Problem**: Inside the branch `n > 1`, the sub-case `n < 2` is not "already covered" — it is *contradictory*. Deriving `n = 1` while assuming `n > 1` is a contradiction (`n = 1 ∧ n > 1`), which proves the sub-branch empty, not that it duplicates the earlier top-level `n = 1` case. "Already covered" implies a benign overlap; the correct status is vacuity by contradiction. The same loose phrasing recurs in the nested `n > 2` handling.
**Required**: Mark these sub-branches as vacuous (refuted by the branch hypothesis), not as cases "already covered." Distinguish "this case cannot arise" from "this value was handled elsewhere."

### Issue 3: Segment walk is heavier than its own conclusion and obscures the load-bearing step
**ASN-0045, Well-Definedness (at-least-one)**: the multi-paragraph trichotomy/discreteness walk concluding `0 ≤ n ≤ 3 ∧ n ∈ ℕ ⟹ n ∈ {0,1,2,3}`.
**Problem**: The two defects above are products of an over-elaborated derivation in which the actual mechanism (each adjacent gap `k < n < k+1` is empty by NAT-discrete) is restated three times with inconsistent attributions. As written, a reader cannot cleanly extract which axiom discharges which step, which is precisely where Issues 1–2 slipped in.
**Required**: Replace with a single uniform statement: for `n ∈ ℕ` with `0 ≤ n ≤ 3`, NAT-discrete instantiated at `m ∈ {0,1,2}` rules out every open gap `m < n < m+1`, and NAT-order trichotomy against the boundaries `0,1,2,3` exhausts the segment; hence `n ∈ {0,1,2,3}`. One application schema, cited once, applied at three boundaries.

## OUT_OF_SCOPE

None. The ASN stays within field-level classification and correctly defers lifecycle/allocation topics.

VERDICT: REVISE
