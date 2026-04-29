# Regional Review — ASN-0034/Divergence (cycle 1)

*2026-04-24 05:01*

### T1's Depends omits NAT-closure
**Class**: REVISE
**Foundation**: (foundation ASN; internal)
**ASN**: T1 (LexicographicOrder), *Formal Contract → Depends*. The Depends list enumerates T0, T3, NAT-order, NAT-addcompat, NAT-cancel, NAT-discrete, and NAT-wellorder; NAT-closure is absent.
**Issue**: T1's Definition, prose, and proof use symbols that NAT-closure alone posits directly: the literal `1 ∈ ℕ` (throughout `1 ≤ k`, `1 ≤ i < k`, and in the Definition's `k = #a + 1 ≤ #b`), and the binary `+` closed over ℕ (every `m + 1`, `n + 1`, `#a + 1`). NAT-addcompat, NAT-cancel, and NAT-discrete each *declare* NAT-closure in their own Depends to ground these same symbols, and NAT-cancel's prose explicitly articulates the convention ("NAT-zero is named directly rather than reached transitively through NAT-closure, matching the precedent NAT-closure itself sets"). T1 consumes `1` and `+` at identical arity but names NAT-closure only transitively through its order-compat/discreteness citations. T0's own Depends declares NAT-closure directly for the single literal `1` in `1 ≤ #a`; T1 uses `1` more heavily and should follow the same precedent.
**What needs resolving**: Either declare NAT-closure directly in T1's Depends with a citation that names the specific supplied symbols (`+ : ℕ × ℕ → ℕ` closing `m + 1`, `n + 1`, `#a + 1`; `1 ∈ ℕ` grounding the literal `1`), or, if the convention permits transitive sourcing in some cases, state where the line is drawn and why T1 sits on the permissive side while T0 does not.

### T3 prose statement has a floating variable `n`
**Class**: REVISE
**Foundation**: (foundation ASN; internal)
**ASN**: T3 (CanonicalRepresentation) — "`(A a, b ∈ T : a₁ = b₁ ∧ ... ∧ aₙ = bₙ ∧ #a = #b ≡ a = b)`".
**Issue**: The index `n` appearing in `aₙ = bₙ` is not bound by the outer quantifier `(A a, b ∈ T : ...)`, nor is it tied to `#a` or `#b` before use. The `...` ellipsis obscures what range of positions is being equated — reading literally, `n` is free, and the conjunction `... ∧ #a = #b` sits at the same level as the ellipsis so it cannot be the binder. The Formal Contract's postcondition `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)` is precise; the prose statement is not, and T3 is cited by T1 as the bridge between component-level agreement and tumbler equality, so the prose ambiguity is read at every invocation site.
**What needs resolving**: Bring the prose statement into correspondence with the Formal Contract — either quantify `i` explicitly over `1 ≤ i ≤ #a` (with `#a = #b` as a separate conjunct) or replace the ellipsis with the universally-quantified form used in the contract.

VERDICT: REVISE
