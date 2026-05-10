# Review of ASN-0036

## REVISE

### Issue 1: S8a guarded quantification leaves universal V-position well-formedness unstated

**ASN-0036, S8a**: `(A v ∈ dom(Σ.M(d)) : v₁ ≥ 1 : zeros(v) = 0 ∧ v > 0)`

**Problem**: The Dijkstra-style guard `v₁ ≥ 1` makes S8a a conditional — "for V-positions *where* `v₁ ≥ 1`, these properties hold" — without ever asserting that `v₁ ≥ 1` holds universally. V-positions are element-field tumblers, and T4's positive-component constraint guarantees every element field component is strictly positive, so `v₁ ≥ 1` is always true. But this chain is never stated formally in the ASN. The gap matters: S8's partition proof depends on every V-position belonging to some subspace `S` with `v₁ = S ≥ 1` (to invoke T5 and T10 for cross-subspace disjointness). If V-positions with `v₁ = 0` were possible, they would be orphaned from the partition argument.

A secondary inconsistency: S8a is labeled "V-position well-formedness" in the properties table but "Every text-subspace V-position" in the body. More broadly, S8a's condition `v₁ ≥ 1` captures both text-subspace (`v₁ = 1`) and link-subspace (`v₁ = 2`) V-positions — the ASN itself notes this ("The range guard `v₁ ≥ 1` captures both text-subspace and link-subspace V-positions"). Yet the prose and the properties table repeatedly label S8a and S8 as "text-subspace," which would mean `v₁ = 1`. The formal scope and the prose label disagree.

**Required**: Either (a) remove the guard and state S8a as a universal property: `(A v ∈ dom(Σ.M(d)) :: v₁ ≥ 1 ∧ zeros(v) = 0 ∧ v > 0)`, citing T4's positive-component constraint for the `v₁ ≥ 1` conjunct; or (b) add a separate property asserting `v₁ ≥ 1` for all V-positions and cite it in S8a's dependencies. In either case, fix the "text-subspace" labels on S8a and S8 to match the actual condition — either narrow the condition to `v₁ = 1` (text only) or change the labels to "element-subspace" or drop the subspace qualifier entirely.

### Issue 2: D-SEQ notation is ill-defined at depth m = 1

**ASN-0036, D-SEQ**: `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}` where the tuple has length `m`

**Problem**: At `m = 1`, the tuple `[S, 1, ..., 1, k]` of length 1 is a single-component tumbler where the first component (subspace identifier `S`) and the last component (varying ordinal `k`) occupy the same position. The set comprehension `{[k] : 1 ≤ k ≤ n}` generates tumblers `[1], [2], ..., [n]`, which span multiple subspaces — `[k]` has subspace `k`, not subspace `S`. For `S = 2`, `V_2(d) = {[2]}` but the formula gives `{[1]}` (with `n = 1`), which is false.

The derivation step also fails at `m = 1`: "D-MIN gives the minimum `k = 1`" refers to the last component of `min(V_S(d)) = [S, 1, ..., 1]`. At `m = 1`, `min = [S]`, whose last (and only) component is `S`, not `1`. For `S ≥ 2`, the derivation's claim "minimum `k = 1`" is incorrect.

The issue is unreachable in practice — ValidInsertionPosition requires `m ≥ 2` — but D-SEQ is stated as a standalone corollary without this precondition. A downstream consumer citing D-SEQ directly would inherit the ill-defined case.

**Required**: Add `m ≥ 2` as an explicit precondition to D-SEQ: "...if `V_S(d)` is non-empty and the common V-position depth `m ≥ 2`, then there exists `n ≥ 1` such that..." The D-SEQ entry in the Properties table should include `m ≥ 2` in its dependency/precondition list.

## OUT_OF_SCOPE

### Topic 1: Maximal span decomposition uniqueness
**Why out of scope**: S8 proves existence of a decomposition (via singletons). Whether a unique maximal decomposition (fewest runs) exists is a separate structural question about the arrangement function's internal regularity, not a correctness issue for the invariants established here. Already noted in Open Questions.

### Topic 2: Operation preservation of D-CTG and D-MIN
**Why out of scope**: Whether DELETE, INSERT, COPY, and REARRANGE preserve contiguity and the minimum-position constraint is a verification obligation for each operation's ASN. The ASN correctly identifies this as future work and defines the constraints that operations must be shown to preserve.

VERDICT: REVISE
