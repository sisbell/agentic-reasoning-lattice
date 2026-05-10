# Cone Review — ASN-0034/TS1 (cycle 6)

*2026-04-18 07:41*

Looking at the ASN as a whole with attention to cross-property consistency, I'll focus on issues not already captured in Previous Findings.

### OrdinalShift's and OrdinalDisplacement's Preconditions omit the explicit ℕ typing that TS1 now carries
**Foundation**: Previous findings #9/#10 established that every variable appearing in a contract's Preconditions must be bound to its type: TS1's fix moved from `n ≥ 1, #v₁ = #v₂ = m` (free `m`, untyped `n`) to `n ∈ ℕ, n ≥ 1, #v₁ = #v₂` with explicit `n ∈ ℕ` both in the quantifier header `(A v₁, v₂ ∈ T, n ∈ ℕ : ...)` and in the Formal Contract's Preconditions list.
**ASN**: OrdinalShift's *Formal Contract* — *Preconditions:* `v ∈ T, n ≥ 1`. OrdinalDisplacement's *Formal Contract* — *Preconditions:* `n ≥ 1, m ≥ 1`. Neither list types `n` or `m` as `∈ ℕ`; the ℕ-typing is carried only by prose ("For a tumbler v ∈ T of length m = #v and natural number n ≥ 1", "For natural number n ≥ 1 and depth m ≥ 1").
**Issue**: The strict-reading standard TS1's fix adopted — every symbol in the property statement and Preconditions must be bound where used, not left to prose — applies equally to OrdinalShift and OrdinalDisplacement in the same document. Their Preconditions use `n ≥ 1` and `m ≥ 1` (comparisons presupposing an ordered set) and downstream Postconditions involve `vₘ + n` (addition presupposing both operands in ℕ) without the Preconditions placing `n` or `m` in ℕ. A reviser reading OrdinalShift's contract without its prose would encounter `n ≥ 1` against an unbound `n`, exactly the condition TS1's free-`m` finding disallowed. This is a cross-property consistency gap: three contracts in the same ASN apply different standards to numeric variables.
**What needs resolving**: OrdinalShift's Preconditions must type `n` (e.g., `v ∈ T, n ∈ ℕ, n ≥ 1`), and OrdinalDisplacement's must type both (e.g., `n ∈ ℕ, m ∈ ℕ, n ≥ 1, m ≥ 1`), matching the typing rigor TS1 now carries — or TS1's explicit `n ∈ ℕ` must be removed in favor of a uniform prose-only convention across the ASN.
