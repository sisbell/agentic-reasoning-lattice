**SC** (*SpanClassification*). Given spans α and β, their relationship is determined by comparing starts and reaches under T1. Since T1 is a total order, five mutually exclusive cases arise:

(i) *Separated.* reach(α) < start(β) or reach(β) < start(α). The spans share no positions and have space between them.

(ii) *Adjacent.* reach(α) = start(β) or reach(β) = start(α). The spans share no positions but touch at a single boundary point.

(iii) *Proper overlap.* The spans share positions but neither contains the other: start(α) < start(β) < reach(α) < reach(β), or symmetrically.

(iv) *Containment.* One span's denotation is a proper subset of the other's: start(α) ≤ start(β) and reach(β) ≤ reach(α) with at least one inequality strict, or symmetrically.

(v) *Equal.* start(α) = start(β) and reach(α) = reach(β).

Cases (i) and (ii) are the *disjoint* cases — ⟦α⟧ ∩ ⟦β⟧ = ∅. Cases (iii), (iv), and (v) are the *overlapping* cases — ⟦α⟧ ∩ ⟦β⟧ ≠ ∅.

*Exhaustiveness.* Assume without loss of generality that start(α) ≤ start(β); configurations with start(α) > start(β) yield the same case with α, β exchanged, since each case clause is either symmetric (cases (i), (ii), (v)) or carries an explicit "or symmetrically" rider (cases (iii), (iv)). Compare reach(α) with start(β): if reach(α) < start(β), case (i); if reach(α) = start(β), case (ii); if reach(α) > start(β), the spans share positions. In the sharing case, compare start(α) with start(β): if start(α) < start(β), compare reach(α) with reach(β) — reach(α) < reach(β) gives case (iii), reach(α) ≥ reach(β) gives case (iv). If start(α) = start(β), compare reaches — reach(α) = reach(β) gives case (v), otherwise case (iv). Every ordering of the four boundary points {start(α), reach(α), start(β), reach(β)}, subject to start < reach for each span, falls into exactly one case.
