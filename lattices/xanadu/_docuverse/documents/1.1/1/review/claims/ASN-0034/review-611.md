# Cone Review — ASN-0034/TA3 (cycle 5)

*2026-04-26 07:27*

### Case B's preamble instantiates ZPD's padded equality at an index that may exceed `L_{b,w}`
**Class**: REVISE
**Foundation**: (n/a — internal)
**ASN**: TA3, Case B preamble (the proof that `d_b = zpd(b, w)` is well-defined):

> "were `b` zero-padded-equal to `w`, ZPD's padded equality would give `b̂_{dₐ} = ŵ_{dₐ}`, hence `â_{dₐ} > b̂_{dₐ}`; chaining ZPD's pre-divergence agreement `âᵢ = ŵᵢ` for `i < dₐ` with the hypothesised `b̂ᵢ = ŵᵢ` gives `âᵢ = b̂ᵢ` for `i < dₐ`."

ZPD's "zero-padded-equal" predicate is `(A i : 1 ≤ i ≤ L_{b,w} : b̂ᵢ = ŵᵢ)`. Instantiating it at `i = dₐ` (and at any `i < dₐ` in the chaining step) requires the index to lie in `1..L_{b,w}`. The preamble has only the hypothesis-free bound `dₐ ≤ #a` at this point — `dₐ ≤ #b` is *derived later in the same block* via the `dₐ ≤ j` argument. We have no a-priori bound `dₐ ≤ L_{b,w} = max(#b, #w)`.

**Issue**: The chain `b̂_{dₐ} = ŵ_{dₐ}` and the chain `b̂ᵢ = ŵᵢ for i < dₐ` are both unjustified instantiations of ZPD's padded equality at indices not yet shown to lie in its range. There is no obstruction to `#a > max(#b, #w)` in Case B (T1 case (i) for `a < b` only constrains `j ≤ #a ∧ j ≤ #b`, not `#a` versus `#b` or `#w`), so `dₐ ≤ L_{b,w}` is not derivable from the hypothesis-free `dₐ ≤ #a` alone. The subsequent step that forces `dₐ ≤ j ≤ #b` itself depends on the chain `âᵢ = b̂ᵢ for i < dₐ`, which already used the unjustified instantiations — circularity. (As it happens, `H ∧ a ≥ w ∧ a < b ∧ a` not zpd-equal to `w` is itself contradictory, so the gap does not yield a wrong final conclusion. But the prose's specific dₐ-routed argument does not walk a sound path.)

**What needs resolving**: Either (a) establish `dₐ ≤ L_{b,w}` independently before instantiating H — e.g., via Case B's witness `j ≤ #b ≤ L_{b,w}` together with `dₐ ≤ j` argued without relying on H, or directly from `a ≥ w ∧ a < b ∧ a` not zpd-equal to `w`; or (b) refute `H` via Case B's witness `j` directly (instantiate `b̂_j = ŵ_j` at `j ≤ #b ≤ L_{b,w}`, then case on `j ≤ #w` to derive `aⱼ ≥ wⱼ ≥ bⱼ` or `aⱼ = 0 = bⱼ`, contradicting `aⱼ < bⱼ`) without routing through `dₐ`.

VERDICT: REVISE
