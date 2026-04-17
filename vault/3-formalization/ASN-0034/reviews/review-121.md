# Cone Review — ASN-0034/D2 (cycle 2)

*2026-04-17 03:34*

### T1's proof uses uncited ℕ-facts about the successor and discreteness

**Foundation**: (foundation ASN — internal consistency; per-step ℕ-fact citation convention established by T0 and applied to sister properties like TumblerAdd, GlobalUniqueness revisions, TA-LC, and NAT-sub's consumers)

**ASN**: T1 (LexicographicOrder) is one of the properties the ASN holds to the citation convention (its Depends already itemizes T0, NAT-order, NAT-wellorder, T3), yet its proof invokes at least three distinct ℕ-facts that no Depends entry underwrites:

- Irreflexivity, Case (ii): *"Case (ii) requires `m + 1 ≤ m`, which is false."* The "is false" step is a ℕ claim that rests on the strict successor inequality `m < m + 1` (NAT-addcompat) combined with NAT-order's asymmetry; neither NAT-addcompat nor a direct successor-strictness citation appears in T1's Depends.
- Transitivity, Case `k₁ < k₂` under Case (ii) of `a < b`: *"`k₂ = n + 1 > n ≥ k₁`"* — the link `n + 1 > n` is again the strict successor inequality (NAT-addcompat), uncited.
- Transitivity, Case `k₁ = k₂ = k`, sub-case (ii, ii): *"Then `m + 1 = n + 1`, hence `m = n`. But the first condition requires `m + 1 ≤ n`, i.e., `m < n`..."* — the step `m + 1 = n + 1 ⟹ m = n` is successor injectivity (derivable from NAT-cancel applied at the fixed summand `1`), and the equivalence `m + 1 ≤ n ⟺ m < n` is NAT-discrete. T1 cites neither NAT-cancel nor NAT-discrete.

**Issue**: Sister properties apply the per-step citation convention uniformly — TumblerAdd cites NAT-addcompat explicitly for "strict successor inequality (`aₖ + 1 > aₖ`)", TA-Pos and ActionPoint cite NAT-discrete for the "nonzero ⇒ `≥ 1`" step, and the recent revisions to GlobalUniqueness and TA-LC extended Depends to cover composed ℕ steps. T1's proof uses ℕ-facts of comparable flavor (strict successor, discreteness, successor injectivity) but routes them through implicit background arithmetic. A reviser tightening NAT-addcompat, NAT-discrete, or NAT-cancel has no Depends-backed signal that T1 — the ordering property cited by almost every downstream proof — consumes those facts.

**What needs resolving**: T1's Depends must either (a) extend to cite NAT-addcompat (strict successor inequality), NAT-discrete (the `m < n ⟺ m + 1 ≤ n` equivalence), and NAT-cancel (or an equivalent successor-injectivity source) at the sites identified above, or (b) restate the three uncited inferences in terms of facts already underwritten by T1's current Depends (NAT-order's irreflexivity/trichotomy/transitivity, NAT-wellorder's least element, T3's canonical representation), making each step discharge-able from the existing citations. The current state leaves the foundational total-order property with a weaker citation trail than the properties that cite it.
