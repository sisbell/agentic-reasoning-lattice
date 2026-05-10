# Cone Review — ASN-0034/TA5-SIG (cycle 1)

*2026-04-25 19:12*

Reading the ASN as a system: foundation arithmetic claims (NAT-*), the tumbler carrier T0, and the constructed last-significant-position function TA5-SIG.

I traced the dependency graph (NAT-carrier → NAT-order → {NAT-zero, NAT-closure} → NAT-addcompat → NAT-addbound, with NAT-discrete, NAT-sub, NAT-wellorder threading through; T0 and TA5-SIG layered on top). No cycles. All declared depends supply what their citing claims actually use.

I walked the four nontrivial proofs:

- NAT-discrete no-interval form: the `m < n` branch dispatches both sub-cases (`m + 1 < n` via `¬(a < b ∧ b < a)`, `m + 1 = n` via substitution into `n < m+1`); `m = n` branch direct.
- NAT-sub strict monotonicity: trichotomy on (a, b) covers `a < b` (goal), `a = b` (irreflexivity at `a + p`), `b < a` with both sub-cases of `b + p ≤ a + p`.
- NAT-sub strict positivity: `m − n = 0` collapses to `n = m` against `n < m`, then NAT-zero + NAT-discrete lift to `m − n ≥ 1`.
- TA5-SIG: well-orders the upper-bound set `U`, contradicts minimality of `m` by exhibiting `m − 1 ∈ U` smaller — every precondition (`m ≥ 1`, `i + 1 ≥ 1`) is discharged from `S ⊆ {1, …, #t}` via the `≤`-defining clause and `<`-transitivity, with NAT-sub's right-inverse and right-telescoping doing the arithmetic.

Cases are exhaustive and exclusive throughout. The TA5-SIG zero/nonzero split covers all `t ∈ T`. Postconditions `1 ≤ sig(t) ≤ #t` hold in both branches via `m ∈ S` (nonzero) and `#t ≥ 1` from T0 (all-zero).

Every cited instantiation matches the cited axiom's signature under the renamings given. Depends lists are tight — no missing citations, no unused ones.

VERDICT: CONVERGED

## Result

Cone review converged.

*Elapsed: 350s*
