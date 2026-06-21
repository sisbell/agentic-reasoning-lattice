# Claim Formal Contract — ASN-0053/SC — run 1

*2026-06-20T22:04:24Z*
*Model: opus*
*Cycles: 1*
*Validation: MATCH*

## Validation detail

(no detail)

## Review-rewrite detail

(passed)

## Final LLM response

**SC** (*SpanClassification*). Given spans α and β, their relationship is determined by comparing starts and reaches under T1. Since T1 is a total order, five mutually exclusive cases arise:

(i) *Separated.* reach(α) < start(β) or reach(β) < start(α). The spans share no positions and have space between them.

(ii) *Adjacent.* reach(α) = start(β) or reach(β) = start(α). The spans share no positions but touch at a single boundary point.

(iii) *Proper overlap.* The spans share positions but neither contains the other: start(α) < start(β) < reach(α) < reach(β), or symmetrically.

(iv) *Containment.* One span's denotation is a proper subset of the other's: start(α) ≤ start(β) and reach(β) ≤ reach(α) with at least one inequality strict, or symmetrically.

(v) *Equal.* start(α) = start(β) and reach(α) = reach(β).

Cases (i) and (ii) are the *disjoint* cases — ⟦α⟧ ∩ ⟦β⟧ = ∅. Cases (iii), (iv), and (v) are the *overlapping* cases — ⟦α⟧ ∩ ⟦β⟧ ≠ ∅.

*Exhaustiveness.* Assume without loss of generality that start(α) ≤ start(β); configurations with start(α) > start(β) yield the same case with α, β exchanged, since each case clause is either symmetric (cases (i), (ii), (v)) or carries an explicit "or symmetrically" rider (cases (iii), (iv)). Compare reach(α) with start(β): if reach(α) < start(β), case (i); if reach(α) = start(β), case (ii); if reach(α) > start(β), the spans share positions. In the sharing case, compare start(α) with start(β): if start(α) < start(β), compare reach(α) with reach(β) — reach(α) < reach(β) gives case (iii), reach(α) ≥ reach(β) gives case (iv). If start(α) = start(β), compare reaches — reach(α) = reach(β) gives case (v), otherwise case (iv). Every ordering of the four boundary points {start(α), reach(α), start(β), reach(β)}, subject to start < reach for each span, falls into exactly one case.

*Disjointness and overlap.* It remains to show that this case split coincides with the emptiness of ⟦α⟧ ∩ ⟦β⟧, where a span's denotation is the half-open set of positions ⟦γ⟧ = { p : start(γ) ≤ p < reach(γ) } — the convention forced by case (ii), in which the boundary point shared by reach(α) = start(β) belongs to neither span. Continue under the assumption start(α) ≤ start(β).

In case (i), reach(α) < start(β): every p ∈ ⟦α⟧ satisfies p < reach(α) < start(β) ≤ q for every q ∈ ⟦β⟧, so no position lies in both and ⟦α⟧ ∩ ⟦β⟧ = ∅. In case (ii), reach(α) = start(β): every p ∈ ⟦α⟧ satisfies p < reach(α) = start(β), so p ∉ ⟦β⟧, and again ⟦α⟧ ∩ ⟦β⟧ = ∅. These are the disjoint cases.

In case (iii), start(α) < start(β) < reach(α) < reach(β): the position start(β) satisfies start(α) ≤ start(β) < reach(α), so start(β) ∈ ⟦α⟧, and start(β) < reach(β), so start(β) ∈ ⟦β⟧; hence start(β) ∈ ⟦α⟧ ∩ ⟦β⟧ ≠ ∅. In case (iv) with α the larger span, start(α) ≤ start(β) and reach(β) ≤ reach(α): every q ∈ ⟦β⟧ satisfies start(α) ≤ start(β) ≤ q < reach(β) ≤ reach(α), so ⟦β⟧ ⊆ ⟦α⟧; since start(β) < reach(β) makes ⟦β⟧ nonempty, ⟦α⟧ ∩ ⟦β⟧ = ⟦β⟧ ≠ ∅. In case (v), start(α) = start(β) and reach(α) = reach(β): ⟦α⟧ = ⟦β⟧, which is nonempty because start(α) < reach(α); hence ⟦α⟧ ∩ ⟦β⟧ ≠ ∅. These are the overlapping cases. The symmetric configurations (start(α) > start(β), or β the larger span in case (iv)) follow by exchanging α and β throughout. ∎

*Formal Contract:*

- *Preconditions:* α and β are spans whose starts and reaches lie in the domain of the total order T1, each non-degenerate: start(α) < reach(α) and start(β) < reach(β).
- *Postconditions:* Exactly one of the five cases (i)–(v) holds. Moreover the case determines intersection emptiness: ⟦α⟧ ∩ ⟦β⟧ = ∅ iff the case is (i) or (ii), and ⟦α⟧ ∩ ⟦β⟧ ≠ ∅ iff the case is (iii), (iv), or (v).
- *Definition:* The denotation of a span γ is the half-open position set ⟦γ⟧ = { p : start(γ) ≤ p < reach(γ) } (reach exclusive); this is the convention under which adjacency (reach(α) = start(β)) shares no position.
- *Axiom:* T1 — positions are totally ordered, so any two of the four boundary points {start(α), reach(α), start(β), reach(β)} are comparable, which is what makes the case split exhaustive and the cases mutually exclusive.
- *Frame:* Classification reads only the four boundary points start(α), reach(α), start(β), reach(β); it neither modifies α, β, nor their denotations.
