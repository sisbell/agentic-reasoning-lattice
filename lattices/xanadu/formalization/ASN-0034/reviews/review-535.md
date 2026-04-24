# Regional Review — ASN-0034/TA5-SIG (cycle 2)

*2026-04-24 14:10*

Reading TA5-SIG with the previous findings in hand: the `i + 1 ≥ 1` discharge has been added, and NAT-closure is now declared. I walked the revised proof end-to-end looking for new gaps.

### `i + 1 ≥ 1` case-split compression mirrors the earlier `m ≥ 1` observation
**Class**: OBSERVE
**Foundation**: NAT-order `≤`-defining clause and transitivity of `<`; NAT-addcompat strict successor inequality.
**ASN**: TA5-SIG, newly-added discharge: "`i + 1 ≥ 1` is obtained ... by chaining `1 ≤ i` ... with NAT-addcompat's strict successor inequality `i < i + 1` — the weak bound `1 ≤ i` dispatched into `<`-or-`=` cases ... and the strict segment composed by NAT-order's transitivity of `<` — yielding `1 < i + 1`".
**Issue**: The split of `1 ≤ i` produces two subcases. The `1 < i` subcase composes with `i < i + 1` via `<`-transitivity to yield `1 < i + 1` as claimed. The `1 = i` subcase does not compose via `<`-transitivity — it requires substituting `i = 1` via indiscernibility of `=` into `i < i + 1` (or equivalently instantiating NAT-addcompat's successor inequality at `n := 1` to obtain `1 < 1 + 1` and rewriting `i + 1 = 1 + 1`). The discharge was introduced in this cycle to close finding #1; the compression pattern is the same as the pre-existing `m ≥ 1` OBSERVE but lands at a new site.

### Final minimality-of-`m` contradiction is one step compressed
**Class**: OBSERVE
**Foundation**: NAT-order exactly-one-trichotomy Consequence (`¬(x < y ∧ y < x)`) together with `≤`-definition; alternatively transitivity of `<` with irreflexivity.
**ASN**: TA5-SIG, closing step of the `m ∈ S` derivation: "So `m − 1 ∈ U` with `m − 1 < m`, contradicting minimality of `m` in `U`."
**Issue**: Minimality of `m` in `U` supplies `m ≤ m − 1`. Combined with the established `m − 1 < m`, the contradiction is not immediate — one must split `m ≤ m − 1` via the `≤`-defining clause into `m < m − 1 ∨ m = m − 1`: the `<` branch conjoins with `m − 1 < m` and hits `¬(x < y ∧ y < x)` at `(m, m − 1)`, while the `=` branch substitutes into `m − 1 < m` to yield `m − 1 < m − 1` against irreflexivity. The prose compresses this to one clause. Correct as written, but the precise reader walks the split.

VERDICT: OBSERVE

## Result

Regional review converged after 2 cycles.

*Elapsed: 896s*
