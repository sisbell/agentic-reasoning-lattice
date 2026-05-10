# Cone Review — ASN-0034/T1 (cycle 6)

*2026-04-17 10:03*

### NAT-order transitivity undercount at Case `k₂ < k₁` case-(i) branch's `k₂ ≤ m` derivation

**Foundation**: NAT-order (NatStrictTotalOrder).

**ASN**: T1 (LexicographicOrder), part (c) Transitivity, Case `k₂ < k₁`: *"Therefore `b < c` is via case (i): `bₖ₂ < cₖ₂` with `k₂ ≤ min(n, p)`. Since `k₂ < k₁` and `a` has components at all positions below `k₁`, we have `k₂ ≤ m`..."* The NAT-discrete enumeration in T1's Depends explicitly acknowledges this step and delimits its own applicability: *"the sibling case-(i) branch of `a < b`, where `k₁ ≤ min(m, n) ≤ m`, yields `k₂ ≤ m` from `k₂ < k₁ ≤ m` via NAT-order alone, so the discreteness appeal is specific to the case-(ii) branch."*

**Issue**: The NAT-order transitivity enumeration lists exactly five sites: Case `k₂ < k₁`'s `k₂ > n ≥ k₁ → k₂ > k₁` chain (which operates within the sub-case (ii) refutation of `b < c`, not this step), sub-case (i, i), sub-case (ii, ii), and Case 3's two reverse-witness rebuttals. The case-(i) branch's derivation of `k₂ ≤ m` from `k₂ < k₁ ≤ m` — the step whose NAT-order routing is explicitly invoked in the NAT-discrete enumeration — is a distinct transitivity use (composing the strict `k₂ < k₁` with the non-strict `k₁ ≤ m` via the standard strict/equality case analysis) and appears at none of the five enumerated sites. Under T0's convention that each proof cites only the ℕ facts it actually uses, the enumeration is exhaustive; the acknowledged NAT-order reliance at the case-(i) branch is therefore a sixth transitivity site absent from the count. The parallel concern applies at the preliminary `k₁ ≤ min(m, n) ≤ m` step itself, which composes `≤` transitively and is similarly uncounted.

**What needs resolving**: Either extend the NAT-order transitivity enumeration to include the case-(i) branch's `k₂ < k₁ ≤ m → k₂ ≤ m` derivation (and, if the preliminary `min(m, n) ≤ m` composition is also counted under the same convention, enumerate that as well), or restructure the step so the case-(i) branch routes through an already-enumerated NAT-order site — for instance, by folding both branches of `a < b` through NAT-discrete's contrapositive under a unified `k₁ ≤ m` premise that the case-(i) branch discharges directly from `k₁ ≤ min(m, n)` without an intermediate transitivity step.
