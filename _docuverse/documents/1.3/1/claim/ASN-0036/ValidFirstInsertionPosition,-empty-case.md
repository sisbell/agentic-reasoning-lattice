**Definition (ValidFirstInsertionPosition, empty case).** For a document `d` with `V_1(d) = ∅`, the *ternary* predicate `ValidFirstInsertionPosition(d, v, m)` is satisfied when `m ∈ ℕ` with `m ≥ 2` and `v = [1, 1, ..., 1]` of depth `m`.

*Formal Contract (ValidFirstInsertionPosition, empty case).*
- *Signature:* `ValidFirstInsertionPosition(d, v, m)` — a *ternary* predicate on document `d`, V-position `v`, and depth `m`.
- *Preconditions:* Document `d` with `V_1(d) = ∅`; `m ∈ ℕ` with `m ≥ 2`.
- *Definition:* `ValidFirstInsertionPosition(d, v, m)` holds iff `v = [1, 1, ..., 1]` of depth `m`.
- *Postconditions:* (a) `subspace(v) = 1` and `#v = m`. (b) `v` satisfies S8a: `zeros(v) = 0` and all components positive. (c) For fixed `d` and `m`, exactly one value of `v` satisfies the predicate.
- *Depends:* S8a — for the lower bound `m ≥ 2`; T0 (ASN-0034) — for componentwise positivity of the constant tuple.

### Valid insertion position examples

**Non-empty case (binary predicate).** Let subspace S = 1 and suppose V₁(d) = {[1, 1], [1, 2], [1, 3]}, so N = 3 and min(V₁(d)) = [1, 1]. The depth `m = 2` is read from state via S8-depth. The values of `v` satisfying `ValidInsertionPosition(d, v)` are:

- j = 0: v = min(V₁(d)) = [1, 1]
- j = 1: v = shift([1, 1], 1) = [1, 2]
- j = 2: v = shift([1, 1], 2) = [1, 3]
- j = 3: v = shift([1, 1], 3) = [1, 4]

That gives N + 1 = 4 positions. Any successor state whose `V₁(d)` gains a position at, say, [1, 2] must still satisfy D-CTG and D-MIN.

**Empty case (ternary predicate).** V₁(d) = ∅. Choosing depth m = 2, the unique `v` satisfying `ValidFirstInsertionPosition(d, v, 2)` is `[1, 1]`. D-MIN requires min(V₁(d)) = [1, 1] once the subspace becomes non-empty, so the position is exactly the one D-MIN demands. Choosing m = 3 instead, `ValidFirstInsertionPosition(d, v, 3)` is satisfied uniquely by `v = [1, 1, 1]`; by T3, this is a different tumbler.
