## Audit

**D-CTG (VContiguity).** Posit. Depends list grounds every symbol in the formal statement (V-sub for V₁(d), subspace for the first-component guard, T4 for zeros, T1 for <, T0 for the carrier T and #·). Well-formed.

**subspace (VPositionSubspaceIdentifier).** Definition. T0 grounds #· and the component projection; T0's nonemptiness clause discharges the depth guard. Complete.

**V-sub (SubspaceProjection).** Definition. Σ.M(d) grounds dom(Σ.M(d)); subspace grounds the membership filter. Complete.

**Σ.M(d) (Arrangement).** Stub definition only; no formal contract to audit.

**S8-fin (FiniteArrangement).** Posit. Cites NAT-carrier (for ℕ), NAT-closure (for 1 ∈ ℕ), NAT-order (for < and ≤ in index domain and injectivity clause), T0 (for carrier T). The bijection formulation avoids NAT-card's out-of-scope domain. Depends are consistent with the formal statement and with the pattern used elsewhere.

**S8-depth (FixedDepthVPositions).** Posit. Formal statement uses dom(Σ.M(d)) (Σ.M(d)), subspace(·) (subspace), #· (T0), and S8a for the well-formedness domain restriction. No `≥` or numerals appear in the formal statement itself. Depends complete.

**S8a (ArrangementDomainRestriction).** Posit. See finding below.

**D-CTG-depth (SharedPrefixReduction).** Proof by contradiction. The logical structure is sound: assume u < x in V₁(d) disagree at some interior j; extract j minimal by NAT-wellorder; show the T1 witness k equals j; construct w by copying u through component j, placing a fresh n > uⱼ₊₁ at j+1, and filling j+2…m with 1; verify u < w < x and zeros(w) = 0; apply D-CTG to land w ∈ V₁(d); iterate via T0(a) to get infinitely many distinct w's; contradict S8-fin. See finding below.

---

### S8a Depends missing NAT-order for the ≥ symbol
**Class**: REVISE
**Foundation**: NAT-order (NatStrictTotalOrder) — defines `m ≥ n ⟺ n ≤ m`
**ASN**: S8a formal axiom — `dom(Σ.M(d)) ⊆ {t ∈ T : zeros(t) = 0 ∧ #t ≥ 2}`
**Issue**: The `≥` in `#t ≥ 2` is the companion relation defined by NAT-order (`m ≥ n ⟺ n ≤ m`). NAT-order is not in S8a's Depends list. S8-fin, which uses `≤` and `<` in a structurally parallel role, cites NAT-order directly; S8a does not. The numeral `2 ∈ ℕ` is grounded through T4 (which defines `2 := 1+1` in its formal contract and is in S8a's Depends). The relation symbol `≥` is not.
**What needs resolving**: Add NAT-order (NatStrictTotalOrder) to S8a's Depends list, with a note that it supplies the `≥` companion relation used in the `#t ≥ 2` clause of the axiom.

---

### D-CTG-depth Depends missing NAT-addcompat; backward direction of the j+1 ≤ m ⟺ j < m equivalence is ungrounded
**Class**: REVISE
**Foundation**: NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality `(A n ∈ ℕ :: n < n + 1)`
**ASN**: D-CTG-depth proof, two steps: (1) "clause (ii) would demand the impossible m + 1 ≤ m"; (2) "NAT-discrete's discreteness of ℕ… makes the additive interior bound j + 1 ≤ m and the strict comparison j < m interchangeable on ℕ"
**Issue**: Both steps require `n < n + 1` (NAT-addcompat), which is not in D-CTG-depth's Depends list.

Step (1): ruling out T1 clause (ii) when `#u = #x = m` requires showing `m + 1 ≤ m` is impossible. This needs `m < m + 1` (NAT-addcompat at `n := m`); combined with NAT-order's trichotomy, it makes `m + 1 ≤ m` false. No other listed foundation supplies `m < m + 1`.

Step (2): the proof claims NAT-discrete alone makes `j + 1 ≤ m` and `j < m` interchangeable. NAT-discrete supplies only the forward direction (`j < m ⟹ j + 1 ≤ m`). The backward direction (`j + 1 ≤ m ⟹ j < m`) requires `j < j + 1` (NAT-addcompat) followed by NAT-order's transitivity of `<`. This backward direction is used in the `w < x` branch, where `k = j ≤ min(m, m) = m` is derived from the interior bound `j + 1 ≤ m`.

**What needs resolving**: Add NAT-addcompat (NatAdditionOrderAndSuccessor) to D-CTG-depth's Depends list. The Depends entry should note: (a) the strict successor inequality `n < n + 1` instantiated at `n := m` to discharge impossibility of `m + 1 ≤ m` (ruling out T1 clause (ii)); and (b) the same inequality instantiated at `n := j`, combined with NAT-order transitivity, to derive `j < m` from the interior bound `j + 1 ≤ m` in the `w < x` branch. The prose claim that NAT-discrete alone makes the two forms interchangeable should be corrected to name NAT-addcompat as the additional ingredient for the backward direction.

---

VERDICT: REVISE