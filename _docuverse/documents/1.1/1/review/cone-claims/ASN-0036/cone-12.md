The four axioms S7a, S7b, S7d, and S0 feed the main proof S7. The proof's Well-definedness, Identification, Uniqueness, and Permanence steps are each internally sound — the component-map construction is rigorous, the zero-index set is correctly enumerated, and the T4-validity discharge of origin(a) walks all four conjuncts. The cross-claim chain (S7a → T10a.4 → T4-validity; S7b → zeros = 3; T4b → projections; T0 → origin ∈ T; S7d + GlobalUniqueness → injectivity; S0 → permanence) is unbroken. One pair of per-claim dependency gaps appears by cross-comparison of the axioms, and one informal-numeral notation issue is recorded.

### S7d depends missing T4 — `zeros` function ungrounded
**Class**: REVISE
**Foundation**: T4 (HierarchicalParsing) — sole definition of `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|`
**ASN**: S7d (DocumentAllocationDiscipline) — "Every document is addressed by a document-level tumbler (`zeros = 2`)"
**Issue**: S7d's statement uses `zeros` in the expression `zeros = 2`, but T4 — the unique definition site of `zeros` — is absent from S7d's depends. T10a appears in S7d's depends, and T10a cites T4 transitively, but direct usage of `zeros` in S7d's statement requires a first-order dependency. S7b and S7 both cite T4 directly whenever `zeros` appears in their statements or proofs; S7d does not, leaving its formal contract inconsistent with the rest of the ASN.
**What needs resolving**: Add T4 (HierarchicalParsing, ASN-0034) to S7d's depends with a gloss explaining it supplies the `zeros` function used in the `zeros = 2` characterization.

---

### S7a depends missing Σ.C — quantifier domain ungrounded
**Class**: REVISE
**Foundation**: Σ.C (ContentStore) — sole definition of `dom(Σ.C)` within this ASN
**ASN**: S7a (DocumentScopedAllocation) — "for every `a ∈ dom(Σ.C)`…"
**Issue**: S7a universally quantifies over `dom(Σ.C)` but does not list Σ.C in its depends. S7b carries exactly the same quantifier pattern — `(A a ∈ dom(Σ.C) :: zeros(a) = 3)` — and correctly lists Σ.C with the gloss "supplies `dom(Σ.C)`, the set over which the universal quantifier ranges." S7a's omission leaves its formal contract incomplete and inconsistent with S7b despite identical domain usage.
**What needs resolving**: Add Σ.C (ContentStore) to S7a's depends with a gloss paralleling S7b's.

---

### S7 Well-definedness: informal numeral "5" without grounding
**Class**: OBSERVE
**Foundation**: NAT-closure (NatArithmeticClosureAndIdentity) — posits `1 ∈ ℕ` and closure under `+`
**ASN**: S7 (StructuralAttribution), Well-definedness step — "p ≥ 5 (with 5 ∈ ℕ by NAT-closure)"
**Issue**: The numeral `5` is used without being grounded through the foundation's defined numerals. T4 explicitly defines `2 := 1+1` and `3 := 2+1`; no definition of `4` or `5` appears in the provided foundations. While `5 ∈ ℕ` is derivable from NAT-closure by successive addition, the chain is not spelled out. The bound `p ≥ 5` is also stronger than T0's comprehension requires; `p ≥ 1` suffices and follows in one step from `#N(a) ≥ 1`, giving `p ≥ #N(a) + 1 ≥ 2`.
**What needs resolving**: Either ground `5` through an explicit numeral-definition chain (`4 := 3+1`, `5 := 4+1` from NAT-closure), or replace the `p ≥ 5` assertion with the weaker `p ≥ 1`, which is all T0 needs and follows immediately from T4a's `#N(a) ≥ 1`.

---

VERDICT: REVISE