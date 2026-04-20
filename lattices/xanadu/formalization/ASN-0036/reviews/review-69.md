# Cone Review — ASN-0036/S8 (cycle 5)

*2026-04-14 18:31*

I'll read the ASN content carefully against the foundation statements.

### S8-depth: subscript notation `v₁` overloaded between axiom and postconditions within the same formal contract

**Foundation**: T1, T3 (use `aᵢ` consistently as component access — subscript always means position)
**ASN**: S8-depth axiom: `(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)` — here `v₁` and `v₂` are **bound tumbler variables**. S8-depth postcondition 1: `(A k : 0 ≤ k < n : (v + k)₁ = v₁)` — here `v₁` is **component access** (first component of `v`). S8 proof text: `v₁ = S₁` — **component access**. S8 postcondition: `(E! j :: vⱼ ≤ v < vⱼ + nⱼ)` — subscript `j` is a **run index**.
**Issue**: Within S8-depth's formal contract, the symbol `v₁` means "a quantified tumbler" in the axiom and "the first component of tumbler `v`" in the postconditions. A formalizer translating the contract into TLA+ or Dafny encounters the same token with two meanings in the same property's specification. The foundation properties (T1, T3) use subscripts exclusively for component access (`aᵢ`, `bᵢ`), establishing a convention that the axiom breaks. The ambiguity extends across properties: S8 uses subscripts for run indexing (`vⱼ`, `aⱼ`, `nⱼ`) and component access (`v₁ = S₁`) within the same proof. A mechanical translation must disambiguate three subscript roles — variable naming, component access, and collection indexing — with no syntactic distinction between them.
**What needs resolving**: Use distinct variable names in S8-depth's axiom (e.g., `u, w` or `p, q`) so that subscripts uniformly mean component access, matching the convention established by the foundation properties.

## Result

Cone converged after 6 cycles.

*Elapsed: 13370s*
