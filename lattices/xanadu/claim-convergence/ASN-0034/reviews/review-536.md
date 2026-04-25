# Regional Review — ASN-0034/TumblerAdd (cycle 1)

*2026-04-24 14:20*

Reading the ASN carefully — foundation-only, no external statements to cite against. Checking for internal consistency, precondition chains, and proof coverage.

### T0 lacks a comprehension/constructor principle for T
**Class**: REVISE
**Foundation**: T0 (CarrierSetDefinition)
**ASN**: TumblerAdd's closure argument concludes `Therefore a ⊕ w ∈ T by T0` after showing each constructed component `rᵢ ∈ ℕ` and that `p = n ≥ 1`.
**Issue**: T0's *Formal Contract* axiomatises only *projection* facts about inhabitants of T — that T is a set, that `# : T → ℕ`, the nonemptiness bound `1 ≤ #a`, the typing `aᵢ ∈ ℕ` on the index domain, and extensionality. None of these clauses say "every nonempty finite sequence of naturals is represented in T"; they only constrain what each existing `a ∈ T` looks like. The prose `T is the set of nonempty finite sequences over ℕ` carries that commitment, but the formal slot does not. TumblerAdd's membership claim depends on that commitment: it presents a freshly-described sequence `[r₁, ..., rₚ]` with `p ≥ 1` and `rᵢ ∈ ℕ` and concludes membership in T. Without a comprehension/constructor axiom in T0 — e.g., `for every p ≥ 1 and every r : {1,...,p} → ℕ, there exists t ∈ T with #t = p and tᵢ = r(i)` — the citation `by T0` is not discharged by any of T0's stated axiom clauses. Extensionality establishes at most uniqueness of such a t if it exists, not existence. The same gap would bite any downstream operation that constructs tumblers from components (TumblerSub is foreshadowed; any quoting/composition operator would hit it).
**What needs resolving**: T0 should either export a comprehension/constructor axiom characterising which sequences over ℕ inhabit T, or TumblerAdd must cite a different mechanism for discharging `a ⊕ w ∈ T` from the component-level construction.

VERDICT: REVISE

## Result

Regional review converged after 2 cycles.

*Elapsed: 1268s*
