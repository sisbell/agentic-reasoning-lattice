# Regional Review — ASN-0034/T4a (cycle 8)

*2026-04-22 02:51*

### T4b's Depends credits T4a with inequalities outside T4a's stated Postcondition
**Foundation**: T4a's stated Postcondition — "The three positional conditions (i), (ii), (iii) hold if and only if every field segment of `t` is non-empty."
**ASN**: T4b Formal Contract Depends: "T4a (SyntacticEquivalence) — field-segment non-emptiness (reverse direction of T4's field-segment constraint) yielding `s₁ ≥ 2`, `s_k ≤ #t - 1`, `s_{j+1} ≥ s_j + 2`." T4b Formal Contract Definition: "The segment-length inequalities `s₁ ≥ 2`, `s_k ≤ #t - 1` (when `k ≥ 1`), and `s_{j+1} ≥ s_j + 2` (T4a's reverse direction) keep every index `s_i ± 1` appearing above within `{1, …, #t}`."
**Issue**: T4a's Postcondition is the biconditional between positional conditions and segment non-emptiness. The three inequalities `s₁ ≥ 2`, `s_k ≤ #t − 1`, `s_{j+1} ≥ s_j + 2` appear as intermediate steps inside T4a's Forward and Reverse proofs but are not named as outputs of T4a's contract. A downstream claim can cite only an upstream claim's exported postconditions; T4b's Depends and Definition slots attribute these inequalities to T4a directly, parenthetically labeling them "T4a's reverse direction" as if they were the reverse direction's output. The actual output of the reverse direction is "every field segment is non-empty" — T4b must itself perform the re-expression from segment non-emptiness to the inequalities.
**What needs resolving**: Either extend T4a's Postcondition to explicitly export the position-inequalities `s₁ ≥ 2`, `s_k ≤ #t − 1`, `s_{j+1} ≥ s_j + 2`, or rewrite T4b's Depends and Definition so T4a supplies only segment non-emptiness, with T4b performing (and justifying) the re-expression to inequalities as a local step.

### T4a and T4b use `+2` and `−1` arithmetic without axiomatic basis
**Foundation**: NAT-zero (`0 ∈ ℕ`, `0 ≤ n`), NAT-discrete (`m < n → m + 1 ≤ n`), NAT-order (strict total order, `≤` derived). None defines `+` as a function on ℕ, closure of `+`, `−`, or the numerals `2, 3`.
**ASN**: T4a proof: "therefore `s₁ ≥ 2`", "`s_k ≤ #t − 1`", "`s_{i+1} ≥ s_i + 2`". T4b proof and Definition: case `k = 1` uses `t_{s₁ − 1}` and `t_{s₁ + 1}`; case `k ≥ 2` uses `s_{j+1} ≥ s_j + 2`; Definition: "`s_i ± 1` appearing above". T4 Axiom: "`zeros(t) ≤ 3`" — numeral `3`.
**Issue**: NAT-discrete employs `m + 1` and thus tacitly introduces a successor, but this is the only appearance of `+` in the foundations. The operations `+ 2` (two successors), `− 1` (predecessor), and the numerals `2` and `3` have no grounding in any axiom in scope. Previous findings note that T4c explicitly cites an unstated NAT-addcompat for `n < n + 1`; here the same gap appears in T4a and T4b, whose Depends lists do not even cite NAT-addcompat and which nonetheless use arithmetic operators and numerals beyond what NAT-discrete implicitly allows. A precise reader cannot verify that `s_k ≤ #t − 1` is well-typed, let alone derivable.
**What needs resolving**: Either introduce an axiom (e.g., NAT-addcompat with closure of `+`, definition of `−` via `+` inverse where defined, and numerals `1, 2, 3` as `0 + 1`, `1 + 1`, `2 + 1`) and cite it in T4, T4a, T4b's Depends, or recast the inequalities and canonical-form indices to avoid `+ 2`, `− 1`, and the numerals `2, 3` (e.g., by expressing `s_{j+1} ≥ s_j + 2` as "there exists an index strictly between `s_j` and `s_{j+1}`").

## Result

Regional review not converged after 8 cycles.

*Elapsed: 10048s*
