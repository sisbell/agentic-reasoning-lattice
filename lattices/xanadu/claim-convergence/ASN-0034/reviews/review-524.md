# Regional Review — ASN-0034/T1 (cycle 1)

*2026-04-24 11:59*

### Case 3 branch selection implicit

**Class**: OBSERVE
**Foundation**: Case 3 of T1 trichotomy proof
**ASN**: T1 proof, part (b) Case 3: "NAT-order's trichotomy at `(m, n)` resolves `m ≠ n` into `m < n ∨ n < m`. If `m < n`, then `k = m + 1 ≤ n`, so `a` is a proper prefix of `b` and `k` witnesses `a < b` via T1(ii)."
**Issue**: The step "if `m < n`, then `k = m + 1 ≤ n`" silently assumes we are in the (β) branch of Case 3. Rigorously, `m < n` excludes (γ) — since (γ) forces `n + 1 ≤ m`, hence `n < m` via NAT-addcompat — leaving only (β), which then gives `k = m + 1 ≤ n`. The symmetric "if `n < m`" branch likewise implicitly eliminates (β) before concluding `k = n + 1 ≤ m`. Reasoning is sound but the intermediate elimination is not written out.

### Agreement-range existence phrased circularly

**Class**: OBSERVE
**Foundation**: Transitivity Case `k₁ < k₂` in T1 proof
**ASN**: T1 proof, part (c): "If `a < b` via T1(i): `aₖ₁ < bₖ₁ = cₖ₁` with `k₁ ≤ m`, and the existence of `cₖ₁` gives `k₁ ≤ p`; position `k₁` witnesses `a < c` via T1(i)."
**Issue**: The phrasing "the existence of `cₖ₁` gives `k₁ ≤ p`" inverts the dependency: `cₖ₁` being a well-defined component already requires `k₁ ≤ p`. The bound `k₁ ≤ p` is what needs to be derived first — from `k₁ < k₂` together with `k₂ ≤ p` (case (i) of `b < c`) or `k₂ = n + 1 ≤ p` (case (ii)). The result is correct; the phrasing reads as if it follows from what it actually presupposes.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 597s*
