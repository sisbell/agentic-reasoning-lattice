# Cone Review — ASN-0034/TumblerAdd (cycle 4)

*2026-04-16 19:54*

### T0's ℕ-ordering axioms are not enumerated, and T1's proof invokes trichotomy/irreflexivity/transitivity of `<` on ℕ without citation
**Foundation**: T0 (CarrierSetDefinition) — `Axiom` field enumerates only "closure under successor and addition, and discreteness" as properties of ℕ.
**ASN**: T1 (LexicographicOrder), proof of strict total order, which appeals to three ℕ-ordering facts:
- Irreflexivity: "Case (i) requires `aₖ < aₖ`, violating irreflexivity of `<` on ℕ."
- Trichotomy: "By trichotomy on ℕ, exactly one of `aₖ < bₖ` or `bₖ < aₖ` holds."
- Transitivity: "Transitivity of `<` on ℕ gives `aₖ < cₖ`."

T1's `Depends` list cites T0 only for length `#a` and component projection `aₖ`: "T0 (CarrierSetDefinition) — the definition and proof use length `#a` and component projection `aₖ` for `a ∈ T`, which T0 introduces." The ℕ-ordering properties that the proof invokes are not cited to any source.
**Issue**: T0's axiom explicitly lists "closure under successor and addition, and discreteness" as properties of ℕ, while the relation `<` on ℕ appears in T0 only incidentally, inside the statement of discreteness (`m ≤ n < m + 1 ⟹ n = m`). The phrasing "taken with their standard properties, including closure under successor and addition, and discreteness" is ambiguous — "including" could be read as enumerating *all* the properties admitted, or as highlighting a subset of many. A Lamport-style formalizer building the axiom set for T has no basis in T0's `Axiom` field to admit strict-order irreflexivity, trichotomy, or transitivity of `<` on ℕ. T1's own `Depends` acknowledges the gap by citing T0 for length and projection but not for any ℕ-ordering property, and the proofs apply these properties without any other source in scope. The same pattern would affect any future property that reasons about component-level ordering.
**What needs resolving**: Either (i) amend T0's `Axiom` field to enumerate the ℕ-ordering properties that downstream proofs rely on (strict-order irreflexivity, trichotomy, transitivity, and the implicit definability of `≤`/`<` used in the discreteness formula), and update T1's `Depends` citation of T0 to name them; or (ii) restructure so that ℕ's ordered-semiring structure is introduced as a named background axiom that every proof invoking ℕ-ordering cites explicitly.
