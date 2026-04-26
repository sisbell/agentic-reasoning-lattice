# Cone Review (Confirmation) — ASN-0034/T10a

*2026-04-26 05:39*

### Vacuous sub-case `i = sig(t)` in case `k = 0`'s T4(ii) discharge
**Class**: REVISE
**Foundation**: TA5-SigValid (SigOnValidAddresses) — on T4-valid `t`, `sig(t) = #t`; T4 (HierarchicalParsing) — T4(ii)'s index range is `1 ≤ i < #t'`
**ASN**: TA5a, Case `k = 0`, T4(ii) discharge: "we split each `i` with `1 ≤ i < #t'` (equivalently `1 ≤ i < #t` by TA5(c)'s `#t' = #t`) on whether `sig(t) ∈ {i, i + 1}`: when `sig(t) ∉ {i, i + 1}`, ...; when `i = sig(t)`, `t'ᵢ = t'_{sig(t)} = t_{sig(t)} + 1 ≠ 0` ... falsifies the conjunct `t'ᵢ = 0`, and hence the conjunction `t'ᵢ = 0 ∧ t'ᵢ₊₁ = 0`; when `i + 1 = sig(t)`, ..."
**Issue**: The three-way split takes `sig(t)` generically, but TA5-SigValid (already in Depends and explicitly cited elsewhere in this case for `sig(t) = #t`) forces `sig(t) = #t`. The sub-case `i = sig(t)` then requires `i = #t`, contradicting the index-range bound `i < #t` (equivalently `i < #t' = #t` by TA5(c)). The sub-case is therefore provably vacuous on T4-valid `t`. Worse, in this sub-case the proof refers to `t'ᵢ₊₁` at the position `sig(t) + 1 = #t + 1`, which is outside `t'`'s domain (since `#t' = #t`), so the conjunct `t'ᵢ₊₁ = 0` it claims to falsify is itself ill-typed. Discharging a vacuous and ill-formed sub-case with an extended NAT-chain instantiation is exactly the reviser-drift pattern flagged in prior cycles for this proof — defensive case work around a sig(t) the case's own foundations have already pinned to `#t`. The work is sound (vacuous sub-cases discharge automatically) but the prose introduces an incoherent reference and obscures the actual case structure (only two non-vacuous sub-cases on T4-valid `t`: `sig(t) ∉ {i, i + 1}` and `i + 1 = sig(t)`).
**What needs resolving**: Either reduce the T4(ii) split in case `k = 0` to the two non-vacuous sub-cases on T4-valid `t` — `sig(t) ∉ {i, i + 1}` (where TA5(b) + T4(ii) on `t` discharge) and `i + 1 = sig(t) = #t` (where the NAT chain at position `#t = sig(t)` falsifies `t'ᵢ₊₁ = 0`, with the case itself only arising when `#t ≥ 2`) — using TA5-SigValid's `sig(t) = #t` to exclude the third sub-case, or, if the generic-`sig(t)` split is retained for structural symmetry, label the `i = sig(t)` sub-case as vacuous (with a one-line discharge from `sig(t) = #t` and `i < #t`) rather than constructing an extended NAT-chain instantiation against an ill-typed `t'_{#t+1}` reference.

VERDICT: REVISE

## Result

Cone review not converged after 8 cycle(s).

*Elapsed: 6368s*
