# Cone Review — ASN-0034/TS5 (cycle 1)

*2026-04-18 13:51*

### TS4 omits `n ∈ ℕ` from its precondition/binder
**Foundation**: OrdinalShift (Preconditions: `v ∈ T, n ∈ ℕ, n ≥ 1`); OrdinalDisplacement (preconditions include `n ∈ ℕ`).
**ASN**: TS4 binder `(A v, n : n ≥ 1 ∧ #v = m : shift(v, n) > v)` and Formal Contract Preconditions `v ∈ T, n ≥ 1, #v = m`. The proof then writes "fix n ≥ 1" and immediately invokes "By OrdinalShift, shift(v, n) = v ⊕ δ(n, m)" and "By OrdinalDisplacement, δ(n, m) = [0, ..., 0, n] of length m".
**Issue**: TS4's range and preconditions never name `n ∈ ℕ`. OrdinalShift's call requires `n ∈ ℕ` and OrdinalDisplacement's call requires `n ∈ ℕ`. The convention this ASN repeatedly enforces — articulated at OrdinalDisplacement's m-th-position-typing site and re-cited in TS3 ("an order statement like `n ≥ 1` presupposes rather than establishes carrier membership") — forecloses routing the carrier-typing through `n ≥ 1` alone. TS3 by contrast carries `n₁ ∈ ℕ ∧ n₂ ∈ ℕ` explicitly in both binder and preconditions for exactly this reason. TS4's chain to OrdinalShift / OrdinalDisplacement therefore has no named source for the `n ∈ ℕ` precondition.
**What needs resolving**: TS4 must either add `n ∈ ℕ` to its binder/preconditions (matching TS3's discipline) or supply a named source for the `n ∈ ℕ` carrier-typing at each downstream invocation, and update Depends to reflect that discharge.

---

### TS5 omits `n₁ ∈ ℕ` and `n₂ ∈ ℕ` from its precondition/binder
**Foundation**: TS3 (Preconditions include `n₁ ∈ ℕ, n₂ ∈ ℕ`); NAT-sub axioms `(A m, n ∈ ℕ : m ≥ n : m − n ∈ ℕ)`, `(A m, n ∈ ℕ : m > n : m − n ≥ 1)`, `(A m, n ∈ ℕ : m ≥ n : n + (m − n) = m)` — all guard their conclusions on `m, n ∈ ℕ`.
**ASN**: TS5 binder `(A v, n₁, n₂ : n₁ ≥ 1 ∧ n₂ > n₁ ∧ #v = m : ...)` and Preconditions `v ∈ T, n₁ ≥ 1, n₂ > n₁, #v = m`. The proof then invokes NAT-sub conditional closure and strict positivity at `m = n₂, n = n₁`, NAT-sub left-inverse to write `n₂ = n₁ + d`, and TS3 instantiated at `a = n₁, b = d`.
**Issue**: TS5 names neither `n₁ ∈ ℕ` nor `n₂ ∈ ℕ`. NAT-sub's three consumed clauses each gate on `m, n ∈ ℕ` in their axiom statements; TS3 requires `n₁ ∈ ℕ` for the `a = n₁` substitution (and `d ∈ ℕ`, which the proof does derive via NAT-sub closure, for `b = d`). The order facts `n₁ ≥ 1` and `n₂ > n₁` cannot supply ℕ-typing under the same convention OrdinalDisplacement and TS3 articulate. The chain to TS3 and to all three NAT-sub clauses therefore has no named source for the carrier-typing.
**What needs resolving**: TS5 must either add `n₁ ∈ ℕ, n₂ ∈ ℕ` to its binder/preconditions or route the typings through named axioms (and acknowledge those routings in Depends).

---

### TS4 binder leaves `m` free
**Foundation**: TS3 binder `(A v, n₁, n₂, m : ... : ...)` explicitly binds `m` and the proof preface justifies the dummy abbreviation in detail.
**ASN**: TS4 binder `(A v, n : n ≥ 1 ∧ #v = m : shift(v, n) > v)`.
**Issue**: `m` appears in the range `#v = m` and is implicitly used downstream (e.g. in the OrdinalDisplacement invocation `δ(n, m)`), but `m` is not a binder variable and is not introduced as an abbreviation at the property statement. TS3 explicitly binds `m` as a dummy and gives a paragraph explaining why the universal collapses to a single witness; TS4 reuses the same syntactic pattern without the same scoping or justification, leaving `m` free at the property level.
**What needs resolving**: TS4's binder should either add `m` to the binder list (paralleling TS3's `(A v, n₁, n₂, m : ...)`) with the matching abbreviation justification, or reformulate the property so `m` does not appear free.
