# Cone Review — ASN-0036/D-SEQ (cycle 2)

*2026-04-15 02:28*

I've read all the property files and traced every cross-cutting chain. Here are my findings.

---

### D-SEQ and VIP construct intermediates by tuple specification but omit T0 from formal preconditions, leaving T-membership undischarged

**Foundation**: T0 (CarrierSetDefinition, ASN-0034) — "T is the set of all finite sequences over ℕ with length ≥ 1"
**ASN**: D-SEQ Step 3: "the tuple w = [S, 1, …, 1, k] satisfies subspace(w) = S, #w = m, and v₁ < w < v₂ … By D-CTG (VContiguity), w ∈ V_S(d)." Also VIP sequential form proof (m = 2 case): "every [S, k] with k₁ < k < k₂ belongs to V_S(d)." Also VIP empty case: "v = [S, 1, ..., 1] of depth m."
**Issue**: D-CTG's formal invariant quantifies `(A v ∈ T : v₁ = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d))`. The `v ∈ T` guard means every application of D-CTG to a constructed intermediate requires that intermediate's T-membership to be established first. D-SEQ's Step 3 constructs `w = [S, 1, …, 1, k]` as a tuple specification and invokes D-CTG — but `w ∈ T` is never discharged. At m ≥ 3, D-CTG-depth's postcondition (2) explicitly cites "T0 (CarrierSetDefinition, ASN-0034) — each π.n is a finite sequence of naturals with length m ≥ 1, hence belongs to T," establishing the ASN's own convention that T0 is required when constructing tumblers by tuple notation. At m = 2, D-CTG-depth does not apply (its precondition requires m ≥ 3), so D-SEQ has no source for intermediate T-membership. VIP has the same gap in both its sequential-form re-derivation (which constructs the same intermediates) and its empty-case construction (where `[S, 1, ..., 1]` is not in `dom(M(d))` — the subspace is empty — so the `V_S(d) ⊆ dom(M(d)) ⊆ T` chain provides nothing). Neither D-SEQ nor VIP lists T0 in formal preconditions. The gap also affects D-SEQ's postcondition: `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}` equates a subset of T with a set of tuple specifications; the equation is well-typed only if each tuple is in T, which requires T0.
**What needs resolving**: Both D-SEQ and VIP must cite T0 (CarrierSetDefinition, ASN-0034) in their formal preconditions for tuple-constructed T-membership, matching D-CTG-depth's convention. Alternatively, the proofs could express intermediates as OrdinalShift outputs (which carry T-membership by postcondition), but this would require restructuring the argument rather than adding a citation.

---

### D-CTG-depth references "AX-4 (BaseOrdinal)" for the base-ordinal property, but no AX-4 exists — D-MIN provides this guarantee under a different name

**Foundation**: D-MIN (VMinimumPosition): "min(V_S(d)) = [S, 1, ..., 1]"
**ASN**: D-CTG-depth body text: "Nelson's specification includes a second claim beyond contiguity: that ordinal numbering begins at 1, so V_S(d) occupies {prefix.1, prefix.2, …, prefix.N} rather than an arbitrary contiguous block starting at some a ≥ 1. This base-ordinal property is independent of D-CTG and is formalized separately as AX-4 (BaseOrdinal)."
**Issue**: The `vault/3-formalization/ASN-0036/AX*` glob returns only AX-1 and AX-5 — no AX-4 exists. D-MIN is the property that asserts the minimum V-position is `[S, 1, ..., 1]` (base ordinal = 1). D-MIN's own body text describes this role: "D-MIN's axiom, together with contiguity (D-CTG) and finiteness (S8-fin), motivates a sequential structure: positions within a subspace should differ only at the last component and form a contiguous range starting at 1." D-SEQ and VIP both cite D-MIN — not AX-4 — for the base-ordinal guarantee. D-CTG-depth is the only property that references AX-4, and no other YAML `depends:` field lists it. The naming discrepancy suggests either AX-4 was renamed to D-MIN (matching the "D-" prefix convention for V-position design requirements) without updating D-CTG-depth's body text, or AX-4 was planned but replaced by D-MIN. A formalization engineer following D-CTG-depth's reference to AX-4 would find a dangling dependency.
**What needs resolving**: D-CTG-depth's body text should reference D-MIN (VMinimumPosition) instead of AX-4 (BaseOrdinal), or if AX-4 is a distinct planned property, it should be created with a clear scope statement distinguishing it from D-MIN.
