Reading the ASN as a system before reporting.

**S3 (ReferentialIntegrity).** The two-case induction (inherited via J0+S1; new/redirected via AX-2) is exhaustive and the case boundary is correct. The domain guard in AX-2's second disjunct is well-placed: `Σ.M(d)(v)` is only evaluated after `v ∈ dom(Σ.M(d))` is established. Base case is vacuous under AX-1. Proof is sound.

**S2, S0, AX-1, AX-2, S1.** All posits or trivial definitional unfoldings. No gaps.

**S8a.** NAT-card applies correctly: `{i : 1 ≤ i ≤ #t ∧ tᵢ = 0} ⊆ {1,…,#t} ⊆ ℕ`, so `|·|` is within NAT-card's defined scope. The `zeros(t) = 0 ⟺ (A i : tᵢ > 0)` derivation via NAT-card empty-set characterization and NAT-zero is sound.

**OrdShiftHom.** Part (a) routes through TumblerAdd's copy rule at position 1 < m (from m ≥ 2); part (b) uses OrdinalShift's exported lower bound at the action point instead of re-deriving from ℕ arithmetic. Both precondition discharge chains (TumblerAdd's `actionPoint(δ(n,m)) = m ≤ #v`, OrdinalDisplacement's positivity) are complete. Proof is sound.

**S8-depth.** Acknowledged as a design posit ungrounded for non-text subspaces. OrdShiftHom frame (`#shift(v,1) = #v`, ultimately TA0) grounds the per-step depth preservation without invoking S8-depth's domain-restricted quantifier. No circularity in the current text.

**S8.** The succ-confinement step, injectivity (via TS2 after locally deriving `#u = #u'` from shift's frame), acyclicity (TS4 + T1 irreflexivity), and chain decomposition are all sound. The displacement identity induction handles i=0 via the convention and i≥1 via TS3, with TS3's preconditions (both shift amounts ≥ 1) correctly satisfied in the i≥1 branch. Partition (coverage, disjointness, finiteness) is complete. The convention `shift(t,0) := t` is consistent with OrdinalShift's postconditions and does not conflict with TS3 or TS4, whose preconditions exclude n=0.

One genuine gap:

---

### S8-fin applies `|·|` to a set of tumblers outside NAT-card's defined scope
**Class**: REVISE
**Foundation**: NAT-card (NatFiniteSetCardinality)
**ASN**: S8-fin (FiniteArrangement) — axiom `(A d :: |dom(Σ.M(d))| ∈ ℕ)`
**Issue**: NAT-card axiomatizes `|S|` exclusively for `S ⊆ {j ∈ ℕ : 1 ≤ j ≤ n}` — subsets of initial segments of ℕ. S8-fin applies the same `|·|` notation to `dom(Σ.M(d)) ⊆ T`, a set of tumblers. T is the carrier set of finite sequences over ℕ, not a subset of ℕ, so dom(M(d)) falls outside NAT-card's stated domain. S8-fin carries no Depends entry and cites no foundation that extends cardinality to arbitrary finite sets. The axiom therefore invokes an operator outside its grounded scope. Contrast with S8a and T4, which apply `|·|` to index sets `{i : 1 ≤ i ≤ #t ∧ tᵢ = 0} ⊆ ℕ` — within NAT-card's domain — and with S8's proof, which consumes S8-fin only as the property "dom(M(d)) is finite," never as a numeric cardinality value, showing that the axiom's intent outstrips what `|·|` can deliver here.
**What needs resolving**: Replace the `|·|`-based formulation with one that stays within grounded notation. One direct option: posit existence of a bijection — "for every reachable state Σ and every document d, there exists n ∈ ℕ and a bijection f: {j ∈ ℕ : 1 ≤ j ≤ n} → dom(Σ.M(d))" — which expresses finiteness using only NAT-carrier and T0's typed sets. Alternatively, if a general cardinality operator covering arbitrary finite sets is needed elsewhere in the ASN family, introduce it as a named foundation and cite it in S8-fin's Depends. S8's proof requires only the finiteness property (forward walks terminate, decomposition is finite), so either formulation supports the downstream argument without change.

VERDICT: REVISE