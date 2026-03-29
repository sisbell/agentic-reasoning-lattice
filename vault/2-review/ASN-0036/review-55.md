# Proof Verification: S8-depth

Looking at S8-depth, the axiom itself is a design requirement and is cleanly stated. The issue lies in the correspondence run definition.

The narrative claims:

> ordinal displacement `[x] ⊕ [k] = [x + k]` preserves the component count by construction, **so** the full I-address preserves depth and prefix when the structural context is held fixed.

That "so" is unjustified for multi-component ordinals. By TA0, `#(a ⊕ w) = #w`. For single-component ordinals, `#([x] ⊕ [k]) = #[k] = 1 = #[x]` — depth preserved. But if ordinals have depth `m > 1` (which S8-depth permits — it guarantees uniform depth, not depth 2), then `[x₁, x₂] ⊕ [k]` yields `#result = #[k] = 1 ≠ 2`. The displacement `[k]` **destroys the ordinal depth** for multi-component ordinals.

The correct depth-preserving displacement for an `m`-component ordinal is `[0, …, 0, k]` of length `m` (action point `m`), giving `(o ⊕ w)_i = o_i` for `i < m` and `(o ⊕ w)_m = o_m + k`, with `#result = m`. This mapping `δ: (k, m) ↦ [0, …, 0, k]` is not defined in S8-depth, TA7a, or any provided dependency.

The correspondence run definition's `v + k` notation therefore has no formal semantics for the general case that S8-depth's own axiom permits.

```
RESULT: FOUND

**Problem**: The correspondence run definition uses `v + k` for natural number `k`,
referencing TA7a, but TA7a's `⊕` operates on tumbler pairs. The narrative justifies
depth preservation only for single-component ordinals (`[x] ⊕ [k] = [x + k]`), then
claims "so the full I-address preserves depth" — but this generalization fails for
multi-component ordinals. Concretely: for ordinal `o = [x₁, x₂]` and displacement
`w = [k]`, TA0 gives `#(o ⊕ w) = #w = 1 ≠ 2 = #o`, changing the depth. Since
S8-depth's axiom guarantees uniform depth without constraining the depth value,
multi-component ordinals are formally permitted, and the definition is incomplete.

**Required**: Define an ordinal displacement function δ(k, m) = [0, ..., 0, k] of
length m (where m is the ordinal depth within the subspace, as guaranteed uniform by
S8-depth). Then restate the correspondence run's `v + k` as displacement by δ(k, m),
making the depth-matching explicit. This could be added to TA7a as a corollary or
defined within S8-depth's formal contract. The formal contract's Definition should
become:

  - *Definition:* δ(k, m) = [0, ..., 0, k] of length m, with actionPoint m.
    A *correspondence run* in document d is a triple (v, a, n) with n ≥ 1 such that
    (A k : 0 ≤ k < n : Σ.M(d)(v ⊕ δ(k, mᵥ)) = a ⊕ δ(k, mₐ)), where mᵥ and mₐ
    are the uniform ordinal depths of V-positions and I-address element ordinals
    respectively.
```
