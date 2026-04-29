# Cone Review — ASN-0034/TS1 (cycle 1)

*2026-04-18 06:36*

### TS1 cites a TA1-strict precondition that does not exist in TA1-strict's contract
**Foundation**: TA1-strict (StrictOrderPreservation) — Preconditions: `a ∈ T, b ∈ T, w ∈ T, a < b, Pos(w), actionPoint(w) ≤ #a, actionPoint(w) ≤ #b, actionPoint(w) ≥ divergence(a, b)`
**ASN**: TS1 precondition check (iii): "actionPoint(δ(n, m)) ≤ min(#v₁, #v₂) — the action point of δ(n, m) is m (OrdinalDisplacement), and min(#v₁, #v₂) = min(m, m) = m, so m ≤ m holds."
**Issue**: TA1-strict's contract demands the *conjunction* `actionPoint(w) ≤ #a ∧ actionPoint(w) ≤ #b` (two separate inequalities, exactly as TA1-strict's proof and Depends repeatedly emphasize), not a single inequality against a primitive `min(#a, #b)`. TS1 has rewritten the precondition to use a binary-minimum operator that the ASN explicitly disclaims — Divergence's Definition prose: "stated without invoking any primitive binary-minimum operator on ℕ", and TA1-strict's case-(ii) rule-out goes through a multi-step trichotomy detour for the express purpose of avoiding `min`.
**What needs resolving**: TS1 must discharge the two TA1-strict precondition conjuncts separately (`actionPoint(w) ≤ #v₁` and `actionPoint(w) ≤ #v₂`) without introducing a `min` operator that no listed NAT-* axiom supplies.

### TS1 redefines `divergence` using a primitive `min` that contradicts Divergence's contract
**Foundation**: Divergence — case (i) defines `divergence(a, b) = k` as the unique index satisfying `aₖ ≠ bₖ ∧ (A i : 1 ≤ i < k : aᵢ = bᵢ)`, with case-(i) least-element existence sourced to NAT-wellorder; the Definition prose explicitly avoids any primitive binary-minimum operator on ℕ.
**ASN**: TS1 precondition check (iv): "case (i) applies: divergence(v₁, v₂) = min({j : 1 ≤ j ≤ m ∧ v₁ⱼ ≠ v₂ⱼ}), which satisfies divergence(v₁, v₂) ≤ m."
**Issue**: This rewrites Divergence case (i) using a `min` over a set, dropping the prior-position-agreement conjunct that Divergence's contract requires for `k` to qualify, and importing the very minimization operator Divergence's contract is structured to avoid (Divergence routes least-element selection through NAT-wellorder, not `min`). Two parts of the same ASN therefore disagree about what `divergence` denotes.
**What needs resolving**: TS1 must reach the bound `divergence(v₁, v₂) ≤ m` through Divergence's actual contract — case (i)'s defining bound `k ≤ #v₁ = m` (or via NAT-wellorder applied to the qualifying ℕ-subset) — rather than by re-defining the function with `min`.

### TS1 verifies four TA1-strict preconditions but TA1-strict has eight
**Foundation**: TA1-strict — Preconditions: `a ∈ T, b ∈ T, w ∈ T, a < b, Pos(w), actionPoint(w) ≤ #a, actionPoint(w) ≤ #b, actionPoint(w) ≥ divergence(a, b)` (eight items).
**ASN**: TS1 proof: "We verify the four preconditions of TA1-strict with w = δ(n, m): (i) v₁ < v₂ — given. (ii) δ(n, m) > 0 … (iii) actionPoint(δ(n, m)) ≤ min(#v₁, #v₂) … (iv) actionPoint(δ(n, m)) ≥ divergence(v₁, v₂) …"
**Issue**: TS1 silently fuses several of TA1-strict's preconditions into composite items (notably `actionPoint(w) ≤ #a ∧ actionPoint(w) ≤ #b` collapsed into one `min`-flavoured item, and the membership preconditions `a ∈ T, b ∈ T, w ∈ T` not discharged at the call site). OrdinalShift, by contrast, explicitly walks through "the four preconditions of TA0" with each membership conjunct discharged. The asymmetry leaves TS1's TA1-strict invocation under-discharged against the contract TA1-strict actually exports.
**What needs resolving**: TS1 must enumerate and discharge TA1-strict's preconditions one-for-one as TA1-strict states them, including the three membership preconditions and the two separate length bounds.

