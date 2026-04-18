# Cone Review — ASN-0034/TS5 (cycle 2)

*2026-04-18 14:03*

### TS5 binder leaves `m` free
**Foundation**: TS3's binder `(A v, n₁, n₂, m : ... ∧ #v = m : ...)` explicitly binds `m` with an abbreviation-justification paragraph. TS4's binder (in the current draft) binds `m` identically.
**ASN**: TS5's binder `(A v, n₁, n₂ : n₁ ∈ ℕ ∧ n₂ ∈ ℕ ∧ n₁ ≥ 1 ∧ n₂ > n₁ ∧ #v = m : shift(v, n₁) < shift(v, n₂))`.
**Issue**: The binder list `(A v, n₁, n₂ : ...)` does not include `m`, yet `m` appears in the range (`#v = m`) and is used downstream ("Fix v ∈ T with #v = m", TS3/TS4 instantiations with `#u = m`). This is exactly the free-`m` pattern flagged for an earlier version of TS4, and TS5 does not replicate the abbreviation-justification preface that TS3 and the new TS4 provide. So `m` remains free at TS5's property-statement level.
**What needs resolving**: TS5's binder should either add `m` to the binder list (paralleling TS3's `(A v, n₁, n₂, m : ...)` and TS4's `(A v, n, m : ...)`) with the matching abbreviation-justification preface, or reformulate the property so `m` does not appear free.

---

### TS4 and TS5 binder range predicates omit `v ∈ T`
**Foundation**: TS3's binder range carries `v ∈ T ∧ n₁ ∈ ℕ ∧ n₂ ∈ ℕ ∧ n₁ ≥ 1 ∧ n₂ ≥ 1 ∧ #v = m`, and TS3's Formal Contract Preconditions list also names `v ∈ T`.
**ASN**: TS4's binder range `n ∈ ℕ ∧ n ≥ 1 ∧ #v = m` (with Preconditions `v ∈ T, n ∈ ℕ, n ≥ 1, #v = m`); TS5's binder range `n₁ ∈ ℕ ∧ n₂ ∈ ℕ ∧ n₁ ≥ 1 ∧ n₂ > n₁ ∧ #v = m` (with Preconditions `v ∈ T, n₁ ∈ ℕ, n₂ ∈ ℕ, n₁ ≥ 1, n₂ > n₁, #v = m`).
**Issue**: The binder quantifies over `v` without restricting it to `T`, so the property as stated claims something about arbitrary `v`, relying on the Preconditions list (which is separate from the binder) to supply the carrier-typing. TS3 keeps binder range and Preconditions in lock-step; TS4 and TS5 diverge. The proofs ("Fix v ∈ T") and the downstream discharges to OrdinalShift / OrdinalDisplacement / TA0 (all of which gate on `v ∈ T`) rest on this carrier-typing. Having the binder silently omit it while Preconditions names it means the property statement at the top is weaker than the contract.
**What needs resolving**: TS4 and TS5 should either add `v ∈ T` to the binder range predicate (aligning with TS3) or articulate the convention by which binder range and Preconditions diverge.
