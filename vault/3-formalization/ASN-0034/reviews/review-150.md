# Cone Review — ASN-0034/T1 (cycle 3)

*2026-04-17 11:15*

### NAT-order consumption at Case 2's `k' < k` rebuttal via case (i) — "fails on equal components" step uncounted

**Foundation**: NAT-order (NatStrictTotalOrder).

**ASN**: T1 (LexicographicOrder), part (b) Trichotomy, Case 2: *"If `k' < k`, the minimality of `k` gives `a_{k'} = b_{k'}`, so case (i) fails on equal components and case (ii) requires `k' = n + 1` (or `m + 1`)..."*

**Issue**: The inference "case (i) fails on equal components" is a NAT-order consumption that appears nowhere in the enumeration. Case (i) of the reverse witness requires a strict inequality at position `k'` (e.g., `b_{k'} < a_{k'}` when the forward sub-case is `aₖ < bₖ`); combined with `a_{k'} = b_{k'}` from minimality, this reduces by substitution to a claim of the form `v < v`, which is refuted either by NAT-order's irreflexivity or by trichotomy's exactly-one clause (equality excludes strict inequality). Under the declared per-instance convention ("each proof cites only the ℕ facts it actually uses"), this step must be attributed to a NAT-order site. But the enumeration states irreflexivity is *"invoked once, at part (a) Case (i), to contradict `aₖ < aₖ`"* and the trichotomy tally of nine explicitly restricts Case 2's rebuttal contributions to (opening step, `k'=k` via case (i), `k'=k` via case (ii) ×2 sub-cases, `k'<k` via case (ii) ×2 sub-cases). The `k'<k` rebuttal via case (i) is absent from both counts, even though the proof text explicitly executes that rebuttal. The parallel `k'=k` case-(i) rebuttal *is* enumerated (trichotomy site 3), so the omission is specific to the `k'<k` variant rather than an intentional elision of all case-(i) rebuttals.

**What needs resolving**: Either enumerate the `k'<k` case-(i) rebuttal as an additional NAT-order site (irreflexivity becomes "invoked twice" or trichotomy becomes "invoked ten times", with the preamble total raised to seventeen and the per-instance convention applied to decide whether the two Case 2 sub-cases contribute one or two sites here), or restructure the narrative so the `k'<k` rebuttal routes its case-(i) failure through an already-enumerated site — for example, by folding both case-(i) and case-(ii) failures at `k'<k` under a single uniform appeal whose NAT-order attribution is already counted.
