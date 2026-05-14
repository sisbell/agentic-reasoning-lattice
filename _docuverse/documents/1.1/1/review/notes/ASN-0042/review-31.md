# Review of ASN-0042

## REVISE

### Issue 1: O10 trajectory uses arithmetically incorrect baptism semantics

**ASN-0042, O10 proof, "Trajectory for `zeros(pfx(π)) = 0`"**: "Let `b₀ = pfx(π)` and define `b₁ = inc(b₀, 2) = pfx(π).0.u` (account-level, `zeros = 1`)"

**Problem**: This equation is mathematically false. By TA5(d), `inc(t, 2)` extends `t` by exactly two positions where position `#t + 1` is `0` and position `#t + 2` is `1`. So `inc(b₀, 2) = pfx(π).0.1`, with terminal value always `1`, not arbitrary `u`. The u-selection argument that produces `u ∈ ℕ_{>0} ∖ S` is incompatible with a single `inc(·, 2)` baptism step. The trajectory is only correct for `u = 1`.

**Required**: Either (a) restrict the construction to `u = 1` and separately handle the case `1 ∈ S` with a different strategy, or (b) extend the trajectory to use sibling increments: baptize `pfx(π).0.1` via `inc(pfx(π), 2)`, then `pfx(π).0.2` via `inc(pfx(π).0.1, 0)`, ... up to `pfx(π).0.u` via repeated `inc(·, 0)` calls (TA5(c)). The corresponding baptism step count is `u + 2`, not `3`.

### Issue 2: O10 step count `k = 3 - zeros(pfx(π))` is incorrect for u > 1

**ASN-0042, O10 Formal Contract**: "exhibits a chain `b₀ = pfx(π) ⊏ b₁ ⊏ ... ⊏ b_k = a'` of `k = 3 - zeros(pfx(π))` baptism steps, each invoking `inc(b_{j-1}, 2)` to descend one field level"

**Problem**: For the `zeros(pfx(π)) = 0` case with `u > 1` (forced when `1 ∈ S`), reaching `pfx(π).0.u` from `pfx(π)` requires `u` baptisms at the user-field level (one `inc(·, 2)` plus `u - 1` sibling increments via `inc(·, 0)`), not one. Each `inc(·, 0)` step extends laterally, not into a deeper field — yet the formal contract claims every step "descend[s] one field level". The total step count is `u + 2`, not `3`.

**Required**: Restate the step count to reflect the lateral sibling sub-trajectory, and distinguish field-descending steps (`inc(·, 2)`) from same-level sibling steps (`inc(·, 0)`). The "each invoking `inc(b_{j-1}, 2)`" claim must be corrected.

### Issue 3: O10 does not address baptismal sequencing when sub-delegate domains contain intermediate siblings

**ASN-0042, O10 proof, "Per-step authorization and trajectory closure"**: "At each step `Σ_{j-1} → Σ_j`, the per-intermediate analysis just given establishes that `π` is the most-specific covering principal for `b_j` in `Π_{Σ_{j-1}}`."

**Problem**: The baptism mechanism (ASN-0040 `next(B, p, d)`) produces siblings sequentially: `next` returns `inc(p, d)` if no children exist at `(p, d)`, otherwise `inc(max(children), 0)`. To baptize `pfx(π).0.u` for `u > 1`, the system first requires `pfx(π).0.1, ..., pfx(π).0.(u-1)` to be baptized in order. If `1 ∈ S` because a Form B sub-delegate has prefix exactly `pfx(π).0.1`, then `π` is *not* the most-specific covering principal of `pfx(π).0.1` — the sub-delegate is. So `π` cannot baptize `pfx(π).0.1`, and the system cannot reach `pfx(π).0.2` without the sub-delegate first baptizing its own prefix. The proof's per-intermediate analysis verifies non-coverage at the *target* `a'` but does not address authorization for the intermediate sibling baptisms that the baptismal mechanism forces.

**Required**: Either (a) prove that `π` can always reach a fully-owned address via an alternative trajectory that avoids sub-delegate-owned siblings (e.g., for account-level `π`, the document-level address `inc(pfx(π), 2) = pfx(π).0.1` is always safe and requires only one baptism — this is actually the account-level case and works correctly), or (b) explicitly handle the cooperative scenario where sub-delegates must baptize their own prefixes before `π` can proceed, or (c) weaken the existence claim to be conditional on the baptismal state.

### Issue 4: O10's "u-selection" assumes the sub-delegate set is fully known but doesn't ground baptismal authority for intermediates

**ASN-0042, O10 proof**: "Choose any `u ∈ ℕ_{>0} ∖ S`; if `S = ∅`, choose any `u ≥ 1`."

**Problem**: The u-selection ensures the *target* `pfx(π).0.u` is not covered by any sub-delegate. But when `1 ∈ S` (forcing `u > 1`), the intermediate sibling addresses `pfx(π).0.k` for `k < u` may include both sub-delegate-covered values (e.g., `k = 1`) and π-covered values. The proof doesn't analyze whether the *sequence* of baptisms can interleave authorizations across principals. Even if `u = 2` and `1 ∈ S` but `2 ∉ S`, the baptismal mechanism still produces `pfx(π).0.1` first, and `π` cannot authorize it.

**Required**: Extend the existence argument to either (a) demonstrate that some target reachable via π-only baptisms always exists (perhaps using `inc(pfx(π), 1)` paths that avoid Form B interference, or the document-level escape used in the account-level case), or (b) admit that the construction depends on sub-delegate cooperation and rephrase the postcondition accordingly.

## OUT_OF_SCOPE

(None — the scope is appropriately observed.)

VERDICT: REVISE
