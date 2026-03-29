# Review of ASN-0042

## REVISE

### Issue 1: `nodeField` notation reinvents foundation definition
**ASN-0042, O9 and O6 proof**: `nodeField(pfx(π)) ≼ nodeField(a)`
**Problem**: The foundation (ASN-0034, T6) already defines `N(t)`, `U(t)`, `D(t)`, `E(t)` as the field extraction functions via `fields(t)`. The ASN uses `nodeField(a)` as an informal synonym for `N(a)` without defining it or citing the foundation's notation. This appears in O9's formal statement, in the O6 forward-direction proof ("pfx(π) ≼ nodeField(a)"), and in the O9 case analysis. The `acct(a)` definition is genuinely new (the foundation defines no such composite), but it too would be clearer written in terms of the foundation's `N(t)` and `U(t)`.
**Required**: Replace `nodeField(a)` with `N(a)` throughout. In the `acct` definition, consider stating: when `zeros(a) ≥ 1`, `acct(a)` is the tumbler whose components are `N(a)` followed by `[0]` followed by `U(a)`, using the foundation's field extraction functions.

### Issue 2: O10 existence proof omits the empty sub-delegate boundary case
**ASN-0042, O10 existence (zeros = 0 case)**: "such a value exists because a finite set of natural numbers has a maximum"
**Problem**: The argument collects user-field components of all existing sub-delegate prefixes into a finite set and invokes "a finite set of natural numbers has a maximum" to find a fresh value `u`. But if there are no sub-delegates (or all sub-delegates are node-level with no user field), the collected set is empty, and the empty set has no maximum. The conclusion is still correct — any `u ≥ 1` suffices vacuously — but the intermediate reasoning has a gap at this boundary. The zeros = 1 case has a separate gap of the same kind: "The allocation mechanism (TA5) can always produce such addresses" is asserted without showing the construction (which would be: `inc(pfx(π), 2)` to reach document level, then `inc(·, 2)` to reach element level).
**Required**: Handle the empty case explicitly: "if no sub-delegate has user-field components, choose any `u ≥ 1`; otherwise, choose `u` exceeding the maximum user-field component." For the zeros = 1 case, show the two-step `inc` construction or cite the allocator's ability to reach document-level addresses from account-level prefixes.

## OUT_OF_SCOPE

None. The ASN's scope exclusions are well-drawn and the ASN stays within them.

VERDICT: REVISE
