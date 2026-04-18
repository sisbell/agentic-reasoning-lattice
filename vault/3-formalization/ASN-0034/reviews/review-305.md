# Cone Review — ASN-0034/TA3 (cycle 6)

*2026-04-18 16:22*

### TA3 Sub-case A2's `≠ 0 ⟹ > 0` step uses NAT-order's defining clause in the converse direction not enumerated in TA3's Depends

**Foundation**: N/A — cross-cutting citation discipline established by TumblerSub's precondition-consequence case (ii), TA2's sub-case (ii), ActionPoint's third postcondition, and TA6's Conjunct 2 (all discharging the `≠ 0 ⟹ > 0` step by combining NAT-zero's lower bound `0 ≤ n` with NAT-order's defining clause `m ≤ n ⟺ m < n ∨ m = n` at `m = 0` and excluding the equality disjunct via `≠ 0`).

**ASN**: TA3 Sub-case A2, first-disagreement branch: "`(a ⊖ w)_p = 0` while `(b ⊖ w)_p ≠ 0` (since they disagree and tumbler components are non-negative, `(b ⊖ w)_p > 0`); `p` satisfies `p ≤ L_{a,w} ∧ p ≤ L_{b,w}` ..., so T1 case (i) yields `a ⊖ w < b ⊖ w`." TA3's NAT-order Depends enumerates role 4 as: "*Defining-clause conversion at component pairs*: `m ≤ n ⟺ m < n ∨ m = n` converts the strict inequalities `x_d > w_d` at divergence points (from `x > w` via T1) into the weak form `x_d ≥ w_d` required by NAT-sub's monotonicity and closure preconditions."

**Issue**: Sub-case A2's step from `(b ⊖ w)_p ≠ 0` together with non-negativity (NAT-zero's `0 ≤ (b ⊖ w)_p`) to `(b ⊖ w)_p > 0` is the converse direction of NAT-order's defining clause — unfolding `0 ≤ n` to `0 < n ∨ 0 = n` and excluding the equality disjunct via `≠ 0`, plus NAT-order's irreflexivity of `<` for the forward direction. TA3's NAT-order role 4 describes only the forward `> ⟹ ≥` conversion used for NAT-sub's preconditions; it does not cover the converse `≥ ∧ ≠ 0 ⟹ > 0` direction used here. T1 case (i) at position `p` requires the strict `(a ⊖ w)_p < (b ⊖ w)_p`, which in this branch reduces (via `(a ⊖ w)_p = 0`) to `0 < (b ⊖ w)_p` — a step the prose elides into "tumbler components are non-negative" without citing the axiom clauses that discharge it.

**What needs resolving**: TA3's NAT-order Depends must either extend role 4 (or add a sixth role) to enumerate the converse-direction `≠ 0 ⟹ > 0` use at Sub-case A2's first-disagreement branch — matching the per-step convention TumblerSub's precondition-consequence case (ii), TA2's sub-case (ii), ActionPoint's third postcondition, and TA6 Conjunct 2 all apply for the structurally identical inference — or reformulate the branch so that `(b ⊖ w)_p > 0` is supplied directly by a cited postcondition (e.g., by routing the argument through TumblerSub's `Pos(b ⊖ w)` + ActionPoint rather than a pointwise `≠ 0 ⟹ > 0` step).
