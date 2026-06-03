# Review of ASN-0091

## REVISE

### Issue 1: The "value-uniform ⟺ M'(d) = M(d)" equivalence is false

**ASN-0091, "REARRANGE as Vstream-Only Operation" (case split into Non-trivial / Collapse):**
> "*Non-trivial case* — `M'(d) ≠ M(d)`, equivalently `M(d)` restricted to the affected range `[c₀, c_{n−1}) ∩ V_S(d)` is not value-uniform."
> "*Collapse case* — `M'(d) = M(d)` with π ≠ id, arising exactly when the affected range is value-uniform."

**Problem**: The claimed equivalence (and the "exactly when") is wrong. REARRANGE_K's cut-driven permutation is a *block rotation* (pivot: `new = β ++ α`) or *block swap* (4-cut: `new = β ++ μ ++ α`). Such a permutation fixes the arrangement whenever the affected-range value sequence is **invariant under that rotation/swap**, which is strictly weaker than value-uniformity (a single I-address everywhere).

Concrete counterexample, admissible under S5 (UnrestrictedSharing). Take a 3-cut pivot with `w_α = w_β = 2` (cuts `c₀`, `c₁ = c₀+2`, `c₂ = c₀+4`) and pre-state
```
c₀ ↦ a,  c₀+1 ↦ b,  c₀+2 ↦ a,  c₀+3 ↦ b   (a ≠ b)
```
Applying R-P1/R-P2:
- R-P1 (`0 ≤ j < w_β = 2`): `M'(c₀) = M(c₁) = a`, `M'(c₀+1) = M(c₁+1) = b`
- R-P2 (`0 ≤ j < w_α = 2`): `M'(c₀+2) = M(c₀) = a`, `M'(c₀+3) = M(c₀+1) = b`

Post-state is identical to pre-state, so `M'(d) = M(d)`, yet the affected range `{a, b, a, b}` is **not value-uniform** (it contains two distinct I-addresses). This refutes both "equivalently ... is not value-uniform" and "arising exactly when ... value-uniform."

This is not a harmless mislabeling. The ASN routes the *Non-trivial case* (defined as "not value-uniform") through K.μ~ as realiser and asserts "K.μ~'s admissibility clause (ii) `M'(d) ≠ M(d)` holds." For the counterexample above the range is not value-uniform (so the ASN classifies it Non-trivial) but `M'(d) = M(d)`, so clause (ii) **fails** and K.μ~ cannot fire — the named realiser is invalid exactly where the ASN claims it applies. The downstream statement "REARRANGE_K ... collapsing to the identity transition precisely on value-uniform affected ranges" is likewise wrong: it also collapses on rotation/swap-invariant ranges.

**Required**: Replace the value-uniformity criterion with the correct one. `M'(d) = M(d)` holds iff the affected-range value sequence is invariant under the cut-induced block rotation (pivot) or block swap (4-cut) — for the pivot, periodicity with period `gcd(w_α, w_α+w_β)`; for the 4-cut swap, positional equality of the α- and β-blocks (with `w_α = w_β`) together with arbitrary μ. Then re-derive which configurations land in the Non-trivial case (K.μ~ realiser, clause (ii) genuinely satisfied) versus the Collapse case (identity transition). Every RE-* claim still holds in both cases, but the realisation argument and the case boundary must be corrected.

### Issue 2: Reverse direction of the bijection-class characterization asserted without proof

**ASN-0091, "REARRANGE as Vstream-Only Operation"**:
> "The reverse direction reconstructs RA-π pointwise from the per-block bijection condition."

**Problem**: The forward direction is given four explicit sub-inferences (a)–(d); the reverse direction of the stated biconditional gets one sentence with no work shown. Standard 1 ("No proof by 'similarly'") applies — if the characterization is stated as an iff, both directions need to be discharged.

**Required**: Show the reverse construction explicitly (given a family of per-block bijections `Σ.M(d)⁻¹(a) → Σ'.M(d)⁻¹(a)`, assemble the global π and verify RA-π holds at each `v`), or downgrade the claim to the forward implication actually used.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
The ASN restricts the cut subspace to `S = s_C` (via CS3) and treats link-subspace effects only as a frame property (RE-sub). An operation that rearranges the link subspace, and the invariants it must preserve, is genuine future territory — correctly listed in Open Questions, not an error here.

### Topic 2: Net cardinality bounds across multi-step sequences
RE-frag★/RE-coal★/RE-eq★ deliberately assert only per-step direction arbitrariness, not a bound on net run-cardinality change. The upper-bound question is flagged in Open Questions and belongs to a future ASN.

VERDICT: REVISE
