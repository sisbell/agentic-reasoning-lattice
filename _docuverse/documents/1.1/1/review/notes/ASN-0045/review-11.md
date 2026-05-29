# Review of ASN-0045

## REVISE

### Issue 1: The lower bound `0 ≤ zeros(t)` is asserted, not discharged
**ASN-0045, Well-Definedness, At-least-one**: "a cardinality is a count of elements — non-negative by construction — so `0 ≤ zeros(t)` holds by what zeros(t) is, not by any minimum-of-ℕ axiom."

**Problem**: This is the one load-bearing step left on prose. The ASN correctly proves that *none* of the cited NAT axioms names 0 as ℕ's least element, then anchors the entire at-least-one case split on `0 ≤ zeros(t)` (the first branch, `zeros(t) < 1`, applies NAT-discrete with m = 0, which requires `0 ≤ zeros(t)` as its left bound). The justification "non-negative by construction" appeals to an informal notion of cardinality. To conclude `0 = |∅| ≤ |S|` rigorously one needs monotonicity of cardinality under ⊆, which itself presupposes the ℕ-order fact being established — the appeal is circular as written. Every other inference in this document cites an axiom; this one does not, and it is exactly the kind of hand-wave the document's own standard forbids.

**Required**: Either (a) state the relied-upon property of `zeros` as an explicit cited premise (e.g., a lemma that the T4 cardinality function lands in ℕ with `zeros(t) ≥ 0` as a stipulated property of counting), or (b) derive `0 ≤ n` for all `n ∈ ℕ` from the foundation — note this requires an induction/well-ordering argument that produces 0 as the minimum, not merely NAT-wellorder's unnamed least element. Discharge it to the same standard as the rest of the proof.

### Issue 2: The `3 ≤ zeros(t) ≤ 3 ⟹ zeros(t) = 3` collapse skips antisymmetry
**ASN-0045, Well-Definedness, At-least-one**: "`2 < zeros(t)` yields `3 ≤ zeros(t)` by the derived form, which with T4's bound `zeros(t) ≤ 3` forces zeros(t) = 3."

**Problem**: The step from `3 ≤ zeros(t) ∧ zeros(t) ≤ 3` to `zeros(t) = 3` is antisymmetry of `≤`, an inference the document elsewhere spells out (e.g., excluding `3 < zeros(t)` via transitivity + irreflexivity). Given the per-step citation convention this document holds itself to, leaving this implicit is inconsistent.

**Required**: Add the one-line discharge: `3 < zeros(t)` combined with `zeros(t) < 3` would give `3 < 3` by NAT-order transitivity, contradicting irreflexivity, so `zeros(t) = 3`.

### Issue 3: Imprecise foundation citation "T4(i)"
**ASN-0045, Examples, counter-example table**: "[1,0,1,0,1,0,1,0,1] | zeros(t) = 4 > 3 violates T4(i)"

**Problem**: T4's axiom (ASN-0034) is not decomposed into numbered clauses (i)/(ii); the bound is stated as `zeros(t) ≤ 3`. The label "T4(i)" references a clause that does not exist in the foundation contract.

**Required**: Cite the clause by its content (`zeros(t) ≤ 3`) rather than an invented sub-label.

## OUT_OF_SCOPE

### Topic 1: Field-projection semantics beyond level classification
The ASN names the four level predicates but does not develop `fields(t)` projections, sub-tumbler extraction, or containment relations between levels. That belongs with field-projection or containment ASNs, not here — Partition is correctly scoped to the level-classification claim alone.

VERDICT: REVISE
