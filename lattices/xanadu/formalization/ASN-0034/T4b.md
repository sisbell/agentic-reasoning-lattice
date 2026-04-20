**T4b (UniqueParse).** Under the constraints of T4 — at most three zero-valued components, no two zeros adjacent, `t₁ ≠ 0`, `t_{#t} ≠ 0` — the partial function

  `fields : T ⇀ Seq(ℕ⁺) × Seq(ℕ⁺) × Seq(ℕ⁺) × Seq(ℕ⁺)`

that decomposes a tumbler into its node, user, document, and element sub-sequences is well-defined and uniquely determined by `t` on the T4-valid subdomain, with absent fields represented by the empty sequence `ε`.

We read `fields(t)` as the 4-tuple `(N(t), U(t), D(t), E(t))` and fix the projections `N, U, D, E : T ⇀ Seq(ℕ⁺)` accordingly, each sharing the T4-valid subdomain of `fields`. Here `ℕ⁺ = {n ∈ ℕ : n > 0}`. Each projection returns a finite sequence over `ℕ⁺` on its domain: NAT-zero gives `0 ≤ tᵢ` for every component of `t` (in ℕ by T0), NAT-discrete at `m = 0` rules out `0 ≤ tᵢ < 1` when `tᵢ ≠ 0`, and T4 assigns zero the role of separator, so every field-content position is strictly positive. By T4a, for each `X ∈ {N, U, D, E}` and every T4-valid `t`, `X(t) = ε` iff field `X` is absent in `t`.

The absence pattern of `fields(t)` is fixed by case analysis on `zeros(t) ∈ {0, 1, 2, 3}`:

  - `zeros(t) = 0`: `N(t) = (t₁, ..., t_{#t})`, `U(t) = D(t) = E(t) = ε`.
  - `zeros(t) = 1`: `N(t)` and `U(t)` non-empty, `D(t) = E(t) = ε`.
  - `zeros(t) = 2`: `N(t), U(t), D(t)` non-empty, `E(t) = ε`.
  - `zeros(t) = 3`: all four non-empty.

The component-access notation `t.X₁` denotes the first component of `X(t)` and is defined iff `X(t) ≠ ε`: `t.N₁` is defined for every T4-valid `t`; `t.U₁` iff `zeros(t) ≥ 1`; `t.D₁` iff `zeros(t) ≥ 2`; `t.E₁` iff `zeros(t) = 3`.

*Derivation.* A position `i` satisfies `tᵢ = 0` iff `i` is a field separator. Forward: every separator has value 0 in the T4 address format `N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`. Reverse: if `tᵢ = 0` then T4 assigns `i` the role of separator; non-zero positions are strictly positive by NAT-zero and NAT-discrete at `m = 0` on T0's carrier ℕ, so they carry field components. Thus `{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}` is exactly the set of separator positions.

Let the zero positions in increasing order be `s₁ < s₂ < ... < s_k`, with `k = zeros(t) ∈ {0, 1, 2, 3}` by T4 and the enumeration licensed by NAT-order. Compute `fields(t)` case by case:

  - *Case k = 0.* `N(t) = (t₁, ..., t_{#t})`, `U(t) = D(t) = E(t) = ε`. Non-emptiness of `N(t)` from `#t ≥ 1` (T0).
  - *Case k = 1.* `N(t) = (t₁, ..., t_{s₁ - 1})`, `U(t) = (t_{s₁ + 1}, ..., t_{#t})`, `D(t) = E(t) = ε`. `t₁ ≠ 0` forces `s₁ ≥ 2`; `t_{#t} ≠ 0` forces `s₁ ≤ #t - 1`.
  - *Case k = 2.* `N(t) = (t₁, ..., t_{s₁ - 1})`, `U(t) = (t_{s₁ + 1}, ..., t_{s₂ - 1})`, `D(t) = (t_{s₂ + 1}, ..., t_{#t})`, `E(t) = ε`. Boundary segments as in `k = 1`; no-adjacent-zeros gives `s₂ ≥ s₁ + 2`, so `s₁ + 1 ≤ s₂ - 1`.
  - *Case k = 3.* `N(t) = (t₁, ..., t_{s₁ - 1})`, `U(t) = (t_{s₁ + 1}, ..., t_{s₂ - 1})`, `D(t) = (t_{s₂ + 1}, ..., t_{s₃ - 1})`, `E(t) = (t_{s₃ + 1}, ..., t_{#t})`. Boundary segments from `t₁ ≠ 0`, `t_{#t} ≠ 0`; interior segments from `s₂ ≥ s₁ + 2`, `s₃ ≥ s₂ + 2`.

