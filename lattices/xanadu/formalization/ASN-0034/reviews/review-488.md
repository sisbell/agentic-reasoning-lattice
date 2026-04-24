# Regional Review — ASN-0034/T4 (cycle 2)

*2026-04-24 04:36*

### T4b imports subtractive last-segment form without justifying conversion from T4a's `+1` form
**Class**: REVISE
**Foundation**: T4a (exports last-segment non-emptiness as `s_k + 1 ≤ #t`); NAT-sub (strict-monotonicity Consequence, right-telescoping)
**ASN**: T4b setup — "the last segment occupies the indices `s_k + 1, …, #t` (when `k ≥ 1`), so its non-emptiness requires `s_k ≤ #t - 1`" and subsequently "These three inequalities are the local re-expression of T4a's segment non-emptiness conclusion." The subtractive form is then used in every case (k=1: `s₁ ≤ #t - 1`, k=2: `s₂ ≤ #t - 1`, k=3: `s₃ ≤ #t - 1`).
**Issue**: T4a explicitly lands on the native `+1` form `s_k + 1 ≤ #t` and its Depends block flags that a subtractive form "would require a further non-strict-monotonicity step not declared by NAT-sub." T4b silently switches to `s_k ≤ #t - 1` and calls it a "local re-expression," but the conversion `s_k + 1 ≤ #t ⟹ s_k ≤ #t - 1` is not a rewriting — in ℕ it requires NAT-sub's strict-monotonicity Consequence at `p = 1`, right-telescoping `(s_k + 1) − 1 = s_k`, and case analysis on the `≤`-unfolding of `s_k + 1 ≤ #t`. The form T4b consumes is not the form T4a produces, and the bridging argument is absent.
**What needs resolving**: Either (a) restate T4b's last-segment non-emptiness inequality in T4a's native `+1` form `s_k + 1 ≤ #t` and adapt the per-case derivations to consume that form directly, or (b) make the conversion step explicit — cite NAT-sub's strict-monotonicity Consequence and telescoping, and walk both branches of `≤` — and update T4a's Depends commentary accordingly. The current "local re-expression" framing does not license the switch.

### T4c re-derives T4's already-exported Exhaustion Consequence
**Class**: REVISE
**Foundation**: T4 (exports `zeros(t) ∈ {0, 1, 2, 3}` as its Exhaustion *Consequence*, derived in T4's own body from the bound, NAT-zero, trichotomy, and NAT-discrete)
**ASN**: T4c, Exhaustion prose — "By T4, every T4-valid tumbler satisfies `zeros(t) ≤ 3`, and by NAT-zero, `0 < zeros(t) ∨ 0 = zeros(t)`… These bounds alone do not fix `zeros(t) ∈ {0, 1, 2, 3}`… Proceed by iterated case analysis using NAT-order's trichotomy… At `m = 0`… At `m = 1`… At `m = 2`… At the final step, trichotomy at `(zeros(t), 3)`… leaving `zeros(t) = 3`. Every branch terminates with `zeros(t) ∈ {0, 1, 2, 3}`."
**Issue**: This passage reproduces T4's Exhaustion Consequence derivation step-for-step rather than citing it. T4 already exports `zeros(t) ∈ {0, 1, 2, 3}` for every T4-valid tumbler, derived using exactly the same foundations (NAT-zero, trichotomy, NAT-discrete) and the same iterated-case mechanism. T4c's Depends does not even list this as a citation of T4's *Consequence* — T4 is cited only for "the T4-valid subdomain constraints." The prose that should have been one line ("By T4's Exhaustion Consequence, `zeros(t) ∈ {0, 1, 2, 3}`") is instead a re-derivation. This is noise the precise reader must work around, and it obscures whether T4c is building on T4 or paralleling it.
**What needs resolving**: Replace T4c's Exhaustion re-derivation with a single citation of T4's Exhaustion Consequence, and add that Consequence to T4c's Depends entry for T4. The duplicated NAT-zero/NAT-discrete/NAT-order citations can then be pruned (they remain justified for Injectivity's chain separately).

### Exhaustion citation missing from T4a's case enumeration over `k ∈ {0, 1, 2, 3}`
**Class**: REVISE
**Foundation**: T4 (Exhaustion Consequence `zeros(t) ∈ {0, 1, 2, 3}` for every T4-valid tumbler)
**ASN**: T4a setup — "Set `k = zeros(t) ∈ {0, 1, 2, 3}` with zeros at positions `s₁ < s₂ < … < s_k`". T4a's Depends lists T4 as supplying "the positional conditions (i), (ii), (iii), the field-segment terminology, and the zero-count bound `zeros(t) ≤ 3`."
**Issue**: T4a's precondition is `t ∈ T ∧ zeros(t) ≤ 3`; the bound alone does not pin `zeros(t)` to `{0, 1, 2, 3}` (it additionally needs NAT-zero's `0 ≤ zeros(t)` and NAT-discrete to collapse the interval). T4a asserts `k ∈ {0, 1, 2, 3}` without either deriving it inline or citing T4's Exhaustion Consequence that already packages this fact. The four-case presentation that follows relies on exhaustion, so the citation chain must be closed. T4b, in contrast, does explicitly cite T4's Exhaustion Consequence for the same purpose.
**What needs resolving**: T4a should either (a) cite T4's Exhaustion Consequence to license `k ∈ {0, 1, 2, 3}`, adding it to the T4 entry in Depends, or (b) derive the exhaustion inline from the preconditions it already cites (NAT-zero, NAT-discrete, NAT-order). Picking one removes the silent step; the present text does neither.

VERDICT: REVISE
