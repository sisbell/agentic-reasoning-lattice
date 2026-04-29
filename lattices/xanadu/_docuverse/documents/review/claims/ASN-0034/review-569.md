# Cone Review — ASN-0034/TA5-SigValid (cycle 1)

*2026-04-25 21:36*

Reading the ASN as a system. The Foundation NAT-* claims, T0, T4, T4a–c, TA5-SIG, TA5-SigValid all hang together; the heavy work is in TA5-SIG's max-construction and T4a's biconditional. I'll flag what I noticed beyond the prior findings.

### Defensive meta-prose in T4 body and Consequence justifying downstream instantiation
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: T4 body — "T4 is purely definitional: it characterises T4-valid as a predicate on `T`... downstream consumers requiring T4-validity (T4b's projection domains `dom(N), dom(U), dom(D), dom(E)`; T4c's level subdomain) carry it as an explicit precondition rather than receiving it from T4." T4 Consequence — "Stated under the bound-alone hypothesis so that downstream consumers — T4a (precondition `t ∈ T ∧ zeros(t) ≤ 3` without the field-segment constraint) and T4b (transitively, via T4-validity) — instantiate the cited Consequence directly at their use-site, without a meta-argument about which derivation steps are needed."
**Issue**: Both passages explain *why* T4 is structured the way it is (consumer-convention justification, anticipating instantiation patterns), rather than asserting the claim itself. The same use-site inventory recurs in T4b's Depends ("matching T4a's precondition pointwise, so instantiation at the local `t` yields the conclusion at the use-site directly — no meta-argument... is required"). The pattern is reviser-drift: paragraphs added to defend the chosen quantification rather than to advance the argument. The claim stands without them.

### T4b restates the presence pattern in three slots
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: T4b *Definition*: per-`k` formulas for `N, U, D, E` and `dom(·)`. T4b body *Derivation*: same per-`k` case analysis with non-emptiness justifications. T4b *Postconditions*: "Presence pattern, exhausted over `dom(N)` by T4's Exhaustion Consequence... `k = 0` → only `N` defined; `k = 1` → `N, U` defined; `k = 2` → `N, U, D` defined; `k = 3` → all four defined."
**Issue**: The four-case presence pattern appears in Definition, walks in the body, and is restated in Postconditions. The Postconditions restatement also re-quotes the Exhaustion-Consequence instantiation already given in Definition. A reader navigating Postconditions for the contract gets the body content again rather than a distinct closure. Compresses without affecting soundness.

### TA5-SigValid invokes antisymmetry of `≤` not exported as a NAT-order Consequence
**Class**: OBSERVE
**Foundation**: NAT-order — Consequences listed are exactly-one trichotomy and `≤`-transitivity.
**ASN**: TA5-SigValid body — "Combining the two through antisymmetry of `≤` — supplied by NAT-order via exactly-one trichotomy, which eliminates the three disjoint-pair cases `m < n ∧ n < m`, `m < n ∧ m = n`, and `m = n ∧ n < m` from the four-way distribution of the conjoined disjunctions — yields `sig(t) = #t`." Depends entry restates the same derivation sketch.
**Issue**: Antisymmetry of `≤` is a load-bearing fact at the closing step but is derived inline at the use-site rather than exported as a Consequence in NAT-order (alongside `≤`-transitivity). The derivation is sound, but other derived properties (`≤`-transitivity, exactly-one trichotomy) are first-class Consequences while antisymmetry is not — an asymmetry in the foundation surface. The convention elsewhere (NAT-sub strict-monotonicity, NAT-addbound dominance) is to host such derivations as Consequences of the supplying claim.

### T4c "labels are pairwise distinct" conflates symbol-distinctness with single-valuedness
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: T4c Postconditions — "*Pairwise distinctness:* the four labels `node address`, `user address`, `document address`, `element address` are pairwise distinct, since `0, 1, 2, 3` are pairwise distinct in ℕ — NAT-addcompat's strict successor inequality `n < n + 1` instantiated at `n ∈ {0, 1, 2}` chained by NAT-order transitivity yields `0 < 1 < 2 < 3`... and `zeros(t)` is single-valued, so distinct zero counts induce distinct labels."
**Issue**: The label terms (`node address`, etc.) are syntactically distinct identifiers introduced by definition; their pairwise distinctness as labels is trivial. The substantive injectivity claim being established is "no T4-valid `t` receives more than one label," which follows because `zeros(t)` is single-valued and the four biconditionals partition by zero count. The phrasing routes the substantive claim through the auxiliary `0 ≠ 1 ≠ 2 ≠ 3` chain when the operative fact is single-valuedness of `zeros(·)` against partition by biconditional. The conclusion is correct.

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 663s*