By T3 the components of `t` are fixed, so the separator positions, field boundaries, and sub-sequences are uniquely determined. Two distinct decompositions would require two distinct separator sets; there is exactly one. Therefore `fields(t)` is well-defined and unique. ∎

*Formal Contract:*
- *Preconditions:* `t` satisfies T3 (component sequence fixed by sequence identity). `t` satisfies T4 (`zeros(t) ≤ 3`, no two zeros adjacent, `t₁ ≠ 0`, `t_{#t} ≠ 0`).
- *Definition:* `fields : T ⇀ Seq(ℕ⁺) × Seq(ℕ⁺) × Seq(ℕ⁺) × Seq(ℕ⁺)` has domain exactly the T4-valid subset of `T`. Let `s₁ < s₂ < ... < s_k` enumerate the zero positions of `t`, `k = zeros(t) ∈ {0, 1, 2, 3}`, with sentinels `s₀ = 0` and `s_{k+1} = #t + 1`. The `(i+1)`-th field segment (for `0 ≤ i ≤ k`) is `(t_{s_i + 1}, ..., t_{s_{i+1} - 1})`. Then `fields(t) = (N(t), U(t), D(t), E(t))` assigns these `k + 1` segments to the first `k + 1` components in order and `ε` to the remaining `3 - k`. Outside the T4-valid subdomain, `fields(t)` is not assigned a value.
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies ℕ as the carrier; supplies `#t ≥ 1`.
  - NAT-zero (NatZeroMinimum) — supplies `0 ≤ tᵢ` for every component.
  - NAT-discrete (NatDiscreteness) — at `m = 0`, promotes non-zero components to strictly positive.
  - NAT-order (NatStrictTotalOrder) — licenses the strictly increasing enumeration of zero positions and the inequality manipulations on them.
  - T3 (CanonicalRepresentation) — fixes the component values of `t`, licensing the uniqueness conclusion.
  - T4 (HierarchicalParsing) — supplies `zeros(t) ≤ 3`, the boundary and no-adjacent-zeros clauses, and the separator role of zero-valued positions.
  - T4a (SyntacticEquivalence) — supplies the absence-marker equivalence: `X(t) = ε` iff field `X` is absent in `t`.
- *Postconditions:* `fields` is a partial function with domain the T4-valid subset of `T`. On that subdomain `fields(t) = (N(t), U(t), D(t), E(t))` is well-defined and uniquely determined by `t`. Each projection `N, U, D, E : T ⇀ Seq(ℕ⁺)` shares that subdomain and returns a finite sequence over `ℕ⁺`; absent fields are represented by `ε`, and by T4a this marker is unambiguous. Absence pattern: `zeros(t) = 0` → only `N(t)` non-empty; `zeros(t) = 1` → `N(t), U(t)` non-empty; `zeros(t) = 2` → `N(t), U(t), D(t)` non-empty; `zeros(t) = 3` → all four non-empty. The component-access notation `t.X₁` is defined iff `X(t) ≠ ε`: `t.N₁` always; `t.U₁` iff `zeros(t) ≥ 1`; `t.D₁` iff `zeros(t) ≥ 2`; `t.E₁` iff `zeros(t) = 3`. Outside the T4-valid subdomain, `fields(t)` has no value; consumers must carry T4-validity as a precondition.
