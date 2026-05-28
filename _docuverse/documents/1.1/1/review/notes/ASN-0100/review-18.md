# Review of ASN-0100

## REVISE

### Issue 1: Worked example misstates `coverage` as a finite address set
**ASN-0100, A Worked Example (projection-shift correspondence)**: "endset `e_1` whose coverage is exactly `{a₂, a₃, a₄}`" and the later trace uses "coverage(e_1) = {a₂, a₃, a₄}" (e.g., "a₃, a₄ ∈ coverage(e_1) but a₅ ∉ coverage(e_1)").

**Problem**: The endset is delivered by "the canonical span `(a_2, δ(3, #a_2))`". By the `coverage` definition (ASN-0098), `coverage((a_2, δ(3,#a_2))) = {t ∈ T : a_2 ≤ t < a_5}` — the full half-open *tumbler interval*, which strictly contains `{a₂, a₃, a₄}` (e.g., any descendant `a_2.x` lies in the interval by T5). It is *not* a three-element set. The quantity that equals `{a₂, a₃, a₄}` is `coverage(e_1) ∩ ran(M(d))`, not `coverage(e_1)`. The downstream membership facts (`a₅ ∉ coverage`, `a_new ∉ coverage`) happen to be correct because those specific addresses fall outside the interval, but the characterisation of `coverage` itself is wrong — and this is the ASN's one concrete verification of its key projection postcondition, where Dijkstra-level precision is mandatory.

**Required**: State the endset's coverage as the interval `[a_2, a_5)` and write `project(ℓ,1,d,Σ) = coverage(e_1) ∩ ran(M(d)) = {a₂,a₃,a₄}`; reserve `coverage(e_1) = {a₂,a₃,a₄}`-style equalities for sets that are genuinely three-element (e.g., three width-1 spans).

### Issue 2: `δ(0, m_C)` invoked in the functionality disjointness arithmetic
**ASN-0100, Verifying the Invariants → Arrangement functionality (S2)**: "the final component is `(shift(p, k))_{m_C} = p_{m_C} + δ(k, m_C)_{m_C} = p_m + k` for `0 ≤ k < n`."

**Problem**: `δ(n, m)` is defined only for `n ≥ 1` (OrdinalDisplacement, ASN-0034). At `k = 0` the expression `δ(0, m_C)` is undefined, so the cited "OrdinalShift definition `shift(p,k) = p ⊕ δ(k, m_C)`" does not apply over the full range `0 ≤ k < n`. The S8a and S8-depth verifications elsewhere in the ASN correctly split `k = 0` (using OrdinalShiftBase `shift(p,0) = p`) from `k ≥ 1`, but the functionality disjointness paragraph applies the displacement formula uniformly, leaving the `k = 0` Insertion position (last component `= p_m`) on undischarged footing.

**Required**: Split the `k = 0` case here as done in the S8a/S8-depth sections — invoke `shift(p,0) = p` (OrdinalShiftBase) for the `k = 0` last component `p_m`, and the `p ⊕ δ(k, m_C)` arithmetic only for `k ≥ 1`.

## OUT_OF_SCOPE

None. Link-subspace insertion (K.μ⁺_L), COPY, DELETE, REARRANGE, version creation, and replication are all correctly bounded in the Scope section and Open Questions rather than specified here.

VERDICT: REVISE
