# Regional Review — ASN-0034/NAT-card (cycle 7)

*2026-04-24 02:33*

### T0 axiom and body mix ellipsis `{1, …, #a}` and comprehension `{j ∈ ℕ : 1 ≤ j ≤ #a}` for the same index set
**Class**: REVISE
**Foundation**: —
**ASN**: T0 Axiom: "component projection `·ᵢ` whose index domain for each `a ∈ T` is `{1, …, #a} ⊆ ℕ`, with `aᵢ ∈ ℕ` at each `i ∈ {1, …, #a}`." T0 body: "The component positions of `a` form the index domain `{1, …, #a} ⊆ ℕ` … `aᵢ ∈ ℕ` at each `i ∈ {1, …, #a}`." T0 body a few sentences later: "so `{j ∈ ℕ : 1 ≤ j ≤ #a}` is nonempty."
**Issue**: Within T0 two notations coexist for the index domain: the informal ellipsis `{1, …, #a}` (Axiom slot, opening prose, component-type clause) and the grounded comprehension `{j ∈ ℕ : 1 ≤ j ≤ #a}` (nonemptiness prose). The same inconsistency was flagged in NAT-card in a prior finding ("mixes ellipsis notation and set-builder comprehension"); it recurs here. The ellipsis form has no formal unfolding in T0 itself — a reader consulting only the Axiom slot cannot expand it without importing convention or cross-referencing NAT-card's Depends-slot gloss. The Axiom's "with `aᵢ ∈ ℕ` at each `i ∈ {1, …, #a}`" is the component-typing clause; if `{1, …, #a}` is to be read as `{j ∈ ℕ : 1 ≤ j ≤ #a}`, that reading should be posited, not left to the reader.
**What needs resolving**: Use a single notation for the index domain throughout T0. Comprehension form (`{j ∈ ℕ : 1 ≤ j ≤ #a}`) is what the Axiom's dependency on NAT-order's `≤` already supports and what is used later in T0's own prose; adopting it in the Axiom's index-domain and component-typing clauses removes the need for any ellipsis-unfolding convention.

VERDICT: REVISE
