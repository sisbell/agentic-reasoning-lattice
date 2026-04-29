# Regional Review — ASN-0034/T4c (cycle 1)

*2026-04-24 07:46*

### Depends slots carry use-site inventory rather than dependency declarations
**Class**: OBSERVE
**Foundation**: n/a (structural)
**ASN**: NAT-sub, NAT-addbound, T4, T4a, T4b, T4c — Depends entries run multi-sentence with heavy narration of where and how each dependency fires. E.g., NAT-sub's entry for NAT-order: "supplies the strict order `<` and its companions... used in the signature's domain condition... and in the antecedents... of the conditional-closure and inverse-characterisation clauses; supplies the at-least-one trichotomy axiom and irreflexivity axiom, together with two conjuncts of the exactly-one-trichotomy Consequence..."
**Issue**: Use-site inventory and derivation narration in the Depends slot. The reader must skip past prose to find what is depended on. A Depends entry should name the dependency and the symbols/clauses imported, not re-narrate the proof.

### T4 Axiom slot contains derived canonical form
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: T4 — "The canonical written form of a T4-valid address tumbler is given by the following schema, quantified per-`k`..." and the positivity rider "In every case, `0 < Nᵢ, 0 < Uⱼ, 0 < Dₖ, 0 < Eₗ` at every position present."
**Issue**: The per-`k` schema is a representation consequence of (zeros(t) ≤ 3, no-adjacent-zeros, boundary-nonzero, separator definition). The positivity rider follows from NAT-zero + tᵢ ≠ 0 at non-separator positions. These belong in a Consequence, not the Axiom.

### T4c treats definitional biconditionals as postconditions
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: T4c — no Definition or Axiom slot; the four label biconditionals (`zeros(t) = 0 ↔ node address`, etc.) appear only in Postconditions.
**Issue**: The four labels are introduced by definition ("T4c defines four hierarchical level labels by zero count"), not established as theorems. A pure definition should sit in a Definition slot; Postconditions are for what the claim *proves*. The exhaustion and injectivity argument is the real content and should be the Consequence.

### NAT-sub conditional closure redundant with signature
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: NAT-sub — Axiom: `− : {(m, n) ∈ ℕ × ℕ : m ≥ n} → ℕ` ... `(A m, n ∈ ℕ : m ≥ n : m − n ∈ ℕ)` (conditional closure).
**Issue**: Declaring the signature with codomain ℕ and guarded domain already commits to `m − n ∈ ℕ` whenever `m ≥ n`. Stating conditional closure as a separate axiom clause duplicates the signature's content.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 684s*
