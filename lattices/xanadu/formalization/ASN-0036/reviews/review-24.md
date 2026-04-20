# Formalize — ASN-0036 / V_S(d)

*2026-04-13 12:21*

**V_S(d) (SubspaceVPositionSet).** The set of V-positions in subspace S of document d:

`V_S(d) = {v ∈ dom(Σ.M(d)) : v₁ = S}`

V_S(d) partitions dom(Σ.M(d)) by subspace identifier. Every element of V_S(d) satisfies S8a (V-position well-formedness): zeros(v) = 0, v₁ ≥ 1, v > 0. Within V_S(d), all positions share a common depth by S8-depth.

*Proof.* The definition filters dom(Σ.M(d)) on first component; we verify the three claimed consequences.

**Partition.** We show the family {V_S(d) : S ≥ 1} partitions dom(Σ.M(d)). *Coverage:* by S8a (V-position well-formedness), every v ∈ dom(Σ.M(d)) satisfies v₁ ≥ 1, so v ∈ V_{v₁}(d) — every V-position belongs to at least one member of the family. *Disjointness:* if v ∈ V_S(d) ∩ V_{S'}(d), then v₁ = S and v₁ = S', hence S = S'. The sets are pairwise disjoint. Together: dom(Σ.M(d)) = ∪{V_S(d) : S ≥ 1}, and the union is disjoint.

**S8a satisfaction.** Every v ∈ V_S(d) is, by construction, an element of dom(Σ.M(d)). S8a quantifies universally over dom(Σ.M(d)), so zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0 holds for each such v. The filter condition v₁ = S selects a subset of a domain whose elements already satisfy S8a; it adds no new constraint.

**Common depth.** All positions in V_S(d) share the first component v₁ = S, so they extend the single-component prefix [S]. S8-depth (MinimalVPositionDepth) establishes that within any subspace, all V-positions share a common depth. Since V_S(d) is precisely the set of V-positions in subspace S, S8-depth applies directly: there exists a depth δ_S such that #v = δ_S for all v ∈ V_S(d). ∎

*Formal Contract:*
- *Definition:* `V_S(d) = {v ∈ dom(Σ.M(d)) : v₁ = S}` for subspace identifier S ≥ 1 and document d.
- *Preconditions:* S8a — every v ∈ dom(Σ.M(d)) satisfies zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0; S8-depth (MinimalVPositionDepth) — within any subspace, all V-positions share a common depth.
- *Postconditions:* {V_S(d) : S ≥ 1} partitions dom(Σ.M(d)) into pairwise disjoint sets; every v ∈ V_S(d) satisfies S8a; all positions in V_S(d) share common depth δ_S with #v = δ_S for all v ∈ V_S(d).
