The proofs are well-structured at the macro level. The five-case SC split is exhaustive and mutually exclusive under T1. WF is applied correctly in both S11c cases, with level-uniformity and reach identity properly derived. S11's boundary characterisation, tightness argument, and element-chasing proof are all sound. S11a and S11b are trivially correct. S11d's case synthesis is faithful to the sub-lemmas. The concrete examples check out arithmetically. Three issues remain.

---

### S11c Case 2 — ⊇ direction of the set equality is unestablished

**Class**: REVISE
**Foundation**: TumblerSub, T1 (transitivity of the ordering), via the Case 2 hypothesis start(β) < start(α) < reach(β) < reach(α)
**ASN**: S11c, Case 2 element-chase: "Therefore ⟦α⟧ \ ⟦β⟧ = {t : reach(β) ≤ t < reach(α)}"
**Issue**: The proof partitions t ∈ ⟦α⟧ by whether t < reach(β) and shows t ∈ ⟦β⟧ iff t < reach(β). That gives ⟦α⟧ \ ⟦β⟧ = {t ∈ ⟦α⟧ : t ≥ reach(β)} = {t : start(α) ≤ t < reach(α) ∧ reach(β) ≤ t}. The proof then silently drops the start(α) ≤ t guard and asserts equality with {t : reach(β) ≤ t < reach(α)}. This requires the ⊇ inclusion: for every t with reach(β) ≤ t < reach(α), that start(α) ≤ t. The step follows from start(α) < reach(β) ≤ t (Case 2 hypothesis gives start(α) < reach(β)) by T1 transitivity, but is not stated.
**What needs resolving**: The ⊇ direction must be established explicitly: the Case 2 hypothesis start(α) < reach(β) must be cited, and the chain start(α) < reach(β) ≤ t must be traced to conclude start(α) ≤ t before equating {t ∈ ⟦α⟧ : t ≥ reach(β)} with {t : reach(β) ≤ t < reach(α)}.

---

### S11c — T1 absent from Depends despite direct transitivity invocations

**Class**: REVISE
**Foundation**: T1 (LexicographicOrder) — transitivity of the strict order
**ASN**: S11c Formal Contract, Depends section; invocations appear in Case 1 ("t ∈ ⟦α⟧ since start(α) ≤ t < start(β) < reach(α)" and "start(β) ≤ t < reach(α) < reach(β), so t ∈ ⟦β⟧") and Case 2 (the comparison of t with reach(β))
**Issue**: Both element-chasing proofs invoke T1 transitivity directly — not via SC. SC supplies the case taxonomy (the ordering of the four boundary points); it does not supply the step-by-step transitivity reasoning applied to a fresh variable t drawn from ⟦α⟧. S11 (DifferenceBound) cites T1 explicitly for its comparable element-chasing ("supplies the strict total order whose totality partitions ⟦α⟧"). S0 (Convexity) cites T1 for exactly the same reason. S11c is inconsistent with this pattern and the formal dependency graph is missing the T1 edge.
**What needs resolving**: T1 must be added to S11c's Depends with a note that its transitivity underwrites the element-chasing in both sub-cases.

---

### S11d — T1 absent from Depends despite direct transitivity invocation in the SC(iv)-reverse inline proof

**Class**: REVISE
**Foundation**: T1 (LexicographicOrder) — transitivity of ≤ and <
**ASN**: S11d proof, SC(iv)-reverse sub-case: "for t ∈ ⟦α⟧, start(β) ≤ start(α) ≤ t and t < reach(α) ≤ reach(β), so t ∈ ⟦β⟧"
**Issue**: The conclusion t ∈ ⟦β⟧ is derived by two applications of T1 transitivity: start(β) ≤ start(α) ≤ t gives start(β) ≤ t, and t < reach(α) ≤ reach(β) gives t < reach(β). This is an inline proof step that directly invokes T1, not one delegated to SC or any listed sub-lemma. T1 is not in S11d's Depends.
**What needs resolving**: T1 must be added to S11d's Depends, identifying its transitivity as the axiom underpinning the SC(iv)-reverse inline derivation.

---

VERDICT: REVISE