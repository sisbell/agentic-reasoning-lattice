**Definition (OrdinalDisplacementExtension).** Extends ordinal displacement notation to `k = 0` as an identity case: `v + 0 = v` for V-positions, and `a + 0 = a` for I-addresses. For `k ≥ 1`, `v + k` is defined by `shift(v, k)` — see OrdinalShift (ASN-0034) — which displaces the last component of `v` by `k` positions. The extension to `k = 0` makes the indexing `M(d)(v + k) = a + k` for `0 ≤ k < n` uniform, avoiding a special case at the starting position of a correspondence run.

*Contract:*

- *Label:* S8-depth(b)
- *Name:* OrdinalDisplacementExtension
- *Definition:* Extends ordinal displacement notation to `k = 0` as identity for both V-positions and I-addresses
- *Status:* introduced
- *Dependencies:* OrdinalShift (ASN-0034)
- *Notes:* Notation convention; allows uniform run indexing.
