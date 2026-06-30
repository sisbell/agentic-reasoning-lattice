## Audit

The posits (S8a, D-CTG, S8-depth, S8-fin) are correctly labeled as design constraints. The definitions (Σ.M(d), subspace, V-sub) are clean and grounded. NAT-induction is correctly identified as an augmentation of ASN-0034's NAT-* group, with its gap from the order-and-addition axioms properly motivated.

**D-PRED:** The H-set construction is sound. The successor-closure step uses the presentation `k+1` directly (witness i = k) without consulting `k ∈ H`, correctly avoiding circularity. The exclusion of j = 0 via the mixed chain `0 < 1 ≤ j ⟹ 0 < j` is correctly built inline from NAT-order's ≤-definition rather than a missing mixed-transitivity postcondition.

**D-INJ:** The shifted induction via W = {P ∈ ℕ : P < 1 ∨ L.P} is correctly structured. The k = 0 successor-closure step correctly invokes L.1 as an independently established base, not the induction hypothesis. The ρ-injectivity argument correctly handles all three placement cases; the same-branch upper case correctly uses NAT-cancel when order compatibility would leave a collision admissible. The surjectivity's "successor reflection" lemma `n+1 ≤ m+1 ⟹ n ≤ m` is correctly derived inline via NAT-order's ≤-split, NAT-cancel for the equality sub-case, and NAT-addcompat + irreflexivity for the strict sub-case. The prepend-μ construction's three strictly-increasing cases (seam, beyond, spanning) are complete and correctly closed.

**D-CTG-depth:** The WLOG is sound: the interior disagreement set is symmetric, and the construction anchored on the smaller member refutes either ordering identically. The k = j pinning correctly handles k = 1 (shared subspace) and 2 ≤ k < j (NAT-discrete places k in the interior range, minimality of j gives agreement). The witness construction's zeros(w) = 0 check correctly draws from S8a's positivity Consequence for copied components, NAT-order transitivity for the new component, and NAT-closure's 0 < 1 for the tail. The N+1 applications of T0(a) produce a strictly increasing run (each nₖ > nₖ₋₁), the witnesses are pairwise distinct by T3, and the D-INJ instantiation at P := N+1, n := N is correctly guarded via NAT-zero + NAT-addcompat + NAT-closure's left identity.

---

### D-INJ Depends missing NAT-carrier
**Class**: OBSERVE
**Foundation**: NAT-carrier (NatCarrierSet, ASN-0034)
**ASN**: D-INJ Formal Contract Depends
**Issue**: D-INJ's formal statement universally quantifies `n ∈ ℕ` and `P ∈ ℕ` and uses the initial-segment sets `{k ∈ ℕ : 1 ≤ k ≤ P}` and `{j ∈ ℕ : 1 ≤ j ≤ n}` — the same pattern for which NAT-card cites "NAT-carrier — supplies ℕ as the underlying set appearing in the outer membership clause n ∈ ℕ, in the initial-segment domain" and S8-fin cites it analogously. D-INJ omits NAT-carrier. D-PRED similarly omits it, which may indicate a deliberate convention distinguishing derived lemmas from posits, but the inconsistency is observable against NAT-card, S8-fin, and NAT-induction.
**What needs resolving**: Either add NAT-carrier to D-INJ's Depends with the same rationale used in NAT-card and S8-fin, or document the convention that derived lemmas do not cite NAT-carrier directly (and verify D-PRED is consistently treated). N/A if the omission is intentional and the convention is settled.

---

### S8a T4 Depends entry omits numeral 2
**Class**: OBSERVE
**Foundation**: T4 (HierarchicalParsing, ASN-0034)
**ASN**: S8a Formal Contract Depends — T4 entry: "supplies the symbol `zeros` and its zero-count definition `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|`"
**Issue**: S8a's axiom contains `#t ≥ 2`, and the body grounds the numeral `2` via "T4's `2 := 1+1`". T4 is cited, so the grounding is present. But the T4 Depends description covers only `zeros`; a reader checking what S8a draws from T4 would find no mention of `2`. The numeral and its justification (`2 ∈ ℕ` from NAT-closure applied twice to `1 ∈ ℕ`) are defined in T4's Definition section and consumed in S8a's axiom.
**What needs resolving**: Extend the T4 Depends entry in S8a to note that T4 also supplies the numeral `2 := 1+1` used in the depth clause `#t ≥ 2` of the axiom.

VERDICT: OBSERVE