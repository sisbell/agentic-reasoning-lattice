# Cone Review — ASN-0036/S8 (cycle 1)

*2026-04-14 16:20*

### V-positions not formally placed in carrier set T

**Foundation**: OrdinalShift (precondition: `v ∈ T, n ≥ 1`); T1 (defined on T); T5, T10 (arguments in T)
**ASN**: S8's partition proof, S8-depth's correspondence run definition — throughout
**Issue**: S8's proof applies OrdinalShift to V-positions (`shift(v, 1)` for `v ∈ dom(M(d))`), invokes T1's lexicographic order on V-positions, and feeds V-positions into T5/T10. Every one of these operations requires its arguments to be elements of the carrier set T. S8-depth similarly applies OrdinalShift to I-addresses in the correspondence run definition. No axiom in the ASN states `dom(M(d)) ⊆ T` or that I-addresses are elements of T. S8a constrains V-position component values and S8-depth refers to "tumbler depth," but the formal contracts define V-positions only as elements of `dom(M(d))` — an abstract set whose relationship to T is implicit. The membership is inferrable (S8a's constraints produce values consistent with T0's definition), but the chain `v ∈ dom(M(d)) → v ∈ T` is never closed. This is not a local gap in one proof — it is a foundational assumption underlying every property in the ASN simultaneously.
**What needs resolving**: An axiom (or definition of `M(d)`) that formally places V-positions and I-addresses in T, so that OrdinalShift, T1, T5, and T10 can be invoked with a complete precondition chain.

---

### S8-vdepth omitted from S8-depth's formal preconditions

**Foundation**: OrdinalShift (prefix rule: `shift(v, k)ᵢ = vᵢ` for `i < #v`)
**ASN**: S8-depth Postcondition 1: `"S8-vdepth guarantees #v ≥ 2, so 1 < #v and OrdinalShift's prefix rule copies the subspace identifier at position 1 unchanged."`
**Issue**: S8-depth's formal preconditions section documents what Postcondition 3 requires (S3, S7b, S7c) but is silent about what Postcondition 1 requires. The dependency on S8-vdepth (`#v ≥ 2`) appears only inline within Postcondition 1's text. Postcondition 1 is false without it: at `#v = 1`, `shift(v, k)₁ = v₁ + k ≠ v₁`, so the subspace identifier changes and subspace preservation fails. A consumer checking S8-depth's formal preconditions section to determine what must hold before invoking the postconditions would miss this critical constraint.
**What needs resolving**: S8-depth's formal preconditions section should list S8-vdepth (or the condition `#v ≥ 2`) explicitly as a precondition for Postcondition 1, parallel to how S3/S7b/S7c are listed for Postcondition 3.

---

### Depth-1 subspace status unresolved between S8 and S8-depth

**Foundation**: T1 (used in S8's m=1 case analysis); OrdinalShift (prefix rule requires `i < #v`)
**ASN**: S8's proof, cross-subspace uniqueness: `"For m = 1, each subspace S contains at most one V-position..."` vs. S8-depth Postcondition 1: `"S8-vdepth guarantees #v ≥ 2"`
**Issue**: S8's decomposition proof treats depth-1 subspaces as a live case, devoting a dedicated argument (the entire m=1 cross-subspace block, including the three-way case analysis against `[S₁+1]`) to proving the partition holds at depth 1. S8-depth's Postcondition 1 treats depth-1 as excluded via S8-vdepth (`#v ≥ 2`). The ASN never states which is true. If S8-vdepth is an axiom (depth-1 impossible), the entire m=1 block in S8's proof is vacuously true dead code and should be documented as such. If S8-vdepth is not an axiom (depth-1 possible), then S8-depth's Postcondition 1 is conditional — subspace preservation holds only when `#v ≥ 2` — and downstream consumers must check depth before relying on it. The ASN provides no way to resolve this.
**What needs resolving**: The ASN should state whether depth-1 V-position subspaces are permitted by the model. If yes, S8-depth's postconditions need explicit conditionality. If no, S8-vdepth should appear as a defined axiom, and S8's m=1 case should note it is vacuous under that axiom.
