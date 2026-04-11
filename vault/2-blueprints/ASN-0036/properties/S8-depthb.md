**S8-depth(b) (OrdinalDisplacementExtension).** We extend ordinal displacement notation to `k = 0`: define `v + 0 = v` (identity) and `v + k = shift(v, k)` for `k ≥ 1`. OrdinalShift (ASN-0034) has precondition `n ≥ 1`; the extension to `k = 0` is purely notational — no arithmetic is performed. For I-addresses, define `a + 0 = a` and `a + k = shift(a, k) = a ⊕ δ(k, #a)` for `k ≥ 1`. This is well-defined: the action point of `δ(k, #a)` is `#a`, which falls at the element field's last component — S7c guarantees element-field depth `δ ≥ 2`, so the last component of the full address *is* the element ordinal's deepest position — and TumblerAdd's prefix rule copies all earlier components (node, user, document fields, their separators, and the subspace identifier) unchanged, producing a result of length `#a`.

*Formal Contract:*
- *Definition:* For V-positions: `v + 0 = v`; `v + k = shift(v, k)` for `k ≥ 1`. For I-addresses: `a + 0 = a`; `a + k = a ⊕ δ(k, #a)` for `k ≥ 1`
- *Well-definedness:* I-address case requires `a ∈ dom(Σ.C)` satisfying S7c (`#fields(a).element ≥ 2`)
- *Dependencies:* OrdinalShift, TumblerAdd (ASN-0034), S7c
