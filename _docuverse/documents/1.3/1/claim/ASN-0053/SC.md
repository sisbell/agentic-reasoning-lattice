**SC (SpanClassification).** Given spans α and β, their relationship is determined by comparing starts and reaches under T1.

We first fix this vocabulary at its source. By the Span definition (ASN-0034), a span σ is a pair (s, ℓ) — a start address s ∈ T together with a positive length ℓ whose action point satisfies actionPoint(ℓ) ≤ #s — denoting the address-set span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}. The projections start(σ) = s and width(σ) = ℓ are read off this pair, and the displaced endpoint is reach(σ) = start(σ) ⊕ width(σ) = s ⊕ ℓ. Before we compare it, we must know that reach(σ) is itself a position, i.e. that s ⊕ ℓ ∈ T; this is postcondition (a) of T12 (SpanWellDefinedness, ASN-0034), which discharges s ⊕ ℓ ∈ T for every pair meeting the Span preconditions, so reach(σ) ∈ T is inherited rather than assumed. The companion postcondition (b), s ∈ span(s, ℓ), unfolds to start(σ) < reach(σ): the non-degeneracy we invoke below is therefore a consequence of well-formedness, not an extra hypothesis. We abbreviate the denotation ⟦σ⟧ = span(start(σ), width(σ)) = {p : start(σ) ≤ p < reach(σ)}; since reach(σ) is grounded before ⟦σ⟧ refers to it, this bracket is well-defined, not circular.

Since T1 is a total order, five mutually exclusive cases arise:

(i) *Separated.* reach(α) < start(β) or reach(β) < start(α). The spans share no positions and have space between them.

(ii) *Adjacent.* reach(α) = start(β) or reach(β) = start(α). The spans share no positions but touch at a single boundary point.

(iii) *Proper overlap.* The spans share positions but neither contains the other: start(α) < start(β) < reach(α) < reach(β), or symmetrically.

(iv) *Containment.* One span's denotation is a proper subset of the other's: start(α) ≤ start(β) and reach(β) ≤ reach(α) with at least one inequality strict, or symmetrically.

(v) *Equal.* start(α) = start(β) and reach(α) = reach(β).

Cases (i) and (ii) are the *disjoint* cases — ⟦α⟧ ∩ ⟦β⟧ = ∅. Cases (iii), (iv), and (v) are the *overlapping* cases — ⟦α⟧ ∩ ⟦β⟧ ≠ ∅.

*Exhaustiveness.* Assume without loss of generality that start(α) ≤ start(β); configurations with start(α) > start(β) yield the same case with α, β exchanged, since each case clause is either symmetric (cases (i), (ii), (v)) or carries an explicit "or symmetrically" rider (cases (iii), (iv)). Compare reach(α) with start(β): if reach(α) < start(β), case (i); if reach(α) = start(β), case (ii); if reach(α) > start(β), the spans share positions. In the sharing case, compare start(α) with start(β): if start(α) < start(β), compare reach(α) with reach(β) — reach(α) < reach(β) gives case (iii), reach(α) ≥ reach(β) gives case (iv). If start(α) = start(β), compare reaches — reach(α) = reach(β) gives case (v), otherwise case (iv). Every ordering of the four boundary points {start(α), reach(α), start(β), reach(β)}, subject to start < reach for each span, falls into exactly one case.

*Disjointness and overlap.* It remains to show that this case split coincides with the emptiness of ⟦α⟧ ∩ ⟦β⟧. Recall the denotation fixed above, ⟦γ⟧ = span(start(γ), width(γ)) = { p : start(γ) ≤ p < reach(γ) }, half-open with reach excluded — the convention forced by case (ii), in which the boundary point reach(α) = start(β) belongs to exactly one of the two spans: it is β's included start, hence in ⟦β⟧, but equals α's excluded reach, hence not in ⟦α⟧, so the two spans share no position. Continue under the assumption start(α) ≤ start(β).

