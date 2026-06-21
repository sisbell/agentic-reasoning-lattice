# Signature Resolve — ASN-0053/SC — run 1

*2026-06-20T22:44:24Z*
*Model: sonnet*

## Output

INTRODUCES:
- bullet: "- `start` — function symbol extracting the start boundary of a span; appears in all five case conditions and the non-degeneracy precondition"
- bullet: "- `reach` — function symbol extracting the reach (exclusive upper boundary) of a span; appears in all five case conditions and the non-degeneracy precondition"
- bullet: "- `⟦·⟧` — denotation bracket: maps a span γ to the half-open position set { p : start(γ) ≤ p < reach(γ) }; explicitly defined in this claim's Definition field"
- bullet: "- `<` — strict total order relation on positions; its totality (axiom T1) makes the five-case split exhaustive and the cases mutually exclusive"
- bullet: "- `≤` — non-strict companion order on positions; used in containment-case boundary conditions and the non-degeneracy precondition"
- bullet: "- `≥` — reverse non-strict order on positions; appears in the exhaustiveness argument (reach(α) ≥ reach(β) gives case (iv))"
- bullet: "- `∩` — set intersection on position sets; used in the postcondition to characterize overlap vs. disjointness of span denotations"
- bullet: "- `∅` — the empty set; used to state disjointness (⟦α⟧ ∩ ⟦β⟧ = ∅) in cases (i) and (ii) of the postcondition"

REMOVES: []
