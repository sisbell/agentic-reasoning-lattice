## Audit

**Foundation pass.** NAT-cancel exports exactly `n + m = p + m ⟹ n = p` (right) and `m + n = m + p ⟹ n = p` (left) — equality cancellation only. No inequality form `n + m ≤ p + m ⟹ n ≤ m` appears in any foundation statement. NAT-addcompat's right order-compatibility gives the forward direction only: `p ≤ n ⟹ p + m ≤ n + m`. The backward direction — order cancellation under `+` — is a derived consequence requiring NAT-order trichotomy, NAT-addcompat (forward), and NAT-order irreflexivity; it is not an axiom.

**Claim-by-claim scan.** S8a, D-CTG, subspace, V-sub, S8-depth, Σ.M(d), S8-fin, D-PRED, NAT-induction, and D-CTG-depth are individually clean. D-CTG-depth in particular has the fix from the declined finding in place: D-PRED and NAT-cancel absent from its Depends, NAT-discrete entry correctly describes the direct `(i, m)` instantiation. One defect surfaces inside D-INJ.

---

### D-INJ surjectivity steps misapply NAT-cancel to inequalities
**Class**: REVISE
**Foundation**: NAT-cancel (NatAdditionCancellation) — axiom `n + m = p + m ⟹ n = p`
**ASN**: D-INJ (InjectiveImageCardinality) — three sites in the ρ-surjectivity prose and the NAT-cancel Depends bullet:

*Proof body, below-k₀ sub-case:* "NAT-discrete's … forward direction … descends this strict bound to `j + 1 ≤ P + 1`, **whence right cancellation of the summand `1` (NAT-cancel) returns `j ≤ P`**."

*Proof body, above-k₀ sub-case (lower end):* "descends `k₀ < j` to `k₀ + 1 ≤ j`; rewriting `j` as `i + 1` gives `k₀ + 1 ≤ i + 1`, **whence right cancellation of the summand `1` (NAT-cancel) returns `k₀ ≤ i`**."

*Proof body, above-k₀ sub-case (upper end):* "`j ≤ P + 1`, that is `i + 1 ≤ P + 1`, and **the same right cancellation of the summand `1` (NAT-cancel) returns `i ≤ P`**."

*Depends bullet for NAT-cancel:* "The same right cancellation at the summand `1` also discharges `ρ`'s surjectivity placements … **it reads the discreteness-derived bound `j + 1 ≤ P + 1` as `j ≤ P`** in the below-`k₀` sub-case, and **the bounds `k₀ + 1 ≤ i + 1` and `i + 1 ≤ P + 1` as `k₀ ≤ i` and `i ≤ P`** in the above-`k₀` sub-case."

**Issue**: All three proof steps and the Depends description apply NAT-cancel's equality axiom `n + 1 = m + 1 ⟹ n = m` to hypotheses of the form `n + 1 ≤ m + 1` (strict inequalities). NAT-cancel's stated axiom takes an equation on the left; an inequality hypothesis `n + 1 ≤ m + 1` is not an instance of it. A formal verifier applying the literal axiom at these steps fails. The injectivity use of NAT-cancel in the same-branch upper case — `a + 1 = b + 1 ⟹ a = b` from the hypothetical collision — is correct; the error is confined to the three surjectivity inequality steps.

The conclusion `n + 1 ≤ m + 1 ⟹ n ≤ m` is derivable from the stated foundations, but not via NAT-cancel alone. The actual chain: unfold `n + 1 ≤ m + 1` by NAT-order's `≤`-definition; in the equality case `n + 1 = m + 1`, apply NAT-cancel to get `n = m`; in the strict case `n + 1 < m + 1`, NAT-order trichotomy on `(n, m)` — the case `n ≥ m` (i.e., `m ≤ n`) is refuted by NAT-addcompat's right compatibility (`m + 1 ≤ n + 1`) combined with `n + 1 < m + 1` and NAT-order's irreflexivity — leaving `n < m`, hence `n ≤ m`. This requires NAT-order (trichotomy + irreflexivity) and NAT-addcompat (right compat, forward direction) in addition to NAT-cancel.

**What needs resolving**: The three surjectivity proof steps and the NAT-cancel Depends bullet must be corrected to reflect the actual inference chain: the `n + 1 ≤ m + 1 ⟹ n ≤ m` step is a two-case split on NAT-order's `≤`-definition, with NAT-cancel handling the equality sub-case and NAT-addcompat + NAT-order (trichotomy, irreflexivity) handling the strict sub-case. The NAT-cancel Depends entry should restrict its surjectivity claim to the equality sub-case; NAT-order and NAT-addcompat should be acknowledged as contributors to the inequality cancellation in the strict sub-case.

---

VERDICT: REVISE