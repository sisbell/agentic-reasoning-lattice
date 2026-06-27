Reading the foundation statements, then the ASN claims as a system.

---

**Dependency chain audit**

The central logical path is: S8-depth (shared depth axiom) → first postcondition of D-CTG-depth (shared prefix) → reduction step (guard collapses to component m) → second postcondition. I traced the proof of D-CTG-depth in full. The contradiction argument (infinitely many intermediates via T0(a) + D-CTG, contra S8-fin) is sound. T0 comprehension licenses w ∈ T; S8a verification on w is correct for all j ∈ [2, m−1] including the j = m−1 edge (empty third clause, last component covered by wⱼ₊₁ = n > uₘ ≥ 1). The T3 distinctness step is correct. The reduction step correctly handles j = 1 via the subspace guard and j ∈ [2, m−1] via first-postcondition agreement and T1 trichotomy. OrdShiftHom's proof is sound: the m ≥ 2 precondition places position 1 in the copy region for part (a); part (b)'s S8a chain closes via OrdinalShift's exported lower bound on the action-point component.

---

### D-CTG-depth formal contract missing precise second postcondition
**Class**: REVISE
**Foundation**: T1 (LexicographicOrder), D-CTG-depth first postcondition
**ASN**: D-CTG-depth Formal Contract — *Postconditions* second bullet: *"Contiguity of V_1(d) is determined by component m alone, structurally identical to the depth-2 case."*
**Issue**: The proof body establishes a formal result — *"D-CTG's guard u < v < x is therefore equivalent to the single ordinal betweenness uₘ < vₘ < xₘ"* — that is the primary output D-SEQ will consume. The formal contract's second postcondition is an informal gloss on that result, not a citable formal statement. A downstream claim cannot formally instantiate or cite an informal postcondition; D-SEQ would be forced to re-derive the reduction or invoke it without anchor. The first postcondition is precisely stated (`A u, x ∈ V_1(d) : A i : 2 ≤ i ≤ m−1 : uᵢ = xᵢ`); the second should be as well. The proof already contains the necessary formal content — it is a matter of promoting the body's result into the contract.
**What needs resolving**: State the second postcondition precisely in the formal contract, to the effect: for any u, x ∈ V_1(d) with u < x and any v ∈ T with `#v = m ∧ subspace(v) = 1 ∧ zeros(v) = 0`, the comparison `u < v < x` holds if and only if `uₘ < vₘ < xₘ`. The body proof already establishes this; the formal contract must export it.

---

### S8-depth axiom scope exceeds evidential grounding
**Class**: OBSERVE
**Foundation**: S8-depth (FixedDepthVPositions)
**ASN**: S8-depth formal statement — *"(A d, u, w : u ∈ dom(Σ.M(d)) ∧ w ∈ dom(Σ.M(d)) ∧ subspace(u) = subspace(w) : #u = #w)"* with justification *"Gregory's evidence supports it: V-addresses in the text subspace consistently use the form s.x"*.
**Issue**: The axiom quantifies over all subspaces (`subspace(u) = subspace(w)` is unconstrained), but the cited evidence only grounds depth uniformity for the text subspace (the s.x, i.e., depth-2, form). For link or annotation subspaces, depth uniformity is neither argued from evidence nor stated as an independent design decision. Nothing in this ASN consumes S8-depth for a non-text subspace, so this creates no soundness gap here. But if a future ASN applies S8-depth to link positions, it will be drawing on an ungrounded portion of the axiom.
**What needs resolving**: Either scope S8-depth to the text subspace and add separate axioms for other subspaces when evidence is available, or explicitly note that the axiom is a blanket design constraint asserting depth-per-subspace uniformity for all subspaces by fiat (not by evidence), and record what evidence would be needed to ground it for non-text subspaces.

---

### T0(a) invocation in D-CTG-depth does not name the instantiation
**Class**: OBSERVE
**Foundation**: T0(a) (UnboundedComponentValues)
**ASN**: D-CTG-depth proof — *"T0(a) (UnboundedComponentValues, ASN-0034) supplies, for any natural-number bound M, one witness n ∈ ℕ with n > M."*
**Issue**: T0(a)'s postcondition delivers not a bare natural number but a tumbler t' ∈ T satisfying t'ᵢ > M at a chosen component index i, agreeing with some supplied t at all other positions. The proof treats T0(a) as if it directly yields an arbitrary large ℕ element, without naming which tumbler t and which index i are supplied. The instantiation (e.g., take t = u, i = j+1, then set n = t'_{j+1}) is unambiguous in context but is never written. The result is correct; this is an underspecified proof step.
**What needs resolving**: Name the tumbler and index at which T0(a) is instantiated so the extraction of the large natural number n is explicit. Alternatively, note that NAT-addcompat (n < n+1) directly supplies ℕ-unboundedness without requiring T0(a)'s tumbler machinery, and cite the simpler lemma.

---

VERDICT: REVISE