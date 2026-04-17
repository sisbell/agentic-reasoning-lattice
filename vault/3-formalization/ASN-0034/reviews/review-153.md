# Cone Review — ASN-0034/T1 (cycle 6)

*2026-04-17 11:40*

### Uncounted NAT-order closures at "contradicting" steps in sub-case (ii, ii) and Case `k₂ < k₁` under case-(ii) of `b < c`

**Foundation**: NAT-order (NatStrictTotalOrder).

**ASN**: T1 (LexicographicOrder), part (c) Transitivity.

Sub-case (ii, ii) ends: *"Either way `m < n`, contradicting `m = n`."* The strict comparison `m < n` is produced by an enumerated transitivity site; the equality `m = n` is produced by an enumerated NAT-cancel site. But the closure step — that `m < n` and `m = n` are jointly impossible — is itself a NAT-order consumption (either irreflexivity after substituting `n = m` into `m < n` to yield `m < m`, or trichotomy's exactly-one clause at the length pair `(m, n)` ruling out the co-holding of the strict and equality alternatives).

Case `k₂ < k₁` under the hypothetical case-(ii) branch of `b < c` ends: *"by NAT-order's transitivity yields `k₂ > k₁`, contradicting `k₂ < k₁`."* The transitivity composition itself is enumerated as site 1; the subsequent contradiction between `k₂ > k₁` and `k₂ < k₁` is a further NAT-order consumption (trichotomy's exactly-one clause at the index pair `(k₁, k₂)`, or irreflexivity after noting that the two strict inequalities cannot both hold by the `<` relation's structure).

**Issue**: Case 3's case-(ii) reverse-witness rebuttals close analogously — transitivity produces `n < m` (resp. `m < n`) which contradicts the case hypothesis `m < n` (resp. `n < m`) — and the enumeration explicitly attributes that closure to *"the mutual-exclusivity form of the same invocation that opened Case 3"*, i.e., the opening trichotomy site is reused for the closure under the same-pair / co-pair absorption convention the enumeration establishes. Sub-case (ii, ii) and Case `k₂ < k₁` under case-(ii) of `b < c` have no prior trichotomy invocation at their relevant pair — `(m, n)` in sub-case (ii, ii), `(k₁, k₂)` in the Case `k₂ < k₁` step — to absorb the closure into, so the co-pair reuse mechanism is unavailable. The closures therefore must either be enumerated as fresh NAT-order sites or routed through an already-enumerated site. Under the declared convention that each proof cites only the ℕ facts it actually uses, these closure steps are unattributed consumptions: neither the "invoked once" irreflexivity tally nor the eleven-site trichotomy itemization covers them.

**What needs resolving**: Either enumerate these closures as additional NAT-order sites (if trichotomy, the preamble total rises and the eleven-site count becomes thirteen; if irreflexivity, its "invoked once" count becomes "invoked three times"; the per-instance convention decides whether the two sub-cases contribute jointly or separately), or restructure the closure step so it folds into an already-counted site — for instance, deriving the contradiction directly from an enumerated transitivity composition rather than from a separate strict-vs-equality or strict-vs-opposite-strict comparison. Whichever route is chosen, the convention that Case 3 applies (co-pair absorption into an opening trichotomy site) and the convention that sub-case (ii, ii) and the `k₂ < k₁` case-(ii) step apply must be the same, since all three patterns close a "strict inequality contradicts a known fact at the same pair" step by the same logical move.