In case (i), reach(α) < start(β): every p ∈ ⟦α⟧ satisfies p < reach(α) < start(β) ≤ q for every q ∈ ⟦β⟧, so no position lies in both and ⟦α⟧ ∩ ⟦β⟧ = ∅. In case (ii), reach(α) = start(β): every p ∈ ⟦α⟧ satisfies p < reach(α) = start(β), so p ∉ ⟦β⟧, and again ⟦α⟧ ∩ ⟦β⟧ = ∅. These are the disjoint cases.

In case (iii), start(α) < start(β) < reach(α) < reach(β): the position start(β) satisfies start(α) ≤ start(β) < reach(α), so start(β) ∈ ⟦α⟧, and start(β) < reach(β), so start(β) ∈ ⟦β⟧; hence start(β) ∈ ⟦α⟧ ∩ ⟦β⟧ ≠ ∅. In case (iv) with α the larger span, start(α) ≤ start(β) and reach(β) ≤ reach(α): every q ∈ ⟦β⟧ satisfies start(α) ≤ start(β) ≤ q < reach(β) ≤ reach(α), so ⟦β⟧ ⊆ ⟦α⟧; since start(β) < reach(β) makes ⟦β⟧ nonempty, ⟦α⟧ ∩ ⟦β⟧ = ⟦β⟧ ≠ ∅. In case (v), start(α) = start(β) and reach(α) = reach(β): ⟦α⟧ = ⟦β⟧, which is nonempty because start(α) < reach(α); hence ⟦α⟧ ∩ ⟦β⟧ ≠ ∅. These are the overlapping cases. The symmetric configurations (start(α) > start(β), or β the larger span in case (iv)) follow by exchanging α and β throughout. ∎

*Formal Contract:*

- *Preconditions:* α and β are spans in the sense of the Span definition (ASN-0034) — each a pair (start, width) meeting Span's preconditions — so that, by T12, their starts and reaches lie in T, the domain of the total order T1, and each is non-degenerate: start(α) < reach(α) and start(β) < reach(β).
- *Postconditions:* Exactly one of the five cases (i)–(v) holds. Moreover the case determines intersection emptiness: ⟦α⟧ ∩ ⟦β⟧ = ∅ iff the case is (i) or (ii), and ⟦α⟧ ∩ ⟦β⟧ ≠ ∅ iff the case is (iii), (iv), or (v).
- *Definition:* The denotation of a span γ is ⟦γ⟧ = span(start(γ), width(γ)) = { p : start(γ) ≤ p < reach(γ) } (reach exclusive) — the Span set (ASN-0034) named in boundary-point form via the projections start(γ), width(γ) and the displaced endpoint reach(γ) = start(γ) ⊕ width(γ); this is the convention under which adjacency (reach(α) = start(β)) shares no position.
- *Axiom:* T1 — positions are totally ordered, so any two of the four boundary points {start(α), reach(α), start(β), reach(β)} are comparable, which is what makes the case split exhaustive and the cases mutually exclusive.
- *Frame:* Classification reads only the four boundary points start(α), reach(α), start(β), reach(β); it neither modifies α, β, nor their denotations.

- *Depends:*
  - Span (Span, ASN-0034) — fixes the span type as a pair (s, ℓ), its projections start(σ) = s and width(σ) = ℓ, the displaced endpoint reach(σ) = s ⊕ ℓ, and the denotation span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ} that ⟦σ⟧ abbreviates.
  - T12 (SpanWellDefinedness, ASN-0034) — discharges reach(σ) = s ⊕ ℓ ∈ T (postcondition a), making each reach a position T1 can compare, and s ∈ span(s, ℓ), i.e. start(σ) < reach(σ) (postcondition b), grounding the non-degeneracy of well-formed spans.
  - T1 (LexicographicOrder, ASN-0034) — supplies the total order on positions whose comparability of any two boundary points makes the five-case split exhaustive and mutually exclusive