### TS1 uses `δ(n, m) > 0` where TA1-strict requires `Pos(w)`
**Foundation**: TA1-strict precondition `Pos(w)`; TA-Pos defines positivity as the existential `(E i : tᵢ ≠ 0)`; OrdinalDisplacement's contract exports `Pos(δ(n, m))` directly.
**ASN**: TS1 precondition check (ii): "δ(n, m) > 0 — by OrdinalDisplacement, δ(n, m) = [0, ..., 0, n] with n ≥ 1, so its m-th component is positive."
**Issue**: `δ(n, m) > 0` is an order comparison against a "0" tumbler that is not in scope (T0 stipulates length ≥ 1 with components in ℕ, but no zero-tumbler is named, and `<` on T is T1's lexicographic order, not a comparison to a scalar 0). TA1-strict consumes the predicate `Pos(w)`, which OrdinalDisplacement already exports and TS1 should cite directly. The two notations are not definitionally identified anywhere in the ASN.
**What needs resolving**: TS1 must discharge TA1-strict's precondition under its actual name `Pos(δ(n, m))`, citing OrdinalDisplacement's exported `Pos(δ(n, m))` postcondition, rather than introducing an unspecified `> 0` comparison.

### TS1 Depends omits foundations that the per-step citation discipline requires
**Foundation**: TA1-strict's Depends explicitly justifies listing T0 even though T0 flows transitively through Divergence/T1/ActionPoint/TumblerAdd/TA0: "The per-step citation discipline … requires T0 to be listed here rather than left to flow transitively". OrdinalShift's Depends similarly enumerates T0, NAT-zero, NAT-addcompat, NAT-closure, NAT-order despite the same transitivity being available.
**ASN**: TS1 *Depends* lists only OrdinalShift, OrdinalDisplacement, Divergence, TA1-strict.
**Issue**: TS1 directly consumes T0 (lengths `#v₁`, `#v₂`, the equation `#v₁ = #v₂ = m`, component projection `v₁ⱼ ≠ v₂ⱼ`, membership `v₁, v₂ ∈ T`), T1 (`v₁ < v₂` is the lex order), TA-Pos (the `Pos(δ)` it discharges at TA1-strict precondition (ii)), NAT-order (its case-(iv) reasoning compares lengths and indices and excludes Divergence case (ii) via `#v₁ = #v₂`), and NAT-wellorder (any least-element use in case-(iv)'s bound). None are cited. This violates the same per-step discipline TA1-strict and OrdinalShift document.
**What needs resolving**: TS1's Depends must enumerate the foundations consumed at each step it executes, not delegate them transitively to the lemmas it invokes.

### Declared Depends list at the ASN level is empty
**Foundation**: ASN Metadata "**Declared depends**: " is blank; the ASN is presented as a foundation ASN with internal-only review.
**ASN**: TA1-strict's, OrdinalShift's, OrdinalDisplacement's, Divergence's, TS1's per-property Depends collectively cite T0, T1, T3, TA-Pos, TA0, TumblerAdd, ActionPoint, NAT-zero, NAT-order, NAT-addcompat, NAT-cancel, NAT-closure, NAT-wellorder.
**Issue**: A foundation ASN with no declared dependencies whose properties cite a dozen external foundations (T0, T1, T3, NAT-* family, TA-Pos, TA0, TumblerAdd, ActionPoint) is internally inconsistent: either these foundations live inside this ASN (in which case their definitions should appear here, but only Divergence and OrdinalDisplacement and OrdinalShift are defined, while T0/T1/T3/NAT-*/TA-Pos/TA0/TumblerAdd/ActionPoint are merely cited), or the ASN depends on other ASNs that should appear in the header's Declared depends list.
**What needs resolving**: Reconcile the empty Declared depends with the per-property Depends citations — either by adding the genuinely external foundations to the ASN-level dependency list, or by clarifying which cited names refer to definitions located elsewhere in this same ASN.
