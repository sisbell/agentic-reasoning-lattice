# Regional Review — ASN-0034/T4 (cycle 2)

*2026-04-24 12:08*

### NAT-card's upper-bound clause is derivable from the characterisation, not independent
**Class**: OBSERVE
**Foundation**: NAT-card (NatFiniteSetCardinality)
**ASN**: NAT-card Axiom second clause: "`(A n ∈ ℕ, S : S ⊆ {j ∈ ℕ : 1 ≤ j ≤ n} :: |S| ≤ n)` — upper bound."
**Issue**: Given the first clause (strictly-increasing-function characterisation), the upper bound `|S| ≤ n` is a theorem: any strictly increasing `f : {1, …, k} → ℕ` with image `S ⊆ {1, …, n}` satisfies `f.k ≥ k` (by NAT-discrete's `m < n ⟹ m + 1 ≤ n` iterated from `f.1 ≥ 1`, together with NAT-closure for `+1`) and `f.k ∈ S ⊆ {1, …, n}`, so `k ≤ n`. Presenting `|S| ≤ n` as an axiom clause alongside the characterisation invites the reader to suspect an independent constraint where none exists. Related to the previous "NAT-card depends on T0 only for a disambiguation aside" pattern — axiom clauses accreting beyond what the operator's definition requires.

### T4-valid is the predicate of the Consequence but is never explicitly introduced
**Class**: OBSERVE
**ASN**: T4. Body: "Every tumbler `t ∈ T` used as an address satisfies: `zeros(t) ≤ 3`; …". Axiom: "Valid address tumblers satisfy: …". Consequence: "`zeros(t) ∈ {0, 1, 2, 3}` for every T4-valid tumbler `t`". Preconditions: "`t ∈ T`".
**Issue**: The Consequence quantifies over "T4-valid tumbler", a class never named in a Definition slot. The Axiom phrases the four conditions as a "satisfies:" clause on an informal category ("valid address tumblers", "used as an address"), relying on the reader to read this as an implicit definition of T4-validity. Preconditions restrict only to `t ∈ T`, so they do not carry the validity predicate downstream. T4a/T4b/T4c (cited as building on T4) will need to invoke "T4-valid" and there is no single formal clause to cite.

### "Field separator" definition lives in the Axiom slot, not the Definition slot
**Class**: OBSERVE
**ASN**: T4 Axiom: "…`t_{#t} ≠ 0`. T4 stipulates that a position `i` of `t` is a *field separator* iff `tᵢ = 0`."
**Issue**: A definitional stipulation sits in the Axiom slot alongside the four primitive constraints. Definition slot currently contains only `zeros(t) = |…|`. The terms "field separator", "field component", and "field segment" (the last defined in body prose as "the maximal contiguous sub-sequences of non-zero positions") are used by the Axiom's schema and by the downstream T4a/T4b/T4c claims, so they need a formal home. Slot hygiene: definitions belong in Definition.

### Per-k canonical-form schema presupposes Exhaustion it later Consequences
**Class**: OBSERVE
**ASN**: T4 Axiom: "for each `k ∈ ℕ` with `0 ≤ k ≤ 3` at which `zeros(t) = k`, the form is …"; Consequence: "`zeros(t) ∈ {0, 1, 2, 3}` … so the Axiom's per-`k` schema collectively covers every T4-valid tumbler."
**Issue**: The Axiom's schema is only stated for `k ∈ {0, 1, 2, 3}`. The Consequence's role is to justify that this enumeration exhausts the cases — i.e., the schema's "collectively covers" claim is post hoc. This is not unsound (the schema is phrased as "for each `k` at which `zeros(t) = k`", so it is vacuous at other `k`), but reading order is: Axiom asserts schema over `{0,…,3}`, Consequence proves no other `k` arises. A precise reader expects the covered domain to be a bound from a prior foundation rather than a target the Consequence has to hit. Compounds with prior finding #3 (schema is derivable from field-segment constraint).

VERDICT: OBSERVE

## Result

Regional review converged after 2 cycles.

*Elapsed: 577s*
