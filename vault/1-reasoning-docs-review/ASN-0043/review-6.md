# Review of ASN-0043

## REVISE

### Issue 1: L13 exclusion proof — incorrect equality in greater-depth case

**ASN-0043, Reflexive Addressing, exclusion proof, greater-depth case**: "If `t` does not extend `b`, there exists `k ≤ #b` with `t_k ≠ b_k`. As `t ≥ b`, we have `t_k > b_k = (b ⊕ ℓ_b)_k`, giving `t > b ⊕ ℓ_b` — outside the interval."

**Problem**: The equality `b_k = (b ⊕ ℓ_b)_k` holds only for `k < #b`. At the action point `k = #b`, TumblerAdd gives `(b ⊕ ℓ_b)_{#b} = b_{#b} + 1`, not `b_{#b}`. The same-depth case immediately above correctly splits `k < #b` and `k = #b` with distinct arguments; the greater-depth case applies the `k < #b` reasoning uniformly across all `k ≤ #b`, which is invalid at the action point.

The conclusion is correct. At `k = #b`: `t_{#b} > b_{#b}` gives `t_{#b} ≥ b_{#b} + 1 = (b ⊕ ℓ_b)_{#b}`. If strict: `t > b ⊕ ℓ_b` by T1(i). If equal: `t` agrees with `b ⊕ ℓ_b` at all `#b` positions and `#t > #(b ⊕ ℓ_b) = #b`, so `b ⊕ ℓ_b` is a proper prefix of `t`, giving `b ⊕ ℓ_b < t` by T1(ii). Either way `t ≥ b ⊕ ℓ_b`, contradicting the interval bound. But this two-subcase argument is absent from the proof.

**Required**: Split the greater-depth case at `k = #b`, mirroring the same-depth case. The `k = #b` subcase needs both the strict and prefix-equality branches.

### Issue 2: L9 witness — unsupported `g ≠ a` justification

**ASN-0043, TypeGhostPermission witness**: "Since `g ∉ dom(Σ.C) ∪ dom(Σ.L)` and `g ≠ a` (they occupy different subspaces or different documents), `g ∉ dom(Σ'.C) ∪ dom(Σ'.L)`."

**Problem**: The parenthetical asserts that `g` and `a` occupy different subspaces or different documents, but the construction places no constraint on `g`'s subspace or document — only that `g ∉ dom(Σ.C) ∪ dom(Σ.L)`. If `g` happens to fall in subspace `s_L` within document `d`, it could coincide with the freshly allocated `a`.

**Required**: Constrain the choice of `g` — e.g., require `fields(g).E₁ = s_C` so that T7 gives `g ≠ a` — or note that `g` can always be chosen to differ from the single address `a` since `T` is infinite.

## OUT_OF_SCOPE

None beyond the topics the ASN already identifies in its scope section and open questions.

VERDICT: REVISE
